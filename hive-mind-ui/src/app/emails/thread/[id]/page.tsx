import { getThread } from '@/actions/gmail';
import ReplyBox from '@/components/ReplyBox';
import { User, Clock } from 'lucide-react';
import BackButton from '@/components/BackButton';

// Helper to decode Base64Url
// Helper to decode Base64Url
function decodeBody(parts: any[]): string {
    if (!parts) return '';
    // Look for text/plain or text/html
    const plain = parts.find((p: any) => p.mimeType === 'text/plain');
    const html = parts.find((p: any) => p.mimeType === 'text/html');

    // Prefer HTML, fallback to plain
    const selected = html || plain;

    if (selected && selected.body && selected.body.data) {
        return Buffer.from(selected.body.data, 'base64').toString('utf-8');
    }

    // Recursive check for multipart
    if (!selected) {
        for (const part of parts) {
            if (part.parts) {
                const nested: string = decodeBody(part.parts);
                if (nested) return nested;
            }
        }
    }

    return '(No readable content)';
}

export default async function ThreadPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    const thread = await getThread(id);

    // Process Messages (Chronological)
    const messages = (thread.messages || []).map((msg: any) => {
        const headers = msg.payload.headers;
        const subject = headers.find((h: any) => h.name === 'Subject')?.value || '(No Subject)';
        const from = headers.find((h: any) => h.name === 'From')?.value || 'Unknown';
        const to = headers.find((h: any) => h.name === 'To')?.value || 'Unknown';
        const date = headers.find((h: any) => h.name === 'Date')?.value;

        let body = '';
        if (msg.payload.body && msg.payload.body.data) {
            body = Buffer.from(msg.payload.body.data, 'base64').toString('utf-8');
        } else if (msg.payload.parts) {
            body = decodeBody(msg.payload.parts);
        }

        return {
            id: msg.id,
            subject,
            from,
            to,
            date,
            body,
            timestamp: parseInt(msg.internalDate)
        };
    });

    const lastMsg = messages[messages.length - 1];
    // Simple logic: If last message FROM me, I reply to TO. Else reply to FROM.
    // NOTE: This is simplistic. Real reply logic parses "Reply-To" etc.
    // MVP: Reply to the 'From' of the last message if I didn't send it.
    // If I sent it, reply to 'To'.
    const myEmail = 'tim@augos.io'; // Hardcoded for MVP context
    const replyTo = lastMsg.from.includes(myEmail) ? lastMsg.to : lastMsg.from;
    // Extract email from "Name <email>" format if needed, but Gmail API handles raw strings often ok.
    // Better to extract clean email for the 'To' header.
    const cleanRecipient = replyTo.replace(/.*<(.+)>.*/, '$1') || replyTo;

    return (
        <div className="max-w-4xl mx-auto space-y-6 pb-20">
            {/* Header */}
            <div className="flex items-center gap-4 mb-6">
                <BackButton />
                <div className="flex-1">
                    <h1 className="text-2xl font-bold text-slate-100">{lastMsg.subject}</h1>
                    <div className="flex items-center gap-2 text-sm text-slate-500 mt-1">
                        <span className="bg-slate-800 px-2 py-0.5 rounded text-xs text-slate-400">{messages.length} Messages</span>
                        <span>•</span>
                        <span>Last activity: {new Date(lastMsg.timestamp).toLocaleString()}</span>
                    </div>
                </div>
            </div>

            {/* Message List */}
            <div className="space-y-6">
                {messages.map((msg: any, i: number) => (
                    <div key={msg.id} className={`flex gap-4 ${i === messages.length - 1 ? 'opacity-100' : 'opacity-80'}`}>
                        <div className="flex flex-col items-center">
                            <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 border border-slate-700">
                                <User size={16} />
                            </div>
                            {i !== messages.length - 1 && <div className="w-px h-full bg-slate-800 my-2" />}
                        </div>

                        <div className="flex-1 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                            {/* Msg Header */}
                            <div className="bg-slate-950/50 p-4 border-b border-slate-800 flex justify-between items-start">
                                <div>
                                    <div className="font-semibold text-slate-200">{msg.from}</div>
                                    <div className="text-xs text-slate-500 mt-0.5">To: {msg.to}</div>
                                </div>
                                <div className="flex items-center gap-1 text-xs text-slate-500">
                                    <Clock size={12} />
                                    {new Date(msg.timestamp).toLocaleString()}
                                </div>
                            </div>

                            {/* Msg Body */}
                            <div className="p-6 text-slate-300 text-sm whitespace-pre-wrap font-sans leading-relaxed overflow-x-auto">
                                <div dangerouslySetInnerHTML={{ __html: msg.body }} className="prose prose-invert max-w-none" />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Reply Area */}
            <div className="ml-14 pt-4">
                <ReplyBox
                    threadId={id}
                    lastMessageId={lastMsg.id}
                    subject={lastMsg.subject}
                    recipient={cleanRecipient}
                />
            </div>

        </div>
    );
}
