'use client';

import { useState } from 'react';
import { BookOpen, HelpCircle, ChevronRight, AlertTriangle, Clock, Hash } from 'lucide-react';
import type { TopQuestion, BestResponse } from '@/actions/knowledge';

// ── Urgency bar ────────────────────────────────────────────────────────────────
function UrgencyBar({ value, max = 5 }: { value: number; max?: number }) {
    const pct = Math.min(100, (value / max) * 100);
    const color = value >= 4 ? 'from-red-500 to-orange-500'
        : value >= 3 ? 'from-yellow-500 to-orange-400'
            : 'from-blue-500 to-cyan-500';
    return (
        <div className="flex items-center gap-2">
            <div className="w-20 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className={`h-full bg-gradient-to-r ${color} rounded-full`} style={{ width: `${pct}%` }} />
            </div>
            <span className="text-[11px] text-slate-500 tabular-nums">{value}/5</span>
        </div>
    );
}

// ── Topic pill ────────────────────────────────────────────────────────────────
const TOPIC_COLORS: Record<string, string> = {
    'Billing': 'bg-green-500/10 text-green-400 border-green-500/20',
    'Support': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    'Technical': 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    'Product': 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    'General': 'bg-slate-700 text-slate-400 border-slate-600',
    'Sales': 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    'Onboarding': 'bg-pink-500/10 text-pink-400 border-pink-500/20',
    'HR': 'bg-orange-500/10 text-orange-400 border-orange-500/20',
};

function TopicPill({ topic }: { topic: string }) {
    const style = TOPIC_COLORS[topic] ?? 'bg-slate-700 text-slate-400 border-slate-600';
    return (
        <span className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full border ${style}`}>
            <Hash size={8} />
            {topic}
        </span>
    );
}

// ── Props ─────────────────────────────────────────────────────────────────────
interface Props {
    questions: TopQuestion[];
    responses: BestResponse[];
    clusters: { topic: string; count: number; avg_urgency: number }[];
    stats: { total_questions: number; total_responses: number; topics_covered: number; high_urgency: number };
}

export default function KnowledgeBaseClient({ questions, responses, clusters, stats }: Props) {
    const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<'questions' | 'responses'>('questions');

    const filteredQuestions = selectedTopic
        ? questions.filter(q => q.topic === selectedTopic)
        : questions;

    const filteredResponses = selectedTopic
        ? responses.filter(r => r.topic === selectedTopic)
        : responses;

    const isEmpty = (activeTab === 'questions' ? filteredQuestions : filteredResponses).length === 0;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <BookOpen className="text-blue-400" />
                        Knowledge Base
                    </h1>
                    <p className="text-slate-500 mt-1">
                        Most-asked questions extracted from inbound email, paired with the best-known responses.
                    </p>
                </div>
            </div>

            {/* Stats row */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                    { label: 'Questions Captured', value: stats.total_questions, icon: HelpCircle, color: 'text-yellow-400 bg-yellow-500/10' },
                    { label: 'Best Responses', value: stats.total_responses, icon: BookOpen, color: 'text-blue-400 bg-blue-500/10' },
                    { label: 'Topics Covered', value: stats.topics_covered, icon: Hash, color: 'text-purple-400 bg-purple-500/10' },
                    { label: 'High Urgency', value: stats.high_urgency, icon: AlertTriangle, color: 'text-red-400 bg-red-500/10' },
                ].map(({ label, value, icon: Icon, color }) => (
                    <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex items-center gap-4">
                        <div className={`p-2.5 rounded-xl ${color}`}><Icon size={16} /></div>
                        <div>
                            <p className="text-2xl font-bold text-slate-100 tabular-nums">{value.toLocaleString()}</p>
                            <p className="text-xs text-slate-500 mt-0.5">{label}</p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Empty state hint */}
            {stats.total_questions === 0 && (
                <div className="flex items-start gap-3 bg-yellow-500/5 border border-yellow-500/15 rounded-xl px-5 py-4">
                    <AlertTriangle size={16} className="text-yellow-400 shrink-0 mt-0.5" />
                    <div>
                        <p className="text-sm font-semibold text-yellow-400">No questions extracted yet</p>
                        <p className="text-xs text-slate-500 mt-0.5">
                            The Question Extractor agent runs as part of the HiveMind pipeline once emails are classified.
                            <code className="ml-2 text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                                python3 HiveMind/hivemind_pipeline.py
                            </code>
                        </p>
                    </div>
                </div>
            )}

            <div className="flex gap-6">
                {/* Left: Topic filter sidebar */}
                <div className="w-52 shrink-0 space-y-1">
                    <p className="text-[10px] uppercase tracking-wider text-slate-500 font-semibold px-2 mb-2">Filter by Topic</p>
                    <button
                        onClick={() => setSelectedTopic(null)}
                        className={`w-full flex justify-between items-center px-3 py-2 rounded-lg text-sm transition-colors ${!selectedTopic ? 'bg-blue-600/15 text-blue-400 font-semibold' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                            }`}
                    >
                        <span>All Topics</span>
                        <span className="text-xs font-mono tabular-nums text-slate-500">{questions.length}</span>
                    </button>
                    {clusters.map(c => (
                        <button
                            key={c.topic}
                            onClick={() => setSelectedTopic(c.topic)}
                            className={`w-full flex justify-between items-center px-3 py-2 rounded-lg text-sm transition-colors ${selectedTopic === c.topic
                                    ? 'bg-blue-600/15 text-blue-400 font-semibold'
                                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                                }`}
                        >
                            <span className="truncate">{c.topic}</span>
                            <div className="flex items-center gap-1.5 shrink-0">
                                {c.avg_urgency >= 4 && <AlertTriangle size={10} className="text-red-400" />}
                                <span className="text-xs font-mono tabular-nums text-slate-500">{c.count}</span>
                            </div>
                        </button>
                    ))}
                </div>

                {/* Right: Main content */}
                <div className="flex-1 min-w-0 space-y-4">
                    {/* Tab bar */}
                    <div className="flex gap-1 bg-slate-950 border border-slate-800 rounded-xl p-1 w-fit">
                        {(['questions', 'responses'] as const).map(tab => (
                            <button
                                key={tab}
                                id={`kb-tab-${tab}`}
                                onClick={() => setActiveTab(tab)}
                                className={`px-4 py-1.5 rounded-lg text-sm font-semibold transition-colors capitalize ${activeTab === tab
                                        ? 'bg-slate-800 text-slate-100'
                                        : 'text-slate-500 hover:text-slate-300'
                                    }`}
                            >
                                {tab === 'questions' ? `Most Asked (${filteredQuestions.length})` : `Best Responses (${filteredResponses.length})`}
                            </button>
                        ))}
                    </div>

                    {/* Questions tab */}
                    {activeTab === 'questions' && (
                        <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                            {isEmpty ? (
                                <p className="px-6 py-12 text-center text-slate-500 italic text-sm">
                                    {selectedTopic ? `No questions in topic "${selectedTopic}" yet.` : 'No questions extracted yet.'}
                                </p>
                            ) : (
                                <div className="divide-y divide-slate-800/60">
                                    {filteredQuestions.map((q, i) => (
                                        <div key={i} className="px-5 py-4 hover:bg-slate-900/60 transition-colors group">
                                            <div className="flex items-start gap-3">
                                                {/* Rank */}
                                                <span className="text-xs font-mono text-slate-600 w-6 shrink-0 mt-0.5 tabular-nums text-right">
                                                    {i + 1}.
                                                </span>
                                                <div className="flex-1 min-w-0">
                                                    {/* Badges */}
                                                    <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                                                        <TopicPill topic={q.topic} />
                                                        {q.ask_count > 1 && (
                                                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                                                                asked {q.ask_count}×
                                                            </span>
                                                        )}
                                                    </div>
                                                    {/* Question text */}
                                                    <p className="text-sm text-slate-200 font-medium leading-snug group-hover:text-white transition-colors">
                                                        {q.question_text}
                                                    </p>
                                                    {/* Meta row */}
                                                    <div className="flex items-center gap-4 mt-2">
                                                        <div className="flex items-center gap-1.5">
                                                            <span className="text-[10px] text-slate-500">Urgency</span>
                                                            <UrgencyBar value={q.avg_urgency} />
                                                        </div>
                                                        <div className="flex items-center gap-1 text-[10px] text-slate-600">
                                                            <Clock size={9} />
                                                            {q.latest_at ? new Date(q.latest_at).toLocaleDateString() : '—'}
                                                        </div>
                                                        <span className="text-[10px] text-slate-600 truncate max-w-[180px]" title={q.latest_sender}>
                                                            {q.latest_sender}
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}

                    {/* Best Responses tab */}
                    {activeTab === 'responses' && (
                        <div className="space-y-3">
                            {isEmpty ? (
                                <div className="bg-slate-950 border border-slate-800 rounded-xl px-6 py-12 text-center text-slate-500 italic text-sm">
                                    {selectedTopic
                                        ? `No best responses for "${selectedTopic}" yet.`
                                        : 'No best responses yet — run the Support Thread Scorer agent.'}
                                </div>
                            ) : (
                                filteredResponses.map((r, i) => (
                                    <div key={i} className="bg-slate-950 border border-slate-800 rounded-xl px-5 py-4 hover:border-slate-700 transition-colors">
                                        <div className="flex items-start justify-between gap-4 mb-3">
                                            <TopicPill topic={r.topic ?? 'General'} />
                                            {r.extracted_at && (
                                                <span className="text-[10px] text-slate-600 flex items-center gap-1 shrink-0">
                                                    <Clock size={9} />
                                                    {new Date(r.extracted_at).toLocaleDateString()}
                                                </span>
                                            )}
                                        </div>
                                        <p className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
                                            {r.best_reply_content}
                                        </p>
                                        {r.thread_id && (
                                            <div className="mt-3 pt-3 border-t border-slate-800/60">
                                                <a
                                                    href={`/emails/thread/${r.thread_id}`}
                                                    className="inline-flex items-center gap-1.5 text-xs text-blue-400 hover:text-blue-300 transition-colors font-medium"
                                                >
                                                    View source thread <ChevronRight size={11} />
                                                </a>
                                            </div>
                                        )}
                                    </div>
                                ))
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
