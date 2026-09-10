-- Seed data — transcribed exactly from 02-data-model.md's "Seed data" section.
-- The real 11-node testbed and 3 attack paths, not placeholders.

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
    (3, 2, (SELECT asset_id FROM assets WHERE name='Engineering WS-2'), 'Discovery', NULL, 'Network and remote system enumeration');

INSERT INTO candidate_locations (asset_id, passes_plausibility, detectability_risk, is_candidate, rationale) VALUES
    ((SELECT asset_id FROM assets WHERE name='Engineering WS-2'), 1, 0.2, 1, 'Standard deception target, precedent in HoneyPLC/Conpot'),
    ((SELECT asset_id FROM assets WHERE name='PLC-02'),           1, 0.2, 1, 'Standard deception target'),
    ((SELECT asset_id FROM assets WHERE name='HMI'),              1, 0.3, 1, 'Standard deception target'),
    ((SELECT asset_id FROM assets WHERE name='Historian'),        1, 0.3, 1, 'Collection-tactic relevance'),
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),      0, 0.0, 0, 'Fails plausibility — no realistic "decoy firewall"'),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),    1, 0.7, 1, 'Passes plausibility, down-weighted — most externally-scanned zone');

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
