# Iteration 9 Findings — OT/ICS Deception Placement Optimization

Builds on iterations 1–8. Does not repeat those conclusions — see `sources.md` for the running source log. Source numbers below refer to that file (iteration 9 = #299–304).

Continued the diversification from iteration 8: a targeted DTIC/OSTI sweep, and a first real pass at European sources. Both paid off, though differently than expected.

## 1. The best find: a federal tool that does almost everything except the one thing you're doing

MITRE built and licenses a tool called CICAT — the Critical Infrastructure Cyberspace Analysis Tool [299] — originally for an IAEA project on nuclear-facility cybersecurity. Feed it an infrastructure model and it does MITRE-ATT&CK-based attack-path analysis, computes impact and risk scores per path from asset criticality, and identifies **"hot spots"**: places in the infrastructure an adversary is likely to transit or dwell. Read that description again and it sounds like it could be doing your project's job.

It isn't. CICAT stops at identification and risk scoring — it's built for incident-response planning and countermeasure prioritization, not for deciding where to put decoys. But that's exactly what makes it valuable to you: it's a federally-built, nuclear-facility-validated confirmation that the *analysis* half of your pipeline (attack-path generation, criticality-weighted scoring, identifying which nodes matter most) is mature, real, and already trusted for critical infrastructure. Your contribution starts exactly where CICAT stops — taking that same kind of hot-spot analysis and using it to decide *deception* placement rather than incident-response priority. That's a clean, citable line to draw in your differentiation section: "the underlying attack-path-and-criticality analysis this project depends on is not novel and is validated by tools like CICAT; the novel step is using that analysis to drive a deception-placement objective, which CICAT and tools like it do not attempt."

## 2. Europe has the same kind of tool, funded differently

securiCAD [303], developed by a KTH (Sweden) spin-off under the EU's Horizon 2020 program, does essentially the same thing as CICAT — simulates attacks across a modeled network, finds critical attack paths, estimates time-to-compromise — for a European commercial and research audience rather than a US federal one. Independent confirmation, from a completely different funding and institutional context, that CICAT's category of tool is a recognized, mature space. Neither this nor CICAT does deception placement, which is worth stating plainly rather than stretching either into something it isn't.

On the regulatory side, ENISA's honeypot report [302] is a legitimate EU-agency citation to sit alongside iteration 7's CISA/FBI/NCSC guidance — but it's general-purpose (any honeypot, not OT-specific) and about honeypot *types*, not placement. Don't oversell it; it's a breadth citation, not a methodological one.

## 3. A decade of comparable graduate work, and it tells the same story

A DTIC search surfaced a real corpus of NPS Master's theses on ICS honeypots beyond what iteration 8 found from Rowe's own bibliography [304] — cost-effective honeypot construction, building-automation honeypots, SIEM integration, honeypot evasion. This is useful less as individual citations and more as a pattern: an entire decade of comparable-level graduate thesis work at a peer military postgraduate institution, and none of it attempts formal placement optimization either. Every single thesis is about building, hardening, or evading detection of a honeypot once its location is already decided. That's now four independent bodies of work — the academic optimization literature (iterations 3–7), the commercial vendors (iteration 1), Sandia (iteration 8), and now a decade of NPS theses — all confirming the same gap from different angles. That redundancy is worth a sentence in your thesis: this isn't a gap because nobody looked, it's a gap that's held up across every adjacent community that could plausibly have filled it.

## Still open

- CICAT and securiCAD are described from public capability documents, not their actual source code or algorithms — if either turns out to be open enough to inspect, their attack-path/criticality scoring formulas could be a direct methodological reference for your own model.
- The DTIC corpus [304] wasn't individually catalogued thesis-by-thesis — if you want specific citations rather than a pattern observation, a follow-up pass could pull 3-4 of the most relevant by title.
- Still untouched: a dedicated look at whether any water-sector or electricity-sector ISAC (WaterISAC, E-ISAC) or EPRI has published anything on deception specifically, as opposed to general OT security.

## Candidates for iteration 10

- Pull CICAT's and securiCAD's actual scoring methodology if publicly documented in more depth than the capability-description PDFs found this round — worth knowing whether either has a formula you can adapt or cite, the way iteration 6's patent formula worked.
- A sector-specific pass (water, electricity) rather than a general-OT pass, since general OT/ICS search has now been run from academic, commercial, national-lab, and EU angles and each has returned a version of the same picture.
- At this point, nine iterations in, the source base is broad enough that further iterations are likely to keep confirming rather than overturning the novelty picture — worth weighing against the same time cost you were weighing between iterations 5 and 6.
