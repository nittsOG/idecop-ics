"""
plausibility — Filter 1 of formal-problem-definition.md §4, as code (D26).

The API's confirm endpoint, scripts/import_plausibility_scores.py,
scripts/review_io.py and the scoring notebook all apply these rules through
this one module, so they cannot drift apart. D16 and D24 were both defects
where two implementations of one rule disagreed.

The rubric is adapted from Valeros et al. 2026 (sources.md #40):
- four criteria, scored in a fixed order;
- a four-point forced-choice scale with no neutral midpoint;
- "the first No ends the evaluation".

D26 adds this project's combination rule: an asset passes Filter 1 only if
every criterion is answered and none is No. Mostly No passes.
"""

LEVELS = ("yes", "mostly_yes", "mostly_no", "no")
LEVEL_LABELS = {"yes": "Yes", "mostly_yes": "Mostly Yes", "mostly_no": "Mostly No", "no": "No"}
# Higher is stronger; used for "weakest path decides" and for agreement measures.
LEVEL_RANK = {"no": 0, "mostly_no": 1, "mostly_yes": 2, "yes": 3}

# Scored in this order. Each entry is:
# (column suffix used in the database and API payloads, name in #40, plain question)
CRITERIA = (
    ("decoy_exists", "Feasibility",
     "Can a defender build and control a convincing decoy of this asset type at this position?"),
    ("attacker_reach", "Interaction",
     "Would an attacker following a modelled attack path through this position interact with the decoy?"),
    ("useful_signal", "Intelligence yield",
     "Would that interaction tell the defender something useful about the attacker?"),
    ("reliable_indicator", "Malice fidelity",
     "When the decoy is touched, is that reliably an attacker rather than routine benign activity?"),
)
KEYS = tuple(c[0] for c in CRITERIA)

# Answers that sit at the in/out boundary. D26 requires a written reason for them.
BOUNDARY = frozenset({"mostly_no", "no"})


class RubricError(ValueError):
    """A set of answers that breaks the rubric's rules. The message says which rule."""


def normalise_level(value):
    """Accept 'Mostly Yes', 'mostly yes', 'mostly_yes' and so on; return the stored
    form, or None for a blank. Anything else is an error, not a guess."""
    if value is None:
        return None
    v = str(value).strip().lower()
    if v in ("", "null", "none", "—", "-"):
        return None
    v = "_".join(v.replace("-", " ").replace("_", " ").split())
    if v not in LEVELS:
        raise RubricError(f"{value!r} is not a rubric level; use one of {', '.join(LEVEL_LABELS.values())}")
    return v


def check_sequence(values):
    """Validate one asset's four answers against the sequential rule and return
    them as a tuple in criterion order.

    - Every answer is one of the four levels, or blank.
    - Answers run in order until the first No. Every criterion before it must
      be answered, and every criterion after it must be blank, because #40's
      rule is that the first No ends the evaluation.
    - With no No at all, all four must be answered.
    """
    ordered = tuple(normalise_level(values.get(k)) for k in KEYS)
    stopped_at = None
    for i, (key, name, _) in enumerate(CRITERIA):
        v = ordered[i]
        if stopped_at is not None:
            if v is not None:
                raise RubricError(
                    f"{name} must be blank: {CRITERIA[stopped_at][1]} is No, and the first No ends the evaluation")
            continue
        if v is None:
            raise RubricError(f"{name} is not answered")
        if v == "no":
            stopped_at = i
    return ordered


def check_answers(values, n_paths):
    """check_sequence plus the §4 path rule (D26): an asset that lies on no
    modelled attack path cannot be intercepted by the model, so once its
    Feasibility is answered with anything but No, its Interaction must be No.
    `n_paths` is the number of distinct attack paths the asset lies on."""
    ordered = check_sequence(values)
    if n_paths == 0 and ordered[0] not in (None, "no") and ordered[1] != "no":
        raise RubricError("Interaction must be No: this asset is on no modelled attack path (§4)")
    return ordered


def passes(values, n_paths):
    """Filter 1's combination rule (D26): pass only if all four criteria are
    answered and none is No. Raises RubricError for answers that break the
    sequential rule or the path rule."""
    ordered = check_answers(values, n_paths)
    return all(v is not None and v != "no" for v in ordered)


def reason_required(values, ai_values, blind, n_paths):
    """D26's safeguard: when must the reviewer write a reason?

    Returns a list of plain-language triggers. An empty list means no reason is needed.
    - A blind card always needs one, because there is no AI answer to agree with.
    - A card with no AI suggestion needs one. That is a direct, route-B score.
    - Changing any AI answer needs one.
    - Any final answer at the boundary (Mostly No or No) needs one, because those
      answers decide whether the asset is on the shortlist. The exception is the
      Interaction No that the path rule imposes on an off-path asset; the rule
      is its reason.
    - An asset on several paths needs one, because "weakest path decides": the
      reason is where each path's own Interaction level is recorded.
    """
    ordered = check_answers(values, n_paths)
    triggers = []
    if blind:
        triggers.append("blind card")
    else:
        ai = tuple(normalise_level(ai_values.get(k)) for k in KEYS) if ai_values else (None,) * 4
        if all(a is None for a in ai):
            triggers.append("no AI suggestion (direct score)")
        elif ordered != ai:
            changed = [CRITERIA[i][1] for i in range(4) if ordered[i] != ai[i]]
            triggers.append("changed the AI's answer on " + ", ".join(changed))
    at_boundary = [CRITERIA[i][1] for i, v in enumerate(ordered)
                   if v in BOUNDARY and not (i == 1 and n_paths == 0)]
    if at_boundary:
        triggers.append("Mostly No or No on " + ", ".join(at_boundary))
    if n_paths > 1:
        triggers.append(f"on {n_paths} attack paths: give each path's Interaction level (weakest path decides)")
    return triggers


def weakest(levels):
    """'Weakest path decides' (D26): the lowest of several per-path levels."""
    present = [normalise_level(l) for l in levels if normalise_level(l) is not None]
    if not present:
        return None
    return min(present, key=lambda l: LEVEL_RANK[l])
