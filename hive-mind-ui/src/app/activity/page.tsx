import { getLiveFeed, getFeedStats } from '@/actions/activity';
import { Activity, ShieldAlert, Clock, CheckCircle, Inbox } from 'lucide-react';
import LiveFeedStream from '@/components/LiveFeedStream';

export const dynamic = 'force-dynamic';

const StatPill = ({
    label,
    value,
    icon: Icon,
    color,
}: {
    label: string;
    value: number | string;
    icon: any;
    color: string;
}) => (
    <div className={`flex items-center gap-3 bg-slate-900 border border-slate-800 rounded-xl px-5 py-4 hover:border-slate-700 transition-colors`}>
        <div className={`p-2 rounded-lg ${color}`}>
            <Icon size={18} />
        </div>
        <div>
            <p className="text-2xl font-bold text-slate-100 leading-none">{value}</p>
            <p className="text-xs text-slate-500 mt-1 font-medium uppercase tracking-wide">{label}</p>
        </div>
    </div>
);

export default async function ActivityPage() {
    const [events, stats] = await Promise.all([
        getLiveFeed(100),
        getFeedStats(),
    ]);

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <Activity className="text-green-400" />
                        Live Feed
                    </h1>
                    <p className="text-slate-500 mt-1">
                        Real-time ingestion stream — every email as it enters the system.
                    </p>
                </div>

                {/* Pulse badge */}
                <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-lg px-4 py-2">
                    <span className="relative flex h-2.5 w-2.5">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-60" />
                        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-400" />
                    </span>
                    <span className="text-sm font-medium text-green-400">Ingestion Active</span>
                </div>
            </div>

            {/* Stats row */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <StatPill
                    label="Last Hour"
                    value={stats.total_last_hour}
                    icon={Inbox}
                    color="bg-blue-500/10 text-blue-400"
                />
                <StatPill
                    label="Blocked (1h)"
                    value={stats.blocked_last_hour}
                    icon={ShieldAlert}
                    color="bg-red-500/10 text-red-400"
                />
                <StatPill
                    label="Pending AI"
                    value={stats.pending_count}
                    icon={Clock}
                    color="bg-yellow-500/10 text-yellow-400"
                />
                <StatPill
                    label="Processed"
                    value={stats.processed_count}
                    icon={CheckCircle}
                    color="bg-green-500/10 text-green-400"
                />
            </div>

            {/* Live stream */}
            <LiveFeedStream initialEvents={events} />
        </div>
    );
}
