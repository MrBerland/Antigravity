'use server';

import { BigQuery } from '@google-cloud/bigquery';

const bigquery = new BigQuery();

export async function getPotentialSubscriptions(limit = 20) {
  // Find senders with high volume that are NOT already blocked.
  const query = `
    SELECT 
      sender,
      count(*) as count,
      MAX(timestamp) as last_seen,
      ARRAY_AGG(STRUCT(subject, message_id) ORDER BY timestamp DESC LIMIT 1)[OFFSET(0)] as latest
    FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
    WHERE security_verdict != 'BLOCK' OR security_verdict IS NULL
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT @limit
  `;

  const options = {
    query: query,
    params: { limit: limit },
  };

  const [rows] = await bigquery.query(options);

  return rows.map(row => ({
    sender: row.sender,
    count: row.count,
    last_seen: row.last_seen ? row.last_seen.value : '',
    sample_subject: row.latest.subject,
    latest_message_id: row.latest.message_id
  }));
}
