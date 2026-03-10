'use client';

import { unsubscribeSender } from '@/actions/unsubscribe';
import { Ban, Loader2, CheckCircle, AlertTriangle, ChevronDown } from 'lucide-react';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

type State = 'idle' | 'loading' | 'success' | 'error' | 'manual_required';

export function SubscriptionActions({ sender }: { sender: string }) {
    const [state, setState] = useState<State>('idle');
    const [message, setMessage] = useState('');
    const [expanded, setExpanded] = useState(false);
    const router = useRouter();

    const handleUnsubscribe = async () => {
        setState('loading');
        try {
            const result = await unsubscribeSender(sender);
            if (result.success) {
                setState('success');
                setMessage(result.message || 'Unsubscribed!');
                router.refresh();
            } else if (result.message?.includes('Manual click required')) {
                setState('manual_required');
                setMessage(result.message);
            } else {
                setState('error');
                setMessage(result.message || 'Failed.');
            }
        } catch (err: any) {
            setState('error');
            setMessage(err.message ?? 'Agent error');
        }
    };

    // ── Outcomes ──────────────────────────────────────────────────────────────

    if (state === 'success') {
        return (
            <div className="flex items-center gap-2 text-green-400 text-sm font-medium whitespace-nowrap">
                <CheckCircle size={14} />
                <span>Unsubscribed</span>
            </div>
        );
    }

    if (state === 'manual_required') {
        return (
            <div className="flex flex-col items-end gap-1">
                <div className="flex items-center gap-1.5 text-yellow-400 text-xs font-medium">
                    <AlertTriangle size={13} />
                    <span>Manual click required</span>
                </div>
                <button
                    onClick={() => setState('idle')}
                    className="text-[10px] text-slate-500 hover:text-slate-300 underline"
                >
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div className="flex flex-col items-end gap-1">
            <div className="flex items-center gap-2">
                {state === 'error' && (
                    <span
                        className="text-xs text-red-400 font-medium flex items-center gap-1 cursor-help"
                        title={message}
                    >
                        <AlertTriangle size={11} />
                        Failed
                    </span>
                )}
                <button
                    id={`unsub-${sender.replace(/[^a-z0-9]/gi, '-')}`}
                    onClick={handleUnsubscribe}
                    disabled={state === 'loading'}
                    className="flex items-center gap-2 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors disabled:opacity-50 whitespace-nowrap"
                >
                    {state === 'loading'
                        ? <Loader2 size={13} className="animate-spin" />
                        : <Ban size={13} />
                    }
                    {state === 'loading' ? 'Working…' : 'Unsubscribe'}
                </button>
            </div>
            {state === 'error' && message && (
                <p className="text-[10px] text-slate-500 max-w-[180px] text-right leading-tight">{message}</p>
            )}
        </div>
    );
}
