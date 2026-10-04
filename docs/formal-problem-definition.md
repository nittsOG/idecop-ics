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

The current set is P1–P5 (`threat-attack-model.md`). D21 added P4, and D27 added P5, the backup-conduit path.

## 4. Candidate Deception Locations

Not every **v ∈ V** is a valid decoy site. Define **L ⊆ V** by applying two filters in sequence. Everything in this section up to Filter 2 was fixed by D26 **before any scoring took place**, which is the order the source itself follows ("we fixed the decision rules before scoring", #40).

**What a candidate means.** **x_l = 1** places a decoy imitating `type(l)` in `zone(l)`, on the same network segment and behind the same conduits as `l`. Attack paths through `l` pass where it sits. It is not a change to the real asset. Whether an attacker on a path would actually interact with the decoy is not assumed here: criterion 2 scores it.

**Filter 1 — Plausibility rubric** (adapted from #40, Valeros et al. 2026). Each asset except the Attacker node is scored on four criteria, in this order:

| # | Criterion (#40's name) | Plain question | Database column |
|---|---|---|---|
| 1 | Feasibility | Can a defender build and control a convincing decoy of this asset type at this position? | `criterion_decoy_exists` |
| 2 | Interaction | Would an attacker following a modelled path through this position interact with the decoy? | `criterion_attacker_reach` |
| 3 | Intelligence yield | Would that interaction tell the defender something useful about the attacker? | `criterion_useful_signal` |
| 4 | Malice fidelity | When the decoy is touched, is that reliably an attacker rather than routine benign activity? | `criterion_reliable_indicator` |

**Scale.** Every criterion uses #40's four-point forced choice with no neutral midpoint: **Yes / Mostly Yes / Mostly No / No**. The level definitions are #40's Table 1, reproduced unchanged below. *(Before D26 this section used yes / mostly / no. That scale's "mostly" merged #40's two middle levels and, with the prompt's instruction "if you are genuinely unsure, say mostly", re-introduced the neutral default #40 removes by design.)*

**Combination rule (D26).** An asset passes Filter 1 only if all four criteria are answered and none is **No**. Mostly No passes.
- #40 defines "admits a decoy" by Feasibility alone. But none of its 80 admitted techniques scored No on a later criterion, so the paper never had to decide what a later No means. *(For Malice fidelity the zero is by arithmetic, 80 − 30 − 44 − 6, because the printout truncates that column; #40.)* Its conclusion speaks of a decoy "that the attacker could plausibly reach".
- This project's objective counts every interception as a detection and has no false-positive term. An asset that scores No on Interaction would be credited with interceptions the rubric says will not happen. One that scores No on Malice fidelity would be credited with detections the rubric says cannot be told apart from routine activity. Exclusion is the smallest rule that keeps F consistent with the rubric.
- Intelligence yield is the one criterion the objective does not strictly need to gate, since F credits detection, not intelligence. It is kept in the rule for simplicity. #40 found it almost never limiting: one Mostly No, and no No, among 80 techniques.
- This is a declared adaptation, not #40's own rule.

**Scoring conventions (D26), fixed before scoring:**
1. **Order.** Score the criteria in order. The first No ends the evaluation, and the criteria after it stay blank (#40).
2. **Ties.** Where the evidence fits two adjacent levels equally, choose the lower one, closer to No (#40).
3. **Best case, actual position.** Score each criterion for "the best case a well-instrumented decoy could plausibly produce" (#40), but at this position in this network. #40 scores what is possible in principle; this project scores one deployment.
4. **Interaction is judged only against the paths in P, as modelled.** For each path, name it and say whether the encounter is a **Sweep** or a **Seek** (see below). The card lists the steps.
   - An asset that appears in no path's asset sequence scores **No**, because the model cannot credit it with any interception. The API and Screen 3 enforce this for human answers, and the notebook's code for the AI's. In the current testbed it applies only to PLC-02. *(D26 also named the Backup Control Switch here. D27 added P5 through it.)* Because the rule imposes this No, it needs no written reason. An asset excluded this way is still scored, and the thesis reports it as a plausible decoy site outside the modelled threats (D27, option (a)). It is not silently dropped.
   - An asset on more than one path is scored per path, and the lowest per-path level is recorded (**weakest path decides**). The objective credits an interception on every path through a chosen site, so a single best-case score would credit paths the rubric says the attacker would not take that way. The reviewer gives each path's level in the required reason. Since D27 this applies to three assets: Engineering WS (P1, P4), the DMZ Jump Host (P2, P5) and PLC-01 (P1, P5).
5. **Malice fidelity names the benign activity first.** Before scoring, write down the routine benign activity that reaches this position. In OT networks that includes asset-inventory and monitoring scans, historian polling and data collection, engineering-software and vendor maintenance sessions, backup jobs and time synchronisation. #40's own expert study asks for this ("make Malice Fidelity more explicit about benign administrative activity"); the list of examples is this project's.

**Level definitions — #40, Table 1, reproduced unchanged.** In this project the unit is an asset position, so read "the technique" as "the attack-path steps at this position". That reading note is ours, not part of the table.

| Score | Feasibility | Interaction | Intelligence Yield | Malice Fidelity |
|---|---|---|---|---|
| **Yes** | The defender can fully fabricate and control the target asset as a decoy, and it responds convincingly to attacker actions. | The technique naturally leads attackers to the decoy. Interaction follows as a direct consequence of the technique. | Interaction directly yields strategic, operational, tactical, or technical intelligence attributable to the decoy. | Legitimate interaction is not expected by design. The only plausible trigger is an attacker action, so the false-positive rate is near zero. |
| **Mostly Yes** | The target asset can be mimicked but it is hard to make convincing. May not withstand close scrutiny. | Interaction is likely but not certain, depending on the decoy’s positioning, configuration, or the attacker’s tools. | Interaction yields intelligence, but only after correlation with other data, added context, or further analysis. | Interaction strongly indicates malice. A small set of benign activities could trigger it, but these cases are identifiable and filterable. |
| **Mostly No** | The target asset can only be partially mimicked as a decoy. It is difficult to simulate convincingly and only works in limited conditions. | Interaction is possible but unlikely, requiring attacker-specific knowledge, unusual timing, or atypical choices. | Interaction produces some data, but it is too generic or ambiguous to be meaningful without significant further analysis. | Interaction may indicate malice, but many triggers are benign or ambiguous. Telling them apart is complex, so the signal is useful but not standalone. |
| **No** | The technique has no defender-controllable target asset that can be fabricated and operated as a decoy. | No plausible attacker path to the decoy exists. An attacker following the technique would not be expected to interact with this decoy. | No intelligence yield. The observable data gives no insight into the attacker’s behavior, identity, or intent. | Benign activity routinely triggers this decoy. Interaction does not distinguish an attacker. |

*Source: Valeros, Lisý, Catania and Griffioen (2026), "Decoys Cannot Go Everywhere: Mapping the Deception Surface in MITRE ATT&CK", arXiv:2606.27966, Table 1 (#40). Licence [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) (#368). No changes made.*

**What is adapted, stated precisely (revised at iteration 11, extended by D26).** #40 applies its criteria to *ATT&CK techniques*, asking of each technique whether it admits a decoy anywhere, and scores what is possible in principle. This project applies them to *assets in a specific architecture*, asking of each `v ∈ V` in a zone-structured topology whether a decoy at that position is plausible, given the paths in **P** that actually traverse it.
- The unit of analysis changes from technique to network position.
- The output is a filtered search space for an optimiser, rather than a coverage map of a matrix.
- #40 names an asset-centred assessment as future work. This is one deployment-specific form of it.
- D26 adds three things: the combination rule, convention 3's restriction to the actual position, and conventions 4 and 5. The scale, the order rule, the tie rule and the best-case wording are #40's own.

*This replaces an earlier and weaker claim* that the project is "the first to apply the rubric to ICS ATT&CK." That claim was dropped at iteration 11 rather than defended: MITRE Engage has published mappings for ATT&CK for ICS since 2024, and while those map techniques to engagement *activities* rather than applying this rubric, the distinction is definitional and not worth the argument it would invite. The claim above is narrower, is specific to this formulation, and does not depend on what any adjacent mapping does or does not contain. See `iteration-11-findings.md`.

**Sweep–Seek refinement of criterion 2 (added at iteration 11).** #40's full text supplies a sharper operational form of criterion 2 than "would an attacker plausibly reach it." A decoy is encountered under exactly one of two conditions: **Sweep** — the attacker moves broadly through assets in range and meets the decoy incidentally; or **Seek** — the attacker is looking for a specific asset type and interacts with a fabricated instance of it. A candidate satisfying neither goes untouched regardless of how plausible it looks in isolation. Score criterion 2 by naming which of the two applies, and to which path in **P**. This maps directly onto the attack path set: P3 is a sweep, P1 is a seek, and a candidate that can be justified under neither should not be in **L**. *(Corrected 3 October 2026, D26: this paragraph and the one above it cited "source 53", which is an unrelated IEC 62443 paper. The rubric's source is #40.)*

**Available external input.** MITRE Engage's ATT&CK for ICS mappings are a curated, defensible source for criteria 2 and 3 and should be cited where they inform a score, rather than every score being derived from scratch.

**How the scores are produced (D26, route A).** The process has seven steps.
1. An AI first pass suggests a level and a one-line reason per criterion. It runs once, in `notebooks/plausibility_scoring.ipynb` (A20). The model is Qwen3-14B, loaded in 4-bit. Qwen3-8B is the pre-declared fallback if 14B cannot load.
2. A human reviews every asset in Screen 3 and confirms or changes each answer. Only confirmed answers count.
3. **Three blind cards:** DMZ Jump Host, Historian and PLC-03 (RTU).
   - They were drawn at random, before any AI output existed, from the eight assets that lie on a modelled path. The draw is recorded in D26.
   - They are scored before their AI answers are shown.
   - Their first answers are stored once and never change, even if the final answers are later revised with a reason.
   - They give the one unanchored measure of how often the AI agrees with independent judgement.
4. **A written reason** is required:
   - on a blind card;
   - on a card with no AI suggestion;
   - after changing any AI answer;
   - for any Mostly No or No.
5. **No fallback to the AI's answer.** A blank stays blank.
6. **Fallback route.** If the notebook produces no suggestions within two weekends of the blind cards being finished, the remaining cards are scored directly (route B), with reasons.
7. **The review is committed.** It is exported to `data/review/plausibility_review.csv` and committed, because the database is not tracked. That file is the frozen Filter 1 input.

This is D12's route: an AI first pass, then human confirmation. People shown an LLM's suggestion drift toward it even when they review it (#362, #363), so D26 adds the safeguards above. The risk that remains is stated as a limitation in `02-ai-role.md` §10. The alternatives considered are recorded in D26.

**Filter 2 — Detectability check** (new synthesis from sources 262, 263, 290, 278): exclude or down-weight candidates that would be trivially fingerprintable at that network position (e.g., a heavily-externally-scanned segment where port-count or TTL heuristics reliably expose decoys). Implemented as the D22a rubric (`02-detectability-rubric.md`). **Every asset that passes Filter 1 needs a D22a score before the optimiser will run on it.** The candidate loader refuses a candidate set in which any member lacks one (D26). Before D26 the optimiser silently read a missing score as 0.0, i.e. as a perfectly safe decoy.

**L** is the surviving set after both filters — this is the actual search space for the optimizer, not **V** itself.

> ⚠️ **State of the data after D26.** The seed no longer pre-judges L: every asset starts unscored and outside it, so **L is empty until the A32 review**. The scripts refuse to run on an empty set, and on any candidate that bypassed the review.
> - D25 found that the seeded set had bypassed Filter 1. That set is kept only as `data/legacy/d25_candidate_set.sql`, to reproduce numbers recorded before D26, behind an explicit `--legacy-d25` flag. The API never accepts it.
> - Assets without a D22a score: Engineering WS, PLC-01, PLC-03 (RTU), Backup Control Switch and the OT Firewall. Any of them that passes Filter 1 is scored at A32 step 4.
> - The attack-path set is P1–P5. D27 added P5 through the Backup Control Switch.

**Process note (added after D12, revised by D26):** Filter 1's criteria are scored with AI assistance. A model suggests a first pass, and a human confirms or overrides each answer before it counts. D26 fixed the scale, the rules and the safeguards above. Detail in `02-ai-role.md` §7–10.

## 5. Decision Variables and Objective

For each **l ∈ L**, a binary decision variable:

**x_l ∈ {0, 1}** — 1 if a decoy is placed at location `l`, 0 otherwise

**Maximize:**

**F(x) = α·Coverage(x) + β·Early(x) + γ·CritProt(x) − δ·Risk(x) − ε·Cost(x)**

Where:
- **Coverage(x)** = |{p ∈ P : p intersects at least one l with x_l = 1}| / |P|
- **Early(x)** = Σ over intercepted paths of (1 − stage_intercepted / length(p)), divided by **|P|** — *not* by the number of intercepted paths. Earlier interception scores higher. **The denominator is the whole point (D20):** dividing by the intercepted count makes this a mean, and a mean is non-monotone — adding a late-intercepting decoy *lowers* it. Verified by exhaustive enumeration over all subsets of **L** (`scripts/structure_check.py`): on the frozen four-path instance, **30 monotonicity and 57 submodularity violations** under the mean form, zero under this one. (D20 recorded 16 and 18; those were correct for the three-path instance and went stale when D21 added P4 — see D24. The qualitative finding is unchanged, and F's submodularity violations equal Early's exactly on both instances, which demonstrates rather than asserts that the Early mean was the sole cause.) Mean interception stage is still *reported* as a descriptive statistic; it is no longer what the solver maximises
- **CritProt(x)** = Σ over intercepted paths of Crit(target(p)), divided by **Σ over all p ∈ P of Crit(target(p))**. D20 changed this denominator: normalising against the criticality of every asset in the graph capped the term near 0.30 even at full coverage, so γ = 1 was silently γ ≈ 0.3 and the sensitivity sweep would have swept a distorted axis
- **Risk(x)** = Σ over placed decoys of detectability/exposure, divided by the fixed constant **K = 4** (D25; D20 divided by **B**). **Read the wording carefully (D20):** this is *normalised detectability exposure*, not a probability. The earlier wording called it a probability while the implementation summed per-decoy values — unbounded above, and inconsistent with the three normalised gain terms. The divided-sum form is deliberate: a union-probability form, 1 − ∏(1 − r_l), *would* be a genuine probability but is submodular, and subtracting a submodular function would destroy the submodularity Section 7 depends on. A sum over a constant stays modular. **Why a constant and not B (D25):** B is a cap on how many decoys the site deploys, and the adversary never observes it. Dividing by B made the same decoy worth a different amount at different budgets: the DMZ Jump Host alone scored −0.063 at B=1 and +0.332 at B=2, and under δ=3 greedy placed 0, 0, 1 and 4 decoys at B=1..4. It also confounded B with δ across the sweep. Dividing by |P| or |L| fails other invariance tests recorded in D25. K = 4 was the smallest constant keeping Risk and Cost in [0,1] for every budget of the declared comparison grid when D25 chose it. It is frozen from then on and not re-derived from any grid, because dividing by K is the same as rescaling δ and ε; changing it is an objective change needing its own entry. Weight **δ** should still be set high, per the ablation evidence in source 250
- **Cost(x)** = (Σ x_l) / **K** — decoy count divided by the same fixed K = 4 as Risk (D25; D20 divided by **B**), so it lands in [0,1] across the declared grid like every other term, and a decoy's operating burden does not depend on how many decoys were licensed. Raw decoy count is still reported. A resource-weighted variant remains possible if deception types differ in overhead

**α, β, γ, δ, ε** are not fixed a priori. Per source 272 (the field's standard practice is parametric sensitivity sweeps, not expert elicitation), run the optimizer across a grid or range of weight combinations and report how the selected placement and each metric shifts — that sweep *is* the justification, not a citation alone.

## 6. Constraints

- **Budget:** Σ x_l ≤ B, where B is the maximum number of deployable decoys (set by testbed resource limits)
- Optional, if time allows: minimum per-zone coverage (Σ x_l for l in zone z ≥ 1 for each zone z with a critical asset), to prevent the optimizer from concentrating all decoys in one high-value area at the expense of others

## 7. Baseline Methods (for validation)

- **Method 1 — Random:** select B locations from **L** uniformly at random. Repeat and average, since a single random draw isn't a fair comparison.
- **Method 2 — Centrality-based:** select the top-B locations in **L** ranked by `Central(v)` alone. State explicitly that this is betweenness centrality specifically, and cite (without needing to implement) the finding that role-aware centrality variants exist and may outperform this (source 237) — naming the limitation is stronger than ignoring it.
- **Method 3 — Proposed:** solve the optimization in Section 5 via:
  - **Primary:** greedy algorithm. **It carries NO approximation guarantee, and this must be stated plainly (D20, D23).** After the D20 normalisation, **F(x) is submodular but not monotone** — verified by exhaustive enumeration, and necessarily non-monotone because Risk and Cost are subtracted. The classical (1−1/e) bound requires *monotone* submodular maximisation under a cardinality constraint, so it does **not** apply to F(x), and it does **not** apply to plain greedy on F(x). Worse than merely unproven: source #353's Appendix A, *"Greedy Performs Arbitrarily Poorly"*, constructs an instance on which standard greedy's ratio on f = g − c is **unbounded**. Plain greedy is retained as the primary *reported* method because it is the standard practitioner heuristic and because the exact MILP validates it at testbed scale — not because it is guaranteed. **On the seeded candidate set that validation holds by construction (D25):** every attack path meets exactly one candidate, so the gain part is modular and greedy is exactly optimal whatever the weights. It shows the implementation is correct, not that the heuristic searches well. **The distorted-greedy bound below must never be transferred to it.**
    - **(iii) — ADOPTED (D23).** Cite **Harshaw, Feldman, Ward & Karbasi (2019)**, source #353, and run their **Distorted Greedy** as a fifth method. Our objective is exactly their form, **f = g − c**, with `g = α·Coverage + β·Early + γ·CritProt` monotone submodular and non-negative, and `c = δ·Risk + ε·Cost` modular and non-negative. Then **g(S) − c(S) ≥ (1 − e^−γ)·g(OPT) − c(OPT)** in O(nk) evaluations, deterministically. Our g is genuinely submodular rather than weakly submodular, so **γ = 1** and the bound is **(1 − 1/e) ≈ 0.632**. All five preconditions are *verified on the frozen instance*, not argued from composition, by `scripts/structure_check.py` — which tests the aggregate g and c directly and tests c for **modularity**, not merely submodularity. The paper also proves a **matching hardness result**: no polynomial-time algorithm with value-oracle access to g can beat (1 − e^−γ), and value-oracle access is our access model, so this is the best bound obtainable rather than merely one we hold. Implemented as `distorted_greedy` in `src/optimizer/baselines.py`, exposed as `proposed_distorted_greedy`.
    - **(i) — SUPERSEDED by (iii).** The regularised result for f = g − ℓ attributed to Sviridenko, Vondrák & Ward. Rejected on practicality, not correctness: their algorithm requires continuous optimisation of the multilinear extension. Source #354 records that this characterisation comes from #353's related-work discussion and that their paper was never obtained, so nothing may be claimed about *their* theorem specifically. A27, which existed to verify this route, is closed by (iii).
    - **(ii) — available, not adopted.** Reformulate: maximise the monotone submodular gain part subject to Σ x_l ≤ B *and* Σ r_l·x_l ≤ R_max, moving risk from penalty to constraint. The classical guarantee then applies cleanly, at the cost of one extra parameter. Kept on the record as a fallback; unnecessary now that (iii) gives a guarantee without changing the problem statement.
    - Before D20 the question was moot: F(x) was **not submodular at all** — 57 submodularity violations on the frozen four-path instance (18 on the three-path instance those figures were originally measured on, D24), driven entirely by the Early mean — so no guarantee of any kind was available. Report this honestly; it is a genuine finding, not an embarrassment.
    - **Honest statement of what the guarantee buys, measured.** Distorted greedy is **beaten by plain greedy in 3 of the 20 cells of the comparison grid**, all under δ=3 (17.1%, 25.4% and 11.4% below optimum at B=2, 3 and 4). A declined iteration is never retried, and the early distortion factor can forfeit a budget slot. Under D24's normalisation it was 2 cells, 34.2% at B=2 default and 11.4% at B=4 δ=3; D25 changed the normalisation, not the algorithm. The guarantee is a worst-case **floor**, not competitive average-case performance. It earns its place through the *scalability* claim — instances too large for MILP validation — not through these results, where plain greedy equals the exhaustive optimum in all 20 cells (D24). See `scripts/sweep.py`, which holds the comparison grid as a constant.
  - **Validation:** exact MILP formulation at testbed scale (tractable per source 296's precedent), used to report an optimality gap against the greedy result, not as the primary method

All three methods are run against the same **P** and compared on: Coverage, Early, CritProt, Cost, and wall-clock computation time.

## 8. Research Questions, Restated Formally

**Primary (rephrased at D20):** Does Method 3 achieve a higher composite objective **F(x)** than Methods 1 and 2 across the attack scenario set **P** and across a range of objective weightings — and, specifically, achieve equal or greater **Coverage(x)** and **CritProt(x)** at equal or lower **Cost(x)**?

*Why rephrased.* The original wording asked only about Coverage and Cost, two of the five terms. A method that deliberately trades raw coverage against operational risk — which is the entire point of this work — can lose on that phrasing while being the better answer. Asking about the composite objective *and* retaining the checkable coverage-at-cost clause keeps the question falsifiable without understating the contribution. The original wording is preserved here rather than deleted, because the results chapter reports against both.

> ⚠️ **Open under A12 — read before the evaluation campaign (D24; figures below are D24's, updated by D25 at the end).** On the testbed instance, greedy equals the exhaustive optimum in all 20 cells of the comparison grid, so it cannot score lower on F than any other placement. **The first clause above ("a higher composite objective F(x)") is therefore implied by optimality at this scale**: it measures search quality, not whether F is a good objective, because F is both what is maximised and the yardstick. **The second clause — equal or greater Coverage and CritProt at equal or lower Cost — holds in 16 of 20 cells and fails in 4**, all of them cells where greedy deploys fewer decoys than the budget allows. The wording above is deliberately left unchanged here: rephrasing it, and choosing an evaluation criterion that is not F itself, is A12's decision and must be settled before Phase D runs.
>
> **Updated by D25.**
> - **The first clause is implied by construction on the seeded candidate set,** not merely by optimality at small scale. Every attack path meets exactly one candidate, so the gain part is modular and greedy is exactly optimal. On that set the comparison cannot speak to search quality either.
> - **The second clause now holds in 20 of 20 cells.** This is not an improvement in the method. The four failures were declines, and those declines were produced by dividing Risk and Cost by B. Under D25's fixed divisor the grid record is 5 wins / 15 ties / 0 losses, with no declines.
> - **The 20 of 20 is fragile.** The grid's δ=3 sits just below δ ≈ 3.03, where the first decoy's value turns negative. At δ=3.05 greedy already declines at B=4 and the clause fails.
> - **D25 also fixes what the thesis may claim, before the candidate set is corrected:** the formulation, its verified structure, the objective's two distinct disagreements with centrality, and an exact implementation — and not search quality, distorted greedy's practical value, or held-out-path robustness while the gain part stays modular.

**Secondary:** Can a local LLM, given `(x*, F(x*), Coverage/Early/CritProt/Risk/Cost breakdown, comparison to Methods 1–2)` as structured input, generate an analyst-readable explanation of *why* each `l` with `x_l = 1` was selected — without altering `x*` itself? (Architecture precedent: sources 244, 255, 257 — planner decides, LLM explains, and the planning formalism has already been shown to transfer to OT-adjacent topologies.)

## What This Enables Next

With this specification fixed, the next artifacts become well-defined rather than open-ended:
- **Threat/attack model** — formalize the specific paths in **P** (Section 3) with real ATT&CK-for-ICS technique IDs
- **Testbed architecture** — map **V**, **E**, and zones directly onto the VMware/Kali/pfSense/OpenPLC/Node-RED build
- **Data model** — the schema for storing **G**, **P**, **L**, and computed scores (SQLite, per the original brief)
- **Evaluation methodology** — the exact procedure for running Methods 1–3 against **P** and reporting results
