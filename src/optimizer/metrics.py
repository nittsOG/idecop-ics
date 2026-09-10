"""
metrics — F(x) and its five components, formal-problem-definition.md §5.
Shared by every method (greedy, MILP, random, centrality) so all four are
scored identically, per 02-optimization-formulation.md §3's note that this
is what actually keeps a MILP result and a greedy result comparable.
"""
from dataclasses import dataclass


@dataclass
class Metrics:
    coverage: float
    early: float
    crit_prot: float
    risk: float
    cost: float
    f_score: float


def _intercepted_paths(x: set[int], paths: list[dict]) -> dict[int, int]:
    """For each path index that x intercepts, the earliest step_order (1-based
    position in asset_sequence) where a placed decoy appears. Paths not
    intercepted are absent from the returned dict."""
    hits = {}
    for i, p in enumerate(paths):
        for step_idx, asset_id in enumerate(p["asset_sequence"]):
            if asset_id in x:
                hits[i] = step_idx + 1  # 1-based stage
                break
    return hits


def score(x: set[int], paths: list[dict], criticality: dict[int, dict],
          detectability_risk: dict[int, float],
          weights: tuple[float, float, float, float, float] = (1.0, 1.0, 1.0, 1.0, 0.1)) -> Metrics:
    """weights = (alpha, beta, gamma, delta, epsilon), formal-problem-definition.md §5.
    Default epsilon is deliberately smaller than the other four: coverage,
    early, crit_prot, and risk are all 0-1 normalized, but cost is a raw
    decoy count — equal weights would let cost dominate and make the
    optimizer always prefer zero decoys. This default isn't a claimed
    'correct' weighting — it's what makes the sensitivity sweep in
    formal-problem-definition.md §5 meaningful to run at all; the sweep
    itself is what actually justifies a final choice, not this default."""
    alpha, beta, gamma, delta, epsilon = weights
    n_paths = len(paths)
    hits = _intercepted_paths(x, paths)

    coverage = len(hits) / n_paths if n_paths else 0.0

    if hits:
        early = sum(1 - (stage / p["length"]) for i, stage in hits.items() for p in [paths[i]]) / len(hits)
    else:
        early = 0.0

    if hits:
        crit_prot_raw = sum(criticality[paths[i]["asset_sequence"][-1]]["criticality"] for i in hits)
        max_possible = sum(c["criticality"] for c in criticality.values()) or 1.0
        crit_prot = crit_prot_raw / max_possible
    else:
        crit_prot = 0.0

    risk = sum(detectability_risk.get(l, 0.0) for l in x)
    cost = len(x)
    f_score = alpha * coverage + beta * early + gamma * crit_prot - delta * risk - epsilon * cost

    return Metrics(coverage, early, crit_prot, risk, cost, f_score)
