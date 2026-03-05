'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export async function getDashboardStats() {
  // 1. Total Ingested (Staging + Production - duplicate awareness)
  // For simplicity (Lake First), we count everything in Staging.
  const queryStaging = `
    SELECT count(*) as count 
    FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
  `;

  // 2. AI Processed (Production Messages OR Processed Staging)
  // For now, since we have a streaming buffer lock on PROCESSED status, let's just count ALL for the demo
  // OR count items where we have run AI.
  const queryProcessed = `
    SELECT count(*) as count 
    FROM \`augos-core-data.hive_mind_core.fact_work_patterns\`
  `;

  // 3. Blocks (Governance Hits)
  const queryBlocked = `
    SELECT count(*) as count 
    FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
    WHERE security_verdict = 'BLOCK'
  `;

  // Run in parallel
  const [stagingRes, processedRes, blockedRes] = await Promise.all([
    bigquery.query(queryStaging),
    bigquery.query(queryProcessed),
    bigquery.query(queryBlocked)
  ]);

  return {
    totalIngested: stagingRes[0][0].count,
    processed: processedRes[0][0].count, // Now reflects Workforce/AI Analysis count
    blocked: blockedRes[0][0].count,
    activeUsers: 3, // Tim, Maretha, Chris
  };
}

export async function getVelocityData(range: string = '24h') {
  let interval = '24 HOUR';
  let format = '%H:00'; // Hourly by default

  if (range === '7d') {
    interval = '7 DAY';
    format = '%a %d'; // Day name + Number (e.g. Mon 24)
  } else if (range === '30d') {
    interval = '30 DAY';
    format = '%d %b'; // Day + Month (e.g. 24 Jan)
  }

  // Aggregate emails by timebucket for the chart
  const query = `
    SELECT 
      FORMAT_TIMESTAMP('${format}', ingest_time, 'UTC') as name,
      count(*) as emails,
      -- We assume the grouping key is enough for sorting logic logic usually, 
      -- but for string formats it might not sort chronologically. 
      -- We should sort by MIN(timestamp) to get correct timeline order.
      MIN(ingest_time) as sort_key
    FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
    WHERE ingest_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL ${interval})
    GROUP BY 1
    ORDER BY sort_key
  `;

  try {
    const [rows] = await bigquery.query(query);
    // Serialize BigQuery Timestamp objects for Client Component
    return rows.map((r: any) => ({
      ...r,
      sort_key: r.sort_key ? r.sort_key.value : 0 // Convert BQ Timestamp to simple string/number
    }));
  } catch (e) {
    console.error(e);
    return [];
  }
}
