"""
sweep — the comparative sweep behind every comparative number quoted in
README.md, the decisions log and the thesis results chapter.

THE GRID IS THE ONE THE README HAS DOCUMENTED SINCE D20 (see D24):

    budgets     B = 1, 2, 3, 4
    weightings  (alpha, beta, gamma, delta, epsilon)
        default   (1, 1, 1, 1, 0.1)
        alpha=3   (3, 1, 1, 1, 0.1)
        beta=3    (1, 3, 1, 1, 0.1)
        gamma=3   (1, 1, 3, 1, 0.1)
        delta=3   (1, 1, 1, 3, 0.1)

Twenty cells. D20 (17 wins / 3 ties), D21 (10/10), D22 (5/15) and D22a
(9 wins / 11 ties / 0 losses) all quote results from this grid. The grid itself
lived in a single line of README prose — in no decisions-log entry and in no
code. It is now a constant here, and on the frozen inputs it reproduces D22a's
9 / 11 / 0 exactly.

WHY IT MOVED INTO CODE. An earlier draft of D24 — never pushed, caught when the
patch was reviewed before being applied — rewrote the README section holding
the grid without recognising that line as its definition, concluded that no
grid had ever been recorded, and substituted a delta-only grid over B = 1..5
that reports a more favourable 13 / 7 / 0. A definition that can be deleted by
editing prose is too fragile for an evaluation input. Do not change the
constants below without a decisions-log entry stating the effect on every
quoted number, per the evaluation-integrity rule.

WHAT THE RECORD MEANS — read before quoting it. The win/tie count alone
misleads, so this script reports what it is made of:

  * Greedy equals the exhaustive optimum in every cell of the declared grid.
    On this instance it therefore cannot score lower on F than any other
    placement: "0 losses" is IMPLIED BY OPTIMALITY. It measures search quality,
    which the 0.00% optimality gap already reports. It is not evidence that F
    is a good objective, because F is both what is maximised and the yardstick.

  * Wins come in two kinds. A SWAP places as many decoys as the baseline but
    different ones. A DECLINE places fewer. They are different claims and are
    counted separately.

  * The primary research question's second clause (formal-problem-definition
    §8: equal or greater Coverage and CritProt at equal or lower Cost) is
    checked cell by cell against the centrality baseline. It fails exactly
    where greedy declines.

How these facts are framed in the thesis is A12's decision, not this script's.

Run:  python scripts/sweep.py          the declared grid
      python scripts/sweep.py --sens   plus a labelled sample of alternative grids
"""
import sys
import itertools
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.graph_model import (load_graph, compute_criticality,
                             load_candidate_locations, load_attack_paths)
from src.optimizer.baselines import greedy, centrality_baseline, distorted_greedy
from src.optimizer.milp import solve_milp
from src.optimizer.metrics import score

# ---------------------------------------------------------------------------
# THE DECLARED GRID — as documented in the README since D20. Changing any value
# here changes every comparative number in the documentation.
# ---------------------------------------------------------------------------
BUDGETS = (1, 2, 3, 4)
WEIGHTINGS = {
    "default": (1.0, 1.0, 1.0, 1.0, 0.1),
    "alpha=3": (3.0, 1.0, 1.0, 1.0, 0.1),
    "beta=3":  (1.0, 3.0, 1.0, 1.0, 0.1),
    "gamma=3": (1.0, 1.0, 3.0, 1.0, 0.1),
    "delta=3": (1.0, 1.0, 1.0, 3.0, 0.1),
}
# ---------------------------------------------------------------------------

TOL = 1e-9
ROOT = Path(__file__).resolve().parents[1]
g = load_graph()
crit = compute_criticality(g)
candidates = load_candidate_locations()
paths = load_attack_paths()
central_scores = {n: crit[n]["central"] for n in crit}
names = {n: crit[n]["name"] for n in crit}

conn = sqlite3.connect(ROOT / "data" / "deception_placement.db")
detectability = {r[0]: r[1] or 0.0 for r in
                 conn.execute("SELECT asset_id, detectability_risk FROM candidate_locations")}
conn.close()

L = list(candidates)


def exhaustive_best(weights, budget):
    """Ground truth by enumeration. |L| is small, so the optimum is available
    without trusting either the solver or the heuristic."""
    best = None
    for r in range(budget + 1):
        for c in itertools.combinations(L, r):
            f = score(set(c), paths, crit, detectability, weights, budget).f_score
            if best is None or f > best:
                best = f
    return best


def evaluate_cell(B, W):
    xg, mg = greedy(L, paths, crit, detectability, B, W)
    xc, mc = centrality_baseline(L, central_scores, paths, crit, detectability, B, W)
    _, md = distorted_greedy(L, paths, crit, detectability, B, W)
    _, mm, _info = solve_milp(L, paths, crit, detectability, B, W)
    truth = exhaustive_best(W, B)

    if mg.f_score < mc.f_score - TOL:
        kind = "LOSS"
    elif mg.f_score <= mc.f_score + TOL:
        kind = "tie"
    elif len(xg) < len(xc):
        kind = "decline"
    else:
        kind = "swap"

    clause2 = (mg.coverage >= mc.coverage - TOL and
               mg.crit_prot >= mc.crit_prot - TOL and
               mg.cost <= mc.cost + TOL)
    return {
        "B": B, "fg": mg.f_score, "fc": mc.f_score, "fd": md.f_score,
        "fm": mm.f_score, "truth": truth, "kind": kind, "clause2": clause2,
        "greedy_opt": abs(mg.f_score - truth) < TOL,
        "milp_exact": abs(mm.f_score - truth) < TOL,
        "distorted_below": md.f_score < mg.f_score - TOL,
        "pair": (frozenset(xg), frozenset(xc)),
    }


def run_grid(budgets, weightings):
    return [(name, evaluate_cell(B, W)) for B in budgets for name, W in weightings.items()]


def tally(cells):
    kinds = [c["kind"] for _, c in cells]
    wins = [c for _, c in cells if c["kind"] in ("swap", "decline")]
    return {
        "n": len(cells),
        "swap": kinds.count("swap"), "decline": kinds.count("decline"),
        "tie": kinds.count("tie"), "loss": kinds.count("LOSS"),
        "distinct": len({c["pair"] for c in wins}),
        "greedy_opt": sum(c["greedy_opt"] for _, c in cells),
        "milp_exact": sum(c["milp_exact"] for _, c in cells),
        "clause2": sum(c["clause2"] for _, c in cells),
        "distorted_below": sum(c["distorted_below"] for _, c in cells),
    }


cells = run_grid(BUDGETS, WEIGHTINGS)
T = tally(cells)
n = T["n"]

print("=" * 86)
print("DECLARED GRID  (README since D20; code since D24)")
print("=" * 86)
print(f"budgets B = {list(BUDGETS)}")
for k, w in WEIGHTINGS.items():
    print(f"  {k:<8} (alpha, beta, gamma, delta, epsilon) = {w}")
print()
print(f"{'B':>2} {'weighting':<9} | {'greedy':>8} {'centr':>8} {'result':<8} {'clause2':<7} | "
      f"{'distort':>8} | {'MILP':>8} {'exhaust':>8} {'exact':<5}")
print("-" * 86)
for name, c in cells:
    print(f"{c['B']:>2} {name:<9} | {c['fg']:>8.4f} {c['fc']:>8.4f} {c['kind']:<8} "
          f"{'holds' if c['clause2'] else 'FAILS':<7} | {c['fd']:>8.4f} | "
          f"{c['fm']:>8.4f} {c['truth']:>8.4f} {'OK' if c['milp_exact'] else 'NO':<5}")

wins = T["swap"] + T["decline"]
fails = [(name, c) for name, c in cells if not c["clause2"]]
fails_are_declines = all(c["kind"] == "decline" for _, c in fails)

print()
print("=" * 86)
print("RESULT")
print("=" * 86)
print(f"greedy vs centrality: {wins} wins ({T['swap']} swap, {T['decline']} decline) / "
      f"{T['tie']} ties / {T['loss']} losses   (n={n})")
print(f"  the {wins} wins rest on {T['distinct']} distinct placement disagreements")
print()
print(f"greedy equals the exhaustive optimum in {T['greedy_opt']} of {n} cells.")
if T["greedy_opt"] == n:
    print("  => '0 losses' is implied by optimality on this instance. It reports search")
    print("     quality (as the 0.00% gap does), not the value of the objective.")
print()
print(f"RQ clause 2 vs centrality (Coverage >=, CritProt >=, Cost <=): holds in "
      f"{T['clause2']} of {n}, fails in {len(fails)}")
if fails:
    print("  fails at: " + ", ".join(f"B={c['B']} {name}" for name, c in fails))
    print(f"  every failure is a decline: {'YES' if fails_are_declines else 'NO'}")
print()
print(f"MILP vs exhaustive optimum: "
      f"{'exact in all ' + str(n) if T['milp_exact'] == n else str(n - T['milp_exact']) + ' MISMATCHES'}")
if T["milp_exact"] != n:
    raise SystemExit(
        "INVARIANT VIOLATED: the exact MILP disagrees with exhaustive enumeration. "
        "Its linearisation no longer matches metrics.score. Do not interpret these "
        "results; see D16 and D24.")
print(f"distorted greedy below plain greedy in {T['distorted_below']} of {n} cells "
      f"-- expected by design; see distorted_greedy's docstring")

if "--sens" in sys.argv:
    def delta_only(ds):
        return {f"delta={d:g}": (1.0, 1.0, 1.0, d, 0.1) for d in ds}

    alternatives = [
        ("declared (documented) grid", BUDGETS, WEIGHTINGS),
        ("one-at-a-time at 2 instead of 3", (1, 2, 3, 4), {
            "default": (1.0, 1.0, 1.0, 1.0, 0.1), "alpha=2": (2.0, 1.0, 1.0, 1.0, 0.1),
            "beta=2": (1.0, 2.0, 1.0, 1.0, 0.1), "gamma=2": (1.0, 1.0, 2.0, 1.0, 0.1),
            "delta=2": (1.0, 1.0, 1.0, 2.0, 0.1)}),
        ("delta only {0.1..1}", (1, 2, 3, 4), delta_only((0.1, 0.25, 0.5, 0.75, 1.0))),
        ("delta only {0.25..3}", (1, 2, 3, 4), delta_only((0.25, 0.5, 1.0, 2.0, 3.0))),
        ("delta only {0.5..3}", (1, 2, 3, 4), delta_only((0.5, 1.0, 1.5, 2.0, 3.0))),
        ("delta only {1..5}", (1, 2, 3, 4), delta_only((1.0, 2.0, 3.0, 4.0, 5.0))),
        ("unpushed D24 draft grid", (1, 2, 3, 4, 5), delta_only((0.5, 1.0, 2.0, 3.0))),
    ]
    print()
    print("=" * 86)
    print("GRID SENSITIVITY -- a hand-picked SAMPLE of alternatives, not a bound")
    print("=" * 86)
    print(f"{'grid':<34} {'wins (swap/decl)':<18} {'ties':>5} {'loss':>5} "
          f"{'clause2':>8} {'greedy=OPT':>11}")
    print("-" * 86)
    for label, Bs, Ws in alternatives:
        t = tally(run_grid(Bs, Ws))
        print(f"{label:<34} {t['swap'] + t['decline']:>2} ({t['swap']}/{t['decline']})"
              f"{'':<9} {t['tie']:>5} {t['loss']:>5} {t['clause2']:>4}/{t['n']:<3} "
              f"{t['greedy_opt']:>6}/{t['n']}")
    print()
    print("The win/tie split moves with the grid. Losses stay at zero wherever greedy")
    print("is optimal, which is a property of this small instance, not of the grid.")
