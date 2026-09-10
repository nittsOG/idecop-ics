# Optimization Formulation — Algorithms for Method 3, and the Two Baselines

Turns `formal-problem-definition.md` §5–7 and decision D1 into actual algorithms. Column and table names below match `02-data-model.md` directly — this document is written to be coded against, not translated first.

## 1. Does F(x) actually satisfy submodularity? (checking D1's open item)

D1 flagged this as something to check, not assume. Working through it term by term rather than citing the guarantee and moving on:

- **Coverage(x)** — a path counts as covered if *any* placed decoy intercepts it. This is a textbook coverage function: once a path is covered, covering it again adds nothing, so the marginal value of adding a decoy can only shrink as the placement set grows. **Submodular.**
- **CritProt(x)** — the same coverage structure, weighted by `Crit(target)` instead of counted uniformly. Weighted coverage functions inherit submodularity from unweighted coverage. **Submodular.**
- **Cost(x)** — `Σ x_l`, a plain count. Linear functions are both submodular and supermodular (the degenerate case). **Submodular (trivially).**
- **Risk(x)** — if modeled as independent per-location risk contributions summed across placements (the straightforward version, and the one this project uses), it's linear in `x` for the same reason as Cost. **Submodular (trivially), under that modeling choice.**
- **Early(x)** — this is the term that breaks the clean story. It's a *mean over intercepted paths*, and the denominator (how many paths are intercepted) itself changes as you add decoys. Ratios of submodular quantities aren't generally submodular — a decoy added late that suddenly intercepts a previously-uncovered path can shift the average in ways a pure coverage function can't.

**Conclusion:** F(x) is a weighted sum of four submodular terms and one term (Early) that isn't cleanly submodular. That means the Kulkarni et al. (1−1/e) guarantee (source #236) does **not** transfer automatically to this specific objective — say this explicitly in the thesis rather than citing the guarantee as if it applies outright. What still holds: greedy remains a well-motivated, standard heuristic for this class of problem regardless of the formal guarantee, and running the MILP validation (§3) is what actually tells you how far greedy lands from optimal on your specific graph — which is a stronger empirical claim than a theoretical bound would give you anyway. If you want the clean guarantee for the thesis's theory section, drop `Early(x)` from the greedy algorithm's internal scoring (use it only in final reporting) and note that as a deliberate simplification.

## 2. Greedy algorithm (primary)

Standard forward greedy over the candidate set `L`, using marginal gain in `F(x)`.

```
GREEDY(L, P, Crit, B, weights=(α,β,γ,δ,ε)):
    x ← ∅                                  # placement set, x_l = 1 for l in x
    remaining ← L
    while |x| < B and remaining is not empty:
        best_l ← None
        best_gain ← 0
        for l in remaining:
            gain ← F(x ∪ {l}) − F(x)        # marginal gain, per §5's F(x)
            if gain > best_gain:
                best_gain ← gain
                best_l ← l
        if best_l is None:
            break                            # no positive marginal gain left — stop early
        x ← x ∪ {best_l}
        remaining ← remaining − {best_l}
    return x, F(x)
```

**Complexity:** each iteration evaluates `F` for every remaining candidate, and evaluating `F` once means checking every path in `P` for interception — `O(B · |L| · |P|)` overall. At this project's scale (`|L|` on the order of 10, `|P| = 3`, `B` a handful), this runs in well under a second. Not a performance concern here; stated for completeness since a reviewer may ask.

**Early stopping matters practically**, not just theoretically: once no candidate improves `F(x)`, stop rather than filling the budget — this is what lets the evaluation report "the method found K decoys sufficient" as a real result, not just "used all B decoys because that's what was allowed."

## 3. MILP formulation (validation)

The harder question here isn't the standard set-cover-style linearization — it's `Early(x)`, which needs auxiliary variables because "the earliest stage at which any placed decoy intercepts path p" isn't linear in `x` on its own.

**Decision variables:** `x_l ∈ {0,1}` for each `l ∈ L` (as in §5).

**Coverage linearization** — standard set-cover trick. For each path `p`, let `covers(p) = {l ∈ L : l appears in p}`. Introduce `y_p ∈ {0,1}`:
```
y_p ≤ Σ_{l ∈ covers(p)} x_l          for each p ∈ P
y_p ≥ x_l                            for each l ∈ covers(p), each p ∈ P   (forces y_p = 1 if any covering l is placed)
Coverage(x) = (1/|P|) Σ_p y_p
```

**CritProt linearization** — same `y_p` variables, reweighted:
```
CritProt(x) = (1/norm) Σ_p y_p · Crit(target(p))
```

**Cost and Risk** — already linear, no auxiliary variables needed: `Cost(x) = Σ_l x_l`; `Risk(x) = Σ_l risk(l) · x_l` under the independent-contribution model from §1.

**Early linearization** — the real work. For each path `p` with steps `1..len(p)`, introduce `s_p` (continuous, `0 ≤ s_p ≤ 1`) representing `(1 − stage_intercepted/len(p))`, and binary `z_{p,i}` for "path p is first intercepted at step i":
```
Σ_i z_{p,i} = y_p                              # exactly one interception stage, if covered at all
z_{p,i} ≤ Σ_{l ∈ covers_at_step(p,i)} x_l       # can only claim step i if a decoy sits there
z_{p,i} ≤ 1 − Σ_{j<i} z_{p,j}                   # "first" — can't have already been intercepted earlier
s_p = Σ_i z_{p,i} · (1 − i/len(p))              # linear once z_{p,i} are fixed as binaries
Early(x) = (1/Σ_p y_p) Σ_p s_p                  # NOTE: still a ratio — see below
```

**The one thing that stays non-linear:** the final division by `Σ_p y_p` (a variable, not a constant) makes the *objective itself* a ratio of linear expressions — not something MILP solvers handle directly. Two honest options, not one hidden fix:
1. **Fix the denominator** — since `|P| = 3` is small and known, enumerate the possible coverage counts `k = 0..|P|`, fix `Σ_p y_p = k` per solve, and take the best result across all `k+1` runs.
2. **Drop the division for the MILP run specifically** — use `Σ_p s_p` (unnormalized) as the MILP's internal objective, and compute the true normalized `Early(x)` afterward from the resulting `x*` outside the solver.

**Option 2 is wrong, and this was found by implementing it, not by re-reading the math.** It looks like the simpler choice, but building it and running it against greedy on this project's own testbed produced a placement that scored *worse* on the true, normalized `F(x)` than greedy's result — which is logically impossible for a validation method that's supposed to be exact. The reason: an unnormalized sum of per-path early-contributions systematically rewards covering *more* paths over covering *fewer* paths *earlier*, which is not what the real, normalized `Early(x)` rewards — so the proxy and the true objective can rank placements differently, and the solver faithfully optimizes the wrong thing. This is exactly the failure mode the "drop the division" framing should have made obvious in advance, and didn't, until it was actually run.

**Use Option 1.** With `|P| = 3`, this is four solver calls (`k = 0, 1, 2, 3`), each still solved in milliseconds — the exactness that's the entire point of running MILP at all isn't worth trading away for one fewer solver call. Compute all five metrics (§5's `F(x)`, fully normalized) using the same scoring function greedy uses, for every `k`, and keep whichever `k` gives the best true `F(x)`.

**Objective, per fixed `k`:** `maximize α·Coverage(x) + β·(1/k)·Σ_p s_p + γ·CritProt(x) − δ·Risk(x) − ε·Cost(x)` subject to `Σ_l x_l ≤ B`, `Σ_p y_p = k`, and the linearization constraints above — solved once per `k`, best result kept.

## 4. Random baseline (Method 1)

```
RANDOM(L, B, R=30):
    results ← []
    for trial in 1..R:
        x ← uniform_sample(L, size=min(B, |L|), without replacement)
        results.append(F(x))
    return mean(results), std(results)
```
`R = 30` repetitions, not one draw — a single random placement isn't a fair comparator, and the standard deviation across trials is itself worth reporting (it shows how much luck matters for naive placement, which is a point worth making in the thesis regardless of the mean result).

## 5. Centrality baseline (Method 2)

```
CENTRALITY(L, B, Central):
    ranked ← sort L by Central(l) descending
    x ← top B elements of ranked
    return x, F(x)
```
Deterministic — one run, no repetition needed. Betweenness centrality specifically, per D4.

## 6. Solver choice

**OR-Tools CP-SAT**, not PuLP/CBC or a commercial solver. Reasoning: the model above is fundamentally a constraint-satisfaction problem with a linear-ish objective (binary variables, logical implications for the `z_{p,i}` "first interception" constraints) more than a classical LP relaxation problem — CP-SAT is built for exactly this mix and handles the implication-style constraints (`z_{p,i} ≤ 1 − Σ_{j<i} z_{p,j}`) natively without needing big-M reformulation, which is both less error-prone to implement and easier to explain in the thesis than a hand-rolled big-M version. It's free, actively maintained by Google, and was already named as a candidate in the original brief — no new tool to justify.

## What This Enables Next

- **AI role** — the explanation layer's prompt takes exactly this document's output as input: `x*`, `F(x*)` and its five components, plus the same metrics for Methods 1 and 2 for comparison. Nothing here is invented fresh in that document; it's assembled from what greedy/MILP/random/centrality all return.
- **Prototype architecture** — the `/optimize` endpoint from `02-data-model.md`'s API contract calls whichever of GREEDY/MILP/RANDOM/CENTRALITY the request specifies; this document is that endpoint's actual implementation, not just its interface.
