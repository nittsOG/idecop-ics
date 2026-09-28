# Action Items — Manual Tasks

Standing checklist of things that need your action because they're outside what I can do from this conversation. Added here the moment they come up, marked done when you tell me they're done. Check this file instead of hunting through chat history for something I mentioned once.

## TA-1 — did not take place on 22 September 2026; not yet rescheduled

The guide was unavailable on the day. Nothing below is overdue: these items block TA-1 whenever it is rescheduled, and the new date is part of A14.

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A7 | Fill the guide's name and designation into the TA-1 title block | Not something I hold | **Pending — blocks TA-1 once rescheduled** |
| A8 | Complete reference [23], the D3O-IIoT deep-RL deception paper. PMC link is recorded in `sources.md` | Currently the sole citation justifying heavy operational-risk weighting, and it is uncitable without author and venue details | **Pending — blocks TA-1 once rescheduled** |
| A9 | Complete references [12] and [26] — the GNN placement paper (2nd Graph Neural Networking Workshop, ACM 2023) and the criticality-analysis patent number | Author and patent details were not captured during the review | **Pending — blocks TA-1 once rescheduled** |
| A10 | Confirm with the guide whether IEEE citation style applies and whether the template exists yet | Institutional convention | Pending |

## Blocking the evaluation campaign

| # | Item | Why it's manual | Status |
|---|---|---|---|
| ~~A11~~ | ~~Decide how to resolve the `Risk(x)` and `CritProt(x)` normalisation mismatch — mean, union probability, or keep the sum and document the scale | A modelling decision with thesis consequences, not a bug fix. Blocks Phase D~~ | Resolved by D20 | **Done** |
| A12 | **Decide the primary research question's wording and what Phase D evaluates it against — together, before any evaluation run.** D24 establishes two facts on the frozen instance. (1) Greedy equals the exhaustive optimum in 20 of 20 comparison-grid cells, so §8's first clause ("a higher composite objective F(x)") cannot fail: it is implied by optimality and measures search quality, not whether the objective is a good one. (2) §8's second clause — equal or greater Coverage and CritProt at equal or lower Cost — holds in 16 of 20 cells and fails in 4, all of them cells where greedy deploys fewer decoys than the budget allows; whether those declines are better depends on δ and the D22a risk values. So the evaluation needs a yardstick that is not F. Options, rough cost in weekend-units: **held-out attack paths** (~1 — optimise on some paths, measure interception on paths the optimiser never saw; needs more paths, chosen by a stated rule rather than by hand); **input-perturbation robustness** (~0.5 — vary risk and criticality within their uncertainty and check the component metrics hold); **synthetic larger instances** (~1–2 — a sampling unit for statistics, and cases where greedy is not optimal, the only place distorted greedy's guarantee matters); **testbed attack simulation** (3–4 — see A16). Whatever is chosen is frozen before the campaign | Research-question wording and evaluation scope are yours and the guide's call | **Pending — gates Phase D** |
| ~~A13~~ | ~~Decide what to do about Historian and PLC-02 — both are confirmed candidates that appear in no attack path and can never contribute coverage. Reroute a path through them, or document them as search-space filler ~~ | Resolved by D21 — P4 added, Historian now selected in 16/20 configurations; PLC-02 documented as search-space richness rather than made selectable | **Done** |

## Schedule and coordination

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A14 | Obtain the final submission date, the rescheduled TA-1 date, TA-2 and TA-3 dates, and the institutional template | Every interval in `00-project-timeline.md` is relative until these exist. TA-1 did not take place on 22 September, so its date is now unknown too | **Pending — highest coordination priority** |
| A15 | Agree with the guide, before results exist, that an honestly reported negative or mixed evaluation result is an acceptable outcome | Much easier to agree before the numbers arrive. **No longer hypothetical:** D24 shows §8's second clause already fails in 4 of 20 comparison-grid cells | Pending |
| A16 | Agree a scope position on the physical testbed — full seven VMs, or reduced to one zone boundary with the rest modelled | 3–4 weekend-units at stake; the optimiser runs on the modelled graph either way. Testbed attack simulation is also one of A12's options for an evaluation criterion outside F, so the two are best decided together | Pending |

## Research completeness

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A2 | Set up / confirm access to NFSU's remote e-library portal (`elibrarynfsu.remotexs.in`) | Needed for any paywalled paper — I can search and verify citations but cannot fetch subscription content | Pending |
| A4 | Get the full PDF of Shahin, Maghanaki, Chen (2026), `sources.md` #315 — likely free via MDPI | Needed to confirm whether it is a genuine manufacturing-sector competitor. The Jay paper showed that abstracts are an unreliable basis for a novelty judgement | Pending |
| A17 | Perform the certified systematic database sweep — IEEE Xplore, Scopus, Web of Science | The one systematic gap in the literature review. Request access early; the lead time is outside your control | Pending |
| A28 | Retain the word **"published"** in every statement of the novelty claim, and add the four commercial distinctions to section 14 | Wording of the claim is yours to own. A granted patent *is* published work, so "published" alone does not separate this project from US 9,853,999 — the distinction must be method-level: their output is a **count for a subnet**, ours is a **set of positions** | **Pending — was referenced in `iteration-13-findings.md` as logged but had never been written into this file until D23** |
| A29 | Systematic patent sweep — Acalvio (25+ granted US patents), Commvault/TrapX, Fortinet, SentinelOne/Attivo, Proofpoint/Illusive. Also read the **granted claims** of US 9,853,999, not just its abstract and description | Prior art includes patents and shipping products, not only papers. Needs no institutional credentials, so unlike A17 it is not access-blocked. `03-commercial-prior-art-analysis.md` currently states the comparison at description level only, and the claims are what define legal scope | **Pending — comparable in importance to A17; was referenced as "Logged as A29" in `03-commercial-prior-art-analysis.md` but had never been written into this file until D23** |
| A30 | Only if the thesis cites `sources.md` #353 **by theorem number**: obtain the PDF and confirm the number. One retrieval route reported Theorem 1; a second could not corroborate it | The repository now cites the result by content rather than by number, which is accurate and sufficient, so this is optional rather than blocking. Do **not** cite a number that has not been read directly | Pending — optional, low priority |
| A31 | Only if the thesis makes any claim about **Sviridenko, Vondrák & Ward's own theorem**: obtain that paper (`sources.md` #354). The current characterisation comes from #353's related-work discussion, not from their text | Adequate for rejecting §7(i) on practicality, since the only claim relied on is "impractical". Not adequate for stating their result | Pending — optional, low priority |

## Specification decisions opened by iterations 11–12

| # | Item | Why it's manual | Status |
|---|---|---|---|
| ~~A22~~ | ~~Decide how conduits enter the model quantitatively. They are named in the novelty claim as a first-class input, but currently carry no security level and contribute nothing to `Crit(v)`. Options (a) assign conduit SL per #330 and feed it into criticality, (b) use conduit adjacency in rubric criterion 2 only, (c) narrow the claim to zones. Resolved by D20 — option (a) implemented: ConduitSL(v) added to Crit(v). Option (b) would not have made the novelty claim true, since it shapes L rather than F(x)~~ | — | **Done** |
| ~~A23~~ | ~~Build a Filter 2 scoring rubric from #333's fingerprinting-artifact taxonomy, replacing the current qualitative down-weighting. Read #333 in full first ~~ | Resolved by D22 — three-factor rubric implemented, values re-derived, effect on results reported | **Done** |
| A24 | Add to `threat-attack-model.md`: the stated assumption that emulated ICS decoys are detectable by a capable adversary with engineering tooling (#20 §6.3), and the derived principle that Sweep candidates are more robust to detectability than Seek candidates | A threat-model assumption, yours to confirm | Pending |
| A25 | Reframe `Damage(v)` elicitation in Asset Criticality Analysis consequence-category terms (#336), using the consequence decomposition only, never ACA's likelihood term | Changes how the number is requested from a process engineer | Pending — low priority |
| ~~A27~~ | ~~Locate and verify the primary source for the regularised submodular result (f = g − ℓ, g monotone submodular, ℓ modular non-negative) — attributed to Sviridenko, Vondrák & Ward. **Until verified, claim no approximation guarantee for greedy.** Alternative: adopt the risk-as-constraint reformulation in §7(ii)~~ | Resolved by **D23** via a third route neither option anticipated: Harshaw et al. (2019), `sources.md` #353, obtained in full. Distorted Greedy carries (1−1/e) on f = g − c with a matching hardness result; preconditions verified on the frozen instance. §7(i) is superseded — Sviridenko's algorithm needs the multilinear extension. **Plain greedy still has no guarantee and must not borrow this one** | **Done** |
| A26 | Disambiguate "detectability" in `00-glossary.md` — ACA uses it for advance detection of failures, this project for attacker identification of decoys | Trivial; fold into the next glossary edit | Pending |

## Repository hygiene

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A18 | ~~Remove `references/312-jay-2023-deception-substations.pdf` from the public repository~~ — **re-inspected in the D24 session.** The file was deleted from the tree on 15 September (`6effbd5`) but is still retrievable from the first commit (`66d4f14`). Removing it from history would mean rewriting every commit hash and force-pushing, which breaks existing clones. That is probably unnecessary: the paper is an *IEEE Access* article, and IEEE publishes every open-access article under either CC BY or CC BY-NC-ND (`sources.md` #356), both of which permit non-commercial redistribution of the unmodified article with attribution. Recommendation: close without a history rewrite, keep citing by DOI, and keep the rule of not committing publisher PDFs of non-open-access papers | Licence reading, not legal advice. The journal's licence options are verified; this article's own licence line was not read (#357) | **Pending — recommend closing; needs your confirmation** |
| A19 | Adopt incremental commits rather than single snapshots | The thesis claims incremental build-and-verify as methodology; commit history is the evidence for that claim | Pending |

## Build

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A6 | Wire `/runs/{id}/explain` to a real Ollama instance | Needs Ollama installed and running to test a real model call; cannot be verified in a sandbox the way everything else has been | Pending, deferred by choice |
| A20 | Build the Colab plausibility-scoring notebook | Needs a GPU-backed runtime and your Google account | Pending |
| A21 | Stand up the physical VM testbed | Needs VMware Workstation and your hardware | Pending |

## Completed

| # | Item | Resolution |
|---|---|---|
| ~~A1~~ | ~~Add specification files to Project Knowledge~~ | Superseded — the GitHub repository is now the canonical source and is fetched directly |
| ~~A3~~ | ~~Share the current direction and specification with the guide~~ | TA-1 submission and the progress review pack now serve this |
| ~~A5~~ | ~~Decide how to resolve D15~~ | Resolved via D19 — P3 rerouted through Engineering WS-2, implemented and re-verified |

To mark something done: tell me the item number and I'll update this file.
