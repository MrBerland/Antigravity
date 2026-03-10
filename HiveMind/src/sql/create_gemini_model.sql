CREATE OR REPLACE MODEL `augos-core-data.hive_mind_core.gemini_flash`
REMOTE WITH CONNECTION `augos-core-data.us.vertex-ai`
OPTIONS(endpoint = 'gemini-2.0-flash');

