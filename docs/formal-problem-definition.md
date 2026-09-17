# Formal Problem Definition — Deception Placement Optimization for OT/ICS

Operationalizes the decisions from `research-synthesis-implementation.md` into a precise specification. Every modeling choice below is traceable to a source in `sources.md`; citations use the source numbers from that file.

## 1. Network Model

The OT/ICS architecture is represented as a directed graph **G = (V, E)**.

- **V** — the set of assets: PLCs, HMIs, engineering workstations, historians, firewalls, switches, jump servers. Each **v ∈ V** carries three attributes:
  - `zone(v)` — the IEC 62443 zone the asset belongs to
  - `level(v)` — its Purdue level
  - `type(v)` — asset class (used later to determine deception plausibility)

- **E** — communication relationships. Each edge **e = (u, v) ∈ E** carries:
  - `protocol(e)` — e.g. Modbus, S7comm, OPC UA
  - `weight(e)` — traffic volume or frequency, used for centrality

- **Conduits** — for each pair of zones with permitted communication, a conduit **c(z_i, z_j) ⊆ E** is the subset of edges crossing that zone boundary. Zones and conduits are structural inputs to the model, not decorative labels — this is the specific thing the literature review (sources 231–232, 269) confirmed nobody else does algorithmically.

## 2. Asset Criticality

For every **v ∈ V**, define a criticality score **Crit(v)** combining two independently-sourced components (per the synthesis's explicit recommendation not to pick just one):

**Crit(v) = w₁ · SL(v) + w₂ · Central(v) · Damage(v) + w₃ · ConduitSL(v)**

*(third term added by D20/A22)*

- **SL(v)** — derived from the IEC 62443-3-3 Security Level vector for `zone(v)`: a 7-element vector (source 267) across FR1–FR7 (Identification & Authentication, Use Control, System Integrity, Data Confidentiality, Restricted Data Flow, Timely Response, Resource Availability), aggregated to a scalar (e.g., mean or max of the seven scores, normalized 0–1). State explicitly in the writeup that this is a semi-quantitative approximation, not a solved measurement (source 268).
- **Central(v)** — a graph-centrality measure computed on **G**, weighted by `weight(e)`. Default to betweenness centrality, matching the field's most common choice (source 1 finding) and the pattern in source 282.
- **Damage(v)** — fraction of operational/process load `v` is responsible for, elicited during testbed design (e.g., "this PLC controls 40% of the simulated process") — following the worked pattern in source 282.
- **ConduitSL(v)** — the highest security level among conduits incident to `zone(v)`, where a conduit takes the higher SL of the two zones it joins (rule from source #330). **Why this exists:** the novelty claim names zone *and conduit* structure as first-class inputs, but until D20 conduits were stored and diagrammed while entering no computation. Every path in **P** must traverse a conduit to reach impact, so an asset at a high-SL boundary is materially more important to protect than the same asset type deep inside one zone. The term is modular in **x**, so it does not disturb the submodularity established in Section 7.
- **w₁, w₂, w₃** — weights, set via the same sensitivity-sweep process as the top-level objective (Section 5), not fixed arbitrarily.

## 3. Attack Paths

A finite set of attack scenarios **P = {p₁, …, p_m}** is defined, each **pᵢ** a sequence of (asset, ATT&CK-for-ICS technique) pairs from an entry point to a target, e.g.:

`p₁ = [(VPN, Initial Access), (OT DMZ, Discovery), (Jump Server, Lateral Movement), (Engineering WS, Lateral Movement), (HMI, Collection), (PLC-01, Impair Process Control)]`

At minimum, include one reconnaissance-heavy path, one credential-theft/lateral-movement path (Stuxnet-class), and one direct-impact path (Industroyer/Ukraine-2015-class) — this range is what the comparable literature (sources 12, 45–46) validates against.

## 4. Candidate Deception Locations

Not every **v ∈ V** is a valid decoy site. Define **L ⊆ V** by applying two filters in sequence:

**Filter 1 — Plausibility rubric** (adapted from source 53). For each candidate, score four criteria (yes/mostly/no):
1. Can a defender-controlled decoy plausibly exist at `type(v)`?
2. Would an attacker following a path in **P** plausibly reach or interact with it?
3. Does that interaction yield useful signal?
4. Is the interaction a reliable indicator of malicious intent (low false-positive risk)?

**What is adapted, stated precisely (revised at iteration 11).** Source 53 applies these four criteria to *ATT&CK techniques*, asking of each technique whether it admits a decoy anywhere. This project applies them to *assets in a specific architecture* — asking, of each `v ∈ V` in a zone-structured topology, whether a decoy at that position is plausible given the paths in **P** that actually traverse it. The unit of analysis changes from technique to network position, and the output is a filtered search space for an optimizer rather than a coverage map of a matrix.

*This replaces an earlier and weaker claim* that the project is "the first to apply the rubric to ICS ATT&CK." That claim was dropped at iteration 11 rather than defended: MITRE Engage has published mappings for ATT&CK for ICS since 2024, and while those map techniques to engagement *activities* rather than applying this rubric, the distinction is definitional and not worth the argument it would invite. The claim above is narrower, is specific to this formulation, and does not depend on what any adjacent mapping does or does not contain. See `iteration-11-findings.md`.

**Sweep–Seek refinement of criterion 2 (added at iteration 11).** Source 53's full text supplies a sharper operational form of criterion 2 than "would an attacker plausibly reach it." A decoy is encountered under exactly one of two conditions: **Sweep** — the attacker moves broadly through assets in range and meets the decoy incidentally; or **Seek** — the attacker is looking for a specific asset type and interacts with a fabricated instance of it. A candidate satisfying neither goes untouched regardless of how plausible it looks in isolation. Score criterion 2 by naming which of the two applies, and to which path in **P**. This maps directly onto the attack path set: P3 is a sweep, P1 is a seek, and a candidate that can be justified under neither should not be in **L**.

**Available external input.** MITRE Engage's ATT&CK for ICS mappings are a curated, defensible source for criteria 2 and 3 and should be cited where they inform a score, rather than every score being derived from scratch.

**Filter 2 — Detectability check** (new synthesis from sources 262, 263, 290, 278): exclude or down-weight candidates that would be trivially fingerprintable at that network position (e.g., a heavily-externally-scanned segment where port-count or TTL heuristics reliably expose decoys).

**L** is the surviving set after both filters — this is the actual search space for the optimizer, not **V** itself.

**Process note (added after D12):** Filter 1's four criteria are scored with AI assistance — a model generates a first-pass yes/mostly/no per criterion with reasoning, a human confirms or overrides each before it counts. The criteria themselves are unchanged; what changed is how they're populated. Detail in `02-ai-role.md` §7–10.

## 5. Decision Variables and Objective

For each **l ∈ L**, a binary decision variable:

**x_l ∈ {0, 1}** — 1 if a decoy is placed at location `l`, 0 otherwise

**Maximize:**

**F(x) = α·Coverage(x) + β·Early(x) + γ·CritProt(x) − δ·Risk(x) − ε·Cost(x)**

Where:
- **Coverage(x)** = |{p ∈ P : p intersects at least one l with x_l = 1}| / |P|
- **Early(x)** = Σ over intercepted paths of (1 − stage_intercepted / length(p)), divided by **|P|** — *not* by the number of intercepted paths. Earlier interception scores higher. **The denominator is the whole point (D20):** dividing by the intercepted count makes this a mean, and a mean is non-monotone — adding a late-intercepting decoy *lowers* it. Verified by exhaustive enumeration over all subsets of **L** (`scripts/structure_check.py`): 16 monotonicity and 18 submodularity violations under the mean form, zero under this one. Mean interception stage is still *reported* as a descriptive statistic; it is no longer what the solver maximises
- **CritProt(x)** = Σ over intercepted paths of Crit(target(p)), divided by **Σ over all p ∈ P of Crit(target(p))**. D20 changed this denominator: normalising against the criticality of every asset in the graph capped the term near 0.30 even at full coverage, so γ = 1 was silently γ ≈ 0.3 and the sensitivity sweep would have swept a distorted axis
- **Risk(x)** = Σ over placed decoys of detectability/exposure, divided by **B**. **Read the wording carefully (D20):** this is *normalised detectability exposure*, not a probability. The earlier wording called it a probability while the implementation summed per-decoy values — unbounded above, and inconsistent with the three normalised gain terms. The sum-over-B form is deliberate: a union-probability form, 1 − ∏(1 − r_l), *would* be a genuine probability but is submodular, and subtracting a submodular function would destroy the submodularity Section 7 depends on. Sum/B stays modular. Weight **δ** should still be set high, per the ablation evidence in source 250
- **Cost(x)** = (Σ x_l) / **B** — decoy count normalised by budget, so it lands in [0,1] like every other term. Raw decoy count is still reported. A resource-weighted variant remains possible if deception types differ in overhead

**α, β, γ, δ, ε** are not fixed a priori. Per source 272 (the field's standard practice is parametric sensitivity sweeps, not expert elicitation), run the optimizer across a grid or range of weight combinations and report how the selected placement and each metric shifts — that sweep *is* the justification, not a citation alone.

## 6. Constraints

- **Budget:** Σ x_l ≤ B, where B is the maximum number of deployable decoys (set by testbed resource limits)
- Optional, if time allows: minimum per-zone coverage (Σ x_l for l in zone z ≥ 1 for each zone z with a critical asset), to prevent the optimizer from concentrating all decoys in one high-value area at the expense of others

## 7. Baseline Methods (for validation)

- **Method 1 — Random:** select B locations from **L** uniformly at random. Repeat and average, since a single random draw isn't a fair comparison.
- **Method 2 — Centrality-based:** select the top-B locations in **L** ranked by `Central(v)` alone. State explicitly that this is betweenness centrality specifically, and cite (without needing to implement) the finding that role-aware centrality variants exist and may outperform this (source 237) — naming the limitation is stronger than ignoring it.
- **Method 3 — Proposed:** solve the optimization in Section 5 via:
  - **Primary:** greedy algorithm. **The guarantee must be stated carefully (D20).** After the D20 normalisation, **F(x) is submodular but not monotone** — verified by exhaustive enumeration, and necessarily non-monotone because Risk and Cost are subtracted. The classical (1−1/e) bound requires *monotone* submodular maximisation under a cardinality constraint, so it does **not** apply to F(x) directly. Two defensible positions, one of which must be adopted before any guarantee is claimed:
    - **(i)** Cite the regularised result for f = g − ℓ with g monotone submodular and ℓ modular non-negative (Sviridenko, Vondrák & Ward), which yields a weaker bound of the form (1−1/e)·g(S) − ℓ(S) ≥ (1−1/e)·g(OPT) − ℓ(OPT). **Primary source not yet located and verified — see A27. Claim nothing until it is.**
    - **(ii)** Reformulate: maximise the monotone submodular gain part subject to Σ x_l ≤ B *and* Σ r_l·x_l ≤ R_max, moving risk from penalty to constraint. The classical guarantee then applies cleanly, at the cost of one extra parameter.
    - Before D20 the question was moot: F(x) was **not submodular at all** (18 violations, driven entirely by the Early mean), so no guarantee of any kind was available. Report this honestly — it is a genuine finding, not an embarrassment.
    - **What carries the practical argument meanwhile:** the exact MILP validator reports a 0.0% optimality gap on this instance. The approximation guarantee matters for the *scalability* claim, not for these results
  - **Validation:** exact MILP formulation at testbed scale (tractable per source 296's precedent), used to report an optimality gap against the greedy result, not as the primary method

All three methods are run against the same **P** and compared on: Coverage, Early, CritProt, Cost, and wall-clock computation time.

## 8. Research Questions, Restated Formally

**Primary (rephrased at D20):** Does Method 3 achieve a higher composite objective **F(x)** than Methods 1 and 2 across the attack scenario set **P** and across a range of objective weightings — and, specifically, achieve equal or greater **Coverage(x)** and **CritProt(x)** at equal or lower **Cost(x)**?

*Why rephrased.* The original wording asked only about Coverage and Cost, two of the five terms. A method that deliberately trades raw coverage against operational risk — which is the entire point of this work — can lose on that phrasing while being the better answer. Asking about the composite objective *and* retaining the checkable coverage-at-cost clause keeps the question falsifiable without understating the contribution. The original wording is preserved here rather than deleted, because the results chapter reports against both.

**Secondary:** Can a local LLM, given `(x*, F(x*), Coverage/Early/CritProt/Risk/Cost breakdown, comparison to Methods 1–2)` as structured input, generate an analyst-readable explanation of *why* each `l` with `x_l = 1` was selected — without altering `x*` itself? (Architecture precedent: sources 244, 255, 257 — planner decides, LLM explains, and the planning formalism has already been shown to transfer to OT-adjacent topologies.)

## What This Enables Next

With this specification fixed, the next artifacts become well-defined rather than open-ended:
- **Threat/attack model** — formalize the specific paths in **P** (Section 3) with real ATT&CK-for-ICS technique IDs
- **Testbed architecture** — map **V**, **E**, and zones directly onto the VMware/Kali/pfSense/OpenPLC/Node-RED build
- **Data model** — the schema for storing **G**, **P**, **L**, and computed scores (SQLite, per the original brief)
- **Evaluation methodology** — the exact procedure for running Methods 1–3 against **P** and reporting results
