"""
graph_model — builds G = (V, E) as a real NetworkX graph from SQLite, and
computes the two derived quantities formal-problem-definition.md §1-2 define:
Central(v) and Crit(v). Read-only against the database; nothing here writes.

Central(v) is genuinely computed from the graph's real edges (fixed in D14 —
see 02-data-model.md's edges/conduits section). SL(v) and Damage(v) are NOT
computed here — formal-problem-definition.md §2 is explicit that these are
elicited inputs, not derived quantities ("Damage... elicited during testbed
design"; SL is "a semi-quantitative approximation, not a solved measurement",
source #268). The placeholder values below exist so the pipeline runs
end-to-end for testing — they are not a substitute for real elicitation, and
are flagged loudly rather than passed off as real inputs.
"""
import sqlite3
from pathlib import Path

import networkx as nx

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "deception_placement.db"

# Illustrative SL(v) by Purdue level, following IEC 62443's usual convention
# that required security level rises closer to the physical process — NOT
# elicited data. Replace with real per-asset SL-3-3 vectors (7 FR scores,
# formal-problem-definition.md §2) before treating any Crit(v) result as
# more than a pipeline smoke test.
PLACEHOLDER_SL_BY_LEVEL = {
    "—": 0.3, "3.5": 0.5, "3": 0.6, "2-3": 0.65, "1-2": 0.85,
}
# Illustrative Damage(v) by asset type — same caveat. A real value needs the
# actual simulated-process load fraction per §2's worked pattern
# ("this PLC controls 40% of the process").
PLACEHOLDER_DAMAGE_BY_TYPE = {
    "PLC": 0.7, "HMI": 0.3, "Historian": 0.2, "Engineering Workstation": 0.2,
    "Jump Server": 0.1, "Firewall": 0.1, "Switch": 0.1, "Attacker": 0.0,
}


def load_graph(db_path: Path = DB_PATH) -> nx.DiGraph:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    g = nx.DiGraph()
    for row in conn.execute("SELECT a.*, z.name AS zone_name FROM assets a JOIN zones z ON z.zone_id = a.zone_id"):
        g.add_node(row["asset_id"], name=row["name"], asset_type=row["asset_type"],
                   zone=row["zone_name"], purdue_level=row["purdue_level"],
                   is_physical=row["is_physical"])
    for row in conn.execute("SELECT * FROM edges"):
        g.add_edge(row["source_asset_id"], row["target_asset_id"],
                   protocol=row["protocol"], weight=row["weight"] or 1.0)
    conn.close()
    return g


def compute_centrality(g: nx.DiGraph) -> dict[int, float]:
    """Central(v) — betweenness centrality, per D4's default choice, weighted
    by edge weight as formal-problem-definition.md §2 specifies."""
    if g.number_of_edges() == 0:
        return {n: 0.0 for n in g.nodes}
    return nx.betweenness_centrality(g, weight="weight", normalized=True)


def load_conduit_sl(g: nx.DiGraph, db_path: Path = DB_PATH) -> dict[int, float]:
    """ConduitSL(v) — the highest security level among the conduits incident to
    v's zone, or 0.0 if v's zone has none.

    A22/D20: conduits were named in the novelty claim as a first-class input
    but entered no computation — they were stored, diagrammed, and otherwise
    inert. This makes them numeric. The aggregation rule (a conduit takes the
    highest SL of the zones it joins) follows sources.md #330, which treats a
    conduit as carrying the protection burden of the more demanding side of the
    boundary it crosses.

    Rationale for attaching it to the asset rather than to the edge: every
    attack path in P must traverse a conduit to reach impact, so an asset
    sitting at a high-SL boundary is materially more important to protect than
    the same asset type deeper inside a single zone. Modular in x, so it does
    not disturb the submodularity D20 restores."""
    conn = sqlite3.connect(db_path)
    # graph nodes carry the zone NAME; conduits reference zone IDs
    id_to_name = {r[0]: r[1] for r in conn.execute("SELECT zone_id, name FROM zones")}

    zone_sl: dict[str, float] = {}
    for _, data in g.nodes(data=True):
        z = data.get("zone")
        if z is None:
            continue
        sl = PLACEHOLDER_SL_BY_LEVEL.get(data["purdue_level"], 0.5)
        zone_sl[z] = max(zone_sl.get(z, 0.0), sl)

    incident: dict[str, float] = {}
    for za, zb in conn.execute("SELECT zone_a_id, zone_b_id FROM conduits"):
        na, nb = id_to_name.get(za), id_to_name.get(zb)
        c_sl = max(zone_sl.get(na, 0.0), zone_sl.get(nb, 0.0))
        for nz in (na, nb):
            if nz is not None:
                incident[nz] = max(incident.get(nz, 0.0), c_sl)
    conn.close()

    return {n: incident.get(data.get("zone"), 0.0) for n, data in g.nodes(data=True)}


def compute_criticality(g: nx.DiGraph, w1: float = 0.4, w2: float = 0.4,
                        w3: float = 0.2) -> dict[int, dict]:
    """Crit(v) = w1*SL(v) + w2*Central(v)*Damage(v) + w3*ConduitSL(v),
    formal-problem-definition.md §2. The third term was added by A22/D20.

    Default weights are a starting point for the sensitivity sweep, not a
    claimed correct weighting — same status as the objective's alpha..epsilon.
    Returns per-node components so it stays visible which term drives a
    given asset's ranking."""
    central = compute_centrality(g)
    conduit_sl = load_conduit_sl(g)
    result = {}
    for n, data in g.nodes(data=True):
        sl = PLACEHOLDER_SL_BY_LEVEL.get(data["purdue_level"], 0.5)
        damage = PLACEHOLDER_DAMAGE_BY_TYPE.get(data["asset_type"], 0.3)
        c = central.get(n, 0.0)
        csl = conduit_sl.get(n, 0.0)
        crit = w1 * sl + w2 * c * damage + w3 * csl
        result[n] = {"name": data["name"], "sl": sl, "central": c, "damage": damage,
                     "conduit_sl": csl, "criticality": crit}
    return result


def write_computed_scores(g: nx.DiGraph, w1: float = 0.4, w2: float = 0.4, w3: float = 0.2,
                          db_path: Path = DB_PATH) -> None:
    """Persists central_score and criticality back to assets, per data-model.md's
    'computed scores are stored, not just derivable' design principle. sl_aggregate
    and damage_score get written too, so it's visible in the DB that these are
    placeholders, not silently missing.

    D24: the weight defaults now match compute_criticality(). They had stayed at
    the pre-D20 two-term values (0.5, 0.5) when D20 added the ConduitSL term, so
    this function silently inherited w3 = 0.2 and wrote criticality with weights
    summing to 1.2 -- different from what the optimizer computes. Nothing reads
    the stored column (the optimizer and API compute criticality live), so no
    result was affected; the stored values were simply wrong."""
    scores = compute_criticality(g, w1, w2, w3)
    conn = sqlite3.connect(db_path)
    for asset_id, s in scores.items():
        conn.execute(
            "UPDATE assets SET central_score=?, damage_score=?, sl_aggregate=?, criticality=? WHERE asset_id=?",
            (s["central"], s["damage"], s["sl"], s["criticality"], asset_id),
        )
    conn.commit()
    conn.close()


class CandidateSetError(RuntimeError):
    """The candidate set did not come through formal-problem-definition.md §4's
    filters, so no result computed on it may be reported (D26)."""


def load_candidate_locations(db_path: Path = DB_PATH, allow_legacy: bool = False) -> list[int]:
    """L — asset_ids marked is_candidate=1, after checking how they got there.

    D25 found that the seed had put assets into L that no human had scored.
    D26 makes that impossible to miss. The loader raises CandidateSetError when
    a member of L:
    - was never confirmed by a human in Screen 3, or whose four recorded answers
      do not pass Filter 1 when recomputed, path rule included. The stored flags
      alone are not trusted. This is the D25 bypass. It is allowed only with allow_legacy=True, which
      exists to reproduce numbers recorded before D26 from
      data/legacy/d25_candidate_set.sql;
    - has no Filter 2 (D22a) detectability score. This is never allowed,
      because the optimiser used to read a missing score silently as 0.0, i.e.
      as a perfectly safe decoy.

    An empty list means the A32 review has not produced any candidate yet."""
    from src.plausibility import passes, RubricError, KEYS   # local import: plausibility is a sibling package

    conn = sqlite3.connect(db_path)
    rows = conn.execute(f"""
        SELECT cl.asset_id, a.name, cl.human_confirmed, cl.passes_plausibility, cl.detectability_risk,
               {", ".join("cl.criterion_" + k for k in KEYS)},
               (SELECT COUNT(DISTINCT s.path_id) FROM attack_path_steps s WHERE s.asset_id = cl.asset_id)
        FROM candidate_locations cl JOIN assets a ON a.asset_id = cl.asset_id
        WHERE cl.is_candidate = 1 ORDER BY cl.asset_id""").fetchall()
    conn.close()

    def reviewed(r):
        # The stored flags are not trusted alone: the Filter 1 result is recomputed
        # from the four recorded answers, path rule included, and must agree.
        _, _, confirmed, passed, _, *answers, n_paths = r
        try:
            recomputed = passes(dict(zip(KEYS, answers)), n_paths)
        except RubricError:
            return False
        return bool(confirmed) and bool(passed) and recomputed

    unreviewed = [r[1] for r in rows if not reviewed(r)]
    if unreviewed and not allow_legacy:
        raise CandidateSetError(
            "These candidates did not come through Filter 1's human review: " + ", ".join(unreviewed)
            + ". To reproduce a number recorded before D26, load data/legacy/d25_candidate_set.sql into a "
              "freshly built database and pass --legacy-d25 to the script. Otherwise rebuild the database from "
              "schema.sql and seed.sql, and restore the review with scripts/review_io.py.")
    unscored = [r[1] for r in rows if r[4] is None]
    if unscored:
        raise CandidateSetError(
            "These candidates have no Filter 2 (D22a) detectability score: " + ", ".join(unscored)
            + ". A32 step 4 adds one for every asset that passes Filter 1 (02-detectability-rubric.md).")
    return [r[0] for r in rows]


def legacy_flag(argv: list[str]) -> bool:
    """Shared by the three scripts: strip --legacy-d25 from argv and report whether
    it was given. If it was, print the banner that marks the output as historical."""
    if "--legacy-d25" not in argv:
        return False
    argv.remove("--legacy-d25")
    print("=" * 78)
    print("LEGACY D25 CANDIDATE SET — reproduces numbers recorded before D26.")
    print("This set did not come through §4's filters (D25, Finding 2).")
    print("Nothing below is an evaluation result.")
    print("=" * 78)
    return True


def candidates_or_exit(db_path: Path = DB_PATH, allow_legacy: bool = False) -> list[int]:
    """For the scripts: load L, or explain why there is nothing to run on, and exit."""
    try:
        ids = load_candidate_locations(db_path, allow_legacy=allow_legacy)
    except CandidateSetError as e:
        raise SystemExit(f"Refusing to run: {e}")
    if not ids:
        raise SystemExit(
            "No candidate set yet. L is empty until the A32 review in Screen 3 confirms at least one asset "
            "(formal-problem-definition.md §4, D26). To reproduce a number recorded before D26, load "
            "data/legacy/d25_candidate_set.sql into the database and pass --legacy-d25.")
    return ids


def load_attack_paths(db_path: Path = DB_PATH) -> list[dict]:
    """P — each path as an ordered list of asset_ids, matching
    formal-problem-definition.md §3's (asset, technique) sequence structure."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    paths = []
    for p in conn.execute("SELECT * FROM attack_paths ORDER BY path_id"):
        steps = conn.execute(
            "SELECT * FROM attack_path_steps WHERE path_id=? ORDER BY step_order", (p["path_id"],)
        ).fetchall()
        paths.append({
            "path_id": p["path_id"], "name": p["name"],
            "asset_sequence": [s["asset_id"] for s in steps],
            "length": len(steps),
        })
    conn.close()
    return paths


if __name__ == "__main__":
    g = load_graph()
    print(f"Graph: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")
    scores = compute_criticality(g)
    print("\nCriticality by asset (w1=0.4, w2=0.4, w3=0.2; SL and damage are placeholders):")
    for s in sorted(scores.values(), key=lambda x: -x["criticality"]):
        print(f"  {s['name']:<24} SL={s['sl']:.2f}  Central={s['central']:.3f}  "
              f"Damage={s['damage']:.2f}  Crit={s['criticality']:.3f}")
    write_computed_scores(g)
    print("\nWrote central_score/damage_score/sl_aggregate/criticality back to assets table.")
