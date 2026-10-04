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
from src.graph_model import load_graph, compute_criticality, load_candidate_locations, load_attack_paths, CandidateSetError
from src.plausibility import KEYS, check_answers, passes, reason_required, RubricError
from src.optimizer.baselines import greedy, random_baseline, centrality_baseline, distorted_greedy
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


VALID_METHODS = {"random", "centrality", "proposed_greedy", "proposed_distorted_greedy", "proposed_milp"}


class ConfirmPayload(BaseModel):
    """The reviewer's four answers, in criterion order. D26: yes / mostly_yes /
    mostly_no / no. After the first 'no' the remaining answers must be blank
    (sequential rule). There is no fallback to the AI's suggestion: a blank is a
    blank, never 'accept the AI'."""
    decoy_exists: str | None = Field(None, description="Feasibility")
    attacker_reach: str | None = Field(None, description="Interaction")
    useful_signal: str | None = Field(None, description="Intelligence yield")
    reliable_indicator: str | None = Field(None, description="Malice fidelity")
    reason: str | None = Field(None, description="Required on a blind card, with no AI suggestion, after changing an AI answer, or for any Mostly No / No answer")


class OptimizePayload(BaseModel):
    method: str = Field(..., description="random | centrality | proposed_greedy | proposed_distorted_greedy | proposed_milp")
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
    """Every asset in Screen 3's review (all except the Attacker node, A32), with
    the attack-path steps it sits on.

    D26: on a blind card the AI's answer stays hidden until the reviewer has
    confirmed their own. The design-time `rationale` text is no longer sent,
    because it pre-judged the outcome."""
    conn = get_db()
    rows = conn.execute("""
        SELECT a.asset_id, a.name, a.asset_type, a.purdue_level, z.name AS zone,
            cl.criterion_decoy_exists, cl.criterion_attacker_reach,
            cl.criterion_useful_signal, cl.criterion_reliable_indicator,
            cl.passes_plausibility, cl.detectability_risk, cl.is_candidate, cl.blind_first,
            cl.blind_decoy_exists, cl.blind_attacker_reach, cl.blind_useful_signal,
            cl.blind_reliable_indicator, cl.blind_reason, cl.blind_confirmed_at,
            cl.ai_suggested_decoy_exists, cl.ai_suggested_attacker_reach,
            cl.ai_suggested_useful_signal, cl.ai_suggested_reliable_indicator,
            cl.ai_reasoning, cl.ai_model, cl.human_reason, cl.human_confirmed, cl.confirmed_at
        FROM candidate_locations cl
        JOIN assets a ON a.asset_id = cl.asset_id
        JOIN zones z ON z.zone_id = a.zone_id
        ORDER BY a.asset_id
    """).fetchall()
    steps = conn.execute("""
        SELECT s.asset_id, p.name AS path, s.step_order, s.tactic, s.technique_id, s.technique_name,
               (SELECT COUNT(*) FROM attack_path_steps s2 WHERE s2.path_id = s.path_id) AS path_length
        FROM attack_path_steps s JOIN attack_paths p ON p.path_id = s.path_id
        ORDER BY p.path_id, s.step_order
    """).fetchall()
    conn.close()

    by_asset = {}
    for st in steps:
        by_asset.setdefault(st["asset_id"], []).append({k: st[k] for k in st.keys() if k != "asset_id"})
    out = []
    for r in rows:
        d = dict(r)
        d["path_steps"] = by_asset.get(d["asset_id"], [])
        d["n_paths"] = len({st["path"] for st in d["path_steps"]})
        d["ai_hidden"] = bool(d["blind_first"] and not d["blind_confirmed_at"])
        if d["ai_hidden"]:
            for k in KEYS:
                d[f"ai_suggested_{k}"] = None
            d["ai_reasoning"] = None
            d["ai_model"] = None
        out.append(d)
    return out


@app.post("/candidates/{asset_id}/confirm")
def confirm_candidate(asset_id: int, payload: ConfirmPayload):
    """Writes the reviewer's answers and applies Filter 1's rules from
    src/plausibility (D26), the same rules the import and restore scripts use:
    - the sequential rule (the first 'no' ends the card);
    - the path rule (an asset on no modelled path has Interaction No);
    - the reason rule (see ConfirmPayload.reason);
    - the combination rule (pass only if all four are answered and none is 'no').

    A blind card's first confirmation is also stored, once, in the blind_*
    columns, which the AI-agreement measure reads.

    is_candidate follows the Filter 1 result. A candidate still needs a Filter 2
    score before the optimiser will accept it; load_candidate_locations checks that."""
    conn = get_db()
    row = conn.execute("SELECT * FROM candidate_locations WHERE asset_id = ?", (asset_id,)).fetchone()
    if row is None:
        conn.close()
        raise HTTPException(404, f"No candidate_locations row for asset_id {asset_id}")

    n_paths = conn.execute("SELECT COUNT(DISTINCT path_id) FROM attack_path_steps WHERE asset_id = ?",
                           (asset_id,)).fetchone()[0]
    answers = {k: getattr(payload, k) for k in KEYS}
    try:
        ordered = check_answers(answers, n_paths)
        passed = passes(answers, n_paths)
        # Blind card: the AI's answer is not compared here, so a validation
        # message cannot reveal whether the reviewer agreed with it.
        ai = None if row["blind_first"] else {k: row[f"ai_suggested_{k}"] for k in KEYS}
        needs_reason = reason_required(answers, ai, bool(row["blind_first"]), n_paths)
    except RubricError as e:
        conn.close()
        raise HTTPException(422, str(e))
    reason = (payload.reason or "").strip()
    if needs_reason and not reason:
        conn.close()
        raise HTTPException(422, "A reason is required: " + "; ".join(needs_reason))

    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""
        UPDATE candidate_locations SET
            criterion_decoy_exists=?, criterion_attacker_reach=?,
            criterion_useful_signal=?, criterion_reliable_indicator=?,
            human_reason=?, passes_plausibility=?, is_candidate=?, human_confirmed=1, confirmed_at=?
        WHERE asset_id=?
    """, (*ordered, reason or None, int(passed), int(passed), now, asset_id))
    if row["blind_first"] and not row["blind_confirmed_at"]:
        # D26: the first confirmation of a blind card is recorded once and never
        # changed. The final answers above may still change later, with a reason;
        # the agreement measure reads these columns.
        conn.execute("""
            UPDATE candidate_locations SET
                blind_decoy_exists=?, blind_attacker_reach=?, blind_useful_signal=?,
                blind_reliable_indicator=?, blind_reason=?, blind_confirmed_at=?
            WHERE asset_id=?
        """, (*ordered, reason, now, asset_id))
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
    """Runs one of the five methods against the live graph and the current
    candidate set, writes a placement_runs row and its placements rows, and
    returns the
    run_id. The frontend fetches the actual result via GET /runs/{id}
    afterward — deliberate, per 02-prototype-architecture.md §2, so nothing
    displayed didn't come from a durably stored row."""
    if payload.method not in VALID_METHODS:
        raise HTTPException(422, f"method must be one of {VALID_METHODS}")

    g = load_graph(DB_PATH)
    criticality = compute_criticality(g)
    # D26: the API never runs on a candidate set that bypassed Filter 1's review
    # or lacks a Filter 2 score. There is no legacy switch here.
    try:
        candidates = load_candidate_locations(DB_PATH)
    except CandidateSetError as e:
        raise HTTPException(409, str(e))
    if not candidates:
        raise HTTPException(400, "No candidate locations yet: L is empty until the A32 review in Screen 3 confirms at least one asset that passes Filter 1 (formal-problem-definition.md §4, D26).")
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
    elif payload.method == "proposed_distorted_greedy":
        # The only method here carrying a worst-case approximation guarantee
        # ((1 - 1/e), Harshaw et al. 2019). Exposed for the scalability argument,
        # NOT as the better performer — it is measurably more conservative than
        # plain greedy on this testbed. See distorted_greedy's docstring and D23.
        x, metrics = distorted_greedy(candidates, paths, criticality, detectability, payload.budget, weights)
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
