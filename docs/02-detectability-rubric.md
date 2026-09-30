# Filter 2 — Detectability Scoring Rubric

Replaces the qualitative down-weighting in `formal-problem-definition.md` §4 with a three-factor scoring procedure. Closes A23.

**Version note.** This is version 2. Version 1 was built from fragments of Chaudhry et al. (#352) gathered through search snippets, because the full text had not been obtained. It was wrong on one factor in a way that mattered. The full paper was then read, the factor corrected, and the values re-derived. Version 1's error and its consequence are kept in §5 rather than deleted, because the failure mode — building on partial access to a source that was freely available — is worth recording.

---

## 1. The source taxonomy, as actually published

Chaudhry, Andersen, Choudhary & Dragoni, *Future Internet* 18(4):190, 2026. Systematic review of 64 papers selected by PICO across Google Scholar, ACM DL, IEEE Xplore, Scopus and DTU Findit.

**Fingerprinting techniques (T1–T7)** — T1 banner and metadata grabbing, T2 handshake and negotiation, T3 command and state analysis, T4 timing and latency, T5 implementation-specific checks, T7 host and system inspection. *(T6 is not named in the article text; the full list appears only in Figure 3.)*

**Probing techniques (P1–P7), all named, ranked by prevalence** — P2 active multi-stage (most prevalent), P1 active single-stage, P5 differential, P3 malformed/fuzzing-based, P4 timing-based, P6 cross-protocol/multi-service, P7 longitudinal/behavioural.

**Susceptibility artifacts (A1–A8)** — explicitly coded in the text: **A1** static banners, **A4** incomplete state machines, **A5** virtualisation artifacts, **A7** default configurations, **A8** behavioural inconsistencies. *(A2, A3 and A6 are not coded in the article text. §6 analyses four protocol artifacts in depth — static banners, limited negotiation, malformed packet handling, error messages — so the uncoded letters most likely map to the latter three, but this project does not assert that mapping.)*

### The two findings that drive this rubric

**§4.9:** *"Low-interaction deployments (e.g., ICS/OT) are primarily identified through surface-level artifacts such as static banners (A1) and default configurations (A7), using basic active probing (P1)."*

**§4.1:** in the OT space, fingerprinting relies heavily on **T1 banner-grabbing** and **T5 implementation-specific checks**, and **A7 default configurations** is the most common artifact.

Read together: **ICS and OT decoys are the easiest class to fingerprint.** They fall to P1 — a single crafted packet, one Nmap scan, one Modbus request plus a TTL check. Supporting specifics from the same paper: Conpot's default banners and absent custom CIP identity attributes; OS leakage through ports left open such as 514/Syslog; GasPot's non-standard error code `9999FF1B`; abnormal error code 03 packets from industrial CPS honeypots under malformed probing; Linux-default TTL values on OT honeypots as distinguishable fingerprints; and a memory-feature testing tool that identifies Conpot and ICSPot by probing control logic blocks.

### Independent support for this project's premise, from the same paper

Two findings worth citing beyond this rubric:

- Ref. [38] measured that corporate-network honeypots received **91% more S7comm traffic** than cloud-hosted ones, while cloud honeypots saw **45% more HTTP traffic** — concluding that *"setting and placement are critical."*
- Ref. [37] found the same for smart grids, adding that *"the complexity in the deployment can help mask the suspiciousness of the honeypot's vulnerability."*

A 2026 systematic review stating that decoy **placement** materially changes both exposure and detectability is direct, independent support for this project's core premise — arriving from the fingerprinting literature rather than the placement literature.

---

## 2. The three factors

**risk(l) = 0.4·Exposure + 0.3·ProbingTierRequired + 0.3·ArtifactExposure**

### E — Exposure: is this position probed at all?

Zone-derived. The OT DMZ is the most externally scanned zone; the Control zone the least reachable. Supported by the measured corporate-vs-cloud traffic differential above.

| Zone | E |
|---|---|
| OT DMZ (PL 3.5) | 0.9 |
| Supervisory (PL 3) | 0.5 |
| Control (PL 1–2) | 0.2 |

### P_req — Probing tier required: how little effort suffices?

The **simplest probing tier that identifies a decoy at this asset type**. A lower required tier means higher risk, because more adversaries reach that tier. This is a property of the *asset type*, not of attacker intent.

| Simplest sufficient tier | P_req |
|---|---|
| P1 — single-stage active (one scan, one protocol request, TTL check) | 0.9 |
| P1–P2 — single or early multi-stage | 0.7 |
| P2 — multi-stage active | 0.6 |
| P2–P7 — multi-stage plus longitudinal realism checks | 0.5 |

### A — Artifact exposure: how many artifact classes are on show?

Which of A1, A4, A5, A7, A8 a decoy at this position must get right, weighted by the review's own prevalence findings — A1 static banners is the single most-reported vulnerable artifact (21 of 64 studies), A7 default configurations the most common in OT.

---

## 3. Scored candidates

| Candidate | Zone | E | P_req | A | **risk** | Reasoning |
|---|---|---|---|---|---|---|
| DMZ Jump Host | OT DMZ | 0.9 | 0.6 (P2) | 0.5 | **0.69** | Heavily scanned, but a generic host needs multi-stage interaction to expose state artifacts |
| Historian | OT DMZ | 0.9 | 0.5 (P2–P7) | 0.6 | **0.69** | Heavily scanned; data-realism failures need sustained observation, so the required tier is higher |
| Engineering WS-2 | Supervisory | 0.5 | 0.6 (P2) | 0.6 | **0.56** | Moderate exposure; VM-based, so A5 virtualisation artifacts apply |
| HMI | Supervisory | 0.5 | 0.7 (P1–P2) | 0.7 | **0.62** | Web-endpoint structure checks identify emulated dashboards early (§4.4) |
| PLC-02 | Control | 0.2 | **0.9 (P1)** | 0.9 | **0.62** | Deepest zone, so rarely reached — but trivially identified once it is |

### What the correction changed

Under version 1, PLC-02 scored 0.59 on the reasoning that deep probing was needed to expose it. **That was backwards.** The paper shows ICS protocol assets are the *easiest* to fingerprint — one Nmap scan, or one Modbus request plus a TTL check. Its exposure is genuinely low, but its identifiability once touched is the highest of any candidate, and the corrected factors express that.

The Historian moved from 0.78 down to 0.69, because data-realism failures require sustained or longitudinal observation rather than a single probe — a higher required tier, therefore lower risk than version 1 assumed.

### A limitation that disappeared

Version 1 derived probing depth from whether a path in **P** swept or sought the asset, which coupled Risk to the attack path set and had to be declared as a modelling caveat. **P_req is a property of the asset type, so that coupling is gone.** Risk and Coverage no longer share an input.

---

## 4. Remaining limitations

**Factor weights (0.4 / 0.3 / 0.3) remain a judgement** and should be swept alongside the objective weights.

**A is asset-type-level, not implementation-level.** It estimates how hard a *class* of asset is to fake, not the quality of a particular decoy. A high-interaction decoy on real hardware would score far better. UHBS (#341) measures actual decoy quality and is the right instrument if this moves to deployment.

**Anchor values are reasoned, not measured.** Measuring them means deploying decoys of each type and running fingerprinting tools against them — a separate study.

**T6 and artifacts A2, A3, A6 are not coded in the article text**, appearing only in figures. The rubric uses only the explicitly coded artifacts.

---

## 5. What version 1 got wrong, and why it is recorded

Version 1 defined the middle factor as *ProbingDepth* — "how hard does the adversary look at this position" — derived from the sweep/seek distinction. Sweep scored 0.3, seek 0.8.

That conflated **attacker intent** with **asset vulnerability**, and for OT it inverts the truth. A sweeping adversary running a single Nmap scan identifies a PLC decoy; the paper states this directly. Version 1 scored that scenario as low risk.

**The cause was working from search fragments rather than the source.** The paper is open access under CC BY and was one fetch away. The rubric was built from four or five sentences visible in snippets, and the structural finding that overturned it sits in the summary of §4.9.

**Effect on results.** Version 1 gave greedy 5 wins / 15 ties / 0 losses against the centrality baseline across 20 configurations. Version 2 gives **9 wins / 11 ties / 0 losses**. The corrected rubric happens to favour the proposed method more than the flawed one did — which is why the correction and its cause are documented here rather than quietly absorbed. *(Both figures were measured while Risk and Cost were divided by the budget. D25 replaced that divisor with a fixed K = 4 and left these risk values unchanged. The same grid now reads 5 / 15 / 0, for a different reason: the four decline wins disappear. See D25.)*

---

## 6. Sources

Chaudhry, Andersen, Choudhary & Dragoni (#352, full text) · Shodan Honeyscore precision on ICS decoys (#332) · HoneyJudge PLC memory-feature identification (#334) · UHBS decoy quality benchmark (#341) · TTL/ICMP identification of ICS honeypots (#342) · ICSLure comparative evaluation · Valeros et al. sweep/seek rule (#329).
