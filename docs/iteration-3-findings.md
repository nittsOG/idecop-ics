# Iteration 3 Findings — OT/ICS Deception Placement Optimization

Builds on iterations 1–2. Does not repeat those conclusions — see `sources.md` for the running source log. Source numbers below refer to that file (iteration 3 = #233–249).

## Loose end from iteration 2, closed

Iteration 2 couldn't confirm where the Park & Dagher Bayesian Stackelberg paper was actually published. It's confirmed now: **Computers & Security, Volume 168 (2026), Article 104949** [247] — iteration 1's original citation was right after all. Authors are at Boise State University, with no connection to the Kamhoua/Army Research Lab cluster that dominates the rest of this literature — worth noting in the thesis as two *independent* research groups converging on the same conclusion (generic-graph honeypot allocation is a mature, multiply-discovered problem; OT-structured allocation is not).

## The Kamhoua/Fu research cluster runs deeper than iterations 1–2 captured

Chasing the "closest thing to uncertainty-aware OT modeling" thread (iteration 2's note on source 211) led into a much bigger web than expected — the same small group of researchers (Kamhoua at Army Research Lab, collaborating with Fu, Han, Leslie, Anwar, and others at Florida/UIC/Boise State) has been working this specific corner of cyber deception for years, across a lot of venues. Some of it materially matters for your design choices:

**A real basis for choosing greedy, if you want one.** [236] proves the decoy-placement objective in their formulation is monotone and, in certain cases, sub- or super-modular — which gives a **greedy algorithm a formal (1−1/e)-approximation guarantee**, not just "greedy because it's fast." If you want to justify greedy as more than a convenience baseline in your report, this is the citation to build that argument on (you'd need to check your own objective satisfies the same submodularity property, which isn't automatic — but the *pattern* of proof is directly reusable).

**The probabilistic attack graph thread is real, but has a citation problem you should sort out before relying on it** [233, 234]. The paper iteration 2 flagged — "Optimal Decoy Resource Allocation for Proactive Defense in Probabilistic Attack Graphs" — is a bi-level (Stackelberg-style) optimization, proven NP-hard in general, solved via a projected-gradient-ascent method under simplifying assumptions. That much is solid. What's *not* solid: a near-identically-titled paper appears to exist at GameSec 2023 (Springer) with a 4-author list that drops Nandi Leslie, versus the AAMAS-flavored arXiv version's 5 authors. This could be a normal workshop-paper-then-full-paper pair, or a citation error somewhere upstream — either way, resolve which is the citable version before it goes in your thesis.

## Centrality baseline: this needs a decision, not just a label

This is the most actionable finding this iteration. Your Method 2 is "centrality-based placement" — but the same research cluster has, within the last year, published work arguing that's not one thing:

- [237] argues standard centrality measures (degree, betweenness, closeness, eigenvector) **structurally fail** at lateral-movement scenarios because they don't distinguish source, intermediate, and target node roles, and proposes a replacement measure built specifically for that.
- [238] doesn't treat centrality as a baseline to beat at all — it uses node importance/centrality as an *input* to a POSG-based allocation policy.

Practical implication: "centrality-based placement" as currently written in your brief is underspecified. You'll want to pick a specific centrality measure (betweenness is the most defensible default, per iteration 1's finding that it's the most commonly used in this literature) and say so explicitly. A reviewer familiar with this corner of the field may ask why you didn't use a role-aware variant like [237] — you don't need to implement their measure, but citing it and explaining your choice preempts the question.

## Qin et al.'s ICS paper: confirmed real, not yet fully read

[240] is a real, correctly-cited paper (Computers & Security 136:103506) framed around IT/OT convergence making ICS a more attractive attack target — but the actual method (what "hybrid" means here, what it defends against beyond reconnaissance) wasn't extractable from available snippets this pass. Worth a direct full-text fetch next iteration. In the meantime, the same author group's broader survey [241], "Hybrid Cyber Defense Strategies Using Honey-X," is likely the more useful citation — Robin Doss's group at Deakin runs a critical-infrastructure-focused research centre, which is good context for a related-work paragraph.

## India context: thin, but not empty

No CERT-In or NCIIPC guidance specifically on deception or honeypot *placement* exists, as far as this pass found [243] — that reads as a genuine gap, not a search failure, since NCIIPC's Protected System framework is explicit that standard IT-VAPT doesn't cover OT/SCADA/PLC and expects a separate OT-aware assessment. That's exactly the kind of gap your thesis's motivation section could point to. On the academic side, the nearest Indian-institution prior work is IIT Kanpur's C3i Center [242] — a SOAR-triggered dynamic honeypot deployment engine. It's enterprise/VLAN-based, not OT, and not placement-optimization, but it's worth a mention for committee context: you're not the first in India working on adaptive deception, you're extending it toward OT and toward a formal placement objective.

## AI-explanation layer: a real architectural precedent exists

This is worth knowing about regardless of whether you end up citing it: [244] (i-EXAM, Colorado State University, 2026) does almost exactly your section-9 architecture — a formal planner (PDDL, not an LLM) identifies attack paths and generates diverse network-hardening strategies with soundness/completeness guarantees, and an LLM's *only* job is to explain those strategies in natural language to a sysadmin. [245] (Auto-Prov) is a second, independent example of the same decide/explain split, explicitly scoped as "post-detection" only. Neither is about deception placement specifically — but together they confirm your "deterministic optimizer decides, AI only explains" design isn't an ad hoc constraint you're imposing on yourself; it's a recognized good-practice pattern with recent, citable precedent. Worth a line in your related-work section framing it that way, rather than defending the design choice from scratch.

## Still open (candidates for iteration 4)

- **Operational-risk / false-positive-cost quantification for OT tooling** — flagged in iteration 2, not touched this round either. Still the weakest-grounded term in your composite objective.
- Resolve the [233]/[234] citation discrepancy directly against both PDFs.
- Full read of Qin et al. [240] — what "hybrid" actually means in their framework.
- Full read of [244] (i-EXAM/SPEAR) — how directly its planning formulation could be adapted from "hardening strategy" to "deception placement."
- Direct source for [238] (Decoy Allocation Against Lateral Movement) — currently only confirmed via a publication listing, not the paper itself.
- A dedicated pass on whether [237]'s role-aware centrality measure has been tested as an honeypot-placement baseline anywhere, or only proposed for general lateral-movement analysis.
