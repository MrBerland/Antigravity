CREATE OR REPLACE VIEW `augos-core-data.hive_mind_core.view_ops_bottlenecks` AS
WITH ThreadStats AS (
    SELECT 
        thread_id,
        ANY_VALUE(subject) as subject,
        count(*) as message_count,
        max(timestamp) as last_active,
        -- Check for escalation keywords in ANY message in the thread
        LOGICAL_OR(REGEXP_CONTAINS(LOWER(snippet), r'urgent|delay|manager|escalate')) as has_escalation,
        -- Check for "Stalled" keywords in the LAST message
        -- (Ideally we'd sort, but ANY_VALUE is approx. Let's just check if ANY has it for now as a proxy, 
        -- or use window functions for last message specific content. Let's keep it simple: heavy threads are bottlenecks.)
        array_agg(sender) as participants
    FROM `augos-core-data.hive_mind_core.staging_raw_emails`
    GROUP BY thread_id
),
EntityLinks AS (
    -- Get the primary entity linked to this thread (if any)
    -- We take the one with highest confidence or count
    SELECT 
        s.thread_id,
        e.name as entity_name,
        e.entity_type
    FROM `augos-core-data.hive_mind_core.staging_raw_emails` s
    JOIN `augos-core-data.hive_mind_core.fact_email_entities` f ON s.message_id = f.message_id
    JOIN `augos-core-data.hive_mind_core.dim_entities` e ON f.entity_id = e.entity_id
    GROUP BY 1, 2, 3
    QUALIFY ROW_NUMBER() OVER(PARTITION BY s.thread_id ORDER BY count(*) DESC) = 1
)

SELECT
    t.thread_id,
    COALESCE(e.entity_name, 'Unlinked Project') as entity_name,
    COALESCE(e.entity_type, 'UNKNOWN') as entity_type,
    t.subject,
    t.message_count,
    t.last_active as last_active_ts,
    
    -- Friction Score Calculation
    (
      (CASE WHEN t.message_count > 10 THEN 50 ELSE t.message_count * 2 END) + 
      (CASE WHEN t.has_escalation THEN 30 ELSE 0 END) +
      (CASE WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), t.last_active, DAY) > 3 THEN 20 ELSE 0 END)
    ) as friction_score,
    
    CASE 
        WHEN t.has_escalation THEN 'ESCALATION'
        WHEN t.message_count > 15 THEN 'HIGH_VOLUME'
        WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), t.last_active, DAY) > 7 THEN 'STALLED'
        ELSE 'NORMAL'
    END as status

FROM ThreadStats t
LEFT JOIN EntityLinks e ON t.thread_id = e.thread_id
WHERE t.message_count > 2 -- Ignore trivial one-offs
ORDER BY friction_score DESC;
