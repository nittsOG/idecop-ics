"""
Phase D: A12's two new criteria, for every method (D37; docs/03-evaluation-methodology.md).

- Leave-one-path-out validation (§2): each path held out in turn.
- The attack simulation (§3): every route from every non-controller foothold
  to every objective, primary slack 1, with slacks 0 and 2 and the documented
  footholds as secondary populations.
- Methods: greedy (primary), distorted greedy, the exact MILP, the coverage-
  only comparator in both forms (§4), centrality and random, each called
  exactly as scripts/run_comparison.py calls it.
- Grid: BUDGETS and WEIGHTINGS read from scripts/sweep.py, so the grid has one
  definition (D24). Default weights are primary; the other weightings are
  reported as counts.
- Hypotheses H1-H3: classified by the rules fixed in §5 and in the user's
  pre-registration (A15).

The F-based grid and the weight sweep are run, as before, by scripts/sweep.py
(--sens), scripts/run_comparison.py and scripts/structure_check.py.

It refuses to run until the inputs are frozen: data/freeze/manifest.json must
exist, and every file it lists must still match its recorded SHA-256
(scripts/freeze.py writes it). A run before the freeze would show results
before the design is fixed, which the evaluation-integrity rule forbids.
scripts/evaluation_selftest.py exercises the same code on a toy network.

Usage:  uv run python scripts/evaluate.py [--json data/results/phase-d.json]
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.optimizer.baselines import greedy, distorted_greedy, centrality_baseline, random_baseline  # noqa: E402
from src.optimizer.milp import solve_milp  # noqa: E402
from src.evaluation.holdout import leave_one_path_out, mean_and_sd  # noqa: E402
from src.evaluation.simulation import (build_population, evaluate_placement, documented_footholds,  # noqa: E402
                                       PRIMARY_SLACK, SENSITIVITY_SLACKS)
from src.evaluation.comparators import COVERAGE_ONLY_WEIGHTS, coverage_maximal_placements  # noqa: E402

MANIFEST = ROOT / "data" / "freeze" / "manifest.json"
METHODS = ("greedy", "distorted_greedy", "milp", "coverage_max", "coverage_greedy", "centrality", "random")
LABELS = {
    "greedy": "Greedy (proposed)", "distorted_greedy": "Distorted greedy", "milp": "MILP (exact)",
    "coverage_max": "Coverage-only, ties averaged", "coverage_greedy": "Coverage-only greedy",
    "centrality": "Centrality", "random": "Random (30, mean)",
}
LOPO_KEYS = ("hits", "earliness", "crit_weighted")
SIM_KEYS = ("detection", "before_objective", "earliness")
PRIMARY_WEIGHTING = "default"
TOL = 1e-9

NOT_FROZEN = ("Phase D runs only after the freeze (A12, A15; D37). data/freeze/manifest.json does not "
              "exist. Commit the pre-registration and the frozen inputs, then run scripts/freeze.py. "
              "To exercise this code without the testbed, run scripts/evaluation_selftest.py.")


def declared_grid(sweep_path: Path = ROOT / "scripts" / "sweep.py") -> tuple[tuple[int, ...], dict]:
    """BUDGETS and WEIGHTINGS from sweep.py's source text, without running it."""
    tree = ast.parse(sweep_path.read_text(encoding="utf-8"))
    found = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("BUDGETS", "WEIGHTINGS")):
            found[node.targets[0].id] = ast.literal_eval(node.value)
    if set(found) != {"BUDGETS", "WEIGHTINGS"}:
        raise SystemExit(f"could not read BUDGETS and WEIGHTINGS from {sweep_path}")
    return tuple(found["BUDGETS"]), dict(found["WEIGHTINGS"])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_frozen(root: Path = ROOT, manifest: Path = MANIFEST) -> dict:
    if not manifest.exists():
        raise SystemExit(NOT_FROZEN)
    m = json.loads(manifest.read_text(encoding="utf-8"))
    changed = [p for p, h in sorted(m["files"].items()) if not (root / p).exists() or sha256(root / p) != h]
    if changed:
        raise SystemExit("These frozen files no longer match data/freeze/manifest.json: " + ", ".join(changed)
                         + ". A frozen input changed after the freeze. That needs its own decisions-log entry "
                           "stating its effect, and a new freeze, before Phase D runs (evaluation integrity).")
    return m


def placements_for(method: str, ctx: dict, paths: list[dict], budget: int, weights) -> list[set[int]]:
    """Equally likely placements of one method, called as run_comparison.py calls it."""
    L, crit, risk = ctx["candidates"], ctx["crit"], ctx["risk"]
    if method == "greedy":
        return [greedy(L, paths, crit, risk, budget, weights)[0]]
    if method == "distorted_greedy":
        return [distorted_greedy(L, paths, crit, risk, budget, weights)[0]]
    if method == "milp":
        x_m, m_m, _ = solve_milp(L, paths, crit, risk, budget, weights)
        _, m_g = greedy(L, paths, crit, risk, budget, weights)
        if m_m.f_score < m_g.f_score - TOL:
            raise SystemExit("INVARIANT VIOLATED: the exact MILP scored below greedy on the same paths "
                             f"(B={budget}, {len(paths)} paths). Do not interpret any result (D16, D24).")
        return [x_m]
    if method == "coverage_greedy":
        return [greedy(L, paths, crit, risk, budget, COVERAGE_ONLY_WEIGHTS)[0]]
    if method == "coverage_max":
        return coverage_maximal_placements(L, paths, budget)
    if method == "centrality":
        return [centrality_baseline(L, ctx["central"], paths, crit, risk, budget, weights)[0]]
    if method == "random":
        return random_baseline(L, paths, crit, risk, budget, weights)[0]
    raise ValueError(f"unknown method {method}")


def populations(ctx: dict) -> dict:
    g, P = ctx["graph"], ctx["paths"]
    pops = {"primary": build_population(g, P, PRIMARY_SLACK)}
    for s in SENSITIVITY_SLACKS:
        pops[f"slack{s}"] = build_population(g, P, s)
    pops["documented"] = build_population(g, P, PRIMARY_SLACK, footholds=documented_footholds(P))
    return pops


def evaluate_cell(ctx: dict, method: str, budget: int, weights, pops: dict) -> dict:
    P, crit = ctx["paths"], ctx["crit"]
    full = placements_for(method, ctx, P, budget, weights)
    if method == "random":
        lopo = mean_and_sd([leave_one_path_out(lambda train, x=x: [x], P, crit) for x in full], LOPO_KEYS)
    elif method == "centrality":
        lopo = leave_one_path_out(lambda train: full, P, crit)
    else:
        lopo = leave_one_path_out(lambda train: placements_for(method, ctx, train, budget, weights), P, crit)
    sim = {}
    for key, pop in pops.items():
        vals = [evaluate_placement(x, pop) for x in full]
        sim[key] = mean_and_sd(vals, SIM_KEYS) if len(vals) > 1 else vals[0]
    return {"placements": [sorted(x) for x in full], "lopo": lopo, "sim": sim}


def compare(a: float, b: float) -> str:
    return "win" if a > b + TOL else ("loss" if a < b - TOL else "tie")


def classify(n_holding: int, n_total: int) -> str:
    return "supported" if n_holding == n_total else ("not supported" if n_holding == 0 else "mixed")


def hypotheses(cells: dict, budgets) -> dict:
    """The rules of docs/03-evaluation-methodology.md §5, at the default weights.
    A comparison holds at a budget when greedy is not below its comparator
    (ties hold). Supported = holds at every budget; mixed = at some; not
    supported = at none."""
    def at(B, m):
        return cells[(PRIMARY_WEIGHTING, B)][m]

    out = {}
    rules = {
        "H1": [("lopo", "hits", "centrality"), ("lopo", "hits", "random")],
        "H2": [("sim", "detection", "centrality"), ("sim", "earliness", "centrality"),
               ("sim", "detection", "random"), ("sim", "earliness", "random")],
        "H3": [("sim", "detection", "coverage_max"), ("sim", "earliness", "coverage_max"),
               ("lopo", "hits", "coverage_max")],
    }
    for h, comps in rules.items():
        per_budget, details = [], []
        for B in budgets:
            ok = True
            for crit, key, other in comps:
                if crit == "lopo":
                    a, b = at(B, "greedy")["lopo"][key], at(B, other)["lopo"][key]
                else:
                    a, b = at(B, "greedy")["sim"]["primary"][key], at(B, other)["sim"]["primary"][key]
                r = compare(a, b)
                details.append({"B": B, "criterion": f"{crit}.{key}", "vs": other, "greedy": a, "other": b, "result": r})
                ok &= r != "loss"
            per_budget.append(ok)
        out[h] = {"holds_at": [B for B, ok in zip(budgets, per_budget) if ok],
                  "outcome": classify(sum(per_budget), len(budgets)), "details": details}
    return out


def all_cell_counts(cells: dict, weightings: dict, budgets) -> dict:
    """Secondary: greedy against each comparator in every cell of the grid."""
    criteria = [("lopo", "hits"), ("lopo", "earliness"), ("sim", "detection"), ("sim", "earliness")]
    out = {}
    for other in ("centrality", "random", "coverage_max"):
        for crit, key in criteria:
            tally = {"win": 0, "tie": 0, "loss": 0}
            for w in weightings:
                for B in budgets:
                    c = cells[(w, B)]
                    a = c["greedy"]["lopo"][key] if crit == "lopo" else c["greedy"]["sim"]["primary"][key]
                    b = c[other]["lopo"][key] if crit == "lopo" else c[other]["sim"]["primary"][key]
                    tally[compare(a, b)] += 1
            out[f"{other}:{crit}.{key}"] = tally
    return out


def run(ctx: dict, budgets, weightings: dict) -> dict:
    if PRIMARY_WEIGHTING not in weightings:
        raise SystemExit(f"the grid has no '{PRIMARY_WEIGHTING}' weighting")
    pops = populations(ctx)
    cells = {}
    for w, W in weightings.items():
        for B in budgets:
            cells[(w, B)] = {m: evaluate_cell(ctx, m, B, W, pops) for m in METHODS}
    return {
        "budgets": list(budgets), "weightings": weightings, "n_paths": len(ctx["paths"]),
        "populations": {k: {"slack": p["slack"], "pairs": len(p["pairs"]), "routes": p["n_routes"],
                            "unreachable": p["unreachable"]} for k, p in pops.items()},
        "cells": cells,
        "hypotheses": hypotheses(cells, budgets),
        "all_cells": all_cell_counts(cells, weightings, budgets),
    }


def report(res: dict, names: dict) -> None:
    budgets = res["budgets"]
    print("=" * 92)
    print("PHASE D -- A12's criteria outside F (D37; docs/03-evaluation-methodology.md)")
    print("=" * 92)
    for k, p in res["populations"].items():
        print(f"population {k:<10} slack {p['slack']}  pairs {p['pairs']:>3}  routes {p['routes']:>4}"
              f"  unreachable pairs {len(p['unreachable'])}")
    print(f"\nDefault weights {res['weightings'][PRIMARY_WEIGHTING]}; budgets {budgets}\n")
    head = " ".join(f"{'B=' + str(B):>17}" for B in budgets)
    for title, crit, keys in ((f"LEAVE-ONE-PATH-OUT  (held-out hits of {res['n_paths']} / earliness / crit-weighted)", "lopo", LOPO_KEYS),
                              ("SIMULATION, primary  (detection / before objective / earliness)", "sim", SIM_KEYS)):
        print(title)
        print(f"{'method':<30} {head}")
        for m in METHODS:
            row = []
            for B in budgets:
                c = res["cells"][(PRIMARY_WEIGHTING, B)][m]
                v = c["lopo"] if crit == "lopo" else c["sim"]["primary"]
                row.append("/".join(f"{v[k]:.2f}" for k in keys))
            print(f"{LABELS[m]:<30} " + " ".join(f"{r:>17}" for r in row))
        print()
    print("PLACEMENTS at default weights (full P)")
    for m in METHODS:
        if m in ("random", "coverage_max"):
            continue
        cells = [res["cells"][(PRIMARY_WEIGHTING, B)][m]["placements"][0] for B in budgets]
        print(f"{LABELS[m]:<30} " + " | ".join(", ".join(names[a] for a in x) or "(none)" for x in cells))
    print("\nSENSITIVITY (detection / earliness): greedy vs centrality vs coverage-only (ties averaged)")
    for key in ("slack0", "slack2", "documented"):
        parts = []
        for B in budgets:
            c = res["cells"][(PRIMARY_WEIGHTING, B)]
            parts.append(f"B={B}: " + " vs ".join(f"{c[m]['sim'][key]['detection']:.2f}/{c[m]['sim'][key]['earliness']:.2f}"
                                                    for m in ("greedy", "centrality", "coverage_max")))
        print(f"{key:<11} " + "   ".join(parts))
    print("\nHYPOTHESES (rules in docs/03-evaluation-methodology.md §5 and the pre-registration)")
    for h, r in res["hypotheses"].items():
        losses = [d for d in r["details"] if d["result"] == "loss"]
        print(f"{h}: {r['outcome']:<13} holds at B = {r['holds_at']}   losses: "
              + (", ".join(f"B={d['B']} {d['criterion']} vs {d['vs']}" for d in losses) or "none"))
    print("\nALL CELLS (greedy vs comparator: wins / ties / losses over the grid)")
    for k, t in res["all_cells"].items():
        print(f"  {k:<36} {t['win']:>2} / {t['tie']:>2} / {t['loss']:>2}")


def load_context() -> dict:
    import sqlite3
    from src.graph_model import load_graph, compute_criticality, load_attack_paths, candidates_or_exit
    g = load_graph()
    crit = compute_criticality(g)
    risk = {}
    conn = sqlite3.connect(ROOT / "data" / "deception_placement.db")
    for asset_id, r in conn.execute("SELECT asset_id, detectability_risk FROM candidate_locations"):
        risk[asset_id] = r or 0.0
    conn.close()
    return {"graph": g, "crit": crit, "candidates": candidates_or_exit(), "paths": load_attack_paths(),
            "central": {n: crit[n]["central"] for n in crit}, "risk": risk,
            "names": {n: crit[n]["name"] for n in crit}}


def jsonable(res: dict) -> dict:
    out = dict(res)
    out["cells"] = {f"{w}|B={B}": v for (w, B), v in res["cells"].items()}
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--json", help="also write the full results to this file")
    args = ap.parse_args()
    manifest = check_frozen()
    ctx = load_context()
    budgets, weightings = declared_grid()
    res = run(ctx, budgets, weightings)
    print(f"Frozen at commit {manifest.get('commit', '?')} ({manifest.get('frozen_at', '?')})\n")
    report(res, ctx["names"])
    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = jsonable(res)
        payload["manifest"] = {"commit": manifest.get("commit"), "frozen_at": manifest.get("frozen_at")}
        out.write_text(json.dumps(payload, indent=1, default=list), encoding="utf-8")
        print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
