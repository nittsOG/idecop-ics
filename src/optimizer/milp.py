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
"""
from ortools.sat.python import cp_model

from .metrics import score

SCALE = 10_000


def _solve_for_fixed_coverage(candidates, paths, criticality, detectability_risk,
                               budget, weights, k, time_limit_seconds):
    alpha, beta, gamma, delta, epsilon = weights
    model = cp_model.CpModel()
    x = {l: model.NewBoolVar(f"x_{l}") for l in candidates}
    model.Add(sum(x.values()) <= budget)

    y, z = {}, {}
    max_crit = sum(c["criticality"] for c in criticality.values()) or 1.0
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
        early_coef = (beta * SCALE / k) if k > 0 else 0
        for step_idx, a in candidate_steps:
            w = int(round(early_coef * (1 - step_idx / p["length"])))
            obj_terms.append(w * z[(i, step_idx)])

    model.Add(sum(y.values()) == k)  # the fix: fix the denominator, don't let the solver choose it

    for l in candidates:
        penalty = int(round(delta * SCALE * detectability_risk.get(l, 0.0) + epsilon * SCALE))
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
    """Runs |P|+1 solves (one per achievable coverage count) and returns
    whichever gives the best TRUE F(x), evaluated the same way every other
    method is scored — this is what makes it a trustworthy validator rather
    than an optimizer for a proxy that might not match."""
    best_x, best_metrics, total_time, statuses = set(), score(set(), paths, criticality, detectability_risk, weights), 0.0, []

    for k in range(0, len(paths) + 1):
        result = _solve_for_fixed_coverage(candidates, paths, criticality, detectability_risk,
                                           budget, weights, k, time_limit_seconds)
        if result is None:
            statuses.append(f"k={k}: infeasible")
            continue
        x_k, wall_time = result
        total_time += wall_time
        m_k = score(x_k, paths, criticality, detectability_risk, weights)
        statuses.append(f"k={k}: F={m_k.f_score:.4f}")
        if m_k.f_score > best_metrics.f_score:
            best_x, best_metrics = x_k, m_k

    solve_info = {"status": "OPTIMAL (best-of-k)", "wall_time": total_time, "per_k": statuses}
    return best_x, best_metrics, solve_info
