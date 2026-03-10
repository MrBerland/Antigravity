'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

const PROJECT = 'augos-core-data';
const DATASET = 'hive_mind_core';

export type SearchResult = {
    message_id: string;
    thread_id: string | null;
    subject: string;
    sender: string;
    snippet: string;
    timestamp: string | null;
    security_verdict: string | null;
    distance: number;
};

export type SearchStats = {
    total_embedded: number;
    last_embedded_at: string | null;
};

/**
 * Semantic vector search over embedded emails.
 * Embeds the user's query through ML.GENERATE_EMBEDDING at query time,
 * then runs VECTOR_SEARCH against fact_embeddings.
 */
// COSINE distance threshold — results above this are considered too dissimilar to be useful.
// 0 = identical vectors, 1 = orthogonal. 0.55 = ~45% similarity minimum.
const MAX_DISTANCE = 0.55;

export async function semanticSearch(queryText: string, topK = 20): Promise<SearchResult[]> {
    if (!queryText || queryText.trim().length < 3) return [];

    // Problem: fact_embeddings can have multiple rows per message_id due to duplicate
    // pipeline runs. VECTOR_SEARCH treats each row as a separate candidate, inflating
    // results. Fix: deduplicate embeddings with ROW_NUMBER() before searching, keeping
    // the most recently embedded copy per message. We request top_k * 6 internally to
    // ensure enough unique messages survive after deduplication in the outer GROUP BY.
    const internalK = topK * 6;

    const query = `
        WITH query_vec AS (
            SELECT ml_generate_embedding_result AS embedding
            FROM ML.GENERATE_EMBEDDING(
                MODEL \`${PROJECT}.${DATASET}.embedding_model\`,
                (SELECT @query AS content)
            )
        ),
        -- Deduplicate: keep only the most recent embedding per message
        deduped_embeddings AS (
            SELECT message_id, embedding
            FROM (
                SELECT
                    message_id,
                    embedding,
                    ROW_NUMBER() OVER (PARTITION BY message_id ORDER BY embedded_at DESC) AS rn
                FROM \`${PROJECT}.${DATASET}.fact_embeddings\`
            )
            WHERE rn = 1
        ),
        raw_matches AS (
            SELECT
                base.message_id,
                distance
            FROM VECTOR_SEARCH(
                (SELECT message_id, embedding FROM deduped_embeddings),
                'embedding',
                (SELECT embedding FROM query_vec),
                top_k => @internal_k,
                distance_type => 'COSINE'
            )
        ),
        -- After dedup, take the best distance per message and apply relevance threshold
        best_matches AS (
            SELECT message_id, MIN(distance) AS distance
            FROM raw_matches
            GROUP BY message_id
            HAVING MIN(distance) <= @max_distance
            ORDER BY distance ASC
            LIMIT @top_k
        )
        SELECT
            m.message_id,
            s.thread_id,
            s.subject,
            s.sender,
            s.snippet,
            s.timestamp,
            s.security_verdict,
            m.distance
        FROM best_matches m
        JOIN \`${PROJECT}.${DATASET}.staging_raw_emails\` s
            ON m.message_id = s.message_id
        ORDER BY m.distance ASC
    `;

    try {
        const [rows] = await bigquery.query({
            query,
            params: {
                query: queryText.trim(),
                top_k: topK,
                internal_k: internalK,
                max_distance: MAX_DISTANCE,
            },
        });
        return rows.map((r: any) => ({
            message_id: r.message_id,
            thread_id: r.thread_id ?? null,
            subject: r.subject ?? '(no subject)',
            sender: r.sender ?? '',
            snippet: r.snippet ?? '',
            timestamp: r.timestamp?.value ?? null,
            security_verdict: r.security_verdict ?? null,
            distance: typeof r.distance === 'number' ? r.distance : parseFloat(r.distance ?? '1'),
        }));
    } catch (e) {
        console.error('semanticSearch error:', e);
        return [];
    }
}

/**
 * Returns embedding coverage stats for the header.
 */
export async function getSearchStats(): Promise<SearchStats> {
    const query = `
        SELECT
            COUNT(*) AS total_embedded,
            MAX(embedded_at) AS last_embedded_at
        FROM \`${PROJECT}.${DATASET}.fact_embeddings\`
    `;
    try {
        const [rows] = await bigquery.query(query);
        return {
            total_embedded: Number(rows[0]?.total_embedded ?? 0),
            last_embedded_at: rows[0]?.last_embedded_at?.value ?? null,
        };
    } catch (e) {
        console.error('getSearchStats error:', e);
        return { total_embedded: 0, last_embedded_at: null };
    }
}
