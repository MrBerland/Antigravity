CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.search_vectors`(query_text STRING, top_k INT64)
BEGIN
  -- 1. Generate Embedding for Query
  CREATE TEMP TABLE query_embedding AS
  SELECT ml_generate_embedding_result as text_embedding 
  FROM ML.GENERATE_EMBEDDING(
    MODEL `augos-core-data.hive_mind_core.embedding_model`,
    (SELECT query_text as content)
  );

  -- 2. Vector Search (Dynamic SQL for top_k)
  EXECUTE IMMEDIATE FORMAT("""
    SELECT
      base.message_id,
      s.subject,
      s.sender,
      distance
    FROM
      VECTOR_SEARCH(
        TABLE `augos-core-data.hive_mind_core.fact_embeddings`,
        'embedding',
        (SELECT text_embedding FROM query_embedding),
        top_k => %d
      ) v
    JOIN `augos-core-data.hive_mind_core.staging_raw_emails` s ON v.base.message_id = s.message_id
  """, top_k);

END;
