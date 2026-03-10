CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.fact_embeddings` (
  message_id STRING NOT NULL,
  embedding ARRAY<FLOAT64>,
  embedded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
