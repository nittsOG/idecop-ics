# Project Index — AI-Assisted Deception Placement Optimization for OT/ICS

Master reference for every document produced in this thread. Updated each time a new document is created. Organized against the 12-item roadmap from the original project brief so it's always clear what's done, what's in progress, and what's still open.

## How to use this

- New to the project? Read in this order: `research-synthesis-implementation.md` → `formal-problem-definition.md` → `threat-attack-model.md` → `testbed-architecture.md`. That's the whole current specification in ~30 minutes, without the research trail behind it.
- Need a specific citation or fact? `sources.md` is the single running bibliography (312 entries as of this point) — search it before searching the web again.
- Need to see *how* a conclusion was reached, not just the conclusion? The `iteration-N-findings.md` files are the reasoning trail.
- Need to know *why* a specific choice was made (for the methodology chapter, or a guide question)? `00-decisions-log.md`.
- Not sure what to do next, or what's still waiting on you specifically? `00-action-items.md` for manual tasks, `00-project-phases.md` for where the project stands overall.
- Forgot how any of this is organized or maintained? `00-workflow-and-rules.md` — that document governs this one, not the other way around.

## Project status

Phase A (Foundation) is complete; Phase B (Detailed Design) is next. Full phase breakdown, exit criteria, and the original 12-item roadmap mapped against it: `00-project-phases.md`. That file is now the single tracker for project status — kept here too would mean two places that can drift out of sync, which is exactly what the naming/maintenance rules in `00-workflow-and-rules.md` exist to prevent.

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
        02-data-model.md (next)
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
| `sources.md` | Research | Living | 💾 Offline | — | `research-synthesis-implementation.md`, every specification document |
| `01-thesis-citation-shortlist.md` | Research | Stable | 💾 Offline | `sources.md` | Literature Review chapter (Phase E) |
| `01-original-brief.md` | Research | Stable | 📌 Project Knowledge | — | Everything — this is the origin the whole chain traces back to |
| `iteration-2-findings.md` … `iteration-10-findings.md` (9 files) | Research | Stable | 💾 Offline | Previous iteration's open-items list | `sources.md`, `research-synthesis-implementation.md` |
| `research-synthesis-implementation.md` | Research | Stable | 📌 Project Knowledge | `sources.md`, all iteration findings | `formal-problem-definition.md` |
| `formal-problem-definition.md` | Specification | Stable | 📌 Project Knowledge | `research-synthesis-implementation.md` | `threat-attack-model.md`, `testbed-architecture.md`, every future `02-` document |
| `threat-attack-model.md` | Specification | Stable | 📌 Project Knowledge | `formal-problem-definition.md` §3 | `testbed-architecture.md`, future `03-evaluation-methodology.md` |
| `testbed-architecture.md` | Specification | Stable | 📌 Project Knowledge | `formal-problem-definition.md` §1, `threat-attack-model.md` | `02-data-model.md`, `02-prototype-architecture.md` |
| `02-data-model.md` | Specification | Stable | 💾 Offline | `formal-problem-definition.md`, `testbed-architecture.md`, `threat-attack-model.md` | `02-optimization-formulation.md`, `02-ai-role.md`, `02-prototype-architecture.md` |
| `02-optimization-formulation.md` | Specification | Stable | 💾 Offline | `formal-problem-definition.md` §5–7, `02-data-model.md` | `02-ai-role.md`, `02-prototype-architecture.md` |
| `02-ai-role.md` | Specification | Stable | 💾 Offline | `02-optimization-formulation.md`, `02-data-model.md`, `01-original-brief.md` §9 | `02-prototype-architecture.md` |
| `02-prototype-architecture.md` | Specification | Stable | 💾 Offline | `02-data-model.md`, `02-optimization-formulation.md`, `02-ai-role.md` | Phase C build directly |

**26 files as of this point — 9 in Project Knowledge, 17 offline.** This table is what gets a new row every time — per the trigger in `00-workflow-and-rules.md`'s maintenance table, which now includes assigning a tier to every new file, not just a category.

## Context tier — what goes in Project Knowledge, what stays offline

Anthropic's own documentation states Project Knowledge allows unlimited files, capped only by total content fitting the context window (no fixed file-count limit, officially). In practice, though, a widely-reported behavior shift kicks in well before that: Project Knowledge has been observed switching from loading everything directly into context to a search-based retrieval mode at around a dozen files — sometimes at a small fraction of the raw token limit, not when the token budget is actually exhausted. That's a real-world report, not official Anthropic documentation, and these thresholds change — but it's reason enough to plan conservatively rather than assume "unlimited" means "load everything."

**Policy: keep Project Knowledge to 10 files or fewer.** Currently 8, tagged 📌 above. That's deliberate headroom, not the max — leaves room to add one or two more before anything needs to be retired.

**What earns a 📌 Project Knowledge slot:** files needed to orient *any* new conversation about this project, regardless of which specific task it's about — current phase and status, the rules governing how work gets done, why past decisions were made, and the core specification (the math problem, the threat model, the testbed) everything else builds on.

**What stays 💾 Offline, provided manually when a task needs it:** `sources.md` — despite being central to the project, it's the single largest file here and only needed for citation-specific work (writing the lit review chapter, verifying a claim), not for most day-to-day specification or build tasks. The nine iteration-findings files are the *reasoning trail* behind conclusions already captured in `research-synthesis-implementation.md` — valuable when revisiting *why* a research conclusion was reached, rarely needed otherwise. `00-action-items.md` and `00-repository-structure.md` are short and low-frequency-need.

**Going forward:** every new file gets a tier assignment the moment it's created, same as it gets a category and dependencies. If Project Knowledge would exceed 10, something already there graduates to offline first — the likely first candidate is `testbed-architecture.md`, once its content is fully absorbed into later Phase C documents and it's needed for reference rather than active building.

## Keeping this available across conversations

These files exist in this conversation. Since it's now inside a Project, other conversations in the same project can search and read this chat's content — but if you want a document available to me directly in a *new* conversation without re-deriving it, the reliable way is downloading it and adding it to this Project's knowledge base through Project settings. The 8 files tagged 📌 above are the ones worth adding; the "Context tier" section explains why the rest are better kept offline and provided when a specific task needs them.

## Next document

Per `00-project-phases.md` (Phase B): **`02-data-model.md`** — the SQLite schema for `G`, `L`, `P`, and computed scores, and how the FastAPI backend reads and writes it.
