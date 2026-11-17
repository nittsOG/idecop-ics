"""
Leave-one-path-out validation (A12; D37; docs/03-evaluation-methodology.md §2).

The guide asked for a K-fold-style validation (D32). With |P| = 5, each fold
holds one path out: the method places decoys knowing only the other four, and
the placement is scored on the held-out path, which the method never saw.
Path-agnostic methods (centrality, random) place the same decoys in every
fold, so for them every path is always held out.

On the reviewed candidate set every path meets at least two candidates (D31),
so decoys placed for the other paths can catch a held-out one. On D25's seeded
set every path met exactly one candidate and the test was degenerate, which is
why A12 waited for A32.

A held-out path caught at step s of n scores 1 for interception,
(n - s)/(n - 1) for earliness (the endpoint Early uses, D33) and
Crit(target) for criticality-weighted protection. Earliness and protection are
divided by the five-path totals, as Early and CritProt are in F, so an
uncaught path counts 0.

A method may return several equally likely placements for a fold (the
coverage-only comparator's ties); the fold then scores their mean.
"""
from __future__ import annotations

from typing import Callable, Iterable


def first_stage(x: set[int], path: dict) -> int | None:
    """1-based step at which the placement first meets the path, or None."""
    for s, asset in enumerate(path["asset_sequence"], start=1):
        if asset in x:
            return s
    return None


def _score_on(x: set[int], path: dict, criticality: dict) -> tuple[float, float, float]:
    s = first_stage(x, path)
    if s is None:
        return 0.0, 0.0, 0.0
    n = path["length"]
    return 1.0, (n - s) / (n - 1), criticality[path["target"]]["criticality"]


def leave_one_path_out(place: Callable[[list[dict]], Iterable[set[int]]],
                       paths: list[dict], criticality: dict) -> dict:
    """place(train_paths) returns one or more equally likely placements."""
    if len(paths) < 2:
        raise ValueError("leave-one-path-out needs at least two paths")
    folds = []
    for h in paths:
        train = [p for p in paths if p is not h]
        placements = [set(x) for x in place(train)]
        if not placements:
            raise ValueError(f"no placement returned for the fold holding out {h['name']}")
        scores = [_score_on(x, h, criticality) for x in placements]
        m = len(scores)
        folds.append({
            "held_out": h["name"],
            "placements": [sorted(x) for x in placements],
            "hit": sum(s[0] for s in scores) / m,
            "earliness": sum(s[1] for s in scores) / m,
            "crit": sum(s[2] for s in scores) / m,
        })
    crit_total = sum(criticality[p["target"]]["criticality"] for p in paths) or 1.0
    return {
        "folds": folds,
        "hits": sum(f["hit"] for f in folds),
        "earliness": sum(f["earliness"] for f in folds) / len(paths),
        "crit_weighted": sum(f["crit"] for f in folds) / crit_total,
    }


def mean_and_sd(results: list[dict], keys: Iterable[str]) -> dict:
    """Mean and population s.d. of summary numbers over several placements (random)."""
    out = {}
    for key in keys:
        vals = [r[key] for r in results]
        m = sum(vals) / len(vals)
        out[key] = m
        out[key + "_sd"] = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5
    return out
