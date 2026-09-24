# Commercial Prior Art — Acalvio's Placement Method Analysed

Deep dive requested after iteration 13 flagged Acalvio ShadowPlex as the sharpest challenge to the novelty claim. Iteration 13 concluded from marketing material that Acalvio recommends decoy *attributes* rather than *positions*. **That conclusion was incomplete, and this document corrects it.** A granted patent discloses an actual placement method.

---

## 1. The correction to iteration 13

Iteration 13 stated that the word "published" in the novelty claim was load-bearing, on the grounds that commercial capabilities are proprietary and unexaminable.

**That reasoning is wrong for this case. A granted patent is a published document with a disclosed method.** The defence cannot be "it isn't published." It has to be a method-level distinction, which — fortunately — is available and is stronger.

This is worth recording as a reasoning error, not just a fact update. The lesson: *checking the marketing and concluding there is no method is not the same as checking the patents.* Marketing describes what a product does for a buyer; patents describe what it does mechanically. They are different corpora and the second is the one that constitutes prior art.

---

## 2. The patent

**US 9,853,999 B2 — "Context-aware knowledge system and methods for deploying deception mechanisms"**
Assignee: Acalvio Technologies, Inc.
Inventors: Satnam Singh, Nirmesh Neema, Suril Desai, Venkata Babji Sama, Rajendra Gopalakrishna
Provisional 62/328,224 filed 27 April 2016; application filed 3 February 2017; granted 26 December 2017.
Application publication US 2017/0318053.

### The disclosed method, step by step

A component called a **deception profiler** decides deployment as follows:

1. **Identify a network** to deploy into. Options disclosed: receive an identification; select randomly from several networks; compute asset densities for each and take the **highest**; or rank by an **importance score** computed from asset densities plus machine information such as asset types.

2. **Compute asset densities.** Defined explicitly as a ratio:
   - *general density* = assets in a portion of the site network ÷ total assets in the site network
   - *critical density* = critical assets in that portion ÷ total critical assets in the site network

   Both may be used together.

3. **Compute a summary statistic** over the **number of historical attacks** on that network.

4. **Determine the number of deception mechanisms to deploy**, from the densities, the summary statistic, and other network information.

5. **Deploy that number.**

### What the method actually outputs

**A count of decoys for a chosen subnetwork.** Not a set of positions.

The decision variables are *which subnet* (by density or importance ranking) and *how many decoys go there* (by a function of density and historical attack volume). Nothing in the disclosed method selects individual assets within a topology, and nothing evaluates where along an attack sequence a decoy would intercept.

---

## 3. Comparison against iDECOP-ICS

| Dimension | US 9,853,999 | This project |
|---|---|---|
| **Decision made** | Which subnet, and how many decoys | Which specific positions — a binary variable per candidate location |
| **Output** | A count | A set `x*` |
| **Budget** | Not a constraint — the count *is* the output | Hard constraint, Σ x_l ≤ B |
| **Objective function** | None disclosed | Explicit F(x), five weighted terms, maximised |
| **Optimisation** | None — a heuristic rule producing a number | Constrained combinatorial optimisation: greedy, distorted greedy, exact MILP |
| **Guarantee** | None | Submodularity verified by exhaustive enumeration; distorted greedy carries a proven bound |
| **Threat model** | A *count* of historical attacks, as a summary statistic | Ordered attack paths with verified ATT&CK for ICS techniques; interception **stage** is scored |
| **Early detection** | Absent | Explicit term — and the term with the strongest independent justification |
| **Operational risk** | Absent | Explicit term, weighted heavily on published ablation evidence |
| **Decoy detectability** | Absent from this patent | Filter 2 — candidates down-weighted by exposure |
| **Criticality** | Present, as a **count ratio** of critical assets | IEC 62443 Security Level vector × operational damage share × centrality, plus conduit exposure |
| **Standards structure** | None — subnets and address ranges | IEC 62443 zones and conduits as numeric inputs |
| **Candidate filtering** | None — all subnets eligible | Two-filter plausibility and detectability screen |
| **Domain** | Enterprise IT | OT/ICS — Purdue levels, industrial protocols |
| **Validation** | None disclosed | Random and centrality baselines, identical attack set, weight sweep, optimality gap |
| **Reproducible** | Method disclosed; no data, code or results | Open repository, seed data, scripts, reproducible on a clean machine |

### Where it is genuinely closer than anything else found

Three points, stated plainly because pretending otherwise would be the weaker position:

1. **It is criticality-aware.** "Critical asset density" is a real, if coarse, criticality input — the closest analogue to CritProt found in commercial prior art.
2. **It is threat-informed.** Historical attack counts are an empirical threat signal, analogous in *spirit* to using attack paths, though not in structure.
3. **It is automated end to end.** No human decides where decoys go.

So this is a genuine placement heuristic informed by criticality and threat history. In *intent* it is closer to this project than TrapManager. In *method* it is far simpler.

---

## 4. Does it break the novelty claim?

Clause by clause:

| Clause | Status against US 9,853,999 |
|---|---|
| "formal, quantitative … optimisation" | **Holds.** The patent is quantitative but is not an optimisation — there is no objective, no feasible set, nothing maximised |
| "across a multi-zone OT/ICS architecture" | **Holds.** Subnets in enterprise IT, not IEC 62443 zones |
| "using IEC 62443 zone and conduit structure" | **Holds.** Entirely absent |
| "asset criticality as a first-class input" | **Weakest clause.** Critical-asset density is a criticality input. This clause alone does not distinguish the work |
| "composite objective" | **Holds.** No objective function exists to compose |
| "validated against baseline placement strategies" | **Holds.** No comparison disclosed |

**Verdict: the claim survives, and the surviving distinction is the objective function itself.** The patent decides *how many* decoys to put in the *densest or most-attacked* subnet. This project decides *which* positions maximise a stated, weighted, multi-term security objective under a budget — and then proves the result against baselines.

**The one-line answer to "hasn't Acalvio patented this?":**

> *"They patented a heuristic for how many decoys to place in which subnet, driven by asset density and historical attack counts. There is no objective function, no budget constraint, no notion of when along an attack path an interception occurs, and no zone or conduit structure. My work optimises which positions to use against a five-term objective and validates it against baselines."*

---

## 5. Actions this forces

1. **Cite US 9,853,999 explicitly in section 14 and add it to the literature table.** Treating it openly is far stronger than hoping an examiner does not find it. Patents are already in scope as prior art in this project — Jay's patent and the criticality-analysis patent are both cited.
2. **Strengthen the criticality clause.** Since critical-asset *density* is the weakest point of separation, the claim should emphasise what makes this project's criticality different: a standards-derived Security Level vector combined with operational damage share and conduit exposure, not a count ratio.
3. **Do not lean on the word "published."** It does not do the work iteration 13 assigned it. The method-level distinction does.
4. **Search more patents.** This one surfaced from a single query. Acalvio holds over 25 granted US patents; Commvault, Fortinet, SentinelOne/Attivo and Proofpoint/Illusive hold more. One incidental find already noted: **US 12,375,527** describes a deception host deployment module that "may also recommend suitable deception hosts and its appropriate placement in the private network based on historical knowledge of the attack and attack types." A systematic patent sweep is now a genuine gap, comparable in importance to A17. **Logged as A29, and it does not need institutional credentials.**

---

## 6. Confidence

**Verified:** the patent exists, its assignee and inventors, its filing and grant dates, and the method as described in its own text.

**Not verified:** the formal claim language. This analysis rests on the abstract and the description of the process steps, not on a clause-by-clause reading of the granted claims. **The claims are what define legal scope**, and before section 14 states the comparison as settled, they should be read — the same standard applied to the Jay paper after its abstract proved misleading. Logged as part of A29.
