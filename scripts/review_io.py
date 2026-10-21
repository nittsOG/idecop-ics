"""
The committed record of the Filter 1 review (A32, D26).

The database file is not tracked by git. Without this script, the reviewer's
confirmations would exist only on one machine, and the candidate set could
not be frozen or rebuilt.

    python scripts/review_io.py export [--out PATH] [--require-complete]
    python scripts/review_io.py check PATH
    python scripts/review_io.py restore PATH [--skip-changed]

export
    Writes every reviewed row to a CSV (default data/review/plausibility_review.csv):
    - the AI's suggestion, its reasoning and the model that produced it;
    - a blind card's first answers, which never change (D26);
    - the reviewer's final answers, reason and timestamp;
    - the Filter 1 result;
    - the context hash of the facts the card showed (D30), as context_sha256.
    On a blind card that is still open, the AI fields are left blank, so an
    export taken mid-review cannot reveal them. Re-import the notebook's CSV
    after restoring. Use --require-complete at freeze time; it refuses while
    any card is unconfirmed. It refuses a database built before D30.

check
    Runs every check restore runs, against a database built in memory from
    schema.sql and seed.sql, and changes nothing. Run it before deleting a
    database you mean to rebuild: it names any card whose facts have changed.

restore
    Rebuilds the review on a fresh database (schema.sql + seed.sql). It re-checks
    every row with the same rules the API applies (src/plausibility):
    - the sequential rule and the path rule;
    - the reason rule;
    - the combination rule, whose result must match the recorded one;
    - a confirmed blind card must carry its first (blind) answers, with a reason;
    - the context hash (D30). A record without one predates D30 and is refused
      whole. A card holding answers or an AI suggestion whose facts have since
      changed is refused, by name. With --skip-changed, used only when a
      decisions-log entry authorises the change, everything else is restored and
      those cards are left unscored, to be re-scored under D28's rule.
    It refuses if the database already holds any confirmation.
"""
import csv
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.plausibility import KEYS, check_sequence, check_answers, passes, reason_required, RubricError  # noqa: E402
from src.plausibility.prompt import asset_context, context_hash  # noqa: E402

DB = ROOT / "data" / "deception_placement.db"
SCHEMA = ROOT / "data" / "schema.sql"
SEED = ROOT / "data" / "seed.sql"
DEFAULT_OUT = ROOT / "data" / "review" / "plausibility_review.csv"
FIELDS = (["asset_id", "asset_name", "blind_first", "ai_model"]
          + [f"ai_suggested_{k}" for k in KEYS] + ["ai_reasoning"]
          + [f"blind_{k}" for k in KEYS] + ["blind_reason", "blind_confirmed_at"]
          + [f"criterion_{k}" for k in KEYS]
          + ["human_reason", "human_confirmed", "confirmed_at", "passes_plausibility", "is_candidate",
             "context_sha256"])
AI_FIELDS = [f"ai_suggested_{k}" for k in KEYS] + ["ai_reasoning", "ai_model"]


def export(out, require_complete):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT cl.*, a.name AS asset_name FROM candidate_locations cl
        JOIN assets a ON a.asset_id = cl.asset_id ORDER BY cl.asset_id""").fetchall()
    try:
        hashes = {r["asset_id"]: context_hash(asset_context(conn, r["asset_id"])) for r in rows}
    except sqlite3.OperationalError:
        raise SystemExit("This database was built before D30, which restarted the Filter 1 review. Do not export "
                         "it: stop the backend, delete data/deception_placement.db and run `uv run scripts/setup.py`.")
    finally:
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
            d = {k: r[k] for k in FIELDS if k != "context_sha256"}
            d["context_sha256"] = hashes[r["asset_id"]]
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


PRE_D30 = ("This database was built before D30, which restarted the Filter 1 review. Stop the backend, delete "
           "data/deception_placement.db and run `uv run scripts/setup.py`.")


def _carries_data(r):
    """A row with something to restore: final answers, blind answers, or an AI suggestion."""
    return bool(int(r["human_confirmed"] or 0) or r["blind_confirmed_at"] or r["ai_model"] or r["ai_reasoning"]
                or any(r[f"ai_suggested_{k}"] for k in KEYS))


def _replay(conn, path, skip_changed):
    """Applies the record at `path` to `conn`, checking every rule first.
    Returns (cards restored, names of cards whose facts have changed)."""
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    if not rows:
        raise SystemExit(f"{path} has no rows.")
    if "context_sha256" not in rows[0] or any(not r["context_sha256"] for r in rows):
        raise SystemExit("This record has no context hash, so it was made before D30, which restarted the Filter 1 "
                         "review. It cannot be restored.")
    current = {r["asset_id"]: r for r in conn.execute("""
        SELECT cl.asset_id, cl.blind_first, a.name,
               (SELECT COUNT(DISTINCT s.path_id) FROM attack_path_steps s WHERE s.asset_id = cl.asset_id) AS n_paths
        FROM candidate_locations cl JOIN assets a ON a.asset_id = cl.asset_id""")}
    changed = []
    for r in rows:
        aid, name = int(r["asset_id"]), r["asset_name"]
        cur = current.get(aid)
        if cur is None or cur["name"] != name:
            raise SystemExit(f"Asset {aid} ({name!r}) does not match this database's seed.")
        if int(r["blind_first"]) != cur["blind_first"]:
            raise SystemExit(f"{name}: blind_first differs from the seed's draw.")
        if r["context_sha256"] != context_hash(asset_context(conn, aid)) and _carries_data(r):
            changed.append(name)
    if changed and not skip_changed:
        raise SystemExit("The facts these cards were reviewed against have changed: " + ", ".join(changed)
                         + ". Their answers cannot be restored. Only if a decisions-log entry authorises the change, "
                         "run restore again with --skip-changed: everything else is restored, and these cards are "
                         "left unscored, to be re-scored. A blind card among them loses its agreement measure (D28).")
    n = 0
    for r in rows:
        aid, name = int(r["asset_id"]), r["asset_name"]
        if name in changed:
            continue
        cur = current[aid]
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
    return n, changed


def check(path):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    conn.executescript(SEED.read_text(encoding="utf-8"))
    n, changed = _replay(conn, path, skip_changed=True)
    conn.close()
    if changed:
        raise SystemExit(f"{path}: the facts these cards were reviewed against have changed: " + ", ".join(changed)
                         + f". A plain restore refuses them. Every other check passes, and {n} other confirmed card(s) "
                         "would be restored with --skip-changed, which needs a decisions-log entry authorising the "
                         "change (D28).")
    print(f"{path} passes every check against data/schema.sql and data/seed.sql: {n} confirmed card(s) would be restored.")


def restore(path, skip_changed=False):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    try:
        if conn.execute("SELECT COUNT(*) FROM candidate_locations WHERE human_confirmed = 1").fetchone()[0]:
            raise SystemExit("This database already holds confirmations. Rebuild it from schema.sql and seed.sql first.")
        n, changed = _replay(conn, path, skip_changed)
    except sqlite3.OperationalError:
        raise SystemExit(PRE_D30)
    conn.commit()
    conn.close()
    print(f"Restored {n} confirmed card(s) from {path}.")
    if changed:
        print("Left unscored because their facts have changed: " + ", ".join(changed) + ". Re-score them (D28).")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["export"]:
        out = DEFAULT_OUT
        if "--out" in args:
            out = Path(args[args.index("--out") + 1])
        export(out, "--require-complete" in args)
    elif args[:1] == ["check"] and len(args) == 2:
        check(args[1])
    elif args[:1] == ["restore"] and len(args) in (2, 3) and args[2:] in ([], ["--skip-changed"]):
        restore(args[1], skip_changed="--skip-changed" in args)
    else:
        raise SystemExit(__doc__)
