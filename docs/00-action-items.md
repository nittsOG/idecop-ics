# Action Items — Manual Tasks

Standing checklist of things that need your action because they're outside what I can do from this conversation. Added here the moment they come up, marked done when you tell me they're done. Check this file instead of hunting through chat history for something I mentioned once.

## Blocking TA-1 (21 September 2026)

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A7 | Fill the guide's name and designation into the TA-1 title block | Not something I hold | **Pending — blocking** |
| A8 | Complete reference [23], the D3O-IIoT deep-RL deception paper. PMC link is recorded in `sources.md` | Currently the sole citation justifying heavy operational-risk weighting, and it is uncitable without author and venue details | **Pending — blocking** |
| A9 | Complete references [12] and [26] — the GNN placement paper (2nd Graph Neural Networking Workshop, ACM 2023) and the criticality-analysis patent number | Author and patent details were not captured during the review | **Pending — blocking** |
| A10 | Confirm with the guide whether IEEE citation style applies and whether the template exists yet | Institutional convention | Pending |

## Blocking the evaluation campaign

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A11 | Decide how to resolve the `Risk(x)` and `CritProt(x)` normalisation mismatch — mean, union probability, or keep the sum and document the scale | A modelling decision with thesis consequences, not a bug fix. Blocks Phase D, which blocks Chapter 5 | **Pending — highest technical priority** |
| A12 | Decide whether the primary research question should be rephrased. As written it asks for higher Coverage and CritProt than the baselines; current output wins on the objective while covering fewer paths | Research-question wording is yours and the guide's call | Pending |
| A13 | Decide what to do about Historian and PLC-02 — both are confirmed candidates that appear in no attack path and can never contribute coverage. Reroute a path through them, or document them as search-space filler | Same fork D19 resolved for Engineering WS-2 | Pending |

## Schedule and coordination

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A14 | Obtain the final submission date, TA-2 and TA-3 dates, and the institutional template | Every interval in `00-project-timeline.md` is relative until these exist | **Pending — highest coordination priority** |
| A15 | Agree with the guide, before results exist, that an honestly reported negative or mixed evaluation result is an acceptable outcome | Much easier to agree hypothetically than after the numbers arrive | Pending |
| A16 | Agree a scope position on the physical testbed — full seven VMs, or reduced to one zone boundary with the rest modelled | 3–4 weekend-units at stake; the optimiser runs on the modelled graph either way | Pending |

## Research completeness

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A2 | Set up / confirm access to NFSU's remote e-library portal (`elibrarynfsu.remotexs.in`) | Needed for any paywalled paper — I can search and verify citations but cannot fetch subscription content | Pending |
| A4 | Get the full PDF of Shahin, Maghanaki, Chen (2026), `sources.md` #315 — likely free via MDPI | Needed to confirm whether it is a genuine manufacturing-sector competitor. The Jay paper showed that abstracts are an unreliable basis for a novelty judgement | Pending |
| A17 | Perform the certified systematic database sweep — IEEE Xplore, Scopus, Web of Science | The one systematic gap in the literature review. Request access early; the lead time is outside your control | Pending |

## Repository hygiene

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A18 | Remove `references/312-jay-2023-deception-substations.pdf` from the public repository; keep it locally and cite by DOI | Redistributing a publisher PDF on a public repo is a copyright exposure | **Pending** |
| A19 | Adopt incremental commits rather than single snapshots | The thesis claims incremental build-and-verify as methodology; commit history is the evidence for that claim | Pending |

## Build

| # | Item | Why it's manual | Status |
|---|---|---|---|
| A6 | Wire `/runs/{id}/explain` to a real Ollama instance | Needs Ollama installed and running to test a real model call; cannot be verified in a sandbox the way everything else has been | Pending, deferred by choice |
| A20 | Build the Colab plausibility-scoring notebook | Needs a GPU-backed runtime and your Google account | Pending |
| A21 | Stand up the physical VM testbed | Needs VMware Workstation and your hardware | Pending |

## Completed

| # | Item | Resolution |
|---|---|---|
| ~~A1~~ | ~~Add specification files to Project Knowledge~~ | Superseded — the GitHub repository is now the canonical source and is fetched directly |
| ~~A3~~ | ~~Share the current direction and specification with the guide~~ | TA-1 submission and the progress review pack now serve this |
| ~~A5~~ | ~~Decide how to resolve D15~~ | Resolved via D19 — P3 rerouted through Engineering WS-2, implemented and re-verified |

To mark something done: tell me the item number and I'll update this file.
