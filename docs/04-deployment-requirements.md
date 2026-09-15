# Deployment Requirements — What an Industrial Site Would Need

What it would actually take for a real plant to use iDECOP-ICS. Written for the Limitations and Future Work chapter, and as the prepared answer to "could this be used in industry?"

**Framing, stated first.** iDECOP-ICS is a research prototype validated on a synthetic testbed. This document is not a claim that it is deployable today; it is an inventory of what deployment would require. Several items below are open engineering problems, not configuration steps, and they are marked as such. Being able to enumerate them precisely is a stronger position than claiming the gap is small.

**Confidence markers used throughout:** **[verified]** — actually run and observed in this project. **[likely]** — reasoned from the design or from comparable published work. **[unverified]** — not tested; stated as an open question.

---

## 1. Data the site must supply

This is the real barrier, and it is worth putting first. Every software dependency below is trivially satisfiable. The data is not.

| Input | What it is | Where a plant gets it | Difficulty |
|---|---|---|---|
| Asset inventory | Every asset in scope, with a stable identifier | Existing CMDB, or passive discovery tooling | **Hard.** Most sites do not have a complete, accurate OT inventory. This is the industry's standing problem, not a gap unique to this system |
| `type(v)` | Asset class per asset — PLC, HMI, historian, workstation, firewall | Inventory, or inferred from protocol behaviour | Moderate |
| `zone(v)` | IEC 62443 zone membership | Existing zone and conduit model | **Hard** if no formal segmentation model exists, which is common |
| `level(v)` | Purdue level | Usually derivable once zones are known | Easy |
| `E` — communication relationships | Which assets talk to which, with protocol and a weight | Passive network capture, firewall rules, switch configuration | Moderate. Passive capture is the realistic route; active scanning in OT is often prohibited |
| `SL(v)` | IEC 62443-3-3 Security Level vector per zone | A completed IEC 62443-3-2 risk assessment | **Hard.** Many sites have not done one. Without it, this term has to be substituted or dropped |
| `Damage(v)` | Share of process load the asset is responsible for | A control engineer, not a security team | Moderate — requires process knowledge the security function does not hold |
| `P` — attack paths | Plausible attack scenarios against this specific architecture | Threat modelling against MITRE ATT&CK for ICS | Moderate. Quality of output depends directly on quality of P |
| Plausibility scores | The four-criterion rubric applied per candidate asset | Security analyst, optionally AI-assisted first pass | Easy but manual |
| `B` — budget | How many decoys the site will actually deploy | Management decision, constrained by licence cost and operational appetite | Easy |
| `α…ε` — weights | Relative importance of coverage, earliness, criticality, risk, cost | Sensitivity sweep plus a policy decision by the asset owner | Moderate — the sweep is mechanical, the choice is not |

**The honest summary of this table:** a site that already has an accurate asset inventory and a completed IEC 62443 risk assessment can supply these inputs in days. A site that has neither is looking at a multi-month prerequisite project that has nothing to do with deception.

---

## 2. Software dependencies

Current prototype stack. All open source, no paid dependency — the original brief's constraint, which turns out to matter more for deployment than it did for development.

**Core system**
- Python 3.x
- NetworkX — graph construction and centrality
- Google OR-Tools, CP-SAT solver — exact MILP validation
- FastAPI + an ASGI server (uvicorn) — backend
- SQLite — datastore. **[likely]** a site with existing database standards would substitute PostgreSQL; the schema is not SQLite-specific

**Interface**
- Node.js toolchain (build time only)
- React + Vite — the three screens
- Served as static files at runtime; no Node runtime needed in production

**AI components, both optional**
- Ollama or an equivalent local inference runtime
- A small instruction-tuned model for explanation
- A larger model for the plausibility assist, if that step is used at all

**Operating system** — Linux or Windows. Nothing platform-specific. **[unverified]** the prototype has been run on the development machine only.

**Critical property:** both AI components can be removed entirely and the system still produces a valid placement. Explanation degrades to the raw metric breakdown; plausibility scoring degrades to a human filling in the rubric, which is how it worked before that component existed. A deployment with no AI at all is a supported configuration, not a broken one.

---

## 3. Hardware

**For the optimizer** — negligible. **[verified]** at this project's scale (11 nodes, 5 candidates, 3 paths) both greedy and the CP-SAT validator complete in under a second on a laptop. Any modern machine runs it.

**Scaling is the open question.** **[unverified]** — behaviour at plant scale has not been tested. Reasoning, not measurement:
- Greedy cost grows with budget × candidate count × cost of evaluating F(x), and **[likely]** stays tractable into the hundreds of candidates.
- The MILP validator is the part that will not scale. The formulation solves once per coverage count, and exact methods on NP-hard placement problems degrade sharply with instance size. Comparable published work places MILP tractability at testbed scale, not plant scale.
- **Practical consequence:** at real scale the MILP becomes a validation tool for a sampled sub-problem, not a whole-network validator. That is a design change, not a parameter change, and it is genuine future work.

**For local inference, if the AI components are used**
- Explanation, small model: runs on CPU, or a modest GPU. **[likely]** 8 GB system RAM is sufficient.
- Plausibility assist, larger model: **[likely]** roughly 10–16 GB VRAM for GPU inference, or CPU inference with more RAM and more patience. It is a one-time batch job, so slow is acceptable. This project runs it on Colab specifically because the development machine has 4 GB VRAM — in a plant it must be on-premises instead.

**For hosting** — one modest VM or server inside the plant's security perimeter. No external connectivity required, and that should be enforced rather than merely expected.

---

## 4. What the site needs that this system does not provide

The most commonly missed point, and the one to state plainly. iDECOP-ICS answers *where*. It does not deploy anything, and it does not detect anything.

To act on its output, a site additionally needs:

- **An actual deception platform** — Conpot, HoneyPLC, a commercial OT deception vendor, or an in-house decoy build. This is the crowded, well-served part of the field, which is precisely why this project does not address it.
- **Network capability to place decoys** — VLAN, switch port, or virtualisation capacity at the selected positions. A recommended location that cannot physically host a decoy is an unusable recommendation.
- **Alerting and monitoring integration** — decoy interactions have to reach a SIEM or SOC. A decoy nobody is watching is decoration.
- **An incident response process for decoy alerts.** A decoy alert is high-confidence by construction. Treating it like any other alert wastes its main advantage.

---

## 5. Organisational and process requirements

Usually the binding constraint in OT, ahead of anything technical.

- **Asset owner authorisation.** Placing anything new on a control network is a change to a safety-relevant system.
- **Change management and a safety case.** Specifically: what happens if a decoy PLC is accidentally addressed by an engineering workstation, and does decoy traffic disturb deterministic timing on the segment? These are safety questions, not risk scores. **[unverified]** — not examined in this project, and a real deployment could not skip them.
- **Control engineering time** for `Damage(v)`. Security cannot supply this.
- **Security analyst time** for the plausibility rubric and for reviewing the output before it is acted on. The system is advisory.
- **Re-run cadence.** Networks drift. A placement computed once is stale as soon as a vendor adds a device. A site needs a defined trigger — periodic, or on significant architecture change.
- **Governance of the output itself.** See below.

---

## 6. Security requirements of the deployment

The system's own inputs and outputs are sensitive, and this is easy to overlook because the software is small.

- **Inputs are a target map.** Asset inventory plus zone structure plus criticality plus attack paths is a more useful document to an attacker than most individual device configs.
- **The output is worse.** `x*` states exactly where the decoys are. A leaked placement does not merely neutralise the deception — it inverts it, because the defender continues trusting alerts from positions the attacker now knows to avoid.
- **Therefore:** the whole pipeline runs inside the plant's security perimeter. Inference is on-premises. The placement database is access-controlled at least as strictly as the asset inventory, arguably more. No cloud service touches any of it, including the plausibility-assist step, which must move on-premises or be done manually.
- **Architectural property worth stating:** because the optimiser is deterministic and both AI components sit outside the decision path, a compromised or malfunctioning model cannot alter `x*`. Worst case is a bad explanation or a bad suggestion that a human reviews, not a bad placement.

---

## 7. Open problems, not configuration steps

Listed separately so they are not mistaken for setup tasks.

1. **MILP scalability** beyond testbed size — see §3.
2. **Topology drift** — the model is static; real networks are not. No incremental re-optimisation exists.
3. **Validation methodology** — nobody runs Industroyer2 against a live substation. Real validation means a red team in a maintenance window, or a digital twin. This project validates against modelled attack paths, which is appropriate for a thesis and insufficient for a deployment claim.
4. **`Damage(v)` elicitation at scale** — workable for 11 assets by asking an engineer; unclear for 800.
5. **Detectability scoring is currently qualitative** — applied as a downward adjustment by reasoning, not computed from measurable signatures. A deployment would want it measured.
6. **Safety analysis of decoys on live control segments** — not addressed here at all.

---

## 8. A realistic first deployment

If a site wanted to trial this rather than adopt it, the sensible shape is narrow:

- **One zone pair**, not the whole plant — most plausibly the DMZ-to-supervisory boundary, where the data is easiest to obtain and the operational risk of a decoy is lowest.
- **An offline copy of the topology**, not a live integration.
- **Advisory output only** — the system proposes, humans decide and deploy.
- **A small budget**, two or three decoys, so the change-management burden stays proportionate.
- **A defined success measure agreed in advance** — otherwise the trial produces an opinion rather than a result.

That scope tests the method without requiring any of the open problems in §7 to be solved first. It is also, not coincidentally, close to what this project already demonstrates.
