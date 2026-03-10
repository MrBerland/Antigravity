'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export async function getWorkforcePulse() {
    const query = `
        SELECT user_email, category, email_volume, estimated_hours_communication
        FROM \`augos-core-data.hive_mind_core.view_team_pulse\`
        ORDER BY email_volume DESC
        LIMIT 50
    `;
    try {
        const [rows] = await bigquery.query(query);
        return rows;
    } catch (e) {
        console.error('getWorkforcePulse error:', e);
        return [];
    }
}

export async function getUserProfiles() {
    const query = `
        SELECT email, latest_detected_title, detected_skills, last_updated
        FROM \`augos-core-data.hive_mind_core.dim_user_attributes\`
        ORDER BY last_updated DESC
        LIMIT 20
    `;
    try {
        const [rows] = await bigquery.query(query);
        return rows;
    } catch (e) {
        console.error('getUserProfiles error:', e);
        return [];
    }
}
