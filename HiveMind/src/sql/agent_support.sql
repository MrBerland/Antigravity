-- 1. Create Sentiment Model (Links to Gemini Pro)
-- We use a Generative Model to get nuanced sentiment, not just +1/-1.
-- CREATE OR REPLACE MODEL `hive_mind_core.sentiment_model`
-- REMOTE WITH CONNECTION `us.vertex_conn`
-- OPTIONS(ENDPOINT = 'gemini-pro');

CREATE OR REPLACE PROCEDURE `hive_mind_core.analyze_support_threads`(batch_size INT64)
BEGIN
  -- 1. Identify Candidates
  -- We group by thread_id first
  EXECUTE IMMEDIATE FORMAT("""
    CREATE TEMP TABLE pending_threads AS
    SELECT
        thread_id,
        STRING_AGG(CONCAT(sender, ': ', snippet), '\\n') as thread_content
    FROM `augos-core-data.hive_mind_core.v_business_emails`  -- ✅ CLEAN FEED ONLY
    WHERE thread_id NOT IN (SELECT thread_id FROM `hive_mind_core.support_thread_scores`)
    GROUP BY thread_id
    LIMIT %d
  """, batch_size);

  -- 2. Analyze Sentiment & Resolution
  INSERT INTO `hive_mind_core.support_thread_scores` (thread_id, analysis_json)
  SELECT
    thread_id,
    PARSE_JSON(REGEXP_EXTRACT(ml_generate_text_llm_result, r'\{[^{}]*\}'))
  FROM
    ML.GENERATE_TEXT(
      MODEL `hive_mind_core.gemini_flash`,
      (
        SELECT
          thread_id,
          CONCAT('Analyze this support thread. Return JSON with fields: "sentiment_score" (1-10), "was_resolved" (boolean), "topic" (string), "best_message_id" (string of the best reply). Thread: ', thread_content) as prompt
        FROM pending_threads
      ),
      STRUCT(
        0.2 AS temperature,
        500 AS max_output_tokens,
        TRUE AS flatten_json_output
      )
    );
END;

-- 3. The "Gold Standard" View (The Knowledge Base)
-- The Agent queries THIS view to find answers.
-- It only returns threads that Gemini marked as "Resolved" and High Score.
CREATE OR REPLACE VIEW `hive_mind_core.best_responses` AS
SELECT
  JSON_VALUE(scores.analysis_json, '$.topic') as topic,
  scores.analysis_json, -- Contains the rationale
  msgs.snippet as best_reply_content,
  msgs.gcs_uri as full_email_ref
FROM `hive_mind_core.support_thread_scores` scores
JOIN `hive_mind_core.messages` msgs 
  -- Join on the Message ID that Gemini identified as the "Winner"
  -- (Note: In production, we'd need to parse the JSON output to extract the ID cleanly)
  ON msgs.message_id = JSON_VALUE(scores.analysis_json, '$.best_message_id')
WHERE 
  JSON_VALUE(scores.analysis_json, '$.was_resolved') = 'true'
  AND CAST(JSON_VALUE(scores.analysis_json, '$.sentiment_score') AS INT64) >= 8;
