-- Shared Models for Hive Mind

-- 1. Gemini Pro (General Purpose: Sentiment, Reasoning, Complex Extraction)
CREATE OR REPLACE MODEL `hive_mind_core.sentiment_model`
REMOTE WITH CONNECTION `us.vertex_conn`
OPTIONS(ENDPOINT = 'gemini-1.5-pro-002');

-- 2. Gemini Flash (High Speed: Entity Extraction, Simple Classification)
CREATE OR REPLACE MODEL `hive_mind_core.gemini_flash`
REMOTE WITH CONNECTION `us.vertex_conn`
OPTIONS(ENDPOINT = 'gemini-1.5-flash-002');
