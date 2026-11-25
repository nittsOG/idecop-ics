# Decisions Log

Chronological record of significant decisions and why they were made. Appended to, not rewritten — a superseded decision gets marked superseded in place, with a pointer to what replaced it, so the history stays visible. This is the file to check before re-litigating something already settled, and the file to cite when the thesis methodology chapter needs to justify a choice.

---

**D1 — Optimization method: greedy (primary), MILP (validation), GA (reserve)**
Placement is proven NP-hard even on static graphs (source #14/15). A separate result (source #236) proves a comparable decoy-placement objective is submodular in structured cases, giving greedy a real (1−1/e) approximation guarantee — check whether this project's own objective satisfies the same property before claiming the guarantee. MILP is tractable and exact at the ~20-node testbed scale, used to report an optimality gap. Genetic algorithms have precedent in this literature but aren't the primary method.
*[D28: the guarantee sentence is superseded. D20 found F(x) submodular but not monotone, so plain greedy carries no approximation guarantee, and D23 attached the (1−1/e) bound to Distorted Greedy (#353). #236's result concerns its own objective. D20 recorded this, but this entry carried no pointer until D28.]*
*Status: confirmed. Reference: `research-synthesis-implementation.md`, `formal-problem-definition.md` §7.*

**D2 — Criticality scoring: combine two independent methods, not one**
IEC 62443 SL vectors (source #267, standards-grounded) multiplied by a network-centrality-and-operational-damage factor (source #282, graph-grounded). Neither alone was judged sufficient; citing both and explaining what each captures is stronger than picking one.
*[D28: "multiplied by" never described the formula as specified or built. Since the first commit Crit(v) has added SL to a product of centrality and damage, w₁·SL(v) + w₂·Central(v)·Damage(v), and D20 added w₃·ConduitSL(v). Nor is that product #282's pattern: the granted patent (#325, read in full on 6 October 2026) adds its three factors, C(i) = α·l(i) + β·c(i) + γ·d(i), and its centrality is a degree-and-strength measure over traffic shares, not betweenness. Whether Crit(v) should take the additive form is A40, undecided.]*
*Status: confirmed. Reference: `formal-problem-definition.md` §2.*

**D3 — Candidate locations are filtered, not the full asset list**
Two filters applied in sequence: a four-criterion plausibility rubric adapted from source #53 (can a decoy exist here / would an attacker reach it / does it yield signal / is it a reliable malice indicator), then a detectability check (sources #262, #263) excluding or down-weighting positions that are trivially fingerprintable. Demonstrated concretely in `testbed-architecture.md` — the OT Firewall fails the plausibility filter; OT-DMZ-zone candidates pass but get risk-adjusted downward for detectability.
*[D25: the seeded candidate set was not produced by these filters. Three of its five members (Historian, HMI, PLC-02) have no criterion scores, three assets on attack paths (Engineering WS, PLC-01, PLC-03) were never assessed, and the seed departs from the worked example cited here. The three confirmed rows are transcriptions from demo data, and the DMZ Jump Host's confirmed scores fail the only implemented Filter 1 rule. Re-deriving the set by these filters is A32, before Phase D.]*
*[D26: "source #53" above should read #40. #53 is an unrelated IEC 62443 paper. §4 now states how the four scores combine, and the seed no longer pre-judges the set.]*
*Status: confirmed. Reference: `formal-problem-definition.md` §4, `testbed-architecture.md`.*

**D4 — Baseline is betweenness centrality specifically, named as such**
Betweenness is the most common choice in comparable literature (source #1 finding). A recent role-aware centrality critique exists (source #237) arguing standard measures miss source/intermediate/target structure in lateral movement — cited explicitly as a known limitation rather than either ignored or independently re-implemented.
*Status: confirmed. Reference: `formal-problem-definition.md` §7.*

**D5 — Operational risk gets weighted heavily, justified by sensitivity sweep**
An ablation study (source #250) found removing a false-positive-control term cost 51.4% of a comparable system's performance — real evidence this term matters more than a default low weight would suggest. Weight justification method: parametric sensitivity sweep (source #272, the field's standard practice), not formal expert elicitation, which has no precedent in this literature.
*[D28: the first sentence is withdrawn, and with it the case for weighting operational risk heavily. Read in full on 6 October 2026, #250 gives its false-positive penalty a weight of 0.06, and that penalty concerns deception actions applied to benign traffic. Its ablation shows the term matters when present, not that it should weigh heavily. Separately, the link to δ lapsed at D20: this entry was written when §5 defined Risk as legitimate traffic interacting with decoys, but the code always summed each decoy's detectability, and since D20 aligned the definition with the code, #250's term corresponds to Filter 1's malice fidelity instead. The second sentence stands and is now the whole justification. Nothing in the objective changes: the default δ has always been 1, equal to α, β and γ.]*
*Status: confirmed in part: the sensitivity-sweep method stands, and the heavy weighting is withdrawn (D28). Reference: `formal-problem-definition.md` §5.*

**D6 — AI layer: deterministic optimizer decides, LLM only explains**
Matches the original project brief's own AI philosophy (section 9). Now has direct architectural precedent: sources #244 and #255 (i-EXAM/SPEAR) do the same decide/explain split for general network hardening; source #257 bridges that same planning formalism to IT-to-OT attack-path discovery specifically.
*Status: confirmed. Reference: `formal-problem-definition.md` §8, `testbed-architecture.md`.*

**D7 — Novelty claim, precise wording**
"No published work performs formal, quantitative deception-placement optimization across a multi-zone OT/ICS architecture using IEC 62443 zone/conduit structure and asset criticality as first-class inputs to a composite objective, validated against baselines." Devika Jay (2023) is the closest prior work but solves a structurally different problem — resource allocation under a guaranteed-full-observability requirement on one VLAN's message graph, using GOOSE-protocol-specific physics — not budget-constrained, multi-metric site selection across a multi-zone architecture. Confirmed against her full text, not just the abstract (source #312).
*Status: confirmed, and strengthened by the full-text read. Reference: `research-synthesis-implementation.md`, sources.md #305 & #312.*
*Note added 29 September 2026 — tested again after this entry.* Iteration 13 found a granted Acalvio patent disclosing a placement method (US 9,853,999, `sources.md` #347). A granted patent is published work, so "published" no longer does the distinguishing; `03-commercial-prior-art-analysis.md` §4 concludes the claim survives on a method-level distinction — the patent decides *how many* decoys go into the densest or most-attacked subnet, with no objective function, budget constraint, zone/conduit structure or baseline validation. No decisions-log entry had recorded that verdict until this note. Final wording is A28, pending.
*[D28: the note above is incomplete. The granted claims were read on 6 October 2026 (A29, #347). Besides the count, dependent claim 6 deploys the decoys "on or near the central node", so the patent combines a count rule with one central-node rule. The method-level distinction holds, since nothing in it maximises a stated objective over positions under a budget. This project's centrality baseline is the nearest analogue of the patented rule.]*

**D8 — Testbed scope: 7 physical VMs, 4 modeled-only graph nodes**
Kept the physical build close to the original brief's own skeleton (Kali, pfSense, DMZ host, Engineering WS, HMI, 2×PLC) rather than expanding it — the research process found no reason the original scope was wrong. Added a historian, second engineering workstation, a third PLC modeled as an IEC-104 RTU, and a redundant conduit as graph-only nodes, specifically so the optimizer has real tradeoffs to make rather than a single linear chain.
*Status: confirmed. Reference: `testbed-architecture.md`.*

**D9 — Stopped broad research iteration after iteration 10**
Pattern across ten iterations showed diminishing returns from general searching, punctuated by real finds only from genuinely new angles (a sector pivot, a specific paper's follow-up). Given weekend-hours constraints, further research is now targeted (closing named gaps as they arise) rather than open-ended.
*Status: confirmed. Reference: iteration-10-findings.md, this conversation's own discussion.*

**D10 — Water/manufacturing sector check: run, mostly resolved, one item still open**
Closed the single biggest named risk to the novelty claim (per D7 and the synthesis document's "what could still change this picture"). Water sector strengthens the novelty claim — its cybersecurity guidance doesn't yet discuss deception technology as a category, a less mature ecosystem than electric utility's. Manufacturing surfaced a real candidate (Shahin, Maghanaki, Chen 2026, `sources.md` #315) that looks like a general analytical framework rather than an OT-topology-structured placement system — but that conclusion rests on abstract evidence only, the same level that turned out to be misleading for the Jay paper before its full text was read.
*Status: mostly confirmed, one sub-item open — get the full text of source #315 before section 14 states the manufacturing comparison as settled. Reference: `sources.md` "Targeted Sector Check," `research-synthesis-implementation.md`.*
*[D28: the sub-item is closed. #315 was read in full on 6 October 2026 (A4): a Stackelberg game on decoy quality against quantity, choosing decoy types greedily, with no network topology, zones or set of positions. It is not a placement competitor.]*

**D11 — AI role: unstructured-OT-documentation interpretation cut from scope**
The original brief (§9) named this as a *possible* AI use, not a committed one. Nothing in the current pipeline produces or consumes unstructured OT documentation — no component reads it, nothing downstream expects it. Adding it now would mean inventing a use case to justify a capability, which the brief's own working principle (§16) explicitly warns against. Cut, not deferred silently.
*Status: confirmed. Reference: `02-ai-role.md` §1.*

**D12 — AI role expanded: plausibility-scoring assist added, interactive Q&A deferred**
Weighed three directions for giving AI a more substantial role than a single post-run explanation: (a) an interactive Q&A layer over completed runs, (b) AI-assisted first-pass scoring of formal-problem-definition.md §4's plausibility rubric with human confirmation, (c) replacing the optimizer itself with an AI-driven decision — rejected outright, since it would move the project out of the specific novelty gap ten research iterations found and into the crowded RL/game-theoretic placement literature, and would require an entirely different, much less certain evaluation methodology this late in the specification. Between (a) and (b): (b) chosen. Lower implementation cost, lower guardrail risk (single-shot per-asset scoring vs. open-ended multi-turn conversation), and it strengthens a real, currently-manual step already in the formal spec rather than adding a new demo-facing feature. Runs on Google Colab (Qwen3 14B) rather than local Ollama, since it's a disconnected one-time batch step, not part of the live system — see D6's local/no-paid-API constraint, which this doesn't violate since Colab's free tier is being used for a step that doesn't touch OT topology data at deployment time, only during offline testbed setup.
*[D26: the route stands, an AI first pass with a human reviewing every card, with safeguards against anchoring. D26 also corrects one claim in its documentation: a free Colab T4 cannot run Qwen3 14B unquantised. It needs 4-bit weights.]*
*Status: confirmed. Reference: `02-ai-role.md` Part B, `02-data-model.md`'s `candidate_locations` table, `formal-problem-definition.md` §4.*

**D13 — Three UI screens, not one; single write-path through the API**
The interface walkthrough left open how many distinct screens the prototype actually needs. Resolved as three, because they serve different moments (live demo, evaluation-data generation, one-time setup), not different views of the same data: a single-run dashboard, a sensitivity-sweep comparison view, and a plausibility-review screen. Build order given weekend hours: review screen first (nothing else works without confirmed candidates), dashboard second (most demo value, most already specified), comparison view last (simplest to build, only meaningful once Phase D generates multiple runs). Separately: only the `/api` module has database write access — `graph_model` and `optimizer` are libraries it calls, not independent services — keeping every write auditable at one layer, consistent with how AI-component writes are already gated in D12.
*[D26: the principle holds for the running system, but four offline setup steps also write to the database:*
*- the notebook import (`ai_*` columns only, as `02-prototype-architecture.md` §4 specified in Phase B);*
*- `scripts/review_io.py restore`, which replays a committed review through the API's rules;*
*- the legacy SQL, which reproduces historical numbers and which the loader refuses without `--legacy-d25`;*
*- `graph_model`'s `write_computed_scores`, when run as a script.]*
*Status: confirmed. Reference: `02-prototype-architecture.md` §1, §3.*

**D14 — Phase C started: Screen 3 built and tested, one spec gap found and fixed in the process**
Built and verified the actual SQLite database, FastAPI backend, and React frontend for the plausibility-review screen — not just specified, actually run: database queried, API hit with real requests including validation-error and not-found cases, frontend built to a clean production bundle. In the process, found that `02-data-model.md`'s seed data never populated `edges` or `conduits`, leaving the graph with zero connectivity — fixed by deriving real edges from `testbed-architecture.md`'s topology and the two attack paths with specified traversals, fed back into the canonical document rather than only patched locally. This is the kind of gap that only surfaces when a spec actually gets built against, which is itself worth noting as a reason to keep building incrementally rather than writing all remaining code before testing any of it.
*Status: confirmed. Reference: `phase-c-screen-3.zip`, `02-data-model.md` (edges/conduits section).*

**D15 — graph_model and three of four optimizer methods built, run, and a real methodology gap found — open, not yet resolved**
Built and ran greedy, random (30 trials), and centrality against the real 11-node graph (now with real edges, per D14) and the real 5-candidate subset of `L`. Confirmed greedy's early-stopping and risk-sensitivity behave as specified — it declined a second placement at DMZ Jump Host specifically because that location's detectability_risk outweighed its coverage gain, which is D5's "weight risk heavily" decision visibly doing something, not just being stated. Also surfaced a genuine gap: Engineering WS-2 is a valid, confirmed candidate location, but no attack path in `threat-attack-model.md` actually routes through it — only the primary Engineering WS appears in P1's steps — so it currently contributes zero coverage value despite testbed-architecture.md's stated reason for including it ("gives the optimizer an actual choice" between workstations). Two ways to resolve this: add branching to the threat model so a path could plausibly route through either workstation, or reframe this asset's documented purpose as topological search-space richness rather than attack-path coverage specifically. Not resolved yet — needs a call before Phase D locks in the final threat model, not urgent enough to block continued building.
*[D28: "D5's 'weight risk heavily' decision" is withdrawn with D5's evidence. What this entry observed was the operational-risk term at the default δ = 1, not a heavy weighting.]*
*Status: open. Reference: `phase-c-build.zip` README, `scripts/run_comparison.py`'s actual output.*

**D16 — MILP's "unnormalized Early proxy" (documented in 02-optimization-formulation.md §3, Option 2) was wrong, found by implementing and testing it**
Building the MILP validator using the originally-recommended Option 2 produced a placement that scored *worse* on the true, normalized F(x) than greedy's result — logically impossible for an exact validator whose entire purpose is confirming greedy's optimality gap. Root cause: an unnormalized sum of per-path early-detection contributions rewards covering more paths over covering fewer paths earlier, which the true (normalized) Early(x) does not — so the proxy and the real objective can rank placements differently, and the solver correctly optimizes the wrong thing. Fixed by switching to Option 1 (enumerate coverage count k = 0..|P|, fix the denominator per solve, keep the best true F(x) across all k) — tractable here since |P|=3 means only 4 solver calls, each still sub-second. Re-tested against greedy across four risk-weight configurations after the fix; the two methods matched exactly in every case on this testbed's scale, which is expected for a small instance and not itself evidence the guarantee from D1 holds in general. `02-optimization-formulation.md` §3 corrected to document Option 1 as the actual recommendation, with the Option 2 failure kept in the text rather than quietly removed, since it's a real, useful cautionary finding for the methodology chapter.
*Status: confirmed, fixed. Reference: `02-optimization-formulation.md` §3, `phase-c-build.zip`, `src/optimizer/milp.py`.*

**D17 — /optimize, /runs, /runs/{id} wired and tested; random baseline's API-stored result is one trial, not the 30-trial mean**
Connected graph_model and all four optimizer methods to the live FastAPI app, verified with real HTTP calls: all four methods run and write correctly, GET /runs and /runs/{id} return correct stored data matching the standalone script's results exactly, and bad-method/zero-budget/unknown-run all correctly return 422/404. One design nuance worth remembering for Phase D: `/optimize` with `method=random` still runs the full 30-trial sweep internally (per §4), but only stores the single best-scoring trial as that call's `placement_runs` row, since a stored run needs one concrete placement, not a distribution. The mean/std across all 30 trials is available by calling `random_baseline()` directly, not by reading a single stored run — Phase D's evaluation should use the direct function for the statistical comparison, and treat any one `/optimize(random)` call as illustrative, not the baseline's true average performance.
*Status: confirmed. Reference: `phase-c-build.zip`, `src/api/main.py`.*

**D18 — Prototype named iDECOP-ICS; thesis title unchanged**
The artifact needed a name distinct from the thesis title ("AI-Assisted Deception Placement Optimization for Industrial Control Systems"), for the repository, the FastAPI application, the UI header, and the Implementation chapter's shorthand. Chosen: **iDECOP-ICS** — *intelligent Deception Planning and Placement Optimization for Industrial Control Systems* (IEC 62443 zone-aware, with explainable AI). Repo `idecop-ics`. The letters carry AI (the `i`), deception, optimization, and planning; the expansion carries the zone/conduit grounding and the domain. The lowercase `i` is deliberate — it visually breaks the string `IDEC`, which in an OT context reads as IDEC Corporation, a Japanese PLC/HMI manufacturer. Styling rule: never begin a sentence with the name (write "The iDECOP-ICS prototype selects…"), since some style guides reject sentence-initial lowercase and Word will autocapitalize it. If a submission style guide forbids it outright, all-caps IDECOP-ICS is the accepted fallback.

Selection criteria, applied in order: (1) foreground placement/optimization rather than deception generation — the brief's §4 boundary exists to prevent the "another honeypot" misreading, and the name is the first thing an examiner parses; (2) the expansion must literally state the contribution; (3) a coined term rather than a common English word, so it is searchable and unambiguous in prose; (4) no collision with existing tooling, checked rather than assumed.

Candidates rejected, and why — recorded because the reasons are not reconstructable later: DECIDE, CONDUIT (common English words; CONDUIT additionally collides with the standard's own vocabulary, producing ambiguous prose); DePOT (the "POT" reading invites the honeypot association the boundary rejects); OPTIDEC (registered French trademark); ZONDEX (**live collision** — zondex.io is an active attack-surface-scanning security product, and Zondex Engineering manufactures industrial valves for oil, gas, mining, energy, and water plants — both inside this project's own domains); ZONDEC (Zondec 50 Injection, a pharmaceutical brand sold in India — would be the first search result domestically); ZODEX (zodex.dev, an AI coding IDE); DECOPLAN (design studios, a roofing manufacturer, a registered Westag product, a GitHub repo); DECIZONE (US SaaS and a Pune IT firm); DecoyPlan (too close to DecoyPlanner). A Sanskrit-themed name was considered and dropped: VYUHA — semantically the best fit available, meaning a strategic battle formation — is taken three times in Indian cybersecurity specifically (Vyuha Labs of the Telangana Cyber Security Bureau with IIIT Hyderabad; VYUH CISO Dashboard; Asta-Vyuha). The general finding is worth keeping: Sanskrit naming is heavily worked ground in Indian security branding, so collision risk in that theme is higher than for an invented acronym, not lower.

Suffix choice: `-ICS` over `-OT` and over `-CIS`. `-CIS` was rejected outright — in security, CIS means the Center for Internet Security (CIS Controls, CIS Benchmarks), so the name would imply compliance tooling, the territory §4 excludes. `-OT` is arguably more accurate about the search space, since the DMZ jump host, historian, and engineering workstations sit above Purdue level 2 and are candidate decoy sites — but the thesis title, the primary research question, and the novelty claim all say Industrial Control Systems, and an artifact name that disagrees with them makes a reader stop to check whether scope shifted between the research question and the implementation. The OT accuracy is carried in the expansion instead.

Accepted known risk: the `IDEC` proximity described above. Judged minor and mitigated by the lowercase `i` plus expanding the acronym on first use in each chapter — recorded here as accepted with eyes open, not overlooked.
*Status: confirmed; uniqueness checked on every channel reachable from this environment, all clear, including a second pass on the bare stem `IDECOP` (not just the hyphenated form) per D18's own follow-up — same two unrelated firms (Colombian metalworking, Dominican cooperative institute), nothing software/security/OT. GitHub, PyPI, npm: unregistered. IEEE Xplore: checked via NFSU access — no results. Still open and manual: Google Scholar, Indian/US trademark registries. Rename pass across the codebase completed in D19.*
*[D28: the IEEE Xplore check is withdrawn. It is recorded as made "via NFSU access", but the NFSU library is not available to the user (A2), and IEEE Xplore is not reachable from Claude's environment (A33). It is therefore treated as not made: IEEE Xplore is unchecked for the name, alongside Google Scholar and the trademark registries. A42 now tracks those checks.]*

**D19 — D15 resolved: P3 rerouted through Engineering WS-2, not left disjunctive; re-run confirms the structural fix, and surfaces a genuine property of Early(x) worth keeping for the results chapter**
Weighed three options. (A) Split P1 into two paths, one per workstation — rejected: `|P|` goes 3→4, the Stuxnet scenario is then represented twice, and CritProt double-counts one PLC target relative to P2/P3, a distortion an examiner could reasonably challenge. (B) Reframe Engineering WS-2's documented purpose as search-space richness rather than coverage — honest and zero-cost, but weaker than testbed-architecture.md's existing claim, and left as fallback only. (C) — **chosen** — resolve `threat-attack-model.md` P3 step 2's existing disjunction ("Engineering WS or HMI," never actually settled) toward WS-2 specifically. Keeps `|P|=3`, fixes a pre-existing ambiguity the spec needed to settle anyway independent of D15, and is realistic: a reconnaissance-stage scan plausibly lands on whichever workstation is discoverable, not necessarily the primary one.

Implemented and re-run, not just decided on paper: `threat-attack-model.md` and `seed.sql` updated (P3 step 2 → Engineering WS-2, replacing an unexamined default of HMI that the code had picked without real justification when first written); `demo_ai_suggestions.sql`'s stored AI reasoning for WS-2 corrected too, since it previously cited "P1 routes through the engineering workflow" — never actually true, WS-2 has no P1 involvement — now correctly cites its real P3 role.

Re-running all four methods surfaced something worth keeping, not a problem to hide: under the default weights, greedy now picks **DMZ Jump Host alone**, not WS-2 or HMI, at every budget from 1 to 3. Reason, confirmed by hand-computation: `Early(x)` is a *mean over intercepted paths*, and both WS-2 (P3, step 2 of 2) and HMI (P1, step 5 of 5) intercept at the latest possible stage — adding either after DMZ Jump Host's excellent early catch (step 1 of 4 on P2) *drags the average down*, so the coverage gain doesn't clear the combined cost, risk, and early-detection penalty. Confirmed this isn't WS-2 still being structurally excluded: with coverage weighted higher (α=3 instead of 1), the optimizer selects **all three** (DMZ Jump Host, Engineering WS-2, HMI), reaching full coverage. The fix achieves exactly what it needed to — WS-2 is no longer *impossible* to select — without forcing it to be selected under every weighting, which isn't what a correct optimizer should do anyway. Worth a sentence in the results chapter: this is a real, interpretable illustration of the coverage/early-detection tradeoff the sensitivity sweep in `formal-problem-definition.md` §5 exists to explore, found by re-running the model, not asserted from the formula alone.
*Status: confirmed, fixed, re-verified. Reference: `threat-attack-model.md` P3, `phase-c-build.zip`'s `seed.sql`/`demo_ai_suggestions.sql`.*

**D20 — Objective function corrected: Early's denominator, Risk and CritProt normalisation, conduits made numeric. Verified by exhaustive enumeration, not argued.**
Four changes, made together because all four are normalisation defects in the same function and fixing them separately would have meant three re-runs.

*(1) `Early(x)` denominator changed from |intercepted| to |P|.* As a mean over intercepted paths it is **non-monotone** — adding a late-intercepting decoy lowers it, which D19 observed empirically without recognising the structural cause. Confirmed by enumerating all 32 subsets of `L` (`scripts/structure_check.py`): 16 monotonicity and 18 submodularity violations. With a fixed |P| denominator: zero of each. Mean interception stage survives as a *reported* statistic — it is the interpretable number for the results chapter — it just stops being what the solver maximises. **Note the connection to D16:** the fixed denominator is what D16's rejected "Option 2" was approximating. Option 2 was correctly rejected *at the time*, because it did not match the then-current mean-normalised definition. Changing the definition removes the mismatch, and with it the need for D16's k-enumeration workaround — `solve_milp` is now a single exact solve.

*(2) `Risk(x)` divided by B, and its definition reworded.* §5 called it a probability while the code summed per-decoy values, unbounded above. Sum/B bounds it to [0,1] and **keeps it modular**, which is the load-bearing property: the semantically nicer union form 1 − ∏(1 − r_l) is a genuine probability but is submodular, and subtracting a submodular function would destroy the submodularity this fix exists to restore. The spec now says "normalised detectability exposure", not "probability". *[Divisor superseded by D25: Risk and Cost are now divided by the fixed constant K = 4. Dividing by B made the same decoy worth a different amount at different budgets, a side effect this entry did not record. Modularity, the load-bearing property, is unchanged.]*

*(3) `CritProt(x)` denominator changed to the criticality of path targets.* Normalising against every asset in the graph capped the term near 0.30 at full coverage, making γ=1 behave as γ≈0.3. The sensitivity sweep would have swept a distorted axis.

*(4) `ConduitSL(v)` added to `Crit(v)` (resolves A22).* The novelty claim names zone **and conduit** structure as first-class inputs; conduits were stored and diagrammed but entered no computation, so that clause was false as built. A conduit now takes the higher SL of the two zones it joins (rule from source #330), and an asset inherits the highest SL among conduits incident to its zone. Modular in x, so submodularity is unaffected — re-verified after the change. **This supersedes the option (b) recommendation made in `iteration-11-findings.md` §4:** (b) would have put conduits into the candidate filter, which shapes `L`, not `F(x)` — it would not have made the claim true. Option (a) does.

**Structural result, stated precisely.** Before: F(x) neither monotone nor submodular; **no greedy guarantee of any kind was available**, contradicting D1 as written. After: F(x) **submodular but still non-monotone** — necessarily so, since Risk and Cost are subtracted. The classical (1−1/e) bound needs monotone submodularity, so it still does not apply directly to F(x). §7 now records the two honest routes (cite the regularised g − ℓ result, or move risk from penalty to constraint) and forbids claiming a guarantee until the primary source is verified (A27). D1's wording is superseded on this point.

**Effect on results — reported because concealing it would be worse.** Under the old objective, greedy selected DMZ Jump Host alone (Coverage 0.33) while the centrality baseline reached 0.67, so the primary research question was unanswerable in the affirmative. Under the corrected objective, greedy reaches **Coverage 1.00 at B=3**, and across 20 budget/weight configurations beats centrality in 17 and ties in 3, never losing. **This is exactly the pattern a sceptical examiner is trained to distrust** — objective changed, result improved. The defence, recorded here before the evaluation campaign rather than after: every change is an independently verified structural defect, all four were found by structural testing rather than by hunting for a cause after seeing unwelcome results, and the results chapter will report under **both** objectives. The primary research question was also rephrased (§8) rather than merely being made answerable — if it is only ever answerable after an objective change, it was too narrow to begin with.

**Two honest observations from the re-run.** At B=2 under default weights, greedy, MILP and centrality all select the same pair and score identically — on a five-candidate instance a topology heuristic can coincide with the optimum, and that must be reported, not hidden behind a more favourable budget. Conversely at δ=3, B=1 greedy places **nothing** (F=0) where centrality places a decoy and scores −1.239: the proposed method knows when not to act, which a top-B ranking structurally cannot. *[Superseded by D25: that decline was produced by dividing Risk and Cost by B. With a budget-independent divisor greedy places a decoy in that cell.]* Centrality also spends spare budget on the Historian, an asset on no attack path — pure cost and risk for zero coverage, and a clean illustration of why topology-only ranking fails here.
*Status: confirmed, implemented, re-verified. Reference: `scripts/structure_check.py`, `docs/03-honest-review.md`, `formal-problem-definition.md` §2/§5/§7/§8.*

**D21 — P4 added to the attack path set, before the evaluation campaign. First attempt failed; recorded rather than tidied away.**
`|P|` goes 3 → 4. Motivated by A13: two confirmed candidates — Historian and PLC-02 — appeared on no path at all, so no method could ever select them. They contributed cost and detectability risk with zero possible coverage gain, and the four-value coverage granularity (0, ⅓, ⅔, 1) was coarse.

**Grounding.** Dragonfly / Dragonfly 2.0, an intelligence-gathering campaign against ICS operators. `T0811 Data from Information Repositories` verified directly at attack.mitre.org/techniques/T0811/: Collection tactic, Dragonfly 2.0 listed as a procedure example, and — decisively — its **Targeted Assets list names A0006 Data Historian explicitly**. *[D34: Dragonfly 2.0 is not a procedure example on the T0811 page, at v17.1 or live; Duqu is the only one. The targeted-asset claim stands (#350's update).]* `T0862 Supply Chain Compromise` verified against MITRE-authored ATT&CK for ICS material as Dragonfly's documented initial-access vector (trojanised vendor software).

**The first attempt did not work, and the sequence matters.** P4 was first drafted entering at the DMZ Jump Host, mirroring P2's perimeter entry. Re-running showed the Historian *still* unselectable: a decoy at the jump host intercepts P4 at step 1, leaving the Historian redundant. The path was redrafted to enter at the Engineering Workstation via supply-chain compromise.

**That redraft is defensible on its own terms, and the reasoning must be stated in that order rather than reversed.** Supply-chain compromise is Dragonfly's *documented* initial access; perimeter intrusion is not. So the second version is the historically accurate one and the first was the weaker reconstruction — the structural benefit is a consequence of getting the history right, not the reason for the change. Recording it this way because the alternative reading — "the path was adjusted until the desired asset became selectable" — is available to a sceptical examiner, and pre-empting it honestly is stronger than hoping it goes unnoticed. **Both versions were built and run before any evaluation campaign; nothing here was changed after seeing evaluation results.**

**Effect, measured across 20 budget/weight configurations.** The Historian is now selected in **16 of 20** — it has become a genuine competitor rather than dead weight. Coverage now moves in quarters rather than thirds. Greedy beats or ties the centrality baseline in all 20 and loses none; the ties concentrate at B=3 and B=4, where the small candidate set saturates and both methods reach the same placement. At B=1 under δ=3 greedy still places nothing while centrality scores −1.473, which remains the clearest single illustration of the operational-risk term doing work. *[Superseded by D25: the decline came from dividing Risk and Cost by B, not from the risk term alone.]*

**PLC-02 is not fixed, and is not being fixed.** It remains on no path. Documented in `testbed-architecture.md` as search-space richness — a plausible decoy site the optimiser must evaluate and correctly reject. Manufacturing a fifth path solely to make it selectable would be fitting the threat model to the search space rather than to documented adversary behaviour, which is the error this entry exists to avoid. *[D26: under §4's path rule an off-path asset scores No on Interaction, so PLC-02 cannot pass Filter 1 and leaves the candidate set. The search-space-richness position stands only as history.]*

**Freeze status.** Attack paths are now final for Phase D unless a documented defect emerges. *[D27: one did. The Backup Control Switch's stated purpose, the two-route test, was never modelled, and ATT&CK for ICS treats switches as targets. P5 was added.]* *[D28: a second, smaller one: P1 step 5 gave T0832 the wrong tactic. It is Impact (#387).]* Remaining unfrozen input: the detectability values in `candidate_locations`, still hand-assigned (A23).
*Status: confirmed, implemented, re-verified. Reference: `threat-attack-model.md` P4, `data/seed.sql`, `testbed-architecture.md` verification table.*

**D22 — Filter 2 detectability values derived by a stated rubric, not judgement. The change made the headline result worse, and it stays.**
Closes A23. `detectability_risk` in `candidate_locations` was previously assigned by judgement — plausible numbers with no procedure behind them, so unreproducible and uncheckable. Replaced with a three-factor rubric: **risk = 0.4·Exposure + 0.3·ProbingDepth + 0.3·ArtifactSurface**, each factor traceable to logged evidence. Full derivation, per-candidate scoring and limitations: `02-detectability-rubric.md`.

**The ranking reverses, which is the substantive finding.** Under judgement the DMZ Jump Host was riskiest (0.70) because it sits in the most scanned zone. Under the rubric it is the *least* risky exposed candidate (0.54) and the Historian becomes the riskiest (0.30 → 0.78). Reason: exposure alone does not determine detection. A minimal jump host is heavily scanned but easy to emulate — almost nothing for a decoy to get wrong. A historian is heavily scanned, *and* a deliberate objective for a collection-motivated adversary who will interrogate it properly, *and* hard to fake, since a process historian with no plausible history is obvious immediately. **The hand-assigned values over-weighted exposure and ignored probing depth and artifact surface entirely.**

**Effect on results — worse for the proposed method, reported rather than reverted.** Across the same 20 budget/weight configurations, greedy's record against the centrality baseline moved from **10 wins / 10 ties** to **5 wins / 15 ties**. Still zero losses. The rubric raised risk on the Historian, HMI and PLC-02 relative to the jump host, flattening the differences between candidates and making the greedy ordering coincide with the centrality ordering more often.

**Reverting was available and is exactly what the project's own rules forbid.** The old values produced a better-looking comparison. They were also unjustifiable. Changing a frozen input *back* because the grounded version scored worse would be the precise malpractice `00-workflow-and-rules.md` and the D20 entry exist to prevent. The rubric values stand. **This happened before Phase D, which is the entire reason the freeze sequence was ordered this way.**

**One illustration got stronger.** At δ=3 greedy now declines to place anything at both B=1 and B=2, and places only two decoys at B=3 and B=4, while the centrality baseline scores −0.993 and −0.360 by spending its budget regardless. The proposed method's ability to decline is more visible under better-grounded risk values, not less. *[Superseded by D25, in part. Under these (v1) risk values, the declines at B=1 and B=2 depended on dividing Risk and Cost by B. The two-decoy placements at B=3 and B=4 did not: dividing by B and by 4 coincide at B=4, and with a modular objective the same two decoys are the only positive ones at B=3. Under the current D22a values and the fixed divisor, no cell of the comparison grid declines at δ=3, but that rests on δ=3 sitting just below the first threshold, 3.025 — see D25.]*

**Honest coupling to declare.** ProbingDepth is derived from whether a path in **P** sweeps or seeks the asset, so the attack path set now influences both Coverage and Risk. Defensible — an asset adversaries deliberately seek genuinely is examined more closely — but it is a modelling decision, not a neutral measurement, and the results chapter must say so. The 0.4/0.3/0.3 factor weights are themselves a judgement and should be swept or at minimum reported as a stated choice.

**Freeze status: all four evaluation inputs are now final.** Attack paths (D21), objective function (D20), candidate set and risk values (D22), methods (D20 plus distorted greedy). Phase D may begin. Any further change to these requires a decisions-log entry stating its effect on results, per the evaluation-integrity rule.
*Status: confirmed, implemented, re-verified. Reference: `02-detectability-rubric.md`, `data/seed.sql`, `formal-problem-definition.md` §4.*

**D22a — Correction to D22. The rubric's middle factor was wrong; full text of the source was obtained and it was rebuilt.**
D22 was built from search snippets of Chaudhry et al. (#352) because the full text had not been fetched. The paper is open access under CC BY and was one request away. That was the error, and it produced a second one.

**What was wrong.** D22's middle factor, *ProbingDepth*, asked "how hard does the adversary look here", derived from the sweep/seek distinction — sweep 0.3, seek 0.8. The paper's §4.9 states the opposite for this domain: *"Low-interaction deployments (e.g., ICS/OT) are primarily identified through surface-level artifacts such as static banners (A1) and default configurations (A7), using basic active probing (P1)."* **ICS decoys fall to the simplest probing tier.** A sweeping adversary running one Nmap scan identifies a PLC decoy. D22 scored exactly that scenario as low risk.

**The fix.** The factor is now *ProbingTierRequired* — the simplest probing tier that suffices to identify a decoy at this asset type, a property of the **asset**, not of attacker intent. Lower required tier means higher risk. Re-derived values: DMZ Jump Host 0.69, Historian 0.69, Engineering WS-2 0.56, HMI 0.62, PLC-02 0.62.

**A declared limitation disappeared.** D22 had to declare that Risk was coupled to the attack path set, since sweep/seek came from **P**. P_req is an asset-type property, so Risk and Coverage no longer share an input. The corrected rubric is cleaner, not merely more accurate.

**Effect on results, and why this is uncomfortable.** D22's flawed values gave greedy 5 wins / 15 ties. The corrected values give **9 wins / 11 ties / 0 losses**. So the correction *improved* the proposed method's standing. D22 recorded the opposite situation — a grounded change that made results worse, kept anyway. This entry records a grounded change that made results better. Both are recorded in full, with their causes, precisely so that neither reads as selective.

**Two findings from the full text worth carrying into the thesis, independent of this rubric.** The same review reports measured evidence that placement changes decoy exposure: corporate-network honeypots received 91% more S7comm traffic than cloud-hosted ones, while cloud honeypots saw 45% more HTTP traffic, with the authors concluding that *"setting and placement are critical"*; and for smart grids, that *"the complexity in the deployment can help mask the suspiciousness of the honeypot's vulnerability."* **A 2026 systematic review in the fingerprinting literature independently asserting that placement materially affects decoy effectiveness is direct support for this project's premise**, and should be cited in section 14.

**Process lesson, recorded because it has now cost twice.** Iteration 13 concluded Acalvio had no placement method from marketing copy, and a granted patent proved otherwise. D22 built a scoring rubric from snippets, and the full text inverted a factor. **Both failures share a cause: treating partial access as sufficient when full access was available.** The working rule going forward: if a source is load-bearing for a decision, obtain the primary text before deciding, not after.
*Status: confirmed, corrected, re-verified. Reference: `02-detectability-rubric.md` v2, `data/seed.sql`.*

**D23 — A27 closed. The approximation guarantee is real, but it attaches to Distorted Greedy, not to plain greedy, and two of my own claims about the source were wrong.**
Closes A27, which had stood as **"Pending — blocks any guarantee claim"** while `src/optimizer/baselines.py` already implemented the method that resolves it and D22's freeze statement already counted it among the frozen methods. That contradiction is itself part of what this entry fixes.

**The source, obtained in full before anything here was written.** Chris Harshaw, Moran Feldman, Justin Ward, Amin Karbasi, *"Submodular Maximization beyond Non-negativity: Guarantees, Fast Algorithms, and Applications"*, Proceedings of the 36th International Conference on Machine Learning, PMLR vol. 97, pp. 2634–2643, 2019. Logged as `sources.md` #353. It addresses exactly our objective's form: **f = g − c**, with g monotone, non-negative and γ-weakly submodular, and c non-negative modular. Distorted Greedy returns S with **g(S) − c(S) ≥ (1 − e^−γ)·g(OPT) − c(OPT)** in O(nk) evaluations of g. Our g is genuinely submodular, not merely weakly submodular, so γ = 1 and the bound is (1 − 1/e) ≈ 0.632.

**The paper also proves a matching hardness result** — no polynomial-time algorithm accessing g through a value oracle can beat (1 − e^−γ). A value oracle is precisely our access model, so this is not merely *a* bound we happen to hold; it is the best obtainable. Worth stating in the thesis, because it converts "we have a guarantee" into "we have the best guarantee available".

**§7's route (i) is not usable, and is now recorded as such.** §7 named Sviridenko, Vondrák & Ward as the route to a guarantee. Their bound is comparable, but their algorithm requires continuous optimisation of the multilinear extension — impractical at any scale and absurd at this one. Harshaw et al.'s algorithm is combinatorial and about fifteen lines. Route (i) is superseded by a route (iii) that §7 did not previously contain.

**Two of my own claims about this source were wrong, and are corrected here rather than quietly amended.** The previous docstring in `baselines.py` asserted (a) that the guarantee is "Theorem 3" and (b) that Appendix A establishes an **O(1/k)** competitive ratio for plain greedy. Neither survived contact with the text. The full text attributes the Distorted Greedy guarantee to a theorem I could confirm only through a single retrieval route, and a second retrieval could not corroborate the number; the appendix is titled *"Greedy Performs Arbitrarily Poorly"* and establishes an **unbounded** ratio, not a specific O(1/k) rate. Both claims are removed. **The result is now cited by content rather than by number**, which is accurate and still citable. Confidence: the form, the bound, γ = 1, O(nk), the hardness result and the full citation are *verified* (abstract, full text and the published PMLR record agree); the theorem's number is *unconfirmed* and is therefore not cited.

**What plain greedy may and may not claim.** F(x) itself is submodular but **not monotone**, necessarily, since Risk and Cost are subtracted — so the classical (1−1/e) bound does not apply to F(x), and it does not apply to plain greedy on F(x) either. Plain greedy remains the **primary reported method**, justified as the standard practitioner heuristic and validated exactly by MILP at testbed scale, but it carries **no approximation guarantee** and the distorted-greedy bound must never be transferred to it. `scripts/structure_check.py`'s closing note previously said the guarantee "applies to the monotone submodular COVERAGE part", which is both the wrong part of the objective — g is all three gain terms, not Coverage alone — and an invitation to make exactly that illegitimate transfer. Rewritten.

**The preconditions are now verified rather than argued.** `structure_check.py` previously tested only the individual components and F as a whole. The theorem's preconditions are properties of the **aggregates**: g monotone submodular and non-negative, c **modular** — not merely submodular — and non-negative. A non-negative weighted sum of monotone submodular functions is monotone submodular, so the aggregate results *follow* from the component ones, but the script can test the actual preconditions directly instead of relying on that argument, so it now does, including a dedicated modularity test that checks marginal-cost invariance. On the frozen instance all five preconditions hold, which is what licenses γ = 1.

**Measured behaviour, which is unflattering and is reported anyway.** Distorted greedy is **beaten by plain greedy in 2 of the 20 cells of the comparison grid** (D24) — 34.2% below the exhaustive optimum at B=2 under default weights, and 11.4% at B=4 under δ=3 — while plain greedy attains the exact optimum in all 20. This is correct behaviour, not a defect: each of the k iterations carries its own acceptance test and a declined iteration is **not** retried, so when the early distortion factor pushes every candidate's distorted value below zero the algorithm permanently forfeits that slot. At B=2 the i=0 distortion of 0.5 halves every gain, nothing is accepted, and one decoy is placed against a budget of two. The docstring now forbids "fixing" this by looping to fill the budget or relaxing the acceptance test — the per-iteration structure is what the proof rests on, and removing it yields an algorithm that is neither plain greedy nor a guaranteed one. **The guarantee is a worst-case floor, not a promise of competitive average-case performance**, and it earns its place in the thesis through the *scalability* argument, where MILP validation is unavailable — which is what §7 already said before any of this was measured. *[Figures superseded by D25's normalisation: 3 of 20 cells, all under δ=3 — 17.1%, 25.4% and 11.4% below the optimum at B=2, 3 and 4. The algorithm and the reasoning are unchanged.]*

**Wiring completed, and an inaccuracy in D22 noted.** `distorted_greedy` is now reachable as `proposed_distorted_greedy` through `POST /optimize`, and `data/schema.sql`'s `method` CHECK constraint accepts it so its runs can be stored. D22's freeze statement declared distorted greedy one of the frozen methods while it was reachable only from Python and could not be recorded in the database — the freeze statement ran ahead of the implementation. Completing the wiring adds nothing to the frozen set; it makes the freeze statement true.
*Status: confirmed, implemented, verified. A27 closed. Reference: `docs/sources.md` #353, `src/optimizer/baselines.py`, `scripts/structure_check.py`, `src/api/main.py`, `data/schema.sql`, `formal-problem-definition.md` §7.*

**D24 — The exact MILP validator was not exact, and the comparison grid lived only in README prose. Both fixed before Phase D; the grid itself is unchanged.**
Two defects in the evaluation machinery, found during the D23 cleanup rather than sought. Neither changes an evaluation *input* — attack paths, objective, candidate set and risk values, methods — so the D20–D22a freeze holds.

**Defect 1 — an off-by-one made the exact validator inexact.** `metrics._intercepted_paths` records the interception stage **1-based** (`step_idx + 1`), and `Early(x)` uses `1 − stage/length`. `milp.py`'s objective coefficient used the raw **0-based** `step_idx`. The solver therefore over-valued every interception by exactly `1/length` and was maximising a different function from the one `metrics.score` reports, so it could return placements scoring **below** greedy on the true objective. On the comparison grid behind every quoted comparative number (defined under Defect 2), the pre-fix MILP was **suboptimal in 5 of 20 cells** — B=2 under default, α=3 and γ=3; B=3 under γ=3 and δ=3 — with shortfalls from 0.0125 to 0.1103, and at B=3, δ=3 it returned a **negative** F(x) where the true optimum is positive. **All five are cells where greedy and the centrality baseline choose different placements; the defect touched none of the 11 ties.** In four of them the pre-fix solver returned exactly the baseline's placement instead of the optimum, and in the fifth a placement that was neither. The defect concentrated exactly where the comparative evidence lies. A supplementary check over 30 δ/ε configurations found 6 suboptimal. After the fix the MILP matches exhaustive enumeration in 20 of 20 and 30 of 30.

**This is D16's failure mode in a second location, and D16's lesson was not fully applied.** D16 recorded an unnormalised Early proxy causing the same impossible symptom — an exact validator beaten by a heuristic — and corrected the formulation. It did not install a check that would catch the symptom again. `scripts/run_comparison.py` computed `gap = MILP − greedy`, printed it, and tested only `abs(gap) < 1e-9` to decide whether to print a success line. At its configured B=2 with default weights — **one of the five broken cells** — it printed `MILP F(x) - Greedy F(x) = -0.0193` and said nothing more. A negative optimality gap is logically impossible, and the script treated it as an unremarkable number for as long as the defect existed. The guard now exists in both `run_comparison.py` and `sweep.py`: a MILP result below greedy, or disagreeing with exhaustive enumeration, raises and refuses to report. **The general lesson, now paid for twice: when a decision turns on an invariant, assert the invariant in code — recording it in prose is what let this survive.**

**Precision widened at the same time.** CP-SAT needs integer coefficients, so `milp.py` rounds every term at a fixed `SCALE`. At 10,000 the solver was exact everywhere tested, but by thin margins: the gap between the optimum and the best strictly-worse placement was 34 integer units on the comparison grid and 8 on a δ-only check grid. `SCALE` is now 1,000,000, widening every margin a hundredfold. Re-solving 122 configurations changed no placement and no F-value. Recorded because it is a change to a frozen method's implementation, however inert — and because the exhaustive cross-check exists only while |L| is small, so on any larger instance rounding error would otherwise go unchecked.

**Effect on the optimality-gap claim.** Greedy's reported 0.00% gap **survives**: the defect did not bite at B=3 under default weights, the configuration the README quotes. But the reference it was measured against was wrong in a quarter of the comparison grid, so the claim was *unsupported* until now. It rests now on the corrected solver and, independently of both solver and heuristic, on exhaustive enumeration.

**Defect 2 — the comparison grid was recorded only in prose.** D20, D21, D22 and D22a quote results "across 20 budget/weight configurations" without restating them. The configurations lived in a single line of the README: **B = 1..4 across five weightings — default (α=β=γ=δ=1, ε=0.1), α=3, β=3, γ=3, δ=3.** That grid is now a constant in `scripts/sweep.py`, unchanged, and on the frozen inputs it reproduces D22a's **9 wins / 11 ties / 0 losses exactly**.

**Why that matters, recorded as a near-miss.** An earlier draft of this entry — delivered as a patch, caught in review before it was applied, never pushed — rewrote the README section containing that line without recognising it as the grid's definition. Having searched only variations of δ, the draft concluded that no grid had ever been recorded, declared the earlier results unreproducible, substituted a δ-only grid over B = 1..5 that reports a more favourable 13 / 7 / 0, deleted the README line, stated that its grid had been fixed before its result was read (also untrue), and recommended leading the results chapter with "greedy never loses" — which the paragraph after next shows is implied by optimality. Replacing the evaluation grid with a more favourable one on a false premise is exactly the failure the evaluation-integrity rule exists to prevent. Reviewing the patch before applying it stopped it, and it is the concrete reason the grid now lives in code rather than prose: a definition that can be deleted by editing prose is too fragile for an evaluation input. Any change to those constants requires an entry here stating its effect on every quoted number.

**What the 9 / 11 / 0 record is made of.** `sweep.py` reports this alongside the count, because the count alone misleads:
- **11 ties** — identical placements.
- **5 swap wins** — as many decoys as the baseline, different ones, equal coverage. Four are one decision repeated across weightings: at B=2, the Historian instead of Engineering WS-2, accepting **+0.065 Risk for +0.083 Early**. The fifth, at B=3 under γ=3, takes the HMI instead of Engineering WS-2 for marginally higher CritProt.
- **4 decline wins** — fewer decoys than the budget allows: B=1 under default weights, and B=1, 2 and 3 under δ=3.

The 9 wins rest on **5 distinct placement disagreements**.

**Two consequences for the primary research question (feeds A12).** First, greedy equals the exhaustive optimum in **20 of 20** cells, so on this instance it cannot score lower on F than any other placement: "0 losses" is implied by optimality. It measures search quality, which the 0.00% gap already reports, and says nothing about whether F is a good objective, because F is both what is maximised and the yardstick. §8's first clause — "a higher composite objective F(x)" — is therefore not a test of the contribution at testbed scale. Second, §8's second clause — equal or greater Coverage and CritProt at equal or lower Cost — **holds in 16 of 20 cells and fails in 4, and all 4 are the declines**, where lower coverage is bought with lower risk. Whether those are better placements depends on δ and on the D22a risk values: modelling choices, not measurements. Phase D needs an evaluation criterion outside F before it can speak to the objective's value; A12 lists the options, and whichever is chosen must be frozen before the campaign runs. *[D25: the first consequence is strengthened — on the frozen candidate set greedy is optimal by construction, because the gain part is modular. The second is superseded: the four declines came from dividing Risk and Cost by B, and under the fixed divisor the record is 5 wins / 15 ties / 0 losses with clause 2 holding in 20 of 20 — a fragile result, since the grid's δ=3 sits just below the first decline threshold (δ ≈ 3.03; see D25). The figures above remain the historical measurements of D24's objective.]*

**Grid sensitivity, reported as secondary.** *[Figures in this paragraph are D24's objective's. Under D25's fixed divisor the sample ranges from 5 to 9 wins. δ ∈ {1..5} gives 9 wins, 7 of them declines, with clause 2 in 13 of 20, and δ ∈ {0.1..1} gives 8 wins, all swaps. So "a higher win count mostly measures how often the method chooses to deploy less" no longer holds as stated — see D25.]* `sweep.py --sens` runs a hand-picked sample of alternative grids — a sample, not a bound. The split moves with the grid, from 8 wins / 12 ties to 15 / 5 across the sample, and the direction is informative: grids weighted toward high δ produce more wins, nearly all of them declines, while clause 2 falls. The δ-only grid over 1..5 gives 15 wins, 14 of them declines, with clause 2 holding in 6 of 20. On this instance a higher win count mostly measures how often the method chooses to deploy less.

**Also corrected.** `run_comparison.py` ran at B=2 while the README quotes B=3; its default is now 3 and it reports distorted greedy. The violation counts quoted in `metrics.py`, `README.md` and §5 (16 monotonicity / 18 submodularity) were correct for the **three-path** instance and went stale when D21 added P4; on the frozen four-path instance they are **30 and 57**, and F(x) pre-D20 shows 78 and 57. The archival records — D20's entry, `03-honest-review.md`, the iteration findings — keep their original numbers as historical measurements. F's submodularity violations equal Early's exactly on both instances (18 = 18 at three paths, 57 = 57 at four), so D20's claim that they were "driven entirely by the Early mean" is demonstrated rather than asserted.

**Stale references corrected in the same batch, none affecting a result.** `graph_model.write_computed_scores()` still defaulted to the pre-D20 two-term weights (0.5, 0.5) and silently inherited w₃ = 0.2, so running the module as a script wrote criticality with weights summing to 1.2; it now uses the optimizer's 0.4 / 0.4 / 0.2. Nothing reads the stored column — the optimizer and API compute criticality live — so no result changed, as a re-run of the comparison grid confirms. `00-project-phases.md` still called Phase C "next" and described Phase D as "Methods 1–3 against P1–P3"; `00-project-index.md` kept its own status line ("Phase B is next") despite stating that status lives only in the phase tracker; `02-system-flow.md` presented pre-D20 output as current and listed discrepancies D20 had resolved; the README listed a `references/` directory deleted on 15 September. All corrected or marked superseded in place. `00-project-timeline.md` is anchored on TA-1, which did not take place on 22 September (guide unavailable) and has not been rescheduled; it is marked stale rather than rebuilt, because rebuilding it needs A14's dates. A18 was re-inspected: see `00-action-items.md` and `sources.md` #356–357.
*Status: confirmed, implemented, verified against exhaustive enumeration. Reference: `src/optimizer/milp.py`, `scripts/sweep.py`, `scripts/run_comparison.py`, `src/graph_model/__init__.py`, `README.md`, `src/optimizer/metrics.py`, `formal-problem-definition.md` §5 and §8, `00-action-items.md` A12 and A18, `00-project-phases.md`.*

**D25 — Before Phase D, two defects in the frozen inputs. On the seeded candidate set greedy is optimal by construction, and dividing Risk and Cost by the budget made a decoy's value depend on the budget. The divisor is now a fixed K = 4; the candidate set is corrected next, in its own entry.**
Neither defect was found by looking at an evaluation result: no evaluation campaign has run. The first came from asking *why* greedy equals the exhaustive optimum in all 20 comparison-grid cells (D24). The second surfaced on 30 September while the consequences of the first were being worked through. Only the second changes an input in this entry.

**Finding 1 — greedy is optimal by construction on the seeded candidate set.** *Verified.* Each attack path meets exactly one candidate: P1 meets the HMI (step 5 of 5), P2 the DMZ Jump Host (step 1 of 4), P3 Engineering WS-2 (step 2 of 2), P4 the Historian (step 2 of 3). PLC-02 is on no path. So no candidate's gain depends on any other, and the gain part g is **modular** — zero violations in an exhaustive test of every subset. F = g − c is then modular too, and for a modular objective under a cardinality constraint, taking the best positive-value candidate at each step *is* the optimum. Three consequences:
- "Greedy equals the exhaustive optimum in 20 of 20" and the 0.00% gap show that the implementation is correct — greedy, MILP and enumeration agree. They say nothing about the quality of the search method. D24's first consequence is therefore strengthened: on this set it holds by construction, not merely by small size.
- Distorted greedy's preconditions still hold (a modular g is trivially submodular), but nothing on this set can show whether its guarantee matters.
- Held-out-path evaluation, one of A12's options, is degenerate here. A held-out path's only candidate contributes nothing on the training paths and carries risk and cost, so a path-aware method never selects it and scores 0 on that path by construction. Random and centrality can still pick it by chance or by rank.

**Finding 2 — the seeded candidate set bypasses §4's Filter 1.** *Verified from `data/seed.sql`, `data/demo_ai_suggestions.sql` and `src/api/main.py`.* Filter 2 (the D22/D22a rubric) was applied to all five seeded candidates; Filter 1 was not.
- Historian, HMI and PLC-02 are seeded with `is_candidate` = 1 but all four criterion scores NULL and `human_confirmed` = 0. The optimiser reads `is_candidate` alone, so the seed bypasses the human-confirmation gate that `02-ai-role.md` §8 and `02-system-flow.md` Flow B describe.
- Engineering WS, PLC-01 and PLC-03 (RTU) lie on attack paths and have no row at all.
- The three confirmed rows (DMZ Jump Host, Engineering WS-2, OT Firewall) come from `data/demo_ai_suggestions.sql`, headed "for Screen 3 demo purposes only". It transcribes worked examples from the design documents; no Screen 3 review is recorded.
- The DMZ Jump Host's confirmed criterion 4 is `no`, yet the seed sets `passes_plausibility` = 1. The only implemented Filter 1 rule, in `POST /candidates/{id}/confirm`, fails any `no`, so confirming that row through the API would remove the DMZ Jump Host from the candidate set. §4 never states how the four scores combine, so either the rule or the row is wrong. The DMZ Jump Host is in every greedy placement.
- The seed departs from the specification's own worked example of §4 in `testbed-architecture.md`. The example passes a decoy Engineering WS; the seed has Engineering WS-2 and no row for Engineering WS. The example's decoy PLC mimics PLC-01/02, but PLC-01 has no row.
- The documented reason for those two is search-space design ("one real, one modeled gives the optimizer an actual choice"; "so 'which PLC' is a real decision"), not a filter outcome.
- One ambiguity must be settled before the filters are applied. WS-2 is modelled as a real workstation that P3 traverses, but its stored plausibility reasoning justifies it as "a parallel decoy workstation". What x_l = 1 means physically — a decoy of l's type at l's network position, which an attacker reaching l interacts with — needs stating first, because criteria 1 and 2 depend on it.

**Finding 3 — dividing Risk and Cost by B made a placement's value depend on the budget.** *Verified.*
- The DMZ Jump Host alone scored −0.063 at B=1, +0.332 at B=2 and +0.529 at B=4.
- Under δ=3 greedy placed 0, 0, 1 and 4 decoys at B=1..4, so decoys "too risky" at a budget of two were all worth deploying at four.
- Each decoy's penalty was (δ·r + ε)/B, so budget and risk weight were confounded across the whole grid.
- It also contradicted `02-optimization-formulation.md` §2, which stops greedy early so the evaluation can report "the method found K decoys sufficient" — "sufficient" depended on B itself.
- D20 chose the divisor B for boundedness and modularity and never recorded this side effect.

**Decision — Risk and Cost are divided by a fixed K = 4.**

*Criteria.* These were fixed before any option was compared, from how a real site works:
1. **Budget-free.** The adversary sees the decoys deployed, never B. B is a procurement and change-management cap (`04-deployment-requirements.md` §1, §5, §8). One commercial method even treats the count as an *output* of asset density and attack history (#347 — from the patent's description; its granted claims have not been read, A29) *[D28: they have now been read (A29's claims half). Claim 6 also fixes a position, on or near the central node.]*. Detectability is a property of each deployed decoy (#352).
2. **Modular** (D20; a precondition of D23).
3. **On the scale of the gain terms**, which was D20's reason for normalising at all.
4. **Independent of the candidate set**, which changes next.
5. **Invariant to how finely the threat model is written.** An analyst can write the same threat as 4 paths or 40.

*Tests.* Each option was scored on the DMZ Jump Host alone under default weights:

| Divide by | B=1 / 2 / 4 | Every path written twice | One unused candidate added | Verdict |
|---|---|---|---|---|
| B (D20–D24) | −0.063 / 0.332 / 0.529 | unchanged | unchanged | fails criterion 1 |
| \|L\| | 0.569 throughout | unchanged | 0.569 → 0.595 | fails criterion 4 |
| \|P\| | 0.529 throughout | **0.529 → 0.628** | unchanged | fails criterion 5 |
| nothing (raw sum) | −0.063 throughout | unchanged | unchanged | passes, but default weights would place nothing in the default and δ=3 rows; needs a new default δ |
| **K = 4** | **0.529 throughout** | **unchanged** | **unchanged** | **passes all five, with the caveat below on criterion 1** |

*Why 4.* It is the smallest budget-independent constant that keeps Risk and Cost in [0,1] for every budget of the declared grid. That is D20's boundedness reason, with the budget taken out.
- **K is frozen from here and is not re-derived if the grid changes.** Criterion 1 holds per run: a placement's value no longer depends on its budget. K itself is not a physical quantity, though — dividing by K equals rescaling δ and ε — so a rule tying it to the grid's largest budget would move the budget confound from the run to the grid. Changing K is an objective change needing its own entry. For budgets above 4, Risk and Cost can exceed 1, which is harmless. `sweep.py` prints the divisor in its header, and `run_comparison.py` flags a budget above K.
- 3 fails the rule: Cost would reach 4/3 at B=4. It would also have left the README's B=3 headline unchanged, which is a reason tied to results and played no part.
- Another instance family, for example synthetic instances under A12, must fix its own constant before its first run, never from the budget of a run.
- Raw sum and K = 4 are the same option in different units. Dividing by 4 equals the raw sum with δ and ε divided by 4. K = 4 keeps the frozen grid's δ values meaningful.

*How the choice was made.* The user decided on 30 September, after the tests and before the grid was re-run.
- **Claude's first recommendation was \|P\|.** It was withdrawn when the user asked for the analysis to be grounded in how an industrial site actually works, which produced criterion 5 and the path-count test that \|P\| fails.
- **Two consequences were deducible from recorded numbers and were known when the choice was made:**
  - the B=4 column cannot change, because K = B there;
  - no declared cell would decline, because no weighting declined at B=4.

**Effect on results, in full — the comparison grid constants are unchanged.** *Verified by `scripts/sweep.py`, `scripts/run_comparison.py` and `scripts/structure_check.py`.*

*Headline record against centrality.*
- **9 wins (5 swap, 4 decline) / 11 ties / 0 losses → 5 wins (5 swap, 0 decline) / 15 ties / 0 losses.** Distinct placement disagreements fall from 5 to 2, and the four decline wins become ties.
- **The 5 remaining wins are two decisions.** At B=2 under default, α=3, β=3 and γ=3, greedy takes the Historian instead of Engineering WS-2 (+0.0325 Risk for +0.0833 Early). At B=3 under γ=3 it takes the HMI instead of Engineering WS-2 (+0.0150 Risk for +0.0108 CritProt).
- **§8's second clause: 16 of 20 → 20 of 20.** This is not an improvement in the method. The four failures were the four declines, and on this grid the declines existed only because dividing by a budget below 4 inflated every penalty.

*Checks that did not move.*
- Greedy equals the exhaustive optimum in 20 of 20 cells, unchanged and by construction (Finding 1).
- The MILP matches exhaustive enumeration in all 20 declared cells and in all 68 distinct configurations of the `--sens` sample, which include the declared 20. `sweep.py` now asserts this for the sample too; before D25 it only tallied it.
- The smallest rounding margins are 3,826 units on the declared grid (B=4, δ=3) and 413 across the sample (B=3, δ=0.75). `sweep.py` now computes both and raises if either falls within the rounding bound. Rounding can shift the comparison of two placements by at most 3|P| + B units, which is 16 on the declared grid.
- Structure: preconditions still hold; F is still submodular and not monotone (16 monotonicity violations, as before).

*Distorted greedy: 2 → 3 cells below plain greedy, all under δ=3.*
- It is 17.1%, 25.4% and 11.4% below the optimum at B=2, 3 and 4.
- At B=2 under default weights it now reaches the optimum; it was 34.2% below.
- The algorithm is unchanged.

*B=3 headline.* The placement is unchanged (DMZ Jump Host, Engineering WS-2, Historian), and all four methods still coincide.
- F: 1.0303 → 1.2170
- Risk: 0.65 → 0.48
- Cost: 1.00 → 0.75
- Random mean: 0.7097 → 0.8942

*`--sens` sample, secondary.*
- Wins/ties: 5/15 on the declared grid; 6/14 at one-at-a-time 2; 8/12 for δ ∈ {0.1..1}; 6/14 for {0.25..3}; 5/15 for {0.5..3}.
- **9/11 for δ ∈ {1..5},** with 7 declines and clause 2 holding in 13 of 20. Which decoys are worth deploying no longer depends on the budget; a cell declines when its budget exceeds that number. At δ=4 greedy places only the DMZ Jump Host at every budget from 2 to 4, and at δ=5 nothing at any budget, so "K decoys sufficient" is stable across budgets, which is what `02-optimization-formulation.md` §2 wanted.
- The unpushed D24 draft grid gives 8/12. Its four declines are at B=5, where greedy leaves out PLC-02; that decoy covers nothing, so leaving it out is not a risk trade-off, and clause 2 holds.

*Which way it cuts.* The proposed method's record against the baseline weakens: fewer wins, fewer distinct disagreements, and the decline illustration that D20, D21 and D22 relied on leaves the declared grid. Clause 2 looks better, but for a reason unconnected to the method. Both are reported.

*How fragile the new result is — found by an independent review of this batch, verified.* Under K = 4 each candidate's value turns negative at a δ of its own: HMI at 3.025, the Historian at 3.144, Engineering WS-2 at 3.271 and the DMZ Jump Host at 4.068. The declared grid's δ=3 sits just below the lowest threshold: the HMI is worth +0.0038 there, which is also the 3,826-unit MILP margin.
- At δ=3.05, greedy places 3 decoys at B=4 and clause 2 fails.
- At δ=3.25, it declines at B=3 and B=4.
- At δ=3.5, it places only the DMZ Jump Host at every budget.

"No declared cell declines" and "clause 2 holds in 20 of 20" therefore rest on where the grid happens to put δ, not on a robust property. They must not be quoted without this. Moving δ to 3.1 or beyond to bring the declines back would be choosing the grid by its results. The δ range of the sensitivity sweep is set under A12, on its own grounds.

**Claim rule, fixed before the candidate set changes.**
- **On the seeded set, the thesis may claim:**
  - the formulation
  - its verified structural properties
  - that the objective's placements differ from centrality's (two decisions, with the trade-offs above)
  - that the implementation is exact
- **It may not claim:**
  - search quality from greedy equalling the optimum
  - any empirical value of distorted greedy's guarantee
  - robustness from held-out paths
- **After §4 is applied:**
  - If the new set's g is still modular, which `sweep.py` and `structure_check.py` now test and report, these limits stand.
  - If it is not, the testbed supports exactly one further statement: that greedy matched the exact optimum on one non-trivial instance of this size.
  - Broader search-quality claims need a family of instances (A12).
- **Whatever the filters produce is accepted,** including a set that stays modular. The new candidates are scored before any comparison is run on them.

**Corrected in the same batch; none of these changes a result.**
- **`metrics.score` fallback removed.** It divided by |x| when no budget was passed. That is a mean, which is not modular (D20's Early defect again), and it made Cost 1.0 for any placement. No caller reached it.
- **`structure_check.py`** now asserts that its own F equals `metrics.score` on every subset, and reports whether g is modular.
- **`distorted_greedy`'s docstring** had claimed the testbed "shows this shape of behaviour at delta=3", meaning the Appendix A failure mode. Greedy's stops there matched the optimum, so the claim was wrong, and it is withdrawn.
- **`milp.py`'s module docstring** still described the k-enumeration that D20 removed. It is now marked as history.
- **`testbed-architecture.md`'s role column** still gave HMI a P3 step (rerouted to WS-2 by D19), placed PLC-01 on P2 (the seeded P2 runs through PLC-03), and named the Attacker "entry point for all three paths".
- **`04-deployment-requirements.md`** still quoted "5 candidates, 3 paths", a MILP that "solves once per coverage count" (removed by D20), and detectability scoring as "currently qualitative" (replaced by D22/D22a).
- **`src/api/main.py`, `02-ai-role.md` and `02-system-flow.md`** described the candidate set as confirmed, or described the human-confirmation gate as unbypassable. The seed bypasses it, and the wording now says so. `02-system-flow.md` §9 also said "three attack paths".
- **Screen 3 (`src/frontend/src/PlausibilityReview.jsx`) re-sent AI suggestions over confirmed values.** The card displays your edit, else the confirmed value, else the AI suggestion. "Confirm" sent your edit, else the AI suggestion, else the confirmed value. For the DMZ Jump Host, that would have silently replaced the human `no` on criterion 4 with the AI's `mostly` during A32. The independent review found this. Confirm now sends exactly what the card displays. The fixed frontend builds cleanly (checked on a scratch copy). It has not been exercised in a browser. One consequence: with the stored `no` now sent faithfully, confirming the DMZ Jump Host under the current rule removes it from the candidate set. That is why A32 settles the combination rule before anything is confirmed.

**What no modular form captures — limitations for the thesis, not decisions.**
- **The burn effect.** Once one decoy is fingerprinted, the adversary knows deception is present. A sum over decoys over-counts relative to "at least one fingerprinted".
- **Density.** Several decoys in one small segment can look anomalous to an adversary doing asset discovery.

Modelling either one needs a non-modular cost, which forfeits distorted greedy's guarantee (D23).

**Next — A32, planned before this entry's results existed.** The user proposed applying §4 on 30 September, before the normalisation defect surfaced. Finding 2 widens it from six assets to the whole of V except the Attacker node: the three confirmed rows are demo transcriptions, and one of them conflicts with the only implemented rule.
1. Two things are settled before any scoring: what `x_l = 1` means physically, and how the four criterion scores combine into pass or fail.
2. Rows are seeded for the assets that have none, so that Screen 3 lists them.
3. The first-pass route is the user's call. D12's route is the Colab notebook (A20, not yet built). The supported no-AI configuration is the user scoring directly (`04-deployment-requirements.md` §2). A Claude-drafted first pass would be a process change needing its own entry.
4. Every score counts only after the user confirms it in Screen 3. New candidates receive D22a detectability scores.
5. The set is frozen, every check is re-run, and the effect is stated against this entry's numbers, in its own entry, before Phase D.

*[D26 settles steps 1 and 3 and completes step 2.]*

*Status: confirmed, implemented, verified against exhaustive enumeration. Reference: `src/optimizer/metrics.py`, `src/optimizer/milp.py`, `src/optimizer/baselines.py`, `scripts/sweep.py`, `scripts/structure_check.py`, `scripts/run_comparison.py`, `formal-problem-definition.md` §4, §5, §7 and §8, `README.md`, `00-action-items.md` A12, A15 and A32, `testbed-architecture.md`, `04-deployment-requirements.md`, `02-optimization-formulation.md`, `00-project-phases.md`, `02-system-flow.md`, `02-detectability-rubric.md`, `05-thesis-structure.md`, `02-ai-role.md`, `src/api/main.py`, `src/frontend/src/PlausibilityReview.jsx`.*

**D26 — Filter 1 is defined before any scoring: what a candidate is, how the four scores combine, #40's four-level scale, and the scoring route. The seed no longer pre-judges the candidate set, so L is empty until the A32 review.**
A32's steps 1 and 3 were the user's calls. They were made between 1 and 3 October 2026, after #40 had been re-read in full from a printout the user supplied. No evaluation campaign has run, and no Filter 1 score existed when these rules were fixed. #40 follows the same order ("we fixed the decision rules before scoring").

**1. What a candidate means.** `x_l = 1` places a decoy imitating `type(l)` in `zone(l)`, on the same segment and behind the same conduits, so that attack paths through `l` pass where it sits. It does not change the real asset. Whether an attacker would interact with the decoy is what criterion 2 scores; the definition does not assume it. This is D25's proposed wording, tightened.

**2. Combination rule: an asset passes Filter 1 only if all four criteria are answered and none is No. Mostly No passes.** User's choice, on Claude's recommendation.
- #40 defines "admits a decoy" by Feasibility alone. None of its 80 admitted techniques scored No on a later criterion (Interaction 34/24/22/0, Intelligence Yield 71/8/1/0, Malice Fidelity 30/44/6/0, where the last zero is by arithmetic because the printout truncates that column), so the paper never had to decide what a later No means. "Exclude on any No" therefore contradicts no result in the paper.
- The objective counts every interception as a detection and has no false-positive term. Without the rule, it would credit detections that the rubric says will not happen (Interaction No) or cannot be told apart from routine activity (Malice fidelity No).
- *Alternative considered:* #40's literal rule, where only a Feasibility No excludes. Rejected: implausible and off-path sites would stay in L. The random and centrality baselines draw from L, so such sites would hand them picks that gain nothing.
- Intelligence yield gates too, for simplicity. #40 found it almost never limiting.

**3. Scale: #40's four-point forced choice (Yes / Mostly Yes / Mostly No / No) with Table 1's level definitions, reproduced unchanged.** User's choice, on Claude's recommendation.
- *Two further rules from #40:* ties between adjacent levels go to the lower level, and the first No ends the evaluation.
- *One adaptation:* each criterion is scored for "the best case a well-instrumented decoy could plausibly produce" (#40), but at the actual network position, not in principle.
- *What the old scale did:* yes / mostly / no merged #40's two middle levels. The prompt's "if you are genuinely unsure, say mostly" re-introduced the neutral default #40 removes by design.
- *Effect at the boundary:* pass or fail depends only on No under either scale. What changes is the boundary: a tie between No and Mostly No now goes to No, where "unsure, say mostly" sent it to a pass.
- *Licence:* Table 1 is reproduced with credit under CC BY-NC-SA 4.0 (#368). Licence reading, not legal advice.

**4. Interaction is judged against the paths as modelled.** Each path is named, and the encounter is called a Sweep or a Seek.
- An asset in no path's asset sequence scores No, because the model cannot credit it with an interception. Consequence known now: PLC-02 and the Backup Control Switch cannot pass, so PLC-02, a member of D25's set, leaves L unless the threat model changes. *[D27: only PLC-02 now, kept off-path as option (a). P5 runs through the switch.]*
- An asset on several paths is scored per path, and the lowest level is recorded ("weakest path decides"). A best-case score would credit paths the rubric says the attacker would not take that way. The reviewer gives each path's level in the required reason. Only Engineering WS (P1, P4) is affected.
- The path rule's No needs no written reason: the rule is the reason. The API, Screen 3, the restore script and the candidate loader all enforce it.

**5. Malice fidelity names the routine benign activity at the position before it is scored.** This is #40's own proposed refinement. The OT examples are this project's.

**6. Route A: D12's route, an AI first pass with a human reviewing every card.** The user's choice. Recorded in full because Claude recommended otherwise. Four routes were considered:
- **A**, this one;
- **B**, the user scores alone with no AI, which is the cheapest but leaves the AI assist unevaluated;
- **C**, the user scores every card blind and then compares with the AI;
- **D**, Claude scores. D was rejected outright: it would replace the expert rather than support them, which #40 advises against, and the scorer would be the system's builder.
- *Claude's recommendation was route C:* the user scores every card before seeing the AI's answer, and the two are then compared. The evidence closest to this setting found that reviewers move toward an LLM's suggestion even when they review it:
  - #362: overlap with the LLM's labels rose from about 40% to 81–87%, and evaluating the LLM against the assisted labels inflated its F1 from .47 to .79;
  - #363: requiring a corrected value reduced corrections.
- *Claude's own earlier correction went too far.* On 30 September Claude had called this anchoring argument overstated, on the strength of #359–#361. Those studies are linguistic annotation with accurate taggers, and the two closer studies point the other way.
- *The user chose A* to keep the reviewer's work low, and because the AI's value at plant scale is exactly that reduction.
- *The safeguards adopted:*
  - **Three blind cards.** They are drawn at random, before any AI output exists, from the eight assets on a modelled path. They are scored before their AI answers are shown, and give the one unanchored agreement measure. Their first answers are written once, to their own columns, and never change. *[D30: the review restarted once, on a fresh database and before any AI output existed. The first answers are those given on that database.]* The final answers may still be revised, with a reason. Draw: `random.Random(20261003).sample(population, 3)` under CPython 3.11, where the population is DMZ Jump Host, Engineering WS, Engineering WS-2, HMI, Historian, OT Firewall, PLC-01 and PLC-03 (RTU), sorted by name. Result: **DMZ Jump Host, Historian, PLC-03 (RTU)**.
  - **A written reason** on a blind card, on a card with no AI suggestion, after changing any AI answer, and for any Mostly No or No.
  - **No fallback to the AI's answer.** The confirm endpoint used to fill a blank with the AI's suggestion.
  - **Each card shows the asset's attack-path steps.** The design-time rationale text, which pre-judged outcomes, is no longer shown.
- *Fallback route:* if the notebook produces no suggestions within two weekends of the blind cards being finished, the remaining cards are scored directly (route B), with reasons.
- *Model:* Qwen3-14B per D12, in 4-bit, because 16-bit weights do not fit a 16 GB T4 (#364–#366). With the embeddings and output layer left at 16-bit the total is about 10 GB (#376). Qwen3-8B is pre-declared as the fallback if 14B cannot load. Decoding is non-thinking and greedy, for reproducibility. That departs from the model card's sampling recommendation (#364), and the departure is declared.
- *What the thesis may say:* the acceptance rate on the seven pre-filled cards is reported as a limitation, not as evidence that the AI is accurate. The blind cards give the agreement measure, reported as counts.
- *At plant scale (thesis design, not built):* the AI scores everything, and humans review an exception queue: boundary answers, answers the AI flags as unsure, and a random audit sample.

**Deferred, not decided:**
- The user's idea of presenting Screen 3 as a network view, with cards in a side panel (A34).
- The K wording for further instance families (A12).
- Closing A18.

**Corrections made in this batch.**
- `02-ai-role.md` §7 said a free Colab T4 runs Qwen3 14B "at full speed with room to spare". It cannot: 14.8B parameters are about 29.6 GB at 16-bit, against 16 GB, and Colab does not guarantee any GPU (#364–#366).
- §8 said confirmation means the model "can be wrong without anything downstream trusting it by default". That overstated what review achieves (#362, #363).
- §10's evaluation by match rate would have been inflated by design. It is replaced by the blind-card measure.
- `formal-problem-definition.md` §4, D3 and #329 cited "source 53" for the rubric, which is an unrelated IEC 62443 paper. The source is #40.
- `00-glossary.md` still said "Applying it to the ICS matrix is new to this project". That claim was dropped at iteration 11.

**Implemented.**
- `src/plausibility/` holds the rubric rules: the sequence, path, combination and reason rules, and "weakest path". It also holds the AI prompt, the parser and the scoring loop. The API, both scripts and the notebook all use them, so no second copy of a rule exists.
- Schema: four-level `CHECK` constraints, plus `blind_first`, the write-once `blind_*` columns, `human_reason` and `ai_model`. `detectability_risk` is now NULL when unscored, not 0.0.
- Seed: rows for all ten non-Attacker assets, all unscored, none in L. `data/demo_ai_suggestions.sql` was removed: its values were written by Claude, so loading it would have made the first pass Claude-drafted, which is route D.
- `load_candidate_locations` refuses an unreviewed candidate and a candidate without a D22a score. It recomputes each candidate's Filter 1 result from the four recorded answers, path rule included, rather than trusting the stored flags.
- `notebooks/plausibility_scoring.ipynb` (A20).
- `scripts/import_plausibility_scores.py`, specified in `02-prototype-architecture.md` §4 since Phase B but never built.
- `scripts/review_io.py`: the committed review record. An export taken while a blind card is open leaves that card's AI fields blank.
- The import never changes or clears an AI suggestion already stored on a confirmed card.
- Screen 3 rebuilt: blind cards first, path steps, four levels, the reason box, no AI fallback.

**Independent review, and what it changed.** A separate agent reviewed the batch before handover. It had not seen the work produced, as D25's review had not. Its findings were fixed before handover:
- *High:* a confirmed blind card could be re-confirmed after its AI answer had been shown, overwriting the one unanchored measure. Fixed with the write-once `blind_*` columns.
- *Medium, in four places:*
  - the path rule was enforced only for AI suggestions, so a human could have passed PLC-02;
  - the loader trusted stored flags, so the legacy SQL loaded over a reviewed database would have been accepted;
  - a null reason in the model's output would have crashed the notebook run;
  - an export taken mid-review would have written open blind cards' AI answers.
- *Lower:*
  - error messages that could hint at a blind card's AI level;
  - a stale suggestion surviving a failed re-run;
  - gaps in the parser (duplicate path entries, "Neither", echoed path names, a dash read as a level);
  - the notebook's restart advice, dtype and version pinning;
  - the 4-bit memory figure, about 10 GB rather than 7.4 GB.
- *Stale text, corrected in place:*
  - thesis-facing text that still claimed the rubric was applied to "the ICS matrix" (`05-front-matter-pack.md`, `01-thesis-citation-shortlist.md`), a claim dropped at iteration 11;
  - PLC-02's "search-space richness" position (D21, A13, `testbed-architecture.md`), which §4's path rule overtakes;
  - D13's single-write-path rule, which needed a note on the offline setup scripts.

**Effect on results.** No evaluation result exists, and none changes.
- D25's numbers stay reproducible. With `data/legacy/d25_candidate_set.sql` loaded and `--legacy-d25` passed, `run_comparison.py`, `sweep.py --sens` and `structure_check.py` print output identical to commit `1a93af9`'s, apart from a five-line banner. Verified 3 October.
- By default L is empty, and every script and `POST /optimize` refuse to run, with the reason.
- Known in advance: PLC-02 and the Backup Control Switch cannot pass Filter 1. Everything else depends on the review. *[D27: the switch now lies on P5; only PLC-02 remains.]*

*Status: confirmed and implemented. Verified, after the review's fixes:*
- *the confirm rules through the API: sequence, path rule, reason rule, blind hiding, write-once blind answers, and refusal of unscored or unreviewed candidates, including the legacy SQL loaded over a reviewed database;*
- *an import → review → export → rebuild → restore round trip that reproduced the database exactly;*
- *the frontend build;*
- *Screen 3, driven in Chromium through the blind, import and review steps;*
- *the legacy reproduction.*

*The notebook's model-loading and generation cells are untested: neither a GPU nor Hugging Face is reachable from this environment. Its prompt, parsing and loop run locally against a stand-in model. The first Colab run is the test of the rest.*

*Reference: `formal-problem-definition.md` §4, `02-ai-role.md` §7–10, `02-data-model.md`, `02-prototype-architecture.md` §1–4, `02-system-flow.md`, `02-detectability-rubric.md`, `testbed-architecture.md`, `threat-attack-model.md`, `00-glossary.md`, `00-project-phases.md`, `00-repository-structure.md`, `00-action-items.md` A13, A18, A20, A26, A29, A32, A33 and A34, D3, D12, D13, D21 and D25 (pointer notes), `05-front-matter-pack.md`, `05-thesis-structure.md`, `01-thesis-citation-shortlist.md`, `iteration-11-findings.md`, `04-deployment-requirements.md`, `README.md`, `.gitignore`, `data/schema.sql`, `data/seed.sql`, `data/legacy/d25_candidate_set.sql`, `src/plausibility/`, `src/graph_model/__init__.py`, `src/api/main.py`, `src/optimizer/baselines.py` (docstring), `src/frontend/src/PlausibilityReview.jsx`, `src/frontend/src/Dashboard.jsx`, `src/frontend/src/App.css`, `scripts/`, `notebooks/plausibility_scoring.ipynb`, `sources.md` #40, #319, #328, #329, #357, #359–#376.*

**D27 — A fifth attack path, P5, runs through the Backup Control Switch, and PLC-02 stays off every path by the user's choice. Both decided on 4 October 2026, before any Filter 1 score existed.**
The user objected to D26's stated consequence that the Backup Control Switch "cannot pass": "we will not out a single asset … backup control switch even not connected play important part, and is subject to exploit".

**Claude's framing was wrong, and this is the correction.** D26 presented the switch's exclusion as a property of the asset. It was a gap in **P**.
- The switch is connected: DMZ Jump Host → switch → PLC-01 and PLC-02.
- `testbed-architecture.md` gives it exactly one purpose: "a second conduit tests whether your placement covers both routes to the same target". No path ever used it.
- ATT&CK for ICS lists **A0015 Switch** as an asset that 33 techniques target (#377, #378). VPNFilter is documented malware that sniffed ICS traffic from inside network devices (#379, #380).

**Why simply keeping the switch on the list would not have worked.** F credits only interceptions on modelled paths. A decoy on the switch would earn nothing, so the optimiser would never choose it. Random and centrality placement could choose it and score nothing for it, which would unfairly favour the proposed method. It would be included in name only.

**1. P5 is added (the user's choice, on Claude's recommendation).**

| Step | Asset | Tactic | Technique | Grounding |
|---|---|---|---|---|
| 1 | DMZ Jump Host | Initial Access | T0822 External Remote Services | #383; the 2015 Ukraine attack entered through the control-system VPN |
| 2 | Backup Control Switch | Lateral Movement | T0866 Exploitation of Remote Services | #382; Switch is a targeted asset |
| 3 | Backup Control Switch | Discovery | T0842 Network Sniffing | #381; VPNFilter "monitors ICS traffic" (#380) |
| 4 | PLC-01 | Impair Process Control | T0836 Modify Parameter | P1's verified step at the same PLC |

- *Route:* the testbed's existing edges.
- *Target:* PLC-01, because P1 reaches it by the primary route and the switch exists to test both routes to the same target.
- *Composition:* P5 combines documented techniques rather than replaying one campaign, as P3 does. That is stated in `threat-attack-model.md`.
- *T0855 Unauthorized Command Message* would fit step 4, but its page could not be fetched (#384), so the verified T0836 is used instead.

**Why D21 permits this.** D21 froze the paths "unless a documented defect emerges". The defect is documented twice over: the testbed's stated purpose was never modelled, and MITRE treats switches as targets.

**Why this is not D21's error in reverse.** D21 refused to add a path "solely to make [PLC-02] selectable". P5 does make the switch selectable, but as a consequence. The reasons are the documented ones above, and the choice of target follows the same stated purpose rather than any asset's selectability.

**2. PLC-02 stays off every path: option (a), the user's choice on Claude's recommendation.** PLC-02 is scored like every asset. Its Interaction is No because no modelled attack reaches it, and the thesis reports it as a plausible decoy site the modelled threats never reach: a finding about the threat model's coverage, not a silent removal.
- *(b) Include it anyway* was rejected. It would earn zero credit and unfairly favour the proposed method over the baselines.
- *(c) Give it a path* was rejected. No documented attack targets PLC-02 specifically, so a path would repeat D21's error.

**Effects, stated before any scoring.**
- |P| goes from 4 to 5.
- Three assets now lie on two paths each: the DMZ Jump Host (P2, P5), PLC-01 (P1, P5) and Engineering WS (P1, P4). D26's reason rule asks their reviewer for each path's level.
- P5 can meet up to three candidates, and two of them also sit on other paths. So the gain part of F is unlikely to stay modular, and greedy is unlikely to remain optimal by construction. That is a side effect, not the motive, and whether it holds depends on the review.
- The blind draw stands. It was made over the eight assets then on a path, before any scoring or AI output. P5 later put the switch on a path. Redrawing would create a second draw to choose between, which is worse than a recorded population that changed afterwards.
- `data/legacy/d25_candidate_set.sql` now removes P5 as well, because the pre-D26 numbers were measured on P1–P4. Those numbers still reproduce exactly.
- No evaluation result exists, and none changes.

**Implemented:**
- `data/seed.sql`: P5 and its four steps.
- `data/legacy/d25_candidate_set.sql`.
- `threat-attack-model.md`: the P5 section.
- `testbed-architecture.md`: the role and verification tables, and the PLC-02 and D26 notes.
- `formal-problem-definition.md` §3–4.
- `00-glossary.md`, `00-project-phases.md`, `02-system-flow.md`, `02-data-model.md`, `04-deployment-requirements.md`, and `00-action-items.md` A32.
- Pointer notes on D21 and D26.
- `sources.md` #377–#384.

*Status: confirmed, implemented and verified. With P5 removed, the legacy reproduction is identical to commit `1a93af9`'s output. The API lists P5's steps, and asks for per-path reasons on the three two-path assets. The prompt contexts show P5. All scratch test suites and the browser test pass.*

**D28 — Corrections from the 6 October full-text reads and from A2, other stale text, and two changes to P's step labels made before any Filter 1 score: P1 step 5's tactic and P2 step 1's technique. No number changes.**
On 6 October 2026 the user supplied full texts and printouts that had been out of reach: `sources.md` #29, #34, #250, #282 with #325, #315, #330, #347, #372 and #386–#389. Commit `bb9dd6e` logged what they say. This entry records what they overturn in the rest of the repository, and other stale text found while propagating them.
- The 6 October session planned it as "a new D28 correcting D5, plus notes on D2, D7, D10 and D18", and held it for the user's go-ahead.
- A check on 11 October found six more places that plan had missed, and building this batch found more. All are listed under item 8.
- The user started the batch on 12 October 2026, and chose T0822 for P2 step 1 on 13 October (item 7).

**1. D5's evidence is withdrawn: nothing in the repository supports weighting operational risk heavily.**
- #250 (D3O-IIoT, *Scientific Reports* 16:2389; #324) uses the reward r = 0.70·A + 0.20·D − 0.06·F − 0.04·C, where F is the paper's false-positive indicator, not this project's objective. That penalty carries the second-smallest weight, and the authors credit the low penalty weights with allowing "aggressive defense".
- The indicator is 1 when a deception action other than no-op is applied to benign traffic: a false alarm caused by the defender's own action.
- Removing the term cut mitigation, not precision. The attack-mitigation rate fell from 12.4 to 6.0, and the false-alarm rate fell too, from 2.0% to 0.9% (Table 6). So the ablation D5 quoted shows the term matters when present, not that it should weigh heavily. That alone withdraws "heavily".
- *Why the link to δ also lapsed, separately.* When D5 was written, §5 defined Risk(x) as the probability of legitimate OT traffic interacting with placed decoys, a false-positive notion, so citing #250 for δ fitted the text. The code never computed that: from the first commit it summed each placed decoy's detectability value. D20 rewrote the definition to match the code, as normalised detectability exposure, and D22 and D22a derived the values from a detectability rubric. From then on #250's term corresponded to Filter 1's malice fidelity, not to δ·Risk. No entry noticed that D5's evidence sentence had stopped applying.
- *What stands:* D5's method. The weights are justified by the parametric sensitivity sweep (#272). The default δ has been 1, equal to α, β and γ, in every commit, so no default ever implemented "heavily". The comparison grid is unchanged.
- *Where #250 still belongs:* as a precedent for a multi-term deception objective.
- *Known and unchanged: a departure from the brief.* The brief (§10) names this metric "false-positive/operational risk", so the false-positive reading is its own intent. In this project the δ term measures detectability exposure, and false positives are handled only by Filter 1's malice-fidelity gate (D26), not by a term in F. The term keeps the brief's name. The thesis should present the split as a deliberate departure from the brief's metric where the term first appears, in the abstracts; `05-front-matter-pack.md`'s drafting notes now say so.

**2. The criticality patent was misdescribed (D2).** The granted patent (#282, #325) adds its three factors, C(i) = α·l(i) + β·c(i) + γ·d(i).
- Its centrality is a degree-and-strength measure over packet-share weights. It mentions betweenness but does not use it.
- Its damage term, an asset's share of operational load, is the one §2's Damage(v) follows. That sentence stays.
- D2's "multiplied by" never matched the specification. Since the first commit Crit(v) has added SL, and multiplied only centrality by damage.
- The synthesis's "locality × centrality × damage" and §2's claim that betweenness follows "the pattern in source 282" misstate the source.
- This entry corrects descriptions only. Whether Crit(v) should take the additive form is A40, and what an edge weight means is A35. Both stay open.

**3. The Acalvio patent's claims also fix a position (D7; A29's claims half).** Independent claims 1, 19 and 20 of US 9,853,999 set the number of deception mechanisms from asset densities and from an attack probability derived from historical attacks, updated in real time. Dependent claim 6 deploys them "on or near the central node". In FIG. 13's example that is the node with the most incoming connections.
- The novelty claim holds at method level. The patent combines a count rule with one central-node rule. This project selects a set of positions by maximising a stated objective under a budget.
- The centrality baseline is the nearest analogue of the patented rule, and the thesis should say so when it presents that baseline.

**4. D10's open sub-item is closed (A4).** #315 is a Stackelberg game on decoy quality against quantity, which chooses decoy types greedily and has no network topology. It is not a placement competitor.

**5. D18's IEEE Xplore check is withdrawn.** It is recorded as made "via NFSU access". The NFSU library is not available to the user, who had said so in conversation before A2 recorded it, and IEEE Xplore is not reachable from Claude's environment (A33). The check is therefore treated as not made. Iteration findings 4 and 6 rest on the same premise and are marked.

**6. P1 step 5's tactic is Impact (A41), corrected under D21's defect clause.** MITRE lists T0832 Manipulation of View under Impact (#387). P1 step 5 had carried Inhibit Response Function since the threat model was written.
- *Why an entry:* the label is part of P, an evaluation input frozen since D21 "unless a documented defect emerges". This is such a defect, as P5's gap was in D27.
- *Effect, stated before any Filter 1 score could see it:* no number moves, because no term of F reads a tactic. Two inputs to Filter 1 change:
  - the HMI's card in Screen 3;
  - the scoring prompts of the three assets on P1, Engineering WS, PLC-01 and the HMI, because a prompt lists every step of each path through its asset.
- No blind card shows P1, and no blind asset's prompt includes it.
- *Order:* the batch must be pushed before the notebook runs, because Colab clones the repository. It also changes the seed, so the database is rebuilt before the blind cards are scored.

**7. P2 step 1 takes T0822, and P is frozen, as seeded, once the first blind card is scored.** "As seeded" means `data/seed.sql`, which is what the cards, the prompts and F read. `threat-attack-model.md`'s tables number some steps differently and include steps that were never seeded.
- *The change: the user's choice, on 13 October 2026, on Claude's recommendation.* P2 step 1 now carries **T0822 External Remote Services**, verified (#383) and already used at the same asset and tactic by P5 step 1. It had read "Network-perimeter entry", with no ID. MITRE's record for Industroyer2 maps no initial-access technique (#389), so P2's entry is now a composition grounded in Sandworm's 2015 attack, as P5's is. The threat model says so.
- *Why D21 permits it:* the threat model states that each path is "grounded in MITRE ATT&CK IDs verified directly against attack.mitre.org". A step with no ID fell short of that, and a verified ID was already in the log.
- *Effect, stated before any Filter 1 score:* no number moves. The DMZ Jump Host's card changes, and it is a blind card: its P2 step 1 now reads the same as its P5 step 1. The prompts of the two assets whose prompts show the step, the DMZ Jump Host and PLC-03 (RTU), change likewise, and PLC-03 is a blind card too. No blind card had been scored: the user confirmed on 12 October that none had, and scores them only after this batch.
- *Claude's error, corrected here:* the first draft of this entry called T1692.001 "the only candidate found" and missed T0822, and Claude's recommendation on 11 October to leave P2's steps alone rested on the same oversight. The independent review caught it.
- *Still without IDs:* P1 step 3, P2 step 2 and P3 steps 1–2. T1692.001 for P2 step 2 (#389) fails the primary-source rule, because its own page has not been read. The other three would each need a MITRE page verified. Of the four, only P2 step 2 appears on a blind card, PLC-03's.
- *Why freeze at the first blind-card score:* once scoring starts, a change would leave the reviewer and the model judging different steps.
- *The rule until the review is committed:* any change to P needs its own entry, and every card and AI suggestion showing the changed step is re-scored. A blind card cannot be re-scored blind, because its first answers are written once (D26). *[D30: the review restarted once, before any AI output existed. D30 records it and states the limitation.]* Its comparison also rests on the AI's prompt, which shows every step of P2, P4 and P5, the paths through the three blind assets. So a change to any step of those paths after the blind cards are confirmed voids the affected cards' agreement measure, and the entry must say so.
- Claude recommended freezing on 11 October 2026. The user started this batch on that basis on 12 October and chose T0822 on 13 October.

**8. Stale text corrected in the same batch.** None of it changes a number or an input. Most of it was found by the 11 October check and by an independent review of this batch, which had not seen it being written.
- *Heavy risk weighting:* `README.md`, `00-glossary.md` (False positive; Ablation study), `formal-problem-definition.md` §5, `research-synthesis-implementation.md` (its header note), `03-commercial-prior-art-analysis.md` §3, citation shortlist entry 16, `05-thesis-structure.md` §8, `sources.md` #324 and #326, iteration findings 4 and 5 (marked, not rewritten), and pointer notes on D5 (whose status now reads "confirmed in part") and D15.
- *Risk's definition:* `00-glossary.md`'s notation table still defined Risk(x) as the pre-D20 probability of legitimate traffic hitting a decoy, a false-positive term the objective no longer has. It now gives D20's normalised detectability exposure.
- *Criticality:* `formal-problem-definition.md` §2, the synthesis's header note, the prior-art analysis's criticality row, shortlist entry 35 (now with the patent's number, US 11,252,175 B2), and a pointer on D2.
- *Patent claims:* `03-commercial-prior-art-analysis.md` §2, §3, §4 and §6, the synthesis's header note, `00-action-items.md` A29, and pointers on D7 and D25.
- *Library access:* iteration findings 4 and 6, `sources.md` #266, #276 and #310, the shortlist's closing paragraph, `05-thesis-structure.md` §8, `00-workflow-and-rules.md`'s example of what the user handles, and a pointer on D18. That example now reads: papers and patents the user supplies as PDFs, asked for up front.
- *Citation details from the supplied texts:* shortlist entries 7 and 14 (the first author is A. L. Nguemkam), 15 (the GNN paper's authors, from A9) and 16 (D3O-IIoT's authors and venue), and `sources.md` #324's article number.
- *Greedy's guarantee:* shortlist entry 9 still gave plain greedy a (1−1/e) bound, the glossary's Submodularity entry still said the check was to be done, its Greedy algorithm entry implied submodularity alone gives greedy a guarantee, and D1 had no pointer to D20 and D23. All four are corrected.
- *Earliness:* the glossary still described Early(x) in its pre-D20 form, a mean over intercepted paths, as "not a bug".
- *Iteration 11's dropped claim:* shortlist entry 26 still said Filter 1 "partially addresses" the ICS-matrix gap, and the synthesis still advised adapting the rubric "to the MITRE ATT&CK *ICS* matrix specifically" (now its header note's item 6). Its item 7 marks the Jay distinctions, long since confirmed against the full text.
- *Filter 1 pre-judgements:* three glossary entries (Plausibility, Jump host, OT DMZ) stated how decoys at particular testbed asset types or zones would score. They are reworded neutrally under D26's rule that nothing written before scoring may serve as an expected answer. This entry does not repeat what they said.
- *Build descriptions:*
  - `02-prototype-architecture.md`: the module list, and the route table. No `run_metrics` table exists, the damage column is `damage_score`, and three listed routes are not built.
  - `02-ai-role.md`: `run_metrics`, and a worked example that put Engineering WS-2 on P1 and PLC-02 on P1 and P2. The example is now marked as showing shape only.
  - `02-data-model.md`: `/graph`'s Cytoscape.js, `/optimize`'s return value, two unbuilt routes, and a sentence calling every other route read-only.
  - `testbed-architecture.md`: Cytoscape.js, and the claim that every path crosses Supervisory→Control, which P2 and P5 contradict (A38). `formal-problem-definition.md` §2 makes a similar claim and now carries a pointer to A38.
  - `02-optimization-formulation.md` §2: |P| = 3.
  - `src/graph_model/__init__.py`: a docstring saying nothing in the module writes, and a comment calling the placeholder SL-by-level mapping "IEC 62443's usual convention". #330 does not support that, and argues against high SL targets for the embedded devices at the bottom of the Purdue model. Comments only; the values are unchanged and remain A37's question.
- *Thesis-facing:*
  - `05-front-matter-pack.md`: the iteration and source counts, five methods rather than four, the figure and table lists through P5, and drafting notes that its evaluation sentences describe the finished thesis and that "operational risk" departs from the brief's metric (item 1);
  - `05-thesis-structure.md`: TA-1's date, the normalisation gate that D20 closed, A15 among the gates, and §8's open items.
- *The path set and its labels:* `00-glossary.md` still gave P as {P1, P2, P3} in two places and used three paths in its Coverage example, which D27's update had missed. Its Tactic entry omitted Execution, which two seeded steps use, and its notation row for Cost(x) omitted D25's divisor.
- *The README's D15 sentence* had the order of D15's run reversed, as well as crediting D5's heavy weighting. Its next paragraph said greedy "still" chose the DMZ Jump Host alone after D19; D19 records that it "now" did.
- *Counts:* the shortlist's "322 entries" and "roughly 280".
- *Reference style:* the shortlist wrote its own entry numbers with `#` in six places, which rule 3's check reads as source citations. They now read "entry N".
- *Trackers:* `00-action-items.md` (A4, A8, A29, A32, A38, A40, A41, and a new A42 for D18's name checks) and `00-project-phases.md`.

**Effect on results.** None. No evaluation result exists, and no input to F changed. *Verified on 12 October 2026 by comparing outputs before and after the batch:*
- With the legacy set loaded and `--legacy-d25` passed, `run_comparison.py`, `sweep.py --sens` and `structure_check.py` print output identical to the output before the batch.
- On the default seed L is empty, and all three scripts still refuse to run, with identical messages.
- The scoring prompts differ in exactly five lines. P1 step 5's tactic changes in the prompts for Engineering WS, the HMI and PLC-01, and P2 step 1's technique in those for the DMZ Jump Host and PLC-03 (RTU).
- `GET /candidates` differs in exactly three fields: P1 step 5's tactic on the HMI's card, and P2 step 1's technique ID and name on the DMZ Jump Host's card, a blind card not yet scored.
- `GET /attack-paths` shows both changes too, and nothing else in it changes. No screen calls that route at present.

*Status: confirmed, implemented and verified as above. Reference: `data/seed.sql`, `threat-attack-model.md`, `02-data-model.md`, `formal-problem-definition.md` §2 and §5, `research-synthesis-implementation.md`, `03-commercial-prior-art-analysis.md`, `01-thesis-citation-shortlist.md`, `00-glossary.md`, `README.md`, `02-prototype-architecture.md`, `02-ai-role.md`, `testbed-architecture.md`, `02-optimization-formulation.md`, `src/graph_model/__init__.py`, `05-front-matter-pack.md`, `05-thesis-structure.md`, `iteration-4-findings.md`, `iteration-5-findings.md`, `iteration-6-findings.md`, `00-workflow-and-rules.md`, `00-action-items.md` A4, A8, A29, A32, A38, A40, A41 and A42, `00-project-phases.md`, D1, D2, D5, D7, D10, D15, D18, D21 and D25 (pointer notes), `sources.md` #28, #29, #34, #229, #236, #250, #266, #272, #276, #282, #310, #312, #315, #323–#326, #330, #347, #353, #383, #387 and #389 (update notes added to #266, #276, #310, #324, #326 and #383).*

**D29 — The development environment is pinned, and a setup script builds it once. One `.venv`, built by uv, holds Python 3.13, every package at an exact version with checksums, and Node.js. The user's choices, 14 October 2026. No number changes.**
While setting up a fresh clone, the user asked for two things.
- **A pinned environment:** "a venv in which we use a different python version", one that "includes all required environment dependency that includes node".
- **A static, one-time setup:** "I want static one time setup with venv creation and setting up. It would be better if it can done with any script running".

Until then the environment was whatever each machine had:
- `requirements.txt` gave only minimum versions;
- the Python version was the machine's own;
- Node.js was a separate install.

**1. Why it matters for the evaluation, not only for setup.**
- **Unpinned installs drift.** On 13 October 2026 the same `requirements.txt` installed NetworkX 3.4.2 on Python 3.10, 3.6.1 on 3.11 and 3.7 on 3.13. `compute_centrality` runs on NetworkX, and #385 was read from 3.6.1.
- **No number has moved yet.** The legacy sweep printed identical output on all five Python versions tested, 3.10 to 3.14. But nothing held it there.
- **The Python version mattered too.**
  - OR-Tools has no package for Python 3.15 (#358), so a fresh install on the newest Python fails outright.
  - Python 3.9 installs, but the API fails to start.
- **Claude's reasoning.** The project's evaluation-integrity rule freezes the methods before Phase D. The libraries the methods run on are part of them, so the environment is frozen with them.

**2. What is pinned.**
- **`.python-version`: `3.13`.** uv creates `.venv` with it, downloading it if the computer lacks it.
- **`requirements.txt`:** the direct dependencies with minimum versions. It now includes `nodejs-wheel>=22.12`, the newer of Vite 8's two Node minimums.
- **`requirements.lock`:** generated by `uv pip compile requirements.txt --universal --python-version 3.13 --generate-hashes`.
  - It pins 32 packages, including Node.js 24.19.0 through `nodejs-wheel`.
  - It records a SHA-256 checksum for every file.
  - One file covers Windows, macOS and Linux through environment markers: uvloop is skipped on Windows, and tzdata is installed only there.
- **`package-lock.json`** already pinned the JavaScript packages, and is unchanged.
- **The Colab notebook is unaffected.** It runs in Colab's own environment, with the pins D26 gave it.

**3. The setup script, `scripts/setup.py`.** It is run once per clone with `uv run scripts/setup.py`, the same command on every operating system, and works through four steps.
- **Environment.** It creates `.venv` with Python 3.13, or replaces one with another Python version. It then makes `.venv` match the lock exactly, and uv checks every checksum.
- **Database.** It builds the database only if none exists, and never changes an existing one, because that holds the user's confirmations.
  - It builds a fresh copy in memory from `schema.sql` and `seed.sql`, and compares the seeded tables with the copy on disk.
  - It ignores confirmations and the scores the code writes back into `assets`.
  - A database built before a schema or seed change, or read in the wrong encoding, gets a warning that points to the export, rebuild and restore procedure.
- **Frontend.** It runs `npm ci`, using the Node inside `.venv`.
- **Checks.** It checks the versions, the backend's imports, the database, and a frontend build. `--check` runs the checks without changing anything except the frontend's build output.
- **Static by design.** It runs only when the user runs it. Following a lock change after a pull means running it again on purpose.

**4. Options considered.** On 14 October Claude set out A to D, and the user chose A. Claude then proposed E, and the user rejected it in favour of the setup script.
- **(A) uv with the lock: chosen.** Verified on Linux. A dry run found ready-made builds for Windows and macOS.
- **(B) The same lock in a plain venv,** with a Python 3.13 the user installs. Kept as the setup guide's fallback.
- **(C) pixi or conda,** which manage Python and Node from conda-forge. Not tested. conda-forge (conda.anaconda.org and prefix.dev) was unreachable from Claude's environment on 14 October 2026, so neither option could be verified.
- **(D) Pin only the Python packages, and install Node from nodejs.org.** This avoids an unofficial Node build, but keeps Node a separate install.
- **(E) uv's project mode (`pyproject.toml` and `uv.lock`): rejected by the user.** Here every `uv run` creates and updates `.venv` from the lock.
  - *Tested on 14 October.* It created the environment on first use, and followed a lock change on the next run.
  - *Its hazard.* A plain `uv run` also rewrites the lock when the dependency list is edited.
  - *The user's decision.* The user rejected it the same day: "It creates problem for user". The setup script in item 3 replaces it.

**5. The trade-off accepted with A: Node.js comes from an unofficial build (#391).**
- `nodejs-wheel` repackages Node.js for PyPI. One maintainer publishes it, not the Node.js project. basedpyright depends on it.
- Node serves only the screens, through the Vite dev server and build, and never the evaluation.
- Switching to the official installer later means removing the `nodejs-wheel` line and regenerating the lock, under item 6.

**6. The rule from now on.**
- The lock changes only through a decisions-log entry that states the effect. The setup script, step 6 of `04-setup-guide.md` and the legacy reproduction are re-run before and after.
- It does not change between the freeze before Phase D and the end of Phase D.
- If a change is forced, for example by a security fix, the entry says which results it touches, whether the effect is favourable or not.

**Effect on results.** None. *Verified on 14 October 2026 from fresh clones with the batch applied, using uv 0.13.1 on Linux:*
- **Legacy reproduction unchanged.** With the legacy set loaded and `--legacy-d25` passed, `run_comparison.py`, `sweep.py --sens` and `structure_check.py` print output identical to the unpinned run of 13 October at commit `d490df7`. This held both in an environment built by hand and in one built by the setup script.
- **Refusals unchanged.** On the default seed, all three scripts refuse with the same message.
- **Screens unchanged.** Screen 3 shows the expected header and cards, served by the Node inside `.venv`.
- **The setup script's recovery cases.** These behaved as described:
  - re-runs, which left the database byte-for-byte unchanged;
  - `--check`;
  - a package removed by hand;
  - a `.venv` made with Python 3.12;
  - a database built from an older seed, and one read as cp1252, both warned about and left untouched;
  - a database holding a confirmation and the code's written-back scores, which raised no false warning;
  - a run with uv missing, which stops with instructions.
- *Not verified:* runs on Windows and macOS.

*Status: confirmed by the user (option A, and the setup script, 14 October 2026), implemented, and verified on Linux as above. Reference: `.python-version`, `requirements.txt`, `requirements.lock`, `scripts/setup.py`, `.gitignore`, `README.md` (Running it and the layout table), `04-setup-guide.md`, `04-deployment-requirements.md`, `02-prototype-architecture.md` §5 (a pointer note), `00-repository-structure.md`, `sources.md` #358, #391 and #392.*

**D30 — The Filter 1 review restarts on a fresh database, under route A. The testbed gets a written operating profile, which each card and its asset's AI prompt both show, and four connections are added to E. The user's choices, 17–19 October 2026. No recorded number changes.**
A32 step 2, scoring the three blind cards, began on 14 October 2026. Three things surfaced in it.

**1. The cards were filled twice before this restart, and both fillings were discarded.**
- *14 October:* placeholder entries, made while trying the screen. The database was deleted the same day.
- *17 October:* all ten cards, before any AI output existed, with levels the user chose and reasons drafted with an AI writing tool from the user's points. It was not exported or committed.
- *The user's decision, 18 October 2026:* "We are working on fresh start. No referencing to the all 10 path data provided by me earlier."
- *How it is applied:* neither filling is used anywhere, not as a record, a comparison or a fallback. This entry records only that they existed, not what they contained.
- *The safeguard:* a database built before D30 cannot carry anything over (item 7).
- *Why record them at all:* the thesis presents the blind cards' answers as first answers, given before any AI answer. They are the first answers on the fresh database, and no output from the scoring model (Qwen) existed before them. But the reviewer had chosen levels for these cards once before, and had read AI-drafted reasons for them. Item 6 states the limitation.

**2. Route A stands (D26).**
- On 17 October Claude called the all-ten scoring "a plus". That was its own earlier preference for route C coming back, against D26's recorded decision.
- The user restated route A on 18 October: "I want ai to first decide and them human to to varify." Claude withdrew the remark.
- The user chose to send the seven non-blind cards back through route A. They wait for the notebook's suggestions, and the user reviews them after the import.
- The three blind cards are scored by the user alone, in their own words, before the notebook runs.

**3. The setup the cards needed did not exist.** The user, on 18 October: "in order for to answer the or provide input in card we need to establish the set-up which is currently missing." Claude checked what the repository defined, against `data/seed.sql` and `testbed-architecture.md`:
- **Defined:**
  - each asset's name, type, zone and Purdue level;
  - 14 connections;
  - the five paths;
  - one line of software per VM.
- **Not defined:**
  - any asset's services;
  - the routine activity that reaches any asset, which §4's convention 5 asks the reviewer to name;
  - 9 of the 14 protocols;
  - anything about the four graph-only assets beyond one line each.
- **The card showed less than the prompt.** D26 gave the model each asset's connections "for criterion 4" and every step of its paths "for criterion 2" (`02-ai-role.md` §8). Screen 3's card showed neither, only the asset's own steps. Until now the reviewer would have judged from less than the model.
- **Two paths moved between assets with no recorded connection:**
  - P3, from the OT Firewall to Engineering WS-2;
  - P4, between Engineering WS and the Historian.

  §3 does not require paths to follow E, so no rule was broken, but the network and the paths disagreed.
- **Options set out by Claude on 18 October.** The user chose (a).
  - **(a) A written operating profile, held in the seed and shown to both the reviewer and the model: chosen.**
  - (b) The network view in Screen 3 (A34): deferred, since (a) puts the connections on each card.
  - (c) Building the VM testbed first (A21): not made a precondition. The rubric judges positions in the modelled network, and a written profile describes those fully.

**4. The operating profile.**
- **What it holds.**
  - Three plant-wide facts.
  - For each of the ten assets on a card: its role, what it runs, and the routine activity that reaches it.
  - The eight blank protocols, filled in. The Attacker's connection, and the firewall rule G4 adds, carry none.
- **Where it lives.** `data/seed.sql` (`plant_facts`, `asset_profiles`, `edges`) is the only copy.
- **One source for both readers.**
  - Screen 3's cards and the scoring prompt are built by the same function, `asset_context` in `src/plausibility/prompt.py`. Each card now also shows the connections and every step of each path through the asset. A card shows exactly the facts its asset's prompt receives.
  - The reviewer sees all ten cards on one screen, and designed the testbed, so can know more than one prompt shows. A fact about a connection is therefore written into the profiles of both assets it joins. This was checked for every connection: for example, the firewall rule appears on the OT Firewall's and Engineering WS-2's profiles, and the switch's failover test on the switch's, both PLCs' and the jump host's.
- **What it may not hold.** Facts only: no judgement about decoys and no rubric level. Two checks ran over the stored text:
  - a word check for evaluative terms;
  - after the independent review, a check for wording that echoes Table 1's level definitions.
- **Completeness, checked against convention 5's example list, because convention 5 now says the profile settles which of these happen in this plant:**
  - **Scans:** the plant runs none of its own, and the internet's reach the firewall.
  - **Historian data collection:** from the HMI, which polls the PLCs and the RTU.
  - **Engineering and vendor maintenance sessions:** at the Engineering WS, Engineering WS-2, the jump host, the RTU and the switch.
  - **Backups:** the weekly PLC program backups and the Historian's nightly archive.
  - **Time synchronisation:** the RTU takes IEC-104 clock commands from its master, the HMI (G3). No other time service is modelled.
- **Who wrote it.**
  - Claude drafted it from `testbed-architecture.md`, `threat-attack-model.md` and `data/seed.sql`.
  - Claude had seen the discarded 17 October answers, which were pasted into the conversation, before drafting. It did not draw on them, and every choice that bears on routine activity is listed below with its alternatives, so a reader can judge.
  - **From the repository:**
    - the firewall's role and pfSense;
    - the jump host's "Linux, minimal services" and "patch-relay stand-in";
    - the engineering workstations' software;
    - the HMI's Node-RED dashboard;
    - OpenPLC on PLC-01 and PLC-02;
    - PLC-02 as a second controller;
    - the RTU's IEC-104 and breaker operation (P2);
    - the switch as "an alternate conduit into PLC-01/02";
    - the Historian as a modelled node in the OT DMZ;
    - the five protocols already recorded.
  - **Claude's proposals:** everything else.
- **Three choices, each with its alternative:**
  - **Network scanning in normal operation:** none, the monitoring being passive, chosen; or a quarterly asset-inventory scan from the Engineering WS.
  - **The firewall rule to Engineering WS-2:** left over from an earlier setup, with no scheduled traffic, chosen; or a vendor's remote support for Engineering WS-2 in maintenance windows.
  - **The Backup Control Switch:** a standby route, carrying traffic only in a quarterly failover test from the DMZ Jump Host, chosen; or the vendors' maintenance route to the PLCs.
  - The draft also settled the Engineering WS as Windows 10/11, where `testbed-architecture.md` allowed "Windows 10/11 or Linux".
- **Confirmation.** The user confirmed the whole draft on 19 October 2026 ("ALL OK"), with no changes. After the independent review (item 7), twelve profile lines were reworded, with the facts and choices unchanged. The user confirmed them on 21 October 2026 ("ok").
- **The rules change with it,** and the prompt's rules carry the same text:
  - §4's convention 6, *this plant*, is new;
  - convention 5 now names the benign activity "as the operating profile describes it";
  - convention 4's card shows the full paths.

**5. Four connections are added to E.** The user's choices of 19 October 2026, as Claude recommended:
- **G1, HMI → Historian (OPC UA):** the Historian's data source. No control asset sent it data.
- **G2, Engineering WS → Historian (HTTPS):** engineers' trend queries, and the connection P4's moves use.
- **G3, HMI → PLC-03 (RTU) (IEC-104):** the RTU's master, which polls it. Only the DMZ Jump Host connected to it.
- **G4 (i), OT Firewall → Engineering WS-2 (no protocol):** the left-over firewall rule, which P3's move uses. Option (ii), stating instead that P3 uses a route the model does not record, was not taken.
  - In zone terms the connection crosses the existing OT DMZ→Supervisory conduit, so no conduit row changes, and ConduitSL does not move.
- **No step of P changed.** Since D30, every move between consecutive steps uses a recorded connection, in one direction or the other.

**6. Limitations, stated for the thesis.** These are facts the user stated or the record shows:
- before the fresh start, the reviewer had chosen levels for all ten cards once, the three blind cards included;
- the reviewer had read AI-drafted reasons, written from the reviewer's own points, for those cards;
- the reviewer may earlier have read AI-drafted design text about candidate sites;
- the operating profile is a declared design, not measured traffic. It was drafted by an AI (Claude) that had seen the discarded answers, and confirmed by the reviewer. Its choices about routine activity were made after the 17 October filling.

**7. Independent review, and what it changed.** A separate agent reviewed the batch on 19 October 2026, without having seen it produced. Everything functional passed its checks. It found one High, five Medium and four Low issues, and all were fixed before handover:
- **High: a pre-D30 database could be carried over.** The general rebuild procedure (export, rebuild, restore) would have written the discarded answers, the write-once blind ones included, into the fresh database. The fix:
  - a database built before D30 is now refused by the setup script, which says to delete it and not restore it;
  - the backend refuses it too, with the same message, which Screen 3 shows;
  - the export refuses it;
  - every review record and every AI suggestion now carries a hash of the facts its card showed (`context_sha256`), and the restore and the import check it. The word "fingerprint" is avoided, because in this project it means telling a decoy from a real asset (Filter 2).
- **Medium:**
  - the limitations understated the blind cards' history, and statements in D26, D28, §4 and `02-ai-role.md` needed pointer notes;
  - "identical facts" holds per card, not per screen, so connection facts are now written on both assets;
  - the profile contradicted itself and E in five places (scans, "single entry point", the failover traffic's source, the route of updates, the firewall rule's conduit);
  - the effect statement was incomplete, and the new edges' weights were unexplained;
  - the choices that feed criterion 4, their alternatives and the drafter's prior exposure were not recorded, and three lines echoed Table 1's wording.
- **Low:** stale text in six places; the prompt's label for the plant facts; error messages on a stale database; and nothing linking an AI suggestion to the facts it was made from.
- **Found while verifying the fixes:** Screen 1 drew an error reply as if it were a graph. When the backend refused a database, the whole app went blank. It now shows the backend's message.
- **A second pass,** by the same reviewer on the fixes, found two more Medium issues and five Low ones. All were fixed:
  - **Medium: the hash check was all-or-nothing.** One card whose facts changed made the restore refuse the whole record, blind answers included, although D28's rule re-scores only the cards a change affects. It also gave its refusal only after the database had been deleted.
    - The restore now checks per card, and refuses by name any card holding answers or an AI suggestion whose facts have changed.
    - `--skip-changed`, for use only when a decisions-log entry authorises the change, restores everything else and leaves those cards unscored.
    - A new `check` command runs every restore check against a database built in memory, before anything is deleted.
    - The import works the same way.
  - **Medium: Claude's weight-sensitivity statement was false.** It said the weights of G1 and G2 change no ranking between 0.5 and 2.0. Claude had varied the two together, and their effects cancel. *Effect on results* now gives the measured thresholds.
  - **Low:**
    - The rule that a connection's facts sit on both its assets failed for G1, G2 and the VPN connection. The HMI, Engineering WS, OT Firewall and DMZ Jump Host profiles now name them. Checked for every connection.
    - The completeness note wrongly said no asset serves time.
    - Stale text in three files.
    - The restore crashed, without a message, on a database built before D30.
    - "Fingerprint" was renamed to context hash.

**Freeze.** The operating profile and the connections freeze at the first blind-card score on the fresh database, under the rule D28 set for P. P itself is unchanged.

**Effect on results.** No evaluation result exists on the new candidate set, so none moves.

*Measured on 19 October 2026 with the current code, on the confirmed seed:*
- **Crit:** no asset moves by more than 0.002.
- **Betweenness:**
  - DMZ Jump Host 0.156 → 0.111;
  - Backup Control Switch 0.067 → 0.044;
  - Engineering WS 0.033 → 0.017;
  - Engineering WS-2 0.011 → 0.033;
  - HMI 0 → 0.006.
- **Ranking, in two places:**
  - Engineering WS-2 moves above Engineering WS, because of G4;
  - the HMI rises from the zero tie to above the Historian and the PLCs, because of G1.

  The centrality baseline ranks candidates by this number, so either change alters its pick whenever the budget falls between the two.
- **The weights are placeholders.** The four new edges take the seed's default weight, 1.0, as placeholders under A35, the open question of what an edge weight means. The ranking depends on them.
  - *The HMI's place:* at equal weights, two shortest routes from the DMZ Jump Host to the Historian, through the HMI and through the Engineering WS, share the credit. Any difference between G1's and G2's weights hands it all to one route.
  - G1 alone at 1.25 or more, or G2 alone at 0.75 or less, returns the HMI's betweenness to 0 and the HMI below the Historian.
  - On a grid of 0.5 to 2.0 for both, 21 of 49 pairs change the ranking.
  - *The Engineering WS / Engineering WS-2 order:* it returns to the original once G4's weight exceeds about 1.5. The flip falls between 1.5 and 1.6.
  - *Measured* on 19 October 2026 by Claude, and independently by the reviewer.
- **Legacy reproduction unchanged.** `data/legacy/d25_candidate_set.sql` now also removes the four added connections. With it loaded and `--legacy-d25` passed, `run_comparison.py`, `sweep.py --sens` and `structure_check.py` print output identical to commit `1af1333`'s.

*Status: confirmed by the user: the profile and G1–G4 on 19 October 2026 ("ALL OK"), and the post-review rewording on 21 October 2026 ("ok"). Implemented and verified.*
- *Implemented and verified on Linux after the review's fixes:*
  - the setup script on a fresh copy, and its refusal of a database built before D30;
  - the API, including its refusal of such a database;
  - the prompt's text, and the scoring loop against a stand-in model;
  - Screens 1 and 3 in Chromium, on a current database and on one built before D30;
  - the confirm, export, restore and import round trip;
  - the context hash: a record or a CSV without one is refused whole, and a changed card is named and refused, or skipped with `--skip-changed`;
  - the dry-run `check`, which changes nothing;
  - the legacy reproduction.
- *Reference:*
  - data and code: `data/schema.sql`, `data/seed.sql`, `data/legacy/d25_candidate_set.sql`, `src/plausibility/prompt.py`, `src/api/main.py`, `src/frontend/src/PlausibilityReview.jsx`, `src/frontend/src/Dashboard.jsx`, `src/frontend/src/App.css`, `scripts/setup.py`, `scripts/review_io.py`, `scripts/import_plausibility_scores.py`;
  - specification: `formal-problem-definition.md` §3–4, `02-ai-role.md` §8–10, `02-data-model.md`, `02-prototype-architecture.md` §2–3, `02-system-flow.md`, `testbed-architecture.md`, `threat-attack-model.md`;
  - guides and trackers: `00-glossary.md`, `00-action-items.md` A32 and A35, `00-project-phases.md`, `04-setup-guide.md`, `README.md`. The last also gets the frontend command split onto two lines, because Windows PowerShell 5.1 rejects `&&`;
  - pointer notes on D26 and D28.

**D31 — A32 step 4: Filter 2 scores for the five assets that passed Filter 1 for the first time, and the first run on the reviewed candidate set. The run is pre-freeze: A35–A38 and A40 are still open, by the user's choice of 26 October 2026.**

**1. Where A32 stood.** Its steps up to the export are done and committed.
- *Blind cards:* scored first, on the fresh database, before any AI output existed (commit `79830f7`).
- *AI first pass (A20):* one run of `notebooks/plausibility_scoring.ipynb` in Colab on 24 October 2026, generated at 19:29:20 UTC from commit `79830f7`.
  - Model: Qwen3-14B at revision `40c069824f42`, in 4-bit nf4, with greedy decoding, on a T4. All ten cards parsed on the first attempt.
  - A second run in the same session could not load the model, because the first copy was still in GPU memory, and produced no output. The first run is the only one. Its files are `data/review/ai_suggestions.csv` and `data/review/ai_raw_outputs.jsonl`.
- *Review:* all ten cards confirmed and exported (`cda4c98`). Engineering WS-2's Interaction answer was then set to match its written reason (`a986abd`).
- *Filter 1 result:* nine assets pass. PLC-02 fails by the path rule, as known in advance (D26, D27).

**2. What the review measured, reported as counts (D26).**
- *Blind cards, first answers against the AI's suggestions:* 7 of 12 answers agree.
  - All 5 disagreements are the AI one level higher than the reviewer: Feasibility on all three cards (Yes against Mostly Yes), and Malice fidelity on the DMZ Jump Host and the Historian (Mostly Yes against Mostly No).
  - The reviewer kept every first answer as final after seeing the AI's.
- *The seven pre-filled cards:* the reviewer kept 25 of the AI's 26 answers. The one change is Engineering WS-2's Interaction, from Mostly No to Mostly Yes. Its reason: the leftover firewall rule exposes the workstation to the outside, which the AI's reason contradicted. Per D26, this acceptance rate is reported as a limitation, not as evidence that the AI is accurate.
- *Three cards are not a sample.* The blind measure rests on three cards and twelve answers. D30's limitation stands: the reviewer had scored these cards once before the restart.

**3. A disclosure: Claude's part in three of the reviewer's reasons.** On 25 October 2026 the reviewer asked Claude for help with the three non-blind cards that required a written reason. Claude is the AI assistant used to develop this project, not the scoring model. The three are Engineering WS and PLC-01, which lie on two paths each, and Engineering WS-2, whose AI answer was Mostly No.
- Claude declined to discuss the blind cards, and did not discuss them.
- For the three cards, Claude explained each path, gave its own reading of each path's Interaction level, and drafted reason text. The reviewer adopted all three drafts unedited.
- On Engineering WS-2, Claude argued that the scoring model's reason contradicted the plant facts and leaned to Mostly Yes. The reviewer changed the answer to Mostly Yes and adopted Claude's reason for that change.
- So on those three cards the record shows the reviewer accepting a second AI's reading, not an independent human check. The levels on Engineering WS and PLC-01 equal the scoring model's. Engineering WS-2's differs from it by the one change above.
- Claude offered the alternative of rewriting the reasons in the reviewer's own words, and said that keeping them meant recording this disclosure. The reviewer kept them because of the time available before the midsem.

**4. The five Filter 2 scores (A32 step 4).** Five assets entered L for the first time and had no D22a score, so the candidate loader refused to run (D26).
- *Who decided:* Claude scored them on 26 October 2026, after re-reading #352's full text. The user accepted all five the same day, choosing the anchor for each of the two least-grounded ones.
- *How:* by the rubric's formula, risk = 0.4·E + 0.3·P_req + 0.3·A, with each asset anchored to the already-scored asset of the same or nearest type.

| Asset | Zone | E | P_req | A | risk | Basis | Confidence |
|---|---|---|---|---|---|---|---|
| Engineering WS | Supervisory | 0.5 | 0.6 | 0.6 | 0.56 | Same type and zone as Engineering WS-2 | Verified consistent with D22a |
| PLC-01 | Control | 0.2 | 0.9 | 0.9 | 0.62 | Same type (OpenPLC) and zone as PLC-02. #352 §5.2: one Modbus request, or one scan, separates PLC honeypots from real PLCs | Verified consistent with D22a |
| PLC-03 (RTU) | Control | 0.2 | 0.9 | 0.9 | 0.62 | An ICS field device, so #352 §4.9's ICS/OT finding applies. #352 names neither RTUs nor IEC-104, so this is an extension | Likely |
| OT Firewall | OT DMZ | 0.9 | 0.7 | 0.7 | 0.78 | #352 does not discuss firewalls. Anchored to the HMI: the attacker-facing surface is a web management interface, which endpoint checks and default TLS certificates expose early (§4.4, §6.1) | Unconfirmed |
| Backup Control Switch | Control | 0.2 | 0.9 | 0.7 | 0.56 | #352 does not discuss switches. Its one interface is SSH, which a single connection fingerprints (§5.2, HASSH; §6.2, default OpenSSH versions). Artifacts anchored to the HMI's one emulated interface | Unconfirmed |

- *Alternatives the user rejected:*
  - the OT Firewall scored as a real-OS decoy, like the DMZ Jump Host: P_req 0.6, A 0.5, risk 0.69;
  - the switch scored like the PLCs: risk 0.62.

  Neither alternative changes any placement on the comparison grid (item 6).
- *Arithmetic:* all ten values were recomputed in code from their factors and match the seed.

**5. Two gaps in the rubric, found while scoring and not changed (A43).**
- *Artifact exposure has no stated scale.* `02-detectability-rubric.md` §2 gives numbers for E and P_req, but A's values were set by reasoning per asset type. The five new A values are anchored to the existing ones, not derived from a formula.
- *Exposure is zone-only.* D30's leftover firewall rule (G4) exposes Engineering WS-2 to the outside, which E's zone rule does not see. Scored at the OT DMZ's exposure, WS-2's risk would be 0.72, not 0.56. *Measured:* no placement on the comparison grid changes either way.

**6. The first run on the reviewed set, pre-freeze.** *Verified by `scripts/run_comparison.py`, `scripts/sweep.py` (also with `--sens`) and `scripts/structure_check.py`, on a database rebuilt from this batch's seed with the committed review restored.*
- *What is open.* This is the first time any result on this candidate set has been seen. Five inputs are still open:
  - A35, edge weights;
  - A36, path targets: CritProt still weights P1 by the HMI, its last step;
  - A37, the placeholder criticality inputs;
  - A38, the OT DMZ–Control conduit;
  - A40, the criticality formula's form.
- *The instance is no longer trivial.* L has nine members, every path meets at least two candidates, and the gain part g is not modular (1,584 violations). D25's Finding 1, that greedy is optimal by construction, no longer holds.
- *Structure:* F is submodular and not monotone (1,168 monotonicity violations). Distorted greedy's preconditions all hold, so γ = 1.
- *B = 3, default weights:*
  - Greedy, distorted greedy, the exact MILP and exhaustive search all place the DMZ Jump Host, Engineering WS and the OT Firewall: F = 2.1108, Coverage 1.00, Early 0.69, CritProt 1.00, Risk 0.51, Cost 0.75. Every path is intercepted at its first step.
  - Centrality places the Backup Control Switch, the DMZ Jump Host and the OT Firewall: F = 1.0473, Coverage 0.60.
  - Random averages F = 1.1838 (s.d. 0.3875, 30 trials).
- *Declared grid, 20 cells:*
  - Greedy against centrality: 16 wins (10 swap, 6 decline) / 4 ties / 0 losses, resting on 6 distinct placement disagreements.
  - Greedy equals the exhaustive optimum in 20 of 20, and the MILP is exact in 20 of 20.
  - Distorted greedy is below plain greedy in 0 of 20.
  - The smallest rounding margin is 12,580 units, against a bound of 19.
- *§8's clause 2 holds in 19 of 20.* It fails at B = 1, δ = 3, which is a swap, not a decline. Greedy takes Engineering WS (risk 0.56) instead of the DMZ Jump Host (0.69), with the same coverage and lower CritProt (0.37 against 0.45).
- *Sensitivity sample (`--sens`):*
  - 15 to 18 wins, and no loss, in every sampled grid;
  - greedy equals the optimum in every sampled grid;
  - the MILP is exact in all 68 sampled configurations;
  - clause 2 holds in 17 to 20 of 20.
- *What centrality does here.* It ranks by betweenness alone, so it spends picks on positions that cover the same paths. At B = 4 it places the OT Firewall and Engineering WS-2, both only on P3, and the switch and the DMZ Jump Host, both on P5. It never reaches more than three of the five paths.

**7. What the thesis may claim from this (D25's claim rule).**
- The instance is non-trivial, so greedy matching the exact optimum in every cell is a finding, for this one instance of nine candidates only. Broader search-quality claims need a family of instances (A12).
- "0 losses" is still implied by optimality. It says nothing about whether F is a good objective; that needs A12's criterion outside F.
- Nothing here is a Phase D result, because the inputs are not frozen.

**8. Why pre-freeze, and the order from here.** With the midsem on 28 October 2026 and one evening left, the user chose on 26 October to run before settling A35–A38 and A40, and to settle them after the midsem, before the freeze.
- *Claude's recommendations, given in conversation earlier the same day, before this run:*
  - A35: unweighted betweenness;
  - A36: an explicit target per path. P1 PLC-01, P2 PLC-03 (RTU), P3 Engineering WS-2, P4 the Historian, P5 PLC-01;
  - A37: the guide's call;
  - A38: record the conduit;
  - A40: the additive form, with weights 0.4 / 0.2 / 0.2 / 0.2.

  They are recorded in `00-action-items.md` in this batch.
- *The rule for each:* each decision, whichever way it goes, gets an entry stating its effect against item 6's numbers, whether that effect is favourable or not.
- *Then:* the freeze, every check re-run, and the entry stating the effect against D25.

**9. A gap in the setup script's database check, found and fixed.** `scripts/setup.py` compares an existing database with the seed, but it left out `candidate_locations`' seeded Filter 2 score.
- *The consequence:* on a database built before this batch it reported "matches the current schema and seed", while the five new scores were missing there. Today the optimizer then refuses, with a clear message. But a later change of a score from one value to another, for example under A43, would have run on the old value without any warning.
- *The fix:* the check now includes `detectability_risk`, so it warns and points to the guide's rebuild procedure (export, check, stop the backend, delete, run the script, restore).
- *Verified* on a copy of a database built before this batch and holding the committed review:
  - the check now warns;
  - an export from it equals the committed `data/review/plausibility_review.csv` byte for byte;
  - after the rebuild and restore, the check passes and the optimizer runs;
  - Screen 1 runs both methods in Chromium. At its fixed budget of two, the proposed method places the DMZ Jump Host and Engineering WS (Coverage 0.80), and centrality the DMZ Jump Host and the OT Firewall (0.60).

**Effect on recorded numbers.** None changes: no result on the reviewed set existed before this entry. The legacy reproduction is unchanged. With the legacy set loaded and `--legacy-d25` passed, `run_comparison.py`, `sweep.py --sens` and `structure_check.py` print output identical to the output at commit `4dce7ff`.

*Status: confirmed by the user (the five scores and both anchors, 26 October 2026), implemented and verified as above. Not independently reviewed: the batch was prepared in one evening before the midsem. Reference: `data/seed.sql`, `scripts/setup.py`, `02-detectability-rubric.md` §3–4, `formal-problem-definition.md` §4, `02-data-model.md` (a pointer note), `00-action-items.md` A20, A32, A35–A38, A40 and A43, `00-project-phases.md`, `README.md` (its status lines, and two counts that were already stale: ten endpoints, not nine; twelve tables, not ten), `sources.md` #352.*

**D32 — From 30 October 2026 the user settles the open methodological questions without consulting the guide. No input, code or number changes.**

On 30 October 2026 the user decided not to consult the guide on the open methodological questions.
- *Who decides:* A12, A15, A16, A17 and A37, recorded as "the guide's call", are the user's own decisions from that date.
- *How:* with written independent reviews. Twelve single-item reviews and a combined review were written on 30 October 2026, and an advisor's review of all of them on 2 November 2026. Independent Claude agents wrote them, not people. They are working documents outside the repository, so each decision's own entry states its grounds.
- *A15:* the advance agreement with the guide, that an honestly reported negative result is acceptable, becomes a dated pre-registration entry of the user's own, committed before any Phase D run.
- *Unaffected:* the institutional items A7, A10 and A14. The guide's two post-midsem requests, a simulation and a K-fold-style validation, stand as requirements; A12 answers both.

*Status: the user's decision, 30 October 2026; recorded 2 November 2026.*

**D33 — The open inputs are settled before the freeze: A35, A36, A37, A38, A40, A43, the cost weight ε and Early's endpoint. Greedy places the same decoys as D31 in all 20 cells; §8's clause 2 falls from 19 to 18 of 20. The user's choices, 2 November 2026.**

**1. How they were decided (D32).** The reviews of 30 October proposed a slate. The advisor's review of 2 November accepted it with four changes: two belong here (Control's FR4 at 2, and the edge-level ConduitSL), and two belong to A12's and A15's entries. Claude re-ran the advisor's final set and reproduced its outputs byte for byte. The user accepted every value below, as proposed, on 2 November 2026.
- Every value is a design declaration with stated grounds, not a measurement.
- Every one was chosen after D31's numbers had been seen, so items 4 and 5 state each one's effect, favourable or not.
- This is before Phase D, and the inputs are not yet frozen: the freeze follows the A12, A15 and A17 entries.

**2. The decisions.**
- **A35, edge weights.** Betweenness is unweighted (hop count), for Crit and for the centrality baseline. `weight(e)` stays recorded; no computation uses it.
  - *Why:* the weights are unmeasured placeholders. NetworkX reads a weight as a distance, so the rare-traffic links (0.5) counted as shortcuts, which is why the Backup Control Switch ranked third. Two edges carry no legitimate traffic at all, so no consistent traffic reading exists.
  - Betweenness stays directed, while P and A12's simulation move along edges either way. That is a limitation, not a change to D4's baseline.
- **A36, path targets.** A new column, `attack_paths.target_asset_id`: P1 PLC-01, P2 PLC-03 (RTU), P3 Engineering WS-2, P4 the Historian, P5 PLC-01. The loader refuses a target that is not on its path.
  - *Why:* CritProt credited P1 to the HMI, where the attack hides its effect, and P4 to the Engineering WS, not to what each scenario attacks.
  - A written rule gives the same five: the asset of the first step whose tactic is Impair Process Control or Impact; for a path with neither, the first step of its final tactic. It stays out of code, so relabelling a tactic cannot change F.
  - PLC-01 carries 0.45 of CritProt across P1 and P5. That is two scenarios with one target, not D19's split scenario.
- **A37, SL and Damage.** Per-zone SL-T vectors over FR1–FR7, with SL = mean ÷ 4:
  - OT DMZ [3,3,3,2,3,2,1] = 0.607;
  - Supervisory [3,4,3,2,3,2,3] = 0.714;
  - Control [4,4,4,2,3,3,4] = 0.857;
  - External has none, so 0.

  Damage is 1/3 for each of PLC-01, PLC-02 and PLC-03 (RTU), and 0 for every other asset. The values live in their own columns, never in `plant_facts` or `asset_profiles`.
  - *Why:* each cell takes the SL whose attacker the zone must resist, judged from what a failure of that requirement there would do; `seed.sql` states the rule. This is consequence-led SL-T, a declared adaptation, not an IEC 62443-3-2 allocation. #330 advises against high SL-T for field devices when allocating protection, while Crit measures importance.
  - Control's FR4 is 2, not 1: P5 sniffs traffic there deliberately (T0842), and SL 1 covers only casual violation.
  - The operating profile names three controllers and states no ratio between them.
- **A38, the OT DMZ–Control conduit.** Recorded: the RTU vendor's IEC-104 maintenance sessions and the switch failover route. `load_graph` now refuses an edge between two zones that have no conduit row.
  - **ConduitSL becomes edge-level, replacing D20(4)'s zone step.** An asset's ConduitSL is the highest SL among the recorded conduits that its own connections cross, in either direction, and 0 if there are none. A conduit's SL is still the higher SL of the two zones it joins (#330).
  - *Why:* under the zone step the new row would give every internal asset the same ConduitSL (0.857), so the term would be a constant, and the Historian would inherit a boundary that none of its connections touches. §1 defines a conduit as the edges crossing a zone boundary, and §2 says the term exists to mark assets at a high-SL boundary. The edge rule does both.
  - Now the OT Firewall and the Historian get 0.714, and every other asset 0.857.
- **A40, Crit's form.** Crit = 0.25·SL + 0.25·Central + 0.25·Damage + 0.25·ConduitSL, with Central on betweenness's normalised [0, 1] scale. The weights are a declared convention and are not swept, so §2's promise of a sweep is withdrawn.
  - *Why:* Central·Damage zeroed every controller's damage, since every controller has zero betweenness. The additive form is #325's.
  - Equal weights and 0.4/0.2/0.2/0.2 give identical counts.
  - On this graph Central adds at most 0.028 to any asset's Crit, and 0.008 to any target's.
- **A43, Filter 2's two gaps.**
  - *G1-B:* A's values are declared reasoned anchors. The missing numeric scale stays a stated limitation.
  - *G2-B:* an asset to which a recorded rule of the perimeter firewall passes connections from the External zone takes the OT DMZ's exposure, E = 0.9. Exposure reached only through another asset's onward connections does not count. Only Engineering WS-2 qualifies (D30's G4): its risk goes from 0.56 to 0.72.
  - *Why:* a count-based scale for A, written now, would be written knowing the target values, and #352 gives none. The narrow rule does not re-expose the Supervisory and Control assets the Jump Host reaches.
- **ε, the cost weight.** Kept at 0.1, with its rationale now in `metrics.score`'s docstring: a declared convention that charges 0.025 per decoy at K = 4, one-eighth of the coverage value of one more path. `sweep.py --sens` gains an ε-only row, {0, 0.1, 0.3, 1, 3}.
  - *Why:* its only written reason lapsed at D20, and it had never been varied.
- **Early's endpoint.** A path caught at step s of n contributes (n − s)/(n − 1): 1 at the first step, 0 at the last. The loader refuses a path of fewer than two steps. Phase D's F-based comparisons are also reported under D24's 1 − s/n.
  - *Why:* under 1 − s/n the best possible score depended on how many steps the path was written with. P3, the early-detection test, could never score above 0.5.
- **The legacy route.** `--legacy-d25` is retired from the three scripts and the loader. `data/legacy/d25_candidate_set.sql` stays, as history, and the numbers recorded before D26 reproduce at commit `ebcaaa4` with that flag.
  - *Why:* A35, A37, A40 and Early change its output through code, so in the current tree it would no longer reproduce those numbers.

**3. What does not change.**
- The candidate set L (nine assets), the five paths and their steps, the defaults of α to δ, K = 4, the five methods and the 20-cell grid.
- No card changes: `asset_context` puts none of these inputs on a card, no edge is added or removed, and no path's name, description or step changes. All 10 committed cards pass the check and restore.

**4. Effect against D31's run.** *Verified by `run_comparison.py 3`, `sweep.py --sens` and `structure_check.py`, on a database rebuilt from this batch with the committed review restored. The outputs are byte-identical to the advisor's final set.*
- Greedy, distorted greedy and the MILP place the same decoys as D31 in all 20 cells.
- *B = 3, default weights:*
  - Greedy places the DMZ Jump Host, Engineering WS and the OT Firewall: F 2.1108 → 2.4175, and Early 0.69 → 1.00. Coverage, CritProt, Risk and Cost are unchanged (1.00, 1.00, 0.51, 0.75). The rise comes from Early's new endpoint alone, since every path is caught at its first step.
  - Centrality now places the DMZ Jump Host, Engineering WS-2 and the OT Firewall, where D31 had the Backup Control Switch in place of WS-2: F 1.0473 → 1.2060.
  - Random placements average 1.1838 → 1.3229.
- *Declared grid:*
  - Against centrality: 16 wins (10 swap, 6 decline) / 4 ties / 0 losses, unchanged.
  - Greedy equals the exhaustive optimum in 20 of 20.
  - The MILP is exact in 20 of 20, and in all 84 sampled configurations.
  - Distorted greedy is below greedy in 0 of 20.
  - The smallest rounding margins are 17,426 units on the grid and 15,074 in the sample, against bounds of 19 and 20.
- *§8's clause 2:* 19 → 18 of 20. It fails at B = 1, δ = 3, a swap, as in D31, and now also at B = 4, δ = 3, a decline.
- *Structure:* F is submodular and not monotone (1,104 monotonicity violations). Distorted greedy's preconditions hold, and g is not modular.
- *Early equals Coverage in every cell,* so on this grid Early's timing part is never exercised.
- *ε:* the optimum is the same at ε = 0 and ε = 0.1 in all 20 cells. It first changes at:
  - 1.528 under default weights (B = 3–4);
  - 3.128 under α = 3 or β = 3;
  - 2.943 under γ = 3;
  - 2.936 under δ = 3 (B = 2–4).

**5. Each decision's direction,** as measured in the reviews, each against D31 or the slate. *Likely:* those runs were not repeated here, but their combination reproduces exactly.
- *A35, unfavourable to the method.* It causes the new clause-2 failure, and greedy's lead at B = 4 with default weights falls from 1.2285 to 0.2050.
- *A43's G2-B, favourable.* Centrality picks WS-2 at B = 3–4, so its F falls in 10 cells.
- *The edge-level ConduitSL, unfavourable on leads.* Greedy's lead falls by up to 0.0375, and at B = 1, δ = 3 from 0.0342 to 0.0174. In the sample it loses one win and gains one clause-2 cell.
- *Control's FR4 cell, negligible.* Leads move by −0.0020 to +0.0041, and no count moves.
- *Early* raises F for every placement that catches a path early, and moves no placement.

**6. Disclosures.**
- *A close cell.* Greedy's lead at B = 1, δ = 3 is 0.0174. The combined review found that this cell flips only if the RTU's Damage share exceeds about 0.62–0.69, or the OT DMZ's SL falls below about 0.31–0.35. It computed these on the slate's values, before the edge-level change, so the thresholds are likely lower now. They were known when the Damage split was declared, and they are re-measured at the freeze. *[D40: re-measured on the frozen inputs, by the method D40 item 4 states: about 0.491 and 0.463. D40 item 4 compares them with these figures.]*
- *A gap in P.* No path continues the outside route through D30's leftover rule, OT Firewall → Engineering WS-2 → PLC-02, to a controller. P cannot change without voiding committed cards, so this is recorded as a limitation. A12's simulation covers the route, and its entry must disclose what was expected of it in advance.
- *Who proposed the values.* Independent Claude agents proposed every value here (D32), and Claude prepared this batch. The user accepted the values unedited.

**7. Now stale, for the next documentation pass.** Where these differ from this entry, this entry governs.
- `formal-problem-definition.md`: §2's bullets, and §5's Early and CritProt bullets, carry D33 pointer notes only. §8's question awaits A12.
- `00-glossary.md`, `02-optimization-formulation.md`, `02-system-flow.md` and `02-prototype-architecture.md`: the old Crit, Early or placeholder wording, and `02-system-flow.md`'s description of the legacy route.
- `threat-attack-model.md`: the paths do not list their targets yet.
- *T0811, separately:* D21's and #350's claims are wrong in part. The v17.1 and live pages name Duqu, not Dragonfly 2.0, as the procedure example, and list A0006 Data Historian and A0007 as targeted assets, with no engineering workstation. So P4's Historian target and step 2 stand, while step 3 (T0811 at the Engineering WS) no longer has a listed-target grounding. `sources.md` #350 carries an update line from this batch; D21's wording is corrected in the next pass.
- `testbed-architecture.md`, `04-setup-guide.md` and `00-repository-structure.md`: their mentions of the legacy route.
- `02-data-model.md`: the seed transcription, already marked stale there. Its schema copy is updated.
- `README.md`: the comparison table and the sweep subsection are marked historical, not rewritten.
- `00-action-items.md`: the rows for A35–A38, A40 and A43 are marked done, and A12 and A15–A17 carry D32's note. Their text is not rewritten.
- `02-detectability-rubric.md`: the per-asset list of artifact classes and #352 sections that G1-B asks for.

*Status: the user's choices, 2 November 2026, on the reviews that D32 describes; implemented, and verified as in item 4. Reference: `data/schema.sql`, `data/seed.sql`, `data/legacy/d25_candidate_set.sql`, `src/graph_model/__init__.py`, `src/optimizer/metrics.py`, `src/optimizer/milp.py`, `scripts/run_comparison.py`, `scripts/sweep.py`, `scripts/structure_check.py`, `README.md`, `formal-problem-definition.md` §1, §2 and §5 (pointer notes), `02-detectability-rubric.md`, `02-data-model.md`, `00-action-items.md`, `sources.md` #350.*

**D34 — A17 decided: a structured search of open indexes, with citation chasing and a patent arm, fixed in a protocol committed before any query. With it, the documentation pass for D33's stale list. No input, code or number changes. The user's choices, 2 November 2026; recorded 3 November 2026.**

**1. A17.** On 2 November 2026 the user accepted the A17 review's recommendation (D32): its option (e), a targeted protocol with citation chasing, packaged with option (d), A29's patent sweep. The protocol is `01-search-protocol.md`, fixed on 3 November 2026 and committed before any query.
- *What it fixes:*
  - five strings, built clause by clause from the novelty claim;
  - OpenAlex and Semantic Scholar as the counted indexes, arXiv as a recency check, and IEEE Xplore's public search if it is usable;
  - forward citations on eight anchor papers;
  - a patent arm;
  - screening tiers T1–T3;
  - recording that follows PRISMA-S (#394).
- *Why:* the gap was not too few indexes. No search had been recorded so that it could be re-run, and no citations had been chased. Citation chasing is the one method that has caught a paper the keyword searches missed (#326, #327). The forward-citation searches that #327 assigned, and that A17's 6 October wording dropped, are restored.
- *Not used for counts:* Google Scholar's keyword search and Crossref, whose counts cannot be re-run.
- *Route, and a correction:* the searches run from the user's browser. Claude's environment could not reach any index on 30 October 2026 (#402). A17 said "Claude can run the queries", and Claude repeated that to the user on 2 November 2026. Both were wrong.
- *Timing:* before A12 and the freeze, so that a competing method the search finds can still become a baseline.
- *What the thesis calls it:* a structured search, never a systematic review. The protocol's §13 fixes the limitation's wording and A28's opening clause.

**2. The documentation pass.** Fixed in place, from D33 item 7:
- `formal-problem-definition.md`: §2's definitions, §5's Early and CritProt, ε's rationale, the legacy note, and §7's distorted-greedy figures, which were the legacy set's.
- `00-glossary.md`, `02-optimization-formulation.md`, `02-system-flow.md` and `02-prototype-architecture.md`.
- `threat-attack-model.md`: a section listing the path targets, and the T0811 corrections at P4. D21 now carries a pointer to them.
- `testbed-architecture.md`, `04-setup-guide.md` and `00-repository-structure.md`: the legacy route.

Fixed in place, from the A17 review's own stale list:
- `sources.md`'s legend, which defined only the old meanings of 🟢 and 🔴;
- `research-synthesis-implementation.md` and `05-thesis-structure.md`;
- `00-project-timeline.md`, `05-front-matter-pack.md` and `03-honest-review.md`;
- `00-glossary.md`'s "ten iterations";
- `01-thesis-citation-shortlist.md`, which gains PRISMA-S;
- the action items A12, A17, A28, A29, A32, A33 and A42.

**3. Still open, named.**
- *`02-detectability-rubric.md`: G1-B's per-asset list* of artifact classes and #352 sections. A concern, for the user to decide: A's values were set first, so a class list written now would be written to fit them. §3's reasoning column already records each value's basis.
- *`README.md`'s comparison section* stays marked historical until Phase D's results replace it.
- *`02-data-model.md`'s seed transcription* stays marked stale in place; `seed.sql` holds the values.
- *§8's research question* awaits A12's entry.

**4. Effect.** None. The batch changes only Markdown files in `docs/`, and no code reads `docs/`, so no input, card or number changes (verified: every changed file is a `docs/` Markdown file).

*Status: A17 decided by the user on 2 November 2026; protocol fixed and committed 3 November 2026; nothing run yet. Reference: `01-search-protocol.md`, `sources.md` #393–#404, `00-action-items.md` A17.*

**D35 — A17's main search screened: no work threatens the claim and two narrow it. Full texts limited to free copies; no new baseline. The user's choices, 10–11 November 2026; recorded 11 November 2026.**

**1. What was screened.** The 375 unique records from the ten runs (#405–#416).
- *Title stage:* Claude's first pass on 5 November 2026, confirmed by the user on 8 November: 82 to the abstract stage, 5 already assessed, 133 related by title, 155 excluded.
- *Abstract stage:* 8–11 November. 77 of the 82 were judged on the abstract or more, and 5 on the title alone.
- *Full-text stage:* 13 records.
- *Already in `sources.md`:* at least 24 of the 375, not the five the first pass reported (#416).
- *Record by record:* `01-search-screening-record.md`, new.

**2. The verdicts, confirmed by the user on 11 November 2026** ("Park & Dagher T2. 269 T2. Ward T1. 368 T1. Rest confirmed.").
- *T3:* none.
- *T2, narrowing the claim:*
  - Park & Dagher 2026 (record 43; #192): optimisation-based honeypot allocation. Its version of record runs its scalability tests on synthetic Purdue-style layered graphs and sets payoffs from target values.
  - Dong et al. 2025 (record 269; #417): budgeted decoy-node placement in a power distribution grid, with a multi-term objective and criticality-weighted nodes.
  - Clause-by-clause mappings: screening record §3.
- *T1:* 202. Among them:
  - Ward 2026 (record 11; #426), the closest in topic, but designed rather than optimised;
  - Qu et al. 2026 (record 368; #432), which shares honeypots in proportion to vulnerability or risk.
- *Unresolved:* 8 records whose full text was not obtained (item 3).
- *Excluded:* 158.

**3. Full texts limited to free copies.** On 10 November 2026 the user decided to use only freely available papers: no paid access, and no waiting for author copies. No library access is available (A2) and the schedule allows no waiting. This narrows the protocol's §11.2 (an open copy, an email to the author, or a supplied PDF). It is recorded as the protocol's second amendment, in §11 and §13.
- *Effect:* 8 of the 13 full-text candidates were not read (#610):
  - six are paywalled with no free copy: records 41, 89, 151, 160, 188 and 333;
  - two have free copies the user could not reach: records 288 and 307.

  Their tiers stay unresolved. The thesis cites them from their abstracts and names them in the limitation.
- *The cost, stated openly:* record 89, Gong et al. 2027 (#419), has the closest abstract of the search.
  - What it describes: consequence-driven honeypot placement in a three-layer chemical-park ICS, along attack graphs, under a budget, validated on a water-tank rig and the Tennessee Eastman Process.
  - It could be T2 or T3, and it was not read.
  - Its abstract shows none of the claim's distinguishing clauses: no IEC 62443 zones or conduits, no ATT&CK paths, no interception-stage term. The full text could contradict that, and an examiner who has read it could find overlap this project missed.

**4. Effect on the claim (A28).** The draft survives as worded. No work found combines three things: IEC 62443 zones and conduits as numeric inputs; a scored interception stage along ATT&CK-grounded paths; and validation against random and centrality baselines.

It is narrower than the project's earlier framing:
- *Purdue-style evaluation already exists.* Optimisation-based honeypot placement has been evaluated on Purdue-style layered graphs (Park & Dagher). The earlier conclusion that their paper is "an enterprise/general-network paper, full stop" held for its preprint only (#192). It is corrected in the three files that repeated it.
- *Budgeted, criticality-weighted placement already exists.* Multi-term decoy-placement optimisation under a budget, with criticality weights, exists for power CPS (Dong et al.).
- *IEC 62443 levels already enter optimisation as numbers.* Sakata et al. 2026 (record 72; #427) use them to choose one PLC's countermeasures, not for zones, conduits or placement. The thesis may not claim the first numeric use of IEC 62443 levels, only of zones and conduits in a deception-placement objective.
- *The landscape cell is no longer "one close paper".* `research-synthesis-implementation.md`'s "nearly empty, one close paper" cell is updated.

A28's wording does not change now. Its opening clause waits for the remaining runs and A29 (protocol §13).

**5. Baselines (§11.6).** Neither T2 method becomes a baseline:
- *Park & Dagher* solve a different problem: a multi-round Bayesian Stackelberg game over attacker types, with honeypots moved every round. Their code is in a private repository (#192).
- *Dong et al.* combine a GAN, multi-agent reinforcement learning and distributionally robust optimisation across three levels, and released no data or code.
- *Cost:* re-implementing either would take about a weekend-unit or more, with no way to check the copy against the original.
- *Deferred:* adding Park & Dagher's greedy rule as an extra comparison is decided with A12, before the freeze, because its worth depends on what Phase D measures. The rule places the honeypot at the node with the highest distance-discounted target value.

No evaluation input changes.

**6. Record-keeping.**
- `sources.md`:
  - #417–#609: one entry for each of the 193 kept records not already logged (protocol §10);
  - #610: the free-copy search, a negative result;
  - #611: three backward-round candidates from Park & Dagher's references, queued;
  - #612: a patent lead for A29, US 12,335,308;
  - update lines on #192, #317, the run entries #405–#409 and #411–#415, and #416.
- `01-search-protocol.md`: amendment 2, in §11 and in §13's limitation text. The limitation text also records the two titles screened by translation.
- `01-search-screening-record.md`: new, with its registry row in `00-project-index.md`.
- *Fixed in place, with D35 notes:*
  - `iteration-2-findings.md`'s headline correction;
  - `01-thesis-citation-shortlist.md`: entry 8, plus five new entries, 45–49;
  - `research-synthesis-implementation.md`'s landscape table.
  - `05-thesis-structure.md`: section 2.4's plan and the line on the claim's strength.
- `00-action-items.md`: A17, A28 and A29.

**7. Effort.** The protocol estimated about 1 weekend-unit for the literature part, with 0–3 full texts (§12). The main search sent 13 records to full text, and the abstract stage ran from 8 to 11 November, so the estimate was exceeded. The remaining runs (item 8) are estimated at about 0.5 weekend-unit.

**8. Still open.**
- the arXiv recency check;
- IEEE Xplore's public search (S1 and S4), whose pages open in the user's browser;
- TechRxiv;
- forward citations on the eight anchors, plus one backward and one forward round for each T2 work (§7.4; three candidates queued, #611);
- the patent arm (A29);
- the update re-run within a month of submission.

**9. Effect.** None on any input, card or number. Only Markdown files in `docs/` change (verified: every changed file is a `docs/` Markdown file).

*Status: the verdicts and the free-only rule are the user's (10–11 November 2026); recorded 11 November 2026. Reference: `01-search-screening-record.md`, `sources.md` #405–#416 and #417–#612, `01-search-protocol.md` §11 and §13.*

**D36 — A17's remaining searches and A29's patent arm run and screened: nothing found threatens the claim as worded; one patent is proposed as T2 and two are borderline. Searching closes as the protocol fixed it, with one re-run recommended. The user's choices, 15 November 2026; recorded 15 November 2026.**

**1. What ran** (14–15 November 2026; protocol §3, §7 and §8; run entries `sources.md` #613–#643).
- *Paper side (A17):*
  - arXiv, S1 and S2: 5 and 7 records, none new (#613, #614).
  - IEEE Xplore's public search, S4 and S1: 9 and 85 (#615, #616). Whether IEEE's terms allow this use is still unverified (#404).
  - The papers citing the ten works, through OpenAlex: 82 (#617).
  - The term "honeypoint" in OpenAlex: 16 (#618; amendment 3).
  - Google Scholar's "Cited by" lists of the ten works: 129 rows (#619).
  - TechRxiv, covered through OpenAlex (#620).
  - One backward round for Dong et al. (#621); backward and forward rounds for BAG-HRF and Voznyi et al., and the queued round of #611 (#622).
  - *Result:* 187 new records (376–562 of the screening record): T3 0; T2 0; related (T1) 80; tier unresolved 2; excluded 105 (#623). With the main search (D35), 562 records: T3 0; T2 2; T1 282; unresolved 10; assessed earlier 5; excluded 263.
  - *The papers in run P6's tables* (below): 193 non-patent rows on 16 pages; 35 deception-titled titles, of which 8 were in the log and 27 were not (23 per cent in the log); the 27 are related (T1) on their titles and none was read (#641).
- *Patent side (A29), Google Patents only:*
  - S1 on the full text returned about 24,680, over §6's limit of 1,500, so it was narrowed once, to title, abstract and claims: about 260 (#624, #625).
  - The term "honeypoint": 574 distinct patents, with up to about 400 more reported but never seen (#626).
  - Assignees: Acalvio, Attivo and Illusive, all patents; Fortinet, Commvault, SentinelOne and Proofpoint, on deception terms only; TrapX and CounterCraft returned nothing (#627–#635).
  - Classification H04L 63/1491, a count of 11,205 (#636), and with placement and OT terms, 409 (#637); the patents citing US 9,853,999 B2 (#638); the ten known leads (#639).
  - *Run P6, the similarity route (amendment 7; #640):* the "Similar documents", "Patent citations", "Cited by" and "Families citing this family" tables on the pages of nine of the closest patents and of seven pages that those led to: 243 patent rows, 229 distinct patents. 60 carry a deception term in the title, and the earlier runs already held 27 of them (45 per cent); 38 patents are new to the data (20 opened, 18 judged on a title).
  - *Result:* 1,394 distinct publication numbers (#642).
- *Route.* The paper-side searches ran from the user's browser. The 262 patent pages that were read, Claude read through its fetch tool on the Google Patents page, which returns a small model's summary of what Claude asks for, and Chinese, Korean, Japanese and Taiwanese ones through Google's machine translation. For 24 pages the first fetch returned a server error and another address was read. **Three pages needed more than that, and all three were read in the end:** the A document of CN 119051914 A (#969) failed at both addresses at first, the page of its granted B document, which carries the same title, was read in its place, and the A document's page was read afterwards at /zh once the fetch tool was available again (its claims carry no version label, so it is not confirmed whether they are the A or the B text); CN 120498905 A (#974) failed at the plain address and at /en and was read at /zh, Google's machine translation of the Chinese; and CN 122621588 A (#981), a cut-title exclusion of run P1b (14.5 of the screening record), was refused at its /en address ("robots_disallowed") and was read afterwards at /zh.
- *Not searched:* the USPTO's own Patent Public Search (the protocol said it would be; amendment 5 corrects that); Scopus and Web of Science (already in the limitation).

**2. The verdicts.** First passes by Claude, except where the user decided on 15 November 2026 ("Tan unresolved. Rest confirmed.").
- *T3:* none, in papers or patents.
- *T2, papers:* none new. Park & Dagher (#192) and Dong et al. (#417) stay the two.
- *T2, patents:* one, **proposed**: CN 122339846 A, granted as CN 122339846 B (Guangzhou University; #727). The user confirms it (protocol §9). Item 3.
- *Borderline between T1 and T2, the user's call:* CN 117675308 A (#838) and CN 121012683 A (#886). Item 4. Both are counted T1 until he decides.
- *The user's nine calls of 15 November:* BAG-HRF (record 419; #645) and Tan et al. (record 412; #646) tier unresolved, because their full texts are not free (the thesis cites both from their abstracts and names them in the limitation); Voznyi et al. (#667) and Wang et al., "Turn the tables" (#686) T1; and T1 for the five patents closest by method, which the tiers gate on the OT domain: Cybersense GmbH's US 12,261,855 B2 (#730), Bosch's EP 4 586 550 A1 (#914), CN 122339820 A (#728), CN 120034354 A (#729) and CN 118694612 B (#731).
- *Patents, all:* T3 0; T2 1; related (T1) 712; excluded 681. Counts are by publication number, and the grant of the proposed T2, CN 122339846 B, is counted among the related (T1) on titles (record 15.1). 262 pages were opened in five rounds (91, 41, 68, 39 and 23); 1,128 patents were judged on a title alone. No patent found by run P6, or found again by it, is T2 or T3.
- *Not reviewed by the user record by record:* the other paper title-stage and abstract-stage calls and the patent title screen. They stand as Claude's first pass (D35 had its title stage confirmed three days after).

**3. The proposed T2: CN 122339846 A/B** (Guangzhou University; priority 2026-06-02; the application published 2026-07-03; granted 2026-08-11). It is of the same kind as Dong et al., which the user ruled T2 in D35. Clause by clause against A28's draft claim, from the claims of both pages and the description of the A page, read through machine translation:
- *OT/CPS setting:* yes, an electric power information physical system (servers, switches, gateways, power terminals).
- *Selects deception positions under a decoy budget:* yes. Claim 1 takes each node's state, vulnerability, asset value, type and links, picks a target defence set under a defence-resource constraint and deploys baits of matching types. Claim 3 takes the top scorers up to a preset quantity; claim 4 gives light, medium or heavy baits by asset value; claim 7 makes the scorer a reinforcement-learning Q-network.
- *A stated objective:* in the description, a reward of capture bonus minus intrusion penalty minus bait cost; not in the claims.
- *Asset criticality as a numeric input:* yes (asset value).
- *IEC 62443 zones and conduits:* no. The network is an undirected graph; no Purdue levels.
- *Interception along ATT&CK-grounded attack paths:* no. No ATT&CK, attack paths or attack graph; the modelled attacker picks targets by a Softmax over asset value, availability, degree centrality and neighbour value.
- *Validation against random and centrality baselines:* one random strategy; no network, node counts or figures in the text.
- *Same applicant:* CN 122339820 A (#728) and CN 121603304 B (#775).
- *Effect:* it narrows the claim and does not threaten it. If the user confirms T2, the thesis cites it with Dong et al. in Section 14.

**4. The two borderline patents.** The user decides; Claude's lean is stated with its confidence.
- **CN 117675308 A** (State Grid research institutes; priority 2023-11-28; application pending; #838). Claim 1 builds an attack graph from scanned host vulnerabilities (MulVAL or similar), finds a high-harm path by an adaptive depth-limited search, and "determine[s] a honeypot deployment scheme on the high-harm attack path by adopting a game theory algorithm". The three-player game has payoffs with a honeypot deployment cost, and its optimal strategy decides node by node whether a honeypot goes there. It has no explicit budget, no zones, no asset criticality (harm is a CVSS node score) and no ATT&CK. The setting is stated as large-scale power grid systems, but the method is a generic vulnerability graph.
  - *Lean: T1, likely.* The user ruled CN 118694612 B T1 on 15 November: a State Grid patent that also builds a MulVAL graph and places honeypoints by CVSS difficulty, with a power-system framing and no OT-specific input. This one is more formal but has the same setting. T2 only if a power-grid framing alone counts as an OT setting.
- **CN 121012683 A** (Anhui University of Traditional Chinese Medicine; priority 2025-09-09; application pending; #886). Claim 1 models a substation virtual LAN, builds a graph of all IEDs, splits it into observable subgraphs and deploys "detection baits" and "protection baits" in each. A bilevel mixed-integer problem (defender leader, attacker follower) decides, per subgraph, how many attack agents and how many IDS and IPS agent groups; it is solved by regret-minimisation rules. It has no deployment cost, budget, asset criticality, attack-graph or ATT&CK data, zones or conduits, and no experiments; the utility formulas are blank in the translation.
  - *Lean: T2, likely.* **This changes the first draft of this entry, which leaned T1 (unconfirmed);** a re-read of the page on the evening of 15 November, with quotations in the original Chinese, resolved the open point (whether the baits are deception assets). The Chinese title is 一种变电站TSN网络欺骗防御方法、装置、设备及介质, "a substation TSN network deception-defence method, device, equipment and medium", which Google Patents' English title renders with "spoofing"; claim 1 opens with the same words; the background says the invention lures attackers away from the real system; and attacker traffic is lured into the protection bait and interacts with it there. The detection bait reads as a sensor, no sentence says a bait imitates a device, and neither is called a honeypot or decoy. The construction is Jay (2023): observable subgraphs, two rings plus per-node subgraphs, and protection and detection decoy types (#305, #312). The page cites neither Jay nor anything else.
  - *It is T2 if Jay-type allocation counts as formal deception-placement optimisation in OT* (how many decoys of which type for each observable subgraph; a substation VLAN; a bilevel optimisation; no criticality, no zones), which is how §9's definition reads, and T1 if the user does not count that kind of allocation as placement. Jay (2023) is already the closest work named in the novelty argument (D7), with its distinctions argued from the full text (#312); a T2 ruling on this patent adds a patent that follows Jay's construction, not a new kind of work.
- *Either way the claim stands:* neither has zones, conduits, criticality, ATT&CK-grounded paths or baselines. A T2 ruling adds one more work to cite and distinguish.

**5. The closest by method, and what each lacks.** All T1, by the user's calls or as Claude's first passes. None has IEC 62443 zones or conduits as numeric inputs, an ATT&CK-grounded interception term, or the random-and-centrality validation.
- *US 12,261,855 B2* (Cybersense; #730; granted 2025-03-25): an attack graph; the type and number of lures and decoys follow from its structure; a target function rewards decoys on short paths and on many paths and near weak points (worked example A = 10, B = 2). Upper limits on counts are parameters, but there is no budget. An Active Directory example; no zones, segments or asset criticality.
- *EP 4 586 550 A1* (Bosch; #914; application): chooses which vehicles host honeypoints and scores a placement by the probability that the honeypoints would have detected reported attacks; keeps it or searches for a better one. No objective function, budget, criticality or zones. A vehicle fleet, not OT.
- *CN 122339820 A* (Guangzhou University; #728): honeypoint placement in a two-layer IoT architecture as a zero-sum Stackelberg game over a network layer and a physical layer treated as separate security domains; the defender's commitment is a k-sparse mixed-integer program that maximises expected interception over active attack paths, with exact honeypot counts per layer and node risk scores. The nearest to the claim's interception stage. No industrial wording, criticality, zones, conduits or ATT&CK, and no evaluation reported; the formulas were stripped in the translation.
- *CN 120034354 A* (BUPT; #729): a Stackelberg game places honeypots on edges under a total-honeypot budget, solved by linear programs; breach probability by logistic regression, damage weighted by node importance, attack paths from entry to target nodes; simulated against an unnamed method. Enterprise and SDN networks; distribution grids appear as motivation only.
- *CN 118694612 B* (State Grid Jiangxi; #731): a MulVAL attack graph; the top N of M attack edges by CVSS difficulty get honeypoints; a multi-objective firefly algorithm tunes position-prediction models. No budget, asset value or zones; the translation of the claims was garbled.
- *CN 121603304 B* (Guangzhou University; #775), the nearest in a power setting that names an optimisation, tier at the user's option: language-model-generated decoy web targets for power scenes, with an unspecified multi-objective optimisation whose output includes a deployment position; no formulas, solver, budget, criticality or zones.
- *CN 118842645 A* (#749) and *CN 122457351 A* (#785): formal placement outside OT. The first rebuilds attack paths from honeypoint logs, ranks nodes by centrality and places honeypoints by an objective over attacker cost, attack time and a risk index, with a cap on protected nodes; the second gives a Nash deployment probability over candidate honeypoint nodes, with a deployment cost.
- *Formal placement outside OT, found in the fourth and fifth rounds* (8 patents, all T1 on the OT gate): **CN 121356815 A** (#771; item 6), CN 120658528 A (#879; State Grid Shanghai: a decision-tree search that maximises the attacker's cost of re-planning, with a machine-capacity cap, positions and vulnerability types; no OT wording in the text), CN 118802292 B (#849; China Mobile: how many honeypots on each node by a benefit function over an attack-path graph), CN 116155542 B (#820; PLA Information Engineering University: a minimal count of breadcrumbs from a threshold on the probability of leading an attacker into a trap), CN 115580430 A (#814; where only, by a DQN on an attack tree), CN 118400169 B (#845; Internet of things: a DDPG security game with a count constraint and a centrality-based cost), CN 121664448 A (#893; China Southern Power Grid: a Stackelberg MILP, deploy-or-not per node, node value minus deployment cost; no OT wording although the applicant is a power-grid company) and CN 119383021 B (#858; which IP addresses honeypots take, not where). CN 117061224 A (#831) is a configuration game (whether a server acts as a honeypot), not a where-or-how-many method.
- *BAG-HRF* (#645; abstract only): greedy honeypoint placement by marginal risk reduction under a budget on a Bayesian attack graph with path probabilities and asset values, evaluated on an airport network. Its abstract shows none of the three distinguishing clauses; the full text could. *Voznyi et al.* (#667; abstract only): budgeted Bayesian Stackelberg placement, brute force and greedy, on synthetic networks of 10 to 40 nodes. *Tan et al.* (#646; abstract only): a time-delay evolutionary game for PLC honeypoint defence in power-IoT, with payoff from load loss on an IEEE 22-bus system; the abstract does not say whether its strategies are positions.

**6. Effect on the claim (A28).** The draft survives as worded. Nothing found is T3. *Confidence: likely, not verified* (limits below).
- *What no work combines:* the three things D35 named, now also checked against the patents and the 187 later paper records: IEC 62443 zones and conduits as numeric inputs; a scored interception stage along ATT&CK-grounded attack paths; validation against random and centrality baselines.
- *The nearest on method is an IT-side patent, CN 121356815 A* (Guangzhou University; #771; published 2026-01-16; read on three occasions, with the readings in agreement). It collects network data, builds a MulVAL attack graph, scores honeypoint placements on three coverage objectives (area; the attack-path blocking ratio, blocked paths over all paths; vulnerability-rank coverage) and outputs Pareto-optimal deployment sets by NSGA-II under a count cap, with a criticality-weighted environmental factor (business importance, asset value and zone level). Against the draft claim: *a stated composite objective*, yes (three terms); *a decoy budget*, a count cap within resource limits and no monetary budget; *asset criticality*, partly, through the environmental factor; *a path term*, yes (the blocking ratio, with no ATT&CK and no stage labels beyond "multi-stage penetration path"); *IEC 62443 zones and conduits as numeric inputs*, no: a zone level enters its vulnerability score, but nothing ties it to IEC 62443 and there are no conduits; *OT setting*, none in the text; *baselines*, none, and no experiments. It is the nearest published method to the objective and the budget of the claim, and it lacks the OT setting, the zone and conduit inputs, the ATT&CK-grounded stage term and the baselines. Its title, as Google's list cut it, no longer showed a deception word, and its text has no word from S1's OT block, so the title rule excluded it and run P1n could not have returned it (item 8).
- *What the new results narrow,* beyond D35:
  - A budget or count cap, asset value or criticality, and attack paths each appear in published placement methods, two or three at a time: in general networks (BAG-HRF's abstract, Voznyi et al., CN 120034354 A, US 12,261,855 B2, CN 118842645 A, CN 122457351 A, CN 121356815 A, CN 120658528 A, CN 121664448 A) and in power systems (Dong et al., CN 122339846 A/B, CN 117675308 A, CN 118694612 B, Tan et al.).
  - So the claim rests on its distinguishing clauses together, not on any one of the others. The thesis may not claim a first for budgeted, criticality-weighted or attack-path-based placement, for multi-objective placement, or for placement in a power system; D35 already limited the IEC 62443 clause to zones and conduits.
  - One group is very active: 61 of the 262 patents opened are Guangzhou University's or its research institute's (some filed jointly with companies), and four of its 2026 publications are game or optimisation methods (CN 122339820 A, CN 122339846 A, CN 122457351 A, CN 121356815 A). The update re-run (item 10) may find more.
- *Baselines (§11.6):* none of the new works becomes a baseline, for the reason D35 gave for Dong et al. CN 122339846 A/B is a reinforcement-learning scorer with no data or code in its text, and the formulas of the game-theoretic patents were stripped by the machine translation, so a re-implementation could not be checked against the original. D35's deferred question, Park & Dagher's greedy rule as an extra comparison, stays with A12, which D34 placed after this search. **One question for A12 (the user's, optional):** whether a coverage-style comparator, an attack-path blocking ratio under a count cap as in CN 121356815 A, is added beside the random and centrality baselines. It would need its own entry and must be fixed before Phase D; this entry adds none.
- *A gap found in the strings, and a re-run recommended (amendment 7; protocol §4).* Block O of the strings has "smart grid" and "substation" but no "power grid", "power system", "electric power", "new power system", "distribution network" or "power plant". S1, S2 and S5 use it on the paper side, and S1 (P1, P1n) and the classification run P3b on the patent side. A work that describes a power network in those words and carries no other word of the block was not returned by them. It matters in practice: CN 121356815 A, CN 120658528 A and CN 121664448 A have no OT wording at all, and two of the three are power-utility patents. S3, S4, P1b, the assignee, citation and lead runs, run P6, the thirteen earlier rounds of web searching and the forward-citation searches do not use the block, so the paper side has other routes to power-system work; how much they covered was not measured. **Recommended, before A12 and the freeze:** a widened re-run, S1 on Google Patents (narrowed as P1n was) and S1, S2 and S5 on OpenAlex and Semantic Scholar with the six words added to block O, keeping only what the first runs did not return. About 45 minutes in the user's browser and about 0.2–0.3 weekend-unit to screen what is new; both are estimates. The protocol puts the literature part before the freeze so that a competing method can still become a baseline (§12), which is why it should come now. It is a search, not an evaluation input; nothing in it changes a card or a number.
- *Limits on the confidence:* ten paper full texts not obtained (the eight of D35 and BAG-HRF and Tan et al.); 1,128 patents judged on a title alone, and the rule's exclusions proved unsafe (item 8); patent pages read through a small model's summary and, for most, machine translation; the gap in block O above; and the similarity route is a sample: the earlier runs already held 27 of the 60 deception-titled patents that its tables name (45 per cent), so the neighbourhood of the closest patents was not covered by the keyword runs, and the route stopped at depth two on Claude's choice. That figure measures the runs' reach around those patents, not recall in general, because the tables are Google's selection and not a sample.
- *A28's opening clause.* D34 fixed "open scholarly indexes and granted patents". The patent arm covered published applications too (the proposed T2 is an application and its grant; Bosch's, CN 120034354 A and CN 117675308 A are applications), so "granted patents" understates it. D36 proposes "granted patents and published patent applications", for the opening clause and for "including granted patents" in the draft claim. The wording is the user's (A28); `01-search-protocol.md` §13 carries the proposal and leaves the clause unchanged.

**7. Protocol amendments 3 to 7** (each is in the protocol in place; before and after in #643).
- *3:* the term "honeypoint", as two further runs (#618, #626), because BAG-HRF was found by it alone.
- *4, the user's choice (a):* patents are recorded compactly: an entry for each run and for each patent whose page was opened; the other patents appear in the screening record's tables only.
- *5, a correction:* the protocol said patents would be searched in "Google Patents and the USPTO's Patent Public Search". Only Google Patents was searched.
- *6, added by Claude; the user can strike it:* patents were screened on their titles by a keyword rule written during the screening, with the pages of flagged titles opened and five rounds of reading (91, 41, 68, 39 and 23 pages).
- *7, added by Claude; the user can strike it:* run P6, the similarity route, a sixth patent route that starts from the pages of the closest patents (#640), and the statement of the gap in block O (protocol §4).
- The limitation text of §13 follows: "a patent search in Google Patents", "four titles in other scripts" (records 374, 375, 490, 501), a sentence on the patent screening, a sentence on the OT words of the strings, and [n] = 10.
- *Not amendments:* S1's one narrowing (§6 applied); the four vendors searched on deception terms only; the lead US 12,335,308 joined §8 by D35.

**8. Corrections to Claude's own earlier statements.**
- *"No T2 patent."* That held for the patents screened on titles. The one T2, CN 122339846 A, has a neutral title ("A method and system for active defense of power cyber-physical systems") that the keyword rule had excluded; it came to light only because a check of run P1n's excluded titles opened some. The statement is now "one proposed T2".
- *The rule's exclusions are not safe.* In the second round 35 excluded P1n titles were opened: 30 were related, 1 was T2 and 4 stayed excluded. In the third round 29 were opened: 19 related and 10 excluded. In the fourth, 39 were opened: 26 related and 13 excluded. US 2024/0323228 A1 (#939) is the published application of US 12,425,450 B2 (#311), a deception patent that a neutral title had excluded; it is corrected to T1. Some patents had titles that Google Patents cut before or just after their deception word (CN 122386884 A, CN 117113335 A, CN 121808769 A), and the rule excluded them; they were read and are T1.
- *"The residual cut-title exclusions of run P1b are false hits"* was Claude's earlier reading of that residual, and it was wrong. Of the 21 cut-title exclusions opened in the fourth round 13 proved related (T1), and CN 121356815 A, the nearest patent by method, was one. The last 3 of those 21 (CN 115752492 A, CN 122621588 A, WO 2015/196373 A1) were the ones that showed a security-type word in the visible title; they were read at the end of the round, after the fetch tool's usage limit had lifted, and stay excluded. 13 cut-title exclusions of that run are still unopened, and none shows a security-type, industrial-control or power word in the visible part; they are a limit, not a set of false hits (screening record 14.5).
- *The lean on CN 121012683 A* changed from T1 (unconfirmed) to T2 (likely) after the re-read of its Chinese text (item 4).
- *A fetch summary overstated one patent:* CN 117560175 A (#837) was first read as having "zone and threshold rules"; a targeted re-read found only "network areas". The entry carries the corrected reading, and the example is why summaries are named as a limit.
- *The protocol's "USPTO Patent Public Search"* was never searched (amendment 5).

**9. Record-keeping.**
- `sources.md`: #613–#988. Run entries #613–#640, the papers named in P6's tables #641, the outcome #642 and the amendments #643; #644, a budgeted, zone-aware hardening paper found incidentally; #645–#726, the 82 kept papers (80 T1, 2 unresolved); #727–#988, one entry for each of the 262 patents whose page was opened (amendment 4). Update lines on #15, #285, #347, #374, #390, #401, #404, #611 and #612.
- `01-search-protocol.md`: amendments 3–7 in §3, §4, §8, §10 and §13.
- `01-search-screening-record.md`: records 376–562 (§12–§13), the patent arm (§14–§17), and §1, §10 and §11 brought up to date.
- `00-action-items.md`: A12, A17, A28, A29 and A32.
- *Fixed in place, with D36 notes:* `01-thesis-citation-shortlist.md` (entries 50–55, the count and the log size); `research-synthesis-implementation.md`; `05-thesis-structure.md`; `03-commercial-prior-art-analysis.md`; `03-honest-review.md`; `00-project-index.md`.

**10. Effort.** D35 estimated about 0.5 weekend-unit for the remaining runs. They took the weekend of 14–15 November 2026, about one weekend-unit; the user's share was the browser runs and the decisions, and the rest, the patent arm's screening and reading in five rounds, was Claude's. Still to come: the recommended widened re-run (about 0.2–0.3 weekend-unit, item 6); the update re-run within a month of submission (about 0.1–0.2); an optional re-run of the "honeypoint" patent search in date slices (about 0.1); and two optional readings by Claude with no step for the user, of the 67 patents of run P1n still related on a title only (none of the 47 of that kind already read proved T2 or T3) and of the 175 patents related on a title that Google Patents had cut (about 0.5–1 weekend-unit of elapsed time together).

**11. Waiting for the user.**
- Confirm or reject CN 122339846 A/B as T2 (item 3).
- Rule on CN 117675308 A (lean T1, likely) and CN 121012683 A (lean T2, likely) (item 4); optionally on CN 121603304 B.
- Say whether the OT gate stands for CN 121356815 A and CN 120658528 A, and whether a zone level inside a score counts toward the zone clause (item 6). Claude's first pass is that it stands and that it does not count.
- Confirm four patent exclusions that §9 asks him to confirm: CN 116318314 B (#959) and CN 115914014 B (#957), physical anti-drone navigation-spoofing transmitters; CN 117834239 A (#964), a mimic-defence firewall; CN 304151907 S, a design registration of an "industrial control honeynet" display model, judged on its title alone. And one paper row: Arunagirinathan et al. (2025), where "deception attacks" is the control-theory false-data term (Claude recommends it stand excluded).
- A28's opening clause (item 6).
- Amendments 6 and 7: keep or strike.
- The widened re-run of block O (item 6): yes or no.
- Optional: free full texts of BAG-HRF and Tan et al., if he finds any.

**12. Effect.** None on any input, card or number: no code, data, parameter, attack path, objective or candidate changes. Only Markdown files in `docs/` change. Nothing that feeds the evaluation is touched.

*Status: the nine borderline calls are the user's (15 November 2026); the tiers, the proposals, amendments 6 and 7 and the screening are Claude's first pass; searching for A17 and A29 closes with this entry as the protocol fixed it, apart from the re-run recommended in item 6; recorded 15 November 2026. Reference: `01-search-screening-record.md` §12–§17, `sources.md` #613–#988, `01-search-protocol.md` amendments 3–7.*

**D37 — Phase D's evaluation is fixed before any run on the testbed: leave-one-path-out, an attack simulation from every non-controller foothold, a coverage-only comparator, and the research question reworded (A12). D36's rulings are made, the physical testbed comes last (A16), and the explanation layer is built before TA-2 (A6). The user's choices, 16 November 2026.**

**1. Why now.** The user reported that TA-2 is on 27 November 2026, the first of A14's dates to become known, and asked that the project be ready by then: "at least project should be ready, tunning and test bad can be done after TA 2". TA-2's format, TA-3 and the final submission date are still unknown (A14).

**2. D36's rulings (its item 11).** All the user's, 16 November 2026, each on Claude's lean:
- *Tiers:*
  - CN 122339846 A/B is T2.
  - CN 117675308 A is T1.
  - CN 121012683 A is T2, because §9's definition counts a Jay-type allocation as formal deception-placement optimisation in OT.
  - CN 121603304 B stays T1.
- *The OT gate:* it stands for CN 121356815 A and CN 120658528 A, and a zone level inside a score does not count toward the zone clause.
- *Exclusions:* the four patent exclusions stand (CN 116318314 B, CN 115914014 B, CN 117834239 A and CN 304151907 S), and so does the paper row Arunagirinathan et al. (2025).
- *A28's opening clause* becomes "open scholarly indexes, granted patents and published patent applications". The draft claim's "including granted patents" becomes "including granted patents and published patent applications".
- *Protocol amendments 6 and 7* are kept.
- *The widened re-run of block O* (D36 item 6) goes ahead. Its run sheet went to the user on 16 November, with the six power-network words as a separate block, so each query returns only records that carry one of them. Its results are screened in a later entry, before the freeze, as the protocol puts the literature part before it (§12). *[D38: screened, 16 November 2026.]*

The works that narrow the claim are now Park & Dagher and Dong et al. (D35), CN 122339846 A/B and CN 121012683 A. None threatens it, and A28's draft survives with the new opening clause. CN 121012683 A joins the citation shortlist as entry 56, as the shortlist said it would if ruled T2; entry 50, the synthesis table and `05-thesis-structure.md` §2.4 record the rulings.

**3. The testbed (A16): the modelled network carries the evaluation, and the physical build comes last.** The user: "test bed is least priority if everything else is done then we will go to testbed." Every Phase D number is computed on the modelled network; the VMs would demonstrate, not measure. A21 stays open.

**4. A12: the evaluation and the research question.** `03-evaluation-methodology.md`, new in this batch, fixes them before any of the new tests has run on the testbed. The user accepted Claude's three-part design ("this should be done"):
- *Leave-one-path-out* (§2), the guide's K-fold-style request (D32). Each path is held out in turn, and the placement chosen from the other four is scored on it.
- *An attack simulation* (§3), the guide's simulation request (D32). It takes every loop-free route, at most one hop longer than the shortest, from every non-controller foothold to every controller and path target, through the recorded connections in either direction. Every route is enumerated, so the result is exact and needs no seed.
- *The existing grid, weight sweep and structure check*, reported as before.

Two more things were added on 16 November:
- *A coverage-only comparator* (§4). It answers D36 item 6's question: does F's five-term objective add anything over attack-path blocking alone? Its primary form averages over every placement that reaches the highest coverage; the frozen greedy run on coverage alone is reported beside it. The user chose the averaged form once Claude raised greedy's arbitrary tie-break.
- *The research question* (§5), accepted by the user as worded:

> On the modelled testbed, does choosing decoy positions by the composite objective F — found by greedy and confirmed exact by MILP — catch attacks the optimiser was not given, at least as often and as early as betweenness-centrality placement, random placement and a coverage-only optimiser, at equal budget? The attacks are each attack path when it is held out of the optimisation, and simulated attack routes from every non-controller foothold to every objective.

The D20 wording is still reported against, with D24's caveat that its first clause follows from optimality.
- *Hypotheses and rules:* §5 fixes hypotheses H1–H3 and the rules that classify each as supported, mixed or not supported. The user's pre-registration (A15) restates them, and `scripts/evaluate.py` applies them.
- *Expectations:* §7 states what is expected before any run, including the expectation D33 asked for on the route OT Firewall → Engineering WS-2 → PLC-02.
- *Not added:* Park & Dagher's greedy rule (D35 item 5). Their rule places a honeypot at the node with the highest distance-discounted target value. That needs target values and a discount defined for their game, and this model has neither, so a copy could not be checked against theirs. The coverage-only comparator tests the composite objective directly instead. The user can still add the rule before the freeze, with its own entry.

**5. Two corrections Claude made while designing, stated rather than folded in.**
- *The footholds.* Claude's first design started the simulated attackers at P's three entry assets: the Engineering WS, the DMZ Jump Host and the OT Firewall. Greedy's published placement at B = 3 is exactly those three (D31, D33), so it would have caught every route at its first step by construction, which repeats F's Early term instead of testing it. The footholds were widened to every non-controller asset. The documented-entry population is kept as a secondary result, with that caveat.
- *The comparator.* The greedy form the user first approved breaks ties by scan order (§4 above).

*Disclosure:* Claude designed the populations and the comparator knowing D31's and D33's published placements. No leave-one-path-out or simulation output on the testbed existed when they were fixed. `scripts/evaluate.py` cannot produce one before the freeze, because it refuses to run without the freeze manifest.

**6. The explanation layer (A6) is built before TA-2.** The user's choice ("this must be done before ta 2").
- *Model:* `qwen3:4b`, Q4_K_M, 2.5 GB on the Ollama registry (#989, checked 16 November 2026). It fits the graphics memory of the user's laptop: an NVIDIA GeForce RTX 2050 with 4 GB, 16 GB RAM, from the user's screenshots of 16 November. *[D43: the tag `qwen3:4b` is Qwen3-4B-Thinking-2507, which cannot switch thinking off, and 2.5 GB is its size. The declared model is now `qwen3:4b-q4_K_M`. And the card also draws the laptop's screen, so the model may not fit entirely: D43 item 7.]*
- *Settings:* temperature 0 and thinking off, as the scoring notebook used greedy, non-thinking decoding (D26).
- *Checks:* every number and asset in an explanation is checked against the run, with a template fallback (`03-evaluation-methodology.md` §6). That section fixes now how the secondary research question is evaluated.
- *Timing:* the layer is built in a later batch. It is not an evaluation input, so it is not frozen.

**7. "Tuning".** The user listed tuning, with the testbed, as work for after TA-2.
- Under the evaluation-integrity rule no weight, K, rubric or input changes after the freeze. The weight sweep reports how the results move with the weights; that is reporting, not tuning.
- A change the user means by tuning that would alter an input is made before the freeze with its own entry, or after Phase D as a separately reported study.

**8. Verified on 16 November 2026, before this batch.**
- *Reproduction:* a fresh clone of `7c88be5` builds with `scripts/setup.py` and restores the committed review. Its three scripts reproduce D33 item 4 exactly:
  - `run_comparison.py 3`: greedy F 2.4175, centrality 1.2060, random mean 1.3229;
  - `sweep.py --sens`: 16 wins / 4 ties / 0 losses, and clause 2 in 18 of 20. The MILP is exact in all 20 cells and in all 84 sampled configurations;
  - `structure_check.py`: F is submodular and not monotone (1,104 violations), and g is not modular.
- *Self-test:* `scripts/evaluation_selftest.py` passes on its toy network. It matches every hand-computed value, runs every method unchanged end to end, and shows that the freeze check refuses a missing or changed manifest.
- *Not run:* `scripts/evaluate.py` was not run on the testbed.

**9. Effect.** No input, card, weight, method or number changes. The new code adds criteria: `src/evaluation/`, `scripts/evaluate.py`, `scripts/freeze.py` and `scripts/evaluation_selftest.py`. It calls the frozen methods unchanged.

**10. Next.**
1. The re-run's results, screened.
2. The user's pre-registration (A15).
3. The freeze: `scripts/freeze.py`, every check re-run, and the entry against D25.
4. Phase D.
5. The explanation layer.

*Status: the user's choices, 16 November 2026, on Claude's proposals; design fixed before any run on the testbed. Reference: `03-evaluation-methodology.md`, `src/evaluation/`, `scripts/evaluate.py`, `scripts/freeze.py`, `scripts/evaluation_selftest.py`, `formal-problem-definition.md` §8, `testbed-architecture.md`, `01-search-protocol.md` §13, `01-search-screening-record.md` §15, `01-thesis-citation-shortlist.md` entries 50 and 56, `research-synthesis-implementation.md`, `05-thesis-structure.md` §2.4, `00-action-items.md` A6, A12, A14, A15, A16, A17, A28, A29 and A32, `00-project-phases.md`, `00-project-index.md`, `README.md`, `sources.md` #989.*

**D38 — The widened re-run of block O is screened: one more paper narrows the claim, Zhan et al. 2026 (T2, the user's ruling); no patent does; A28 survives as worded. 16 November 2026.**

**1. What ran (protocol amendment 8).** D36 item 6's re-run, which the user approved in D37. He ran it on 16 November 2026 from the run sheet Claude sent:
- R1–R6: S1, S2 and S5 on OpenAlex and Semantic Scholar;
- R7, run P1c: S1 on Google Patents, narrowed to title, abstract and claims as P1n was.

The six missing words formed a separate block O′ in place of block O, so each query returned only records carrying one of them, and records the first runs had returned were dropped. That gives the new records of a full widened run, except works added to the indexes since the first runs that carry only block O's words; the update re-run (A17) covers those. R7's first attempt was typed into the browser's address bar, and Brave Search refused it as too long; it was re-run on Google Patents from a direct link. The classification run P3b also uses block O and was not repeated, as D36 item 6 did not include it; the thesis limitation says so (`01-search-protocol.md` §13).

**2. Papers.** R1–R6 returned 53, 28, 6, 39, 22 and 4 records: 73 distinct, 45 of them returned before. Zhan et al.'s backward round (§7.4) added 55 references new to the search; its forward round found none. The 83 new records are numbered 563–645:
- T2: 1, Zhan et al. (item 3);
- related (T1): 11. The most useful to cite is Kalinin et al. 2022 (#1010): it switches a hybrid honeypot's virtual topology in energy networks by rules, from an attack-development graph and ATT&CK techniques, with no objective function;
- excluded: 71. Of the 19 from the runs, 10 use a deception word in another sense, 6 have no deception asset and 3 are not works. The 52 references excluded carry no deception asset in their titles.

*A correction:* Claude's first pass marked Spitzner (2003), one of the references, as returned by the first runs. It was not, so it is a new record, related (T1).

**3. Zhan et al. 2026 is T2, the user's ruling** (#1000).
- *What it does:* a stochastic trilevel model, reduced to one MILP with CVaR, decides which grid components to protect and where to deploy honeypots against insider-enabled load-redistribution attacks, under a protection budget, on the IEEE 14-bus system.
- *What it lacks,* so far as its abstract shows: zones and conduits, ATT&CK-grounded paths and an interception stage, and random or centrality baselines.
- *Basis:* its full text is not free (D35), so the tier rests on the abstract, read on the page the user saved. It is now one of the [n] = 11 works the thesis cites from abstracts alone.
- *Why only now:* its abstract says "smart power grids", which block O's "smart grid" does not match.
- *Not a baseline* (§11.6): a different threat model, and only its abstract is free.

**4. Patents.** P1c returned about 145 publication numbers: 43 already in the patent arm and 102 new.
- *First round:* 7 pages read; the rest judged on titles and list snippets. The user's rulings on 16 November 2026, on Claude's leans:
  - *CN 117439810 A: T1.* It assigns honeynet trap nodes to host devices to cut the honeynet's own communication cost: where the honeynet runs, not where decoys meet attackers.
  - *CN 111756687 B: T1.* It maximises survivability under a budget by allocating six kinds of defence measure, honeypots among them, per service of a power-grid information system: general defence allocation, not decoy positions.
  - *CN 122293365 A: excluded,* confirmed under §9. It conceals grid nodes and lines from physical attackers: physical grid planning, not cyber deception.
- *Second round, Claude's, after the first draft of this entry:* the first round fell short of the first arm's standard. There, round 3 opened every excluded title of run P1n naming a cyber, industrial or power subject, and the arm's only T2 at that time had come from such a neutral title (`01-search-screening-record.md` §14.4).
  - 31 more pages were opened: 18 excluded titles of that kind, and 13 related titles suggesting a strategy, a configuration, an attack path or a power-sector honeypot.
  - All 13 related stay related. Of the 18 excluded, 5 prove related (T1): honeypots as side elements in power or nuclear systems, or as a data source. The other 13 stay excluded: decoy states, optimisers named after honeypots and similar.
  - None decides positions by an objective. The nearest, CN 118484310 A, assigns honeypots to host nodes by load, the kind ruled T1 in CN 117439810 A.
- *Result:* related (T1) 32, excluded 70, T2 0, T3 0; 38 pages read (#1012–#1049). The arm counts 1,496: T2 2, related (T1) 743, excluded 751.

**5. Effect on the claim (A28).** It survives as worded. *Confidence: likely,* resting on Zhan et al.'s abstract, page summaries read through a fetch tool, and machine translation.
- The works that narrow the claim are now Park & Dagher, Dong et al. and Zhan et al., CN 122339846 A/B and CN 121012683 A.
- Budgeted, formally optimised decoy placement in a power grid now has two papers, Dong et al. and Zhan et al. D36 already ruled out any claim to be first there.
- No work found combines IEC 62443 zones and conduits as numeric inputs, a scored interception stage along ATT&CK-grounded attack paths, and validation against random and centrality baselines.

**6. What else it shows.**
- *The gap was real:* the one work that narrows the claim was returned only through the new words.
- *The title rule's exclusions are again unsafe* (D36 item 8): 5 of the 18 opened proved related, though none proved T2.

**7. Record-keeping.**
- `01-search-protocol.md`: amendment 8 (§4, §8) and the limitation (§13), with its old wording kept;
- `01-search-screening-record.md`: §18 (new), its header and notes on the totals and limitations;
- `sources.md` #990–#1049: the amendment, the runs, the citation rounds, the outcome, the T2, the kept papers and every patent page read; update lines on #623 and #642;
- `01-thesis-citation-shortlist.md`: entry 57, Zhan et al.;
- `research-synthesis-implementation.md`'s landscape table and `05-thesis-structure.md` §2.4;
- `00-action-items.md` A17, A28 and A29;
- `00-project-phases.md` and `00-project-index.md`.

**8. Effect.** None on any input, card or number. Only Markdown files in `docs/` change.

*Status: the user's rulings, 16 November 2026; the rest of the screening is Claude's first pass, which he can question before the freeze. Searching for A17 and A29 closes here, apart from the update re-run within a month of submission (A17). Reference: `01-search-screening-record.md` §18, `01-search-protocol.md` §4, §8 and §13, `sources.md` #990–#1049.*

**D39 — The user's pre-registration for Phase D (A15), adopted before any Phase D run. Drafted by Claude on 17 November 2026 and corrected after an independent review on 18 November; adopted by the user on 18 November 2026.**

This entry is committed before any leave-one-path-out or attack-simulation result exists on the testbed. `scripts/evaluate.py` cannot produce one yet: it refuses to run until the freeze.

**1. What I accept in advance.** A negative or mixed result, reported honestly, is an acceptable outcome of this project. I will report the results as they come out, and I will not change any input, weight, rule, definition or method after seeing them. A defect is code that does not do what this entry and `03-evaluation-methodology.md` §2–§5 state. Its fix changes no rule, input or definition; it gets its own entry stating its effect on every verdict, and a new freeze. Both runs are reported, and the corrected run is the result.

**2. The question** (proposed by Claude and accepted by me as worded, 16 November 2026, D37): On the modelled testbed, does choosing decoy positions by the composite objective F — found by greedy and confirmed exact by MILP — catch attacks the optimiser was not given, at least as often and as early as betweenness-centrality placement, random placement and a coverage-only optimiser, at equal budget? The attacks are each attack path when it is held out of the optimisation, and simulated attack routes from every non-controller foothold to every objective. Results are also reported against the D20 wording (`formal-problem-definition.md` §8), with D24's caveat that its first clause follows from optimality.

**3. The test.** Default weights (1, 1, 1, 1, 0.1); budgets B = 1, 2, 3 and 4.
- *A comparison holds* at a budget when greedy is not below its comparator by more than 10⁻⁹ (absolute; `TOL` in `scripts/evaluate.py`). A smaller difference is a tie, and a tie holds.
- *H1, held-out interceptions:* each attack path is left out of the optimisation in turn, and I count how many of the five held-out paths the placement chosen from the other four still catches. Greedy against centrality, and against the mean of the 30 random placements.
- *H2, simulated detection rate and earliness, primary population:* greedy against centrality, and against the mean of the 30 random placements.
- *H3, simulated detection rate, earliness and held-out interceptions:* greedy against the coverage-only optimiser, averaged over all of its tied best placements.
- *Verdicts:* at a budget, a hypothesis holds if every one of its comparisons holds there. It is supported if it holds at all four budgets, not supported if it holds at none (even where some of its comparisons hold), and mixed otherwise. Every verdict is reported with its wins, ties and losses, and a supported verdict with no win is labelled "supported (ties only)". I report the three verdicts separately and do not combine them into one score.
- *What answers the question:* H1–H3 together. On held-out paths only interception is tested; held-out earliness and criticality-weighted protection are reported as counts.

**4. Definitions.** Terms not defined here mean what `03-evaluation-methodology.md` §2–§4 say, as committed with this entry; the frozen code computes them.
- *Primary population:* the footholds are the seven assets other than the Attacker node and the three controllers, and the objectives are every controller and every path target. Routes are loop-free, at most one hop longer than the shortest, and use the recorded connections in either direction, never through the Attacker node. Each reachable foothold–objective pair weighs the same, and its routes share that weight equally. A pair whose foothold is its objective is skipped, and an unreachable pair carries no weight.
- *Detection:* a route is detected at its first decoy, the foothold included. Earliness is (n − k)/(n − 1) for a route of n assets detected at its k-th, and 0 if it is not detected.
- *How the comparators enter:* centrality and random do not read the paths, so they place the same decoys in every fold. The coverage-only optimiser's tied best placements are recomputed on the four training paths of each fold and averaged there. Random is 30 placements drawn with seed 42, judged by their mean. The comparators always place exactly B decoys; greedy places fewer when no further decoy raises F.
- *The candidate set:* every fold keeps the reviewed set L. Filter 1 derived it with all five paths, so a fold's L can still hold assets that lie only on its held-out path: for P3, the OT Firewall and Engineering WS-2. Greedy never places such an asset, because it raises no term of F on the training paths; centrality, random and the coverage-only optimiser can.
- *Greedy and the MILP:* greedy's own placement is what H1–H3 judge, in every cell and fold. A run in which the MILP scores below greedy on the same paths is void (D24). After the run, the F of greedy's and the MILP's placements in every cell and fold, and whether any other placement reaches greedy's F, are computed from the results file with the frozen `metrics.score`. Any case where greedy is not the unique optimum is reported beside the verdicts.

**5. How Phase D runs.** On a database rebuilt from the frozen seed with the committed review restored; the results entry records that an export from it equals `data/review/plausibility_review.csv` byte for byte. The command is `uv run python scripts/evaluate.py --json data/results/phase-d.json`, and the results file is committed with the results. Wins, ties and losses, and every count the script does not print, are tallied from that file by the same 10⁻⁹ rule.

**6. Also reported, as counts:** every comparison over all 20 cells of the declared grid; the simulation at zero and two extra hops and from the documented entry points; the coverage-only greedy form; criticality-weighted protection and detection before the objective; and the F-based grid, the weight sweep and the structure check, as before. Greedy never losing on F follows from its optimality here, so I do not present it as evidence that F is a good objective.

**7. What I expect, before running** (`03-evaluation-methodology.md` §7, as corrected with this entry):
- *Documented entry points:* greedy at B = 3 holds all three, so it should catch every route there at its first step. That population is reported but not counted toward H2.
- *Primary population:* H2 is at risk. Routes that start at the HMI, the Historian, Engineering WS-2 or the Backup Control Switch do not start at any of P's entry assets, so a placement of those assets cannot catch them at their foothold. Centrality favours assets that many shortest paths of the recorded network cross, so it may detect more routes there than greedy does.
- *Leave-one-path-out:* holding out P1 or P4 leaves the Engineering WS on the other path, and holding out P2 or P5 leaves the DMZ Jump Host on the other, so those four are expected to be caught at the held-out path's first step whenever the budget lets greedy keep those assets. P3 is the only path through the OT Firewall and Engineering WS-2, so with P3 held out greedy cannot catch it at any budget (item 4, the candidate set); the comparators can.
- *The route OT Firewall → Engineering WS-2 → PLC-02:* caught only by a placement holding the OT Firewall (greedy holds it only from B = 3) or Engineering WS-2.

**8. The explanation layer (secondary question).** Greedy's placement at B = 1–4 under the default weights, explained by `qwen3:4b` (Q4_K_M) at temperature 0 with thinking off. The prompt, the model tag and both checks are committed before the four counted explanations are generated, and "first try" means the first generation after that commit. I report how many passed both automatic checks on the first try, the failures by kind, and how long each took on my laptop. I rate the four as clear, partly clear or unclear for a reader new to the project, reported as counts. This is a small check, not a user study. *[D43, 24 November 2026: the model tag is now `qwen3:4b-q4_K_M`, on my choice, before any counted explanation; the tag `qwen3:4b` is a thinking-only model.]*

**9. Next.** The freeze (`scripts/freeze.py`) follows this entry, then Phase D. Its results get their own entry, whichever way they go.

**10. Made with this entry** (record-keeping; no rule, input or code changes):
- `03-evaluation-methodology.md`: §3's detection-rate wording states its weights; §5's verdict rule and tolerance are stated as `scripts/evaluate.py` applies them; §6 and §8 carry items 8 and 5's run rules; and §7 is corrected in two places, with the old wording kept in notes. It said such routes "pass none of P's entry assets", which is false, since the Historian connects to the OT Firewall and Engineering WS; and it said greedy would miss held-out P3 "unless spare budget or Engineering WS-2 covers it", which greedy's stopping rule rules out.
- `formal-problem-definition.md` §8: it called the research question "the user's wording"; it was proposed by Claude and accepted by the user as worded.
- `00-action-items.md`: A15 is done (its note planned the user's own wording, and he adopted this text instead); the A12 and A32 notes, stale since D38. `00-project-phases.md`.
- An independent review, by a separate agent that had not seen the draft written, checked it against the methodology and the code on 18 November 2026. Claude verified each finding against the code; all twelve are reflected above.

*Status: drafted by Claude, the project's AI assistant, on 17 November 2026, restating `03-evaluation-methodology.md` §5 and §7; corrected on 18 November 2026 after the independent review; read and adopted, unedited, by Naitik as his pre-registration on 18 November 2026, before any Phase D run. Reference: `03-evaluation-methodology.md` §2–§8, `scripts/evaluate.py`, `src/evaluation/`, D24, D32, D37, D38, `00-action-items.md` A15.*

**D40 — The evaluation inputs are frozen: `data/freeze/manifest.json` holds the SHA-256 of the 19 files that feed Phase D, at commit `bc93d85`. Every check, re-run on a fresh clone, reproduces D33 exactly. Against D25, greedy's record against centrality rises from 5 to 16 wins, §8's clause 2 falls from 20 to 18 of 20, and the instance is no longer modular. No input or code changes. 19 November 2026.**

**1. What is frozen.** `scripts/freeze.py` (D37) wrote the manifest on a fresh clone of `bc93d85`, the D39 commit, with a clean working tree. It lists the files of `03-evaluation-methodology.md` §8:
- `requirements.lock`;
- `data/schema.sql`, `data/seed.sql` and `data/review/plausibility_review.csv`;
- the eleven Python files of `src/graph_model/`, `src/optimizer/`, `src/evaluation/` and `src/plausibility/`;
- `scripts/evaluate.py`, `sweep.py`, `run_comparison.py` and `structure_check.py`.

`scripts/evaluate.py` refuses to run if any of them differs from the manifest. The manifest is committed with this entry (2,077 bytes, SHA-256 `6b0626391ccb…`). None of these files has changed since `7c88be5`, where D37 item 8 last reproduced D33, except `src/evaluation/` and `scripts/evaluate.py`, which were new in `400e17a` and are unchanged since.

**2. How it was checked** *(verified, 19 November 2026)*.
- `uv run scripts/setup.py` built the pinned environment on the fresh clone (Python 3.13.18, every package as in `requirements.lock`, Node.js v24.19.0 from `.venv`) and a database from the frozen schema and seed.
- `review_io.py check` passed, and `restore` restored the 10 confirmed cards. An export with `--require-complete` (10 of 10 confirmed, 9 pass Filter 1) equals the committed `data/review/plausibility_review.csv` byte for byte (SHA-256 `f61f51ab4cfd…`).
- `check_frozen`, imported from `scripts/evaluate.py` without running it, accepts the manifest. `scripts/evaluate.py` was not run.

**3. Every check re-run on that database.** Each output matches D33 item 4 exactly.
- *`run_comparison.py 3`:* greedy, distorted greedy and the MILP place the DMZ Jump Host, Engineering WS and the OT Firewall (F 2.4175). Centrality places the DMZ Jump Host, Engineering WS-2 and the OT Firewall (1.2060), and random placements average 1.3229.
- *`sweep.py --sens`:*
  - against centrality, 16 wins (10 swap, 6 decline) / 4 ties / 0 losses, resting on 6 distinct placement disagreements;
  - greedy equals the exhaustive optimum in 20 of 20 cells;
  - the MILP is exact in all 20, and in all 84 sampled configurations. The smallest rounding margins are 17,426 units on the grid and 15,074 in the sample, against bounds of 19 and 20;
  - distorted greedy is below greedy in 0 of 20;
  - §8's clause 2 holds in 18 of 20. It fails at B = 1, δ = 3 (a swap) and at B = 4, δ = 3 (a decline).
- *`structure_check.py`:* F is submodular and not monotone (1,104 violations). Distorted greedy's preconditions hold, and the gain part g is not modular (1,584 violations).
- *`evaluation_selftest.py`:* passes on its toy network, the only network it reads.

**4. The close cell, re-measured as D33 item 6 required.** At B = 1, δ = 3 greedy places Engineering WS (F 0.7265) and centrality the DMZ Jump Host (0.7091), a lead of 0.0174.
- *Method:* each declared input below was varied alone, in memory only, on the frozen code. Crit was recomputed by `compute_criticality`, greedy and centrality were run at B = 1 with weights (1, 1, 1, 3, 0.1), and a bisection found the value at which greedy's lead falls within 10⁻⁹.
- *The RTU's process share,* s, with PLC-01 and PLC-02 at (1 − s)/2 each: the lead reaches zero at s ≈ 0.491. The declared share is 1/3.
- *The OT DMZ's SL,* t, set as seven equal SL-T cells of 4t: the lead reaches zero at t ≈ 0.463. The declared SL is 0.607.
- Past either value greedy places the DMZ Jump Host, the cell becomes a tie, and clause 2 holds there. A scan of each range at 201 points found no other crossing.

*Against D33's figures.* D33 quoted "about 0.62–0.69" and "about 0.31–0.35". The combined review computed them on the slate's values, before the edge-level ConduitSL, and D33 expected the thresholds to be lower now.
- The share's threshold is lower, as expected.
- The SL's is higher, so a smaller fall flips the cell. Read literally, D33's expectation was wrong for it.
- Both now lie nearer the declared values, so the cell is more fragile than D33's figures said.
- The review's method is not recorded in the repository, so how much of the difference comes from method rather than inputs is *unconfirmed*.

**5. The effect against D25** (D31 item 8; `03-evaluation-methodology.md` §8). D25's numbers were recorded on 30 September 2026. Every D25 number in the table below was reproduced today at commit `ebcaaa4` with `--legacy-d25`, except the fragility row's threshold, which is quoted from D25's text.

*What changed in between.* Each change had its own entry, which stated its effect at the time.
- *L:* five seeded candidates that bypassed Filter 1 (the DMZ Jump Host, the Historian, Engineering WS-2, the HMI and PLC-02) became the nine that passed the review (D26, D30, D31), with five new Filter 2 scores (D31).
- *P and E:* P5 was added (D27), two step labels changed (D28), four connections were added (D30), and each path got an explicit target (D33, A36).
- *F's inputs, all D33:* unweighted betweenness (A35); declared SL-T vectors and process shares (A37); the edge-level ConduitSL (A38); Crit's additive form (A40); Engineering WS-2's risk, raised under A43; and Early's (n − s)/(n − 1) endpoint.
- *Unchanged:* the defaults of α to ε, K = 4, the five methods and the 20-cell grid.

| | D25 | Frozen inputs | Which way it cuts |
|---|---|---|---|
| Instance | 5 candidates, 4 paths. g is modular: no path meets two candidates | 9 candidates, 5 paths. g is not modular: all five paths meet two or more | For the method: greedy equalling the optimum is now a finding for this one instance, not a construction (D25's claim rule) |
| B = 3, default weights | All four methods place the DMZ Jump Host, Engineering WS-2 and the Historian (F 1.2170); random mean 0.8942 | Greedy: the DMZ Jump Host, Engineering WS and the OT Firewall (2.4175). Centrality: the DMZ Jump Host, Engineering WS-2 and the OT Firewall (1.2060). Random mean 1.3229 | The methods now disagree at the headline budget. F values are not comparable across the two columns, because F's inputs and Early's endpoint differ |
| Grid against centrality | 5 wins (5 swap, 0 decline) / 15 ties / 0 losses, on 2 distinct disagreements | 16 wins (10 swap, 6 decline) / 4 ties / 0 losses, on 6 | For the method on its face. But 0 losses is implied by optimality in both columns, so the count measures disagreement, not whether F is a good objective |
| §8's clause 2 | 20 of 20 | 18 of 20 | Against the method |
| Greedy = exhaustive optimum | 20 of 20, by construction | 20 of 20 | — |
| MILP exact | 20 of 20, and all 68 sampled configurations | 20 of 20, and all 84 sampled | — |
| Smallest rounding margin | 3,826 units (bound 16); 413 in the sample (bound 17) | 17,426 (bound 19); 15,074 in the sample (bound 20) | Wider: the exactness checks sit further from rounding |
| Distorted greedy below greedy | 3 of 20, all at δ = 3 | 0 of 20 | Reported, not claimed: one instance says nothing about the guarantee's value in practice |
| F's structure | Submodular, not monotone (16 violations) | Submodular, not monotone (1,104) | — |
| Fragility | δ = 3 sits just below the first decline threshold (the HMI's, at 3.025) | The close cell's lead is 0.0174 (item 4) | Both depend on where the declared values sit |

*Overall.*
- On F, the proposed method's standing against centrality is stronger than at D25: more wins, on more distinct disagreements, on an instance that is no longer trivial.
- Clause 2 is weaker, and the close cell is fragile.
- None of this is a Phase D result. On F greedy cannot lose here, because it is optimal (D24; D39 item 6). Every change since D25 was made with D25's numbers known, and D33's with D31's known too (D33 item 1).
- The research question is answered by H1–H3, on held-out paths and simulated routes. No held-out or simulation result on the testbed existed when any of these inputs was chosen.

**6. What the freeze means from now.** Each point follows from rules already recorded; none is new.
- No frozen file changes before Phase D runs. A change needs its own entry stating its effect, and a new freeze. A defect is handled as D39 item 1 states.
- A method found by the update re-run (A17) can no longer become a Phase D baseline. Neither can Park & Dagher's rule, which D37 item 4 left open until the freeze. Either would be related work, or a separately reported study after Phase D (D37 item 7), as tuning is.
- The explanation layer (A6) is not an evaluation input (D37 item 6). It is built outside the four frozen packages, so building it changes no frozen file.

**7. Made with this entry** (record-keeping; no input or code changes).
- `03-evaluation-methodology.md` §8: step 3 is marked done.
- `00-action-items.md`: A12, A16, A20, A29 and A32 are marked done. A20 had been done since D31, A12 and A16 since D37 (with A12's rules fixed by D39), and A29's searching since D38, but their IDs were not struck. A32 closes with this entry. A11's row has had one cell too many since before D37; it is repaired, and its words are kept.
- `00-project-phases.md`: a D40 update, and notes on the overview and Phase D.
- `README.md`: the data row names `data/freeze/`. The line calling D33's run pre-freeze gets a note, and so does the line saying five inputs are still open, which has been stale since D33.
- `formal-problem-definition.md` §4: the same "pre-freeze" line, stale since D33, gets a note.
- `00-repository-structure.md`: `data/freeze/` is added. The file also put Phase D's outputs in a top-level `/results`, while D39 item 5 fixed the results file at `data/results/phase-d.json`. The D39 batch missed this; a note now says D39 governs.
- D33 item 6: an inline note gives the re-measured thresholds.

*Now stale, for the next documentation pass:*
- `02-system-flow.md` §8 says "§7.3 continues as A12, which now gates Phase D"; A12 is done.
- `05-thesis-structure.md`'s priority list, item 3, says Phase D is gated on A32, A35–A38, A40, A12 and A15; all are done.
- `03-honest-review.md` says a re-run of the OT keywords is recommended before the freeze; D38 made it.

**8. Next.**
1. Phase D, on a fresh clone of the pushed commit, as D39 item 5 states. Its results get their own entry, whichever way they go.
2. The explanation layer (A6).
3. The TA-2 presentation.

*Status: Claude's work on the user's instruction of 19 November 2026 to start the freeze, which D39 item 9 put next; verified as in items 2–5. Not independently reviewed. Reference: `data/freeze/manifest.json`, `scripts/freeze.py`, `scripts/evaluate.py`, `03-evaluation-methodology.md` §8, D24, D25, D31, D33, D37, D39, `00-action-items.md` A12, A16, A20, A29 and A32, `00-project-phases.md`, `README.md`, `formal-problem-definition.md` §4, `00-repository-structure.md`.*

**D41 — Phase D, run once as pre-registered: H1, H2 and H3 are all mixed. The composite objective's placement holds every comparison at a budget of two decoys. It fails at four, where it places three decoys against the comparators' four, and on held-out paths at one. Greedy is the unique F-optimum in all 120 cells and folds. No input, code or rule changes. 19 November 2026.**

**1. The run.** On a fresh clone of `b43de49` (D40), as D39 item 5 states:
- `uv run scripts/setup.py` built the pinned environment (Python 3.13.18) and a database from the frozen schema and seed. The committed review was restored (10 cards, 9 pass Filter 1), and an export equals `data/review/plausibility_review.csv` byte for byte.
- `uv run python scripts/evaluate.py --json data/results/phase-d.json` ran once, at 17:17 UTC, in 2.3 seconds. Every frozen file matched the manifest (`bc93d85`). The results file (SHA-256 `3081026ed338…`) is committed with this entry.
- Every win, tie and loss was re-counted from the results file by the 10⁻⁹ rule, separately from the script's own tallies. The two agree exactly.

**2. The verdicts** (default weights, B = 1 to 4; the rules of D39 item 3).

| Hypothesis | Holds at | Verdict | Wins / ties / losses |
|---|---|---|---|
| H1: held-out interceptions, against centrality and random | B = 2, 3 | mixed | 4 / 0 / 4 |
| H2: simulated detection and earliness, against centrality and random | B = 1, 2 | mixed | 9 / 2 / 5 |
| H3: the same two, and held-out interceptions, against the coverage-only optimiser (ties averaged) | B = 1, 2 | mixed | 6 / 3 / 3 |

*By budget:*
- *B = 1:* H1 fails. Greedy catches 0 of the 5 held-out paths; centrality catches 2, and random 1.43 on average. In the simulation greedy ties centrality, which places the same decoy, and beats random and the coverage-only optimiser.
- *B = 2:* all three hold. Greedy catches 4 held-out paths, against 3, 2.53 and 0.75. Its detection (0.555) and earliness (0.439) equal or exceed every comparator's.
- *B = 3:* H1 holds, with 4 against 3, 3.47 and 1.67. H2 and H3 fail on detection only: 0.692, against random's 0.716 and the coverage-only optimiser's 0.710. Greedy's earliness, 0.583, is the highest.
- *B = 4:* none holds. The one comparison greedy wins there is held-out paths against the coverage-only optimiser (4 against 3.03). Centrality catches all 5 held-out paths and detects 0.779; random catches 4.10 and detects 0.826.

*The answer to the research question* comes from H1–H3 together (D39 item 3), so it is mixed. At equal budget, F's placement caught unseen attacks at least as often and as early as every comparator at a budget of two. It did not at four, and not on held-out paths at one.

**3. What drives the verdicts.** The facts here are verified from the placements in the results file.
- *B = 4:* greedy's placement is its B = 3 placement, in every weighting and every fold. At the default weights its three decoys already catch all five paths at their first step. A fourth decoy raises no gain term and adds Risk and Cost, so greedy stops. The comparators always place B (D39 item 4), and their fourth decoy catches more: centrality's includes Engineering WS-2, which catches held-out P3.
- *B = 1:* when P1 or P4 is held out, the single decoy goes on the DMZ Jump Host, the entry of P2 and P5. When P2 or P5 is held out, it goes on the Engineering WS, the entry of P1 and P4. When P3 is held out, it goes on the DMZ Jump Host. No held-out path is caught. That paths share entry assets was named in advance as a limit of the test (`03-evaluation-methodology.md` §2).
- *Earliness and detection:* greedy's decoys sit on P's entry assets, so routes that start there are caught at their first step. Routes from the HMI, the Historian, Engineering WS-2 or the Backup Control Switch are caught only if they pass one of those assets. F credits only the modelled paths, so once P is covered it sees no value in reaching more routes. *(That this is the main mechanism is Claude's reading, likely.)*

**4. The expectations of D39 item 7, against the outcomes.**
- *Documented entry points:* confirmed. Greedy detects every route there at its first step at B = 3 and 4 (1.00 detection and earliness).
- *Primary population:* H2 was at risk, and it is mixed. Centrality detected more routes than greedy only at B = 4. Random detected more at B = 3 and 4, which was not stated in advance.
- *Leave-one-path-out:* confirmed at B = 2 to 4. P1, P2, P4 and P5 are caught at their first step, and P3 never. At B = 1 the budget cannot hold both entry assets, so none is caught. Item 7's condition, "whenever the budget lets greedy keep those assets", covers this, but the zero itself was not stated in advance.
- *The route OT Firewall → Engineering WS-2 → PLC-02:* confirmed. Greedy catches it at its foothold from B = 3, and centrality from B = 2.

**5. The post-run checks of F (D39 item 4).** With the frozen `metrics.score`, in all 20 cells and 100 folds:
- greedy's placement has the best possible F;
- no other placement of at most B candidates reaches that F, so greedy is the unique optimum everywhere and no exception needs reporting;
- the MILP placed the same decoys as greedy in all 120 and is never below it, so no run is void (D24).

Distorted greedy differed from greedy in one fold: B = 3 under δ = 3, with P5 held out.

**6. Also reported, as counts** (D39 item 6; in full in `03-phase-d-results.md` §5 and §7).
- *All 20 cells, greedy's wins / ties / losses* on held-out interceptions, then simulated detection:
  - against centrality, 7/3/10 and 9/4/7;
  - against random, 9/0/11 and 10/0/10;
  - against the coverage-only optimiser, 14/5/1 and 5/5/10.

  On earliness: centrality 7/3/10 and 9/4/7, random 14/0/6 and 14/0/6, and the coverage-only optimiser 15/5/0 and 9/5/6.
- *Slack 0 and slack 2:* greedy's losses again fall at B = 3 and 4. *Documented population:* greedy never loses.
- *The coverage-only greedy form:* greedy never loses to it. It places the same decoys as greedy on all five paths, and greedy wins on held-out paths at B = 2 to 4.
- *Criticality-weighted protection of held-out paths:* greedy loses to centrality at B = 1 and 4, and to random at B = 1. *Detection before the objective:* it loses to centrality and to random at B = 4.
- *The F-based grid, the weight sweep and the structure check,* re-run on the Phase D database: their output equals D40's byte for byte.
- *The D20 wording:* clause 1 holds by optimality. Greedy's F is above the random mean in all 20 cells; against centrality it is higher in 16 and equal in 4, where centrality places the same decoys. Clause 2 holds against centrality in 18 of 20.

**7. No defect was found** (D39 item 1). The re-count matches the script's verdicts and tallies exactly, and every post-run check passes.

**8. What the thesis may claim** is set out in `03-phase-d-results.md` §10, for this one modelled network.
- *It may report:* the pattern by budget above, and that greedy found the unique best F everywhere, confirmed by the MILP.
- *It may not claim:*
  - that F's placements catch unseen attacks better than the baselines in general;
  - anything statistical;
  - that a larger budget improves F's placements, since greedy places at most three decoys under the default weights.

**9. Made with this entry** (record-keeping; no input, code or rule changes).
- `data/results/phase-d.json`: the results file (D39 item 5).
- `03-phase-d-results.md`, new: the results in full, written for a reader new to the project. Category Evaluation, 💾 Offline, registered in `00-project-index.md`.
- `03-evaluation-methodology.md` §8: steps 4 and 5 are marked done.
- `00-project-phases.md`: a D41 update, and notes on the overview and Phase D. Phase D's primary question is answered; its secondary question, the explanation layer's four counted explanations, remains.
- `00-action-items.md`, A28, and `research-synthesis-implementation.md`'s statement of the claim: item 10's change.
- `README.md`: a Phase D section, and the data row names `data/results/`.
- `00-repository-structure.md`: `data/results/` in the layout.

**10. The novelty claim's validation clause (A28): the user's choice, 19 November 2026.** The draft claim ended "validated against random and centrality baselines". With the verdicts mixed, "validated" could read as "shown to be better than". The user chose "evaluated against random and centrality baselines". The clause still names the baselines that the prior-art search checked (D35, D36, D38), and the rest of the draft is unchanged.
- *Disclosure:* the wording was chosen after seeing these results. It weakens the claim, and it changes no input, rule or result.
- `03-commercial-prior-art-analysis.md` and the archival `03-honest-review.md` quote older wordings of the clause ("validated against baseline placement strategies", "validated against baselines"). Their analysis does not depend on the verb, so they are left as they are.

**11. Next.**
1. The explanation layer (A6). Its prompt, model tag and checks are committed before the four counted explanations are generated (D39 item 8).
2. The TA-2 presentation.

*Status: Claude's run of Phase D on the user's instruction of 19 November 2026, after the D40 push. The verdicts are the output of the pre-registered rules; item 3's reading of the mechanism is Claude's; item 10 is the user's choice. Not independently reviewed. Reference: `data/results/phase-d.json`, `03-phase-d-results.md`, `scripts/evaluate.py`, `03-evaluation-methodology.md` §2–§8, D24, D37, D39, D40, `00-action-items.md` A28.*

**D42 — The explanation layer (A6) is built, and its rules are fixed before the four counted explanations. The prompt, the declared model (`qwen3:4b`, Q4_K_M, temperature 0, thinking off) and the two checks are in `src/explain/`, committed with this entry, as D39 item 8 requires. It was tested against a stand-in model only; the real model runs on the user's laptop. No input, frozen file or result changes. 21 November 2026.**

**1. What is built.**
- `src/explain/` (new) builds the facts and the prompt, asks the model once, checks the text, and falls back to a template. It sits outside the four frozen packages and only reads them.
- `POST /runs/{id}/explain` (the API's eleventh endpoint) explains a stored run of the proposed method. Each explanation served goes into the `explanations` table, which the schema has had since Phase B, so the frozen schema does not change.
- Screen 1 gains an *Explain this placement* button. The panel shows the model's text with a line saying it was checked, or the template with the reason.
- `scripts/explain_counted.py` has three commands: `check`, `run` (the counted run, once) and `rate`.
- `scripts/explain_selftest.py` runs 37 checks against a stand-in Ollama server.

**2. The facts the model is given,** for a placement at budget B:
- the network's counts (9 candidate positions, 5 attack paths) and the weights;
- what F rewards and penalises, in words;
- the budget, the placement and its six scores;
- each path it catches, with the step, the path's length, the catching asset and the path's target;
- the paths it misses, by label only;
- the number of baselines (2), centrality's placement, scores and caught paths, and the mean scores of the 30 random placements (seed 42).

The comparators are computed with the frozen baselines, and every score is given to two decimals. When greedy or the MILP places fewer than B decoys, one sentence says that no further decoy raises F.

**3. The prompt.** The system prompt keeps `02-ai-role.md` §4's guardrail: explain the placement, never suggest another. It adds four rules that the checks enforce:
- use only the facts;
- write every number as digits, exactly as given;
- do not calculate, convert to percentages or round differently;
- name only assets that appear in the facts.

The task asks for under 150 words on three points: the locations and the paths each catches, how early, and the comparison with the two baselines. The exact text is in `src/explain/__init__.py`.

**4. The two checks, made exact.** These implement `03-evaluation-methodology.md` §6.
- *The number check.*
  - The numbers in a text are its numerals and the number words zero to twenty and thirty. Ordinals ("first step") are not counted.
  - Digits inside asset names (PLC-01), path labels (P1–P5), ATT&CK technique IDs and "IEC 62443" are not numbers.
  - A number passes if, rounded to two decimals (half up), it equals a number of the facts rounded the same way.
- *The asset check.*
  - An asset is named when its recorded name appears as a whole word, in any case, matched longest first, so that "Engineering WS-2" is not read as "Engineering WS". For "PLC-03 (RTU)", "PLC-03" and "RTU" count too.
  - The Attacker node is not an asset.
  - A named asset passes if it is in the placement or in centrality's placement, or lies on an attack path through either. The facts name no random placement, so random adds no allowed asset.
- *What replaces a text.* A text that fails either check, is empty, or does not arrive (an error or a timeout) is replaced by the template. The template is built only from the facts' numbers and names, and the self-test confirms that it passes both checks in all 20 cells of the declared grid.
- *Thinking.* A thinking trace in a reply is recorded as a deviation from the declared settings. The text is still judged by the two checks alone. *[D43: a trace in the text closed by `</think>` alone now counts too.]*

**5. The settings.**
- *Model and decoding:* `qwen3:4b` *[D43: `qwen3:4b-q4_K_M`]* with `think: false`; temperature 0, seed 0, a 4,096-token context and at most 512 tokens out.
- *One try:* one request per explanation, never retried.
- *Sources:* the Ollama API fields come from its documentation (#1050, #1051, #1053). Its `/api/show` page could not be fetched (#1052), so `check` prints what the user's own Ollama reports.

**6. How the counted run is kept a first try (D39 item 8).**
- *`run` refuses* if `data/results/explanations.json` exists, if `src/explain/` or the script has uncommitted changes, if a frozen file differs from the freeze manifest, or if Ollama is not ready.
- *`run` records* the commit, the Ollama version and the model's digest and quantization. It writes after each explanation, so no first try can be lost.
- *`check` generates no explanation.* Its one warm-up request asks for a single word.
- *The API holds back.* Until the counted record exists, it serves the template without calling the model, so the Explain button cannot use up a first try.
- *What "first try" means:* the first generation for each of the four placements after the commit of this batch.

**7. What the user does next** (`04-setup-guide.md` §7, new).
1. Install Ollama on the Windows host and `ollama pull qwen3:4b` *[D43: `ollama pull qwen3:4b-q4_K_M`]*. Make it reachable from the Kali VM, and set `IDECOP_OLLAMA_URL` there.
2. Run `uv run python scripts/explain_counted.py check` until it says READY.
3. Run `run`, once. Then run `rate`, judging the model's own four texts as clear, partly clear or unclear.
4. Commit `data/results/explanations.json`. D43 records the counts. *[D43: D44 records them; D43 amends the model first.]*

**8. Verified, and not.**
- *Verified on 21 November 2026, on Linux:*
  - the 37 self-test checks;
  - `check`, `run` and `rate` end to end against the stand-in, with every refusal;
  - Screen 1 in Chromium, in three states (before the counted run, a passing text and a failing text), and for a baseline's run;
  - the frontend build;
  - `check_frozen`, which still passes.
- *Not verified:* a real model's output, Ollama on Windows, and the route through VMware's network. The user's `check` and counted run test them.

**9. Effect.** No input, rule, result or frozen file changes, and the freeze check passes. The explanation layer is not an evaluation input (D37 item 6).

**10. Made with this entry** (record-keeping).
- `03-evaluation-methodology.md` §6 points here for the exact rules.
- `02-ai-role.md` Part A gets notes on the model, the input, the prompt, output handling and evaluation.
- `02-prototype-architecture.md` gets notes on its module list, routes and run commands.
- `04-setup-guide.md` gains §7 and troubleshooting rows, and its note on Ollama is updated.
- `02-data-model.md`'s route table and `00-glossary.md`'s Phi-4-mini entry get notes.
- `README.md`: the layout, the endpoint count and *Running it*.
- `00-action-items.md` A6 and `00-project-phases.md`.
- `sources.md` #1050–#1053, and `00-project-index.md`'s source count.

*Now stale, for the next documentation pass:*
- `02-system-flow.md` says "Not yet built: the explanation layer" and lists `POST /runs/{id}/explain` as not built.
- `05-thesis-structure.md`'s row 4.7 reads "pending build".

**11. A correction.** On 19 November Claude told the user that "D42 records the counts". The counts go to D43. *[D43: now D44, because D43 amends the model first.]* D42 fixes the prompt, the model and the checks before them, as D39 item 8 requires.

*Status: Claude's build, on the user's instruction of 21 November 2026 to continue after the D41 push. Not independently reviewed. Reference: `src/explain/`, `scripts/explain_counted.py`, `scripts/explain_selftest.py`, `src/api/main.py`, `src/frontend/src/Dashboard.jsx`, `03-evaluation-methodology.md` §6, `02-ai-role.md`, `04-setup-guide.md` §7, D37 item 6, D39 item 8, `00-action-items.md` A6, `sources.md` #1050–#1053.*

**D43 — Before the four counted explanations, the declared model becomes `qwen3:4b-q4_K_M`. The tag `qwen3:4b` that D37 and D39 named is a thinking-only model, so "thinking off" could not hold. A pre-run amendment of D39 item 8, on the user's choice; no explanation had been generated. 24 November 2026.**

**1. What was found.**
- *The readiness check refused.* On 24 November 2026 the user ran `scripts/explain_counted.py check` in the Kali VM, against Ollama 0.40.17 on the Windows host. It reported: "qwen3:4b cannot switch thinking off (its thinking values are [True])". On the laptop, `ollama show qwen3:4b` gave thinking levels `true` only, default `true`, a context length of 262144, quantization Q4_K_M, and a digest beginning `359d7dd4bcda`.
- *The tag.* Ollama's list of qwen3 tags (`sources.md` #1059, read 24 November) gives `qwen3:4b`, `qwen3:4b-thinking` and `qwen3:4b-thinking-2507-q4_K_M` one ID, `359d7dd4bcda`: Qwen3-4B-Thinking-2507, 2.5 GB, 256K context. `qwen3:4b-q4_K_M` has its own ID, `2bfd38a7daaf`: 2.6 GB, 40K context.
- *The warm-up.* Asked for one word with thinking off, the model wrote its reasoning into the reply text, ending in `</think>` with no opening tag, then "OK". That one-word request is the only generation so far. No explanation exists.

**2. How the error arose.** D37 item 6 chose `qwen3:4b` from its registry page (#989): parameters, quantization and download size. It assumed the tag could switch thinking off, as D26's Qwen3-14B could. The page's "thinking and non-thinking modes" describes the qwen3 family, not this tag, and the 2.5 GB that D37 recorded is the thinking-only model's size. Claude re-read the page on 21 November and did not catch it either. D42's readiness check, built to refuse such a model, caught it before any counted generation.

**3. The amendment.** The user chose on 24 November 2026, from four options Claude set out.
- *Chosen:* `qwen3:4b-q4_K_M`.
  - It has thinking and non-thinking modes, so `think: false` holds.
  - It is the model D37 described: the same generation, and the same non-thinking greedy decoding, as D26's Qwen3-14B.
  - That it is the original Qwen3-4B of April 2025 is inferred from its 40K context and its own ID; the tag list does not say so.
  - On the user's laptop on 25 November, `ollama show qwen3:4b-q4_K_M` reported thinking levels `false, true` (default `true`), a context length of 40960, 4.0B parameters and quantization Q4_K_M; it pulled as 2.6 GB. So `think: false` is available. Whether it holds in a reply is what `check`'s warm-up tests.
- *Not chosen:*
  - `qwen3:4b-instruct-2507-q4_K_M`, which never thinks but is a newer generation than D37 and D26 used;
  - keeping `qwen3:4b` with thinking on, which changes the declared setting and needs a larger output limit and code to separate the reasoning from the answer;
  - postponing the counted run until after TA-2.
- *Unchanged:* everything else that D39 item 8 and D42 fixed: Q4_K_M, `think: false`, temperature 0, seed 0, a 4,096-token context, at most 512 tokens out, one try, the prompt and the two checks.
- *"First try"* now means the first generation for each placement after the commit of this batch.

**4. Effect.** No explanation had been generated, so no result changes, and none was seen before the choice. What changes is the model that the secondary question tests. The primary result (D41) and every frozen file are untouched, and the freeze check passes.

**5. A fix to D42's code (Claude's error).** A thinking trace was looked for only in Ollama's separate thinking field and as an opening `<think>` in the text. The leak in item 1 had neither, so in an explanation it would not have been recorded as a deviation. Now `thinking_trace` (`src/explain/__init__.py`) also counts `</think>`, both in `check`'s warm-up and in each explanation. As before, a trace is recorded as a deviation, and the text is still judged by the two checks alone (D42 item 4). The self-test has 40 checks, up from 37: the leak in an explanation, the leak in the warm-up, and the trace test itself.

**6. The Windows set-up as done** (D42 item 7; `04-setup-guide.md` §7).
- *The laptop:* Windows 11, version 26H2; NVIDIA driver 566.07, where Ollama asks for 551.61 or newer (#1057).
- *Ollama:* version 0.40.17, installed in `D:\Ollama`, with its models in `D:\ollama-models` (`OLLAMA_MODELS`).
- *The address:* `OLLAMA_HOST=192.168.115.1:11434`, the VMnet8 address. Ollama then listened on that address alone. Its FAQ shows only `0.0.0.0` (#1054); this was observed on the laptop on 24 November.
- *The firewall:* the rule of §7.4. No firewall rule names an Ollama program, so no firewall prompt was answered either way.
- *The VM:* the Kali VM, at 192.168.115.128, reaches Ollama, and its self-test passed.
- *The download:* the first pull stopped at 29% ("unexpected EOF"); a second pull completed.
- *How:* with two helper scripts Claude gave in the chat, a Windows check-and-apply script and a Kali check. They are not in the repository.

**7. Corrections.**
- *D37 item 6* said the model "fits the graphics memory of the user's laptop".
  - That is true of the file. But the laptop's Ryzen 7 7435HS has no integrated graphics (#1055), so the RTX 2050 also draws the screen: 1.26 GB of its 4 GB were in use at idle on 24 November.
  - With a 4,096-token context, the model may not fit entirely, and Ollama then runs part of it on the processor.
  - That changes no declared setting. The counted run records the time as it is, and D44 records the split that `ollama ps` shows.
- *Chat advice, 21–22 November.* Claude told the user to click Cancel if Windows asked whether to allow Ollama. That was wrong: cancelling the prompt creates block rules, and block rules override allow rules (#1058). The user had not been asked. §7 now says Allow access.

**8. Made with this entry.**
- The model tag and the trace fix: `src/explain/__init__.py`, `src/explain/ollama.py`, `scripts/explain_counted.py` and `scripts/explain_selftest.py`.
- Inline notes in D37 item 6, D39 item 8 and D42 items 4, 5, 7 and 11, and in `03-evaluation-methodology.md` §6, `02-ai-role.md`, `02-prototype-architecture.md` and `00-glossary.md`.
- `04-setup-guide.md` §7: the tag, Ollama's minimum versions, the model folder, the listening address, the firewall prompt, `ollama ps` after the run, and two new troubleshooting rows.
- `README.md`, `00-action-items.md` A6 and `00-project-phases.md`.
- `sources.md` #1054–#1059, and notes on #989 and #1052; `00-project-index.md`'s source count.

*Still stale, as D42 item 10 named them:* `02-system-flow.md` and `05-thesis-structure.md` row 4.7.

**9. Next.**
1. The user applies and pushes this batch.
2. Then `check` until READY, `run` once, `ollama ps` on Windows, and `rate`.
3. Then the user pushes `data/results/explanations.json`.
4. D44 records the four counts, the ratings and the split between graphics card and processor.

The counts were to go to D43 (D42 items 7 and 11); this amendment takes D43.

*Status: the user's decision of 24 November 2026 (item 3), drafted by Claude; the code fix and the record-keeping are Claude's. Not independently reviewed. Reference: D37 item 6, D39 item 8, D42, `src/explain/`, `04-setup-guide.md` §7, `sources.md` #989, #1052, #1054–#1059.*
