"""
Self-test for the Phase D evaluation code (A12; D37), on a toy network only.

It never reads the testbed's database, so it can run before the freeze without
showing any result on the real instance. Every expected value below was worked
out by hand from the toy network drawn here, then checked by the code:

    Attacker(1) -> FW(2) -> JH(3) -> WS(4) -> PLC-A(6)
                            JH(3) -> HMI(5) -> PLC-A(6)
                                     HMI(5) -> PLC-B(7)

    tp1 = JH > WS > PLC-A        (target PLC-A)
    tp2 = FW > JH > HMI > PLC-B  (target PLC-B)

Footholds {FW, JH, WS, HMI}; objectives {PLC-A, PLC-B}: 8 pairs.

Usage:  uv run python scripts/evaluation_selftest.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.evaluation import simulation as sim  # noqa: E402
from src.evaluation.holdout import leave_one_path_out, first_stage  # noqa: E402
from src.evaluation.comparators import coverage_maximal_placements  # noqa: E402

spec = importlib.util.spec_from_file_location("evaluate", ROOT / "scripts" / "evaluate.py")
evaluate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluate)

FAILS = []


def check(label: str, got, want, tol: float = 1e-12) -> None:
    ok = abs(got - want) <= tol if isinstance(want, (int, float, Fraction)) and not isinstance(want, bool) else got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" (expected {want!r})"))
    if not ok:
        FAILS.append(label)


def toy():
    g = nx.DiGraph()
    for n, (name, t) in {1: ("Attacker", "Attacker"), 2: ("FW", "Firewall"), 3: ("JH", "Jump Server"),
                         4: ("WS", "Engineering Workstation"), 5: ("HMI", "HMI"),
                         6: ("PLC-A", "PLC"), 7: ("PLC-B", "PLC")}.items():
        g.add_node(n, name=name, asset_type=t)
    g.add_edges_from([(1, 2), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (5, 7)])
    paths = [{"path_id": 1, "name": "tp1", "asset_sequence": [3, 4, 6], "length": 3, "target": 6},
             {"path_id": 2, "name": "tp2", "asset_sequence": [2, 3, 5, 7], "length": 4, "target": 7}]
    crit = {v: {"criticality": c, "central": 0.0, "name": g.nodes[v]["name"]}
            for v, c in {1: 0.0, 2: 0.2, 3: 0.3, 4: 0.3, 5: 0.3, 6: 0.6, 7: 0.4}.items()}
    ctx = {"graph": g, "paths": paths, "crit": crit, "candidates": [2, 3, 4, 5],
           "central": {2: 0.1, 3: 0.6, 4: 0.2, 5: 0.3}, "risk": {2: 0.5, 3: 0.3, 4: 0.4, 5: 0.2},
           "names": {v: g.nodes[v]["name"] for v in g}}
    return ctx


def main() -> int:
    ctx = toy()
    g, P = ctx["graph"], ctx["paths"]

    print("population")
    check("footholds", sim.all_footholds(g), [2, 3, 4, 5])
    check("documented footholds", sim.documented_footholds(P), [2, 3])
    check("objectives", sim.objectives(g, P), [6, 7])
    check("route graph drops the Attacker", sorted(sim.route_graph(g).nodes), [2, 3, 4, 5, 6, 7])
    pops = {s: sim.build_population(g, P, s) for s in (0, 1, 2)}
    check("pairs", len(pops[1]["pairs"]), 8)
    check("routes at slack 0", pops[0]["n_routes"], 11)
    check("routes at slack 1", pops[1]["n_routes"], 11)
    check("routes at slack 2", pops[2]["n_routes"], 15)
    check("no unreachable pair", pops[1]["unreachable"], [])
    r = {(p["foothold"], p["objective"]): p["routes"] for p in pops[2]["pairs"]}
    check("FW to PLC-B at slack 2", r[(2, 7)], [(2, 3, 4, 6, 5, 7), (2, 3, 5, 7)])

    print("simulation scores (slack 1)")
    a = sim.evaluate_placement({3}, pops[1])
    check("decoy at JH: detection", a["detection"], 9 / 16)
    check("decoy at JH: before objective", a["before_objective"], 9 / 16)
    check("decoy at JH: earliness", a["earliness"], 11 / 24)
    b = sim.evaluate_placement({6}, pops[1])
    check("decoy at PLC-A: detection", b["detection"], 9 / 16)
    check("decoy at PLC-A: before objective", b["before_objective"], 1 / 16)
    check("decoy at PLC-A: earliness", b["earliness"], 1 / 24)
    check("no decoy: detection", sim.evaluate_placement(set(), pops[1])["detection"], 0.0)

    print("leave-one-path-out")
    check("first stage of tp2 for {JH}", first_stage({3}, P[1]), 2)
    lo = leave_one_path_out(lambda train: [{train[0]["asset_sequence"][0]}], P, ctx["crit"])
    check("held-out hits", lo["hits"], 1)
    check("held-out earliness", lo["earliness"], 1 / 3)
    check("crit-weighted protection", lo["crit_weighted"], 0.4)
    lo2 = leave_one_path_out(lambda train: [{3}, {2}], P, ctx["crit"])
    check("two equally likely placements: hits", lo2["hits"], 1.5)

    print("coverage-only comparator")
    check("maximal placements, B=1", coverage_maximal_placements(ctx["candidates"], P, 1), [{3}])
    check("maximal placements, B=2", coverage_maximal_placements(ctx["candidates"], P, 2),
          [{2, 3}, {2, 4}, {3, 4}, {3, 5}, {4, 5}])

    print("declared grid, read from scripts/sweep.py")
    budgets, weightings = evaluate.declared_grid()
    check("budgets", budgets, (1, 2, 3, 4))
    check("weightings", list(weightings), ["default", "alpha=3", "beta=3", "gamma=3", "delta=3"])

    print("freeze check")
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "a.txt").write_text("frozen")
        man = root / "manifest.json"
        man.write_text(json.dumps({"files": {"a.txt": evaluate.sha256(root / "a.txt")}}))
        check("matching file passes", evaluate.check_frozen(root, man)["files"]["a.txt"][:8],
              evaluate.sha256(root / "a.txt")[:8])
        (root / "a.txt").write_text("changed")
        try:
            evaluate.check_frozen(root, man)
            check("changed file refused", False, True)
        except SystemExit:
            check("changed file refused", True, True)
        try:
            evaluate.check_frozen(root, root / "absent.json")
            check("missing manifest refused", False, True)
        except SystemExit:
            check("missing manifest refused", True, True)

    print("end to end on the toy network (every method, B = 1, 2)")
    res = evaluate.run(ctx, (1, 2), {"default": (1.0, 1.0, 1.0, 1.0, 0.1), "delta=3": (1.0, 1.0, 1.0, 3.0, 0.1)})
    cells = res["cells"]
    check("cells", sorted(cells), [("default", 1), ("default", 2), ("delta=3", 1), ("delta=3", 2)])
    check("methods per cell", sorted(cells[("default", 1)]), sorted(evaluate.METHODS))
    ranges = all(0.0 <= c[m]["sim"][k][s] <= 1.0 + 1e-12 and 0.0 <= c[m]["lopo"]["hits"] <= len(P)
                 for c in cells.values() for m in c for k in c[m]["sim"]
                 for s in ("detection", "before_objective", "earliness"))
    check("every score within its range", ranges, True)
    check("greedy at B=1 places JH (the toy's best F)", cells[("default", 1)]["greedy"]["placements"], [[3]])
    check("MILP agrees with greedy at B=1", cells[("default", 1)]["milp"]["placements"], [[3]])
    check("hypotheses classified", sorted(res["hypotheses"]), ["H1", "H2", "H3"])
    check("all-cell counts cover the grid", sum(res["all_cells"]["centrality:sim.detection"].values()), 4)
    evaluate.report(res, ctx["names"])

    print(f"\n{'ALL CHECKS PASSED' if not FAILS else 'FAILED: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
