'use client';

import { useState, useTransition, useRef } from 'react';
import { Search, Sparkles, Loader2, ExternalLink, Mail, Clock, ShieldCheck, ChevronRight, AlertCircle, Zap } from 'lucide-react';
import { semanticSearch, type SearchResult } from '@/actions/search';

// ─── Similarity badge ──────────────────────────────────────────────────────────
function SimilarityBadge({ distance }: { distance: number }) {
    // COSINE distance: 0 = identical, 1 = orthogonal
    const pct = Math.round((1 - distance) * 100);
    const color =
        pct >= 80 ? 'from-emerald-500 to-teal-500' :
            pct >= 60 ? 'from-blue-500 to-cyan-500' :
                pct >= 40 ? 'from-yellow-500 to-orange-400' :
                    'from-slate-600 to-slate-500';
    return (
        <div className="flex items-center gap-1.5 shrink-0">
            <div className="relative w-7 h-7">
                <svg viewBox="0 0 36 36" className="w-7 h-7 -rotate-90">
                    <circle cx="18" cy="18" r="15" fill="none" stroke="#1e293b" strokeWidth="4" />
                    <circle
                        cx="18" cy="18" r="15" fill="none"
                        stroke="url(#sg)" strokeWidth="4" strokeLinecap="round"
                        strokeDasharray={`${pct * 0.942} 94.2`}
                    />
                    <defs>
                        <linearGradient id="sg" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor={pct >= 80 ? '#10b981' : pct >= 60 ? '#3b82f6' : pct >= 40 ? '#eab308' : '#64748b'} />
                            <stop offset="100%" stopColor={pct >= 80 ? '#14b8a6' : pct >= 60 ? '#06b6d4' : pct >= 40 ? '#f97316' : '#475569'} />
                        </linearGradient>
                    </defs>
                </svg>
                <span className="absolute inset-0 flex items-center justify-center text-[8px] font-bold text-slate-300">
                    {pct}
                </span>
            </div>
            <span className="text-[10px] text-slate-500 font-medium">match</span>
        </div>
    );
}

// ─── Verdict chip ──────────────────────────────────────────────────────────────
const VERDICT_STYLES: Record<string, string> = {
    BUSINESS: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    PERSONAL: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    MARKETING: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    SYSTEM: 'bg-slate-700/60 text-slate-400 border-slate-600',
    CONFIDENTIAL: 'bg-red-500/10 text-red-400 border-red-500/20',
    HR_SENSITIVE: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
};

function VerdictChip({ verdict }: { verdict: string | null }) {
    if (!verdict) return null;
    const style = VERDICT_STYLES[verdict] ?? 'bg-slate-700/60 text-slate-400 border-slate-600';
    return (
        <span className={`inline-flex items-center gap-1 text-[9px] font-bold px-2 py-0.5 rounded-full border ${style}`}>
            <ShieldCheck size={8} />
            {verdict}
        </span>
    );
}

// ─── Result card ───────────────────────────────────────────────────────────────
function ResultCard({ result, rank }: { result: SearchResult; rank: number }) {
    const date = result.timestamp ? new Date(result.timestamp).toLocaleDateString('en-ZA', { day: 'numeric', month: 'short', year: 'numeric' }) : null;
    const senderShort = result.sender.replace(/<.*>/, '').trim() || result.sender;

    return (
        <div className="group bg-slate-900/60 border border-slate-800 hover:border-slate-600 rounded-xl p-5 transition-all duration-200 hover:bg-slate-900">
            <div className="flex items-start gap-4">
                {/* Rank */}
                <span className="text-xs font-mono text-slate-600 w-5 shrink-0 mt-1 tabular-nums text-right">{rank}.</span>

                {/* Content */}
                <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4 mb-2">
                        <div className="flex items-center gap-2 flex-wrap">
                            <VerdictChip verdict={result.security_verdict} />
                            {date && (
                                <span className="inline-flex items-center gap-1 text-[10px] text-slate-500">
                                    <Clock size={9} /> {date}
                                </span>
                            )}
                        </div>
                        <SimilarityBadge distance={result.distance} />
                    </div>

                    {/* Subject */}
                    <p className="text-sm font-semibold text-slate-100 group-hover:text-white transition-colors leading-snug mb-1 truncate">
                        {result.subject}
                    </p>

                    {/* Sender */}
                    <div className="flex items-center gap-1.5 mb-2">
                        <Mail size={10} className="text-slate-500 shrink-0" />
                        <span className="text-xs text-slate-500 truncate">{senderShort}</span>
                    </div>

                    {/* Snippet */}
                    {result.snippet && (
                        <p className="text-xs text-slate-400 leading-relaxed line-clamp-2 mt-1">
                            {result.snippet}
                        </p>
                    )}

                    {/* Thread link */}
                    {result.thread_id && (
                        <div className="mt-3 pt-3 border-t border-slate-800/60">
                            <a
                                href={`/emails/thread/${result.thread_id}`}
                                className="inline-flex items-center gap-1.5 text-xs text-blue-400 hover:text-blue-300 transition-colors font-medium"
                            >
                                Open thread <ChevronRight size={11} />
                            </a>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

// ─── Suggestion pills ──────────────────────────────────────────────────────────
const SUGGESTIONS = [
    'outstanding invoices',
    'meter maintenance',
    'contract renewal',
    'load shedding impact',
    'site visit schedule',
    'pricing query',
    'consumption report',
    'technical fault',
];

// ─── Main component ────────────────────────────────────────────────────────────
interface Props {
    initialStats: { total_embedded: number; last_embedded_at: string | null };
}

export default function SemanticSearchClient({ initialStats }: Props) {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<SearchResult[]>([]);
    const [hasSearched, setHasSearched] = useState(false);
    const [isPending, startTransition] = useTransition();
    const inputRef = useRef<HTMLInputElement>(null);

    const doSearch = (q: string) => {
        const text = q.trim();
        if (!text || text.length < 3) return;
        setHasSearched(true);
        startTransition(async () => {
            const res = await semanticSearch(text, 20);
            setResults(res);
        });
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') doSearch(query);
    };

    const handleSuggestion = (s: string) => {
        setQuery(s);
        doSearch(s);
        inputRef.current?.focus();
    };

    const lastEmbeddedDate = initialStats.last_embedded_at
        ? new Date(initialStats.last_embedded_at).toLocaleDateString('en-ZA', { day: 'numeric', month: 'short', year: 'numeric' })
        : null;

    return (
        <div className="space-y-8">
            {/* ── Header ──────────────────────────────────────────────────── */}
            <div>
                <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                    <Sparkles className="text-purple-400" />
                    Semantic Search
                </h1>
                <p className="text-slate-500 mt-1">
                    Find emails by <span className="text-purple-400 font-medium">meaning</span>, not just keywords — powered by vector embeddings.
                </p>
            </div>

            {/* ── Coverage stat bar ────────────────────────────────────────── */}
            <div className="flex items-center gap-6 bg-slate-900/60 border border-slate-800 rounded-xl px-5 py-3">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <span className="text-sm text-slate-300 font-semibold tabular-nums">
                        {initialStats.total_embedded.toLocaleString()}
                    </span>
                    <span className="text-xs text-slate-500">emails in vector index</span>
                </div>
                {lastEmbeddedDate && (
                    <>
                        <div className="w-px h-4 bg-slate-700" />
                        <span className="text-xs text-slate-500 flex items-center gap-1">
                            <Clock size={10} /> Last indexed {lastEmbeddedDate}
                        </span>
                    </>
                )}
                <div className="ml-auto flex items-center gap-1.5 text-xs text-purple-400 font-medium">
                    <Zap size={11} />
                    BigQuery VECTOR_SEARCH
                </div>
            </div>

            {/* ── Search bar ───────────────────────────────────────────────── */}
            <div className="relative">
                <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
                <input
                    ref={inputRef}
                    id="semantic-search-input"
                    type="text"
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="e.g. contract dispute with Tiger Brands about pricing…"
                    className="w-full bg-slate-900 border border-slate-700 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 rounded-xl pl-11 pr-32 py-4 text-sm text-slate-100 placeholder-slate-600 outline-none transition-all"
                />
                <button
                    id="semantic-search-btn"
                    onClick={() => doSearch(query)}
                    disabled={isPending || query.trim().length < 3}
                    className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-semibold transition-colors"
                >
                    {isPending ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />}
                    Search
                </button>
            </div>

            {/* ── Low confidence notice ────────────────────────────────────── */}
            {!isPending && results.length > 0 && results[0].distance > 0.45 && (
                <div className="flex items-start gap-3 bg-slate-800/40 border border-slate-700 rounded-xl px-5 py-3">
                    <AlertCircle size={15} className="text-slate-400 shrink-0 mt-0.5" />
                    <p className="text-xs text-slate-400">
                        <span className="font-semibold text-slate-300">Low confidence results.</span>{' '}
                        No emails closely matched your query — showing the nearest vectors found. Try a shorter or more specific phrase.
                    </p>
                </div>
            )}

            {/* ── Suggestion pills ─────────────────────────────────────────── */}
            {!hasSearched && (
                <div className="space-y-2">
                    <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">Try searching for</p>
                    <div className="flex flex-wrap gap-2">
                        {SUGGESTIONS.map(s => (
                            <button
                                key={s}
                                id={`suggestion-${s.replace(/\s+/g, '-')}`}
                                onClick={() => handleSuggestion(s)}
                                className="px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 hover:border-purple-500/50 hover:bg-slate-700 text-xs text-slate-300 hover:text-white transition-all"
                            >
                                {s}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* ── Loading skeleton ─────────────────────────────────────────── */}
            {isPending && (
                <div className="space-y-3">
                    {[...Array(5)].map((_, i) => (
                        <div key={i} className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 animate-pulse">
                            <div className="flex gap-4">
                                <div className="w-4 h-4 bg-slate-800 rounded" />
                                <div className="flex-1 space-y-2">
                                    <div className="h-3 bg-slate-800 rounded w-1/4" />
                                    <div className="h-4 bg-slate-800 rounded w-2/3" />
                                    <div className="h-3 bg-slate-800 rounded w-full" />
                                </div>
                            </div>
                        </div>
                    ))}
                    <p className="text-center text-xs text-slate-500 italic pt-2">
                        Embedding query and searching {initialStats.total_embedded.toLocaleString()} vectors…
                    </p>
                </div>
            )}

            {/* ── No results ───────────────────────────────────────────────── */}
            {!isPending && hasSearched && results.length === 0 && (
                <div className="flex items-start gap-3 bg-slate-800/40 border border-slate-700 rounded-xl px-5 py-4">
                    <AlertCircle size={16} className="text-slate-400 shrink-0 mt-0.5" />
                    <div>
                        <p className="text-sm font-semibold text-slate-300">No relevant emails found</p>
                        <p className="text-xs text-slate-500 mt-1">
                            No emails in the index are semantically similar enough to your query (minimum 45% similarity required).
                            This likely means there are genuinely no emails on this topic — not a data issue.
                        </p>
                        <p className="text-xs text-slate-600 mt-1.5">
                            Try a shorter phrase, different keywords, or check the pipeline has been run recently.
                        </p>
                    </div>
                </div>
            )}

            {/* ── Results ──────────────────────────────────────────────────── */}
            {!isPending && results.length > 0 && (
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <p className="text-sm text-slate-400">
                            <span className="font-semibold text-slate-200">{results.length}</span> results for{' '}
                            <span className="text-purple-400 font-medium">"{query}"</span>
                        </p>
                        <button
                            onClick={() => { setResults([]); setHasSearched(false); setQuery(''); }}
                            className="text-xs text-slate-500 hover:text-slate-300 transition-colors"
                        >
                            Clear
                        </button>
                    </div>

                    {/* Results grid */}
                    <div className="space-y-3">
                        {results.map((r, i) => (
                            <ResultCard key={r.message_id} result={r} rank={i + 1} />
                        ))}
                    </div>

                    {/* Footer note */}
                    <p className="text-center text-xs text-slate-600 pt-2">
                        Results ranked by cosine similarity · powered by Gemini text-embedding-004
                    </p>
                </div>
            )}
        </div>
    );
}
