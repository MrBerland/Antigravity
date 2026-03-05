'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export async function getStagingEmails(page = 1, limit = 50, filter = 'ALL') {
  const offset = (page - 1) * limit;

  let whereClause = '1=1';
  if (filter === 'BLOCKED') {
    whereClause = "security_verdict = 'BLOCK'";
  } else if (filter === 'PENDING') {
    whereClause = "processing_status = 'PENDING'";
  }

  const query = `
    SELECT 
      message_id,
      timestamp,
      sender,
      recipient,
      subject,
      COALESCE(processing_status, 'PENDING') as status,
      COALESCE(security_verdict, 'ALLOW') as verdict
    FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
    WHERE ${whereClause}
    ORDER BY timestamp DESC
    LIMIT @limit OFFSET @offset
  `;

  const countQuery = `
      SELECT count(*) as total 
      FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
      WHERE ${whereClause}
    `;

  const options = {
    query: query,
    params: { limit, offset },
  };

  try {
    const [rows] = await bigquery.query(options);
    const [countRows] = await bigquery.query(countQuery);

    return {
      emails: rows.map(row => ({
        ...row,
        timestamp: row.timestamp ? (row.timestamp.value || new Date(row.timestamp).toISOString()) : null,
      })),
      total: countRows[0].total
    };
  } catch (e) {
    console.error("BigQuery Staging Error:", e);
    return { emails: [], total: 0 };
  }
}
