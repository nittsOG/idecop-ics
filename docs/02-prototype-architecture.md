# Prototype Architecture — Module Breakdown, API Contract, Screens

The last Phase B document. Pulls `02-data-model.md`, `02-optimization-formulation.md`, and `02-ai-role.md` together into something buildable — every module, every endpoint, every screen, and how the disconnected Colab piece rejoins the live system.

## 1. Module breakdown

```
/src
  /graph_model      NetworkX construction from SQLite; writes G, L, P back to SQLite
  /optimizer        greedy.py, milp.py (OR-Tools CP-SAT), random_baseline.py, centrality.py
  /ai_explain        Ollama client (Phi-4-mini), prompt templates, called only from /runs/{id}/explain
  /api               FastAPI app — the only thing that calls into the four modules above
  /frontend          React + Cytoscape.js, the three screens in §3
/scripts
  import_plausibility_scores.py   one-time import of the Colab notebook's CSV output
/notebooks
  plausibility_scoring.ipynb      Part B of 02-ai-role.md — lives outside /src entirely, never imported by it
```

**One rule worth stating plainly:** `/api` is the only module with write access to the database. *(D26: this holds for the running system. Four offline setup steps also write: the notebook import, `scripts/review_io.py restore`, the legacy SQL for historical reproduction, and `graph_model`'s `write_computed_scores` when run as a script. See D13's note.)* `graph_model` and `optimizer` are libraries the API calls, not services with their own persistence logic — this keeps every write auditable at one layer instead of scattered across modules, and it's the same principle already enforced structurally for the AI components in `02-ai-role.md` (neither `ai_explain` nor the Colab notebook can write to a table that matters without going through a confirmed, API-mediated step).

## 2. API contract

Extends the sketch in `02-data-model.md` to the full set actually needed once all three screens (§3) are accounted for:

| Method & path | Reads | Writes | Used by |
|---|---|---|---|
| `GET /graph` | `assets`, `edges` | — | Screen 1, 2 |
| `GET /candidates` | `candidate_locations` (both real and `ai_suggested_*` columns) | — | Screen 3 |
| `POST /candidates/{asset_id}/confirm` | — | `criterion_*`, `human_reason`, `passes_plausibility`, `is_candidate`, `human_confirmed`, `confirmed_at`; on a blind card's first confirmation, the write-once `blind_*` columns (D26) | Screen 3 |
| `GET /attack-paths` | `attack_paths`, `attack_path_steps` | — | Screen 1 |
| `PUT /assets/{id}/damage-score` | — | `assets.damage_fraction` | Screen 3 (setup) |
| `POST /optimize` | `assets`, `candidate_locations` (confirmed only), `attack_paths` | `placement_runs`, `placements`, `run_metrics` | Screen 1 |
| `GET /runs` | `placement_runs`, `run_metrics` | — | Screen 2 |
| `GET /runs/{id}` | `placement_runs`, `placements`, `run_metrics` | — | Screen 1 |
| `GET /runs/compare?budget={b}` | `run_metrics`, filtered by budget | — | Screen 2 |
| `POST /runs/{id}/explain` | `run_metrics` (this run + same-budget Random/Centrality runs) | `explanations` | Screen 1 |

`POST /optimize` never returns a placement directly in its response body beyond the `run_id` — the frontend always fetches the actual result via `GET /runs/{id}` afterward. Small deliberate choice: it means every placement the UI ever displays came from a row that's already durably stored, not from an in-flight response that could get lost on a page refresh mid-run.

## 3. Three screens, not one

The interface walkthrough earlier flagged this and left it open. Resolving it here: this is genuinely three distinct screens, because they serve three different moments in the workflow, not three views of the same data.

**Screen 1 — Single-run dashboard.** The one already mocked up: network graph with the chosen placement highlighted, metric cards, the AI explanation panel. Method tabs at top trigger `POST /optimize`, then `GET /runs/{id}`. This is the demo screen — what you'd show your guide running live.

**Screen 2 — Sensitivity-sweep comparison.** Doesn't exist as a mockup yet, and it's a genuinely different shape: not a graph, a chart — objective value and each metric plotted across the weight combinations from `formal-problem-definition.md` §5's sensitivity sweep, reading from `GET /runs/compare`. This is the evaluation screen — what actually produces the figures for your Results chapter. No graph rendering needed here at all; it's tables and line charts.

**Screen 3 — Plausibility review.** The one mocked up in the AI-role discussion: list of candidate assets, AI-suggested scores as badges, confirm or edit, calling `POST /candidates/{asset_id}/confirm`. This is a setup screen, used once per testbed configuration, not part of the demo flow.

*Rebuilt by D26:*
- the three blind cards come first, with the AI's answer hidden until each is confirmed;
- each card lists the asset's attack-path steps;
- answers use four levels, in order, and the first No ends the card;
- a reason box is required on blind cards, on cards with no AI suggestion, on changed answers, on Mostly No / No, and on an asset that lies on several paths;
- a blank is never filled with the AI's answer.

A network view of the same review, with cards in a side panel, is an open design idea (A34).

Building order given weekend hours: Screen 3 first, since nothing else works without confirmed candidates in `L`; Screen 1 second, since it's both the most valuable demo asset and the one most already speced; Screen 2 last, since it's the simplest to build (charts over already-stored data, no live interaction) but only becomes meaningful once Phase D's sensitivity sweep is actually generating multiple runs to compare.

## 4. Bridging the Colab notebook back into the live system

The plausibility-scoring notebook (`02-ai-role.md` §7–10; `notebooks/plausibility_scoring.ipynb`, written in D26) never touches the live system directly. It clones the repository, builds the prompt from `src/plausibility/prompt.py`, and produces a CSV: `asset_id, asset_name, ai_suggested_decoy_exists, ai_suggested_attacker_reach, ai_suggested_useful_signal, ai_suggested_reliable_indicator, ai_reasoning, ai_model, generated_at, repo_commit, parse_status, notes`. It also writes a JSONL file of the raw outputs, for audit. *(D26 added `asset_name`, which the import checks against the database, together with the model and commit identity and the parse status. Levels use the four-point scale.)* `scripts/import_plausibility_scores.py` reads that CSV and writes it into the matching columns on `candidate_locations` — nothing more. It doesn't touch `criterion_*` or `human_confirmed`; those only get set by an actual human going through Screen 3. The import script's only job is getting the AI's suggestion from a spreadsheet into a database row where the review screen can find it.

This is a one-time step per testbed configuration, run manually (`python scripts/import_plausibility_scores.py ai_suggestions.csv`) — not scheduled, not triggered by the API, not something the live system ever calls on its own. *Built in D26.* It refuses three things:
- a row whose asset id and name do not match the database;
- a suggestion that breaks the sequential rule;
- changing or clearing an AI suggestion already stored on a confirmed card. On a normal card the confirmation was made against it; on a blind card it is half of the agreement measure.

An empty suggestion on a confirmed card is filled. That is the expected order for a blind card. A row the notebook could not score clears any older suggestion on an unconfirmed card. The import prints counts and asset names only, and on a blind card it withholds even a rubric error's detail, so it cannot spoil an open blind card.

**The review's committed record (D26).** The database is not tracked, so `scripts/review_io.py export` writes the completed review to `data/review/plausibility_review.csv` for committing. `restore` rebuilds it on a fresh database, re-checking every rule. That CSV, not the database file, is the frozen Filter 1 input.

## 5. Running it

For your own reference when Phase C starts, not a deployment guide:

```
ollama pull phi4-mini                    # once
ollama serve                             # background, for /runs/{id}/explain

uvicorn src.api.main:app --reload        # the backend
npm run dev  --prefix src/frontend       # the UI, separately; score the three blind cards first

python scripts/import_plausibility_scores.py ai_suggestions.csv   # after the Colab notebook runs, once (D26 order)
```

Four things running, three of them only during active development or a demo (Ollama, the API, the frontend dev server) and one that runs once and is done (the import script). The Colab notebook isn't in this list at all — it runs in a browser tab, independent of everything here.

## What This Enables Next

Phase B is complete. Every box in the testbed architecture's system diagram now has a spec concrete enough to build against directly — the exit criteria `00-project-phases.md` set for this phase. Phase C starts with Screen 3 and the testbed VMs, per §3's build order and the phase document's own suggested sequencing.
