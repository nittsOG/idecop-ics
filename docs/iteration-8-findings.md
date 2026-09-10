# Iteration 8 Findings — OT/ICS Deception Placement Optimization

Builds on iterations 1–7. Does not repeat those conclusions — see `sources.md` for the running source log. Source numbers below refer to that file (iteration 8 = #287–298).

You asked for genuinely new sources rather than deeper digging in the same cluster. That's what this round did: two entire source ecosystems — US national laboratory technical reports (Sandia, INL, via DOE's OSTI.gov) and a decade of empirical ICS-honeypot research from the Naval Postgraduate School — hadn't been touched at all in seven iterations, which had stayed almost entirely inside arXiv/IEEE/ACM/ScienceDirect/Springer academic-publisher space. Both turned out to matter.

## 1. The most important find of any iteration so far — read this one carefully

Neil Rowe (NPS) published a 2025 book chapter, "Designing Deceptions for Protecting Industrial Control Systems" [287], and it needed a full read rather than a snippet, because the title alone could make you think someone already did your project. They didn't — but the reason why matters, and you need to be able to explain it precisely.

Rowe's chapter defines eight "deception locations": external interface, user interface, real/bait files, device table, kernel, device-driver interface, real devices, decoy devices. That sounds exactly like your placement problem. It isn't. **These are layers inside one ICS device's software stack** — the same distinction as OSI-layer defense-in-depth, but for deception. His question is "given one PLC or one HVAC controller, which layer of its software should carry the deception, and which of ten tactics (false displays, fake controls, decoys, false error messages, obfuscatory controls, and so on) should it use, given what we've inferred about this specific attacker's psychology?" Your question is "given a network of many PLCs, HMIs, and workstations, which *assets* should get a decoy, using a formal multi-metric objective?" Both are legitimately called "deception placement." They are not the same problem.

This distinction is exactly the kind of thing your section 14 needs to get right. If you cite Rowe without explaining this, a reader familiar with the chapter might think you've either duplicated it or misunderstood it. If you cite it *and* draw this distinction explicitly, it does real work for you: it shows you've found and understood the closest-sounding prior art and can articulate precisely why your contribution is different — device-internal layering with psychologically-adaptive tactics, versus network-topology optimization with a formal objective function. That's a stronger differentiation section than most citations you have on file.

Two more things from this chapter worth knowing: its qualitative Tables 1–2 (rating each attacker goal against deception difficulty and desirability) are a genuinely useful sanity-check reference when you're deciding which deception *types* to include in your prototype, independent of where you place them. And its reference list [288–295] opened up a whole sub-cluster of NPS empirical work you didn't have before — real honeypots, deployed for years, with real attack data, which is a different kind of evidence than the mostly-simulated game-theory papers dominating iterations 3–7.

## 2. A government national lab already says what you're trying to prove

Sandia National Laboratories published an internal R&D report in 2021 (SAND2021-11609, hosted on the Department of Energy's OSTI.gov) [296] stating plainly: **"there is currently an absence of well-developed cyber-physical deception elements and virtualization technologies for OT systems."** This is not an academic survey making a literature-review claim — it's a U.S. national laboratory's own internal assessment of the field, funded to build exactly this kind of capability because it recognized the gap. That's about as strong a piece of evidence for your motivation section as you're likely to find, and it's from a completely independent source (DOE, not academia) confirming the same conclusion iterations 1–7 built from journal papers.

The same search surfaced Sandia's HADES system [297] — a real, deployed, federally-recognized (2018 Government Innovation Award) deception platform — and INL's dedicated Controls Laboratory [298], the DOE's primary ICS red-team/blue-team research facility. Neither does placement optimization, but both belong in your "existing tools" inventory alongside Conpot, HoneyPLC, and the commercial vendors, and citing a national lab platform alongside academic ones shows breadth.

## 3. A decade of empirical placement-adjacent data, independent of game theory

Everything from iterations 3–7 was either simulation-based or proof-based (game theory, MILP, submodularity). Rowe's group has spent years running *real* ICS honeypots in the wild and measuring what actually happens — how deployment location (cloud vs. corporate network), geographic region, and interaction level affect the traffic and attacks a honeypot receives [293], and how obfuscating real PLCs to look like honeypots affects reconnaissance [290]. None of this is a formal optimizer, but it's real-world evidence about *which factors actually matter* for deception effectiveness in practice — useful for grounding your metric choices (which factors are worth including in your objective) in something other than theory.

## Still open

- Rowe's chapter cites several more NPS theses and papers not individually pulled this round (Ramirez et al. on RDP attack classification, Rrushi's physics-driven kernel deception, Landsborough et al. on multilayer deception-in-depth) — worth a pass if you want to exhaust this specific vein.
- OSTI.gov and DTIC (apps.dtic.mil) are now confirmed-useful search targets but weren't searched exhaustively — a dedicated pass on either could surface more national-lab or military-thesis material specifically on placement (as opposed to the deception-mechanism material found this round).
- PNNL (Pacific Northwest National Laboratory) was mentioned in passing (their GridLAB-D simulator appears in Rowe's own testbed) but not searched directly as its own source.

## Candidates for iteration 9

- A dedicated OSTI.gov / DTIC sweep specifically for "placement" or "allocation" language, now that both repositories are confirmed to hold relevant material — this round found them via a general query and got deception-mechanism results; a more targeted query might surface something closer to your actual optimization problem.
- European sources (ENISA, EU-funded OT security projects) — still untouched; another source ecosystem entirely, and Europe has its own regulatory push (NIS2) that iteration 5's IEC 62443 material touched only in passing.
- Given how much this round changed the picture (a top-tier related-work citation, a new independent gap-confirmation source, and a real distinction to draw in section 14), it may be worth pausing to actually draft the differentiation section with what's now on file, before opening more source ecosystems — eight iterations plus this one substantial new vein is a strong foundation.
