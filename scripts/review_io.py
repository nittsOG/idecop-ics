"""
The committed record of the Filter 1 review (A32, D26).

The database file is not tracked by git. Without this script, the reviewer's
confirmations would exist only on one machine, and the candidate set could
not be frozen or rebuilt.

    python scripts/review_io.py export [--out PATH] [--require-complete]
    python scripts/review_io.py restore PATH

export
    Writes every reviewed row to a CSV (default data/review/plausibility_review.csv):
    - the AI's suggestion, its reasoning and the model that produced it;
    - a blind card's first answers, which never change (D26);
    - the reviewer's final answers, reason and timestamp;
    - the Filter 1 result.
    On a blind card that is still open, the AI fields are left blank, so an
    export taken mid-review cannot reveal them. Re-import the notebook's CSV
    after restoring. Use --require-complete at freeze time; it refuses while
    any card is unconfirmed.

restore
    Rebuilds the review on a fresh database (schema.sql + seed.sql). It re-checks
    every row with the same rules the API applies (src/plausibility):
    - the sequential rule and the path rule;
    - the reason rule;
    - the combination rule, whose result must match the recorded one;
    - a confirmed blind card must carry its first (blind) answers, with a reason.
    It refuses if the database already holds any confirmation.
"""
import csv
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.plausibility import KEYS, check_sequence, check_answers, passes, reason_required, RubricError  # noqa: E402

DB = ROOT / "data" / "deception_placement.db"
DEFAULT_OUT = ROOT / "data" / "review" / "plausibility_review.csv"
FIELDS = (["asset_id", "asset_name", "blind_first", "ai_model"]
          + [f"ai_suggested_{k}" for k in KEYS] + ["ai_reasoning"]
          + [f"blind_{k}" for k in KEYS] + ["blind_reason", "blind_confirmed_at"]
          + [f"criterion_{k}" for k in KEYS]
          + ["human_reason", "human_confirmed", "confirmed_at", "passes_plausibility", "is_candidate"])
AI_FIELDS = [f"ai_suggested_{k}" for k in KEYS] + ["ai_reasoning", "ai_model"]


def export(out, require_complete):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT cl.*, a.name AS asset_name FROM candidate_locations cl
        JOIN assets a ON a.asset_id = cl.asset_id ORDER BY cl.asset_id""").fetchall()
    conn.close()
    open_cards = [r["asset_name"] for r in rows if not r["human_confirmed"]]
    if require_complete and open_cards:
        raise SystemExit("Not complete; still unconfirmed: " + ", ".join(open_cards))
    out.parent.mkdir(parents=True, exist_ok=True)
    withheld = []
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            d = {k: r[k] for k in FIELDS}
            if r["blind_first"] and not r["blind_confirmed_at"]:
                if any(d[k] for k in AI_FIELDS):
                    withheld.append(r["asset_name"])
                for k in AI_FIELDS:
                    d[k] = None
            w.writerow(d)
    done = len(rows) - len(open_cards)
    passed = sum(1 for r in rows if r["human_confirmed"] and r["passes_plausibility"])
    print(f"Wrote {out}: {done} of {len(rows)} confirmed, {passed} pass Filter 1.")
    if open_cards:
        print("Still open: " + ", ".join(open_cards))
    if withheld:
        print("AI answers withheld for open blind cards: " + ", ".join(withheld)
              + ". Re-import the notebook's CSV after a restore.")


def restore(path):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    if conn.execute("SELECT COUNT(*) FROM candidate_locations WHERE human_confirmed = 1").fetchone()[0]:
        raise SystemExit("This database already holds confirmations. Rebuild it from schema.sql and seed.sql first.")
    current = {r["asset_id"]: r for r in conn.execute("""
        SELECT cl.asset_id, cl.blind_first, a.name,
               (SELECT COUNT(DISTINCT s.path_id) FROM attack_path_steps s WHERE s.asset_id = cl.asset_id) AS n_paths
        FROM candidate_locations cl JOIN assets a ON a.asset_id = cl.asset_id""")}
    n = 0
    for r in rows:
        aid, name = int(r["asset_id"]), r["asset_name"]
        cur = current.get(aid)
        if cur is None or cur["name"] != name:
            raise SystemExit(f"Asset {aid} ({name!r}) does not match this database's seed.")
        if int(r["blind_first"]) != cur["blind_first"]:
            raise SystemExit(f"{name}: blind_first differs from the seed's draw.")
        n_paths = cur["n_paths"]
        try:
            ai = check_sequence({k: r[f"ai_suggested_{k}"] or None for k in KEYS}) \
                if any(r[f"ai_suggested_{k}"] for k in KEYS) else (None,) * 4
        except RubricError as e:
            raise SystemExit(f"{name}: recorded AI suggestion breaks the rubric: {e}")
        conn.execute("""
            UPDATE candidate_locations SET
                ai_suggested_decoy_exists=?, ai_suggested_attacker_reach=?,
                ai_suggested_useful_signal=?, ai_suggested_reliable_indicator=?,
                ai_reasoning=?, ai_model=?
            WHERE asset_id=?""", (*ai, r["ai_reasoning"] or None, r["ai_model"] or None, aid))
        if r["blind_confirmed_at"]:
            if not cur["blind_first"]:
                raise SystemExit(f"{name}: has blind answers but is not a blind card.")
            try:
                blind = check_answers({k: r[f"blind_{k}"] or None for k in KEYS}, n_paths)
            except RubricError as e:
                raise SystemExit(f"{name}: recorded blind answers break the rubric: {e}")
            if not (r["blind_reason"] or "").strip():
                raise SystemExit(f"{name}: a blind card's first answers need a reason, and none is recorded.")
            conn.execute("""
                UPDATE candidate_locations SET
                    blind_decoy_exists=?, blind_attacker_reach=?, blind_useful_signal=?,
                    blind_reliable_indicator=?, blind_reason=?, blind_confirmed_at=?
                WHERE asset_id=?""", (*blind, r["blind_reason"], r["blind_confirmed_at"], aid))
        if not int(r["human_confirmed"] or 0):
            continue
        if cur["blind_first"] and not r["blind_confirmed_at"]:
            raise SystemExit(f"{name}: a confirmed blind card must carry its first (blind) answers.")
        answers = {k: r[f"criterion_{k}"] or None for k in KEYS}
        try:
            ordered = check_answers(answers, n_paths)
            passed = passes(answers, n_paths)
            ai_vals = None if cur["blind_first"] else dict(zip(KEYS, ai))
            triggers = reason_required(answers, ai_vals, bool(cur["blind_first"]), n_paths)
        except RubricError as e:
            raise SystemExit(f"{name}: recorded answers break the rubric: {e}")
        if triggers and not (r["human_reason"] or "").strip():
            raise SystemExit(f"{name}: a reason was required ({'; '.join(triggers)}) but none is recorded.")
        if int(r["passes_plausibility"]) != int(passed):
            raise SystemExit(f"{name}: recorded pass/fail does not match the combination rule.")
        conn.execute("""
            UPDATE candidate_locations SET
                criterion_decoy_exists=?, criterion_attacker_reach=?,
                criterion_useful_signal=?, criterion_reliable_indicator=?,
                human_reason=?, passes_plausibility=?, is_candidate=?, human_confirmed=1, confirmed_at=?
            WHERE asset_id=?""", (*ordered, r["human_reason"] or None, int(passed), int(passed),
                                  r["confirmed_at"], aid))
        n += 1
    conn.commit()
    conn.close()
    print(f"Restored {n} confirmed card(s) from {path}.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["export"]:
        out = DEFAULT_OUT
        if "--out" in args:
            out = Path(args[args.index("--out") + 1])
        export(out, "--require-complete" in args)
    elif args[:1] == ["restore"] and len(args) == 2:
        restore(args[1])
    else:
        raise SystemExit(__doc__)
