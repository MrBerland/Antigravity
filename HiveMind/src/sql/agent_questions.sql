-- Agent: The Question Extractor
-- Goal: Identify questions asked TO employees and efficient/inefficient responses.

CREATE OR REPLACE PROCEDURE `hive_mind_core.analyze_questions`(batch_size INT64)
BEGIN
  -- 1. Identify Candidates (Inbound emails to our users from external senders)
  -- Source: v_business_emails — clean, classified, personal/MARKETING filtered out.
  EXECUTE IMMEDIATE FORMAT("""
    CREATE TEMP TABLE pending_questions_analysis AS
    SELECT 
      message_id, 
      sender, 
      subject,
      snippet
    FROM `augos-core-data.hive_mind_core.v_business_emails`
    WHERE sender NOT LIKE '%%@augos.io'  -- External sender only
      AND message_id NOT IN (SELECT message_id FROM `hive_mind_core.fact_questions`)
    LIMIT %d
  """, batch_size);


  -- 2. Analyze with Gemini
  INSERT INTO `hive_mind_core.fact_questions` (message_id, sender, question_text, topic, difficulty, urgency, analysis_json)
  SELECT
    message_id,
    sender,
    JSON_VALUE(ml_generate_text_llm_result, '$.question') as question_text,
    JSON_VALUE(ml_generate_text_llm_result, '$.topic') as topic,
    CAST(JSON_VALUE(ml_generate_text_llm_result, '$.difficulty') AS INT64) as difficulty,
    CAST(JSON_VALUE(ml_generate_text_llm_result, '$.urgency') AS INT64) as urgency,
    PARSE_JSON(REGEXP_EXTRACT(ml_generate_text_llm_result, r'\{[^{}]*\}'))
  FROM
    ML.GENERATE_TEXT(
      MODEL `hive_mind_core.gemini_flash`,
      (
        SELECT 
          message_id, sender, subject,
          CONCAT(
            'Analyze this email from a customer/external party. ',
            '1. Extract the main QUESTION or REQUEST they are making. ',
            '2. Categorize the topic (e.g. "Pricing", "Technical Issue", "Scheduling"). ',
            '3. Rate Difficulty (1-5) and Urgency (1-5). ',
            '4. Return JSON: {"has_question": boolean, "question": "string", "topic": "string", "difficulty": int, "urgency": int}. ',
            'Return ONLY raw JSON. No markdown. ',
            'Subject: ', subject, '. Body: ', snippet
          ) as prompt
        FROM pending_questions_analysis
      ),
      STRUCT(
        0.0 AS temperature, 
        TRUE AS flatten_json_output
      )
    )
  WHERE JSON_VALUE(ml_generate_text_llm_result, '$.has_question') = 'true';
END;

-- Table Definition (if not exists)
CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.fact_questions` (
    message_id STRING,
    sender STRING,
    question_text STRING,
    topic STRING,
    difficulty INT64,
    urgency INT64,
    analysis_json JSON
);
