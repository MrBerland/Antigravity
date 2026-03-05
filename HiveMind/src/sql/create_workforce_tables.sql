-- DDL for Workforce Intelligence Tables

-- 1. Fact Table: Work Patterns (Time Allocation)
CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.fact_work_patterns` (
    analysis_id STRING,
    message_id STRING,
    user_email STRING,
    category STRING, -- e.g. DEVELOPMENT, SALES
    urgency BOOLEAN,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- 2. Dim Table: User Attributes (Enriched Profile)
CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.dim_user_attributes` (
    email STRING,
    latest_detected_title STRING,
    detected_skills ARRAY<STRING>,
    last_updated TIMESTAMP
);
