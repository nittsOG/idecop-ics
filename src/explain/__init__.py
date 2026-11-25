"""The explanation layer (A6; D37 item 6, D39 item 8; 03-evaluation-methodology.md §6).

A local language model explains a placement that the optimiser has already
made. It never chooses, changes or vetoes a placement (D6; 02-ai-role.md §1).

Every explanation is checked before it is shown (§6):
  - the number check: every number in the text must equal a number in the
    facts the model was given, both rounded to two decimals;
  - the asset check: every asset the text names must belong to the run: the
    placement, the centrality comparator's placement, or an attack path that
    passes through either.
A text that fails either check, or no text at all, is replaced by a template
built from the same facts, and the failure is reported.

This package is not an evaluation input (D37 item 6). It sits outside the four
frozen packages and only reads them.

D39 item 8: the prompt, the declared model and the two checks in this package
and in `ollama.py` are committed before the four counted explanations
(`scripts/explain_counted.py run`) are generated. Changing any of them after
that commit needs a decisions-log entry. D42 records the rules below in words.
"""
from __future__ import annotations

import re
import sqlite3
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from src.graph_model import (compute_criticality, load_attack_paths, load_candidate_locations,
                             load_graph)
from src.optimizer.baselines import centrality_baseline, random_baseline
from src.optimizer.metrics import score

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "deception_placement.db"
# The four counted explanations' record (D39 item 8). Until it exists, the API
# serves the template and does not call the model, so that the counted run is
# the first generation after the commit that fixes the prompt and checks.
COUNTED_RESULTS = ROOT / "data" / "results" / "explanations.json"

DECLARED_MODEL = "qwen3:4b-q4_K_M"    # D43; D37 item 6 and D39 item 8 named qwen3:4b, a thinking-only model
DECLARED_QUANTIZATION = "Q4_K_M"      # D39 item 8; sources.md #1059
THINK = False                         # thinking off (D37 item 6)
GENERATION_OPTIONS = {"temperature": 0, "seed": 0, "num_ctx": 4096, "num_predict": 512}
DEFAULT_WEIGHTS = (1.0, 1.0, 1.0, 1.0, 0.1)
PROPOSED_METHODS = ("proposed_greedy", "proposed_distorted_greedy", "proposed_milp")
# Methods whose stopping rule makes "no further decoy raises F" true when they
# place fewer decoys than the budget: greedy stops only then, and the MILP is
# optimal. Distorted greedy can stop for its distortion factor (D23), so it gets
# no reason sentence.
_STOPS_ONLY_WITHOUT_GAIN = ("proposed_greedy", "proposed_milp")

SYSTEM_PROMPT = (
    "You are explaining a cybersecurity decoy-placement decision to a security analyst who is new "
    "to this network. A deterministic optimisation algorithm has already selected which network "
    "locations receive decoys. That decision is final and outside your control. Your only task is "
    "to explain why this placement was chosen and how it compares with two baseline strategies, in "
    "plain language.\n\n"
    "Do not suggest a different placement. Do not recommend more or fewer decoys. Do not question "
    "the algorithm's choice.\n\n"
    "Use only the facts you are given. Write every number as digits, exactly as it appears in the "
    "facts. Do not calculate new numbers, convert numbers to percentages or round them differently. "
    "Name only the assets that appear in the facts."
)

TASK = (
    "Write a short explanation, under 150 words, covering: (1) which locations were chosen and "
    "which attack paths each one catches; (2) how early the attack paths are caught; (3) how the "
    "placement compares with the centrality and random baselines."
)

NUMBER_WORDS = {w: Decimal(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty".split())}
NUMBER_WORDS["thirty"] = Decimal(30)

_NUMBER = re.compile(r"(?<![A-Za-z0-9.])\d+(?:\.\d+)?(?![A-Za-z0-9])")
_WORD = re.compile(r"[A-Za-z]+")
# Identifiers whose digits are not quantities: attack-path labels (P1-P5),
# ATT&CK technique IDs and the IEC standard's number.
_IDENTIFIERS = (re.compile(r"\bP\d+\b"), re.compile(r"\bT\d{4}(?:\.\d{3})?\b"),
                re.compile(r"\b(?:ISA\s*/\s*)?IEC[\s-]*\d+(?:-\d+)*\b", re.I),
                re.compile(r"\b62443(?:-\d+)*\b"))


# ---------------------------------------------------------------- the run's context

def load_context(db_path: Path = DB_PATH) -> dict:
    """What the facts are built from, read the way /optimize reads it. Raises
    CandidateSetError (from graph_model) when L is not a reviewed candidate set."""
    g = load_graph(db_path)
    crit = compute_criticality(g)
    candidates = load_candidate_locations(db_path)
    paths = load_attack_paths(db_path)
    conn = sqlite3.connect(db_path)
    try:
        risk = {a: (r or 0.0) for a, r in conn.execute(
            "SELECT asset_id, detectability_risk FROM candidate_locations")}
        labels = {name: desc for name, desc in conn.execute(
            "SELECT name, description FROM attack_paths")}
    finally:
        conn.close()
    names = {n: g.nodes[n]["name"] for n in g.nodes}
    assets = {n for n in g.nodes if g.nodes[n]["asset_type"] != "Attacker"}
    return {"graph": g, "crit": crit, "central": {n: crit[n]["central"] for n in crit},
            "candidates": candidates, "paths": paths, "risk": risk, "labels": labels,
            "names": names, "assets": assets}


def aliases(ctx: dict) -> dict[str, int]:
    """Every way the asset check recognises an asset as named: its recorded name,
    and for a name of the form "X (Y)" also X and Y ("PLC-03", "RTU"). The
    Attacker node is not an asset and is not listed."""
    out = {}
    for a in ctx["assets"]:
        name = ctx["names"][a]
        out[name] = a
        m = re.fullmatch(r"(.+?)\s*\((.+)\)", name)
        if m:
            out[m.group(1)] = a
            out[m.group(2)] = a
    return out


# ---------------------------------------------------------------- the facts

def _fmt(v: float) -> str:
    return f"{v:.2f}"


def _n(count: int, noun: str) -> str:
    return f"{count} {noun}" + ("" if count == 1 else "s")


def _short(label: str) -> tuple[str, str]:
    head, _, tail = label.partition(":")
    return head.strip(), tail.strip()


def _caught(x: set[int], paths: list[dict]) -> list[tuple[dict, int, int]]:
    """(path, step, asset) for each path x catches: the first step whose asset holds
    a decoy, 1-based, as metrics._intercepted_paths counts it."""
    out = []
    for p in paths:
        for i, a in enumerate(p["asset_sequence"]):
            if a in x:
                out.append((p, i + 1, a))
                break
    return out


def _scores(m) -> str:
    return (f"F {_fmt(m['f_score'])}; coverage {_fmt(m['coverage'])}; early detection {_fmt(m['early'])}; "
            f"critical-asset protection {_fmt(m['crit_prot'])}; detectability risk {_fmt(m['risk'])}; "
            f"cost {_fmt(m['cost'])}")


def _as_dict(metrics) -> dict:
    return {k: getattr(metrics, k) for k in ("f_score", "coverage", "early", "crit_prot", "risk", "cost")}


def build_facts(ctx: dict, placement, budget: int, weights=DEFAULT_WEIGHTS,
                method: str = "proposed_greedy") -> dict:
    """The facts the model is given, as text, and what the checks need. The
    comparators are computed here with the frozen baselines: centrality's top-B
    placement, and the mean of the 30 random placements (seed 42)."""
    names, paths = ctx["names"], ctx["paths"]
    weights = tuple(float(w) for w in weights)
    x = set(placement)
    nm = lambda xs: ", ".join(sorted(names[a] for a in xs))  # noqa: E731
    m = _as_dict(score(x, paths, ctx["crit"], ctx["risk"], weights))
    cx, cmet = centrality_baseline(ctx["candidates"], ctx["central"], paths, ctx["crit"], ctx["risk"],
                                   budget, weights)
    c = _as_dict(cmet)
    _, rres, _ = random_baseline(ctx["candidates"], paths, ctx["crit"], ctx["risk"], budget, weights)
    r = {k: sum(getattr(t, k) for t in rres) / len(rres)
         for k in ("f_score", "coverage", "early", "crit_prot", "risk", "cost")}
    caught = _caught(x, paths)
    caught_names = {p["name"] for p, _, _ in caught}
    c_caught = [p["name"] for p, _, _ in _caught(set(cx), paths)]
    allowed = set(x) | set(cx)
    for p in paths:
        if set(p["asset_sequence"]) & (set(x) | set(cx)):
            allowed |= set(p["asset_sequence"])

    lines = [
        f"Network: {len(ctx['candidates'])} candidate decoy positions; {len(paths)} modelled attack paths.",
        "Objective weights: the defaults." if weights == DEFAULT_WEIGHTS else
        "Objective weights: alpha {:g}, beta {:g}, gamma {:g}, delta {:g}, epsilon {:g}.".format(*weights),
        "F is the optimiser's objective: it rewards catching attack paths, catching them early and "
        "protecting critical assets, and penalises detectability risk and the number of decoys.",
        f"Budget: at most {_n(budget, 'decoy')}.",
        f"Chosen placement: {nm(x) or 'none'} ({_n(len(x), 'decoy')}), selected by the optimiser to maximise F.",
    ]
    if len(x) < budget and method in _STOPS_ONLY_WITHOUT_GAIN:
        lines.append(f"Fewer decoys than the budget: the optimiser placed {len(x)} because no further "
                     "decoy raises F.")
    lines.append(f"Scores of the chosen placement: {_scores(m)}. Attack paths caught: {len(caught)} of "
                 f"{len(paths)}.")
    if caught:
        lines.append("Attack paths caught by the chosen placement:")
        for p, step, a in caught:
            head, tail = _short(ctx["labels"].get(p["name"], ""))
            lines.append(f"- {p['name']}, {head} ({tail}): caught at step {step} of {p['length']}, at "
                         f"{names[a]}; target {names[p['target']]}.")
    missed = [p for p in paths if p["name"] not in caught_names]
    lines.append("Attack paths not caught by the chosen placement: " + (
        ", ".join(f"{p['name']} ({_short(ctx['labels'].get(p['name'], ''))[0]})" for p in missed)
        if missed else "none") + ".")
    lines.append("Baselines compared: 2.")
    lines.append(f"Centrality baseline: the {_n(budget, 'candidate position')} with the highest betweenness "
                 f"centrality, that is, the ones the most shortest network routes pass through: {nm(cx)}. "
                 f"Scores: {_scores(c)}. Attack paths caught: {len(c_caught)} of {len(paths)}"
                 + (f" ({', '.join(c_caught)})." if c_caught else "."))
    lines.append(f"Random baseline: the average of 30 random placements of {_n(budget, 'decoy')}. "
                 f"Scores: {_scores(r)}.")
    return {"text": "\n".join(lines), "budget": budget, "weights": weights, "method": method,
            "placement": sorted(x), "metrics": m, "caught": [(p["name"], s, a) for p, s, a in caught],
            "missed": [p["name"] for p in missed],
            "centrality": {"placement": sorted(cx), "metrics": c, "caught": c_caught},
            "random_mean": r, "allowed_assets": sorted(allowed)}


def build_prompt(facts: dict) -> tuple[str, str]:
    return SYSTEM_PROMPT, f"FACTS\n{facts['text']}\n\nTASK\n{TASK}"


# ---------------------------------------------------------------- the two checks

def _mask(text: str, alias_map: dict[str, int]) -> str:
    """Blank out asset names (longest first, so "Engineering WS-2" is not read as
    "Engineering WS") and identifiers, so that their digits are not read as numbers."""
    for name in sorted(alias_map, key=len, reverse=True):
        text = re.sub(r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])", " ", text, flags=re.I)
    for pattern in _IDENTIFIERS:
        text = pattern.sub(" ", text)
    return text


def numbers(text: str, alias_map: dict[str, int]) -> list[str]:
    """The numbers in a text, as written: numerals, and the number words zero to
    twenty and thirty. Ordinals ("first step") are not counted."""
    t = _mask(text, alias_map)
    found = [m.group(0) for m in _NUMBER.finditer(t)]
    found += [w for w in _WORD.findall(t) if w.lower() in NUMBER_WORDS]
    return found


def _value(token: str) -> Decimal:
    v = NUMBER_WORDS.get(token.lower())
    return v if v is not None else Decimal(token)


def _round2(v: Decimal) -> Decimal:
    return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def check_numbers(text: str, facts: dict, alias_map: dict[str, int]) -> list[str]:
    """The number check: the numbers in the text that, rounded to two decimals,
    equal no number in the facts rounded to two decimals. Empty means it passes."""
    allowed = {_round2(_value(t)) for t in numbers(facts["text"], alias_map)}
    return [t for t in numbers(text, alias_map) if _round2(_value(t)) not in allowed]


def named_assets(text: str, alias_map: dict[str, int]) -> dict[str, int]:
    """Assets the text names: an alias appearing as a whole word, any case,
    matched longest first."""
    out = {}
    for name in sorted(alias_map, key=len, reverse=True):
        pattern = r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])"
        if re.search(pattern, text, flags=re.I):
            out[name] = alias_map[name]
            text = re.sub(pattern, " ", text, flags=re.I)
    return out


def check_assets(text: str, facts: dict, alias_map: dict[str, int]) -> list[str]:
    """The asset check: the assets the text names that do not belong to the run.
    Empty means it passes."""
    allowed = set(facts["allowed_assets"])
    return [name for name, a in named_assets(text, alias_map).items() if a not in allowed]


def check(text: str, facts: dict, alias_map: dict[str, int]) -> dict:
    bad_numbers = check_numbers(text, facts, alias_map)
    bad_assets = check_assets(text, facts, alias_map)
    return {"numbers": {"passed": not bad_numbers, "offending": bad_numbers},
            "assets": {"passed": not bad_assets, "offending": bad_assets},
            "passed": not bad_numbers and not bad_assets}


# ---------------------------------------------------------------- the template

def template_text(facts: dict, ctx: dict) -> str:
    """The fallback, built only from the facts' own numbers and names, so it
    passes both checks by construction (the self-test confirms it)."""
    names = ctx["names"]
    nm = lambda xs: ", ".join(sorted(names[a] for a in xs))  # noqa: E731
    m, c, r, B = facts["metrics"], facts["centrality"]["metrics"], facts["random_mean"], facts["budget"]
    k, total = len(facts["placement"]), len(ctx["paths"])
    out = [f"The optimiser chose {nm(facts['placement']) or 'no decoy'} ({_n(k, 'decoy')}; budget {B})."]
    if k < B and facts["method"] in _STOPS_ONLY_WITHOUT_GAIN:
        out.append(f"It placed {_n(k, 'decoy')} because no further decoy raises F.")
    for path, step, a in facts["caught"]:
        length = next(p["length"] for p in ctx["paths"] if p["name"] == path)
        out.append(f"{path} is caught at step {step} of {length}, at {names[a]}.")
    if facts["missed"]:
        out.append(f"Not caught: {', '.join(facts['missed'])}.")
    out.append(f"It catches {len(facts['caught'])} of {total} attack paths. Its scores: {_scores(m)}.")
    out.append(f"The centrality baseline places {nm(facts['centrality']['placement'])} and catches "
               f"{len(facts['centrality']['caught'])} of {total} attack paths, with F {_fmt(c['f_score'])}. "
               f"The average of 30 random placements has F {_fmt(r['f_score'])} and coverage "
               f"{_fmt(r['coverage'])}.")
    return " ".join(out)


# ---------------------------------------------------------------- one explanation

def thinking_trace(content: str, thinking: str = "") -> bool:
    """True if a reply shows thinking: Ollama's separate thinking field, or a think
    tag in the reply text. A model that cannot switch thinking off writes its
    reasoning into the text, ending with </think> and with no opening tag (D43)."""
    return bool(thinking) or "<think>" in content or "</think>" in content


def explain_placement(ctx: dict, placement, budget: int, weights=DEFAULT_WEIGHTS,
                      method: str = "proposed_greedy", *, call_model: bool = True,
                      url: str | None = None, model: str = DECLARED_MODEL,
                      timeout: float | None = None) -> dict:
    """Builds the facts and the prompt, asks the model once (if call_model), checks
    its text, and returns what to show: the model's text if it passes both checks,
    otherwise the template. Nothing is retried, so a counted generation is a first try."""
    from src.explain import ollama  # here, so that the checks import without the client

    facts = build_facts(ctx, placement, budget, weights, method)
    system, user = build_prompt(facts)
    alias_map = aliases(ctx)
    result = {"facts": facts["text"], "allowed_assets": [ctx["names"][a] for a in facts["allowed_assets"]],
              "system_prompt": system, "user_prompt": user, "model": model, "model_called": call_model,
              "model_text": None, "model_meta": None, "error": None, "checks": None,
              "failures": [], "deviations": []}
    if call_model:
        try:
            reply = ollama.chat(system, user, url=url, model=model, timeout=timeout)
            result["model_text"] = reply.pop("content")
            result["model_meta"] = reply
        except ollama.OllamaError as e:
            result["error"] = str(e)
            result["failures"].append("model error")
    text = result["model_text"]
    if text is not None:
        # A thinking trace means the declared setting did not hold. It is recorded,
        # and the text is still judged by the two checks alone (§6). D43: a trace in
        # the text itself counts too, not only Ollama's thinking field.
        if thinking_trace(text, result["model_meta"].get("thinking") or ""):
            result["deviations"].append("thinking")
        if not text.strip():
            result["failures"].append("empty")
        result["checks"] = check(text, facts, alias_map)
        if not result["checks"]["numbers"]["passed"]:
            result["failures"].append("numbers")
        if not result["checks"]["assets"]["passed"]:
            result["failures"].append("assets")
    served_model = bool(text and text.strip() and result["checks"]["passed"])
    result["source"] = "model" if served_model else "template"
    result["text"] = text.strip() if served_model else template_text(facts, ctx)
    result["model_used"] = model if served_model else "template"
    return result


def counted_run_done() -> bool:
    return COUNTED_RESULTS.exists()
