# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
One-time setup for iDECOP-ICS (D29). Run it from anywhere inside the repository:

    uv run scripts/setup.py            set up, or bring an existing setup back in line
    uv run scripts/setup.py --check    check only; changes nothing except the
                                       frontend's build output (src/frontend/dist)

Steps, in order:

1. Environment. Creates .venv with the Python in .python-version (3.13) if it
   is missing or has another version. Then it makes .venv match
   requirements.lock exactly, Node.js included; uv checks every file's checksum.
2. Database. Builds data/deception_placement.db from data/schema.sql and
   data/seed.sql if it does not exist.
   - An existing database is never changed, because it holds your confirmations.
   - If it no longer matches the current schema and seed, the script says so.
     docs/04-setup-guide.md, "Your review data", explains how to rebuild it
     without losing the review.
3. Frontend. Installs the exact packages in src/frontend/package-lock.json,
   using the Node.js inside .venv.
4. Checks. Python and Node versions, the key imports, the database against
   the schema and seed, and a frontend build.

Re-run it after a pull that changes requirements.lock or
src/frontend/package-lock.json. It uses the standard library only, so
`python scripts/setup.py` works too, as long as uv is on PATH.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = "docs/04-setup-guide.md"
WINDOWS = os.name == "nt"
VENV = ROOT / ".venv"
VENV_BIN = VENV / ("Scripts" if WINDOWS else "bin")
VENV_PYTHON = VENV_BIN / ("python.exe" if WINDOWS else "python")
LOCK = ROOT / "requirements.lock"
DB = ROOT / "data" / "deception_placement.db"
SCHEMA = ROOT / "data" / "schema.sql"
SEED = ROOT / "data" / "seed.sql"
FRONTEND = ROOT / "src" / "frontend"

# Tables the seed fills. Comparing them with a fresh in-memory build shows
# whether the database on disk was built from the current schema and seed.
SEEDED_TABLES = ("zones", "conduits", "assets", "edges", "attack_paths", "attack_path_steps")
# Columns the code writes back after the build (src/graph_model stores its
# computed scores in assets). They are left out of the comparison.
COMPUTED_COLUMNS = {"assets": {"sl_aggregate", "central_score", "damage_score", "criticality"}}

warnings: list[str] = []


class Stop(Exception):
    """A step failed. The message says what to do."""


def say(text: str = "") -> None:
    print(text, flush=True)


def child_env() -> dict:
    """Environment for commands run inside .venv: its folder first on PATH, and
    no VIRTUAL_ENV inherited from `uv run`, which points at this script's own
    temporary environment."""
    env = dict(os.environ)
    env.pop("VIRTUAL_ENV", None)
    env["PATH"] = str(VENV_BIN) + os.pathsep + env.get("PATH", "")
    return env


def run(cmd: list, cwd: Path = ROOT, capture: bool = False) -> subprocess.CompletedProcess:
    if not capture:
        say("    $ " + " ".join([Path(str(cmd[0])).stem] + [str(c) for c in cmd[1:]]))
    return subprocess.run([str(c) for c in cmd], cwd=str(cwd), env=child_env(),
                          capture_output=capture, text=True)


def find_uv() -> str:
    uv = os.environ.get("UV") or shutil.which("uv")
    if not uv:
        raise Stop(f"uv was not found. Install it as described in {GUIDE}, step 1, "
                   "open a new terminal, and run this script again.")
    return uv


def wanted_python() -> str:
    path = ROOT / ".python-version"
    if not path.exists():
        raise Stop(".python-version is missing from the repository root. "
                   "Pull the latest commit and run this script again.")
    return path.read_text(encoding="utf-8").strip()


def venv_version() -> str | None:
    if not VENV_PYTHON.exists():
        return None
    r = run([VENV_PYTHON, "-c", "import sys; print('%d.%d.%d' % sys.version_info[:3])"], capture=True)
    return r.stdout.strip() if r.returncode == 0 else None


def same_version(have: str, want: str) -> bool:
    parts = want.split(".")
    return have.split(".")[:len(parts)] == parts


# ---------------------------------------------------------------- step 1
def step_environment(uv: str, check_only: bool) -> None:
    say("[1/4] Python environment (.venv)")
    want = wanted_python()
    have = venv_version()

    if check_only:
        if have is None:
            raise Stop("There is no working .venv. Run this script without --check to create it.")
        if not same_version(have, want):
            raise Stop(f".venv has Python {have}, not {want}. Run this script without --check to replace it.")
        say(f"    ok  .venv has Python {have}")
        r = run([uv, "pip", "sync", "--dry-run", "--python", VENV_PYTHON.relative_to(ROOT), LOCK.name], capture=True)
        if r.returncode != 0 or "Would make no changes" not in (r.stdout + r.stderr):
            raise Stop("The packages in .venv do not match requirements.lock. "
                       "Run this script without --check to bring them back in line.")
        say("    ok  the packages match requirements.lock")
        return

    if have is None or not same_version(have, want):
        if VENV.exists():
            state = "is not a working environment" if have is None else f"has Python {have}"
            say(f"    .venv {state}; replacing it with Python {want}")
            cmd = [uv, "venv", "--clear", "--python", want, VENV.relative_to(ROOT)]
        else:
            say(f"    creating .venv with Python {want}; uv downloads Python first if this computer lacks it")
            cmd = [uv, "venv", "--python", want, VENV.relative_to(ROOT)]
        if run(cmd).returncode != 0:
            raise Stop(f"uv could not create .venv. Read uv's message above, and see Troubleshooting in {GUIDE}.")
        have = venv_version()
        if have is None:
            raise Stop(f"uv reported success but .venv has no working Python. See Troubleshooting in {GUIDE}.")
    say(f"    ok  .venv has Python {have}")

    say("    installing exactly the packages in requirements.lock; uv checks each file's checksum")
    if run([uv, "pip", "sync", "--python", VENV_PYTHON.relative_to(ROOT), LOCK.name]).returncode != 0:
        raise Stop("uv could not install the locked packages. If it reported a hash mismatch, do not "
                   f"work around it: see Troubleshooting in {GUIDE}.")
    say("    ok  the packages match requirements.lock")


# ---------------------------------------------------------------- step 2
def build(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    conn.executescript(SEED.read_text(encoding="utf-8"))
    conn.commit()


def snapshot(conn: sqlite3.Connection) -> dict:
    snap = {"table definitions": conn.execute(
        "SELECT type, name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name").fetchall()}
    for table in SEEDED_TABLES:
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})")
                if r[1] not in COMPUTED_COLUMNS.get(table, set())]
        snap[table] = conn.execute(f"SELECT {', '.join(cols)} FROM {table} ORDER BY rowid").fetchall()
    snap["candidate cards"] = conn.execute(
        "SELECT asset_id, blind_first FROM candidate_locations ORDER BY asset_id").fetchall()
    return snap


def step_database(check_only: bool) -> None:
    say("[2/4] Database (data/deception_placement.db)")
    fresh = sqlite3.connect(":memory:")
    build(fresh)
    expected = snapshot(fresh)
    fresh.close()

    if not DB.exists():
        if check_only:
            raise Stop("There is no database. Run this script without --check to build it.")
        partial = DB.with_name(DB.name + ".building")
        if partial.exists():
            partial.unlink()
        conn = sqlite3.connect(str(partial))
        build(conn)
        conn.close()
        os.replace(partial, DB)          # appears only once complete
        say("    ok  built from data/schema.sql and data/seed.sql")

    conn = sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True)    # read-only: never changed here
    try:
        actual = snapshot(conn)
        total, confirmed, blind, blind_done = conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(human_confirmed = 1), 0), COALESCE(SUM(blind_first = 1), 0), "
            "COALESCE(SUM(blind_first = 1 AND human_confirmed = 1), 0) FROM candidate_locations").fetchone()
    except sqlite3.DatabaseError as e:
        actual, total = {"error": str(e)}, None
    finally:
        conn.close()

    if actual == expected:
        say(f"    ok  matches the current schema and seed: {total} candidate cards, "
            f"{confirmed} confirmed, {blind_done} of {blind} blind cards done")
        return
    differs = [k for k in expected if actual.get(k) != expected[k]] or ["the database could not be read"]
    message = ("The database does not match the current data/schema.sql and data/seed.sql "
               f"(different: {', '.join(differs)}). It was built from older files, or read in the wrong "
               "encoding. It was left untouched, because it holds your confirmations. Rebuild it as "
               f"described in {GUIDE}, 'Your review data': export, stop the backend, delete the file, "
               "run this script, restore.")
    warnings.append(message)
    say("    WARNING  " + message)


# ---------------------------------------------------------------- step 3
def venv_tool(name: str) -> str:
    path = shutil.which(name, path=str(VENV_BIN))
    if not path:
        raise Stop(f"{name} is missing from .venv. Run this script without --check, which installs Node.js "
                   "from requirements.lock.")
    return path


def step_frontend(check_only: bool) -> None:
    say("[3/4] Frontend packages (src/frontend)")
    npm = venv_tool("npm")
    if check_only:
        if not (FRONTEND / "node_modules").is_dir():
            raise Stop("The frontend packages are not installed. Run this script without --check.")
        say("    ok  src/frontend/node_modules is present")
        return
    say("    $ npm ci")
    r = run([npm, "ci"], cwd=FRONTEND, capture=True)
    out = (r.stdout + r.stderr).strip()
    if r.returncode != 0:
        say("\n".join("    " + line for line in out.splitlines()))
        raise Stop(f"npm could not install the frontend packages. Read npm's message above, and see "
                   f"Troubleshooting in {GUIDE}.")
    for line in out.splitlines():
        if line.startswith("added ") or "vulnerabilit" in line:
            say("    " + line.strip())
    say("    ok  installed the versions in package-lock.json")
    if "vulnerabilit" in out:
        say(f"    note: npm's audit warning is known and harmless for local use. Do not run `npm audit fix`; "
            f"see Troubleshooting in {GUIDE}.")


# ---------------------------------------------------------------- step 4
def step_checks() -> None:
    say("[4/4] Checks")
    want = wanted_python()
    have = venv_version()
    if not have or not same_version(have, want):
        raise Stop(f".venv has Python {have}, not {want}.")
    say(f"    ok  Python {have}")

    r = run([VENV_PYTHON, "-c", "import fastapi, uvicorn, pydantic, networkx, ortools, src.api.main"], capture=True)
    if r.returncode != 0:
        raise Stop("The backend's imports failed:\n" + r.stderr.strip()[-800:])
    say("    ok  the backend and its libraries import")

    pinned = re.search(r"^nodejs-wheel==(\S+)", LOCK.read_text(encoding="utf-8"), re.M)
    r = run([venv_tool("node"), "--version"], capture=True)
    node = r.stdout.strip()
    if r.returncode != 0 or (pinned and node != "v" + pinned.group(1)):
        raise Stop(f"Node.js in .venv reports {node or 'nothing'}, but requirements.lock pins "
                   f"{pinned.group(1) if pinned else 'a version this script cannot read'}.")
    say(f"    ok  Node.js {node}, from .venv")

    r = run([venv_tool("npm"), "run", "build"], cwd=FRONTEND, capture=True)
    if r.returncode != 0:
        raise Stop("The frontend build failed:\n" + (r.stdout + r.stderr).strip()[-800:])
    say("    ok  the frontend builds")


def main() -> int:
    parser = argparse.ArgumentParser(description="One-time setup for iDECOP-ICS (D29). See " + GUIDE + ".")
    parser.add_argument("--check", action="store_true",
                        help="check the setup without changing it (apart from the frontend's build output)")
    args = parser.parse_args()
    say(f"iDECOP-ICS setup in {ROOT}" + ("  (check only)" if args.check else ""))
    try:
        uv = find_uv()
        step_environment(uv, args.check)
        step_database(args.check)
        step_frontend(args.check)
        step_checks()
    except Stop as stop:
        say()
        say("SETUP STOPPED: " + str(stop))
        return 1
    say()
    if warnings:
        say(f"Setup finished with {len(warnings)} warning(s); read the WARNING above before scoring cards.")
    else:
        say("Setup complete." if not args.check else "Everything checks out.")
    say()
    say("Start the app from the repository root, in two terminals:")
    say("  terminal 1:  uv run python -m uvicorn src.api.main:app --reload")
    say("  terminal 2:  cd src/frontend")
    say("               uv run npm run dev")
    say("Then open http://localhost:5173 (not 127.0.0.1) and click Plausibility Review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
