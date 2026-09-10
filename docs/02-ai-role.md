# AI Role — Explanation Layer and Plausibility-Scoring Assist

Turns the architecture principle from `01-original-brief.md` §9 and D6 into actual prompts and interfaces for two AI components. Explanation reads from `02-optimization-formulation.md`'s output and writes to the `explanations` table; plausibility-scoring assist reads asset/zone data and writes suggestions into `candidate_locations` — both from `02-data-model.md`.

**Confirmed scope, per D12:** explanation layer (as originally specified) plus plausibility-scoring assist (§7–10 below). The interactive Q&A layer discussed alongside plausibility-scoring assist is **not** in scope for this prototype — stronger demo value, but higher implementation cost and higher guardrail risk for the hours available; revisit only if Phase C finishes early.

## 1. Scope — what each component does, and what neither does

**Explanation does:** given a completed placement run (from any of the four methods, but reported to the analyst only for the proposed method's result), generate a plain-language explanation of which locations were chosen, why, and how the result compares to the two baselines.

**Plausibility-scoring assist does:** given an asset's type, zone, and which attack paths touch it, generate a first-pass score and justification for each of the four Filter 1 criteria from `formal-problem-definition.md` §4 — reviewed and confirmed or overridden by a human before any value reaches the `candidate_locations` columns the optimizer actually reads.

**Neither does:** choose, adjust, veto, or second-guess a placement. Explanation is never called before `/optimize` completes; plausibility-scoring assist is never called after it — it's a pre-processing step during testbed setup, not something the live system invokes. Neither has write access to the columns that matter without a human step in between: explanation writes only to `explanations` (which can't modify `placement_runs`), and plausibility-scoring assist writes only to `ai_suggested_*` columns (which can't modify the real `plausibility_*` columns without confirmation — see §8).

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

Second, this step is disconnected from the live system by design — it runs once, during testbed setup, before the FastAPI backend or the optimizer ever run, and produces a result (11 scored assets) that gets loaded into SQLite and then never touched again unless the testbed topology changes. That profile is exactly what Colab suits: no session-persistence problem, nothing to keep running, no tunnel back into a live service. Free-tier Colab typically provides a T4 with 15GB VRAM, comfortably running Qwen3 14B at full speed with room to spare — faster and simpler than squeezing it onto a 4GB local card via CPU offload for a task where local deployment carries none of the "this is what a real OT environment would run" argument that justifies keeping explanation local.

### 8. Input and the human-confirmation gate

For each of the 11 assets in `testbed-architecture.md`'s graph:

```
asset_type, zone, is_physical           — from the assets table
which attack path(s) touch this asset   — from attack_path_steps, filtered by asset_id
the four Filter 1 criteria, verbatim    — from formal-problem-definition.md §4
```

Output writes to **columns already added to `candidate_locations` in `02-data-model.md`**, kept separate from the ones the optimizer reads:

```sql
ai_suggested_decoy_exists, ai_suggested_attacker_reach,
ai_suggested_useful_signal, ai_suggested_reliable_indicator,
ai_reasoning, human_confirmed, confirmed_at
```

The real `criterion_decoy_exists`, `criterion_attacker_reach`, `criterion_useful_signal`, `criterion_reliable_indicator` columns — the ones `passes_plausibility` and ultimately `L` get computed from — only get written when `human_confirmed = 1`. An unconfirmed AI suggestion has no path into the optimizer's input. This is the same structural pattern as explanation's safety property in §6, applied to a component that's advisory rather than purely descriptive: the model can be wrong without anything downstream trusting it by default.

### 9. The prompt

**System prompt:**

```
You are assisting a security analyst in applying a deception-placement
plausibility rubric to network assets. For each asset, score four
criteria as yes, mostly, or no, with a one-sentence justification for
each. A human will review every suggestion before it is used — your
job is to give an honest, well-reasoned first pass, not a final answer.
If you are genuinely unsure, say mostly rather than guessing yes or no.
```

**User prompt template (one call per asset):**

```
Asset: {asset_name} ({asset_type}, zone: {zone})
Attack paths that reach this asset: {path_list}

Score these four criteria:
1. Can a defender-controlled decoy plausibly exist at this asset type?
2. Would an attacker following one of the listed paths plausibly reach
   or interact with it?
3. Would that interaction yield useful signal?
4. Is the interaction a reliable indicator of malicious intent (as
   opposed to routine legitimate traffic)?

For each: answer yes / mostly / no, with one sentence of reasoning.
```

### 10. Worked example and the review step

For **OT Firewall** (no attack path terminates there — it's a conduit every path crosses, not a target): expected output is `no` on criterion 1 with reasoning close to "a firewall is functional infrastructure an attacker routes through, not a target it interacts with" — matching the manual reasoning already in `testbed-architecture.md`'s worked example. For **Engineering WS-2** (on P1's path): expected output is `yes` across all four, reasoning citing the direct precedent in existing honeypot tooling.

The review screen shows each asset's four suggested scores as compact labeled badges plus the one-line reasoning, with a single confirm action per asset, or manual edit before confirming. Eleven assets, each taking seconds to confirm once the AI's reasoning is visible — the time cost is the review, not the scoring itself. Where the AI's reasoning doesn't hold up (borderline cases like a DMZ-zone asset where detectability muddies the "reliable indicator" question), overriding a single badge before confirming is the expected path, not an edge case to design around specially.

This isn't just a cautious default — it's addressing a documented failure mode. Source #318 (arXiv:2509.23573) found standard LLM-as-a-judge classification unreliable specifically because models "tend to rationalize their own outputs" rather than critically evaluate them, and proposes the same human-in-the-loop pattern used here. Worth citing directly in the methodology chapter as the reason confirmation isn't optional. A refinement worth naming even if not implemented: source #319 found confidence-based review routing (prioritizing human attention on hedged "mostly" answers over clean yes/no ones) more efficient than reviewing everything uniformly — a reasonable next step if the review step ever needs to scale past 11 assets.

## Evaluating both components (the secondary research question)

`formal-problem-definition.md` §8 asks specifically whether the explanation is accurate and useful, not just whether it runs. Given weekend hours don't support a full user study, the honest, scoped-down evaluation for **explanation** is a manual accuracy check: generate explanations for each of the sensitivity-sweep runs from Phase D, and check each one against three criteria —

1. **Factual accuracy** — do the numbers it states match `run_metrics` exactly, or does it round oddly, invent a figure, or misattribute a metric to the wrong method?
2. **Guardrail adherence** — does it ever suggest a change, recommend an additional decoy, or hedge on the algorithm's choice, despite being told not to?
3. **Readability** — would this actually help an analyst who hadn't seen the raw numbers?

**Plausibility-scoring assist** gets a parallel but distinct check, since its failure mode is different — not "does the text read well" but "does a human reviewer agree with it": for all 11 assets, note whether the confirmed values matched the AI's suggestion unedited, or required a correction, and if corrected, why. A high edit rate on a specific criterion (not just occasional disagreement) would be worth naming in the thesis as a limitation of that specific check, not glossed over.

Report both as qualitative tables in the Results chapter (pass/fail or match/edited per case), not a statistical claim — an honest match to what a manual check over a handful of runs and 11 assets can actually support.

## What This Enables Next

**Prototype architecture** — the last Phase B document. It defines the module boundaries and the full API surface (this document has been assuming `/runs/{id}/explain` exists; that document is where it actually gets specified alongside every other endpoint), resolves the two-screen question flagged during the interface walkthrough — single-run view versus the sensitivity-sweep comparison view — and now also needs to account for the Colab notebook as a genuinely separate, disconnected piece of the system: not a FastAPI endpoint, a standalone script whose CSV output gets imported once during setup.
