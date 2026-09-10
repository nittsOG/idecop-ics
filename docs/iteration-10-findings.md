# Iteration 10 Findings — OT/ICS Deception Placement Optimization

Builds on iterations 1–9. Does not repeat those conclusions — see `sources.md` for the running source log. Source numbers below refer to that file (iteration 10 = #305–309).

This round took iteration 9's suggestion to go sector-specific (electric utility / smart grid) rather than general-OT. It found the single most important piece of prior art in the whole process.

## 1. Read this paper before you write section 14

Devika Jay published "Deception Technology Based Intrusion Protection and Detection Mechanism for Digital Substations: A Game Theoretical Approach" in IEEE Access in 2023 [305]. It formally optimizes decoy *allocation* — not just decoy design, actual allocation — inside a digital substation's GOOSE-message VLAN, using a bi-level Stackelberg game between defender and attacker, with proven equilibrium existence, validated against real protection-relay data on 3-IED and 12-IED test systems.

This is the closest thing to direct prior art found across all ten iterations. Closer than Zambianco et al., because Zambianco is enterprise IT. Closer than DecIED or Decepti-SCADA, because neither of those formally optimizes placement the way this does. This is a published, peer-reviewed, formally-optimized, OT-specific decoy-placement paper.

That doesn't mean your project is subsumed by it — there are real distinctions, but they need to be argued on the page, not assumed:

- **Scope.** Jay's model lives inside one substation's internal VLAN. Your project spans a multi-zone OT architecture — DMZ, engineering workstation, HMI, control LAN, multiple PLCs, the IT/OT boundary itself. Hers is a local optimization within one zone; yours is a placement problem across zones.
- **Standard and protocol.** Jay's formulation is built on IEC 61850 and GOOSE-message semantics specifically — a protocol-level model for one kind of OT system (digital substations). Yours is built on IEC 62443 zones and conduits — an architecture-level model meant to generalize across OT system types, not tied to one protocol.
- **Objective.** Jay optimizes a game-theoretic equilibrium over *which type* of decoy to allocate (protection vs. detection) under a leader-follower game. Your objective is a composite of attack-path coverage, early detection, criticality, operational risk, and cost, with criticality and risk as separate weighted terms tied to asset importance — a different mathematical object solving a different question, even though both are called "decoy allocation."

Those distinctions are real and defensible. But given how close this paper sits to your core contribution, it deserves a dedicated paragraph in your differentiation section — not a citation buried in a list with Zambianco and the rest. Get the full text, confirm the distinctions hold up against the actual formulation (not just the abstract), and write the paragraph early rather than discovering a problem with it during your defense.

## 2. The cleanest gap citation found yet

EPRI — the electric utility industry's own collaborative R&D organization, not an academic body — published a 2019 report stating plainly that "practical unknowns" remain around "the appropriate design and placement of lures and decoys" [306]. This is worth more than it might look like: it's the industry itself, not researchers studying the industry, saying placement is unresolved. Paired with Sandia (iteration 8, a national lab) and now EPRI (iteration 10, an industry R&D consortium), you have gap confirmations from academia, government, and industry — three structurally different kinds of authority all saying the same thing independently.

## 3. The sector-specific pattern holds

A smart-grid-focused survey [307] independently found what the general-OT surveys already found: deception in this space is under-researched, and what exists has only been evaluated preliminarily. An EU Horizon 2020 project (SDN-microSENSE [308]) is doing honeypot-based smart-grid risk assessment with Schneider Electric and several European universities — another sector-specific European entry, alongside a second power-grid-specific honeypot tool [309]. None of this changes the picture on its own; it reinforces it from the electricity sector specifically, the way iterations 1-9 built it from the general-OT angle.

## Still open

- Source 305 needs a full read of the actual mathematical formulation (not just the abstract) to confirm the three distinctions drawn above hold up in detail, and to check its own related-work section for anything it cites that might be even closer to your problem than it is.
- Water and manufacturing sectors haven't had the same targeted pass electric utility just got — worth checking whether either sector has its own version of the Jay paper.

## Candidates for iteration 11

- A full-text read of source 305, specifically checking whether its bi-level formulation could extend beyond one VLAN to a multi-zone topology — if it explicitly says it can't (a stated limitation), that's a strong, citable line for your differentiation section. If it says nothing either way, that's still useful to know.
- A water-sector and manufacturing-sector pass, mirroring this round's electric-utility pass, to see whether the same "sector body confirms the gap" pattern repeats or whether one of those sectors already has its own close prior art the way electric utilities turned out to.
