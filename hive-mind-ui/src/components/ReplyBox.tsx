'use client';

import { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { sendReply } from '@/actions/gmail';

export default function ReplyBox({ threadId, lastMessageId, subject, recipient }: { threadId: string, lastMessageId: string, subject: string, recipient: string }) {
    const [body, setBody] = useState('');
    const [sending, setSending] = useState(false);
    const [sent, setSent] = useState(false);

    const handleSend = async () => {
        if (!body.trim()) return;
        setSending(true);
        try {
            await sendReply(threadId, lastMessageId, subject, recipient, body);
            setSent(true);
            setBody('');
        } catch (e) {
            console.error(e);
            alert('Failed to send reply');
        } finally {
            setSending(false);
        }
    };

    if (sent) {
        return (
            <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 text-green-400 text-sm font-medium flex items-center gap-2">
                <Send size={16} />
                Reply sent successfully. refreshing...
                {/* In a real app we'd revalidate path here */}
            </div>
        );
    }

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-500 uppercase">
                <Send size={14} />
                <span>Reply to {recipient}</span>
            </div>
            <textarea
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="Write your reply..."
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-purple-500/50 min-h-[100px]"
            />
            <div className="flex justify-end">
                <button
                    onClick={handleSend}
                    disabled={sending || !body.trim()}
                    className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
                >
                    {sending ? <Loader2 className="animate-spin" size={16} /> : <Send size={16} />}
                    {sending ? 'Sending...' : 'Send Reply'}
                </button>
            </div>
        </div>
    );
}
