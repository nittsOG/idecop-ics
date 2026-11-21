# Phase D Results

The results of Phase D, the project's evaluation. It was run once, on 19 November 2026, with the inputs and code frozen (D40) and the rules for judging the results fixed in advance by the user's pre-registration (D39). This file reports what came out; D41 records it in the decisions log. The full output is `data/results/phase-d.json`. How the tests work is in `03-evaluation-methodology.md`; this file does not repeat it beyond what a reader needs.

## 1. In plain terms

**What the project builds.** An optimiser that decides where to put decoys (fake machines that raise an alarm when an attacker touches them) in a model of an industrial control network. It chooses positions by maximising a score, F, built from five things: how many known attack paths are caught, how early, how important the protected machines are, minus how exposed the decoys are and how many there are. The method that does the choosing is called greedy.

**Why F alone cannot judge it.** Greedy finds the best possible F every time on this network. So "greedy scores higher on F than other methods" is automatic, and it says nothing about whether F picks good positions. Phase D therefore judged the positions by tests the optimiser never sees.

**The three tests**, each run at budgets of one to four decoys:
- **H1, hidden attack paths.** One of the five known attack paths is hidden from the optimiser, the decoys are placed using the other four, and the test asks whether the hidden path is caught anyway. This is done five times, hiding each path in turn. The result is how many of the five hidden paths are caught.
- **H2, simulated attackers.** Attackers start from any of seven machines an attacker could break into first, and walk every short route to any controller or attack target: 109 routes. The result is the share of routes that run into a decoy (detection), and how early they do (earliness).
- **H3, a simpler optimiser.** The same tests against an optimiser that only counts how many paths are caught, ignoring F's other four parts. If those parts are worth having, the full method should do at least as well.

**What greedy is compared with:** betweenness centrality (the decoys go on the machines that the most shortest network routes pass through), random placement (30 random placements, averaged), and the coverage-only optimiser.

**The rule, fixed before the run:** a hypothesis holds at a budget if greedy is at least as good as every comparator on every measure there. It is *supported* if it holds at all four budgets, *not supported* if it holds at none, and *mixed* otherwise.

**The answer: all three are mixed.**
- **At a budget of two decoys, all three hold.** Greedy's placement caught four of the five hidden paths (centrality three, random 2.5 on average, the coverage-only optimiser under one) and caught at least as many simulated attackers as any comparator, at least as early.
- **At a budget of four, none holds.** Greedy places only three decoys there, because once every known path is caught at its first step a fourth decoy adds risk and cost to F and nothing else. The comparators always use all four, and the extra decoy catches more: centrality caught all five hidden paths and 78% of simulated routes, against greedy's four paths and 69%.
- **At a budget of one, greedy caught none of the hidden paths.** Its single decoy goes on the entry point shared by two of the four paths it can see, and the hidden path never starts there. In the simulation at that budget it did as well as centrality (the same decoy) and better than the others.
- **At a budget of three,** greedy caught more hidden paths than every comparator, and caught simulated attackers earlier than every comparator. But it caught slightly fewer of them than random placement (69% against 72%) and the coverage-only optimiser (69% against 71%), so H2 and H3 fail there.

**What this means.** F picks positions that catch attacks like the known ones, and catch them early. It sees no value in decoys beyond the known paths, so once those are covered it stops, while attacks from other starting points remain. On this network that costs it most comparisons at the largest budget, the hidden paths at the smallest, and, narrowly, simulated detection at a budget of three. The result is reported as it came out: a mixed result was accepted in advance as a valid outcome (D39 item 1).

## 2. How it was run

| | |
|---|---|
| Commit | `b43de49` (D40), a fresh clone; the freeze manifest is at `bc93d85` and every frozen file matched it |
| Environment | `uv run scripts/setup.py`: Python 3.13.18, every package as in `requirements.lock` |
| Database | built from the frozen schema and seed; the committed review restored (10 cards, 9 pass Filter 1); an export equals `data/review/plausibility_review.csv` byte for byte |
| Command | `uv run python scripts/evaluate.py --json data/results/phase-d.json`, run once, at 17:17 UTC on 19 November 2026; it took 2.3 seconds |
| Output | `data/results/phase-d.json`, SHA-256 `3081026ed338…` |
| Grid | default weights (1, 1, 1, 1, 0.1) for the hypotheses; the 20 cells of the declared grid (B = 1 to 4 under five weightings) for the secondary counts |

Every win, tie and loss below was re-counted from the results file by the 10⁻⁹ rule, separately from the script's own tallies; the two agree exactly.

## 3. The verdicts

| Hypothesis | Measures | Holds at | Verdict | Wins / ties / losses |
|---|---|---|---|---|
| H1 | hidden paths caught, against centrality and random | B = 2, 3 | **mixed** | 4 / 0 / 4 |
| H2 | simulated detection and earliness, against centrality and random | B = 1, 2 | **mixed** | 9 / 2 / 5 |
| H3 | simulated detection and earliness, and hidden paths caught, against the coverage-only optimiser | B = 1, 2 | **mixed** | 6 / 3 / 3 |

**Every comparison**, greedy's value first:

| B | H1: hidden paths (of 5) | H2: detection | H2: earliness | H3 (coverage-only): detection / earliness / hidden paths |
|---|---|---|---|---|
| 1 | 0 vs centrality 2 (loss); vs random 1.43 (loss) | 0.336 vs 0.336 (tie); vs 0.295 (win) | 0.255 vs 0.255 (tie); vs 0.179 (win) | 0.336 vs 0.300 (win) / 0.255 vs 0.171 (win) / 0 vs 0 (tie) |
| 2 | 4 vs 3 (win); vs 2.53 (win) | 0.555 vs 0.480 (win); vs 0.532 (win) | 0.439 vs 0.401 (win); vs 0.341 (win) | 0.555 vs 0.555 (tie) / 0.439 vs 0.439 (tie) / 4 vs 0.75 (win) |
| 3 | 4 vs 3 (win); vs 3.47 (win) | 0.692 vs 0.669 (win); vs 0.716 (**loss**) | 0.583 vs 0.515 (win); vs 0.471 (win) | 0.692 vs 0.710 (**loss**) / 0.583 vs 0.568 (win) / 4 vs 1.67 (win) |
| 4 | 4 vs 5 (**loss**); vs 4.10 (**loss**) | 0.692 vs 0.779 (**loss**); vs 0.826 (**loss**) | 0.583 vs 0.674 (**loss**); vs 0.591 (**loss**) | 0.692 vs 0.823 (**loss**) / 0.5833 vs 0.5835 (**loss**) / 4 vs 3.03 (win) |

In the H2 columns the first comparison is against centrality and the second against random. The earliness loss to the coverage-only optimiser at B = 4 is by 0.00025, but it is above 10⁻⁹, so by the rule it is a loss.

## 4. Hidden paths (leave-one-path-out) in detail

Held-out paths caught (of 5) / earliness / criticality-weighted protection, default weights:

| Method | B = 1 | B = 2 | B = 3 | B = 4 |
|---|---|---|---|---|
| Greedy (proposed) | 0.00 / 0.00 / 0.00 | 4.00 / 0.80 / 0.82 | 4.00 / 0.80 / 0.82 | 4.00 / 0.80 / 0.82 |
| Distorted greedy | 0.00 / 0.00 / 0.00 | 4.00 / 0.80 / 0.82 | 4.00 / 0.80 / 0.82 | 4.00 / 0.80 / 0.82 |
| MILP (exact) | 0.00 / 0.00 / 0.00 | 4.00 / 0.80 / 0.82 | 4.00 / 0.80 / 0.82 | 4.00 / 0.80 / 0.82 |
| Coverage-only, ties averaged | 0.00 / 0.00 / 0.00 | 0.75 / 0.15 / 0.16 | 1.67 / 0.32 / 0.35 | 3.03 / 0.47 / 0.62 |
| Coverage-only greedy | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 3.00 / 0.60 / 0.60 | 3.00 / 0.60 / 0.60 |
| Centrality | 2.00 / 0.40 / 0.45 | 3.00 / 0.60 / 0.63 | 3.00 / 0.60 / 0.63 | 5.00 / 1.00 / 1.00 |
| Random (mean of 30) | 1.43 / 0.21 / 0.29 | 2.53 / 0.38 / 0.52 | 3.47 / 0.48 / 0.71 | 4.10 / 0.61 / 0.82 |

**What the folds show** (from the placements in the results file; *verified*):
- **B = 1.** When P1 or P4 is hidden, greedy's one decoy goes on the DMZ Jump Host, the entry of P2 and P5. When P2 or P5 is hidden, it goes on the Engineering WS, the entry of P1 and P4. When P3 is hidden, it goes on the DMZ Jump Host. None of these is on the hidden path, so it catches none. Centrality's decoy, the DMZ Jump Host, does not depend on the paths, and catches P2 and P5 when they are hidden.
- **B = 2 to 4.** Greedy holds the DMZ Jump Host and the Engineering WS in every fold, so it catches P1, P2, P4 and P5 at their first step. It never catches P3, the only path through the OT Firewall and Engineering WS-2. That was stated in advance (D39 item 7).
- **B = 4.** Centrality's four decoys include Engineering WS-2, so it catches P3 too: five of five.

## 5. Simulated attackers in detail

The primary population: seven footholds, 33 foothold–objective pairs, 109 routes at most one hop longer than the shortest. Detection / detected before the objective / earliness, default weights:

| Method | B = 1 | B = 2 | B = 3 | B = 4 |
|---|---|---|---|---|
| Greedy (proposed) | 0.336 / 0.336 / 0.255 | 0.555 / 0.555 / 0.439 | 0.692 / 0.692 / 0.583 | 0.692 / 0.692 / 0.583 |
| Distorted greedy | 0.336 / 0.336 / 0.255 | 0.555 / 0.555 / 0.439 | 0.692 / 0.692 / 0.583 | 0.692 / 0.692 / 0.583 |
| MILP (exact) | 0.336 / 0.336 / 0.255 | 0.555 / 0.555 / 0.439 | 0.692 / 0.692 / 0.583 | 0.692 / 0.692 / 0.583 |
| Coverage-only, ties averaged | 0.300 / 0.230 / 0.171 | 0.555 / 0.555 / 0.439 | 0.710 / 0.676 / 0.568 | 0.823 / 0.678 / 0.584 |
| Coverage-only greedy | 0.336 / 0.336 / 0.255 | 0.555 / 0.555 / 0.439 | 0.692 / 0.692 / 0.583 | 0.692 / 0.692 / 0.583 |
| Centrality | 0.336 / 0.336 / 0.255 | 0.480 / 0.480 / 0.401 | 0.669 / 0.588 / 0.515 | 0.779 / 0.756 / 0.674 |
| Random (mean of 30) | 0.295 / 0.230 / 0.179 | 0.532 / 0.433 / 0.341 | 0.716 / 0.582 / 0.471 | 0.826 / 0.710 / 0.591 |

**What drives it.**
- Greedy's decoys sit on P's entry points: the DMZ Jump Host, then the Engineering WS, then the OT Firewall. Routes that start there are caught at their first step, so greedy's earliness is high. Routes that start at the HMI, the Historian, Engineering WS-2 or the Backup Control Switch are caught only if they pass one of those three. *(Verified from the placements; that this is the main reason greedy wins earliness more often than detection is Claude's reading, likely.)*
- None of greedy's decoys sits on an objective, so everything it detects it detects before the objective.
- At B = 4 greedy's placement is its B = 3 placement, and the other methods' fourth decoy reaches more routes.

**Sensitivity, reported as counts** (detection / earliness; greedy against centrality, random and the coverage-only optimiser over B = 1 to 4, wins / ties / losses):

| Population | Routes | Against centrality | Against random | Against coverage-only |
|---|---|---|---|---|
| Shortest routes only (slack 0) | 54 | 1/1/2 and 2/1/1 | 2/0/2 and 3/0/1 | 1/1/2 and 3/1/0 |
| Up to two hops longer (slack 2) | 259 | 2/1/1 and 2/1/1 | 2/0/2 and 3/0/1 | 1/1/2 and 2/1/1 |
| P's entry points only (documented) | 50 | 2/2/0 and 2/2/0 | 4/0/0 and 4/0/0 | 3/1/0 and 3/1/0 |

As expected, greedy caught every route of the documented population at its first step from B = 3 (detection 1.00, earliness 1.00); that population is reported, not counted toward H2.

## 6. Expectations stated before the run, against what happened

| Stated in advance (D39 item 7) | Outcome |
|---|---|
| Documented entry points: greedy at B = 3 catches every route at its first step | Confirmed: 1.00 detection and earliness at B = 3 and 4 |
| Primary population: H2 is at risk; centrality may detect more routes than greedy | Partly: H2 is mixed. Centrality detected more at B = 4 only (0.779 against 0.692); random detected more at B = 3 and 4 |
| Hidden P1, P2, P4, P5 caught at their first step whenever the budget lets greedy keep the DMZ Jump Host and the Engineering WS | Confirmed at B = 2 to 4. At B = 1 the budget cannot hold both, and none is caught |
| Hidden P3 never caught by greedy; the comparators can catch it | Confirmed: greedy misses it at every budget. Centrality catches it from B = 2, random in 27%, 43%, 57% and 70% of its placements at B = 1 to 4, and the coverage-only optimiser in some of its tied placements from B = 3 |
| The route OT Firewall → Engineering WS-2 → PLC-02 is caught only by a placement holding the OT Firewall (greedy from B = 3) or Engineering WS-2 | Confirmed: greedy catches it at its first step from B = 3; centrality from B = 2; the coverage-only optimiser from B = 3; random in 27%, 43%, 57% and 70% of its placements at B = 1 to 4 |

## 7. Also reported, as counts

**Every comparison over all 20 cells of the declared grid** (greedy against each comparator, wins / ties / losses):

| Comparator | Hidden paths | Hidden-path earliness | Simulated detection | Simulated earliness |
|---|---|---|---|---|
| Centrality | 7 / 3 / 10 | 7 / 3 / 10 | 9 / 4 / 7 | 9 / 4 / 7 |
| Random (mean) | 9 / 0 / 11 | 14 / 0 / 6 | 10 / 0 / 10 | 14 / 0 / 6 |
| Coverage-only, ties averaged | 14 / 5 / 1 | 15 / 5 / 0 | 5 / 5 / 10 | 9 / 5 / 6 |

**Other counts at the default weights** (over B = 1 to 4):
- *Criticality-weighted protection of hidden paths:* against centrality 2/0/2, random 3/0/1, coverage-only 3/1/0.
- *Detected before the objective:* against centrality 2/1/1, random 3/0/1, coverage-only 3/1/0.
- *The coverage-only greedy form:* greedy never loses to it. It places the same decoys as greedy on all five paths, so the simulation ties at every budget; on hidden paths greedy wins at B = 2 to 4 and ties at B = 1.
- *Distorted greedy and the MILP:* the MILP placed the same decoys as greedy in every cell and fold. Distorted greedy differed in one fold, B = 3 under δ = 3 with P5 hidden.
- *Decoys greedy placed:* at B = 4, three under four of the five weightings; under δ = 3 it places two at both B = 3 and B = 4. The comparators always place B.

**The F-based grid, the weight sweep and the structure check**, re-run on the Phase D database: the outputs equal D40's byte for byte. Against centrality on F, 16 wins / 4 ties / 0 losses; §8's clause 2 holds in 18 of 20; greedy equals the exact optimum in all 20 cells.

## 8. Post-run checks of F (D39 item 4)

With the frozen `metrics.score`, the F of greedy's and the MILP's placements was computed in every cell (20, on all five paths) and every fold (100, on the four visible paths), and compared with every placement of at most B candidates:
- greedy's placement is the best possible F in all 120;
- no other placement reaches greedy's F in any of them, so greedy is the unique optimum everywhere and no exception is reported;
- the MILP placed the same decoys as greedy in all 120 and is never below it, so no run is void (D24).

## 9. Against the D20 wording (`formal-problem-definition.md` §8)

- *Clause 1, a higher F than random and centrality:* greedy's F is never below either, and that follows from optimality (D24's caveat): greedy is the unique optimum in all 20 cells. It is above the random mean in all 20. Against centrality it is higher in 16 cells and equal in 4, where centrality places the same decoys (16 wins / 4 ties / 0 losses).
- *Clause 2, equal or greater Coverage and CritProt at equal or lower Cost:* holds against centrality in 18 of 20 cells; it fails at B = 1, δ = 3 (a swap) and B = 4, δ = 3 (a decline). As in every earlier entry since D24, the clause is measured against centrality.

## 10. What the results support

**May be stated, for this one modelled network:**
- At a budget of two decoys, F's placement caught at least as many hidden paths and simulated attackers as every comparator, at least as early.
- At a budget of three, it caught more hidden paths than every comparator (four of five) and caught simulated attackers earlier than every comparator, while detecting slightly fewer than random placement and the coverage-only optimiser.
- At budgets of two and more it never caught the one hidden path that shares no entry point with the others (P3), and at a budget of one it caught no hidden path.
- With a fourth decoy available it placed three, and lost every comparison at that budget except hidden paths against the coverage-only optimiser (four against 3.03).
- Greedy found the unique best F in every case tested, and the exact MILP agreed.

**May not be stated:**
- That F's placements catch unseen attacks better than the baselines in general: every hypothesis is mixed.
- Anything statistical: five folds and one network give counts, not significance.
- That a larger budget improves F's placements: on this network greedy places at most three decoys under the default weights.

Because the verdicts are mixed, the novelty claim's validation clause now reads "evaluated against random and centrality baselines" (A28; the user's choice, recorded in D41).

## 11. Limitations

- **One modelled network**, of eleven assets, five paths and nine candidate positions.
- **Paired entry points.** P1 and P4 start at the same machine, as do P2 and P5, so hiding one of a pair tests less than hiding P3 (`03-evaluation-methodology.md` §2).
- **The simulated attacker is a model.** Its starting points, uniform weights and route lengths are declared choices; slacks 0 and 2 and the documented population show how much they matter.
- **Detectability is not simulated:** a route counts as caught the moment it reaches a decoy's position.
- **Equal budget, not equal decoy count.** The research question compares methods at equal budget, so greedy's choice to place fewer decoys counts against it where a fourth decoy would have caught more. That was fixed before the run (D39 item 4).

*Recorded in D41, 19 November 2026. Reference: `data/results/phase-d.json`, `scripts/evaluate.py`, `03-evaluation-methodology.md`, D24, D33, D37, D39, D40.*
