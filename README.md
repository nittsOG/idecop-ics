# iDECOP-ICS — Phase C build

*intelligent Deception Planning and Placement Optimization for Industrial Control Systems.* Prototype name per D18 in `docs/00-decisions-log.md` — the thesis title itself is unchanged ("AI-Assisted Deception Placement Optimization for Industrial Control Systems").

Real, tested code — the database was initialized and queried, the API was started and hit with real requests, the frontend built successfully, and now the optimizer has actually been run against real data and produced real comparative results. Nothing below is illustrative or hypothetical.

## What's here

- `data/schema.sql`, `data/seed.sql` — transcribed from `02-data-model.md`, with a real fix fed back into that document: the original seed data never populated `edges`/`conduits`, leaving the graph with zero connectivity (found while building this).
- `data/demo_ai_suggestions.sql` — the three assets worked through by name in `02-ai-role.md` §10, for the review-screen demo.
- `src/api/main.py` — FastAPI backend for Screen 3 (plausibility review): `GET /assets`, `GET /candidates`, `POST /candidates/{asset_id}/confirm`.
- `src/frontend/` — the working React app for Screen 3.
- `src/graph_model/` — loads the real graph from SQLite, computes betweenness centrality (genuinely computed, not placeholder) and `Crit(v)` (uses placeholder SL/damage values — see the module's own docstring for why those specifically still need real elicitation, not computation).
- `src/optimizer/metrics.py` — `F(x)` and all five components, shared by every method so they're scored identically.
- `src/optimizer/baselines.py` — greedy, random (30 trials), and centrality, implementing `02-optimization-formulation.md` §2/4/5 exactly.
- `scripts/run_comparison.py` — runs all three against the real testbed graph and prints a comparison. This produced the results below.

## First real comparison — all four methods, read the caveats not just the numbers

Budget = 2, candidates = 5 (the confirmed subset of `L`), default weights (α=β=γ=δ=1, ε=0.1):

| Method | F(x) | Coverage | Early | CritProt |
|---|---|---|---|---|
| Greedy (proposed) | **0.450** | 0.67 | 0.00 | 0.18 |
| MILP (validation) | **0.450** | 0.67 | 0.00 | 0.18 |
| Centrality | 0.103 | 0.33 | 0.75 | 0.12 |
| Random (mean of 30) | -0.179 | — | — | — |

Greedy matched MILP's exact optimum on this instance (0.0% gap) — expected on a small testbed, not itself evidence the D1 approximation guarantee holds in general. This is a 5-candidate, 3-path smoke test with placeholder criticality inputs, not a thesis result. Three genuine findings worth knowing about, not just the headline numbers:

**MILP's first implementation was wrong, and building it is what proved that.** `02-optimization-formulation.md` §3 originally recommended an "unnormalized Early proxy" as the simpler linearization option. Building it and running it produced a placement that scored *worse* on the true F(x) than greedy — logically impossible for an exact validator. Root cause and fix are in that document's §3 now, corrected in place rather than hidden — D16 in the decisions log has the full story.

**Greedy correctly stopped at one decoy, not two.** Adding DMZ Jump Host as a second placement would improve coverage and early-detection, but its `detectability_risk` (0.7 — "most externally-scanned zone") costs more in the objective than it gains. D5's "weight operational risk heavily" decision, actually doing something.

**Resolved (D19):** Engineering WS-2 originally contributed nothing to any attack path — logged as D15. Fixed by rerouting P3 through it rather than leaving P3's second step disjunctive with HMI. Re-running confirmed the fix works as intended: WS-2 is no longer structurally excluded from ever being selected (it joins DMZ Jump Host and HMI for full coverage once coverage is weighted higher, α=3) — though under the *default* weights, greedy still picks DMZ Jump Host alone, since `Early(x)` is a mean over intercepted paths and both WS-2's and HMI's interceptions land at the latest possible stage, dragging that average down rather than helping it. A genuine, worth-keeping illustration of the coverage/early-detection tradeoff for the results chapter, not a bug.

## What's tested and confirmed working

- Database, API, and frontend — see the Phase C notes in `00-decisions-log.md` (D14).
- `graph_model`: real betweenness centrality computed from the actual 14-edge graph (verified DMZ Jump Host has the highest centrality — a genuine hub node, correctly identified); criticality scores written back to `assets`.
- `optimizer`: greedy's early-stopping behavior confirmed (doesn't spend the full budget when nothing improves); random's 30-trial mean and std computed; centrality's deterministic top-B selection confirmed against actual betweenness values.

## What isn't built yet

`/optimize`/`/runs`/`/explain` endpoints (the optimizer modules exist now, just not wired to the API yet), Screens 1 and 2, the AI explanation layer's Ollama integration, the Colab notebook, and the physical VMs.

## Running it

```bash
pip install fastapi "uvicorn[standard]" pydantic networkx ortools --break-system-packages
python3 -c "
import sqlite3
conn = sqlite3.connect('data/deception_placement.db')
for f in ['data/schema.sql','data/seed.sql','data/demo_ai_suggestions.sql']:
    conn.executescript(open(f).read())
conn.commit()
"
python3 scripts/run_comparison.py          # the three-method comparison above

python3 -m uvicorn src.api.main:app --reload   # backend, separately
cd src/frontend && npm install && npm run dev  # frontend, separately
```

`node_modules/`, `dist/`, and `*.db` aren't included — regenerate with the commands above.

