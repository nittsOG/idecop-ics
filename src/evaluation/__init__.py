"""
evaluation — the criteria Phase D judges placements by, other than F (A12; D37).

F is both what the optimiser maximises and, until A12, the only yardstick, so
"greedy never loses on F" follows from greedy being optimal (D24, D25, D31).
This package scores placements on criteria the optimiser never sees:

- holdout.py: leave-one-path-out validation, the guide's K-fold-style request
  (D32). Each path is held out in turn; the placement is chosen from the other
  four and scored on the one it never saw.
- simulation.py: the attack simulation, the guide's simulation request (D32).
  Every route from every non-controller foothold to every objective, through
  the recorded connections, enumerated exactly.
- comparators.py: the coverage-only comparator (D37), which optimises attack-
  path coverage alone, so the evaluation can ask whether F's other four terms
  add anything.

Nothing here changes a method, a weight, K or an input. The methods are called
exactly as scripts/run_comparison.py calls them; leave-one-path-out only hands
them fewer paths. The design and its parameters are fixed in
docs/03-evaluation-methodology.md, before any run on the testbed.
"""
