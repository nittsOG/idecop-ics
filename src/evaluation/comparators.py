"""
The coverage-only comparator (A12; D37; docs/03-evaluation-methodology.md §4).

It asks whether F's five terms add anything over plain attack-path blocking,
the kind of objective CN 121356815 A optimises: an attack-path blocking ratio
under a count cap (D36 item 6). It maximises Coverage alone, with Early,
CritProt, Risk and Cost switched off. Two forms are computed:

- the coverage-only greedy: the frozen greedy (src/optimizer/baselines.py)
  with weights (1, 0, 0, 0, 0). The code is unchanged, so the comparison
  isolates the objective. With Risk and Cost off it stops when no candidate
  catches a new path, and between candidates of equal gain it keeps the first
  one it scans, which is arbitrary;
- the coverage-maximal average: every placement of exactly B decoys (|L| if
  fewer) whose Coverage is the highest any B decoys reach, each equally likely.
  Many placements block the same number of paths, and a coverage-only method
  has no reason to prefer one of them, so averaging removes the arbitrary
  tie-break. D37 makes this form the primary one and reports the greedy form
  beside it.
"""
from __future__ import annotations

from itertools import combinations

COVERAGE_ONLY_WEIGHTS = (1.0, 0.0, 0.0, 0.0, 0.0)
TOL = 1e-12


def coverage(x: set[int], paths: list[dict]) -> float:
    return sum(1 for p in paths if any(a in x for a in p["asset_sequence"])) / len(paths)


def coverage_maximal_placements(candidates: list[int], paths: list[dict], budget: int) -> list[set[int]]:
    k = min(budget, len(candidates))
    if k <= 0:
        return [set()]
    best, out = -1.0, []
    for combo in combinations(sorted(candidates), k):
        c = coverage(set(combo), paths)
        if c > best + TOL:
            best, out = c, [set(combo)]
        elif abs(c - best) <= TOL:
            out.append(set(combo))
    return out
