import { getPotentialSubscriptions } from '@/actions/subscriptions';
import { SubscriptionActions } from './actions';
import { Mail, Zap } from 'lucide-react';
import Link from 'next/link';

export const dynamic = 'force-dynamic';

const CATEGORY_STYLES: Record<string, string> = {
    MARKETING: 'bg-pink-500/10 text-pink-400 border-pink-500/20',
    PERSONAL: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    SYSTEM: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    UNKNOWN: 'bg-slate-700 text-slate-400 border-slate-600',
};

export default async function SubscriptionsPage() {
    const subscriptions = await getPotentialSubscriptions();

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <Mail className="text-pink-400" />
                        Subscription Manager
                    </h1>
                    <p className="text-slate-500 mt-1">
                        AI-classified noise senders — unsubscribe or block them in one click.
                    </p>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-400 flex items-center gap-2">
                    <Zap size={16} className="text-yellow-400" />
                    <span>Unsubscribe Agent: Active</span>
                </div>
            </div>

            {/* Stats bar */}
            <div className="flex gap-4 text-xs text-slate-500">
                <span><strong className="text-slate-300">{subscriptions.length}</strong> senders detected</span>
                <span>·</span>
                <span><strong className="text-slate-300">{subscriptions.reduce((a, s) => a + s.count, 0).toLocaleString()}</strong> total emails</span>
            </div>

            {/* Main Grid */}
            <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden divide-y divide-slate-800/60">
                {subscriptions.map((sub) => {
                    const categoryStyle = CATEGORY_STYLES[sub.category] ?? CATEGORY_STYLES.UNKNOWN;
                    return (
                        <div
                            key={sub.sender}
                            className="flex items-center gap-4 px-5 py-3.5 hover:bg-slate-900/60 transition-colors"
                        >
                            {/* Avatar */}
                            <div className="w-9 h-9 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 font-bold text-sm shrink-0">
                                {sub.sender.charAt(0).toUpperCase()}
                            </div>

                            {/* Sender info */}
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 mb-0.5">
                                    <h3 className="font-semibold text-slate-200 text-sm truncate">{sub.sender}</h3>
                                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border shrink-0 ${categoryStyle}`}>
                                        {sub.category}
                                    </span>
                                </div>
                                <p className="text-xs text-slate-500 truncate max-w-md" title={sub.sample_subject}>
                                    {sub.sample_subject
                                        ? <Link href={`/emails/thread/${sub.latest_message_id}`} className="hover:text-purple-400 transition-colors">{sub.sample_subject}</Link>
                                        : <span className="italic">No subject</span>
                                    }
                                </p>
                            </div>

                            {/* Count */}
                            <div className="text-right shrink-0">
                                <div className="text-lg font-bold text-slate-200">{sub.count}</div>
                                <div className="text-[10px] text-slate-500 uppercase font-semibold">emails</div>
                            </div>

                            <div className="h-8 w-px bg-slate-800 shrink-0" />

                            <SubscriptionActions sender={sub.sender} />
                        </div>
                    );
                })}

                {subscriptions.length === 0 && (
                    <div className="px-6 py-16 text-center text-slate-500 italic text-sm">
                        No unsubscribe candidates found. Run the classifier first.
                    </div>
                )}
            </div>
        </div>
    );
}
