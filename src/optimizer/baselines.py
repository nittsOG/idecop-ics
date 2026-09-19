"""
Three of the four methods from 02-optimization-formulation.md — greedy
(§2), random (§4), centrality (§5). MILP (§3) is in milp.py, separate
since it needs OR-Tools and the linearization the doc discusses at length.
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
    """Distorted Greedy — Harshaw, Feldman, Ward & Karbasi, ICML 2019, Algorithm 1.

    WHY THIS EXISTS (A27). Our objective has the exact form the paper addresses:

        F(x) = g(x) - c(x)
        g(x) = alpha*Coverage + beta*Early + gamma*CritProt   monotone submodular, non-negative
        c(x) = delta*Risk     + epsilon*Cost                  modular, non-negative

    Both properties are verified empirically in scripts/structure_check.py, not
    assumed. For this class of objective the paper proves (Theorem 3):

        g(R) - c(R) >= (1 - e^-1) * g(OPT) - c(OPT)

    using O(nk) evaluations of g, with gamma = 1 because our g is genuinely
    submodular rather than merely weakly submodular.

    PLAIN GREEDY HAS NO SUCH GUARANTEE. The same paper's Appendix A constructs
    an instance on which plain greedy's competitive ratio is O(1/k) — that is,
    arbitrarily bad. The failure mode is a "bad element" with the highest
    immediate gain g(e) - c_e, which once taken drives every remaining marginal
    gain below its cost, so greedy halts early. Our own testbed shows exactly
    this shape of behaviour at delta=3, so it is not a hypothetical risk here.

    HOW IT AVOIDS THAT. The distortion factor (1 - 1/k)^(k-(i+1)) starts small
    and rises to 1 over the run, so early iterations weight cost heavily and
    later ones weight gain. An element is taken only if it improves the
    *distorted* objective, which prevents an early high-gain/high-cost pick from
    foreclosing better cost-efficient ones later.

    Sviridenko, Vondrak & Ward (Math. Oper. Res. 42(4), 2017) proved a comparable
    bound first, but their algorithm needs continuous optimisation of the
    multilinear extension and is impractical. Harshaw et al.'s is combinatorial
    and, as visible below, short.
    """
    alpha, beta, gamma_w, delta, epsilon = weights
    k = max(1, min(budget, len(candidates)))

    def g_of(S: set[int]) -> float:
        m = score(S, paths, criticality, detectability_risk, weights, budget)
        return alpha * m.coverage + beta * m.early + gamma_w * m.crit_prot

    def c_of_element(l: int) -> float:
        # modular, so the cost of an element is independent of the set
        return (delta * detectability_risk.get(l, 0.0) + epsilon) / budget

    S: set[int] = set()
    g_S = g_of(S)
    for i in range(k):
        distortion = (1.0 - 1.0 / k) ** (k - (i + 1))
        best_e, best_val, best_g = None, 0.0, g_S
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
