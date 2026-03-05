CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.match_entities`()
BEGIN
  -- 1. Find new exact matches using Recipient/Sender/Subject against Identifiers
  -- We flatten the array to join
  
  INSERT INTO `augos-core-data.hive_mind_core.fact_email_entities` (link_id, message_id, entity_id, confidence, source)
  SELECT DISTINCT
    GENERATE_UUID() as link_id,
    e.message_id,
    d.entity_id,
    1.0 as confidence,
    'EXACT_MATCH' as source
  FROM `augos-core-data.hive_mind_core.staging_raw_emails` e
  CROSS JOIN `augos-core-data.hive_mind_core.dim_entities` d,
  UNNEST(d.identifiers) as ident
  WHERE 
    -- Avoid duplicates
    NOT EXISTS (
      SELECT 1 FROM `augos-core-data.hive_mind_core.fact_email_entities` f 
      WHERE f.message_id = e.message_id AND f.entity_id = d.entity_id
    )
    AND (
       -- Match Logic: Case Insensitive
       LOWER(e.sender) LIKE CONCAT('%', LOWER(ident), '%')
       OR LOWER(e.subject) LIKE CONCAT('%', LOWER(ident), '%')
       OR (e.recipient IS NOT NULL AND LOWER(e.recipient) LIKE CONCAT('%', LOWER(ident), '%'))
    );

  -- Log run
  SELECT CONCAT('Entity Match Complete. Rows linked: ', @@row_count) as status;
END;
