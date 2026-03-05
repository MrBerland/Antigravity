CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.extract_entities_semantic`(batch_size INT64)
BEGIN
  -- 1. Identity Candidates (Emails not yet processed by Gemini)
  EXECUTE IMMEDIATE FORMAT("""
    CREATE TEMP TABLE pending_emails AS
    SELECT 
      message_id, 
      subject, 
      snippet, 
      sender
    FROM `augos-core-data.hive_mind_core.staging_raw_emails` e
    WHERE NOT EXISTS (
      SELECT 1 FROM `augos-core-data.hive_mind_core.fact_email_entities` f 
      WHERE f.message_id = e.message_id AND f.source = 'GEMINI_ML'
    )
    LIMIT %d
  """, batch_size);

  -- 2. Call Gemini (ML.GENERATE_TEXT)
  CREATE TEMP TABLE gemini_results AS
  SELECT *
  FROM
    ML.GENERATE_TEXT(
      MODEL `augos-core-data.hive_mind_core.gemini_flash`,
      (
        SELECT 
          message_id, 
          CONCAT(
            'Analyze this email snippet. Return a JSON object with a key "entities" containing a list of business entities (Sites, Assets, Projects, Vendors, Customers) referenced. ',
            'Format: {"entities": [{"name": "EntityName", "type": "TYPE"}]}. ',
            'Ignore generic terms. ',
            'Email Context: Subject: ', subject, ', Sender: ', sender, ', Content: ', snippet
          ) as prompt
        FROM pending_emails
      ),
      STRUCT(
        0.2 AS temperature, 
        500 AS max_output_tokens,
        TRUE AS flatten_json_output
      )
    );

  -- 3. Parse and Insert
  -- Step 3a: Insert NEW Entities found by AI
  INSERT INTO `augos-core-data.hive_mind_core.dim_entities` (entity_id, entity_type, name, identifiers)
  SELECT DISTINCT
    GENERATE_UUID(),
    UPPER(JSON_VALUE(entity, '$.type')),
    JSON_VALUE(entity, '$.name'),
    [JSON_VALUE(entity, '$.name')]
  FROM gemini_results,
  UNNEST(JSON_QUERY_ARRAY(SAFE.PARSE_JSON(
    JSON_VALUE(SAFE.PARSE_JSON(ml_generate_text_llm_result), '$.candidates[0].content.parts[0].text')
  ), '$.entities')) as entity
  WHERE JSON_VALUE(entity, '$.name') IS NOT NULL
  AND JSON_VALUE(entity, '$.name') NOT IN (SELECT name FROM `augos-core-data.hive_mind_core.dim_entities`);

  -- Step 3b: Link Emails to Entities (Old and New)
  INSERT INTO `augos-core-data.hive_mind_core.fact_email_entities` (link_id, message_id, entity_id, confidence, source)
  SELECT DISTINCT
    GENERATE_UUID(),
    g.message_id,
    d.entity_id,
    0.8 as confidence,
    'GEMINI_ML'
  FROM gemini_results g,
  UNNEST(JSON_QUERY_ARRAY(SAFE.PARSE_JSON(
    JSON_VALUE(SAFE.PARSE_JSON(g.ml_generate_text_llm_result), '$.candidates[0].content.parts[0].text')
  ), '$.entities')) as entity
  JOIN `augos-core-data.hive_mind_core.dim_entities` d 
    ON d.name = JSON_VALUE(entity, '$.name');

  SELECT CONCAT('Semantic Extraction Complete. Processed ', (SELECT count(*) FROM pending_emails), ' emails.') as status;

END;
