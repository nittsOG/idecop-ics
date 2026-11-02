"""
graph_model — builds G = (V, E) as a real NetworkX graph from SQLite, and
computes the two derived quantities formal-problem-definition.md §1-2 define:
Central(v) and Crit(v). Read-only against the database, except
write_computed_scores(), which writes the computed scores back when this module
is run as a script (D13's note).

Central(v) is genuinely computed from the graph's real edges (fixed in D14 —
see 02-data-model.md's edges/conduits section). SL(v) and Damage(v) are NOT
computed here: formal-problem-definition.md §2 makes them elicited inputs, not
derived quantities. Since D33 (A37) they are declared design inputs read from
the database: a per-zone SL-T vector (zones.sl_t_vector) and a per-controller
share of the simulated process (assets.process_share). They are declarations
with stated grounds, not measurements. The placeholders keyed to Purdue level
and asset type that stood in for them until D33 are retired; they remain at
commit ebcaaa4.
"""
import json
import sqlite3
from pathlib import Path

import networkx as nx

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "deception_placement.db"


def sl_of(data) -> float:
    """SL(v), D33 (A37): the mean of zone(v)'s declared SL-T vector over
    FR1..FR7, divided by 4, the highest SL. A zone with no vector (External)
    gives 0. The vectors are consequence-led SL-T values, a declared adaptation,
    not an IEC 62443-3-2 allocation."""
    vec = data.get("zone_sl_t_vector")
    vec = json.loads(vec) if vec else None
    return (sum(vec) / len(vec)) / 4.0 if vec else 0.0


def damage_of(data) -> float:
    """Damage(v), D33 (A37): a controller's declared share of the simulated
    process (equal thirds over PLC-01, PLC-02 and PLC-03 (RTU), since the
    operating profile states no ratio); 0 for every other asset."""
    return data.get("process_share") or 0.0


def load_graph(db_path: Path = DB_PATH) -> nx.DiGraph:
    """G from the database. Refuses (ValueError) an edge that crosses between two
    zones with no recorded conduit: a conduit joins exactly two zones, and the
    model must agree with E (#330; D33, A38)."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    g = nx.DiGraph()
    for row in conn.execute("SELECT a.*, z.name AS zone_name, z.sl_t_vector AS zone_vec "
                            "FROM assets a JOIN zones z ON z.zone_id = a.zone_id"):
        g.add_node(row["asset_id"], name=row["name"], asset_type=row["asset_type"],
                   zone=row["zone_name"], purdue_level=row["purdue_level"],
                   is_physical=row["is_physical"], zone_sl_t_vector=row["zone_vec"],
                   process_share=row["process_share"])
    for row in conn.execute("SELECT * FROM edges"):
        g.add_edge(row["source_asset_id"], row["target_asset_id"],
                   protocol=row["protocol"], weight=row["weight"] or 1.0)
    recorded = {frozenset((r[0], r[1])) for r in conn.execute(
        "SELECT za.name, zb.name FROM conduits c JOIN zones za ON za.zone_id = c.zone_a_id "
        "JOIN zones zb ON zb.zone_id = c.zone_b_id")}
    conn.close()

    unrecorded = sorted({(g.nodes[u]["name"], g.nodes[v]["name"]) for u, v in g.edges()
                         if g.nodes[u]["zone"] != g.nodes[v]["zone"]
                         and frozenset((g.nodes[u]["zone"], g.nodes[v]["zone"])) not in recorded})
    if unrecorded:
        raise ValueError(
            "These edges cross a zone boundary that has no conduit row: "
            + ", ".join(f"{a} -> {b}" for a, b in unrecorded)
            + ". Record the conduit in data/seed.sql, or remove the edge (D33, A38).")
    return g


def compute_centrality(g: nx.DiGraph) -> dict[int, float]:
    """Central(v) — betweenness centrality, per D4's default choice, on its
    normalised [0, 1] scale, counting hops. D33 (A35): edge weights are recorded
    placeholders and no computation uses them. NetworkX reads a weight as a
    distance, so until D33 the rare-traffic links (weight 0.5) counted as
    shortcuts, the reverse of the traffic reading §1 gave them."""
    if g.number_of_edges() == 0:
        return {n: 0.0 for n in g.nodes}
    return nx.betweenness_centrality(g, weight=None, normalized=True)


def load_conduit_sl(g: nx.DiGraph, db_path: Path = DB_PATH) -> dict[int, float]:
    """ConduitSL(v) — the highest SL among the recorded conduits that v's own
    connections cross, in either direction; 0.0 for an asset with no such
    connection. A conduit's SL is the higher SL of the two zones it joins
    (sources.md #330, unchanged since D20).

    A22/D20 made conduits numeric: the novelty claim names them as a first-class
    input, and before D20 they entered no computation. D20 gave each asset the
    highest SL among the conduits incident to its ZONE. D33 (A38) replaced that
    step with this edge-level one. Once the OT DMZ–Control conduit was recorded,
    every internal zone touched Control, so the zone step gave every internal
    asset the same value, and the Historian inherited a boundary that none of
    its connections touches. §1 defines a conduit as the edges crossing a zone
    boundary, and §2 says the term exists because an asset at a high-SL
    boundary matters more than the same asset type deep inside one zone; the
    edge rule follows both. Modular in x, so it does not disturb submodularity."""
    conn = sqlite3.connect(db_path)
    # graph nodes carry the zone NAME; conduits reference zone IDs
    id_to_name = {r[0]: r[1] for r in conn.execute("SELECT zone_id, name FROM zones")}
    conduits = conn.execute("SELECT zone_a_id, zone_b_id FROM conduits").fetchall()
    conn.close()

    zone_sl: dict[str, float] = {}
    for _, data in g.nodes(data=True):
        z = data.get("zone")
        if z is not None:
            zone_sl[z] = max(zone_sl.get(z, 0.0), sl_of(data))

    pair_sl: dict[frozenset, float] = {}
    for za, zb in conduits:
        na, nb = id_to_name.get(za), id_to_name.get(zb)
        pair_sl[frozenset((na, nb))] = max(zone_sl.get(na, 0.0), zone_sl.get(nb, 0.0))

    out = {n: 0.0 for n in g.nodes}
    for u, v in g.edges():
        zu, zv = g.nodes[u].get("zone"), g.nodes[v].get("zone")
        if zu != zv and frozenset((zu, zv)) in pair_sl:
            s = pair_sl[frozenset((zu, zv))]
            out[u] = max(out[u], s)
            out[v] = max(out[v], s)
    return out


def compute_criticality(g: nx.DiGraph, w1: float = 0.25, w2: float = 0.25,
                        w3: float = 0.25, w4: float = 0.25) -> dict[int, dict]:
    """Crit(v) = w1*SL(v) + w2*Central(v) + w3*Damage(v) + w4*ConduitSL(v),
    formal-problem-definition.md §2.

    D33 (A40): the four factors are added, the form of #325. The earlier form
    multiplied Central by Damage, and every controller has zero betweenness, so
    no controller's process share ever counted. The equal weights are a
    declared convention, not a calibration, and they are not swept. Central
    keeps betweenness's [0, 1] scale, so its realised contribution is small on
    this graph; D33 records it.
    Returns per-node components so it stays visible which term drives a
    given asset's ranking."""
    central = compute_centrality(g)
    conduit_sl = load_conduit_sl(g)
    result = {}
    for n, data in g.nodes(data=True):
        sl = sl_of(data)
        damage = damage_of(data)
        c = central.get(n, 0.0)
        csl = conduit_sl.get(n, 0.0)
        crit = w1 * sl + w2 * c + w3 * damage + w4 * csl
        result[n] = {"name": data["name"], "sl": sl, "central": c, "damage": damage,
                     "conduit_sl": csl, "criticality": crit}
    return result


def write_computed_scores(g: nx.DiGraph, db_path: Path = DB_PATH) -> None:
    """Persists central_score and criticality back to assets, per data-model.md's
    'computed scores are stored, not just derivable' design principle. sl_aggregate
    and damage_score are written too, so the declared inputs behind each stored
    criticality are visible in the DB.

    D24 found that this function's own weight defaults had drifted from
    compute_criticality()'s, so it wrote criticality with weights summing to
    1.2. D33 removed its weight parameters, so the two can no longer differ.
    Nothing reads the stored column: the optimizer and the API compute
    criticality live."""
    scores = compute_criticality(g)
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


def load_candidate_locations(db_path: Path = DB_PATH) -> list[int]:
    """L — asset_ids marked is_candidate=1, after checking how they got there.

    D25 found that the seed had put assets into L that no human had scored.
    D26 makes that impossible to miss. The loader raises CandidateSetError when
    a member of L:
    - was never confirmed by a human in Screen 3, or whose four recorded answers
      do not pass Filter 1 when recomputed, path rule included. The stored flags
      alone are not trusted. This is the D25 bypass. Until D33 it was allowed
      only through the --legacy-d25 route, to reproduce numbers recorded before
      D26; D33 retired that route, and those numbers reproduce at commit ebcaaa4;
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
    if unreviewed:
        raise CandidateSetError(
            "These candidates did not come through Filter 1's human review: " + ", ".join(unreviewed)
            + ". Rebuild the database from schema.sql and seed.sql, and restore the review with "
              "scripts/review_io.py. A number recorded before D26 reproduces only at commit ebcaaa4, "
              "with data/legacy/d25_candidate_set.sql and --legacy-d25 (D33 retired that route).")
    unscored = [r[1] for r in rows if r[4] is None]
    if unscored:
        raise CandidateSetError(
            "These candidates have no Filter 2 (D22a) detectability score: " + ", ".join(unscored)
            + ". A32 step 4 adds one for every asset that passes Filter 1 (02-detectability-rubric.md).")
    return [r[0] for r in rows]


def candidates_or_exit(db_path: Path = DB_PATH) -> list[int]:
    """For the scripts: load L, or explain why there is nothing to run on, and exit."""
    try:
        ids = load_candidate_locations(db_path)
    except CandidateSetError as e:
        raise SystemExit(f"Refusing to run: {e}")
    if not ids:
        raise SystemExit(
            "No candidate set yet. L is empty until the A32 review in Screen 3 confirms at least one asset "
            "(formal-problem-definition.md §4, D26). On a freshly built database, restore the committed "
            "review with: python scripts/review_io.py restore data/review/plausibility_review.csv")
    return ids


def load_attack_paths(db_path: Path = DB_PATH) -> list[dict]:
    """P — each path as an ordered list of asset_ids, matching
    formal-problem-definition.md §3's (asset, technique) sequence structure,
    with its declared target (D33, A36): the asset whose compromise or use is
    the scenario's stated objective. CritProt credits a caught path with its
    target's criticality.

    Refuses (ValueError) a path whose target is not one of its steps, and a path
    of fewer than two steps, since Early_p = (n - s)/(n - 1) needs n >= 2 (D33)."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    paths = []
    for p in conn.execute("SELECT * FROM attack_paths ORDER BY path_id"):
        steps = conn.execute(
            "SELECT * FROM attack_path_steps WHERE path_id=? ORDER BY step_order", (p["path_id"],)
        ).fetchall()
        seq = [s["asset_id"] for s in steps]
        if len(seq) < 2:
            raise ValueError(f"{p['name']}: a path needs at least two steps (D33: Early = (n - s)/(n - 1))")
        if p["target_asset_id"] not in seq:
            raise ValueError(f"{p['name']}: its target is not one of its steps (D33, A36)")
        paths.append({
            "path_id": p["path_id"], "name": p["name"],
            "asset_sequence": seq,
            "length": len(seq),
            "target": p["target_asset_id"],
        })
    conn.close()
    return paths


if __name__ == "__main__":
    g = load_graph()
    print(f"Graph: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")
    scores = compute_criticality(g)
    print("\nCriticality by asset (equal weights 0.25; SL and Damage are declared inputs, D33):")
    for s in sorted(scores.values(), key=lambda x: -x["criticality"]):
        print(f"  {s['name']:<24} SL={s['sl']:.3f}  Central={s['central']:.3f}  "
              f"Damage={s['damage']:.3f}  ConduitSL={s['conduit_sl']:.3f}  Crit={s['criticality']:.3f}")
    write_computed_scores(g)
    print("\nWrote central_score/damage_score/sl_aggregate/criticality back to assets table.")
