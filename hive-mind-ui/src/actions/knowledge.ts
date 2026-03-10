'use server';

import { getBigQueryClient } from '@/lib/bigquery';

const bigquery = getBigQueryClient();

export type TopQuestion = {
    topic: string;
    question_text: string;
    ask_count: number;
    avg_urgency: number;
    avg_difficulty: number;
    latest_sender: string;
    latest_at: string | null;
};

export type BestResponse = {
    topic: string;
    best_reply_content: string;
    thread_id: string | null;
    extracted_at: string | null;
};

export type KnowledgeStats = {
    total_questions: number;
    total_responses: number;
    topics_covered: number;
    high_urgency: number;
};

export async function getMostAskedQuestions(limit = 50): Promise<TopQuestion[]> {
    // Group by semantic similarity isn't feasible without embeddings at query time,
    // so we group by exact question_text first, then by topic for the drilldown.
    const query = `
        SELECT
            COALESCE(topic, 'General') AS topic,
            question_text,
            COUNT(*)                                    AS ask_count,
            ROUND(AVG(CAST(urgency AS FLOAT64)), 1)     AS avg_urgency,
            ROUND(AVG(CAST(difficulty AS FLOAT64)), 1)  AS avg_difficulty,
            MAX(sender)                                 AS latest_sender,
            MAX(extracted_at)                           AS latest_at
        FROM \`augos-core-data.hive_mind_core.fact_questions\`
        WHERE question_text IS NOT NULL
          AND LENGTH(TRIM(question_text)) > 10
        GROUP BY topic, question_text
        ORDER BY ask_count DESC, avg_urgency DESC
        LIMIT @limit
    `;
    try {
        const [rows] = await bigquery.query({ query, params: { limit } });
        return rows.map((r: any) => ({
            ...r,
            latest_at: r.latest_at?.value ?? null,
        }));
    } catch (e) {
        console.error('getMostAskedQuestions error:', e);
        return [];
    }
}

export async function getTopicClusters(): Promise<{ topic: string; count: number; avg_urgency: number }[]> {
    const query = `
        SELECT
            COALESCE(topic, 'General') AS topic,
            COUNT(*)                                AS count,
            ROUND(AVG(CAST(urgency AS FLOAT64)), 1) AS avg_urgency
        FROM \`augos-core-data.hive_mind_core.fact_questions\`
        GROUP BY topic
        ORDER BY count DESC
        LIMIT 20
    `;
    try {
        const [rows] = await bigquery.query(query);
        return rows;
    } catch (e) {
        console.error('getTopicClusters error:', e);
        return [];
    }
}

export async function getBestResponses(topic?: string, limit = 30): Promise<BestResponse[]> {
    const query = topic
        ? `SELECT topic, best_reply_content, thread_id, extracted_at
           FROM \`augos-core-data.hive_mind_core.best_responses\`
           WHERE topic = @topic
           ORDER BY extracted_at DESC
           LIMIT @limit`
        : `SELECT topic, best_reply_content, thread_id, extracted_at
           FROM \`augos-core-data.hive_mind_core.best_responses\`
           ORDER BY extracted_at DESC
           LIMIT @limit`;

    try {
        const params = topic ? { topic, limit } : { limit };
        const [rows] = await bigquery.query({ query, params });
        return rows.map((r: any) => ({
            ...r,
            extracted_at: r.extracted_at?.value ?? null,
        }));
    } catch (e) {
        console.error('getBestResponses error:', e);
        return [];
    }
}

export async function getKnowledgeStats(): Promise<KnowledgeStats> {
    const query = `
        SELECT
            (SELECT COUNT(*) FROM \`augos-core-data.hive_mind_core.fact_questions\`) AS total_questions,
            (SELECT COUNT(*) FROM \`augos-core-data.hive_mind_core.best_responses\`)  AS total_responses,
            (SELECT COUNT(DISTINCT topic) FROM \`augos-core-data.hive_mind_core.fact_questions\` WHERE topic IS NOT NULL) AS topics_covered,
            (SELECT COUNTIF(urgency >= 4) FROM \`augos-core-data.hive_mind_core.fact_questions\`) AS high_urgency
    `;
    try {
        const [rows] = await bigquery.query(query);
        return rows[0] as KnowledgeStats;
    } catch (e) {
        console.error('getKnowledgeStats error:', e);
        return { total_questions: 0, total_responses: 0, topics_covered: 0, high_urgency: 0 };
    }
}

/**
 * Semantic KB lookup: embed the user query via VECTOR_SEARCH against
 * fact_embeddings, then join back to fact_questions for the matched messages.
 * Falls back to an empty array if no embeddings exist yet.
 */
export async function semanticSearchKB(
    queryText: string,
    topK = 10
): Promise<(TopQuestion & { similarity: number })[]> {
    if (!queryText || queryText.trim().length < 3) return [];

    const query = `
        WITH query_vec AS (
            SELECT ml_generate_embedding_result AS embedding
            FROM ML.GENERATE_EMBEDDING(
                MODEL \`augos-core-data.hive_mind_core.embedding_model\`,
                (SELECT @query AS content)
            )
        ),
        matches AS (
            SELECT base.message_id, distance
            FROM VECTOR_SEARCH(
                TABLE \`augos-core-data.hive_mind_core.fact_embeddings\`,
                'embedding',
                (SELECT embedding FROM query_vec),
                top_k => @top_k,
                distance_type => 'COSINE'
            )
        )
        SELECT
            COALESCE(q.topic, 'General') AS topic,
            q.question_text,
            COUNT(*)                                    AS ask_count,
            ROUND(AVG(CAST(q.urgency AS FLOAT64)), 1)  AS avg_urgency,
            ROUND(AVG(CAST(q.difficulty AS FLOAT64)), 1) AS avg_difficulty,
            MAX(q.sender)                               AS latest_sender,
            MAX(q.extracted_at)                         AS latest_at,
            ROUND(1 - AVG(m.distance), 3)               AS similarity
        FROM matches m
        JOIN \`augos-core-data.hive_mind_core.fact_questions\` q
            ON m.message_id = q.message_id
        WHERE q.question_text IS NOT NULL
        GROUP BY q.topic, q.question_text
        ORDER BY similarity DESC, ask_count DESC
    `;

    try {
        const [rows] = await bigquery.query({
            query,
            params: { query: queryText.trim(), top_k: topK },
        });
        return rows.map((r: any) => ({
            topic: r.topic,
            question_text: r.question_text,
            ask_count: Number(r.ask_count ?? 1),
            avg_urgency: Number(r.avg_urgency ?? 0),
            avg_difficulty: Number(r.avg_difficulty ?? 0),
            latest_sender: r.latest_sender ?? '',
            latest_at: r.latest_at?.value ?? null,
            similarity: Number(r.similarity ?? 0),
        }));
    } catch (e) {
        console.error('semanticSearchKB error:', e);
        return [];
    }
}

