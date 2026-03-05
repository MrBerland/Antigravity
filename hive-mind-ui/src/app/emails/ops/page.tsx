import { getBottlenecks } from '@/actions/ops';
import { Clock, ShieldAlert, MessageSquare, Zap } from 'lucide-react';
import Link from 'next/link';

export default async function OpsPage() {
    const bottlenecks = await getBottlenecks();

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'ESCALATION': return 'text-red-400 bg-red-500/10 border-red-500/20';
            case 'STALLED': return 'text-orange-400 bg-orange-500/10 border-orange-500/20';
            case 'HIGH_VOLUME': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
            default: return 'text-slate-400 bg-slate-800 border-slate-700';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <ShieldAlert className="text-orange-500" />
                        Ops War Room
                    </h1>
                    <p className="text-slate-500 mt-1">
                        Bottleneck Detector: Identifying stalled workflows and high-friction threads.
                    </p>
                </div>
                <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-lg text-sm text-slate-400 flex items-center gap-2">
                    <Zap size={14} className="text-yellow-500" />
                    <span>AI Detector Active</span>
                </div>
            </div>

            <div className="grid gap-4">
                {bottlenecks.map((item) => (
                    <div key={item.thread_id} className="bg-slate-950 border border-slate-800 rounded-xl p-5 flex items-center gap-6 hover:border-slate-700 transition-colors">

                        {/* Score Ring */}
                        <div className="flex flex-col items-center justify-center w-16 h-16 rounded-full bg-slate-900 border-2 border-slate-800 relative shrink-0">
                            <span className="text-xl font-bold text-slate-200">{Math.round(item.friction_score)}</span>
                            <span className="text-[10px] text-slate-500 uppercase">Friction</span>
                        </div>

                        {/* Content */}
                        <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getStatusColor(item.status)}`}>
                                    {item.status}
                                </span>
                                <span className="text-xs text-slate-500 uppercase tracking-wide font-semibold">
                                    {item.entity_type} • {item.entity_name}
                                </span>
                            </div>
                            <h3 className="text-lg font-medium text-slate-100 truncate">
                                {item.subject}
                            </h3>
                            <div className="flex items-center gap-4 mt-2 text-sm text-slate-500">
                                <div className="flex items-center gap-1">
                                    <MessageSquare size={14} />
                                    <span>{item.message_count} msgs</span>
                                </div>
                                <div className="flex items-center gap-1">
                                    <Clock size={14} />
                                    <span>Last active: {item.last_active_ts ? new Date(item.last_active_ts).toLocaleDateString() : 'Unknown'}</span>
                                </div>
                            </div>
                        </div>

                        {/* Action */}
                        <Link
                            href={`/emails/thread/${item.thread_id}`}
                            className="px-4 py-2 bg-purple-500/10 hover:bg-purple-500/20 text-purple-400 rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
                        >
                            View Thread
                        </Link>
                    </div>
                ))}

                {bottlenecks.length === 0 && (
                    <div className="p-12 text-center text-slate-500 border border-dashed border-slate-800 rounded-xl">
                        No bottlenecks detected. Operations are smooth.
                    </div>
                )}
            </div>
        </div>
    );
}
