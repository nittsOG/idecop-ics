# Project Timeline and Work Breakdown

The work that remains, in weekend-units, from 26 November 2026 to final submission. Rebuilt by D45 without dates, because none of A14's dates is known. The September 2026 plan follows it, as history.

**Planning unit.** One *weekend-unit* (WU) = one productive Saturday plus Sunday, roughly 10–12 working hours. Weekday evenings are counted separately and only for tasks that genuinely fit into a 60–90 minute block — reference chasing, proofreading, small fixes. Substantial work does not fit in a weekday evening and is not scheduled there.

**Dates.** None is known (A14). TA-2 was scheduled for late November and will not take place for now (D45). TA-1, TA-3, the final submission, the viva and the template are unknown. Current position: `00-project-phases.md`.

---

## 1. Where things stand (26 November 2026)

- Phases A and B are complete.
- Phase C's software is built, except Screen 2. *[D46: Screen 2 is built.]* The physical testbed (A21) comes last (A16, D37).
- Phase D is complete: its primary question in D41, its secondary question in D44 (D45).
- Phase E, the thesis, is written in its own chat. How far it has got is not recorded here.
- Phase F has not started.

## 2. The remaining work

Where the September plan had an estimate, it is kept; that plan called its estimates honest rather than optimistic. The rest are Claude's. All are likely, not verified.

### 2.1 Before testing and tuning — about 2 WU

| # | Task | WU | Notes |
|---|---|---|---|
| N1 | The Dashboard's *Explain this placement* button with the real model (`04-setup-guide.md` §7.7) | about an hour | The last open part of A6. Needs the laptop *[D46: done; A6 is closed.]* |
| N2 | Screen 2, the sensitivity-sweep view, with `GET /runs/compare` | 1 | The last unbuilt screen (`02-prototype-architecture.md` §3; the September plan's B4). It is also where the tuning study is watched, so it comes before T1 runs *[D46: done.]* |
| N3 | `PUT /assets/{id}/damage-score`: build it or drop it, by decision | 0–0.25 | In the API's spec, never built. Damage has been a declared input since D33, so editing it only makes sense inside a tuning study *[D46: dropped.]* |
| N4 | Small documentation items: A28 (the novelty claim's wording), A24 (the threat model's detectability assumption), A33 (CATCH: choose an option), A18 (remove the publisher PDF, on your yes), A19 (close it: one commit per batch is now the practice) | 0.5 | Not blocking. The thesis needs A28 and A24 *[D46: A18 and A33 closed.]* |
| N5 | A thorough analysis of the project, in its own chat | not estimated | Your plan (D45 item 4). Its size depends on its scope. Anything it finds gets its own entry |

*D46, 26 November 2026: N2 and N3 are done, and A18 and A33 are closed, and N1 is done (A6 closed). What remains of this group: A19, A24 and A28, about half a WU, and the analysis chat.*

### 2.2 Testing and tuning — about 2.5 to 6.5 WU

| # | Task | WU | Notes |
|---|---|---|---|
| T1 | The tuning study: define what is tuned, against which measure, and checked on what; then run it and report it | 1–2 | A separately reported study; D41 and D44 stay the pre-registered results (D37 item 7, D45). Checked on the same paths and simulation it is tuned on, it would only fit the test |
| T2 | Optional: a third explanation check, for wrong comparisons | 0.5 | The text for B = 1 calls two equal scores "higher", and both checks pass it (D44 item 5) |
| T3 | The physical testbed (A21) | 3–4, or 1.5–2 | All seven VMs, or one zone boundary with the rest modelled (the September plan's B5 and its §3). Testbeds usually overrun |

### 2.3 After testing and tuning — up to about 15.5 WU

| # | Task | WU | Notes |
|---|---|---|---|
| W | The thesis: chapters, front matter and assembly (the September plan's W1–W9) | up to 11.5 | Less whatever the thesis chat has drafted |
| R | Guide review, plagiarism check and viva preparation (the September plan's R1–R4) | 3.5 | Review needs a full draft |
| S | A17's update re-run, within a month of submission | 0.5 | Its timing follows the submission date (A14) |

### 2.4 Totals

| Group | WU |
|---|---|
| Before testing and tuning | about 2, plus the analysis chat |
| Testing and tuning | 2.5–6.5 |
| After testing and tuning | up to 15.5 |
| Subtotal | 20–24 |
| Contingency at 20%, as in September | 4–5 |
| **Total** | **24–29** |

At the September plan's realistic rate of three weekend-units a month, that is eight to ten months if the thesis is still mostly unwritten, and less by whatever the thesis chat has drafted. If the submission date (A14) turns out earlier, the testbed is the first thing to reduce, as the September plan's §3 already said.

## 3. Order

Dependencies, not dates.
- *Next, by your plan:* the analysis chat (N5), then the testing-and-tuning chat (T1–T3).
- N1–N4 can go before or after the analysis. N2 comes before T1 runs.
- The testbed (T3) comes last (A16, D37).
- The thesis runs alongside, in its own chat. Guide review (R) needs a full draft, and A17's re-run (S) falls within a month of submission.

## 4. Risks now

| Risk | Likelihood | Impact | Response |
|---|---|---|---|
| Weekend availability is worse than assumed | High | High | Reduce the testbed first, by decision, early |
| The testbed overruns | High | Medium | One zone boundary instead of seven VMs (T3) |
| The tuning study is checked on what it was tuned on | Medium | High | T1 fixes the check data before it runs, and reports the study separately |
| The submission date arrives late, or early | Medium | High | A14. This breakdown converts to dates once it is known |
| The analysis finds a defect in the frozen code | Low to medium | High | The defect rule: its own entry, fixed, frozen again, both runs reported (`03-evaluation-methodology.md` §8) |

---

## Historical — the September 2026 plan, superseded by §§1–4 above (D45)

*Kept as written on 14 September 2026, with its banner of 28 September. Its title and planning unit are the ones above, and its headings are moved one level down; its section references (§1–§7) are to its own sections. Its sequencing and estimates fed §2 above; its dates and its list of open items do not hold.*

Schedule for the remainder of the project, from 14 September 2026 to final submission. Built around weekend-only availability, with effort stated in weekend-units rather than calendar weeks so that a missed weekend shows up as a real cost rather than disappearing into a vague estimate.

> ⚠️ **STALE as of 28 September 2026 — do not schedule from this file until it is rebuilt.** It is anchored on TA-1 as a fixed date, and **TA-1 did not take place** (moved to 22 September, then not held because the guide was unavailable; not yet rescheduled). §1 and §6 are therefore superseded, the milestone table's "TA-1 + N weeks" intervals have no anchor, and several items it lists as open have since closed — the B1 normalisation decision, for example, was resolved by D20. The **sequencing and weekend-unit estimates** in §§2–5 still describe the order of work; the **dates** do not. Rebuild once A14 supplies the rescheduled TA-1 date, TA-2/TA-3 and final submission. Current position: `00-project-phases.md`.

**Known fixed date (superseded):** TA-1 submission, Monday 21 September 2026 — did not take place.
**Unknown, needs filling:** TA-2, TA-3 (if applicable), final thesis submission, viva. §6 lists these as the first thing to confirm with the guide.

---

### 1. The immediate problem: one weekend to TA-1

From today, the available time before submission is:

| Day | Date | Available | Use |
|---|---|---|---|
| Mon–Fri | 14–18 Sep | Weekday evenings only | Small, bounded tasks |
| **Sat–Sun** | **19–20 Sep** | **One full weekend-unit** | The only substantial working block |
| Mon | 21 Sep | Submission day | Buffer and submit |

The TA-1 document is drafted. What remains is completion and verification, not writing — which is why one weekend is sufficient, but only just.

#### Plan for the nine days

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

### 2. Work breakdown — everything remaining

Effort estimates are honest rather than optimistic. Each includes verification, not just first-pass completion.

#### Build work (Phase C completion)

| # | Task | WU | Depends on | Notes |
|---|---|---|---|---|
| B1 | Resolve the risk/criticality normalisation question; re-run all methods; update the formulation document | 1 | — | **Blocks Phase D.** Highest priority technical item |
| B2 | Explanation layer — Ollama integration, prompt implementation, endpoint, evaluation criteria | 2 | B1 | Needs local inference working; allow for model-fitting friction |
| B3 | Colab plausibility notebook — prompt, batch scoring, output into the candidate table | 1 | — | Independent; can slot into any weekend |
| B4 | Screen 2 — sensitivity sweep comparison view | 1 | D1 partially | Only meaningful once multiple runs exist |
| B5 | Physical testbed — 7 VMs, pfSense conduit rules, OpenPLC, Node-RED, network segmentation | **3–4** | — | The largest single item. Historically the most underestimated part of OT projects |
| B6 | Repository hygiene — README correction, `requirements.txt`, remove the publisher PDF, commit history | 0.5 | — | Small but affects how the artefact is judged |

**Build subtotal: 8.5–9.5 WU**

#### Evaluation (Phase D)

| # | Task | WU | Depends on |
|---|---|---|---|
| D1 | Full evaluation campaign — all methods, all paths, all budget values | 1 | B1 |
| D2 | Weight sensitivity sweep across the coefficient grid | 1 | D1 |
| D3 | Results analysis, comparison tables, charts | 1 | D2 |

**Evaluation subtotal: 3 WU**

#### Writing (Phase E)

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

#### Review and submission (Phase F)

| # | Task | WU |
|---|---|---|
| R1 | Guide review cycle 1 and revisions | 1 |
| R2 | Guide review cycle 2 and revisions | 1 |
| R3 | Plagiarism check and corrections | 0.5 |
| R4 | Viva preparation — slides, anticipated questions, demo rehearsal | 1 |

**Review subtotal: 3.5 WU**

---

### 3. Totals and what they mean

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

### 4. Sequencing

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

### 5. Milestones to agree with the guide

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

### 6. First actions after TA-1

In order:

1. **Confirm the final submission date, TA-2 and TA-3 dates, and obtain the template.** Everything in this document is provisional until these exist.
2. **Resolve B1** — the normalisation question. It blocks the evaluation, which blocks the results chapter, which blocks the conclusion.
3. **Start Chapter 3** — the largest fully unblocked writing task.
4. **Request institutional database access** for the systematic review. It has a lead time outside your control, so it should be requested early even though the work itself is later. *[Superseded: no institutional access is available (A2, closed 6 October 2026). A17 is a structured search of open indexes, run from your browser (D34, `01-search-protocol.md`).]*

---

### 7. Risk register

| Risk | Likelihood | Impact | Response |
|---|---|---|---|
| Testbed build overruns | High | Medium | Pre-agreed scope reduction to a single zone boundary (see §3) |
| Phase D results do not support the primary question | Medium | High | Agree with the guide *now* that an honestly reported negative result is acceptable; rephrase the question if the tradeoff framing is more accurate |
| Template arrives late or imposes a page limit | Medium | Medium | Draft in markdown, convert once; content is format-independent |
| Local inference does not run acceptably on available hardware | Medium | Medium | Explanation layer degrades to a template-based fallback; the architecture already permits this |
| Systematic database review not obtainable | Medium | Low | Already handled — the review's limitation is stated explicitly in Chapter 2 rather than concealed; the structured open-index search (D34, `01-search-protocol.md`) narrows the gap |
| Weekend availability worse than assumed | High | High | Scope reduction decided deliberately at M2, not improvised at M4 |
| Guide requests major direction change at first review | Low | High | Deliver Chapter 3 early, at M1, so any structural objection surfaces while there is time to act |
