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

**One rule worth stating plainly:** `/api` is the only module with write access to the database. `graph_model` and `optimizer` are libraries the API calls, not services with their own persistence logic — this keeps every write auditable at one layer instead of scattered across modules, and it's the same principle already enforced structurally for the AI components in `02-ai-role.md` (neither `ai_explain` nor the Colab notebook can write to a table that matters without going through a confirmed, API-mediated step).

## 2. API contract

Extends the sketch in `02-data-model.md` to the full set actually needed once all three screens (§3) are accounted for:

| Method & path | Reads | Writes | Used by |
|---|---|---|---|
| `GET /graph` | `assets`, `edges` | — | Screen 1, 2 |
| `GET /candidates` | `candidate_locations` (both real and `ai_suggested_*` columns) | — | Screen 3 |
| `POST /candidates/{asset_id}/confirm` | — | `criterion_*`, `passes_plausibility`, `is_candidate`, `human_confirmed`, `confirmed_at` | Screen 3 |
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

Building order given weekend hours: Screen 3 first, since nothing else works without confirmed candidates in `L`; Screen 1 second, since it's both the most valuable demo asset and the one most already speced; Screen 2 last, since it's the simplest to build (charts over already-stored data, no live interaction) but only becomes meaningful once Phase D's sensitivity sweep is actually generating multiple runs to compare.

## 4. Bridging the Colab notebook back into the live system

The plausibility-scoring notebook (`02-ai-role.md` §7–10) never touches this codebase directly — it's a disconnected script producing a CSV: `asset_id, ai_suggested_decoy_exists, ai_suggested_attacker_reach, ai_suggested_useful_signal, ai_suggested_reliable_indicator, ai_reasoning`. `scripts/import_plausibility_scores.py` reads that CSV and writes it into the matching columns on `candidate_locations` — nothing more. It doesn't touch `criterion_*` or `human_confirmed`; those only get set by an actual human going through Screen 3. The import script's only job is getting the AI's suggestion from a spreadsheet into a database row where the review screen can find it.

This is a one-time step per testbed configuration, run manually (`python scripts/import_plausibility_scores.py candidates.csv`) — not scheduled, not triggered by the API, not something the live system ever calls on its own.

## 5. Running it

For your own reference when Phase C starts, not a deployment guide:

```
ollama pull phi4-mini                    # once
ollama serve                             # background, for /runs/{id}/explain

python scripts/import_plausibility_scores.py candidates.csv   # after the Colab notebook runs, once

uvicorn src.api.main:app --reload        # the backend
npm run dev  --prefix src/frontend       # the UI, separately
```

Four things running, three of them only during active development or a demo (Ollama, the API, the frontend dev server) and one that runs once and is done (the import script). The Colab notebook isn't in this list at all — it runs in a browser tab, independent of everything here.

## What This Enables Next

Phase B is complete. Every box in the testbed architecture's system diagram now has a spec concrete enough to build against directly — the exit criteria `00-project-phases.md` set for this phase. Phase C starts with Screen 3 and the testbed VMs, per §3's build order and the phase document's own suggested sequencing.
