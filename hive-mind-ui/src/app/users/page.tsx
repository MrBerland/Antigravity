import { getUserStats } from '@/actions/users';
import { Users, Mail, Clock, Activity } from 'lucide-react';

export default async function UsersPage() {
    const users = await getUserStats();

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                    <Users className="text-blue-400" />
                    Domain User Status
                </h1>
                <p className="text-slate-500 mt-1">Real-time ingestion metrics per mailbox.</p>
            </div>

            {/* Users Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm text-slate-400">
                    <thead className="bg-slate-950 text-slate-200 uppercase text-xs font-semibold">
                        <tr>
                            <th className="px-6 py-4">User / Mailbox</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Total Ingested</th>
                            <th className="px-6 py-4">Last Sync</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {users.map((user) => (
                            <tr key={user.email} className="hover:bg-slate-800/50 transition-colors">
                                <td className="px-6 py-4 font-medium text-slate-200 flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500/20 to-purple-500/20 flex items-center justify-center text-blue-400">
                                        <Mail size={14} />
                                    </div>
                                    {user.email}
                                </td>
                                <td className="px-6 py-4">
                                    <span className="px-2 py-1 rounded-full text-xs font-semibold bg-green-500/10 text-green-400 flex items-center gap-1 w-fit">
                                        <Activity size={12} />
                                        {user.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-slate-200 font-mono">
                                    {user.totalIngested.toLocaleString()}
                                </td>
                                <td className="px-6 py-4 flex items-center gap-2">
                                    <Clock size={14} />
                                    {user.lastSync}
                                </td>
                            </tr>
                        ))}

                        {users.length === 0 && (
                            <tr>
                                <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                                    No active users found in the ingestion stream.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
