-- =============================================================================
-- create_processor.sql
-- =============================================================================
-- Layer 1 processor: applies deterministic governance rules to staging emails.
--
-- This procedure handles ONLY Layer 1 (rule-based, free, instant).
-- Layer 2 (AI classification via Gemini) is handled by:
--   hivemind_pipeline.py  →  run_classifier.py --layer2
--
-- Called by:
--   python3 HiveMind/src/sql/run_classifier.py --layer1
-- =============================================================================

CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.process_staging_data`()
BEGIN

    -- ── 0. BLOCK: match governance rules with rule_type = 'BLOCK' ────────────
    UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` t
    SET
        security_verdict  = 'BLOCK',
        processing_status = 'CLASSIFIED_L1',
        ai_category       = 'RULE_BLOCKED'
    FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
    WHERE t.processing_status = 'PENDING'
      AND t.ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)  -- Streaming buffer safety
      AND r.rule_type = 'BLOCK'
      AND (
          (r.match_type = 'EXACT_EMAIL'     AND LOWER(t.sender) LIKE CONCAT('%<', LOWER(r.pattern), '>'))
          OR
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(t.sender) LIKE CONCAT('%', LOWER(r.pattern), '%'))
      );

    -- ── 1. MARKETING: newsletters, promos, known marketing platforms ─────────
    UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` t
    SET
        security_verdict  = 'MARKETING',
        processing_status = 'CLASSIFIED_L1',
        ai_category       = 'RULE_MARKETING'
    FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
    WHERE t.processing_status = 'PENDING'
      AND t.ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
      AND r.rule_type = 'MARKETING'
      AND (
          (r.match_type = 'EXACT_EMAIL'     AND LOWER(t.sender) LIKE CONCAT('%<', LOWER(r.pattern), '>'))
          OR
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(t.sender) LIKE CONCAT('%', LOWER(r.pattern), '%'))
      );

    -- ── 2. PERSONAL: personal email providers ────────────────────────────────
    UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` t
    SET
        security_verdict  = 'PERSONAL',
        processing_status = 'CLASSIFIED_L1',
        ai_category       = 'RULE_PERSONAL'
    FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
    WHERE t.processing_status = 'PENDING'
      AND t.ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
      AND r.rule_type = 'PERSONAL'
      AND (
          (r.match_type = 'EXACT_EMAIL'     AND LOWER(t.sender) LIKE CONCAT('%<', LOWER(r.pattern), '>'))
          OR
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(t.sender) LIKE CONCAT('%', LOWER(r.pattern), '%'))
      );

    -- ── 3. SYSTEM: automated alerts, notifications, no-reply senders ─────────
    UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` t
    SET
        security_verdict  = 'SYSTEM',
        processing_status = 'CLASSIFIED_L1',
        ai_category       = 'RULE_SYSTEM'
    FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
    WHERE t.processing_status = 'PENDING'
      AND t.ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
      AND r.rule_type = 'SYSTEM'
      AND (
          (r.match_type = 'EXACT_EMAIL'     AND LOWER(t.sender) LIKE CONCAT('%<', LOWER(r.pattern), '>'))
          OR
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(t.sender) LIKE CONCAT('%', LOWER(r.pattern), '%'))
      );

    -- ── 4. ALLOW: known internal/trusted senders → pass directly as BUSINESS ─
    UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` t
    SET
        security_verdict  = 'BUSINESS',
        processing_status = 'CLASSIFIED_L1',
        ai_category       = 'RULE_ALLOWED'
    FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
    WHERE t.processing_status = 'PENDING'
      AND t.ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR)
      AND r.rule_type = 'ALLOW'
      AND (
          (r.match_type = 'EXACT_EMAIL'     AND LOWER(t.sender) LIKE CONCAT('%<', LOWER(r.pattern), '>'))
          OR
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(t.sender) LIKE CONCAT('%', LOWER(r.pattern), '%'))
      );

    -- ── 5. Promote BUSINESS emails to entity matching ─────────────────────────
    -- Emails in CLASSIFIED_L1 with BUSINESS verdict are immediately ready.
    -- Layer 2 (AI) will promote additional emails once hivemind_pipeline.py runs.
    CALL `augos-core-data.hive_mind_core.match_entities`();

END;
