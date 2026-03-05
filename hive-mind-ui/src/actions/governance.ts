'use server';

import { BigQuery } from '@google-cloud/bigquery';

const bigquery = new BigQuery();

export type GovernanceRule = {
    rule_id: string;
    rule_type: 'ALLOW' | 'BLOCK' | 'QUARANTINE';
    match_type: 'EXACT_EMAIL' | 'DOMAIN_WILDCARD';
    pattern: string;
    added_by: string;
    added_at: string;
    notes: string;
};

export async function getGovernanceRules(): Promise<GovernanceRule[]> {
    const query = `
    SELECT 
      rule_id,
      rule_type,
      match_type,
      pattern,
      added_by,
      added_at,
      notes
    FROM \`augos-core-data.hive_mind_core.dim_governance_rules\`
    ORDER BY added_at DESC
  `;

    const [rows] = await bigquery.query(query);

    return rows.map((row: any) => ({
        ...row,
        added_at: row.added_at ? new Date(row.added_at.value).toISOString().split('T')[0] : '',
    }));
}

export async function addGovernanceRule(pattern: string, type: 'ALLOW' | 'BLOCK', matchType: 'EXACT' | 'LIKE' | 'REGEX', notes: string) {
    // Check if rule already exists (basic check, can be improved)
    // For now, just insert. ID is auto-generated.
    const query = `
    INSERT INTO \`augos-core-data.hive_mind_core.dim_governance_rules\`
    (rule_id, rule_type, pattern, match_type, added_at, notes)
    VALUES
    (GENERATE_UUID(), @type, @pattern, @matchType, CURRENT_TIMESTAMP(), @notes)
  `;

    const options = {
        query: query,
        params: {
            type,
            pattern,
            matchType,
            notes,
        },
    };

    await bigquery.query(options);
    return { success: true };
}
