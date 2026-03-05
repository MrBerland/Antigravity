-- 1. Create the Remote Model (Temporarily Disabled for Debugging)
-- CREATE OR REPLACE MODEL `augos-core-data.hive_mind_core.gemini_bouncer`
-- REMOTE WITH CONNECTION `augos-core-data.us.gemini_conn`
-- OPTIONS (endpoint = 'gemini-pro');

-- 2. The Processor Procedure
CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.process_staging_data`()
BEGIN
    -- 0. Apply Governance Rules (Deterministic / Free)
    -- Block known bad domains/emails
    UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` t
    SET 
        security_verdict = 'BLOCK',
        processing_status = 'PROCESSED',
        ai_category = 'RULE_BLOCKED'
    FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
    WHERE t.processing_status = 'PENDING'
      AND t.ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR) -- Avoid Streaming Buffer
      AND r.rule_type = 'BLOCK'
      AND (
          (r.match_type = 'EXACT_EMAIL' AND t.sender LIKE CONCAT('%<', r.pattern, '>')) -- Handle angle brackets
          OR 
          (r.match_type = 'DOMAIN_WILDCARD' AND t.sender LIKE CONCAT('%', r.pattern, '%')) -- Safer containment check
      );

    -- Allow known good domains (Internal) - Skip AI
    UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` t
    SET 
        security_verdict = 'ALLOW',
        processing_status = 'PROCESSED',
        ai_category = 'RULE_ALLOWED'
    FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
    WHERE t.processing_status = 'PENDING'
      AND t.ingest_time < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 HOUR) -- Avoid Streaming Buffer
      AND r.rule_type = 'ALLOW'
      AND (
          (r.match_type = 'EXACT_EMAIL' AND t.sender LIKE CONCAT('%<', r.pattern, '>')) -- Handle angle brackets
          OR 
          (r.match_type = 'DOMAIN_WILDCARD' AND t.sender LIKE CONCAT('%', r.pattern, '%')) -- Safer containment check
      );

    -- A. Classify REMAINING PENDING items (The Grey Area) with AI
    -- (DISABLED for now - awaiting Model Availability)
    -- We will leave them as PENDING for now so they can be processed once AI is up.
    
    /*
    CREATE TEMP TABLE ai_results AS
    SELECT
        message_id,
        ml_generate_text_result as ai_response
    FROM
    ML.GENERATE_TEXT(
        MODEL `augos-core-data.hive_mind_core.gemini_bouncer`,
        ...
    );
    ...
    */

    -- C. Promote Safe Emails (From Rules) to Production
    -- C. Promote Safe Emails (From Rules) to Production (Idempotent MERGE)
    MERGE `augos-core-data.hive_mind_core.messages` T
    USING (
        SELECT DISTINCT message_id, thread_id, timestamp, sender, subject, snippet, raw_gcs_uri
        FROM `augos-core-data.hive_mind_core.staging_raw_emails`
        WHERE processing_status = 'PROCESSED' 
          AND security_verdict = 'ALLOW'
    ) S
    ON T.message_id = S.message_id
    WHEN NOT MATCHED THEN
        INSERT (message_id, thread_id, timestamp, sender, subject, snippet, gcs_uri)
        VALUES (S.message_id, S.thread_id, S.timestamp, S.sender, S.subject, S.snippet, S.raw_gcs_uri);

    -- D. Trigger Entity Matcher
    CALL `augos-core-data.hive_mind_core.match_entities`();

END;
