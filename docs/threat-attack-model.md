# Threat and Attack Model — Attack Path Set P

Formalizes Section 3 of `formal-problem-definition.md`. Each path is a sequence of (asset, tactic, technique) steps, grounded in MITRE ATT&CK IDs verified directly against attack.mitre.org and cross-checked against secondary analyses of the named incidents — not invented from memory. Asset types (`type(v)`) reference the network model in Section 1 of the formal problem definition.

## P1 — Stuxnet-class: engineering-workflow-mediated physical sabotage

Models a targeted attacker who enters via the engineering workflow rather than the network perimeter, and causes physical damage while hiding it from operators.

| Step | Asset (`v ∈ V`) | Tactic | Technique | Notes |
|---|---|---|---|---|
| 1 | Engineering Workstation | Initial Access | T1091 (Enterprise) — Replication Through Removable Media, or T1195.002 — Supply Chain Compromise: Software Supply Chain | Stuxnet's actual vector was infected Step7 project files shared between engineers, plus USB propagation |
| 2 | Engineering Workstation | Execution / Privilege Escalation | T1203 — Exploitation for Client Execution; T1068 — Exploitation for Privilege Escalation | Both Enterprise-matrix techniques — this is the "IT conduit" portion of the path, before it reaches ICS-specific behavior |
| 3 | Engineering Workstation → PLC | Lateral Movement | Program download / engineering-software transfer to PLC | The IT/OT boundary crossing — the step your candidate-location filter (Section 4 of the formal problem definition) most needs to evaluate for plausibility |
| 4 | PLC | Impair Process Control | **T0836 — Modify Parameter** | Verified: attack.mitre.org/techniques/T0836/ — explicitly cites the Stuxnet Dossier as a procedure example |
| 5 | HMI | Inhibit Response Function | **T0832 — Manipulation of View** | Verified: attack.mitre.org/techniques/T0832/ — explicitly cites Langner's "To Kill a Centrifuge" analysis of Stuxnet |
| 6 | PLC (process) | Impact | Process degradation, no operator-visible alarm | The defining Stuxnet characteristic: physical damage while telemetry reports normal operation |

## P2 — Industroyer2-class: protocol-specific direct grid impact

Models a less stealthy, more direct attack that trades subtlety for speed — relevant because it stresses early detection differently than P1 does.

| Step | Asset (`v ∈ V`) | Tactic | Technique | Notes |
|---|---|---|---|---|
| 1 | OT DMZ / Jump Server | Initial Access | Network-perimeter entry | Industroyer2 is Software S1072 in MITRE's database — confirmed to communicate over IEC-104 specifically |
| 2 | Jump Server → Control LAN | Lateral Movement | IT-to-OT pivot | |
| 3 | Control LAN → PLC/RTU | Execution | Protocol-specific module (IEC-104) | Matches Industroyer2's confirmed design: a static, compiled payload built to speak IEC-104 to substation equipment |
| 4 | PLC/RTU | Impair Process Control | **T0836 — Modify Parameter**; **T0806 — Brute Force I/O** | Both verified against attack.mitre.org, both explicitly cited in the Industroyer2/INCONTROLLER technical analyses referenced on their MITRE pages |
| 5 | PLC/RTU (process) | Impact | Circuit-breaker toggling, service disconnection | The documented real-world effect: rapid open-close-open breaker commands |

## P3 — Reconnaissance-only: the early-detection stress test

Deliberately the least severe path — included because it tests whether your placement catches an attacker *before* any lateral movement into the Control LAN, which is where `Early(x)` in the objective function actually gets exercised. A placement that only catches P1/P2 late is a weaker result than one that catches P3 immediately.

| Step | Asset (`v ∈ V`) | Tactic | Technique | Notes |
|---|---|---|---|---|
| 1 | OT DMZ | Initial Access | External scan / perimeter probe | |
| 2 | OT DMZ → Engineering WS-2 | Discovery | Network and remote system enumeration | Resolved toward WS-2, not left disjunctive — a reconnaissance sweep at this stage plausibly lands on whichever workstation is discoverable, not necessarily the primary one; see D19. Previously read "Engineering WS or HMI," an unresolved disjunction the optimizer needed settled regardless of D15. |
| — | — | — | — | No physical impact by design. Success for your placement means interception *during* this path, not after it — this is the path that most directly measures `Early(x)`. |

## How this feeds the rest of the specification

- **`L` (candidate locations, Section 4 of the formal problem definition):** the plausibility rubric should be run against the specific asset types these three paths actually touch (Engineering WS, HMI, PLC/RTU, OT DMZ, Jump Server) — not the full asset list in the abstract.
- **Testbed architecture (next step):** every asset type named in the tables above needs a corresponding node in the VMware/Kali/pfSense build. If a step can't be physically realized in the testbed (e.g., a true IEC-104 RTU), note where a modeled/simulated node substitutes for a physical one, per the "richer graph than physical build" recommendation in the synthesis document.
- **Baseline comparison:** all three methods (random, centrality, proposed) get evaluated against the same **P = {P1, P2, P3}** — the comparison is only meaningful if every method faces identical attack scenarios.
