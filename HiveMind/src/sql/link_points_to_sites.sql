-- Link Points to Sites based on Augos naming convention "Group | SiteName | PointName (DeviceID)"
INSERT INTO `augos-core-data.hive_mind_core.fact_relationships` 
(relationship_id, source_entity_id, target_entity_id, relationship_type, weight, source)
SELECT
  GENERATE_UUID(),
  p.entity_id as source_entity_id, -- Point
  s.entity_id as target_entity_id, -- Site
  'LOCATED_AT',
  1.0, -- Deterministic naming convention
  'REGEX_MATCH'
FROM `augos-core-data.hive_mind_core.dim_entities` p
CROSS JOIN `augos-core-data.hive_mind_core.dim_entities` s
WHERE 
  p.entity_type = 'ASSET' AND p.source_system = 'AUGOS_WAREHOUSE'
  AND s.entity_type = 'SITE' AND s.source_system = 'AUGOS_WAREHOUSE'
  -- Match logic: Point description contains Site Name
  -- Logic from v_site_points: SPLIT(p.Description, "|")[SAFE_OFFSET(1)]
  AND TRIM(SPLIT(p.name, '|')[SAFE_OFFSET(1)]) = s.name
  
  -- Avoid duplicates
  AND NOT EXISTS (
    SELECT 1 FROM `augos-core-data.hive_mind_core.fact_relationships` r
    WHERE r.source_entity_id = p.entity_id AND r.target_entity_id = s.entity_id
  )
