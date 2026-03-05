'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export type UserStat = {
  email: string;
  totalIngested: number;
  lastSync: string;
  status: 'Active' | 'Idle';
};

export async function getUserStats(): Promise<UserStat[]> {
  /* 
     Since we currently only ingest SENT items, the 'sender' is the Augos User.
     We group by sender to get the stats per mailbox.
  */
  const query = `
    SELECT 
      sender as email,
      count(*) as totalIngested,
      MAX(timestamp) as lastSync
    FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
    WHERE sender LIKE '%@augos.io%' 
       OR sender LIKE '%@augos.cloud%'
    GROUP BY 1
    ORDER BY 2 DESC
  `;

  const [rows] = await bigquery.query(query);

  return rows.map((row: any) => ({
    email: row.email,
    totalIngested: row.totalIngested,
    lastSync: row.lastSync ? new Date(row.lastSync.value).toLocaleString() : 'Never',
    status: 'Active' // simplistic for now
  }));
}
