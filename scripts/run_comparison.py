import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sqlite3

from src.graph_model import load_graph, compute_criticality, load_candidate_locations, load_attack_paths
from src.optimizer.baselines import greedy, random_baseline, centrality_baseline, distorted_greedy
from src.optimizer.milp import solve_milp
from src.optimizer.metrics import NORMALISER_K

g = load_graph()
crit = compute_criticality(g)
candidates = load_candidate_locations()
paths = load_attack_paths()
central_scores = {n: crit[n]["central"] for n in crit}
names = {n: crit[n]["name"] for n in crit}

detectability = {}
conn = sqlite3.connect(Path(__file__).resolve().parents[1] / "data" / "deception_placement.db")
for row in conn.execute("SELECT asset_id, detectability_risk FROM candidate_locations"):
    detectability[row[0]] = row[1] or 0.0
conn.close()

print(f"Candidate locations (L): {[names[c] for c in candidates]}")
print(f"Attack paths (P): {[p['name'] for p in paths]}\n")

BUDGET = int(sys.argv[1]) if len(sys.argv) > 1 else 3   # D24: was 2; 3 is the headline budget reported in README
WEIGHTS = (1.0, 1.0, 1.0, 1.0, 0.1)

x_g, m_g = greedy(candidates, paths, crit, detectability, BUDGET, WEIGHTS)
x_d, m_d = distorted_greedy(candidates, paths, crit, detectability, BUDGET, WEIGHTS)
placements_r, results_r, summary_r = random_baseline(candidates, paths, crit, detectability, BUDGET, WEIGHTS)
x_c, m_c = centrality_baseline(candidates, central_scores, paths, crit, detectability, BUDGET, WEIGHTS)
x_m, m_m, milp_info = solve_milp(candidates, paths, crit, detectability, BUDGET, WEIGHTS)

def fmt(x): return sorted(names[a] for a in x)

print(f"Budget B = {BUDGET}, weights (a,b,g,d,e) = {WEIGHTS}")
print(f"Risk and Cost are divided by the fixed K = {NORMALISER_K}, not by B (D25)"
      f"{' -- B exceeds K, so they can exceed 1 here' if BUDGET > NORMALISER_K else ''}\n")

for label, x, m in [("GREEDY (proposed, primary)", x_g, m_g),
                    ("DISTORTED GREEDY (guaranteed)", x_d, m_d),
                    ("MILP (exact validation)", x_m, m_m),
                    ("CENTRALITY (baseline)", x_c, m_c)]:
    print(f"=== {label} ===")
    print(f"Placement: {fmt(x)}")
    print(f"F(x)={m.f_score:.4f}  Coverage={m.coverage:.2f}  Early={m.early:.2f}  "
          f"CritProt={m.crit_prot:.2f}  Risk={m.risk:.2f}  Cost={m.cost}\n")

print(f"=== RANDOM (30 trials) ===")
print(f"Mean F(x)={summary_r['mean_f']:.4f}  Std={summary_r['std_f']:.4f}\n")

# ---------------------------------------------------------------------------
# Optimality gap, WITH the guard that D16 should have installed and did not.
# The MILP is exact. Its F(x) can therefore never fall below any heuristic's.
# When it did, nothing here objected: the script printed a negative number and
# stayed silent, and the defect survived until D24. A violated invariant must
# fail loudly, not print quietly.
# ---------------------------------------------------------------------------
gap_abs = m_m.f_score - m_g.f_score
print("=== Optimality gap: greedy vs MILP ===")
if gap_abs < -1e-9:
    print(f"MILP F(x) - Greedy F(x) = {gap_abs:.4f}")
    raise SystemExit(
        "INVARIANT VIOLATED: the exact MILP scored BELOW greedy. An exact solver "
        "cannot be beaten by a heuristic on the same objective, so the solver's "
        "linearisation no longer matches metrics.score -- they are optimising "
        "different functions. Do not interpret any result from this run. This is "
        "the D16/D24 failure mode; check the objective coefficients in "
        "src/optimizer/milp.py against src/optimizer/metrics.py first.")
rel = (gap_abs / abs(m_m.f_score) * 100) if abs(m_m.f_score) > 1e-12 else 0.0
print(f"MILP F(x) - Greedy F(x) = {gap_abs:.4f}  ({rel:.2f}% of MILP optimum)")
if abs(gap_abs) < 1e-9:
    print("Greedy matched the exact optimum on this instance (0.00% gap).")

# Distorted greedy carries the only worst-case guarantee, and is expected to be
# more conservative than plain greedy here -- reported, not hidden. See D23.
d_gap = m_m.f_score - m_d.f_score
d_rel = (d_gap / abs(m_m.f_score) * 100) if abs(m_m.f_score) > 1e-12 else 0.0
print(f"MILP F(x) - DistortedGreedy F(x) = {d_gap:.4f}  ({d_rel:.2f}% of MILP optimum)")
if d_gap > 1e-9:
    print("  Expected: the distortion factor forfeits early iterations by design.")
    print("  (1-1/e) ~ 0.632 is a worst-case floor, not a promise of matching greedy.")

print(f"\n{'Method':<30} {'F(x)':>8}")
print(f"{'Greedy (proposed, primary)':<30} {m_g.f_score:>8.4f}")
print(f"{'Distorted greedy (guaranteed)':<30} {m_d.f_score:>8.4f}")
print(f"{'MILP (exact validation)':<30} {m_m.f_score:>8.4f}")
print(f"{'Centrality':<30} {m_c.f_score:>8.4f}")
print(f"{'Random (mean)':<30} {summary_r['mean_f']:>8.4f}")
