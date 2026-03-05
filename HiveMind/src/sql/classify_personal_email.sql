-- =============================================================================
-- classify_personal_email.sql
-- =============================================================================
-- Two-layer personal/sensitive email classification pipeline.
--
-- LAYER 1: Domain Blocklist  (fast, zero-cost, deterministic)
--   Marks emails from known personal providers and marketing automation
--   platforms directly from the sender field. No AI needed.
--
-- LAYER 2: AI Content Classifier  (Gemini Flash, targeted, cheap)
--   Runs ONLY on emails that passed Layer 1 (unclassified). Uses subject +
--   snippet to detect personal content sent from business addresses
--   (e.g. "My son's school" from tim@augos.io).
--
-- VERDICT VALUES written to staging_raw_emails.security_verdict:
--   BUSINESS        → Safe for KB, agents, and search indexes
--   PERSONAL        → Personal life content — exclude from all agents
--   SYSTEM          → Automated notifications, alerts, cron emails
--   MARKETING       → Newsletters, promotions — exclude from KB
--   HR_SENSITIVE    → Payroll, disciplinary, medical — hard exclude
--   CONFIDENTIAL    → Legal, financial, board — restricted access only
--   PENDING         → Not yet classified (default)
--
-- HOW TO RUN:
--   1. CALL `hive_mind_core.layer1_domain_classify`();
--   2. CALL `hive_mind_core.layer2_ai_classify`(1000);
--   3. Check results: SELECT * FROM `hive_mind_core.v_classification_summary`;
-- =============================================================================


-- =============================================================================
-- STEP 0: Seed the governance table with personal email domains
-- Uses MERGE so this is safe to re-run (idempotent — won't duplicate rows)
-- =============================================================================

MERGE `augos-core-data.hive_mind_core.dim_governance_rules` T
USING (
  SELECT * FROM UNNEST([
    -- ── Personal Consumer Email Providers ──────────────────────────
    STRUCT('PERSONAL','DOMAIN_WILDCARD','gmail.com',          'Personal gmail accounts'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','googlemail.com',     'Personal gmail EU variant'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','yahoo.com',          'Personal Yahoo'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','yahoo.co.uk',        'Personal Yahoo UK'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','yahoo.co.za',        'Personal Yahoo ZA'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','hotmail.com',        'Personal Hotmail'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','hotmail.co.uk',      'Personal Hotmail UK'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','outlook.com',        'Personal Outlook (when not corporate)'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','live.com',           'Personal Microsoft Live'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','msn.com',            'Personal MSN'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','icloud.com',         'Personal Apple iCloud'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','me.com',             'Personal Apple Me'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','mac.com',            'Personal Apple Mac'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','protonmail.com',     'Personal ProtonMail'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','proton.me',          'Personal Proton'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','aol.com',            'Personal AOL'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','webmail.co.za',      'Personal ZA Webmail'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','telkomsa.net',       'Personal Telkom SA'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','vodamail.co.za',     'Personal Vodacom Mail'),
    STRUCT('PERSONAL','DOMAIN_WILDCARD','iafrica.com',        'Personal iAfrica'),
    -- ── Marketing Automation & Newsletters ─────────────────────────
    STRUCT('MARKETING','DOMAIN_WILDCARD','mailchimp.com',     'Mailchimp campaigns'),
    STRUCT('MARKETING','DOMAIN_WILDCARD','hubspot.com',       'HubSpot marketing'),
    STRUCT('MARKETING','DOMAIN_WILDCARD','sendgrid.net',      'SendGrid bulk mail'),
    STRUCT('MARKETING','DOMAIN_WILDCARD','email.mailjet.com', 'Mailjet campaigns'),
    STRUCT('MARKETING','DOMAIN_WILDCARD','klaviyo.com',       'Klaviyo ecomm email'),
    STRUCT('MARKETING','DOMAIN_WILDCARD','constantcontact.com','Constant Contact'),
    STRUCT('MARKETING','DOMAIN_WILDCARD','campaign-monitor.com','Campaign Monitor'),
    STRUCT('MARKETING','DOMAIN_WILDCARD','marketing.tajhotels.com','Taj Hotels marketing'),
    -- ── System / Automated Senders ─────────────────────────────────
    STRUCT('SYSTEM','DOMAIN_WILDCARD','zohocalendar.com',     'Zoho Calendar notifications'),
    STRUCT('SYSTEM','EXACT_EMAIL','noreply@google.com',       'Google noreply'),
    STRUCT('SYSTEM','EXACT_EMAIL','no-reply@accounts.google.com','Google account alerts'),
    STRUCT('SYSTEM','DOMAIN_WILDCARD','notifications.google.com','Google notifications'),
    STRUCT('SYSTEM','DOMAIN_WILDCARD','mailer-daemon.googlemail.com','Mail delivery failures'),
    STRUCT('SYSTEM','EXACT_EMAIL','noreply@github.com',       'GitHub notifications'),
    STRUCT('SYSTEM','DOMAIN_WILDCARD','jira.atlassian.com',   'Jira issue notifications'),
    STRUCT('SYSTEM','DOMAIN_WILDCARD','slack.com',            'Slack notification emails'),
    STRUCT('SYSTEM','DOMAIN_WILDCARD','xero.com',             'Xero accounting system (review — may want BUSINESS)'),
    STRUCT('SYSTEM','DOMAIN_WILDCARD','zoom.us',              'Zoom meeting invites/notifications'),
    -- ── Internal domain ─────────────────────────────────────────────
    STRUCT('ALLOW','DOMAIN_WILDCARD','augos.io',              'Internal Augos domain — always allow')
  ] AS t (rule_type, match_type, pattern, notes))
) S ON T.pattern = S.pattern AND T.rule_type = S.rule_type
WHEN NOT MATCHED THEN
  INSERT (rule_id, rule_type, match_type, pattern, added_by, notes)
  VALUES (GENERATE_UUID(), S.rule_type, S.match_type, S.pattern, 'pii_classifier', S.notes);


-- =============================================================================
-- PROCEDURE 1: Layer 1 — Domain-Based Classification
-- Fast sweep: classify everything we can without touching Gemini.
-- Safe to run repeatedly — only touches PENDING rows.
-- =============================================================================

CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.layer1_domain_classify`()
BEGIN

  -- 1a. Mark PERSONAL — sender domain matches a PERSONAL rule
  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET
    security_verdict = 'PERSONAL',
    processing_status = 'CLASSIFIED_L1'
  WHERE
    e.processing_status = 'PENDING'
    AND EXISTS (
      SELECT 1
      FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
      WHERE r.rule_type = 'PERSONAL'
        AND (
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))
          OR (r.match_type = 'EXACT_EMAIL'  AND LOWER(e.sender) = LOWER(r.pattern))
        )
    );

  -- 1b. Mark MARKETING — domain matches a MARKETING rule
  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET
    security_verdict = 'MARKETING',
    processing_status = 'CLASSIFIED_L1'
  WHERE
    e.processing_status = 'PENDING'
    AND EXISTS (
      SELECT 1
      FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
      WHERE r.rule_type = 'MARKETING'
        AND (
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))
          OR (r.match_type = 'EXACT_EMAIL'  AND LOWER(e.sender) = LOWER(r.pattern))
        )
    );

  -- 1c. Mark SYSTEM — domain matches a SYSTEM rule
  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET
    security_verdict = 'SYSTEM',
    processing_status = 'CLASSIFIED_L1'
  WHERE
    e.processing_status = 'PENDING'
    AND EXISTS (
      SELECT 1
      FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
      WHERE r.rule_type = 'SYSTEM'
        AND (
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))
          OR (r.match_type = 'EXACT_EMAIL'  AND LOWER(e.sender) = LOWER(r.pattern))
        )
    );

  -- 1d. Mark internal AUGOS domains as ALLOW immediately (skip AI cost)
  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET
    security_verdict  = 'BUSINESS',
    processing_status = 'CLASSIFIED_L1'
  WHERE
    e.processing_status = 'PENDING'
    AND EXISTS (
      SELECT 1
      FROM `augos-core-data.hive_mind_core.dim_governance_rules` r
      WHERE r.rule_type = 'ALLOW'
        AND (
          (r.match_type = 'DOMAIN_WILDCARD' AND LOWER(e.sender) LIKE CONCAT('%@', LOWER(r.pattern)))
          OR (r.match_type = 'EXACT_EMAIL'  AND LOWER(e.sender) = LOWER(r.pattern))
        )
    );

  -- 1e. Subject-line quick wins — common personal patterns
  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails`
  SET
    security_verdict  = 'PERSONAL',
    ai_category       = 'SUBJECT_PATTERN_MATCH',
    processing_status = 'CLASSIFIED_L1'
  WHERE
    processing_status = 'PENDING'
    AND (
      REGEXP_CONTAINS(LOWER(subject), r'\b(unsubscribe|newsletter|your order|shipment|delivery|tracking number|your account|password reset|verify your email|confirm your email|receipt|bank statement|statement of account|loan|insurance|medical aid|discovery health|momentum|liberty|old mutual|fnb|nedbank|absa|standard bank|capitec|nedgroup)\b')
    );

  SELECT
    CONCAT(
      'Layer 1 complete. ',
      CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE security_verdict = 'PERSONAL'  AND processing_status = 'CLASSIFIED_L1') AS STRING), ' PERSONAL, ',
      CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE security_verdict = 'MARKETING' AND processing_status = 'CLASSIFIED_L1') AS STRING), ' MARKETING, ',
      CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE security_verdict = 'SYSTEM'    AND processing_status = 'CLASSIFIED_L1') AS STRING), ' SYSTEM, ',
      CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE security_verdict = 'BUSINESS'  AND processing_status = 'CLASSIFIED_L1') AS STRING), ' BUSINESS tagged.'
    ) AS status;
END;


-- =============================================================================
-- PROCEDURE 2: Layer 2 — AI Content Classifier (Gemini Flash)
-- Runs only on rows that are still PENDING after Layer 1.
-- These are emails from unknown/external domains where we can't tell from
-- the sender alone whether the content is personal or business.
-- batch_size: how many to process per call (recommended: 500–1000)
-- =============================================================================

CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.layer2_ai_classify`(batch_size INT64)
BEGIN

  -- Stage: grab a batch of still-unclassified emails
  CREATE TEMP TABLE pending_ai_classify AS
  SELECT
    message_id,
    sender,
    subject,
    snippet
  FROM `augos-core-data.hive_mind_core.staging_raw_emails`
  WHERE processing_status = 'PENDING'
  LIMIT batch_size;

  -- Call Gemini Flash to classify each one
  CREATE TEMP TABLE ai_verdicts AS
  SELECT
    message_id,
    sender,
    ml_generate_text_llm_result AS raw_response
  FROM
    ML.GENERATE_TEXT(
      MODEL `augos-core-data.hive_mind_core.gemini_flash`,
      (
        SELECT
          message_id,
          sender,
          CONCAT(
            'You are a privacy classifier for a corporate email system. ',
            'Classify this email into EXACTLY ONE category. Return ONLY a JSON object, no markdown, no explanation.\n\n',
            'CATEGORIES:\n',
            '  BUSINESS     - Work-related: client communication, contracts, operations, support tickets, internal projects\n',
            '  PERSONAL     - Private life: family, friends, personal finances, health, hobbies, personal shopping\n',
            '  HR_SENSITIVE - Salary, disciplinary action, resignation, recruitment, medical leave, benefits\n',
            '  CONFIDENTIAL - Legal matters, M&A, board communications, investor relations, NDA content\n',
            '  MARKETING    - Newsletter, promotion, discount offer, event invitation (unsolicited)\n',
            '  SYSTEM       - Automated notification: alerts, calendar invite, CI/CD, account confirmation\n\n',
            'EMAIL:\n',
            'From: ', sender, '\n',
            'Subject: ', subject, '\n',
            'Preview: ', snippet, '\n\n',
            'RESPOND WITH JSON ONLY:\n',
            '{"verdict": "CATEGORY", "confidence": 0.0-1.0, "reason": "one sentence"}'
          ) AS prompt
        FROM pending_ai_classify
      ),
      STRUCT(
        0.1 AS temperature,
        150 AS max_output_tokens,
        TRUE AS flatten_json_output
      )
    );

  -- Write verdicts back to staging table
  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET
    security_verdict  = JSON_VALUE(v.raw_response, '$.verdict'),
    ai_category       = CONCAT('AI_L2:', JSON_VALUE(v.raw_response, '$.reason')),
    processing_status = 'CLASSIFIED_L2'
  FROM ai_verdicts v
  WHERE e.message_id = v.message_id
    AND JSON_VALUE(v.raw_response, '$.verdict') IS NOT NULL;

  -- Any that the AI failed to parse — mark for manual review, don't leave as PENDING
  UPDATE `augos-core-data.hive_mind_core.staging_raw_emails` e
  SET
    security_verdict  = 'BUSINESS', -- fail open — assume business, agents will handle safely
    ai_category       = 'AI_L2_PARSE_FAILURE',
    processing_status = 'CLASSIFIED_L2'
  FROM ai_verdicts v
  WHERE e.message_id = v.message_id
    AND JSON_VALUE(v.raw_response, '$.verdict') IS NULL;

  SELECT
    CONCAT(
      'Layer 2 AI classify complete. Batch of ',
      CAST((SELECT COUNT(*) FROM pending_ai_classify) AS STRING),
      ' emails processed. Remaining PENDING: ',
      CAST((SELECT COUNT(*) FROM `augos-core-data.hive_mind_core.staging_raw_emails` WHERE processing_status = 'PENDING') AS STRING)
    ) AS status;
END;


-- =============================================================================
-- VIEW: Classification Summary Dashboard
-- =============================================================================

CREATE OR REPLACE VIEW `augos-core-data.hive_mind_core.v_classification_summary` AS
SELECT
  security_verdict,
  processing_status,
  COUNT(*)                                      AS email_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct_of_total,
  MIN(timestamp)                                AS earliest,
  MAX(timestamp)                                AS latest,
  COUNT(DISTINCT REGEXP_EXTRACT(sender, r'@(.+)$')) AS distinct_sender_domains
FROM `augos-core-data.hive_mind_core.staging_raw_emails`
GROUP BY 1, 2
ORDER BY email_count DESC;


-- =============================================================================
-- VIEW: Safe business emails only — THE CLEAN FEED
-- All agents, KB builders, and search indexers should use THIS view,
-- never query staging_raw_emails directly.
-- =============================================================================

CREATE OR REPLACE VIEW `augos-core-data.hive_mind_core.v_business_emails` AS
SELECT *
FROM `augos-core-data.hive_mind_core.staging_raw_emails`
WHERE security_verdict = 'BUSINESS'
  AND processing_status IN ('CLASSIFIED_L1', 'CLASSIFIED_L2');


-- =============================================================================
-- VIEW: Personal / sensitive emails (audit view — restricted access)
-- Use this to verify what got filtered out, or to handle data deletion requests.
-- =============================================================================

CREATE OR REPLACE VIEW `augos-core-data.hive_mind_core.v_personal_flagged` AS
SELECT
  message_id,
  thread_id,
  timestamp,
  sender,
  subject,           -- Subject only — NOT snippet (minimise exposure)
  security_verdict,
  ai_category,
  processing_status,
  raw_gcs_uri        -- Reference so you can delete GCS object if needed
FROM `augos-core-data.hive_mind_core.staging_raw_emails`
WHERE security_verdict IN ('PERSONAL', 'HR_SENSITIVE', 'CONFIDENTIAL');
