"""Self-test of Screen 2's backend, GET /runs/compare (D46).

    uv run python scripts/screen2_selftest.py

It needs the database with the committed review restored (L must not be
empty). It works on a temporary copy of the database, with that copy's stored
runs removed first, so your own runs are untouched and the counts are exact.
Checks: the route order; the declared grid; a missing run reported as missing;
every stored row equal to the frozen method called directly; random as the
mean of its 30 trials, never a stored run (D17); the latest run winning; the
published numbers at B = 3 (D33, D40); and the MILP's F equal to greedy's in
all 20 cells of the grid.
"""
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fastapi import HTTPException  # noqa: E402

import src.api.main as api  # noqa: E402
from src.graph_model import compute_criticality, load_attack_paths, load_candidate_locations, load_graph  # noqa: E402
from src.optimizer.baselines import centrality_baseline, distorted_greedy, greedy, random_baseline  # noqa: E402
from src.optimizer.milp import solve_milp  # noqa: E402

PASSED = []
TOL = 1e-9
WKEYS = ("alpha", "beta", "gamma", "delta", "epsilon")


def ok(cond, what):
    if not cond:
        print(f"FAILED: {what}")
        sys.exit(1)
    PASSED.append(what)


def direct(db, method, budget, w):
    """The frozen method called as POST /optimize calls it, outside the API."""
    crit = compute_criticality(load_graph(db))
    cands, paths = load_candidate_locations(db), load_attack_paths(db)
    conn = sqlite3.connect(db)
    risk = {a: r or 0.0 for a, r in conn.execute("SELECT asset_id, detectability_risk FROM candidate_locations")}
    names = dict(conn.execute("SELECT asset_id, name FROM assets"))
    conn.close()
    if method == "random":
        _, res, _ = random_baseline(cands, paths, crit, risk, budget, w)
        return None, {c: sum(getattr(t, a) for t in res) / len(res) for c, a in api._SCORE_ATTRS.items()}
    if method == "centrality":
        x, m = centrality_baseline(cands, {n: crit[n]["central"] for n in crit}, paths, crit, risk, budget, w)
    elif method == "proposed_greedy":
        x, m = greedy(cands, paths, crit, risk, budget, w)
    elif method == "proposed_distorted_greedy":
        x, m = distorted_greedy(cands, paths, crit, risk, budget, w)
    else:
        x, m, _ = solve_milp(cands, paths, crit, risk, budget, w)
    return sorted(names[a] for a in x), {c: getattr(m, a) for c, a in api._SCORE_ATTRS.items()}


def sweep(budget, weightings):
    for w in weightings.values():
        for method in api.COMPARE_METHODS:
            api.optimize(api.OptimizePayload(method=method, budget=budget, **dict(zip(WKEYS, w))))


def main():
    db = api.DB_PATH
    if not db.exists():
        print("No database: run `uv run scripts/setup.py` and restore the review first.")
        sys.exit(1)
    tmp = Path(tempfile.mkdtemp(prefix="screen2-selftest-"))
    try:
        test_db = tmp / "db.sqlite"
        shutil.copy(db, test_db)
        conn = sqlite3.connect(test_db)
        conn.execute("PRAGMA foreign_keys = ON")
        for table in ("explanations", "placements", "placement_runs"):
            conn.execute(f"DELETE FROM {table}")
        conn.commit()
        conn.close()
        api.DB_PATH = test_db
        run_tests(test_db)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"ALL {len(PASSED)} SCREEN 2 CHECKS PASSED")


def run_tests(db):
    paths = [r.path for r in api.app.routes if hasattr(r, "path")]
    ok(paths.index("/runs/compare") < paths.index("/runs/{run_id}"),
       "/runs/compare is declared before /runs/{run_id}")

    budgets, weightings = api.declared_grid()
    ok(budgets == (1, 2, 3, 4) and list(weightings) == ["default", "alpha=3", "beta=3", "gamma=3", "delta=3"],
       "the declared grid is read from scripts/sweep.py")
    ok(weightings["default"] == (1.0, 1.0, 1.0, 1.0, 0.1), "the default weighting is (1, 1, 1, 1, 0.1)")

    try:
        api.compare_runs(0)
        ok(False, "budget 0 is refused")
    except HTTPException as e:
        ok(e.status_code == 422, "budget 0 is refused")

    out = api.compare_runs(3)
    ok(len(out["missing"]) == 20 and len(out["rows"]) == 5 and all(r["method"] == "random" for r in out["rows"]),
       "with no stored runs, all 20 are missing and only random's means are given")

    sweep(3, weightings)
    out = api.compare_runs(3)
    ok(not out["missing"] and len(out["rows"]) == 25, "after the sweep at B = 3, none is missing")
    for r in out["rows"]:
        w = weightings[r["weighting"]]
        placement, scores = direct(db, r["method"], 3, w)
        same = all(abs(r[c] - scores[c]) <= TOL for c in api.SCORE_COLUMNS)
        ok(same and r["placement"] == placement, f"B = 3, {r['weighting']}, {r['method']}: equals the frozen method")

    default = {r["method"]: r for r in out["rows"] if r["weighting"] == "default"}
    ok(round(default["proposed_greedy"]["objective_value"], 4) == 2.4175, "greedy's F at B = 3 is 2.4175 (D33)")
    ok(round(default["centrality"]["objective_value"], 4) == 1.2060, "centrality's F at B = 3 is 1.2060 (D33)")
    ok(round(default["random"]["objective_value"], 4) == 1.3229, "random's mean F at B = 3 is 1.3229 (D33)")
    ok(default["random"]["run_id"] is None and default["random"]["trials"] == 30, "random is computed, not stored")

    conn = sqlite3.connect(db)
    conn.execute("INSERT INTO placement_runs (method, alpha, beta, gamma, delta, epsilon, budget, objective_value) "
                 "VALUES ('random', 1, 1, 1, 1, 0.1, 3, 99.0)")
    conn.commit()
    conn.close()
    again = {r["method"]: r for r in api.compare_runs(3)["rows"] if r["weighting"] == "default"}
    ok(abs(again["random"]["objective_value"] - default["random"]["objective_value"]) <= TOL,
       "a stored random run is never read (D17)")

    first = default["proposed_greedy"]["run_id"]
    newer = api.optimize(api.OptimizePayload(method="proposed_greedy", budget=3))["run_id"]
    again = {r["method"]: r for r in api.compare_runs(3)["rows"] if r["weighting"] == "default"}
    ok(newer > first and again["proposed_greedy"]["run_id"] == newer, "the latest stored run is the one shown")

    for b in budgets:
        if b != 3:
            sweep(b, weightings)
        rows = api.compare_runs(b)["rows"]
        f = {(r["weighting"], r["method"]): r["objective_value"] for r in rows}
        ok(all(abs(f[(n, "proposed_milp")] - f[(n, "proposed_greedy")]) <= TOL for n in weightings),
           f"B = {b}: the MILP's F equals greedy's in every weighting")


if __name__ == "__main__":
    main()
