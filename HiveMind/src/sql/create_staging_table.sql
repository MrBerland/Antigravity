CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.staging_raw_emails` (
    message_id STRING,
    thread_id STRING,
    timestamp TIMESTAMP,
    sender STRING,
    subject STRING,
    snippet STRING,
    raw_gcs_uri STRING,
    ingest_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    processing_status STRING DEFAULT 'PENDING', -- PENDING, PROCESSED, ERROR
    security_verdict STRING, -- ALLOW, BLOCK, PII
    ai_category STRING
);
