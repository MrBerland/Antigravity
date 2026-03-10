-- Watermark table for tracking Gmail History API position per user.
-- Created as part of the production hardening of the Cloud Function extractor.
-- The extractor uses this to fetch only NEW messages since the last push event
-- (via users.history.list with startHistoryId) instead of blindly grabbing maxResults=1.

CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.ingest_watermarks` (
    user_email  STRING    NOT NULL,
    history_id  STRING    NOT NULL,   -- Last historyId successfully processed
    updated_at  FLOAT64   NOT NULL    -- Unix timestamp (time.time())
);
