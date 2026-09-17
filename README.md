# iDECOP-ICS

*intelligent Deception Planning and Placement Optimization for Industrial Control Systems.*

Prototype for an M.Tech Cyber Security major project at the National Forensic Sciences University. Prototype name per D18 in `docs/00-decisions-log.md`; the thesis title itself is unchanged — "AI-Assisted Deception Placement Optimization for Industrial Control Systems".

**The problem.** Industrial networks can be defended with decoys — fake PLCs, honey credentials, decoy services — so that any interaction with them is high-confidence evidence of intrusion. Building convincing decoys is a solved, crowded field. Deciding *where* to put them is still done manually, by template, or by architectural convention. This project makes that decision a formal optimisation problem over IEC 62443 zone structure, asset criticality, and MITRE ATT&CK for ICS attack paths.

**What this is not:** another honeypot, a honeytoken platform, an AI chatbot, a generic attack graph, a vulnerability scanner, an asset inventory, a GRC dashboard, or a network visualiser. That boundary governs every design decision in `docs/00-decisions-log.md`.

Everything below is real, executed code. The database is initialised and queried, the API is started and hit with real requests, the frontend builds, and the optimiser runs against the real graph. Nothing here is illustrative.

---

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | Specification, research, decisions log, project tracking. Naming convention in `docs/00-workflow-and-rules.md` |
| `src/graph_model/` | Builds `G = (V,E)` from SQLite; weighted betweenness centrality; `Crit(v)` |
| `src/optimizer/` | `metrics.py` (F(x) and its five components), `baselines.py` (greedy, random, centrality), `milp.py` (exact validator) |
| `src/api/` | FastAPI backend — nine endpoints |
| `src/frontend/` | React + Vite interface |
| `data/` | Schema, seed data, demo AI suggestions |
| `scripts/` | `run_comparison.py` — runs all four methods and prints a comparison |
| `references/` | Papers cited in `docs/sources.md`, by source number |

---

## Current state

**Built and working**

- `data/schema.sql`, `data/seed.sql` — ten tables, transcribed from `docs/02-data-model.md`. A real fix was fed back into that document while building: the original seed never populated `edges`/`conduits`, leaving the graph with zero connectivity.
- `src/graph_model/` — loads the real graph, computes betweenness centrality (genuinely computed, not placeholder) and `Crit(v)`. SL and damage values are still placeholders pending real elicitation; the module docstring explains why.
- `src/optimizer/` — all four methods, scored by a single shared `score()` so results stay comparable.
- `src/api/main.py` — `GET /health`, `/graph`, `/assets`, `/candidates`, `/attack-paths`, `/runs`, `/runs/{id}`; `POST /optimize`, `/candidates/{asset_id}/confirm`.
- `src/frontend/` — Screen 3 (plausibility review) and Screen 1 (single-run dashboard).

**Not built yet**

Explanation layer (`/runs/{id}/explain` — needs a live Ollama instance), Screen 2 (sensitivity-sweep comparison), the Colab plausibility-scoring notebook, and the physical VM testbed.

---

## Current comparison — read the caveats, not just the numbers

Budget = 3, five confirmed candidates, three attack paths, default weights (α=β=γ=δ=1, ε=0.1). Produced by `scripts/run_comparison.py`.

| Method | Placement | F(x) | Coverage | Early | CritProt | Risk | Cost |
|---|---|---|---|---|---|---|---|
| Greedy (proposed) | DMZ Jump Host, Eng WS-2, HMI | **1.750** | **1.00** | 0.25 | 1.00 | 0.40 | 3 |
| MILP (validation) | DMZ Jump Host, Eng WS-2, HMI | **1.750** | **1.00** | 0.25 | 1.00 | 0.40 | 3 |
| Centrality | DMZ Jump Host, Eng WS-2, Historian | 1.098 | 0.67 | 0.25 | 0.68 | 0.40 | 3 |
| Random (mean of 30) | — | 1.024 | — | — | — | — | — |

Greedy matched the exact optimum — a 0.0% optimality gap. Expected at this instance size and **not** evidence that an approximation guarantee holds in general; see the note on that below.

### Across budgets and weightings

A single budget is a single data point. Sweeping B = 1..4 across five weightings (default, α=3, β=3, γ=3, δ=3) gives 20 configurations:

**Greedy beats the centrality baseline in 17, ties in 3, and never loses.**

Three results worth reading the code for:

- **Full coverage at lower cost.** At B=3 greedy reaches Coverage 1.00; centrality needs B=4 for the same. That is the "equal coverage at lower deployment cost" clause of the primary research question, answered.
- **It knows when not to act.** At δ=3, B=1 greedy places *nothing* (F = 0.000) while centrality places a decoy and scores **−1.239**. A top-B ranking has no mechanism for declining to spend its budget.
- **Topology-only ranking misfires.** Centrality spends spare budget on the Historian — an asset that appears on no attack path in **P**. Pure cost and detectability risk for zero coverage gain.

### Reported honestly: where the methods coincide

At **B=2 under default weights, greedy, MILP and centrality all select the same pair and score identically** (1.048). On a five-candidate instance a topology heuristic can land on the optimum by coincidence. This is in the results because selecting a more flattering budget and omitting this one would make the other 17 configurations less credible, not more.

### On the greedy approximation guarantee — read before citing

The objective was corrected in D20 after exhaustive structural testing (`scripts/structure_check.py` enumerates all 32 subsets of **L**; no sampling).

- **Before D20:** `Early(x)` was a mean over *intercepted* paths, making it non-monotone — 16 monotonicity and 18 submodularity violations. F(x) was **not submodular at all**, so no greedy guarantee of any kind was available, contradicting what the specification claimed.
- **After D20:** F(x) is **submodular but not monotone**, and necessarily so, because Risk and Cost are subtracted. The classical (1−1/e) bound requires *monotone* submodular maximisation under a cardinality constraint, so **it still does not apply directly to F(x)**.

No approximation guarantee is claimed here. `formal-problem-definition.md` §7 records the two honest routes — cite the regularised result for a monotone-submodular-minus-modular objective, or move risk from a penalty to a constraint — and A27 blocks any claim until a primary source is verified. What carries the practical argument meanwhile is the exact validator's 0.0% gap: at testbed scale the optimum is computable, so the guarantee matters for the scalability argument rather than for these results.

## Three findings that only appeared when the specification was built

**The MILP's first implementation was wrong, and building it proved that.** `docs/02-optimization-formulation.md` §3 originally recommended an unnormalised early-detection proxy as the simpler linearisation. Running it produced a placement scoring *worse* on the true F(x) than greedy — impossible for an exact validator. The unnormalised proxy rewards covering more paths over covering them earlier. Corrected in place, with the failed option kept in the text. Full account in D16.

**Greedy correctly stops before spending its budget.** A second placement at DMZ Jump Host would improve coverage, but its detectability risk costs more in the objective than it gains. D5's decision to weight operational risk heavily, visibly doing something.

**`Early(x)` was structurally broken, and only exhaustive testing showed it.** Engineering WS-2 originally contributed to no attack path (D15), fixed by rerouting P3 through it (D19). After that fix greedy *still* selected DMZ Jump Host alone under default weights, and the reason turned out to be structural rather than incidental: a mean over intercepted paths is non-monotone, so adding a late-intercepting decoy lowers the score. D19 observed the symptom; D20 identified the cause by enumerating every subset and verifying the violation count. Changing the denominator to a fixed |P| makes the term monotone and submodular, and — not coincidentally — removes the need for D16's k-enumeration workaround entirely, since the early coefficient stops depending on a quantity the solver is choosing.

**Conduits were named in the novelty claim and computed nowhere.** The claim states that IEC 62443 zone *and conduit* structure are first-class inputs. Zones genuinely were: `SL(zone(v))` enters `Crit(v)`. Conduits were stored, diagrammed, and inert — the clause was false as built. D20 adds `ConduitSL(v)`: a conduit takes the higher SL of the two zones it joins, and an asset inherits the highest SL among conduits incident to its zone. Modular in **x**, so submodularity survives; re-verified after the change.

## Running it

```bash
pip install -r requirements.txt

python3 -c "
import sqlite3
conn = sqlite3.connect('data/deception_placement.db')
for f in ['data/schema.sql','data/seed.sql','data/demo_ai_suggestions.sql']:
    conn.executescript(open(f).read())
conn.commit()
"

python3 scripts/run_comparison.py               # the comparison above
python3 scripts/structure_check.py              # monotonicity + submodularity, exhaustive
python3 -m uvicorn src.api.main:app --reload    # backend
cd src/frontend && npm install && npm run dev   # frontend
```

`node_modules/`, `dist/` and `*.db` are not tracked — regenerate with the commands above.

---

## Where to start reading

New to the project: `docs/02-system-flow.md` for how it fits together, then `docs/formal-problem-definition.md` for the mathematics. `docs/00-glossary.md` defines every term. `docs/00-decisions-log.md` explains why each choice was made, including the ones that turned out wrong.
