# Iteration 13 — Findings

First iteration to search **products and code repositories** rather than publications. Every previous pass asked what the literature contains; this one asked what vendors and open-source projects actually ship.

**Sources added:** #338–346. **Result:** the novelty claim survives, but one word in it is now doing much more work than before, and that must be understood rather than assumed.

---

## 1. Why this angle was missed for twelve iterations

The research question is academic, so the searching was academic. That is a reasonable default and it is also a blind spot: **a capability can exist in a shipping product without ever appearing in a paper.** Iteration 10 learned that a sector pivot finds what keyword search misses; iteration 11 learned that citation chasing does; this iteration adds a third channel — searching the market rather than the literature.

The pattern across all three is the same. Each new *channel* produced a real find. Additional passes within an exhausted channel produced nothing.

---

## 2. The finding that matters — commercial platforms market "AI-driven placement"

**Acalvio ShadowPlex** advertises an "AI-Enabled Deception Recommendation Engine" and states that the platform "automates network discovery, deception recommendation, and placement" across IT, OT and cloud. **Commvault Threatwise** is described as offering "AI-guided decoy placement." **FortiDeceptor** "automatically discovers network resources and recommends suitable decoys."

On the surface this reads as a direct competitor to this project's entire premise.

### It is not, and the reason is specific

**What Acalvio's engine recommends is decoy *attributes*, not network *positions*.** From their own material: the engine "generates specific properties that enable deceptions to blend into the production network. For decoys, the engine recommends properties like hostnames, operating system versions, and services… the 100+ AD attributes for honeytoken accounts."

That is the **deception-generation** problem — making a decoy believable in its surroundings — which `01-original-brief.md` §4 explicitly places outside this project's scope. The "placement" language refers to automated provisioning and lifecycle management across discovered subnets: the product decides *how many decoys go in each discovered segment and keeps them running*, not *which subset of candidate positions maximises a stated security objective*.

### Four distinctions, for section 14

1. **No published objective.** Nothing is stated to be maximised. There is no F(x) to compare against.
2. **No published baseline comparison.** No evidence that the automated positioning outperforms manual or random placement — the comparison this project's entire evaluation is built around.
3. **Not reproducible.** Proprietary and unpublished, so no formulation exists for anyone to examine, replicate or improve.
4. **No zone structure.** IEC 62443 zones and conduits appear nowhere in the public material. Positioning is driven by network discovery and subnet structure, not by a standards-derived security architecture.

### The consequence — one word is now load-bearing

The novelty claim reads: *"no **published** work performs formal, quantitative deception-placement optimisation…"*

**That word must never be dropped.** The defensible claim is about the published record. It is not a claim about what proprietary products may do internally, and it cannot be — closed products cannot be examined.

This is a *narrowing* of what the claim asserts, not a weakening of the contribution. An open, formal, reproducible method with a stated objective and a baseline comparison is a different kind of artifact from a closed commercial feature, and the thesis should say so plainly. **If asked "isn't Acalvio already doing this?", the answer is: they automate deployment and realism; there is no published method, objective or evaluation to compare against, and that absence is itself part of the problem this work addresses.**

---

## 2a. CORRECTION, added after a patent search

**Section 2 above is incomplete and its central inference was wrong.** It concluded from marketing material that Acalvio recommends decoy attributes rather than positions, and that the word "published" in the novelty claim therefore carries the defence.

A subsequent patent search found **US 9,853,999**, a granted Acalvio patent disclosing an actual placement method: select a subnetwork by asset density or importance score, then determine how many deception mechanisms to deploy there from critical-asset density and a summary statistic over historical attacks.

Two consequences:

1. **A granted patent is published.** The "it isn't published" defence does not apply. The distinction must be method-level — and it is: the patent outputs a *count for a subnet*, not a *set of positions*, and has no objective function, budget constraint, interception-stage reasoning, zone structure or baseline validation.
2. **The reasoning error is worth recording.** Checking marketing and concluding there is no method is not the same as checking patents. Marketing says what a product does for a buyer; patents say what it does mechanically. The second corpus is the one that constitutes prior art, and it had never been searched.

Full comparison: `03-commercial-prior-art-analysis.md`. Sources #347–349.

---

## 3. Open-source landscape — checked directly, nothing found

DejaVu, Beelzebub, DecoyNet, OpenCanary, Cowrie, Conpot, T-Pot, Honeytrap, OWASP Python-Honeypot.

**Every one is generation, deployment or management. None performs placement optimisation.** DejaVu comes closest in spirit — it deploys decoys "strategically across their network on different VLANs" — but the strategy is an administrator's manual choice through a console, which is exactly the practice this project proposes to replace.

One useful adjacent find: **UHBS**, an open-source honeypot benchmarking standard scoring decoy realism, containment and telemetry quality 0–100. Not placement, but it is the complement of Filter 2 — an independent quantitative measure of decoy *quality*, where Filter 2 estimates decoy *exposure*. Worth cross-referencing when the A23 scoring rubric is built.

---

## 4. Second academic sweep — no new competitor

Searching optimal honeypot placement in ICS with Purdue/zone structure and attack-path coverage returned no work occupying the cell. Thirteen iterations, consistent.

Two adjacent papers logged (#343), both with **two-term objectives** — maximise interception, minus cost. That is now the third independent confirmation of the pattern first noted with TrapManager: **the five-term composite objective remains this project's clearest structural distinction from everything found.**

Also logged: an attacker-side ICPS paper deriving optimal strategies for *defeating* honeypot-protected industrial systems, and an ICMP/TTL fingerprinting paper for ICS honeypots specifically (#342). Both reinforce Filter 2 and the detectability assumption due in the threat model (A24).

---

## 5. An incidental finding with two consequences

`github.com/nittsOG/idecop-ics` is now the **top search result** for "github open source tool deception decoy placement optimization ICS OT network."

1. **The work is publicly discoverable and indexed**, which establishes a visible timestamp — useful if priority is ever questioned.
2. **Future searches in this vocabulary will surface this project itself.** Any later iteration must phrase queries to exclude it, or a self-hit will read as a false confirmation that the cell is occupied.

---

## 6. What this iteration did not do

- Did not search patent databases for vendor placement methods. Acalvio and others hold patents; a patent search could reveal whether any proprietary method is objective-driven. **This is the obvious next channel and it is untried.** Google Patents is accessible without institutional credentials, unlike the database sweep in A17.
- Did not search student theses or dissertation repositories.
- Did not run systematic forward-citation searches (still A17, still blocked on database access).

---

## 7. Open items after this iteration

| Item | Status |
|---|---|
| A28 — ensure "published" is retained in every statement of the novelty claim, and add the four commercial distinctions to section 14 | **New** |
| A29 — patent search on Acalvio, Commvault and Fortinet deception placement methods | **New, untried channel, no credentials needed** |
| A23 — Filter 2 scoring rubric; now has two further supporting sources (#341, #342) | Reinforced |
| A24 — detectability assumption in the threat model | Reinforced by #342, #343 |
| A17 — institutional database access for forward-citation search | Unchanged, still the largest methodological gap |
