"""
Four of the five methods from 02-optimization-formulation.md — greedy
(§2), random (§4), centrality (§5), and distorted greedy (the guaranteed
method adopted in D23; see formal-problem-definition.md §7(iii)). MILP (§3)
is in milp.py, separate since it needs OR-Tools and the linearization the doc
discusses at length.
"""
import random as _random

from .metrics import score


def greedy(candidates: list[int], paths: list[dict], criticality: dict,
           detectability_risk: dict, budget: int, weights=(1.0, 1.0, 1.0, 1.0, 0.1)) -> tuple[set[int], object]:
    """§2's exact algorithm: at each step, add whichever remaining candidate
    gives the best marginal F(x) gain; stop early if nothing improves."""
    x: set[int] = set()
    remaining = set(candidates)
    while len(x) < budget and remaining:
        best_l, best_gain = None, 0.0
        current = score(x, paths, criticality, detectability_risk, weights, budget).f_score
        for l in remaining:
            gain = score(x | {l}, paths, criticality, detectability_risk, weights, budget).f_score - current
            if gain > best_gain:
                best_gain, best_l = gain, l
        if best_l is None:
            break
        x.add(best_l)
        remaining.discard(best_l)
    return x, score(x, paths, criticality, detectability_risk, weights, budget)


def random_baseline(candidates: list[int], paths: list[dict], criticality: dict,
                    detectability_risk: dict, budget: int, weights=(1.0, 1.0, 1.0, 1.0, 0.1),
                    trials: int = 30, seed: int = 42) -> tuple[list[set[int]], list, object]:
    """§4: R=30 trials, not one draw — returns every trial plus the mean/std
    summary, since a single random placement isn't a fair comparator."""
    rng = _random.Random(seed)
    placements, results = [], []
    k = min(budget, len(candidates))
    for _ in range(trials):
        x = set(rng.sample(candidates, k))
        placements.append(x)
        results.append(score(x, paths, criticality, detectability_risk, weights, budget))
    mean_f = sum(r.f_score for r in results) / trials
    variance = sum((r.f_score - mean_f) ** 2 for r in results) / trials
    return placements, results, {"mean_f": mean_f, "std_f": variance ** 0.5}


def centrality_baseline(candidates: list[int], central_scores: dict[int, float],
                        paths: list[dict], criticality: dict, detectability_risk: dict,
                        budget: int, weights=(1.0, 1.0, 1.0, 1.0, 0.1)) -> tuple[set[int], object]:
    """§5: deterministic, top-B candidates by Central(v), betweenness by
    default per D4 — no repetition needed."""
    ranked = sorted(candidates, key=lambda l: central_scores.get(l, 0.0), reverse=True)
    x = set(ranked[:budget])
    return x, score(x, paths, criticality, detectability_risk, weights, budget)


def distorted_greedy(candidates: list[int], paths: list[dict], criticality: dict,
                     detectability_risk: dict, budget: int,
                     weights=(1.0, 1.0, 1.0, 1.0, 0.1)) -> tuple[set[int], object]:
    """Distorted Greedy — Harshaw, Feldman, Ward & Karbasi (2019).

    SOURCE, verified from primary text (sources.md #353):
        Chris Harshaw, Moran Feldman, Justin Ward, Amin Karbasi.
        "Submodular Maximization beyond Non-negativity: Guarantees, Fast
        Algorithms, and Applications." Proceedings of the 36th International
        Conference on Machine Learning, PMLR vol. 97, pp. 2634-2643, 2019.

    WHY THIS EXISTS (closes A27). Our objective has the exact form the paper
    addresses — f = g - c, with g monotone, non-negative and gamma-weakly
    submodular, and c non-negative modular:

        F(x) = g(x) - c(x)
        g(x) = alpha*Coverage + beta*Early + gamma*CritProt   monotone submodular, non-negative
        c(x) = delta*Risk     + epsilon*Cost                  modular, non-negative

    Both preconditions are verified empirically on this instance by
    scripts/structure_check.py, which tests the AGGREGATE g and c directly (not
    merely the components) and tests c for modularity, not just submodularity.
    Nothing here is assumed. For this class of objective Distorted Greedy
    returns a set S with

        g(S) - c(S) >= (1 - e^-gamma) * g(OPT) - c(OPT)

    using O(nk) evaluations of g. We take gamma = 1 because our g is genuinely
    submodular rather than merely weakly submodular, giving (1 - 1/e) ~ 0.632.
    The bound for Distorted Greedy is deterministic; the paper's *stochastic*
    variants carry the analogous bound in expectation, with an extra -epsilon
    term. This implementation is the deterministic one.

    The paper also proves a matching HARDNESS result: no polynomial-time
    algorithm accessing g through a value oracle can do better than
    (1 - e^-gamma). So this is not merely a bound we happen to have — it is the
    best obtainable under value-oracle access, which is the access model we have.

    PLAIN GREEDY HAS NO SUCH GUARANTEE. The same paper's Appendix A, titled
    "Greedy Performs Arbitrarily Poorly", constructs an instance on which
    standard greedy's ratio is unbounded. The failure mode is a "bad element"
    with the highest immediate gain g(e) - c_e, which once taken drives every
    remaining marginal gain below its cost, so greedy halts early. Our own
    testbed shows this shape of behaviour at delta=3, so it is not hypothetical
    here. NOTE ON CONFIDENCE: the unbounded-ratio claim and the appendix title
    are verified; an earlier version of this docstring asserted a specific
    O(1/k) rate and a theorem number ("Theorem 3"), neither of which the primary
    text confirmed. Both were removed rather than restated more cautiously. The
    result is cited by content, not by number. See D23.

    HOW IT AVOIDS THAT. The distortion factor (1 - gamma/k)^(k-(i+1)) starts
    small — approximately e^-1 at i=0 — and rises to exactly 1 at the final
    iteration, so early iterations weight cost heavily relative to gain and
    later ones weight gain fully. An element is taken only if it improves the
    *distorted* objective, which stops an early high-gain/high-cost pick from
    foreclosing better cost-efficient ones later.

    ROUTE NOT TAKEN. Sviridenko, Vondrak & Ward proved a comparable bound
    earlier, and formal-problem-definition.md §7(i) originally named it as the
    route to a guarantee. It is not usable here: their algorithm requires
    continuous optimisation of the multilinear extension, which is impractical
    at any scale and disproportionate at this one. Harshaw et al.'s algorithm is
    combinatorial and, as visible below, short. §7 records this.

    MEASURED BEHAVIOUR ON THIS TESTBED, AND A WARNING AGAINST "FIXING" IT.
    Distorted greedy is *beaten by plain greedy* in 2 of the 20 cells of the
    comparison grid (scripts/sweep.py) — 34.2% below the exhaustive optimum at
    B=2 under default weights, and 11.4% at B=4 under delta=3 — while plain
    greedy attains the exact optimum in all 20. This is correct behaviour, not a
    defect. Each of the k iterations applies
    its own acceptance test, and an iteration that declines is NOT retried, so
    when the early distortion factor pushes every candidate's distorted value
    below zero the algorithm permanently forfeits that slot. At B=2 the i=0
    distortion of 0.5 halves every gain, nothing is accepted, and only one decoy
    is placed against a budget of two.

    Do NOT "fix" this by looping until the budget is filled, by relaxing the
    acceptance test, or by restarting declined iterations. The per-iteration
    accept/decline structure is what the proof rests on; removing it removes the
    guarantee and leaves an algorithm that is neither plain greedy nor a
    guaranteed one. The conservatism is the price of the worst-case floor.

    Consequently plain `greedy` above remains the PRIMARY reported method, and
    this function is reported alongside it as the only method carrying a
    worst-case guarantee — which is what the scalability argument needs, where
    MILP validation is unavailable. It is not claimed to be the better performer
    on this instance, because it measurably is not. See D23.
    """
    alpha, beta, gamma_w, delta, epsilon = weights
    k = max(1, min(budget, len(candidates)))
    # Weak-submodularity parameter from the source's Algorithm 1. Held at 1.0
    # because structure_check.py verifies g is genuinely submodular on this
    # instance; written explicitly rather than folded into the expression so the
    # code reads against the paper's (1 - gamma/k)^(k-(i+1)) without translation.
    GAMMA = 1.0

    def g_of(S: set[int]) -> float:
        m = score(S, paths, criticality, detectability_risk, weights, budget)
        return alpha * m.coverage + beta * m.early + gamma_w * m.crit_prot

    def c_of_element(l: int) -> float:
        # modular, so the cost of an element is independent of the set
        return (delta * detectability_risk.get(l, 0.0) + epsilon) / budget

    S: set[int] = set()
    g_S = g_of(S)
    for i in range(k):
        distortion = (1.0 - GAMMA / k) ** (k - (i + 1))
        best_e, best_val, best_g = None, 0.0, g_S
        # The paper's argmax ranges over the whole ground set. Elements already
        # in S are skipped here: g is monotone submodular so their marginal gain
        # is 0, leaving value -c_e < 0, which can never win the argmax against
        # the empty-selection floor and would be rejected by the acceptance test
        # regardless. Same output, fewer evaluations.
        for e in candidates:
            if e in S:
                continue
            g_new = g_of(S | {e})
            val = distortion * (g_new - g_S) - c_of_element(e)
            if best_e is None or val > best_val:
                best_e, best_val, best_g = e, val, g_new
        # accept only on strictly positive contribution to the DISTORTED objective
        if best_e is not None and best_val > 0:
            S.add(best_e)
            g_S = best_g

    return S, score(S, paths, criticality, detectability_risk, weights, budget)
