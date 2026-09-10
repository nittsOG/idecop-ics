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

-- Candidate locations — L. The two-filter output from §4.
CREATE TABLE candidate_locations (
    asset_id                     INTEGER PRIMARY KEY REFERENCES assets(asset_id),
    criterion_decoy_exists       TEXT CHECK (criterion_decoy_exists IN ('yes','mostly','no')),
    criterion_attacker_reach     TEXT CHECK (criterion_attacker_reach IN ('yes','mostly','no')),
    criterion_useful_signal      TEXT CHECK (criterion_useful_signal IN ('yes','mostly','no')),
    criterion_reliable_indicator TEXT CHECK (criterion_reliable_indicator IN ('yes','mostly','no')),
    passes_plausibility          INTEGER NOT NULL CHECK (passes_plausibility IN (0,1)),  -- Filter 1
    detectability_risk           REAL DEFAULT 0.0,  -- Filter 2, 0 (safe) to 1 (trivially fingerprinted)
    is_candidate                 INTEGER NOT NULL CHECK (is_candidate IN (0,1)),  -- final L membership
    rationale                    TEXT,
    -- AI-suggested first pass (02-ai-role.md §7-10) — advisory only. The four
    -- criterion_* columns above are the ones the optimizer reads, and only
    -- get written once human_confirmed = 1. An unconfirmed suggestion here
    -- has no path into L.
    ai_suggested_decoy_exists       TEXT CHECK (ai_suggested_decoy_exists IN ('yes','mostly','no')),
    ai_suggested_attacker_reach     TEXT CHECK (ai_suggested_attacker_reach IN ('yes','mostly','no')),
    ai_suggested_useful_signal      TEXT CHECK (ai_suggested_useful_signal IN ('yes','mostly','no')),
    ai_suggested_reliable_indicator TEXT CHECK (ai_suggested_reliable_indicator IN ('yes','mostly','no')),
    ai_reasoning                    TEXT,
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
    method           TEXT NOT NULL CHECK (method IN ('random','centrality','proposed_greedy','proposed_milp')),
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

-- Candidate locations — the worked example from testbed-architecture.md, not every asset
INSERT INTO candidate_locations (asset_id, passes_plausibility, detectability_risk, is_candidate, rationale) VALUES
    ((SELECT asset_id FROM assets WHERE name='Engineering WS-2'), 1, 0.2, 1, 'Standard deception target, precedent in HoneyPLC/Conpot'),
    ((SELECT asset_id FROM assets WHERE name='PLC-02'),           1, 0.2, 1, 'Standard deception target'),
    ((SELECT asset_id FROM assets WHERE name='HMI'),              1, 0.3, 1, 'Standard deception target'),
    ((SELECT asset_id FROM assets WHERE name='Historian'),        1, 0.3, 1, 'Collection-tactic relevance'),
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),      0, 0.0, 0, 'Fails plausibility — no realistic "decoy firewall"'),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),    1, 0.7, 1, 'Passes plausibility, down-weighted — most externally-scanned zone');

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
| `/candidates` | GET | `L` with filter scores — what the optimizer actually searches over |
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
