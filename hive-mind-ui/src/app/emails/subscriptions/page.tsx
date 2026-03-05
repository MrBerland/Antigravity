import { getPotentialSubscriptions } from '@/actions/subscriptions';
// We need a client component for the "Unsubscribe" button to handle interactivity
import { SubscriptionActions } from './actions';
import { Mail, Zap } from 'lucide-react';
import Link from 'next/link';

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
                        Identify and manage high-volume senders and newsletters.
                    </p>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-400 flex items-center gap-2">
                    <Zap size={16} className="text-yellow-400" />
                    <span>Auto-Agent: Active</span>
                </div>
            </div>

            {/* Main Grid */}
            <div className="grid grid-cols-1 gap-4">
                {subscriptions.map((sub: any) => (
                    <div key={sub.sender} className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center justify-between hover:border-slate-700 transition-colors">
                        <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 font-bold">
                                {sub.sender.charAt(0).toUpperCase()}
                            </div>
                            <div>
                                <h3 className="font-semibold text-slate-200">{sub.sender}</h3>
                                <p className="text-sm text-slate-500 max-w-md truncate" title={sub.sample_subject}>
                                    Latest: <Link href={`/emails/thread/${sub.latest_message_id}`} className="hover:text-purple-400 transition-colors">{sub.sample_subject}</Link>
                                </p>
                            </div>
                        </div>

                        <div className="flex items-center gap-6">
                            <div className="text-right">
                                <div className="text-xl font-bold text-slate-200">{sub.count}</div>
                                <div className="text-xs text-slate-500 uppercase">Emails</div>
                            </div>
                            <div className="h-8 w-px bg-slate-800"></div>
                            <SubscriptionActions sender={sub.sender} />
                        </div>
                    </div>
                ))}

                {subscriptions.length === 0 && (
                    <div className="text-center py-12 text-slate-500 bg-slate-900 border border-slate-800 rounded-xl">
                        No active high-volume senders found.
                    </div>
                )}
            </div>
        </div>
    );
}
