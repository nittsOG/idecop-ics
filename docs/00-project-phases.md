# Project Phases

The full lifecycle of the M.Tech project, start to defense. This is the authoritative status tracker — the roadmap table in `00-project-index.md` now points here instead of keeping its own copy, so there's one place to check, not two that can drift apart.

## Overview

```
A: Foundation ──▶ B: Detailed Design ──▶ C: Build ──▶ D: Evaluation ──▶ E: Writing ──▶ F: Defense
   (complete)         (complete)            (next)                        ↑
                                                          can start early ─┘
```

Six phases. A and B are done. C is next. E overlaps earlier than it looks — worth reading that section even though it's fifth on the list.

## Phase A — Foundation ✅ Complete (one minor open item, doesn't block Phase B)

Literature review; analysis of existing OT deception solutions and existing placement-optimization research; formal problem definition; threat/attack model; testbed architecture.

**Original roadmap items covered:** 1, 2, 3, 4, 5, 6
**Documents:** `sources.md`, `iteration-2` through `iteration-10-findings.md`, `research-synthesis-implementation.md`, `formal-problem-definition.md`, `threat-attack-model.md`, `testbed-architecture.md`
**Exit criteria (all met):** novelty claim tested against the closest available prior art via primary-source read, not just an abstract; tested again via a targeted water/manufacturing sector check; the optimization problem has a precise mathematical statement; the testbed has a verified path for every step of every attack scenario.
**One open item, tracked not blocking:** the full text of `sources.md` #315 (a manufacturing-sector paper) hasn't been read yet — logged in `00-action-items.md` rather than held as a phase gate, since it can be resolved in parallel with Phase B.

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

**Started — Screen 3 slice complete and tested (see `phase-c-screen-3.zip`):** the actual SQLite database, built and verified against `02-data-model.md`'s schema (a real gap was found and fixed in the process — `edges`/`conduits` were never seeded, leaving zero graph connectivity; fixed and fed back into that document); a working FastAPI backend (`GET /assets`, `GET /candidates`, `POST /candidates/{id}/confirm`) tested with real requests including validation and error cases; a working React frontend for the plausibility-review screen, builds cleanly. Not yet built: graph_model, the optimizer, `/optimize`/`/runs`/`/explain`, Screens 1 and 2, the Colab notebook itself, and the physical VMs.

**Suggested internal order:** the Colab notebook can happen first, independent of everything else — it only needs the asset/zone list, not a live testbed or database, and its output (confirmed values in `candidate_locations`) is needed before the optimizer has a real `L` to run against. Testbed VMs and graph model/data store next (these can proceed in parallel — the graph model doesn't need live VMs); optimizer after that (developable and testable against the graph alone, before the testbed is fully live — worth starting this early given weekend-hours constraints); AI explanation layer and UI integration last, once there's real optimizer output to explain and display.

**Exit criteria:** all three methods (random, centrality, proposed) run end-to-end against the testbed and produce comparable output.

**Realistic expectation:** the core build (testbed, optimizer, explanation layer, UI) is still very likely the single largest time cost in the whole project — the Colab notebook doesn't change that, it's a small, early, parallel-track item, not a schedule risk of its own. If the core build slips, everything after it slips with it — worth surfacing schedule problems here early rather than discovering them at Phase D.

## Phase D — Evaluation

Run Methods 1–3 against P1–P3, collect Coverage / Early / CritProt / Risk / Cost / runtime for each, run the weight-sensitivity sweep from `formal-problem-definition.md` §5, produce the comparison tables and charts.

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

Phase A and Phase B are both complete. Phase C is next, starting with Screen 3 (plausibility review) and the testbed VMs, per `02-prototype-architecture.md` §3's suggested build order.
