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

Budget = 2, five confirmed candidates, three attack paths, default weights (α=β=γ=δ=1, ε=0.1). Produced by `scripts/run_comparison.py`.

| Method | Placement | F(x) | Coverage | Early | CritProt | Risk | Cost |
|---|---|---|---|---|---|---|---|
| Greedy (proposed) | DMZ Jump Host | **0.4032** | 0.33 | 0.75 | 0.12 | 0.70 | 1 |
| MILP (validation) | DMZ Jump Host | **0.4032** | 0.33 | 0.75 | 0.12 | 0.70 | 1 |
| Centrality | DMZ Jump Host, Eng WS-2 | 0.1465 | 0.67 | 0.38 | 0.20 | 0.90 | 2 |
| Random (mean of 30) | — | −0.1358 | — | — | — | — | — |

Greedy matched the exact optimum (0.0% gap). Expected at this instance size, and not itself evidence that the D1 approximation guarantee holds in general. This is a five-candidate, three-path instance with placeholder criticality inputs — a working comparison, not a thesis result.

### Known open issue, stated here rather than buried

`Risk(x)` is implemented as an unnormalised sum of per-decoy detectability, while `docs/formal-problem-definition.md` §5 defines it as a probability. `CritProt(x)` is normalised against the criticality of every asset in the graph, capping it at roughly 0.30 even at full coverage. Both terms are therefore on different scales from `Coverage` and `Early`, which distorts what equal weights mean. This is the same failure class as D16 and must be resolved before the evaluation campaign. It is why greedy currently wins on the objective while covering *fewer* paths than the centrality baseline.

---

## Three findings that only appeared when the specification was built

**The MILP's first implementation was wrong, and building it proved that.** `docs/02-optimization-formulation.md` §3 originally recommended an unnormalised early-detection proxy as the simpler linearisation. Running it produced a placement scoring *worse* on the true F(x) than greedy — impossible for an exact validator. The unnormalised proxy rewards covering more paths over covering them earlier. Corrected in place, with the failed option kept in the text. Full account in D16.

**Greedy correctly stops before spending its budget.** A second placement at DMZ Jump Host would improve coverage, but its detectability risk costs more in the objective than it gains. D5's decision to weight operational risk heavily, visibly doing something.

**`Early(x)` is a mean, and that has consequences.** Engineering WS-2 originally contributed to no attack path (D15), fixed by rerouting P3 through it (D19). After the fix, greedy still selects DMZ Jump Host alone under default weights — both WS-2 and HMI intercept at the latest possible stage, so adding either drags the mean down. Raise the coverage weight to α=3 and all three are selected for full coverage. An interpretable illustration of the coverage/earliness tradeoff, not a bug.

---

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
python3 -m uvicorn src.api.main:app --reload    # backend
cd src/frontend && npm install && npm run dev   # frontend
```

`node_modules/`, `dist/` and `*.db` are not tracked — regenerate with the commands above.

---

## Where to start reading

New to the project: `docs/02-system-flow.md` for how it fits together, then `docs/formal-problem-definition.md` for the mathematics. `docs/00-glossary.md` defines every term. `docs/00-decisions-log.md` explains why each choice was made, including the ones that turned out wrong.
