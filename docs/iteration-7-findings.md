# Iteration 7 Findings — OT/ICS Deception Placement Optimization

Builds on iterations 1–6. Does not repeat those conclusions — see `sources.md` for the running source log. Source numbers below refer to that file (iteration 7 = #283–286).

Shorter than previous iterations, and worth saying plainly why: most of this round's search budget went to identifying two specific names from iteration 5's citation-list scan, which is bookkeeping work, not discovery. The one genuinely new item is a strong citation, not a new methodological direction.

## 1. Two more names from the citation list, resolved as far as they'll go

"Udupa et al., 2024" is now fully identified: **"Reactive Synthesis of Sensor Revealing Strategies in Hypergames on Graphs"** [283], a University of Florida / Army Research Lab paper about deceiving attackers on whether a sensor exists at all, not about decoy or honeypot placement. It's adjacent to your project's theme (deception, graphs, the same research ecosystem) but a genuinely different sub-problem — worth knowing about, not worth citing as competing work.

"Wan et al., 2023" probably refers to a hypergame-theoretic paper about defending against multiple simultaneous APT attackers [284] — the topic matches what other papers say about it, but I couldn't independently confirm the author list this round, so treat it as probable rather than settled if you plan to cite it directly.

"Jia et al., 2024" and "Shen et al., 2025" stayed unresolved. They've now shown up as bare citations — never as their own page — across six-plus different papers checked over two iterations. That pattern is itself the answer, the same way it was for the centrality/lateral-movement paper in iteration 6: these are two more items that need a different access route (a citation database, or the citing papers' own reference-list DOIs) rather than more general web search.

## 2. A strong new citation for the criticality term

Joint 2025 guidance from CISA, the FBI, and the UK's NCSC states plainly that every OT asset should be scored on **three factors: criticality, exposure, and availability** [286]. This doesn't hand you a formula — it's not that specific — but it's about as authoritative a source as exists for the claim that criticality-weighted asset scoring is the right thing to be doing in OT security, which is a different and useful role than the two computational approaches already on file. Iteration 5 gave you the IEC 62443 SL-vector route and iteration 6 gave you the locality/centrality/damage patent formula, both answering *how* to compute criticality. This answers *why it matters*, from a source your thesis committee will recognize immediately. Worth opening your criticality-term justification with this citation, then dropping into one or both of the computational methods for the actual mechanics.

## Still open

- Jia et al. 2024 and Shen et al. 2025 — same diagnosis as the centrality paper: try a citation database (Google Scholar's own citing-papers view, or Semantic Scholar's API) rather than general web search.
- Wan et al. 2023's exact identity still wants direct confirmation.
- No new thread opened this round — everything above closes something from iteration 5 or 6 rather than surfacing new territory.

## Candidates for iteration 8

Seven iterations in, this round's yield was the thinnest yet: one clean resolution, one probable resolution, two confirmed dead ends, and one strong citation with no new direction attached. Worth noticing, not worth a long comment — the numbers speak for themselves here more than they have in past iterations. If iteration 8 goes the same way, the sources file at that point is genuinely a solid foundation for section 14, and further iterations would be picking at diminishing bookkeeping items rather than changing the picture.
