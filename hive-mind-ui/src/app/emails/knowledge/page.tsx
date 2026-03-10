import {
    getMostAskedQuestions,
    getBestResponses,
    getTopicClusters,
    getKnowledgeStats,
} from '@/actions/knowledge';
import KnowledgeBaseClient from '@/components/KnowledgeBaseClient';

export const dynamic = 'force-dynamic';

export default async function KnowledgePage() {
    const [questions, responses, clusters, stats] = await Promise.all([
        getMostAskedQuestions(100),
        getBestResponses(undefined, 50),
        getTopicClusters(),
        getKnowledgeStats(),
    ]);

    return (
        <KnowledgeBaseClient
            questions={questions}
            responses={responses}
            clusters={clusters}
            stats={stats}
        />
    );
}
