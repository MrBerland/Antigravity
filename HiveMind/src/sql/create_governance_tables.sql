-- Governance Rules Table
-- Manually overrides the AI for specific senders or domains.

CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.dim_governance_rules` (
    rule_id STRING,
    rule_type STRING,      -- 'ALLOW', 'BLOCK', 'QUARANTINE'
    match_type STRING,     -- 'EXACT_EMAIL', 'DOMAIN_WILDCARD'
    pattern STRING,        -- 'tim@augos.io' or 'marketing.tajhotels.com'
    added_by STRING,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    notes STRING
);

-- Seed some obvious Block patterns (Marketing)
INSERT INTO `augos-core-data.hive_mind_core.dim_governance_rules` 
(rule_id, rule_type, match_type, pattern, added_by, notes)
VALUES 
    (GENERATE_UUID(), 'BLOCK', 'DOMAIN_WILDCARD', 'tajhotels.com', 'system', 'Marketing Spam'),
    (GENERATE_UUID(), 'BLOCK', 'DOMAIN_WILDCARD', 'zohocalendar.com', 'system', 'Automated Calendar Notifications'),
    (GENERATE_UUID(), 'ALLOW', 'DOMAIN_WILDCARD', 'augos.io', 'system', 'Internal Domain');
