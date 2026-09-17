# Iteration 11 — Findings

Resumes the research trail after D9 closed open-ended searching at iteration 10. This iteration was not open-ended: it tested a specific hypothesis about the *method* of the review rather than searching for more of the same.

**Sources added:** #328–331. **Documents changed:** `formal-problem-definition.md` §4. **Claims dropped:** one. **Model gaps opened:** one, unresolved.

---

## 1. Why this iteration happened at all

D9 stopped broad iteration after ten passes on diminishing returns. That decision stands. What triggered iteration 11 was a method observation, not a hunch that more searching would help.

While verifying bibliographic details for a reference in the TA-1 document, a 2026 paper (#326, TrapManager) surfaced — not because it matched any query, but because it *cites* the paper being verified. Ten iterations of keyword search had missed it. It turned out to be the closest methodological analogue to this project's MIP formulation found anywhere.

That is a diagnosable weakness, not bad luck. **Keyword search finds work that describes itself the way you describe your problem. Citation chasing finds work that builds on something you already know is relevant, regardless of its vocabulary.** A review conducted almost entirely through the first channel has a systematic blind spot, and it is the blind spot most likely to hide a direct competitor — because a competitor solving your problem in a different research vocabulary is exactly the paper keyword search cannot reach.

Iteration 11 ran the second channel deliberately.

---

## 2. Result on the core novelty claim — negative, and recorded as such

Direct vocabulary-inversion search on the precise combination claimed — IEC 62443 zones and conduits, decoy placement, optimization objective, recent work only — returned standards explainers, vendor guidance, and one already-logged paper (Zambianco, microservices). Nothing occupying the cell.

**Eleven iterations, still nothing.** This is consistent with the claim and does not prove it. Logged as #331 so the search is not silently repeated in six weeks.

---

## 3. A claim was dropped

`formal-problem-definition.md` §4 previously stated that this project is "the first to apply [the four-criterion plausibility rubric] to ICS ATT&CK."

**MITRE Engage has published ATT&CK for ICS mappings since 2024** (#328).

The two are not the same instrument. Engage maps techniques to adversary-engagement *activities*. The rubric scores per-technique decoy feasibility across four dimensions including malice fidelity. A defence of the original claim is available and might even be correct.

It was dropped anyway, for three reasons recorded here so the decision is not revisited from scratch later:

1. **Low value.** "First to apply someone else's instrument to an adjacent dataset" is a minor contribution and is not what this thesis argues. Every claim costs viva time to defend.
2. **Fragile.** Source 53 was published mid-2026. The obvious next paper is someone applying that rubric to the ICS matrix, and it could appear during the writing phase. A claim a single publication can erase should not be load-bearing. This project has already been through that exact shape once — nine iterations of "nothing exists," then Jay.
3. **Invites the wrong argument.** An examiner raising Engage forces a definitional defence. Winning it still signals that the novelty rests on boundary-drawing.

**Replaced with a narrower claim that is specific to this formulation:** source 53 applies the criteria to *techniques*; this project applies them to *assets in a zone-structured architecture*, producing a filtered optimizer search space rather than a coverage map of a matrix. The unit of analysis changes. That claim does not depend on what Engage contains.

**Engage is now an input.** Its ICS mappings are a curated, citable source for rubric criteria 2 and 3, and §4 now says so.

**If the strong claim ever becomes worth making**, the way to earn it is to run the rubric systematically across the full ICS matrix and publish the resulting ICS deception-surface figure — the ICS analogue of source 53's 32%. That is a checkable artifact and a genuine contribution. It is also a second paper's worth of work, not a section, and is out of scope on weekend hours. Recorded as a possible extension, not a plan.

---

## 4. A real gap opened in this project's own model — unresolved

Iteration 11 surfaced *Security Aspects of Zones and Conduits in IEC 62443* (#330), which addresses SL allocation for conduits specifically.

**The problem it exposes:** `formal-problem-definition.md` §1 defines conduits structurally — the subset of edges crossing a zone boundary — and §2 draws `SL(v)` from `zone(v)` only. **Conduits therefore carry no security level and contribute nothing quantitative to the model.**

This matters more than it first appears. The novelty claim names "IEC 62443 zone *and conduit* structure as first-class inputs to a composite objective." Zones are genuinely first-class: every asset carries `zone(v)`, and SL flows from it into `Crit(v)`. Conduits are currently structural bookkeeping. An examiner who reads the claim carefully and then looks for where conduits enter the mathematics will find that they do not.

**Three possible resolutions, none chosen yet:**

- **(a) Assign SL to conduits** per #330's rule — a conduit takes the highest SL of the zones it connects — and let an asset adjacent to a high-SL conduit inherit a criticality contribution from it. Closes the gap directly, adds a term to `Crit(v)`, requires re-running everything and re-verifying against the current results.
- **(b) Use conduits in the candidate filter rather than in criticality** — a candidate adjacent to a conduit crossing a high-SL boundary scores higher on rubric criterion 2, since every path in **P** must cross that conduit. Cheaper, no change to `Crit(v)`, but keeps conduits qualitative.
- **(c) Narrow the novelty claim** to zone structure alone and describe conduits as topology rather than as an input. Honest, free, and weaker — the same trade rejected in §3 above, which argues against it here by consistency.

**Recommendation: (b), with (a) as a stretch.** (b) makes conduits do real work in the pipeline at low cost and low risk to the existing results; (a) is more defensible but lands on the wrong side of the effort/deadline line while the normalisation issue (A11) is still open. **Decision required before Phase D locks.** Added to `00-action-items.md` as A22.

---

## 5. A refinement that improves the specification

Source 53's full text supplies detail not captured when it was first logged: the **Sweep–Seek rule** (#329).

Decoy encounters occur under exactly two conditions. **Sweep** — the attacker moves broadly through assets in range and meets the decoy incidentally. **Seek** — the attacker looks for a specific asset type and interacts with a fabricated instance. A candidate satisfying neither goes untouched, regardless of how plausible it looks in isolation. The paper states this as a rule intended to replace ad-hoc placement.

This is a sharper operational form of rubric criterion 2 than "would an attacker plausibly reach it," and it maps cleanly onto this project's own path set: **P3 is a sweep, P1 is a seek.** Folded into `formal-problem-definition.md` §4, which now asks that criterion 2 be scored by naming which pattern applies and to which path.

**Useful side effect.** This gives a principled test for the two candidates that currently appear in no attack path — Historian and PLC-02 (open item A13). Under Sweep–Seek, a Historian is a plausible *seek* target for a collection-tactic attacker even without appearing in P1–P3. That is an argument for keeping it in **L** and for adding a fourth path, rather than deleting it as filler. Does not resolve A13, but it reframes the choice.

---

## 6. What this iteration did not do

- Did not run forward-citation searches on Jay, Zambianco, Kulkarni or Valeros through a real citation index. The available search tool has no "cited by" function; #326 was found incidentally, not systematically. **This remains the single most valuable outstanding search action** and is the strongest practical argument for A17 (institutional database access). Scopus and Google Scholar both expose forward citations directly.
- Did not examine the criticality or detectability literature. Deferred to iteration 12.
- Did not obtain the full text of #315, the manufacturing-sector paper (A4, still open since iteration 10).

---

## 7. Open items after this iteration

| Item | Status |
|---|---|
| A22 — conduit SL decision, options (a)/(b)/(c) in §4 above | **New, blocking Phase D** |
| A17 — institutional database access, specifically for forward-citation search | Reinforced; now has a concrete justification rather than a general one |
| A13 — Historian and PLC-02 as zero-coverage candidates | Reframed by Sweep–Seek, not resolved |
| A4 — full text of #315 | Unchanged, still open |
| A11 — Risk/CritProt normalisation | Unchanged, still the highest technical priority |
