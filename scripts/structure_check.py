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
def F_current(x):
    a,b,c,d,e = W
    return (a*coverage(x) + b*early_current(x) + c*critprot_current(x)
            - d*risk_current(x) - e*cost(x))
def F_proposed(x):
    a,b,c,d,e = W
    return (a*coverage(x) + b*early_proposed(x) + c*critprot_proposed(x)
            - d*risk_proposed(x) - e*(cost(x)/B))

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

print("=" * 66)
print("COMPONENT-LEVEL STRUCTURE")
print("=" * 66)
comps = [
    ("Coverage",            coverage),
    ("Early  (CURRENT,mean)", early_current),
    ("Early  (PROPOSED,/|P|)", early_proposed),
    ("CritProt (CURRENT)",   critprot_current),
    ("CritProt (PROPOSED)",  critprot_proposed),
    ("Risk (CURRENT,sum)",   risk_current),
    ("Risk (PROPOSED,/B)",   risk_proposed),
    ("Cost",                 cost),
]
for nm, f in comps:
    m = test_monotone(f); s = test_submodular(f)
    print(f"{nm:<24} monotone={'YES' if not m else 'NO ('+str(len(m))+' viol)':<14} "
          f"submodular={'YES' if not s else 'NO ('+str(len(s))+' viol)'}")

print()
print("=" * 66)
print("FULL OBJECTIVE F(x)")
print("=" * 66)
for nm, f in [("F CURRENT", F_current), ("F PROPOSED", F_proposed)]:
    m = test_monotone(f); s = test_submodular(f)
    print(f"{nm:<12} monotone={'YES' if not m else 'NO ('+str(len(m))+')':<10} "
          f"submodular={'YES' if not s else 'NO ('+str(len(s))+')'}")
    if s:
        A, Bs, e, gA, gB = s[0]
        print(f"   counterexample: A={sorted(names[i] for i in A)}")
        print(f"                   B={sorted(names[i] for i in Bs)}")
        print(f"                   adding {names[e]}: gain(A)={gA} < gain(B)={gB}")

print()
print("NOTE: monotonicity of F is NOT required for the greedy guarantee when")
print("cost/risk are subtracted; the guarantee applies to the monotone")
print("submodular COVERAGE part under a cardinality constraint. Reported for")
print("completeness -- what matters is whether the gain-value part is")
print("monotone submodular and whether the penalties are modular.")

# ---------- what the objective actually picks ----------
print()
print("=" * 66)
print(f"EXHAUSTIVE OPTIMUM  (budget B={B})")
print("=" * 66)
for nm, f in [("CURRENT", F_current), ("PROPOSED", F_proposed)]:
    feas = [A for A in ALL if len(A) <= B]
    best = max(feas, key=f)
    h = _intercepted_paths(best, paths)
    print(f"{nm:<9} x*={sorted(names[i] for i in best)}")
    print(f"          F={f(best):.4f}  Coverage={coverage(best):.2f}  "
          f"paths_hit={sorted(paths[i]['name'] for i in h)}")
