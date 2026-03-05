-- Agent: The Workforce Analyst
-- Goal: Analyze internal communications to understand time allocation, patterns, and enrich user profiles.

-- 1. Create Work Classification Model (if not exists, we reuse the generic Gemini Pro connection)
-- We assume `hive_mind_core.gemini_pro` or similar connection exists.

-- 2. Analyze "Sent" Emails for Time Allocation
-- We only look at emails SENT by internal users.
CREATE OR REPLACE PROCEDURE `hive_mind_core.analyze_workforce_patterns`(batch_size INT64)
BEGIN
    -- A. Identify Internal Sent Emails not yet analyzed
    -- We assume 'Internal' means sender contains '@augos.io' (or domain param)
    EXECUTE IMMEDIATE FORMAT("""
        CREATE TEMP TABLE pending_analysis AS
        SELECT 
            message_id,
            sender,
            subject,
            snippet,
            timestamp
        FROM `augos-core-data.hive_mind_core.v_business_emails`  -- ✅ CLEAN FEED ONLY
        WHERE 
            sender LIKE '%%@augos.io'  -- ✅ FIXED: internal senders only (was broken wildcard)
            AND message_id NOT IN (SELECT message_id FROM `hive_mind_core.fact_work_patterns`)
        LIMIT %d
    """, batch_size);

    -- B. Run Gemini Analysis for Categorization & Profile Enrichment
    CREATE TEMP TABLE ai_results AS
    SELECT *
    FROM ML.GENERATE_TEXT(
        MODEL `hive_mind_core.gemini_flash`, -- Using existing Flash model
        (
            SELECT 
                message_id,
                CONCAT(
                    'Analyze this email sent by an employee. ',
                    '1. Classify the "Work Context" into exactly one of: [DEVELOPMENT, SALES, SUPPORT, MANAGEMENT, RECRUITING, ADMIN, PERSONAL]. ',
                    '2. Extract the sender\'s likely "Job Title" and "Skills" demonstrated if apparent (e.g. if they talk about SQL, they know SQL). ',
                    '3. Return JSON: {"category": "CATEGORY", "title_guess": "string", "skills": ["skill1", "skill2"], "is_urgent": boolean}. ',
                    'Return ONLY raw JSON. No markdown formatting. No explanations. ',
                    'Email Subject: ', subject, '. Snippet: ', snippet
                ) as prompt
            FROM pending_analysis
        ),
        STRUCT(0.1 AS temperature, TRUE AS flatten_json_output)
    );

    -- C. Store Work Patterns (Time/Focus Analysis)
    INSERT INTO `hive_mind_core.fact_work_patterns` (analysis_id, message_id, user_email, category, urgency, analyzed_at)
    SELECT
        GENERATE_UUID(),
        p.message_id,
        p.sender,
        JSON_VALUE(a.ml_generate_text_llm_result, '$.category'),
        CAST(JSON_VALUE(a.ml_generate_text_llm_result, '$.is_urgent') AS BOOL),
        CURRENT_TIMESTAMP()
    FROM pending_analysis p
    JOIN ai_results a ON p.message_id = a.message_id;

    -- D. Enrich User Profiles (The "Ambition")
    -- We extract skills/titles and UPSERT them into a user_attributes table
    MERGE `hive_mind_core.dim_user_attributes` T
    USING (
        SELECT 
            p.sender as email,
            JSON_VALUE(a.ml_generate_text_llm_result, '$.title_guess') as title,
            ARRAY(SELECT JSON_VALUE(s, '$') FROM UNNEST(JSON_QUERY_ARRAY(a.ml_generate_text_llm_result, '$.skills')) s) as skills
        FROM pending_analysis p
        JOIN ai_results a ON p.message_id = a.message_id
        WHERE JSON_VALUE(a.ml_generate_text_llm_result, '$.title_guess') IS NOT NULL
        QUALIFY ROW_NUMBER() OVER(PARTITION BY p.sender ORDER BY p.message_id DESC) = 1
    ) S
    ON T.email = S.email
    WHEN MATCHED THEN
        UPDATE SET 
            latest_detected_title = S.title,
            detected_skills = S.skills,
            last_updated = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN
        INSERT (email, latest_detected_title, detected_skills, last_updated)
        VALUES (S.email, S.title, S.skills, CURRENT_TIMESTAMP());

    SELECT FORMAT('Analyzed %d sent emails for workforce patterns.', (SELECT count(*) FROM pending_analysis)) as status;
END;

-- 3. The "Pulse" View (Dashboarding)
-- What is the team working on this week?
CREATE OR REPLACE VIEW `hive_mind_core.view_team_pulse` AS
SELECT
    user_email,
    category,
    count(*) as email_volume,
    -- rudimentary "hours" estimate: 5 mins per email
    count(*) * 5.0 / 60.0 as estimated_hours_communication
FROM `hive_mind_core.fact_work_patterns`
WHERE analyzed_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY 1, 2
ORDER BY 1, 3 DESC;
