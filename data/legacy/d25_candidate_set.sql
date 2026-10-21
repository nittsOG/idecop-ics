-- LEGACY — the candidate set that every result from D20 to D25 was measured on.
-- It was NOT produced by formal-problem-definition.md §4's filters (D25,
-- Finding 2): three of its five members were never scored through Filter 1,
-- and the other two only through demo data that D26 removed.
--
-- Load it only to reproduce numbers recorded in docs/00-decisions-log.md
-- before D26, on a database built from data/schema.sql and data/seed.sql:
--
--     conn.executescript(open("data/legacy/d25_candidate_set.sql").read())
--
-- The scripts then refuse to run unless given --legacy-d25, and they print a
-- banner saying the result is historical. The API never accepts this set.
-- Nothing here is an evaluation input.
--
-- Those numbers were measured on P1-P4, so this file also removes P5, which
-- D27 added after them.
DELETE FROM attack_path_steps WHERE path_id = (SELECT path_id FROM attack_paths WHERE name = 'P5');
DELETE FROM attack_paths WHERE name = 'P5';
-- They were also measured on the 14 connections recorded before D30, so this
-- file removes the four D30 added (G1-G4). The protocols D30 filled in and the
-- operating profile stay: no term of F reads them.
DELETE FROM edges WHERE edge_id IN (
    SELECT e.edge_id FROM edges e
    JOIN assets s ON s.asset_id = e.source_asset_id
    JOIN assets t ON t.asset_id = e.target_asset_id
    WHERE (s.name, t.name) IN (VALUES ('HMI', 'Historian'), ('Engineering WS', 'Historian'),
                                      ('HMI', 'PLC-03 (RTU)'), ('OT Firewall', 'Engineering WS-2')));
UPDATE candidate_locations SET passes_plausibility = 1, is_candidate = 1
WHERE asset_id IN (SELECT asset_id FROM assets WHERE name IN
    ('Engineering WS-2', 'PLC-02', 'HMI', 'Historian', 'DMZ Jump Host'));
