MERGE `augos-core-data.hive_mind_core.dim_entities` T
USING (
  SELECT 
    CAST(PointID AS STRING) as PointID,
    Description,
    SerialNumber
  FROM `augos-core-data.augos_warehouse.augos_points`
  WHERE Status = 'Active' AND IsSite = false
) S
ON T.source_id = S.PointID AND T.source_system = 'AUGOS_WAREHOUSE' AND T.entity_type = 'ASSET'

WHEN MATCHED THEN
  UPDATE SET 
    name = S.Description,
    identifiers = ARRAY_CONCAT(T.identifiers, [S.Description, S.SerialNumber])

WHEN NOT MATCHED THEN
  INSERT (entity_id, entity_type, name, identifiers, source_id, source_system)
  VALUES (GENERATE_UUID(), 'ASSET', S.Description, 
  IF(S.SerialNumber IS NULL, [S.Description], [S.Description, S.SerialNumber]), 
  S.PointID, 'AUGOS_WAREHOUSE')
