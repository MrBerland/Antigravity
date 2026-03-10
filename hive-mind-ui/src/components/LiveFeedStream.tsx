'use client';

import { useEffect, useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';
import { ShieldAlert, Clock, CheckCircle, Mail, RefreshCw } from 'lucide-react';
import type { FeedEvent } from '@/actions/activity';

interface Props {
    initialEvents: FeedEvent[];
}

const VERDICT_MAP: Record<string, { label: string; className: string; dot: string; icon: React.ReactNode }> = {
    BLOCK: { label: 'Blocked', className: 'bg-red-500/10 text-red-400 border-red-500/20', dot: 'bg-red-400', icon: <ShieldAlert size={11} /> },
    MARKETING: { label: 'Marketing', className: 'bg-pink-500/10 text-pink-400 border-pink-500/20', dot: 'bg-pink-400', icon: <Mail size={11} /> },
    PERSONAL: { label: 'Personal', className: 'bg-purple-500/10 text-purple-400 border-purple-500/20', dot: 'bg-purple-400', icon: <Mail size={11} /> },
    SYSTEM: { label: 'System', className: 'bg-blue-500/10 text-blue-400 border-blue-500/20', dot: 'bg-blue-400', icon: <Mail size={11} /> },
    BUSINESS: { label: 'Business', className: 'bg-green-500/10 text-green-400 border-green-500/20', dot: 'bg-green-400', icon: <CheckCircle size={11} /> },
    HR_SENSITIVE: { label: 'HR', className: 'bg-orange-500/10 text-orange-400 border-orange-500/20', dot: 'bg-orange-400', icon: <ShieldAlert size={11} /> },
};

function getVerdictBadge(verdict: string, status: string) {
    if (verdict && VERDICT_MAP[verdict]) return VERDICT_MAP[verdict];
    if (status === 'PENDING') {
        return { label: 'Pending', className: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20', dot: 'bg-yellow-400', icon: <Clock size={11} /> };
    }
    return { label: 'Processed', className: 'bg-slate-700 text-slate-400 border-slate-600', dot: 'bg-slate-500', icon: <CheckCircle size={11} /> };
}


function timeAgo(dateStr: string | null): string {
    if (!dateStr) return '—';
    const diff = Date.now() - new Date(dateStr).getTime();
    const s = Math.floor(diff / 1000);
    if (s < 60) return `${s}s ago`;
    const m = Math.floor(s / 60);
    if (m < 60) return `${m}m ago`;
    const h = Math.floor(m / 60);
    if (h < 24) return `${h}h ago`;
    return `${Math.floor(h / 24)}d ago`;
}

function extractDomain(sender: string): string {
    const match = sender.match(/@([\w.-]+)/);
    return match ? match[1] : sender;
}

export default function LiveFeedStream({ initialEvents }: Props) {
    const router = useRouter();
    const [isPending, startTransition] = useTransition();
    const [lastRefresh, setLastRefresh] = useState<Date>(new Date());
    const [secondsAgo, setSecondsAgo] = useState(0);

    // Auto-refresh every 30s
    useEffect(() => {
        const refresh = setInterval(() => {
            startTransition(() => router.refresh());
            setLastRefresh(new Date());
            setSecondsAgo(0);
        }, 30_000);
        return () => clearInterval(refresh);
    }, [router]);

    // Tick the "X seconds ago" counter
    useEffect(() => {
        const tick = setInterval(() => {
            setSecondsAgo(Math.floor((Date.now() - lastRefresh.getTime()) / 1000));
        }, 1000);
        return () => clearInterval(tick);
    }, [lastRefresh]);

    const handleManualRefresh = () => {
        startTransition(() => router.refresh());
        setLastRefresh(new Date());
        setSecondsAgo(0);
    };

    return (
        <div className="space-y-3">
            {/* Toolbar */}
            <div className="flex items-center justify-between px-1">
                <div className="flex items-center gap-2">
                    {/* Pulsing live dot */}
                    <span className="relative flex h-2.5 w-2.5">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-60" />
                        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-400" />
                    </span>
                    <span className="text-xs font-semibold text-green-400 uppercase tracking-wider">Live</span>
                    <span className="text-xs text-slate-600">
                        {isPending ? 'Refreshing…' : `refreshed ${secondsAgo}s ago`}
                    </span>
                </div>
                <button
                    onClick={handleManualRefresh}
                    disabled={isPending}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors disabled:opacity-40"
                >
                    <RefreshCw size={12} className={isPending ? 'animate-spin' : ''} />
                    Refresh
                </button>
            </div>

            {/* Event rows */}
            <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                <div className="divide-y divide-slate-800/60">
                    {initialEvents.map((event, i) => {
                        const badge = getVerdictBadge(event.security_verdict ?? '', event.processing_status);
                        return (
                            <div
                                key={event.message_id}
                                className="flex items-start gap-4 px-5 py-3.5 hover:bg-slate-900/60 transition-colors group"
                            >
                                {/* Index + colour dot */}
                                <div className="flex flex-col items-center gap-1.5 pt-0.5 shrink-0 w-6">
                                    <span className={`w-2 h-2 rounded-full ${badge.dot} mt-1 shrink-0`} />
                                </div>

                                {/* Main content */}
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2 flex-wrap mb-0.5">
                                        <span className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full border ${badge.className}`}>
                                            {badge.icon}
                                            {badge.label}
                                        </span>
                                        {event.ai_category && (
                                            <span className="text-[10px] text-slate-500 bg-slate-800 px-2 py-0.5 rounded-full font-mono">
                                                {event.ai_category}
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-sm font-medium text-slate-200 truncate group-hover:text-white transition-colors" title={event.subject ?? undefined}>
                                        {event.subject ?? <span className="italic text-slate-500">(no subject)</span>}
                                    </p>
                                    <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
                                        <span className="flex items-center gap-1">
                                            <Mail size={11} />
                                            <span className="truncate max-w-[220px]" title={event.sender}>{event.sender}</span>
                                        </span>
                                        <span>→</span>
                                        <span className="font-mono text-slate-600">{extractDomain(event.sender)}</span>
                                    </div>
                                </div>

                                {/* Time */}
                                <div className="shrink-0 text-right">
                                    <p className="text-xs text-slate-500 font-mono tabular-nums">{timeAgo(event.ingest_time)}</p>
                                    <p className="text-[10px] text-slate-700 mt-0.5 font-mono">
                                        {event.ingest_time
                                            ? new Date(event.ingest_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
                                            : '—'}
                                    </p>
                                </div>
                            </div>
                        );
                    })}

                    {initialEvents.length === 0 && (
                        <div className="px-6 py-16 text-center text-slate-500 italic text-sm">
                            No events received yet. Waiting for ingestion…
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
