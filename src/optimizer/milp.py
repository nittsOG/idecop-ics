"""
milp — the validation method, per 02-optimization-formulation.md §3.

The first version of this file implemented that section's "Option 2"
(unnormalized Early proxy inside the solver, real metric computed after) —
and running it against greedy exposed a real flaw in that approach, not a
coding bug: the proxy and the true F(x) can *disagree* on which placement
is better, because summing per-path early-contributions without normalizing
by how many paths got covered systematically over-rewards covering more
paths at the cost of true early-detection quality. On this project's own
5-candidate test case, the proxy-optimal placement scored *worse* on the
real, normalized F(x) than greedy's result — which should be logically
impossible for a method whose entire purpose is validating greedy's
optimality gap.

Rebuilt using §3's Option 1 instead: since |P| is small (3 in this
project's testbed), solve once per possible coverage count k = 0..|P|,
fixing sum(y_i) = k so the Early normalization (1/k) is a known constant,
not a solver variable — then take the best result across all k. This is
still exact, just run |P|+1 times instead of once.

(History. D20 made the k-enumeration unnecessary: with Early divided by a
fixed |P| the objective linearises directly, and `solve_milp` below is a
single exact solve. The two paragraphs above record why the file looks the
way it does; they no longer describe what it runs.)
"""
from ortools.sat.python import cp_model

from .metrics import score, NORMALISER_K

# D24: raised from 10_000. CP-SAT needs integer coefficients, so every term is
# rounded, and each rounding can shift a placement's objective by up to half a
# unit. At 10_000 the MILP was still exact on every configuration tested, but by
# thin margins: the gap between the optimum and the best strictly-worse placement
# was only 34 integer units on the documented grid (B=3, delta=3; true-F gap
# 0.0034) and 8 units on a delta-only check grid (B=3, delta=0.5; gap 0.00084).
# At 1_000_000 those margins become 3,356 and 837. No placement or F-value
# changes on any configuration tested. The margin matters beyond this testbed:
# the exhaustive-enumeration cross-check in scripts/sweep.py exists only while
# |L| is small, so on a larger instance rounding error would go unchecked.
#
# D25 re-measured after Risk and Cost moved to the fixed NORMALISER_K: the
# smallest margin is 3,826 units on the declared grid (B=4, delta=3) and 413
# across the 68 distinct configurations of `sweep.py --sens`, which include the
# declared 20 (B=3, delta=0.75). One placement's objective sums at most
# 3|P| + B rounded terms, each off by at most half a unit, so rounding can move
# the comparison of two placements by at most 3|P| + B units -- 16 on the
# declared grid, 17 at the sample's B=5: far inside both margins. The MILP
# matched exhaustive enumeration in all 68. sweep.py now computes the margins
# and raises if one falls within the rounding bound.
SCALE = 1_000_000


def _solve_for_fixed_coverage(candidates, paths, criticality, detectability_risk,
                               budget, weights, k, time_limit_seconds):
    alpha, beta, gamma, delta, epsilon = weights
    model = cp_model.CpModel()
    x = {l: model.NewBoolVar(f"x_{l}") for l in candidates}
    model.Add(sum(x.values()) <= budget)

    y, z = {}, {}
    max_crit = sum(criticality[p["asset_sequence"][-1]]["criticality"] for p in paths) or 1.0  # D20
    obj_terms = []

    for i, p in enumerate(paths):
        seq = p["asset_sequence"]
        candidate_steps = [(s, a) for s, a in enumerate(seq) if a in x]
        yi = model.NewBoolVar(f"y_{i}")
        y[i] = yi
        if not candidate_steps:
            model.Add(yi == 0)
            continue
        model.Add(yi <= sum(x[a] for _, a in candidate_steps))
        for _, a in candidate_steps:
            model.Add(yi >= x[a])

        prior_z = []
        for step_idx, a in candidate_steps:
            zi = model.NewBoolVar(f"z_{i}_{step_idx}")
            z[(i, step_idx)] = zi
            model.Add(zi <= x[a])
            if prior_z:
                model.Add(zi + sum(prior_z) <= 1)
            prior_z.append(zi)
        model.Add(sum(z[(i, s)] for s, _ in candidate_steps) == yi)

        target_crit = criticality[seq[-1]]["criticality"]
        obj_terms.append(int(round(alpha * SCALE / len(paths))) * yi)
        obj_terms.append(int(round(gamma * SCALE * target_crit / max_crit)) * yi)
        # Early is now correctly normalized by the FIXED k, not a variable.
        early_coef = beta * SCALE / len(paths)   # D20: fixed |P|, never k
        for step_idx, a in candidate_steps:
            # D24: stage is 1-BASED, matching metrics._intercepted_paths, which
            # records `step_idx + 1`. This term previously used the raw 0-based
            # step_idx, over-valuing every interception by exactly 1/length and
            # making the solver maximise a different function from the one
            # metrics.score reports — so the "exact" validator returned
            # placements that scored BELOW greedy on the true objective. Same
            # class of defect as D16, in a different place. See D24.
            w = int(round(early_coef * (1 - (step_idx + 1) / p["length"])))
            obj_terms.append(w * z[(i, step_idx)])

    if k is not None:
        model.Add(sum(y.values()) == k)

    # D25: Risk and Cost are divided by the fixed NORMALISER_K, exactly as in
    # metrics.score. D20-D24 divided by the budget here; the budget now enters
    # only as the cardinality constraint above.
    for l in candidates:
        penalty = int(round((delta * SCALE * detectability_risk.get(l, 0.0) + epsilon * SCALE) / NORMALISER_K))
        obj_terms.append(-penalty * x[l])

    model.Maximize(sum(obj_terms))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    x_star = {l for l in candidates if solver.Value(x[l]) == 1}
    return x_star, solver.WallTime()


def solve_milp(candidates: list[int], paths: list[dict], criticality: dict,
               detectability_risk: dict, budget: int,
               weights: tuple[float, float, float, float, float] = (1.0, 1.0, 1.0, 1.0, 0.1),
               time_limit_seconds: float = 10.0) -> tuple[set[int], object, dict]:
    """SINGLE exact solve. D20 removed the |P|+1 enumeration: once Early(x) is
    normalized by a FIXED |P| rather than by the variable count of intercepted
    paths, the early coefficient is constant and the objective linearizes
    directly. The k-enumeration existed only to work around the variable
    denominator described in D16 — with the denominator fixed, the workaround
    is unnecessary. Kept as a comment rather than deleted silently because the
    reason it existed is methodologically useful."""
    result = _solve_for_fixed_coverage(candidates, paths, criticality, detectability_risk,
                                       budget, weights, None, time_limit_seconds)
    if result is None:
        empty = score(set(), paths, criticality, detectability_risk, weights)
        return set(), empty, {"status": "INFEASIBLE", "wall_time": 0.0, "solves": 1}
    x_star, wall_time = result
    metrics = score(x_star, paths, criticality, detectability_risk, weights)
    return x_star, metrics, {"status": "OPTIMAL", "wall_time": wall_time, "solves": 1}
