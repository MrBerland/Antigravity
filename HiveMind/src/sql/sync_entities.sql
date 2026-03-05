CREATE OR REPLACE PROCEDURE `augos-core-data.hive_mind_core.sync_entities`()
BEGIN
  -- 1. Sync SITES
  -- We assume SiteID is the stable UUID.
  INSERT INTO `augos-core-data.hive_mind_core.dim_entities` (entity_id, entity_type, name, identifiers)
  SELECT 
    SiteID as entity_id, 
    'SITE' as entity_type,
    SiteName as name,
    -- Identifiers: Name + City to help matching
    ARRAY_AGG(DISTINCT x IGNORE NULLS) as identifiers
  FROM `augos-core-data.augos_warehouse.sites`,
  UNNEST([SiteName, Address, City]) as x
  WHERE x != '' AND x IS NOT NULL
  AND SiteID NOT IN (SELECT entity_id FROM `augos-core-data.hive_mind_core.dim_entities`)
  GROUP BY SiteID, SiteName;

  -- 2. Sync DEVICES (Assets)
  INSERT INTO `augos-core-data.hive_mind_core.dim_entities` (entity_id, entity_type, name, identifiers)
  SELECT 
    -- Use SerialNumber as entity_id (Stable)
    SerialNumber as entity_id, 
    'ASSET' as entity_type,
    DeviceDescription as name,
    [SerialNumber, DeviceDescription] as identifiers
  FROM `augos-core-data.augos_warehouse.devices`
  WHERE SerialNumber IS NOT NULL
  AND SerialNumber NOT IN (SELECT entity_id FROM `augos-core-data.hive_mind_core.dim_entities`);

  -- 3. Sync CONTACTS (People)
  INSERT INTO `augos-core-data.hive_mind_core.dim_entities` (entity_id, entity_type, name, identifiers)
  SELECT 
    ContactID as entity_id,
    'PERSON' as entity_type,
    Name as name,
    ARRAY_AGG(DISTINCT x IGNORE NULLS) as identifiers
  FROM `augos-core-data.augos_warehouse.contacts`,
  UNNEST([Name, Email]) as x
  WHERE x != '' AND x IS NOT NULL
  AND ContactID NOT IN (SELECT entity_id FROM `augos-core-data.hive_mind_core.dim_entities`)
  GROUP BY ContactID, Name;

  SELECT CONCAT('Entity Sync Complete. Total Entities: ', (SELECT count(*) FROM `augos-core-data.hive_mind_core.dim_entities`)) as status;
END;
