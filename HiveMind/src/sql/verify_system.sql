-- 1. Check for recent messages (Ingestion Verification)
SELECT 
  message_id, 
  timestamp, 
  sender, 
  subject, 
  snippet 
FROM `augos-core-data.hive_mind_core.messages`
ORDER BY timestamp DESC
LIMIT 10;

-- 2. Check for Security Blocks (if you enabled audit logging)
-- Or simpler: Check that NO email with "Lunch" is in the list above.

-- 3. Check Intelligence (Embeddings)
-- Run this AFTER the scheduled query runs (or run init_brain.sql again)
SELECT count(*) as vectorized_count FROM `augos-core-data.hive_mind_core.email_embeddings`;
