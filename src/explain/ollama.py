"""A minimal client for a local Ollama server (standard library only).

Settings come from the environment, so that the backend in the Kali VM can use
an Ollama server running on the Windows host (docs/04-setup-guide.md §7):
  IDECOP_OLLAMA_URL       default http://127.0.0.1:11434
  IDECOP_EXPLAIN_MODEL    default qwen3:4b (the counted run always uses qwen3:4b)
  IDECOP_EXPLAIN_TIMEOUT  seconds per request, default 300

API fields as documented at docs.ollama.com (sources.md #1050, #1051, #1053): POST
/api/chat takes `think` (false asks for no thinking output) and returns
`message.content` and `message.thinking`; durations are in nanoseconds.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from src.explain import DECLARED_MODEL, DECLARED_QUANTIZATION, GENERATION_OPTIONS, THINK

DEFAULT_URL = "http://127.0.0.1:11434"
DEFAULT_TIMEOUT = 300.0


class OllamaError(Exception):
    """The server could not be reached, refused the request or answered badly."""


def settings() -> dict:
    return {"url": os.environ.get("IDECOP_OLLAMA_URL", DEFAULT_URL).rstrip("/"),
            "model": os.environ.get("IDECOP_EXPLAIN_MODEL", DECLARED_MODEL),
            "timeout": float(os.environ.get("IDECOP_EXPLAIN_TIMEOUT", DEFAULT_TIMEOUT))}


def _request(url: str, path: str, payload: dict | None, timeout: float) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url.rstrip("/") + path, data=data,
                                 headers={"Content-Type": "application/json"},
                                 method="GET" if payload is None else "POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        raise OllamaError(f"Ollama at {url} answered {e.code} on {path}: {detail}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        reason = getattr(e, "reason", e)
        raise OllamaError(f"Cannot reach Ollama at {url} ({path}): {reason}") from None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise OllamaError(f"Ollama at {url} sent a reply on {path} that is not JSON") from None


def chat(system: str, user: str, *, url: str | None = None, model: str = DECLARED_MODEL,
         timeout: float | None = None) -> dict:
    """One non-streamed chat request with the declared settings: temperature 0,
    thinking off, and the fixed context and length limits."""
    s = settings()
    url = url or s["url"]
    timeout = timeout or s["timeout"]
    payload = {"model": model, "stream": False, "think": THINK, "options": dict(GENERATION_OPTIONS),
               "keep_alive": "10m",
               "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    t0 = time.perf_counter()
    reply = _request(url, "/api/chat", payload, timeout)
    elapsed = time.perf_counter() - t0
    message = reply.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise OllamaError(f"Ollama at {url} sent a chat reply without message.content")
    ns = lambda k: (reply.get(k) or 0) / 1e9  # noqa: E731
    return {"content": message["content"], "thinking": message.get("thinking") or "",
            "elapsed_seconds": round(elapsed, 3), "total_duration_seconds": round(ns("total_duration"), 3),
            "load_duration_seconds": round(ns("load_duration"), 3),
            "eval_duration_seconds": round(ns("eval_duration"), 3),
            "prompt_eval_count": reply.get("prompt_eval_count"), "eval_count": reply.get("eval_count"),
            "done_reason": reply.get("done_reason"), "reply_model": reply.get("model")}


def preflight(url: str | None = None, model: str = DECLARED_MODEL, timeout: float | None = None) -> dict:
    """Checks the server and the declared model, then asks for one word to warm
    the model up. It generates no explanation, so it does not use up the first try
    (D39 item 8). Returns what it found and a list of problems; empty means ready."""
    s = settings()
    url = url or s["url"]
    timeout = timeout or s["timeout"]
    found, problems = {"url": url, "model": model}, []
    found["ollama_version"] = _request(url, "/api/version", None, timeout).get("version")
    show = _request(url, "/api/show", {"model": model}, timeout)
    details = show.get("details") or {}
    found["quantization"] = details.get("quantization_level")
    found["parameter_size"] = details.get("parameter_size")
    found["family"] = details.get("family")
    found["capabilities"] = show.get("capabilities")
    found["thinking"] = show.get("thinking")
    if found["quantization"] is None:
        found["quantization_note"] = "not reported by this Ollama version; D37 recorded qwen3:4b as Q4_K_M"
    elif str(found["quantization"]).upper() != DECLARED_QUANTIZATION:
        problems.append(f"{model} is {found['quantization']}, not the declared {DECLARED_QUANTIZATION}.")
    thinking = found["thinking"]
    if isinstance(thinking, dict) and isinstance(thinking.get("values"), list) and False not in thinking["values"]:
        problems.append(f"{model} cannot switch thinking off (its thinking values are {thinking['values']}).")
    tags = _request(url, "/api/tags", None, timeout)
    found["digest"] = next((m.get("digest") for m in tags.get("models", [])
                            if model in (m.get("name"), m.get("model"))), None)
    smoke = chat("Reply with exactly one word.", "Say OK.", url=url, model=model, timeout=timeout)
    found["warm_up"] = {k: smoke[k] for k in ("content", "elapsed_seconds", "load_duration_seconds")}
    # An Ollama too old to know `think` ignores it, and qwen3 then thinks by default,
    # so this also catches a server that cannot switch thinking off (#1051, #1053).
    if smoke["thinking"] or "<think>" in smoke["content"]:
        problems.append("Thinking output appeared although thinking was switched off. Update Ollama.")
    if not smoke["content"].strip():
        problems.append("The model returned an empty reply to the warm-up request.")
    return {"found": found, "problems": problems}
