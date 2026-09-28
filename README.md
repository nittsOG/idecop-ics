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
| `src/optimizer/` | `metrics.py` (F(x) and its five components), `baselines.py` (greedy, distorted greedy, random, centrality), `milp.py` (exact validator) |
| `src/api/` | FastAPI backend — nine endpoints |
| `src/frontend/` | React + Vite interface |
| `data/` | Schema, seed data, demo AI suggestions |
| `scripts/` | `run_comparison.py` — runs all five methods at one budget; `sweep.py` — the declared 20-cell grid behind every comparative number (D24); `structure_check.py` — exhaustive monotonicity/submodularity/modularity tests |

---

## Current state

**Built and working**

- `data/schema.sql`, `data/seed.sql` — ten tables, transcribed from `docs/02-data-model.md`. A real fix was fed back into that document while building: the original seed never populated `edges`/`conduits`, leaving the graph with zero connectivity.
- `src/graph_model/` — loads the real graph, computes betweenness centrality (genuinely computed, not placeholder) and `Crit(v)`. SL and damage values are still placeholders pending real elicitation; the module docstring explains why.
- `src/optimizer/` — all five methods, scored by a single shared `score()` so results stay comparable.
- `src/api/main.py` — `GET /health`, `/graph`, `/assets`, `/candidates`, `/attack-paths`, `/runs`, `/runs/{id}`; `POST /optimize`, `/candidates/{asset_id}/confirm`.
- `src/frontend/` — Screen 3 (plausibility review) and Screen 1 (single-run dashboard).

**Not built yet**

Explanation layer (`/runs/{id}/explain` — needs a live Ollama instance), Screen 2 (sensitivity-sweep comparison), the Colab plausibility-scoring notebook, and the physical VM testbed.

---

## Current comparison — read the caveats, not just the numbers

Budget = 3, five confirmed candidates, **four** attack paths (P4 added in D21), default weights (α=β=γ=δ=1, ε=0.1). Produced by `scripts/run_comparison.py`.

| Method | Placement | F(x) | Coverage | Early | CritProt | Risk | Cost |
|---|---|---|---|---|---|---|---|
| Greedy (proposed, primary) | DMZ Jump Host, Eng WS-2, Historian | **1.0303** | 0.75 | 0.27 | 0.76 | 0.65 | 1.00 |
| Distorted greedy (guaranteed) | DMZ Jump Host, Eng WS-2, Historian | **1.0303** | 0.75 | 0.27 | 0.76 | 0.65 | 1.00 |
| MILP (exact validation) | DMZ Jump Host, Eng WS-2, Historian | **1.0303** | 0.75 | 0.27 | 0.76 | 0.65 | 1.00 |
| Centrality | DMZ Jump Host, Eng WS-2, Historian | 1.0303 | 0.75 | 0.27 | 0.76 | 0.65 | 1.00 |
| Random (mean of 30) | — | 0.7097 | — | — | — | — | — |

Greedy matched the exact optimum — a **0.00% optimality gap**, now verified against both the corrected MILP and independent exhaustive enumeration. Expected at this instance size and **not** evidence that an approximation guarantee holds for plain greedy in general; see below.

**All four methods coincide at this budget**, which is reported first rather than buried. On a five-candidate instance with four paths, B=3 saturates the useful search space and a topology heuristic reaches the same placement. The interesting behaviour is at other budgets and risk weightings, which is why the sweep below — not this table — is the result.

### Across budgets and weightings — `python scripts/sweep.py`

Twenty cells: budgets B = 1..4, each under five weightings — default (α=β=γ=δ=1, ε=0.1), then α=3, β=3, γ=3 and δ=3 one at a time. Every comparative number since D20 has come from this grid. It is held as a constant in `scripts/sweep.py` (D24); before that it existed only as a line in this README.

**Greedy beats the centrality baseline in 9 cells, ties in 11, and never loses.** That count needs three qualifications, and `sweep.py` prints all three:

- **"Never loses" is implied by optimality here, not earned.** Greedy equals the exhaustive optimum in all 20 cells, so it cannot score lower on F than any other placement. That shows the search works — the same fact as the 0.00% gap — not that F is a good objective.
- **The 9 wins are two different things, resting on 5 distinct placement disagreements.** Five are *swaps*: the same number of decoys, different ones, equal coverage. Four of those are one decision repeated across weightings — at B=2, the Historian instead of Engineering WS-2, accepting **+0.065 risk for +0.083 earlier detection**. Four are *declines*: greedy deploys fewer decoys than the budget allows (B=1 under default weights; B=1, 2 and 3 under δ=3), while centrality spends its budget regardless and scores as low as **−1.443**.
- **The research question's second clause fails exactly at the declines.** §8 asks for equal or greater Coverage and CritProt at equal or lower Cost. That holds in 16 of 20 cells; in the 4 declines greedy buys lower risk with lower coverage. Whether those are better placements depends on δ and on the detectability values — which is why A12, choosing an evaluation criterion that is not F itself, gates Phase D.

`--sens` reruns the comparison on a hand-picked sample of alternative grids. The split moves — from 8 to 15 wins across the sample — and in a consistent direction: the more heavily a grid weights risk, the more wins it shows, nearly all of them declines, and the more often clause 2 fails. So the count is never quoted without its grid.

### On the approximation guarantee — read before citing

The objective was corrected in D20 after exhaustive structural testing (`scripts/structure_check.py` enumerates all 32 subsets of **L**; no sampling).

- **Before D20:** `Early(x)` was a mean over *intercepted* paths, making it non-monotone — **30 monotonicity and 57 submodularity violations** on the current four-path instance. F(x) was **not submodular at all**, so no guarantee of any kind was available, contradicting what the specification claimed. (D20 recorded 16 and 18; correct then, for the three-path instance, stale since D21 — see D24.)
- **After D20:** F(x) is **submodular but not monotone**, and necessarily so, because Risk and Cost are subtracted. The classical (1−1/e) bound requires *monotone* submodular maximisation, so **it does not apply to F(x)**.

**Plain greedy carries no approximation guarantee, and this is stronger than "unproven".** Harshaw et al. (2019) — `sources.md` #353, obtained in full — include an appendix titled *"Greedy Performs Arbitrarily Poorly"* constructing an instance where standard greedy's ratio on f = g − c is **unbounded**. Plain greedy is the primary *reported* method because it is the standard practitioner heuristic and the MILP validates it exactly here, not because it is guaranteed.

**A guarantee is available, and it attaches to a different method.** D23 adopts Harshaw et al.'s **Distorted Greedy**, whose f = g − c form matches this objective exactly: `g = α·Coverage + β·Early + γ·CritProt` is monotone submodular and non-negative, `c = δ·Risk + ε·Cost` is modular and non-negative. Then g(S) − c(S) ≥ (1 − e^−γ)·g(OPT) − c(OPT), with **γ = 1** because g is genuinely submodular, giving **(1 − 1/e) ≈ 0.632**. All five preconditions are *verified on this instance* by `structure_check.py`, which tests the aggregate g and c and tests c for **modularity** rather than merely submodularity. The paper also proves a **matching hardness result** — no polynomial-time algorithm with value-oracle access to g can do better — so this is the best bound obtainable, not merely one we hold.

**And it costs something, which is reported rather than hidden.** Distorted greedy is **beaten by plain greedy in 2 of the 20 cells** — 34.2% below the optimum at B=2 under default weights, and 11.4% at B=4 under δ=3. That is correct behaviour: each of the k iterations has its own acceptance test and a declined iteration is never retried, so the early distortion factor can forfeit a budget slot permanently. The guarantee is a worst-case **floor**, not competitive average-case performance, and it earns its place through the *scalability* argument, where MILP validation is unavailable.

## Four findings that only appeared when the specification was built

**The MILP's first implementation was wrong, and building it proved that.** `docs/02-optimization-formulation.md` §3 originally recommended an unnormalised early-detection proxy as the simpler linearisation. Running it produced a placement scoring *worse* on the true F(x) than greedy — impossible for an exact validator. The unnormalised proxy rewards covering more paths over covering them earlier. Corrected in place, with the failed option kept in the text. Full account in D16. **It then happened a second time, in a different place: D24 found an off-by-one in the MILP's stage index (0-based in the solver, 1-based in `metrics.py`) producing the same impossible symptom — the exact validator beaten by a heuristic — suboptimal in 5 of the 20 comparison-grid cells — every one of them a cell where greedy and centrality disagree, and in four of them returning exactly centrality's placement. `run_comparison.py` had printed the resulting negative optimality gap and said nothing, because it only ever tested for equality. The real lesson of D16 was not "fix the proxy" but "assert the invariant in code"; that guard now exists in both `run_comparison.py` and `sweep.py` and refuses to report when it trips.**

**Greedy correctly stops before spending its budget (D15).** With a decoy already at DMZ Jump Host, a second placement would have improved coverage, but its detectability risk cost more in the objective than it gained — D5's decision to weight operational risk heavily, visibly doing something. The same behaviour now accounts for the four decline wins in the comparison grid, which is exactly where the research question's second clause fails.

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

python3 scripts/run_comparison.py               # the comparison above (B=3; pass a budget to change it)
python3 scripts/sweep.py --sens                 # the 20-cell comparison grid, plus grid sensitivity
python3 scripts/structure_check.py              # monotonicity, submodularity, modularity — exhaustive
python3 -m uvicorn src.api.main:app --reload    # backend
cd src/frontend && npm install && npm run dev   # frontend
```

`node_modules/`, `dist/` and `*.db` are not tracked — regenerate with the commands above. **After pulling any change to `data/schema.sql`, delete `data/deception_placement.db` and rebuild it:** SQLite does not retrofit table constraints, so an old database keeps the old ones (D23 added a method name to a `CHECK` constraint; an unrebuilt database rejects that method's runs with HTTP 500).

---

## Where to start reading

New to the project: `docs/02-system-flow.md` for how it fits together, then `docs/formal-problem-definition.md` for the mathematics. `docs/00-glossary.md` defines every term. `docs/00-decisions-log.md` explains why each choice was made, including the ones that turned out wrong.
