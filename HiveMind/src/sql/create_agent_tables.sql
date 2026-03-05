-- Create tables for Agents if they don't exist

-- Sales
CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.sales_leads` (
    message_id STRING,
    sender STRING,
    subject STRING,
    timestamp TIMESTAMP,
    sales_analysis JSON
);

-- Support
CREATE TABLE IF NOT EXISTS `augos-core-data.hive_mind_core.support_thread_scores` (
    thread_id STRING,
    analysis_json JSON
);
