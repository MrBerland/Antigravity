'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export type Subscription = {
  sender: string;
  count: number;
  category: string;
  last_seen: string;
  sample_subject: string;
  latest_message_id: string;
};

export async function getPotentialSubscriptions(limit = 30): Promise<Subscription[]> {
  // Target MARKETING and PERSONAL classified senders — the real unsubscribe candidates.
  // Exclude already-BLOCKED senders. Require minimum 2 emails to avoid noise.
  const query = `
    SELECT
      sender,
      COUNT(*) as count,
      -- Most common verdict for this sender
      APPROX_TOP_COUNT(COALESCE(security_verdict, 'UNKNOWN'), 1)[OFFSET(0)].value as category,
      MAX(timestamp) as last_seen,
      ARRAY_AGG(
        STRUCT(subject, message_id)
        ORDER BY timestamp DESC LIMIT 1
      )[OFFSET(0)] as latest
    FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
    WHERE COALESCE(security_verdict, 'UNKNOWN') IN ('MARKETING', 'PERSONAL', 'SYSTEM', 'UNKNOWN')
      AND COALESCE(processing_status, 'PENDING') != 'BLOCKED'
    GROUP BY sender
    HAVING COUNT(*) >= 2
    ORDER BY count DESC
    LIMIT @limit
  `;

  try {
    const [rows] = await bigquery.query({ query, params: { limit } });
    return rows.map((row: any) => ({
      sender: row.sender,
      count: row.count,
      category: row.category ?? 'UNKNOWN',
      last_seen: row.last_seen?.value ?? '',
      sample_subject: row.latest?.subject ?? '(no subject)',
      latest_message_id: row.latest?.message_id ?? '',
    }));
  } catch (e) {
    console.error('Subscriptions query error:', e);
    return [];
  }
}
