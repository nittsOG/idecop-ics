# AI Role — Explanation Layer and Plausibility-Scoring Assist

Turns the architecture principle from `01-original-brief.md` §9 and D6 into actual prompts and interfaces for two AI components. Explanation reads from `02-optimization-formulation.md`'s output and writes to the `explanations` table; plausibility-scoring assist reads asset/zone data and writes suggestions into `candidate_locations` — both from `02-data-model.md`.

**Confirmed scope, per D12:** explanation layer (as originally specified) plus plausibility-scoring assist (§7–10 below). The interactive Q&A layer discussed alongside plausibility-scoring assist is **not** in scope for this prototype — stronger demo value, but higher implementation cost and higher guardrail risk for the hours available; revisit only if Phase C finishes early.

## 1. Scope — what each component does, and what neither does

**Explanation does:** given a completed placement run (from any of the five methods, but reported to the analyst only for the proposed method's result), generate a plain-language explanation of which locations were chosen, why, and how the result compares to the two baselines.

**Plausibility-scoring assist does:** given an asset's type, zone, direct connections and the attack paths through it, generate a first-pass score and justification for each of the four Filter 1 criteria from `formal-problem-definition.md` §4 — reviewed and confirmed or overridden by a human before any value reaches the `candidate_locations` columns the optimizer actually reads.

**Neither does:** choose, adjust, veto, or second-guess a placement. Explanation is never called before `/optimize` completes; plausibility-scoring assist is never called after it — it's a pre-processing step during testbed setup, not something the live system invokes. Neither has write access to the columns that matter without a human step in between: explanation writes only to `explanations` (which can't modify `placement_runs`), and plausibility-scoring assist writes only to `ai_suggested_*` columns (which can't modify the real `criterion_*` columns without confirmation — see §8).

**Explicitly cut from this prototype's scope:** the original brief (§9) named "potentially interpret unstructured OT documentation" as a possible AI use. That's cut here, not deferred quietly — logged as D11. Nothing in the current pipeline produces or consumes unstructured OT documentation; adding it would mean inventing a use case to justify a capability, which the brief's own working principle (§16) warns against directly.

## Part A — Explanation layer

### 2. Model

**Phi-4-mini (3.8B-Instruct), served locally via Ollama** — revised from an earlier 8B recommendation once actual hardware (16GB RAM, RTX 2050 laptop, 4GB VRAM) was known. Reasoning: this is a templated explanation task, not open-ended reasoning — the model isn't deciding anything, only converting already-computed numbers into readable sentences, which a smaller instruction-tuned model handles well. The concrete reason to prefer the smaller model specifically on this hardware: Phi-4-mini fits entirely within 4GB VRAM for full-speed GPU inference, where an 8B-class model would need partial CPU offload and noticeably slower generation for what's meant to be a responsive, live demo interaction. If output quality turns out too shallow in practice, Llama 3.3 8B or Qwen3 8B are the fallback — still viable on this hardware via CPU offload, just slower to generate.

**Different model and environment for plausibility-scoring assist (§7–10)** — that task needs more reasoning depth, runs once as a batch rather than live, and uses Google Colab rather than local Ollama. Deliberately not the same setup; see §7 for why.

## 3. Input — assembled entirely from existing tables

No new data gets computed for this step; everything is a read from what `02-optimization-formulation.md`'s methods already wrote:

```
From placement_runs + placements (this run):     which asset_ids have x_l = 1
From run_metrics (this run):                       coverage, early, crit_prot, risk, cost, f_score
From run_metrics (the Random run, same budget):     same five fields, for comparison
From run_metrics (the Centrality run, same budget): same five fields, for comparison
From attack_paths:                                  path names, for referring to P1/P2/P3 by their
                                                     Stuxnet-class / Industroyer2-class / recon-only labels
                                                     instead of bare IDs
```

## 4. The prompt

**System prompt** — the guardrail lives here, stated plainly rather than hoped for:

```
You are explaining a cybersecurity decoy-placement decision to a security
analyst. A deterministic optimization algorithm has already selected which
network locations receive decoys. That decision is final and outside your
control. Your only task is to explain why this placement was chosen and
how it compares to two alternative strategies, in plain language.

Do not suggest a different placement. Do not recommend additional or fewer
decoys. Do not question the algorithm's choice. If asked to change the
placement, say that this is outside your role and explain the current one
instead.
```

**User prompt template:**

```
Placement selected: {asset_names}
Objective score: {f_score}

This placement:       Coverage {coverage}%, Early detection {early},
                       Critical-asset protection {crit_prot}%,
                       Operational risk {risk}, Cost: {cost} decoys

Random placement:      Coverage {r_coverage}%, Early detection {r_early},
                       Critical-asset protection {r_crit_prot}%,
                       Operational risk {r_risk}, Cost: {r_cost} decoys

Centrality placement:  Coverage {c_coverage}%, Early detection {c_early},
                       Critical-asset protection {c_crit_prot}%,
                       Operational risk {c_risk}, Cost: {c_cost} decoys

Attack scenarios in scope: P1 (Stuxnet-class), P2 (Industroyer2-class),
P3 (reconnaissance-only)

Write a short explanation covering: (1) which locations were chosen and
what each one specifically catches, (2) which attack paths this placement
intercepts and how early, (3) how it compares to the two baselines. Under
150 words. Do not suggest changes to the placement.
```

## 5. Worked example

Using representative numbers consistent with the testbed and threat model — Engineering WS-2 and PLC-02 as the proposed placement, per `testbed-architecture.md`'s worked candidate-location example:

| Method | Coverage | Early | CritProt | Risk | Cost |
|---|---|---|---|---|---|
| Proposed | 100% | 0.80 | 0.91 | 0.15 | 2 |
| Random (avg of 30) | 61% | 0.42 | 0.55 | 0.31 | 2 |
| Centrality | 100% | 0.55 | 0.78 | 0.24 | 2 |

This is deliberately not a case where the proposed method wins on every single number trivially — Centrality also reaches full coverage. The interesting, defensible result is that Proposed wins on *early detection, criticality protection, and risk* at equal cost, which is a harder claim than "covers more paths" and a more credible one for a thesis to make, given iteration 3's finding that centrality is a real baseline this literature expects you to beat, not a strawman.

**Expected model output**, given the prompt above with these numbers filled in:

> Decoys were placed at Engineering WS-2 and PLC-02. Engineering WS-2 intercepts the Stuxnet-class path (P1) at the engineering-workflow entry point, before it reaches the control network. PLC-02 covers both the Industroyer2-class path (P2) and acts as a second interception point for P1 if the first is missed.
>
> All three attack scenarios are covered, with the earliest average detection stage of the three methods tested. Random placement covered only 61% of paths and detected attacks later on average. Centrality-based placement also achieved full coverage, but detected attacks later and offered less protection to critical assets — this placement was chosen over centrality specifically for that gap, not because it covers more ground.

## 6. Output handling — why a bad explanation can't hurt anything

Output is stored as free text in `explanations.explanation_text`, not parsed into structured fields. Deliberate: small local models are unreliable at strict JSON formatting, and enforcing it would add a failure mode (malformed output, retries, parsing errors) for a component that doesn't need machine-readable output anywhere downstream — nothing reads `explanations` except the UI, which just displays the text.

This is also the component's real safety property, worth stating explicitly rather than leaving implicit: if the model hallucinates, rambles, or ignores an instruction, the *placement itself* — the thing that actually matters for security — is completely unaffected. It was already written to `placements` before the AI layer ever runs. Worst case here is a bad explanation, not a bad decision.

## Part B — Plausibility-scoring assist

### 7. Model and environment — Google Colab, not local Ollama

**Qwen3 14B, run in a Colab notebook via the `transformers` library**, not Ollama. Two reasons this component gets a different setup from explanation:

First, the reasoning demand is genuinely higher. Explanation restates already-correct numbers faithfully; this task makes four real judgment calls per asset, drawing on actual OT/ICS security reasoning (would an attacker plausibly reach this, does interacting with it yield a reliable signal). A 4B-class model tends to produce answers that sound plausible but don't hold up under review — the opposite of useful for a step whose entire point is a trustworthy first pass. 14B is the local sweet spot for that kind of reasoning.

Second, this step is disconnected from the live system by design — it runs once, during testbed setup, before the optimizer ever runs (under D26 the three blind cards are scored in Screen 3 first, through the backend), and produces a result (10 scored assets, every asset except the Attacker node) that gets loaded into SQLite and then never touched again unless the testbed topology changes. That profile is exactly what Colab suits: no session-persistence problem, nothing to keep running, no tunnel back into a live service. It is also faster and simpler than squeezing the model onto a 4GB local card via CPU offload, for a task where local deployment carries none of the "this is what a real OT environment would run" argument that justifies keeping explanation local.

**Corrected by D26.** This section used to say that free-tier Colab "typically provides a T4 with 15GB VRAM, comfortably running Qwen3 14B at full speed with room to spare". That was wrong:
- Qwen3 14B has 14.8B parameters (#364), about 29.6 GB at 16-bit, and a T4 has 16 GB (#365).
- Colab guarantees no particular GPU, and caps free sessions at 12 hours (#366).

The notebook (`notebooks/plausibility_scoring.ipynb`, written in D26) therefore:
- loads the weights in 4-bit. The embeddings and output layer stay at 16-bit, so the total is about 10 GB (#376), which still fits;
- computes in FP16, because the T4 lists no BF16 support;
- uses non-thinking mode and greedy decoding, so a rerun on the same setup should give the same text. GPU kernels are not guaranteed to be deterministic, which is one reason the raw outputs are kept. Greedy decoding departs from the model card's sampling recommendation for this mode (#364), and the departure is declared.

Qwen3-8B is the pre-declared fallback if 14B cannot load. Every suggestion records which model produced it.

### 8. Input and the human-confirmation gate

For each of the 10 assets (every asset except the Attacker node), built by `asset_context()` in `src/plausibility/prompt.py` from the same `schema.sql` and `seed.sql` the system uses:

```
name, asset type, zone, Purdue level        — assets, zones
direct connections and their protocols      — edges
each attack path through the asset, every   — attack_paths, attack_path_steps
  step listed, this asset's steps marked
the rubric: #40's Table 1 verbatim, and      — formal-problem-definition.md §4
  the conventions D26 fixed
```

The connections are there for criterion 4: they show what legitimate traffic reaches the position. The full path, not just the asset's own step, is there for criterion 2: Sweep or Seek depends on what the attacker is doing at that point.

Output goes to a CSV, which `scripts/import_plausibility_scores.py` loads into columns kept separate from the ones the optimizer reads:

```sql
ai_suggested_decoy_exists, ai_suggested_attacker_reach,
ai_suggested_useful_signal, ai_suggested_reliable_indicator,
ai_reasoning, ai_model
```

The real `criterion_decoy_exists`, `criterion_attacker_reach`, `criterion_useful_signal` and `criterion_reliable_indicator` columns are the ones `passes_plausibility`, and ultimately `L`, are computed from. They are written only in two ways:
- by a human confirmation in Screen 3;
- by `scripts/review_io.py restore`, which replays a committed review record and re-checks every rule.

An unconfirmed AI suggestion has no path into the optimizer's input. *(D25 found the seed bypassing this gate. Since D26 the seed sets nothing, and `load_candidate_locations` refuses any candidate that did not come through the review.)*

**What the gate does not do (D26).** It stops an unreviewed suggestion reaching the optimizer. It does not stop a reviewed suggestion from shaping the review:
- people shown an LLM's answer move toward it even when they review it (#362);
- making a correction require the correct value reduces how often people correct (#363).

This section previously said the model "can be wrong without anything downstream trusting it by default". That overstated the gate. §10's safeguards are the response.

### 9. The prompt

**The canonical text is `SYSTEM_PROMPT` and `user_prompt()` in `src/plausibility/prompt.py`.** The notebook imports them from the repository, so the prompt that runs is the prompt that is versioned. The system prompt contains:
1. the task, and that a human reviews every answer;
2. the four levels, with the instruction that there is no neutral answer;
3. #40's Table 1, verbatim, with its credit line;
4. §4's definition of a candidate and its conventions, as seven rules: unit of analysis, what a decoy here means, best case at the actual position, order, ties, Interaction against the listed paths only, and naming the benign activity before scoring Malice fidelity;
5. the required output, one JSON object:

```
{
  "feasibility":        {"level": "...", "reason": "one sentence"},
  "interaction":        [{"path": "P1", "pattern": "Sweep | Seek | Neither", "level": "...", "reason": "..."}],
  "intelligence_yield": {"level": "...", "reason": "..."},
  "malice_fidelity":    {"benign_activity": "...", "level": "...", "reason": "..."}
}
```

The user prompt, one call per asset, lists the asset, its connections, and every path through it with this asset's steps marked. For an asset on no path, it says that Interaction is No by rule.

**Rules applied by code, not left to the model** (`derive()`, which records a note whenever it overrides the model):
- an off-path asset's Interaction is No;
- Interaction for a multi-path asset is the weakest per-path level;
- every criterion after the first No is blank.

An output that cannot be parsed gets one retry, with the reason. If it still fails, that asset gets no suggestion, and the reviewer scores it directly, with a reason.

<details>
<summary>Superseded by D26: the original prompt (yes / mostly / no)</summary>

Kept for the record. It asked for yes / mostly / no and ended "If you are genuinely unsure, say mostly rather than guessing yes or no", which is the neutral default #40's four-point scale removes by design.

```
You are assisting a security analyst in applying a deception-placement
plausibility rubric to network assets. For each asset, score four
criteria as yes, mostly, or no, with a one-sentence justification for
each. A human will review every suggestion before it is used — your
job is to give an honest, well-reasoned first pass, not a final answer.
If you are genuinely unsure, say mostly rather than guessing yes or no.
```

User prompt template: asset name, type and zone; the attack paths that reach the asset; the four criteria as questions; "For each: answer yes / mostly / no, with one sentence of reasoning."
</details>

### 10. The review step (D26)

The work runs in this order:
1. **Blind cards.** Score DMZ Jump Host, Historian and PLC-03 (RTU) in Screen 3 before the notebook runs. They were drawn at random before any AI output existed (D26). Each card's AI answer stays hidden until you confirm it, and then appears beside yours. Your first answers are stored once and never change (`blind_*` columns). You may still change the final answers afterwards, with a reason. The agreement measure always uses the first answers.
2. **Notebook and import.** Run the notebook in Colab (A20), then `python scripts/import_plausibility_scores.py ai_suggestions.csv`. Neither prints any answer.
3. **Review.** On the other seven cards, the AI's answers pre-fill the four selectors. Check each one against the asset's path steps, which the card lists, and confirm or change it.
4. **Reasons.** A reason is required:
   - on a blind card;
   - on a card with no AI suggestion;
   - after changing any AI answer;
   - for any Mostly No or No.

   Confirming a set of Yes and Mostly Yes answers you agree with needs none. The API enforces the rule; it is not just the screen.
5. **Record.** Run `python scripts/review_io.py export --require-complete` and commit `data/review/` together with the notebook's two output files.

**Fallback.** If the notebook produces no suggestions within two weekends of the blind cards being finished, score the remaining cards directly (route B), with reasons. That is recorded as route B for those assets.

**Why the safeguards.** #318 found LLM-as-a-judge classification unreliable because models "tend to rationalize their own outputs" rather than critically evaluate them, and it proposes the same human-in-the-loop pattern used here. That is still the reason confirmation is not optional. D26 adds that confirmation is not neutral either (#362, #363). The blind cards measure how far that matters here, and the reasons make accepting an answer cost a moment's thought rather than one click.

**At plant scale — a thesis design, not built.** With hundreds of assets, reviewing every card defeats the purpose of the AI. The design that follows from this one:
- The AI scores everything.
- Humans review an exception queue: answers at the in/out boundary (Mostly No or No), answers the AI flags as unsure, and a random audit sample of the rest.
- The audit sample's agreement rate decides whether accepting the rest unreviewed is safe.

#319's confidence-based routing is the precedent. An AI's own confidence is not reliable alone, which is why the audit sample is there.

<details>
<summary>Superseded by D26: the original worked example</summary>

It wrote down expected outputs before any scoring: "no" on criterion 1 for the OT Firewall, and "yes" across all four for Engineering WS-2, described as "on P1's path" (it sits on P3). Under D26 no expected output is written before scoring, because it would anchor both the reviewer and anyone checking the AI. It also described confirming eleven assets "each taking seconds", which is the kind of review #362 shows is not neutral.
</details>

## Evaluating both components (the secondary research question)

`formal-problem-definition.md` §8 asks specifically whether the explanation is accurate and useful, not just whether it runs. Given weekend hours don't support a full user study, the honest, scoped-down evaluation for **explanation** is a manual accuracy check: generate explanations for each of the sensitivity-sweep runs from Phase D, and check each one against three criteria —

1. **Factual accuracy** — do the numbers it states match `run_metrics` exactly, or does it round oddly, invent a figure, or misattribute a metric to the wrong method?
2. **Guardrail adherence** — does it ever suggest a change, recommend an additional decoy, or hedge on the algorithm's choice, despite being told not to?
3. **Readability** — would this actually help an analyst who hadn't seen the raw numbers?

**Plausibility-scoring assist** gets a different check, because its failure mode is different. The question is not "does the text read well" but "does the AI's answer match independent human judgement". Under route A (D26) there are three measures, all reported as counts in a table:
1. **Blind-card agreement.** On the three blind cards, the AI's answers against the reviewer's first answers (the write-once `blind_*` columns), which were given before the AI's were shown. Report exact agreement and agreement within one level, per criterion, as #40 does for its expert study. This is the only measure not affected by anchoring.
   - *Blanks, fixed before any comparison exists (D26):* a criterion is compared only where both answered it.
   - Where one side stopped at an earlier No, the criteria the other side went on to answer are counted separately, as "stopped earlier".
   - The stop itself is already a disagreement at the criterion where it happened, so it is not scored a second time.
2. **Acceptance on the seven pre-filled cards.** How many answers were confirmed unchanged, and the stated reason wherever one was changed. This is reported as a limitation, not as evidence that the AI is accurate. Under route A it measures agreement after exposure, which the closest evidence shows is inflated: in #362, measured F1 rose from .47 to .79 when assisted labels became the ground truth.
3. **Where it failed.** Any asset with no usable output, and every criterion the reviewer changed, with the reason. A high change rate on one criterion is named in the thesis as a limitation of the assist, not glossed over.

The blind cards give twelve answers at most, fewer if a No ends a card. That cannot support a reliability statistic; #40's own nine-rater study found chance-corrected agreement hard to interpret at its sample size.

Report both components as qualitative tables in the Results chapter (pass/fail or match/changed per case), not as a statistical claim. That is an honest match to what a manual check over a handful of runs and 10 assets can support.

## What This Enables Next

**Prototype architecture** — the last Phase B document. It defines the module boundaries and the full API surface (this document has been assuming `/runs/{id}/explain` exists; that document is where it actually gets specified alongside every other endpoint), resolves the two-screen question flagged during the interface walkthrough — single-run view versus the sensitivity-sweep comparison view — and now also needs to account for the Colab notebook as a genuinely separate, disconnected piece of the system: not a FastAPI endpoint, a standalone script whose CSV output gets imported once during setup.
