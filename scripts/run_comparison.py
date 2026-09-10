import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sqlite3

from src.graph_model import load_graph, compute_criticality, load_candidate_locations, load_attack_paths
from src.optimizer.baselines import greedy, random_baseline, centrality_baseline
from src.optimizer.milp import solve_milp

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

BUDGET = 2
WEIGHTS = (1.0, 1.0, 1.0, 1.0, 0.1)

x_g, m_g = greedy(candidates, paths, crit, detectability, BUDGET, WEIGHTS)
placements_r, results_r, summary_r = random_baseline(candidates, paths, crit, detectability, BUDGET, WEIGHTS)
x_c, m_c = centrality_baseline(candidates, central_scores, paths, crit, detectability, BUDGET, WEIGHTS)
x_m, m_m, milp_info = solve_milp(candidates, paths, crit, detectability, BUDGET, WEIGHTS)

def fmt(x): return sorted(names[a] for a in x)

for label, x, m in [("GREEDY (proposed)", x_g, m_g), ("MILP (validation)", x_m, m_m), ("CENTRALITY", x_c, m_c)]:
    print(f"=== {label} ===")
    print(f"Placement: {fmt(x)}")
    print(f"F(x)={m.f_score:.4f}  Coverage={m.coverage:.2f}  Early={m.early:.2f}  "
          f"CritProt={m.crit_prot:.2f}  Risk={m.risk:.2f}  Cost={m.cost}\n")

print(f"=== RANDOM (30 trials) ===")
print(f"Mean F(x)={summary_r['mean_f']:.4f}  Std={summary_r['std_f']:.4f}\n")

gap = m_m.f_score - m_g.f_score
print(f"=== Optimality gap: greedy vs MILP ===")
print(f"MILP F(x) - Greedy F(x) = {gap:.4f}")
if abs(gap) < 1e-9:
    print("Greedy matched the exact optimum on this instance.")

print(f"\n{'Method':<20} {'F(x)':>8}")
print(f"{'Greedy (proposed)':<20} {m_g.f_score:>8.4f}")
print(f"{'MILP (validation)':<20} {m_m.f_score:>8.4f}")
print(f"{'Centrality':<20} {m_c.f_score:>8.4f}")
print(f"{'Random (mean)':<20} {summary_r['mean_f']:>8.4f}")
