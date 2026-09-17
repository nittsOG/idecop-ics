# Honest Review — Claims, Objective, Architecture

Requested before implementing the A11/A22 changes. This is an adversarial read of the project's own work, done by running tests rather than by reasoning about it. Where the project is sound, it says so; where it is not, it says that too.

**Method.** All structural claims below were tested empirically on the real instance by enumerating all 32 subsets of **L** and checking monotonicity and submodularity exhaustively — no sampling, no approximation. Script: `scripts/structure_check.py`. Results are reproducible in under a second.

---

## A. Verdict first

| Element | Verdict |
|---|---|
| Novelty claim | **Sound, after the iteration-11 narrowing.** One clause is currently false and is being fixed by A22 |
| Primary research question | **Currently unanswerable as written.** Fixable, and the fix is legitimate — but carries a real integrity risk (§F) |
| Secondary research question | Sound, untested, cheap to satisfy |
| Objective function, as built | **Two defects, both verified, both material** |
| Submodularity / greedy guarantee | **Not currently held. My previous claim about the fix was also wrong** (§D.3) |
| Architecture | **Sound.** The strongest part of the project |
| Overall | Proceed with A11/A22, with one framing change and one honesty requirement |

---

## B. The novelty claim

**Current wording:** no published work performs formal, quantitative deception-placement optimisation across a multi-zone OT/ICS architecture using IEC 62443 zone *and conduit* structure and asset criticality as first-class inputs to a composite objective, validated against baselines.

**Clause-by-clause:**

| Clause | Status |
|---|---|
| "formal, quantitative … optimisation" | Holds. Implemented, exact and heuristic |
| "multi-zone OT/ICS architecture" | Holds. 4 zones, 11 nodes. Jay is single-VLAN; TrapManager has no zones |
| "IEC 62443 zone … as first-class input" | Holds. `SL(zone(v))` enters `Crit(v)` numerically |
| **"and conduit structure"** | **FALSE as built.** Conduits are stored and diagrammed but enter no computation. A22 fixes this |
| "asset criticality as first-class input" | Holds |
| "composite objective" | Holds — five terms, more than any comparator found |
| "validated against baselines" | Holds — random and betweenness, identical paths |

**Assessment:** the claim survives twelve research iterations and two full-text reads of the nearest competitors. It is stated at defensible strength, and the iteration-11 narrowing removed the one clause that invited a definitional fight. The conduit clause is the remaining liability and is precisely the kind of thing a careful examiner checks, because it is named in the claim itself.

**What would break it:** a paper applying IEC 62443 zone structure to placement optimisation. Twelve iterations have not found one. The residual risk is concentrated in forward-citation searches that have not been run systematically (A17), which is the one honest weakness of the review method.

---

## C. The research questions

### Primary — currently unanswerable

> Does Method 3 achieve statistically higher Coverage(x) and CritProt(x), and lower Cost(x) for equivalent coverage, than Methods 1 and 2?

Verified on the current build: the proposed method selects **DMZ Jump Host alone**, Coverage 0.33. The centrality baseline selects **two locations**, Coverage 0.67. The proposed method loses on the exact metric the question asks about, and wins on F(x) — because F(x) charges for risk and cost, which the baselines ignore.

**This is not a bug in the optimiser.** It is optimising exactly what it was told to optimise. The question and the objective ask for different things.

**Two legitimate resolutions, and they are not equivalent:**

1. **Fix the objective** (A11). The defects in §D are real and independently justified. Under the corrected objective the exhaustive optimum at B=3 becomes all three locations, **Coverage 1.00** — verified, not predicted. The primary question then becomes answerable in the affirmative.
2. **Rephrase the question** to ask about the objective-defined tradeoff rather than raw coverage — which is arguably the more honest framing, since the entire point of the work is that raw coverage is *not* the right measure.

**Recommendation: do both, and in that order.** The objective defects should be fixed on their own merits regardless of what happens to the question. But the question should *also* be rephrased, because a question phrased in terms of two of the five terms understates the contribution. See §F for why doing only (1) is dangerous.

### Secondary — sound but untested

> Can a local LLM generate an analyst-readable explanation without altering x*?

Architecturally guaranteed: the explanation layer reads a stored, completed run. The falsifiable half — that every claim in generated text traces to a value in the structured input — has no test yet. Cheap to build, and without it "analyst-readable" is an assertion rather than a result.

---

## D. The objective function

### D.1 Defect one — `Early(x)` is non-monotone. **Verified.**

Defined as a mean over *intercepted* paths. Adding a decoy that intercepts late lowers the mean.

```
Early (current, mean)     monotone=NO (16 violations)   submodular=NO (18 violations)
Early (proposed, /|P|)    monotone=YES                  submodular=YES
```

Changing the denominator from |I(x)| to |P| makes it monotone and submodular. Notably, this is what D16's rejected "Option 2" was approximating — it was rejected for not matching the mean-normalised definition. Redefine the objective and the mismatch disappears, which also means the MILP linearises in a single solve and D16's k-enumeration workaround becomes unnecessary.

**Interpretability is not lost:** keep mean-earliness as a *reported statistic*. "Average interception stage" remains the readable number for the results chapter; it just stops being the thing the solver maximises.

### D.2 Defect two — scale mismatch. **Verified.**

`Risk` is an unnormalised sum, unbounded above. `CritProt` is normalised against the criticality of *all* assets, capping it near 0.30 even at full coverage. Both are structurally fine — monotone and submodular — but they are on different scales from Coverage and Early, so equal weights are not equal. The sensitivity sweep would have swept distorted axes.

### D.3 The submodularity claim — I was wrong, and so is D1

**D1 as written cannot be claimed.** Verified:

```
F CURRENT     submodular = NO (18 violations)
```

Counterexample from the run: with A = {DMZ Jump Host} and B = {DMZ Jump Host, Eng WS-2}, adding HMI gains −0.35 from A but −0.10 from B. Adding to the larger set helps *more*. That is the definition of non-submodular, and it comes entirely from the `Early` mean.

**But my proposed fix does not fully restore the guarantee either, and I stated otherwise last session. Correcting that here.**

```
F PROPOSED    submodular = YES    monotone = NO (32 violations)
```

Submodularity is restored. Monotonicity is not — and cannot be, because Risk and Cost are subtracted. **The classical (1−1/e) greedy guarantee requires monotone submodular maximisation under a cardinality constraint.** A non-monotone submodular objective does not qualify, so plain greedy has no clean (1−1/e) bound on F even after the fix.

**Two honest routes, both defensible:**

- **Route 1 — cite the regularised result.** For f = g − ℓ with g monotone submodular and ℓ modular non-negative, a known guarantee of the form (1−1/e)·g(S) − ℓ(S) ≥ (1−1/e)·g(OPT) − ℓ(OPT) exists in the literature (Sviridenko, Vondrák & Ward). This is weaker than (1−1/e) on F, it is real, and it is the correct thing to cite. Requires locating and verifying the primary source — **not yet done, and it must be before anything is claimed.**
- **Route 2 — move risk from penalty to constraint.** Maximise the monotone submodular gain part subject to Σx ≤ B *and* Σ r_l·x_l ≤ R_max. Then the classical guarantee applies cleanly. Costs one extra parameter and changes the formulation; gains a fully clean theoretical position.

**Recommendation: Route 1 for the thesis, with Route 2 named as an alternative formulation.** Route 1 preserves the five-term composite objective that is the actual contribution. But either way, D1's current wording — "greedy, exploiting submodularity … state the proof or the argument for why it approximately holds" — must be rewritten, because the honest answer today is that it does not hold.

**Silver lining, and it is a real one.** The exact MILP validator reports a 0.0% optimality gap on this instance. The approximation guarantee is a theoretical nicety here, not a practical necessity — the exact optimum is computable at testbed scale. The guarantee matters for the *scalability* argument, not for these results. That is a defensible position and should be stated as such rather than glossed.

### D.4 What the corrected objective actually produces. **Verified.**

```
CURRENT   x* = [DMZ Jump Host]                             F=0.4032  Coverage=0.33
PROPOSED  x* = [DMZ Jump Host, Eng WS-2, HMI]              F=1.7500  Coverage=1.00
```

Full coverage of all three paths at B=3.

---

## E. Architecture

The strongest part of the project, and the review found nothing to change.

- **Optimiser decides, model explains.** Deterministic, reproducible, and a compromised model cannot alter `x*`. Has published precedent. Also the correct answer to the deployment-security question.
- **Single shared `score()`.** All four methods scored identically. Without this the comparison would be meaningless, and it is the kind of thing that is easy to get wrong.
- **Human confirmation gates AI suggestions into `L`.** Unconfirmed suggestions have no path into the search space.
- **Single write path through `/api`.** One violation found (`graph_model.write_computed_scores`), minor, worth fixing for consistency.
- **Graceful degradation.** Delete both AI components and a valid placement still emerges. Rare and worth stating explicitly in the thesis.

---

## F. The integrity risk — stated plainly

**The corrected objective produces the result the research question wants.** That sequence — question unanswerable, objective changed, question now answerable — is exactly the pattern a sceptical examiner is trained to look for. It looks like fitting the model to the desired conclusion.

The defence is genuine and must be documented *now*, before the results exist:

1. Every change is independently justified. Non-monotonicity is a structural defect verified by exhaustive enumeration, not an inconvenience. Unbounded `Risk` contradicts the specification's own definition of it as a probability. The `CritProt` denominator silently down-weights a term the weights claim to treat equally.
2. The defects were found **before** the evaluation campaign, by structural testing, not by observing unwelcome results and hunting for a cause.
3. The full record — the original objective, the defects, the fix, and the effect on the outcome — is preserved in the decisions log rather than replaced.

**Requirements, non-negotiable:**

- Record a decision entry stating the changes, the justification, **and the effect on the result**, explicitly acknowledging that the fix improves the outcome.
- Report results under **both** objectives in the results chapter. The old objective's result is not an embarrassment; it is evidence that the fix was principled, and it demonstrates exactly the coverage/earliness tradeoff the work is about.
- Rephrase the primary question anyway. If it is only ever answerable after an objective change, it was too narrow to begin with.

Doing this converts the biggest vulnerability in the thesis into one of its better methodology sections.

---

## G. What to do

**Proceed with A11 and A22 together**, with three amendments to the plan as previously stated:

1. **D1 must be rewritten**, not merely re-verified. Locate the regularised-submodularity result, verify it against its primary source, and state the guarantee at the strength it actually holds — or adopt Route 2. Until then, claim no guarantee. *(New action item.)*
2. **Report both objectives** in the results chapter.
3. **Rephrase the primary research question** as well as fixing the objective, not instead of.

**Do not change:** the architecture, the AI role separation, the baseline choice, or the testbed scale.

**Confidence.** The structural findings in §D are verified by exhaustive enumeration on the real instance and are as certain as anything in this project. The novelty assessment in §B is *likely* — twelve iterations of consistent negative results, but no systematic database sweep. §F is judgement, not evidence.
