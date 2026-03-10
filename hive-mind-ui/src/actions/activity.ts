'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export type FeedEvent = {
    message_id: string;
    ingest_time: string;
    timestamp: string | null;
    sender: string;
    recipient: string | null;
    subject: string | null;
    snippet: string | null;
    processing_status: string;
    security_verdict: string | null;
    ai_category: string | null;
};

export type FeedStats = {
    total_last_hour: number;
    blocked_last_hour: number;
    pending_count: number;
    processed_count: number;
};

export async function getLiveFeed(limit = 50): Promise<FeedEvent[]> {
    const query = `
        SELECT
            message_id,
            ingest_time,
            timestamp,
            sender,
            recipient,
            subject,
            snippet,
            COALESCE(processing_status, 'PENDING') as processing_status,
            COALESCE(security_verdict, 'UNKNOWN') as security_verdict,
            ai_category
        FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
        ORDER BY ingest_time DESC
        LIMIT @limit
    `;

    try {
        const [rows] = await bigquery.query({ query, params: { limit } });
        return rows.map((row: any) => ({
            ...row,
            ingest_time: row.ingest_time?.value ?? null,
            timestamp: row.timestamp?.value ?? null,
        }));
    } catch (e) {
        console.error('LiveFeed query error:', e);
        return [];
    }
}

export async function getFeedStats(): Promise<FeedStats> {
    const query = `
        SELECT
            COUNTIF(ingest_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)) as total_last_hour,
            COUNTIF(ingest_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR) AND security_verdict = 'BLOCK') as blocked_last_hour,
            COUNTIF(processing_status = 'PENDING' OR processing_status IS NULL) as pending_count,
            COUNTIF(processing_status = 'PROCESSED') as processed_count
        FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
    `;

    try {
        const [rows] = await bigquery.query(query);
        return rows[0] as FeedStats;
    } catch (e) {
        console.error('FeedStats query error:', e);
        return { total_last_hour: 0, blocked_last_hour: 0, pending_count: 0, processed_count: 0 };
    }
}
