# A17 structured search: the screening record

The record of how the 375 unique records from A17's ten runs were screened, under `01-search-protocol.md` §9–§11, and what each became. Decisions: D35. Runs: `sources.md` #405–#415; deduplication and the title stage: #416. D36 (15 November 2026) added the further paper-side runs, records 376–562 (§12–§13), and A29's patent arm, 1,394 publication numbers (§14–§17); their runs, outcome and protocol amendments are `sources.md` #613–#643. D38 (16 November 2026) added the widened re-run of block O: paper records 563–645 and run P1c's 102 publication numbers (§18); its amendment, runs and outcome are `sources.md` #990–#999.

- **Category:** Research. **Tier:** 💾 Offline, kept in the repository on your computer, not in Project Knowledge.
- **Depends on:** `01-search-protocol.md`, `sources.md` #405–#416 and #613–#643, D34.
- **Feeds into:** D35, D36 and D38; `sources.md` #417–#988 and #990–#1049; the Literature Review chapter and its search appendix (Phase E); A28's wording.
- **Record numbers** (1–562) are this file's own: 1–375 were assigned in alphabetical order of title at deduplication in the main search, and 376–562 the same way for the later runs (§13). They are not `sources.md` numbers, which always carry `#`. Patents are identified by publication number.
- **Status:** complete for A17 and A29 as the protocol fixed them (D35 for the main search; D36 for the recency check, IEEE Xplore, TechRxiv, forward citations and the patent arm, §12–§17). Only an update re-run remains (§11).

## 1. Counts at each stage

| Stage | In | Out |
|---|---|---|
| Ten runs, OpenAlex and Semantic Scholar, S1–S5 (#405–#415) | — | 758 records |
| Deduplication by DOI, then by normalised title within a year (#416) | 758 | 375 unique; no self-hits |
| **Title stage**: Claude's first pass, 5 November 2026; confirmed by the user, 8 November 2026 | 375 | A 82 to the abstract stage; K 5 already assessed; R 133 related by title (T1); X 155 excluded |
| **Abstract stage**: Claude, 8–11 November 2026 | 82 | 13 to full text; 61 T1; 3 excluded; 5 with no abstract obtained, judged on the title (T1) |
| **Full-text stage**: free copies only (D35) | 13 | 5 read: 2 T2, 3 T1. 8 not obtained: tier unresolved |
| **Tiers confirmed by the user**, 11 November 2026 | — | as below |

| Final outcome | Records |
|---|---|
| T3, threatens the claim | 0 |
| T2, narrows the claim | 2 (records 43 and 269) |
| T1, related | 202 (133 by title, 55 on the abstract, 8 on the full text, 5 on the title alone, 1 from an earlier entry) |
| Tier unresolved: full text not obtained | 8 (records 41, 89, 151, 160, 188, 288, 307, 333) |
| Assessed in earlier iterations, not re-tiered | 5 |
| Excluded | 158 (155 at the title stage, 3 at the abstract stage) |
| **Total** | **375** |

**Kept records: 217.** 24 were already in `sources.md` (§9). The other 193 have new entries, #417–#609, in the order of `sources.md` §YY. #610–#612 log the free-copy search, the queued backward-round candidates and one patent lead.

**After D36 (15 November 2026)** the paper-side totals are 562 records: T3 0, T2 2, T1 282, tier unresolved 10, assessed earlier 5, excluded 263 (§12). The patent arm adds 1,394 publication numbers: T3 0, T2 1 (proposed), related (T1) 712, excluded 681 (§14). *D37: the user confirmed the proposed T2 and ruled CN 121012683 A T2 (§15.2), so T2 2 and related (T1) 711.* *D38: the widened re-run adds paper records 563–645 and 102 patent publication numbers (§18), so the paper side counts 645 records: T3 0, T2 3, T1 293, tier unresolved 10, assessed earlier 5, excluded 334; and the patent arm 1,496: T3 0, T2 2, related (T1) 743, excluded 751.*

**Evidence at the abstract stage**, for the 82:
- 56 abstracts from the user's OpenAlex files;
- 8 from publisher pages and 1 from an author's page, fetched by Claude;
- 1 abstract the user supplied;
- 10 full texts read;
- 1 earlier `sources.md` entry;
- 5 not obtained.

**Who decided what.**
- Claude made every first pass: the title stage, the abstract stage, and the proposed tiers.
- The user confirmed:
  - the title stage, including the two exclusions that §9 reserves to the user (records 174 and 176), on 8 November 2026;
  - on 11 November 2026, "Park & Dagher T2. 269 T2. Ward T1. 368 T1. Rest confirmed.";
  - the free-only rule for full texts, on 10 November 2026 (D35).

## 2. How the tiers were applied

- **T3:** selects deception positions in a multi-zone OT/ICS network by optimising a stated objective, with zone or conduit structure and criticality as numeric inputs.
- **T2:** formal deception-placement optimisation in OT, ICS or CPS that lacks one of those elements, read as "lacks at least one"; or any placement optimisation that uses IEC 62443 zones as a numeric input.
- **T1:** everything else that is related.
- **No tier was given from an abstract alone** to a record that might be T2 or T3 (§11.1). Such records went to full text. The eight whose full text was not obtained keep an unresolved tier and are cited from their abstracts.

## 3. The two T2 works, clause by clause against A28's draft claim (§11.3)

**Record 43: Park, D. & Dagher, G. G. (2026), "Adaptive honeypot allocation in multi-attacker networks via Bayesian Stackelberg Games", *Computers & Security* 168, 104949 (#30, #192, #247, #272).** Version of record read in full on 8 November 2026, from the ScienceDirect page and the PDF the user supplied (open access, CC BY 4.0).

| A28's draft claim, clause | Park & Dagher |
|---|---|
| Selects deception positions | **Yes.** Honeypot subsets under a budget, as a mixed strategy re-optimised each round |
| Across a multi-zone OT/ICS architecture | **Partly.** Synthetic "Purdue-model" six-level graphs, in the scalability runs only; no OT assets |
| By maximising a stated composite objective under a decoy budget | **Partly.** A stated objective under a budget (defender expected utility: value-weighted interception minus honeypot cost), but not a multi-term composite |
| IEC 62443 zones and conduits as numeric inputs | **No.** The levels shape only the generated graphs and the candidate pruning ("level importance"), never the objective |
| Asset criticality as a numeric input | **Partly.** Target values, discounted by distance into node values, set the payoffs |
| Interception stage along ATT&CK-grounded paths as a scored term | **No.** Ten abstract exploit types, no ATT&CK; an interception is worth more nearer the target |
| Validated against random and centrality baselines | **Partly.** Random, yes. The others are greedy on node value, a one-step lookahead and tabular Q-learning; no centrality baseline |

**Record 269: Dong et al. (2025), "Multi-Layered Optimization for Adaptive Decoy Placement in Cyber-Resilient Power Systems Under Uncertain Attack Scenarios", *IET Renewable Power Generation* 19, e70078 (#417).** Read in full on 11 November 2026, from the PDF the user supplied (open access, CC BY).

| A28's draft claim, clause | Dong et al. |
|---|---|
| Selects deception positions | **Yes.** Binary decoy-node placement variables |
| Across a multi-zone OT/ICS architecture | **Partly.** A power distribution grid (modified IEEE 123-bus) with cyber and physical layers. Its "zones" are decoy coverage zones, not security zones |
| By maximising a stated composite objective under a decoy budget | **Yes.** The upper level of a three-level Stackelberg model trades resilience loss against operating cost and risk exposure, under an explicit budget constraint |
| IEC 62443 zones and conduits as numeric inputs | **No** |
| Asset criticality as a numeric input | **Yes.** Node weights combine load, topological significance and operational criticality |
| Interception stage along ATT&CK-grounded paths as a scored term | **No.** False-data-injection attacks, with attack vectors generated by a GAN; no ATT&CK, no interception-stage term |
| Validated against random and centrality baselines | **No.** Compared with statistical anomaly detection and "classical optimisation" |

**Effect, for both (D35).** Neither defeats the claim. Neither uses IEC 62443 zones and conduits as numeric inputs, nor ATT&CK-grounded paths with an interception-stage term, nor both random and centrality baselines.

Together they narrow it:
- **Budgeted decoy placement** with criticality-weighted, multi-term objectives exists for power CPS (Dong et al.).
- **Optimisation-based honeypot placement** has been evaluated on Purdue-style layered graphs (Park & Dagher).

The thesis cites both and states these differences.

**Baselines (§11.6).** Neither becomes one; D35 gives the reasons.

## 4. The full-text stage: 13 records

| Rec | Paper | Result | Entry |
|---|---|---|---|
| 43 | Park & Dagher, *Computers & Security* 168 (2026) | Read. **T2** | #192 |
| 269 | Dong et al., *IET Renewable Power Generation* 19 (2025) | Read. **T2** | #417 |
| 368 | Qu et al., *Electric Power Systems Research* 251 (2026), SSRN preprint read | Read. T1: honeypots shared in proportion to vulnerability or risk; no optimisation; degree-based and random comparisons | #432 |
| 290 | Tian et al., *IEEE Access* 8 (2020) | Read. T1: one honeypot per bus node; the game picks its mode | #317 |
| 72 | Sakata et al., *IEEE Access* 14 (2026) | Read. T1: PLC countermeasure selection under IEC 62443-4-2 security levels; no placement, no deception | #427 |
| 89 | Gong et al., *Reliability Eng. & System Safety* 278 (2027) | Not obtained: paywalled, no free copy. The closest abstract of the search | #419 |
| 333 | Asghar et al., GameSec 2025 | Not obtained: paywalled, no free copy | #425 |
| 151 | TI-DNDP, IEEE IFEEA 2025 | Not obtained: paywalled | #420 |
| 188 | HoneyCenter, *IEEE Trans. Computational Social Systems* (2026) | Not obtained: paywalled | #422 |
| 41 | Xiao et al., WASA 2024 | Not obtained: paywalled | #418 |
| 160 | AOQ attack graphs, *Int. J. Production Research* (2025) | Not obtained: paywalled | #421 |
| 288 | Barkatsa et al., *IEEE Trans. Consumer Electronics* (2026) | Not obtained: listed as open access, but not reachable by the user | #423 |
| 307 | MTD prioritisation, Stockholm University repository | Not obtained: free copy not reachable by the user | #424 |

## 5. Group A: the 82 records screened on their abstracts

*Title code:* the reason the title stage sent it on (P placement, G game/learning/optimisation, F framework, Z IEC 62443 or Purdue structure, U uninformative title). *Basis:* what the final tier was judged on. *Entry:* its `sources.md` entry.

| Rec | Year | Title | Identifier | Title code | Abstract-stage decision | Final tier | Basis | Entry | Reason |
|---|---|---|---|---|---|---|---|---|---|
| 11 | 2026 | A Decoy Placement Model for Engineering Workstations and Historian Systems in Manufacturing OT Networks | doi:10.5120/ijca54a0f5aecad7 | P | T1 | T1 | full text | #426 | Decoy placement in a manufacturing OT attack graph (26 nodes), evaluated by Monte Carlo against random, centrality, DMZ-heavy and asset-proximal placements. The placement is designed and argued, not optimised: optimisation is named as future work. IEC 62443 appears only in the references; no numeric criticality input. |
| 12 | 2025 | A Dynamic Deceptive Defense Framework for Zero-Day Attacks in IIoT: Integrating Stackelberg Game and Multi-Agent Distributed Deep Deterministic Policy Gradient | doi:10.32604/cmc.2025.069332 | G | T1 | T1 | abstract | #433 | Zero-day defence in IIoT: Stackelberg game plus multi-agent RL tunes packet sampling and deception timing. No honeypot positions. |
| 15 | 2014 | A framework for the design and deployment of a SCADA honeynet | doi:10.1145/2602087.2602110 | F | T1 | T1 | abstract | #434 | Design and deployment framework for a SCADA honeynet in the IMUNES simulator. No choice of positions. |
| 16 | 2024 | A Game Theoretic Framework for Multi Domain Cyber Deception | doi:10.1109/eurospw61312.2024.00056 | G | T1 | T1 | abstract | #435 | Game models for deception coordinated across cyber and physical layers. No network positions. |
| 39 | 2025 | Active cyber defense using intelligent agents in cloud-edge based applications | doi:10.32469/10355/110389 | U | T1 | T1 | abstract | #436 | Dissertation, cloud-edge critical infrastructure. Game-theoretic placement of honeypots, honeyfiles and honeytokens along ransomware kill-chain stages: when in the attack, not where in a network. Borderline T1. |
| 41 | 2024 | Active Defense Simulation Evaluation of Industrial Control Systems Based on Attack-Defense Graph | doi:10.1007/978-3-031-71467-2_26 | F | Full text | Unresolved | abstract only (full text not obtained) | #418 | ICS active defence evaluated on an attack-defence graph; simulates honeypot positions, and three honeypots spread across hierarchy levels beat three in one level (+24.4% time-to-compromise). No optimiser in the abstract, and 'hierarchy' is undefined. Probably T1, like Ward. Full text not obtained: paywalled (free-only rule). Cited from its abstract only. |
| 42 | 2026 | Adaptive Cyber Deception: Performance Evaluation of AI-Driven Strategies Against Traditional Honeypots | doi:10.1109/icpc2t68221.2026.11646292 | G | T1 | T1 | abstract | #437 | Adaptive CPS deception architecture (emulator, safety filter, RL). Its game layer chooses which services to expose, not where decoys go. |
| 43 | 2026 | Adaptive honeypot allocation in multi-attacker networks via Bayesian Stackelberg Games | doi:10.1016/j.cose.2026.104949 | P | Full text | **T2** | full text | #30, #192, #247, #272 | Published version read in full (open access, from the page and PDF the user supplied). Its 'Purdue' structure is a synthetic six-level graph generator used in the scalability runs, and 'level importance' only sets how many candidates the pruning keeps per level. No IEC 62443, zones, conduits or ATT&CK. Target values feed the payoffs. Baselines: greedy, random, one-step lookahead, Q-learning; no centrality. |
| 44 | 2024 | Adaptive Honeypot Defense Deployment: A Stackelberg Game Approach with Decentralized DRL for AMI Protection | doi:10.1109/icnc59896.2024.10556285 | P | T1 | T1 | abstract | #438 | AMI honeypot deployment as a Stackelberg game among power suppliers (multi-agent RL): incentives and task allocation, not network positions. |
| 55 | 2025 | AI-Driven Deception Systems for Advanced Persistent Threat (APT) Mitigation | doi:10.1109/gcat66372.2025.11368570 | U | T1 | T1 | abstract | #439 | AI-driven deception engine against APTs in enterprise networks. |
| 64 | 2019 | An SDN-Enabled Pseudo-Honeypot Strategy for Distributed Denial of Service Attacks in Industrial Internet of Things | doi:10.1109/tii.2019.2917912 | G | T1 | T1 | abstract | #440 | Pseudo-honeypot game against DDoS on SDN-managed IIoT; equilibrium strategies, not positions. |
| 65 | 2025 | Analysis and Optimization of Processes for Integrating Smart Grid Objects into the Critical Infrastructure Cyber Protection System | doi:10.1109/khpiweek61436.2025.11288406 | Z | T1 | T1 | abstract | #441 | Smart-grid security investment: anomaly detection mapped to ATT&CK for ICS and IEC 62443-3-3, with a Gordon-Loeb budget model. No deception and no placement. |
| 68 | 2020 | Anti-Honeypot Enabled Optimal Attack Strategy for Industrial Cyber-Physical Systems | doi:10.1109/ojcs.2020.3030825 | G | T1 | T1 | abstract | #343 | Attacker-side: an optimal strategy against honeypot-protected industrial CPS. |
| 70 | 2026 | Attack-Defense Game Modeling on Complex Networks under Asymmetric Topological Information | doi:10.2139/ssrn.7022022 | G | Abstract not obtained | T1 | title only (abstract not obtained) | #483 | Attack-defence game on complex networks under asymmetric topology information (SSRN). Abstract not reachable. |
| 72 | 2026 | Automated Design of Countermeasures for ICS Based on Security Standards | doi:10.1109/access.2026.3696839 | Z | Full text | T1 | full text | #427 | Full text read. A 0-1 integer program that picks countermeasure features for a PLC under IEC 62443-4-2 security levels and memory and OS limits, with ATT&CK for ICS mapped to the requirements. It uses IEC 62443 levels as numbers, but for one device's features: no zones, conduits, network placement or deception. Worth citing where the thesis uses SL-T vectors. |
| 74 | 2025 | Automatic Expansion and Contraction of Trapping Resources Based on Electric Power Environment | doi:10.1109/iccea65460.2025.11103308 | P | T1 | T1 | abstract | #442 | Kubernetes controller that scales honeypot containers in power networks. Resource scaling, not positions. |
| 77 | 2025 | Balancing Defence and Operational Stability: Resilience-Oriented Reinforcement Learning for Autonomous Critical Infrastructure Cyber Defence | doi:10.1109/rivf68649.2025.11365238 | G | T1 | T1 | abstract | #443 | RL agent for critical infrastructure that chooses when to use high- or low-fidelity honeypots under a resilience reward. Not positions. Borderline T1. |
| 87 | 2026 | Co-ADAM: a co-evolutionary signaling game framework for equilibrium cyber deception in industrial IoT | doi:10.1038/s41598-026-60920-0 | G | T1 | T1 | abstract | #444 | Co-ADAM: how much to invest in deception in IIoT (constrained MDP with a signalling game). An investment level, not positions. |
| 89 | 2026 | Consequence-driven active defense resource allocation for chemical park cyber-physical systems | doi:10.1016/j.ress.2026.113562 | P | Full text | Unresolved | abstract only (full text not obtained) | #419 | Chemical-park ICS in three layers (information, cyber-physical, physical). Attack graphs quantify cross-layer paths, Bayesian networks infer physical consequence severity, and a coupling index ranks nodes under a budget. Honeypot deployment comes from an attack-defence game solved greedily, validated on a real water-tank rig (S7-1200) and the Tennessee Eastman Process. The introduction rejects degree, closeness and betweenness placement. Full text not obtained: paywalled, no free copy (free-only rule). Cited from its abstract only. |
| 90 | 2015 | Constructing Cost-Effective and Targetable ICS Honeypots Suited for Production Networks | OpenAlex W618946352 | P | T1 | T1 | abstract | #445 | Honeyd+: many decoy PLCs proxied to one real PLC. Construction, not positions. |
| 94 | 2021 | Contract-Based Incentive Mechanisms for Honeypot Defense in Advanced Metering Infrastructure | doi:10.1109/tsg.2021.3071513 | G | T1 | T1 | abstract | #446 | Contract theory to make suppliers deploy AMI honeypots and share data honestly. |
| 107 | 2014 | Cyber-Physical System Security With Deceptive Virtual Hosts for Industrial Control Networks | doi:10.1109/tii.2014.2304633 | F | T1 | T1 | abstract | #300 | Self-configuring virtual honeypots that copy observed ICS hosts (Honeyd plus Ettercap). |
| 117 | 2020 | Decepti-SCADA: A cyber deception framework for active defense of networked critical infrastructures | doi:10.1016/j.iot.2020.100320 | F | T1 | T1 | earlier entry | #13 | Decepti-SCADA: decoy generation for SCADA with manual, GUI-driven placement (assessed in #13; abstract not re-fetched). |
| 118 | 2026 | Deception Architecture for Water and Wastewater Operational Technology Environments | doi:10.5281/zenodo.20745399 | F | T1 | T1 | abstract | #57 | Ward: a reference architecture mapping decoys, honey credentials and lures to water-utility zones. Design science, qualitative. |
| 121 | 2024 | Decoding the Human Element in APT Attacks: Unveiling Attention Diversion Techniques in Cyber-Physical System Security | doi:10.1007/978-3-031-61382-1_1 | Z | Abstract not obtained | T1 | title only (abstract not obtained) | #484 | Attention-diversion techniques in CPS against APTs (Springer). Abstract not reachable. |
| 122 | 2026 | Decoy-Assisted Detection Metrics for Manufacturing Operational Technology Networks | doi:10.29322/ijsrp.16.06.2026.p17419 | F | T1 | T1 | abstract | #447 | Ward: a metrics model for decoy-assisted detection in manufacturing OT. Relevant to evaluation, not placement. |
| 123 | 2020 | Decoy-based Moving Target defense Against Cyber-physical Attacks On Smart Grid | doi:10.1109/epec48502.2020.9320029 | P | T1 | T1 | abstract | #448 | Moving-target defence for smart grids with simulated decoy system models in the control loop; 'decoy' in a control sense. |
| 126 | 2026 | Defending against multiple IIoT attackers using hybrid hypergame-reinforcement learning with ML-enhanced beliefs | doi:10.1007/s00521-026-12220-x | G | Abstract not obtained | T1 | title only (abstract not obtained) | #485 | Hypergame plus RL against multiple IIoT attackers (Springer NCA 2026). Abstract not reachable. |
| 129 | 2019 | Defense Strategies Against Network Attacks in Cyber-Physical Systems with Analysis Cost Constraint Based on Honeypot Game Model | doi:10.32604/cmc.2019.05290 | G | T1 | T1 | abstract | #449 | Honeypot game for CPS that splits a limited analysis budget between low- and high-interaction honeypots. Not positions. |
| 135 | 2025 | Design and Deployment of Deception-Based Honeypot Systems for Early Detection of Advanced Persistent Threats | doi:10.1109/icrera66237.2025.11283915 | P | T1 | T1 | abstract | #450 | Hierarchical honeypots in segmented zones, with ML analytics, for early APT detection. An architecture. |
| 138 | 2021 | Design Considerations for Distributed Energy Resource Honeypots and Canaries | doi:10.2172/1821540 | F | T1 | T1 | abstract | #451 | Design considerations for DER honeypots and canaries (Sandia report). |
| 150 | 2019 | Dynamic Bayesian Games for Adversarial and Defensive Cyber Deception | doi:10.1007/978-3-030-02110-8_5 | G | T1 | T1 | abstract | #452 | Huang and Zhu: static, signalling and multi-stage Bayesian games of deception (book chapter). Not positions. |
| 151 | 2025 | Dynamic Deployment Strategy of Decoy Nodes in High-Risk Network Segments Based on Cyber Threat Intelligence | doi:10.1109/ifeea66847.2025.11388193 | P | Full text | Unresolved | abstract only (full text not obtained) | #420 | TI-DNDP: threat intelligence plus game theory and RL to 'optimise honeypot placement' in high-risk segments of cyber-physical power systems. Full text not obtained: paywalled (free-only rule). Cited from its abstract only. |
| 160 | 2025 | Enhancing the security of reconfigurable cyber-physical supply chains: reconstructing vulnerable attack paths using AND/OR/QUORUM graphs | doi:10.1080/00207543.2025.2608292 | U | Full text | Unresolved | abstract only (full text not obtained) | #421 | AND/OR/QUORUM attack graphs for cyber-physical supply chains: extracts the most vulnerable paths, then hardens components and deploys a honeypot on them. Full text not obtained: paywalled (free-only rule). Cited from its abstract only. |
| 162 | 2026 | Evaluating ICS honeypot attractiveness: The role of interaction level, network type, and geolocation | doi:10.1016/j.ijcip.2026.100898 | P | T1 | T1 | abstract | #453 | How interaction level, network type and location affect ICS honeypot attractiveness (16 internet-facing honeypots, three months). |
| 178 | 2020 | Game Theoretic Honeypot Deployment in Smart Grid | doi:10.3390/s20154199 | P | T1 | T1 | abstract | #317 | Smart-grid honeypot game choosing how many honeypots versus real devices. A count, not positions. |
| 179 | 2025 | Game-Theoretic and Machine Learning-based Defensive Deception for Dependable and Secure Cyber-Physical Systems | OpenAlex W7112107853 | G | T1 | T1 | abstract | #454 | Dissertation on game-theoretic and ML defensive deception for CPS (Foureye, Honey Drones). |
| 180 | 2024 | Generative AI and Gametheory for the development and deployment of Honeypots to enhance the Security of Industrial Automation and Control Systems | doi:10.18420/inf2024_165 | P | T1 | T1 | full text | #428 | Generative-AI honeypots for IACS plus a small game: the defender picks 0, 1 or 2 honeypots, solved by a payoff table. No positions, no optimisation, no evaluation. |
| 188 | 2026 | HoneyCenter: An Intelligent Honeypoint IP Mutation Strategy Optimization Based on Multiagent Reinforcement Learning | doi:10.1109/tcss.2026.3658002 | G | Full text | Unresolved | abstract only (full text not obtained) | #422 | HoneyCenter: zero-sum game solved by minimax Q-learning, choosing which host the honeypoint's IP moves to, in smart-grid and ICS settings. Full text not obtained: paywalled (free-only rule). Cited from its abstract only. |
| 190 | 2026 | Honeyfarm: AI-Based Honeypots for Industrial OPC UA Communication via an On-Demand Deployment Architecture | doi:10.1007/978-3-032-35576-8_22 | P | T1 | T1 | abstract | #455 | Honeyfarm: on-demand OPC UA honeypots that take over rerouted attacker traffic; names usable points in the Purdue model, qualitatively. |
| 192 | 2024 | Honeynet Module Simulation and Dynamic Configuration of Honeypots Based on Online Learning | doi:10.1007/978-981-97-1010-2_9 | G | Abstract not obtained | T1 | title only (abstract not obtained) | #486 | Honeynet simulation and online-learning configuration of honeypots (Springer). Abstract not reachable. |
| 197 | 2023 | Honeypot Based Industrial Threat Detection Using Game Theory in Cyber-Physical System | doi:10.1007/s10723-023-09689-4 | G | T1 | T1 | abstract | #316 | Attack detection for industrial CPS with honeypots (Stackelberg game plus RL), on DDoS and MITM. Not placement; confirms #316's guess. |
| 198 | 2021 | Honeypot Detection Strategy Against Advanced Persistent Threats in Industrial Internet of Things: A Prospect Theoretic Game | doi:10.1109/jiot.2021.3080527 | G | T1 | T1 | abstract | #456 | Bounded-rationality honeypot-APT game on SDN-managed IIoT; choice of collection and analysis periods. |
| 199 | 2018 | Honeypot Game Strategy for Distributed Denial of Service in Advanced Metering Infrastructure | Semantic Scholar d820ce59f277058062573db214b0079742b5b078 | G | T1 | T1 | full text | #429 | Honeypot strategy against DDoS in AMI, compared with two monitoring models; no placement rule. Read in full through the fetch tool. |
| 200 | 2019 | Honeypot game‐theoretical model for defending against APT attacks with limited resources in cyber‐physical systems | doi:10.4218/etrij.2019-0152 | P | T1 | T1 | abstract | #457 | Honeypot game for APTs in CPS with low- and high-interaction modes and allocation costs. Equilibrium strategies, not positions. |
| 201 | 2019 | Honeypot Type Selection Games for Smart Grid Networks | doi:10.1007/978-3-030-32430-8_6 | P | T1 | T1 | abstract | #458 | Boumkheld et al.: Bayesian game choosing the honeypot type (low, high or none) in smart-grid AMI. |
| 202 | 2021 | Honeypot-Enabled Optimal Defense Strategy Selection for Smart Grids | doi:10.1109/globecom46510.2021.9685397 | G | T1 | T1 | abstract | #459 | Stochastic game selecting a smart-grid defence strategy, with honeypots among the options. |
| 204 | 2020 | Honeypots for Automatic Network-Level Industrial Control System Security | OpenAlex W3017025980 | F | T1 | T1 | abstract | #460 | Doctoral proposal: ICS honeypots at mixed interaction levels with SDN reconfiguration. |
| 220 | 2026 | IEC 62443 Wireless Security: Deploying OT Wireless Controllers in Industrial Factory Networks | doi:10.5281/zenodo.19428490 | Z | Exclude | Excluded | abstract | — | Deployment guide for IEC 62443-aligned wireless LAN controllers. No deception and no optimisation. |
| 226 | 2026 | Incentive-Driven Honeypot Defense: A Multi-Agent DRL Framework for Securing Smart Grid Networks | doi:10.1109/tnsm.2026.3715400 | G | T1 | T1 | abstract | #461 | AMI honeypot service allocation among suppliers (Stackelberg game, multi-agent RL). Incentives, not positions. |
| 230 | 2026 | Industrial Cloud-Native Proactive Defense: A Dynamic Cyber Deception Orchestration Framework for IIoT Services | doi:10.1109/tii.2026.3740984 | F | T1 | T1 | abstract | #462 | Cloud-hosted IIoT decoys made to look local by emulating hop counts and delays. Fidelity, not positions. |
| 247 | 2021 | Last Line of Defense: Reliability Through Inducing Cyber Threat Hunting With Deception in SCADA Networks | doi:10.1109/access.2021.3111420 | F | T1 | T1 | abstract | #463 | Threat hunting with a decoy farm in a SCADA network. |
| 259 | 2025 | Metrics-Driven Evaluation and Optimization of Honeypots: Toward Standardized Measures of Deception Effectiveness | doi:10.12700/aph.22.12.2025.12.19 | G | T1 | T1 | abstract | #464 | Metrics framework for evaluating honeypots (five dimensions, composite scores). |
| 261 | 2026 | Mitigating the Lateral Movement of APT in IIoT With an Efficient Moving Target Defense and Cyber Deception Approach | doi:10.1109/tr.2026.3685261 | P | T1 | T1 | abstract | #465 | Moving-target defence plus deception against lateral movement in IIoT (Stackelberg game with prospect theory, subnet shuffling). Optimises a defence policy, not decoy positions. Borderline T1. |
| 263 | 2024 | MLNT: A Multi-Level Network Traps Deployment Method | doi:10.1109/cscwd61410.2024.10580355 | P | T1 | T1 | abstract | #466 | MLNT: layered network traps (ports, nodes, security domains) built on FPGA. An architecture, not an optimisation. |
| 264 | 2024 | Modeling a ransomware attack : a game-theoretic exploration of strategic interplay between attacker and defender | doi:10.32469/10355/104992 | U | T1 | T1 | abstract | #467 | Thesis: deception resources across ransomware stages, as an extensive-form game. When, not where. |
| 265 | 2011 | Monitoring critical infrastructure assets and strategic signaling to deter aggression in cyberspace | OpenAlex W2467403741 | G | Exclude | Excluded | abstract | — | Legal and policy study (a government honeynet at a private utility, deterrence signalling). No technical deception content. |
| 269 | 2025 | Multi‐Layered Optimization for Adaptive Decoy Placement in Cyber‐Resilient Power Systems Under Uncertain Attack Scenarios | doi:10.1049/rpg2.70078 | P | Full text | **T2** | full text | #417 | Full text read (open access). A three-level optimisation that decides, node by node, where decoy nodes go under a budget (binary placement variables), with node weights for load, topology and operational criticality; IEEE 123-bus distribution grid. Its 'zones' are decoy coverage zones, not IEC 62443 zones. No ATT&CK. Compared with anomaly detection and 'classical optimisation', not with centrality or random. |
| 270 | 2026 | Network and Device Level Cyber Deception for Contested Environments Using RL and LLMs | doi:10.48550/arxiv.2603.17272 | G | T1 | T1 | abstract | #468 | Review of RL- and LLM-based network and device deception, including OT. |
| 271 | 2018 | Network Softwarization for IACS Security Applications | Semantic Scholar 3d06d816e066172911c13423228ef5278b5882bb | Z | T1 | T1 | full text | #430 | Master's dissertation: SDN/NFV architecture for IACS security probes, including a virtual honeypot. No placement method; no IEC 62443. Read through the fetch tool (first fifth). |
| 278 | 2026 | Operationalizing Deception Technology in ICS/OiticaT: A Control Mapping Framework for Crl Infrastructure Cybersecurity | doi:10.35940/ijsce.c3723.16030726 | Z | T1 | T1 | abstract | #469 | Ward: control mapping of ICS/OT deception to NIST, IEC 62443-2-1, CISA and ATT&CK for ICS. |
| 279 | 2025 | Optimal Honeypot Ratio and Convergent Fictitious-Play Learning in Signaling Games for CPS Defense | doi:10.48550/arxiv.2507.11113 | P | T1 | T1 | abstract | #470 | Signalling game giving the optimal share of honeypots in a CPS. A ratio, not positions. |
| 288 | 2026 | Proactive Cyber Deception in Attack Graphs: A Risk-aware Deployment Framework | doi:10.1109/tce.2026.3714285 | P | Full text | Unresolved | abstract only (full text not obtained) | #423 | Honeypot deployment plus edge changes on a multi-stage attack graph under a budget, with a prospect-theory utility, solved by a genetic algorithm; networked CPS (IEEE Trans. Consumer Electronics 2026). Full text not obtained: listed as open access, but the user could not reach the PDF. Cited from its abstract only. |
| 290 | 2020 | Prospect Theoretic Study of Honeypot Defense Against Advanced Persistent Threats in Power Grid | doi:10.1109/access.2020.2984795 | G | Full text | T1 | full text | #317 | Full text read. Every bus node gets a honeypot; the game only picks high- or low-interaction mode per node, using node values from electrical centrality. No choice of positions. |
| 291 | 2026 | PURITY: An Industry-Standard-Based Security Framework for IT-OT Convergence | doi:10.1109/access.2026.3682366 | Z | Exclude | Excluded | abstract | — | PURITY: maps standards' controls onto Purdue levels for SMEs. No deception and no formal optimisation. |
| 297 | 2026 | QuantumGuard: A Post-Quantum Resilient Deception-Driven Framework for Proactive Threat Hunting and Cognitive Honeynet Orchestration in 6G-Enabled Cyber-Physical Systems | doi:10.14569/ijacsa.2026.0170694 | U | T1 | T1 | abstract | #471 | QuantumGuard: post-quantum deception framework for 6G CPS. |
| 298 | 2026 | Reinforcement Learning-Driven Honeypots: Tactic-Based Defense for Industrial Control Systems | doi:10.1109/tmlcn.2026.3684465 | G | T1 | T1 | abstract | #472 | RL-driven ICS honeypot that shapes responses by ATT&CK for ICS tactic. |
| 302 | 2023 | Research on the Application of Deception Defense Technology in Smart Grid | doi:10.1109/icips59254.2023.10404573 | F | T1 | T1 | abstract | #473 | Review of deception defence in smart grids. |
| 303 | 2019 | Resilient Control Systems | doi:10.1109/rws47064.2019.8971995 | U | Abstract not obtained | T1 | title only (abstract not obtained) | #487 | 'Resilient Control Systems' (IEEE RWS 2019): the title gives nothing. Abstract not reachable. |
| 307 | 2026 | Risk-Based Asset Prioritization for Moving Target Defense in Critical Infrastructure | OpenAlex W7204153552 | Z | Full text | Unresolved | abstract only (full text not obtained) | #424 | Ranks critical-infrastructure IT components for moving-target defence, 'aligned with IEC 62443 Security Levels 2-3'. Stockholm University repository (DiVA), apparently a thesis. Full text not obtained: free repository copy, but the user could not reach it. Cited from its abstract only. |
| 311 | 2018 | Secure Cyber Deception Architecture and Decoy Injection to Mitigate the Insider Threat | doi:10.3390/sym10010014 | P | T1 | T1 | abstract | #474 | Dynamic host mutation with decoy injection against insiders. |
| 316 | 2025 | Securing Industrial Control Systems: PLC, SCADA, and HMI Protection | doi:10.1109/icspc68261.2025.11326487 | Z | T1 | T1 | abstract | #475 | ICS defence in depth, with a SCADA honeypot case. |
| 320 | 2026 | Self-adaptive cyber deception and resilient network defense via adversarial environment simulation | doi:10.1038/s41598-026-59245-9 | G | T1 | T1 | abstract | #476 | Self-adaptive deception trained against GAN-generated attacks (DRL). |
| 329 | 2026 | Stackelberg Games for the “Active Deception” Strategy in the Process of Critical Infrastructure Migration to Post-Quantum Cryptography | doi:10.3390/jcp6050143 | G | T1 | T1 | abstract | #477 | Stackelberg game splitting budget between post-quantum migration and decoy infrastructure. A budget split, not positions. |
| 332 | 2020 | Stochastic games for power grid coordinated defence against coordinated attacks | doi:10.1049/iet-cps.2020.0002 | G | T1 | T1 | abstract | #478 | Stochastic game for coordinated power-grid defence (honeypot plus 'weakening vision'), IEEE 14-bus. |
| 333 | 2025 | Strategic Defense Allocation in Cyber-Physical Sensor Systems Under Dual-Domain Attacks | doi:10.1007/978-3-032-08067-7_5 | P | Full text | Unresolved | abstract only (full text not obtained) | #425 | Asghar, Hemida, Kamhoua and Kleinberg (GameSec 2025): the defender places honeypots on cyber access points and physically protects a subset of sensors; double oracle with a greedy oracle that carries a submodular constant-factor guarantee. No zones or criticality in the abstract. Full text not obtained: paywalled, no free copy (free-only rule). Cited from its abstract only. |
| 334 | 2017 | Strategic Honeypot Game Model for Distributed Denial of Service Attacks in the Smart Grid | doi:10.1109/tsg.2017.2670144 | G | T1 | T1 | abstract | #479 | Honeypot game against DDoS in AMI, on a testbed. |
| 337 | 2021 | Study on the intelligent honeynet model for containing the spread of industrial viruses | doi:10.1016/j.cose.2021.102460 | P | T1 | T1 | abstract | #480 | Epidemic model of an 'intelligent honeynet' containing industrial viruses in SCADA; stability analysis. No placement. Abstract read on Prof. Yu Yao's publication page (Northeastern University), not the publisher's. |
| 355 | 2022 | Towards Optimized Security Attributes for IoT Devices in Smart Agriculture Based on the IEC 62443 Security Standard | doi:10.3390/app12115653 | Z | T1 | T1 | full text | #431 | Shaaban et al.: removes redundant security attributes across IoT components in a THREATGET model. IEC 62443 zones and levels are background only, not numbers; no deception. Read in full through the fetch tool. |
| 358 | 2024 | Trapping resource orchestration scheme based on electric power environment | doi:10.1109/dsc63484.2024.00072 | P | T1 | T1 | abstract | #481 | Kubernetes scheduler for honeypots in power networks. |
| 368 | 2025 | Vulnerability-based and Risk-Aware Honeynet Deployment Framework in Cyber-Physical Power Systems | doi:10.1016/j.epsr.2025.112247 | P | Full text | T1 | full text | #432 | Full text read (free SSRN preprint of the journal paper). Shares a fixed number of honeypots across nodes in proportion to a vulnerability score (static: H_i = M x V_i / sum V) or to changes in a risk score (dynamic). No objective is optimised. Compared with degree-based and random allocation on IEEE 118-bus. |
| 373 | 2026 | ZONING, CONDUITING AND SUBNETTING ARCHITECTURE FOR INDUSTRIAL CONTROL SYSTEMS | doi:10.5281/zenodo.19372328 | Z | T1 | T1 | abstract | #482 | Engineering method for ICS zoning, conduits and subnetting, aligned with IEC 62443 and IEC 61511. No deception; background for the zone model. |

## 6. Group K: 5 records already assessed in earlier iterations, not re-screened

| Rec | Year | Title | Identifier | Entry and earlier assessment |
|---|---|---|---|---|
| 19 | 2023 | A hybrid cyber defense framework for reconnaissance attack in industrial control systems | doi:10.1016/j.cose.2023.103506 | #240, #271: method read; not placement optimisation |
| 113 | 2025 | D3O-IIoT: deep reinforcement learning-driven dynamic deception orchestration for industrial IoT security | doi:10.1038/s41598-025-33426-4 | #250, #324: read in full |
| 119 | 2023 | Deception Technology Based Intrusion Protection and Detection Mechanism for Digital Substations: A Game Theoretical Approach | doi:10.1109/access.2023.3279504 | #305: the closest prior work (D7); read in full |
| 120 | 2020 | DecIED: Scalable k-Anonymous Deception for IEC61850-Compliant Smart Grid Systems | doi:10.1145/3384941.3409592 | #11 |
| 262 | 2022 | MITRE ATT&CK Based Evaluation on In-Network Deception Technology for Modernized Electrical Substation Systems | doi:10.3390/su14031256 | #12 |

## 7. Group R: 133 records related by title (T1), not screened further

| Rec | Year | Title | Identifier | Entry |
|---|---|---|---|---|
| 1 | 2026 | "Synchronized Network and Process Telemetry Dataset from an Industrial Oil-Pipeline Honeypot Testbed" | doi:10.21227/3nmn-tz65 | #488 |
| 6 | 2025 | A Comparative Study of ICS Honeypot Deployments | doi:10.1007/978-3-032-16165-9_8 | #489 |
| 8 | 2025 | A Cyber-Twin Based Honeypot for Gathering Threat Intelligence of Critical Infrastructure | doi:10.1145/3806008.3811698 | #490 |
| 10 | 2026 | A Deception Readiness Index for ICS and OT Cybersecurity Programs | doi:10.22214/ijraset.2026.83810 | #491 |
| 13 | 2015 | A Flexible Architecture for Industrial Control System Honeypots | doi:10.5220/0005522500160026 | #492 |
| 17 | 2017 | A Game-theoretic Taxonomy and Survey of Defensive Deception for Cybersecurity and Privacy | doi:10.1145/3337772 | #493 |
| 18 | 2023 | A GAN-based security strategy for WSN networks based on honeypot algorithm | doi:10.1016/j.phycom.2023.102260 | #494 |
| 23 | 2022 | A Novel IDS Securing Industrial Control System of Critical Infrastructure Using Deception Technology | doi:10.4018/ijdcf.302874 | #495 |
| 24 | 2025 | A novel worm propagation model based on SDN dynamic honeypots | doi:10.1504/ijics.2025.10073162 | #496 |
| 25 | 2026 | A Physics-Aware, Cross-Layer ICS Honeypot for Purdue Level 2 Operational Technology Networks Poster | doi:10.13140/rg.2.2.34718.91201 | #497 |
| 30 | 2017 | A research for high interactive honepot based on industrial service | doi:10.1109/compcomm.2017.8323069 | #498 |
| 31 | 2025 | A Resilient Dual-Purpose Web Honeypot for Analyzing Attacks on Industrial Control Systems | doi:10.24251/hicss.2025.836 | #499 |
| 32 | 2020 | A Scalable High-interaction Physical Honeypot Framework for Programmable Logic Controller | doi:10.1109/vtc2020-fall49728.2020.9348483 | #500 |
| 33 | 2015 | A Scalable Honeynet Architecture for Industrial Control Systems | doi:10.1007/978-3-319-30222-5_9 | #501 |
| 34 | 2026 | A Scalable Real-Time Intrusion Detection System Using Honeypots and Hybrid Machine Learning Pipelines | doi:10.1109/conecct68978.2026.11700758 | #502 |
| 35 | 2024 | A Simulation Method for Industrial Control Honeynet Based on Time Series Prediction | doi:10.1109/ispds62779.2024.10667509 | #503 |
| 40 | 2016 | Active Defence Using an Operational Technology Honeypot | doi:10.1049/cp.2016.0860 | #504 |
| 45 | 2025 | Adaptive MQTT Honeypots for IIoT Security Using Extended Mealy Machines | doi:10.1007/978-3-032-13714-2_28 | #505 |
| 46 | 2025 | Adaptive SSH Honeypot for Power Monitoring Systems: A Synergistic Approach Combining Reinforcement Learning and Large Language Models | doi:10.1109/isaics66888.2025.11350169 | #506 |
| 51 | 2026 | Aegis-Edge: Gated Agentic Cyber Defense with Deception-Oriented Control for IoT/IIoT Edge Systems | doi:10.55041/ijcope.v2i5.262 | #507 |
| 53 | 2026 | AI Adoption in Pipeline Security Monitoring: A Systematic Review of AIoT-Driven Honey Frameworks | doi:10.1109/imcom69009.2026.11360947 | #508 |
| 54 | 2026 | AI Vs. AI: Generative Adversarial Networks (Gans) for Dynamic Honeypot Generation in Next-Generation Cyber Defense | doi:10.55041/ijsmt.v2i4.645 | #509 |
| 56 | 2023 | AMINet: An Industrial Honeynet for AMI Systems | doi:10.1109/bigdata59044.2023.10386375 | #510 |
| 58 | 2011 | An exploration of defensive deception in industrial communication networks | doi:10.1016/j.ijcip.2011.06.002 | #511 |
| 60 | 2021 | An ICS Honeynet for Detecting and Analyzing Cyberattacks in Industrial Plants | doi:10.1109/icecet52533.2021.9698746 | #512 |
| 61 | 2018 | An Improved ICS Honeypot Based on SNAP7 and IMUNES | doi:10.1007/978-3-030-00006-6_27 | #513 |
| 63 | 2018 | An intrusion detection method based on log sequence clustering of honeypot for Modbus TCP protocol | doi:10.1109/icasi.2018.8394581 | #514 |
| 66 | 2021 | Analysis of Conpot and Its BACnet Features for Cyber-Deception | doi:10.1007/978-3-030-71017-0_23 | #515 |
| 69 | 2026 | Application of Cyber Deceptive Technology to Strengthen Defense Industry Technology Protection | doi:10.5762/kais.2026.27.5.437 | #516 |
| 73 | 2025 | Automated Generation of Configurable, High-Fidelity, Smart Grid Honeynet | doi:10.1109/smartgridcomm65349.2025.11204583 | #517 |
| 78 | 2025 | Blockchain-Backed ML-Based Zero-Trust Honeypot for Forensic-Ready Cyber-Physical System Security in Industry X | doi:10.51846/jcsa.v2i2.4636 | #518 |
| 81 | 2019 | Characterizing Background Noise in ICS Traffic Through a Set of Low Interaction Honeypots | doi:10.1145/3338499.3357361 | #519 |
| 83 | 2025 | Characterizing Large-Scale Adversarial Activities Through Large-Scale Honey-Nets | doi:10.1109/uemcon67449.2025.11267576; doi:10.48550/arxiv.2512.06557 | #520 |
| 84 | 2025 | Characterizing Network Threats Against Industrial Control Systems Using Honeypot Technology | doi:10.1109/nana66698.2025.00078 | #521 |
| 91 | 2025 | Containerized Cozenage: Exploring the Effectiveness of High Interaction ICS Honeypot Containers | doi:10.24251/hicss.2025.133 | #522 |
| 101 | 2025 | Cyber Deception Across Domains: A Comprehensive Survey of Techniques, Challenges, and Perspectives | doi:10.14569/ijacsa.2025.0160792 | #42 |
| 104 | 2018 | Cyber Security Threats Targeting CPS Systems: A Novel Approach Using Honeypot | Semantic Scholar e691e257a617acde8c448cbd7f41ff670a877f4b | #523 |
| 105 | 2025 | Cyber-Physical Deception Through Coordinated IoT Honeypots | Semantic Scholar 0ecc62168ab9faa550945e5f2b39cb55a2788511 | #524 |
| 106 | 2015 | CYBER-PHYSICAL SYSTEM SECURITY USING DECOY SYSTEM | Semantic Scholar 78a058bd565b198e975793716a459f9e7ac2c303 | #525 |
| 130 | 2020 | DefRec: Establishing Physical Function Virtualization to Disrupt Reconnaissance of Power Grids' Cyber-Physical Infrastructures | doi:10.14722/ndss.2020.24365 | #526 |
| 132 | 2020 | DEPLOYING AN ICS HONEYPOT IN A CLOUD COMPUTING ENVIRONMENT AND COMPARATIVELY ANALYZING RESULTS AGAINST PHYSICAL NETWORK DEPLOYMENT | OpenAlex W3137173487 | #527 |
| 133 | 2021 | DEPLOYING AND ANALYZING CONTAINERIZED HONEYPOTS IN THE CLOUD WITH T-POT | OpenAlex W7112467617 | #528 |
| 134 | 2018 | Deployment of IoT-based honeynet model | doi:10.1145/3301551.3301586 | #529 |
| 136 | 2026 | Design and Implementation of an IoT Honeypot System for Real-Time Cyber Threat Monitoring and Analysis | doi:10.25258/ijddt.16.61s.189 | #530 |
| 142 | 2025 | Detection of False Data Injection Attacks in Smart Grid: A Honeypot-Based End-Edge-Cloud Collaborative Approach | doi:10.1109/icpre67300.2025.11273941 | #531 |
| 144 | 2023 | DEVELOPING A DUAL-PURPOSE WEB HONEYPOT FOR CHARACTERIZING ATTACKS ON A SIMULATED POWER GRID | OpenAlex W7112796430 | #532 |
| 145 | 2024 | Development of Proactive Cyber Security System using Azure Honeynet Platform | doi:10.1109/ariia63345.2024.11051894 | #533 |
| 146 | 2015 | Did you really hack a nuclear power plant? An industrial control mobile honeypot | doi:10.1109/cns.2015.7346907 | #534 |
| 149 | 2021 | Don’t get stung, cover your ICS in honey: How do honeypots fit within industrial control system security | doi:10.1016/j.cose.2021.102598 | #43, #344 |
| 152 | 2016 | Dynamic Honeypot Configuration for Programmable Logic Controller Emulation | Semantic Scholar 043b0f876405e52293b6c0ca427ab24784abae03 | #535 |
| 156 | 2019 | Energy-grid Threat Analysis Using Honeypots | OpenAlex W3083209706 | #536 |
| 163 | 2026 | Evaluating the Realism of Cyber-Physical Honeynets Against Advanced Attackers | doi:10.1109/noms69089.2026.11668150 | #537 |
| 165 | 2020 | EVASION OF HONEYPOT DETECTION MECHANISMS THROUGH IMPROVED INTERACTIVITY OF ICS-BASED SYSTEMS | OpenAlex W3177851958 | #304 |
| 166 | 2026 | EVPot: A High-Interaction Honeypot for Detecting and Analyzing Attacks Against OCPP-Based Electric Vehicle Charging Infrastructures | doi:10.1145/3847353.3847494 | #538 |
| 170 | 2023 | Fake PLC in the Cloud, We Thought the Attackers Believed that: How ICS Honeypot Deception Gets Impacted by Cloud Deployments? | doi:10.1109/wfcs57264.2023.10144119 | #539 |
| 171 | 2026 | FAKE-OT: An Open Architecture for Threat Detection in OT Environments Using MQTT-Based Honeypots | doi:10.1109/isdfs69419.2026.11458963 | #540 |
| 172 | 2022 | Faking Smart Industry: A Honeypot-Driven Approach for Exploring Cyber Security Threat Landscape | doi:10.1007/978-3-030-98002-3_23 | #541 |
| 173 | 2022 | Faking smart industry: exploring cyber-threat landscape deploying cloud-based honeypot | doi:10.1007/s11276-022-03057-y | #542 |
| 182 | 2026 | H4PLC: Designing PLC Honeypoints Based on Invariants for Industrial Control System Security | doi:10.1109/tmc.2026.3678913 | #543 |
| 183 | 2023 | Hardening Honeypots for Industrial Control Systems | doi:10.24251/hicss.2023.806 | #288 |
| 184 | 2022 | HARDENING WINDOWS-BASED HONEYPOTS TO PROTECT COLLECTED DATA | OpenAlex W7112483478 | #544 |
| 186 | 2026 | HIVE-OT Corpus: A 31-Day Industrial Honeypot Capture of 147,553 Protocol Events Across 14 OT/IT Protocols | doi:10.5281/zenodo.20360674 | #545 |
| 187 | 2021 | HoneyCar: A Framework to Configure Honeypot Vulnerabilities on the Internet of Vehicles | doi:10.1109/access.2022.3210117 | #546 |
| 189 | 2023 | HoneyChart: Automated Honeypot Management over Kubernetes | doi:10.1007/978-3-031-25460-4_18 | #547 |
| 191 | 2023 | HoneyICS: A High-interaction Physics-aware Honeynet for Industrial Control Systems | doi:10.1145/3600160.3604984 | #4 |
| 193 | 2022 | Honeynet – Deploying a Connected System of Diverse Honeypots Using Open-Source Tools | doi:10.1201/9781003338512-3 | #548 |
| 194 | 2020 | HoneyPlant:A Distributed Hybrid Honeypot System for ICS Security | Semantic Scholar 2952cf330c2e5d07058a88b0ebd12784cd21b4db | #549 |
| 195 | 2020 | HoneyPLC: A Next-Generation Honeypot for Industrial Control Systems | doi:10.1145/3372297.3423356 | #2 |
| 196 | 2023 | Honeypot and cyber deception as a tool for detecting cyber attacks on critical infrastructure | doi:10.55056/ceur-ws.org/vol-3374/paper06.pdf | #550 |
| 203 | 2019 | HONEYPOTS AS A PROACTIVE DEFENSE: A COMPARATIVE ANALYSIS WITH TRADITIONAL ANOMALY DETECTION IN MODERN CYBERSECURITY | doi:10.34218/ijcet_10_05_021 | #551 |
| 205 | 2026 | HoneyPrompt: Multi-Sensor Fusion for Detection and Classification of Autonomous AI Agents in Maritime Industrial Control Systems | doi:10.2139/ssrn.6196620 | #552 |
| 206 | 2026 | Honeytoken and Honeypot Systems for IoT Networks: Proof of Concept and Implementation using ESP32-S3 | doi:10.1109/icaiset66439.2026.11541828 | #553 |
| 207 | 2026 | HoneyTrap: AI-Powered Honeypot for Cyberattack Detection | doi:10.5281/zenodo.20615050 | #554 |
| 210 | 2023 | Hybrid H-DOC: A bait for analyzing cyber attacker behavior | doi:10.32985/ijeces.14.1.5 | #555 |
| 211 | 2023 | ICS honeypot frameworks : state-of-the-art and future challenges | OpenAlex W7132173936 | #556 |
| 212 | 2015 | ICS Threat Analysis Using a Large-Scale Honeynet | doi:10.14236/ewic/ics2015.3 | #557 |
| 214 | 2026 | ICSHIve: A Framework for Measurable and High-Interactive Honeypots in Industrial Control Systems | doi:10.1109/tii.2026.3694947 | #558 |
| 217 | 2023 | ICSvertase: A Framework for Purpose-based Design and Classification of ICS Honeypots | doi:10.1145/3600160.3605020 | #559 |
| 218 | 2021 | Identifying Anomalous Industrial-Control-System Network Flow Activity Using Cloud Honeypots | doi:10.1007/978-3-030-84614-5_12 | #560 |
| 219 | 2020 | Identifying Anomalous Network Flow Activity Using Cloud-Based Honeypots | OpenAlex W3178958954 | #561 |
| 223 | 2023 | IMPLEMENTATION OF SECURITY INFORMATION AND EVENT MANAGEMENT SOFTWARE IN A HONEYPOT | OpenAlex W7111850203 | #562 |
| 224 | 2023 | IMPLEMENTING A HIGH-INTERACTION HYBRID HONEYPOT FOR FACILITY AUTOMATION SYSTEMS | OpenAlex W7111919348 | #289 |
| 225 | n.d. | Improving container security with honeypot deployment | Semantic Scholar 84a25fd35933bb530b60c0842348c9209385f42d | #563 |
| 231 | 2022 | Industrial Control Honeypot Based on Power Plant Control System | doi:10.1007/978-3-030-96140-4_6 | #564 |
| 234 | 2026 | Inferring Attacks on a Distributed Honeyfarm Using Adversary Emulation and Centralized Threat Detection | doi:10.24251/hicss.2026.146 | #565 |
| 239 | 2022 | Interaction matters: a comprehensive analysis and a dataset of hybrid IoT/OT honeypots | doi:10.1145/3564625.3564645 | #566 |
| 242 | 2025 | INTRUDEX: Intelligent Honeypot-Based Threat Monitoring System | doi:10.48175/ijarsct-29687 | #567 |
| 244 | 2024 | Investigating Threats to ICS and SCADA Systems Via Honeypot Data Analysis and SIEM | doi:10.33411/ijist/785 | #568 |
| 246 | 2019 | Know Your Enemy: Analysing Cyber-threats Against Industrial Control Systems Using Honeypot | doi:10.1109/raaicon48939.2019.69 | #569 |
| 249 | 2019 | Leveraging Cyber-Physical System Honeypots to Enhance Threat Intelligence | doi:10.1007/978-3-030-34647-8_11 | #570 |
| 250 | 2026 | Leveraging LLMs with Honeypots for the Security of Smart Grid SCADA Systems | doi:10.3390/bdcc10100335 | #571 |
| 251 | 2025 | LLM-based Cybersecurity Honeypots Evaluation Metric Development and Persona Shaping via Structured Prompt Engineering | doi:10.1109/smart66937.2025.11389636 | #572 |
| 252 | 2024 | LLMPot: Dynamically Configured LLM-based Honeypot for Industrial Protocol and Physical Process Emulation | doi:10.1109/eurosp63326.2025.00059 | #9 |
| 253 | 2025 | Machine Learning for Attack Tracking in Cyber-Physical Honeynets | OpenAlex W7224044165 | #573 |
| 254 | 2026 | Machine Learning for Cyber Deception in EV Charging Systems | doi:10.1109/click68749.2026.11742251 | #574 |
| 256 | 2026 | Make the Adversary Spend More Energy: Generative Deception against Language-Model Attackers in Critical Infrastructure | doi:10.48550/arxiv.2610.27739 | #575 |
| 267 | 2019 | Multi Platform Honeypot for Generation of Cyber Threat Intelligence | doi:10.1109/iacc48062.2019.8971584 | #576 |
| 273 | 2025 | Next-Generation Smart Grid Cybersecurity: A Systematic Review of OT Cyber Threats, AI-Driven Defense, Cyber Deception Techniques, and Emerging Security Strategies | doi:10.1109/access.2025.3623834 | #577 |
| 274 | 2015 | NIDS: Network intrusion detection system with Deceptive Virtual Hosts for Industrial Control Networks | Semantic Scholar 9c270a83d27b7e7096d6904ba7d9d4282dce2c09 | #578 |
| 281 | 2025 | Orchestrating Cyber Threat Intelligence using T-Pot and MITRE ATT&CK: From Cyber Attack Data Collection to Advanced Insights | doi:10.1109/iemcon67450.2025.11381043 | #579 |
| 284 | 2019 | Poster: Using Honeypots to Understand Attacks to Industrial Control Systems | OpenAlex W3029643366 | #580 |
| 285 | 2016 | Practical Application Layer Emulation in Industrial Control System Honeypots | doi:10.1007/978-3-319-48737-3_5 | #581 |
| 287 | 2023 | Privacy-Preserving Honeypot-Based Detector in Smart Grid Networks: A New Design for Quality-Assurance and Fair Incentives Federated Learning Framework | doi:10.1109/ccnc51644.2023.10060393 | #582 |
| 289 | 2026 | Project Mimic: Dynamic Honeypots With Live Mimicry System | doi:10.5281/zenodo.21192770 | #583 |
| 299 | 2024 | Research on Dynamic Honeynet Technology Based on Machine Learning | doi:10.1109/swc62898.2024.00367 | #584 |
| 300 | 2023 | Research on Intelligent Dynamic Honeynet Technology for Power Industrial Control System | doi:10.1109/iciba56860.2023.10164895 | #585 |
| 305 | 2021 | RIoTPot:a modular hybrid-interaction IoT/OT honeypot | OpenAlex W7224724682 | #586 |
| 309 | 2017 | S7commTrace: A High Interactive Honeypot for Industrial Control System Based on S7 Protocol | doi:10.1007/978-3-319-89500-0_36 | #587 |
| 310 | 2019 | SCADA security using SSH honeypot | doi:10.1145/3320326.3320328 | #588 |
| 315 | 2023 | Secured Data Transmission for Smart Grid System using Blockchain Technology with a Trusted Gaming Token Honeypot Algorithm | OpenAlex W7217387117 | #589 |
| 322 | 2022 | Shodan Indicators Used to Detect Standard Conpot Implementations and Their Improvement Through Sophisticated Customization | doi:10.1109/dsc54232.2022.9888911 | #590 |
| 323 | 2025 | Smart Grid Intrusion Detection for IEC 60870-5-104 With Feature Optimization, Privacy Protection, and Honeypot-Firewall Integration | doi:10.1109/access.2025.3590151 | #591 |
| 325 | 2025 | Smart Traps for Smart Systems: Scalable Honeynets for IIoT Cybersecurity | doi:10.1109/icccn65249.2025.11133761 | #592 |
| 326 | 2025 | SmartHive-IDS: an advanced intrusion detection framework for SDN-HoneyNet enabled ICPS using hybrid explainable ensemble feature selection with optimized Bi-LSTM | doi:10.1007/s10586-025-05648-8 | #593 |
| 327 | 2025 | Solar Energy System Simulation with Respect to Cybersecurity Using Decoy Device | doi:10.47392/irjash.2025.094 | #594 |
| 328 | 2015 | Specialized Honeypots for SCADA Systems | doi:10.1007/978-3-319-18302-2_16 | #595 |
| 336 | 2021 | Study on Active Defense of Honeypot-Based Industrial Control Network | doi:10.1109/hpcc-dss-smartcity-dependsys53884.2021.00301 | #596 |
| 340 | 2015 | The design and implementation of a PLC honeypot for detecting cyber attacks against industrial control systems | Semantic Scholar 8542dff6763d5e84ef455211cd5f4d0321bcc0b6 | #597 |
| 343 | 2026 | The Psychology of Defensive Cyber Deception Technology Adoption Across IT and OT Environments | doi:10.63671/ijsssr.v4i2.623 | #598 |
| 345 | 2024 | These are Not the PLCs You are Looking for: Obfuscating PLCs to Mimic Honeypots | doi:10.1109/tnsm.2024.3361915 | #290 |
| 346 | 2022 | Threat Analysis on Industrial Control System Based on Attacker's Behaviors using Honeypots | doi:10.1109/icares56907.2022.9993566 | #599 |
| 348 | 2023 | Threat intelligence using Digital Twin honeypots in Cybersecurity | doi:10.1109/csr57506.2023.10224997 | #600 |
| 350 | 2024 | Time-to-Lie: Identifying Industrial Control System Honeypots Using the Internet Control Message Protocol | doi:10.1109/icdcsw63273.2025.00141 | #262, #342 |
| 352 | 2014 | Toward Automating Web Protocol Configuration for a Programmable Logic Controller Emulator | OpenAlex W340482956 | #601 |
| 354 | 2016 | Towards High-Interaction Virtual ICS Honeypots-in-a-Box | doi:10.1145/2994487.2994493 | #602 |
| 360 | 2025 | TwinFedPot: Honeypot Intelligence Distillation into Digital Twin for Persistent Smart Traffic Security | doi:10.3390/s25154725 | #603 |
| 362 | 2023 | Usefulness of Honeypots Towards Data Security: A Systematic Literature Review | doi:10.1109/iwaiip58158.2023.10462777 | #604 |
| 363 | 2022 | Using Cloud Honeypot Platforms for Gathering Industrial-Control-System Attack Intelligence Cloud Honeypot Platforms | Semantic Scholar a18c95ffcb7fbb8b2c087a94c75a2666e85aca3b | #605 |
| 366 | 2019 | Using Honeypots for ICS Threats Evaluation | doi:10.1007/978-3-030-31328-9_9 | #606 |
| 367 | 2024 | Utilisation of a Virtual Honeynet to Proactively Secure the South African National Research and Education Network Against Cyberattacks | doi:10.1007/978-3-031-64881-6_24 | #607 |
| 370 | 2019 | Who's Scanning Our Smart Grid? Empirical Study on Honeypot Data | doi:10.1109/globecom38437.2019.9013835 | #608 |
| 372 | 2021 | World Wide ICS Honeypots:A Study into the Deployment of Conpot Honeypots | OpenAlex W3217519637 | #293 |
| 374 | 2018 | Προστασία SCADA βιομηχανικών συστημάτων ελέγχου με μια ευέλικτη αρχιτεκτονική λύση ανοιχτού κώδικα | Semantic Scholar 5ab079f87bd41d87e907459cb9ee647fa6cb26dd | #609 |

## 8. Excluded: 155 at the title stage and 3 at the abstract stage

| Rec | Year | Title | Stage | Reason |
|---|---|---|---|---|
| 2 | 2024 | 6G Wireless Communication Cyber Physical System Based Smart Healthcare Using Quantum Optimization with Machine Learning | title | no deception or placement content |
| 3 | 2026 | 6ixmap: A Study on Active-Passive Measurement and Asset Exposure in the IPv6 Address Space | title | no deception or placement content |
| 4 | 2020 | A Big Data Fusion to Profile CPS Security Threats Against Operational Technology | title | no deception or placement content |
| 5 | 2023 | A Comparative Analysis of Industrial Cybersecurity Standards | title | no deception or placement content |
| 7 | 2026 | A Cyber-Physical Sovereign Architecture for Autonomous Grid-Inspection Humanoids: Real-Time Kinematic Optimization, LMI-Synthesized H∞ Control, and Immutable Zero-Trust Sandboxing (Phase II) | title | no deception or placement content |
| 9 | 2022 | A Data-Driven Based Security Situational Awareness Framework for Power Systems | title | no deception or placement content |
| 14 | 2026 | A framework for quantum-secure communications in cyber-physical control systems with experimental demonstration in a nuclear reactor | title | no deception or placement content |
| 20 | 2019 | A machine learning-based FinTech cyber threat attribution framework using high-level indicators of compromise | title | no deception or placement content |
| 21 | 2025 | A multilayered deep learning framework for cyber attack detection and mitigation in a heterogeneous IIoT ecosystem | title | no deception or placement content |
| 22 | 2026 | A New Design of a MEMS-Actuated Reconfigurable Soft Robotic Platform for Underwater Environment and Cybersecurity Applications | title | no deception or placement content |
| 26 | 2013 | A preliminary cyber-physical security assessment of the Robot Operating System (ROS) | title | no deception or placement content |
| 27 | 2026 | A quantitative model for embedding quantum-secure communications and evaluating communication autonomy in industrial control systems | title | no deception or placement content |
| 28 | 2017 | A Reactive Security Framework for operational wind parks using Service Function Chaining | title | no deception or placement content |
| 29 | 2025 | A Real-Time Hacker Group Identification Method for Industrial Control Systems Based on Gaussian Self-Organizing Incremental Neural Network | title | no deception or placement content |
| 36 | 2018 | A Survey of Industrial Control System Devices on the Internet | title | no deception or placement content |
| 37 | 2026 | A Survey on Deception Techniques Used in Electronic Warfare | title | the term in another sense: electronic-warfare deception |
| 38 | 2026 | A Unified Security Requirements Catalog for the Industrial IoT | title | no deception or placement content |
| 47 | 2018 | ADVANCED CONTROL SYSTEMS IN INDUSTRIAL INSTRUMENTATION : A COMPREHENSIVE SURVEY | title | no deception or placement content |
| 48 | n.d. | Advanced Persistent Threats (APTs) and U.S. National Security: A Multi-Layered Defense Strategy | title | no deception or placement content |
| 49 | 2026 | Advancements in Wireless Technologies for IIoT | title | no deception or placement content |
| 50 | 2025 | Advances in Security Maturity and Architecture Design in Critical Infrastructures | title | no deception or placement content |
| 52 | 2025 | Agentic AI for Cyber Resilience: A New Security Paradigm and Its System-Theoretic Foundations | title | no deception or placement content |
| 57 | 2001 | An apparatus for the optimized and controlled reactant in reaction systems streamable addition, and methods for use. | title | no deception or placement content |
| 59 | 2020 | An ICS Based Scenario Generator for Cyber Ranges | title | no deception or placement content |
| 62 | 2022 | An Integrated Security Framework for OT System Based on Edge Computing | title | no deception or placement content |
| 67 | 2025 | ANALYZING INDUSTRIAL-CONTROL-SYSTEMS ATTACKS WITH INTEGRATED SECURITY-MONITORING TOOLS AND ADVERSARY EMULATION | title | no deception or placement content |
| 71 | 2026 | AutoMAEC: an automated framework for semantic-aware malware characterization in power grid industrial control systems | title | no deception or placement content |
| 75 | 2026 | Autonomous Traffic Control System (ATCS v2.0) for Low Earth Orbit Debris Mitigation: 12.5-ms Hardware-in-the-Loop Multi-Objective Optimization, Post-Quantum Cryptographic Governance (ML-KEM-768 / Decoy-State QKD), Q-SAFA Self-Executing Orbital Circular Economy, and Isomorphic Pedagogical Communication | title | no deception or placement content |
| 76 | 2026 | Backdoor-Resilient Industrial IoT: A Hybrid Containment Approach | title | no deception or placement content |
| 79 | 2025 | Can an AI-Based Behavioural Scanner Improve the Detection of Protocol-Level Misconfigurations and Anomalies in Industrial IoT Environments | title | no deception or placement content |
| 80 | 2026 | Causality-Aware Active Defense Strategy against FDIAs in Smart Grids | title | no deception or placement content |
| 82 | 2016 | Characterizing industrial control system devices on the Internet | title | no deception or placement content |
| 85 | n.d. | City Research Online City St George’s, University of London | title | front matter, not a paper |
| 86 | 2021 | City, University of London Institutional Repository | title | front matter, not a paper |
| 88 | 2025 | Comparison of methods for calculating the parameters of an explosion shock wave for the design of protective engineering structures | title | no deception or placement content |
| 92 | 2026 | Containment Invariants: Securing Intentionally Vulnerable Systems for Education, Training, and Research | title | no deception or placement content |
| 93 | 2024 | CONTINGENT: Advanced Solution to Enhance Cyber Resilience Through Machine Learning Techniques | title | no deception or placement content |
| 95 | 2025 | Core technologies for hydropower digitalization within the Energy Internet framework: a mini-review | title | no deception or placement content |
| 96 | 2016 | Cover page | title | front matter, not a paper |
| 97 | 2018 | Covert Cyber Assault Detection in Smart Grid Networks Utilizing Feature Selection and Euclidean Distance-Based Machine Learning | title | no deception or placement content |
| 98 | 2025 | Cross-Divisional Cybersecurity Risk Management in Automotive: Requirements and Current Practices | title | no deception or placement content |
| 99 | 2026 | CT-EWS: graph-centric early warning for multi-protocol cyber campaigns using long-memory forecasting and explainable attribution | title | no deception or placement content |
| 100 | 2026 | CTDMF-SC: cybersecurity threat detection and mitigation framework for smart cities | title | no deception or placement content |
| 102 | 2026 | Cyber Physical Security Framework for AI-Driven Digital Oilfield Architectures | title | no deception or placement content |
| 103 | 2018 | Cyber Security Objectives and Requirements for Smart Grid | title | no deception or placement content |
| 108 | 2024 | CyberDefender: an integrated intelligent defense framework for digital-twin-based industrial cyber-physical systems | title | no deception or placement content |
| 109 | 2024 | Cybersecurity for industrial Internet of Things: a case study of the South African transport sector. | title | no deception or placement content |
| 110 | 2026 | CYBERSECURITY GOVERNANCE MECHANISM OF INDUSTRIAL CONTROL SYSTEMS UNDER THE BACKGROUND OF INTELLIGENT MANUFACTURING | title | no deception or placement content |
| 111 | 2026 | Cybersecurity Threat Analysis for an Energy Rich, Small Island Developing State | title | no deception or placement content |
| 112 | 2021 | Cybersecurity Threat Analysis for an Energy Rich, Small Island Developing State | title | duplicate of 111, missed by the automatic deduplication |
| 114 | 2026 | Dark Space Detection: Inline Enforcement Against Traffic Directed at Non-Existent Network Addresses | title | no deception or placement content |
| 115 | 2021 | Data-Driven Approaches for Detecting Malware-Infected IoT Devices and Characterizing Their Unsolicited Behaviors by Leveraging Passive Internet Measurements | title | no deception or placement content |
| 116 | 2025 | DCS Virtualization in Oil and Gas Plants | title | no deception or placement content |
| 124 | 2026 | Deep Learning for Early Detection of Equipment Failure in Smart Manufacturing: An Extension of Edge Computing | title | no deception or placement content |
| 125 | 2022 | Deep Reinforcement Learning for Deception in IRS-assisted UAV Communications | title | the term in another sense: deception in wireless communication |
| 127 | 2025 | Defense Against Aerial Swarm Attacks: A Stackelberg Game-Theoretic Approach | title | no deception or placement content |
| 128 | 2026 | Defense Mechanisms for Network Layer Attacks in IoT and Blockchain Networks | title | no deception or placement content |
| 131 | 2025 | Demonstration of Quantum-Secure Communications in a Nuclear Reactor | title | no deception or placement content |
| 137 | 2026 | Design and study of a virtualization technology-based security attack-defense range for industrial control networks | title | no deception or placement content |
| 139 | 2020 | Design of a strike-back attack against cyber threat actors | title | no deception or placement content |
| 140 | 2017 | Detection and prevention of intrusions in power system cyber-physical infrastructure | title | no deception or placement content |
| 141 | 2022 | Detection of Android Malware Behavior in Browser Downloads | title | no deception or placement content |
| 143 | 2024 | Detection of Illegal Activity of an Employee in an Organisation | title | no deception or placement content |
| 147 | n.d. | Digital Twins of Deception: A Framework for Adaptive AI-Mediated Manipulation and the Trust Divergence Problem | title | the term in another sense: deception as manipulation of people |
| 148 | 2014 | Distributed computing and networking : 15th International Conference, ICDCN 2014, Coimbatore, India, January 4-7, 2014 : proceedings | title | front matter, not a paper |
| 153 | 2026 | EDDE-MT-Based Detection-Record Integrity and DV-QKD with Side-Channel Monitoring Using DVQMTC and E-TeLU-Bi-LSTM for Securing CPS | title | no deception or placement content |
| 154 | 2026 | Edge Computing–Enabled Intelligent Financial Auditing: An Advanced Real-Time Framework for Automated Fraud Detection, Predictive Accounting Analytics, and Financial Risk Assessment | title | no deception or placement content |
| 155 | 2004 | Editorial board | title | front matter, not a paper |
| 157 | 2025 | Engineering Law and Cybersecurity in Digital Health: Legal-Informatics Frameworks for Regulating Cross-Border Data Interoperability, Liability, and Resilience in Public Health Communication Systems | title | no deception or placement content |
| 158 | 2026 | Enhancing Future CNS-ATM Resilience Through Pilot-Centric Mitigation of Cyber Deception | title | the term in another sense: deception attacks on aviation |
| 159 | 2026 | Enhancing Industrial Resilience: NIS2-Compliant Architectures Through Early Warning Systems for OT Monitoring | title | no deception or placement content |
| 161 | 2020 | ESTABLISHMENT OF CYBER-PHYSICAL CORRELATION AND VERIFICATION BASED ON ATTACK SCENARIOS IN POWER SUBSTATIONS | title | no deception or placement content |
| 164 | 2018 | Evaluation of Industrial Firewall Performance Issues in Automation and Control Networks | title | no deception or placement content |
| 167 | 2009 | Experimental Validation of Architectural Solutions | title | front matter, not a paper |
| 168 | 2020 | Exploring Shodan From the Perspective of Industrial Control Systems | title | no deception or placement content |
| 169 | 2025 | Exposed in the Pool: An Analysis of IPv6 NTP Server Scanning Activities | title | no deception or placement content |
| 174 | 2018 | Feature Selection–Based Detection of Covert Cyber Deception Assaults in Smart Grid Communications Networks Using Machine Learning | title | the term in another sense: "cyber deception" meaning an attack, in a smart grid (exclusion confirmed by the user, 8 November 2026) |
| 175 | 2022 | Fighting IoT Cyberattacks | title | no deception or placement content |
| 176 | 2026 | Frequency Control of Smart Grids Under Complex Hybrid Deception Attacks via Point-by-Point Model-Reference Tracking | title | the term in another sense: "deception attacks" in control theory, in a smart grid (exclusion confirmed by the user, 8 November 2026) |
| 177 | 2026 | From Data to Decisions, Unlocking Industry 4.0: AI-Ready Historian and Digital Twin Driving Efficiency & Reliability at Engro Fertilizers | title | no deception or placement content |
| 181 | 2026 | Governance, Accountability, and Regulatory Compliance of AI-Driven Autonomous Drilling Control Systems in Critical Energy Infrastructure | title | no deception or placement content |
| 185 | 2026 | Hidden World Who Controls Access | title | no deception or placement content |
| 208 | 2025 | How Does AI Transform Cyber Risk Management? | title | no deception or placement content |
| 209 | 2026 | Human-centered cybersecurity risk management for IT/OT-converged oil and gas operating facilities | title | no deception or placement content |
| 213 | 2023 | ICScope: Detecting and Measuring Vulnerable ICS Devices Exposed on the Internet | title | no deception or placement content |
| 215 | 2019 | ICSTrace: A Malicious IP Traceback Model for Attacking Data of Industrial Control System | title | preprint of 216, missed by the automatic deduplication |
| 216 | 2021 | ICSTrace: A Malicious IP Traceback Model for Attacking Data of the Industrial Control System | title | no deception or placement content |
| 220 | 2026 | IEC 62443 Wireless Security: Deploying OT Wireless Controllers in Industrial Factory Networks | abstract | Deployment guide for IEC 62443-aligned wireless LAN controllers. No deception and no optimisation. |
| 221 | 2024 | Image-based malware detection based on convolution neural network with autoencoder in Industrial Internet of Things using Software Defined Networking Honeypot | title | no deception or placement content |
| 222 | 2014 | Impact of the Shodan Computer Search Engine on Internet-facing Industrial Control System Devices | title | no deception or placement content |
| 227 | 2025 | Incorporating cybersecurity measures around industrial control systems (ICS) within the petrochemical sector | title | no deception or placement content |
| 228 | 2006 | Increased glucocorticoid receptor–β expression, but not decreased histone deacetylase 2, in severe asthma | title | no deception or placement content |
| 229 | 2020 | Increased IT security by model-based vulnerability analysis of IT/I&C systems and proof of ISO conformity | title | no deception or placement content |
| 232 | 2021 | Industrial control protocols in the Internet core: Dismantling operational practices | title | no deception or placement content |
| 233 | 2019 | Industrial control systems and IoT botnets | title | no deception or placement content |
| 235 | 2026 | Information Physics for Safety-Critical AI | title | no deception or placement content |
| 236 | 2024 | Integrating Cybersecurity Threats into Smart Manufacturing | title | no deception or placement content |
| 237 | 2026 | INTEGRATION OF RISK-BASED RESILIENCE STRATEGIES INTO INTELLIGENT SAFETY MANAGEMENT OF SHIP-PORT CYBER-PHYSICAL SYSTEMS | title | no deception or placement content |
| 238 | 2025 | Intelligent Data Refinement and Analysis of Real-World Cyber Attacks on SCADA Systems | title | no deception or placement content |
| 240 | 2025 | INTERNET-WIDE THREAT INTELLIGENCE AND ENTERPRISE LATERAL MOVEMENT DETECTION | title | no deception or placement content |
| 241 | 2020 | Introduction | title | front matter, not a paper |
| 243 | 2021 | Intrusion Detection System-Based Security Mechanism for Vehicular Ad-Hoc Networks for Industrial IoT | title | no deception or placement content |
| 245 | 2025 | IOT-ENABLED CONDITION MONITORING IN POWER DISTRIBUTION SYSTEMS: A REVIEW OF SCADA-BASED AUTOMATION, REAL-TIME DATA ANALYTICS, AND CYBER-PHYSICAL SECURITY CHALLENGES | title | no deception or placement content |
| 248 | 2025 | Leveraging BRSKI to Protect the Hardware Supply Chain of Operational Technology: Opportunities and Challenges | title | no deception or placement content |
| 255 | 2026 | Machine learning-based early incident detection system in a bakery plant’s industrial network: a cognitive model for counteracting hybrid threats | title | no deception or placement content |
| 257 | 2026 | Make the Adversary Spend More Energy: per-run data, power traces and scripts (energy exchange between language-model attacker and generative decoy) | title | front matter, not a paper |
| 258 | 2022 | Mapping Threats in Smart Grid System Using the MITRE ATT&CK ICS Framework | title | no deception or placement content |
| 260 | 2018 | Mining Anomaly Communication Patterns for Industrial Control Systems | title | no deception or placement content |
| 265 | 2011 | Monitoring critical infrastructure assets and strategic signaling to deter aggression in cyberspace | abstract | Legal and policy study (a government honeynet at a private utility, deterrence signalling). No technical deception content. |
| 266 | 2026 | MQTT Attack Taxonomy and EFSM-Based Behavioral Modeling: A Protocol Aware Framework for IoT Threat Detection | title | no deception or placement content |
| 268 | 2026 | Multi-Layered Modelling Knowledge Graph and Response Derivative Framework for Autonomous Buildings, Energy Communities, and Positive Energy Districts | title | no deception or placement content |
| 272 | 2019 | New scheme to prevent node replication attacks for wireless sensor networks | title | no deception or placement content |
| 275 | 2015 | Notice of Removal The real world evaluation of cyber-attacks against ICS system | title | front matter, not a paper |
| 276 | 2017 | On the impact of empirical attack models targeting marine transportation | title | no deception or placement content |
| 277 | 2009 | One size does not fit all: 10 years of applying context-aware security | title | no deception or placement content |
| 280 | 2025 | Optimized Deep Learning Techniques for Intrusion Detection with Explainable AI-Based Ensemble Feature Selection | title | no deception or placement content |
| 282 | 2023 | Otonom ağlar için dijital ikiz destekli akıllı saldırı tespit mekanizmaları | title | no deception or placement content |
| 283 | 2015 | Papers Delivered in the Thematic Sessions of the 2015 Annual International Conference of the Society of Architectural Historians | title | front matter, not a paper |
| 286 | 2012 | Preliminary Investigation in removing microphonic noise from nuclear detectors | title | no deception or placement content |
| 291 | 2026 | PURITY: An Industry-Standard-Based Security Framework for IT-OT Convergence | abstract | PURITY: maps standards' controls onto Purdue levels for SMEs. No deception and no formal optimisation. |
| 292 | 2026 | QHIE-LKE: a quantum-resilient hybrid intrusion detection and CRYSTALS-Kyber lattice cryptographic framework for secure blockchain-enabled internet of nano-things networks | title | no deception or placement content |
| 293 | 2026 | QKD-Secured Industrial Smart-Grid Cyber-Physical Systems: Simulation and Q-MambaKAN Detection of Adaptive Side-Channel Attacks | title | no deception or placement content |
| 294 | 2026 | Quantum Communication Networks for Secure Foundation Model Distribution Across Shanxi Power Grid Substations | title | no deception or placement content |
| 295 | 2026 | Quantum Communication Technology for Optimizing 3D Cost Estimation and Secure Data Transmission in Substation Engineering | title | no deception or placement content |
| 296 | 2026 | Quantum Key Distribution Protocols | title | no deception or placement content |
| 301 | 2026 | Research on Quantum Key Distribution Technology for Secure Data Transmission in Power System Networks | title | no deception or placement content |
| 304 | 2026 | Resilient Observation Scheduling Against Smart Intermittent DoS Attacks: A Multi-Agent Deep Reinforcement Learning Game | title | no deception or placement content |
| 306 | 2026 | Risk assessment framework for cyber resilience of smart ships: A maturity model integrating IACS UR E26/E27 with testbed validation of the baseline and advanced tiers | title | no deception or placement content |
| 308 | 2025 | Robotics and Sensor Integration in Agricultural Systems Using PLC and Delta V Method | title | no deception or placement content |
| 312 | 2026 | Secure intrusion detection system for industrial control systems using digital twins | title | no deception or placement content |
| 313 | 2025 | Secure Quantum Key Distribution Protocol for Hybrid Classical-Quantum Networks | title | no deception or placement content |
| 314 | 2025 | Secure-by-Construction-planering och -styrning av multiagentsystem : Säkerhet och uppgiftsuppfyllelse i kooperativa autonoma system | title | no deception or placement content |
| 317 | 2026 | Securing the Node: A Cybersecurity Architecture for NIS2-Compliant Community-Scale Distributed Energy Infrastructure and The Regulatory Gaps that Prevent its Deployment | title | no deception or placement content |
| 318 | 2014 | Security Feature Test for Ethernet Switches | title | no deception or placement content |
| 319 | 2024 | Security, Privacy, and Trust Management on Decentralized Systems and Networks | title | front matter, not a paper |
| 321 | 2025 | Self-Reconfiguration of Industrial Control Systems as a Response to Cyberattacks | title | no deception or placement content |
| 324 | 2014 | Smart grid security : Second International Workshop, SmartGridSec 2014, Munich, Germany, February 26, 2014 : revised selected papers | title | front matter, not a paper |
| 330 | 2022 | Standardized cyber security risk assessment for unmanned offshore facilities | title | no deception or placement content |
| 331 | 2026 | Standardizing AI Risk Assessment for Critical Infrastructure: An Integrated Governance Framework for Operational Technology Environments | title | no deception or placement content |
| 335 | 2026 | Strengthening ICS Attack Resiliency: Advanced Incident Response, Threat Intelligence, and Cyber-Physical Systems Monitoring | title | no deception or placement content |
| 338 | 2026 | Temporal Dynamics of AI-Driven Cyberattacks: Timing-Based Detection and Sub-Second Defense Against Autonomous Attack Agents | title | no deception or placement content |
| 339 | 2016 | TGF-beta signaling in an in vivo model of NASH | title | no deception or placement content |
| 341 | 2026 | The future of electrical power grid protection: Adaptive, intelligent, and cyber-resilient architectures for dynamic systems | title | no deception or placement content |
| 342 | 2026 | THE LLM ORIGINAL SIN | title | no deception or placement content |
| 344 | 2026 | Thermodynamic Exhaustion of Digital Perimeter Defense: Frontier AI-Commoditized Penetration, Asymmetric Cyber-Sabotage, and the Inevitable Retreat to Physical-Layer Minimal Data Retention | title | no deception or placement content |
| 347 | 2015 | Threat Analysis Using a Large-Scale Honeynet | title | duplicate of 212, missed by the automatic deduplication |
| 349 | 2026 | Threat Modeling and Attack Surface Analysis of IoT-Enabled Controlled Environment Agriculture Systems | title | no deception or placement content |
| 351 | 2021 | Topics from networks management and operations | title | front matter, not a paper |
| 353 | 2026 | Toward Intelligent Infrastructure: MAIA, a Modular AI Architecture for Industrial Control Systems | title | no deception or placement content |
| 356 | 2019 | Towards the Creation of a Threat Intelligence Framework for Maritime Infrastructures | title | no deception or placement content |
| 357 | 2014 | Tracking smart grid hackers | title | no deception or placement content |
| 359 | 2021 | TRUSTY: A Solution for Threat Hunting Using Data Analysis in Critical Infrastructures | title | no deception or placement content |
| 361 | 2018 | Understanding the Usage of Industrial Control System Devices on the Internet | title | no deception or placement content |
| 364 | 2020 | Using Design Thinking to Understand Cyber Attack Surfaces of Future Smart Grids | title | no deception or placement content |
| 365 | 2014 | Using detection in depth to counter SCADA-specific advanced persistent threats | title | no deception or placement content |
| 369 | 2025 | Water Security in Urban Areas: Integrating Smart Monitoring Systems | title | no deception or placement content |
| 371 | 2009 | Work package contributing to the deliverable: | title | front matter, not a paper |
| 375 | 2026 | РОЗРОБКА АРХІТЕКТУРИ ІНФОРМАЦІЙНО-КЕРУЮЧОЇ СИСТЕМИ ДЛЯ ЕНЕРГОЕФЕКТИВНОЇ ПЕРЕРОБКИ ЗАЛІЗОРУДНОЇ СИРОВИНИ | title | no deception or placement content |

## 9. Records already in `sources.md` before A17

At least 24 of the 375, and two probable. None gets a second entry.

| Rec | Group | Entries |
|---|---|---|
| 19 | K | #240, #271 |
| 43 | A | #30, #192, #247, #272 |
| 68 | A | #343 |
| 101 | R | #42 |
| 107 | A | #300 |
| 113 | K | #250, #324 |
| 117 | A | #13 |
| 118 | A | #57 |
| 119 | K | #305 |
| 120 | K | #11 |
| 149 | R | #43, #344 |
| 165 | R | #304 |
| 178 | A | #317 |
| 183 | R | #288 |
| 191 | R | #4 |
| 195 | R | #2 |
| 197 | A | #316 |
| 224 | R | #289 |
| 252 | R | #9 |
| 262 | K | #12 |
| 290 | A | #317 |
| 345 | R | #290 |
| 350 | R | #262, #342 |
| 372 | R | #293 |
| 8 | R | Probable, so given its own entry (#490): possibly the paper #314 names from its arXiv version |
| 90 | A | Probable, so given its own entry (#445): #304 describes a thesis on cost-effective, targetable ICS honeypot construction, probably this one |

## 10. Limits of this screening

- **One reviewer**, with an AI first pass at every stage. The user confirmed the tiers that §9 reserves to the user.
- **Five records were judged on their titles alone**, because their abstracts could not be obtained (records 70, 121, 126, 192, 303).
- **Full texts were limited to free copies** (D35). Eight candidates that might narrow the claim were judged on their abstracts only, and their tiers are unresolved.
  - Record 89 (Gong et al.) has the closest abstract of the search: consequence-driven honeypot placement in a layered chemical-plant ICS, along attack graphs, under a budget. The thesis cites it from its abstract, says the full text was not accessible, and states the differences the abstract shows: no IEC 62443 zones or conduits, no ATT&CK paths, no interception-stage term.
- **Four titles in other scripts** were screened by translation: record 374 (Greek), related by title; and records 375 and 490 (Ukrainian) and 501 (Russian), excluded.
- **"Already logged" was undercounted** at first. The title pass found 5; a later check found at least 24 (#416).
- **Two more candidates whose full texts are not free** (D36): BAG-HRF (record 419) and Tan et al. (record 412). Their tiers are unresolved by the user's decision of 15 November 2026; with the eight above that makes ten. The thesis cites them from their abstracts and names them in the limitation. Tan et al. is in neither OpenAlex nor Semantic Scholar, so its citing list could not be chased; BAG-HRF has no forward citations. Voznyi et al. (record 468) and "Turn the tables" (record 556) are related (T1) by the user's decision, from abstracts only.
- **The patent arm is screened mostly on titles** (amendment 6, §14.2): 1,128 of 1,394 patents were judged on a title alone, 246 unopened ones on titles that Google Patents cut with "…", and the title rule's exclusions proved unsafe: of the 29 excluded titles opened in the third round, 19 proved related (T1) and 10 stayed excluded, and of the 39 opened in the fourth, 26 proved related and 13 stayed excluded (§14.4). 262 pages were opened; the claims were not reached for 27 of them. Pages were read through a small-model summary by the fetch tool, which reads the first 100,000 characters of a long page; Chinese, Korean, Japanese and Taiwanese pages through Google's machine translation, which often strips formulas, so the objectives of CN 122339820 A and CN 120034354 A could not be checked. *[D38: run P1c adds 102 publication numbers: 38 opened, 56 judged on a title alone, 4 on a title and list snippet and 4 on the family (§18.4). Of the arm's 1,496, 300 are then opened and 1,184 judged on a title alone.]*
- **Block O of the strings has no power-grid words** (§14.5, amendment 7): S1, S2 and S5 on the paper side, and S1 and the classification run P3b on the patent side, need a word from it, and "power grid", "power system", "electric power", "new power system", "distribution network" and "power plant" are not in it. A widened re-run is offered (§11) and was not made. *[D38: made on 16 November 2026 for S1, S2 and S5 and for S1 on Google Patents (run P1c), with the six words as a separate block (§18); the classification run P3b was not repeated with them.]*
- **The similarity route (run P6) is a sample, not a closure** (§14.7, amendment 7): sixteen pages, depth two fixed by Claude; the keyword runs already held 27 of the 60 deception-titled patents its tables name (45 per cent); 158 rows without a deception term in the title were counted and not entered; and of the 35 deception-titled papers in its tables 8 were in the log, 27 not (judged on titles only).
- **Run P1b's list is incomplete:** about 970 results were reported and 574 distinct patents seen (§14.1); up to about 400 were never seen. A re-run in date slices would show the rest.
- **No search was run on the USPTO's Patent Public Search** (amendment 5), and the four large vendors Fortinet, Commvault, SentinelOne and Proofpoint were searched on deception terms only, so §6's limit was not tested for them.
- **IEEE Xplore's terms of access** for the public-search use are still unverified (`sources.md` #404).

## 11. Still to run (A17, A29)

As of D36 (15 November 2026) every search the protocol fixed has run, and nothing found threatens A28's claim as worded. Searches that could still change that come first.

- **Recommended before A12 and the freeze: a widened re-run of block O (D36 item 6).** Add "power grid", "power system", "electric power", "new power system", "distribution network" and "power plant" to block O (§14.5), and run S1 on Google Patents (narrowed, as P1n was, to title, abstract and claims) and S1, S2 and S5 on OpenAlex and Semantic Scholar, keeping only what the first runs did not return. About 45 minutes in the user's browser, and about 0.2–0.3 weekend-unit to screen what is new; both are estimates, and the count is unknown until the queries run. The protocol runs the literature part before the freeze so that a competing method can still become a baseline (§12), which is the reason to run it now and not later. *[D38: made and screened on 16 November 2026 (§18): one more T2 paper, Zhan et al. 2026, and no patent T2 or T3.]*
- **The update re-run** of S1 and the citation lists, within a month of submission (§10).
- **Optional: the "honeypoint" patent run in date slices** (for example by priority year), to see the up to about 400 results of run P1b that were never seen (§14.1). About 15 minutes in the user's browser, and about 0.1 weekend-unit to screen what it returns. It is not needed for any decision.
- **Optional: read the patents that the rules left on a title** (§14.5): the run P1n item below, and the 175 patents related on a title that Google Patents had cut, since the fourth round showed that a cut title can hide a method. Together about 0.5–1 weekend-unit of elapsed time for Claude's page reads, with no step for the user.
- **Optional: open the 67 patents of run P1n that are related on a title only** (§14.5). Run P1n is the narrowed S1, the run most likely to hold a neighbour of A28's claim. Of the 47 P1n patents that the rule had related on a title and that were read, 0 proved T2 or T3. It would be 67 page reads by Claude, with no step for the user.
- **Waiting for the user** (D36): the proposed T2, CN 122339846 A/B (§15.1); two borderline T1 or T2 calls, CN 117675308 A and CN 121012683 A (§15.2); four patent exclusions and one paper row that §9 asks him to confirm (§14.6, §14.7); the tier of CN 121603304 B, if he wants to make it (§15.2); whether the OT gate stands for CN 121356815 A and CN 120658528 A (§15.2); whether A28's opening clause reads "granted patents and published patent applications"; amendments 6 and 7, which he can strike; and whether to run the widened re-run above. *[D37, 16 November 2026: all ruled as Claude proposed (§15.1, §15.2); the four exclusions and the paper row stand; the widened re-run is under way.]* *[D38: the widened re-run is made and screened (§18).]*
- **Free full texts of BAG-HRF and Tan et al.,** if the user finds any, would resolve their tiers.

## 12. The later paper-side runs: counts at each stage

Added by D36, 15 November 2026. Runs 11–17 and the backward and forward rounds (`sources.md` #613–#623). These records were deduplicated against the 375 above, against `sources.md` and against each other, in the run order given in #623. Their record numbers, 376–562, are assigned in alphabetical order of normalised title.

| Run | Returned | Already known or found earlier | New at deduplication | New after checks | Related (T1) | Unresolved | Excluded | Note |
|---|---|---|---|---|---|---|---|---|
| arXiv, S1 (#613) | 5 | 5 | 0 | 0 | 0 | 0 | 0 |  |
| arXiv, S2 (#614) | 7 | 7 | 0 | 0 | 0 | 0 | 0 |  |
| IEEE Xplore, S4 (#615) | 9 | 6 | 3 | 3 | 0 | 0 | 3 |  |
| IEEE Xplore, S1 (#616) | 85 | 51 | 34 | 33 | 23 | 0 | 10 | one of the 34 proved already logged (#251) |
| OpenAlex, citations of the ten works (#617) | 82 | 5 | 77 | 75 | 28 | 0 | 47 | two of the 77 proved already logged (#41, #326) |
| OpenAlex, "honeypoint" (#618) | 16 | 3 | 13 | 13 | 10 | 1 | 2 | amendment 3 |
| Google Scholar, "Cited by", first pages (#619) | 112 rows, 99 unique | 67 | 32 | 29 | 6 | 0 | 23 | of the 32: one already logged (#41), two duplicates |
| Google Scholar, "Cited by", second pages (#619) | 17 | 9 | 8 | 8 | 0 | 0 | 8 |  |
| Backward rounds, BAG-HRF and Voznyi et al. (#622) | 38 | 14 | 24 | 24 | 12 | 0 | 12 | 6 repeats of this batch, 8 already logged |
| Queued round of #611 (#622) | 3 | 1 | 2 | 2 | 1 | 1 | 0 | the third reference, Kamdem et al., came from run 16 |
| **Total** | | | | **187** | **80** | **2** | **105** | |

**Combined with the main search (§1):**

| Final outcome, all paper-side records | Records |
|---|---|
| T3, threatens the claim | 0 |
| T2, narrows the claim | 2 (records 43 and 269) |
| T1, related | 282 (202 + 80) |
| Tier unresolved: full text not obtained | 10 (records 41, 89, 151, 160, 188, 288, 307, 333, and 412 and 419 from this batch) |
| Assessed in earlier iterations, not re-tiered | 5 |
| Excluded | 263 (158 + 105) |
| **Total** | **562** |

**What the 187 new records were judged on:** abstract 77; abstract on a publisher's page 4; full text 1; IEEE Xplore result-list snippet 34; Google Scholar snippet 33; title alone 38. None reached T2 or T3 on its abstract, so the full-text stage of §11 did not apply to this batch. BAG-HRF and Tan et al. are the two unresolved: their full texts are not free, and their abstracts leave open whether they place honeypoints by a formal objective in a way that narrows the claim.

**Kept records: 82.** Each has an entry in `sources.md` #645–#726, in the order of the tables below.

**Who decided what.**
- Claude made every first pass: the title stage, the abstract stage and the proposed tiers.
- The user decided, on 15 November 2026, nine borderline calls put to him ("Tan unresolved. Rest confirmed."): Tan et al. (record 412) and BAG-HRF (record 419) tier unresolved; Voznyi et al. (record 468) and "Turn the tables" (record 556) related (T1); and the five patents in §15.2.
- The user has not reviewed the other calls of this batch record by record. Section 9's reservation holds for the papers: no excluded paper title carries both a deception term and an OT term (checked on all 105 excluded titles by a word match on blocks D and O, widened with "industrial", "power system", "power grid" and "CPS"), so no paper exclusion needs the user's confirmation. Five excluded titles carry a deception word in another sense: records 402 (a radio-jamming "decoy strategy"), 507 and 531 ("honeypoint" in neural-network privacy and wireless eavesdropping), 558 ("deception" in biology) and 561 (deceptive path planning in a grid world). Two excluded titles are in Cyrillic (records 490 and 501) and were screened by translation.

## 13. Records 376–562

### 13.1 Tier unresolved (2)

| Rec | Year | Title | Identifier | Judged on | Entry |
|---|---|---|---|---|---|
| 412 | 2025 | A strategy-making method for pIoT PLC honeypoint defense against attacks based on the time-delay evolutionary game | doi:10.1109/TIFS.2025.3601442; IEEE Xplore 11217210 | abstract (publisher page); full text not obtained | #646 |
| 419 | 2025 | BAG-HRF: A Bayesian Attack Graph-Based Honeypoint Recommendation Framework | doi:10.1109/icaisg68699.2025.11452143 | abstract; full text not obtained | #645 |

### 13.2 Related (T1): 80

| Rec | Year | Title | Identifier | Judged on | Entry |
|---|---|---|---|---|---|
| 377 | 2026 | A Cloudified Dynamic Defense Framework for Cyber Deception as a Service | doi:10.1109/infocom59046.2026.11571616 | abstract | #648 |
| 378 | 2026 | A Comparative Review of Honeypot -Based Intrusion Detection and Isolation Forest Approaches | IEEE Xplore 11706612 | IEEE snippet | #688 |
| 379 | 2026 | Adaptive AI-Powered Firewall with Integrated Deception and Automated Countermeasures for Proactive Cyber Threat Neutralization | IEEE Xplore 11510776 | IEEE snippet | #689 |
| 380 | 2019 | Adaptive Honeypot Engagement Through Reinforcement Learning of Semi-Markov Decision Processes | doi:10.1007/978-3-030-32430-8_13 | title | #711 |
| 382 | 2026 | A Deception-Driven AI Framework for Detecting Cyberattacks in Mobile Financial Applications Using GANs, Reinforcement Learning, and SVM | Google Scholar (no usable link) | title | #712 |
| 383 | 2026 | A DIoT: Multi-AI Agent Adversarial-Based Active Defense Framework for Securing Large-Scale IoT Network | Scholar: ieeexplore.ieee.org/abstract/document/11776034/ | abstract | #649 |
| 384 | 2025 | Advancing Cybersecurity with Honeypots and Deception Strategies | doi:10.3390/informatics12010014 | abstract | #650 |
| 390 | 2024 | A Hypothesis Testing-based Framework for Cyber Deception with Sludging | doi:10.1109/allerton63246.2024.10735267 | abstract | #651 |
| 391 | 2026 | AI-Controlled Modular Decoy Generation for Reconstruction-Resistant Hybrid and Multi-Cloud Storage Systems | doi:10.3390/electronics15061231 | abstract | #652 |
| 394 | 2026 | An adaptive defense generation method for mimic honeypots based on Minimax-Q game theory | doi:10.1016/j.cose.2026.105160 | title | #713 |
| 395 | 2012 | An Adaptive Honeypot System to Capture IPv6 Address Scans | IEEE Xplore 6542540 | IEEE snippet | #690 |
| 399 | 2025 | Analyzing Cyber Attack Patterns and Detection Strategies Through T-Pot Honeypot Deployment | IEEE Xplore 11459680 | IEEE snippet | #691 |
| 403 | 2026 | A novel methodology to enhance Security-by-Design for industrial control systems | doi:10.1016/j.cose.2026.105070 | abstract | #653 |
| 406 | 2024 | Application Layer Cyber Deception Without Developer Interaction | doi:10.1109/eurospw61312.2024.00053 | abstract | #654 |
| 411 | 2026 | A Stackelberg game based deception defense strategy against APT under resource constraints | doi:10.1007/s11432-025-4530-7 | abstract (publisher page) | #655 |
| 413 | 2021 | A Survey of Honeypots and Honeynets for Internet of Things, Industrial Internet of Things, and Cyber-Physical Systems | IEEE Xplore 9520645 | IEEE snippet | #692 |
| 417 | 2025 | Automating Adaptive Deception in Endpoint Detection and Response Systems and Optimizing Decoy Placement | OpenAlex W7165311493 | abstract | #656 |
| 421 | 2026 | Calling the Shots: Constraint-Aware Honeypoint Orchestration for Cloud-Native Anomaly Response | doi:10.1109/tsc.2026.3712455 | abstract | #657 |
| 422 | 2025 | Control and Decision-Making in Deceptive Multi-Computer Systems Based on Previous Experience for Cybersecurity of Critical Infrastructure | doi:10.3390/app152212286 | abstract | #658 |
| 423 | 2026 | Copot-2025: Six-month Observation of Honeypots | IEEE Xplore 11586397 | IEEE snippet | #693 |
| 424 | 2026 | Cyber Deception through LLM-Driven Infrastructure as Code: A Fine-Tuned Pipeline for Context-Aware Honeypot Generation | OpenAlex W7204614351 | abstract | #659 |
| 426 | 2025 | Cyberpsychology: Integrating Cyber Behavioral Sciences with Adaptive Environments for Enhanced Cyber Deception | doi:10.24251/hicss.2025.135 | abstract | #660 |
| 430 | 2017 | Data-centric framework for adaptive smart city honeynets | IEEE Xplore 7973836 | IEEE snippet | #694 |
| 432 | 2026 | Deceptive Defense Model for Better Securing Networked Systems Modeled by Attack Graphs | IEEE Xplore 11610858 | abstract | #661 |
| 435 | 2024 | Demo: Cloud-native Cyber Deception with Decepto | doi:10.1109/iscc61673.2024.10733585 | abstract | #662 |
| 437 | 2017 | Deployment and analysis of honeypots sensors as a paradigm to improve security on systems | IEEE Xplore 8101912 | IEEE snippet | #695 |
| 438 | 2026 | Descriptor: Multiregional Cloud Honeynet Dataset (MURHCAD) | IEEE Xplore 11495004 | IEEE snippet | #696 |
| 445 | 2026 | Dynamic cyber deception for the defense of cyber-physical systems | doi:10.48676/unibo/amsdottorato/13183 | full text | #647 |
| 447 | 2026 | DynNet: A Lightweight Distributed Framework for Topology Obfuscation in Dynamic Networks | IEEE Xplore 11433101 | IEEE snippet | #697 |
| 448 | 2025 | Effectiveness Evaluation Method for Hybrid Defense of Moving Target Defense and Cyber Deception | doi:10.3390/computers14120513 | abstract | #663 |
| 449 | 2027 | Enhancing Cyber Defense with Decoys and Machine Learning: A MITRE ATT&CK Approach | Google Scholar | Scholar snippet | #698 |
| 450 | 2026 | Enhancing Security Monitoring with Deception Techniques | OpenAlex W7160583128 | abstract | #664 |
| 453 | 2025 | Evaluation criteria of centralization options in the architecture of multicomputer systems with traps and baits | doi:10.32620/reks.2025.1.18 | title | #714 |
| 455 | 2026 | Explainable and Interoperable SIEM-Driven Adversary Engagement Based on MITRE Engage | doi:10.1007/978-3-032-35579-9_17 | title | #715 |
| 456 | 2021 | Foureye: Defensive Deception Against Advanced Persistent Threats via Hypergame Theory | doi:10.1109/tnsm.2021.3117698 | title | #716 |
| 459 | 2021 | Game Theory for Cyber Deception: From Theory to Applications | doi:10.1007/978-3-030-66065-9 | title | #717 |
| 462 | 2025 | H$^{4}$4: A Software-Defined Deception Defense System in Safeguard Defense Mode | doi:10.1109/tdsc.2025.3607846 | abstract | #665 |
| 463 | 2019 | Hardening networks against strategic attackers using attack graph games | doi:10.1016/j.cose.2019.101578 | title | #718 |
| 464 | 2026 | High-Interaction Honeypots in Cyber Deception : Evolution, Design, Deployment , and Future Trends | IEEE Xplore 11575664 | IEEE snippet | #699 |
| 466 | 2022 | HoneyComb: A Darknet-Centric Proactive Deception Technique For Curating IoT Malware Forensic Artifacts | IEEE Xplore 9789827 | IEEE snippet | #700 |
| 467 | 2026 | Honeypoint Technology | doi:10.1007/978-981-95-8391-1_4 | abstract | #666 |
| 468 | 2026 | Honeypot Placement for Joint Detection and Attacker-Type Inference: A Bayesian Stackelberg Formulation | doi:10.1109/acit69831.2026.11700210 | abstract | #667 |
| 469 | 2026 | Honeypots for AI Agent Insider Threats | doi:10.48550/arxiv.2610.26664 | abstract | #668 |
| 470 | 2024 | Honeypots in Cybersecurity: Their Analysis, Evaluation and Importance | doi:10.20944/preprints202408.0946.v1 | abstract | #669 |
| 471 | 2019 | Honware: A Virtual Honeypot Framework for Capturing CPE and IoT Zero Days | IEEE Xplore 9037501 | IEEE snippet | #701 |
| 475 | 2025 | ICS-Dev-Sec: A Security-by-Design Methodology based on Model-Driven Technology fo the Development of Secure Industrial Control System | Scholar: theses.hal.science/tel-05519258/ | Scholar snippet | #702 |
| 476 | 2023 | ICS Honeypot Interactions: A Latitudinal Study | IEEE Xplore 10386497 | IEEE snippet | #703 |
| 494 | 2025 | Koney: A Cyber Deception Orchestration Framework for Kubernetes | doi:10.1109/eurospw67616.2025.00084 | abstract | #670 |
| 495 | 2026 | Learning Sequential Deception Defense Strategy Against APT Using Stackelberg Markov Game | doi:10.1109/tifs.2026.3664334 | abstract | #671 |
| 496 | 2025 | LLM-THP: A Large Language Model-Powered Terminal Honeypot Dialogue Framework | IEEE Xplore 11207451 | IEEE snippet | #704 |
| 498 | 2025 | Method and Rules for Determining the Next Centralization Option in Multicomputer System Architecture | doi:10.47839/ijc.24.1.3875 | abstract | #672 |
| 500 | 2026 | Mirage Mesh: A Multi-Layer Cyber Deception Framework for Linux Environments | doi:10.21203/rs.3.rs-10946218/v1 | abstract | #673 |
| 502 | 2026 | Mizong: A Traceable Source-Level Analysis Protocol for Multi-Dimensional Honeypoint Telemetry | doi:10.3390/fi18100547 | abstract | #674 |
| 503 | 2018 | Modeling and Analysis of Leaky Deception Using Signaling Games With Evidence | doi:10.1109/tifs.2018.2886472 | title | #719 |
| 508 | 2020 | NeuralPot: An Industrial Honeypot Implementation Based On Deep Neural Networks | IEEE Xplore 9219712 | IEEE snippet | #705 |
| 509 | 2020 | Online Learning Methods for Controlling Dynamic Cyber Deception Strategies | doi:10.1007/978-3-030-33432-1_11 | title | #720 |
| 511 | 2026 | Optimal Information Falsification Strategies for Cyber Deception | doi:10.23919/fusion67272.2026.11726513 | title | #721 |
| 512 | 2024 | PHCG: PLC Honeypoint Communication Generator for Industrial IoT | doi:10.1109/tmc.2024.3455564 | abstract | #675 |
| 514 | 2019 | Predicting Global Trend of Cybersecurity on Continental Honeynets Using Vector Autoregression | IEEE Xplore 8905639 | IEEE snippet | #706 |
| 516 | 2025 | Proof: Pre-Training Model of Malware Family Classification Based on Active Defense | doi:10.1109/tsusc.2025.3529752 | abstract | #676 |
| 517 | 2025 | Prospect Theoretic Hypothesis Testing-based Cyber Deception | doi:10.1109/mass66014.2025.00055 | abstract | #677 |
| 518 | 2022 | Protecting IEC 60870-5-104 ICS / SCADA Systems with Honeypots | IEEE Xplore 9850329 | IEEE snippet | #707 |
| 521 | 2026 | Ransomware Defence Systems | doi:10.54938/ijemdcsai.2026.04.2.659 | abstract | #678 |
| 522 | 2026 | Real-World Case Studies | doi:10.1007/978-981-95-8391-1_9 | abstract | #679 |
| 530 | 2026 | Scalable RL-Based Honeypot Allocation for Slowing IoT Botnet Propagation | Scholar: ieeexplore.ieee.org/abstract/document/11721258/ | abstract | #680 |
| 532 | 2026 | Secure State Estimation: A Honeypot Strategy | IEEE Xplore 11743944 | abstract | #681 |
| 536 | 2011 | Security and Game Theory: Algorithms, Deployed Systems, Lessons Learned | doi:10.1017/cbo9780511973031 | title | #722 |
| 539 | 2023 | Sequential Decision Making in Games With Incomplete Information | Google Scholar | title | #723 |
| 541 | 2026 | Software-Defined Deceptive Defense (SD3) | doi:10.1007/978-981-95-8391-1_3 | abstract | #682 |
| 542 | 2018 | Stackelberg Security Games: Looking Beyond a Decade of Success | doi:10.24963/ijcai.2018/775 | title | #724 |
| 543 | 2011 | Stackelberg vs. Nash in Security Games: An Extended Investigation of Interchangeability, Equivalence, and Uniqueness | doi:10.1613/jair.3269 | title | #725 |
| 548 | 2025 | The Role of Honeypots in Modern Cybersecurity Strategies | IEEE Xplore 10883300 | IEEE snippet | #708 |
| 550 | 2024 | ThreatInsight: Innovating Early Threat Detection Through Threat-Intelligence-Driven Analysis and Attribution | doi:10.1109/tkde.2024.3474792 | abstract | #683 |
| 553 | 2025 | Towards Bio-Inspired Cyber-Deception: A Case Study of SSH and Telnet Honeypots | doi:10.1109/eurospw67616.2025.00079 | abstract | #684 |
| 554 | 2026 | Towards Innovative Intelligent Cyber Defense Approach Based on Deceptive Security and Deep Learning Techniques | doi:10.1007/978-3-032-38682-3_5 | title | #726 |
| 555 | 2026 | Traffic Tripwire Honeypoint:A new deception technique for countering covert attacks | doi:10.1109/asens69964.2026.11605302 | abstract | #685 |
| 556 | 2025 | Turn the tables: Proactive deception defense decision-making based on Bayesian attack graphs and Stackelberg games | doi:10.1016/j.neucom.2025.130139 | abstract (publisher page) | #686 |
| 557 | 2024 | Two-Layer Deception Model Based on Signaling Games Against Cyber Attacks on Cyber-Physical Systems | doi:10.1109/access.2024.3478808; OpenAlex W4403331645 | abstract | #687 |
| 560 | 2025 | Unveiling IoT Threats: A Case Study on Darknet and Honeypot Analysis | IEEE Xplore 10937952 | IEEE snippet | #709 |
| 562 | 2026 | Wartime UDP-Based Amplification DDoS Activity: A 3.5-Year Longitudinal Measurement During the Russia–Ukraine War | IEEE Xplore 11609421 | IEEE snippet | #710 |

### 13.3 Excluded: 105

| Rec | Year | Title | Judged on | Reason |
|---|---|---|---|---|
| 376 | 2014 | Achieving Source Location Privacy and Network Lifetime Maximization Through Tree-Based Diversionary Routing in Wireless Sensor Networks | IEEE snippet | the term in another sense: diversionary routing for location privacy in sensor networks |
| 381 | 2026 | Adaptive strategy optimization for cyber-physical systems under denial-of-service attacks using continuous learning automata | abstract | sensor-attacker DoS game for CPS state estimation; no deception or placement |
| 385 | 2026 | Adversarially Robust Deep Learning Models for Secure Cyber-Physical Systems: A Multi-Layer Defense Framework for Real-Time Threat Mitigation | Scholar snippet | no deception or placement content |
| 386 | 2026 | A Dynamic Cybersecurity Risk Assessment Framework for SCADA-based Industrial Control Systems | Scholar snippet | no deception or placement content |
| 387 | 2025 | A Framework for Proactive Cyber-Resilience: Non-Intrusive Modeling for Autonomous Defense | IEEE snippet | no deception or placement content |
| 388 | 2025 | A Game Theoretic Model for Strategic Defence Selection Against DDoS Attacks in IoT Networks | IEEE snippet | no deception or placement content |
| 389 | 2026 | A Generative AI-enhanced framework for intrusion detection and resilient Transient Stability Prediction in Networked Cyber–Physical Power Systems | title | no deception or placement content |
| 392 | 2026 | A Metrics-Based Method for Asset Criticality Assessment in Enterprise Network Security | abstract | no deception or placement content |
| 393 | 2026 | A Multi-Agent Framework for Replicating Human Strategic Behaviour via Hypergames | Scholar snippet | hypergames for human strategic behaviour; no cyber deception or placement |
| 396 | 2025 | An Advanced Generative AI-Based Anomaly Detection in IEC61850-Based Communication Messages in Smart Grids | abstract | no deception or placement content |
| 397 | 2024 | Analiza efikasnosti sigurnosnih operativnih centara u detekciji i reakciji na kibernetičke prijetnje | Scholar snippet | no deception or placement content |
| 398 | 2026 | Analysing and Preventing Threat Using Forward Hunting | IEEE snippet | no deception or placement content |
| 400 | 2024 | An Edge Computing-Based and Threat Behavior-Aware Smart Prioritization Framework for Cybersecurity Intrusion Detection and Prevention of IEDs in Smart Grids With Integration of Modified LGBM and One Class-SVM Models | abstract | no deception or placement content |
| 401 | 2026 | An Integrated Cyber-Risk–Based Process Safety Framework for Cybersecurity Risk Assessment in Chemical Process Industries | Scholar snippet | no deception or placement content |
| 402 | 2021 | A novel collaborative jamming method based on decoy strategy | IEEE snippet | the term in another sense: decoy strategy for radio jamming |
| 404 | 2016 | Anti-evasion Technique for the Botnets Detection Based on the Passive DNS Monitoring and Active DNS Probing | title | no deception or placement content |
| 405 | 2012 | A Personalized Product Based Recommendation System Using Web Usage Mining and Semantic Web | title | no deception or placement content |
| 407 | 2025 | APT Attack Detection in Digital Substations Leveraging The ATT&CK Model | Scholar snippet | no deception or placement content |
| 408 | 2025 | A quantitative analysis method for cross-layer attack risks in cyber-physical systems | abstract | no deception or placement content |
| 409 | 2026 | A Review of Resilient IoT Systems: Trends, Challenges, and Future Directions | abstract | no deception or placement content |
| 410 | 2026 | A review of the negative impact of adopting fourth industrial revolution technology in South Africa's mining industry | Scholar snippet | no deception or placement content |
| 414 | 2025 | A Survey on Hypergame Theory: Modeling Misaligned Perceptions and Nested Beliefs for Multi-agent Systems | Scholar snippet | hypergame theory survey (arXiv 2507.19593); no cyber deception or placement |
| 415 | 2026 | A Triangular Fractional Fuzzy CRITIC–COPRAS Framework for Cybersecurity Initiative Prioritisation | Scholar snippet | no deception or placement content |
| 416 | 2022 | Attack graph analysis: An explanatory guide | title | no deception or placement content |
| 418 | 2025 | A Weighted Expert-Based Method for Asset Criticality Assessment in Cyber Risk Evaluation | abstract | no deception or placement content |
| 420 | 2015 | Belling the CAD: Toward Security-Centric Electronic System Design | IEEE snippet | the term in another sense: electronic system design |
| 425 | 2026 | Cyber-physical security and resilience in microgrids: a comprehensive review of attack scenarios, detection methods, and defense mechanisms | abstract | no deception or placement content |
| 427 | 2026 | Cyber-Resilient Adaptive Multi-Agent Reinforcement Learning for Cyber-Resilient Edge Computing Systems | title | no deception or placement content |
| 428 | 2023 | Cybersecurity Assurance System in the New Era and Development Suggestions Thereof: From Self-Defense to Guard | title | no deception or placement content |
| 429 | 2025 | Database-Centered Causal Graph Construction for Industrial Cyber-Risk Propagation: From BPM-STPA Knowledge to Bayesian Inference | Scholar snippet | no deception or placement content |
| 431 | 2017 | DDoS Botnet Detection Technique Based on the Use of the Semi-Supervised Fuzzy c-Means Clustering | title | no deception or placement content |
| 433 | 2024 | Deep learning-enabled energy optimization and intrusion detection for wireless sensor networks | title | no deception or placement content |
| 434 | 2023 | Deep Reinforcement Learning-Driven Mitigation of Adverse Effects of Cyber-Attacks on Electric Vehicle Charging Station | abstract | no deception or placement content |
| 436 | 2024 | Denial-of-Service Attack Detection and Mitigation Strategy for Synchrophasor Data Flowing in Power Transmission System | abstract | no deception or placement content |
| 439 | 2026 | Designing a Research Methodology for Secure IIoT Implementation in Indonesia: A Research Onion–Based Methodological Design | abstract | no deception or placement content |
| 440 | 2026 | Detecção de Intrusão em Tempo Real para Mensagens GOOSE IEC 61850 via GRU Unidirecional Embarcado | abstract | no deception or placement content |
| 441 | 2023 | Developing Audit Strategy for PaaS Applications | abstract | no deception or placement content |
| 442 | 2022 | Development of Cyber Attack Model for Private Network | IEEE snippet | no deception or placement content |
| 443 | 2025 | D-GRAM: Dynamic Game-Theoretic Risk Modeling for Adaptive Cyber Defense | abstract | game-theoretic defence allocation without deception or placement |
| 444 | None | Dynamic Allocation and Identification Techniques for Enhanced AI Performance in Real-Time Applications | Scholar snippet | no deception or placement content |
| 446 | None | Dynamic Resource Management for Efficient Fast Device Placement | Scholar snippet | placement in another sense: device placement, not deception |
| 451 | 2025 | Evaluating Reinforcement Learning Agents for Autonomous Cyber Defence | title | no deception or placement content |
| 452 | None | Evaluating Resource Allocation Techniques in Machine Learning Graph Placement | Scholar snippet | placement in another sense: machine-learning graph placement |
| 454 | 2026 | Evo-TTP: Generative and robust prediction of novel cyber threat tactics using adversarial fine-tuning of large language models | abstract | no deception or placement content |
| 457 | 2026 | From threat to trust: assessing security risks of agentic AI systems | title | no deception or placement content |
| 458 | 2016 | [Front cover] | IEEE snippet | a journal front cover, not a research work |
| 460 | 2025 | Generative AI for critical infrastructure in smart grids: A unified framework for synthetic data generation and anomaly detection | Scholar snippet | no deception or placement content |
| 461 | 2022 | GridAttackAnalyzer: A Cyber Attack Analysis Framework for Smart Grids | title | no deception or placement content |
| 465 | 2024 | HMAC Security Implementation in IEC 61850 Sampled Values for Power System Infraestructure | Scholar snippet | no deception or placement content |
| 472 | 2025 | Hybrid game-theoretic security assessment of cyber-physical power systems using partial-information multi-agent reinforcement learning | abstract (publisher page) | game-theoretic security assessment of a cyber-physical power system (ATT&CK for ICS tactics, DoS on transient stability, WECC 9-bus); no deception or placement (abstract from the ScienceDirect page the user saved) |
| 473 | 2026 | Hybrid STSMC Observer and AI-Based Anomaly Detection in Smart Grids with EV Integration | title | no deception or placement content |
| 474 | 2025 | Hypergames: Modeling misaligned perceptions and nested beliefs for multi-agent systems | Scholar snippet | hypergame theory survey (Royal Holloway copy); no cyber deception or placement |
| 477 | 2025 | Identifying cyber risks in energy systems: Challenges and strategies | title | no deception or placement content |
| 478 | 2026 | IEC 61850 GOOSE: A Systematic Literature Review on the State of the Art and Current Applications | abstract | no deception or placement content |
| 479 | 2024 | Importancia de la gestión del tráfico como una primera medida de ciberseguridad en redes inteligentes | Scholar snippet | no deception or placement content |
| 480 | 2026 | Incidents of Industrial Systems Part 1: Industrial Cybersecurity | Scholar snippet | no deception or placement content |
| 481 | 2025 | Incidents of Industrial Systems–Part 2: Incident Categories | Scholar snippet | no deception or placement content |
| 482 | None | Industrial Control Panels for PLC-Based Automation Systems:(Focus: Introduction) | Scholar snippet | no deception or placement content |
| 483 | 2017 | Information Technology for Botnets Detection Based on Their Behaviour in the Corporate Area Network | title | no deception or placement content |
| 484 | None | Innovative Strategies for Scalable Machine Learning Graph Placement | Scholar snippet | placement in another sense: machine-learning graph placement |
| 485 | 2025 | INTEGRATED ASSESSMENT OF THE CYBERSECURITY LEVEL OF CRITICAL INFRASTRUCTURE IN A POST-QUANTUM ENVIRONMENT | abstract | no deception or placement content |
| 486 | 2026 | Integrating Cybersecurity Risk Assessment With Process Safety in Chemical Process Industries | Scholar snippet | no deception or placement content |
| 487 | 2026 | Integration and Adaptation of Open-Source Monitoring Tools for Detecting Anomalous User Activity in Astra Linux Special Edition | abstract | no deception or placement content |
| 488 | 2026 | Integration of digital technologies in manufacturing: a survey of industry 4.0 applications and challenges | title | no deception or placement content |
| 489 | 2024 | Intelligent framework of sustainable cyber-physical services for autonomous manufacturing industries | abstract | no deception or placement content |
| 490 | 2026 | Методи та моделі контекстно-адаптивного оцінювання ризиків інформаційної безпеки IoT-середовищ | Scholar snippet | no deception or placement content |
| 491 | 2024 | IPAttributor: Cyber Attacker Attribution with Threat Intelligence-Enriched Intrusion Data | title | no deception or placement content |
| 492 | 2025 | ISSF: An Intelligent Security Service Framework for Cloud-native Operations | abstract | no deception or placement content |
| 493 | 2026 | KEYSER: Stateful Adversarial Campaign Evaluation of ML-Based Intrusion Detection in Industrial Automation | IEEE snippet | no deception or placement content |
| 497 | 2008 | Measuring Network Security Using Bayesian Network-Based Attack Graphs | title | no deception or placement content |
| 499 | 2026 | Methodological Approaches to AssessingEnterprise Information Security Using a ProcessOriented Approach | abstract | no deception or placement content |
| 501 | 2026 | Бенчмаркинг возможностей больших языковых моделей в задачах тестирования на проникновение: Двумерная структура оценки на основе матрицы MITRE ATT&CK | abstract | no deception or placement content |
| 504 | None | Multi-Objective Device Placement Optimization in IoT Environments | Scholar snippet | placement in another sense: IoT device placement, not deception |
| 505 | 2026 | NetDiT: A Diffusion-Transformer Framework for Synthetic Network Packet Generation | abstract | no deception or placement content |
| 506 | 2012 | Network Forensics: An Analysis of Techniques, Tools, and Trends | IEEE snippet | no deception or placement content |
| 507 | 2025 | Neural Honeypoint: An Active Defense Framework Against Model Inversion Attacks | abstract | the term in another sense: a 'honeypoint' against model-inversion attacks on neural networks |
| 510 | 2026 | Operationalizing IEC 62443 Through NIST SP 800 82 Revision 3: A Localized OT Security Framework for Indonesia's Energy Sector | abstract | no deception or placement content |
| 513 | 2025 | POSEIDON: An Integrated Cybersecurity Framework for Maritime Systems with Empirical Validation | abstract | no deception or placement content |
| 515 | 2026 | Proactive Cybersecurity Risk Assessment and Implementation in ICS Protocols for Operational Technology | title | no deception or placement content |
| 519 | 2026 | Protótipo de um sistema de detecção de anomalias e intrusão não-invasivo para redes de automação baseadas em Modbus TCP | abstract | no deception or placement content |
| 520 | 2026 | Quantum Clustering Framework for Cybersecurity Vulnerability Prioritization and Risk Grouping | abstract | no deception or placement content |
| 523 | 2025 | Research on Risk Assessment and Response Strategies of Domestic Database Transformation in Electric Power Information Communication | abstract | no deception or placement content |
| 524 | 2026 | Resilient Grid Architectures for High Renewable Penetration: Electrical Engineering Strategies for 2030 and Beyond | abstract | no deception or placement content |
| 525 | 2026 | Revisión sobre la gestión de la seguridad en Internet de las Cosas | abstract | no deception or placement content |
| 526 | 2026 | Revitalisasi Distributed Control System (DCS) untuk Meningkatkan Keandalan Operasional di SHAFTHI dengan Pendekatan Kode Etik Profesi Insinyur | abstract | no deception or placement content |
| 527 | 2026 | Risk Assessment of an Academic Information System Using OCTAVE Allegro: A Case Study of SIMUNIPA at Universitas Papua | Scholar snippet | no deception or placement content |
| 528 | 2026 | Risk Assessment of Industrial Material Handling Equipment | Scholar snippet | no deception or placement content |
| 529 | 2026 | Risk-Based Vendor Reassessment: A Signal-Driven Framework | Scholar snippet | no deception or placement content |
| 531 | 2026 | Secure Semantic Communications With Information-Theoretic Honeypoints | abstract | the term in another sense: a 'honeypoint' that misleads eavesdroppers on a wireless semantic channel |
| 533 | 2026 | Securing Industrial Control Systems and Safety Instrumented Systems | IEEE snippet | a training course, not a research work |
| 534 | 2026 | Securing Reliable Fog Computing Environments: A Systematic Literature Review and Future Research Directions. | Scholar snippet | no deception or placement content |
| 535 | 2023 | Security Analysis of the Module Type Package Concept | IEEE snippet | no deception or placement content |
| 537 | 2018 | Self-adaptive System for the Corporate Area Network Resilience in the Presence of Botnet Cyberattacks | title | no deception or placement content |
| 538 | 2026 | Semantic characterization of android malware through runtime system call analysis | title | no deception or placement content |
| 540 | 2026 | Smart Cities and Cyberattacks in Communication Networks: A Case Study of Water Treatment Plants | abstract | no deception or placement content |
| 544 | 2026 | Standardized Communication Protocols for Digital Twin Integration in Discrete Manufacturing: From Machine to Plant | abstract | no deception or placement content |
| 545 | 2026 | SyneSA: A synergistic framework for dealing with cybersecurity in a globally distributed enterprise | Scholar snippet | no deception or placement content |
| 546 | 2024 | Tactical Cyber Effects | IEEE snippet | no deception or placement content |
| 547 | 2026 | The emerging landscape of cyberthreats in SCADA deployment | abstract | no deception or placement content |
| 549 | 2026 | THREAT DETECTION IN INDUSTRIAL CONTROL SYSTEMS BASED ON THE IEC 62443-3-2 RISK ASSESSMENT FRAMEWORK | Scholar snippet | no deception or placement content |
| 551 | 2025 | Tools for detecting and responding to cyber threats: a comparative analysis of cortex xdr and microsoft defender | abstract | no deception or placement content |
| 552 | 2022 | Towards an information-theoretic framework of intrusion detection for composed systems and robustness analyses | title | no deception or placement content |
| 558 | 2025 | Unmasking Nature's Deceit: A Systematic Review of Biological Deception Across Pathogens, Viruses, and Genetic Systems | Scholar snippet | deception in a non-cyber sense: biological deception |
| 559 | 2025 | Unsupervised cyberattack detection in smart grids: A novel approach integrating horizontal federated learning for the control center and substations | title | no deception or placement content |
| 561 | 2025 | Value of Information-based Deceptive Path Planning Under Adversarial Interventions | abstract | deception in a non-cyber sense: deceptive path planning in gridworlds |

### 13.4 Returned by the runs but already held: 18 titles and 2 duplicates

These have no record numbers of their own. "Found earlier in this batch" means the title is one of records 376–562.

| Title | Year | Found by | Already at |
|---|---|---|---|
| Cyber Deception: Taxonomy, State of the Art, Frameworks, Trends, and Open Challenges | 2025 | OpenAlex citations of Jay | #41 |
| Graph Neural Network-Guided TrapManager for Critical Path Identification and Decoy Deployment | 2026 | OpenAlex citations of Osman et al. | #326 |
| Strategic Deployment of Honeypots in Blockchain-based IoT Systems | 2024 | IEEE Xplore S1 | #251 |
| Cyber deception: State of the art, trends and open challenges | 2024 | Google Scholar cited-by: Jay | #41 (its arXiv preprint, 2409.07194) |
| ThreatInsight: Innovating Early Threat Detection Through Threat-Intelligence-Driven Analysis and Attribution | 2024 | Backward round: BAG-HRF | found earlier in this batch (record 550) |
| PHCG: PLC Honeypoint Communication Generator for Industrial IoT | 2024 | Backward round: BAG-HRF | found earlier in this batch (record 512) |
| H4: A Software-Defined Deception Defense System in Safeguard Defense Mode | 2025 | Backward round: BAG-HRF | found earlier in this batch (record 462) |
| Turn the tables: Proactive deception defense decision-making based on Bayesian attack graphs and Stackelberg games | 2025 | Backward round: BAG-HRF | found earlier in this batch (record 556) |
| Neural Honeypoint: An Active Defense Framework Against Model Inversion Attacks | 2025 | Backward round: BAG-HRF | found earlier in this batch (record 507) |
| A Game-theoretic Taxonomy and Survey of Defensive Deception for Cybersecurity and Privacy | 2019 | Backward round: Voznyi et al. | #493 |
| A comprehensive survey on cyber deception techniques to improve honeypot performance | 2024 | Backward round: Voznyi et al. | #45 |
| A Survey of Defensive Deception: Approaches Using Game Theory and Machine Learning | 2021 | Backward round: Voznyi et al. | #246 (its arXiv version) |
| Honeypot Allocation for Cyber Deception Under Uncertainty | 2022 | Backward round: Voznyi et al. | #195 |
| Honeypot Allocation for Cyber Deception in Dynamic Tactical Networks: A Game Theoretic Approach | 2023 | Backward round: Voznyi et al. | #213, #343 |
| Honeypot-Based Cyber Deception Against Malicious Reconnaissance via Hypergame Theory | 2022 | Backward round: Voznyi et al. | #274 |
| Method and Rules for Determining the Next Centralization Option in Multicomputer System Architecture | 2025 | Backward round: Voznyi et al. | found earlier in this batch (record 498) |
| Optimal Security Hardening over a Probabilistic Attack Graph: A Case Study of an Industrial Control System using CySecTool | 2022 | Backward round: Voznyi et al. | #56 |
| Adaptive honeypot allocation in multi-attacker networks via Bayesian Stackelberg Games | 2026 | Backward round: Voznyi et al. | #192 (record 43) |
| Интеграция и адаптация открытых средств мониторинга для обнаружения аномальной пользовательской активности в Astra Linux Special Edition | 2025 | Google Scholar cited-by: Zambianco et al. (ATT&CK decoys) | duplicate of record 487 of this batch (same paper, shown under its Russian title) |
| Cloud-native Cyber Deception with Decepto | 2024 | Google Scholar cited-by: Zambianco et al. (microservices) | duplicate of record 435 of this batch (same paper, shown under another title) |

## 14. The patent arm (A29): runs, the title screen and the reading

Added by D36, 15 November 2026. `01-search-protocol.md` §8; runs `sources.md` #624–#640, the papers named in P6's tables #641; outcome #642; amendments 4–7, #643.

### 14.1 Runs

A patent is counted once in every run that returned it, so the runs overlap.

| Run | What | Patents | T2 | Related (T1) | Excluded | Opened | Entry |
|---|---|---|---|---|---|---|---|
| P1n | S1 narrowed to title, abstract and claims (about 260) | 260 | 1 | 153 | 106 | 104 | #625 |
| P1b | "honeypoint" (about 970 reported; 910 rows saved) | 574 | 0 | 144 | 430 | 83 | #626 |
| P2a | assignee Acalvio | 21 | 0 | 21 | 0 | 1 | #627 |
| P2c | assignee Attivo | 21 | 0 | 16 | 5 | 0 | #629 |
| P2d | assignee Illusive | 11 | 0 | 10 | 1 | 4 | #630 |
| P2f | Fortinet, deception terms | 46 | 0 | 7 | 39 | 2 | #632 |
| P2g | Commvault, deception terms | 8 | 0 | 2 | 6 | 1 | #633 |
| P2h | SentinelOne, deception terms | 19 | 0 | 13 | 6 | 1 | #634 |
| P2i | Proofpoint, deception terms | 55 | 0 | 10 | 45 | 3 | #635 |
| P3b | H04L 63/1491 with placement and OT terms (about 409) | 409 | 0 | 404 | 5 | 65 | #637 |
| P4 | patents citing US 9,853,999 B2 (#347) | 47 | 0 | 10 | 37 | 10 | #638 |
| P5 | the ten leads of #374, #390, #401, #612 | 10 | 0 | 9 | 1 | 10 | #639 |
| P6 | the similarity route: the tables on the pages of 16 patents (14.7) | 71 | 0 | 68 | 3 | 39 | #640 |
| P1 | S1 on the full text (about 24,680) | not screened; first 10 saved | | | | 1 (also in P1n) | #624 |
| P2b, P2e | assignee TrapX; assignee CounterCraft | 0 | | | | | #628, #631 |
| P3a | H04L 63/1491 alone (11,205) | a count, not screened | | | | | #636 |

**Totals.** 1,394 distinct publication numbers: 1,307 from the list runs (P1n, P1b, P2a, P2c, P2d, P2f–P2i, P3b) and 87 only through P4, P5 and P6. T3 0; **T2 1 (proposed; §15.1)**; related (T1) 712; excluded 681 *[D37: T2 2 and related (T1) 711, after the user's rulings]*. Two kinds of one patent (for example CN 119728206 A and B) count twice. Opened: 262 (235 on the abstract and the first independent claim; 27 on the abstract, the claims not reached). Judged on a title alone: 1,128. Read earlier: US 9,853,999 B2 (#347). Judged on its family: 2 (US 11,212,315 B2, of the family of US 10,616,276 B2, and CN 122339831 A, the application publication of the granted CN 122339831 B; the page of the one read stands for both). Judged on a title and list snippet: 1. *[D38: run P1c (§18.4) adds 102: related (T1) 32 and excluded 70; opened 38, judged on a title alone 56, on a title and list snippet 4, on the family 4. The arm then counts 1,496: T3 0, T2 2, related (T1) 743, excluded 751; opened 300; judged on a title alone 1,184.]*

### 14.2 How the title screen worked

Amendment 6 (`sources.md` #643). Claude, 14–15 November 2026: a keyword rule applied by script to the 1,307 patents of the list runs, then the flagged patents read. The rule was written during the screening, not before it. In order:
1. A patent already opened as a lead or an early read kept that reading (36).
2. A Chinese design registration (a publication number ending in S) was excluded as a product appearance, not a method (356). 355 of the 574 patents of the "honeypoint" run are of this kind, 353 of them for honey products (packaging, jars, labels); Google Patents returned them for the query.
3. A title with words from another field (model inversion, radar, jamming, GNSS, nucleic acids, antibodies, cancer, honey products and similar) was excluded as the term in another sense (69).
4. A title with a deception word (honeypot, honeynet, honeypoint, decoy, deception, lure, trap, bait, tripwire and similar) and a security word was related (T1) if it showed no placement decision (298), and flagged for opening if it also carried a placement word (deploy, placement, allocation, layout, arrange, optimi-, location, position, orchestrat-) (31).
5. A patent of run P3b not caught above was related (T1) if its title showed no placement decision (204), and flagged otherwise (14).
6. A patent of the all-patents runs of Acalvio, Attivo and Illusive with a security word in its title was related (T1) (16).
7. Everything else was excluded: no deception or placement content in the title (283).

**The flagged patents** (45) were opened and read on 14–15 November 2026: 41 related (T1), 2 excluded after reading, one (US 9,853,999 B2) already read (#347), and one excluded on its title (FR 2845565 A1, a fishing lure). Patents reached only through P4 and P5 (48) were handled the same way: the leads and the closest of the citing patents were opened (12), the rest excluded on titles.

**Corrections to the rule's output, by title only.** Four patents the rule had related were moved to excluded on a second look at their titles: KR 10-2022-0164736 A (a protein decoy), TW M507653 U ("Lure"), EP 3 418 937 A1 (a decoy of an operation inside an integrated circuit) and US 2023/0336588 A1 (simulated phishing). None was opened.

### 14.3 The second round of reading: run P1n

Amendment 6, second part. Every result of run P1n carries a deception word, a placement word and an OT word in its title, abstract or claims. The title rule in 14.2 ignores that: a neutral title was excluded, or a deception title related, without anyone reading what the patent does. A check of the excluded P1n titles on 15 November found 142 excluded patents on a title alone, of which 56 had a security-, network-, control- or power-related word in the title (a keyword match, which includes some false hits such as "Chiral control"). The first nine pages read turned up CN 122339846 A, a placement method in a power cyber-physical system (§15.1), so the reading was extended. In all 41 pages were opened in this round:
- 35 patents the rule had excluded on their titles: now 4 excluded, 30 related (T1), 1 proposed T2;
- 6 patents the rule had related on their titles: now 5 related (T1), 1 excluded.

Reading method: the Google Patents page through Claude's fetch tool, which returns a summary of what Claude asked for (the title, applicant, dates, abstract, the first independent claim, whether deception assets are involved and whether the patent chooses where, how many or which to deploy and by what rule). It is a summary by a small model, not the page text; for CN 122339846 A and B the claims were read in detail on both pages and the description's reward, attacker model and experiments were asked for separately. The tool read the first 100,000 characters of long pages. The reading was interrupted when the fetch tool reached a usage limit late on 14 November (UTC) and went on after the limit lifted (14.4).

**Pages that failed.** For 24 of the 262 pages the first fetch returned a server error, at the plain address or at /en, and another address was read; the entry of each says which. Three pages needed more than that, and all three were read in the end. The A document of CN 119051914 A failed at both addresses at first, so the page of its granted B document, which carries the same title, was read in its place; the A document's page was read afterwards, at /zh, once the fetch tool was available again. It shows the same method, and its claims carry no version label, so it is not confirmed whether they are the A or the B text. CN 120498905 A failed at the plain address and at /en and was read at /zh, Google's machine translation of the Chinese. CN 122621588 A, excluded on a cut title (14.5), was refused at its /en address ("robots_disallowed") and was read afterwards at /zh in the same way (the end of the fourth round, 14.4).

**What the reading showed.** Of the 41, 1 proposed T2, 35 related (T1) and 5 excluded. None of the T1 patents chooses decoy positions by an objective, a budget or attack paths. Their deception content is a honeypot as a data source, a honeypot or decoy as one response action, a fixed or threshold rule for where to put it (CN 113904819 A, CN 122053124 A, CN 116436653 A, WO 2025/130185 A1) or the honeypot's own construction.

### 14.4 The third, fourth and fifth rounds of reading

**Third round: 68 candidates.** After the second round, 68 patents were chosen for reading because their titles, in runs P1n, P3b and P1b, suggested a strategy, a game, a configuration, an attack path or a cyber-physical honeypot, or because the title rule had excluded a security, industrial-control or power title of run P1n, or a security title of run P1b that Google Patents had cut. The choice was Claude's, by eye, from the titles. They were opened on 15 November 2026 by the same route as in 14.3 (the fetch tool on the Google Patents page; 10 pages returned a server error at the address ending "/en" and were read at the address without it). All 68 were opened.

| Run | The title rule's call | Patents | Opened | Related (T1) | Excluded | Proposed T2 |
|---|---|---|---|---|---|---|
| P1n | related | 25 | 25 | 25 | 0 | 0 |
| P1n | excluded | 20 | 20 | 10 | 10 | 0 |
| P3b | related | 7 | 7 | 7 | 0 | 0 |
| P1b | related | 7 | 7 | 7 | 0 | 0 |
| P1b | excluded | 9 | 9 | 9 | 0 | 0 |

**What the reading showed.**
- **No T3 and no further proposed T2** (proposed T2 among the 68: 0). None of the readings showed zones or conduits as numeric inputs.
- **Two are borderline between T1 and T2 and are the user's call** (D36): CN 117675308 A (Electric Power Research Institute of State Grid Sichuan Electric Power and co-applicants), a game-theoretic honeypot placement along high-harm attack paths with a deployment-cost term, framed for power grids but built on a generic host-vulnerability graph; and CN 121012683 A (Anhui University of Traditional Chinese Medicine), a bilevel optimisation of how many detection and protection "baits" go in each subgraph of a substation network. Both are counted related (T1) here as first passes. Claude's lean: the first T1 (likely); the second T2 (likely), because its Chinese title and claim 1 call it a deception-defence method and its construction is that of Jay 2023 (#305, #312), a lean that a re-read on the evening of 15 November changed from T1 (§15.2). *[D37: the user ruled CN 117675308 A T1 and CN 121012683 A T2 on 16 November 2026; the third round's table above still counts CN 121012683 A as related (T1).]*
- **The 29 patents the rule had excluded on their titles** (CN 106778210 A, CN 109685200 B, CN 120263467 A, CN 121750505 A, CN 122411384 A, CN 110222505 A, CN 116232777 A, US 12,589,673 B1, US 2024/0323228 A1, CN 116625171 A, CN 122248026 A, CN 121967028 A, CN 118432759 A, CN 116642373 A, CN 118631442 A, CN 119696772 A, CN 122386884 A, CN 120638394 A, US 6,836,847 B1, WO 2025/210623 A2, CN 117579302 B, CN 120822218 A, CN 122394875 A, CN 122204438 A, CN 119484109 B, CN 117113335 A, CN 118590275 A, CN 121808769 A, CN 120956520 A): **19 proved related (T1) on reading and 10 stayed excluded.** 24 of the 29 were added last, after the other 44 candidates had been read and the batch looked finished, because the only proposed T2 patent had come from a neutral title the rule had excluded: they are the excluded titles of runs P1n and P1b that name a cyber, industrial or power subject and had not yet been opened. The related ones are not all incidental. In some the deception is a side element: a honeynet step in a verification method (CN 106778210 A), an industrial-control honeypot in a train node (CN 120263467 A), a honeypot as a digital-twin body (CN 122411384 A), a honeypot host as one response in a DDoS method (CN 116232777 A), honeypots as the source of attack samples (CN 110222505 A), honeypot ports on an EV charger (US 12,589,673 B1), a trap grid in the description of an early-warning method (CN 120956520 A), a model that reads four-honey logs (CN 118590275 A) and a trapping environment as one of four actions chosen by reinforcement learning (CN 122204438 A). In others it is the subject, but no rule for where, how many or which is given: a generator of honeypot protocol streams (CN 109685200 B), PLC honeypot code (CN 122386884 A), process honeypots against ransomware (CN 117113335 A), decoy domain accounts (CN 117579302 B), smart-contract honeypoints (CN 121808769 A), a scene builder for a honey array (CN 122394875 A) and a gatekeeper graph that picks honeypot service types (CN 119484109 B). US 2024/0323228 A1 is the published application of the substation decoy-network patent US 12,425,450 B2 (#311), a correction of the title rule: a deception patent that its neutral title had excluded. CN 121750505 A has a passage that sets trap points on the critical path by node value, centrality and risk exposure, without a formula and outside the claims. The 10 still excluded are three anti-drone navigation-spoofing devices, a federated-learning interconnection device, a cryptographic trapdoor, two quantum-key-distribution patents for power networks, a grid-frequency control method, a hardware tamper-resistance patent and a token-based compliance firewall. So the title rule's exclusions are not safe; 14.5 says what the screen leaves unseen.
- **The rest** either describe a honeypot's construction, its responses, its configuration or a fixed rule for where it goes (core hosts, peripheral hosts, one gateway, free addresses in a segment), or are games and optimisations on a generic network that choose strategies, an address mutation, a decoy-data proportion per port or which weak honey points to replace, not positions. The two nearest by method outside OT are in 15.2.
- Reading limits as in 14.3: a summary by a small model; the claims were not reached for 6 of the 68; long pages were read to character 100,000; the Chinese pages through Google's machine translation.


**Fourth round: 39 patents.** A last check of the title rule's exclusions, made after the third round. All 39 had been excluded on their titles (37 of run P1b, 1 of P1n and 1 of P4). Claude chose them by eye from the excluded titles that named a security, attack or defence topic or that Google Patents had cut (21 of the 39 are cut titles; the list is 15.6). They were opened on 15 November 2026 by the route of 14.3; 13 returned an error at the plain address and were read at another address (the entries say which). The last 3 were read after the others, late on 15 November, when the fetch tool had come back from a usage limit: they are the 3 cut-title exclusions of run P1b that showed a security-type word in the visible part of the title (14.5), found by a keyword match and not chosen by eye (CN 115752492 A, CN 122621588 A, WO 2015/196373 A1: a bee-keeping route, an IPv6 address scanner and laser drilling), and all 3 stay excluded. **26 proved related (T1) and 13 stayed excluded:** the rule's exclusions were wrong for 67 per cent of these, and of the 21 cut titles 13 proved related (T1). In the related patents deception is a data source for a detector or a classifier, a honeypoint-fed alarm system, a trigger, a file-level bait against ransomware or the construction of a honeypot, with no objective, budget or zones. Two come nearer. CN 119363420 A places decoy-username honey points on a set attack path planned from an anticipated attacker strategy, with no objective or budget. **CN 121356815 A** (Guangzhou University; §15.2) builds a MulVAL attack graph, scores honeypoint positions on three coverage objectives (area, the share of attack paths blocked, vulnerability rank) and outputs NSGA-II Pareto sets under a count cap, with a criticality-weighted environmental factor; Google's list cut its title, and its text has no industrial or power word. It is T1: the OT setting, IEC 62443 zones and conduits as numeric inputs, an ATT&CK-grounded stage term and baselines are missing.

**Fifth round: 23 patents, from run P6 (14.7).** They were named in the tables on the pages of the closest patents, except CN 118101346 B, which CN 120498905 A names in its background: 20 were new to the data and 3 were in it already on a title only. **20 proved related (T1) and 3 excluded** (CN 120455078 A, CN 120498762 A, CN 120415882 A: power-sector defence patents with no deception in the text that was read; one is truncated before its claims). 7 of the 23 choose positions, counts or addresses by a formal rule or game, all outside OT: CN 120658528 A, CN 118802292 B, CN 116155542 B, CN 115580430 A, CN 118400169 B, CN 121664448 A, CN 119383021 B. None combines an OT multi-zone setting, IEC 62443 zones and conduits as numeric inputs, an ATT&CK-grounded stage term and baselines, which are the elements of A28. The claims were not reached for 3 (CN 120498762 A, US 12,425,417 B2, CN 116132190 A). The strongest are in 15.2; the others are in 15.7.


### 14.5 What the screen cannot see

A placement method behind a neutral or truncated title. 485 patents are related (T1) on a title or a list snippet and 646 are excluded on a title alone; none of these had its abstract or claims read. Google Patents cuts long titles in its result lists with "…"; 246 of the 1,394 patents were screened on a cut title (the opened ones were read in full). The thesis limitation says so (`01-search-protocol.md` §13). *[D38: run P1c adds 4 related (T1) on a title and list snippet and 56 excluded on a title alone (§18.4).]*

**Run P1n, the run most likely to hold a neighbour, after the rounds of reading.** 104 of its 260 patents were opened. Of the 156 that were not, 67 are related (T1) on a title and 89 are excluded on a title. Of the 89 excluded, 8 carry a security-, network-, control- or power-related word in the visible title (AU2022291426A1 Chiral control; CN304151907S Industrial control honeynet system structure distribution display model; DE202026001140U1 Device for detecting moving objects and arrangement with such a device; EP2474556A2 APCDD1 inhibitors for treating, diagnosing or detecting cancer; EP2562560A1 Method and system for detecting fraudulent positioning information from a …; JP2019508063A Oncolytic virus vector and use thereof; US20100124746A1 Method for the detection of gene transcripts in blood and uses thereof; WO2021009033A1 Method and device for detecting a decoy operation of a gnss system): false hits, anti-spoofing of satellite navigation, or the design registration of §14.6. The rest are biomedical, chemical or otherwise outside the field. **The open question is the 67 related on a title alone.** Of the 47 P1n patents the rule had related on a title and that were read, 46 stayed related (T1), 1 proved excluded and 0 proved T2 or T3; the one proposed T2 patent came from the rule's excluded group. Opening the 67 would settle it (§11).

**Run P1b.** 83 of its 574 distinct patents were opened (the fourth round took 37 of its exclusions), and up to about 400 more results that the run reported were never seen (§10). 13 excluded patents of the run are still judged on a title that Google Patents had cut, and none of them shows a security-type, industrial-control or power word in the visible part. The three that did (CN 115752492 A, CN 122621588 A, WO 2015/196373 A1) were read last, at the end of the fourth round, and stay excluded. **A correction to an earlier reading of this residual:** it was first taken to be false hits. In the fourth round 21 cut-title exclusions were opened and 13 proved related (T1), CN 121356815 A among them, so a cut title can hide a placement method, and the 13 not opened are a limit, not a set of false hits. Every patent of the run was returned by the query "honeypoint", which also returned honey products, so a match does not by itself show that a patent concerns deception.

**The OT block has no power-grid words, and several runs depend on it.** Block O (§4) names industrial control, SCADA, ICS, operational technology, cyber-physical, programmable logic controller, smart grid, substation, critical infrastructure and IIoT. It has no "power grid", "power system", "electric power", "new power system", "distribution network" or "power plant". Runs P1, P1n and P3b on the patent side, and strings S1, S2 and S5 on the paper side, need a word of that block in the title, the abstract or the claims, so a work that describes a power network in other words is not returned by them. CN 121356815 A, which no run of that kind could return, shows it can matter. Strings S3 and S4, runs P1b, P2a–P2i, P4, P5 and P6, the thirteen earlier rounds of web searching and the forward-citation searches do not depend on the block, so the paper side has other routes to power-system work, but how much they covered was not measured. A widened re-run of the patent run (P1c) and of the three paper strings is offered in D36 and was not made. *[D38: made on 16 November 2026 and screened (§18); the classification run P3b was not repeated with the six words.]*

### 14.6 Section 9's confirmation rule for patents

Four excluded patents carry a deception-like term and an OT term in the title, and the user confirmed all four exclusions on 16 November 2026 (D37; none was confirmed before) (`sources.md` #642):
- **CN 116318314 B**, "A method for deploying drone decoy equipment for hierarchical substations" (#959), and **CN 115914014 B**, "… unmanned aerial vehicle decoy equipment of transformer substation" (#957), both of Guangzhou Power Supply Bureau, Guangdong Power Grid. Both read: physical anti-drone navigation-spoofing transmitters, not network deception.
- **CN 117834239 A**, "A traffic processing method and system based on mimicry industrial control firewall" (#964). Read: a mimic-defence firewall of heterogeneous instances; its untrusted traffic goes to a sandbox or honeypot. "Mimicry" is not in block D; the rule is applied as a precaution.
- **CN 304151907 S**, "Industrial control honeynet system structure distribution display model": a design registration (a product appearance), excluded on its title and not opened.

### 14.7 The similarity route: run P6

Amendment 7 (`sources.md` #643); run entry #640, papers #641. On 15 November 2026, from the Google Patents page of each of nine patents (level 1) and of seven pages that level 1 led to (level 2), the rows of four tables were taken through the fetch tool: "Similar documents", "Patent citations", "Cited by" and "Families citing this family". The depth was fixed at two by Claude and the route was not run to saturation.

| Page | Level | Patent rows | Paper rows |
|---|---|---|---|
| CN 121356815 A | 1 | 5 | 20 |
| CN 122339846 A | 1 | 3 | 0 |
| CN 121012683 A | 1 | 4 | 21 |
| CN 117675308 A | 1 | 28 | 1 |
| US 12,261,855 B2 | 1 | 21 | 20 |
| CN 120034354 A | 1 | 10 | 16 |
| CN 118694612 B | 1 | 21 | 5 |
| CN 121603304 B | 1 | 21 | 5 |
| CN 118842645 A | 1 | 18 | 17 |
| CN 119254537 A | 2 | 15 | 19 |
| CN 121664448 A | 2 | 17 | 11 |
| CN 117240502 A | 2 | 13 | 13 |
| EP 4 586 550 A1 | 2 | 27 | 0 |
| CN 120896776 B | 2 | 10 | 16 |
| CN 119182584 B | 2 | 13 | 16 |
| CN 120498898 A | 2 | 17 | 13 |
| **Total** | | **243** | **193** |

| What | Count |
|---|---|
| Distinct patents (the two kinds of one patent counted once) | 229 |
| With a deception term in the title | 60 |
| — already in the data | 27 (13 read earlier, 13 related (T1) on a title only, 1 the published application of #347) |
| — new, opened | 15 |
| — new, judged related (T1) on the title | 18 |
| Without a deception term in the title | 169 |
| — already in the data | 6 |
| — new, opened (power-sector or defence-allocation neighbours) | 5 |
| — counted and not entered | 158 |
| Patents in the data that carry P6 | 71 (38 found by P6 alone, 33 found by earlier runs too) |

**What the figures show.** The keyword runs already held 27 of the 60 deception-titled patents that the tables name (45 per cent); 33 were new, so the runs had not covered the neighbourhood of the closest patents. That measures their reach around those patents, not recall in general, because the tables are Google's selection and not a sample. **None of the patents found by P6, and none that it found again, is T3 or T2.** Of the 20 opened and new, 17 are related (T1) and 3 excluded; the 18 judged on the title are in §16, with "deception title (P6)" as the ground.

**Limits.** The tables of the other formal placement patents read at level 1 (CN 120658528 A, CN 117061224 A, CN 119383021 B, CN 118802292 B, CN 116155542 B, CN 115580430 A, CN 118400169 B) were not taken. A table shows what Google chooses to show. Patent rows whose titles carry no deception term were counted and not entered (158), so a placement method behind a neutral title that a table names is not in the data. The pages were read through a fetch tool that returns a small model's summary, so a row can be wrong. The depth is Claude's choice.

**The papers in the tables** (`sources.md` #641). The 16 pages name 193 non-patent documents; 57 distinct titles that carried a deception, OT-system or placement-type word were typed, and 36 of them carry a deception term. One, Arunagirinathan et al. (2025), uses "deception attacks" in the control-theory sense and also carries "cyber-physical" in the title, so §9 asks the user to confirm its exclusion (Claude recommends it stand). *D37: confirmed, 16 November 2026.* Of the other 35, 8 were in the log already and 27 were not (23 per cent in the log); the 27 are related (T1) on their titles and none was read. None of the new titles names an OT or power setting. The paper searches were built to find work close to A28's claim, not to list the deception literature, so the figure does not show that the claim's neighbours were missed. Confidence: likely.

## 15. Patents read

### 15.1 Proposed T2

The user confirms every T2 decision (`01-search-protocol.md` §9). This one is of the same kind as Dong et al. (#417), which the user ruled T2 in D35. **D37: the user confirmed it T2 on 16 November 2026.**

| Entry | Number | Title | Applicant | Runs | Tier |
|---|---|---|---|---|---|
| #727 | CN 122339846 A | A method and system for active defense of power cyber-physical systems | Guangzhou University | P1n | T2 |

**Clause by clause against A28's draft claim** (D36 states the effect): OT/CPS setting, yes (an electric power information physical system). A decoy budget, yes ("a defence-resource constraint", a preset quantity). A stated objective, a reinforcement-learning reward of capture bonus minus intrusion penalty minus bait cost (description, not the claims). Asset criticality as a numeric input, yes (asset value in the state; baits tiered by it). IEC 62443 zones and conduits, no: the network is an undirected graph. Interception along ATT&CK-grounded attack paths, no: no ATT&CK, no attack paths; the attacker picks targets by a Softmax over asset value, availability, degree centrality and neighbour value. Validation against random and centrality baselines: one random baseline, no network, node counts or numbers given. The granted document CN 122339846 B (2026-08-11) has the same claim 1.

### 15.2 The closest by method

**The user's five borderline calls.** All related (T1) by his decision of 15 November 2026: Cybersense GmbH's US 12,261,855 B2, Bosch's EP 4 586 550 A1, CN 122339820 A, CN 120034354 A and CN 118694612 B.

| Entry | Number | Title | Applicant | Runs | Tier |
|---|---|---|---|---|---|
| #728 | CN 122339820 A | An optimization method for honeypoint deployment strategy in a two-layer IoT architecture | Guangzhou University | P1b | T1 |
| #729 | CN 120034354 A | Honeypot deployment method, device, equipment, medium and product based on attack and defense benefits | Beijing University of Posts and Telecommunications | P3b | T1 |
| #730 | US 12,261,855 B2 | Procedures for improving security in an electronic communications network | Cybersense GmbH | P5 | T1 |
| #731 | CN 118694612 B | A honey spot deployment method based on improved multi-objective firefly algorithm | State Grid Jiangxi Electric Power (Information and Telecommunication Branch) | P1b | T1 |
| #914 | EP 4 586 550 A1 | Method for placing honeypots in a vehicle fleet network | Robert Bosch | P3b, P4 | T1 |

**Other near neighbours: first passes by Claude, not among the nine calls.** CN 121603304 B is the nearest in a power setting that names an optimisation. Two from the third round are borderline between T1 and T2 and are the user's call (D36): CN 117675308 A, a game-theoretic honeypot placement along high-harm attack paths with a deployment-cost term, framed for power grids but built on a generic host-vulnerability graph, and CN 121012683 A, a bilevel optimisation of how many detection and protection "baits" go in each subgraph of a substation network. Claude's lean on the first is T1 (likely). On the second it is T2 (likely): the Chinese title and claim 1 call it a deception-defence method, its construction is that of Jay 2023 (#305, #312), and it has no budget, experiments or citations; D36's first draft leaned T1, and a re-read changed the lean (the entry has the quotations). Two more are formal placement methods outside OT: CN 118842645 A (attack paths rebuilt from honeypot logs, a cost, time and risk objective, centrality ranking, a cap on protected nodes) and CN 122457351 A (a Bayesian-belief game giving a Nash deployment probability over candidate honeypot nodes, with a deployment cost). The nearest outside OT, found in the fourth and fifth rounds, are CN 121356815 A (a MulVAL attack graph, three coverage objectives with an attack-path blocking term, a criticality-weighted environmental factor, NSGA-II Pareto sets and a count cap; no OT wording at all in its text) and CN 120658528 A (a decision-tree search that maximises the attacker's cost of re-planning; positions and vulnerability types; a machine-capacity cap; the applicant is a power utility, the text has no OT wording). Each lacks the OT setting, IEC 62443 zones and conduits as numeric inputs, an ATT&CK-grounded stage term and baselines. **D37: the user ruled the first T1 and the second T2 on 16 November 2026; CN 121603304 B stays T1.**

| Entry | Number | Title | Applicant | Runs | Tier |
|---|---|---|---|---|---|
| #775 | CN 121603304 B | Intelligent target deployment method and system for power scene APT attack | Guangzhou University | P1n, P3b, P6 | T1 |
| #838 | CN 117675308 A | High-risk path defense method based on adaptive depth-limited search and game theory | Electric Power Research Institute of State Grid Sichuan Electric Power; State Grid Beijing Electric Power; State Grid Smart Grid Research Institute; State Grid Corporation of China | P3b | T1 |
| #886 | CN 121012683 A | Method, device, equipment and medium for preventing TSN network spoofing in substations | Anhui University of Traditional Chinese Medicine | P1n, P3b | T2 (D37; T1 until then) |
| #749 | CN 118842645 A | Honey array defense strategy dynamic generation method and system based on large model | Guangzhou University | P1b | T1 |
| #785 | CN 122457351 A | A cognitive game theory model for attack and defense based on Bayesian belief updates | Huangpu Research Institute of Guangzhou University | P3b | T1 |
| #771 | CN 121356815 A | A multi-dimensional performance evaluation method and related equipment for honeypoint deployment based on multi-objective optimisation | Guangzhou University | P1b | T1 |
| #879 | CN 120658528 A | Multi-honeypot deployment device and method for honeypot perception multi-stage attack | State Grid Shanghai Electric Power Co Ltd | P6 | T1 |

### 15.3 The other 85 patents opened in the first round

In the order of `sources.md` #727–#988. US 9,853,999 B2 (#347) was read earlier and is not repeated.

| Entry | Number | Title | Applicant | Runs | Tier |
|---|---|---|---|---|---|
| #735 | CN 117176452 A | A dynamic honey point placement method and device | Guangzhou University (Tian Zhihong et al.) | P1b, P6 | T1 |
| #736 | CN 117220968 B | A honey point domain name optimization deployment method, system, equipment and storage medium | Guangzhou University | P1b, P6 | T1 |
| #739 | CN 118101332 B | An adaptive honey spot deployment method based on attack graph | Guangzhou University | P1b | T1 |
| #740 | CN 118101333 B | Multi-strategy fusion honey point domain name optimizing deployment method | Guangzhou University | P1b | T1 |
| #742 | CN 118233223 B | A control and defense graph construction method for the four-honey dynamic defense system | Guangzhou University | P1b, P6 | T1 |
| #746 | CN 118740492 B | A network system defense method based on control and guard graph | Guangzhou University | P1b, P6 | T1 |
| #748 | CN 118802363 A | Honey spot adaptive deployment method, system and readable storage medium | Guangzhou University | P1b | T1 |
| #750 | CN 119051894 B | A honey spot deployment optimization method | Guangzhou University | P1b | T1 |
| #751 | CN 119172102 B | A close-range honeypot deployment method based on attack graph | Guangzhou University | P1b | T1 |
| #752 | CN 119182584 B | Dynamic honey point deployment method and system based on attack graph and Shapley values | Guangzhou University | P1b, P6 | T1 |
| #755 | CN 119728206 B | A method for constructing and deploying command honeypots based on large models | Guangzhou University | P1b, P6 | T1 |
| #756 | CN 119830282 A | Policy generation method for deploying file honey points based on large language model | Guangzhou University | P1b | T1 |
| #763 | CN 120128391 A | A method and system for automatically deploying honey spots based on business scenario matching | Guangzhou University and DBAPPSecurity | P1b | T1 |
| #768 | CN 120956536 B | Honey-bait deployment method and system based on honeypoints | Guangzhou University | P1b | T1 |
| #769 | CN 121037132 B | A proactive defense method against APT attacks based on a four-honeycomb system | Guangzhou University | P1b | T1 |
| #773 | CN 121530770 B | A method and system for dynamic orchestration of cloud honey points based on software-defined deception defense | Guangzhou University and QAX | P1b | T1 |
| #778 | CN 121814467 A | Dynamic trapping network deployment method and system based on Markov decision process | Guangzhou University | P1b | T1 |
| #780 | CN 121967044 A | Attack intention driven cloud-native honey point dynamic arrangement method and system | Guangzhou University | P1b | T1 |
| #793 | CN 110099040 B | Defense method for detecting and intercepting intranet attack sources by deploying large numbers of bait hosts | Jiangsu Jiyuan Information Technology | P1n, P3b | T1 |
| #795 | CN 110430190 B | Deception defense system based on ATT&CK, construction method and full link defense realization method | Beijing Jingwei Xinan Technology | P3b | T1 |
| #797 | CN 110784361 A | Virtualized cloud honeynet deployment method, device, system and computer-readable storage medium | State Grid (Henan EPRI) | P3b | T1 |
| #798 | CN 110784476 A | A power monitoring active defense method and system based on virtualized dynamic deployment | State Grid (Henan EPRI) | P3b | T1 |
| #799 | CN 110990115 A | Containerized deployment management system and method for honeypots | Bozhi Safety Technology | P1n | T1 |
| #801 | CN 111600953 A | Method for realizing distributed deployment based on honeypot system | Guangzhou Jeeseen Network Technologies | P3b | T1 |
| #803 | CN 112448910 A | Social engineering honeypot system, honeypot system deployment method, and storage medium | Beijing University of Posts and Telecommunications | P3b | T1 |
| #813 | CN 115150140 A | Distributed attack trapping system and method based on centralized and unified defense deployment | Yunnan Power Grid | P3b | T1 |
| #816 | CN 115913632 A | A honeynet cluster deployment method for an industrial control system | China Communications Information Technology Group | P1n | T1 |
| #817 | CN 116015755 B | Mother-child portable industrial control honeynet system and deployment method | Huaneng Group | P1n | T1 |
| #828 | CN 116599765 B | Honeypot deployment method | Softpole Network Technology (Beijing) | P1b | T1 |
| #829 | CN 116915417 A | Honeynet deployment method and device suitable for industrial control environment | China Mobile | P1n, P3b | T1 |
| #830 | CN 117061191 B | Bait file deployment method, device, and medium based on incomplete-information games | Harbin Engineering University | P1n, P3b | T1 |
| #833 | CN 117459289 A | A security exploration reinforcement learning method based on honeypot and pseudo-honeypot deployment | State Grid Fujian Electric Power | P3b | T1 |
| #839 | CN 117749483 A | Trap construction method, system, equipment and medium for electric power network protection | State Grid Shandong (Xintai Power Supply) | P1b | T1 |
| #840 | CN 117792749 A | Dynamic industrial control honeypot deployment method based on deep reinforcement learning | Xidian University | P1n | T1 |
| #842 | CN 118041562 A | Honeypot deployment method and device, computer storage medium and terminal | 360 Digital Security | P1n, P3b | T1 |
| #843 | CN 118041645 A | Prophet honey spot deployment method, system and server based on intelligent time-delay differential game | PLA Information Engineering University (Tan Jinglei et al.) | P1b | T1 |
| #846 | CN 118573401 A | Service deployment method for cooperatively manufacturing multidimensional security level by network based on honey network | Tongji University | P3b | T1 |
| #847 | CN 118573443 A | Honeypot deployment method, system and server based on intelligent time lag differential game | PLA Information Engineering University | P3b, P6 | T1 |
| #854 | CN 119254537 A | A defense method for power system honey array dynamic deployment based on learning perception | State Grid Jiangxi Electric Power | P3b, P6 | T1 |
| #857 | CN 119341821 B | Industrial Internet of things honeypot deployment method and device based on antagonism reinforcement learning | Zhejiang University | P1n, P3b, P6 | T1 |
| #863 | CN 119892454 A | Method and system for building a deception-based defense system for industrial control systems (Conpot) | Naval University of Engineering | P1b, P1n, P3b, P6 | T1 |
| #875 | CN 120512723 A | Internet of things data transmission optimization system based on intelligent routing | Jiangsu Sairong Technology | P1n, P3b | T1 |
| #877 | CN 120639507 B | Honey point deployment optimization method (translated) | Peng Cheng Laboratory | P1b | T1 |
| #878 | CN 120658435 A | Network security management optimization method and system for non-control type service | Guizhou Power Grid | P3b | T1 |
| #881 | CN 120811687 A | Cross-domain honey array collaborative deployment method, device and equipment based on federal learning | Jizhi Hainan Information Technology | P1b | T1 |
| #883 | CN 120934858 A | Screening algorithm optimization and defense method and device for electric power Internet of things defense strategy | Guangdong Power Grid (Electric Power Research Institute) | P3b | T1 |
| #892 | CN 121585406 A | An adaptive optimization method and system for dynamic interaction strategy of SSH honeypots based on PPO | Beijing University of Posts and Telecommunications; State Grid Liaoning Electric Power Research Institute | P3b | T1 |
| #896 | CN 121792145 A | Methods ... for deploying honeypots that integrate self-game theory and reinforcement learning | China Southern Power Grid | P3b | T1 |
| #905 | CN 122339831 B | Method and apparatus for deploying and updating network defenses based on attack behavior monitoring and prediction | Xidian University and State Grid Jiangxi Electric Power | P1b | T1 |
| #909 | KR 10-1917062 B1 | Honeynet method, system and computer program for mitigating link flooding attacks of software defined network | KAIST | P4 | T1 |
| #913 | EP 4 482 083 A1 | Cyber defence deception effectiveness metrics | British Telecommunications | P1n, P5 | T1 |
| #915 | LU 506571 B1 | An adaptive dynamic traffic allocation method in mimic defense | Jiaxing Vocational and Technical College | P1n, P3b | T1 |
| #916 | US 10,097,577 B2 | Predicting and preventing an attacker's next actions in a breached network | Illusive Networks (now Proofpoint) | P2d | T1 |
| #917 | US 10,291,650 B2 | Automatically generating network resource groups and assigning customized decoy policies thereto | Illusive Networks (now Proofpoint) | P5 | T1 |
| #918 | US 10,326,796 B1 | Dynamic security mechanisms for mixed networks | Acalvio | P2a, P3b, P4 | T1 |
| #919 | US 10,382,483 B1 | User-customized deceptions and their deployment in networks | Illusive Networks (now Proofpoint) | P2d, P2i | T1 |
| #920 | US 10,404,747 B1 | Detecting malicious activity by using endemic network hosts as decoys | Illusive Networks (now Proofpoint) | P2d, P2i | T1 |
| #921 | US 10,432,665 B1 | Creating, managing and deploying deceptions on mobile devices | Illusive Networks (now Proofpoint) | P2d, P2i | T1 |
| #922 | US 10,616,276 B2 | Tunneling for network deceptions | Acalvio | P4 | T1 |
| #923 | US 10,986,126 B2 | Intelligent-interaction honeypot for IoT devices | Palo Alto Networks | P4 | T1 |
| #924 | US 11,777,988 B1 | Probabilistically identifying anomalous honeypot activity | Rapid7 | P4, P6 | T1 |
| #925 | US 11,777,989 B1 | Automated deployment of decoy production networks | Raymond James Financial | P5 | T1 |
| #926 | US 12,041,094 B2 | Threat sensor deployment and management | Amazon Technologies | P3b | T1 |
| #927 | US 12,335,308 B1 | System and method for modelling a cyber-physical system to act as a honeypot for cyberattacks | University of Toronto (Mohamed, Kundur) | P3b, P5 | T1 |
| #928 | US 12,341,814 B2 | Implementing decoys in a network environment | SentinelOne (Attivo) | P2h | T1 |
| #930 | US 12,495,073 B2 | Cloud-based deception technology with auto-decoy and breadcrumb creation based on user's role and without on-premises appliances | Zscaler | P3b, P5 | T1 |
| #931 | US 12,500,918 B2 | Website security with deceptive responses | Target Brands | P4 | T1 |
| #932 | US 12,506,781 B2 | Generating deceptions using web assembly binaries | IBM | P4 | T1 |
| #933 | US 12,519,833 B2 | Automated deployment of decoy production networks | Raymond James Financial | P5 | T1 |
| #935 | US 12,592,968 B2 | Cloud-based deception technology with granular scoring for breach detection | Zscaler | P3b, P5 | T1 |
| #936 | US 12,657,340 B2 | System and method for generating decoy data and sharding sensitive data utilizing quantum computing | Bank of America | P4 | T1 |
| #937 | US 2018/0309787 A1 | Deploying deception campaigns using communication breadcrumbs | Cymmetria | P5 | T1 |
| #940 | US 2025/0039236 A1 | Efficient token deployment in cyber threat detection and deception system | Commvault | P2g | T1 |
| #941 | US 2025/0150488 A1 | Identifying network-based attacks on physical operational technology (OT) devices with decoy OT devices | Fortinet | P1n, P2f, P3b | T1 |
| #942 | US 2025/0175456 A1 | AI-controlled sensor network for threat mapping and characterization and risk adjusted response | Qomplx | P1n | T1 |
| #944 | US 2026/0067333 A1 | Deception as a service (DaaS) system with large scale deployment of template-based decoys | Fortinet | P2f | T1 |
| #945 | US 9,866,575 B2 | Management and distribution of virtual cyber sensors | General Electric | P3b | T1 |
| #947 | WO 2021/221930 A1 | Threat sensor deployment and management | Amazon Technologies | P3b | T1 |
| #948 | WO 2024/121950 A1 | Placement location selection device, placement location selection method, and placement location selection program | Mitsubishi Electric | P3b | T1 |
| #951 | WO 2025/180750 A1 | Automatic deployment of breadcrumbs | British Telecommunications | P3b, P6 | T1 |
| #952 | WO 2025/180755 A1 | Automatic deployment of decoys | British Telecommunications | P3b | T1 |
| #959 | CN 116318314 B | A method for deploying drone decoy equipment for hierarchical substations | Guangzhou Power Supply Bureau, Guangdong Power Grid | P1n | X |
| #976 | CN 120710776 A | A deployment strategy for access control and authentication of dynamic power data transmission | Guangxi Power Grid | P3b | X |
| #983 | US 12,609,964 B2 | Systems and methods for cloud-based threat alerts and monitoring | Zscaler | P3b, P5 | X |
| #984 | US 2026/0189981 A1 | Bidirectional bandwidth allocation in a SASE network | Cato Networks | P3b | X |

### 15.4 The 40 other patents opened in the second round

| Entry | Number | Title | Applicant | Runs | Tier |
|---|---|---|---|---|---|
| #765 | CN 120455293 A | A method for evaluating the simulation capabilities of industrial control honeypots | Guangzhou University | P1n | T1 |
| #781 | CN 121967096 B | Traffic trip line generation method and system based on honey points for industrial control equipment | Guangzhou University | P1n | T1 |
| #788 | CN 107391598 B | Automatic threat information generation method and system | Beihang University | P1n | T1 |
| #789 | CN 107566390 B | A system and method for analyzing network security of industrial control system based on threat intelligence | Northeastern University | P1n | T1 |
| #790 | CN 108319161 B | An industrial SCADA system simulation platform | Zhejiang University | P1n | T1 |
| #792 | CN 110058565 A | An industrial control PLC system fingerprint simulation method based on Linux OS | China Electronic Technology Cyber Security | P1n | T1 |
| #804 | CN 112948821 A | APT detection early warning method | not shown on the page | P1n | T1 |
| #808 | CN 113904819 A | Safety system applied to industrial control network | not shown on the page | P1n | T1 |
| #810 | CN 114430344 A | Attack organization identification method based on industrial control flow and threat information correlation analysis | Northeastern University | P1n | T1 |
| #815 | CN 115883169 A | Response method and response system for industrial control network attack message based on honeypot system | Shenyang Power Supply Company, State Grid Liaoning Electric Power | P1n | T1 |
| #824 | CN 116318936 B | A networked industrial control asset identification method based on improved decision tree | Northeastern University | P1n | T1 |
| #825 | CN 116389016 A | Network security analysis method and system | China Information Technology Security Evaluation Center | P1n | T1 |
| #826 | CN 116405258 B | Smart grid honeypot design method and system based on reinforcement learning | Information Engineering University of the PLA Cyberspace Force | P1n | T1 |
| #827 | CN 116436653 A | Honeypot dynamic configuration method, device, honeypot intrusion detection system and medium | Hangzhou Jiaer Technology | P1n, P3b | T1 |
| #844 | CN 118174904 A | Industrial control network security protection processing system based on encrypted software defined network | China Electronic Product Reliability and Environmental Test Institute | P1n | T1 |
| #855 | CN 119276627 B | Network security deduction method and device for power industry, electronic equipment and storage medium | Guangdong Power Grid; Electric Power Research Institute of Guangdong Power Grid | P1n | T1 |
| #859 | CN 119449467 B | A Modbus-based federated learning threat detection method and system | Yantai University; Jinan Sanze Information Security Evaluation | P1n | T1 |
| #861 | CN 119520154 A | A reinforcement learning decision method, device and storage medium for network threats | Liaocheng Power Supply Company, State Grid Shandong Electric Power | P1n | T1 |
| #862 | CN 119728243 B | Intrusion detection and defense system and method for industrial control network of gate pumps in water conservancy industry | Ningbo Hongtai Water Resources Information Technology | P1n | T1 |
| #864 | CN 119945718 A | A network attack identification and blocking method and system based on deep packet inspection | Yunnan Power Grid | P1n | T1 |
| #868 | CN 120180441 A | Industrial Internet operating system security risk prediction method and system based on knowledge graph | Tongji University | P1n | T1 |
| #871 | CN 120474762 A | Power system network attack identification method and device based on intrinsic security | Nanjing Power Supply Company, State Grid Jiangsu Electric Power | P1n | T1 |
| #872 | CN 120498742 A | Industrial Internet spoofing prevention technical system based on supergame | Huzhou University | P1n | T1 |
| #876 | CN 120567475 A | Defensive strategy recommendation system and method | China Oil and Gas Pipeline Network; National Pipe Network Group North Pipeline | P1n, P3b | T1 |
| #880 | CN 120768798 A | Survivability testing method and system based on dynamic heterogeneous network | Wuhan Minghe Yongan Technology | P1n | T1 |
| #885 | CN 121012674 A | An intelligent system for intrusion detection | Tianjin Shengyou Technology | P1n | T1 |
| #890 | CN 121567381 A | Network security self-adaptive learning method and related device for large electric power model | China Electric Power Research Institute | P1n | T1 |
| #894 | CN 121690744 A | AI power industry control network threat detects and self-evolution defense system | Zhejiang Xinzhishu Carbon Technology | P1n | T1 |
| #897 | CN 121907578 A | Multi-mode APT defense transmission system based on power line channel characteristic adaptation | Lianyungang Wanchang Technology | P1n | T1 |
| #898 | CN 122053124 A | Safety protection method and device for industrial control system and storage medium | China Nuclear Control System Engineering | P1n | T1 |
| #900 | CN 122053601 A | Thermoelectric group industrial control security situation sensing system supporting global expansion | Qingdao Thermoelectricity Group | P1n | T1 |
| #901 | CN 122093107 A | Cross-domain collaborative emergency response and attack suppression method for key infrastructure | China Southern Power Grid Digital Power Grid Group Information Communication Technology | P1n | T1 |
| #903 | CN 122179137 A | A method, device, and electronic equipment for network security situation awareness in open-pit mines | Liaoning Technical University | P1n | T1 |
| #910 | TW 202301205 A | Industrial control network threat intelligent detection system and training system with deep learning which can predict the attack category of normal or abnormal packets | ICP DAS; National Chung Hsing University | P1n | T1 |
| #950 | WO 2025/130185 A1 | Substation data security monitoring system based on SCD modeling | Yunnan Electric Power Test and Research Institute Group; Electric Power Research Institute of Yunnan Power Grid | P1n | T1 |
| #954 | CN 106685953 A | Unknown file detection system and method based on security baseline sample machine | Beijing Ahtech Network Safe Technology | P1n | X |
| #957 | CN 115914014 B | Acceptance detection system, method, equipment and medium for unmanned aerial vehicle decoy equipment of transformer substation | Guangzhou Power Supply Bureau, Guangdong Power Grid | P1n | X |
| #958 | CN 115914555 A | A three-dimensional security system based on big data research | Beijing Fusion Huikong Technology | P1n | X |
| #964 | CN 117834239 A | A traffic processing method and system based on mimicry industrial control firewall | Electric Power Research Institute of State Grid Zhejiang Electric Power | P1n | X |
| #977 | CN 120811596 B | A secure communication method for substation dispatch data network based on quantum tunnel encryption | Inner Mongolia Huiqiang Technology | P1n | X |

### 15.5 The 64 other patents opened in the third round

| Entry | Number | Title | Applicant | Runs | Tier |
|---|---|---|---|---|---|
| #734 | CN 117113335 A | Ransomware defense method, system and storage medium based on process honeypoints | Guangzhou University; Beijing Yuanbao Technology Co Ltd | P1b | T1 |
| #737 | CN 117579302 B | Intranet lateral movement attack defense method, system, device and storage medium | Guangzhou University | P1b | T1 |
| #744 | CN 118590275 A | An abnormal node detection method based on honey-stepping log and traceability graph attention neural network | Guangzhou University | P1b | T1 |
| #754 | CN 119484109 B | Gatekeeper graph decision method and system based on defined organization attack preference | Guangzhou University | P1b, P6 | T1 |
| #758 | CN 120090879 A | Honeypot address mutation decision method, system and readable storage medium | Guangzhou University | P1b | T1 |
| #760 | CN 120110797 A | A honey array local transformation method and device based on Shapley value | Guangzhou University | P1b, P6 | T1 |
| #761 | CN 120110798 A | A honeycomb graph evolution method based on Moran process | Guangzhou University | P1b | T1 |
| #762 | CN 120110799 A | A three-party honey array diagram scheduling method | Guangzhou University | P1b | T1 |
| #766 | CN 120822218 A | A method, device and electronic device for analyzing PLC variable association relationships based on weight calculation | Guangzhou University | P1b | T1 |
| #776 | CN 121644139 B | Dynamic honey matrix defense method based on dendritic cell algorithm and related equipment | Guangzhou University | P1b | T1 |
| #777 | CN 121808769 A | Security protection method and system based on large-model-generated smart contract honeypoints | Guangzhou University | P1b | T1 |
| #782 | CN 122293425 B | Data honey point confusion decision method and system based on strategy gradient evolution game | Guangzhou University | P1b | T1 |
| #783 | CN 122386884 A | Structured text code generation method for PLC honey points | Guangzhou University | P1n | T1 |
| #784 | CN 122394875 A | Semantic association TTP scene construction method for software defined spoofing defense system | Huangpu Research Institute of Guangzhou University; China Information Technology Security Evaluation Center | P1b | T1 |
| #787 | CN 106778210 A | A kind of industrial control system functional safety verification method based on immunological learning | Chengdu Wonderful Technology Co Ltd | P1n | T1 |
| #791 | CN 109685200 B | Fog computing industrial protocol construction method and construction system based on generative confrontation network | East China Normal University; Shanghai Industrial Control Safety Innovation Technology Co Ltd | P1n | T1 |
| #794 | CN 110222505 A | Industrial control attack sample expansion method and system based on genetic algorithm | North China University of Technology | P1n | T1 |
| #800 | CN 111343174 B | Intelligent learning type self-response industrial internet honeypot induction method and system | Information and Data Security Solutions Co Ltd | P1n, P3b | T1 |
| #802 | CN 111756761 A | Network defense system and method based on flow forwarding and computer equipment | Hangzhou DBAPPSecurity Co Ltd | P1n, P3b | T1 |
| #806 | CN 113285926 B | Honey pot trapping method and device for power monitoring system and computer equipment | Southern Power Grid Digital Grid Research Institute Co Ltd | P1n | T1 |
| #807 | CN 113572785 A | Honeypot defense method and device for nuclear power industrial control system | 6th Research Institute of China Electronics Corp | P1n | T1 |
| #811 | CN 114462023 A | Honeypot defense control method and device for power plant control system | Inner Mongolia University of Technology | P1n | T1 |
| #812 | CN 114528546 A | Power information network defense system and method based on honey net | State Grid Liaoning Electric Power Co Ltd; Information and Telecommunication Branch | P1n | T1 |
| #818 | CN 116032512 A | A multi-node dynamic trapping system and method for industrial control network | Beijing Huaan Network Information Technology Co Ltd | P1n | T1 |
| #821 | CN 116155580 A | A network security management method and system based on high-interaction honeypot | Guangdong Power Grid Co Ltd | P1n, P3b | T1 |
| #822 | CN 116192495 A | Design method, system, equipment and medium of honey farm of power monitoring system | State Nuclear Power Automation System Engineering | P3b | T1 |
| #823 | CN 116232777 A | DDoS attack detection and defense method and related equipment based on statistical measurement in SDN-IIoT | Beijing Research Institute of Automation for Machinery Industry; Beijing Jiaotong University | P1n | T1 |
| #834 | CN 117478395 A | An anti-honeypot camouflage attack method based on reinforcement learning | State Grid Fujian Electric Power Co Ltd; Information and Telecommunication Branch of State Grid Fujian Electric Power Co Ltd | P1n, P3b | T1 |
| #835 | CN 117527332 A | Design and implementation of honeypot dynamic configuration and honeynet based on online learning | Sichuan University | P1n, P3b | T1 |
| #837 | CN 117560175 A | An SDN-based adaptive high-interaction quasi-dynamic simulation cloning method and device | Information and Telecommunication Branch of State Grid Zhejiang Electric Power Co Ltd | P1n, P3b | T1 |
| #841 | CN 117857086 A | Industrial network threat trapping system for power industry scene | Bozhi Safety Technology Co Ltd | P1n, P3b | T1 |
| #848 | CN 118611970 A | Network security management system and network security management method for industrial control network | an individual applicant | P1n, P3b | T1 |
| #851 | CN 119009976 A | Smart power grids honeypot system based on neural network | University of Shanghai for Science and Technology | P1n, P3b | T1 |
| #852 | CN 119135401 B | Industrial control system threat trapping method based on machine learning algorithm | Naval University of Engineering | P1n | T1 |
| #856 | CN 119299172 A | A deception defense system design method based on heterogeneous fusion | Beijing Jiwo Technology | P3b, P6 | T1 |
| #865 | CN 120165922 A | Industrial network security honeypot simulation and threat trapping system | Saisheng Digital Economy Research Institute Guangzhou Co Ltd | P1n, P3b | T1 |
| #869 | CN 120263467 A | Train onboard network security protection method, device and electronic equipment | Ningbo Helishi Information Security Research Institute Co Ltd | P1n | T1 |
| #873 | CN 120498746 A | Method and system for generating tripwire based on light load data simulation in power system network | Electric Power Research Institute of State Grid Xinjiang Electric Power | P1n, P3b | T1 |
| #884 | CN 120956520 A | A method and system for early warning of cybersecurity risks based on multi-source data fusion | Guangzhou Jiayang Information Technology Co Ltd | P1b | T1 |
| #888 | CN 121333732 A | A method for automatically generating honeypot response strategies based on large models | Shenzhen Fanyun Digital Intelligence Technology Co Ltd | P1n | T1 |
| #891 | CN 121585386 A | An Automatic Protection Method for Unknown Application-Layer Threats Based on Dynamic Compensation Mechanism | Guizhou Power Grid Co Ltd | P1n, P3b | T1 |
| #895 | CN 121750505 A | Full-flow data monitoring and early warning method in vehicle-network interaction scene | State Grid Information and Telecommunication Group Co Ltd; China Industrial Control Systems Cyber Emergency Response Team; State Grid Smart Internet of Vehicles Co Ltd; State Grid Hubei Electric Vehicle Service Co Ltd | P1n | T1 |
| #904 | CN 122204438 A | Cyber security dynamic active defense system based on attack chain look-ahead deduction | individual inventors (Wei Jun, Su Xiaowei, Li Gaoyuan) | P1b | T1 |
| #907 | CN 122411384 A | Industrial control system vulnerability physical hazard assessment method and system based on digital twinning | Nanjing University of Posts and Telecommunications | P1n | T1 |
| #908 | CN 122457332 A | A method for real-time detection and management of dynamic attack surfaces based on multi-spatial awareness | Information and Telecommunication Branch of State Grid Hubei Electric Power Co Ltd | P1n, P3b | T1 |
| #911 | CA 3041865 A1 | High-fidelity model-driven deception platform for cyber-physical systems | Battelle Memorial Institute | P1n | T1 |
| #912 | EP 3 291 501 A1 | System and method for using a virtual honeypot in an industrial automation system and cloud connector | Siemens AG; Siemens Corporation | P3b | T1 |
| #934 | US 12,589,673 B1 | Electric vehicle (EV) charging system | an individual applicant | P1n | T1 |
| #938 | US 2024/0106839 A1 | Cyber-physical protections for edge computing platforms | Intel Corp | P1n, P3b | T1 |
| #939 | US 2024/0323228 A1 | Method for securing digital substations and system thereof | GridSentry Private Ltd | P1n | T1 |
| #943 | US 2026/0052163 A1 | Cybersecurity Device for Emulating Networked Devices in Industrial Systems | an individual applicant | P1n, P3b | T1 |
| #946 | WO 2018/044410 A1 | High interaction non-intrusive industrial control system honeypot | Siemens AG; Siemens Corporation | P1n, P3b | T1 |
| #949 | WO 2024/162927 A2 | Digital twin-supported honeypot for cyber-secure smart sea ports | BTS Kurumsal Bilisim Teknolojileri | P3b | T1 |
| #953 | WO 2026/030820 A1 | System and method for modelling a cyber-physical system to act as a honeypot for cyberattacks | University of Toronto | P3b | T1 |
| #962 | CN 116625171 A | A UAV detection and countermeasure method, system, electronic equipment and storage medium suitable for substations | Guangzhou Power Supply Bureau of Guangdong Power Grid Co Ltd | P1n | X |
| #963 | CN 116642373 A | Substation UAV defence and inspection coordination method and system | State Grid Power Space Technology Co Ltd | P1n | X |
| #967 | CN 118432759 A | Unmanned aircraft detection and countering system and method | Hainan Electric Power Industry Development Co Ltd | P1n | X |
| #968 | CN 118631442 A | Power quantum secure communication method, networking method, system, device and medium | Anhui Jiyuan Software Co Ltd; State Grid Information and Telecommunication Group; State Grid Zhejiang Electric Power; Electric Power Research Institute of State Grid Zhejiang Electric Power | P1n | X |
| #970 | CN 119696772 A | Environmental adaptation and security assessment method and system for substation quantum key distribution system | Information and Telecommunication Branch of State Grid Zhejiang Electric Power; Anhui Jiyuan Software Co Ltd | P1n | X |
| #975 | CN 120638394 A | Method for identifying grid frequency signal assessment standards | Hubei Energy Group Xiangyang Yicheng Power Generation Co Ltd | P1n | X |
| #979 | CN 121967028 A | Method and system for editing anonymous liability data of industrial Internet of things based on blockchain | Anhui University | P1n | X |
| #980 | CN 122248026 A | An industrial interconnection device and its usage method | Gongda Offshore Engineering Jiangsu Intelligent Equipment Technology Co Ltd | P1n | X |
| #985 | US 6,836,847 B1 | Software protection for single and multiple microprocessor systems | Johns Hopkins University (from a legal-events entry; the page has no applicant field) | P1n | X |
| #988 | WO 2025/210623 A2 | Compliance firewall for inline validation of tokens in communication, storage, and financial transactions | an individual (Sangam Das) | P1n | X |

### 15.6 The 38 other patents opened in the fourth round

All excluded on a title by the rule before they were read (14.4). CN 121356815 A is in 15.2.

| Entry | Number | Title | Applicant | Runs | Tier |
|---|---|---|---|---|---|
| #732 | CN 116506213 A | A server protection method and device based on dynamic IP switching | Guangzhou University | P1b | T1 |
| #733 | CN 117034264 A | A ransomware protection method, system and storage medium based on file monitoring | Guangzhou University; Beijing Yuanbao Technology Co Ltd | P1b | T1 |
| #738 | CN 118018266 A | A method, system and storage medium for diverting traffic to account honey points based on a honey-court proxy | Guangzhou University | P1b | T1 |
| #743 | CN 118400185 B | A detection method for model inversion attacks | Guangzhou University | P1b | T1 |
| #745 | CN 118690197 A | Method, device, medium and electronic device for generating classified data security identification | Guangzhou University | P1b | T1 |
| #747 | CN 118784365 A | URL feature drainage method, system, storage medium and electronic device of front-end honey court | Guangzhou University | P1b | T1 |
| #753 | CN 119363420 A | A method for generating account lines in a domain environment | Guangzhou University | P1b | T1 |
| #757 | CN 120086839 A | A method for investigating causal association attacks of alarms by integrating honeypoint intelligence | Guangzhou University | P1b | T1 |
| #767 | CN 120834966 B | Global threat perception method and system for public network | Guangzhou University | P1b | T1 |
| #770 | CN 121234365 A | A ransomware defense method and related equipment based on whitelisted file honey points | Guangzhou University | P1b | T1 |
| #774 | CN 121561896 A | Lesu software defense method and related equipment based on Lesu encrypted white list file backup and recovery | Guangzhou University | P1b | T1 |
| #779 | CN 121902146 A | Asset simulation system for threat awareness | Guangzhou University | P1b | T1 |
| #786 | CN 122496235 A | Self-adaptive noise reduction and attacker high-fidelity attribution method for honey arrays | Huangpu Research Institute of Guangzhou University; China Information Technology Security Evaluation Center | P1b | T1 |
| #836 | CN 117544335 A | Bait activation method, device, equipment and storage medium | China Mobile Communications Group Co Ltd; China Mobile Group Jiangsu Co Ltd | P1b | T1 |
| #850 | CN 118839331 A | Lesu attack detection method and device and storage system | Huawei Technologies Co Ltd | P1b | T1 |
| #853 | CN 119254471 A | Network unknown attack detection method, system, device and storage medium | China Electric Power Research Institute and several State Grid entities | P1b | T1 |
| #860 | CN 119484152 A | Address security assessment model training method, device, equipment and medium | Peng Cheng Laboratory | P1b | T1 |
| #866 | CN 120165986 B | Multisource information fusion processing method, device, equipment and medium | Peng Cheng Laboratory | P1b | T1 |
| #867 | CN 120165989 A | Network attack homology analysis method, device, computer equipment and storage medium | Peng Cheng Laboratory | P1b | T1 |
| #870 | CN 120378229 A | Safety alarm information processing method and device based on multi-agent collaboration | PowerChina Jiangxi Electric Power Engineering Co Ltd | P1b | T1 |
| #887 | CN 121173601 A | Attack behavior analysis method based on attack mapping and path analysis | Information and Telecommunication Branch of State Grid Jiangxi Electric Power Co Ltd | P1b, P6 | T1 |
| #889 | CN 121396685 B | A proactive defense method and system based on a large model | Shandong Inspur New Century Technology Co Ltd | P1b | T1 |
| #899 | CN 122053184 A | Network space inverse survey and drawing method, device, equipment and medium | Webray Tech Group Inc | P1b | T1 |
| #902 | CN 122160087 A | Consortium blockchain-assisted large-scale model collaborative SAGVN threat trapping method | Nanjing Tech University | P1b | T1 |
| #906 | CN 122365495 A | Ransomware detection methods, devices, electronic equipment, storage media and products | Uniontech Software Technology Co Ltd | P1b | T1 |
| #955 | CN 115242460 B | Cloud platform security architecture system and implementation method thereof | Unit 63891 of the PLA | P1b | X |
| #956 | CN 115752492 A | Method and device for determining bee-keeping transition route, and network device | China Telecom Corp Ltd | P1b | X |
| #960 | CN 116346436 B | A lightweight malicious traffic identification method based on ViT improvement | Shenyang Ligong University | P1b | X |
| #961 | CN 116578970 A | A method for detecting social robots in heterogeneous graphs based on graph neural network | Guangzhou University | P1b | X |
| #965 | CN 117939468 A | A method for constructing a swarm of unmanned vehicles based on safety reputation evaluation | Tongji University | P1b | X |
| #966 | CN 118332529 A | A method, device, medium and electronic device for generating data security identification | Guangzhou University | P1b | X |
| #969 | CN 119051914 A | A network attack path reconstruction and evaluation method and system | Guangzhou University | P1b | X |
| #974 | CN 120498905 A | Method, system, storage medium and program product for automatically constructing an attack knowledge graph from cyber threat reports using a large language model | State Grid Shanghai Electric Power Co Ltd; NARI Information and Communication Technology Co Ltd | P1b | X |
| #978 | CN 121832975 A | Embedded program programming system, method and device based on CAN bus | Beijing Institute of Technology | P1n | X |
| #981 | CN 122621588 A | IPv6 active address probing method and device based on a context-aware prefix space tree | Guangzhou University | P1b | X |
| #982 | US 10,419,313 B2 | Industrial network monitoring | General Electric Co (now GE Vernova Infrastructure Technology LLC) | P4 | X |
| #986 | US 9,516,063 B2 | System, method, and computer-readable medium for performing automated security validation on a virtual machine | Raytheon Co | P1b | X |
| #987 | WO 2015/196373 A1 | Control method and system for utilizing laser pulse to process hole on hollow component | Siemens AG; Siemens Corp | P1b | X |

### 15.7 The 22 other patents opened in the fifth round (run P6)

CN 118101346 B was named in a background; the others in the tables of 14.7. CN 120658528 A is in 15.2.

| Entry | Number | Title | Applicant | Runs | Tier |
|---|---|---|---|---|---|
| #741 | CN 118101346 B | A method for automatically generating attack graph interaction rules for honeypoint deployment | Guangzhou University | P1b | T1 |
| #759 | CN 120110791 A | Intelligent array chart generation method and system based on spoofing defense strategy | Guangzhou University | P1b, P6 | T1 |
| #764 | CN 120200848 A | Honeypot configuration method based on graph neural network | Guangzhou University | P6 | T1 |
| #772 | CN 121418134 B | A Method and System for Lateral Movement Attack Path Analysis Based on Virtualized Decoy Networks | Guangzhou University | P6 | T1 |
| #796 | CN 110768987 A | A method and system for dynamic deployment of virtual honeynet based on SDN | University of Electronic Science and Technology of China | P6 | T1 |
| #805 | CN 113132398 A | Array honeypot system defense strategy prediction method based on Q learning | China University of Petroleum (East China) | P6 | T1 |
| #809 | CN 114363093 A | Honeypot deployment active defense method based on deep reinforcement learning | Zhejiang Juntong Intelligent Technology Co Ltd | P6 | T1 |
| #814 | CN 115580430 A | A defense method and device for attack tree honeypot deployment based on deep reinforcement learning | Zhejiang University of Technology | P6 | T1 |
| #819 | CN 116132190 A | Internet of things honey network system based on reinforcement learning and dynamic scheduling method | Henan University | P6 | T1 |
| #820 | CN 116155542 B | Minimum deployment method and system for breadcrumb spoofing resources in information network | PLA Information Engineering University | P6 | T1 |
| #831 | CN 117061224 A | A honeynet configuration optimization method based on non-cooperative incomplete information game | Nanjing University of Aeronautics and Astronautics | P6 | T1 |
| #832 | CN 117240502 A | An active defense method and system for new power systems | China Electric Power Research Institute; State Grid Shanghai Electric Power Co Ltd; State Grid Corporation of China | P6 | T1 |
| #845 | CN 118400169 B | Internet of things spoofing trapping strategy evaluation method and system based on DDPG secure game | PLA Information Engineering University | P6 | T1 |
| #849 | CN 118802292 B | Method, device, equipment, storage medium and product for deployment of honeypots in honeynets | China Mobile Communications Group Co Ltd; China Mobile Group Anhui Co Ltd | P6 | T1 |
| #858 | CN 119383021 B | A honeypot IP dynamic configuration method based on model predictive control | Information and Telecommunication Branch of State Grid Jiangxi Electric Power Co Ltd | P6 | T1 |
| #874 | CN 120498898 A | Electric honey pot construction method and system based on large language model | PowerChina Jiangxi Electric Power Engineering Co Ltd | P6 | T1 |
| #882 | CN 120896776 B | Construction Method and System of Dynamic Threat Capture System | Bozhi Safety Technology Co Ltd | P6 | T1 |
| #893 | CN 121664448 A | A method, system, device, and medium for generating dynamic honeycomb defense strategies based on Stackelberg game theory | China Southern Power Grid Digital Power Grid Group Information and Communication Technology Co Ltd | P1b, P6 | T1 |
| #929 | US 12,425,417 B2 | Systems and methods for generation and implementation of cyber deception strategies | The MITRE Corporation | P6 | T1 |
| #971 | CN 120415882 A | An active defense system for security management of distribution network of power monitoring system | Laiwu Power Supply Company of State Grid Shandong Electric Power Co | P6 | X |
| #972 | CN 120455078 A | Digital power grid attack defense methods, devices, equipment, media and program products | China Southern Power Grid Co Ltd; China Southern Power Grid Electric Power Research Institute | P6 | X |
| #973 | CN 120498762 A | Method, device, equipment, storage medium and program product for controlling network attack of digital power grid | China Southern Power Grid Co Ltd; China Southern Power Grid Electric Power Research Institute | P6 | X |

## 16. Patents related (T1) on a title: 485

Not opened. "Why" is the title rule's ground: a deception title, classification H04L 63/1491, or a security patent of Acalvio, Attivo or Illusive. US 11,212,315 B2 shares its family and title with US 10,616,276 B2 (#922), which was read; US 2023/0060323 A1 (Illusive) was judged on its title and list snippet. The 18 found only by run P6 have the ground "deception title (P6)": a deception term in the title as a table on a closest patent's page shows it, and no placement decision in it; US 2016/0359905 A1 has the title of US 10,291,650 B2 (read, #917) and is probably its published application, which was not checked. Titles cut with "…" are cut in Google Patents' list.

| Number | Title | Runs | Why |
|---|---|---|---|
| CA2714549A1 | Off-line mms malware scanning system and method | P3b | H04L 63/1491 |
| CA3178468A1 | Method for automatic aggregating and enriching data from honeypots | P3b | deception title |
| CN105306487A | Active deception type power dispatching SCADA intrusion detection method based … | P1n | deception title |
| CN105516159A | Smart Grid based intelligent attack capture system | P3b | H04L 63/1491 |
| CN105552886B | Intelligent deception system based on Smart Grid | P1n | deception title |
| CN105721417A | Honeypot apparatus carried in industrial control system, and industrial control … | P3b | deception title |
| CN106326742A | System and method for determining modified web pages | P3b | H04L 63/1491 |
| CN106357637A | Active defense system in allusion to smart energy terminal data | P3b | H04L 63/1491 |
| CN106561028A | Quarantining An Internet Protocol Address | P3b | H04L 63/1491 |
| CN107070929A | A kind of industry control network honey pot system | P3b | deception title |
| CN107360145B | Multi-node honeypot system and data analysis method thereof | P3b | deception title |
| CN107509193A | The information processing terminal, information processing system, computer- … | P3b | H04L 63/1491 |
| CN107770199A | It is a kind of towards industry internet with the industry control agreement … | P1n, P3b | H04L 63/1491 |
| CN108429739B | Method, system and terminal equipment for identifying honeypots | P1n, P3b | deception title |
| CN108600193B | Industrial control honeypot identification method based on machine learning | P1n | deception title |
| CN108833333B | A Honeypot System Based on DCS Distributed Control | P3b | deception title |
| CN108881179A | Transmission line of electricity applied to smart grid reliably monitors system | P3b | H04L 63/1491 |
| CN109067778B | Industrial control scanner fingerprint identification method based on honeynet … | P1n | deception title |
| CN109167796B | A Deep Packet Detection Platform Based on Industrial SCADA System | P1n, P3b | H04L 63/1491 |
| CN109257326B | Method and device for defending against data stream attack, storage medium and … | P3b | H04L 63/1491 |
| CN109462599B | Honeypot management system | P3b | deception title |
| CN109474625A | Network safety protection method, device and embedded system | P3b | H04L 63/1491 |
| CN109889488A | A kind of industry control network honey net safety protective system based on … | P1n | deception title |
| CN110035079A | A kind of honey jar generation method, device and equipment | P3b | H04L 63/1491 |
| CN110071929B | Method for defending massive bait capture attack sources based on … | P3b | deception title |
| CN110138759A | The lightweight self-adapting detecting method and system of Packet-In … | P3b | H04L 63/1491 |
| CN110198300A | A kind of honey jar operation system fingerprint concealment method and device | P3b | H04L 63/1491 |
| CN110266650B | Recognition method of Conpot industrial control honeypot | P1n | deception title |
| CN110336811A | A kind of Cyberthreat analysis method, device and electronic equipment based on … | P3b | H04L 63/1491 |
| CN110351237B | Honeypot method and device for CNC machine tools | P1n, P3b | deception title |
| CN110351238A | Industry control honey pot system | P3b | deception title |
| CN110365636A | Method and device for identifying data source of industrial control honeypot … | P1n | deception title |
| CN110519272A | A kind of industrial control system information security test device and method … | P3b | H04L 63/1491 |
| CN110677414A | Network detection method and device, electronic equipment and computer readable … | P3b | H04L 63/1491 |
| CN110691097A | Industrial honey pot system based on hpfeeds protocol and working method … | P3b | deception title |
| CN111126440B | An integrated industrial control honeypot identification system and method … | P3b | deception title |
| CN111212053B | A Homologous Attack Analysis Method for Industrial Control Honeypots | P1n, P3b | deception title |
| CN111224973A | Network attack rapid detection system based on industrial cloud | P1n, P3b | H04L 63/1491 |
| CN111327636B | A Reverse Method of S7-300PLC Private Protocol Involving Network Security | P3b | H04L 63/1491 |
| CN111343139B | Multi-mode judgment method for industrial control mimicry security gateway | P3b | H04L 63/1491 |
| CN111343158B | Network shooting range platform based on virtualization technology | P1n, P3b | H04L 63/1491 |
| CN111371758B | Network spoofing efficiency evaluation method based on dynamic Bayesian attack graph | P6 | deception title (P6) |
| CN111404934B | Network attack tracing method and system based on dynamic and static … | P3b | H04L 63/1491 |
| CN111541705B | A method for automatic extraction of TTP and clustering of attack teams | P3b | H04L 63/1491 |
| CN111628981A | A network security system and method that can be linked with an application … | P3b | H04L 63/1491 |
| CN111641634B | Honey net based active defense system and method for industrial control network | P1n, P3b | deception title |
| CN111698257A | Industrial information physical system security detection method for multi- … | P3b | H04L 63/1491 |
| CN111711599A | Safety situation perception system based on multivariate mass data fusion … | P3b | H04L 63/1491 |
| CN111818052B | CNN-LSTM-based industrial control protocol homologous attack detection method | P1n, P3b | H04L 63/1491 |
| CN111818077A | An industrial control hybrid honeypot system based on SDN technology | P3b | deception title |
| CN111931874B | Adjoint bait generation method and device based on deep learning and data … | P3b | deception title |
| CN111935185A | Method and system for constructing large-scale trapping scene based on cloud computing | P6 | deception title (P6) |
| CN112039717A | Honeypot-based real-time monitoring method and system | P3b | deception title |
| CN112054996B | Attack data acquisition method and device for honeypot system | P3b | deception title |
| CN112070161B | A network attack event classification method, device, terminal and storage … | P3b | H04L 63/1491 |
| CN112182564B | An industrial control honeypot interactive system based on time series … | P1n | deception title |
| CN112202738A | A machine learning-based industrial control situational awareness system and … | P1n, P3b | H04L 63/1491 |
| CN112217800A | Honeypot identification method, system, device and medium | P1n | deception title |
| CN112217800B | Honeypot identification method, system, device and medium | P3b | deception title |
| CN112235241B | Industrial control honeypot feature extraction method, system and medium based … | P1n, P3b | deception title |
| CN112261046A | Industrial control honeypot identification method based on machine learning | P3b | deception title |
| CN112367307B | Intrusion detection method and system based on container-level honey pot group | P1n, P3b | deception title |
| CN112383538B | Hybrid high-interaction industrial honeypot system and method | P1n, P3b | deception title |
| CN112398844A | Flow analysis implementation method based on internal and external network real … | P3b | H04L 63/1491 |
| CN112398876B | Network security early warning system of self-adaptation mimicry technique | P3b | H04L 63/1491 |
| CN112422537B | Behavior prediction method of network attack knowledge graph generated based on … | P3b | H04L 63/1491 |
| CN112464229B | Method and device for detecting spoofing attacks on an autopilot system | P3b | deception title |
| CN112491892A | Network attack inducing method, device, equipment and medium | P3b | deception title |
| CN112565186A | Distributed industrial control honey net flow acquisition system and method … | P3b | deception title |
| CN112578761A | Industrial control honey pot safety protection device and method | P1n | deception title |
| CN112637217A | Active defense method and device of cloud computing system based on bait … | P3b | deception title |
| CN112637244B | Threat detection method for common and industrial control protocols and ports | P3b | H04L 63/1491 |
| CN112650077A | PLC honeypot system based on industrial control service simulation, … | P1n | deception title |
| CN112671692A | Industrial control attack detection method based on intrusion decoy technology | P1n | deception title |
| CN112738002A | Technology for building industrial control honey net based on virtuality and … | P1n, P3b | deception title |
| CN112738120A | Honeypot-based data processing method, device and system and electronic … | P3b | deception title |
| CN112866259A | Industrial control honey pot node management method and device, computer … | P1n, P3b | deception title |
| CN113162948B | Modularized industrial control honey pot system | P1n, P3b | deception title |
| CN113285926A | Honey pot trapping method and device for power monitoring system and computer … | P3b | deception title |
| CN113328992B | Dynamic honey net system based on flow analysis | P1n, P3b | deception title |
| CN113535632B | Honeypot system, attack information capturing method and storage medium | P3b | deception title |
| CN113572785B | Honeypot defense method and device for nuclear power industrial control system | P3b | deception title |
| CN113676479A | Data defense method, defense device, terminal device and readable storage … | P3b | H04L 63/1491 |
| CN113765883A | Industrial control network honeypot identification method based on successive … | P1n | deception title |
| CN113765883B | Industrial control network honeypot identification method based on successive … | P3b | deception title |
| CN113810423A | Industrial control honey pot | P1n, P3b | deception title |
| CN114157454A | Attack countercheck method, device, computer equipment and storage medium | P3b | H04L 63/1491 |
| CN114157467A | Distributed switchable industrial honeynet trapping method | P3b | deception title |
| CN114221804A | A Honeypot Recognition Method Based on Feature Recognition and Interactive … | P3b | deception title |
| CN114257438A | Honeypot-based power monitoring system management method and device and … | P3b | deception title |
| CN114285599B | Industrial control honey pot construction method based on controller deep … | P1n, P6 | deception title |
| CN114401108B | Dynamic monitoring system and method for energy supply and demand states | P3b | H04L 63/1491 |
| CN114430344B | Attack organization identification method based on industrial control flow and … | P3b | H04L 63/1491 |
| CN114465784A | A honeypot identification method and device for an industrial control system | P1n, P3b | deception title |
| CN114531261B | Information processing methods, devices, systems, media and programs for … | P3b | H04L 63/1491 |
| CN114531294A | Network anomaly sensing method and device, terminal and storage medium | P3b | H04L 63/1491 |
| CN114584359B | Security trapping method, device and computer equipment | P3b | deception title |
| CN114598512A | Honeypot-based network security guarantee method and device and terminal … | P3b | deception title |
| CN114629691A | Data processing method, device and storage medium | P3b | H04L 63/1491 |
| CN114666128A | Honeypot threat information sharing method, device, equipment and readable storage medium | P6 | deception title (P6) |
| CN114679292B | Honeypot identification method, device, equipment and medium based on network … | P3b | deception title |
| CN114679334B | An industrial control safety detection system based on multi-mode artificial … | P1n, P3b | H04L 63/1491 |
| CN114884744A | Attack behavior analysis method and electronic equipment | P3b | H04L 63/1491 |
| CN114978595A | Method, device and computer equipment for constructing threat model | P3b | H04L 63/1491 |
| CN114978768B | Conpot-based networked control system honeypot | P3b | deception title |
| CN115021981A | Industrial control system intrusion detection and tracing method | P1n, P3b | H04L 63/1491 |
| CN115086059B | Deception scene description file generation method and device based on specific language of deception domain | P6 | deception title (P6) |
| CN115118510A | Hidden cheating attack method based on leaked resources and damaged resources | P3b | deception title |
| CN115134166B | Attack tracing method based on honey hole | P1b | deception title |
| CN115150124A | Fraud defense system | P3b | H04L 63/1491 |
| CN115150175B | Edge data drainage trapping method for independent network attack of power … | P3b | deception title |
| CN115174227A | Method for honey pot mirroring technology of main power station of power grid | P3b | deception title |
| CN115208679B | Attacker IP defending method and defending system based on honey array … | P1b | deception title |
| CN115225359A | Honeypot data tracing method and device, computer equipment and storage medium | P3b | deception title |
| CN115242466A | Intrusion active trapping system and method based on high-simulation virtual … | P3b | deception title |
| CN115242541A | A honeypot-based network attack response method, device and storage medium | P3b | deception title |
| CN115277142A | Safety protection method and device, storage medium and electronic equipment | P3b | H04L 63/1491 |
| CN115296909B | Method, device, medium and attack response method for obtaining target honeypot … | P3b | deception title |
| CN115334096A | Security decision method, device, equipment and storage medium of Internet of … | P3b | H04L 63/1491 |
| CN115378643B | Network attack defense method and system based on honey points | P1b | deception title |
| CN115378650A | Method for improving safety of industrial control system by adopting … | P3b | H04L 63/1491 |
| CN115378686B | A sandbox application method, device, and storage medium for industrial control … | P3b | H04L 63/1491 |
| CN115378729A | Service configuration generation method and device for simulated honeypots and … | P3b | deception title |
| CN115484326A | Method, system and storage medium for processing data | P3b | H04L 63/1491 |
| CN115499198B | Honeypot management method, device, honeypot defense system and storage medium | P3b | deception title |
| CN115549943B | Four-honey-based integrated network attack detection method | P1b | deception title |
| CN115549950B | A security protection system for industrial control equipment based on … | P3b | H04L 63/1491 |
| CN115622759A | A distributed honeypot management system in a heterogeneous environment and its … | P3b | deception title |
| CN115622760A | A definable industrial control honeypot system and its operation method | P1n, P3b | deception title |
| CN116055159A | A security defense method, device and computer equipment | P3b | H04L 63/1491 |
| CN116094795A | Multi-dimensional attribute dynamic industrial control low-interaction honeypot … | P1n | deception title |
| CN116132197A | Network homologous attack analysis method and system based on function codes | P3b | H04L 63/1491 |
| CN116192530B | Unknown threat self-adaptive detection method based on deceptive defense | P1n, P3b | deception title |
| CN116318828B | A Method for Prevention and Control of Viruses in the Industrial Internet | P3b | H04L 63/1491 |
| CN116318936A | A Networked Industrial Control Asset Identification Method Based on Improved … | P3b | H04L 63/1491 |
| CN116405258A | Smart grid honeypot design method and system based on reinforcement learning | P3b | deception title |
| CN116471085B | Methods, devices, and storage media for generating web parasitic honeypots and … | P1b | deception title |
| CN116527308A | Electric power industry Internet of things security attack and defense … | P3b | H04L 63/1491 |
| CN116527379A | Network attack prevention method, system and device based on honey point … | P1b | deception title |
| CN116614256A | Method for generating remote measurement mimicry data of industrial control … | P3b | H04L 63/1491 |
| CN116614256B | A method for generating industrial control honeypot telemetry mimic data using … | P1n | deception title |
| CN116668061A | Network security active defense method for power monitoring system based on … | P3b | H04L 63/1491 |
| CN116668173A | Method for non-inductive switching of user service based on honey point | P1b | deception title |
| CN116723030A | Honey array diagram changing method based on situation awareness | P1b | deception title |
| CN116760558A | A secure honeypot system and its implementation method | P3b | deception title |
| CN116781412A | An automatic defense method based on abnormal behavior | P3b | H04L 63/1491 |
| CN116866075A | A timely adaptive honeypot network construction method and device | P3b | deception title |
| CN116866076A | Network honeypot identification method, device, equipment and storage medium | P3b | deception title |
| CN116886383A | A honeypot interface method, system, medium and equipment based on power IED … | P1n | deception title |
| CN116886383B | Honeypot interface method, system, medium and equipment based on electric IED … | P3b | deception title |
| CN117040845A | A honeypot network configuration method and system based on elastic scaling | P1b | deception title |
| CN117040890A | Honey array defense method and system based on feedback adjustment deception … | P1b | deception title |
| CN117061147A | An industrial control honeypot and its application method | P3b | deception title |
| CN117061199B | IP reputation calculation method, device and medium integrating honey spot … | P1b | deception title |
| CN117061210A | … for constructing a deception defense honey array based on dynamic honey points | P1b | deception title |
| CN117097549A | Safety guarantee system and method for honeypot system | P1n, P3b | deception title |
| CN117111489B | A simulation method, storage medium and electronic device for PLC equipment | P3b | H04L 63/1491 |
| CN117118708B | Threat trapping process evaluation method and system for hybrid honeypot | P3b | deception title |
| CN117118981A | Industrial cloud platform communication method based on CODESYS programming … | P3b | H04L 63/1491 |
| CN117134973A | A dynamic deception method and system based on honey array linkage | P1b | deception title |
| CN117134986A | External network honey point generation method, system and device based on … | P1b | deception title |
| CN117155683A | System and method for generating internal network honey points based on ChatGPT | P1b | deception title |
| CN117220900A | Method and system for automatically detecting honeypot system | P1n | deception title |
| CN117220918A | A dynamic deception defense system for network attacks based on honey points | P1b | deception title |
| CN117278299A | … -interaction honeypot anti-identification method and system based on industrial … | P3b | deception title |
| CN117278338A | A network intrusion detection method and system based on deep learning … | P3b | H04L 63/1491 |
| CN117278423B | Model construction method, test platform, computer device and storage medium | P3b | H04L 63/1491 |
| CN117354037A | Virus invasion monitoring system for industrial control network and monitoring … | P1n, P3b | H04L 63/1491 |
| CN117375914A | Monitoring data processing system of industrial Internet of things | P3b | H04L 63/1491 |
| CN117375997A | … a security knowledge plane for malicious traffic attacks based on honey points | P1b | deception title |
| CN117527331A | Highly interactive hybrid honeynet architecture design based on malware … | P1n, P3b | deception title |
| CN117596067A | A DDoS defense verification method based on controllable honeypots | P3b | deception title |
| CN117610026B | Honey point vulnerability generation method based on large language model | P1b, P6 | deception title |
| CN117614717A | A full-process processing system and method based on network security alarm … | P3b | H04L 63/1491 |
| CN117614742A | A malicious traffic detection method with enhanced honey point awareness | P1b | deception title |
| CN117650923A | An information security active defense method based on K-means | P3b | H04L 63/1491 |
| CN117896155A | Method, device, electronic device and storage medium for countering phishing … | P3b | H04L 63/1491 |
| CN117938473A | Spoofing defense method and device based on reinforcement learning high-attack and defense interaction in multi-honeypot scene | P6 | deception title (P6) |
| CN117978474A | Abnormal traffic processing method, device, computer equipment and storage … | P3b | H04L 63/1491 |
| CN117978542B | Digital stand-by defense system design method and device for advanced … | P3b | H04L 63/1491 |
| CN117999554A | Honeypot entity and operation method thereof | P1b | deception title |
| CN118018268A | Industrial control honeypot simulation interaction method and system based on … | P1n, P3b | deception title |
| CN118041581A | Network security situation prediction method and system based on artificial … | P3b | H04L 63/1491 |
| CN118075035B | Network camera honey point generation method and device based on active defense | P1b | deception title |
| CN118174911A | Industrial control honeypot detection method based on fuzzy testing | P1n, P3b | deception title |
| CN118250087B | A method and system for automatically generating email account honeypots for … | P1b | deception title |
| CN118316675A | A method, device, medium and equipment for trapping honeypot of IED equipment … | P3b | deception title |
| CN118316745A | A honey spot generation method and generation system | P1b | deception title |
| CN118337540B | Internet of things-based network intrusion attack recognition system and method | P3b | H04L 63/1491 |
| CN118381627A | LLM driven industrial network intrusion detection method and response system | P3b | H04L 63/1491 |
| CN118449748A | Modbus protocol-based data security transmission method, device and medium | P3b | H04L 63/1491 |
| CN118523931A | Industrial controller honeypot identification method and device based on device … | P1n, P3b | deception title |
| CN118590274A | A method for detecting abnormal nodes in provenance graph based on honeypoint … | P1b | deception title |
| CN118611949A | Malicious Internet Protocol address analysis method, device, equipment and … | P3b | H04L 63/1491 |
| CN118631496A | A honeypot-based security verification method and system in BAS | P3b | deception title |
| CN118631579A | A honey array graph generation method and generation system based on obfuscated … | P1b | deception title |
| CN118740399A | A method for storing and analyzing network security threat intelligence | P1n, P3b | H04L 63/1491 |
| CN118740447A | An internal attack perception method based on PLC honeypot | P1b, P1n, P3b | deception title |
| CN118748624A | A protective controller based on intelligent algorithm | P3b | H04L 63/1491 |
| CN118764274A | A virtualized honey array generation method and system | P1b | deception title |
| CN118784341A | Covert false data injection method for remote state estimation of cyber- … | P3b | H04L 63/1491 |
| CN118802341A | Honeypot-based APT attack capture and detection method, device, and medium | P3b | deception title |
| CN118802353A | A method for constructing a honey array model based on dynamic perception … | P1b, P6 | deception title |
| CN118869346A | An active defense method based on pre-placed honey court content trap | P1b | deception title |
| CN118939909A | Iterative learning robust safety predictive control method based on deception … | P3b | deception title |
| CN118940756A | A honeyspot-based cue injection detection method for large language models | P1b | deception title |
| CN119011208B | Executor scheduling method, device, electronic device and storage medium | P3b | H04L 63/1491 |
| CN119051889B | A method for identifying industrial control honeypots based on multidimensional … | P1n, P3b | deception title |
| CN119071043A | An active defense method for IoT devices | P1b, P3b | H04L 63/1491 |
| CN119135401A | Industrial control system threat trapping method based on machine learning … | P1b, P3b | deception title |
| CN119172117A | A honey spot generation method for Web API | P1b, P6 | deception title |
| CN119210765A | … constructing consistency evaluation indicators of QKD protocol for substations | P3b | H04L 63/1491 |
| CN119210849A | A cloud service honeypot generation method and system for active defense | P1b | deception title |
| CN119232763A | Industrial control ring network monitoring system and monitoring method thereof | P3b | H04L 63/1491 |
| CN119254495A | Network stream watermark detection method and system based on abstract feature … | P3b | H04L 63/1491 |
| CN119402216A | Honey spot anti-aging method and system based on digital twin | P1b | deception title |
| CN119402218B | Method and system for generating near-body honey point document based on large … | P1b | deception title |
| CN119449457A | IoT defense method based on reinforcement learning with graph attention … | P3b, P6 | H04L 63/1491 |
| CN119449467A | A Modbus-based federated learning threat detection method and system | P3b | H04L 63/1491 |
| CN119561746A | … attack trapping method and system based on full-scene simulation of industrial … | P1n, P3b | deception title |
| CN119628903A | A tracing deterrence method and system based on floating code honey hole | P3b | deception title |
| CN119670810A | Node feature construction method based on honeypoint intelligence and … | P1b | deception title |
| CN119675929B | A fine-grained micro-element node device management method and system | P3b, P6 | H04L 63/1491 |
| CN119692438A | Node feature construction method based on nonlinear interaction of honeypoint … | P1b | deception title |
| CN119696932A | Honeypot network simulation method and system based on attack trapping system | P1b | deception title |
| CN119766493A | Threat information detection method, device, equipment and medium based on honeypot trapping | P6 | deception title (P6) |
| CN119766566A | A method and system for path honeypot based on browser fingerprint recognition | P1b | deception title |
| CN119854001A | Honey pot technology-based spoofing defending method, device and medium | P6 | deception title (P6) |
| CN119996015A | A four-honeypot threat detection method for enterprise intranet | P1b | deception title |
| CN119996017B | Method for realizing trapping system based on intelligent large model | P6 | deception title (P6) |
| CN119996025B | A high-interaction honey spot design method and system based on GPT | P1b | deception title |
| CN120110774B | … detection method, system, storage medium and terminal equipment for industrial … | P3b | H04L 63/1491 |
| CN120110795A | Dynamic deception defense system and method based on service tripwire … | P1b | deception title |
| CN120185900A | An industrial control honeypot concealment method for anti-fuzz testing | P1n, P3b | deception title |
| CN120200856B | Cloud original honey array-oriented map hopping method and system | P1b | deception title |
| CN120358100A | Industrial control honeypot defense system and method based on mirror image … | P1n | deception title |
| CN120415816A | Network security space mapping method, system and equipment based on multi- … | P3b | H04L 63/1491 |
| CN120415854A | Network threat response method, system, device and medium based on … | P3b | H04L 63/1491 |
| CN120433958A | A distributed threat intelligent honeynet trapping method | P6 | deception title (P6) |
| CN120546980A | A distributed diversion pulse control method for complex networks based on dual … | P3b | H04L 63/1491 |
| CN120602236B | Electric power monitored control system based on artificial intelligence | P3b | H04L 63/1491 |
| CN120639372A | A dynamic honey spot evolution method and system based on behavioral … | P1b | deception title |
| CN120639470A | Dynamic honeypot collaborative intelligent threat trapping system and method … | P1b | deception title |
| CN120639490A | An edge-side attack aggregation analysis method based on traffic self-learning | P3b | H04L 63/1491 |
| CN120658498A | Network abnormal behavior detection and dynamic defense method and system | P3b | H04L 63/1491 |
| CN120675782A | A correlation analysis system based on power network security data | P1n, P3b | H04L 63/1491 |
| CN120693840A | Target-side link Denial of Service (DoS) detection via inter-UE coordination … | P3b | H04L 63/1491 |
| CN120750578A | Honeypot interaction response generation method based on large language model | P3b | deception title |
| CN120750810A | Network flow generation method based on large model fine tuning | P3b | H04L 63/1491 |
| CN120768630A | Situational awareness and threat warning methods for malicious programs in the … | P3b | H04L 63/1491 |
| CN120768699A | Honeypot-based network attack protection method, device, equipment and medium | P6 | deception title (P6) |
| CN120785544A | Batch mining honeypot fingerprint and recognition method and system | P1b, P3b | deception title |
| CN120856453A | An active defense system for cloud environments based on dynamic honeypots | P1b, P6 | deception title |
| CN120856467A | A method and system for generating dynamic deceptive domain name honeypots for … | P1b | deception title |
| CN120880810A | GAN-based electric power protocol honeypot trapping and anomaly identification … | P3b | deception title |
| CN120979731A | A Mimicry Defense Architecture for Power Monitoring Systems Based on Dynamic … | P3b | H04L 63/1491 |
| CN121000455A | A method and system for network security situation awareness and early warning … | P1n, P3b | H04L 63/1491 |
| CN121000457A | Network security systems based on deep learning and SDN architecture | P3b | H04L 63/1491 |
| CN121000535A | A method, apparatus, medium, and electronic device for generating honey array … | P1b | deception title |
| CN121193464A | A deception-inducing method and related equipment based on pre-honey court | P1b | deception title |
| CN121309053A | Honeypot countermeasures, devices, computer equipment and storage media | P1b | deception title |
| CN121309235A | A proactive defense method based on software-defined deception defense and … | P1b | deception title |
| CN121356905A | A Highly Interactive Industrial Honeypot System Based on Hyperconverged … | P1n | deception title |
| CN121462309A | Attack detection method and system based on semantic analysis of power protocol | P3b | H04L 63/1491 |
| CN121508887A | An attack trapping method integrating mimicry simulation and traffic … | P3b | deception title |
| CN121508896A | A Honeypot Response Data Generation Method and Honeypot Defense System Based on … | P3b | deception title |
| CN121509101A | Dynamic defense methods and devices for extending honeypot mapping points | P3b | deception title |
| CN121530748A | A smart threat perception method and system integrating honeynet and honeypot | P1b, P6 | deception title |
| CN121547235A | A method and system for implementing industrial honeypot networks based on … | P1n, P3b | deception title |
| CN121547289B | Distributed network spoofing defending method and system based on honey array | P3b | deception title |
| CN121547299A | An Adaptive Network Deception System and Method Based on Dynamic Honeypoints | P1b | deception title |
| CN121567485A | Attack chain identification method and device for honey array attack trapping … | P1b | deception title |
| CN121567485B | Attack chain identification method and device for honey array attack trapping … | P3b | deception title |
| CN121585397A | Countermeasures against cyberattacks: methods, systems, devices, computer … | P3b | H04L 63/1491 |
| CN121585474A | A causal-driven method for reconstructing honeycomb attack chains and linking … | P1b, P3b | deception title |
| CN121644246B | A TTPs Scenario Analysis Method for Software-Defined Deception Defense Systems | P1b | deception title |
| CN121658912B | Honey pot-honey point collaborative analysis system and method | P1b | deception title |
| CN121664497A | Honey matrix transformation method and device based on large language model | P1b | deception title |
| CN121690756A | Industrial control network high-interaction honeynet method based on finite … | P1n | deception title |
| CN121727840A | Industrial network protection method, electronic equipment, machine-readable … | P3b | H04L 63/1491 |
| CN121841799A | Industrial control hacker organization identification method based on Gaussian … | P1n, P3b | H04L 63/1491 |
| CN121864365A | Invariant-based PLC ( programmable logic controller ) honey point construction … | P1b, P3b | deception title |
| CN121887548A | Grading honey point trapping method and device based on self-adaptive UEBA … | P1b | deception title |
| CN121923884A | Digital power grid open source software supply chain safety control method | P3b | H04L 63/1491 |
| CN121923938A | Dynamic trapping defense method and system based on software defined spoofing … | P1b | deception title |
| CN121967045A | Domain environment ADCS deception trapping method based on attack and defense … | P1b | deception title |
| CN121967096A | Traffic trip line generation method and system based on honey points for … | P1b | deception title |
| CN122027363A | Honey array driven network security situation awareness method and system | P6 | deception title (P6) |
| CN122120014A | Industrial control honey pot trapping method and system | P1n, P3b | deception title |
| CN122160182A | General network service simulation honey point construction method based on … | P1b | deception title |
| CN122204428A | A method and system for generating honeypots dynamically and adaptively across … | P3b | deception title |
| CN122316652A | Industrial control honeypot creation, monitoring, and analysis methods and … | P1n | deception title |
| CN122339785A | A privacy-preserving, resilient average consensus method and system for multi- … | P3b | H04L 63/1491 |
| CN122339831A | Method and apparatus for deploying and updating network defenses based on … | P1b | the application publication of CN 122339831 B, whose page was read |
| CN122339846B | A method and system for active defense of power cyber-physical systems | P3b | the granted document of CN 122339846 A, the proposed T2 (15.1); its page was read with the A's, so the tier of the pair is the A's |
| CN122372331A | A Honeypot Intelligent Modeling and Dynamic Response Method Based on World … | P3b | deception title |
| CN122386884B | … code generation method for PLC (programmable logic controller) honey points | P1b | deception title |
| CN122394973A | Layered self-triggering fixed-pinning aperiodic intermittent safety synchronous … | P3b | H04L 63/1491 |
| CN122394973B | A layered, self-triggered, fixed-restraint, non-periodic intermittent security … | P3b | H04L 63/1491 |
| CN122419819A | Raspberry pie-based VxWorks real type honey pot and design method thereof | P1b, P1n, P3b | deception title |
| CN122419875A | Network detection organization identification and attribution method based on … | P1n, P3b | H04L 63/1491 |
| CN122437728A | Digital twinning-based measuring box monitoring data tamper-proof … | P3b | H04L 63/1491 |
| CN122513203A | A method for vulnerability simulation and dynamic attack trapping powered by a … | P1b | deception title |
| CN122554133A | A Two-Path Attack Intent Inference Method Based on Software-Defined Deception … | P1b | deception title |
| CN122601305A | A Methodology for Building a Training-Application Fusion Intelligent Honeypot … | P1b | deception title |
| CN209717667U | A portable toolbox for industrial control network honeypot system | P1n | deception title |
| CN219395219U | Portable industrial control honey net probe device | P1n | deception title |
| CZ36587U1 | System for detection and analysis of cyber attacks in data networks of … | P3b | H04L 63/1491 |
| DE102014012257B4 | UPDATE MANAGEMENT | P3b | H04L 63/1491 |
| DE102018006755A1 | Danial of Service Mitigation with Two-Tier Hash | P3b | H04L 63/1491 |
| DE102023209243A1 | Method for creating a honeypot | P3b, P6 | deception title |
| DE102023209244A1 | Method for creating a honeypot | P3b | deception title |
| DE102023209246A1 | Method for creating a honeypot | P3b | deception title |
| DE102023209599A1 | Method for creating a honeypot | P3b, P6 | deception title |
| DE102023209600A1 | Method for creating a honeypot | P3b | deception title |
| DE102023209601A1 | Procedure for configuring a honeypot | P3b, P6 | deception title |
| EP1212682A1 | System and method for quickly authenticating messages using sequence numbers | P3b | H04L 63/1491 |
| EP2541861A1 | Server security systems and related aspects | P3b | H04L 63/1491 |
| EP2721801B1 | Security measures for the smart grid | P3b | H04L 63/1491 |
| EP2882159B1 | Profiling cyber threats detected in a target environment and automatically … | P3b | H04L 63/1491 |
| EP2950502A1 | Apparatus and method for preventing leakage of vehicle information | P3b | H04L 63/1491 |
| EP3164995B1 | Secure enclave-rendered contents | P3b | H04L 63/1491 |
| EP3375159B1 | Dynamic honeypot system | P3b | deception title |
| EP3486824B1 | Determine malware using firmware | P3b | H04L 63/1491 |
| EP4024252A1 | A system and method for identifying exploited CVEs using honeypots | P6 | deception title (P6) |
| EP4060938B1 | Method for improving security in an electronic communication network | P3b | H04L 63/1491 |
| EP4184868B1 | Cloud-based deception technology utilizing zero trust to identify threat … | P3b | deception title |
| EP4586548A1 | Method for configuring a honeypot | P3b, P6 | deception title |
| EP4586549A1 | Method for producing a honeypot | P3b | deception title |
| EP4594909A1 | System and method for detecting and/or blocking malware attacks using decoys | P3b | deception title |
| GB2544803A | Context-aware threat intelligence | P3b | H04L 63/1491 |
| GB2606591A | Cyber security deception system | P3b | deception title |
| JP2012164309A | Method, system and device for detecting attempted intrusion into network | P3b | H04L 63/1491 |
| JP2018019218A | Electronic control unit | P3b | H04L 63/1491 |
| JP6634009B2 | Honeyport enabled network security | P3b | deception title |
| JP7667149B2 | Ransomware Prevention | P3b | H04L 63/1491 |
| JP7898584B2 | Honeypot for protecting the security of infrastructure as a service | P3b | deception title |
| KR20230064450A | Security management method and system for blended environment | P3b | H04L 63/1491 |
| KR20250172039A | System for IoT terminal infection malicious file collection and method for … | P3b | H04L 63/1491 |
| RU2634211C1 | Method and system of protocols analysis of harmful programs interaction with … | P3b | H04L 63/1491 |
| RU2667052C2 | Detection of harmful software with cross-review | P3b | H04L 63/1491 |
| TW202109328A | Industrial control trapping system and method with high interaction combination … | P1n | deception title |
| US10033762B2 | Threat engagement and deception escalation | P3b | deception title |
| US10193924B2 | Network intrusion diversion using a software defined network | P2a | vendor |
| US10200406B1 | Configuration of application randomization mechanism | P3b | H04L 63/1491 |
| US10230745B2 | Using high-interaction networks for targeted threat intelligence | P2a | vendor |
| US10250636B2 | Detecting man-in-the-middle attacks | P2c, P2h | vendor |
| US10270789B2 | Multiphase threat analysis and correlation engine | P3b | H04L 63/1491 |
| US10277629B1 | Systems and methods for creating a deception computing system | P6 | deception title (P6) |
| US10333976B1 | Open source intelligence deceptions | P2d, P2i | deception title |
| US10333977B1 | Deceiving an attacker who is harvesting credentials | P2d, P2i | deception title |
| US10348763B2 | Responsive deception mechanisms | P2a | deception title |
| US10362057B1 | Enterprise DNS analysis | P2a, P3b | H04L 63/1491 |
| US10375110B2 | Luring attackers towards deception servers | P2c, P2h, P3b | deception title |
| US10375111B2 | Anonymous containers | P3b | H04L 63/1491 |
| US10382484B2 | Detecting attackers who target containerized clusters | P2d, P2i | vendor |
| US10412116B1 | Mechanism for concealing application and operation system identity | P3b | H04L 63/1491 |
| US10419479B2 | Testing environment cyber vaccine | P2a | vendor |
| US10440055B2 | Apparatus and method for implementing network deception | P3b | deception title |
| US10447733B2 | Deception network system | P3b | deception title |
| US10476891B2 | Monitoring access of network darkspace | P2c, P2h | vendor |
| US10505955B2 | Using virtual sensors to accommodate industrial asset control systems during … | P3b | H04L 63/1491 |
| US10509905B2 | Ransomware mitigation system | P2c, P2h | vendor |
| US10567431B2 | Emulating shellcode attacks | P2c | vendor |
| US10599842B2 | Deceiving attackers in endpoint systems | P2c, P2h | deception title |
| US10609074B2 | Implementing decoys in network endpoints | P2c, P2h | deception title |
| US10623442B2 | Multi-factor deception management and detection for malicious actions in a … | P2i | deception title |
| US10713636B2 | Defense against credit card theft from point-of-sale terminals | P2d, P2i | vendor |
| US10972503B1 | Deception mechanisms in containerized environments | P2a, P3b, P6 | deception title |
| US10986121B2 | Multivariate network structure anomaly detector | P3b | H04L 63/1491 |
| US11038658B2 | Deceiving attackers in endpoint systems | P2c, P2h | deception title |
| US11038919B1 | Multiple personality deception systems | P6 | deception title (P6) |
| US11038920B1 | Behavior management of deception system fleets | P6 | deception title (P6) |
| US11102245B2 | Deception using screen capture | P3b | deception title |
| US11122079B1 | Obfuscation for high-performance computing systems | P3b | deception title |
| US11202254B1 | Methods, systems, and devices for simulating voice and data traffic in a mobile … | P3b | H04L 63/1491 |
| US11212315B2 | Tunneling for network deceptions | P2a, P4 | same family and title as US 10,616,276 B2, which was read |
| US11303667B2 | Organization attack surface management | P2d, P2i | vendor |
| US11303675B1 | Containing compromised credentials using deception systems | P6 | deception title (P6) |
| US11431684B2 | Data response method, terminal device, and server | P3b | H04L 63/1491 |
| US11431751B2 | Live forensic browsing of URLs | P3b | H04L 63/1491 |
| US11470061B2 | Parallel scheduling of encryption engines and decryption engines to prevent … | P3b | H04L 63/1491 |
| US11531749B2 | Controlling access to external networks by an air-gapped endpoint | P3b | H04L 63/1491 |
| US11627160B2 | Intelligent-interaction honeypot for IoT devices | P3b | deception title |
| US11695800B2 | Deceiving attackers accessing network data | P2h | deception title |
| US11843634B2 | High-fidelity model-driven deception platform for cyber-physical systems | P3b | deception title |
| US11934948B1 | Adaptive deception system | P3b | deception title |
| US11962611B2 | Cyber security system and method using intelligent agents | P3b | H04L 63/1491 |
| US12028376B2 | Systems and methods for creation, management, and storage of honeyrecords | P3b | deception title |
| US12107889B2 | Cloud-based deception technology utilizing zero trust to identify threat … | P3b | deception title |
| US12321456B2 | Automatic generation of malware detection traps | P3b | deception title |
| US12341802B2 | Method and system for generating stateful attacks | P3b | H04L 63/1491 |
| US12375527B2 | … to obtain enhanced information regarding an attack chain involving a decoy file | P2f, P3b | deception title |
| US12407725B1 | Unified threat management and mitigation | P3b | H04L 63/1491 |
| US12425450B2 | Method for securing digital substations and system thereof | P3b | H04L 63/1491 |
| US12464020B2 | AI-generated virtual file honeypots for computing systems behavior-based … | P3b | deception title |
| US12477004B2 | Dynamic calculation of security risk score of network security services based … | P3b | H04L 63/1491 |
| US12489798B2 | Managing artificial intelligence models to identify goals of malicious … | P3b | H04L 63/1491 |
| US12500931B2 | Risk mitigation effectiveness score of network security services | P3b | H04L 63/1491 |
| US12526314B2 | Cyber security deception system | P3b | deception title |
| US12598212B2 | Cybersecurity risk analysis and modeling of risk data on an interactive display | P3b | H04L 63/1491 |
| US12613961B2 | Identifying attacks to active resources by trusted devices with fake … | P2f | deception title |
| US12641121B2 | Electronic decoy apparatus and associated methods | P3b | deception title |
| US12647458B2 | Breach prediction via generative artificial intelligence (AI) with multi- … | P3b | H04L 63/1491 |
| US12676888B2 | Virtual file honey pots for computing systems protection against ransomware … | P1n | deception title |
| US12688326B2 | System and methods for click-jacking and content redressing protection | P3b | H04L 63/1491 |
| US12711232B2 | Ransomware prevention | P3b | H04L 63/1491 |
| US12712854B2 | … tunneling infrastructure for delivering high-interaction OS-based deception as … | P2f, P3b | deception title |
| US20090328216A1 | Personalized honeypot for detecting information leaks and security breaches | P6 | deception title (P6) |
| US20160212154A1 | Method and system for handling malware | P3b | H04L 63/1491 |
| US20160359905A1 | Automatically generating network resource groups and assigning customized decoy policies thereto | P6 | deception title (P6) |
| US20170093910A1 | Dynamic security mechanisms | P2a, P3b | H04L 63/1491 |
| US20170134422A1 | Deception Techniques Using Policy | P3b | deception title |
| US20170149825A1 | Modification of a Server to Mimic a Deception Mechanism | P2a, P3b | deception title |
| US20170214708A1 | Detecting security threats by combining deception mechanisms and data science | P2a, P3b | deception title |
| US20170264639A1 | Active deception system | P2a, P3b | deception title |
| US20170289191A1 | Infiltration Detection and Network Rerouting | P2a, P3b | H04L 63/1491 |
| US20170374032A1 | Autonomic Protection of Critical Network Applications Using Deception … | P3b | deception title |
| US20180027015A1 | System and method for identifying cyber-attacks | P3b | H04L 63/1491 |
| US20180075233A1 | Systems and methods for agent-based detection of hacking attempts | P3b | H04L 63/1491 |
| US20180124064A1 | Separated application security management | P3b | H04L 63/1491 |
| US20180375897A1 | Automated network device cloner and decoy generator | P3b | deception title |
| US20190260788A1 | Transient Transaction Server | P3b | H04L 63/1491 |
| US20200134235A1 | Physical and logical attack resilient polymorphic hardware | P3b | H04L 63/1491 |
| US20200213355A1 | Security Network Interface Controller (SNIC) Preprocessor with Cyber Data … | P3b | H04L 63/1491 |
| US20200252429A1 | Deceiving Attackers Accessing Network Data | P2c | deception title |
| US20210168173A1 | Detection and remediation of malicious network traffic using tarpitting | P3b | H04L 63/1491 |
| US20220030009A1 | Computer security based on artificial intelligence | P3b | H04L 63/1491 |
| US20220166799A1 | Leveraging 5g network slicing capability to increase network security | P3b | H04L 63/1491 |
| US20220182412A1 | Systems and methods of evaluating probe attributes for securing a network | P3b | H04L 63/1491 |
| US20230060323A1 | How to confuse adversarial environment mapping tools | P2d | read |
| US20230065321A1 | Implementing decoys in a network environment | P2c | deception title |
| US20230171292A1 | Holistic external network cybersecurity evaluation and scoring | P3b | H04L 63/1491 |
| US20230291766A1 | System, Device, and Method of Protecting Users and Online Accounts against … | P3b | H04L 63/1491 |
| US20230319087A1 | Systems, methods, and devices for preventing credential passing attacks | P2c | vendor |
| US20230370439A1 | Network action classification and analysis using widely distributed honeypot … | P3b | deception title |
| US20240098100A1 | Automated sandbox generator for a cyber-attack exercise on a mimic network in a … | P3b | H04L 63/1491 |
| US20240236125A1 | Systems and methods for dynamic network baiting | P2f | deception title |
| US20240267409A1 | Cyber clone of a computing entity | P3b | H04L 63/1491 |
| US20240364686A1 | Systems and methods for securing devices in a computing environment | P3b | H04L 63/1491 |
| US20240394364A1 | Data processing system and method for mitigating a malware attack | P3b | H04L 63/1491 |
| US20250088536A1 | Deceptive Resistance to Adversary Cyber Operations (DRACO) | P3b | deception title |
| US20250088537A1 | Systems and methods for service response analysis via out-of-band signaling | P3b | H04L 63/1491 |
| US20250106251A1 | Virtual file honey pots for computing systems protection against ransomware … | P3b | deception title |
| US20250112942A1 | Service level verification in distributed system and enforcement | P3b | H04L 63/1491 |
| US20250175498A1 | Ransomware protection in advanced injection-based attacks | P3b | H04L 63/1491 |
| US20250254197A1 | Cybersecurity Risk Analysis via Reverse External Attack Surface Discovery | P3b | H04L 63/1491 |
| US20250260721A1 | Deceiving attackers accessing active directory data | P2c, P2h | deception title |
| US20250272401A1 | Automatic generation of malware detection traps | P2g | deception title |
| US20250284803A1 | Detecting ransomware activity in data storage systems | P3b | H04L 63/1491 |
| US20250301017A1 | Machine learning based cyber threat intelligence system and related methods | P3b | H04L 63/1491 |
| US20250358316A1 | Network mapping behavior anomaly detection method and system based on machine … | P3b | H04L 63/1491 |
| US20260122041A1 | … tunneling infrastructure for delivering high-interaction os-based deception as … | P2f, P3b | deception title |
| US20260149738A1 | Method and system for unveiling dns monitoring via stimulated network emissions | P3b | H04L 63/1491 |
| US7461257B2 | System for detecting spoofed hyperlinks | P2i | deception title |
| US8844044B2 | Systems and methods for implementing and scoring computer network defense … | P3b | H04L 63/1491 |
| US9356950B2 | Evaluating URLS for malicious content | P2c, P2h | vendor |
| US9356958B2 | Apparatus and method for protecting communication pattern of network traffic | P3b | H04L 63/1491 |
| US9392001B2 | Multilayered deception for intrusion detection and prevention | P3b | deception title |
| US9407602B2 | Methods and apparatus for redirecting attacks on a network | P2c, P2h | vendor |
| US9516059B1 | Using mock tokens to protect against malicious activity | P3b | deception title |
| US9680867B2 | Network stimulation engine | P2a | vendor |
| US9729567B2 | Network infrastructure obfuscation | P2a | deception title |
| US9756075B1 | Dynamic hiding of deception mechanism | P2a, P3b | deception title |
| US9773109B2 | Alternate files returned for suspicious processes in a compromised computer … | P2a | vendor |
| US9836512B1 | Systems and methods for identifying similar hosts | P2a, P3b | H04L 63/1491 |
| US9912695B1 | Techniques for using a honeypot to protect a server | P3b | deception title |
| US9942270B2 | Database deception in directory services | P2c, P2h | deception title |
| US9961099B2 | Systems and methods for detecting and tracking adversary trajectory | P2a, P3b | H04L 63/1491 |
| US9979750B2 | Tunneling for network deceptions | P3b | deception title |
| US9985988B2 | Deception to detect network scans | P2a, P3b | deception title |
| WO2002077777A1 | Method, a system and a network terminal for protected entry of data | P3b | H04L 63/1491 |
| WO2002086724A1 | System and method for analyzing logfiles | P3b | H04L 63/1491 |
| WO2016081561A1 | System and method for directing malicious activity to a monitoring system | P2c | vendor |
| WO2017213998A1 | In-band asymmetric protocol simulator | P3b | H04L 63/1491 |
| WO2020155045A1 | Method and device for establishing communication model of network device | P3b | H04L 63/1491 |
| WO2022066181A1 | Security deception using a unidirectional communication device | P3b | deception title |
| WO2022091207A1 | Risk analysis apparatus, analysis target element determination device, method, … | P3b | H04L 63/1491 |
| WO2022164504A1 | Deception system | P3b | deception title |
| WO2024226393A1 | Emulated network environment generation methods and systems for cyberwarfare … | P3b | H04L 63/1491 |
| WO2024251350A1 | Unauthorized database access detection using honeypots | P3b | deception title |
| WO2024260658A1 | Cyber defence deception effectiveness metrics | P3b | deception title |
| WO2025017376A1 | Zero trust anomaly traffic management for a network | P3b | H04L 63/1491 |
| WO2026062320A1 | A method, a system and a computer program for monitoring security threats in an … | P3b | H04L 63/1491 |
| WO2026076480A1 | Computer-implemented method to divert hacker attacks on a computer network | P3b | H04L 63/1491 |

## 17. Patents excluded (X) on a title: 646

Not opened, except the 35 excluded after reading, which are in §15.3 to §15.7. One of the 646, the design registration CN 304151907 S (17.1), is among the four exclusions that §9 asks the user to confirm; the other three were read (14.6). *D37: all four confirmed, 16 November 2026.*

### 17.1 Chinese design registrations: 356

Product appearances, not methods. 355 come from the "honeypoint" run, of which 353 name honey in the title (packaging, jars, labels) and 2 are other products (CN304552591S "packing box", CN307080808S "Bottle (Confession)"); the other, CN 304151907 S, comes from P1n and awaits the user's confirmation (14.6).

CN301278935S, CN301278936S, CN301389241S, CN301437308S, CN301478758S, CN301481742S, CN301482835S, CN301484356S, CN301484363S, CN301484364S, CN301484365S, CN301484373S, CN301484385S, CN301484387S, CN301498057S, CN301498345S, CN301543922S, CN301551327S, CN301646027S, CN301646167S, CN301726941S, CN301813596S, CN301858682S, CN301858686S, CN301858698S, CN301858699S, CN301858704S, CN301858706S, CN301859080S, CN301934979S, CN301981243S, CN302028688S, CN302044400S, CN302044401S, CN302052628S, CN302079755S, CN302090922S, CN302107010S, CN302107319S, CN302129626S, CN302227645S, CN302240576S, CN302240637S, CN302240882S, CN302265085S, CN302276443S, CN302306801S, CN302325961S, CN302338886S, CN302339135S, CN302339324S, CN302359077S, CN302359079S, CN302359080S, CN302359082S, CN302421826S, CN302452533S, CN302456927S, CN302465417S, CN302465686S, CN302474361S, CN302474501S, CN302487968S, CN302488130S, CN302488202S, CN302488351S, CN302503011S, CN302525149S, CN302525152S, CN302581272S, CN302618572S, CN302648708S, CN302669913S, CN302679876S, CN302724884S, CN302725003S, CN302734444S, CN302738690S, CN302758785S, CN302766370S, CN302787790S, CN302795032S, CN302795887S, CN302795888S, CN302795889S, CN302795890S, CN302795983S, CN302807296S, CN302807297S, CN302807298S, CN302835017S, CN302855086S, CN302871262S, CN302872006S, CN302952681S, CN302952839S, CN302958740S, CN302972196S, CN303017695S, CN303057352S, CN303094192S, CN303094708S, CN303094709S, CN303100274S, CN303106311S, CN303140437S, CN303140751S, CN303141049S, CN303149472S, CN303188313S, CN303188592S, CN303195567S, CN303196232S, CN303196246S, CN303214412S, CN303214628S, CN303214629S, CN303215631S, CN303226517S, CN303237668S, CN303237902S, CN303237903S, CN303238245S, CN303238252S, CN303326103S, CN303356001S, CN303365885S, CN303366328S, CN303375233S, CN303385198S, CN303407723S, CN303437045S, CN303450031S, CN303450032S, CN303450033S, CN303450287S, CN303450382S, CN303464325S, CN303464388S, CN303467590S, CN303467592S, CN303517976S, CN303518242S, CN303518469S, CN303539557S, CN303540879S, CN303560245S, CN303633312S, CN303645688S, CN303645693S, CN303653177S, CN303653178S, CN303653181S, CN303664147S, CN303668790S, CN303668834S, CN303689864S, CN303735772S, CN303736675S, CN303736676S, CN303753876S, CN303767851S, CN303767852S, CN303768086S, CN303768887S, CN303769424S, CN303788440S, CN303802657S, CN303803358S, CN303814227S, CN303814228S, CN303823532S, CN303836846S, CN303836847S, CN303852002S, CN303852003S, CN303861640S, CN303876611S, CN303885186S, CN303885662S, CN303905645S, CN303945357S, CN304003215S, CN304003630S, CN304026085S, CN304040482S, CN304040949S, CN304040953S, CN304041269S, CN304070661S, CN304079466S, CN304101518S, CN304110061S, CN304136597S, CN304137064S, CN304151907S, CN304165558S, CN304166221S, CN304239294S, CN304239295S, CN304239296S, CN304248450S, CN304262179S, CN304266034S, CN304269515S, CN304286943S, CN304291293S, CN304296419S, CN304326545S, CN304326546S, CN304339649S, CN304352509S, CN304352510S, CN304358276S, CN304362734S, CN304370229S, CN304398791S, CN304399147S, CN304401081S, CN304406789S, CN304406790S, CN304460005S, CN304503364S, CN304507376S, CN304517765S, CN304518120S, CN304552591S, CN304552747S, CN304564878S, CN304564888S, CN304565021S, CN304582347S, CN304592137S, CN304592510S, CN304612007S, CN304618068S, CN304645947S, CN304670555S, CN304682531S, CN304709828S, CN304710049S, CN304710071S, CN304726225S, CN304735945S, CN304744178S, CN304746292S, CN304750783S, CN304766598S, CN304792132S, CN304852321S, CN304856525S, CN304873132S, CN304880084S, CN304929719S, CN304932177S, CN304950849S, CN304966561S, CN304966686S, CN304972876S, CN304991181S, CN304997152S, CN304997611S, CN305008145S, CN305048659S, CN305050288S, CN305069771S, CN305134909S, CN305155212S, CN305168131S, CN305170848S, CN305186368S, CN305201137S, CN305254134S, CN305264212S, CN305284702S, CN305337727S, CN305343081S, CN305343082S, CN305343086S, CN305352003S, CN305360567S, CN305375125S, CN305379977S, CN305425696S, CN305431969S, CN305441090S, CN305470800S, CN305529000S, CN305579824S, CN305712751S, CN305764763S, CN305764764S, CN305772426S, CN305876001S, CN305884403S, CN305902174S, CN305910605S, CN305936999S, CN305954862S, CN306102387S, CN306138705S, CN306204631S, CN306222104S, CN306222150S, CN306288379S, CN306322357S, CN306347904S, CN306347913S, CN306366118S, CN306379914S, CN306380155S, CN306493249S, CN306496101S, CN306516522S, CN306516523S, CN306529619S, CN306558642S, CN306558891S, CN306585984S, CN306609844S, CN306683047S, CN306714211S, CN306758580S, CN306775173S, CN306811163S, CN306861110S, CN306890554S, CN307029962S, CN307035539S, CN307080808S, CN307081074S, CN307166564S, CN307188661S, CN307188909S, CN307252851S, CN307365687S, CN307400634S, CN307400635S, CN307460076S, CN307474527S, CN307520473S, CN307567348S, CN307652604S, CN307681933S, CN307719280S, CN307737795S, CN307767567S, CN307808733S, CN307823173S, CN307917542S, CN307922958S, CN307995520S, CN308021328S, CN308128388S, CN308134130S, CN309447893S

### 17.2 The other 290

| Number | Title | Runs | Reason |
|---|---|---|---|
| AU1345995A | Metabolic treatments | P1n | no deception or placement content in the title |
| AU2014240370A1 | Amphoteric liposomes comprising neutral lipids | P1n | no deception or placement content in the title |
| AU2016279050A1 | Tumor immunotherapy | P1n | the term in another sense, or not a cyber-security patent |
| AU2016303474A1 | Motile sperm domain containing protein 2 and cancer | P1n | the term in another sense, or not a cyber-security patent |
| AU2018394875A1 | Conjugates and preparation and use thereof | P1n | no deception or placement content in the title |
| AU2020100181A4 | Stable Prebiotic Compositions | P1b | no deception or placement content in the title |
| AU2020276307A1 | Ultraspecific cell targeting using de novo designed co-localization dependent … | P1n | no deception or placement content in the title |
| AU2022291426A1 | Chiral control | P1n | no deception or placement content in the title |
| BR102016018421A2 | COMPOSITION CONTAINING EUROPEAN AND INDIGENOUS BEE AVERAGES WITH ANTIMICROBIAN … | P1b | no deception or placement content in the title |
| BR102016018421B1 | COMPOSITION CONTAINING EUROPEAN AND INDIGENOUS BEES HONEY WITH ANTIMICROBIAL … | P1b | no deception or placement content in the title |
| BR112020007139A2 | treatment of smc-mediated disease | P1n | no deception or placement content in the title |
| CA2158663A1 | Perhydroisoindole derivatives, their preparation and pharmaceutical … | P1b | no deception or placement content in the title |
| CA2968327C | Systems and methods for malicious code detection accuracy assurance | P2f | no deception or placement content in the title |
| CA3087106C | Conjugates and preparation and use thereof | P1n | no deception or placement content in the title |
| CA3140064A1 | Lockr-mediated recruitment of car t cells | P1n | no deception or placement content in the title |
| CA3200622A1 | Micellar nanoparticles and uses thereof | P1n | no deception or placement content in the title |
| CA3208196A1 | Coronal protein-coated nanoparticles and uses thereof | P1n | no deception or placement content in the title |
| CA3215606A1 | Improved compositions for delivery of mrna | P1n | no deception or placement content in the title |
| CA3216346A1 | Hypoimmunogenic cells comprising engineered hla-e or hla-g | P1n | the term in another sense, or not a cyber-security patent |
| CN101009704A | A computer system and method for processing advanced network content | P2f | no deception or placement content in the title |
| CN101141243A | A device and method for performing security inspection and content filtering on … | P2f | no deception or placement content in the title |
| CN101141447A | HTTPS communication tunnel security inspection and content filtering system and … | P2f | no deception or placement content in the title |
| CN101175013B | Refused service attack protection method, network system and proxy server | P2f | no deception or placement content in the title |
| CN101247406A | Method for Classifying Local Information Using Global Intelligence and Spam … | P2f | no deception or placement content in the title |
| CN102663214A | Construction and prediction method of integrated drug target prediction system | P1n | no deception or placement content in the title |
| CN103271179B | Nine-processed honey tea and processing method thereof | P1b | the term in another sense, or not a cyber-security patent |
| CN103271258A | Health product and application thereof | P1b | no deception or placement content in the title |
| CN103641795A | Acetophenone derivatives containing 1,2,3-thiadiazole and preparation method … | P1n | no deception or placement content in the title |
| CN103803949B | A kind of Yao county kiln tea foam vitreous enamel and manufacture method … | P1b | no deception or placement content in the title |
| CN103952460B | A kind of method differentiating natural honey and artificial honey | P1b | no deception or placement content in the title |
| CN104053356B | Improvements in beekeeping | P1b | the term in another sense, or not a cyber-security patent |
| CN104781127B | Automatic audio optimization system | P1b | the term in another sense, or not a cyber-security patent |
| CN104815430B | A kind of golf swing batting exit point prover and its training method | P1b | the term in another sense, or not a cyber-security patent |
| CN105329569A | Honey storing and transporting trough | P1b | the term in another sense, or not a cyber-security patent |
| CN105777064A | Black-body celadon body material, black-body celadon ware and production method … | P1b | the term in another sense, or not a cyber-security patent |
| CN105920814A | Golf club head and golf club having the same | P1b | the term in another sense, or not a cyber-security patent |
| CN106082663A | A kind of green statin glaze containing shraff and preparation method thereof | P1b | the term in another sense, or not a cyber-security patent |
| CN106941645A | The audio reproduction of a large amount of audiences | P1b | the term in another sense, or not a cyber-security patent |
| CN106954173B | Method and apparatus for playback of higher order ambisonic audio signals | P1b | the term in another sense, or not a cyber-security patent |
| CN107456434A | Compact pore composition and preparation method thereof | P1b | no deception or placement content in the title |
| CN107505349B | A kind of nuclear magnetic resonance decoupling hydrogen spectrometry method to … | P1b | no deception or placement content in the title |
| CN107518153A | A kind of preparation method of small molecule biological feedstuff | P1b | the term in another sense, or not a cyber-security patent |
| CN107551505A | Iron golf club head | P1b | the term in another sense, or not a cyber-security patent |
| CN107568468A | A kind of small molecule biological feedstuff | P1b | the term in another sense, or not a cyber-security patent |
| CN107823576A | Antipsychotic capsule | P1b | no deception or placement content in the title |
| CN108936605A | A kind of high-purity deerskin glue and preparation method thereof | P1b | the term in another sense, or not a cyber-security patent |
| CN108967479A | Qingqian Willow leaf biscuit and preparation method thereof | P1b | no deception or placement content in the title |
| CN108983165A | … interference method of netted radar system based on substation selection | P1n | the term in another sense, or not a cyber-security patent |
| CN109884211A | A kind of assay method for detecting glycerin content in honey | P1b | no deception or placement content in the title |
| CN110463956A | A kind of the production and processing device and technique of crystallization … | P1b | the term in another sense, or not a cyber-security patent |
| CN110501099A | The method that the chemically reinforced glass by ion exchange containing … | P1b | no deception or placement content in the title |
| CN110620656A | Polarization coding-based integrated weak coherent light source component | P1n | no deception or placement content in the title |
| CN111030247B | A switching circuit for type C switching between host and device modes | P1n | no deception or placement content in the title |
| CN111260908A | Infrared characteristic simulation system and method applicable to simulation … | P1n | no deception or placement content in the title |
| CN111815202B | Honey production prediction method and system | P1b | the term in another sense, or not a cyber-security patent |
| CN112274611A | A pharmaceutical composition for treating acute alcoholism, and its preparation … | P1b | no deception or placement content in the title |
| CN112759620A | Liver targeting compounds and oligonucleotide conjugates | P1n | the term in another sense, or not a cyber-security patent |
| CN1129526A | Plum blossom health-care tea for eliminating summer-heat | P1b | no deception or placement content in the title |
| CN113033180A | Service system for automatically generating Tibetan language reading problems … | P1n | no deception or placement content in the title |
| CN113992375A | Heterogeneous complex network defense method based on genetic algorithm | P3b | the term in another sense, or not a cyber-security patent |
| CN114174914A | Lens driving device, camera module, and optical apparatus | P1n | no deception or placement content in the title |
| CN114217624B | Path planning method and device for bridge crane | P1b | no deception or placement content in the title |
| CN115035184B | A method for estimating the volume of pomelo based on lateral multi-view … | P1b | no deception or placement content in the title |
| CN116027360A | Beidou broadband interference resistant identification system | P1n | the term in another sense, or not a cyber-security patent |
| CN116762775A | Environment-friendly insect prevention device for white peony | P1n | no deception or placement content in the title |
| CN117892217A | Method and system for identifying inconsistencies between multimodal titles and … | P1n | no deception or placement content in the title |
| CN118246448A | Named entity recognition method based on BERT model | P1n | no deception or placement content in the title |
| CN118571312A | LCK inhibitor virtual screening method, device, equipment and storage medium … | P1n | no deception or placement content in the title |
| CN118797262A | A time series prediction method based on NABC-BiGRU and self-attention … | P1n | no deception or placement content in the title |
| CN118800344A | A method for predicting KRAS inhibitor activity based on machine learning | P1n | no deception or placement content in the title |
| CN118981356A | A Ethereum ERC20 honeypot contract detector and detection method in blockchain | P1b | the term in another sense, or not a cyber-security patent |
| CN119451723A | Compositions, systems and methods for treating cancer using tumor treating … | P1n | the term in another sense, or not a cyber-security patent |
| CN121604977A | Multivalent cargo carrying complex and uses thereof | P1n | no deception or placement content in the title |
| CN121634307A | A method for determining favorable lithofacies assemblages in terrestrial mixed … | P1b | no deception or placement content in the title |
| CN1226664C | Improved electrophoretic display device and its manufacture | P2d | not a deception patent; matched on the assignee name |
| CN205511605U | A get honey machine automatically for well bee honeycomb | P1b | no deception or placement content in the title |
| CN205826228U | A kind of integral type inflation test point light source | P1b | no deception or placement content in the title |
| CN206604422U | A kind of reactor of honey concentration | P1b | the term in another sense, or not a cyber-security patent |
| CN207755833U | Honey sterilising filtration device | P1b | no deception or placement content in the title |
| CN208434551U | The combination frame of one seed honey separation | P1b | the term in another sense, or not a cyber-security patent |
| CN208692057U | A kind of wooden son honey separation combination frame | P1b | the term in another sense, or not a cyber-security patent |
| CN208770417U | A kind of steam honey pot | P1b | the term in another sense, or not a cyber-security patent |
| CN208838590U | It is a kind of can be with the steam honey pot of temperature adjustment | P1b | the term in another sense, or not a cyber-security patent |
| CN208972333U | A kind of honey separating machine of high speed | P1b | the term in another sense, or not a cyber-security patent |
| CN209089704U | A kind of honey separating machine of variable-ratio | P1b | the term in another sense, or not a cyber-security patent |
| CN209345998U | A kind of honey dehydration device | P1b | the term in another sense, or not a cyber-security patent |
| CN209767560U | Polarization coding-based integrated weak coherent light source component | P1n | no deception or placement content in the title |
| CN212763597U | High-efficient swift onion filament cutter | P1b | the term in another sense, or not a cyber-security patent |
| CN219918439U | LED wireless charging desk lamp supporting multi-protocol quick charging | P1n | no deception or placement content in the title |
| CN224329227U | A charging device for an interface device | P1n | no deception or placement content in the title |
| DE202026001140U1 | Device for detecting moving objects and arrangement with such a device | P1n | no deception or placement content in the title |
| DE2525569A1 | Identification of pick=up from acoustic mine sweepers - uses fact that sound … | P1n | no deception or placement content in the title |
| DE4322421A1 | Biscuit containing wheat flour, fat, whole milk, salt and a raising agent | P1b | no deception or placement content in the title |
| EA049052B1 | VACCINE COMPOSITION AGAINST STREPTOCOCCUS PNEUMONIAE INFECTION | P1n | no deception or placement content in the title |
| EP1185316A1 | Devices and compounds for treating arterial restenosis | P1n | no deception or placement content in the title |
| EP2063709A2 | Hindered ester-based biodegradable linkers for oligonucleotide delivery | P1n | the term in another sense, or not a cyber-security patent |
| EP2076257A2 | Polymeric conjugates containing positively-charged moieties | P1n | no deception or placement content in the title |
| EP2347366B1 | Improvements in or relating to digital forensics | P2f | no deception or placement content in the title |
| EP2474556A2 | APCDD1 inhibitors for treating, diagnosing or detecting cancer | P1n | the term in another sense, or not a cyber-security patent |
| EP2562560A1 | Method and system for detecting fraudulent positioning information from a … | P1n | no deception or placement content in the title |
| EP2606130A2 | Camkk-beta as a target for treating cancer | P1n | the term in another sense, or not a cyber-security patent |
| EP2859495B1 | Malicious message detection and processing | P2i | no deception or placement content in the title |
| EP3195140A1 | Malicious message detection and processing | P2i | no deception or placement content in the title |
| EP3418937A1 | Method for creating a decoy of an operation of an integrated circuit and … | P1n | the title reads as a hardware side-channel countermeasure (a decoy of an operation inside an integrated circuit), not network deception; judged on the title |
| EP3933811A1 | Dynamically adapting cybersecurity training templates based on measuring user- … | P2i | no deception or placement content in the title |
| EP3984186B1 | Executing real-time message monitoring to identify potentially malicious … | P2i | no deception or placement content in the title |
| EP3993361B1 | Bulk messaging detection and enforcement | P2i | no deception or placement content in the title |
| EP3993362B1 | Detecting and preventing transmission of spam messages using modified source … | P2i | no deception or placement content in the title |
| EP4009160B1 | Methods for application deployment across multiple computing domains and devices thereof | P4 | no deception or placement content in the title |
| EP4152729B1 | Interactive email warning tags | P2i | no deception or placement content in the title |
| EP4471581A1 | Methods for generating an application programming interface inventory and devices thereof | P4 | no deception or placement content in the title |
| ES2932030B2 | POWDERED HONEY PREPARATION METHOD BY VACUUM DRYING | P1b | no deception or placement content in the title |
| ES2932054B2 | HONEY POWDER PREPARATION METHOD BY LYODRYING | P1b | the term in another sense, or not a cyber-security patent |
| ES482754A1 | Procedure for obtaining a wax depilator. (Machine-translation by Google … | P1b | no deception or placement content in the title |
| FR2561701A1 | Keyless lock allowing the opening or closing of a door by means of a coded … | P1n | no deception or placement content in the title |
| FR2845565A1 | … section which fits into bait, stabilizer returning bait to horizontal position … | P1n | the term in another sense, by title: a fishing lure; the page was not opened |
| FR2929393A1 | Rugosity value e.g. macro-rugosity value, determining method for managing … | P1b | the term in another sense, or not a cyber-security patent |
| HK1244125A1 | Systems and methods for malicious code detection accuracy assurance | P2f | no deception or placement content in the title |
| HK1250813B | Computer network security system | P2f | no deception or placement content in the title |
| HK40134827A | Methods of treating cancer associated with reduced interleukin 1 beta … | P1n | the term in another sense, or not a cyber-security patent |
| IL263686A | Treatment of amd using aav2 variant with aflibercept | P1n | no deception or placement content in the title |
| IL264064A | Hiv pre-immunization and immunotherapy | P1n | the term in another sense, or not a cyber-security patent |
| IL297460A | Compositions and methods related to scavenger particles | P1n | no deception or placement content in the title |
| JP2011244331A | Data input system and data input program | P1b | the term in another sense, or not a cyber-security patent |
| JP2012509066A5 | Patent JP2012509066A5 | P1n | no deception or placement content in the title |
| JP2012509272A5 | Patent JP2012509272A5 | P1n | no deception or placement content in the title |
| JP2014235357A | Globe and world map | P1b | no deception or placement content in the title |
| JP2019508063A | Oncolytic virus vector and use thereof | P1n | no deception or placement content in the title |
| JP2019529210A | Automotive headlamp with low beam lift function | P1n | no deception or placement content in the title |
| JP2025509220A | Methods and Compositions for the Treatment and Prevention of Fibrosis | P1n | no deception or placement content in the title |
| JP5505078B2 | Data input system and data input program | P1b | the term in another sense, or not a cyber-security patent |
| JP7302665B2 | Analysis system, method and program | P4 | no deception or placement content in the title |
| JPS5911162A | Preparation of health drink containing extract of snapping turtle | P1b | the term in another sense, or not a cyber-security patent |
| JPS59501809A | Method of recording and reproducing acoustic phenomena and apparatus for … | P1n | no deception or placement content in the title |
| JPS6085124A | Slewing type working vehicle | P1n | no deception or placement content in the title |
| KR102548703B1 | Providing method, apparatus and computer-readable medium of controlling access to a remote system in a home network environment | P4 | no deception or placement content in the title |
| KR20010105111A | Cosmetic composition for containing jade powder | P1b | no deception or placement content in the title |
| KR20220164736A | De novo protein decoy of angiotensin converting enzyme 2 (ACE2) | P1n | the term in another sense: a protein decoy (biomedical), judged on the title |
| KR20260105714A | Methods to treat cancer associated with reduced interleukin 1 beta expression | P1n | the term in another sense, or not a cyber-security patent |
| MXPA02009738A | Polyamide nucleic acid derivatives, agents and methods for producing the same. | P1n | the term in another sense, or not a cyber-security patent |
| NZ622092A | Antibodies against tl1a and uses thereof | P1n | the term in another sense, or not a cyber-security patent |
| NZ751584A | Antibodies to mica and micb proteins | P1n | the term in another sense, or not a cyber-security patent |
| NZ751584B2 | Antibodies to mica and micb proteins | P1n | the term in another sense, or not a cyber-security patent |
| RU2826261C2 | Method and systems for prediction of hla class ii-specific epitopes and cd4+ t- … | P1n | no deception or placement content in the title |
| TW200422525A | High performance axial fan | P1b | the term in another sense, or not a cyber-security patent |
| TW200914097A | Electronic game utilizing photographs | P1b | no deception or placement content in the title |
| TW201522363A | Continuous multistep process for purifying antibodies | P1b | the term in another sense, or not a cyber-security patent |
| TW567080B | Golf club | P1b | the term in another sense, or not a cyber-security patent |
| TWI222374B | Striking faceplate for golf club head | P1b | the term in another sense, or not a cyber-security patent |
| TWM507653U | Lure | P1n | the term in another sense: the title "Lure" alone, a utility model that reads as a fishing lure; judged on the title |
| UA121464C2 | ANTI-JAGGED1 ANTIBODY AND METHODS OF ITS APPLICATION | P1n | the term in another sense, or not a cyber-security patent |
| UA124301C2 | SALTS OF 1- (4- (2 - ((1- (3,4-DIFLUTORPHENYL) -1H-PYRAZOL-3-YL) METHOXY) ETHYL … | P1n | no deception or placement content in the title |
| UA125120C2 | BETA-3 MODULATORS OF THE ADRENERGIC RECEPTOR USEFUL IN THE TREATMENT AND … | P1n | no deception or placement content in the title |
| US10169586B2 | Ransomware detection and damage mitigation | P2f | no deception or placement content in the title |
| US10218741B2 | Immunizing network devices using a malware marker | P3b | the term in another sense, or not a cyber-security patent |
| US10230743B1 | Rogue endpoint detection | P4 | no deception or placement content in the title |
| US10367832B2 | Reactive virtual security appliances | P4 | no deception or placement content in the title |
| US10397250B1 | Methods for detecting remote access trojan malware and devices thereof | P4 | no deception or placement content in the title |
| US10432652B1 | Methods for detecting and mitigating malicious network behavior and devices thereof | P4 | no deception or placement content in the title |
| US10445479B2 | Spatiotemporal credential leak detection to prevent identity fraud using a log … | P2f | no deception or placement content in the title |
| US10447665B2 | IPv6 link local secure network with biometric security to secure IOT devices | P4 | no deception or placement content in the title |
| US10462188B2 | Computer network security system | P2f | no deception or placement content in the title |
| US10476947B1 | Methods for managing web applications and devices thereof | P4 | no deception or placement content in the title |
| US10484418B2 | Systems and methods for updating security policies for network traffic | P2f | no deception or placement content in the title |
| US10511562B2 | Classifying social entities and applying unique policies on social entities … | P2i | no deception or placement content in the title |
| US10521584B1 | Computer threat analysis service | P4 | no deception or placement content in the title |
| US10542044B2 | Authentication incident detection and management | P2c | no deception or placement content in the title |
| US10581902B1 | Methods for mitigating distributed denial of service attacks and devices thereof | P4 | no deception or placement content in the title |
| US10594708B2 | Providing security in a communication network | P2f | no deception or placement content in the title |
| US10616272B2 | Dynamically detecting abnormalities in otherwise legitimate emails containing … | P2i | no deception or placement content in the title |
| US10666681B2 | Detecting malicious actors | P4 | no deception or placement content in the title |
| US10716027B1 | Extending airtime fairness in WLANS (wireless local access networks) with … | P2f | no deception or placement content in the title |
| US10728135B2 | Location based test agent deployment in virtual processing environments | P4 | no deception or placement content in the title |
| US10834110B1 | Methods for preventing DDoS attack based on adaptive self learning of session and transport layers and devices thereof | P4 | no deception or placement content in the title |
| US10969467B1 | Programmable multi-waveform RF generator for use as battlefield decoy | P4 | the term in a non-cyber sense |
| US11038869B1 | Methods for managing a federated identity environment based on application availability and devices thereof | P4 | no deception or placement content in the title |
| US11096243B2 | Programmable multi-waveform RF generator for use as battlefield decoy | P4 | the term in a non-cyber sense |
| US11165802B2 | Network security assessment using a network traffic parameter | P4 | no deception or placement content in the title |
| US11171916B2 | Domain name classification systems and methods | P2i | no deception or placement content in the title |
| US11184372B2 | Detection and mitigation of time-delay based network attacks | P2f | no deception or placement content in the title |
| US11223635B2 | Inception of suspicious network traffic for enhanced network security | P2f | no deception or placement content in the title |
| US11258763B2 | Computer network security configuration visualization and control system | P4 | no deception or placement content in the title |
| US11349981B1 | Methods for optimizing multimedia communication and devices thereof | P4 | no deception or placement content in the title |
| US11363048B1 | Information security systems for threat detection (two) | P4 | no deception or placement content in the titles |
| US11444957B2 | Automated feature extraction and artificial intelligence (AI) based detection … | P2f | no deception or placement content in the title |
| US11445380B2 | Methods and systems of automatic network deployment deviation detection | P4 | no deception or placement content in the title |
| US11463264B2 | Use of data block signatures for monitoring in an information management system | P2g | no deception or placement content in the title |
| US11526617B2 | Information security systems for threat detection (two) | P4 | no deception or placement content in the titles |
| US11539740B1 | Methods for protecting CPU during DDoS attack and devices thereof | P4 | no deception or placement content in the title |
| US11611590B1 | System and methods for reducing the cybersecurity risk of an organization by … | P2i | no deception or placement content in the title |
| US11616806B1 | Methods for protecting web based resources from D/DoS attacks and devices thereof | P4 | no deception or placement content in the title |
| US11621893B2 | Methods, systems, and computer readable media for establishing dynamic agent associations in a cloud computing environment | P4 | no deception or placement content in the title |
| US11636213B1 | System and methods for reducing an organization's cybersecurity risk based on … | P2i | no deception or placement content in the title |
| US11640470B1 | System and methods for reducing an organization's cybersecurity risk by … | P2i | no deception or placement content in the title |
| US11665135B2 | Domain name processing systems and methods | P2i | no deception or placement content in the title |
| US11687548B2 | Storage of backup data using a time-series data lake | P2g | no deception or placement content in the title |
| US11716255B1 | Methods and systems for automatic network topology deviation detection | P4 | no deception or placement content in the title |
| US11973799B2 | Domain name processing systems and methods | P2i | no deception or placement content in the title |
| US12052276B2 | People-centric threat scoring | P2i | no deception or placement content in the title |
| US12052278B1 | Cloud data peak signal detection and prioritization for data security posture … | P2i | no deception or placement content in the title |
| US12058782B2 | Programmable multi-waveform RF generator for use as battlefield decoy | P4 | the term in a non-cyber sense |
| US12063140B2 | Methods, systems, and computer readable media for test system agent deployment in a smartswitch computing environment | P4 | no deception or placement content in the title |
| US12113820B2 | Threat actor identification systems and methods | P2i | no deception or placement content in the title |
| US12143410B1 | Incremental cloud infrastructure detection for data security posture management | P2i | no deception or placement content in the title |
| US12197618B2 | Database log analyzer in a cloud environment using microservice orchestration | P2i | no deception or placement content in the title |
| US12231463B2 | Content-based socially-engineered threat classifier | P2i | no deception or placement content in the title |
| US12238127B1 | Anomalous data transfer detection | P4 | no deception or placement content in the title |
| US12271811B2 | Systems and methods for email campaign domain classification | P2i | no deception or placement content in the title |
| US12307531B2 | Detection and prevention of fraudulent activity on social media accounts | P2i | no deception or placement content in the title |
| US12314288B2 | Data scan sampling control for data discovery and posture management | P2i | no deception or placement content in the title |
| US12323464B2 | Expedited recovery based on data storage management integration with cyber … | P2g | no deception or placement content in the title |
| US12347212B2 | Visual domain detection systems and methods | P2i | no deception or placement content in the title |
| US12381901B1 | Unified storage for event streams in an anomaly detection framework | P2f | no deception or placement content in the title |
| US12401685B2 | Methods for mitigating DDoS attack using hardware device and devices thereof | P4 | no deception or placement content in the title |
| US12500825B2 | Systems and methods for network traffic monitoring | P4 | no deception or placement content in the title |
| US12519827B2 | Methods for detecting ICMP flood attacks | P4 | no deception or placement content in the title |
| US12536235B2 | Using a machine learning system to process a corpus of documents associated … | P2i | no deception or placement content in the title |
| US12549577B1 | Tracking and relating discovered security issues over time | P2f | no deception or placement content in the title |
| US12627686B1 | Generating the ancestry of a deployment in a cloud environment | P2f | no deception or placement content in the title |
| US12627706B2 | Volumetric distributed denial of service attack mitigation | P4 | no deception or placement content in the title |
| US12652297B2 | Automatic risk remediation in multi-cloud environment | P2i | no deception or placement content in the title |
| US12672021B2 | Methods for efficient overload protection in 5G core networks | P4 | no deception or placement content in the title |
| US12712913B2 | Machine learning for visual similarity-based phishing detection | P2f | no deception or placement content in the title |
| US20030151271A1 | Torsion absorber for roller crank assemblies | P1b | no deception or placement content in the title |
| US20050203881A1 | Database user behavior monitor system and method | P2f | no deception or placement content in the title |
| US20070042344A1 | Differentiation regulating agent containing gene which regulating … | P1n | the term in another sense, or not a cyber-security patent |
| US20070269406A1 | Transcatheter tumor immunoembolization | P1n | the term in another sense, or not a cyber-security patent |
| US20100124746A1 | Method for the detection of gene transcripts in blood and uses thereof | P1n | the term in another sense, or not a cyber-security patent |
| US20110229581A1 | Releasable cationic lipids for nucleic acids delivery systems | P1n | the term in another sense, or not a cyber-security patent |
| US20110230420A1 | Releasable conjugates for nucleic acids delivery systems | P1n | the term in another sense, or not a cyber-security patent |
| US20110274745A1 | Instillation of liposomal formulation of sirna and antisense oligonucleotides | P1n | the term in another sense, or not a cyber-security patent |
| US20160180022A1 | Abnormal behaviour and fraud detection based on electronic medical records | P2f | no deception or placement content in the title |
| US20190108340A1 | Ransomware detection | P2g | no deception or placement content in the title |
| US20190109870A1 | Ransomware detection and intelligent restore | P2g | no deception or placement content in the title |
| US20190245885A1 | Methods and Systems for Malicious Message Detection and Processing | P2i | no deception or placement content in the title |
| US20190336608A1 | Cationic carriers for nucleic acid delivery | P1n | the term in another sense, or not a cyber-security patent |
| US20190336611A1 | Hybrid carriers for nucleic acid cargo | P1n | the term in another sense, or not a cyber-security patent |
| US20200214039A1 | Increasing downstream network throughput from access points in data … | P2f | no deception or placement content in the title |
| US20200285735A1 | Controlling access to external networks by an air-gapped endpoint | P2f | no deception or placement content in the title |
| US20210200859A1 | Malware detection by a sandbox service by utilizing contextual information | P2f | no deception or placement content in the title |
| US20210271758A1 | Ransomware detection and data pruning management | P2g | no deception or placement content in the title |
| US20210390181A1 | Generating Simulated Spear Phishing Messages and Customized Cybersecurity … | P2i | no deception or placement content in the title |
| US20220006830A1 | Modeling Simulated Cybersecurity Attack Difficulty | P2i | no deception or placement content in the title |
| US20230087093A1 | Cloud environment analytics using snapshotting | P2i | no deception or placement content in the title |
| US20230094856A1 | Compact cloud access network based on role-to-resource detection with resource … | P2i | no deception or placement content in the title |
| US20230231879A1 | Machine learning for visual similarity-based phishing detection | P2f | no deception or placement content in the title |
| US20230336588A1 | Simulated Phishing Lure Generation Using Artificial Intelligence for Improved … | P2i | a simulated-phishing training patent, not a deception-technology patent; judged on the title |
| US20240176874A1 | Preserving dll hooks | P2c, P2h | no deception or placement content in the title |
| US20240205251A1 | Methods, systems, and devices for dynamically modeling and grouping endpoints … | P2h | no deception or placement content in the title |
| US20240291760A1 | Global visibility for virtual private network (vpn) conditions for routing … | P2f | no deception or placement content in the title |
| US20240333760A1 | Systems and methods for network endpoint device security fabric | P2f | no deception or placement content in the title |
| US20250005144A1 | Detecting insider user behavior threats by comparing a user’s behavior to the … | P2i | no deception or placement content in the title |
| US20250113254A1 | Dynamically maximizing sub-channel bandwidth utilization for ofdma … | P2f | no deception or placement content in the title |
| US20250113288A1 | Smart bss-coloring to overcome co-channel-interference (cci) for wi-fi6 | P2f | no deception or placement content in the title |
| US20250168171A1 | Cloud infrastructure excessive resource permission detection based on semantic … | P2i | no deception or placement content in the title |
| US20250247435A1 | System and Methods for Agentless Managed Device Identification as Part of … | P2i | no deception or placement content in the title |
| US20250272417A1 | Computing System Access Path Detection And Governance For Data Security Posture … | P2i | no deception or placement content in the title |
| US20250284841A1 | Systems and methods for detecting risk events in a computing environment using … | P2i | no deception or placement content in the title |
| US20250301009A1 | Asset crawling with internet archives for enhanced web application scanning | P2f | no deception or placement content in the title |
| US20250310120A1 | Computing system data posture analysis using signature encoders with similarity … | P2i | no deception or placement content in the title |
| US20250310351A1 | Threat-informed adversary attack simulation | P2f | no deception or placement content in the title |
| US20250310374A1 | Training trusted users of an enterprise network for phishing attacks on a per- … | P2f | no deception or placement content in the title |
| US20250342266A1 | Data posture analysis using a distinct scanner environment | P2i | no deception or placement content in the title |
| US20260006073A1 | Accelerated detection of spear phishing during email malware detection on … | P2f | no deception or placement content in the title |
| US20260023845A1 | Generalizing extended detection and response events through vector embeddings | P2h | no deception or placement content in the title |
| US20260064835A1 | Externally securing unmanaged devices using artificial intelligence operations … | P2f | no deception or placement content in the title |
| US20260205484A1 | Systems, methods, and devices for preventing credential passing attacks | P2h | no deception or placement content in the title |
| US6772196B1 | Electronic mail filtering system and methods | P2i | no deception or placement content in the title |
| US7783597B2 | Email filtering using recipient reputation | P2i | no deception or placement content in the title |
| US8423483B2 | User-controllable learning of policies | P2i | no deception or placement content in the title |
| US8569504B2 | Imidazopyridine compound | P1n | no deception or placement content in the title |
| US9143476B2 | Real-time classification of email message traffic | P2i | no deception or placement content in the title |
| US9503477B2 | Network policy assignment based on user reputation score | P2f | no deception or placement content in the title |
| US9609019B2 | System and method for directing malicous activity to a monitoring system | P2c, P2h | no deception or placement content in the title |
| US9634989B2 | Systems and methods for detecting undesirable network traffic content | P2f | no deception or placement content in the title |
| US9769204B2 | Distributed system for Bot detection | P2h | no deception or placement content in the title |
| US9912694B2 | Dashboards for displaying threat insight information | P2i | no deception or placement content in the title |
| WO2000060433A2 | Techniques for communicating events among users and applications | P2c | no deception or placement content in the title |
| WO2001033362A1 | Action communication and synchronization for documents accessed by multiple … | P2c | no deception or placement content in the title |
| WO2001053965A1 | E-mail spam filter | P1n | no deception or placement content in the title |
| WO2007139150A1 | ANTI-INFLUENZA VIRAL AGENT COMPRISING TNF-α INHIBITOR | P1n | no deception or placement content in the title |
| WO2010100899A1 | Genetic testing method for cancer by analysis of expression of cancer-relating … | P1n | the term in another sense, or not a cyber-security patent |
| WO2017197439A1 | Prebiotic compositions | P1b | no deception or placement content in the title |
| WO2021009033A1 | Method and device for detecting a decoy operation of a gnss system | P1n | the term in another sense, or not a cyber-security patent |
| WO2024084394A1 | Compositions and methods for delivering a macromolecule to a cell | P1n | no deception or placement content in the title |
| WO2025085598A2 | Personalized regenerative cells | P1n | no deception or placement content in the title |
| WO2025208000A1 | Methods of treating cancer in patients with altered protein expression | P1n | the term in another sense, or not a cyber-security patent |
| WO2026115520A2 | Hardware-Enforced Cryptographic Execution-Time Governance Infrastructure for … | P1n | no deception or placement content in the title |
| WO2026120177A1 | Novel long-acting degrader conjugates | P1n | no deception or placement content in the title |
| WO2026151479A1 | Assistive technology system for orchestrating multiple artificial intelligence … | P1n | no deception or placement content in the title |

## 18. The widened re-run of block O (D38)

D36 found that block O lacked six words for a power network ("power grid", "power system", "electric power", "new power system", "distribution network" and "power plant") and recommended a re-run before A12 and the freeze. The user agreed on 16 November 2026 (D37), and the protocol records it as amendment 8 (`01-search-protocol.md` §4; `sources.md` #990). The six words were run as a separate block O′ in place of block O, so each query returned only records carrying one of them, and records the first runs had returned were dropped. That gives the new records of a full widened run, except works added to the indexes since the first runs that carry only block O's words; the update re-run (A17) covers those. The classification run P3b, which also uses block O, was not repeated (D36 item 6 did not include it).

### 18.1 What ran

| Run | Index | String | Count | New in run order | `sources.md` |
|---|---|---|---|---|---|
| R1 | OpenAlex | S1 with O′ | 53 | 17 | #991 |
| R2 | OpenAlex | S2 with O′ | 28 | 8 | #992 |
| R3 | OpenAlex | S5 with O′ | 6 | 0 | #993 |
| R4 | Semantic Scholar | S1 with O′ | 39 | 2 | #994 |
| R5 | Semantic Scholar | S2 with O′ | 22 | 1 | #995 |
| R6 | Semantic Scholar | S5 with O′ | 4 | 0 | #996 |
| R7 = P1c | Google Patents | S1 with O′, title, abstract and claims | about 145 (100 + 45) | 102 | #997 |
| Backward round | Zhan et al.'s references | — | 56 | 55 | #998 |

### 18.2 Paper records 563–645

R1–R6 returned 73 distinct records; 45 had been returned by the first runs and 28 are new. Zhan et al.'s backward round added 55 (§18.3). The 83 are numbered in alphabetical order of normalised title: T2 1, related (T1) 11, excluded 71. None was in `sources.md` before. No excluded title carries both a deception term and an OT term, so none needs the user's confirmation (§9). Of the 19 run records excluded, 10 use a deception word in another sense (decoy states in quantum key distribution, bird, naval and transport decoys, a photography essay), 6 have no deception asset (three use "distribution network" for malware or content delivery) and 3 are not works.

| Record | Title | Year | DOI | Found by | Tier | Judged on | Reason | `sources.md` |
|---|---|---|---|---|---|---|---|---|
| 563 | A Distributionally Robust Defender-Attacker-Defender Model for Resilience Enhancement of Power Systems Against Malicious Cyberattacks | 2022 | 10.1109/tpwrs.2022.3222309 | Zhan et al., ref. 23 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 564 | A Game-Theoretic Study of Load Redistribution Attack and Defense in Power Systems | 2017 | 10.1016/j.epsr.2017.05.020 | Zhan et al., ref. 46 | X | title | load-redistribution or false-data attacks on a power system; no deception asset in the title | — |
| 565 | A General Framework for the Assessment of Power System Vulnerability to Malicious Attacks | 2017 | 10.1111/risa.12781 | Zhan et al., ref. 30 | X | title | power-system modelling or analysis; no deception asset in the title | — |
| 566 | A Kangaroo Escape Optimizer-Enabled Fractional-Order PID Controller for Enhancing Dynamic Stability in Multi-Area Power Systems | 2025 | 10.3390/fractalfract9080530 | R2 | X | title | power-system control (a PID controller); no deception asset | — |
| 567 | Analysis of Electric Grid Security Under Terrorist Threat | 2004 | 10.1109/tpwrs.2004.825888 | Zhan et al., ref. 33 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 568 | Analysis of the Cyber Attack on the Ukrainian Power Grid: Defense Use Case | 2016 | — | Zhan et al., ref. 19 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 569 | An Efficient Tri-Level Optimization Model for Electric Grid Defense Planning | 2016 | 10.1109/tpwrs.2016.2628887 | Zhan et al., ref. 44 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 570 | A Risk Analysis Framework for Cyber Security and Critical Infrastructure Protection of the US Electric Power Grid | 2020 | 10.1111/risa.13511 | Zhan et al., ref. 5 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 571 | A Robust Approach for Mitigating Risks in Cyber Supply Chains | 2019 | 10.1111/risa.13269 | Zhan et al., ref. 54 | X | title | a risk measure or optimisation method; no deception asset in the title | — |
| 572 | A Robust Power Grid Defense Model Considering Load Demand and Wind Generation Uncertainties | 2018 | — | Zhan et al., ref. 47 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 573 | Assessing and minimizing adversarial risk in a nuclear material transportation network | 2013 | — | R2+R5 | X | title | decoys in physical transport security, not cyber deception | — |
| 574 | A Survey of Security in SCADA Networks: Current Issues and Future Challenges | 2019 | 10.1109/access.2019.2926441 | Zhan et al., ref. 13 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 575 | A Tri-Level Distributionally Robust Defender-Attacker-Defender Model for Grid Resilience Enhancement Under Repair Time Uncertainty | 2025 | 10.3390/asi8040115 | Zhan et al., ref. 53 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 576 | A Tri-Level Optimization Model for Power Systems Defense Considering Cyber-Physical Interdependence | 2023 | 10.1049/gtd2.12758 | Zhan et al., ref. 14 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 577 | A Trilevel Programming Approach for Electric Grid Defense Planning | 2014 | 10.1016/j.cor.2013.06.009 | Zhan et al., ref. 2 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 578 | Behavioral Analysis of Insider Threat: A Survey and Bootstrapped Prediction in Imbalanced Data | 2014 | 10.1109/tcss.2014.2377811 | Zhan et al., ref. 4 | X | title | an insider-threat study; no deception asset in the title | — |
| 579 | BLITHE: Behavior Rule-Based Insider Threat Detection for Smart Grid | 2015 | 10.1109/jiot.2015.2459049 | Zhan et al., ref. 6 | X | title | an insider-threat study; no deception asset in the title | — |
| 580 | Characterization of Geometric Space via Homotopy Type Theory and Gnomonic Growth | 2026 | 10.5281/zenodo.20285647 | R1 | X | title | unrelated (mathematics) | — |
| 581 | Classification of Insider Threat Detection Techniques | 2016 | — | Zhan et al., ref. 36 | X | title | an insider-threat study; no deception asset in the title | — |
| 582 | Common Sense Guide to Mitigating Insider Threats | 2016 | — | Zhan et al., ref. 10 | X | title | an insider-threat study; no deception asset in the title | — |
| 583 | Computability of Global Solutions to Factorable Nonconvex Programs: Part I—Convex Underestimating Problems | 1976 | 10.1007/bf01580665 | Zhan et al., ref. 25 | X | title | a risk measure or optimisation method; no deception asset in the title | — |
| 584 | Computational science and its applications - ICCSA 2003 : International Conference, Montreal, Canada, May 18-21, 2003 : proceedings | 2003 | — | R5 | X | title | a proceedings volume, not a work | — |
| 585 | Conditional Value-at-Risk for General Loss Distributions | 2002 | 10.1016/s0378-4266(02)00271-6 | Zhan et al., ref. 32 | X | title | a risk measure or optimisation method; no deception asset in the title | — |
| 586 | COSMICENERGY: New OT Malware Possibly Related to Russian Emergency Response Exercises | 2023 | — | Zhan et al., ref. 24 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 587 | Cyberattack Graph Modeling for Visual Analytics | 2023 | 10.1109/access.2023.3304640 | R1+R3+R4+R6 | T1 | title | attack-graph modelling for visual analytics; no placement in the title | #1001 |
| 588 | Cyber–Physical System Security for the Electric Power Grid | 2011 | 10.1109/jproc.2011.2165269 | Zhan et al., ref. 40 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 589 | Cybersecurity Risk Management in Small and Medium-Sized Enterprises: A Systematic Review of Recent Evidence | 2020 | — | Zhan et al., ref. 1 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 590 | DC Power Flow in Unit Commitment Models | 2014 | — | Zhan et al., ref. 42 | X | title | power-system modelling or analysis; no deception asset in the title | — |
| 591 | Decoys and Documents | 1999 | 10.1525/aft.1999.27.1.12 | R1+R4 | X | title | the term in another sense (a photography essay) | — |
| 592 | Defense Strategy Against Load Redistribution Attacks on Power Systems Considering Insider Threats | 2020 | 10.1109/tsg.2020.3023426 | Zhan et al., ref. 22 | T1 | abstract (its OpenAlex record, read through the fetch tool's summary) | a security-resource allocation game against load-redistribution attacks with an insider who leaks the defence; no honeypot, decoy or deception; the model Zhan et al. extend with honeypots | #1002 |
| 593 | Detecting malicious landing pages in Malware Distribution Networks | 2013 | 10.1109/dsn.2013.6575316 | R1+R4 | X | title | web malware distribution networks; 'distribution network' in the malware sense, and no deception asset in the title | — |
| 594 | Dynamic Detection of False Data Injection Attack in Smart Grid Using Deep Learning | 2019 | — | Zhan et al., ref. 27 | X | title | load-redistribution or false-data attacks on a power system; no deception asset in the title | — |
| 595 | Dynamic Rescheduling of Trapping Resources Based on Electric Power Environment | 2025 | 10.1109/icsp65755.2025.11086961 | R1+R2+R4+R5 | T1 | abstract (the user's screenshot of the IEEE page, 16 November 2026; its last sentence cut) | honeypot container scheduling across the nodes of a power Kubernetes cluster by a particle-force model, for resource use and affinity rules, against Descheduler; it places containers on cluster nodes, not decoys where attackers move; the same group as #442 and #481, both T1 | #1003 |
| 596 | Dynamic Vulnerability Containment for Distributed Computing Ecosystems via Intelligent Decoy-Oriented Mechanisms | 2026 | — | R1+R2 | T1 | abstract (fetch tool's summary) | reinforcement-learning decoy allocation in cloud and distributed computing; power systems only as an evaluation context, so the OT gate fails | #1004 |
| 597 | Effects of Intentional Threats to Power Substation Control Systems | 2008 | 10.1504/ijcis.2008.016096 | Zhan et al., ref. 11 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 598 | Enhancing honeynet-based protection with network slicing for massive Pre-6G IoT Smart Cities deployments | 2024 | 10.1016/j.jnca.2024.103918 | R1 | T1 | title | honeynet protection with network slicing for IoT smart cities; no OT setting | #1005 |
| 599 | Ep. 722: The Seven-Day Sprint: Iran's Nuclear Threshold | 2026 | 10.5281/zenodo.19360938 | R2 | X | title | a podcast episode | — |
| 600 | Evolving IoT Botnet Threats and Practical Honeypot Observation: A Summary Review and Experimental Study | 2026 | 10.3390/jcp6030082 | R1+R4 | T1 | title | honeypot observation of IoT botnets; no placement | #1006 |
| 601 | Expiry Certified Cluster Routing for Renewable Key Pools in Trusted Relay QKD Networks | 2026 | 10.22541/authorea.15011356/v1 | R1 | X | title | decoy states in quantum key distribution | — |
| 602 | Extraction of Viscoelastic Decoherence in Satellite-to-Ground Quantum Entanglement | 2026 | 10.5281/zenodo.19064173 | R2 | X | title | quantum physics; the term in another sense | — |
| 603 | False Data Injection Attacks Against State Estimation in Electric Power Grids | 2011 | 10.1145/1952982.1952995 | Zhan et al., ref. 21 | X | title | load-redistribution or false-data attacks on a power system; no deception asset in the title | — |
| 604 | Focus on Quantum Cryptography: Theory and Practice | 2009 | 10.1088/1367-2630/11/4/045005 | R1+R2+R4+R5 | X | title | decoy states in quantum key distribution | — |
| 605 | Free-space reconfigurable quantum key distribution network | 2015 | 10.1109/icsos.2015.7425063 | R1+R4 | X | title | decoy states in quantum key distribution | — |
| 606 | Honeypots: Catching the Insider Threat | 2003 | — | Zhan et al., ref. 39 | T1 | title | honeypots against the insider threat; no placement in the title | #1007 |
| 607 | Implementation of Insider Threat Detection System Using Honeypot Based Sensors and Threat Analytics | 2020 | 10.1007/978-3-030-12385-7_56 | Zhan et al., ref. 48 | T1 | title | honeypot-based sensors for insider-threat detection; no placement in the title | #1008 |
| 608 | Insiders and Insider Threats—An Overview of Definitions and Mitigation Techniques | 2011 | — | Zhan et al., ref. 18 | X | title | an insider-threat study; no deception asset in the title | — |
| 609 | Insider Threat Identification by Process Analysis | 2014 | 10.1109/spw.2014.40 | Zhan et al., ref. 9 | X | title | an insider-threat study; no deception asset in the title | — |
| 610 | Insight into Insiders and It: A Survey of Insider Threat Taxonomies, Analysis, Modeling, and Countermeasures | 2019 | 10.1145/3303771 | Zhan et al., ref. 16 | X | title | an insider-threat study; no deception asset in the title | — |
| 611 | Intelligent Active Defense Methods for Mitigating Penetration Attacks on Power Grid Buffer Networks | 2024 | 10.1007/978-981-97-2757-5_53 | R2 | T1 | abstract (fetch tool's summary) | deceptive actions (state inversion, flipped rewards) against reinforcement-learning penetration of power-grid buffer networks; no decoy placement | #1009 |
| 612 | Intent-Driven Insider Threat Detection in Intelligence Analyses | 2008 | — | Zhan et al., ref. 35 | X | title | an insider-threat study; no deception asset in the title | — |
| 613 | Journal of Network and Computer Applications | — | — | R4 | X | title | a journal record, not a work | — |
| 614 | Load Redistribution Attacks Against Smart Grids—Models, Impacts, and Defense: A Review | 2024 | 10.1109/tii.2024.3393005 | Zhan et al., ref. 43 | X | title | load-redistribution or false-data attacks on a power system; no deception asset in the title | — |
| 615 | Long-Distance Trust-Free Quantum Key Distribution Networks | 2014 | — | R2 | X | title | decoy states in quantum key distribution | — |
| 616 | Marginal Loss Calculations for the DCOPF | 2017 | — | Zhan et al., ref. 12 | X | title | power-system modelling or analysis; no deception asset in the title | — |
| 617 | Matpower: A Matlab Power System Simulation Package [Online] | 2015 | — | Zhan et al., ref. 56 | X | title | power-system modelling or analysis; no deception asset in the title | — |
| 618 | Minimizing Risk of Load Redistribution Attacks on Electric Grids in the Presence of Insider Threats | 2026 | 10.1111/risa.70336 | R1+R2+R4+R5 | T2 | abstract (from the Wiley page the user saved, 16 November 2026; the full text is not free) | a stochastic optimisation (trilevel MINLP, reduced to a single-level MILP, with CVaR) that decides which critical grid components to protect and where to deploy honeypots against insider-enabled load-redistribution attacks, under a protection budget, on the IEEE 14-bus system; no zones or conduits, no ATT&CK paths or interception stage, and no random or centrality baseline in the abstract. Found only through the widened words: its abstract says 'smart power grids', which block O's 'smart grid' does not match | #1000 |
| 619 | Modeling Coupled Nonlinear Multilayered Dynamics: Cyber Attack and Disruption of an Electric Grid | 2021 | 10.1155/2021/5584123 | R2+R5 | X | title | attack-propagation dynamics in an electric grid; no deception asset in the title | — |
| 620 | Modeling Load Redistribution Attacks in Power Systems | 2011 | 10.1109/tsg.2011.2123925 | Zhan et al., ref. 52 | X | title | load-redistribution or false-data attacks on a power system; no deception asset in the title | — |
| 621 | Multiattribute SCADA-Specific Intrusion Detection System for Power Networks | 2014 | 10.1109/tpwrd.2014.2300099 | Zhan et al., ref. 49 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 622 | Optimal Power Grid Protection Through a Defender–Attacker–Defender Model | 2014 | 10.1016/j.ress.2013.08.003 | Zhan et al., ref. 51 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 623 | Optimization of Conditional Value-at-Risk | 2000 | 10.21314/jor.2000.038 | Zhan et al., ref. 31 | X | title | a risk measure or optimisation method; no deception asset in the title | — |
| 624 | Optimization With Multivariate Conditional Value-at-Risk Constraints | 2013 | 10.1287/opre.2013.1186 | Zhan et al., ref. 28 | X | title | a risk measure or optimisation method; no deception asset in the title | — |
| 625 | Optimizing re-evaluation of malware distribution networks | 2011 | 10.14288/1.0072288 | R2+R5 | X | title | re-evaluating malware distribution networks; 'distribution network' in the malware sense | — |
| 626 | Parameter optimization and real-time calibration of a measurement-device-independent quantum key distribution network based on a back propagation artificial neural network | 2019 | 10.1364/josab.36.000b92 | R1+R2+R4+R5 | X | title | decoy states in quantum key distribution | — |
| 627 | Power System Reliability Evaluation Considering Load Redistribution Attacks | 2016 | — | Zhan et al., ref. 45 | X | title | load-redistribution or false-data attacks on a power system; no deception asset in the title | — |
| 628 | Preliminary System Dynamics Maps of the Insider Cyber-Threat Problem | 2004 | — | Zhan et al., ref. 3 | X | title | an insider-threat study; no deception asset in the title | — |
| 629 | Protection of Energy Network Infrastructures Applying a Dynamic Topology Virtualization | 2022 | 10.3390/en15114123 | R1+R4 | T1 | full text (fetch tool's summary) | rule-based switching of a hybrid honeypot's virtual topology in energy networks, from an attack-development graph and MITRE ATT&CK techniques, under resource limits; no objective function, criticality or zones | #1010 |
| 630 | Quasi Second-Order Stochastic Dominance Model for Balancing Wildfire Risks and Power Outages Due to Proactive Public Safety De-Energizations | 2023 | 10.1109/tpwrs.2023.3289788 | Zhan et al., ref. 41 | X | title | a risk measure or optimisation method; no deception asset in the title | — |
| 631 | Risk Assessment of Catastrophic Failures in Electric Power Systems | 2004 | 10.1504/ijcis.2004.003795 | Zhan et al., ref. 26 | X | title | power-system modelling or analysis; no deception asset in the title | — |
| 632 | Security Constrained Economic Dispatch Based on Shift Factor Adaptive Calculation | 2023 | — | Zhan et al., ref. 17 | X | title | power-system modelling or analysis; no deception asset in the title | — |
| 633 | Security Management in Content Distribution Networks: a delay-variance reduction approach for content mirror site placement | 2023 | 10.1109/comsnets56262.2023.10041417 | R1+R2+R4+R5 | X | title | placement of CDN mirror sites; 'distribution network' in the content-delivery sense, and no deception asset in the title | — |
| 634 | State of the Art Authentication, Access Control, and Secure Integration in Smart Grid | 2015 | 10.3390/en81011883 | Zhan et al., ref. 37 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 635 | Survey and Management of Interior Least Terns in Indiana – 2014 | 2014 | — | R1 | X | title | bird decoys in a wildlife survey | — |
| 636 | Surveying cyber-physical honeynets: Realism, attractiveness, and emerging applications | 2026 | 10.1016/j.jisa.2026.104698 | R1 | T1 | title | a survey of cyber-physical honeynets | #1011 |
| 637 | The 2015 Ukraine Blackout: Implications for False Data Injection Attacks | 2017 | 10.1109/tpwrs.2016.2631891 | Zhan et al., ref. 20 | X | title | load-redistribution or false-data attacks on a power system; no deception asset in the title | — |
| 638 | The Insider Attack Problem Nature and Scope | 2008 | 10.1007/978-0-387-77322-3_1 | Zhan et al., ref. 7 | X | title | an insider-threat study; no deception asset in the title | — |
| 639 | The Multi-Role NATO-Interoperable Light Weight Torpedo for the 21st Century | 2004 | 10.11610/isij.1306 | R4 | X | title | naval decoys | — |
| 640 | Trilevel Optimization in Power Network Defense | 2007 | 10.1109/tsmcc.2007.897487 | Zhan et al., ref. 50 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |
| 641 | Ukraine Power Grid Cyberattack and US Susceptibility: Cybersecurity Implications of Smart Grid Advancements in the US | 2016 | — | Zhan et al., ref. 38 | X | title | a security study, survey or incident report; no deception asset in the title | — |
| 642 | Understanding Insider Threat: A Framework for Characterising Attacks | 2014 | — | Zhan et al., ref. 29 | X | title | an insider-threat study; no deception asset in the title | — |
| 643 | Using Graph Models to Analyze the Vulnerability of Electric Power Networks | 2006 | 10.1111/j.1539-6924.2006.00791.x | Zhan et al., ref. 15 | X | title | power-system modelling or analysis; no deception asset in the title | — |
| 644 | Worst-Case Conditional Value-at-Risk With Application to Robust Portfolio Management | 2009 | 10.1287/opre.1080.0684 | Zhan et al., ref. 55 | X | title | a risk measure or optimisation method; no deception asset in the title | — |
| 645 | Worst-Case Interdiction Analysis of Large-Scale Electric Power Grids | 2009 | 10.1109/tpwrs.2008.2004825 | Zhan et al., ref. 34 | X | title | grid defence or interdiction planning that protects components; no decoy in the title | — |

### 18.3 The T2 work and its citation rounds

**Zhan, Mehrani, Xie & Dehghanian (2026)**, *Risk Analysis*, record 618 (`sources.md` #1000). A stochastic trilevel model, reduced to a single-level MILP with CVaR, decides which grid components to protect and where to deploy honeypots against insider-enabled load-redistribution attacks, under a protection budget, on the IEEE 14-bus system. Ruled T2 by the user on 16 November 2026. So far as its abstract shows, it has no zones or conduits, no ATT&CK-grounded paths or interception stage, and no random or centrality baseline. The full text is not free (D35's rule), so the tier rests on the abstract. The first runs missed it because its abstract says "smart power grids", which block O's phrase "smart grid" does not match.

*Backward round* (`sources.md` #998): 56 references. 1 was returned by the first runs (Belqruch & Maach 2019); 55 are records in 563–645: related (T1) 3 (Liu & Wang 2020, Spitzner 2003, Yamin et al. 2020) and excluded 52 (the table above gives each one's reason). *A correction:* Claude's first pass marked Spitzner (2003) as returned by the first runs; it is in neither records 1–562 nor `sources.md`. *Forward round:* OpenAlex lists 0 works citing it (16 November 2026).

### 18.4 Patents (run P1c)

About 145 results on two pages, all parsed. 43 were in the patent arm already (related (T1) 36, excluded 6, T2 1: CN 122339846 A) and 102 are new: related (T1) 32, excluded 70, T2 0, T3 0.

**First round (Claude, 16 November 2026).** The title rule of §14.2, with the result-list snippets: 7 pages were opened, chosen by eye from titles and snippets that suggested a deployment, configuration or defence decision, or a deception method in a power setting; 4 numbers are the other publication of a document screened before and take its tier; the rest were called on their titles and snippets. The user ruled CN 117439810 A and CN 111756687 B related (T1), on Claude's leans, and confirmed the exclusion of CN 122293365 A, whose title carries a deception word and a power-grid word (§9).

**Second round (Claude, 16 November 2026, after the first draft of D38).** The first round fell short of the first arm's standard. There, round 3 opened every excluded title of run P1n that named a cyber, industrial or power subject, and the arm's only T2 at that time had come from such a neutral title (§14.4). P1c is P1n's counterpart. 31 more pages were opened:
- 18 titles the rule had excluded that name a cyber, industrial or power subject. Left out were titles naming an animal lure or trap, and titles showing a sense that earlier readings had confirmed as excluded: quantum key distribution (two such patents for power networks stayed excluded in round 3) and drones or counter-drone devices (three counter-drone devices stayed excluded in round 3);
- 13 related titles that suggest a strategy, a configuration, an attack path or a power-sector honeypot, among them CN 118484310 A, whose title carries a placement word (rule 4 flags such titles).

All 13 related stay related. Of the 18 excluded, 5 proved related (T1) and 13 stayed excluded: 5 quantum-key-distribution decoy states, 3 optimisation algorithms named after honeypots, a data-privacy decoy, a DHCP spoofer, a smart card's lure circuit, a counter-drone decoy and one page with no deception term. None decides positions by an objective. The nearest is CN 118484310 A, which assigns honeypots to host nodes by load, the kind ruled T1 in CN 117439810 A. Pages that returned a server error were read at another address, as each entry says.

**Pages read**

| Publication | Title | Round | The title rule's call | Tier | Reason | `sources.md` |
|---|---|---|---|---|---|---|
| CN 111756687 B | Defense measure configuration method and system for coping with network attack | 1 | — | T1 | maximises a fused survivability score under a total budget and per-service ceilings by allocating counts of six defence measures, honeypots and camouflage components among them, per service of a power-grid information system, with service-importance weights; general defence allocation, not decoy positions | #1012 |
| CN 117439810 A | Honeynet node deployment method, system and storage medium for power Internet … | 1 | — | T1 | assigns honeynet trap nodes to hosting devices by an iterative probabilistic search that minimises the honeynet's communication cost under resource limits; where the honeynet runs, not where decoys meet attackers; no criticality, zones, attack paths or baselines | #1013 |
| CN 118540112 A | Honeypot deployment method, system, device and storage medium for power system | 1 | — | T1 | predicts a honeypot count per asset type (LSTM with attention) and adjusts it against an expected attack count; importance weights and an availability cap; counts, not positions | #1014 |
| CN 118784334 B | Method, system, equipment and medium for trapping network attack behaviors in … | 1 | — | T1 | a virtual honeynet mirroring a power information system, with honey baits scored by data sensitivity and vulnerability harm; no rule for where traps go | #1015 |
| CN 121530655 A | A Risk Decision Engine and Method for Distributed Power Systems | 1 | — | T1 | a risk decision engine for distributed power systems in which a honeypot is one response action at the isolation level; no placement | #1016 |
| CN 122226502 A | Dynamic spoofing decoy customization method, system, equipment and medium based … | 1 | — | T1 | generates decoy content from a power-business knowledge graph after attributing an attack, and places each decoy on the accessible path of the host under attack; no placement objective, budget, zones or ATT&CK | #1017 |
| CN 122293365 A | A Power Grid Deceptive Topology Search and Defense Method Based on Adaptive … | 1 | — | X | a genetic algorithm choosing which grid nodes and lines get concealed construction so that a physical attacker sees a deceptive topology; physical grid planning against physical attacks, not cyber deception | #1018 |
| CN 100409217 C | Internet protocol address allocation device and method | 2 | excluded on a title alone | X | one public IP address shared by all hosts of a local network through a DHCP server emulator (a "spoofer"); networking, with no decoy or honeypot | #1019 |
| CN 109218292 A | A kind of electric power networks security boundary composite defense method … | 2 | related on a title and list snippet | T1 | border defence of a power network by pseudo-random rotation of node addresses, ports and protocols, with a decoy module that generates false messages; no placement decision, objective or budget | #1020 |
| CN 113676472 B | Expandable honey pot tracing and countering method in power industry | 2 | related on a title and list snippet | T1 | honeypot templates carrying a traceability interface and an anti-Trojan payload, to trace and counter attackers on power information systems; deployed on "real attack and intrusion links" with no rule for where or how many | #1021 |
| CN 115174218 A | Method for carrying out power grid safety protection based on high-simulation … | 2 | related on a title and list snippet | T1 | high-simulation virtual honeypots (Docker) on station-end hosts of a power monitoring network, reporting through node control centres to a management centre; deployment fixed; no placement method, experiments or baselines | #1022 |
| CN 115314193 A | Detector defect analysis method and system, storage medium and computing device | 2 | excluded on a title alone | X | single-photon detector defects in quantum key distribution; "decoy" and "trap" are quantum states | #1023 |
| CN 115510499 B | Power distribution network scheduling decision model outsourcing calculation … | 2 | excluded on a title alone | X | outsourced computation of a distribution-network scheduling model; its "decoy-type" protection is a desensitised virtual network sent to cloud providers, a data-privacy device, not a deception asset in a network | #1024 |
| CN 115618710 B | A probabilistic wind power prediction method and system based on GAN | 2 | excluded on a title alone | X | probabilistic wind-power forecasting with a Wasserstein GAN; no deception term on the page | #1025 |
| CN 115694965 A | Network security close network system for power industry | 2 | related on a title and list snippet | T1 | a power-industry deception network: lures placed on the internet, a simulated range, internal decoy systems (office, mail and marketing baits) and honeypots in a fixed architecture of five security zones, which are the power sector's own zones, not IEC 62443 zones and conduits; no placement method, experiments or baselines | #1026 |
| CN 116471064 A | Network safety protection system, method and device based on active defense … | 2 | related on a title and list snippet | T1 | an active-defence device in a power grid's management network that builds clusters of application-level decoy nodes and picks a dynamic defence strategy by security-risk scores; the device sits at a fixed point (between a core switch and a layer-2 switch); no placement decision | #1027 |
| CN 117808174 B | Microgrid operation optimization method and system based on reinforcement … | 2 | excluded on a title alone | T1 | reinforcement-learning microgrid operation under network attack, with a honeypot server built beside the real server and a game-theoretic comparison of the benefit with and without it; the honeypot type is chosen by a manual procedure; no placement decision | #1028 |
| CN 117908439 A | Millions of kilowatt-level nuclear power station safety system, method, … | 2 | excluded on a title alone | T1 | a nuclear plant instrument-and-control safety system with identity-based access control in its field, process and operation units and a honeypot in the field control unit to detect attacks on field devices; its position is fixed and no method chooses it | #1029 |
| CN 118173101 B | A method for identifying external force damage risk based on voiceprint | 2 | excluded on a title alone | X | transformer external-damage risk from voiceprints; "honeypot" only as the name of an optimisation algorithm that selects features | #1030 |
| CN 118484310 A | Honeypot trapping resource deployment method and system | 2 | related on a title and list snippet | T1 | predicts each honeypot's CPU and memory load (an LSSVM tuned by a spectral optimiser) and assigns honeypots to Kubernetes nodes by a resource-compatibility score: which host runs a honeypot, not where decoys meet attackers, the kind the user ruled T1 in CN 117439810 A; no count, budget, criticality, zones, ATT&CK, experiments or baselines | #1031 |
| CN 119049195 A | Device and method for safety production space defense of intelligent power plant | 2 | excluded on a title alone | X | airspace defence of a thermal power plant against drones, kites and balloons; its "fixed point decoy" is a physical counter-drone measure | #1032 |
| CN 119272263 A | Quantum-resistant computing methods and systems for power information systems | 2 | excluded on a title alone | X | quantum-safe certificate services for a power information system; "decoy" only in the decoy BB84 protocol | #1033 |
| CN 119324807 A | Defense system for complex cooperative attack in power distribution network | 2 | related on a title and list snippet | T1 | a defence system against coordinated attacks on a distribution network whose attack-source location module uses honeypot technology; no placement decision | #1034 |
| CN 119544332 A | … , electronic device and storage medium for attack trapping of virtual power … | 2 | related on a title and list snippet | T1 | attack trapping in a virtual power plant network: on a probe's alarm a honeypot instance matching the device is created and bound to the probe, and simultaneous requests are ranked by device criticality and attack rate under a honeypot capacity limit; the honeypot nodes sit at fixed sites, so no positions are chosen | #1035 |
| CN 120185204 A | A distributed energy storage station monitoring system | 2 | excluded on a title alone | X | distributed energy-storage monitoring; "decoy" only in the decoy BB84 protocol | #1036 |
| CN 120257325 A | An endogenous safety collaborative protection method and system for a campus … | 2 | excluded on a title alone | T1 | endogenous security for a campus microgrid (tamper-proof storage, access control, decision fusion), in which starting a honeypot system that leads attack traffic into isolation is one listed response; no placement | #1037 |
| CN 120414882 A | A Kubernetes-based control method | 2 | related on a title and list snippet | T1 | a Kubernetes controller that suspends or hot-reloads honeypot ("trap") resources by predicted load and attack activity (regression cost models, a variable-order Markov model over a service graph, an LSTM for preheating); no node-placement algorithm, budget, criticality, zones, ATT&CK or experiments | #1038 |
| CN 120675799 A | Attack chain association analysis and tracing method based on RASP technology | 2 | related on a title and list snippet | T1 | RASP probes in a power business system's Java stack redirect attackers to a simulated honeypot, and browser fingerprints link attacker addresses into an attack chain; a fixed design; no placement | #1039 |
| CN 120768577 A | … and early warning system integrated into the browser of a nuclear power plant | 2 | excluded on a title alone | T1 | a browser plug-in that detects phishing sites for nuclear plant staff, trained on samples from public phishing databases and honeypot systems: honeypots as a data source, as CN 110222505 A (§14.4) | #1040 |
| CN 120782111 A | Electric power carbon emission intelligent analysis system based on double- … | 2 | excluded on a title alone | X | power carbon-emission analysis; "decoy" only in the decoy BB84 protocol of quantum key distribution | #1041 |
| CN 121349613 A | Micro-patch seamless deployment engine and resource scheduling methods, systems … | 2 | excluded on a title alone | T1 | a micro-patch hot-deployment engine for power-grid disaster-recovery systems (SCADA-EMS) that quarantines a suspect terminal into a honeypot VLAN by a fixed flow rule; no placement | #1042 |
| CN 121525918 A | A method and system for optimizing energy storage capacity based on flexible … | 2 | excluded on a title alone | X | energy-storage sizing for industrial grids; "honeypot" only as the name of an improved bio-inspired optimisation algorithm | #1043 |
| CN 121585389 A | A power information network security protection system and method based on … | 2 | related on a title and list snippet | T1 | power information network protection by distributed neural-network probes, with a deception module that plants forged documents and credentials as bait once reconnaissance is detected; no placement; asset value is used only in threat grading | #1044 |
| CN 121886480 A | Modeling and collaborative scheduling method for zero-carbon harbor green … | 2 | excluded on a title alone | X | zero-carbon port microgrid scheduling with a stingless-bee optimiser whose "honeypot construction stage" is a metaphor | #1045 |
| CN 122131827 A | Solar module angle control system and method for self-adaptive illumination … | 2 | excluded on a title alone | X | solar-module angle control; "decoy" only as the decoy-state method of quantum key distribution | #1046 |
| EP 1 374 160 A1 | Method for protecting a smart card | 2 | excluded on a title alone | X | a smart card powered from an internal accumulator during sensitive operations, with a "lure" circuit that masks its current consumption: a decoy inside a chip, as EP 3 418 937 A1 (§14.2) | #1047 |
| US 2013/0086635 A1 | System and method for communication in a network | 2 | related on a title and list snippet | T1 | secure configuration commands in a power distribution network, executed when a threshold number of command sites agree; honeypots appear only as an optional kind of host device; no placement | #1048 |
| US 2013/0086680 A1 | System and method for communication in a network | 2 | related on a title and list snippet | T1 | the setting of US 2013/0086635 A1, with configuration-command shadows combined at the host; honeypots only in passing | #1049 |

**Judged without opening the page (64)**

| Publication | Title | Tier | Judged on | Reason |
|---|---|---|---|---|
| CN 105282170 A | Information security offense and defense drill competition system for power … | T1 | title and snippet | an offence-and-defence drill system for power information security |
| CN 114978767 A | Centralized monitoring system based on multisource honeypots | T1 | title and snippet | centralised monitoring of multi-source honeypots |
| CN 118540166 A | A honeypot network security situation prediction method and system | T1 | title and snippet | honeypot-based security situation prediction |
| CN 119921973 A | Network security device management method based on generative big model and … | T1 | title and snippet | security-device management with a generative model for a power system; deception only in its text |
| CN 105552886 A | Smart Grid based intelligent trapping system | T1 | family member of one screened | the other publication of CN105552886B, screened as T1 |
| CN 115150175 A | … trapping technical method for independent network attack of power system | T1 | family member of one screened | the other publication of CN115150175B, screened as T1 |
| CN 115883169 B | … for Responding to Industrial Control Network Attack Packets Based on Honeypot … | T1 | family member of one screened | the other publication of CN115883169A, screened as T1 |
| CN 119276627 A | A network security deduction method, device, electronic device and storage … | T1 | family member of one screened | the other publication of CN119276627B, screened as T1 |
| CN 104965544 A | Tunnel project gateway infrared decoy system and manufacturing method thereof | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| CN 120871968 A | Remote primary-secondary unmanned aerial vehicle combat system and control … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| CN 121808565 A | Performance prediction method of passive true and false target identification … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| CN 122179053 A | Low-altitude unmanned aerial vehicle (UAV) all-domain monitoring and targeted … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| CN 122505099 A | Portable decoy trajectory simulation device for individual soldiers and its … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| CN 122607552 A | A composite unmanned aerial vehicle system based on distributed power and … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| CN 218410895 U | Fixed anti-unmanned aerial vehicle defense device suitable for power plant's … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| CN 222014469 U | A drone navigation decoy device | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| EP 0 706 024 A2 | Protecting device for an object and method to oprate a protecting device | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| JP 2016529462 A | decoy | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| RU 2764781 C1 | Method for tracking air target of "turbojet engine aircraft" class under … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| RU 2765145 C1 | Method for integrating information from a radar station and radar homing heads … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| US 10,457,391 B2 | Method and system for a small unmanned aerial system for delivering electronic … | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| US 2019/0252791 A1 | Inflatable Radar Decoy System and Method | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| US 7,028,947 B2 | Self-powered tethered decoy for heat-seeking transport aircraft missile defense | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| US 8,919,028 B2 | Moving decoy and method | X | title | a physical decoy, or a military, radar or drone subject; nothing cyber in the title |
| CN 107836425 A | A kind of dual-purpose killing device of mosquito | X | title | an animal lure, trap, replica or attractor |
| CN 121139299 A | A method and system for regulating animal activity paths in wind farms | X | title | an animal lure, trap, replica or attractor |
| CN 201499535 U | Sex pheromone power grid insect killer | X | title | an animal lure, trap, replica or attractor |
| FR 3031875 A1 | COMPLEX MOSQUITO TRAP FOR EXTERIOR SPACES | X | title | an animal lure, trap, replica or attractor |
| KR 10-0846193 B1 | Jellyfish Attractor | X | title | an animal lure, trap, replica or attractor |
| TW I246885 B | Microbe-mediated method and apparatus for attracting mosquitoes | X | title | an animal lure, trap, replica or attractor |
| US 2020/0329695 A1 | Migratory bird decoy and migratory bird decoy wing assembly | X | title | an animal lure, trap, replica or attractor |
| US 6,675,522 B2 | Cable-driven animated bird replica apparatus | X | title | an animal lure, trap, replica or attractor |
| CN 122436991 A | Directional drainage principle of field energy echo | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| CN 221463805 U | Multifunctional landscape lamp | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| FR 2741704 A1 | AIR CONDITIONING SYSTEM COMPRISING A HEAT PUMP AND AN ADDITIONAL HEATING MEANS | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| JP S59118366 A | … type or arch type working system, through which mechanism unit can be selected , … | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| JP S59501448 A | Irradiation device | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| KR 10-2016-0034576 A | Mobile terminal | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| TW 201226394 A | Electron transport material and organic electroluminescent device using the … | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| US 2007/0225993 A1 | Method for Civilly-Catastrophic Event-Based Transport Service and Vehicles … | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| US 2007/0233506 A1 | Privately Managed Entertainment and Recreation Supplies Provisioning Method | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| US 2010/0279649 A1 | Personal Security and Law Enforcement Evidence Documenting and Criminal … | X | title | no deception asset in the title, and no cyber-security, industrial-control or power subject |
| CN 102820968 A | … control signals between transformer stations based on quantum key distribution | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 103491531 A | Method for using quantum keys to improve safety of electric power information … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 103595468 B | A kind of quantum signal method of testing of high ammonia syrings | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 106209361 B | A secure star quantum key distribution network without trusted relays | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 108111304 B | Multi-party measuring equipment irrelevant quantum key distribution network … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 108111305 B | Multi-type quantum terminal compatible converged network access system and … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 109450628 B | A plug-and-play measurement device-independent quantum key distribution network … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 111934784 A | A Satellite-Earth Integrated Quantum Key Distribution System Applicable to … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 112448814 A | Asymmetric double-field quantum key distribution method facing power grid wide … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 114221765 B | Quantum key distribution method for fusion of QKD network and classical … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 114448620 B | Business path selection method and related equipment for multi-protocol quantum … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 114765535 A | Intelligent data operation and maintenance system of quantum key distribution … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 114765536 B | Operation and maintenance method and device of quantum key distribution network | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 116318682 B | Channel disturbance resistant reconfigurable quantum key distribution network | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 117318806 A | Quantum key distribution system and interferometer deviation self-compensation … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 118764187 A | A plug-and-play time-phase coded quantum key distribution network | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 119449281 A | A quantum key distribution network based on space division multiplexing | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 119995848 B | Quantum communication-based power grid operator security authentication method … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 120729558 A | Financial-grade secure transmission system based on quantum cryptography … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| CN 207625571 U | The converged network access system of polymorphic type quantum terminal … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| US 11,888,978 B1 | Systems and methods for measurement-device-independent quantum key distribution | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |
| US 2022/0029729 A1 | Qtth system based on multicore optical fiber mode division multiplexing and … | X | title | quantum key distribution or other quantum communication, where "decoy" means a decoy state |

Already in the patent arm: CN 105306487 A (T1), CN 107566390 B (T1), CN 109167796 B (T1), CN 109889488 A (T1), CN 110784476 A (T1), CN 113285926 B (T1), CN 114401108 B (T1), CN 114462023 A (T1), CN 114528546 A (T1), CN 115150140 A (T1), CN 115174227 A (T1), CN 115914014 B (X), CN 116389016 A (T1), CN 116405258 B (T1), CN 116614256 B (T1), CN 116781412 A (T1), CN 117478395 A (T1), CN 117560175 A (T1), CN 117857086 A (T1), CN 118432759 A (X), CN 118631442 A (X), CN 119254537 A (T1), CN 119675929 B (T1), CN 119945718 A (T1), CN 120433958 A (T1), CN 120474762 A (T1), CN 120498746 A (T1), CN 120638394 A (X), CN 120675782 A (T1), CN 120768630 A (T1), CN 120811596 B (X), CN 120880810 A (T1), CN 120934858 A (T1), CN 121000455 A (T1), CN 121567381 A (T1), CN 121603304 B (T1), CN 121690744 A (T1), CN 121750505 A (T1), CN 121923884 A (T1), CN 122316652 A (T1), CN 122339846 A (T2), CN 122437728 A (T1), WO 2025/210623 A2 (X).

### 18.5 What it shows

- *The gap was real.* One work that narrows the claim, Zhan et al., was returned only through the new words.
- *A28 survives as worded.* Budgeted, formally optimised decoy placement in a power grid now has two papers, Dong et al. and Zhan et al.; D36 already ruled out any claim to be first there. Nothing found uses IEC 62443 zones and conduits as numeric inputs, scores an interception stage along ATT&CK-grounded paths, or validates against random and centrality baselines.
- *The title rule's exclusions are again shown unsafe, without changing a tier that matters:* 5 of the 18 excluded titles opened proved related, and none proved T2.
- *No new baseline* (§11.6): Zhan et al. model a different threat, and only their abstract is free.
