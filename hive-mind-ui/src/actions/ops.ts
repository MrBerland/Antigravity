'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export type Bottleneck = {
    thread_id: string;
    entity_name: string;
    entity_type: string;
    subject: string;
    message_count: number;
    last_active_ts: string | null;
    friction_score: number;
    status: string;
};

export async function getBottlenecks(): Promise<Bottleneck[]> {
    const query = `
        SELECT *
        FROM \`augos-core-data.hive_mind_core.view_ops_bottlenecks\`
        ORDER BY friction_score DESC
        LIMIT 20
    `;
    try {
        const [rows] = await bigquery.query(query);
        return rows.map((row: any) => ({
            ...row,
            last_active_ts: row.last_active_ts?.value ?? null,
        }));
    } catch (e) {
        console.error('getBottlenecks error:', e);
        return [];
    }
}
