# System Flow and Structure

How iDECOP-ICS fits together: components, data flow, and the runtime sequence of an optimization run.

**Basis for this document.** Written against the actual repository at `github.com/nittsOG/idecop-ics`, cloned and executed — not against the specification documents alone. Every module name, endpoint, table and function named below was read in the source. The results in §6 were produced by running `scripts/run_comparison.py` against a freshly built database, not copied from the README. Where the code and the specification disagree, that is stated rather than smoothed over (§7).

---

## 1. The pipeline in one picture

The original brief's §5 concept, unchanged:

```
OT/ICS architecture + asset criticality + communication
relationships + attack scenarios
        │
        ▼  OT network model
        ▼  attack-path analysis
        ▼  candidate deception locations
        ▼  deception placement optimization
        ▼  recommended placement
        ▼  AI-assisted explanation  →  security analyst
```

In one sentence: *describe the network, work out how an attacker moves through it, work out where a decoy could believably sit, pick the best subset of those places, then explain the choice.*

---

## 2. Components as actually built

```
src/frontend/          React + Vite
  App.jsx              routing between screens
  PlausibilityReview.jsx   Screen 3 — candidate confirmation
  Dashboard.jsx            Screen 1 — single-run view
        │  HTTP/JSON, CORS-restricted to localhost:5173
        ▼
src/api/main.py        FastAPI — 9 endpoints, 240 lines
        │
        ├──▶ src/graph_model/__init__.py   130 lines
        │      load_graph()              builds nx.DiGraph from SQLite
        │      compute_centrality()      betweenness, weighted
        │      compute_criticality()     Crit(v) = w₁·SL + w₂·Central·Damage
        │      write_computed_scores()   persists back to assets
        │      load_candidate_locations()  → L
        │      load_attack_paths()         → P
        │
        ├──▶ src/optimizer/metrics.py     66 lines
        │      score()   F(x) and all five components
        │                shared by all four methods
        │
        ├──▶ src/optimizer/baselines.py   55 lines
        │      greedy()  random_baseline()  centrality_baseline()
        │
        └──▶ src/optimizer/milp.py       111 lines
               solve_milp()   OR-Tools CP-SAT, exact validator
        │
        ▼
data/deception_placement.db     SQLite, 10 tables
```

**Not yet built:** the explanation layer (`/runs/{id}/explain` — needs the Ollama integration), Screen 2 (sensitivity-sweep comparison), the Colab plausibility notebook, and the physical VMs.

**Design property worth noting:** every method calls the same `score()` function. That is what makes a greedy result and a MILP result comparable at all — if each method computed its own objective, the comparison would be meaningless.

---

## 3. Database schema — 10 tables

| Table | Holds | Maps to |
|---|---|---|
| `zones` | IEC 62443 zones | `zone(v)` |
| `conduits` | Permitted zone-to-zone channels | `c(z_i, z_j)` |
| `assets` | Nodes, plus computed `central_score`, `sl_aggregate`, `damage_score`, `criticality` | `V`, `Crit(v)` |
| `edges` | Communication relationships with protocol and weight | `E` |
| `candidate_locations` | Plausibility scores, AI suggestions, `is_candidate` flag | `L` |
| `attack_paths` | Path headers | `P` |
| `attack_path_steps` | Ordered steps per path | Path sequences |
| `placement_runs` | One row per optimization run: method, weights, budget, metrics, runtime | Run records |
| `placements` | Which locations were selected in a given run | `x*` |
| `explanations` | Generated explanation text per run | AI output (table exists, not yet populated) |

Computed scores are stored rather than only derived, so a stored run remains interpretable later without re-running the pipeline.

---

## 4. API surface — 9 endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Liveness check |
| `GET /graph` | Nodes *and* edges — what Screen 1's visualization needs |
| `GET /assets` | Flat asset list with computed scores |
| `GET /candidates` | Candidate locations with AI suggestions and confirmation state |
| `POST /candidates/{asset_id}/confirm` | Human confirms or overrides the four rubric scores |
| `GET /attack-paths` | P, with step sequences |
| `POST /optimize` | Runs a method, stores the result |
| `GET /runs` | Run history |
| `GET /runs/{run_id}` | One stored run with its placements |

`POST /optimize` validates `method` against `{random, centrality, proposed_greedy, proposed_milp}` and requires `budget > 0`. Weights α through ε are request parameters with defaults, which is what makes the sensitivity sweep runnable over HTTP rather than only from a script.

---

## 5. Data flow

### Flow A — Setup, one time

```
testbed-architecture.md  +  threat-attack-model.md
        ▼
data/schema.sql  +  data/seed.sql
        ▼
zones · assets · edges · conduits · attack_paths · attack_path_steps
```

This is where D14's bug lived: assets were seeded, edges and conduits were not, so the graph had zero connectivity.

### Flow B — Candidate selection, human-in-the-loop

```
Colab notebook (Qwen3 14B)  [not yet built]
   scores 4 rubric criteria per asset
        ▼
candidate_locations.ai_suggested_*     (suggestions only)
        ▼
Screen 3 ← GET /candidates
   human reads AI reasoning, confirms or overrides
        ▼
POST /candidates/{asset_id}/confirm
        ▼
candidate_locations.is_candidate = 1   ──►  this is L
```

The optimizer reads only `is_candidate=1`. An unconfirmed AI suggestion has no path into the search space.

### Flow C — A single optimization run

```
POST /optimize { method, budget, alpha…epsilon }
        ▼
load_graph()              → nx.DiGraph from assets + edges
compute_criticality()     → Crit(v) per asset
load_candidate_locations()→ L
load_attack_paths()       → P with asset_sequence and length
        ▼
method dispatch:
  proposed_greedy → greedy()              marginal gain, early stop
  proposed_milp   → solve_milp()          CP-SAT, exact
  random          → random_baseline()     30 trials, seed 42
  centrality      → centrality_baseline() top-B by betweenness
        ▼
score() computes Coverage · Early · CritProt · Risk · Cost · F(x)
        ▼
INSERT placement_runs  +  INSERT placements
        ▼
GET /runs/{id} → Dashboard renders it
        ▼
POST /runs/{id}/explain  [not built]
```

Per D17: `method=random` runs all 30 trials internally but stores only one placement, since a stored run needs one concrete answer. **Phase D's statistical comparison must call `random_baseline()` directly** to get the mean and standard deviation — a single stored random run is illustrative only.

### Flow D — Evaluation, Phase D

```
for each weight configuration in the sweep grid:
  for each method:
    POST /optimize → one placement_runs row
        ▼
Screen 2 reads accumulated runs → comparison tables and charts
```

---

## 6. Current verified output

Produced by running `scripts/run_comparison.py` against a freshly built database. Budget 2, five candidates, three paths, default weights (α=β=γ=δ=1, ε=0.1).

```
Candidates (L): DMZ Jump Host, Historian, Engineering WS-2, HMI, PLC-02
```

| Method | Placement | F(x) | Coverage | Early | CritProt | Risk | Cost |
|---|---|---|---|---|---|---|---|
| Greedy | DMZ Jump Host | **0.4032** | 0.33 | 0.75 | 0.12 | 0.70 | 1 |
| MILP | DMZ Jump Host | **0.4032** | 0.33 | 0.75 | 0.12 | 0.70 | 1 |
| Centrality | DMZ Jump Host, Engineering WS-2 | 0.1465 | 0.67 | 0.38 | 0.20 | 0.90 | 2 |
| Random (mean of 30) | — | −0.1358 | — | — | — | — | — |

Optimality gap: 0.0000. Greedy matched the exact optimum on this instance — expected at this size, and not by itself evidence that the D1 approximation guarantee holds in general.

**Read the Coverage column, not only F(x).** Greedy wins decisively on the objective while selecting *fewer* paths covered than the centrality baseline. See §7.

---

## 7. Discrepancies found while verifying

Recorded because they are real and actionable, not to pad the document.

### 7.1 The README's results table is stale

It reports greedy at Coverage 0.67 / Early 0.00. The current code produces Coverage 0.33 / Early 0.75 — a pre-D19 run, from before P3 was rerouted through Engineering WS-2. The README also lists `/optimize`, `/runs` and `/runs/{id}` as unbuilt; all three exist in `src/api/main.py`. **Status: needs updating.**

### 7.2 Risk(x) is an unnormalized sum — same failure class as D16

`metrics.py` computes:

```python
risk = sum(detectability_risk.get(l, 0.0) for l in x)
```

`formal-problem-definition.md` §5 defines Risk(x) as *"estimated probability of legitimate OT traffic interacting with placed decoys."* A probability is bounded in [0,1]; a sum of per-decoy risks is not, and grows without limit as decoys are added. The module's own docstring asserts that *"coverage, early, crit_prot, and risk are all 0-1 normalized"* — which is true of the first three and false of the fourth.

Consequence, visible in §6: with δ=1, each added decoy costs its full risk value while coverage gains at most 1/|P|. DMZ Jump Host alone carries risk 0.70. Adding Engineering WS-2 brings the total to 0.90 for a coverage gain of 0.33. The optimizer therefore places as few decoys as possible, correctly, against a term that is scaled differently from everything it is being traded against.

This is structurally identical to D16: a term that is not equivalent to its specified definition, so the solver optimizes something adjacent to the intended objective. It was caught the same way — by running the thing.

Candidate fixes, none yet chosen: treat risk as a mean over placed decoys; or as a union probability, 1 − ∏(1 − r_l); or keep the sum and set δ from the sensitivity sweep with the scale mismatch documented. The third is defensible but should be a stated decision, not an accident.

### 7.3 This currently contradicts the primary research question

`formal-problem-definition.md` §8 asks whether Method 3 achieves *higher* Coverage(x) and CritProt(x) than Methods 1 and 2. At default weights it does not: greedy reaches Coverage 0.33 and CritProt 0.12 against centrality's 0.67 and 0.20. It wins on F(x) because F(x) penalizes risk and cost, which the baselines ignore.

This is not necessarily a failure. It may mean the research question is phrased too narrowly — the honest claim is that the proposed method achieves a better *objective-defined tradeoff*, not uniformly higher coverage. But it needs resolving before Phase D, because running the full sweep against a question the results structurally cannot answer wastes the evaluation. §7.2 may or may not change this; the weight scaling is likely implicated.

### 7.4 `graph_model` writes to the database, contradicting D13

D13 states that only `/api` has write access, with `graph_model` and `optimizer` as libraries it calls. But `write_computed_scores()` opens its own connection and issues `UPDATE assets`. Its own module docstring says *"Read-only against the database; nothing here writes."*

Low practical risk — it writes computed scores only. But D13's rationale was keeping every write auditable at one layer, and this is a quiet exception to it. Either move the write into the API layer, or amend D13 to permit it explicitly.

### 7.5 `references/` contains a publisher PDF on a public repository

`references/312-jay-2023-deception-substations.pdf` is redistributed publicly. Regardless of the paper's access status, republishing a publisher's PDF is a copyright question. Safest fix: remove it from the repository and keep it locally, citing by DOI instead.

---

## 8. Build order, and what remains

Each step unblocks the next.

1. ~~Database and seed data~~ — done, D14
2. ~~`graph_model`~~ — done, real betweenness computed
3. ~~Optimizer, four methods~~ — done, D15/D16
4. ~~Screen 3, plausibility review~~ — done
5. ~~`/optimize`, `/runs`, `/runs/{id}`~~ — done, D17
6. ~~Screen 1, dashboard~~ — built, present in `src/frontend/src/Dashboard.jsx`
7. **Explanation layer** — needs Ollama running; not testable in a sandbox
8. **Colab notebook** — independent; needs GPU-backed inference
9. **Screen 2** — only meaningful once Phase D generates multiple runs
10. **Physical VMs** — needed for demonstration, not for the algorithm

Before Phase D starts, §7.2 and §7.3 need decisions. Both are cheap to resolve now and expensive to discover halfway through an evaluation sweep.

---

## 9. The one-paragraph version

An OT network is described as a directed graph whose nodes carry an IEC 62443 zone, a Purdue level and an asset type, and whose edges carry protocols and weights. Three attack paths are traced across it using verified MITRE ATT&CK for ICS techniques. Every asset is scored for criticality, then filtered by a four-criterion plausibility rubric and a detectability check to produce the candidate set. An optimizer selects the subset of candidates maximizing a five-term objective — attack-path coverage, earliness of interception, criticality-weighted protection, minus operational risk and deployment cost — within a budget. A local language model explains the result to an analyst without altering it. Three baseline strategies run against identical attack paths so the result can be compared rather than asserted.
