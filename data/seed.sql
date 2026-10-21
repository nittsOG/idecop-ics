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
    -- D28: T0832's tactic is Impact (sources.md 387). It was recorded as Inhibit
    -- Response Function until 12 October 2026. No term of F reads a tactic.
    (1, 5, (SELECT asset_id FROM assets WHERE name='HMI'),            'Impact', 'T0832', 'Manipulation of View'),
    -- D28: T0822 added at the user's choice, before any blind card was scored
    -- (sources.md 383; P5 step 1 uses it at the same asset). It read 'Network-perimeter entry'.
    (2, 1, (SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),  'Initial Access', 'T0822', 'External Remote Services'),
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

-- D30: eight of the nine blank protocols are filled from the operating profile
-- (below); the Attacker's connection has none.
-- No term of F reads a protocol; Screen 3's cards and the scoring prompt do.
INSERT INTO edges (source_asset_id, target_asset_id, protocol, weight) VALUES
    ((SELECT asset_id FROM assets WHERE name='Attacker'),          (SELECT asset_id FROM assets WHERE name='OT Firewall'),          NULL,      1.0),
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),       (SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),        'SSH over VPN', 1.0),
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),       (SELECT asset_id FROM assets WHERE name='Historian'),            'HTTPS',   1.0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),     (SELECT asset_id FROM assets WHERE name='Engineering WS'),       'RDP',     1.0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),     (SELECT asset_id FROM assets WHERE name='HMI'),                  'HTTP',    1.0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),     (SELECT asset_id FROM assets WHERE name='PLC-03 (RTU)'),         'IEC-104', 1.0),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),     (SELECT asset_id FROM assets WHERE name='Backup Control Switch'),'SSH',     0.5),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS'),    (SELECT asset_id FROM assets WHERE name='Engineering WS-2'),     'SMB',     0.5),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS'),    (SELECT asset_id FROM assets WHERE name='PLC-01'),               'S7comm',  1.0),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS-2'),  (SELECT asset_id FROM assets WHERE name='PLC-02'),               'S7comm',  0.5),
    ((SELECT asset_id FROM assets WHERE name='HMI'),               (SELECT asset_id FROM assets WHERE name='PLC-01'),               'Modbus',  1.0),
    ((SELECT asset_id FROM assets WHERE name='HMI'),               (SELECT asset_id FROM assets WHERE name='PLC-02'),               'Modbus',  1.0),
    ((SELECT asset_id FROM assets WHERE name='Backup Control Switch'), (SELECT asset_id FROM assets WHERE name='PLC-01'),           'Ethernet', 0.5),
    ((SELECT asset_id FROM assets WHERE name='Backup Control Switch'), (SELECT asset_id FROM assets WHERE name='PLC-02'),           'Ethernet', 0.5),
    -- D30: four connections the profile and the paths imply, appended so that the
    -- 14 rows above keep their edge_ids; data/legacy/d25_candidate_set.sql removes them.
    -- G1, the Historian's data source; G2, engineers' trend queries and P4's move;
    -- G3, the RTU's master; G4 (i), the firewall rule that P3's scan uses.
    ((SELECT asset_id FROM assets WHERE name='HMI'),               (SELECT asset_id FROM assets WHERE name='Historian'),            'OPC UA',  1.0),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS'),    (SELECT asset_id FROM assets WHERE name='Historian'),            'HTTPS',   1.0),
    ((SELECT asset_id FROM assets WHERE name='HMI'),               (SELECT asset_id FROM assets WHERE name='PLC-03 (RTU)'),         'IEC-104', 1.0),
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),       (SELECT asset_id FROM assets WHERE name='Engineering WS-2'),     NULL,      1.0);

-- Operating profile (D30). Facts about the plant as designed, drafted by Claude
-- from testbed-architecture.md, threat-attack-model.md and this file, and confirmed
-- by the user on 19 October 2026, before any blind card was scored on the fresh database.
-- Screen 3 shows it and the scoring prompt includes it, word for word. No
-- judgement about decoys and no rubric level belongs here. It freezes at the
-- first blind-card score on the fresh database.
INSERT INTO plant_facts (text) VALUES
    ('Operators watch the HMI around the clock. Engineers work weekday day shifts. Vendors connect only in maintenance windows agreed in advance.'),
    ('The plant runs no network scans of its own: its network monitoring is passive.'),
    ('External stands for the company''s office network and, beyond it, the internet. The Attacker node is the only modelled asset there.');

INSERT INTO asset_profiles (asset_id, role, runs, routine_activity) VALUES
    ((SELECT asset_id FROM assets WHERE name='OT Firewall'),
     'The perimeter firewall between the External zone and the OT DMZ. Its rules are that conduit.',
     'pfSense. It filters traffic between External and the OT DMZ, terminates the remote-access VPN, and has a web management interface. One rule, left over from an earlier setup, lets connections from outside reach Engineering WS-2 directly; no scheduled traffic uses it.',
     'Unsolicited scans and connection attempts from the internet, all day. VPN logins by engineers on working days and by vendors in maintenance windows, passed on to the DMZ Jump Host. Office users'' HTTPS requests passing through to the Historian, in working hours. Rare configuration changes, made at the firewall''s own console.'),
    ((SELECT asset_id FROM assets WHERE name='DMZ Jump Host'),
     'The plant''s entry point for remote work. Engineers and vendors log in here first, then open sessions into the plant. It also relays software updates into the plant.',
     'Linux with minimal services: an SSH server for logins, and the tools for onward sessions (a remote-desktop client, a web browser, an SSH client and an IEC-104 maintenance tool).',
     'Engineers'' remote logins over the VPN through the OT Firewall on working days, and vendors'' logins in maintenance windows. Onward remote-desktop sessions to the Engineering WS, and dashboard views of the HMI. The RTU vendor''s scheduled IEC-104 maintenance sessions to PLC-03 (RTU). Rare switch configuration sessions, and the quarterly failover test through the Backup Control Switch. Monthly software updates passing through to the plant.'),
    ((SELECT asset_id FROM assets WHERE name='Historian'),
     'Stores the plant''s process data over time and serves it to engineers and office users.',
     'A time-series database, with a web interface for trends and reports and a data-collection interface.',
     'Process values arriving from the HMI every few seconds. Engineers querying trends from the Engineering WS, in working hours. Office users viewing reports through the firewall, in working hours. A nightly archive job on the Historian itself.'),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS'),
     'Where engineers write PLC programs, download them to PLC-01 and change its parameters.',
     'Windows 10/11 with PLC engineering software. Its project files are shared with Engineering WS-2, and engineers query the Historian''s trends from it over HTTPS.',
     'Engineers'' logins, local and remote, on working days. Program downloads and parameter changes to PLC-01, in maintenance windows. A weekly backup of PLC-01''s program, uploaded to this workstation. Monthly operating-system and engineering-software updates, brought in through the DMZ Jump Host.'),
    ((SELECT asset_id FROM assets WHERE name='Engineering WS-2'),
     'A second engineering workstation in the same zone, used for PLC-02.',
     'Windows 10/11 with the same PLC engineering software as the Engineering WS.',
     'Engineers'' local logins on working days, less often than on the Engineering WS, mainly when PLC-02 needs changes. Program downloads and parameter changes to PLC-02, in maintenance windows. A weekly backup of PLC-02''s program, uploaded to this workstation. Project files and monthly operating-system and engineering-software updates, copied from the Engineering WS. A firewall rule, left over from an earlier setup, lets connections from outside reach this workstation directly; no scheduled traffic uses it.'),
    ((SELECT asset_id FROM assets WHERE name='HMI'),
     'The operators'' screens. They show process values and let operators change setpoints.',
     'A Node-RED dashboard, served over HTTP. It forwards process values to the Historian every few seconds, over OPC UA.',
     'Operators at the console around the clock. Engineers viewing the dashboard through the jump host. Replies to its own polling of PLC-01 and PLC-02 every second over Modbus, and of PLC-03 (RTU) over IEC-104.'),
    ((SELECT asset_id FROM assets WHERE name='PLC-01'),
     'Controls part of the simulated process.',
     'OpenPLC.',
     'Modbus polling by the HMI every second, around the clock. Program downloads and parameter changes from the Engineering WS, in maintenance windows. A weekly upload of its program to the Engineering WS, as a backup. Traffic through the Backup Control Switch only in the quarterly failover test, from the DMZ Jump Host.'),
    ((SELECT asset_id FROM assets WHERE name='PLC-02'),
     'A second controller of the same kind as PLC-01, controlling another part of the simulated process.',
     'OpenPLC.',
     'Modbus polling by the HMI every second, around the clock. Program downloads and parameter changes from Engineering WS-2, in maintenance windows. A weekly upload of its program to Engineering WS-2, as a backup. Traffic through the Backup Control Switch only in the quarterly failover test, from the DMZ Jump Host.'),
    ((SELECT asset_id FROM assets WHERE name='PLC-03 (RTU)'),
     'A remote terminal unit at a substation-type site. It reports measurements and operates circuit breakers on command.',
     'IEC-104 outstation firmware.',
     'The HMI''s IEC-104 polling and the RTU''s own spontaneous reports, around the clock. Clock-synchronisation commands from its master, which IEC-104 includes. The RTU vendor''s scheduled maintenance sessions through the jump host.'),
    ((SELECT asset_id FROM assets WHERE name='Backup Control Switch'),
     'A managed switch giving a second network route into the Control LAN, to PLC-01 and PLC-02.',
     'Managed-switch firmware with an SSH management interface.',
     'Rare administrator configuration sessions through the jump host. It carries traffic only in the quarterly failover test, when an engineer on the DMZ Jump Host connects through it to PLC-01 and PLC-02.');
