-- Agent: The Sales Predator (Lead Scorer)
-- Goal: Identify high-value opportunities in the noise.

-- 1. Create the Analysis Table
-- We process emails where the sender is NOT internal (obviously).
CREATE OR REPLACE PROCEDURE `hive_mind_core.analyze_sales_leads`(batch_size INT64)
BEGIN
  -- 1. Identify Candidates
  EXECUTE IMMEDIATE FORMAT("""
    CREATE TEMP TABLE pending_sales AS
    SELECT 
      message_id, 
      sender, 
      subject,
      timestamp,
      snippet
    FROM `augos-core-data.hive_mind_core.v_business_emails`  -- ✅ CLEAN FEED ONLY
    WHERE sender NOT LIKE '%%@augos.io' -- Ignore internal
      AND message_id NOT IN (SELECT message_id FROM `hive_mind_core.sales_leads`)
    LIMIT %d
  """, batch_size);

  -- 2. Analyze with Gemini
  INSERT INTO `hive_mind_core.sales_leads` (message_id, sender, subject, timestamp, sales_analysis)
  SELECT
    message_id,
    sender,
    subject,
    timestamp,
    -- Check with Gemini - extract JSON object robustly
    PARSE_JSON(REGEXP_EXTRACT(ml_generate_text_llm_result, r'\{[^{}]*\}'))
  FROM
    ML.GENERATE_TEXT(
      MODEL `hive_mind_core.gemini_flash`, 
      (
        SELECT 
          message_id, sender, subject, timestamp,
          -- Prompt Engineering for Sales
          CONCAT(
            'Analyze this email for Sales Opportunity. Return JSON with fields: ',
            '"is_lead" (boolean), "intent" (e.g. "Pricing", "Demo", "Support"), ',
            '"deal_size_estimate" (string or null), "urgency" (1-10), "suggested_action". ',
            'Email Subject: ', subject, '. Snippet: ', snippet
          ) as prompt
        FROM pending_sales
      ),
      STRUCT(
        0.1 AS temperature, 
        300 AS max_output_tokens,
        TRUE AS flatten_json_output
      )
    );
END;

-- 2. The "Hot Leads" View (The Dashboard)
-- Sales reps query this to see who to call FIRST.
CREATE OR REPLACE VIEW `hive_mind_core.hot_leads` AS
SELECT
  l.sender,
  l.subject,
  JSON_VALUE(l.sales_analysis, '$.intent') as intent,
  JSON_VALUE(l.sales_analysis, '$.deal_size_estimate') as estimated_value,
  CAST(JSON_VALUE(l.sales_analysis, '$.urgency') AS INT64) as urgency,
  JSON_VALUE(l.sales_analysis, '$.suggested_action') as AI_suggestion,
  l.timestamp
FROM `hive_mind_core.sales_leads` l
WHERE 
  JSON_VALUE(l.sales_analysis, '$.is_lead') = 'true'
  AND CAST(JSON_VALUE(l.sales_analysis, '$.urgency') AS INT64) >= 7
ORDER BY urgency DESC, timestamp DESC;
