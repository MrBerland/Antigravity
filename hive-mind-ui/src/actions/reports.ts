'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export type ClassificationSummary = {
    security_verdict: string;
    processing_status: string;
    email_count: number;
    pct_of_total: number;
    distinct_sender_domains: number;
};

export type HotLead = {
    sender: string;
    subject: string;
    intent: string;
    estimated_value: string | null;
    urgency: number;
    AI_suggestion: string;
    timestamp: string;
};

export type TopQuestion = {
    topic: string;
    question_text: string;
    urgency: number;
    difficulty: number;
    sender: string;
};

export type KnowledgeEntry = {
    topic: string;
    best_reply_content: string;
    full_email_ref: string;
};

export type ReportSummary = {
    classification: ClassificationSummary[];
    hotLeads: HotLead[];
    topQuestions: TopQuestion[];
    knowledgeBase: KnowledgeEntry[];
    pendingCount: number;
    businessCount: number;
};

export async function getReportSummary(): Promise<ReportSummary> {
    const [classRows, leadRows, questionRows, kbRows, countRows] = await Promise.allSettled([
        // Classification breakdown
        bigquery.query(`
            SELECT security_verdict, processing_status,
                COUNT(*) AS email_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct_of_total,
                COUNT(DISTINCT REGEXP_EXTRACT(sender, r'@(.+)$')) AS distinct_sender_domains
            FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
            GROUP BY 1, 2
            ORDER BY email_count DESC
            LIMIT 20
        `),
        // Hot sales leads
        bigquery.query(`
            SELECT sender, subject,
                JSON_VALUE(sales_analysis, '$.intent') as intent,
                JSON_VALUE(sales_analysis, '$.deal_size_estimate') as estimated_value,
                CAST(JSON_VALUE(sales_analysis, '$.urgency') AS INT64) as urgency,
                JSON_VALUE(sales_analysis, '$.suggested_action') as AI_suggestion,
                timestamp
            FROM \`augos-core-data.hive_mind_core.sales_leads\`
            WHERE JSON_VALUE(sales_analysis, '$.is_lead') = 'true'
              AND CAST(JSON_VALUE(sales_analysis, '$.urgency') AS INT64) >= 6
            ORDER BY urgency DESC, timestamp DESC
            LIMIT 10
        `),
        // Top questions by urgency
        bigquery.query(`
            SELECT topic, question_text, urgency, difficulty, sender
            FROM \`augos-core-data.hive_mind_core.fact_questions\`
            ORDER BY urgency DESC, difficulty DESC
            LIMIT 10
        `),
        // Knowledge base (resolved high-score support threads)
        bigquery.query(`
            SELECT topic, best_reply_content, full_email_ref
            FROM \`augos-core-data.hive_mind_core.best_responses\`
            LIMIT 10
        `),
        // Pending vs business counts
        bigquery.query(`
            SELECT
                COUNTIF(processing_status = 'PENDING' OR processing_status IS NULL) as pending_count,
                COUNTIF(security_verdict = 'BUSINESS') as business_count
            FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
        `),
    ]);

    const safeRows = (result: PromiseSettledResult<any>) =>
        result.status === 'fulfilled' ? result.value[0] : [];

    const countData = countRows.status === 'fulfilled' ? countRows.value[0][0] : {};

    return {
        classification: safeRows(classRows).map((r: any) => ({
            security_verdict: r.security_verdict ?? 'UNCLASSIFIED',
            processing_status: r.processing_status ?? 'PENDING',
            email_count: r.email_count,
            pct_of_total: r.pct_of_total,
            distinct_sender_domains: r.distinct_sender_domains,
        })),
        hotLeads: safeRows(leadRows).map((r: any) => ({
            ...r,
            timestamp: r.timestamp?.value ?? null,
        })),
        topQuestions: safeRows(questionRows),
        knowledgeBase: safeRows(kbRows),
        pendingCount: countData?.pending_count ?? 0,
        businessCount: countData?.business_count ?? 0,
    };
}
