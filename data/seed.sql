-- Seed data. Originally transcribed from 02-data-model.md's "Seed data" section;
-- this file has been canonical since D19, and that section carries a note on
-- what it has not tracked.
-- The real 11-node testbed and 5 attack paths (P4 added by D21, P5 by D27), not placeholders.

INSERT INTO zones (name, purdue_level) VALUES
    ('External', '—'),
    ('OT DMZ', '3.5'),
    ('Supervisory', '3'),
    ('Control', '1-2'),
    ('Process', '—');

INSERT INTO assets (name, zone_id, purdue_level, asset_type, is_physical) VALUES
    ('Attacker',             1, '—',   'Attacker',                1),
    ('OT Firewall',          2, '3.5', 'Firewall',                1),
    ('DMZ Jump Host',        2, '3.5', 'Jump Server',             1),
    ('Historian',            2, '3.5', 'Historian',               0),
    ('Engineering WS',       3, '3',   'Engineering Workstation', 1),
    ('Engineering WS-2',     3, '3',   'Engineering Workstation', 0),
    ('HMI',                  3, '2-3', 'HMI',                     1),
    ('PLC-01',               4, '1-2', 'PLC',                     1),
    ('PLC-02',               4, '1-2', 'PLC',                     1),
    ('PLC-03 (RTU)',         4, '1-2', 'PLC',                     0),
    ('Backup Control Switch',4, '1-2', 'Switch',                  0);

INSERT INTO attack_paths (name, description) VALUES
    ('P1', 'Stuxnet-class: engineering-workflow-mediated physical sabotage'),
    ('P2', 'Industroyer2-class: protocol-specific direct grid impact'),
    ('P3', 'Reconnaissance-only: early-detection stress test'),
    ('P4', 'Dragonfly-class: ICS data collection for later operations'),
    ('P5', 'Backup-conduit: network-device compromise, alternate route to PLC-01');

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
    (3, 2, (SELECT asset_id FROM assets WHERE name='Engineering WS-2'), 'Discovery', NULL, 'Network and remote system enumeration'),
    -- P4 added by D21. T0811 verified at attack.mitre.org/techniques/T0811/ —
    -- Collection tactic, and its Targeted Assets list names A0006 Data Historian
    -- explicitly. Procedure example: Dragonfly 2.0 accessed servers holding ICS
    -- reference documents, wiring diagrams and panel layouts.
    (4, 1, (SELECT asset_id FROM assets WHERE name='Engineering WS'), 'Initial Access', 'T0862', 'Supply Chain Compromise'),
    (4, 2, (SELECT asset_id FROM assets WHERE name='Historian'),      'Collection', 'T0811', 'Data from Information Repositories'),
    (4, 3, (SELECT asset_id FROM assets WHERE name='Engineering WS'), 'Collection', 'T0811', 'Data from Information Repositories'),
    -- P5 added by D27. Every technique verified at attack.mitre.org on 4 October 2026
    -- (sources.md 377-383). The route follows the testbed's own edges, and the
    -- target is PLC-01 because the backup switch exists to test "both routes to
    -- the same target" (testbed-architecture.md); P1 reaches PLC-01 the primary way.
    (5, 1, (SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),         'Initial Access', 'T0822', 'External Remote Services'),
    (5, 2, (SELECT asset_id FROM assets WHERE name='Backup Control Switch'), 'Lateral Movement', 'T0866', 'Exploitation of Remote Services'),
    (5, 3, (SELECT asset_id FROM assets WHERE name='Backup Control Switch'), 'Discovery', 'T0842', 'Network Sniffing'),
    (5, 4, (SELECT asset_id FROM assets WHERE name='PLC-01'),                'Impair Process Control', 'T0836', 'Modify Parameter');

-- detectability_risk values derived by the Filter 2 rubric (D22), not assigned
-- by judgement. risk = 0.4*Exposure + 0.3*ProbingDepth + 0.3*ArtifactSurface.
-- Per-candidate factor scores and their sources: docs/02-detectability-rubric.md
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
