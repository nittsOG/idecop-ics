# Original Project Brief

The founding document for this project, as provided at the start of this conversation. Never previously saved as a file — it existed only in chat history until now, which is a real gap given how much later work (the scope boundary especially) depends on it. Preserved here verbatim; later documents refine and formalize what's here, but this is the source those refinements trace back to.

---

## M.Tech Major Project — Master Project Context

M.Tech Cyber Security student at National Forensic Sciences University (NFSU). Major Project as a working prototype / research-oriented implementation, with a strong focus on OT/ICS cybersecurity and critical infrastructure security.

### 1. Finalized Project

**Title:** "AI-Assisted Deception Placement Optimization for Industrial Control Systems"
**Domain:** SCADA – OT

Direction discussed with and selected by the guide for further development.

### 2. Core Problem

Not about building another honeypot. Existing deception technologies already provide honeypots, honeytokens, honey credentials, honey files, decoy services, decoy industrial devices.

The problem investigated: *given an OT/ICS network architecture, where should deception assets be placed to maximize their cybersecurity value?* — using OT network topology, asset criticality, zones and conduits, communication relationships, potential attack paths, detection coverage, early detection, deployment constraints, and operational considerations. Focuses on placement/optimization, not deployment of deception itself.

### 3. Core Research Question

**Primary:** Can deception assets be systematically placed within an OT/ICS architecture to maximize early attack detection and coverage of plausible attack paths while minimizing operational impact and deployment cost?

**Secondary:** Can AI assist security analysts by explaining and contextualizing the resulting deception-placement recommendations?

### 4. Important Project Boundary

**Do NOT turn this project into:** a generic honeypot; a generic honeytoken platform; a generic AI chatbot; a generic attack graph; a generic vulnerability scanner; a generic OT asset inventory; a GRC/compliance dashboard; a generic network visualization tool.

The central contribution is deception placement optimization for OT/ICS security — this boundary governs every design decision made since.

### 5. Proposed Concept

```
OT/ICS Architecture + Asset Criticality + Network/Communication Relationships + Attack Scenarios
  → OT Network Model → Attack-Path Analysis → Candidate Deception Locations
  → Deception Placement Optimization → Recommended Placement
  → AI-Assisted Explanation → Security Analyst
```

The system should answer: why was this location selected; how many plausible attack paths interact with it; how early would an attacker be detected; which critical assets benefit; how does this compare to random or manual placement.

### 6. Candidate Deception Assets

Decoy PLC, honey credentials, honey files, decoy services, and other OT-specific mechanisms if justified later. Not every type needs implementing initially — the initial prototype focuses on a small number of practical primitives, concentrating on the placement algorithm.

### 7. Testbed

Fully virtualized, no physical PLC required initially:
```
Kali/Attacker → OT Firewall → OT DMZ → {Engineering WS, HMI} → Control LAN → {PLC-01, PLC-02} → Process Model
```
Exists primarily to validate the placement algorithm.

### 8. Proposed Free/Open-Source Technology Stack

Virtualization: VMware Workstation. Attacker: Kali Linux. Firewall/routing: pfSense (or Linux routing). PLC simulation: OpenPLC. HMI/SCADA: Node-RED. Engineering workstation: Windows or Linux VM. Deception: OpenPLC-based decoy PLC, honey files, honey credentials, decoy services. Network/graph modeling: Python, NetworkX. Optimization: to be selected after literature review — candidates include greedy, integer programming, graph-based optimization, genetic algorithms; potential tools OR-Tools, SciPy. Backend: Python, FastAPI. Database: SQLite. Visualization: Cytoscape.js or React Flow. AI: local/open-source model preferred (Ollama) — no paid API dependency in the core project.

### 9. AI Philosophy

AI should not randomly decide placement — the security/optimization layer stays deterministic and measurable.
```
OT Architecture → Network Model → Attack-Path Analysis → Optimization Algorithm
  → Recommended Placement → AI → Explanation / Context / Analyst Assistance
```
AI may explain why a placement was selected, interpret OT architecture descriptions, summarize security implications, convert optimization results into analyst-readable recommendations, and potentially interpret unstructured OT documentation. The core security decision stays explainable and reproducible.

### 10. Possible Optimization Metrics

"Best placement" must be objectively defined: attack-path coverage, early detection (stage of attack path at which deception is encountered), critical-asset protection, false-positive/operational risk, deployment cost. A possible objective combines Detection Coverage + Early Detection + Critical Asset Protection − Operational Risk − Deployment Cost. Exact formulation and weighting must be justified through literature, experiments, sensitivity analysis, and/or expert input — not arbitrarily chosen.

### 11. Validation Strategy

Compare against baselines: Method 1 (Random Placement), Method 2 (Centrality-Based Placement), Method 3 (Proposed Optimization). Run the same controlled OT attack scenarios against each; compare attack-path coverage, detection position, critical-asset coverage, number of deception assets required, operational/deployment cost, computational time.

### 12. Example OT Attack Scenario

```
Attacker → VPN → OT DMZ → Jump Server → Engineering Workstation → HMI → PLC
```
Possible deception locations along this path: VPN, OT DMZ, Jump Server, Engineering Workstation, HMI, PLC Network. The optimizer selects based on the formally defined objective.

### 13. OT Security Frameworks

Grounded in recognized concepts where they actually support the work: MITRE ATT&CK for ICS, IEC 62443, NIST SP 800-82, relevant OT/ICS deception research, relevant graph/optimization research. Frameworks aren't forced in where they don't support the problem formulation, attack modeling, security requirements, or evaluation.

### 14. Existing Solutions and Differentiation

Existing technologies already provide deception (ICS/OT honeypots, Conpot, enterprise deception platforms, honeytokens, decoy credentials/services) — creating a honeypot is not the novel claim. The intended distinction: *existing solutions primarily provide or deploy deception assets, whereas this project investigates the systematic optimization of where deception should be placed within an OT/ICS architecture based on measurable security objectives.* This differentiation must be verified through literature and existing-tool review before making strong novelty claims.

### 15. Current Project Status (at project start)

Direction selected; next stage is not further brainstorming. Original 12-item roadmap: literature review; existing OT deception solutions; existing deception-placement research; formal problem definition; threat/attack model; testbed architecture; data model; optimization formulation; AI role; prototype architecture; evaluation methodology; implementation roadmap.

### 16. Important Working Principle

*I want rigorous reasoning rather than agreement. If an idea is weak, say so. If an existing tool already solves something, identify it. If a proposed feature is unnecessary, remove it. If AI does not add genuine value to a particular component, do not add AI merely because the project title contains AI. If the proposed research contribution cannot be measured, identify the problem before implementation.*

The goal: a working, technically defensible OT cybersecurity prototype with meaningful experimental evaluation — not an attractive dashboard or an AI wrapper.

---

## Immediate Next Objective (at project start)

Deep analysis of existing OT deception/honeypot solutions and academic research on deception placement/optimization, before locking the implementation algorithm — what tools exist, what they solve, how they decide placement, what OT-specific placement algorithms exist, what optimization models and metrics have been used, what gaps remain, what's realistic for an M.Tech prototype, and how this project should differ from existing work. *(This objective is what the ten research iterations and everything since have been answering.)*
