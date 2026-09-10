# Iteration 4 Findings — OT/ICS Deception Placement Optimization

Builds on iterations 1–3. Does not repeat those conclusions — see `sources.md` for the running source log. Source numbers below refer to that file (iteration 4 = #250–266).

This iteration worked straight down iteration 3's "still open" list, in order.

## 1. Operational risk / false-positive cost — resolved

This had been open since iteration 2. It's resolved now, and better than expected: [250] (D3O-IIoT) formalizes exactly this term inside a multi-objective RL reward — attack mitigation, deception engagement, false-positive control, and resource cost, all in one function — and then *ablates* it, showing false-positive control is the single most important term in the whole reward (51.4% performance loss when removed). [251] independently confirms the pattern with a simpler utility-function comparison (deployment strategies with vs. without false-positive penalties).

Practical implication for your thesis: you now have two real, citable precedents for treating operational risk as a first-class, heavily-weighted term rather than an afterthought — which validates the composite-objective structure in section 10 of your brief. Neither paper is OT, and neither gives you a ready-made formula to drop in (they're RL rewards and utility functions, not the kind of closed-form term your MILP/greedy formulation needs) — but the *ablation evidence* that this term matters more than you might assume is a strong argument for not treating it as a minor correction in your own weighting/sensitivity analysis.

## 2. The Ma/Han/Kamhoua/Fu discrepancy — resolved

Iteration 3 flagged a bibliographic problem: two near-identical papers, one via arXiv (5 authors including Nandi Leslie, "submission to AAMAS 2023") and one cited by a JHU faculty page as GameSec 2023 (4 authors, no Leslie). Both exist, and they're genuinely different: [252] is the confirmed, published, peer-reviewed GameSec 2023 paper (Springer LNCS 14167, pp. 215–233) — cite this one. The arXiv version only ever claims "submission to AAMAS 2023," with no evidence found that it was accepted there; it looks like an earlier draft that was reworked (title changed from "Decoy Resource" to "Resource," Leslie dropped) before landing at GameSec. Simple fix for your reference list: use [252]'s Springer citation, not the arXiv one.

Chasing the GameSec 2023 program also surfaced [253] and [254] — more of the same cluster, now confirmed to include epidemic-network control and drone-swarm surveillance as *other* domains they've applied deception placement to. That's now five non-OT domains this one small research group has covered (Active Directory, microservices, epidemic networks, tactical/SDN networks, UAV swarms) without touching OT. That's a stronger novelty argument than "no one's done this" — it's "this specific, prolific group works domain-by-domain and hasn't reached OT yet."

## 3. AI-explanation-layer precedent — now has a direct OT bridge

This is the best find this iteration. [255] confirmed the full SPEAR framework behind i-EXAM (iteration 3, #244) — PDDL-based planning, soundness/completeness guarantees, diverse hardening strategies. [256] gives you a real comparable scale (30 nodes) for how these planning tools perform.

But the actual find is [257]: a 2021 Wiley paper that applies the *exact same* PDDL-based automated-planning approach — the same formalism SPEAR/i-EXAM use — specifically to **IT-to-OT attack path discovery**, with a device-reachability graph-partitioning algorithm to handle scale. It isn't about deception, and it isn't your project. But it closes a gap I couldn't close in iteration 3: it shows the planning formalism your AI-explanation layer would sit on top of has already been demonstrated to work on OT-adjacent topologies, by a different group, for a different purpose. You can now cite a direct chain: SPEAR/i-EXAM (planner decides, LLM explains, on IT networks) + Wang et al. (the same planning formalism, applied to OT) → your project (the same planner-explains-decoy-placement pattern, on OT, for deception). That's a much stronger related-work paragraph than citing SPEAR alone.

## 4. Dynamic vs. static placement — a framing choice worth naming explicitly

Not something you asked to check, but it surfaced clearly enough to flag: [259] and a chunk of the wider literature treat honeypot placement as a *temporal* problem — decoys that relocate over time to stay unpredictable — not just a spatial, one-time optimization. Your brief scopes this as static placement, which is the right call given weekend-only hours and a testbed you're building from scratch. But a reviewer who knows this literature may ask why you didn't consider dynamic placement. One sentence in your related-work section — "dynamic/temporal placement (citing [259]) is out of scope given project constraints; this work addresses the static placement problem as a necessary first step" — closes that off before it's asked.

## 5. Honeypot detectability — a gap in your own framing worth patching

Also unprompted, also relevant: [262] and [263] both show that real ICS honeypots get fingerprinted in the wild — via IP TTL values, open-port counts, and other passive signatures — at meaningful rates. This connects directly to iteration 1's "Decoys Cannot Go Everywhere" finding [source 40] and iteration 3's note about defining candidate locations rigorously: it's not just *whether* a decoy can plausibly sit at a given network position, but whether it can sit there *without immediately outing itself*. If your placement algorithm's objective function doesn't at least acknowledge detectability as a constraint or risk factor, a careful reader will notice the gap. You don't need to solve honeypot fingerprinting — just note in your threat model that placements assume a baseline fidelity level sufficient to avoid trivial detection, citing [262]/[263] as the reason this assumption needs stating.

## 6. Still not resolved

- **Qin et al.'s exact method** [266] — blocked by publisher bot-detection on a direct fetch this iteration. You have institutional access through NFSU; pull it via your library's ScienceDirect proxy rather than the open web.
- **Direct primary source for "Decoy Allocation Against Lateral Movement: A Network Centrality Game Approach"** [source 238] — still only confirmed via a publication listing. The closest thing found is a likely-foundational POSG paper [261]; worth a targeted IEEE Xplore search rather than general web search.
- **Whether [237]'s role-aware centrality measure has been tested as an honeypot-placement baseline anywhere** — carried over from iteration 3, not touched this round either.

## Candidates for iteration 5

- Resolve the two items above via database access rather than open web search (both look like they need IEEE Xplore or a library proxy, not a different search query).
- A dedicated pass on IEC 62443 SL (Security Level) vectors specifically — iteration 1/3 confirmed zones/conduits aren't used algorithmically anywhere, but the SL-vector *scoring* methodology within IEC 62443-3-3 might be adaptable as a criticality-weighting input, which hasn't been checked yet.
- Given [250]'s ablation result, a focused search on how RL/game-theory papers in this space *derive* their false-positive cost coefficients (expert elicitation vs. arbitrary vs. fit to a dataset) — knowing the number matters isn't the same as knowing how to set it.
- A check on whether any of the five non-OT domains this research cluster has covered ([233]–[238], [252]–[254]) has a stated reason for *not* extending to OT (funding scope, access to OT testbeds, etc.) — if a paper explicitly says "future work: extend to ICS," that's worth finding and citing as evidence the gap is recognized, not just unaddressed.
