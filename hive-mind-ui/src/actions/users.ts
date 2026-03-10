'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export type UserStat = {
  email: string;
  totalIngested: number;
  lastSync: string;
  status: 'Active' | 'Idle' | 'New';
};

export async function getUserStats(): Promise<UserStat[]> {
  // Group by sender for internal @augos.io/@augos.cloud mailboxes.
  // Status: Active = sent in last 24h, Idle = sent in last 7d, New = older.
  const query = `
        SELECT
            sender as email,
            COUNT(*) as totalIngested,
            MAX(ingest_time) as lastSync,
            COUNTIF(ingest_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)) as last_24h,
            COUNTIF(ingest_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)) as last_7d
        FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
        WHERE sender LIKE '%@augos.io' OR sender LIKE '%@augos.cloud'
        GROUP BY 1
        ORDER BY 2 DESC
    `;

  try {
    const [rows] = await bigquery.query(query);
    return rows.map((row: any) => {
      const last24h: number = row.last_24h ?? 0;
      const last7d: number = row.last_7d ?? 0;
      const status: UserStat['status'] = last24h > 0 ? 'Active' : last7d > 0 ? 'Idle' : 'New';
      return {
        email: row.email,
        totalIngested: row.totalIngested,
        lastSync: row.lastSync ? new Date(row.lastSync.value).toLocaleString() : 'Never',
        status,
      };
    });
  } catch (e) {
    console.error('getUserStats error:', e);
    return [];
  }
}
