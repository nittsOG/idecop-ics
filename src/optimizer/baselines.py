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
        current = score(x, paths, criticality, detectability_risk, weights).f_score
        for l in remaining:
            gain = score(x | {l}, paths, criticality, detectability_risk, weights).f_score - current
            if gain > best_gain:
                best_gain, best_l = gain, l
        if best_l is None:
            break
        x.add(best_l)
        remaining.discard(best_l)
    return x, score(x, paths, criticality, detectability_risk, weights)


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
        results.append(score(x, paths, criticality, detectability_risk, weights))
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
    return x, score(x, paths, criticality, detectability_risk, weights)
