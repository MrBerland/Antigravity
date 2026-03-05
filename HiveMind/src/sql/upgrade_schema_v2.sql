ALTER TABLE `augos-core-data.hive_mind_core.dim_entities`
ADD COLUMN IF NOT EXISTS source_id STRING,
ADD COLUMN IF NOT EXISTS source_system STRING,
ADD COLUMN IF NOT EXISTS embedding ARRAY<FLOAT64>;

CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.fact_relationships` (
    relationship_id STRING,
    source_entity_id STRING,
    target_entity_id STRING,
    relationship_type STRING,
    weight FLOAT64,
    source STRING,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
