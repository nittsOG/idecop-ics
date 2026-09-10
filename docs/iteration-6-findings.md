# Iteration 6 Findings — OT/ICS Deception Placement Optimization

Builds on iterations 1–5. Does not repeat those conclusions — see `sources.md` for the running source log. Source numbers below refer to that file (iteration 6 = #276–282).

This iteration closed out the centrality/lateral-movement thread definitively, spot-checked the newly surfaced 2024–2025 cluster papers, and took one more pass at the IEC 62443 criticality question.

## 1. The centrality/lateral-movement paper — closed, not resolved

Three iterations (3, 4, 6) have now tried to find a direct link to "Decoy Allocation Against Lateral Movement: A Network Centrality Game Approach." The venue is confirmed a second independent way — IEEE Trans. Netw. Serv. Manag., 2026, Kamhoua as author [276] — and the partial abstract is consistent with what iteration 3 found. But there is no open-access preprint, no arXiv mirror, no publisher page reachable without a subscription. That consistency across three separate search attempts is itself the answer: this paper simply isn't available outside IEEE Xplore. Chasing it with more web searches in iteration 7 would waste a search budget on something already diagnosed. If you want it, pull it through your NFSU library's IEEE Xplore access — that's a five-minute task for you and an unbounded one for open web search.

One adjacent find while looking: a second, unrelated 2026 paper from the same author, **"Coordinated Multi-Domain Deception: A Stackelberg Game Approach"** [277], also IEEE TNSM 2026. Same access situation — flagging its existence, not pursuing it further this round.

## 2. A different way to frame "placement" — worth knowing even if you don't use it

Spot-checking the wider cluster surfaced a paper that frames the placement problem completely differently from everything else catalogued so far [278]: instead of optimizing which nodes a decoy should sit at to intercept attack paths, it optimizes how to **blend** decoys into a set of real production hosts so they're computationally hard to distinguish, formally proving the problem's hardness via a reduction from Subset Product.

This matters for your project in one specific way: coverage-optimal placement and blending-optimal placement can disagree. A node that's excellent for attack-path coverage might be a terrible blending choice (too visible, wrong IP-range context, doesn't match the traffic profile of its neighbors) — which ties directly back to iteration 4's honeypot-detectability finding. You don't need to solve the blending problem too, but your problem formulation should say explicitly that you're optimizing coverage subject to a *baseline* plausibility/blending constraint (citing the "Decoys Cannot Go Everywhere" rubric and this paper), rather than letting a reader wonder whether you've conflated the two.

## 3. A genuine, worked formula for OT asset criticality

This is the best find this iteration, and it's independent of iteration 5's IEC 62443 SL-vector route. A patent on attack-graph criticality analysis [282] lays out an actual equation: **criticality is a function of locality, centrality, and damage**, where locality is the asset's Purdue level, centrality is a network-connectivity measure (their example uses bytes exchanged with other assets), and damage is the fraction of operational load the asset controls. The patent works a full numeric example on an OT/SCADA asset, arriving at a single criticality score.

You now have two legitimate, independent ways to justify the criticality term in your composite objective: the IEC 62443 SL-vector route (standards-based, iteration 5) and this locality/centrality/damage formula (graph-and-operations-based, this iteration). They're not competing — you could reasonably cite both and note that one captures *required* protection level while the other captures *actual* network and operational importance, and a defensible criticality score probably wants to reflect both.

## 4. Cluster bibliography — confirmed, not expanded

The other 2024–2025 papers flagged in iteration 5 ([274]'s Kulkarni 2024, Shen 2025, Jia 2024, Udupa 2024) didn't individually surface this round — instead, search kept returning the same handful of papers already catalogued (Hawkeyes, now with its full venue confirmed as *Computer Networks* [280]; a live-deployment cognitive-honeypot system, CogniTrap [281]) plus a third treatment of the probabilistic-attack-graph line as a 2025 book chapter [279]. None of this changes the picture — still zero OT-structured placement work from this cluster, six iterations in.

## Still open

- The individual 2024–2025 papers named in iteration 5's bibliography scan (Kulkarni 2024, Shen 2025, Jia 2024, Udupa 2024, Wan 2023) still haven't been checked one by one — general searches keep surfacing already-known papers instead.
- Whether any paper combines *both* an SL-vector-style standards input and a locality/centrality/damage-style graph input into one criticality score — worth checking before assuming you're the first to combine them.

## Candidates for iteration 7 — or a scope decision

Two threads that were "still open" are now explicitly closed as needing offline/institutional access rather than more search (the centrality paper, and by extension its sibling). Combined with iteration 5's observation that returns were narrowing, this is a natural point to name the choice directly: iteration 7 could either (a) do a narrow, specific pass on the handful of individually-unchecked 2024–2025 papers, or (b) stop widening and start drafting section 14 of your brief using the six iterations of `sources.md` now on hand, coming back to fill specific citation gaps only as the draft actually needs them. Both are reasonable — but the second is very likely the better use of weekend hours at this point, since the last two iterations combined have surfaced one genuinely new competing-methodology paper and two useful-but-adjacent formulas, not any change to the core novelty picture.
