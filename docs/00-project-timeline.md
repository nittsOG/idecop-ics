# Project Timeline and Work Breakdown

Schedule for the remainder of the project, from 14 September 2026 to final submission. Built around weekend-only availability, with effort stated in weekend-units rather than calendar weeks so that a missed weekend shows up as a real cost rather than disappearing into a vague estimate.

**Planning unit.** One *weekend-unit* (WU) = one productive Saturday plus Sunday, roughly 10–12 working hours. Weekday evenings are counted separately and only for tasks that genuinely fit into a 60–90 minute block — reference chasing, proofreading, small fixes. Substantial work does not fit in a weekday evening and is not scheduled there.

**Known fixed date:** TA-1 submission, Monday 21 September 2026.
**Unknown, needs filling:** TA-2, TA-3 (if applicable), final thesis submission, viva. §6 lists these as the first thing to confirm with the guide.

---

## 1. The immediate problem: one weekend to TA-1

From today, the available time before submission is:

| Day | Date | Available | Use |
|---|---|---|---|
| Mon–Fri | 14–18 Sep | Weekday evenings only | Small, bounded tasks |
| **Sat–Sun** | **19–20 Sep** | **One full weekend-unit** | The only substantial working block |
| Mon | 21 Sep | Submission day | Buffer and submit |

The TA-1 document is drafted. What remains is completion and verification, not writing — which is why one weekend is sufficient, but only just.

### Plan for the nine days

| When | Task | Effort |
|---|---|---|
| Tue 15 Sep, evening | Confirm guide's name and title; fill the title block. Confirm from the guide whether IEEE citation style applies, and whether a template exists yet | 1 hr |
| Wed 16 Sep, evening | Chase reference [23] — the D3O-IIoT paper. This is the sole source justifying heavy operational-risk weighting and is currently uncitable. The PMC link is recorded in `sources.md` | 1.5 hr |
| Thu 17 Sep, evening | Complete references [12] and [26] — the GNN placement paper and the criticality-analysis patent number | 1.5 hr |
| Fri 18 Sep, evening | Read the TA-1 document end to end as a reader, not as its author. Mark, do not fix | 1 hr |
| **Sat 19 Sep** | Apply Friday's marks. Expand §2.4 — the Jay differentiation needs to be argued, not asserted. Verify every reference number in the table matches §6 | 5–6 hr |
| **Sun 20 Sep** | Final read. Convert to PDF. Check pagination, table breaks, and that no placeholder text survives. Prepare a two-minute verbal summary in case the submission is discussed | 4 hr |
| Mon 21 Sep | Submit | — |

**If the weekend is lost**, the minimum viable submission is: title block completed, asterisked references either resolved or explicitly marked as pending, and a single careful proofread. The document is submittable in that state. Everything else on the list is improvement, not requirement.

---

## 2. Work breakdown — everything remaining

Effort estimates are honest rather than optimistic. Each includes verification, not just first-pass completion.

### Build work (Phase C completion)

| # | Task | WU | Depends on | Notes |
|---|---|---|---|---|
| B1 | Resolve the risk/criticality normalisation question; re-run all methods; update the formulation document | 1 | — | **Blocks Phase D.** Highest priority technical item |
| B2 | Explanation layer — Ollama integration, prompt implementation, endpoint, evaluation criteria | 2 | B1 | Needs local inference working; allow for model-fitting friction |
| B3 | Colab plausibility notebook — prompt, batch scoring, output into the candidate table | 1 | — | Independent; can slot into any weekend |
| B4 | Screen 2 — sensitivity sweep comparison view | 1 | D1 partially | Only meaningful once multiple runs exist |
| B5 | Physical testbed — 7 VMs, pfSense conduit rules, OpenPLC, Node-RED, network segmentation | **3–4** | — | The largest single item. Historically the most underestimated part of OT projects |
| B6 | Repository hygiene — README correction, `requirements.txt`, remove the publisher PDF, commit history | 0.5 | — | Small but affects how the artefact is judged |

**Build subtotal: 8.5–9.5 WU**

### Evaluation (Phase D)

| # | Task | WU | Depends on |
|---|---|---|---|
| D1 | Full evaluation campaign — all methods, all paths, all budget values | 1 | B1 |
| D2 | Weight sensitivity sweep across the coefficient grid | 1 | D1 |
| D3 | Results analysis, comparison tables, charts | 1 | D2 |

**Evaluation subtotal: 3 WU**

### Writing (Phase E)

| # | Task | WU | Depends on |
|---|---|---|---|
| W1 | Chapter 3 — Methodology | 2 | Nothing — fully unblocked |
| W2 | Chapter 4 §4.1–4.6 — Implementation, built components | 1.5 | Nothing |
| W3 | Chapter 4 §4.7–4.10 — remaining components and issues encountered | 1 | B2, B3, B5 |
| W4 | Chapter 2 — expand TA-1 material to full chapter length | 1 | TA-1 |
| W5 | Chapter 5 — Results and Analysis | 2 | D3 |
| W6 | Chapter 1 — Introduction | 1 | W5 |
| W7 | Chapter 6 — Conclusion and Future Work | 0.5 | W5 |
| W8 | Front matter, appendices, figure production | 1.5 | Template |
| W9 | Template conversion, formatting, assembly | 1 | Template |

**Writing subtotal: 11.5 WU**

### Review and submission (Phase F)

| # | Task | WU |
|---|---|---|
| R1 | Guide review cycle 1 and revisions | 1 |
| R2 | Guide review cycle 2 and revisions | 1 |
| R3 | Plagiarism check and corrections | 0.5 |
| R4 | Viva preparation — slides, anticipated questions, demo rehearsal | 1 |

**Review subtotal: 3.5 WU**

---

## 3. Totals and what they mean

| Category | WU |
|---|---|
| Build | 8.5–9.5 |
| Evaluation | 3 |
| Writing | 11.5 |
| Review and submission | 3.5 |
| **Subtotal** | **26.5–27.5** |
| Contingency at 20% | 5.5 |
| **Total** | **32–33 WU** |

At one weekend-unit per week with no losses, that is **roughly 32 weeks — about seven and a half months.**

**This needs saying plainly.** Weekends are lost to travel, illness, work obligations and festivals. A realistic completion rate is three weekend-units per month, not four. At that rate the total is closer to eleven months. If the final submission is earlier than that, scope has to be reduced deliberately now rather than abandoned in a panic later.

**The two candidates for scope reduction**, in order of preference:

1. **The physical testbed (B5, 3–4 WU).** The optimiser operates entirely on the modelled graph; the VMs are needed for demonstration and post-placement validation, not for the placement algorithm or for Phase D results. Reducing to three or four VMs covering one zone boundary, with the rest modelled, saves 2 WU and costs little in the evaluation. This is a defensible scope decision and would be recorded as such.
2. **The Colab plausibility notebook (B3, 1 WU).** The rubric can be scored by hand for eleven assets. The AI-assist is a genuine contribution to the AI narrative, so cutting it has a real cost — but it is the cheapest thing to cut that does not affect the core claim.

The explanation layer (B2) should not be cut. It is the secondary research question.

---

## 4. Sequencing

Dependencies, not calendar dates. Start dates follow from whatever the actual submission deadline turns out to be.

```
NOW ──▶ TA-1 (21 Sep, fixed)
          │
          ▼
    B1 normalisation decision  ◀── highest priority after TA-1
          │
          ├──▶ W1 Ch3 Methodology ──┐  (can run in parallel — writing
          │                          │   and building use different energy)
          ├──▶ B2 Explanation layer  │
          ├──▶ B3 Colab notebook     │
          ├──▶ B5 Testbed VMs        │
          │                          │
          ▼                          ▼
    D1 ▶ D2 ▶ D3 Evaluation    W2 Ch4 (built parts)
          │                          │
          ▼                          ▼
    W5 Ch5 Results ◀────────── W3 Ch4 (remainder)
          │
          ▼
    W6 Ch1 ▶ W7 Ch6 ▶ W4 Ch2 expansion
          │
          ▼
    W8 front matter ▶ W9 assembly  ◀── needs template
          │
          ▼
    R1 ▶ R2 ▶ R3 ▶ R4 ▶ SUBMIT
```

**Two sequencing rules worth following deliberately:**

- **Alternate building and writing weekends.** They use different kinds of attention, and alternating prevents the common failure where all the code is written and no chapter exists.
- **Never let the guide's first sight of a chapter be the final draft.** Build R1 and R2 into the schedule as real items, because a review cycle that surfaces a structural problem late costs far more than the review itself.

---

## 5. Milestones to agree with the guide

| Milestone | Suggested content | Date |
|---|---|---|
| TA-1 | Literature review, gap, proposed work | **21 Sep 2026 — fixed** |
| M1 | Normalisation resolved; Chapter 3 draft delivered | TA-1 + 6 weeks |
| M2 | Phase C complete; Chapter 4 draft delivered | M1 + 8 weeks |
| M3 | Phase D complete; Chapter 5 draft delivered | M2 + 6 weeks |
| M4 | Full draft delivered for review | M3 + 5 weeks |
| M5 | Revisions complete; plagiarism check passed | M4 + 4 weeks |
| Final | Submission and viva | To confirm |

Dates here are intervals, not commitments, because the terminal date is unknown. Fixing the terminal date converts every interval above into a real deadline and is the single most useful thing to do at the next guide meeting.

---

## 6. First actions after TA-1

In order:

1. **Confirm the final submission date, TA-2 and TA-3 dates, and obtain the template.** Everything in this document is provisional until these exist.
2. **Resolve B1** — the normalisation question. It blocks the evaluation, which blocks the results chapter, which blocks the conclusion.
3. **Start Chapter 3** — the largest fully unblocked writing task.
4. **Request institutional database access** for the systematic review. It has a lead time outside your control, so it should be requested early even though the work itself is later.

---

## 7. Risk register

| Risk | Likelihood | Impact | Response |
|---|---|---|---|
| Testbed build overruns | High | Medium | Pre-agreed scope reduction to a single zone boundary (see §3) |
| Phase D results do not support the primary question | Medium | High | Agree with the guide *now* that an honestly reported negative result is acceptable; rephrase the question if the tradeoff framing is more accurate |
| Template arrives late or imposes a page limit | Medium | Medium | Draft in markdown, convert once; content is format-independent |
| Local inference does not run acceptably on available hardware | Medium | Medium | Explanation layer degrades to a template-based fallback; the architecture already permits this |
| Systematic database review not obtainable | Medium | Low | Already handled — the review's limitation is stated explicitly in Chapter 2 rather than concealed |
| Weekend availability worse than assumed | High | High | Scope reduction decided deliberately at M2, not improvised at M4 |
| Guide requests major direction change at first review | Low | High | Deliver Chapter 3 early, at M1, so any structural objection surfaces while there is time to act |
