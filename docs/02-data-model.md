# Data Model — SQLite Schema for G, L, P, and Computed Scores

Turns the mathematical objects in `formal-problem-definition.md` into an actual schema, populated with the real testbed from `testbed-architecture.md` and the real attack paths from `threat-attack-model.md` — not a generic example. Every table maps to a specific section of the formal problem definition; that mapping is called out explicitly so nothing here is inventing structure the math didn't already define.

## Design principles

- **One row per formal object.** `assets` is `V`, `edges` is `E`, `candidate_locations` is the output of Section 4's two filters, `attack_paths`/`attack_path_steps` is `P`. No table exists that doesn't correspond to something already defined.
- **Computed scores are stored, not just derivable.** `criticality`, the filter outcomes, and every run's metrics get persisted columns rather than being recomputed on every read — this project's testbed is small enough that recomputation would be cheap, but persisting makes the evaluation methodology (Phase D) able to query historical runs directly instead of re-running the optimizer to compare methods.
- **Every optimizer run is a row, not an overwrite.** `placement_runs` supports exactly what Section 7's baseline comparison needs: Random, Centrality, and Proposed all coexist in the same table, distinguished by `method`, so Phase D's comparison queries are simple `WHERE` clauses, not separate exports.

## Schema

```sql
-- Zones (IEC 62443 zone/conduit structure — formal-problem-definition.md §1)
CREATE TABLE zones (
    zone_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL UNIQUE,
    purdue_level TEXT NOT NULL
);

-- Conduits c(z_i, z_j) — permitted communication between zone pairs
CREATE TABLE conduits (
    conduit_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_a_id   INTEGER NOT NULL REFERENCES zones(zone_id),
    zone_b_id   INTEGER NOT NULL REFERENCES zones(zone_id),
    description TEXT
);

-- Assets — V. zone(v), level(v), type(v) from §1, plus Crit(v) from §2.
CREATE TABLE assets (
    asset_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,
    zone_id       INTEGER NOT NULL REFERENCES zones(zone_id),
    purdue_level  TEXT NOT NULL,
    asset_type    TEXT NOT NULL,           -- 'PLC','HMI','Engineering Workstation','Firewall','Historian','Jump Server','Switch','Attacker'
    is_physical   INTEGER NOT NULL DEFAULT 1 CHECK (is_physical IN (0,1)),
    sl_vector     TEXT,                    -- JSON array [FR1..FR7], each 0-4 (§2, source #267)
    sl_aggregate  REAL,                    -- SL(v), normalized 0-1
    central_score REAL,                    -- Central(v), betweenness by default (§7 baseline)
    damage_score  REAL,                    -- Damage(v), 0-1, elicited during testbed design
    criticality   REAL,                    -- Crit(v) = w1*sl_aggregate + w2*central_score*damage_score
    notes         TEXT
);

-- Edges — E. protocol(e), weight(e) from §1.
CREATE TABLE edges (
    edge_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_asset_id  INTEGER NOT NULL REFERENCES assets(asset_id),
    target_asset_id  INTEGER NOT NULL REFERENCES assets(asset_id),
    protocol         TEXT,
    weight           REAL DEFAULT 1.0
);

-- Candidate locations — L. The two-filter output from §4. Rewritten by D26:
-- four-level scale, blind cards, the reviewer's reason, the AI model's identity,
-- and a NULL (not 0.0) detectability score when Filter 2 has not been applied.
CREATE TABLE candidate_locations (
    asset_id                     INTEGER PRIMARY KEY REFERENCES assets(asset_id),
    -- Filter 1 (formal-problem-definition.md §4, D26): four-level scale from
    -- sources.md #40, scored in order. The first 'no' ends the card, so the
    -- criteria after it stay NULL. Only a human confirmation writes these.
    criterion_decoy_exists       TEXT CHECK (criterion_decoy_exists IN ('yes','mostly_yes','mostly_no','no')),
    criterion_attacker_reach     TEXT CHECK (criterion_attacker_reach IN ('yes','mostly_yes','mostly_no','no')),
    criterion_useful_signal      TEXT CHECK (criterion_useful_signal IN ('yes','mostly_yes','mostly_no','no')),
    criterion_reliable_indicator TEXT CHECK (criterion_reliable_indicator IN ('yes','mostly_yes','mostly_no','no')),
    passes_plausibility          INTEGER NOT NULL DEFAULT 0 CHECK (passes_plausibility IN (0,1)),
    -- Filter 2 (D22a): 0 (safe) to 1 (trivially fingerprinted). NULL means not yet
    -- scored; the candidate loader refuses a candidate without a score (D26).
    detectability_risk           REAL,
    is_candidate                 INTEGER NOT NULL DEFAULT 0 CHECK (is_candidate IN (0,1)),
    rationale                    TEXT,   -- design-time note only; not shown during review (D26)
    blind_first                  INTEGER NOT NULL DEFAULT 0 CHECK (blind_first IN (0,1)),  -- D26 blind card
    -- D26: a blind card's FIRST confirmed answers, written once and never changed,
    -- so the AI-agreement measure cannot be overwritten after the AI's answer is shown.
    blind_decoy_exists           TEXT CHECK (blind_decoy_exists IN ('yes','mostly_yes','mostly_no','no')),
    blind_attacker_reach         TEXT CHECK (blind_attacker_reach IN ('yes','mostly_yes','mostly_no','no')),
    blind_useful_signal          TEXT CHECK (blind_useful_signal IN ('yes','mostly_yes','mostly_no','no')),
    blind_reliable_indicator     TEXT CHECK (blind_reliable_indicator IN ('yes','mostly_yes','mostly_no','no')),
    blind_reason                 TEXT,
    blind_confirmed_at           TEXT,
    ai_suggested_decoy_exists       TEXT CHECK (ai_suggested_decoy_exists IN ('yes','mostly_yes','mostly_no','no')),
    ai_suggested_attacker_reach     TEXT CHECK (ai_suggested_attacker_reach IN ('yes','mostly_yes','mostly_no','no')),
    ai_suggested_useful_signal      TEXT CHECK (ai_suggested_useful_signal IN ('yes','mostly_yes','mostly_no','no')),
    ai_suggested_reliable_indicator TEXT CHECK (ai_suggested_reliable_indicator IN ('yes','mostly_yes','mostly_no','no')),
    ai_reasoning                    TEXT,
    ai_model                        TEXT,   -- model id and revision behind the suggestion (D26)
    human_reason                    TEXT,   -- the reviewer's reason (D26)
    human_confirmed                 INTEGER NOT NULL DEFAULT 0 CHECK (human_confirmed IN (0,1)),
    confirmed_at                    TEXT
);

-- Attack paths — P (formal-problem-definition.md §3, formalized in threat-attack-model.md)
CREATE TABLE attack_paths (
    path_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE attack_path_steps (
    step_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    path_id        INTEGER NOT NULL REFERENCES attack_paths(path_id),
    step_order     INTEGER NOT NULL,
    asset_id       INTEGER NOT NULL REFERENCES assets(asset_id),
    tactic         TEXT NOT NULL,
    technique_id   TEXT,          -- e.g. 'T0836' — verified IDs from threat-attack-model.md
    technique_name TEXT,
    UNIQUE(path_id, step_order)
);

-- One row per optimizer run — supports §7's three-method comparison directly
CREATE TABLE placement_runs (
    run_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    method           TEXT NOT NULL CHECK (method IN ('random','centrality','proposed_greedy','proposed_distorted_greedy','proposed_milp')),   -- distorted greedy added in D23
    alpha REAL, beta REAL, gamma REAL, delta REAL, epsilon REAL,  -- §5 objective weights used this run
    budget           INTEGER NOT NULL,          -- B, §6
    coverage_score   REAL,                      -- Coverage(x)
    early_score      REAL,                      -- Early(x)
    critprot_score   REAL,                      -- CritProt(x)
    risk_score       REAL,                      -- Risk(x)
    cost_score       REAL,                      -- Cost(x)
    objective_value  REAL,                      -- F(x)
    runtime_seconds  REAL,
    run_timestamp    TEXT DEFAULT CURRENT_TIMESTAMP
);

-- x* for a given run — which candidate locations got a decoy
CREATE TABLE placements (
    placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id       INTEGER NOT NULL REFERENCES placement_runs(run_id),
    asset_id     INTEGER NOT NULL REFERENCES candidate_locations(asset_id),
    decoy_type   TEXT   -- 'decoy PLC','honey credentials', etc. — original brief §6
);

-- AI-layer output — secondary RQ, formal-problem-definition.md §8
CREATE TABLE explanations (
    explanation_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id             INTEGER NOT NULL REFERENCES placement_runs(run_id),
    explanation_text    TEXT NOT NULL,
    model_used          TEXT,          -- e.g. 'llama3:8b via Ollama'
    generated_timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## Seed data — the actual testbed, not a placeholder

Populated directly from `testbed-architecture.md`'s 11-node graph and `threat-attack-model.md`'s three paths, so this schema is testable the moment it's created rather than needing data invented later.

> ⚠️ **`data/seed.sql` is the canonical seed, and parts of this section are stale.** This section is the Phase B transcription. It was not kept in step with three later changes:
> - D19 moved P3's step 2 from the HMI to Engineering WS-2;
> - D21 added P4, and D27 added P5;
> - D22/D22a replaced the detectability values.
>
> D26 brought the `candidate_locations` block back into line. The other differences remain, and `seed.sql` holds the current values.

```sql
INSERT INTO zones (name, purdue_level) VALUES
    ('External', '—'),
    ('OT DMZ', '3.5'),
    ('Supervisory', '3'),
    ('Control', '1-2'),
    ('Process', '—');

INSERT INTO assets (name, zone_id, purdue_level, asset_type, is_physical) VALUES
    ('Attacker',            1, '—',   'Attacker',               1),
    ('OT Firewall',         2, '3.5', 'Firewall',               1),
    ('DMZ Jump Host',       2, '3.5', 'Jump Server',            1),
    ('Historian',           2, '3.5', 'Historian',              0),  -- modeled-only
    ('Engineering WS',      3, '3',   'Engineering Workstation',1),
    ('Engineering WS-2',    3, '3',   'Engineering Workstation',0),  -- modeled-only
    ('HMI',                 3, '2-3', 'HMI',                    1),
    ('PLC-01',              4, '1-2', 'PLC',                    1),
    ('PLC-02',              4, '1-2', 'PLC',                    1),
    ('PLC-03 (RTU)',        4, '1-2', 'PLC',                    0),  -- modeled-only, IEC-104
    ('Backup Control Switch',4,'1-2', 'Switch',                 0);  -- modeled-only

-- Attack paths, per threat-attack-model.md — technique IDs verified against attack.mitre.org
INSERT INTO attack_paths (name, description) VALUES
    ('P1', 'Stuxnet-class: engineering-workflow-mediated physical sabotage'),
    ('P2', 'Industroyer2-class: protocol-specific direct grid impact'),
    ('P3', 'Reconnaissance-only: early-detection stress test');

INSERT INTO attack_path_steps (path_id, step_order, asset_id, tactic, technique_id, technique_name) VALUES
    (1, 1, (SELECT asset_id FROM assets WHERE name='Engineering WS'), 'Initial Access', 'T1091', 'Replication Through Removable Media'),
    (1, 2, (SELECT asset_id FROM assets WHERE name='Engineering WS'), 'Execution', 'T1203', 'Exploitation for Client Execution'),
    (1, 3, (SELECT asset_id FROM assets WHERE name='PLC-01'),         'Lateral Movement', NULL, 'Program download to PLC'),
    (1, 4, (SELECT asset_id FROM assets WHERE name='PLC-01'),         'Impair Process Control', 'T0836', 'Modify Parameter'),
    (1, 5, (SELECT asset_id FROM assets WHERE name='HMI'),            'Inhibit Response Function', 'T0832', 'Manipulation of View'),
    (2, 1, (SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),  'Initial Access', NULL, 'Network-perimeter entry'),
    (2, 2, (SELECT asset_id FROM assets WHERE name='PLC-03 (RTU)'),   'Execution', NULL, 'IEC-104 protocol-specific module'),
    (2, 3, (SELECT asset_id FROM assets WHERE name='PLC-03 (RTU)'),   'Impair Process Control', 'T0836', 'Modify Parameter'),
    (2, 4, (SELECT asset_id FROM assets WHERE name='PLC-03 (RTU)'),   'Impair Process Control', 'T0806', 'Brute Force I/O'),
    (3, 1, (SELECT asset_id FROM assets WHERE name='OT Firewall'),    'Initial Access', NULL, 'External scan / perimeter probe'),
    (3, 2, (SELECT asset_id FROM assets WHERE name='HMI'),            'Discovery', NULL, 'Network and remote system enumeration');

-- Candidate locations (D26). One row per asset except the Attacker node, so
-- that Screen 3 lists every asset (A32). Every row starts unscored and outside
-- L: Filter 1 scores come only from a human review in Screen 3, and nothing
-- here sets is_candidate. Until that review, L is empty and the scripts refuse
-- to run. To reproduce numbers recorded before D26, see
-- data/legacy/d25_candidate_set.sql.
--
-- detectability_risk holds Filter 2 scores (02-detectability-rubric.md, D22a)
-- where they exist. NULL means not yet scored: A32 step 4 scores every asset
-- that passes Filter 1. The OT Firewall's former 0.0 was a placeholder for
-- "fails plausibility", not a D22a score, so it is NULL now.
--
-- blind_first marks the three blind cards, drawn before any AI output existed:
-- random.Random(20261003).sample over the eight non-Attacker assets on a
-- modelled path, sorted by name (CPython 3.11). Result: DMZ Jump Host,
-- Historian, PLC-03 (RTU). See D26. The draw predates P5 (D27), which put the
-- Backup Control Switch on a path; it stands, as D27 explains.
INSERT INTO candidate_locations (asset_id, detectability_risk, blind_first) VALUES
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),           NULL, 0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),         0.69, 1),
    ((SELECT asset_id FROM assets WHERE name='Historian'),             0.69, 1),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS'),        NULL, 0),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS-2'),      0.56, 0),
    ((SELECT asset_id FROM assets WHERE name='HMI'),                   0.62, 0),
    ((SELECT asset_id FROM assets WHERE name='PLC-01'),                NULL, 0),
    ((SELECT asset_id FROM assets WHERE name='PLC-02'),                0.62, 0),
    ((SELECT asset_id FROM assets WHERE name='PLC-03 (RTU)'),          NULL, 1),
    ((SELECT asset_id FROM assets WHERE name='Backup Control Switch'), NULL, 0);

-- Conduits and edges — added after a genuine gap was found while building the
-- actual database: this section didn't exist before, and without it the
-- graph has zero connectivity (Central(v) is undefined with no edges at all).
-- Derived directly from testbed-architecture.md's zone diagram and the two
-- attack paths that specify real traversals (P1, P2) — not invented.

INSERT INTO conduits (zone_a_id, zone_b_id, description) VALUES
    ((SELECT zone_id FROM zones WHERE name='External'),    (SELECT zone_id FROM zones WHERE name='OT DMZ'),      'Firewall rules'),
    ((SELECT zone_id FROM zones WHERE name='OT DMZ'),      (SELECT zone_id FROM zones WHERE name='Supervisory'), 'DMZ→Supervisory rules'),
    ((SELECT zone_id FROM zones WHERE name='Supervisory'), (SELECT zone_id FROM zones WHERE name='Control'),     'Supervisory→Control rules — the critical boundary');

INSERT INTO edges (source_asset_id, target_asset_id, protocol, weight) VALUES
    ((SELECT asset_id FROM assets WHERE name='Attacker'),          (SELECT asset_id FROM assets WHERE name='OT Firewall'),          NULL,      1.0),
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),       (SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),        NULL,      1.0),
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),       (SELECT asset_id FROM assets WHERE name='Historian'),            NULL,      1.0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),     (SELECT asset_id FROM assets WHERE name='Engineering WS'),       NULL,      1.0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),     (SELECT asset_id FROM assets WHERE name='HMI'),                  NULL,      1.0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),     (SELECT asset_id FROM assets WHERE name='PLC-03 (RTU)'),         'IEC-104', 1.0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),     (SELECT asset_id FROM assets WHERE name='Backup Control Switch'),NULL,      0.5),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS'),    (SELECT asset_id FROM assets WHERE name='Engineering WS-2'),     NULL,      0.5),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS'),    (SELECT asset_id FROM assets WHERE name='PLC-01'),               'S7comm',  1.0),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS-2'),  (SELECT asset_id FROM assets WHERE name='PLC-02'),               'S7comm',  0.5),
    ((SELECT asset_id FROM assets WHERE name='HMI'),               (SELECT asset_id FROM assets WHERE name='PLC-01'),               'Modbus',  1.0),
    ((SELECT asset_id FROM assets WHERE name='HMI'),               (SELECT asset_id FROM assets WHERE name='PLC-02'),               'Modbus',  1.0),
    ((SELECT asset_id FROM assets WHERE name='Backup Control Switch'), (SELECT asset_id FROM assets WHERE name='PLC-01'),           NULL,      0.5),
    ((SELECT asset_id FROM assets WHERE name='Backup Control Switch'), (SELECT asset_id FROM assets WHERE name='PLC-02'),           NULL,      0.5);
```

## API contract — how FastAPI reads and writes this

| Endpoint | Method | Purpose |
|---|---|---|
| `/graph` | GET | Full `G` — assets + edges as JSON, for the Cytoscape.js/React Flow frontend |
| `/candidates` | GET | Every asset's Filter 1 review state, with its attack-path steps. On an unconfirmed blind card the AI's answer is withheld (D26). `L` is the confirmed subset that passes Filter 1 and has a Filter 2 score |
| `/candidates/{id}/confirm` | POST | The reviewer's four answers and reason; applies the rules in `src/plausibility` (D26) |
| `/attack-paths` | GET | `P` with all steps |
| `/assets/{id}/damage-score` | PUT | Set `Damage(v)` manually during testbed design (§2 — elicited, not computed) |
| `/optimize` | POST | Body: `{method, alpha..epsilon, budget}`. Runs the optimizer, writes a `placement_runs` row + `placements` rows, returns the result |
| `/runs` | GET | List all runs — this is the query Phase D's baseline comparison reads from directly |
| `/runs/{id}` | GET | Full detail: metrics + which assets got decoys |
| `/runs/{id}/explain` | POST | Triggers the Ollama call per `formal-problem-definition.md` §8, writes an `explanations` row |

`/optimize` is the only endpoint that writes to `placement_runs`/`placements` — everything else is read-only or, for damage-score, a narrow single-field write. Keeping writes concentrated in one place matches the "optimizer decides deterministically" principle from the AI philosophy (original brief §9, `00-decisions-log.md` D6): the API surface itself enforces that placement decisions only ever come from one code path, not from several places that could disagree.

## What This Enables Next

- **Optimization formulation, detailed** — the actual greedy/MILP pseudocode that populates `placement_runs`, referencing this schema's exact column names
- **AI role, detailed** — the prompt template for `/runs/{id}/explain`, structured around exactly the columns `placement_runs` and `placements` expose
- **Prototype architecture, detailed** — module boundaries between the FastAPI layer above and the NetworkX/optimizer code that reads and writes it
