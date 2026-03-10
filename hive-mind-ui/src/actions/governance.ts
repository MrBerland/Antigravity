'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export type GovernanceRule = {
  rule_id: string;
  rule_type: 'ALLOW' | 'BLOCK' | 'MARKETING' | 'PERSONAL' | 'SYSTEM';
  match_type: 'EXACT_EMAIL' | 'DOMAIN_WILDCARD';
  pattern: string;
  added_by: string;
  added_at: string;
  notes: string;
};

export async function getGovernanceRules(): Promise<GovernanceRule[]> {
  try {
    const query = `
            SELECT rule_id, rule_type, match_type, pattern, added_by, added_at, notes
            FROM \`augos-core-data.hive_mind_core.dim_governance_rules\`
            ORDER BY added_at DESC
        `;
    const [rows] = await bigquery.query(query);
    return rows.map((row: any) => ({
      ...row,
      added_at: row.added_at ? new Date(row.added_at.value).toISOString().split('T')[0] : '',
    }));
  } catch (e) {
    console.error('getGovernanceRules error:', e);
    return [];
  }
}

export async function addGovernanceRule(
  pattern: string,
  type: 'ALLOW' | 'BLOCK' | 'MARKETING' | 'PERSONAL' | 'SYSTEM',
  matchType: 'EXACT_EMAIL' | 'DOMAIN_WILDCARD',
  notes: string
) {
  // matchType MUST match the schema enum: EXACT_EMAIL or DOMAIN_WILDCARD
  const query = `
        INSERT INTO \`augos-core-data.hive_mind_core.dim_governance_rules\`
        (rule_id, rule_type, pattern, match_type, added_by, added_at, notes)
        VALUES (GENERATE_UUID(), @type, @pattern, @matchType, 'ui_user', CURRENT_TIMESTAMP(), @notes)
    `;
  await bigquery.query({ query, params: { type, pattern, matchType, notes } });
  return { success: true };
}

export async function deleteGovernanceRule(ruleId: string) {
  const query = `
        DELETE FROM \`augos-core-data.hive_mind_core.dim_governance_rules\`
        WHERE rule_id = @ruleId
    `;
  await bigquery.query({ query, params: { ruleId } });
  return { success: true };
}
