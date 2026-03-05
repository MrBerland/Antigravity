CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.generate_embeddings`(batch_size INT64)
BEGIN
  -- 1. Identify Candidates (Emails without embeddings)
  EXECUTE IMMEDIATE FORMAT("""
    CREATE TEMP TABLE pending_embeddings AS
    SELECT 
      message_id, 
      subject || ' ' || snippet as content
    FROM `augos-core-data.hive_mind_core.staging_raw_emails` e
    WHERE NOT EXISTS (
      SELECT 1 FROM `augos-core-data.hive_mind_core.fact_embeddings` f 
      WHERE f.message_id = e.message_id
    )
    LIMIT %d
  """, batch_size);

  -- 2. Generate Embeddings
  INSERT INTO `augos-core-data.hive_mind_core.fact_embeddings` (message_id, embedding)
  SELECT
    message_id,
    ml_generate_embedding_result
  FROM ML.GENERATE_EMBEDDING(
    MODEL `augos-core-data.hive_mind_core.embedding_model`,
    (SELECT message_id, content FROM pending_embeddings),
    STRUCT(TRUE AS flatten_json_output)
  );

  SELECT CONCAT('Embedding Generation Complete. Processed ', (SELECT count(*) FROM pending_embeddings), ' emails.') as status;
END;
