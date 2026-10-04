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
code. It is now a constant here; under D24's objective it reproduced D22a's
9 / 11 / 0 exactly. D25 changed how Risk and Cost are normalised (a fixed
constant instead of the budget), and on the same grid the record is now
5 wins / 15 ties / 0 losses. The grid constants themselves are unchanged.

WHY IT MOVED INTO CODE. An earlier draft of D24 — never pushed, caught when the
patch was reviewed before being applied — rewrote the README section holding
the grid without recognising that line as its definition, concluded that no
grid had ever been recorded, and substituted a delta-only grid over B = 1..5
that reported a more favourable 13 / 7 / 0 (under D24's objective; 8 / 12 / 0
under D25's). A definition that can be deleted by
editing prose is too fragile for an evaluation input. Do not change the
constants below without a decisions-log entry stating the effect on every
quoted number, per the evaluation-integrity rule.

WHAT THE RECORD MEANS — read before quoting it. The win/tie count alone
misleads, so this script reports what it is made of:

  * Greedy equals the exhaustive optimum in every cell of the declared grid.
    On this instance it therefore cannot score lower on F than any other
    placement: "0 losses" is IMPLIED BY OPTIMALITY. It is not evidence that F
    is a good objective, because F is both what is maximised and the yardstick.
    And on the legacy D25 candidate set it is not evidence of search quality
    either: every path meets exactly one candidate, so the gain part g is
    modular and greedy is optimal BY CONSTRUCTION (D25). The script tests this
    and says so; that check is D25's claim rule in code.

  * Wins come in two kinds. A SWAP places as many decoys as the baseline but
    different ones. A DECLINE places fewer. They are different claims and are
    counted separately.

  * The primary research question's second clause (formal-problem-definition
    §8: equal or greater Coverage and CritProt at equal or lower Cost) is
    checked cell by cell against the centrality baseline. Under D20-D24's
    normalisation it failed in exactly the 4 cells where greedy declined. On
    this grid those declines existed only because dividing Risk and Cost by a
    budget below 4 inflated every decoy's penalty (D25); with the fixed divisor
    no declared cell declines, and the clause holds in all 20. That is a change
    in the objective, not an improvement in the method — read D25 before
    quoting it. Declines do still occur at higher delta (see --sens).

How these facts are framed in the thesis is A12's decision, not this script's.

Run:  python scripts/sweep.py          the declared grid
      python scripts/sweep.py --sens   plus a labelled sample of alternative grids
"""
import sys
import itertools
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.graph_model import (load_graph, compute_criticality, load_attack_paths,
                             candidates_or_exit, legacy_flag)
from src.optimizer.baselines import greedy, centrality_baseline, distorted_greedy
from src.optimizer.milp import solve_milp, SCALE
from src.optimizer.metrics import score, NORMALISER_K

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

# D25: Risk and Cost are divided by the FROZEN constant NORMALISER_K. It is not
# re-derived from this grid: if it were, extending BUDGETS would rescale every
# decoy's penalty and move the budget confound D25 removed from the run to the
# grid. A budget above K only lets Risk and Cost exceed 1, which the header
# below reports.

TOL = 1e-9
ROOT = Path(__file__).resolve().parents[1]
g = load_graph()
crit = compute_criticality(g)
LEGACY = legacy_flag(sys.argv)          # D26
candidates = candidates_or_exit(allow_legacy=LEGACY)
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
    without trusting either the solver or the heuristic. Also returns the best
    STRICTLY worse value, so the MILP's rounding margin can be checked (D25)."""
    values = set()
    for r in range(budget + 1):
        for c in itertools.combinations(L, r):
            values.add(round(score(set(c), paths, crit, detectability, weights).f_score, 12))
    ranked = sorted(values, reverse=True)
    return ranked[0], (ranked[1] if len(ranked) > 1 else None)


def gain_structure():
    """D25's claim rule, checked in code. If the gain part g is MODULAR on this
    candidate set, a placement's gain is a plain sum of per-site gains, so
    F = g - c is modular too and greedy is optimal BY CONSTRUCTION: agreement
    with the exact optimum then validates the implementation, not the search
    method. Two views of the same property: the structural cause (paths meeting
    two or more candidates) and an exhaustive modularity test of g itself."""
    shared = [p["name"] for p in paths if sum(a in L for a in set(p["asset_sequence"])) >= 2]

    def g(S):
        m = score(set(S), paths, crit, detectability, (1.0, 1.0, 1.0, 0.0, 0.0))
        return m.coverage + m.early + m.crit_prot

    violations = 0
    for e in L:
        base = g({e}) - g(set())
        for r in range(len(L)):
            for A in itertools.combinations([l for l in L if l != e], r):
                if abs((g(set(A) | {e}) - g(A)) - base) > 1e-12:
                    violations += 1
    return shared, violations


def evaluate_cell(B, W):
    xg, mg = greedy(L, paths, crit, detectability, B, W)
    xc, mc = centrality_baseline(L, central_scores, paths, crit, detectability, B, W)
    _, md = distorted_greedy(L, paths, crit, detectability, B, W)
    _, mm, _info = solve_milp(L, paths, crit, detectability, B, W)
    truth, runner_up = exhaustive_best(W, B)

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
        # gap between the optimum and the best strictly-worse placement, in the
        # MILP's integer units: rounding cannot flip the two while this exceeds
        # the rounding bound printed below (D24, re-measured in D25)
        "margin": (truth - runner_up) * SCALE if runner_up is not None else float("inf"),
        "W": W,
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
        "min_margin": min(((c["margin"], c["B"], name) for name, c in cells), default=None),
    }


def rounding_bound(budget):
    """Upper bound on how far CP-SAT's integer rounding can move the comparison
    of two placements: one placement's objective sums at most 3|P| + B rounded
    coefficients (coverage, CritProt and one earliness term per intercepted
    path, one penalty per placed decoy), each off by at most half a unit."""
    return 3 * len(paths) + budget


cells = run_grid(BUDGETS, WEIGHTINGS)
T = tally(cells)
n = T["n"]

print("=" * 86)
print("DECLARED GRID  (README since D20; code since D24)")
print("=" * 86)
print(f"budgets B = {list(BUDGETS)}")
for k, w in WEIGHTINGS.items():
    print(f"  {k:<8} (alpha, beta, gamma, delta, epsilon) = {w}")
print(f"Risk and Cost divided by the frozen K = {NORMALISER_K} (D25), not by the budget"
      f"{'; B > K here, so they can exceed 1' if max(BUDGETS) > NORMALISER_K else ''}")
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
    print("  => '0 losses' is implied by optimality on this instance, so it says nothing")
    print("     about the value of the objective. What it says about the search depends")
    print("     on the next line.")
shared_paths, g_viol = gain_structure()
print(f"gain part g on this candidate set: "
      f"{'MODULAR' if g_viol == 0 else 'NOT modular (' + str(g_viol) + ' violations)'}; "
      f"paths meeting 2+ candidates: {len(shared_paths)} of {len(paths)}"
      f"{' (' + ', '.join(shared_paths) + ')' if shared_paths else ''}")
if g_viol == 0:
    print("  => D25 claim rule: greedy is optimal BY CONSTRUCTION here. Agreement with the")
    print("     exact optimum validates the implementation, not the search method, and")
    print("     supports no claim about search quality.")
else:
    print("  => D25 claim rule: the instance is non-trivial, so greedy matching the optimum")
    print("     is a finding -- but for one small instance only. Broader search-quality")
    print("     claims need a family of instances (A12).")
print()
print(f"RQ clause 2 vs centrality (Coverage >=, CritProt >=, Cost <=): holds in "
      f"{T['clause2']} of {n}, fails in {len(fails)}")
if fails:
    print("  fails at: " + ", ".join(f"B={c['B']} {name}" for name, c in fails))
    print(f"  every failure is a decline: {'YES' if fails_are_declines else 'NO'}")
if g_viol == 0:
    # D25: with a modular gain part each decoy's value is fixed, so the delta at
    # which it turns negative (and starts being declined) can be computed
    # exactly. Report how close the grid sits to the nearest such threshold:
    # a clause-2 or no-decline result that a slightly larger delta would
    # overturn must not be quoted as robust.
    closest = None
    for wname, (a, b, c, d, e) in WEIGHTINGS.items():
        for l in L:
            m = score({l}, paths, crit, detectability, (a, b, c, d, e))
            gain = a * m.coverage + b * m.early + c * m.crit_prot
            r = detectability.get(l, 0.0)
            if gain <= 0 or r <= 0:
                continue  # never worth placing, or never penalised through delta
            thr = (NORMALISER_K * gain - e) / r
            if thr > d and (closest is None or (thr - d) / d < closest[0]):
                closest = ((thr - d) / d, wname, d, names[l], thr)
    if closest:
        rel, wname, d, who, thr = closest
        print(f"  nearest decline threshold: under '{wname}' (delta={d:g}), {who} turns "
              f"negative at delta={thr:.3f}, {100 * rel:.1f}% higher.")
        print("  (D25: quote the clause-2 result only together with this line.)")
print()
print(f"MILP vs exhaustive optimum: "
      f"{'exact in all ' + str(n) if T['milp_exact'] == n else str(n - T['milp_exact']) + ' MISMATCHES'}")
if T["milp_exact"] != n:
    raise SystemExit(
        "INVARIANT VIOLATED: the exact MILP disagrees with exhaustive enumeration. "
        "Its linearisation no longer matches metrics.score. Do not interpret these "
        "results; see D16 and D24.")
mg_units, mg_B, mg_name = T["min_margin"]
bound = rounding_bound(max(BUDGETS))
print(f"smallest rounding margin: {mg_units:,.0f} units (B={mg_B} {mg_name}); "
      f"rounding can move a comparison by at most {bound} units")
if mg_units <= bound:
    raise SystemExit(
        "INVARIANT VIOLATED: the gap between the optimum and the next-best placement "
        "is within the MILP's rounding bound, so its exactness here is luck. Raise "
        "SCALE in src/optimizer/milp.py; see D24.")
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
        # B=5 exceeds NORMALISER_K, so Risk and Cost can exceed 1 in this row only.
        # Kept because D24 records this grid as the near-miss; it is a sample.
        ("unpushed D24 draft grid", (1, 2, 3, 4, 5), delta_only((0.5, 1.0, 2.0, 3.0))),
    ]
    print()
    print("=" * 86)
    print("GRID SENSITIVITY -- a hand-picked SAMPLE of alternatives, not a bound")
    print("=" * 86)
    print(f"{'grid':<34} {'wins (swap/decl)':<18} {'ties':>5} {'loss':>5} "
          f"{'clause2':>8} {'greedy=OPT':>11}")
    print("-" * 86)
    distinct = {}
    for label, Bs, Ws in alternatives:
        sample = run_grid(Bs, Ws)
        for _, c in sample:
            distinct[(c["B"], c["W"])] = c
        t = tally(sample)
        print(f"{label:<34} {t['swap'] + t['decline']:>2} ({t['swap']}/{t['decline']})"
              f"{'':<9} {t['tie']:>5} {t['loss']:>5} {t['clause2']:>4}/{t['n']:<3} "
              f"{t['greedy_opt']:>6}/{t['n']}")
    print()
    # The same MILP guard as the declared grid, applied to every distinct sample
    # configuration: D25 quotes these, so they are asserted, not just tallied.
    bad = [k for k, c in distinct.items() if not c["milp_exact"]]
    worst = min(distinct.values(), key=lambda c: c["margin"])
    wb = rounding_bound(max(b for b, _ in distinct))
    print(f"MILP vs exhaustive optimum across the {len(distinct)} distinct sample "
          f"configurations: {'exact in all' if not bad else str(len(bad)) + ' MISMATCHES'}")
    print(f"smallest rounding margin in the sample: {worst['margin']:,.0f} units "
          f"(B={worst['B']}, weights {worst['W']}); bound {wb} units")
    if bad or worst["margin"] <= wb:
        raise SystemExit("INVARIANT VIOLATED in the sensitivity sample: see D24 and D25.")
    print()
    print("The win/tie split moves with the grid. Losses stay at zero wherever greedy")
    print("is optimal, which is a property of this small instance, not of the grid.")
