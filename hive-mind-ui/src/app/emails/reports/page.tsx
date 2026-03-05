import { getStagingEmails } from '@/actions/staging';
import { FileText, RefreshCw, Eye, ShieldAlert, CheckCircle } from 'lucide-react';
import Link from 'next/link';

export default async function ReportsPage() {
    const { emails } = await getStagingEmails(1, 100);

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <FileText className="text-blue-400" />
                        Ingestion Reports
                    </h1>
                    <p className="text-slate-500 mt-1">
                        Raw feed of all emails hitting the Staging Layer (Quarantine).
                    </p>
                </div>
                <button className="flex items-center gap-2 text-slate-400 hover:text-slate-200 transition-colors">
                    <RefreshCw size={18} />
                    <span>Refresh</span>
                </button>
            </div>

            {/* Main Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm text-slate-400">
                    <thead className="bg-slate-950 text-slate-200 uppercase text-xs font-semibold">
                        <tr>
                            <th className="px-6 py-4">Time</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Sender</th>
                            <th className="px-6 py-4">Subject</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {emails.map((email: any, i: number) => (
                            <tr key={`${email.message_id}-${i}`} className="hover:bg-slate-800/50 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    {new Date(email.timestamp).toLocaleString()}
                                </td>
                                <td className="px-6 py-4">
                                    {email.security_verdict === 'BLOCK' ? (
                                        <span className="flex items-center gap-1 text-red-400 bg-red-500/10 px-2 py-1 rounded-full w-fit text-xs font-semibold">
                                            <ShieldAlert size={12} /> BLOCKED
                                        </span>
                                    ) : (
                                        <span className="flex items-center gap-1 text-green-400 bg-green-500/10 px-2 py-1 rounded-full w-fit text-xs font-semibold">
                                            <CheckCircle size={12} /> ALLOW
                                        </span>
                                    )}
                                </td>
                                <td className="px-6 py-4 font-medium text-slate-300 max-w-[200px] truncate" title={email.sender}>
                                    {email.sender}
                                </td>
                                <td className="px-6 py-4 max-w-[300px] truncate" title={email.subject}>
                                    {email.subject}
                                </td>
                                <td className="px-6 py-4 text-right">
                                    <div className="flex justify-end gap-2">
                                        <Link href={`/emails/thread/${email.message_id}`} className="p-1 hover:text-blue-400 transition-colors" title="View Details">
                                            <Eye size={18} />
                                        </Link>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {emails.length === 0 && (
                            <tr>
                                <td colSpan={5} className="text-center py-12 text-slate-500">
                                    No emails found in staging.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
