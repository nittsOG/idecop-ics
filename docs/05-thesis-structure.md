# Thesis Structure and Writing Plan

Defines the chapter structure for the final project report, what each chapter contains, which existing document supplies its material, and the order in which to write them. This is the plan document, not the thesis — chapter drafts live in separate `05-*` files.

**Template caveat.** The institutional template is not yet available. Everything below is structured to survive that: chapter *content* and *order* rarely change between templates, while front matter, numbering conventions, citation style and margins always do. Those template-dependent items are isolated in §6 so that only that section needs revisiting.

---

## 1. The central fact about this thesis

Most of it is already written.

Eleven specification and research documents exist, produced during Phases A and B, containing the problem definition, the threat model, the testbed design, the optimisation formulation, the AI architecture and a decisions log recording the rationale for every significant choice. The writing task is therefore **transformation, not creation**: converting working documents into thesis prose, adding the connective argument, and filling genuine gaps.

Two consequences follow:

- The Literature Review and Methodology chapters are draftable now, before the build finishes. Leaving them until after Phase D is the largest avoidable schedule risk in the project.
- The decisions log is an unusual asset. Most students reconstruct their rationale months later from memory. Here, every design choice has a dated record of what was considered, what was chosen, and why — including the choices that turned out to be wrong. That is what makes a Methodology chapter defensible under questioning rather than merely descriptive.

---

## 2. Chapter structure

Six chapters. This is the standard shape for an M.Tech project report and maps cleanly onto the existing material.

### Chapter 1 — Introduction
**Purpose:** establish the problem and why it matters, before any technical content.
**Target: 8–10 pages.**

| Section | Content | Source |
|---|---|---|
| 1.1 | Background — OT/ICS security, why detection is constrained in OT | New writing; NIST SP 800-82 grounding |
| 1.2 | Cyber deception as a detection mechanism | `01-thesis-citation-shortlist.md` §III |
| 1.3 | Motivation — placement determines value | `01-original-brief.md` §2 |
| 1.4 | Problem statement | `formal-problem-definition.md` |
| 1.5 | Research questions, primary and secondary | `formal-problem-definition.md` §8 |
| 1.6 | Scope and boundary — what this is not | `01-original-brief.md` §4 |
| 1.7 | Contributions | Synthesised from the whole |
| 1.8 | Report organisation | Written last |

**Note:** §1.6 is not padding. The boundary is the most common misreading of this project, and stating it in the introduction prevents the examiner from spending the viva on a question you already answered.

---

### Chapter 2 — Literature Review
**Purpose:** establish what exists, what does not, and where this work sits.
**Target: 15–18 pages. Status: substantially drafted for TA-1.**

| Section | Content | Source |
|---|---|---|
| 2.1 | Review methodology and its stated limitations | TA-1 §2.1 |
| 2.2 | OT/ICS deception systems — generation and fidelity | Shortlist §III |
| 2.3 | Placement optimisation in enterprise IT and adjacent domains | Shortlist §II |
| 2.4 | Deception placement in OT — the closest prior art | Shortlist §I |
| 2.5 | Criticality scoring methods | Shortlist §VI |
| 2.6 | Candidate feasibility and decoy detectability | Shortlist §VII |
| 2.7 | Deterministic planning with model-generated explanation | Shortlist §II (SPEAR, i-EXAM) |
| 2.8 | Standards and frameworks — IEC 62443, ATT&CK for ICS, NIST 800-82 | Shortlist §IV |
| 2.9 | Comparative summary table | TA-1 §2.3 |
| 2.10 | Research gap | TA-1 §3 |

**The one section that needs care:** 2.4. Jay (2023) requires a full paragraph arguing the three distinctions explicitly — single VLAN versus multi-zone, IEC 61850 versus IEC 62443, equilibrium over decoy type versus composite multi-metric objective. Rowe (2025) needs its own disambiguation, being the closest-*sounding* work. Everything else in the chapter can be grouped and summarised.

---

### Chapter 3 — Methodology and System Design
**Purpose:** the formal core. This is where the contribution is stated precisely enough to be checked.
**Target: 15–18 pages. Status: draftable now — Phase B is closed.**

| Section | Content | Source |
|---|---|---|
| 3.1 | Overall approach and system architecture | `02-prototype-architecture.md`, `02-system-flow.md` |
| 3.2 | Network model — G, zones, conduits, Purdue levels | `formal-problem-definition.md` §1 |
| 3.3 | Asset criticality formulation | `formal-problem-definition.md` §2 |
| 3.4 | Threat model and attack path construction | `threat-attack-model.md` |
| 3.5 | Candidate location derivation — both filters | `formal-problem-definition.md` §4 |
| 3.6 | Objective function and constraints | `formal-problem-definition.md` §5–6 |
| 3.7 | Optimisation methods — greedy, exact, and the submodularity argument | `02-optimization-formulation.md` |
| 3.8 | Baseline methods and rationale | `formal-problem-definition.md` §7 |
| 3.9 | AI role — the decide/explain separation | `02-ai-role.md` |
| 3.10 | Testbed architecture | `testbed-architecture.md` |
| 3.11 | Design decisions and their justification | `00-decisions-log.md` |

**§3.11 is the differentiator.** Rather than presenting choices as inevitable, it presents them as decisions with alternatives that were considered and rejected — including D16, where the originally specified MILP formulation was wrong and was caught by implementing it. Reporting that strengthens the chapter; concealing it would be both dishonest and weaker.

---

### Chapter 4 — Implementation
**Purpose:** demonstrate that the design was realised, and describe how.
**Target: 12–15 pages. Status: writable in parallel with the remaining build.**

| Section | Content | Source |
|---|---|---|
| 4.1 | Technology stack and rationale | `01-original-brief.md` §8 |
| 4.2 | Data model and schema | `02-data-model.md` |
| 4.3 | Graph model implementation | `src/graph_model/` |
| 4.4 | Optimiser implementation — all four methods | `src/optimizer/` |
| 4.5 | API layer and contract | `src/api/main.py` |
| 4.6 | User interface — three screens | `src/frontend/` |
| 4.7 | Explanation layer | `02-ai-role.md` — pending build |
| 4.8 | Plausibility-scoring assist | `02-ai-role.md` — pending build |
| 4.9 | Testbed deployment | Pending build |
| 4.10 | Verification and issues encountered | `00-decisions-log.md` D14–D19 |

**§4.10 is worth writing deliberately.** Three substantive problems surfaced only when the specification was built against: the unseeded graph, the incorrect MILP proxy, and the behaviour of the earliness term as a mean. These constitute a real argument for incremental verification, and they are the kind of content that distinguishes an implementation chapter from a manual.

---

### Chapter 5 — Results and Analysis
**Purpose:** answer the research questions with evidence.
**Target: 12–15 pages. Status: blocked on Phase D.**

| Section | Content |
|---|---|
| 5.1 | Experimental setup — testbed, paths, candidates, budget range |
| 5.2 | Evaluation metrics and their definitions |
| 5.3 | Comparative results across all four methods |
| 5.4 | Weight sensitivity sweep |
| 5.5 | Optimality gap — greedy against the exact solver |
| 5.6 | Explanation layer assessment |
| 5.7 | Discussion — what the results do and do not support |
| 5.8 | Threats to validity |

**Two things to settle before writing.** First, the primary research question asks whether the proposed method achieves higher coverage and criticality protection than the baselines. Current output shows it winning on the composite objective while covering fewer paths, because the objective charges for risk and cost that the baselines ignore. Either the question is rephrased to ask about the objective-defined tradeoff, or the normalisation issues in the risk and criticality terms are resolved first. Second, §5.8 must exist. A results chapter without a threats-to-validity section invites the examiner to supply one.

---

### Chapter 6 — Conclusion and Future Work
**Purpose:** state what was achieved, honestly, and what follows.
**Target: 5–6 pages.**

| Section | Content |
|---|---|
| 6.1 | Summary of contributions |
| 6.2 | Answers to the research questions, stated plainly |
| 6.3 | Limitations |
| 6.4 | Future work |

**§6.4 has substantial material already** — `04-deployment-requirements.md` §7 lists six open problems: exact-solver scalability, topology drift, validation methodology, criticality elicitation at scale, quantitative detectability measurement, and safety analysis of decoys on live control segments. Naming these precisely is stronger than a vague gesture at "further research."

---

## 3. Front and back matter

Template-dependent in *format*, but the list is standard:

**Front:** title page · certificate · declaration · acknowledgement · abstract · table of contents · list of figures · list of tables · list of abbreviations.

**Back:** references · appendices.

**Abbreviations list** is worth taking seriously here — this project uses a lot of them (OT, ICS, SCADA, PLC, HMI, RTU, IED, DMZ, SL, FR, MILP, CP-SAT, ATT&CK, LLM). `00-glossary.md` already contains the expansions; the list is an extraction task, not a writing task.

**Suggested appendices:**

| Appendix | Content | Source |
|---|---|---|
| A | Full attack path specifications with technique IDs | `threat-attack-model.md` |
| B | Database schema | `data/schema.sql` |
| C | API endpoint reference | `src/api/main.py` |
| D | Plausibility rubric scores per candidate | `data/` seed + review output |
| E | Full sensitivity sweep results | Phase D output |
| F | Glossary | `00-glossary.md` |

---

## 4. File naming and organisation

Per the project's existing convention, one canonical file per chapter:

```
05-ch1-introduction.md
05-ch2-literature-review.md
05-ch3-methodology.md
05-ch4-implementation.md
05-ch5-results.md
05-ch6-conclusion.md
05-front-matter.md
05-appendices.md
```

Same rules as every other document in this project: corrections happen in place, never in a `-v2` copy; each file gets a registry row in `00-project-index.md` when created.

**Assembly happens once, late.** Draft in markdown, convert to the institutional template format at the end. Drafting directly in the template means fighting formatting on every edit, and the template is not available yet in any case.

---

## 5. Writing order and sequencing

Ordered by *readiness*, not by chapter number.

| Order | Chapter | When | Blocked by |
|---|---|---|---|
| 1 | Ch 2 — Literature Review | Now — substantially done via TA-1 | Nothing |
| 2 | Ch 3 — Methodology | Now | Nothing; Phase B is closed |
| 3 | Ch 4 — Implementation, §4.1–4.6 | Now | Nothing; those components are built |
| 4 | Ch 4 — §4.7–4.9 | After the remaining build | Explanation layer, notebook, VMs |
| 5 | Ch 5 — Results | After Phase D | Full evaluation campaign |
| 6 | Ch 1 — Introduction | Late | Easier once the contributions are settled |
| 7 | Ch 6 — Conclusion | Last | Results |
| 8 | Front matter, appendices, assembly | Last | Template |

**Why the Introduction is written late.** It reads as though it comes first, but a good introduction promises exactly what the thesis delivers. Writing it before the results are known produces either vague promises or promises that have to be walked back.

**Immediate priority order, given weekend hours:**

1. TA-1 submission — 21 September, fixed
2. Chapter 3 draft — the largest chapter that is fully unblocked
3. Resolve the risk/criticality normalisation question — this blocks Phase D, which blocks Chapter 5
4. Chapter 4 §4.1–4.6 — while the implementation details are fresh
5. Everything else in readiness order

---

## 6. Template-dependent items — revisit when the template arrives

Isolated here so that only this section needs changing:

- Page size, margins, line spacing, font
- Heading numbering depth and style
- Figure and table caption position and numbering scheme
- Citation style — IEEE numeric is assumed above; confirm
- Reference list format
- Whether chapter-end or thesis-end references are required
- Front matter wording and order, certificate and declaration text
- Page limit, if any — the targets above total roughly 70–90 pages plus appendices
- Whether an abstract keyword list is required
- Plagiarism-check requirements and threshold

---

## 7. Writing conventions to apply throughout

Carried over from the project's own rigor rules, and worth stating once rather than deciding repeatedly:

- **Confidence language is explicit.** Verified, likely and unconfirmed are different claims. Write which one applies.
- **Every claim traces to a source or a result.** If neither exists, it does not go in.
- **Negative findings are reported.** D16's incorrect formulation, the earliness term's behaviour, and any unfavourable comparison in Chapter 5 are all reported as found.
- **The novelty claim is stated at its defensible strength** — sparsely populated with a meaningfully narrower closest occupant, never "nobody has done this."
- **Figures are captioned and referenced in text.** A figure nobody points at is decoration.
- **First use of every acronym is expanded**, in each chapter, not only the first time in the document.

---

## 8. What is missing and needs deciding

Recorded so it does not surface late:

1. **Actual final submission deadline.** The ordering above is relative; converting it to dates requires the real date.
2. **Four incomplete references** flagged in the TA-1 document, including the sole source for weighting operational risk.
3. **The institutional database review** — still the one systematic gap in Chapter 2's methodology.
4. **Whether Chapter 5 can be written at all** under the current objective formulation, per the note in §2 above. This is the highest-priority technical decision outstanding.
