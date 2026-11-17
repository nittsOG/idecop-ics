"""
Freeze the evaluation inputs before Phase D (A12, A15; D37).

Writes data/freeze/manifest.json: the SHA-256 of every file that feeds the
evaluation, the date and the git commit. scripts/evaluate.py refuses to run
unless every listed file still matches. A frozen file that changes afterwards
needs its own decisions-log entry stating its effect, and a new freeze.

It refuses if any listed file has uncommitted changes, so the manifest always
describes a commit.

Usage:  uv run python scripts/freeze.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "freeze" / "manifest.json"

FIXED = [
    "requirements.lock",
    "data/schema.sql",
    "data/seed.sql",
    "data/review/plausibility_review.csv",
    "scripts/evaluate.py",
    "scripts/sweep.py",
    "scripts/run_comparison.py",
    "scripts/structure_check.py",
]
PACKAGES = ["src/graph_model", "src/optimizer", "src/evaluation", "src/plausibility"]


def frozen_files() -> list[str]:
    files = list(FIXED)
    for pkg in PACKAGES:
        files += sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / pkg).glob("*.py"))
    missing = [f for f in files if not (ROOT / f).exists()]
    if missing:
        raise SystemExit("frozen files missing: " + ", ".join(missing))
    return files


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def main() -> int:
    files = frozen_files()
    try:
        dirty = git("status", "--porcelain", "--", *files)
        commit = git("rev-parse", "HEAD")
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit("freeze.py needs a git clone of the repository, so the manifest can name a commit.")
    if dirty:
        raise SystemExit("These frozen files have uncommitted changes; commit them first:\n" + dirty)
    manifest = {
        "frozen_at": datetime.date.today().isoformat(),
        "commit": commit,
        "note": "Inputs and code frozen before Phase D (D37). scripts/evaluate.py refuses to run if any file "
                "below changes.",
        "files": {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(files)} files at commit {commit[:7]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
