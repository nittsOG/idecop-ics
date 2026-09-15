# Front Matter and Pre-Template Content Pack

Content that the institutional template will demand but that does not depend on the template's format. Written now so that template arrival becomes a formatting exercise rather than a writing one.

Everything here is drafted to be pasted and adjusted, not to be used verbatim without reading.

---

## 1. Abstract — three lengths

Templates vary in what they allow. All three versions state the same claims; only the compression differs.

### 1.1 Short form (~150 words)

> Cyber deception is an established defensive technique for industrial control systems, but existing work concentrates almost entirely on the fidelity of the decoy rather than on where it should be placed. In current practice, placement is decided manually or by architectural convention. This work formulates deception placement in OT/ICS networks as a constrained optimisation problem. The network is modelled as a directed graph in which IEC 62443 zones, conduits, Purdue levels and asset types are explicit attributes, and attack scenarios are expressed as sequences of MITRE ATT&CK for ICS techniques. A composite objective combining attack-path coverage, earliness of interception, criticality-weighted protection, operational risk and deployment cost is maximised subject to a decoy budget, using a greedy method validated against an exact solver. A local language model explains the resulting placement without participating in the decision. The method is evaluated against random and centrality-based baselines on a multi-zone virtualised testbed.

### 1.2 Standard form (~300 words)

> Operational technology networks controlling physical industrial processes face detection constraints that conventional security tooling addresses poorly: endpoint agents cannot be deployed on programmable logic controllers, signature-based detection struggles with proprietary industrial protocols, and availability requirements restrict active scanning. Cyber deception offers a structurally different mechanism, since an asset with no legitimate function generates high-confidence evidence of intrusion on any interaction.
>
> The technology for constructing convincing industrial decoys is mature. The complementary question of where such decoys should be positioned within a network architecture remains, in both research and practice, answered manually, by template, or by architectural convention. Placement nevertheless determines value: a decoy that no attacker reaches detects nothing, one reached late detects only after damage, and one reachable by legitimate traffic generates false alarms that carry real operational cost.
>
> This work formulates deception placement for multi-zone OT/ICS architectures as a constrained optimisation problem. The network is represented as a directed graph whose nodes carry IEC 62443 zone membership, Purdue level and asset type, and whose conduits are the edge subsets crossing zone boundaries. Asset criticality combines the IEC 62443-3-3 Security Level vector with weighted network centrality and operational damage share. Attack scenarios are expressed as ordered sequences of verified MITRE ATT&CK for ICS techniques. Candidate locations are derived through a four-criterion plausibility rubric adapted to the ICS matrix, followed by a detectability assessment. A composite objective spanning attack-path coverage, earliness of interception, criticality-weighted protection, operational risk and deployment cost is maximised under a decoy budget using a greedy algorithm, validated against an exact mixed-integer formulation. A local language model generates analyst-facing explanations without altering the placement.
>
> A literature review across ten structured iterations, cataloguing 322 sources, establishes that formal placement optimisation is mature in enterprise IT but effectively absent for multi-zone OT architectures. A working prototype is evaluated against random and centrality baselines on an eleven-node, four-zone virtualised testbed.

### 1.3 Keywords

Industrial control systems; operational technology security; cyber deception; honeypot placement; IEC 62443; MITRE ATT&CK for ICS; combinatorial optimisation; attack path analysis; SCADA security; explainable security

*(Most templates ask for five to eight. A defensible subset: cyber deception, industrial control systems, IEC 62443, placement optimisation, MITRE ATT&CK for ICS, SCADA security.)*

---

## 2. List of Abbreviations

Extracted from the project glossary. Expand each on first use in every chapter regardless of this list.

| Abbreviation | Expansion |
|---|---|
| API | Application Programming Interface |
| ATT&CK | Adversarial Tactics, Techniques and Common Knowledge |
| CP-SAT | Constraint Programming — Satisfiability (solver) |
| CVSS | Common Vulnerability Scoring System |
| DMZ | Demilitarised Zone |
| DQN | Deep Q-Network |
| EPRI | Electric Power Research Institute |
| FR | Foundational Requirement (IEC 62443) |
| GNN | Graph Neural Network |
| GOOSE | Generic Object Oriented Substation Event |
| GRC | Governance, Risk and Compliance |
| HMI | Human Machine Interface |
| HTTP | Hypertext Transfer Protocol |
| ICS | Industrial Control System |
| IEC | International Electrotechnical Commission |
| IED | Intelligent Electronic Device |
| ILP | Integer Linear Programming |
| IIoT | Industrial Internet of Things |
| IT | Information Technology |
| JSON | JavaScript Object Notation |
| LDRD | Laboratory Directed Research and Development |
| LLM | Large Language Model |
| MILP | Mixed-Integer Linear Programming |
| NIST | National Institute of Standards and Technology |
| NP | Nondeterministic Polynomial time |
| OPC UA | Open Platform Communications Unified Architecture |
| OT | Operational Technology |
| PDDL | Planning Domain Definition Language |
| PL | Purdue Level |
| PLC | Programmable Logic Controller |
| POSG | Partially Observable Stochastic Game |
| REST | Representational State Transfer |
| RL | Reinforcement Learning |
| RTU | Remote Terminal Unit |
| SCADA | Supervisory Control and Data Acquisition |
| SIEM | Security Information and Event Management |
| SIL | Safety Integrity Level |
| SL | Security Level (IEC 62443) |
| SOAR | Security Orchestration, Automation and Response |
| SOC | Security Operations Centre |
| SQL | Structured Query Language |
| TTL | Time To Live |
| VLAN | Virtual Local Area Network |
| VM | Virtual Machine |
| VRAM | Video Random Access Memory |

---

## 3. Planned List of Figures

Defined now so the figures can be produced before the template dictates their captioning. Numbering will change if chapter structure shifts.

| Figure | Title | Content | Source material |
|---|---|---|---|
| 1.1 | Purdue Enterprise Reference Architecture | Standard layered ICS model, levels 0–5 | Standard reference; redraw, do not copy |
| 1.2 | Conceptual pipeline | Architecture → model → paths → candidates → optimisation → explanation | `01-original-brief.md` §5 |
| 2.1 | Research landscape | Two-by-two: domain against generation/placement | TA-1 §3.1 |
| 2.2 | Literature review process | Ten iterations, source counts, shortlisting | `sources.md` |
| 3.1 | System architecture | Five components and their interfaces | `02-system-flow.md` §2 |
| 3.2 | Testbed zone and conduit structure | Four zones, eleven nodes, conduits marked | `testbed-architecture.md` |
| 3.3 | Network model G | Directed graph with zone colouring | Generated from the live graph model |
| 3.4 | Attack paths overlaid on the topology | P1, P2, P3 traced across the graph | `threat-attack-model.md` |
| 3.5 | Candidate location filtering | Two-stage filter, assets surviving each stage | `formal-problem-definition.md` §4 |
| 3.6 | Objective function components | Five terms, signs, what each measures | `formal-problem-definition.md` §5 |
| 3.7 | Greedy algorithm flow | Marginal gain loop with early stopping | `02-optimization-formulation.md` |
| 3.8 | AI decide/explain separation | Where each AI component sits relative to the decision | `02-ai-role.md` |
| 4.1 | Module structure | Directory and dependency layout | `02-system-flow.md` §2 |
| 4.2 | Database entity relationships | Ten tables and their keys | `data/schema.sql` |
| 4.3 | Optimisation run sequence | Request through to stored result | `02-system-flow.md` §5 |
| 4.4 | Plausibility review screen | Screenshot | Running prototype |
| 4.5 | Single-run dashboard | Screenshot | Running prototype |
| 4.6 | Sensitivity sweep view | Screenshot | Pending build |
| 5.1 | Method comparison | Composite score by method | Phase D |
| 5.2 | Metric breakdown by method | Grouped comparison across all five terms | Phase D |
| 5.3 | Coverage against earliness | The tradeoff, across weight configurations | Phase D |
| 5.4 | Sensitivity sweep | Selected placement as weights vary | Phase D |
| 5.5 | Computation time by method | Wall-clock comparison | Phase D |

**Twenty-three figures.** Eight of them (3.3, 4.4, 4.5, 4.6, 5.1–5.5) are generated from the running system rather than drawn, which is worth noting because generated figures require the system to be in a presentable state, not merely working.

---

## 4. Planned List of Tables

| Table | Title | Source |
|---|---|---|
| 2.1 | Comparative summary of reviewed literature | TA-1 §2.3 |
| 3.1 | Zone and asset assignment | `testbed-architecture.md` |
| 3.2 | Attack path P1 — step sequence with technique IDs | `threat-attack-model.md` |
| 3.3 | Attack path P2 — step sequence with technique IDs | `threat-attack-model.md` |
| 3.4 | Attack path P3 — step sequence with technique IDs | `threat-attack-model.md` |
| 3.5 | Notation summary | `00-glossary.md` §6 |
| 3.6 | Plausibility rubric criteria | `formal-problem-definition.md` §4 |
| 3.7 | Computed criticality scores by asset | Generated |
| 3.8 | Candidate locations after filtering | Generated |
| 4.1 | Technology stack | `01-original-brief.md` §8 |
| 4.2 | Database schema summary | `data/schema.sql` |
| 4.3 | API endpoint reference | `src/api/main.py` |
| 5.1 | Experimental configuration | Phase D |
| 5.2 | Comparative results across methods | Phase D |
| 5.3 | Sensitivity sweep results | Phase D |
| 5.4 | Optimality gap, greedy against exact | Phase D |

---

## 5. Contributions statement

For §1.7 and, in compressed form, for §6.1. Stated at defensible strength.

1. A formal specification of deception placement in multi-zone OT/ICS architectures as a constrained optimisation problem, in which IEC 62443 zone and conduit structure functions as a numeric input to the objective rather than as architectural annotation.
2. An asset criticality measure combining the IEC 62443-3-3 Security Level vector with weighted network centrality and operational damage share, drawing on two independently sourced methods rather than one.
3. Adaptation of an existing decoy-feasibility rubric, previously applied only to the Enterprise ATT&CK matrix, to the ATT&CK for ICS matrix, combined with a detectability filter to produce the candidate location set.
4. A working prototype implementing the graph model, four placement methods, a REST interface and an analyst-facing web interface, evaluated on a representative multi-zone testbed.
5. An empirical comparison of the proposed method against random and centrality-based baselines across a parametric sweep of objective weights.
6. Demonstration that explanation can be added to a security decision procedure without compromising its determinism, by confining the language model to interpreting output it cannot alter.

---

## 6. Declaration and acknowledgement — drafting notes

Both are institution-specific in wording and must follow the template exactly. Do not draft final text now; the template will supply it. Prepare only the variable content:

- Full name as registered, enrolment number, programme, department, institution
- Guide's full name, designation and department
- Any co-guide or external supervisor
- Month and year of submission
- For the acknowledgement: guide, department, any lab or facility access used, institutional library access if granted, and family. Keep it brief and specific; a long acknowledgement reads as padding.

---

## 7. What still cannot be prepared in advance

Recorded so the gap is visible:

- Certificate and declaration wording — template-supplied
- Table of contents — generated after assembly
- Page numbering scheme — template-dependent
- Figure and table caption placement — template-dependent
- Whether references appear per chapter or once at the end
- Abstract word limit, if enforced
- Any required keyword taxonomy or classification codes
