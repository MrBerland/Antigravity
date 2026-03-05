'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export async function getGraphStats() {
    const query = `
    SELECT 
        e.name,
        e.entity_type,
        count(f.message_id) as links
    FROM \`augos-core-data.hive_mind_core.fact_email_entities\` f
    JOIN \`augos-core-data.hive_mind_core.dim_entities\` e ON f.entity_id = e.entity_id
    GROUP BY 1, 2
    ORDER BY 3 DESC
    LIMIT 10
  `;

    try {
        const [rows] = await bigquery.query(query);
        return rows;
    } catch (e) {
        console.error(e);
        return [];
    }
}

export async function getRecentLinks() {
    const query = `
    SELECT 
        e.name,
        e.entity_type,
        s.subject,
        s.sender,
        f.confidence,
        f.source,
        s.timestamp,
        s.message_id
    FROM \`augos-core-data.hive_mind_core.fact_email_entities\` f
    JOIN \`augos-core-data.hive_mind_core.dim_entities\` e ON f.entity_id = e.entity_id
    JOIN \`augos-core-data.hive_mind_core.staging_raw_emails\` s ON f.message_id = s.message_id
    ORDER BY s.timestamp DESC
    LIMIT 10
  `;

    try {
        const [rows] = await bigquery.query(query);
        return rows;
    } catch (e) {
        console.error(e);
        return [];
    }
}

export async function getTotalCounts() {
    const query = `
    SELECT 
      (SELECT count(*) FROM \`augos-core-data.hive_mind_core.dim_entities\`) as total_entities,
      (SELECT count(*) FROM \`augos-core-data.hive_mind_core.fact_email_entities\`) as total_links
  `;
    try {
        const [rows] = await bigquery.query(query);
        return rows[0] || { total_entities: 0, total_links: 0 };
    } catch (e) {
        console.error(e);
        return { total_entities: 0, total_links: 0 };
    }
}

export async function getSystemHealth() {
    const query = `
    SELECT max(timestamp) as last_sync
    FROM \`augos-core-data.hive_mind_core.staging_raw_emails\`
  `;
    try {
        const [rows] = await bigquery.query(query);
        const lastSync = rows[0]?.last_sync?.value || null;
        return { last_sync: lastSync };
    } catch (e) {
        console.error(e);
        return { last_sync: null };
    }
}

export async function searchEntities(term: string) {
    if (!term || term.length < 2) return [];

    // Safe approach: create parameterized query if possible, or careful string interpolation
    // BigQuery node client supports parameterized queries.
    // BUT user input must be sanitized if not parameterized.
    // Using generic search:

    const query = `
    SELECT 
        name,
        entity_type, 
        count(f.message_id) as link_count
    FROM \`augos-core-data.hive_mind_core.dim_entities\` e
    LEFT JOIN \`augos-core-data.hive_mind_core.fact_email_entities\` f ON e.entity_id = f.entity_id
    WHERE lower(name) LIKE @term
    GROUP BY 1, 2
    ORDER BY 3 DESC
    LIMIT 20
  `;

    const options = {
        query: query,
        params: { term: `%${term.toLowerCase()}%` }
    };

    try {
        const [rows] = await bigquery.query(options);
        return rows;
    } catch (e) {
        console.error(e);
        return [];
    }
}
