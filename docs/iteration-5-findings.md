# Iteration 5 Findings — OT/ICS Deception Placement Optimization

Builds on iterations 1–4. Does not repeat those conclusions — see `sources.md` for the running source log. Source numbers below refer to that file (iteration 5 = #267–275).

This iteration worked the remaining "candidates for iteration 5" list from iteration 4, in order, plus closed out Qin et al. which had been open since iteration 3.

## 1. IEC 62443 Security Level vectors — resolved, and genuinely useful

This is the best find this iteration. A zone or conduit's security level under IEC 62443-3-3 isn't a single number — it's a **7-element vector**, one score (0–4) per Foundational Requirement: Identification & Authentication, Use Control, System Integrity, Data Confidentiality, Restricted Data Flow, Timely Response to Events, and Resource Availability [267]. That's a standardized, already-defined numeric structure sitting right there in the standard your project already cites — you don't need to invent an ad hoc criticality score; you can derive one from the SL vectors your testbed's zones would already need to be assigned under section 13 of your brief.

One important caveat to build in: exida — a well-known functional-safety/OT-security firm — states plainly that **"a pragmatic means of SL quantification has not yet been developed and vetted by the community"** [268]. That's worth citing directly. It does two things for you: it tells you to present any SL-based weighting as a reasonable semi-quantitative approximation rather than claiming to have solved SL measurement (because you haven't, and neither has anyone else), and it reinforces your novelty argument one layer deeper — if the community hasn't even settled how to quantify SL itself, a formal placement *optimizer* built on top of it is even less likely to already exist.

Two more sources are worth engaging directly rather than citing loosely: [269] does formal attack-path analysis inside IEC 62443-3-2's zone/conduit structure (for countermeasure selection, not deception) — treat this the way you're already treating Zambianco et al., as a close-but-distinct precedent you name and differentiate from. [270] shows a working example of combining CVSS, IEC 62443 SL, and IEC 61508 SIL into one composite risk score — a good structural model for how you justify combining your own coverage/detection/criticality/risk/cost terms into a single objective.

## 2. Qin et al. — finally fully resolved

This had been open since iteration 3. The method is now confirmed: a bio-inspired framework combining dissimilar redundancy and diversity, mixing optimal network shuffling (a form of Moving Target Defense) with cyber deception to maximize the time attackers spend on decoys, plus dual heterogeneous subnets that regenerate once compromised for availability protection — evaluated on an SDN platform in a simulated industrial manufacturing network [271].

The useful conclusion: **this is not a placement-optimization paper**, and it never was. It's an MTD-plus-deception hybrid defense mechanism. You can cite it as evidence that ICS-specific hybrid defense combining deception with other techniques is an active research area — but it doesn't compete with your placement-optimization contribution the way Zambianco et al. or the Kamhoua cluster papers do. Downgrade it in your differentiation section from "needs careful distinguishing" to "brief mention as adjacent ICS defense work."

## 3. How the field actually sets false-positive/cost coefficients

Iteration 4 established that operational risk *should* be a heavily-weighted term (the 51.4% ablation result). This iteration checked how papers in this space actually *set* that kind of coefficient, since knowing it matters isn't the same as knowing how to justify a number.

The answer is unglamorous but useful: **parametric sensitivity sweeps**, not expert elicitation. Park & Dagher's own paper is a clean example — they vary their honeypot-cost coefficient from 0 to 10 and report how the optimal strategy and defender utility shift across that range [272]. A dedicated search for formal expert-elicitation methodology (the kind used in health economics and risk management) turned up nothing applied to honeypot or deception cost coefficients specifically. This means your brief's own plan — weighting justified through literature, experiments, and sensitivity analysis — already matches how this exact community operates. You don't need a fancier justification method than a sweep; you need to run one and show the results, which is squarely within a weekend-hours-scale evaluation.

## 4. Bibliography, further filled in

A few more names worth having on file: three more ICS-specific honeypots not previously catalogued (HoneyVP, ICSpot, and a traceback-honeypot design by Abe et al.), plus Trend Micro's well-known "Caught in the Act" realistic factory honeypot report [273]. The journal-length version of iteration 3's submodular-greedy paper turned out to have an even bigger 2024–2025 bibliography within the same research cluster than previously mapped [274] — none of those individual papers have been checked yet, so that's a natural next thread rather than something resolved this round. And a small methodological caution surfaced [275]: honeypot-allocation-strategy *evaluation* studies in this literature sometimes lean on Mechanical Turk subject pools standing in for real attackers, with mixed results — worth a caveat if your own evaluation ever involves human red-teaming rather than purely automated attack scenarios.

## Still open

- **Direct primary source for "Decoy Allocation Against Lateral Movement: A Network Centrality Game Approach"** [source 238] — still only confirmed via a publication listing across three iterations now. This one specifically looks like it needs IEEE Xplore or a library-proxy search rather than another round of open web search.
- **The expanded 2024–2025 bibliography surfaced this iteration** [274] — Kulkarni et al. 2024, Shen et al. 2025, Jia et al. 2024, Udupa et al. 2024, Wan et al. 2023 — none individually checked for any OT-adjacent angle.

## Candidates for iteration 6

- Try the direct-source problem for source 238 via a different route: search for the paper by its likely venue (IEEE TNSM 2026 table of contents) rather than by title.
- Spot-check two or three of the newly surfaced 2024–2025 cluster papers [274] for anything OT-adjacent, the same way the drone/epidemic-network papers turned up in iteration 4.
- A pass specifically on whether any published work uses IEC 62443 SL vectors (not just zones/conduits generally) as a direct numeric input to *any* graph algorithm — placement or otherwise — since [269] gets close but uses ZCR5, not the SL vector itself.
- Given the project is now well into its literature-review phase across five iterations, it may be worth pausing the search and starting to draft the actual differentiation section (section 14 of your brief) using what's accumulated in `sources.md`, rather than continuing to widen the net indefinitely.
