CREATE OR REPLACE MODEL `augos-core-data.hive_mind_core.embedding_model`
REMOTE WITH CONNECTION `augos-core-data.us.vertex-ai`
OPTIONS(endpoint = 'text-embedding-004');
