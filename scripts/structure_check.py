"""
Empirical structural test of F(x): monotonicity and submodularity,
for the CURRENT objective and the PROPOSED one (iteration-13 candidate).

|L| = 5 so all 32 subsets enumerate instantly. No approximation, no sampling.
"""
import sys, itertools
sys.path.insert(0, '.')
from src.graph_model import load_graph, compute_criticality, load_candidate_locations, load_attack_paths
from src.optimizer.metrics import _intercepted_paths

g = load_graph()
crit = compute_criticality(g)
cands = load_candidate_locations()
paths = load_attack_paths()

import sqlite3
L = list(cands)
_c = sqlite3.connect("data/deception_placement.db")
RISK = {r[0]: (r[1] or 0.0) for r in
        _c.execute("SELECT asset_id, detectability_risk FROM candidate_locations")}
CRIT = {k: v["criticality"] for k, v in crit.items()}
TOTAL_CRIT = sum(CRIT.values())
TARGET_CRIT = sum(CRIT[p["asset_sequence"][-1]] for p in paths)
NP = len(paths)
B = 3

names = {n: d["name"] for n, d in g.nodes(data=True)}

# ---------- components ----------
def coverage(x):
    return len(_intercepted_paths(x, paths)) / NP

def early_current(x):                      # mean over INTERCEPTED paths
    h = _intercepted_paths(x, paths)
    if not h: return 0.0
    return sum(1 - (s / paths[i]["length"]) for i, s in h.items()) / len(h)

def early_proposed(x):                     # denominator fixed at |P|
    h = _intercepted_paths(x, paths)
    return sum(1 - (s / paths[i]["length"]) for i, s in h.items()) / NP

def critprot_current(x):                   # normalised by ALL asset criticality
    h = _intercepted_paths(x, paths)
    return sum(CRIT[paths[i]["asset_sequence"][-1]] for i in h) / TOTAL_CRIT

def critprot_proposed(x):                  # normalised by PATH TARGET criticality
    h = _intercepted_paths(x, paths)
    return sum(CRIT[paths[i]["asset_sequence"][-1]] for i in h) / TARGET_CRIT

def risk_current(x):  return sum(RISK[l] for l in x)          # unnormalised sum
def risk_proposed(x): return sum(RISK[l] for l in x) / B      # bounded, modular
def cost(x):          return len(x)

W = (1.0, 1.0, 1.0, 1.0, 0.1)

# F_pre_d20 is the SUPERSEDED objective, kept so the before/after is
# reproducible rather than merely asserted in D20. F_current is what
# src/optimizer/metrics.py actually computes today.
def F_pre_d20(x):
    a,b,c,d,e = W
    return (a*coverage(x) + b*early_current(x) + c*critprot_current(x)
            - d*risk_current(x) - e*cost(x))
def F_current(x):
    a,b,c,d,e = W
    return (a*coverage(x) + b*early_proposed(x) + c*critprot_proposed(x)
            - d*risk_proposed(x) - e*(cost(x)/B))

# ---------- the aggregates the Harshaw et al. guarantee is stated over ----------
# The guarantee is for f = g - c. Its preconditions are properties of the
# AGGREGATE g and the AGGREGATE c, not of the individual components. Non-negative
# weighted sums of monotone submodular functions are monotone submodular, so the
# component results imply the aggregate ones — but this script can verify the
# actual preconditions directly instead of relying on that argument, so it does.
def g_current(x):
    a,b,c,_,_ = W
    return a*coverage(x) + b*early_proposed(x) + c*critprot_proposed(x)

def c_current(x):
    _,_,_,d,e = W
    return d*risk_proposed(x) + e*(cost(x)/B)

# ---------- structural tests ----------
def subsets(items):
    for r in range(len(items)+1):
        for c in itertools.combinations(items, r):
            yield frozenset(c)

ALL = list(subsets(L))

def test_monotone(f):
    bad = []
    for A in ALL:
        for e in L:
            if e in A: continue
            if f(A | {e}) < f(A) - 1e-12:
                bad.append((set(A), e, round(f(A),4), round(f(A|{e}),4)))
    return bad

def test_submodular(f):
    bad = []
    for A in ALL:
        for Bs in ALL:
            if not A <= Bs: continue
            for e in L:
                if e in Bs: continue
                gA = f(A | {e}) - f(A)
                gB = f(Bs | {e}) - f(Bs)
                if gA < gB - 1e-12:
                    bad.append((set(A), set(Bs), e, round(gA,4), round(gB,4)))
    return bad


def test_modular(f):
    """MODULARITY, not submodularity. The Harshaw et al. precondition on the cost
    part is that c is modular — f(A|{e}) - f(A) must be the SAME for every A, so
    the marginal cost of an element is independent of what is already placed.
    Submodularity alone is insufficient: a strictly submodular c would break the
    result. Tested as equality of marginals against the empty-set marginal."""
    bad = []
    for e in L:
        base = f(frozenset({e})) - f(frozenset())
        for A in ALL:
            if e in A: continue
            if abs((f(A | {e}) - f(A)) - base) > 1e-12:
                bad.append((set(A), e, round(base,6), round(f(A | {e}) - f(A),6)))
    return bad

print("=" * 66)
print("COMPONENT-LEVEL STRUCTURE")
print("=" * 66)
comps = [
    ("Coverage",              coverage),
    ("Early (PRE-D20, mean)", early_current),
    ("Early (LIVE, /|P|)",    early_proposed),
    ("CritProt (PRE-D20)",    critprot_current),
    ("CritProt (LIVE)",       critprot_proposed),
    ("Risk (PRE-D20, sum)",   risk_current),
    ("Risk (LIVE, /B)",       risk_proposed),
    ("Cost",                  cost),
]
for nm, f in comps:
    m = test_monotone(f); s = test_submodular(f)
    print(f"{nm:<24} monotone={'YES' if not m else 'NO ('+str(len(m))+' viol)':<14} "
          f"submodular={'YES' if not s else 'NO ('+str(len(s))+' viol)'}")

print()
print("=" * 66)
print("FULL OBJECTIVE F(x)")
print("=" * 66)
for nm, f in [("F PRE-D20 (superseded)", F_pre_d20), ("F CURRENT (live)", F_current)]:
    m = test_monotone(f); s = test_submodular(f)
    print(f"{nm:<24} monotone={'YES' if not m else 'NO ('+str(len(m))+')':<10} "
          f"submodular={'YES' if not s else 'NO ('+str(len(s))+')'}")
    if s:
        A, Bs, e, gA, gB = s[0]
        print(f"   counterexample: A={sorted(names[i] for i in A)}")
        print(f"                   B={sorted(names[i] for i in Bs)}")
        print(f"                   adding {names[e]}: gain(A)={gA} < gain(B)={gB}")

print()
print("=" * 66)
print("GUARANTEE PRECONDITIONS  (f = g - c, Harshaw et al. 2019, sources.md #353)")
print("=" * 66)
gm, gs = test_monotone(g_current), test_submodular(g_current)
g_nonneg = all(g_current(A) >= -1e-12 for A in ALL)
print(f"{'g = a*Cov + b*Early + c*CritProt':<34} "
      f"monotone={'YES' if not gm else 'NO ('+str(len(gm))+')':<10} "
      f"submodular={'YES' if not gs else 'NO ('+str(len(gs))+')':<12} "
      f"non-negative={'YES' if g_nonneg else 'NO'}")
cmod = test_modular(c_current)
c_nonneg = all(c_current(A) >= -1e-12 for A in ALL)
print(f"{'c = d*Risk + e*Cost':<34} "
      f"modular={'YES' if not cmod else 'NO ('+str(len(cmod))+')':<11} "
      f"{'':<23} non-negative={'YES' if c_nonneg else 'NO'}")
_ok = (not gm) and (not gs) and g_nonneg and (not cmod) and c_nonneg
print()
print(f"  ==> preconditions {'ALL SATISFIED' if _ok else 'NOT satisfied'} on this instance"
      f"{' -- gamma = 1, bound (1 - 1/e) ~ 0.632' if _ok else ''}")

print()
print("READ THIS BEFORE CITING ANY GUARANTEE.")
print("F(x) itself is submodular but NOT monotone, and necessarily so, since")
print("Risk and Cost are subtracted. The classical (1-1/e) bound requires")
print("MONOTONE submodularity, so it does not apply to F(x) -- and it does not")
print("apply to plain greedy on F(x) either. The same source's Appendix A,")
print("'Greedy Performs Arbitrarily Poorly', constructs an instance where")
print("standard greedy's ratio is unbounded.")
print()
print("What the guarantee attaches to is DISTORTED GREEDY")
print("(src/optimizer/baselines.py: distorted_greedy) applied to f = g - c, with")
print("the preconditions above holding: g monotone submodular and non-negative,")
print("c modular and non-negative. Then g(S) - c(S) >= (1 - e^-gamma)g(OPT) -")
print("c(OPT). Plain greedy is still reported as the primary method because it")
print("is the standard practitioner heuristic and the MILP validates it exactly")
print("at this scale -- but it carries NO approximation guarantee. Do not")
print("transfer the distorted-greedy bound to it. See formal-problem-definition")
print("section 7 and D23.")

# ---------- what the objective actually picks ----------
print()
print("=" * 66)
print(f"EXHAUSTIVE OPTIMUM  (budget B={B})")
print("=" * 66)
for nm, f in [("PRE-D20", F_pre_d20), ("LIVE", F_current)]:
    feas = [A for A in ALL if len(A) <= B]
    best = max(feas, key=f)
    h = _intercepted_paths(best, paths)
    print(f"{nm:<9} x*={sorted(names[i] for i in best)}")
    print(f"          F={f(best):.4f}  Coverage={coverage(best):.2f}  "
          f"paths_hit={sorted(paths[i]['name'] for i in h)}")
