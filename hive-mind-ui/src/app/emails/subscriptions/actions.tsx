'use client';

import { unsubscribeSender } from '@/actions/unsubscribe';
import { Ban, Loader2, CheckCircle, AlertTriangle } from 'lucide-react';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export function SubscriptionActions({ sender }: { sender: string }) {
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');
    const router = useRouter();

    const handleUnsubscribe = async () => {
        // if (!confirm(`Are you sure you want to unsubscribe from ${sender}?`)) return;

        setLoading(true);
        setStatus('idle');
        try {
            const result = await unsubscribeSender(sender);

            if (result.success) {
                setStatus('success');
                setMessage(result.message || 'Unsubscribed!');
            } else {
                setStatus('error');
                setMessage(result.message || 'Failed.');
            }

            router.refresh();
        } catch (error) {
            console.error('Failed to unsubscribe:', error);
            setStatus('error');
            setMessage('Agent Failed');
        } finally {
            setLoading(false);
        }
    };

    if (status === 'success') {
        return (
            <div className="flex items-center gap-2 text-green-400 text-sm font-medium">
                <CheckCircle size={16} />
                <span>{message}</span>
            </div>
        )
    }

    return (
        <div className="flex items-center gap-2">
            {status === 'error' && (
                <span className="text-xs text-red-400 font-medium flex items-center gap-1" title={message}>
                    <AlertTriangle size={12} />
                    Failed
                </span>
            )}
            <button
                onClick={handleUnsubscribe}
                disabled={loading}
                className="flex items-center gap-2 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 px-4 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
            >
                {loading ? <Loader2 size={16} className="animate-spin" /> : <Ban size={16} />}
                Unsubscribe Agent
            </button>
        </div>
    );
}
