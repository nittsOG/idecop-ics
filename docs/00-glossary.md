# Glossary

Every term this project uses in a technical sense, defined plainly. Ordinary English words used as technical terms (plausibility, rubric, conduit, coverage) are included deliberately — those are the ones that cause confusion, because a reader assumes they already know what they mean.

Where a term has a specific meaning *in this project* that is narrower than its general meaning, that is stated explicitly.

---

## 1. The terms that most need defining

These are ordinary words doing technical work.

**Plausibility** — believability. In this project it means: *could a defender-controlled decoy realistically exist at this position, and would an attacker believe it?* A decoy PLC on a control network is plausible, because real PLCs live there. A decoy firewall is not, because a firewall is infrastructure an attacker routes *through*, not a thing it interacts with and inspects. Plausibility is a property of the *location and asset type*, not of the decoy's technical quality. A perfectly built decoy in an implausible position is still worthless.

**Rubric** — a fixed scoring guide: a set of stated criteria, applied identically to every item being scored, so that two people scoring the same item get the same answer. The word comes from educational assessment. A rubric is the opposite of case-by-case judgement; the criteria are written down *before* scoring begins and do not change between items.

**Plausibility rubric** — this project's specific four-criterion rubric, applied to each asset to decide whether it belongs in the candidate set. Each criterion is scored yes / mostly / no:
1. Can a defender-controlled decoy plausibly exist at this asset type?
2. Would an attacker following one of the defined attack paths plausibly reach or interact with it?
3. Does that interaction yield useful signal?
4. Is the interaction a reliable indicator of malicious intent — i.e. is it unlikely to fire on legitimate activity?

Adapted from a published critique of decoy placement originally written for the enterprise ATT&CK matrix. Applying it to the ICS matrix is new to this project.

**Detectability** — how easily an attacker can tell a decoy is a decoy, from outside. Real, demonstrated attacker capability: passive signatures such as TTL values, open-port counts and response timing can expose a honeypot without the attacker ever touching it. In this project it is the **second filter** on candidate locations. A decoy in a heavily scanned segment is worth less than the same decoy deeper in the network, because it is more likely to be fingerprinted before it can do its job.

**Conduit** — an IEC 62443 term, not a general networking one. A conduit is the *permitted communication channel between two zones*, plus the controls on it. Formally, in this project, the set of edges that cross a given zone boundary. A zone is a group of assets with a shared security requirement; a conduit is how zones are allowed to talk. Note the collision risk in prose: "conduit" also means a physical pipe for cabling in plant engineering, so the standard's meaning should be stated on first use.

**Coverage** — in this project, specifically *attack-path coverage*: the fraction of defined attack paths that have at least one decoy somewhere along them. Not network coverage, not asset coverage. A placement covering two of three paths scores 2/3.

**Early detection / earliness** — how far along an attack path interception happens, expressed as a fraction of the path's length. Catching an attacker at step 1 of 5 is better than at step 5 of 5, because the attacker has done less by then. Scored so that earlier is higher. Critically, in this project it is a **mean over intercepted paths**, which means adding a decoy that only intercepts late can lower the score — a real property of the formulation, not a bug (see D19).

---

## 2. OT / ICS domain

**OT — Operational Technology** — the computing that controls physical processes: valves, motors, breakers, centrifuges. Distinguished from IT, which handles information. An OT failure has physical consequences; an IT failure usually does not.

**ICS — Industrial Control System** — the general category of systems that control industrial processes. Used interchangeably with OT in most contexts, though strictly ICS is a system and OT is the technology domain.

**SCADA — Supervisory Control and Data Acquisition** — an ICS architecture for geographically distributed processes (power grids, pipelines, water networks), where a central station supervises remote sites.

**PLC — Programmable Logic Controller** — the small industrial computer that directly controls physical equipment. Reads sensors, runs control logic, drives actuators. The usual final target of an OT attack, because changing what a PLC does changes what the plant does.

**RTU — Remote Terminal Unit** — similar role to a PLC, typically at a remote or unmanned site, often communicating over a telemetry protocol such as IEC-104. PLC-03 in this testbed is modeled as an RTU.

**HMI — Human Machine Interface** — the operator's screen. Shows process state and accepts operator commands. Attacking the HMI does not change the process, but it changes what the operator *believes* about the process, which is why Stuxnet did it.

**Engineering workstation** — the machine engineers use to write and download control logic to PLCs. High value to an attacker because it is *authorized* to reprogram controllers; compromising it means lateral movement into the control network looks legitimate.

**Historian** — a database that records process data over time, usually sitting in the DMZ so business systems can read it without touching the control network. A common attacker target for reconnaissance.

**Jump host / jump server** — a controlled intermediate machine that administrators must pass through to reach a protected network. Also, therefore, a controlled intermediate machine an attacker must pass through — which is exactly why it is a strong decoy position.

**OT DMZ — demilitarized zone** — the buffer network between the business network and the control network. Nothing crosses directly; traffic terminates in the DMZ and is relayed. The most externally exposed OT-adjacent zone, which is why decoys there score well on interception but poorly on detectability.

**Purdue Model / Purdue level** — the standard layered reference architecture for ICS networks, numbered roughly: Level 0 physical process, Level 1 controllers, Level 2 supervisory control, Level 3 site operations, Level 3.5 DMZ, Levels 4–5 enterprise IT. A shorthand for "how deep in the plant is this asset."

**Zone** — IEC 62443 term: a grouping of assets that share the same security requirements and are protected as a unit. Zones are the structural unit this project optimizes across.

**IEC 62443** — the international standard series for industrial automation and control system security. Source of the zone/conduit model and of Security Levels. Used everywhere in industry as a procedural and architectural framework; this project uses it as a *numeric input to an algorithm*, which is the novelty.

**SL — Security Level** — IEC 62443-3-3's measure of the protection a zone requires, expressed as a vector across seven foundational requirements (FR1 identification and authentication, FR2 use control, FR3 system integrity, FR4 data confidentiality, FR5 restricted data flow, FR6 timely response to events, FR7 resource availability). This project aggregates the vector to a scalar and states plainly that SL quantification is a semi-quantitative approximation, not a solved measurement — which the standards community itself acknowledges.

**Protocols named in this project** — *Modbus*: simple, old, no authentication. *S7comm*: Siemens PLC protocol. *OPC UA*: modern industrial interoperability protocol. *IEC-104*: telemetry protocol for electrical substations, the one Industroyer2 spoke. *IEC 61850 / GOOSE*: substation automation standard and its fast event-messaging mechanism — relevant because the closest prior work (Jay, 2023) is built specifically on GOOSE semantics, which is part of why it does not generalize to this project's problem.

---

## 3. Deception

**Deception asset / decoy** — anything deployed to be interacted with by an attacker and by nobody else, so that any interaction is itself evidence of intrusion. The general category.

**Honeypot** — a whole fake system, deployed to be attacked and observed.

**Honeytoken** — a fake credential, file, database record or API key, planted so that its *use* signals compromise. Cheaper than a honeypot; no system to maintain.

**Honey credential** — a specific honeytoken: a username/password pair that is valid nowhere real. Anyone using it got it by stealing it.

**Honey file** — a document planted to be exfiltrated or opened, instrumented to report when that happens.

**Decoy service** — a fake network service (an open port that answers convincingly) rather than a whole fake machine.

**Decoy PLC** — an OT-specific decoy that presents itself as a controller, typically via an industrial protocol. OpenPLC and HoneyPLC are ways to build one.

**Named tools referenced** — *Conpot*: widely used open-source ICS honeypot. *HoneyPLC*: research honeypot with higher PLC fidelity. *DecIED*, *Decepti-SCADA*: academic OT deception systems. *HADES*: Sandia National Laboratories' deception environment. All of these are about *making* deception. None of them formally optimizes *where it goes* — which is this project's gap.

**Fingerprinting** — identifying what something really is from its observable characteristics. Applied to decoys, it is how an attacker detects the deception. See **detectability**.

**False positive** — a decoy alert triggered by legitimate activity rather than an attacker. In OT this matters more than in IT: a decoy that interferes with real process traffic, or that trains operators to ignore alerts, has a genuine operational cost. Published ablation evidence shows a false-positive-control term was the single most important component of a comparable system's objective, which is why operational risk is weighted heavily here rather than set low by default.

---

## 4. Attack modeling

**Threat model** — the explicit statement of who the attacker is, what they can do, and what they are trying to reach. Without one, "secure" is undefined.

**MITRE ATT&CK for ICS** — a public, structured catalogue of real adversary behaviour observed in industrial environments, organized as tactics and techniques. The ICS matrix is separate from the Enterprise matrix.

**Tactic** — the attacker's goal at a stage: Initial Access, Discovery, Lateral Movement, Collection, Impair Process Control, Inhibit Response Function, Impact. The *why*.

**Technique** — a specific method of achieving a tactic, with an ID. The *how*. ICS technique IDs start with T0 (T0836 Modify Parameter, T0832 Manipulation of View, T0806 Brute Force I/O); Enterprise IDs start with T1 (T1091 Replication Through Removable Media).

**Attack path** — an ordered sequence of (asset, tactic, technique) steps from an entry point to an objective. This project's set is P = {P1, P2, P3}.

**Lateral movement** — moving from one compromised machine to another inside the network, as opposed to breaking in from outside.

**Stuxnet-class** — an attack that enters through the engineering workflow, sabotages the physical process, and conceals the sabotage from the operator's view. Modeled as P1.

**Industroyer2-class** — an attack that enters at the perimeter and speaks an industrial protocol directly to field equipment for fast, unsubtle impact. Modeled as P2.

**Reconnaissance-only path** — an attack path that scans and enumerates but stops before impact. Modeled as P3, deliberately, because it is the path that most directly tests whether a placement detects an attacker *early* rather than eventually.

---

## 5. Graph and optimization

**Graph G = (V, E)** — a set of nodes V (here, assets) and edges E (here, communication relationships). *Directed* means edges have a direction; A→B is not B→A.

**Node attributes** — in this project, each node carries its zone, Purdue level and asset type. Each edge carries its protocol and a weight.

**Centrality** — a family of measures of how structurally important a node is within a graph.

**Betweenness centrality** — specifically: how many shortest paths between other pairs of nodes pass through this node. A node with high betweenness is a chokepoint. This is the project's named baseline method, and it is named explicitly because "centrality-based" alone is ambiguous. A published critique argues that standard centrality measures miss the source/intermediate/target role structure of lateral movement; this project cites that critique as a stated limitation rather than ignoring it or trying to fix it.

**Objective function** — the single number being maximized, combining everything that matters into one comparable score. Here, F(x).

**Decision variable** — what the optimizer is allowed to choose. Here, one binary variable x_l per candidate location: 1 = place a decoy, 0 = do not.

**Constraint** — a hard limit the solution must respect regardless of score. Here, the budget: total decoys ≤ B.

**Budget (B)** — the maximum number of decoys deployable, set by real resource limits rather than chosen for convenience.

**NP-hard** — a complexity class meaning, informally, that no known algorithm finds the exact optimum in reasonable time as the problem grows. Deception placement is proven NP-hard even on static graphs, which is *why* an approximation method is needed rather than brute force.

**Greedy algorithm** — an algorithm that repeatedly takes the single best next step without reconsidering earlier ones. Fast, simple, and usually suboptimal — except when the objective has a property called submodularity.

**Submodularity** — the formal name for diminishing returns: adding a decoy to a small set helps more than adding the same decoy to a large set. When an objective is submodular and monotone, greedy comes with a proven guarantee of at least (1 − 1/e) ≈ 63% of the true optimum. Published work proves a comparable decoy-placement objective is submodular in structured cases. **This project must check whether its own objective satisfies the property before claiming the guarantee** — the proof pattern is reusable, the proof itself is not automatic.

**MILP — Mixed-Integer Linear Programming** — a formal optimization method that finds the *exact* optimum for problems expressible as linear relationships with some integer variables. Exact but expensive; tractable here only because the instance is small.

**CP-SAT** — the constraint-programming solver in Google OR-Tools used to solve this project's MILP formulation.

**Optimality gap** — the distance between an approximate answer and the true optimum. Reported by running the exact method alongside greedy. The whole point of building the MILP validator.

**Linearization / proxy term** — rewriting a term that a linear solver cannot express directly into one it can. This is where D16's bug lived: the substitute term was not equivalent to the original, so the solver optimized the wrong function perfectly.

**Normalization** — scaling a value into a fixed range (usually 0–1) so terms measured in different units can be combined. The failure in D16 came precisely from an *unnormalized* proxy behaving differently from the normalized original.

**Baseline** — a simpler method run under identical conditions, so that the proposed method's result means something. Without baselines, a result is a number with nothing to compare it to. This project uses two: random and betweenness centrality.

**Random baseline** — select B locations uniformly at random. Run 30 times and average, because one draw is not a fair comparison.

**Sensitivity sweep / parametric sweep** — systematically varying the objective's weights and recording how the chosen placement and each metric shift. This is how the weights get *justified* rather than asserted. The field's standard practice; formal expert elicitation has no precedent in this literature.

**Ablation study** — removing one component of a system to measure how much it contributed. Cited here as the evidence for weighting operational risk heavily.

**Wall-clock time** — real elapsed time to compute a result, reported as one of the comparison metrics because a method that is better but takes hours may not be better in practice.

---

## 6. This project's own notation

| Symbol | Meaning |
|---|---|
| `G = (V, E)` | The OT network as a directed graph |
| `V` | All assets |
| `E` | Communication relationships between assets |
| `zone(v)`, `level(v)`, `type(v)` | An asset's IEC 62443 zone, Purdue level, asset class |
| `c(z_i, z_j)` | The conduit between two zones — the edges crossing that boundary |
| `Crit(v)` | Criticality score of asset v |
| `SL(v)` | Security Level component of criticality, from IEC 62443-3-3 |
| `Central(v)` | Graph-centrality component of criticality |
| `Damage(v)` | Share of operational process load the asset is responsible for |
| `P` | The set of attack paths, {P1, P2, P3} |
| `L` | Candidate deception locations — the *confirmed* subset of V after both filters. The optimizer's actual search space |
| `x_l` | Decision variable: 1 if a decoy is placed at location l |
| `x*` | The selected placement — the optimizer's answer |
| `F(x)` | The objective function being maximized |
| `α, β, γ, δ, ε` | Weights on coverage, earliness, criticality protection, risk, cost |
| `B` | Budget — maximum number of decoys |
| `Coverage(x)` | Fraction of paths in P intercepted by at least one decoy |
| `Early(x)` | Mean earliness of interception across intercepted paths |
| `CritProt(x)` | Criticality-weighted protection of path targets, normalized |
| `Risk(x)` | Estimated probability of legitimate OT traffic hitting a decoy |
| `Cost(x)` | Deployment cost — decoy count, or resource-weighted |

---

## 7. Stack and system terms

**NetworkX** — Python library for building and analyzing graphs. Where G lives in memory.

**SQLite** — a serverless, single-file relational database. Where G, L, P and computed results are stored.

**FastAPI** — Python web framework used for the backend API.

**Endpoint** — a single addressable operation in the API (`GET /candidates`, `POST /optimize`). The API contract is the list of endpoints and what each accepts and returns.

**Seed data** — the initial contents written into an empty database, defining the testbed's assets, edges, conduits and attack paths.

**React / Vite** — the JavaScript library and build tool used for the three UI screens.

**Ollama** — a tool for running language models locally, without a paid API. Used for the explanation layer, consistent with the brief's no-paid-API constraint.

**Phi-4-mini** — the small local model used for explanation. Chosen to fit available VRAM.

**Qwen3 14B** — the larger model used for the one-time, offline plausibility-scoring assist, run on Google Colab because it does not fit locally. Not part of the live system.

**iDECOP-ICS** — the prototype's name: *intelligent Deception Planning and Placement Optimization for Industrial Control Systems*. Names the artifact only — repository, application, UI header, Implementation chapter shorthand. The thesis title is unchanged. Lowercase `i` is deliberate, to avoid the string reading as IDEC, a Japanese PLC and HMI manufacturer.

---

## 8. Research-process terms

**Novelty claim** — the precise statement of what this work does that no published work does. Stated narrowly and defensibly, clause by clause, rather than broadly.

**Systematic review vs. broad search** — a systematic review follows a pre-registered, reproducible protocol across named databases. This project's literature work is a broad, persistent, multi-angle search across ten iterations. Both are legitimate; they are *different claims*, and the thesis says which one applies.

**Verification marker** — the status tag attached to every logged source: verified, named but unconfirmed, or needs a different access route. Prevents an unread abstract from being cited as if it were a read paper — a failure mode this project has already encountered once, with the Jay paper.

**Prior art** — existing published work that overlaps with a claimed contribution. The closest prior art here is Jay (2023).
