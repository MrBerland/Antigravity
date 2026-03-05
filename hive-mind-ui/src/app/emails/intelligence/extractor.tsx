'use client';

import { extractEntities } from '@/actions/extract';
import { Search, Loader2, Database, Building, Clock, TrendingUp, CheckCircle, XCircle, Zap } from 'lucide-react';
import { useState } from 'react';

export function EntityExtractor() {
    const [msgId, setMsgId] = useState('');
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        if (!msgId) return;
        setLoading(true);
        setResult(null);
        try {
            const data = await extractEntities(msgId);
            setResult(data);
        } catch (e) {
            console.error(e);
            setResult({ error: 'Failed to analyze.' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl">
            <div className="flex gap-2 mb-6">
                <input
                    type="text"
                    placeholder="Paste Gmail Message ID (e.g. 19be9...)"
                    value={msgId}
                    onChange={(e) => setMsgId(e.target.value)}
                    className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                />
                <button
                    onClick={handleAnalyze}
                    disabled={loading || !msgId}
                    className="bg-purple-600 hover:bg-purple-500 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                    {loading ? <Loader2 className="animate-spin" /> : <Search size={18} />}
                    Analyze
                </button>
            </div>

            {/* Procurement Analysis Report */}
            {result?.procurement_analysis?.sites?.length > 0 && (
                <div className="mb-8 space-y-6 animate-in slide-in-from-bottom-4 duration-500">
                    <div className="flex items-center gap-2 text-purple-400 mb-2">
                        <Zap size={20} />
                        <h2 className="text-lg font-semibold">Procurement Opportunities</h2>
                    </div>

                    {result.procurement_analysis.sites.map((site: any, i: number) => (
                        <div key={i} className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                            <div className="bg-slate-900/50 border-b border-slate-800 p-4 flex items-center gap-3">
                                <div className="p-2 bg-slate-800 rounded-lg text-slate-400">
                                    <Building size={20} />
                                </div>
                                <div>
                                    <h3 className="text-lg font-semibold text-slate-200">{site.site_name}</h3>
                                    {site.address && <p className="text-sm text-slate-500">{site.address}</p>}
                                </div>
                            </div>
                            <div className="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {site.tenure_options?.map((opt: any, j: number) => (
                                    <div key={j} className="bg-slate-900 rounded-lg p-5 border border-slate-800 hover:border-purple-500/30 transition-all hover:bg-slate-900/80 group">
                                        <div className="flex justify-between items-start mb-4">
                                            <div className="flex items-center gap-2 text-slate-300">
                                                <Clock size={16} className="text-purple-400" />
                                                <span className="font-medium">{opt.duration}</span>
                                            </div>
                                            {opt.savings_estimate && (
                                                <div className="flex items-center gap-1.5 text-green-400 bg-green-400/10 px-2 py-1 rounded text-xs font-medium">
                                                    <TrendingUp size={12} />
                                                    {opt.savings_estimate}
                                                </div>
                                            )}
                                        </div>

                                        <div className="space-y-3 mb-4">
                                            <div className="flex justify-between text-sm py-1 border-b border-slate-800/50">
                                                <span className="text-slate-500">Rate</span>
                                                <span className="text-slate-200 font-mono">{opt.rate || 'N/A'}</span>
                                            </div>
                                            <div className="flex justify-between text-sm py-1 border-b border-slate-800/50">
                                                <span className="text-slate-500">Escalation</span>
                                                <span className="text-slate-200 font-mono">{opt.escalation || 'N/A'}</span>
                                            </div>
                                        </div>

                                        <div className="space-y-2">
                                            {opt.pros?.slice(0, 2).map((p: string, k: number) => (
                                                <div key={k} className="flex gap-2 text-xs text-slate-400">
                                                    <CheckCircle size={12} className="text-green-500/50 mt-0.5 shrink-0" />
                                                    <span className="line-clamp-2">{p}</span>
                                                </div>
                                            ))}
                                            {opt.cons?.slice(0, 1).map((c: string, k: number) => (
                                                <div key={k} className="flex gap-2 text-xs text-slate-400">
                                                    <XCircle size={12} className="text-red-500/50 mt-0.5 shrink-0" />
                                                    <span className="line-clamp-2">{c}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {result && (
                <div className="bg-slate-900 rounded-lg p-4 border border-slate-800">
                    <div className="flex items-center gap-2 mb-3 text-xs font-semibold text-slate-500 uppercase">
                        <Database size={14} />
                        <span>Raw Analysis Result</span>
                    </div>
                    <pre className="text-xs font-mono text-green-400 overflow-x-auto whitespace-pre-wrap max-h-[500px]">
                        {JSON.stringify(result, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
}
