# Evaluation Methodology — Phase D (A12)

How Phase D judges the placements, fixed before any of these tests ran on the testbed (D37). It answers A12: the research question's wording, and what the placements are judged against besides F. It changes nothing that F, the methods or the inputs compute. From the freeze onwards it changes only by a decisions-log entry that states the effect. The code is `src/evaluation/` and `scripts/evaluate.py`. `scripts/evaluation_selftest.py` checks that code on a toy network, without touching the testbed.

## 1. In plain terms

The optimiser picks where to put decoys by maximising a score, F, that adds up five things: how many attack paths are caught, how early, how important the protected assets are, minus how exposed the decoys are and what they cost. On the testbed the greedy method finds the best possible F in every case tested (D31, D33). So "greedy scores higher on F than the baselines" is automatic. It shows the search works, not that F is a good way to choose decoy positions. Phase D therefore also judges the placements by things the optimiser never sees:

- **Leave-one-path-out** (§2). Hide one of the five attack paths from the optimiser, let it place decoys using the other four, and check whether the hidden path is caught anyway. Repeat for each path. This is the K-fold-style validation the guide asked for (D32).
- **Attack simulation** (§3). Let simulated attackers start from any machine an attacker could first break into, and walk any loop-free route through the network's recorded connections to any controller or path target. Count how many walk past a decoy, and how early. This is the simulation the guide asked for (D32). F is never consulted.
- **A coverage-only comparator** (§4). The same search, but scoring only "how many paths are caught". If F's other four terms are worth having, the full method should do at least as well on the two tests above.

The existing comparison grid and weight sweep are still run and reported (§5). They answer a narrower question: how well the search optimises F.

## 2. Leave-one-path-out

- **Folds.** One per path in P (P1–P5), so five. In each fold the method receives the other four paths, unchanged: same candidates L, same detectability values, same weights, same K = 4. It is called exactly as `scripts/run_comparison.py` calls it.
- **Scoring.** The placement is scored on the held-out path, which the method never saw:
  - *interception:* 1 if any decoy lies on the path's asset sequence, else 0;
  - *earliness:* (n − s)/(n − 1) for a path caught at step s of n, the endpoint Early uses (D33), and 0 if it is not caught;
  - *criticality-weighted protection:* Crit(target) if caught, else 0.

  Over the five folds, interceptions are summed (0 to 5). Earliness is divided by 5, and protection by the five targets' total criticality, as Early and CritProt are in F.
- **Path-agnostic methods.** Centrality and random do not read P, so they place the same decoys in every fold. Random reports the mean and s.d. over its 30 placements (seed 42, as frozen).
- **Why it is meaningful now.** On the reviewed set every path meets at least two candidates (D31), so decoys placed for four paths can catch the fifth. On D25's seeded set every path met exactly one candidate, so the test could not work, which is why A12 waited for A32.
- **What limits it.** Five folds are five data points, reported as counts and never as statistics. Paths share entry assets: P1 and P4 both start at the Engineering WS, P2 and P5 at the DMZ Jump Host, and only P3 starts at the OT Firewall. So holding out a path that shares its entry tests less than holding out P3. §7 states what that leads one to expect.

## 3. Attack simulation

**The population of simulated attackers** (`src/evaluation/simulation.py`):
- *Footholds:* every asset except the Attacker node and the controllers, that is, every asset where an attacker could make initial access: OT Firewall, DMZ Jump Host, Historian, Engineering WS, Engineering WS-2, HMI and the Backup Control Switch.
- *Objectives:* every controller (PLC-01, PLC-02, PLC-03 (RTU)) and every declared path target (D33, A36), which adds Engineering WS-2 and the Historian.
- *Routes:* every simple (loop-free) path from a foothold to an objective, through the recorded connections walked in either direction, as P's own moves are (D33, A35), with at most the shortest number of hops plus a slack. The primary slack is 1: an attacker takes a shortest route or one hop longer. The Attacker node is not part of any route.
- *Weights:* every foothold–objective pair is equally likely, and every route within a pair is equally likely. A pair whose foothold is its objective is skipped.

The population is enumerated in full, so the result is the exact average over every route. There is no random draw and no seed: it is the limit of simulating ever more attackers.

**Detection.** A decoy at a candidate l sits on l's segment (D26), so a route meets it where the route reaches l. A route is detected at the first position k that holds a decoy. Position 1 is the foothold, where initial access happens, as at P's first steps. For each placement three numbers are reported, each over the routes with the weights above, so each foothold–objective pair weighs the same and its routes share that weight:
- *detection rate:* the weighted share of routes detected anywhere;
- *detected before the objective:* the weighted share detected before the route's last asset;
- *earliness:* the weighted average of (n − k)/(n − 1) for a route of n assets, with an undetected route counting 0. It is 1 when an attacker is caught at the foothold and 0 when caught at the objective.

*(D39 stated the weights in these three lines. Until then they said "the share of routes" and "the average", which could be read as counting every route equally; the code has always weighted them as above.)*

**Populations reported.**

| Population | Footholds | Slack | Role |
|---|---|---|---|
| primary | all seven | 1 | the hypotheses (§5) |
| slack0 | all seven | 0 | sensitivity: shortest routes only |
| slack2 | all seven | 2 | sensitivity: longer detours |
| documented | P's first-step assets: Engineering WS, DMZ Jump Host, OT Firewall | 1 | secondary: the entry points P documents |

**Why the footholds are not just P's entry points.** P's three entry assets are exactly where greedy puts its three decoys at B = 3 (D31, D33). A simulation that starts every attacker there would show any placement holding them catching every route at its first step. That repeats what F's Early term already rewards; it doesn't test it. The documented population is still reported, with that caveat. Claude made this choice knowing greedy's published placements, and the reason is the one given here.

**Not modelled, stated rather than hidden.**
- *Detectability:* an attacker who recognises a decoy and goes round it is not simulated. F prices this with Risk, which is an exposure score and not a probability (D20), so it cannot become an avoidance probability without a new assumption.
- *Attacker skill and time:* not modelled.
- *Unrecorded routes:* routes through connections the model does not record are not considered.

The simulation reads no term of F.

## 4. Methods compared

| Method | Role | How it is called |
|---|---|---|
| Greedy | proposed, primary | `baselines.greedy`, unchanged |
| Distorted greedy | the guaranteed method (D23) | `baselines.distorted_greedy`, unchanged |
| MILP | exact reference; each fold asserts that it is never below greedy on the training paths (D24's guard) | `milp.solve_milp`, unchanged |
| Coverage-only, ties averaged | **comparator, primary form** | every placement of B decoys with the highest Coverage that B decoys reach, each equally likely |
| Coverage-only greedy | comparator, second form | `baselines.greedy` with weights (1, 0, 0, 0, 0) |
| Centrality | baseline (D4) | `baselines.centrality_baseline`, unchanged |
| Random | baseline | `baselines.random_baseline`, 30 placements, seed 42, unchanged |

**The coverage-only comparator** asks whether F's five terms add anything over plain attack-path blocking, the kind of objective CN 121356815 A optimises: an attack-path blocking ratio under a count cap (D36 item 6). The user added it on 16 November 2026 (D37).
- *Why two forms.* The greedy form, which the user first approved, keeps the first candidate it scans among candidates of equal gain, and that order is arbitrary. On the testbed several candidates block the same number of paths, so its result would partly reflect that order. The ties-averaged form removes it. The user chose it as the primary form on 16 November 2026, once Claude raised the tie-break, and the greedy form is reported beside it.
- *Weights.* Neither form reads the weights, so each places the same decoys in every weighting.

## 5. Research question and hypotheses

**Primary research question (A12; proposed by Claude and accepted by the user as worded, 16 November 2026):**

> On the modelled testbed, does choosing decoy positions by the composite objective F — found by greedy and confirmed exact by MILP — catch attacks the optimiser was not given, at least as often and as early as betweenness-centrality placement, random placement and a coverage-only optimiser, at equal budget? The attacks are each attack path when it is held out of the optimisation, and simulated attack routes from every non-controller foothold to every objective.

The D20 wording (`formal-problem-definition.md` §8) is still reported against, with D24's caveat that its first clause follows from optimality.

**Hypotheses, at the default weights (1, 1, 1, 1, 0.1) and budgets B = 1 to 4.** A comparison *holds* at a budget when greedy is not below its comparator by more than 10⁻⁹ (absolute; `TOL` in `scripts/evaluate.py`); a smaller difference is a tie, and a tie holds. *(D39 stated the tolerance, which the code already applied.)*

| | Criterion | Greedy compared with |
|---|---|---|
| H1 | held-out interceptions (§2) | centrality; random (mean) |
| H2 | simulated detection rate and earliness, primary population (§3) | centrality; random (mean) |
| H3 | simulated detection rate and earliness, and held-out interceptions | coverage-only, ties averaged |

At a budget, a hypothesis holds if every one of its comparisons holds there. It is **supported** if it holds at all four budgets, **not supported** if it holds at none (even where some of its comparisons hold), and **mixed** otherwise. Strict wins, ties and losses are reported with it, so a result made only of ties is not presented as a win, and a supported verdict with no win is labelled "supported (ties only)". *(D39: clarified to state the rule `scripts/evaluate.py` applies. It read: "Each hypothesis is supported if all its comparisons hold at every budget, not supported if they hold at none, and mixed otherwise", which could also be read as counting comparisons rather than budgets.)*

**Secondary, reported as counts:**
- every comparison over all 20 cells of the declared grid (`scripts/sweep.py`'s BUDGETS × WEIGHTINGS, read from that file);
- the slack0, slack2 and documented populations;
- the coverage-only greedy form;
- criticality-weighted protection and detection before the objective;
- the F-based grid, the weight sweep and the structure check (`scripts/sweep.py --sens`, `scripts/run_comparison.py`, `scripts/structure_check.py`), as before.

The pre-registration (A15) is the user's own entry. It restates these hypotheses and rules, and `scripts/evaluate.py` applies exactly them. If the user changes a rule there, the code changes to match before the freeze. *D39 (18 November 2026): committed. The user adopted Claude's draft, corrected after an independent review, as his own entry. It changes no rule: it states two that the code already applied, the tolerance and the verdict rule above. Where it is more specific than this file, it governs.*

## 6. The explanation layer's evaluation (secondary research question, A6)

The explanation layer is built before TA-2 (D37). Every explanation it serves is checked automatically before it is shown:
- every number in the text must equal a number in the run's facts when both are rounded to two decimals;
- every asset named must belong to the run: its placement, a comparator's placement or a path through them.

An explanation that fails either check is replaced by a template built from the same facts, and the failure is counted. Phase D generates one explanation for greedy's placement at each budget B = 1–4 under the default weights, with the declared model: `qwen3:4b`, temperature 0, thinking off. It reports:
- how many passed both checks on the first generation;
- the failures, by kind;
- how long each took on the user's laptop.

*D39: the prompt, the model tag (`qwen3:4b`, Q4_K_M) and both checks are committed before the four counted explanations are generated, and "the first generation" means the first after that commit.*

The user rates the four explanations as clear, partly clear or unclear for a reader new to the project, reported as counts. This is a small check of faithfulness and readability, not a user study.

## 7. Expectations stated before any run

These come from the placements published in D31 and D33. No leave-one-path-out or simulation output on the testbed existed when they were written.
- *Documented population.* Greedy's placement at B = 3 holds all three of P's entry assets, so it is expected to catch every route there at its first step. It is reported for that reason, not counted toward H2.
- *Primary population.* H2 is at risk. Routes that start at the HMI, the Historian, Engineering WS-2 or the Backup Control Switch do not start at any of P's entry assets, so a placement of those assets cannot catch them at their foothold. Centrality favours assets that many shortest paths of the recorded network cross, so it may detect more routes there than greedy does. *(D39: corrected. This bullet said such routes "pass none of P's entry assets", which is false: the Historian connects to the OT Firewall and to Engineering WS, so routes from it can pass an entry asset after their foothold. It also said "many shortest routes", where betweenness counts the shortest paths of the recorded, directed network.)*
- *Leave-one-path-out.* Holding out P1 or P4 leaves the Engineering WS on the other path, and holding out P2 or P5 leaves the DMZ Jump Host on the other. Those four are therefore expected to be caught at the held-out path's first step whenever the budget lets greedy keep those assets. P3 is the only path through the OT Firewall and Engineering WS-2, so with P3 held out greedy cannot catch it at any budget: it adds a decoy only when that raises F, and a decoy on no training path raises no gain term. Centrality, random and the coverage-only optimiser can still place those assets. *(D39: corrected. It read "greedy is expected to miss it unless spare budget or Engineering WS-2 covers it"; greedy's stopping rule, in `baselines.greedy`, rules out both.)*
- *The route D33 asked about.* D33 recorded that no path continues the outside route OT Firewall → Engineering WS-2 → PLC-02, and asked that A12's simulation state in advance what it expected there. The route is in the primary population (foothold OT Firewall, objective PLC-02). A placement holding the OT Firewall catches it at the foothold, one holding Engineering WS-2 catches it at step 2, and any other placement misses it. Greedy's published placements hold the OT Firewall only from B = 3.

## 8. Order, freeze and what is frozen

1. D37 and this file are committed: the design is fixed, and nothing has run on the testbed.
2. The user's pre-registration (A15) is committed. *(D39, 18 November 2026.)*
3. **The freeze.** `scripts/freeze.py` writes `data/freeze/manifest.json` with the SHA-256 of every file that feeds the evaluation, and it refuses if any of those files has uncommitted changes. The frozen files are:
   - the lock file;
   - the schema, the seed and the committed review;
   - `src/graph_model/`, `src/optimizer/`, `src/evaluation/` and `src/plausibility/`;
   - `scripts/evaluate.py`, `sweep.py`, `run_comparison.py` and `structure_check.py`.

   Every check is re-run, and the freeze entry states the effect against D25. *(D40, 19 November 2026: frozen at commit `bc93d85`, 19 files. Every check re-run reproduces D33 item 4, and D40 states the effect against D25.)*
4. Phase D runs. `scripts/evaluate.py` refuses to run unless every frozen file still matches the manifest. How it runs (D39 item 5):
   - on a database rebuilt from the frozen seed with the committed review restored; an export from it must equal `data/review/plausibility_review.csv` byte for byte;
   - as `uv run python scripts/evaluate.py --json data/results/phase-d.json`, with the results file committed with the results;
   - wins, ties, losses and every count the script does not print are tallied from that file by the same 10⁻⁹ rule;
   - after the run, the F of greedy's and the MILP's placements in every cell and fold, and whether any other placement reaches greedy's F, are computed from that file with the frozen `metrics.score`.
5. The results are recorded in their own entry, whichever way they go.

A defect found after the freeze gets its own entry stating its effect on every result. It is then fixed and frozen again, and both runs are reported. *D39 item 1 defines a defect, code that does not do what D39 and §2–§5 state, and makes the corrected run the result.*

## 9. Limitations

- **One modelled instance.** There are eleven assets, five paths and nine candidates. The physical testbed comes last, if time allows (A16, D37), and synthetic instances are A12's optional extension, after TA-2.
- **The simulated attacker is a model.** Its foothold and objective sets, uniform weights and slack are declared choices; the slacks 0 and 2 and the documented footholds show how much they matter. It is not a measurement of real attacks.
- **Detectability is not simulated** (§3), and every path and route is credited the moment it reaches a decoy's position, as F credits it (D26).
- **Five folds** support counts only.
