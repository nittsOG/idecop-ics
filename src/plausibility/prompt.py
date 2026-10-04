"""
The AI first pass for Filter 1 (route A, D26): what the model is shown, what it
must return, and how its answer becomes a suggestion that respects the rubric.

notebooks/plausibility_scoring.ipynb imports this module from the cloned
repository. It is also the canonical text of the prompt that 02-ai-role.md §9
summarises. Everything here runs without a GPU, so it is tested locally with a
stand-in model. Only the generation call itself needs Colab.
"""
import json
import re

from . import CRITERIA, LEVEL_LABELS, LEVEL_RANK, check_sequence, normalise_level, weakest, RubricError

# --- Valeros et al. 2026, Table 1, reproduced unchanged -----------------------
SOURCE_CREDIT = (
    "Level definitions reproduced unchanged from Valeros, Lisý, Catania and Griffioen (2026), "
    "\"Decoys Cannot Go Everywhere: Mapping the Deception Surface in MITRE ATT&CK\", "
    "arXiv:2606.27966, Table 1. Licence: CC BY-NC-SA 4.0 "
    "(https://creativecommons.org/licenses/by-nc-sa/4.0/). No changes made."
)

TABLE_1 = {
    "Feasibility": {
        "yes": "The defender can fully fabricate and control the target asset as a decoy, and it responds convincingly to attacker actions.",
        "mostly_yes": "The target asset can be mimicked but it is hard to make convincing. May not withstand close scrutiny.",
        "mostly_no": "The target asset can only be partially mimicked as a decoy. It is difficult to simulate convincingly and only works in limited conditions.",
        "no": "The technique has no defender-controllable target asset that can be fabricated and operated as a decoy.",
    },
    "Interaction": {
        "yes": "The technique naturally leads attackers to the decoy. Interaction follows as a direct consequence of the technique.",
        "mostly_yes": "Interaction is likely but not certain, depending on the decoy’s positioning, configuration, or the attacker’s tools.",
        "mostly_no": "Interaction is possible but unlikely, requiring attacker-specific knowledge, unusual timing, or atypical choices.",
        "no": "No plausible attacker path to the decoy exists. An attacker following the technique would not be expected to interact with this decoy.",
    },
    "Intelligence yield": {
        "yes": "Interaction directly yields strategic, operational, tactical, or technical intelligence attributable to the decoy.",
        "mostly_yes": "Interaction yields intelligence, but only after correlation with other data, added context, or further analysis.",
        "mostly_no": "Interaction produces some data, but it is too generic or ambiguous to be meaningful without significant further analysis.",
        "no": "No intelligence yield. The observable data gives no insight into the attacker’s behavior, identity, or intent.",
    },
    "Malice fidelity": {
        "yes": "Legitimate interaction is not expected by design. The only plausible trigger is an attacker action, so the false-positive rate is near zero.",
        "mostly_yes": "Interaction strongly indicates malice. A small set of benign activities could trigger it, but these cases are identifiable and filterable.",
        "mostly_no": "Interaction may indicate malice, but many triggers are benign or ambiguous. Telling them apart is complex, so the signal is useful but not standalone.",
        "no": "Benign activity routinely triggers this decoy. Interaction does not distinguish an attacker.",
    },
}

# --- This project's adaptation (D26) — our own text, separate from Table 1 ---
CONVENTIONS = (
    "Unit of analysis. The level definitions were written for ATT&CK techniques. Here each item is one asset "
    "position in one network: read \"the technique\" as \"the attack-path steps at this position\".",
    "What a decoy here means. A decoy imitating this asset's type, deployed in the same zone, on the same network "
    "segment and behind the same conduits, so that attack paths through this asset pass where it sits. It is not "
    "a change to the real asset.",
    "Best case, actual position. Score each criterion for the best case a well-instrumented decoy could plausibly "
    "produce, but at this position in this network, not in principle.",
    "Order. Score Feasibility, Interaction, Intelligence yield, Malice fidelity in that order. The first No ends "
    "the evaluation: every later criterion is null.",
    "Ties. Where the evidence fits two adjacent levels equally, choose the lower one (closer to No).",
    "Interaction is judged only against the attack paths listed for this asset, as modelled. For each path, say "
    "whether the encounter is a Sweep (the attacker moves broadly through everything in range and meets the decoy "
    "incidentally) or a Seek (the attacker looks for this kind of asset and interacts with a fabricated one). An "
    "asset on no listed path scores No. An asset on several paths is scored per path, and the lowest per-path "
    "level is the one recorded.",
    "Malice fidelity. First name the routine benign activity that reaches this position. In OT networks that "
    "includes, among others, asset-inventory and monitoring scans, historian polling and data collection, "
    "engineering-software and vendor maintenance sessions, backup jobs and time synchronisation.",
)

OUTPUT_SHAPE = """{
  "feasibility": {"level": "Yes | Mostly Yes | Mostly No | No", "reason": "one sentence"},
  "interaction": [
    {"path": "<path name, e.g. P1>", "pattern": "Sweep | Seek | Neither", "level": "Yes | Mostly Yes | Mostly No | No", "reason": "one sentence"}
  ],
  "intelligence_yield": {"level": "Yes | Mostly Yes | Mostly No | No", "reason": "one sentence"},
  "malice_fidelity": {"benign_activity": "what routine benign activity reaches this position, or none known", "level": "Yes | Mostly Yes | Mostly No | No", "reason": "one sentence"}
}"""


def _table_text():
    lines = []
    for name, levels in TABLE_1.items():
        lines.append(f"{name}:")
        for key in ("yes", "mostly_yes", "mostly_no", "no"):
            lines.append(f"  - {LEVEL_LABELS[key]}: {levels[key]}")
    return "\n".join(lines)


SYSTEM_PROMPT = (
    "You are assisting a security analyst who is deciding where decoys could be placed in an industrial control "
    "system (OT) network. For one asset at a time, you score a four-criterion plausibility rubric. A human analyst "
    "reviews every answer before it is used. Give your honest, reasoned first pass.\n\n"
    "Use exactly one of four levels for each criterion: Yes, Mostly Yes, Mostly No, No. There is no neutral or "
    "middle answer; commit to the level the evidence supports.\n\n"
    "LEVEL DEFINITIONS\n" + _table_text() + "\n(" + SOURCE_CREDIT + ")\n\n"
    "RULES FOR THIS PROJECT\n" + "\n".join(f"{i}. {c}" for i, c in enumerate(CONVENTIONS, 1)) + "\n\n"
    "Return only a JSON object, with no other text, in exactly this shape. Use null for every criterion after the "
    "first No. List one interaction entry per attack path given for the asset, and none if it is on no path.\n"
    + OUTPUT_SHAPE
)


# --- Context for one asset, read from the project database --------------------
def assets_to_score(conn):
    """Every asset with a candidate_locations row, which is every asset except the Attacker node (D25, A32)."""
    return [r[0] for r in conn.execute(
        "SELECT cl.asset_id FROM candidate_locations cl JOIN assets a ON a.asset_id = cl.asset_id "
        "WHERE a.asset_type <> 'Attacker' ORDER BY cl.asset_id")]


def asset_context(conn, asset_id):
    a = conn.execute("""
        SELECT a.asset_id, a.name, a.asset_type, a.purdue_level, z.name
        FROM assets a JOIN zones z ON z.zone_id = a.zone_id WHERE a.asset_id = ?""", (asset_id,)).fetchone()
    if a is None:
        raise KeyError(f"no asset {asset_id}")
    names = {r[0]: r[1] for r in conn.execute("SELECT asset_id, name FROM assets")}

    paths = []
    for pid, pname, pdesc in conn.execute(
            "SELECT path_id, name, description FROM attack_paths ORDER BY path_id").fetchall():
        steps = conn.execute("""
            SELECT step_order, asset_id, tactic, technique_id, technique_name
            FROM attack_path_steps WHERE path_id = ? ORDER BY step_order""", (pid,)).fetchall()
        positions = [s[0] for s in steps if s[1] == asset_id]
        if positions:
            paths.append({
                "path": pname, "description": pdesc, "length": len(steps), "positions": positions,
                "steps": [{"order": s[0], "asset": names[s[1]], "tactic": s[2],
                           "technique": " ".join(x for x in (s[3], s[4]) if x)} for s in steps],
            })

    neighbours = []
    for src, tgt, proto in conn.execute(
            "SELECT source_asset_id, target_asset_id, protocol FROM edges "
            "WHERE source_asset_id = ? OR target_asset_id = ? ORDER BY edge_id", (asset_id, asset_id)):
        other, direction = (tgt, "to") if src == asset_id else (src, "from")
        neighbours.append({"asset": names[other], "direction": direction, "protocol": proto})

    return {"asset_id": a[0], "name": a[1], "asset_type": a[2], "purdue_level": a[3], "zone": a[4],
            "paths": paths, "neighbours": neighbours}


def user_prompt(ctx):
    lines = [f"Asset: {ctx['name']} — {ctx['asset_type']}, zone {ctx['zone']} (Purdue level {ctx['purdue_level']})"]
    if ctx["neighbours"]:
        lines.append("Direct network connections: " + "; ".join(
            f"{n['direction']} {n['asset']}" + (f" ({n['protocol']})" if n["protocol"] else "")
            for n in ctx["neighbours"]))
    else:
        lines.append("Direct network connections: none recorded")
    if ctx["paths"]:
        lines.append(f"Attack paths through this asset ({len(ctx['paths'])}):")
        for p in ctx["paths"]:
            lines.append(f"{p['path']} — {p['description']}")
            for s in p["steps"]:
                mark = "   <- this asset" if s["order"] in p["positions"] else ""
                lines.append(f"  {s['order']}. {s['asset']} — {s['tactic']} — {s['technique']}{mark}")
    else:
        lines.append("Attack paths through this asset: none. By the rules, its Interaction is No, so score "
                     "Feasibility only, return an empty interaction list, and use null for the last two criteria.")
    lines.append("Score this asset now. Return only the JSON object.")
    return "\n".join(lines)


def messages(ctx):
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt(ctx)}]


# --- Turning the model's text into a suggestion -------------------------------
class ParseError(ValueError):
    """The model's output could not be used. The asset then gets no AI suggestion and is
    scored directly by the human, with a reason, as route B allows (D26)."""


def parse_output(text):
    t = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    t = re.sub(r"```(?:json)?", "", t)
    start, end = t.find("{"), t.rfind("}")
    if start < 0 or end <= start:
        raise ParseError("no JSON object in the output")
    try:
        return json.loads(t[start:end + 1])
    except json.JSONDecodeError as e:
        raise ParseError(f"invalid JSON: {e}") from e


def _text(block, field):
    """A free-text field from the model, as a clean string. A missing or null
    value becomes "", so a null reason can never crash the run."""
    if not isinstance(block, dict):
        return ""
    return str(block.get(field) or "").strip()


def _path_key(value):
    """'P2', 'P2 — Industroyer2-class…' and 'p2:' all name path P2."""
    t = re.split(r"[\s—:–-]+", str(value or "").strip(), maxsplit=1)[0]
    return t.upper()


def _level(block, field="level"):
    if block is None:
        return None
    if not isinstance(block, dict):
        raise ParseError(f"expected an object, got {block!r}")
    try:
        return normalise_level(block.get(field))
    except RubricError as e:
        raise ParseError(str(e)) from e


def derive(parsed, ctx):
    """Apply the rubric's rules to a parsed answer and return
    (levels by criterion key, reasoning text, notes on any rule the code applied).

    The code, not the model, applies these rules:
    - an off-path asset's Interaction is No;
    - the weakest path decides;
    - everything after the first No is blank.
    Each time the code overrides the model, it records a note."""
    notes, parts = [], []
    feas = _level(parsed.get("feasibility"))
    if feas is None:
        raise ParseError("Feasibility has no level")
    parts.append(f"Feasibility: {LEVEL_LABELS[feas]} — {_text(parsed['feasibility'], 'reason')}")

    levels = {"decoy_exists": feas, "attacker_reach": None, "useful_signal": None, "reliable_indicator": None}
    if feas == "no":
        if parsed.get("interaction") or parsed.get("intelligence_yield") or parsed.get("malice_fidelity"):
            notes.append("criteria after a No were blanked (sequential rule)")
        return levels, " | ".join(parts), notes

    entries = parsed.get("interaction") or []
    if not isinstance(entries, list):
        raise ParseError("interaction must be a list of per-path entries")
    if not ctx["paths"]:
        if any(_level(e) not in (None, "no") for e in entries):
            notes.append("model scored Interaction for an off-path asset; set to No by the §4 rule")
        inter = "no"
        parts.append("Interaction: No — on no modelled attack path (§4 rule)")
    else:
        by_path = {}
        for e in entries:
            if isinstance(e, dict):
                by_path.setdefault(_path_key(e.get("path")), []).append(e)
        per_path = []
        for p in ctx["paths"]:
            found = by_path.get(_path_key(p["path"]))
            if not found:
                raise ParseError(f"no interaction entry for {p['path']}")
            scored = []
            for e in found:
                lv = _level(e)
                if lv is None:
                    raise ParseError(f"interaction for {p['path']} has no level")
                pattern = _text(e, "pattern") or "?"
                if pattern.lower() == "neither" and lv != "no":
                    # §4: a decoy that is neither swept nor sought goes untouched.
                    notes.append(f"{p['path']}: pattern Neither, so Interaction set to No (§4)")
                    lv = "no"
                scored.append((pattern, lv, _text(e, "reason")))
            if len(scored) > 1:
                notes.append(f"{p['path']}: {len(scored)} entries; the weakest was kept")
            pattern, lv, why = min(scored, key=lambda t: LEVEL_RANK[t[1]])
            per_path.append((p["path"], pattern, lv, why))
        inter = weakest(lv for _, _, lv, _ in per_path)
        text = "; ".join(f"{name} {pattern} {LEVEL_LABELS[lv]} — {why}" for name, pattern, lv, why in per_path)
        if len(per_path) > 1:
            text += f"; recorded {LEVEL_LABELS[inter]} (weakest path)"
        parts.append("Interaction: " + text)
    levels["attacker_reach"] = inter
    if inter == "no":
        if parsed.get("intelligence_yield") or parsed.get("malice_fidelity"):
            notes.append("criteria after a No were blanked (sequential rule)")
        return levels, " | ".join(parts), notes

    yld = _level(parsed.get("intelligence_yield"))
    if yld is None:
        raise ParseError("Intelligence yield has no level")
    levels["useful_signal"] = yld
    parts.append(f"Intelligence yield: {LEVEL_LABELS[yld]} — {_text(parsed['intelligence_yield'], 'reason')}")
    if yld == "no":
        if parsed.get("malice_fidelity"):
            notes.append("Malice fidelity was blanked (sequential rule)")
        return levels, " | ".join(parts), notes

    mal_block = parsed.get("malice_fidelity")
    mal = _level(mal_block)
    if mal is None:
        raise ParseError("Malice fidelity has no level")
    levels["reliable_indicator"] = mal
    benign = _text(mal_block, "benign_activity")
    parts.append(f"Malice fidelity: {LEVEL_LABELS[mal]} (benign activity: {benign or 'not stated'}) — "
                 f"{_text(mal_block, 'reason')}")

    check_sequence(levels)  # must hold by construction; raises if not
    return levels, " | ".join(parts), notes


# --- The scoring loop, shared by the notebook and the local tests -------------
CSV_FIELDS = (["asset_id", "asset_name"]
              + [f"ai_suggested_{c[0]}" for c in CRITERIA]
              + ["ai_reasoning", "ai_model", "generated_at", "repo_commit", "parse_status", "notes"])

RETRY_MESSAGE = "That answer could not be used ({error}). Return only the JSON object, in the required shape."


def run(contexts, generate, model_tag, commit, generated_at, log=print):
    """Score every asset with `generate(messages) -> text`.

    Each asset gets one retry with the reason for the failure. An asset whose
    output still cannot be used gets no suggestion (parse_status 'failed'), and
    the reviewer scores it directly.

    Returns (CSV rows, raw records). `log` reports progress only, never an answer,
    so a blind card that is still open cannot be spoiled by watching the run."""
    rows, raw = [], []
    for ctx in contexts:
        msgs = messages(ctx)
        text, error, status, levels, reasoning, notes = "", "", "failed", {}, "", []
        attempts = 0
        for attempts in (1, 2):
            convo = msgs if attempts == 1 else msgs + [
                {"role": "assistant", "content": text},
                {"role": "user", "content": RETRY_MESSAGE.format(error=error)}]
            text = generate(convo)
            try:
                levels, reasoning, notes = derive(parse_output(text), ctx)
                status, error = "ok", ""
                break
            except Exception as e:   # any unusable output fails this attempt, never the whole run
                error = str(e) if isinstance(e, ParseError) else f"{type(e).__name__}: {e}"
        row = {"asset_id": ctx["asset_id"], "asset_name": ctx["name"],
               "ai_reasoning": reasoning if status == "ok" else "",
               "ai_model": model_tag, "generated_at": generated_at, "repo_commit": commit,
               "parse_status": status, "notes": "; ".join(notes) if status == "ok" else error}
        for c in CRITERIA:
            row[f"ai_suggested_{c[0]}"] = (levels.get(c[0]) or "") if status == "ok" else ""
        rows.append(row)
        raw.append({"asset_id": ctx["asset_id"], "asset_name": ctx["name"], "attempts": attempts,
                    "parse_status": status, "error": error, "notes": notes, "output": text})
        log(f"{ctx['name']}: {'scored' if status == 'ok' else 'no usable answer'} ({attempts} attempt(s))")
    return rows, raw
