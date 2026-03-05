'use server';

import { BigQuery } from '@google-cloud/bigquery';

const bigquery = new BigQuery();

export type Bottleneck = {
    thread_id: string;
    entity_name: string;
    entity_type: string;
    subject: string;
    message_count: number;
    last_active_ts: string; // ISO string
    friction_score: number;
    status: string;
};

export async function getBottlenecks(): Promise<Bottleneck[]> {
    try {
        const query = `
      SELECT *
      FROM \`augos-core-data.hive_mind_core.view_ops_bottlenecks\`
      ORDER BY friction_score DESC
      LIMIT 20
    `;

        // Using simple query
        const [rows] = await bigquery.query(query);

        // Transform timestamps to string to pass to Client Component
        return rows.map((row: any) => ({
            ...row,
            last_active_ts: row.last_active_ts ? row.last_active_ts.value : null
        }));
    } catch (error) {
        console.error("Ops Agent Error:", error);
        return [];
    }
}
