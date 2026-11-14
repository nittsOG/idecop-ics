# A17 structured search: the screening record

The record of how the 375 unique records from A17's ten runs were screened, under `01-search-protocol.md` §9–§11, and what each became. Decisions: D35. Runs: `sources.md` #405–#415; deduplication and the title stage: #416.

- **Category:** Research. **Tier:** 💾 Offline, kept in the repository on your computer, not in Project Knowledge.
- **Depends on:** `01-search-protocol.md`, `sources.md` #405–#416, D34.
- **Feeds into:** D35; `sources.md` #417–#612; the Literature Review chapter and its search appendix (Phase E); A28's wording.
- **Record numbers** (1–375) are this file's own, assigned in alphabetical order of title at deduplication. They are not `sources.md` numbers, which always carry `#`.
- **Status:** complete for the main search. The recency check, IEEE Xplore, TechRxiv, forward citations and the patent arm (§3, §7, §8) are added here as they run.

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
- **Two titles in other scripts** were screened by translation: record 374 (Greek), related by title; and record 375 (Ukrainian), excluded.
- **"Already logged" was undercounted** at first. The title pass found 5; a later check found at least 24 (#416).

## 11. Still to run (A17, A29)

- **Recency check:** arXiv, with S1 and S2 (§3).
- **IEEE Xplore's public search:** S1 and S4. Its pages open in the user's browser.
- **TechRxiv check** (§3).
- **Forward citations on the eight anchors (§7).** Under §7.4 these also include one backward and one forward round for each T2 work. Three candidates from Park & Dagher's reference list are already queued (#611).
- **The patent arm (§8, A29).** One new lead: #612.
- **The update re-run** of S1 and the citation lists, within a month of submission (§10).
