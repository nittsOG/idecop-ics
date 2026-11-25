"""Self-test of the explanation layer (A6, D42, D43) against a stand-in Ollama server.

    uv run python scripts/explain_selftest.py

It needs the database with the committed review restored (L must not be
empty). It works on a temporary copy of the database and never calls a real
model, so it does not use up the counted run's first try (D39 item 8).
Checks: the number and asset checks on chosen cases; the template passing
both checks in all 20 cells; the client's request (declared model, thinking
off, temperature 0); the fallback on bad text, empty text, errors and
timeouts; the readiness check; the API route; and the counted-run guards.
"""
import json
import os
import shutil
import socket
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import src.explain as ex  # noqa: E402
from src.explain import ollama  # noqa: E402
from src.optimizer.baselines import greedy  # noqa: E402

PASSED = []


def ok(cond, what):
    if not cond:
        print(f"FAILED: {what}")
        sys.exit(1)
    PASSED.append(what)
    print(f"ok  {what}")


class Fake:
    def __init__(self):
        self.mode, self.text, self.delay, self.chats = "good", "OK", 0.0, []
        self.version, self.quant, self.values = "0.12.6", "Q4_K_M", [False, True]


def handler(fake):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send(self, code, obj=None, raw=None):
            body = raw if raw is not None else json.dumps(obj).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/api/version":
                self.send(200, {"version": fake.version})
            elif self.path == "/api/tags":
                self.send(200, {"models": [{"name": ex.DECLARED_MODEL, "model": ex.DECLARED_MODEL, "digest": "d1g3st"}]})
            else:
                self.send(404, {"error": "not found"})

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            if self.path == "/api/show":
                self.send(200, {"details": {"quantization_level": fake.quant, "parameter_size": "4.0B",
                                            "family": "qwen3"},
                                "capabilities": ["completion", "thinking"],
                                "thinking": {"values": fake.values, "default": True}})
            elif self.path == "/api/chat":
                fake.chats.append(body)
                if fake.delay:
                    time.sleep(fake.delay)
                if fake.mode == "http500":
                    return self.send(500, {"error": "model crashed"})
                if fake.mode == "garbled":
                    return self.send(200, raw=b"this is not json")
                msg = {"role": "assistant", "content": fake.text}
                if fake.mode == "thinking":
                    msg["thinking"] = "Let me count 7.77 things first."
                if fake.mode == "leak":   # a thinking-only model asked not to think (D43)
                    msg["content"] = "Hmm, the user wants a short answer.\n</think>\n\n" + fake.text
                self.send(200, {"model": body.get("model"), "message": msg, "done": True, "done_reason": "stop",
                                "total_duration": 2_500_000_000, "load_duration": 100_000_000,
                                "eval_duration": 2_000_000_000, "eval_count": 140, "prompt_eval_count": 760})
            else:
                self.send(404, {"error": "not found"})
    return H


class Server(ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):   # a timed-out client is expected
        pass


def main():
    db = ROOT / "data" / "deception_placement.db"
    if not db.exists():
        print("No database: run `uv run scripts/setup.py` and restore the review first.")
        sys.exit(1)
    tmp = Path(tempfile.mkdtemp(prefix="explain-selftest-"))
    fake = Fake()
    srv = Server(("127.0.0.1", 0), handler(fake))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}"
    os.environ["IDECOP_OLLAMA_URL"] = url
    os.environ.pop("IDECOP_EXPLAIN_MODEL", None)
    try:
        shutil.copy(db, tmp / "db.sqlite")
        run_tests(tmp, fake, url)
    finally:
        srv.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\nALL {len(PASSED)} EXPLANATION CHECKS PASSED")


def run_tests(tmp: Path, fake: Fake, url: str):
    dbc = tmp / "db.sqlite"
    try:
        ctx = ex.load_context(dbc)
    except Exception as e:  # noqa: BLE001
        print(f"The candidate set is not ready ({e}). Restore the committed review first:\n"
              "  uv run python scripts/review_io.py restore data/review/plausibility_review.csv")
        sys.exit(1)
    if not ctx["candidates"]:
        print("L is empty: restore the committed review first.")
        sys.exit(1)
    am = ex.aliases(ctx)
    L, P, crit, risk, W = ctx["candidates"], ctx["paths"], ctx["crit"], ctx["risk"], ex.DEFAULT_WEIGHTS
    place = {B: greedy(L, P, crit, risk, B, W)[0] for B in (1, 2, 3, 4)}
    f1, f3 = ex.build_facts(ctx, place[1], 1), ex.build_facts(ctx, place[3], 3)

    # --- the number check
    ok(ex.check_numbers("It scores F 2.42 and catches 5 of 5 attack paths at step 1.", f3, am) == [],
       "numbers stated in the facts pass")
    ok(ex.check_numbers("F is 2.4175, about the stated value.", f3, am) == [],
       "a more precise number passes when it rounds to a fact")
    ok(ex.check_numbers("F is 2.41.", f3, am) == ["2.41"], "a number that rounds differently fails")
    ok(ex.check_numbers("Coverage is 100%.", f3, am) == ["100"], "a converted percentage fails")
    ok(ex.check_numbers("It uses three decoys.", f1, am) == ["three"], "a number word not in the facts fails")
    ok(ex.check_numbers("P3 reaches Engineering WS-2 by T0866 under IEC 62443; PLC-01, PLC-03 (RTU) and "
                        "Industroyer2-class are named.", f3, am) == [],
       "digits inside path labels, asset names, technique IDs and the standard are not numbers")
    ok(ex.check_numbers("The first step is caught.", f1, am) == [], "ordinals are not counted")

    # --- the asset check
    ok(ex.check_assets("The DMZ Jump Host catches P2 and P5 before PLC-03 (RTU).", f1, am) == [],
       "assets of the placement and of the paths through it pass")
    ok(ex.check_assets("Engineering WS-2 would also help.", f1, am) == ["Engineering WS-2"],
       "an asset outside the run fails, matched longest first")
    ok(ex.check_assets("PLC-02 is protected too.", f3, am) == ["PLC-02"], "PLC-02, on no path, fails")
    ok(ex.check_assets("The RTU is the target of P2.", f1, am) == [], "an alias of an allowed asset passes")
    ok(ex.check_assets("The attacker starts outside.", f3, am) == [], "the word attacker is not an asset")

    # --- the template passes both checks in every cell
    bad = []
    for w, wt in {"default": W, "alpha=3": (3, 1, 1, 1, .1), "beta=3": (1, 3, 1, 1, .1),
                  "gamma=3": (1, 1, 3, 1, .1), "delta=3": (1, 1, 1, 3, .1)}.items():
        for B in (1, 2, 3, 4):
            x = greedy(L, P, crit, risk, B, wt)[0]
            f = ex.build_facts(ctx, x, B, wt)
            c = ex.check(ex.template_text(f, ctx), f, am)
            if not c["passed"]:
                bad.append((w, B, c))
    ok(not bad, f"the template passes both checks in all 20 cells {bad or ''}")

    # --- one explanation through the stand-in model
    fake.text = ex.template_text(f3, ctx) + " This placement was chosen because it catches every path early."
    fake.chats.clear()
    r = ex.explain_placement(ctx, place[3], 3, url=url, timeout=10)
    req = fake.chats[-1]
    ok(r["source"] == "model" and r["failures"] == [] and r["text"] == fake.text.strip(),
       "a faithful text is served as the model's")
    ok(req["model"] == ex.DECLARED_MODEL and req["think"] is False and req["stream"] is False
       and req["options"]["temperature"] == 0 and req["options"]["num_ctx"] == 4096,
       "the request carries the declared model, thinking off and temperature 0")
    ok([m["role"] for m in req["messages"]] == ["system", "user"] and req["messages"][1]["content"].startswith("FACTS"),
       "the request sends the system prompt and the facts")
    fake.text = ex.template_text(f3, ctx) + " It is 9.99 times better than random."
    r = ex.explain_placement(ctx, place[3], 3, url=url, timeout=10)
    ok(r["source"] == "template" and r["failures"] == ["numbers"] and r["checks"]["numbers"]["offending"] == ["9.99"],
       "a text with an invented number falls back to the template")
    fake.text = ex.template_text(f3, ctx) + " PLC-02 is covered as well."
    r = ex.explain_placement(ctx, place[3], 3, url=url, timeout=10)
    ok(r["source"] == "template" and r["failures"] == ["assets"], "a text naming an asset outside the run falls back")
    fake.mode, fake.text = "thinking", ex.template_text(f1, ctx)
    r = ex.explain_placement(ctx, place[1], 1, url=url, timeout=10)
    ok(r["deviations"] == ["thinking"] and r["source"] == "model",
       "a thinking trace is recorded as a deviation; the text is judged by the checks alone")
    fake.mode, fake.text = "leak", ex.template_text(f1, ctx)
    r = ex.explain_placement(ctx, place[1], 1, url=url, timeout=10)
    ok(r["deviations"] == ["thinking"],
       "reasoning leaked into the text, closed by </think> alone, is recorded as a deviation (D43)")
    ok(ex.thinking_trace("a</think>b") and ex.thinking_trace("<think>a") and ex.thinking_trace("a", "t")
       and not ex.thinking_trace("plain text"),
       "a thinking trace is found in the thinking field or by either think tag (D43)")
    fake.mode, fake.text = "good", "   "
    r = ex.explain_placement(ctx, place[1], 1, url=url, timeout=10)
    ok(r["source"] == "template" and "empty" in r["failures"], "an empty text falls back")
    for mode, label in (("http500", "an HTTP error"), ("garbled", "a reply that is not JSON")):
        fake.mode = mode
        r = ex.explain_placement(ctx, place[2], 2, url=url, timeout=10)
        ok(r["source"] == "template" and r["failures"] == ["model error"] and r["error"], f"{label} falls back")
    fake.mode, fake.delay = "good", 2.0
    r = ex.explain_placement(ctx, place[2], 2, url=url, timeout=0.5)
    ok(r["source"] == "template" and r["failures"] == ["model error"], "a timeout falls back")
    fake.delay = 0.0
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    closed = f"http://127.0.0.1:{s.getsockname()[1]}"
    s.close()
    r = ex.explain_placement(ctx, place[2], 2, url=closed, timeout=2)
    ok(r["source"] == "template" and r["failures"] == ["model error"], "an unreachable server falls back")

    # --- the readiness check
    fake.text = "OK"
    ok(ollama.preflight(url, timeout=5)["problems"] == [], "readiness: a ready server reports no problem")
    for attr, value, what in (("quant", "Q8_0", "a quantization other than Q4_K_M"),
                              ("values", [True], "a model that cannot switch thinking off")):
        old = getattr(fake, attr)
        setattr(fake, attr, value)
        ok(len(ollama.preflight(url, timeout=5)["problems"]) == 1, f"readiness: {what} is a problem")
        setattr(fake, attr, old)
    fake.mode = "thinking"
    ok(any("Thinking" in p for p in ollama.preflight(url, timeout=5)["problems"]),
       "readiness: thinking output in the warm-up is a problem (it also catches an Ollama too old for `think`)")
    fake.mode = "leak"
    ok(any("Thinking" in p for p in ollama.preflight(url, timeout=5)["problems"]),
       "readiness: reasoning leaked into the warm-up text is a problem (D43)")
    fake.mode = "good"

    # --- the API route, on the temporary database
    from fastapi import HTTPException
    import src.api.main as api
    api.DB_PATH = dbc
    ex.COUNTED_RESULTS = tmp / "explanations.json"
    run_id = api.optimize(api.OptimizePayload(method="proposed_greedy", budget=2))["run_id"]
    before = len(fake.chats)
    out = api.explain_run(run_id)
    ok(out["source"] == "template" and len(fake.chats) == before and "not called" in out["reason"],
       "API: before the counted run, the model is not called and the template is served")
    ex.COUNTED_RESULTS.write_text("{}", encoding="utf-8")
    f2 = ex.build_facts(ctx, place[2], 2)
    fake.text = ex.template_text(f2, ctx)
    out = api.explain_run(run_id)
    ok(out["source"] == "model" and out["reason"] is None and out["model"] == ex.DECLARED_MODEL,
       "API: after the counted run, a faithful text is served as the model's")
    fake.text = ex.template_text(f2, ctx) + " Coverage is 100%."
    out = api.explain_run(run_id)
    ok(out["source"] == "template" and "number check" in out["reason"] and out["model_text"],
       "API: a failing text is replaced by the template, with the reason and the rejected text")
    import sqlite3
    rows = sqlite3.connect(dbc).execute("SELECT model_used FROM explanations WHERE run_id=? ORDER BY explanation_id",
                                        (run_id,)).fetchall()
    ok([r[0] for r in rows] == ["template", ex.DECLARED_MODEL, "template"], "API: every explanation served is stored")
    cid = api.optimize(api.OptimizePayload(method="centrality", budget=2))["run_id"]
    for rid, code, what in ((cid, 422, "a baseline's run is refused"), (10**6, 404, "an unknown run is refused")):
        try:
            api.explain_run(rid)
            ok(False, f"API: {what}")
        except HTTPException as e:
            ok(e.status_code == code, f"API: {what} ({code})")

    # --- the counted-run guards
    import importlib.util
    spec = importlib.util.spec_from_file_location("explain_counted", ROOT / "scripts" / "explain_counted.py")
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    ec.COUNTED_RESULTS = ex.COUNTED_RESULTS
    try:
        ec.cmd_run(None)
        ok(False, "counted run: refuses when the record exists")
    except SystemExit:
        ok(True, "counted run: refuses when the record exists, before calling anything")
    ec.COUNTED_RESULTS = tmp / "missing.json"
    try:
        ec.cmd_rate(None)
        ok(False, "rating: refuses when there is nothing to rate")
    except SystemExit:
        ok(True, "rating: refuses when there is nothing to rate")

    # --- nothing frozen was touched
    spec = importlib.util.spec_from_file_location("evaluate", ROOT / "scripts" / "evaluate.py")
    ev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ev)
    ok(len(ev.check_frozen()["files"]) == 19, "the 19 frozen files still match the freeze manifest")


if __name__ == "__main__":
    main()
