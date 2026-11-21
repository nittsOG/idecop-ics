"""The four counted explanations (D39 item 8; 03-evaluation-methodology.md §6).

    uv run python scripts/explain_counted.py check   # is Ollama ready? generates no explanation
    uv run python scripts/explain_counted.py run     # the counted run, once
    uv run python scripts/explain_counted.py rate    # your ratings of the four texts

`run` explains greedy's placement at B = 1, 2, 3 and 4 under the default
weights with the declared model (qwen3:4b, Q4_K_M, temperature 0, thinking
off), asks the model once per budget, applies the two checks and writes
everything to data/results/explanations.json. It refuses:
  - if that file exists: only the first generation after the commit counts;
  - if src/explain/ or this script has uncommitted changes: the prompt, the
    model and the checks must be committed before the counted run;
  - if a frozen file differs from the freeze manifest (D40);
  - if Ollama is not ready (`check` shows why).
`check` and `run` read IDECOP_OLLAMA_URL (docs/04-setup-guide.md §7).
"""
import argparse
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.explain import (COUNTED_RESULTS, DECLARED_MODEL, DECLARED_QUANTIZATION, DEFAULT_WEIGHTS,  # noqa: E402
                         GENERATION_OPTIONS, THINK, explain_placement, load_context)
from src.explain import ollama  # noqa: E402
from src.optimizer.baselines import greedy  # noqa: E402

BUDGETS = (1, 2, 3, 4)
FIXED = ["src/explain/__init__.py", "src/explain/ollama.py", "scripts/explain_counted.py"]
RATINGS = {"c": "clear", "p": "partly clear", "u": "unclear"}


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stop(msg: str) -> None:
    print(f"REFUSED: {msg}")
    sys.exit(1)


def git_commit() -> str:
    """The commit that fixes the prompt, the model and the checks (D39 item 8)."""
    try:
        subprocess.run(["git", "ls-files", "--error-unmatch", *FIXED], cwd=ROOT, check=True,
                       capture_output=True, text=True)
        dirty = subprocess.run(["git", "status", "--porcelain", "--", *FIXED], cwd=ROOT, check=True,
                               capture_output=True, text=True).stdout.strip()
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                              capture_output=True, text=True).stdout.strip()
    except FileNotFoundError:
        stop("git is not installed here; the counted run records the commit it ran from.")
    except subprocess.CalledProcessError:
        stop(f"these files must be committed first: {', '.join(FIXED)}")
    if dirty:
        stop("the prompt, the model or the checks have uncommitted changes. Commit them, or restore "
             f"them with `git checkout -- src/explain scripts/explain_counted.py`:\n{dirty}")
    return head


def check_frozen() -> None:
    spec = importlib.util.spec_from_file_location("evaluate", ROOT / "scripts" / "evaluate.py")
    ev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ev)
    try:
        ev.check_frozen()
    except SystemExit as e:
        stop(f"the frozen inputs do not match the freeze manifest ({e}).")


def write(data: dict) -> None:
    COUNTED_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    COUNTED_RESULTS.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def print_preflight(pf: dict) -> None:
    f = pf["found"]
    print(f"Ollama {f.get('ollama_version')} at {f['url']}")
    print(f"Model {f['model']}: quantization {f.get('quantization') or f.get('quantization_note')}, "
          f"{f.get('parameter_size')}, digest {f.get('digest')}")
    print(f"Thinking values: {f.get('thinking')}; capabilities: {f.get('capabilities')}")
    w = f.get("warm_up", {})
    print(f"Warm-up reply: {w.get('content', '').strip()!r} in {w.get('elapsed_seconds')} s "
          f"(model load {w.get('load_duration_seconds')} s)")
    for p in pf["problems"]:
        print(f"PROBLEM: {p}")


def cmd_check(_args) -> None:
    s = ollama.settings()
    if s["model"] != DECLARED_MODEL:
        print(f"Note: IDECOP_EXPLAIN_MODEL is {s['model']}; the counted run always uses {DECLARED_MODEL}.")
    try:
        pf = ollama.preflight(s["url"], DECLARED_MODEL, s["timeout"])
    except ollama.OllamaError as e:
        stop(f"{e}\nIs Ollama running, and does IDECOP_OLLAMA_URL point at it? See docs/04-setup-guide.md §7.")
    print_preflight(pf)
    done = COUNTED_RESULTS.exists()
    print(f"Counted run: {'already made (' + str(rel(COUNTED_RESULTS)) + ')' if done else 'not made yet'}")
    if pf["problems"]:
        sys.exit(1)
    print("READY" if not done else "Ready; the counted run is done, so the backend now calls the model.")


def cmd_run(_args) -> None:
    if COUNTED_RESULTS.exists():
        stop(f"{rel(COUNTED_RESULTS)} exists. The counted explanations are generated once: "
             "only the first generation after the commit counts (D39 item 8).")
    commit = git_commit()
    check_frozen()
    s = ollama.settings()
    try:
        pf = ollama.preflight(s["url"], DECLARED_MODEL, s["timeout"])
    except ollama.OllamaError as e:
        stop(f"{e}\nNothing was generated. Run `check` once Ollama is reachable.")
    print_preflight(pf)
    if pf["problems"]:
        stop("Ollama is not ready (problems above). Nothing was generated.")
    ctx = load_context()
    data = {"what": "The four counted explanations of D39 item 8: greedy's placement at B = 1-4, default weights.",
            "started_at": now(), "finished_at": None, "complete": False, "commit": commit,
            "declared": {"model": DECLARED_MODEL, "quantization": DECLARED_QUANTIZATION, "think": THINK,
                         "options": GENERATION_OPTIONS},
            "preflight": pf["found"], "explanations": [], "summary": None, "ratings": None}
    for B in BUDGETS:
        x, _ = greedy(ctx["candidates"], ctx["paths"], ctx["crit"], ctx["risk"], B, DEFAULT_WEIGHTS)
        print(f"B = {B}: asking {DECLARED_MODEL} once ...", flush=True)
        res = explain_placement(ctx, x, B, DEFAULT_WEIGHTS, "proposed_greedy", call_model=True,
                                url=s["url"], model=DECLARED_MODEL, timeout=s["timeout"])
        rec = {"budget": B, "placement": sorted(ctx["names"][a] for a in x), "generated_at": now(), **res}
        data["explanations"].append(rec)
        write(data)   # after every explanation, so that no first try is ever lost
        meta = res["model_meta"] or {}
        print(f"       {'passed both checks' if res['checks'] and res['checks']['passed'] else 'FAILED: ' + ', '.join(res['failures'])}"
              f"; {meta.get('elapsed_seconds', '-')} s")
    recs = data["explanations"]
    data["summary"] = {
        "passed_both_checks_first_try": sum(1 for r in recs if r["source"] == "model"),
        "of": len(recs),
        "failures_by_kind": dict(Counter(k for r in recs for k in r["failures"])),
        "deviations": dict(Counter(k for r in recs for k in r["deviations"])),
        "seconds_each": {r["budget"]: (r["model_meta"] or {}).get("elapsed_seconds") for r in recs},
    }
    data["finished_at"], data["complete"] = now(), True
    write(data)
    sm = data["summary"]
    print(f"\nPassed both checks on the first try: {sm['passed_both_checks_first_try']} of {sm['of']}")
    print(f"Failures by kind: {sm['failures_by_kind'] or 'none'}; deviations: {sm['deviations'] or 'none'}")
    print(f"Seconds each: {sm['seconds_each']}")
    print(f"Written: {rel(COUNTED_RESULTS)}. Next: `uv run python scripts/explain_counted.py rate`, "
          "then commit that file.")


def cmd_rate(_args) -> None:
    if not COUNTED_RESULTS.exists():
        stop("there is nothing to rate yet: run `run` first.")
    data = json.loads(COUNTED_RESULTS.read_text(encoding="utf-8"))
    if not data.get("complete"):
        stop("the counted run did not finish; tell Claude before doing anything else.")
    if data.get("ratings"):
        stop("the four texts are already rated. Ratings are recorded once.")
    print("Rate each text as a reader new to the project would find it: is the placement and its reason clear?\n"
          "You are rating the model's own text, whether or not it passed the checks.\n")
    values = {}
    for r in data["explanations"]:
        print(f"===== B = {r['budget']}: {', '.join(r['placement'])}")
        if r["model_text"] is None:
            print(f"(no model text: {r['error']})\n")
            values[str(r["budget"])] = None
            continue
        print(r["model_text"].strip() + "\n")
        while True:
            a = input("clear, partly clear or unclear? [c/p/u] ").strip().lower()
            if a in RATINGS:
                values[str(r["budget"])] = RATINGS[a]
                break
    data["ratings"] = {"rated_at": now(), "values": values,
                       "counts": dict(Counter(v for v in values.values() if v))}
    write(data)
    print(f"Recorded: {data['ratings']['counts']}. Commit {rel(COUNTED_RESULTS)} and tell Claude.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="is Ollama ready? (generates no explanation)").set_defaults(fn=cmd_check)
    sub.add_parser("run", help="the four counted explanations, once").set_defaults(fn=cmd_run)
    sub.add_parser("rate", help="record your ratings of the four texts").set_defaults(fn=cmd_rate)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
