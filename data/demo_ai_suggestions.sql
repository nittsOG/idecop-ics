-- NOT part of 02-data-model.md's canonical seed data — this populates the
-- ai_suggested_* / human_confirmed columns for Screen 3 demo purposes only,
-- using the exact worked examples already reasoned through in
-- 02-ai-role.md §10 (OT Firewall, Engineering WS-2) and the plausibility
-- review mockup (DMZ Jump Host, the "edited" example). Nothing here invents
-- new judgments — it transcribes ones already made in those documents.

UPDATE candidate_locations
SET ai_suggested_decoy_exists = 'yes',
    ai_suggested_attacker_reach = 'yes',
    ai_suggested_useful_signal = 'yes',
    ai_suggested_reliable_indicator = 'yes',
    ai_reasoning = 'P3''s reconnaissance sweep resolves to this workstation rather than the primary one (D19) — a discovery-stage scan plausibly lands on whichever workstation is reachable, not necessarily the targeted one; a parallel decoy workstation is directly precedented by existing honeypot tooling.',
    criterion_decoy_exists = 'yes', criterion_attacker_reach = 'yes',
    criterion_useful_signal = 'yes', criterion_reliable_indicator = 'yes',
    human_confirmed = 1, confirmed_at = CURRENT_TIMESTAMP
WHERE asset_id = (SELECT asset_id FROM assets WHERE name = 'Engineering WS-2');

UPDATE candidate_locations
SET ai_suggested_decoy_exists = 'no',
    ai_reasoning = 'A firewall is functional infrastructure an attacker routes through, not a target it interacts with. Fails Filter 1 on the first criterion.',
    criterion_decoy_exists = 'no',
    human_confirmed = 1, confirmed_at = CURRENT_TIMESTAMP
WHERE asset_id = (SELECT asset_id FROM assets WHERE name = 'OT Firewall');

UPDATE candidate_locations
SET ai_suggested_decoy_exists = 'yes', ai_suggested_attacker_reach = 'yes',
    ai_suggested_useful_signal = 'yes', ai_suggested_reliable_indicator = 'mostly',
    ai_reasoning = 'AI suggested "mostly reliable" — overridden after review, given the DMZ''s exposure to routine external scanning noise.',
    criterion_decoy_exists = 'yes', criterion_attacker_reach = 'yes',
    criterion_useful_signal = 'yes', criterion_reliable_indicator = 'no',
    human_confirmed = 1, confirmed_at = CURRENT_TIMESTAMP
WHERE asset_id = (SELECT asset_id FROM assets WHERE name = 'DMZ Jump Host');
