# Testbed Architecture

Maps `G = (V, E)` from `formal-problem-definition.md` onto an actual build, and verifies it against every asset type touched by P1/P2/P3 in `threat-attack-model.md`. Follows the synthesis recommendation directly: keep the physically-deployed VM count modest, let the modeled graph be somewhat richer.

## Design principle

Two layers, not one:

- **Physical layer** — real VMs in VMware Workstation, actually running OpenPLC/Node-RED/pfSense/etc. This is what you can demo and what the AI layer explains against real telemetry. Kept small enough to build and maintain on weekend hours.
- **Modeled layer** — the same physical nodes, plus additional nodes that exist only in the NetworkX graph (`G`), not as running VMs. These exist purely to give the placement optimizer a topology with real choices to make — a graph with one path through it has nothing to optimize. Modeled nodes are logged and reasoned about identically to physical ones; they just don't consume build time.

## Physical build (7 VMs)

| VM | Software | Zone | Purdue Level | Role in threat model |
|---|---|---|---|---|
| Attacker | Kali Linux | External | — | Entry point for all three paths |
| OT Firewall | pfSense | Perimeter | 3.5 (DMZ boundary) | Conduit c(External, DMZ) |
| DMZ Jump Host | Linux, minimal services | OT DMZ | 3.5 | P2 step 1–2; also a natural historian/patch-relay stand-in |
| Engineering WS | Windows 10/11 or Linux, engineering software installed | Supervisory | 3 | P1 step 1–3 |
| HMI | Node-RED dashboard | Supervisory | 2–3 | P1 step 5; P3 step 2 |
| PLC-01 | OpenPLC | Control | 1–2 | P1 step 4; P2 step 3–5 |
| PLC-02 | OpenPLC | Control | 1–2 | Redundant control target — gives the optimizer a second asset of comparable criticality, so "which PLC" is a real decision |

VMware host-only/internal networks enforce the zone boundaries; pfSense rules encode the conduits. This is the original brief's proposed skeleton essentially unchanged — it was already well-scoped, and the research process didn't surface a reason to expand the physical footprint.

## Modeled-only extensions (graph nodes, no VM)

Added specifically to give the optimizer real tradeoffs and to fully cover the threat model:

| Node | Zone | Why it's graph-only | Why it's needed |
|---|---|---|---|
| Historian | OT DMZ | Common target, doesn't need to run to test placement logic against it | Collection-tactic relevance; a plausible high-value decoy candidate |
| PLC-03 (RTU-type) | Control | A third control asset, modeled with IEC-104 as its protocol | P2 specifically needs an IEC-104 target — running an actual IEC-104 stack is disproportionate build effort for what it adds; model it, don't build it |
| Second Engineering WS | Supervisory | A parallel path into the same zone | Without it, "which engineering workstation" is a non-decision — one real, one modeled gives the optimizer an actual choice |
| Backup Control LAN switch | Control | An alternate conduit into PLC-01/02 | Real OT networks are rarely single-path; a second conduit tests whether your placement covers both routes to the same target, not just the obvious one |

This brings the total graph to 11 nodes across 4 zones — modest by the field's own standards (comparable published work validates at tens to low-thousands of nodes; iteration 2's synthesis found this scale realistic for weekend-hours work), but no longer a single linear chain, which the original brief's skeleton effectively was.

## Zone / conduit structure

```
Zone 0 (External)          — Attacker
        │  conduit: firewall rules
Zone 1 (OT DMZ, PL 3.5)    — OT Firewall, DMZ Jump Host, Historian*
        │  conduit: DMZ→Supervisory rules
Zone 2 (Supervisory, PL 3) — Engineering WS, Engineering WS-2*, HMI
        │  conduit: Supervisory→Control rules (the critical boundary — this is
        │  the single conduit every path in P must cross to reach impact)
Zone 3 (Control, PL 1–2)   — PLC-01, PLC-02, PLC-03*, Backup Switch*
        │
Zone 4 (Process)           — Process Model (OpenPLC-driven simulation)
```
(`*` = modeled-only node)

This is a direct instantiation of `zone(v)` and `c(z_i, z_j)` from Section 1 of the formal problem definition — not a separate diagram that happens to look similar. The optimizer reads this structure directly.

## Candidate locations, worked example

Running Section 4's two-filter process against this specific graph — included here because a worked example is more useful than an abstract description, and because it should genuinely exclude some nodes, not rubber-stamp everything:

- **Passes both filters:** decoy Engineering WS, decoy PLC (mimicking PLC-01/02), decoy HMI, decoy Historian — all standard deception targets with real precedent (Conpot, HoneyPLC, DecIED all deploy at exactly these asset types).
- **Excluded by the plausibility filter:** the OT Firewall itself. There's no realistic "decoy firewall" — a firewall is functional infrastructure an attacker routes through, not a target it interacts with the way it interacts with a workstation or PLC. This is the filter doing real work, not passing everything through.
- **Passes plausibility, down-weighted by detectability:** a decoy placed directly in the OT DMZ. It's a legitimate target, but it's also the most externally-scanned zone, and per the detectability findings in `sources.md` (#262, #263), a decoy that's trivially fingerprinted at a heavily-probed position is worth less than the same decoy deeper in the network. Model this as a lower effective `Risk`-adjusted value for DMZ-zone candidates, not a hard exclusion.

## Verification against the threat model

| Path | Every step has a corresponding node? |
|---|---|
| P1 (Stuxnet-class) | Engineering WS ✓, PLC ✓, HMI ✓ — all physical |
| P2 (Industroyer2-class) | DMZ Jump Host ✓ (physical), Control LAN ✓, PLC/RTU — **PLC-03 (modeled)** carries the IEC-104-specific step; PLC-01/02 can carry the generic Modify Parameter step |
| P3 (reconnaissance-only) | OT DMZ ✓, Engineering WS or HMI ✓ — terminates before Control LAN by design |

No gaps. If a fourth path is added later, check it against this table before assuming the current build supports it.

## Where the optimizer and AI layer sit

Neither lives inside the network topology — they're a separate service layer that reads `G`, `L`, and `P` from the SQLite store (next artifact: data model) and writes back `x*`:

```
NetworkX graph (G, L, P)  →  SQLite
                                 │
                         Optimizer (greedy/MILP, Python)
                                 │
                              x*, F(x*), metric breakdown  →  SQLite
                                 │
                    Local LLM via Ollama (explanation only,
                    per the i-EXAM/SPEAR pattern — sources 244, 255)
                                 │
                         FastAPI → Cytoscape.js / React Flow UI
```

The optimizer never touches the live VMs directly during placement decisions — it operates on the modeled graph. Live VM telemetry (if you wire it up) feeds evaluation *after* placement, to check whether the deployed decoys actually intercept the attack paths when run — that's the evaluation methodology, not this document.

## What This Enables Next

- **Data model** — the SQLite schema for `G`, `L`, `P`, and computed scores, plus how the FastAPI backend reads/writes it
- **Evaluation methodology** — the actual procedure for running Methods 1–3 against P1–P3 on this build and recording results
