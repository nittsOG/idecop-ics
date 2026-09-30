"""
metrics — F(x) and its five components, formal-problem-definition.md §5.
Shared by every method (greedy, MILP, random, centrality) so all four are
scored identically, per 02-optimization-formulation.md §3's note that this
is what actually keeps a MILP result and a greedy result comparable.
"""
from dataclasses import dataclass

# D25: Risk and Cost are divided by this FIXED constant, never by the budget B.
#
# Why not B (D20-D24 divided by B). B is a procurement cap — how many decoys
# the site will deploy — and the adversary never observes it; detection risk
# and operating burden come from the decoys actually deployed. Dividing by B
# made the same decoy worth a different amount at different budgets: on the
# frozen instance, DMZ Jump Host alone scored -0.063 at B=1 and +0.332 at
# B=2, and under delta=3 greedy placed 0, 0, 1 and 4 decoys at B=1..4. It also
# contradicted 02-optimization-formulation.md §2, which stops greedy early so
# the evaluation can report "the method found K decoys sufficient".
#
# Why not |P| or |L|. Dividing by |P| halves every decoy's penalty when the
# same threat is written with every path twice (the DMZ Jump Host alone goes
# from 0.529 to 0.628); dividing by |L| makes every decoy cheaper when an
# unused candidate is added. Both were tested (D25).
#
# What K is. Not a physical quantity: dividing by K is the same as scaling
# delta and epsilon by 1/K, so K fixes the units in which those weights are
# read. Why 4: when D25 chose it, 4 was the smallest constant that kept Risk
# and Cost in [0,1] for every budget of the declared comparison grid (D20's
# boundedness reason with the budget taken out). It is FROZEN from here, and
# it is not re-derived if a grid changes: re-deriving it would move the budget
# confound from the run to the grid. Changing it is an objective change and
# needs its own decisions-log entry. For budgets above K, Risk and Cost can
# exceed 1, which is harmless; modularity is the load-bearing property (D20;
# a precondition of distorted greedy, D23), and any constant keeps it. A
# different instance family (e.g. synthetic instances under A12) must fix its
# own constant before its first run, never from the budget of a run.
NORMALISER_K = 4


@dataclass
class Metrics:
    coverage: float
    early: float
    crit_prot: float
    risk: float
    cost: float
    f_score: float
    mean_stage_earliness: float = 0.0   # reported, not optimized. See D20.
    raw_decoy_count: int = 0            # cost before the /NORMALISER_K normalization


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

    There is deliberately no budget parameter (D25): the budget constrains how
    many decoys a method may place, and never changes what a placement is worth.

    Default epsilon is smaller than the other four. Before D20 Cost was a raw
    decoy count, and equal weights would have let it dominate. It has been
    normalised since then, and 0.1 is kept as a light, uniform per-decoy
    charge, so that the detectability trade-off is carried mainly by delta.
    This default isn't a claimed 'correct' weighting — it's what makes the
    sensitivity sweep in formal-problem-definition.md §5 meaningful to run at
    all; the sweep itself is what actually justifies a final choice, not this
    default."""
    alpha, beta, gamma, delta, epsilon = weights
    n_paths = len(paths)
    hits = _intercepted_paths(x, paths)

    coverage = len(hits) / n_paths if n_paths else 0.0

    # Early: denominator is |P|, NOT |intercepted|. See D20. Dividing by the
    # number of intercepted paths makes this a MEAN, which is non-monotone —
    # adding a late-intercepting decoy lowers it, verified by exhaustive
    # enumeration in scripts/structure_check.py (30 monotonicity violations,
    # 57 submodularity violations on the frozen four-path instance; the 16/18
    # once recorded here were the three-path instance's, stale since D21 added
    # P4 -- see D24). A fixed |P| denominator is monotone and
    # submodular. Mean earliness is still reported separately as
    # `mean_stage_earliness` because it is the interpretable statistic.
    early = sum(1 - (stage / p["length"]) for i, stage in hits.items() for p in [paths[i]]) / n_paths if n_paths else 0.0
    mean_stage_earliness = (
        sum(1 - (stage / p["length"]) for i, stage in hits.items() for p in [paths[i]]) / len(hits)
        if hits else 0.0
    )

    # CritProt: normalized by the criticality of PATH TARGETS, not of every
    # asset in the graph. The old denominator capped this term near 0.30 even
    # at full coverage, so gamma=1 was silently gamma≈0.3. See D20.
    if hits:
        crit_prot_raw = sum(criticality[paths[i]["asset_sequence"][-1]]["criticality"] for i in hits)
        target_total = sum(criticality[p["asset_sequence"][-1]]["criticality"] for p in paths) or 1.0
        crit_prot = crit_prot_raw / target_total
    else:
        crit_prot = 0.0

    # Risk and Cost: divided by the fixed NORMALISER_K (D25; D20-D24 divided by
    # the budget). Both stay MODULAR, which matters — a union-probability form
    # of Risk would be submodular, and subtracting a submodular function would
    # break the submodularity that D20 restores. See formal-problem-definition
    # §5: Risk is normalized detectability exposure, not a probability.
    # D25 also removed a fallback that divided by len(x) when no budget was
    # passed: that is a MEAN, non-modular (D20's Early defect again), and it
    # made Cost 1.0 for every non-empty placement. No caller reached it.
    risk = sum(detectability_risk.get(l, 0.0) for l in x) / NORMALISER_K
    cost = len(x) / NORMALISER_K
    f_score = alpha * coverage + beta * early + gamma * crit_prot - delta * risk - epsilon * cost

    return Metrics(coverage, early, crit_prot, risk, cost, f_score, mean_stage_earliness,
                   raw_decoy_count=len(x))
