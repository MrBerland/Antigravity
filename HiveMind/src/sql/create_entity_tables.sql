-- 1. Master Entity Table
CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.dim_entities` (
    entity_id STRING, -- UUID
    entity_type STRING, -- CUSTOMER, SITE, ASSET, TICKET
    name STRING,
    identifiers ARRAY<STRING>, -- Synonyms/Serials (e.g. ["The Motley Fool", "Fool.com"])
    source_id STRING, -- e.g. "5864" or "contact_123"
    source_system STRING, -- e.g. "AUGOS_WAREHOUSE", "XERO"
    embedding ARRAY<FLOAT64>, -- Vector for semantic search
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- 2. Linking Table (The Graph)
CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.fact_email_entities` (
    link_id STRING,
    message_id STRING,
    entity_id STRING,
    confidence FLOAT64, -- 1.0 = Exact, 0.5-0.9 = AI
    source STRING, -- "REGEX_MATCH", "GEMINI_EXTRACTION"
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- 3. Seed Mock Data (If empty)
BEGIN
  IF (SELECT count(*) FROM `augos-core-data.hive_mind_core.dim_entities`) = 0 THEN
    INSERT INTO `augos-core-data.hive_mind_core.dim_entities` (entity_id, entity_type, name, identifiers)
    VALUES
      (GENERATE_UUID(), 'CUSTOMER', 'The Motley Fool', ['The Motley Fool', 'Fool.com', 'fool@info.fool.com']),
      (GENERATE_UUID(), 'SITE', 'Augos HQ', ['Augos HQ', 'Headquarters', 'Office']),
      (GENERATE_UUID(), 'CUSTOMER', 'OneDayOnly', ['OneDayOnly', 'onedayonly.co.za']),
      (GENERATE_UUID(), 'INTERNAL', 'Tim Stevens', ['Tim Stevens', 'tim@augos.io']),
      (GENERATE_UUID(), 'ASSET', 'Main Chiller', ['Chiller 1', 'CH-01', 'Serial-123']);
  END IF;
END;
