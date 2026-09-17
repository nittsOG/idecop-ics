# Iteration 12 — Findings

Targeted iteration on the two scoring components that were weakest in the specification: the detectability filter (Filter 2, `formal-problem-definition.md` §4), which was qualitative, and asset criticality (§2), whose `Damage(v)` term had no external grounding.

**Sources added:** #332–336. **Result:** one open problem substantially closed, one uncomfortable finding that the thesis must address head-on, one term grounded, one terminology collision identified.

---

## 1. Detectability is measurable, and the project was wrong to treat it as inherently qualitative

`04-deployment-requirements.md` §7 listed "detectability scoring is currently qualitative — applied as a downward adjustment by reasoning, not computed from measurable signatures" as an open engineering problem. That framing was too pessimistic. Three usable instruments exist.

**Shodan Honeyscore (#332).** A proprietary score returning a probability between 0.0 and 1.0 that a honeypot sits at a given IP address. An independent study of ICS honeypots measured its precision at **70.3%** using a threshold of 0.5. This matters regardless of the algorithm being proprietary: it is an existence proof that per-position detectability is already expressed as a scalar in the interval this project's `detectability_risk` field already uses, and it is externally computable rather than assigned by judgement.

**A 2026 systematic review of fingerprinting (#333)** — *A Review of Honeypots: Fingerprinting Techniques, Detection, and Evasion Mechanisms*, Future Internet 18(4):190. Supplies a structured taxonomy: artifact classes (static banners, default configurations, timing and latency, handshake and negotiation, protocol subset implementation) crossed with probing techniques (single-stage active, multi-stage active). Its central finding is directly applicable: **fingerprinting difficulty scales with interaction level, and low-interaction deployments — which is what ICS and OT honeypots overwhelmingly are — are identified through surface-level artifacts using basic active probing.** That converts Filter 2 from a judgement call into a checklist: which artifact classes are exposed at this network position, and which probing techniques reach it there.

**HoneyJudge (#334)** — memory-feature-based PLC honeypot identification using weighted voting across system-, user- and process-level memory features, going beyond Nmap and PLCScan.

**Consequence for the specification.** Filter 2 can be operationalised without solving honeypot fingerprinting, which the synthesis document correctly said was out of scope. The move is to score a candidate position against #333's artifact taxonomy — a bounded, defensible, citable procedure — and to cite Honeyscore as evidence that the quantity being estimated is real and externally measurable. **This does not require new research, only a scoring rubric, and is therefore cheap.** Recorded as A23.

---

## 2. The uncomfortable finding

`ICSLure`'s comparative evaluation (§6.3, already logged as #20 in the citation shortlist) reports results that the thesis cannot ignore:

- Nmap identifies Conpot as a honeypot. PLCScan flags it as non-authentic.
- Using **TIA Portal** — Siemens' ordinary engineering software, not an attack tool — Conpot, HoneyPLC, ICSpot and ICSpot+LSTM were all detected as honeypots.
- An **idling real PLC remained indistinguishable** from real hardware.

Stated plainly: **essentially every emulated ICS honeypot in the open-source literature is detectable by a competent OT engineer using standard engineering tooling.** Only real hardware passes.

### Why this is a problem for the thesis

An examiner can construct the argument in one line: *if any capable attacker can identify your decoys, what is the value of optimising where they go?*

### Why the project's own design already answers it — and why that must be said explicitly

The answer is not a defence bolted on afterwards. It falls out of the objective function that already exists, which is the strongest form the argument can take.

1. **Detectability is attacker-dependent, not absolute.** An adversary in the reconnaissance stage running broad scans is not running TIA Portal against every host. Fingerprinting costs time, tooling, and exposure. The detection opportunity exists in the window before the attacker invests in verification.
2. **This is precisely why `Early(x)` is in the objective.** Decoy fidelity degrades under scrutiny, and scrutiny increases as an attack progresses. A decoy encountered at step 1 of a path faces a scanning adversary; the same decoy at step 5 faces an adversary with established access, engineering tooling and time. Early interception is not merely *preferable* — it is the condition under which deception works at all. The earliness term was justified in `research-synthesis-implementation.md` on coverage grounds; this finding gives it a second, stronger justification.
3. **This is why Filter 2 down-weights rather than excludes.** The original decision — recorded in D3 — was to treat detectability as a risk adjustment rather than a hard exclusion. That now looks better-founded than when it was made: a hard exclusion would empty the candidate set entirely, since on this evidence no emulated position is undetectable.
4. **It sharpens the Sweep–Seek rule from iteration 11.** A *Sweep* encounter happens under broad, low-scrutiny movement — exactly the regime where decoys survive. A *Seek* encounter happens when the attacker is deliberately examining a specific asset type — exactly the regime where fingerprinting occurs. **Sweep candidates are therefore more robust to detectability than Seek candidates**, which is a substantive placement principle that neither source states and that follows from combining them.

**Action:** this belongs in the thesis as a stated assumption in the threat model and as a paragraph in the results discussion, not as a footnote. Point 4 above is a genuine synthesis of two independent sources and is worth stating as such.

---

## 3. Criticality — no security-specific improvement found, but `Damage(v)` gains grounding

Searching for OT-specific, security-oriented asset criticality quantification returned no method superior to what `formal-problem-definition.md` §2 already specifies. The CVSS-based work found (#335) scores *vulnerability* severity, not asset criticality, and is the same lineage the TrapManager paper (#326) uses for node weighting — a route this project deliberately does not take, since CVE severity is not operational importance.

What did surface is that `Damage(v)` — currently defined loosely as "fraction of operational/process load the asset is responsible for" — has a well-established industrial grounding in **Asset Criticality Analysis** practice (#336). The standard reliability-engineering formulation is Criticality = Consequence × Likelihood, where Consequence is a weighted sum of severity scores across safety, environmental, production, quality, maintenance-cost and customer-impact categories.

**Why this is worth adopting:** it supplies a defensible answer to "where does `Damage(v)` come from?" that is not "elicited during testbed design." It is the language plant engineers already use, which matters for the deployment-credibility argument in `04-deployment-requirements.md` §1, where `Damage(v)` was flagged as requiring process knowledge the security function does not hold. If the number is requested in the form an ACA already produces, the elicitation problem largely disappears.

**Caution — do not overreach.** ACA is maintenance and reliability practice, concerned with failure, not with attack. Importing the vocabulary is legitimate; importing the likelihood term is not, since probability of *failure* is unrelated to probability of *compromise*. Use the consequence decomposition only.

---

## 4. Terminology collision — must be fixed in the glossary

ACA methodologies sometimes extend the formula to Criticality = Consequence × Likelihood × **Detectability**, where detectability means *whether an impending failure can be detected before it occurs*.

This project uses **detectability** to mean *whether an attacker can identify a decoy as a decoy*.

Same word, opposite direction, both in an industrial-asset context. A reader coming from reliability engineering — which includes many OT practitioners — will misread it. `00-glossary.md` must disambiguate explicitly, and the thesis should use "decoy detectability" on first use in each chapter rather than the bare term.

---

## 5. What this iteration did not do

- Did not obtain the full text of #333; the assessment rests on abstract and section-level extracts. The artifact taxonomy should be read in full before a scoring rubric is built from it.
- Did not resolve whether Honeyscore can be queried programmatically for testbed positions, which would matter only for a real deployment, not for this evaluation.
- Did not address A4 (#315 manufacturing paper), unchanged since iteration 10.

---

## 6. Open items after this iteration

| Item | Status |
|---|---|
| A23 — build a Filter 2 scoring rubric from #333's artifact taxonomy | **New, cheap, high value** |
| A24 — add the decoy-detectability assumption and the Sweep/Seek robustness principle to the threat model | **New** |
| A25 — reframe `Damage(v)` elicitation in ACA consequence-category terms | New, low priority |
| A26 — disambiguate "detectability" in the glossary | **New, trivial, do it with the next glossary edit** |
| A22 — conduit SL decision | Unchanged, blocking Phase D |
| A11 — Risk/CritProt normalisation | Unchanged, highest technical priority |
