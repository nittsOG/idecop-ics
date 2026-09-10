-- Schema — transcribed exactly from 02-data-model.md. If this ever needs to
-- change, change it there first; this file should always match that document.

CREATE TABLE zones (
    zone_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL UNIQUE,
    purdue_level TEXT NOT NULL
);

CREATE TABLE conduits (
    conduit_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_a_id   INTEGER NOT NULL REFERENCES zones(zone_id),
    zone_b_id   INTEGER NOT NULL REFERENCES zones(zone_id),
    description TEXT
);

CREATE TABLE assets (
    asset_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,
    zone_id       INTEGER NOT NULL REFERENCES zones(zone_id),
    purdue_level  TEXT NOT NULL,
    asset_type    TEXT NOT NULL,
    is_physical   INTEGER NOT NULL DEFAULT 1 CHECK (is_physical IN (0,1)),
    sl_vector     TEXT,
    sl_aggregate  REAL,
    central_score REAL,
    damage_score  REAL,
    criticality   REAL,
    notes         TEXT
);

CREATE TABLE edges (
    edge_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_asset_id  INTEGER NOT NULL REFERENCES assets(asset_id),
    target_asset_id  INTEGER NOT NULL REFERENCES assets(asset_id),
    protocol         TEXT,
    weight           REAL DEFAULT 1.0
);

CREATE TABLE candidate_locations (
    asset_id                     INTEGER PRIMARY KEY REFERENCES assets(asset_id),
    criterion_decoy_exists       TEXT CHECK (criterion_decoy_exists IN ('yes','mostly','no')),
    criterion_attacker_reach     TEXT CHECK (criterion_attacker_reach IN ('yes','mostly','no')),
    criterion_useful_signal      TEXT CHECK (criterion_useful_signal IN ('yes','mostly','no')),
    criterion_reliable_indicator TEXT CHECK (criterion_reliable_indicator IN ('yes','mostly','no')),
    passes_plausibility          INTEGER NOT NULL CHECK (passes_plausibility IN (0,1)),
    detectability_risk           REAL DEFAULT 0.0,
    is_candidate                 INTEGER NOT NULL CHECK (is_candidate IN (0,1)),
    rationale                    TEXT,
    ai_suggested_decoy_exists       TEXT CHECK (ai_suggested_decoy_exists IN ('yes','mostly','no')),
    ai_suggested_attacker_reach     TEXT CHECK (ai_suggested_attacker_reach IN ('yes','mostly','no')),
    ai_suggested_useful_signal      TEXT CHECK (ai_suggested_useful_signal IN ('yes','mostly','no')),
    ai_suggested_reliable_indicator TEXT CHECK (ai_suggested_reliable_indicator IN ('yes','mostly','no')),
    ai_reasoning                    TEXT,
    human_confirmed                 INTEGER NOT NULL DEFAULT 0 CHECK (human_confirmed IN (0,1)),
    confirmed_at                    TEXT
);

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
    technique_id   TEXT,
    technique_name TEXT,
    UNIQUE(path_id, step_order)
);

CREATE TABLE placement_runs (
    run_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    method           TEXT NOT NULL CHECK (method IN ('random','centrality','proposed_greedy','proposed_milp')),
    alpha REAL, beta REAL, gamma REAL, delta REAL, epsilon REAL,
    budget           INTEGER NOT NULL,
    coverage_score   REAL,
    early_score      REAL,
    critprot_score   REAL,
    risk_score       REAL,
    cost_score       REAL,
    objective_value  REAL,
    runtime_seconds  REAL,
    run_timestamp    TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE placements (
    placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id       INTEGER NOT NULL REFERENCES placement_runs(run_id),
    asset_id     INTEGER NOT NULL REFERENCES candidate_locations(asset_id),
    decoy_type   TEXT
);

CREATE TABLE explanations (
    explanation_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id              INTEGER NOT NULL REFERENCES placement_runs(run_id),
    explanation_text     TEXT NOT NULL,
    model_used           TEXT,
    generated_timestamp  TEXT DEFAULT CURRENT_TIMESTAMP
);
