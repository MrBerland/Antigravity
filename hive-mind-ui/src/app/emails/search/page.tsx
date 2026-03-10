import { getSearchStats } from '@/actions/search';
import SemanticSearchClient from '@/components/SemanticSearchClient';

export const dynamic = 'force-dynamic';

export const metadata = {
    title: 'Semantic Search — Hive Mind',
    description: 'Search your email corpus by meaning using vector embeddings.',
};

export default async function SemanticSearchPage() {
    const stats = await getSearchStats();

    return <SemanticSearchClient initialStats={stats} />;
}
