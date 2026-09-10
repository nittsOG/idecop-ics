"""
FastAPI backend. Screen 3 slice (plausibility review) plus /optimize,
/runs, /runs/{id} — connecting the tested graph_model and optimizer
modules to something callable over HTTP, per the build order in
02-prototype-architecture.md §3.

/runs/{id}/explain (the AI explanation layer) is still not built — that
needs the Ollama integration from 02-ai-role.md, a separate slice.
"""
import time
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.graph_model import load_graph, compute_criticality, load_candidate_locations, load_attack_paths
from src.optimizer.baselines import greedy, random_baseline, centrality_baseline
from src.optimizer.milp import solve_milp

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "deception_placement.db"

app = FastAPI(title="iDECOP-ICS API", description="intelligent Deception Planning and Placement Optimization for Industrial Control Systems")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def get_db() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise HTTPException(500, f"Database not found at {DB_PATH} — run data/seed the DB first.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


VALID_SCORES = {"yes", "mostly", "no"}
VALID_METHODS = {"random", "centrality", "proposed_greedy", "proposed_milp"}


class ConfirmPayload(BaseModel):
    decoy_exists: str | None = Field(None, description="yes/mostly/no — omit to accept AI suggestion")
    attacker_reach: str | None = None
    useful_signal: str | None = None
    reliable_indicator: str | None = None


class OptimizePayload(BaseModel):
    method: str = Field(..., description="random | centrality | proposed_greedy | proposed_milp")
    alpha: float = 1.0
    beta: float = 1.0
    gamma: float = 1.0
    delta: float = 1.0
    epsilon: float = 0.1
    budget: int = Field(..., gt=0)


@app.get("/graph")
def get_graph():
    """Assets AND edges together — what Screen 1's network visualization
    actually needs. GET /assets alone (below) only returns nodes; without
    this, the frontend has no connections to draw, just floating dots."""
    conn = get_db()
    assets = conn.execute("""
        SELECT a.asset_id, a.name, a.asset_type, a.is_physical, z.name AS zone
        FROM assets a JOIN zones z ON z.zone_id = a.zone_id ORDER BY a.asset_id
    """).fetchall()
    edges = conn.execute("""
        SELECT source_asset_id, target_asset_id, protocol, weight FROM edges
    """).fetchall()
    conn.close()
    return {"assets": [dict(r) for r in assets], "edges": [dict(r) for r in edges]}


@app.get("/assets")
def list_assets():
    conn = get_db()
    rows = conn.execute("""
        SELECT a.asset_id, a.name, a.asset_type, a.is_physical, z.name AS zone
        FROM assets a JOIN zones z ON z.zone_id = a.zone_id ORDER BY a.asset_id
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/candidates")
def list_candidates():
    conn = get_db()
    rows = conn.execute("""
        SELECT a.asset_id, a.name, a.asset_type,
            cl.criterion_decoy_exists, cl.criterion_attacker_reach,
            cl.criterion_useful_signal, cl.criterion_reliable_indicator,
            cl.passes_plausibility, cl.detectability_risk, cl.is_candidate, cl.rationale,
            cl.ai_suggested_decoy_exists, cl.ai_suggested_attacker_reach,
            cl.ai_suggested_useful_signal, cl.ai_suggested_reliable_indicator,
            cl.ai_reasoning, cl.human_confirmed, cl.confirmed_at
        FROM candidate_locations cl JOIN assets a ON a.asset_id = cl.asset_id ORDER BY a.asset_id
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/candidates/{asset_id}/confirm")
def confirm_candidate(asset_id: int, payload: ConfirmPayload):
    conn = get_db()
    row = conn.execute("SELECT * FROM candidate_locations WHERE asset_id = ?", (asset_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(404, f"No candidate_locations row for asset_id {asset_id}")

    def resolve(override, ai_value, field_name):
        value = override if override is not None else ai_value
        if value is not None and value not in VALID_SCORES:
            raise HTTPException(422, f"{field_name} must be one of {VALID_SCORES}, got {value!r}")
        return value

    decoy_exists = resolve(payload.decoy_exists, row["ai_suggested_decoy_exists"], "decoy_exists")
    attacker_reach = resolve(payload.attacker_reach, row["ai_suggested_attacker_reach"], "attacker_reach")
    useful_signal = resolve(payload.useful_signal, row["ai_suggested_useful_signal"], "useful_signal")
    reliable_indicator = resolve(payload.reliable_indicator, row["ai_suggested_reliable_indicator"], "reliable_indicator")
    values = [decoy_exists, attacker_reach, useful_signal, reliable_indicator]
    passes = all(v is not None and v != "no" for v in values)

    conn.execute("""
        UPDATE candidate_locations SET
            criterion_decoy_exists=?, criterion_attacker_reach=?,
            criterion_useful_signal=?, criterion_reliable_indicator=?,
            passes_plausibility=?, is_candidate=?, human_confirmed=1, confirmed_at=?
        WHERE asset_id=?
    """, (decoy_exists, attacker_reach, useful_signal, reliable_indicator,
          int(passes), int(passes), datetime.now(timezone.utc).isoformat(), asset_id))
    conn.commit()
    updated = conn.execute("SELECT * FROM candidate_locations WHERE asset_id = ?", (asset_id,)).fetchone()
    conn.close()
    return dict(updated)


@app.get("/attack-paths")
def list_attack_paths():
    conn = get_db()
    paths = []
    for p in conn.execute("SELECT * FROM attack_paths ORDER BY path_id"):
        steps = conn.execute("""
            SELECT aps.step_order, aps.tactic, aps.technique_id, aps.technique_name, a.name AS asset_name
            FROM attack_path_steps aps JOIN assets a ON a.asset_id = aps.asset_id
            WHERE aps.path_id=? ORDER BY step_order
        """, (p["path_id"],)).fetchall()
        paths.append({**dict(p), "steps": [dict(s) for s in steps]})
    conn.close()
    return paths


@app.post("/optimize")
def optimize(payload: OptimizePayload):
    """Runs one of the four methods against the live graph and confirmed
    candidates, writes a placement_runs row + placements rows, returns the
    run_id. The frontend fetches the actual result via GET /runs/{id}
    afterward — deliberate, per 02-prototype-architecture.md §2, so nothing
    displayed didn't come from a durably stored row."""
    if payload.method not in VALID_METHODS:
        raise HTTPException(422, f"method must be one of {VALID_METHODS}")

    g = load_graph(DB_PATH)
    criticality = compute_criticality(g)
    candidates = load_candidate_locations(DB_PATH)
    if not candidates:
        raise HTTPException(400, "No confirmed candidate locations — nothing for the optimizer to search over. Confirm at least one via /candidates/{id}/confirm first.")
    paths = load_attack_paths(DB_PATH)
    weights = (payload.alpha, payload.beta, payload.gamma, payload.delta, payload.epsilon)

    conn = get_db()
    detectability = {r[0]: r[1] or 0.0 for r in conn.execute("SELECT asset_id, detectability_risk FROM candidate_locations")}

    start = time.perf_counter()
    if payload.method == "random":
        _, results, summary = random_baseline(candidates, paths, criticality, detectability, payload.budget, weights)
        x = max(zip(_, results), key=lambda pr: pr[1].f_score)[0]  # report the best trial's placement; mean/std in summary
        metrics = max(results, key=lambda r: r.f_score)
    elif payload.method == "centrality":
        central_scores = {n: criticality[n]["central"] for n in criticality}
        x, metrics = centrality_baseline(candidates, central_scores, paths, criticality, detectability, payload.budget, weights)
    elif payload.method == "proposed_greedy":
        x, metrics = greedy(candidates, paths, criticality, detectability, payload.budget, weights)
    else:  # proposed_milp
        x, metrics, _ = solve_milp(candidates, paths, criticality, detectability, payload.budget, weights)
    runtime = time.perf_counter() - start

    cur = conn.execute("""
        INSERT INTO placement_runs
            (method, alpha, beta, gamma, delta, epsilon, budget,
             coverage_score, early_score, critprot_score, risk_score, cost_score,
             objective_value, runtime_seconds)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (payload.method, *weights, payload.budget,
          metrics.coverage, metrics.early, metrics.crit_prot, metrics.risk, metrics.cost,
          metrics.f_score, runtime))
    run_id = cur.lastrowid
    for asset_id in x:
        conn.execute("INSERT INTO placements (run_id, asset_id) VALUES (?, ?)", (run_id, asset_id))
    conn.commit()
    conn.close()
    return {"run_id": run_id}


@app.get("/runs")
def list_runs():
    """Every stored run — what Screen 2's sensitivity-sweep comparison reads from directly."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM placement_runs ORDER BY run_id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/runs/{run_id}")
def get_run(run_id: int):
    conn = get_db()
    run = conn.execute("SELECT * FROM placement_runs WHERE run_id=?", (run_id,)).fetchone()
    if run is None:
        conn.close()
        raise HTTPException(404, f"No run with id {run_id}")
    placed = conn.execute("""
        SELECT a.asset_id, a.name FROM placements p JOIN assets a ON a.asset_id = p.asset_id
        WHERE p.run_id=?
    """, (run_id,)).fetchall()
    conn.close()
    return {**dict(run), "placements": [dict(p) for p in placed]}


@app.get("/health")
def health():
    return {"status": "ok", "db_exists": DB_PATH.exists()}
