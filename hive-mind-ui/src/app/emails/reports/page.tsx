import { getReportSummary } from '@/actions/reports';
import {
    FileText, ShieldAlert, CheckCircle, Clock, Briefcase,
    HelpCircle, BookOpen, TrendingUp, AlertTriangle, ArrowUpRight
} from 'lucide-react';
import Link from 'next/link';

export const dynamic = 'force-dynamic';

const VERDICT_STYLES: Record<string, string> = {
    BUSINESS: 'bg-green-500/10 text-green-400 border-green-500/20',
    MARKETING: 'bg-pink-500/10 text-pink-400 border-pink-500/20',
    PERSONAL: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    SYSTEM: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    BLOCK: 'bg-red-500/10 text-red-400 border-red-500/20',
    HR_SENSITIVE: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
    CONFIDENTIAL: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    UNCLASSIFIED: 'bg-slate-700 text-slate-400 border-slate-600',
    UNKNOWN: 'bg-slate-700 text-slate-400 border-slate-600',
};

const SectionHeader = ({ icon: Icon, title, color }: { icon: any; title: string; color: string }) => (
    <div className="flex items-center gap-2 mb-4">
        <Icon size={18} className={color} />
        <h2 className="text-base font-semibold text-slate-200">{title}</h2>
    </div>
);

export default async function ReportsPage() {
    const data = await getReportSummary();

    const totalEmails = data.classification.reduce((a, r) => a + r.email_count, 0);

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <FileText className="text-blue-400" />
                        Reports &amp; Intelligence
                    </h1>
                    <p className="text-slate-500 mt-1">
                        Classification breakdown and AI agent outputs across the full corpus.
                    </p>
                </div>
                {/* Pipeline health pill */}
                <div className="flex flex-col items-end gap-1.5">
                    <div className="flex items-center gap-2 text-xs font-medium">
                        <span className="text-slate-500">Total emails:</span>
                        <span className="text-slate-200 font-bold">{totalEmails.toLocaleString()}</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className={`inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border font-semibold ${data.pendingCount > 0 ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' : 'bg-green-500/10 text-green-400 border-green-500/20'}`}>
                            <Clock size={11} />
                            {data.pendingCount > 0 ? `${data.pendingCount.toLocaleString()} PENDING` : 'All Classified'}
                        </span>
                        <span className="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border font-semibold bg-green-500/10 text-green-400 border-green-500/20">
                            <CheckCircle size={11} />
                            {data.businessCount.toLocaleString()} BUSINESS
                        </span>
                    </div>
                </div>
            </div>

            {/* ── Grid Row 1: Classification breakdown + Hot Leads ── */}
            <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">

                {/* Classification Breakdown — spans 2 cols */}
                <div className="xl:col-span-2 bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="px-5 py-4 border-b border-slate-800">
                        <SectionHeader icon={ShieldAlert} title="Classification Breakdown" color="text-purple-400" />
                    </div>
                    <div className="divide-y divide-slate-800/60">
                        {data.classification.length === 0 && (
                            <p className="px-5 py-8 text-sm text-slate-500 italic text-center">
                                Run the classifier to see results.
                            </p>
                        )}
                        {data.classification.map((row, i) => {
                            const style = VERDICT_STYLES[row.security_verdict] ?? VERDICT_STYLES.UNKNOWN;
                            const barWidth = Math.max(2, row.pct_of_total);
                            return (
                                <div key={i} className="px-5 py-3 flex items-center gap-3">
                                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border shrink-0 w-28 text-center ${style}`}>
                                        {row.security_verdict}
                                    </span>
                                    <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                        <div className="h-full bg-gradient-to-r from-blue-500/70 to-purple-500/70 rounded-full" style={{ width: `${barWidth}%` }} />
                                    </div>
                                    <span className="text-xs font-mono text-slate-300 w-12 text-right tabular-nums">
                                        {row.email_count.toLocaleString()}
                                    </span>
                                    <span className="text-xs text-slate-500 w-10 text-right tabular-nums">
                                        {row.pct_of_total.toFixed(1)}%
                                    </span>
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* Hot Sales Leads — spans 3 cols */}
                <div className="xl:col-span-3 bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="px-5 py-4 border-b border-slate-800">
                        <SectionHeader icon={TrendingUp} title="Hot Sales Leads" color="text-green-400" />
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="text-[10px] uppercase text-slate-500 font-semibold">
                                <tr>
                                    <th className="px-5 py-3">Sender</th>
                                    <th className="px-5 py-3">Intent</th>
                                    <th className="px-5 py-3">Urgency</th>
                                    <th className="px-5 py-3">Value Est.</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800/60">
                                {data.hotLeads.length === 0 && (
                                    <tr>
                                        <td colSpan={4} className="px-5 py-8 text-center text-slate-500 italic text-sm">
                                            No leads yet — run the Sales Lead Scorer agent.
                                        </td>
                                    </tr>
                                )}
                                {data.hotLeads.map((lead, i) => (
                                    <tr key={i} className="hover:bg-slate-900/60 transition-colors">
                                        <td className="px-5 py-3 text-slate-300 font-medium text-xs truncate max-w-[180px]" title={lead.sender}>
                                            {lead.sender}
                                        </td>
                                        <td className="px-5 py-3">
                                            <span className="bg-blue-500/10 text-blue-400 text-[10px] font-bold px-2 py-0.5 rounded-full border border-blue-500/20">
                                                {lead.intent ?? '—'}
                                            </span>
                                        </td>
                                        <td className="px-5 py-3">
                                            <div className="flex items-center gap-1.5">
                                                <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                                    <div className="h-full bg-gradient-to-r from-yellow-500 to-red-500" style={{ width: `${(lead.urgency / 10) * 100}%` }} />
                                                </div>
                                                <span className="text-xs text-slate-400 font-mono">{lead.urgency}/10</span>
                                            </div>
                                        </td>
                                        <td className="px-5 py-3 text-xs text-slate-400">{lead.estimated_value ?? '—'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            {/* ── Grid Row 2: Questions + Knowledge Base ── */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

                {/* Top Questions */}
                <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="px-5 py-4 border-b border-slate-800 flex items-center justify-between">
                        <SectionHeader icon={HelpCircle} title="Top Inbound Questions" color="text-yellow-400" />
                        <Link href="/emails/knowledge" className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 transition-colors font-medium">
                            View All <ArrowUpRight size={11} />
                        </Link>
                    </div>
                    <div className="divide-y divide-slate-800/60">
                        {data.topQuestions.length === 0 && (
                            <p className="px-5 py-8 text-sm text-slate-500 italic text-center">
                                No questions yet — run the Question Extractor agent.
                            </p>
                        )}
                        {data.topQuestions.map((q, i) => (
                            <div key={i} className="px-5 py-3 space-y-1">
                                <div className="flex items-center gap-2">
                                    <span className="text-[10px] bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 px-2 py-0.5 rounded-full font-bold">
                                        {q.topic ?? 'Unknown'}
                                    </span>
                                    <span className="text-[10px] text-slate-500">urgency {q.urgency}/5</span>
                                </div>
                                <p className="text-sm text-slate-300 leading-snug">{q.question_text}</p>
                                <p className="text-[11px] text-slate-500 truncate">{q.sender}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Knowledge Base */}
                <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="px-5 py-4 border-b border-slate-800 flex items-center justify-between">
                        <SectionHeader icon={BookOpen} title="Knowledge Base (Best Responses)" color="text-blue-400" />
                        <Link href="/emails/knowledge?tab=responses" className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 transition-colors font-medium">
                            View All <ArrowUpRight size={11} />
                        </Link>
                    </div>
                    <div className="divide-y divide-slate-800/60">
                        {data.knowledgeBase.length === 0 && (
                            <p className="px-5 py-8 text-sm text-slate-500 italic text-center">
                                No resolved threads yet — run the Support Thread Scorer agent.
                            </p>
                        )}
                        {data.knowledgeBase.map((entry, i) => (
                            <div key={i} className="px-5 py-3 space-y-1">
                                <div className="flex items-center gap-2">
                                    <span className="text-[10px] bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded-full font-bold">
                                        {entry.topic ?? 'General'}
                                    </span>
                                </div>
                                <p className="text-sm text-slate-300 leading-snug line-clamp-3">{entry.best_reply_content}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* ── Pipeline hint banner if pending ── */}
            {data.pendingCount > 0 && (
                <div className="flex items-start gap-3 bg-yellow-500/5 border border-yellow-500/20 rounded-xl px-5 py-4">
                    <AlertTriangle size={18} className="text-yellow-400 shrink-0 mt-0.5" />
                    <div>
                        <p className="text-sm font-semibold text-yellow-400">{data.pendingCount.toLocaleString()} emails are still PENDING classification</p>
                        <p className="text-xs text-slate-500 mt-0.5">
                            Run the pipeline to classify them and populate agent outputs:
                            <code className="ml-2 text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                                nohup python3 HiveMind/hivemind_pipeline.py &gt; /tmp/hivemind_pipeline.log 2&gt;&amp;1 &amp;
                            </code>
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
}
