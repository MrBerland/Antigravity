'use client';

import { searchEntities } from '@/actions/intelligence-data';
import { Search, Loader2, Database, Building, User, Briefcase, Zap, AlertCircle } from 'lucide-react';
import { useState } from 'react';

export function EntitySearch() {
    const [term, setTerm] = useState('');
    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [hasSearched, setHasSearched] = useState(false);

    const handleSearch = async () => {
        if (!term || term.length < 2) return;
        setLoading(true);
        setHasSearched(true);
        try {
            const data = await searchEntities(term);
            setResults(data);
        } catch (e) {
            console.error(e);
            setResults([]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    const getIcon = (type: string) => {
        switch (type?.toUpperCase()) {
            case 'COMPANY': return <Building size={16} />;
            case 'person': return <User size={16} />;
            case 'PROJECT': return <Briefcase size={16} />;
            case 'SITE': return <Zap size={16} />;
            default: return <Database size={16} />;
        }
    };

    return (
        <div className="w-full">
            <div className="flex gap-2 mb-6">
                <input
                    type="text"
                    placeholder="Search Knowledge Graph (e.g. 'Solar', 'John', 'Project Alpha')..."
                    value={term}
                    onChange={(e) => setTerm(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all shadow-sm"
                />
                <button
                    onClick={handleSearch}
                    disabled={loading || term.length < 2}
                    className="bg-purple-600 hover:bg-purple-500 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2 shadow-lg shadow-purple-500/20"
                >
                    {loading ? <Loader2 className="animate-spin" size={18} /> : <Search size={18} />}
                    Search
                </button>
            </div>

            {/* Results Grid */}
            {hasSearched && (
                <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-500">
                    <div className="flex items-center justify-between text-xs text-slate-500 uppercase tracking-wider font-semibold px-1">
                        <span>Found {results.length} Entities</span>
                        {results.length > 0 && <span className="text-purple-400">Top Matches</span>}
                    </div>

                    {results.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {results.map((entity, i) => (
                                <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-purple-500/30 transition-all hover:bg-slate-800/50 group cursor-pointer">
                                    <div className="flex justify-between items-start mb-2">
                                        <div className={`p-2 rounded-lg ${entity.entity_type === 'COMPANY' ? 'bg-blue-500/10 text-blue-400' :
                                            entity.entity_type === 'SITE' ? 'bg-yellow-500/10 text-yellow-400' :
                                                entity.entity_type === 'PERSON' ? 'bg-green-500/10 text-green-400' :
                                                    'bg-slate-800 text-slate-400'
                                            }`}>
                                            {getIcon(entity.entity_type)}
                                        </div>
                                        <span className="text-xs font-mono text-slate-500 bg-slate-950 px-2 py-1 rounded">
                                            {entity.link_count || 0} Links
                                        </span>
                                    </div>
                                    <h3 className="text-slate-200 font-medium truncate group-hover:text-purple-300 transition-colors">
                                        {entity.name}
                                    </h3>
                                    <p className="text-xs text-slate-500 mt-1 capitalize">{entity.entity_type?.toLowerCase()}</p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="bg-slate-900/50 border border-dashed border-slate-800 rounded-xl p-8 text-center text-slate-500">
                            <AlertCircle className="mx-auto mb-2 opacity-50" size={24} />
                            <p>No entities found matching "{term}". Try a different search term.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
