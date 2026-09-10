# Workflow, Rules, and Naming Convention

The operating procedure for this project from this point forward. This is the document to update if any of these rules stop working for you.

## Naming convention (applies from this point forward)

Format: `[phase]-[descriptive-name].md`

| Prefix | Phase |
|---|---|
| `00-` | Meta — index, this file, decisions log, action items |
| `01-` | Research & literature — sources, iteration findings, synthesis |
| `02-` | Specification — problem definition, threat model, testbed, data model, optimization, AI role, prototype architecture |
| `03-` | Evaluation — methodology, results |
| `04-` | Implementation & roadmap |
| `05-` | Thesis writing — chapter drafts, if/when we get there |

**Existing files are not being renamed.** Renaming would break any copies you've already downloaded and create a mismatch between what's here and what's on your machine — more confusing, not less. Here's their equivalent phase for reference:

| Existing file | Equivalent phase |
|---|---|
| `sources.md` | 01 |
| `iteration-2-findings.md` … `iteration-10-findings.md` | 01 |
| `research-synthesis-implementation.md` | 01 |
| `formal-problem-definition.md` | 02 |
| `threat-attack-model.md` | 02 |
| `testbed-architecture.md` | 02 |

Everything created from here on uses the prefix. Next document (`data model`) will be `02-data-model.md`, not `data-model.md`.

## File lifecycle rules

1. **One canonical file per document.** Corrections and extensions happen in place, in the existing file. Never forked into a `-v2` or `-updated` copy — that's exactly the kind of confusion this whole setup is meant to prevent.
2. **Every new or edited file gets presented** in the same turn it changes. A file that's written but not shown to you doesn't count as done.
3. **Every source cited anywhere gets logged in `sources.md`** with a verification marker (🟢 verified / 🟡 named but unconfirmed / 🔴 needs a different access route), whether or not it ends up quoted in a specification document.
4. **Every new file's storage location gets stated explicitly when it's created** — Workspace (Project Knowledge) or local computer, per `00-local-storage-setup.md`. Not left implicit, not left for you to infer from the tier symbol alone.

## Maintenance mechanism — what updates when

| Trigger | Gets updated |
|---|---|
| Any new document created | `00-project-index.md` — new row in the file registry, with its dependencies (what it builds on, what it feeds into) and a context tier (📌 Project Knowledge or 💾 Offline); phase status in `00-project-phases.md` refreshed if it closes out a phase item |
| A significant decision made (method choice, scope call, metric definition, scope cut) | `00-decisions-log.md` — appended, never silently edited after the fact; superseded decisions are marked superseded, not deleted |
| A new external fact or paper enters the picture | `sources.md` |
| Something needs your action that I can't do myself | `00-action-items.md` — added with status **pending** |
| You complete a manual action | Tell me and I'll mark it **done** |

## What's automated vs. what needs you

**Automated — I handle this without asking:** creating, editing, and organizing files within this conversation; web research and verification; citation logging; document drafting; keeping the index/log/action-items files current.

**Not automated — I'll flag it, you act:** anything outside this conversation. Adding files to Project Knowledge, institutional library access (NFSU credentials), confirming a decision with your guide, anything requiring physical access or an account only you hold. When this comes up, it goes in `00-action-items.md` in a consistent format — you'll never have to hunt through chat history for a manual step I mentioned once and moved on from.

## Interaction model

I recommend the next concrete step and explain why, then execute it fully once you confirm — a short instruction like "continue" is enough; I won't do a task partially and pause mid-way unless I hit a genuine fork where either direction is reasonable and the choice is yours to make. If something I find changes a prior conclusion, I say so plainly rather than folding it in quietly.

## Rigor rules

Carried over from the working principle you set at the start of this project, made concrete:

- Confidence gets stated explicitly. "Verified," "likely," and "unconfirmed" are different claims and I'll say which one applies to what.
- A claim doesn't go into a specification document as settled until it's actually been checked — plausible isn't the same as confirmed.
- Anything that overturns or narrows a prior conclusion gets flagged as a change, with the old and new position both stated, not quietly merged into the existing text.
