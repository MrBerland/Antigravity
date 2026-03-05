-- 1. Create the Embedding Model (Links to Vertex AI text-embedding-004)
-- This allows us to call the AI model using standard SQL.
CREATE OR REPLACE MODEL `hive_mind_core.embedding_model`
REMOTE WITH CONNECTION `us.vertex_conn`
OPTIONS(ENDPOINT = 'text-embedding-004');

-- 2. Create the Embeddings Table
-- This table will store the vector representation of every email.
-- We use a standard table now; for large scale, we'd use a Vector Index.
CREATE OR REPLACE TABLE `hive_mind_core.email_embeddings` AS
SELECT
  message_id,
  thread_id,
  timestamp,
  sender,
  subject,
  snippet,
  -- Generate the 768-dimensional vector
  ml_generate_embedding_result as embedding
FROM
  ML.GENERATE_EMBEDDING(
    MODEL `hive_mind_core.embedding_model`,
    (
      SELECT 
        message_id, 
        thread_id, 
        timestamp, 
        sender, 
        subject, 
        snippet,
        -- The content we want to "Search" against
        CONCAT('Subject: ', IFNULL(subject, ''), '. Content: ', IFNULL(snippet, '')) as content
      FROM `hive_mind_core.messages`
      -- Optimization: In production, filter by timestamp > last_run
      WHERE snippet IS NOT NULL
    )
  );

-- 3. (Optional) Create a Search Function
-- A helper to make querying easy for the Agents.
-- USAGE: SELECT * FROM hive_mind_core.search_emails('pricing disagreement');
/*
CREATE OR REPLACE TABLE FUNCTION `hive_mind_core.search_emails`(query STRING) AS
SELECT
  base.message_id,
  base.subject,
  base.snippet,
  base.sender,
  -- Calculate Cosine Distance
  ML.DISTANCE(
    (SELECT ml_generate_embedding_result FROM ML.GENERATE_EMBEDDING(MODEL `hive_mind_core.embedding_model`, (SELECT query as content))),
    base.embedding,
    'COSINE'
  ) as distance
FROM
  `hive_mind_core.email_embeddings` base
ORDER BY distance ASC
LIMIT 10;
*/
