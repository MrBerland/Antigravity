'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export async function getDashboardStats() {
  const [totals, pendingCount, classifiedCount, businessCount, blockedCount, activeUsersCount] =
    await Promise.allSettled([
      // Total in staging
      bigquery.query(`SELECT COUNT(*) as n FROM \`augos-core-data.hive_mind_core.staging_raw_emails\``),
      // Still waiting for AI
      bigquery.query(`
                SELECT COUNT(*) as n
                FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
                WHERE COALESCE(processing_status, 'PENDING') = 'PENDING'
            `),
      // Classified by L1 or L2
      bigquery.query(`
                SELECT COUNT(*) as n
                FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
                WHERE processing_status IN ('CLASSIFIED_L1', 'CLASSIFIED_L2', 'PROCESSED')
            `),
      // Clean BUSINESS emails (the signal)
      bigquery.query(`
                SELECT COUNT(*) as n
                FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
                WHERE security_verdict = 'BUSINESS'
            `),
      // Governance blocks
      bigquery.query(`
                SELECT COUNT(*) as n
                FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
                WHERE security_verdict = 'BLOCK'
            `),
      // Active mailboxes (sent email in last 7 days)
      bigquery.query(`
                SELECT COUNT(DISTINCT REGEXP_EXTRACT(sender, r'@(.+)$')) as n
                FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
                WHERE sender LIKE '%@augos.io'
                  AND ingest_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
            `),
    ]);

  const safe = (r: PromiseSettledResult<any>, fallback = 0): number => {
    if (r.status === 'fulfilled') return r.value[0][0]?.n ?? fallback;
    return fallback;
  };

  const totalIngested = safe(totals);
  const pending = safe(pendingCount);
  const classified = safe(classifiedCount);
  const business = safe(businessCount);
  const blocked = safe(blockedCount);
  const activeUsers = safe(activeUsersCount, 1);
  const pctClassified = totalIngested > 0 ? Math.round((classified / totalIngested) * 100) : 0;

  return {
    totalIngested,
    pending,
    classified,
    business,
    blocked,
    activeUsers,
    pctClassified,
  };
}

export async function getVelocityData(range: string = '24h') {
  const MAP: Record<string, { interval: string; format: string }> = {
    '24h': { interval: '24 HOUR', format: '%H:00' },
    '7d': { interval: '7 DAY', format: '%a %d' },
    '30d': { interval: '30 DAY', format: '%d %b' },
  };
  const { interval, format } = MAP[range] ?? MAP['24h'];

  const query = `
        SELECT
            FORMAT_TIMESTAMP('${format}', ingest_time, 'UTC') as name,
            COUNT(*) as emails,
            COUNTIF(security_verdict = 'BUSINESS') as business,
            COUNTIF(security_verdict = 'BLOCK') as blocked,
            MIN(ingest_time) as sort_key
        FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
        WHERE ingest_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL ${interval})
        GROUP BY 1
        ORDER BY sort_key
    `;

  try {
    const [rows] = await bigquery.query(query);
    return rows.map((r: any) => ({
      name: r.name,
      emails: r.emails,
      business: r.business,
      blocked: r.blocked,
      sort_key: r.sort_key?.value ?? 0,
    }));
  } catch (e) {
    console.error('getVelocityData error:', e);
    return [];
  }
}
