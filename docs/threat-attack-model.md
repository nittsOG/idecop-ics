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

## P4 — Dragonfly-class: ICS data collection for later operations

Added at D21, before the evaluation campaign. Models an adversary whose objective is intelligence, not impact: it steals the documentation needed to plan a later physical attack. Included because P1–P3 left the Historian on no path at all, and because a collection-motivated campaign is a distinct attacker behaviour the other three do not represent.

Grounded in Dragonfly / Dragonfly 2.0, whose documented behaviour was accessing workstations and servers holding ICS reference material — wiring diagrams, panel layouts, vendor documentation — after entry through trojanised vendor software.

| Step | Asset (`v ∈ V`) | Tactic | Technique | Notes |
|---|---|---|---|---|
| 1 | Engineering Workstation | Initial Access | **T0862 — Supply Chain Compromise** | Dragonfly's documented vector: legitimate ICS vendor software trojanised at the source and installed by the victim. Verified against MITRE-authored ATT&CK for ICS material |
| 2 | Historian | Collection | **T0811 — Data from Information Repositories** | Verified at attack.mitre.org/techniques/T0811/ — Collection tactic, and its Targeted Assets list names **A0006 Data Historian** explicitly. Dragonfly 2.0 appears as a procedure example |
| 3 | Engineering Workstation | Collection | **T0811 — Data from Information Repositories** | Continued collection of ICS reference documents. The same technique page lists Engineering Workstation as a targeted asset |
| — | — | — | — | No process impact by design. Success for the placement means interception before the documentation leaves the environment |

**Why the entry point is the engineering workstation and not the DMZ jump host.** Both were drafted. The jump-host version was rejected on two grounds: it is less faithful to Dragonfly, whose documented initial access was supply-chain and watering-hole rather than perimeter intrusion; and it left the Historian contributing nothing, since a decoy at the jump host would intercept P4 at step 1 and make the Historian redundant. The supply-chain version is both historically accurate and structurally useful. The order in which those two facts were established is recorded in D21 rather than presented as a single clean decision.

## P5 — Backup-conduit: network-device compromise, alternate route to PLC-01

Added at D27, before the evaluation campaign and before any Filter 1 score existed. The testbed includes a Backup Control LAN switch for one stated purpose: "a second conduit tests whether your placement covers both routes to the same target, not just the obvious one" (`testbed-architecture.md`). No path ever used it. ATT&CK for ICS lists **A0015 Switch** as an asset that 33 techniques target (#378), and VPNFilter is documented malware that sniffed ICS traffic from inside network devices (#380). The user raised the gap. D21 froze the paths "unless a documented defect emerges", and this is one.

P5 combines documented techniques rather than replaying one named campaign, as P3 does. It follows the testbed's own edges (DMZ Jump Host → Backup Control Switch → PLC-01). It targets **PLC-01** because P1 reaches PLC-01 by the primary route, so the two paths test both routes to the same target.

| Step | Asset (`v ∈ V`) | Tactic | Technique | Notes |
|---|---|---|---|---|
| 1 | DMZ Jump Host | Initial Access | **T0822 — External Remote Services** | Verified at attack.mitre.org/techniques/T0822/ (#383). Initial Access; its targeted assets include Jump Host. The 2015 Ukraine attack is a procedure example: Sandworm used valid credentials to reach the control-system VPN |
| 2 | Backup Control Switch | Lateral Movement | **T0866 — Exploitation of Remote Services** | Verified (#382). Tactics Initial Access and Lateral Movement; its targeted assets include Switch |
| 3 | Backup Control Switch | Discovery | **T0842 — Network Sniffing** | Verified (#381). Discovery; its targeted assets include Switch. VPNFilter is a procedure example: its sniffer "monitors ICS traffic" (#380) |
| 4 | PLC-01 | Impair Process Control | **T0836 — Modify Parameter** | The same step P1 takes at PLC-01, already verified for P1. The more specific T0855 Unauthorized Command Message could not be fetched (#384), so it is not used |

**Why this is not D21's error in reverse.** D21 refused to add a path "solely to make [PLC-02] selectable". P5 does make the switch selectable, but that is a consequence, not the reason. The reasons are documented ones: the testbed's stated purpose for the switch, ATT&CK for ICS's treatment of switches as targets, and VPNFilter's recorded behaviour. The target follows the same stated purpose. PLC-02 still lies on no path, and stays there (D27, option (a)).

## How this feeds the rest of the specification

- **`L` (candidate locations, Section 4 of the formal problem definition):** the plausibility rubric should be run against the specific asset types these three paths actually touch (Engineering WS, HMI, PLC/RTU, OT DMZ, Jump Server) — not the full asset list in the abstract. *(D26: overtaken. There are now five paths (P5 added by D27), and A32 scores every asset except the Attacker node, so that an asset off every path is excluded by a recorded rule rather than by omission.)*
- **Testbed architecture (next step):** every asset type named in the tables above needs a corresponding node in the VMware/Kali/pfSense build. If a step can't be physically realized in the testbed (e.g., a true IEC-104 RTU), note where a modeled/simulated node substitutes for a physical one, per the "richer graph than physical build" recommendation in the synthesis document.
- **Baseline comparison:** all methods get evaluated against the same **P = {P1, P2, P3, P4, P5}** (P5 added by D27) — the comparison is only meaningful if every method faces identical attack scenarios.
