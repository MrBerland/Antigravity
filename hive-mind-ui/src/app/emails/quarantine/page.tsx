import { getStagingEmails } from '@/actions/staging';
import { CheckCircle, Clock, ShieldAlert, ChevronLeft, ChevronRight, Search } from 'lucide-react';
import Link from 'next/link';

export default async function QuarantinePage({ searchParams }: { searchParams: Promise<{ page?: string, filter?: string }> }) {
    const params = await searchParams;
    const page = parseInt(params.page || '1');
    const filter = params.filter || 'ALL';
    const limit = 50;

    const { emails, total } = await getStagingEmails(page, limit, filter);
    const totalPages = Math.ceil(total / limit);

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <Search className="text-blue-400" />
                        Quarantine Inspector
                    </h1>
                    <p className="text-slate-500 mt-1">
                        View the raw ingestion stream and security blocks.
                    </p>
                </div>

                {/* Filter Controls */}
                <div className="flex bg-slate-900 rounded-lg p-1 border border-slate-800">
                    <Link
                        href="/emails/quarantine?filter=ALL"
                        className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${filter === 'ALL' ? 'bg-slate-800 text-slate-200' : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        All
                    </Link>
                    <Link
                        href="/emails/quarantine?filter=PENDING"
                        className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${filter === 'PENDING' ? 'bg-yellow-500/10 text-yellow-500' : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        Pending
                    </Link>
                    <Link
                        href="/emails/quarantine?filter=BLOCKED"
                        className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${filter === 'BLOCKED' ? 'bg-red-500/10 text-red-500' : 'text-slate-500 hover:text-slate-300'}`}
                    >
                        Blocked
                    </Link>
                </div>
            </div>

            {/* Data Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm text-slate-400">
                        <thead className="bg-slate-950 text-slate-500 uppercase font-semibold text-xs border-b border-slate-800">
                            <tr>
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Timestamp</th>
                                <th className="px-6 py-4">Sender</th>
                                <th className="px-6 py-4">Recipient</th>
                                <th className="px-6 py-4">Subject</th>
                                <th className="px-6 py-4 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800">
                            {emails.map((email: any) => (
                                <tr key={email.message_id} className="hover:bg-slate-800/50 transition-colors">
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col gap-1">
                                            {email.verdict === 'BLOCK' ? (
                                                <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium bg-red-500/10 text-red-400 w-fit">
                                                    <ShieldAlert size={12} /> Blocked
                                                </span>
                                            ) : email.status === 'PENDING' ? (
                                                <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-500/10 text-yellow-400 w-fit">
                                                    <Clock size={12} /> Pending
                                                </span>
                                            ) : (
                                                <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium bg-green-500/10 text-green-400 w-fit">
                                                    <CheckCircle size={12} /> Processed
                                                </span>
                                            )}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 font-mono text-xs">
                                        {email.timestamp ? new Date(email.timestamp).toLocaleString() : '-'}
                                    </td>
                                    <td className="px-6 py-4 text-slate-300 font-medium">
                                        {email.sender}
                                    </td>
                                    <td className="px-6 py-4 text-slate-500 text-xs">
                                        {email.recipient}
                                    </td>
                                    <td className="px-6 py-4 text-slate-300 max-w-md truncate" title={email.subject}>
                                        {email.subject}
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <Link
                                            href={`/emails/thread/${email.message_id}`}
                                            className="text-purple-400 hover:text-purple-300 text-xs font-medium"
                                        >
                                            View
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                            {emails.length === 0 && (
                                <tr>
                                    <td colSpan={6} className="px-6 py-12 text-center text-slate-500 italic">
                                        No emails found matching this filter.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>

                {/* Pagination Footer */}
                <div className="bg-slate-950 px-6 py-4 border-t border-slate-800 flex items-center justify-between">
                    <div className="text-xs text-slate-500">
                        Showing <span className="text-slate-300 font-medium">{emails.length}</span> of <span className="text-slate-300 font-medium">{total}</span>
                    </div>
                    <div className="flex gap-2">
                        {page > 1 && (
                            <Link href={`?page=${page - 1}&filter=${filter}`} className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 transition-colors">
                                <ChevronLeft size={16} />
                            </Link>
                        )}
                        <span className="px-3 py-1.5 text-xs text-slate-500 font-medium border border-slate-800 rounded-lg">
                            Page {page} of {totalPages}
                        </span>
                        {page < totalPages && (
                            <Link href={`?page=${page + 1}&filter=${filter}`} className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 transition-colors">
                                <ChevronRight size={16} />
                            </Link>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
