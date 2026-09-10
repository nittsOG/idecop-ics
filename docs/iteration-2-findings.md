# Iteration 2 Findings — OT/ICS Deception Placement Optimization

Builds on iteration 1. Does not repeat those conclusions — see `sources.md` §Iteration 1 for that pass. Source numbers below refer to the running log in `sources.md`.

## Headline correction

Iteration 1 described the Bayesian Stackelberg honeypot-allocation paper (Park & Dagher) as using a **"Purdue-model-inspired layered structure."** Having now read the full text directly [source 192], that's wrong and needs to be corrected in any thesis draft that cites it: the paper never mentions Purdue, IEC 62443, or any OT concept. Its "layered structure" is generic graph-distance layering — nodes grouped by shortest-path distance to a target, used purely to make the MILP tractable via backward induction. It's an enterprise/general-network paper, full stop.

**Consequence for the novelty claim: it gets stronger, not weaker.** There is now no partial counterexample using OT-domain concepts at all among the placement-optimization papers found so far. The gap — formal placement optimization with IEC 62443 zones/conduits or Purdue levels as real structural inputs — is clean.

## What's newly verified with exact numbers

Fetched the full text of both Zambianco et al. papers (the closest precedent from iteration 1) rather than relying on abstracts:

- **Zambianco/Facchinetti/Siracusa 2025** [190]: ILP solved with SCIP, 100 random instances, attack targets 1–9, drawn from the 266-technique ATT&CK Enterprise matrix (153 technique-outcomes eligible as targets). Runtime 0.042–0.060 seconds regardless of target count — the NP-hardness is real but irrelevant at ATT&CK's scale. At one target: 4 decoys for their "Optimal" scheme vs. 40 for the next-best "Group" baseline.
- **Zambianco/Facchinetti/Doriguzzi-Corin/Siracusa 2024** [191]: tested at M=100–500 microservices (N up to 20 compute nodes), Barabási–Albert synthetic graphs calibrated against real Alibaba cloud traces, 100 configurations, 95% CI, run on an Apple M1 Pro. Decoy-to-microservice ratio shrinks from 21.5% (M=100) to 14.3% (M=500) — decoys scale sub-linearly with network size. To hit 80% attacker-interception probability, their optimal scheme needs ~50% of spare resources; the naive "sidecar" baseline needs ~160% (i.e., is infeasible without more hardware).

These are real, citable numbers for a "comparable prior work" table in the thesis — useful for framing what a "good" result looks like at your testbed's scale.

## Existing tools: nothing changed, but the citation trail deepened

No new OT deception *tool* overturns iteration 1's picture. What did surface: reading Zambianco's own related-work section [193–204] shows the enterprise/IoT/cloud deception literature is bigger than iteration 1 captured — POMDP-based (Al Amin et al. [194, 212]), hidden Markov (Horák et al. [193]), Stackelberg (Liu et al. [208], Anwar & Kamhoua [209]), DRL (Li et al. [206, 207], Jin et al. [210]), and a probabilistic-attack-graph decoy allocator (Ma, Han, Leslie, Kamhoua, Fu [211], arXiv:2301.01336) that's worth a full read next iteration since probabilistic graphs are closer in spirit to how you'd model uncertain OT attack paths. None of it is OT-specific; all of it reinforces that the *methods* are borrowed from elsewhere and the *domain application* is the contribution.

## Genetic algorithms: real precedent, but thin

Zambianco's related work flags **Ge et al. 2021** [196] (ACM TOIT) and **Rehman et al. 2024** [197] (Computers & Security) as using genetic optimization for IoT decoy allocation. Both are limited to reconnaissance/exfiltration-stage deception (not multi-step attack paths) and neither is OT. This is enough to say "GA has precedent for decoy placement" in your literature review without overclaiming it's been done for attack-path coverage or for OT.

## Patents: deployment mechanics, not placement math

Checked Google Patents / Justia across six representative honeypot patents spanning 2004–2022 [214–219] (Amazon-style resource-pool allocation, adaptive VM deployment, lifecycle-ratio triggers, VPN-tunneled deployment, high-interaction honeypot farms, differential-privacy fake-data generation). **None claims a quantitative, graph- or attack-path-based placement algorithm; none is OT-specific.** This is a clean, citable "no prior art" data point for the novelty section — patents in this space protect *how a honeypot is built or deployed*, not *where it should go*.

## OT testbed architecture: your stack is the standard stack

This wasn't covered in iteration 1 and directly de-risks the project's implementation plan. A dedicated survey [220, arXiv:2102.05631] plus seven individual testbed papers [221–228] confirm that GNS3/virtualization + OpenPLC + a SCADA-HMI layer (ScadaBR, SCADA-LTS, Node-RED-class tools) is the field's default toolkit — used for water treatment, nuclear, and substation testbeds alike, several explicitly Purdue-model-segmented [222, 223, 227]. Reported scale is consistently **small**: 1–2 PLCs, one HMI, a handful of sensors is typical even in published, peer-reviewed work. Your proposed VMware/Kali/pfSense/OpenPLC/Node-RED testbed isn't just feasible — it's smaller than what several published papers already validated. **The testbed is not where your risk lives.**

## MITRE ATT&CK for ICS: exact current numbers, and a confirmed open gap

Pulled the live figures from MITRE's own site [229, April 2026 update]: **ICS matrix = 12 tactics, 79 techniques, 18 sub-techniques, 18 assets** (vs. Enterprise's 15 tactics / 222 techniques / 475 sub-techniques). ICS techniques deliberately don't duplicate Enterprise ones — ladder-logic modification, alarm suppression, and false setpoint injection have no Enterprise equivalent [230].

I could not find any paper that applies the "Decoys Cannot Go Everywhere" four-criterion feasibility rubric (iteration 1, [40]) to this smaller ICS-specific matrix instead of the Enterprise one. **That's a confirmed, real gap** — worth naming explicitly as something your thesis could do that nobody has: audit which of the 79 ICS techniques actually admit a plausible, instrumentable decoy, before your optimizer ever runs. It's also a much smaller, more tractable exercise than the original paper's 250-technique Enterprise audit.

## IEC 62443 zones/conduits: still nobody's using them algorithmically

Checked both an academic source [231, Jaatun et al. 2026] and eight practitioner/vendor guides [232] on how zones and conduits actually get defined in practice. Every single one describes the same manual pipeline: inventory assets → risk-assess (IEC 62443-3-2) → group by shared Security Level → draw conduits → assign controls. It's a **procedural/compliance framework**, never a mathematical input to an optimizer, in deception literature or in general OT security placement (segmentation, sensor placement, IDS placement) alike. This closes off a possible objection — someone might assume zone/conduit *design itself* has been optimized elsewhere and you're just reusing that; it hasn't been, anywhere I found.

## Still open (candidates for iteration 3)

- Full read of Ma/Han/Leslie/Kamhoua/Fu on probabilistic attack graphs [211] — closest thing to uncertainty-aware OT modeling found so far.
- Full read of Qin et al. 2024 "hybrid cyber defense... reconnaissance... industrial control systems" [204] — explicitly ICS-titled, not yet verified in depth.
- A dedicated fresh sweep restricted to 2025–2026 publication dates only, since this pass mostly followed citation trails rather than a clean date-filtered search.
- Operational-risk / false-positive-cost quantification for OT security tooling specifically — touched on lightly this iteration, not resolved. This still needs a dedicated pass to formally justify the "operational risk" term in the composite objective.
- Confirm the actual publication venue for Park & Dagher (Bayesian Stackelberg) — iteration 1 asserted Computers & Security 2026; the arXiv text itself doesn't state this.
