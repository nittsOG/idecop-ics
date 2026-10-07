# Project Phases

The full lifecycle of the M.Tech project, start to defense. This is the authoritative status tracker — the roadmap table in `00-project-index.md` now points here instead of keeping its own copy, so there's one place to check, not two that can drift apart.

## Overview

```
A: Foundation ──▶ B: Detailed Design ──▶ C: Build ──▶ D: Evaluation ──▶ E: Writing ──▶ F: Defense
   (complete)         (complete)            (core done)                   ↑
                                                          can start early ─┘
```

Six phases. A and B are done. C's core computational build is done, with the items listed under Phase C still outstanding. D's inputs were frozen and are being corrected before any campaign: the objective's normalisation by D25, and the candidate set under A32. D is gated on A32 and then A12. E overlaps earlier than it looks — worth reading that section even though it's fifth on the list.

## Phase A — Foundation ✅ Complete (its one open item was closed on 6 October 2026)

Literature review; analysis of existing OT deception solutions and existing placement-optimization research; formal problem definition; threat/attack model; testbed architecture.

**Original roadmap items covered:** 1, 2, 3, 4, 5, 6
**Documents:** `sources.md`, `iteration-2` through `iteration-10-findings.md`, `research-synthesis-implementation.md`, `formal-problem-definition.md`, `threat-attack-model.md`, `testbed-architecture.md`
**Exit criteria (all met):** novelty claim tested against the closest available prior art via primary-source read, not just an abstract; tested again via a targeted water/manufacturing sector check; the optimization problem has a precise mathematical statement; the testbed has a verified path for every step of every attack scenario.
**One open item, tracked not blocking:** the full text of `sources.md` #315 (a manufacturing-sector paper) hasn't been read yet — logged in `00-action-items.md` rather than held as a phase gate, since it can be resolved in parallel with Phase B. *Closed 6 October 2026:* #315 was read in full and is not a placement competitor (A4). The same batch of supplied sources closed A8, A9 and A39 and the claims half of A29; CATCH (A33) remains unobtainable.

## Phase B — Detailed Design ✅ Complete

Takes each component named in Phase A's system diagram and specifies it in enough detail that it could be handed to someone else to code without further design decisions on their part.

- **Data model** — SQLite schema for `G`, `L`, `P`, and computed scores; how FastAPI reads/writes it ✅
- **Optimization formulation, detailed** — actual pseudocode for the greedy algorithm and the MILP formulation, not just the objective function already fixed in Phase A ✅
- **AI role, detailed** — the actual prompt structure and interface between the optimizer's output and the local LLM, plus the plausibility-scoring-assist component added via D12 ✅
- **Prototype architecture, detailed** — module breakdown and API contract between components ✅

**Original roadmap items covered:** 7 ✅, and deepens 8 ✅, 9 ✅, 10 ✅ beyond their prior "specified but not detailed" state
**Documents:** `02-data-model.md`, `02-optimization-formulation.md`, `02-ai-role.md`, `02-prototype-architecture.md`
**Exit criteria (met):** every box in the testbed architecture's system diagram has a spec concrete enough to start coding against directly.

## Phase C — Build 🔨 In progress

The actual construction: standing up the 7 physical VMs, implementing the graph model and data store, the optimizer, the AI explanation layer, and the FastAPI/visualization frontend. Also includes the plausibility-scoring Colab notebook (D12) — genuinely separate from the rest, since it's a standalone script, not a service.

**Historical (D14) — the first slice, Screen 3, complete and tested (see `phase-c-screen-3.zip`):** the actual SQLite database, built and verified against `02-data-model.md`'s schema (a real gap was found and fixed in the process — `edges`/`conduits` were never seeded, leaving zero graph connectivity; fixed and fed back into that document); a working FastAPI backend (`GET /assets`, `GET /candidates`, `POST /candidates/{id}/confirm`) tested with real requests including validation and error cases; a working React frontend for the plausibility-review screen, builds cleanly. Not yet built: graph_model, the optimizer, `/optimize`/`/runs`/`/explain`, Screens 1 and 2, the Colab notebook itself, and the physical VMs.

**Suggested internal order:** the Colab notebook can happen first, independent of everything else — it only needs the asset/zone list, not a live testbed or database, and its output (confirmed values in `candidate_locations`) is needed before the optimizer has a real `L` to run against. Testbed VMs and graph model/data store next (these can proceed in parallel — the graph model doesn't need live VMs); optimizer after that (developable and testable against the graph alone, before the testbed is fully live — worth starting this early given weekend-hours constraints); AI explanation layer and UI integration last, once there's real optimizer output to explain and display.

**Status as of D24 (28 September 2026).** *Built and verified:* the SQLite database; `graph_model` (betweenness centrality; `Crit(v)` including `ConduitSL`, D20); the optimizer — five implementations sharing one `score()`: greedy, distorted greedy (D23), random, centrality and the exact MILP (corrected in D24); the FastAPI backend with nine endpoints; the React frontend's Screen 3 (plausibility review) and Screen 1 (single-run dashboard); and three scripts — `run_comparison.py`, `sweep.py` and `structure_check.py`. *Not yet built:* the explanation layer `/runs/{id}/explain` (A6, needs Ollama); Screen 2, the sensitivity-sweep comparison view; the Colab plausibility-scoring notebook (A20); and the physical VM testbed (A21, scope under A16).

**Exit criteria:** every method (random, centrality, and the proposed method with its MILP validation — five implementations since D23) runs end-to-end against the testbed and produces comparable output. *Met against the modelled graph, not yet against a physical testbed* — whether that matters depends on A16 and on the evaluation design chosen under A12.

**Realistic expectation:** the core build (testbed, optimizer, explanation layer, UI) is still very likely the single largest time cost in the whole project — the Colab notebook doesn't change that, it's a small, early, parallel-track item, not a schedule risk of its own. If the core build slips, everything after it slips with it — worth surfacing schedule problems here early rather than discovering them at Phase D.

## Phase D — Evaluation

Run every method against P1–P5 (P5 added by D27) on the comparison grid held in `scripts/sweep.py` (D24), collect Coverage / Early / CritProt / Risk / Cost / runtime for each, run the weight-sensitivity sweep from `formal-problem-definition.md` §5, and produce the comparison tables and charts.

**Inputs frozen (D20–D22a); evaluation code corrected (D23, D24); two input defects corrected before any campaign — Risk and Cost now divided by a fixed K = 4 (D25), and the candidate set re-derived by §4's filters (A32, pending; its rules fixed by D26). Gated on A32, with A35–A38 and A40 settled before the freeze and A41 before the scoring notebook runs, then A12.** On the seeded candidate set greedy equals the exhaustive optimum in every cell *by construction* (D25: every attack path meets exactly one candidate). Comparing methods on F alone is implied by optimality and cannot test whether F is a good objective. An evaluation criterion outside F must be chosen — held-out attack paths, input-perturbation robustness, synthetic larger instances or testbed attack simulation — and frozen before the campaign runs.

**Original roadmap item covered:** 11
**Exit criteria:** results speak to the primary research question in `formal-problem-definition.md` §8 — including honestly, if they don't support it as strongly as hoped. A negative or mixed result, reported honestly, is a valid thesis outcome; a result quietly reframed to look better than it is isn't.

## Phase E — Thesis Writing

Introduction, Literature Review, Methodology, Implementation, Evaluation/Results, Conclusion.

**This phase starts earlier than its position in the list suggests.** The Literature Review chapter is draftable right now, from the `01-*` files, without waiting for anything else. The Methodology chapter is draftable as soon as Phase B closes. Only the Implementation and Results chapters strictly need Phase C and D finished. Given weekend-hours constraints, drafting these two chapters early — in parallel with Phase C, not after it — is worth doing deliberately rather than defaulting to writing everything at the end.

**Documents:** `05-*` chapter drafts

## Phase F — Defense Preparation & Submission

Guide review cycles, viva preparation, formatting to NFSU's submission requirements, final submission.

**Exit criteria:** submitted and defended.

## Where we are right now

**As of D26 (3 October 2026).** Phases A and B are complete. Phase C's core computational build is complete and verified — database, graph model, all five optimizer implementations, the API and two of three screens — with the explanation layer, Screen 2 and the physical testbed outstanding. The Colab notebook was written in D26 and has not yet been run.

Phase D's inputs were frozen (D20–D22a) and its evaluation code corrected (D23, D24). D25 then found two input defects before any campaign ran:
- On the seeded candidate set, greedy is optimal by construction.
- Risk and Cost were divided by the budget. They are now divided by a fixed K = 4.

D25 also fixed in advance what the thesis may claim. Phase D is gated on:
1. **A32** — re-deriving the candidate set through §4's filters for every asset (your confirmation in Screen 3), then re-running with the effect recorded. **D26 (3 October 2026) fixed the rules first:**
   - what a candidate is, and how the four scores combine;
   - #40's four-level scale;
   - route A, an AI first pass with three blind cards and written reasons.

   Screen 3 was rebuilt, the scoring notebook was written (not yet run), and the seed no longer pre-judges L, which is empty until your review. Remaining steps, in order: the blind cards; the notebook and import; reviewing the other seven cards; exporting the review; D22a scores for new candidates; freeze and re-run.

   *Added 5 October 2026:* four input questions found while preparing the guide's progress report are also settled before the freeze — A35 (what an edge weight means), A36 (a path's target), A37 (placeholder criticality inputs) and A38 (the missing OT DMZ–Control conduit).

   *Added 6 October 2026,* from the sources you supplied that day: a fifth, A40 — the criticality formula multiplies centrality by damage where the patent it draws on adds them — and a label fix, A41 — T0832's tactic is Impact — which must land before the notebook runs.
2. **A12** — the research question's wording together with an evaluation criterion that is not F itself.
3. **A15** — agreement with the guide that a mixed result is acceptable.

TA-1 did not take place on 22 September and has not been rescheduled (A14). Phase E's literature-review and methodology chapters can be drafted now.
