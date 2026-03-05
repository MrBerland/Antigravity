MERGE `augos-core-data.hive_mind_core.dim_entities` T
USING (
  SELECT 
    CAST(PointID AS STRING) as SiteID, 
    -- Extract clean name from Description e.g. "Waterstone | Main" -> "Waterstone"??
    -- Actually for IsSite=true, Description might just be "Waterstone Store" or "Group | SiteName"
    -- Let's use Description as is for Name, and maybe split for identifiers
    Description as SiteName
  FROM `augos-core-data.augos_warehouse.augos_points`
  WHERE IsSite = true AND Status = 'Active'
) S
ON T.source_id = S.SiteID AND T.source_system = 'AUGOS_WAREHOUSE' AND T.entity_type = 'SITE'

WHEN MATCHED THEN
  UPDATE SET 
    name = S.SiteName,
    identifiers = ARRAY_CONCAT(T.identifiers, [S.SiteName])

WHEN NOT MATCHED THEN
  INSERT (entity_id, entity_type, name, identifiers, source_id, source_system)
  VALUES (GENERATE_UUID(), 'SITE', S.SiteName, [S.SiteName], S.SiteID, 'AUGOS_WAREHOUSE')
