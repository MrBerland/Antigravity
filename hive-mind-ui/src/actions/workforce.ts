'use server';

import { BigQuery } from '@google-cloud/bigquery';

const bigquery = new BigQuery();

export async function getWorkforcePulse() {
    const query = `
    SELECT * 
    FROM \`augos-core-data.hive_mind_core.view_team_pulse\`
    LIMIT 50
  `;

    try {
        const [rows] = await bigquery.query(query);
        return rows;
    } catch (e) {
        console.error(e);
        return [];
    }
}

export async function getUserProfiles() {
    const query = `
    SELECT * 
    FROM \`augos-core-data.hive_mind_core.dim_user_attributes\`
    ORDER BY last_updated DESC
    LIMIT 20
  `;

    try {
        const [rows] = await bigquery.query(query);
        return rows;
    } catch (e) {
        console.error(e);
        return [];
    }
}
