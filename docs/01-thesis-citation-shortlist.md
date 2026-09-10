# Thesis Citation Shortlist — Curated from `sources.md`

322 entries logged across ten iterations; this is the subset actually worth citing in the thesis, organized the way the literature review chapter would actually be structured, not the order they were found in. Each entry states what's being drawn from it and why it earns a place, not just the reference. Source numbers in brackets point back to the full entry in `sources.md` for the complete context, link, and verification marker.

**43 entries.** Not a hard target — a defensible, well-justified set given what's actually verified. Padding to a round number with weak entries would be worse than a shorter, stronger list.

---

## I. The closest prior art — needs the deepest treatment in section 14

**1. Jay, D. (2023).** "Deception Technology Based Intrusion Protection and Detection Mechanism for Digital Substations: A Game Theoretical Approach." *IEEE Access*, 11, 53301–53314. [#305, #312]
*What's drawn from it:* the full mathematical formulation, read in full text, not just the abstract — a bi-level Stackelberg game allocating protection/detection decoy type across "observable subgraphs" of a GOOSE VLAN, solving a graph-*observability* problem, not a site-*selection* problem. This is the source the entire differentiation argument in section 14 is built around: three specific, defensible distinctions (single-VLAN vs. multi-zone; IEC 61850/GOOSE-specific vs. IEC 62443-general; game-theoretic equilibrium over decoy type vs. a composite multi-metric objective) all trace back to this one paper's actual math.

**2. Jay, D., Goyel, H., Sreejith, A., & Rathi, R.** US Patent 12,425,450 B2, "Method for securing digital substations and system thereof," filed 2024, assigned to GridSentry Private Ltd. [#311]
*What's drawn from it:* evidence that Jay's research line has been commercialized by a named Indian company, using a *different* mechanism (reactive network-switching, not proactive optimization) than the academic paper. Cited to show "who else is working on this" includes a live commercial entity, not just one paper — and to correctly distinguish the patent's mechanism from the paper's, since they're not the same thing despite the same inventor.

---

## II. Methodological precedents — placement optimization in other domains

**3. Zambianco, M., Facchinetti, T., & Siracusa, D. (2025).** "A Proactive Decoy Selection Scheme for Cyber Deception using MITRE ATT&CK." *Computers & Security*, 148, 104144. [#24, #190]
*What's drawn from it:* the closest *methodological* precedent — a graph-partition ILP minimizing decoy count while covering MITRE ATT&CK-derived attack paths, full text confirmed (Multi-Terminal Vertex Separator formulation, SCIP solver, exact eval setup and results). Needs direct, explicit engagement in section 14: same mathematical shape as this project's approach, different domain (enterprise IT, not OT).

**4. Zambianco, M., Facchinetti, T., Doriguzzi-Corin, R., & Siracusa, D. (2024).** "Resource-aware Cyber Deception for Microservice-based Applications." *IEEE Transactions on Services Computing*, 17(6), 4211–4224. [#25, #191]
*What's drawn from it:* a second paper from the same authors, confirming this is a sustained research line, not a one-off — integer non-linear optimization for decoy placement under a resource budget, using a betweenness-centrality heuristic for scale. Cited alongside #3 to show the depth of the closest precedent group.

**5. Ngo, M.-Q., Guo, M., & Nguyen, H. (2023).** "Near Optimal Strategies for Honeypots Placement in Dynamic and Large Active Directory Networks." AAMAS 2023. [#26]
*What's drawn from it:* the NP-hardness proof for honeypot placement, even on static graphs — the direct justification for why brute-force is ruled out and a heuristic/exact-solver approach (greedy + MILP) is the right method class, cited in `formal-problem-definition.md` §7 and D1.

**6. Ngo, M.-Q., Guo, M., & Nguyen, H. (2023).** "Catch Me if You Can: Effective Honeypot Placement in Dynamic AD Attack Graphs." arXiv:2312.16820. [#27]
*What's drawn from it:* comparable-scale evaluation data (AD graphs up to ~12,001 nodes) used as calibration for what published work considers a reasonable evaluation scale — part of the feasibility argument for this project's own ~11-node testbed being appropriately scoped, not undersized.

**7. Nguemkam, S., Anwar, A. H., Kengne Tchendji, V., Tosh, D., & Kamhoua, C. (2023).** "Optimal Honeypot Allocation Using Core Attack Graph in Cyber Deception Games." IEEE PIMRC 2023. [#28]
*What's drawn from it:* the "core attack graph" abstraction — concentrating decoys on critical-path nodes rather than the full graph — a related simplification strategy worth citing alongside this project's own two-filter candidate-location reduction (Filter 1 + Filter 2 in §4).

**8. Park, D., & Dagher, G. G. (2026).** "Adaptive honeypot allocation in multi-attacker networks via Bayesian Stackelberg Games." *Computers & Security*, 168, 104949. [#30, #192]
*What's drawn from it:* full text read specifically to correct an early misreading — this paper's "layered structure" is generic graph-distance layering for solver tractability, *not* a Purdue-Model or IEC 62443 reference architecture, despite surface resemblance. Cited as the nearest thing to an "OT-flavored" precedent that, on close reading, isn't actually OT-specific — an important negative finding for the novelty argument, not just a citation.

**9. Kulkarni, A., Cohen, J., Kamhoua, C., & Fu, J. (2024).** "Integrated Resource Allocation and Strategy Synthesis in Safety Games on Graphs with Deception." arXiv:2407.14436. [#236]
*What's drawn from it:* the theoretical basis for a greedy algorithm's approximation guarantee — proves a comparable decoy-placement objective is submodular in structured cases, giving greedy a real (1−1/e) bound. Directly underlies D1's method choice, with the honest caveat (in `02-optimization-formulation.md` §1) that this project's own objective only partially satisfies the same property.

**10. Kouam Wamba, K., Hayel, Y., Deugoué, G., & Kamhoua, C. (2025).** "A novel centrality measure for analyzing lateral movement in complex networks." *Physica A*, 658. [#237]
*What's drawn from it:* a direct critique of standard centrality measures (betweenness, degree, etc.) for missing source/intermediate/target role structure in lateral-movement scenarios. Cited in D4 to justify naming *betweenness specifically* as the baseline while acknowledging its limitations, rather than presenting centrality as an unexamined default.

**11. Podder, S., Sreedharan, S., Caglar, T., Ray, A., Bashir, M., & Ray, I. (2025).** "SPEAR: Security Posture Evaluation using AI Planner-Reasoning on Attack-Connectivity Hypergraphs." SACMAT 2025. [#255]
*What's drawn from it:* the formal framework — PDDL-based automated planning generating hardening strategies with soundness/completeness guarantees — underlying i-EXAM (#12 below). Cited as the technical foundation of the "deterministic planner decides" side of the decide/explain split.

**12. Podder, S., Ganim, R., Sreedharan, S., Ray, A., & Ray, I. (2026).** "i-EXAM: Instructable and Explainable Attack Connectivity Graph Modeler." arXiv:2607.05888. [#244]
*What's drawn from it:* the closest architectural match found anywhere for this project's AI philosophy — a formal planner decides, an LLM's only role is explaining the result in natural language, for general network hardening. Directly grounds D6 and `formal-problem-definition.md` §8's secondary research question; the single most load-bearing citation for the AI layer's design.

**13. Wang, K., et al. (2021).** "An Automatic Planning-Based Attack Path Discovery Approach from IT to OT Networks." *Security and Communication Networks* (Wiley). [#257]
*What's drawn from it:* the same PDDL-based planning formalism as SPEAR/i-EXAM, applied specifically to IT-to-OT attack path discovery. Bridges the AI-explanation architecture directly into the OT domain — closes the gap between "this decide/explain pattern is precedented" and "it's been shown to work on OT-adjacent topologies specifically."

**14. Nguemkam, S., et al. (2024).** "Optimal Honeypot Allocation Using Core Attack Graph in Partially Observable Stochastic Games." *IEEE Access*, 12, 187444–187455. [#29]
*What's drawn from it:* comparable-scale POSG evaluation data (scaling to ~300 nodes via a core-attack-graph abstraction) — additional feasibility calibration alongside #6, and an example of the game-theoretic method family this project's approach is explicitly *not* using, with reasoning for that choice available in the decisions log.

**15. Anonymous authors (2023).** "Optimizing Honeypot Placement Strategies with Graph Neural Networks for Enhanced Resilience via Cyber Deception." 2nd Graph Neural Networking Workshop (ACM). [#34]
*What's drawn from it:* one further method-family data point (GNN-based placement, addressing the "curse of dimensionality" in game-theoretic approaches) — cited briefly in the related-work survey of the placement-optimization landscape to show breadth of methods considered before settling on greedy+MILP.

**16. D3O-IIoT** — deep reinforcement learning-driven dynamic deception orchestration for industrial IoT security (full author/venue TBD — 🟡 needs verification before final citation). [#250]
*What's drawn from it:* the direct quantitative justification for weighting operational risk heavily — an ablation study found removing the false-positive-control term cost 51.4% of the system's performance. This is the single citation D5 and `formal-problem-definition.md` §5 rest on; verify full bibliographic details before the thesis draft locks it in.

---

## III. OT/ICS deception tools and platforms — generation/fidelity, not placement (establishes what the field already solves)

**17. Conpot** — MushMush Foundation. Open-source ICS honeypot (Modbus, S7comm, SNMP, BACnet, IEC 60870-5-104). [#1]
*What's drawn from it:* the field's de-facto baseline tool, cited to establish that decoy *generation* is a solved, mature problem — the starting point for the "not another honeypot" framing in the introduction.

**18. López-Morales, E., et al. (2020).** "HoneyPLC: A Next-Generation Honeypot for Industrial Control Systems." ACM CCS 2020. [#2]
*What's drawn from it:* a more advanced fidelity example (profiles specific real PLC models, fools Nmap/Shodan) — used alongside Conpot to show the *range* of maturity in decoy generation, from basic to sophisticated, all still deployment/fidelity-focused rather than placement-focused.

**19. Yang, X., Cheh, C., Chen, B., & Mashima, D. (2020).** "DecIED: Scalable K-Anonymous Deception for IEC61850-Compliant Smart Grid Systems." ACM CPSS Workshop. [#11]
*What's drawn from it:* an OT-specific (smart-grid) deception system — k-anonymous decoy IEDs — cited as evidence that OT deception *specifically* has real prior work, but placement here is architectural (achieving k-anonymity), not the result of a formal multi-metric optimization.

**20. Cifranic, N., Hallman, R. A., Romero-Mariona, J., Souza, B., Calton, T., & Coca, J. (2020).** "Decepti-SCADA: A cyber deception framework for active defense of networked critical infrastructures." *Internet of Things*, 12, 100320. [#13]
*What's drawn from it:* SCADA-specific decoy generation and manual, GUI-driven placement — cited as a direct example supporting the novelty claim's core distinction (existing solutions deploy deception; this project optimizes *where*).

**21. Furfaro, A., et al. (2025).** "ICSLure: A Very High Interaction Honeynet for PLC-based Industrial Control Systems." arXiv:2509.04080. [#3]
*What's drawn from it:* a current (2025), very-high-fidelity example integrating real PLCs with physics-aware simulation — shows the fidelity side of the field is still actively advancing, reinforcing that the *placement* side, by contrast, remains comparatively neglected.

**22. Rowe, N. C. (2025).** "Designing Deceptions for Protecting Industrial Control Systems." In *Foundations of Cyber Deception* (Zhu, Q., Lu, Z., Yu, P., & Wang, C., Eds.). Springer Nature. [#287]
*What's drawn from it:* full text read specifically for a critical distinction — Rowe's "deception locations" are architectural layers *within one device's software stack* (UI, kernel, device driver), not positions across a network topology. Needs explicit citation and disambiguation in section 14: the closest-*sounding* prior work found in the entire process, and the paper most likely to prompt a "didn't you miss this?" question if not addressed directly.

**23. Sandia National Laboratories (2021).** SAND2021-11609, LDRD technical report. OSTI.gov. [#296]
*What's drawn from it:* both a tools citation (Sandia's DER-honeypot implementation work) and a gap-confirmation citation (see §V below) — cited here specifically for the concrete spoofing-script implementation detail as evidence of the state of the art in OT decoy engineering.

**24. Sandia National Laboratories.** HADES (High-Fidelity Adaptive Deception & Emulation System). [#297, #301]
*What's drawn from it:* a real, deployed, federally-recognized (2018 Government Innovation Award) deception platform, with a named real-world deployment (NJ Transit Grid) — cited as evidence deception technology has reached genuine operational maturity in OT-adjacent contexts, independent of the academic literature.

---

## IV. Standards and frameworks

**25. MITRE.** "MITRE ATT&CK for ICS: Design and Philosophy." March 2020. [#51]
*What's drawn from it:* the official framing document for why ATT&CK for ICS exists as a separate matrix from Enterprise ATT&CK — grounds the choice to build the threat model on ICS-specific tactics/techniques rather than generic ones.

**26. MITRE.** ATT&CK for ICS structural update, April 2026. [#229]
*What's drawn from it:* the exact current structure (12 tactics, 79 techniques, 18 sub-techniques) used to precisely scope the threat model's technique selection and to note, accurately, that the "Decoys Cannot Go Everywhere" feasibility rubric (#33 below) has only been applied to the Enterprise matrix, not ICS — an explicitly named open gap this project's Filter 1 partially addresses.

**27. International Electrotechnical Commission.** IEC 62443-3-3, Annex A ("Discussion of the SL vector"). [#267]
*What's drawn from it:* the formal definition of the 7-element Security Level vector (FR1–FR7) — the standards-grounded half of the criticality formula in `formal-problem-definition.md` §2.

**28. National Institute of Standards and Technology.** NIST SP 800-82 Rev. 3 (2023), *Guide to Operational Technology (OT) Security*. [#55]
*What's drawn from it:* the standard general reference for OT security terminology and practice, cited for grounding rather than a specific technical claim — one of the three frameworks named in the original brief §13.

---

## V. Gap-confirmation sources — independent authorities converging on the same conclusion

**29. Sandia National Laboratories (2021).** SAND2021-11609. [#296] *(cross-referenced with #23 above)*
*What's drawn from it, specifically for this section:* the direct quote — "there is currently an absence of well-developed cyber-physical deception elements and virtualization technologies for OT systems" — a national laboratory's own internal justification for funding this exact category of work, independent of any academic literature review.

**30. Electric Power Research Institute (2019).** "Deception Technology: Emerging Cyber Security Technology for Utilities." [#306]
*What's drawn from it:* an industry R&D consortium — not academia — naming decoy placement specifically as unresolved: "many practical unknowns... in terms of the appropriate design and placement of lures and decoys." The cleanest single-sentence gap citation found across all ten iterations, precisely because it's the electric utility industry saying it about itself.

**31. MITRE.** CICAT (Critical Infrastructure Cyberspace Analysis Tool), developed for an IAEA nuclear-facility cybersecurity project. [#299]
*What's drawn from it:* evidence that the *analysis* layer this project depends on (attack-path generation, criticality-weighted scoring, "hot spot" identification) is mature and federally validated on real critical infrastructure — while explicitly stopping short of deception placement, which is exactly where this project's contribution begins. A clean "here's the mature technique, here's the gap I'm filling" citation pair.

**32. Bartwal, U., Mukhopadhyay, S., Negi, R., & Shukla, S. (2022).** "Security Orchestration, Automation, and Response Engine for Deployment of Behavioural Honeypots." arXiv:2201.05326. [#242]
*What's drawn from it:* the nearest Indian-institution prior art (IIT Kanpur's C3i Center) — SOAR-triggered dynamic honeypot deployment, enterprise IT rather than OT, and not placement-optimization. Cited for committee context: this project extends an existing Indian research line toward OT and toward a formal placement objective, rather than working in isolation from national research activity.

**33. Valeros, V., et al. (2026).** "Decoys Cannot Go Everywhere: Mapping the Deception Surface in MITRE ATT&CK." arXiv:2606.27966. [#40]
*What's drawn from it:* both a gap-confirmation and a methodological source (see §VI) — its four-criterion feasibility rubric, applied to the Enterprise ATT&CK matrix, found only 32% of techniques admit a plausible decoy. Directly adapted (not copied) as this project's own Filter 1 rubric, extended to the ICS matrix for the first time.

---

## VI. Criticality-scoring methodology precedents

**34. exida (functional safety / OT security consultancy).** Blog: "IEC 62443 – Levels, Levels and More Levels." [#268]
*What's drawn from it:* the industry's own admission that "a pragmatic means of SL quantification has not yet been developed and vetted by the community" — the explicit justification for presenting this project's SL-based criticality scoring as a semi-quantitative approximation, not a solved measurement.

**35. US Patent (number on file in `sources.md` #282).** "Criticality analysis of attack graphs." [#282]
*What's drawn from it:* a worked, numeric formula — Criticality = f(locality, centrality, damage) — combining Purdue-level locality, network centrality, and operational damage fraction into a single score, with a full example computation. The graph/operational half of this project's dual criticality-scoring approach, independent of and complementary to the IEC 62443 SL-vector route.

**36. Hollerer, S., Sauter, T., & Kastner, W. (2022).** "Risk Assessments Considering Safety, Security, and Their Interdependencies in OT Environments." ARES 2022 (ACM). [#270]
*What's drawn from it:* a precedent for *how* to justify combining heterogeneous risk metrics (CVSS, IEC 62443 SL, IEC 61508 SIL) into one composite score over a zone/conduit structure — a methodological model for this project's own composite-objective writeup, not a source of specific numbers.

**37. Cybersecurity and Infrastructure Security Agency, Federal Bureau of Investigation, & UK National Cyber Security Centre (2025).** Joint OT security guidance. [#286]
*What's drawn from it:* a third, independent, multi-government-agency framing naming criticality, exposure, and availability as the three factors every OT asset should be scored on — cited for *why* criticality-weighted scoring belongs in the objective at all, complementing the standards-based and graph-based sources above, which answer *how* to compute it.

---

## VII. Plausibility-scoring-assist grounding (the AI-assisted Filter 1 design, D12)

**38. Valeros, V., et al. (2026).** "Decoys Cannot Go Everywhere." arXiv:2606.27966. [#40] *(cross-referenced with #33 above)*
*What's drawn from it, specifically here:* the actual four-criterion structure — can a decoy exist, would an attacker reach it, does it yield useful signal, is it a reliable indicator — adapted directly into `formal-problem-definition.md` §4's Filter 1, now scored with AI assistance and human confirmation.

**39. Anonymous authors (2026).** "Uncovering Vulnerabilities of LLM-Assisted Cyber Threat Intelligence." arXiv:2509.23573. [#318]
*What's drawn from it:* direct evidence that standard LLM-as-a-judge classification is unreliable because models "tend to rationalize their own outputs" — the specific, named failure mode that justifies the human-confirmation gate in the plausibility-scoring-assist design as addressing a documented risk, not just being cautious by default.

**40. Anonymous authors.** "ChatGPT and Other Large Language Models for Cybersecurity of Smart Grid Applications." arXiv:2311.05462. [#320]
*What's drawn from it:* confirms LLM-assisted analysis has real precedent specifically in GOOSE/SV digital-substation communications (the same IEC 61850 domain as the Jay paper) — different task (anomaly detection, not plausibility scoring), but establishes this isn't a foreign application of LLMs to this domain.

---

## VIII. Testbed and evaluation-scale precedents (supports the methodology chapter's feasibility argument)

**41. Anonymous authors (2021).** "A Survey on Industrial Control System Testbeds and Datasets for Security Research." arXiv:2102.05631. [#220]
*What's drawn from it:* a dedicated survey of comparable ICS testbed designs (GRFICS, MiniCPS, and others) — direct support for the testbed architecture chapter, confirming this project's VMware/Kali/OpenPLC-class stack matches the standard toolkit used across a decade of published research, not an idiosyncratic choice.

**42. Multiple testbed papers, cited as a group** — VICSORT, AE3GIS, ICSSIM, Gotham Testbed, LICSTER (a representative sample; full list in `sources.md` #221–225). [#221–225]
*What's drawn from it:* confirmation that Purdue-model-segmented, GNS3/Docker-based virtualized OT testbeds are the field's standard approach at comparable scale (typically 1–2 PLCs, single HMI) — the direct evidentiary basis for D8's testbed-scope decision.

**43. Naval Postgraduate School thesis corpus (2015–2023), accessed via DTIC.** Representative: Dougherty, N. (2020). "Evasion of Honeypot Detection Mechanisms through Improved Interactivity of ICS-Based Systems." M.S. thesis. [#304]
*What's drawn from it:* a decade of comparable-scope graduate-level thesis work at a peer institution, none of which attempted formal placement optimization — cited as a scope-calibration benchmark (what's realistic for a graduate thesis in this space) and as a fourth independent confirmation of the novelty gap, from empirical rather than theoretical work.

---

## What didn't make this list, and why

Roughly 280 entries in `sources.md` aren't here. Most fall into one of three buckets, worth naming so the omission reads as deliberate rather than incomplete: **stepping stones** (papers found while chasing a citation-list trail that turned out not to be independently relevant — e.g., most of the Kamhoua-cluster bibliography beyond what's cited above); **unresolved sources** (🔴/🟡-marked entries where a full primary text was never confirmed, like the "Decoy Allocation Against Lateral Movement" paper still needing IEEE Xplore access); and **redundant confirmations** (several sources say the same thing as one already-cited source — citing all of them would pad the reference list without adding an argument). Pulling from any of these later is fine if a specific claim needs a specific new citation — this list is the strong, verified core, not a ceiling.
