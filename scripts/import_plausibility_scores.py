"""
Loads the scoring notebook's CSV (notebooks/plausibility_scoring.ipynb) into
the ai_suggested_* columns of candidate_locations, as specified in
02-prototype-architecture.md §4.

It never writes criterion_*, human_reason or human_confirmed. Only a reviewer
in Screen 3 writes those (D12, D26).

    python scripts/import_plausibility_scores.py path/to/ai_suggestions.csv

Every check below is fatal:
- each row must name an existing asset by both id and name, so a reordered seed
  cannot shift suggestions onto the wrong asset;
- each suggestion must obey the rubric's sequential rule (src/plausibility);
- an AI suggestion already stored on a confirmed card is never changed or
  cleared. On a normal card the confirmation was made against it; on a blind
  card it is half of the agreement measure. An empty suggestion on a confirmed
  card is filled. For a blind card that is the expected order (blind cards
  first); for a card scored directly, it records what the AI would have said.

A row the notebook could not score clears any older suggestion on an
unconfirmed card, so a stale answer cannot pre-fill Screen 3.

It prints counts and asset names only, never the answers. For a blind card it
also withholds the detail of a rubric error, so running it cannot spoil a blind
card that is still open.
"""
import csv
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.plausibility import KEYS, check_sequence, RubricError  # noqa: E402

DB = ROOT / "data" / "deception_placement.db"


def main(path):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    if not rows:
        raise SystemExit(f"{path} has no rows")
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    current = {r["asset_id"]: r for r in conn.execute("""
        SELECT cl.*, a.name FROM candidate_locations cl JOIN assets a ON a.asset_id = cl.asset_id""")}

    planned, failed = [], []
    for r in rows:
        aid = int(r["asset_id"])
        if aid not in current or current[aid]["name"] != r["asset_name"]:
            raise SystemExit(f"Row for asset {aid} ({r['asset_name']!r}) does not match the database. "
                             "Was the notebook run against a different seed?")
        cur = current[aid]
        ok = r.get("parse_status", "ok") == "ok"
        if ok:
            values = {k: r.get(f"ai_suggested_{k}") or None for k in KEYS}
            try:
                ordered = check_sequence(values)
            except RubricError as e:
                detail = "details withheld: blind card" if cur["blind_first"] else str(e)
                raise SystemExit(f"Suggestion for {r['asset_name']} breaks the rubric ({detail}).")
            new = (ordered, r.get("ai_reasoning") or None, r.get("ai_model") or None)
        else:
            failed.append(r["asset_name"])
            new = ((None,) * 4, None, None)
        old = (tuple(cur[f"ai_suggested_{k}"] for k in KEYS), cur["ai_reasoning"], cur["ai_model"])
        has_old = any(old[0]) or old[1] or old[2]
        if cur["human_confirmed"] and has_old and old != new:
            raise SystemExit(f"{r['asset_name']} is confirmed and already has an AI suggestion. Refusing to change "
                             "or clear it: the review record would no longer match what was shown.")
        planned.append((*new, aid, r["asset_name"]))

    for ordered, reasoning, model, aid, _ in planned:
        conn.execute("""
            UPDATE candidate_locations SET
                ai_suggested_decoy_exists=?, ai_suggested_attacker_reach=?,
                ai_suggested_useful_signal=?, ai_suggested_reliable_indicator=?,
                ai_reasoning=?, ai_model=?
            WHERE asset_id=?""", (*ordered, reasoning, model, aid))
    conn.commit()
    conn.close()

    models = sorted({p[2] for p in planned if p[2]})
    print(f"Imported AI suggestions for {len(planned) - len(failed)} asset(s) from {path}.")
    print(f"Model: {', '.join(models) or 'not recorded'}")
    if failed:
        print(f"No usable suggestion for: {', '.join(failed)}. Those cards are scored directly, "
              "with a reason (route B for those assets, D26).")
    print("Answers are not printed here; review them in Screen 3.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
