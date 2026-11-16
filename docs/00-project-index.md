# Project Index — AI-Assisted Deception Placement Optimization for OT/ICS

Master reference for every document produced in this thread. Updated each time a new document is created. Organized against the 12-item roadmap from the original project brief so it's always clear what's done, what's in progress, and what's still open.

## How to use this

- New to the project? Read in this order: `research-synthesis-implementation.md` → `formal-problem-definition.md` → `threat-attack-model.md` → `testbed-architecture.md`. That's the whole current specification in ~30 minutes, without the research trail behind it.
- Need a specific citation or fact? `sources.md` is the single running bibliography (988 entries as of 15 November 2026) — search it before searching the web again.
- Need to see *how* a conclusion was reached, not just the conclusion? The `iteration-N-findings.md` files are the reasoning trail.
- Need to know *why* a specific choice was made (for the methodology chapter, or a guide question)? `00-decisions-log.md`.
- Not sure what to do next, or what's still waiting on you specifically? `00-action-items.md` for manual tasks, `00-project-phases.md` for where the project stands overall.
- Forgot how any of this is organized or maintained? `00-workflow-and-rules.md` — that document governs this one, not the other way around.

## Project status

Current status lives only in `00-project-phases.md` — see its "Where we are right now" section. (D24 removed a status line from this file that had drifted to "Phase B is next" while Phase C's core build was already complete — exactly the failure the next sentence warns about.) Full phase breakdown, exit criteria, and the original 12-item roadmap mapped against it are there too. That file is now the single tracker for project status — kept here too would mean two places that can drift out of sync, which is exactly what the naming/maintenance rules in `00-workflow-and-rules.md` exist to prevent.

## File registry

Every file, what it depends on, and what depends on it — not just what it contains. This is what a flat list of names doesn't give you once the count grows, and it's the piece git's commit history won't provide either once the repo exists (git tracks *changes to* a file over time; it doesn't tell you *which other files* a change should ripple into). Both matter, for different reasons — keep both once `/docs` moves into git.

**Status** means: **Living** = updated on an ongoing basis, no "finished" state (bibliographies, logs, trackers). **Stable** = written once to represent a settled decision or analysis; only touched again for corrections, not routine updates.

### Dependency chain — the specification's actual lineage
```
01-original-brief.md (the origin — scope boundary, working principle, original roadmap)
     │
     ▼
sources.md ◀── iteration-2 … iteration-10-findings.md
     │              (each logs new findings back into sources.md)
     ▼
research-synthesis-implementation.md
     ▼
formal-problem-definition.md
     │
     ├──▶ threat-attack-model.md ──┐
     │                             ▼
     └──▶ testbed-architecture.md ◀┘
                    │
                    ▼
        02-data-model.md
                    │
                    ▼
   02-optimization-formulation.md, 02-ai-role.md,
   02-prototype-architecture.md (after that)
```
If a document upstream in this chain changes in a way that invalidates something downstream, that's exactly when a file's status should move to **Superseded** rather than being silently left inconsistent — noted in `00-decisions-log.md` when it happens, not just fixed quietly.

### Registry

| File | Category | Status | Tier | Depends on | Feeds into |
|---|---|---|---|---|---|
| `00-project-index.md` | Meta | Living | 📌 Project Knowledge | — | — (this is the entry point) |
| `00-project-phases.md` | Meta | Living | 📌 Project Knowledge | Original brief's roadmap; status of every spec document | — |
| `00-workflow-and-rules.md` | Meta | Stable | 📌 Project Knowledge | — | Governs naming/lifecycle for every other file |
| `00-decisions-log.md` | Meta | Living | 📌 Project Knowledge | `research-synthesis-implementation.md`, `formal-problem-definition.md`, `testbed-architecture.md` | Methodology chapter (Phase E) |
| `00-action-items.md` | Meta | Living | 💾 Offline | — | — |
| `00-repository-structure.md` | Meta | Stable | 💾 Offline (until Phase C) | `00-workflow-and-rules.md`, `00-project-phases.md` | GitHub repo setup at Phase C |
| `00-local-storage-setup.md` | Meta | Stable | 💾 Offline | `00-repository-structure.md` | Local folder setup, now; migrates directly into the GitHub repo at Phase C |
| `00-glossary.md` | Meta | Living | 💾 Offline | `formal-problem-definition.md`, `00-decisions-log.md`: its definitions follow the specification and change with it | `README.md`'s reading guide; the thesis glossary and list of abbreviations (`05-thesis-structure.md`, `05-front-matter-pack.md`) |
| `00-project-timeline.md` | Meta | Stale since 28 September 2026, by its own banner: anchored on TA-1, which did not take place; not to be scheduled from until it is rebuilt | 💾 Offline | `00-project-phases.md`; the dates A14 asks for | — until it is rebuilt |
| `sources.md` | Research | Living | 💾 Offline | — | `research-synthesis-implementation.md`, every specification document |
| `01-thesis-citation-shortlist.md` | Research | Stable | 💾 Offline | `sources.md` | Literature Review chapter (Phase E) |
| `01-search-protocol.md` | Research | Stable (fixed before the first query, D34; changed only by recorded amendments: 1 on 5 November, 2 in D35, 3 to 7 in D36) | 💾 Offline | `sources.md`, the novelty claim (D7, A28), `00-action-items.md` A17 and A29 | `sources.md` run entries; `01-search-screening-record.md`; Literature Review chapter (Phase E) and its search appendix; A28's opening clause |
| `01-search-screening-record.md` | Research | Complete for A17 and A29 as the protocol fixed them (D35 for the main search; D36 for the later paper runs and the patent arm) | 💾 Offline | `01-search-protocol.md`, `sources.md` #405–#416 and #613–#643 | D35 and D36; `sources.md` #417–#988; Literature Review chapter (Phase E) and its search appendix; A28 |
| `01-original-brief.md` | Research | Stable | 📌 Project Knowledge | — | Everything — this is the origin the whole chain traces back to |
| `iteration-2-findings.md` … `iteration-10-findings.md` (9 files) | Research | Stable | 💾 Offline | Previous iteration's open-items list | `sources.md`, `research-synthesis-implementation.md` |
| `iteration-11-findings.md` … `iteration-13-findings.md` (3 files) | Research | Stable | 💾 Offline | `research-synthesis-implementation.md`; D9, after which each iteration tested one named question | `sources.md` (#328–#336, #338–#346). 11: `formal-problem-definition.md` §4 and A22, resolved by D20. 12: A23, resolved by D22's rubric (`02-detectability-rubric.md`), and A25. 13: `03-commercial-prior-art-analysis.md`, A28 and A29 |
| `research-synthesis-implementation.md` | Research | Stable | 📌 Project Knowledge | `sources.md`, all iteration findings | `formal-problem-definition.md` |
| `formal-problem-definition.md` | Specification | Stable | 📌 Project Knowledge | `research-synthesis-implementation.md` | `threat-attack-model.md`, `testbed-architecture.md`, every future `02-` document |
| `threat-attack-model.md` | Specification | Stable | 📌 Project Knowledge | `formal-problem-definition.md` §3 | `testbed-architecture.md`, future `03-evaluation-methodology.md` |
| `testbed-architecture.md` | Specification | Stable | 📌 Project Knowledge | `formal-problem-definition.md` §1, `threat-attack-model.md` | `02-data-model.md`, `02-prototype-architecture.md` |
| `02-data-model.md` | Specification | Stable | 💾 Offline | `formal-problem-definition.md`, `testbed-architecture.md`, `threat-attack-model.md` | `02-optimization-formulation.md`, `02-ai-role.md`, `02-prototype-architecture.md` |
| `02-optimization-formulation.md` | Specification | Stable | 💾 Offline | `formal-problem-definition.md` §5–7, `02-data-model.md` | `02-ai-role.md`, `02-prototype-architecture.md` |
| `02-ai-role.md` | Specification | Stable | 💾 Offline | `02-optimization-formulation.md`, `02-data-model.md`, `01-original-brief.md` §9 | `02-prototype-architecture.md` |
| `02-prototype-architecture.md` | Specification | Stable | 💾 Offline | `02-data-model.md`, `02-optimization-formulation.md`, `02-ai-role.md` | Phase C build directly |
| `02-detectability-rubric.md` | Specification | Stable: version 2 (D22a); five scores added in D31; its two gaps settled in D33 | 💾 Offline | `formal-problem-definition.md` §4, `sources.md` #352 | `detectability_risk` in `data/seed.sql`; `formal-problem-definition.md` §4; `02-data-model.md` |
| `02-system-flow.md` | Specification | Stable; corrected in place as the code changes | 💾 Offline | The repository's code, which it was written by running; the specification it is checked against (its §7) | `README.md`'s reading guide; the thesis's §3.1 (`05-thesis-structure.md`, `05-front-matter-pack.md`) |
| `03-commercial-prior-art-analysis.md` | Evaluation | Stable; corrected in place (D28 moved it to claims level) | 💾 Offline | `iteration-13-findings.md`, `sources.md` #347 | The novelty claim (A28) and A29; `research-synthesis-implementation.md`'s header note; `01-search-protocol.md` |
| `03-honest-review.md` | Evaluation | Archival, by its own banner: a record of the three-path instance before D21; its numbers are kept as measured | 💾 Offline | `formal-problem-definition.md`, `scripts/structure_check.py` | D20's corrections; `01-search-protocol.md` (its §B test) |
| `04-setup-guide.md` | Implementation | Stable | 💾 Offline | D29's pinned environment (`.python-version`, `requirements.txt`, `requirements.lock`) and `scripts/setup.py`, `src/frontend/package-lock.json`, `02-prototype-architecture.md` | `README.md`'s *Running it*, its short form; every local run of Screen 3 and the scripts |
| `04-deployment-requirements.md` | Implementation | Stable; corrected in place (D25) | 💾 Offline | The built prototype; `04-setup-guide.md` | The thesis's Limitations and Future Work chapter (`05-thesis-structure.md`) |
| `05-front-matter-pack.md` | Thesis | Living: drafts, adjusted when results and the template arrive | 💾 Offline | `formal-problem-definition.md`, `threat-attack-model.md`, `testbed-architecture.md`, `02-system-flow.md`, `00-glossary.md` | The thesis front matter, once the template exists (A14) |
| `05-thesis-structure.md` | Thesis | Living: the writing plan, updated when the documents it draws on change | 💾 Offline | The specification and research documents it maps to chapters; `00-decisions-log.md` | Phase E's chapter drafts (`05-*`) |

**42 files in `docs/` as of 16 November 2026, every one with a row — 9 in Project Knowledge, 33 offline.** This table is what gets a new row every time — per the trigger in `00-workflow-and-rules.md`'s maintenance table, which now includes assigning a tier to every new file, not just a category.

*13 October 2026: this table is behind the folder.*
- `04-setup-guide.md` was added today.
- Twelve docs in `docs/` have no row:
  - `00-glossary.md`, `00-project-timeline.md`;
  - `02-detectability-rubric.md`, `02-system-flow.md`;
  - `03-commercial-prior-art-analysis.md`, `03-honest-review.md`;
  - `04-deployment-requirements.md`;
  - `05-front-matter-pack.md`, `05-thesis-structure.md`;
  - `iteration-11` to `iteration-13-findings.md`.
- The count above is out of date as well: the table covers 28 of the folder's 40 files.
- Registering the twelve is outstanding.
- *Resolved 16 November 2026:* the twelve now have rows, and the table covers all 42 files in `docs/`.

## Context tier — what goes in Project Knowledge, what stays offline

Anthropic's own documentation states Project Knowledge allows unlimited files, capped only by total content fitting the context window (no fixed file-count limit, officially). In practice, though, a widely-reported behavior shift kicks in well before that: Project Knowledge has been observed switching from loading everything directly into context to a search-based retrieval mode at around a dozen files — sometimes at a small fraction of the raw token limit, not when the token budget is actually exhausted. That's a real-world report, not official Anthropic documentation, and these thresholds change — but it's reason enough to plan conservatively rather than assume "unlimited" means "load everything."

**Policy: keep Project Knowledge to 10 files or fewer.** Currently 9, tagged 📌 above. That's deliberate headroom, not the max — leaves room to add one or two more before anything needs to be retired.

**What earns a 📌 Project Knowledge slot:** files needed to orient *any* new conversation about this project, regardless of which specific task it's about — current phase and status, the rules governing how work gets done, why past decisions were made, and the core specification (the math problem, the threat model, the testbed) everything else builds on.

**What stays 💾 Offline, provided manually when a task needs it:** `sources.md` — despite being central to the project, it's the single largest file here and only needed for citation-specific work (writing the lit review chapter, verifying a claim), not for most day-to-day specification or build tasks. The twelve iteration-findings files are the *reasoning trail* behind conclusions already captured elsewhere (iterations 2–10 in `research-synthesis-implementation.md`, 11–13 in the documents their row names) — valuable when revisiting *why* a research conclusion was reached, rarely needed otherwise. `00-action-items.md` and `00-repository-structure.md` are short and low-frequency-need.

**Going forward:** every new file gets a tier assignment the moment it's created, same as it gets a category and dependencies. If Project Knowledge would exceed 10, something already there graduates to offline first — the likely first candidate is `testbed-architecture.md`, once its content is fully absorbed into later Phase C documents and it's needed for reference rather than active building.

## Keeping this available across conversations

> 📌 **SUPERSEDED (29 September 2026).** The paragraph below told you to download the 📌 files and add them to Project Knowledge yourself, and still counts 8 of them. Under the *Project Knowledge sync* rule in `00-workflow-and-rules.md`, Claude keeps all nine 📌 docs identical to their GitHub versions, syncing after every push and showing you each sync as a table; you add nothing by hand. Files marked 💾 stay offline in the repository and are fetched from GitHub when a task needs them. Kept below as the original instruction.

These files exist in this conversation. Since it's now inside a Project, other conversations in the same project can search and read this chat's content — but if you want a document available to me directly in a *new* conversation without re-deriving it, the reliable way is downloading it and adding it to this Project's knowledge base through Project settings. The 8 files tagged 📌 above are the ones worth adding; the "Context tier" section explains why the rest are better kept offline and provided when a specific task needs them.

## Next document

> 📌 **SUPERSEDED (29 September 2026).** What comes next is tracked only in `00-project-phases.md`, under *Where we are right now*. This line pointed at a Phase B document that was finished long ago — the same drift as the status line removed from this file in D24. Kept below as the original entry.

Per `00-project-phases.md` (Phase B): **`02-data-model.md`** — the SQLite schema for `G`, `L`, `P`, and computed scores, and how the FastAPI backend reads and writes it.
