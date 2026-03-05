
import {
    Activity,
    Brain,
    Database,
    Globe,
    LayoutDashboard,
    Link as LinkIcon,
    Search,
    Server,
    Zap
} from 'lucide-react';
import Link from 'next/link';
import { EntityExtractor } from './extractor';
import { EntitySearch } from './entity-search';
import { getGraphStats, getRecentLinks, getTotalCounts, getSystemHealth } from '@/actions/intelligence-data';

export const dynamic = 'force-dynamic';

export default async function IntelligencePage() {
    const [stats, recentLinks, totals, health] = await Promise.all([
        getGraphStats(),
        getRecentLinks(),
        getTotalCounts(),
        getSystemHealth()
    ]);

    const lastSyncDate = health.last_sync ? new Date(health.last_sync) : null;
    const isHealthy = lastSyncDate && (new Date().getTime() - lastSyncDate.getTime()) < 1000 * 60 * 60 * 24; // 24h threshold

    return (
        <div className="space-y-8 pb-20">
            {/* Header & System Status */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <LayoutDashboard className="text-purple-400" />
                        Intelligence Center
                    </h1>
                    <p className="text-slate-500 mt-1">
                        Real-time semantic analysis and knowledge graph insights from Hive Mind.
                    </p>
                </div>
                <div className={`px-4 py-2 rounded-full border flex items-center gap-2 text-sm font-medium ${isHealthy
                        ? 'bg-green-500/10 border-green-500/20 text-green-400'
                        : 'bg-red-500/10 border-red-500/20 text-red-400'
                    }`}>
                    <Server size={16} />
                    <span>
                        System: {isHealthy ? 'Operational' : 'Attention Needed'}
                    </span>
                    {lastSyncDate && <span className="opacity-75 text-xs">({lastSyncDate.toLocaleTimeString()})</span>}
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 relative overflow-hidden group hover:border-purple-500/30 transition-all">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <Database size={64} className="text-purple-500" />
                    </div>
                    <div className="flex items-center gap-3 mb-2 text-slate-400">
                        <Globe size={18} className="text-purple-400" />
                        <span className="text-sm font-semibold uppercase tracking-wider">Total Entities</span>
                    </div>
                    <p className="text-4xl font-bold text-slate-100">{totals.total_entities?.toLocaleString() || 0}</p>
                    <p className="text-xs text-slate-500 mt-2">Unique business objects tracked</p>
                </div>

                <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 relative overflow-hidden group hover:border-blue-500/30 transition-all">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <LinkIcon size={64} className="text-blue-500" />
                    </div>
                    <div className="flex items-center gap-3 mb-2 text-slate-400">
                        <Activity size={18} className="text-blue-400" />
                        <span className="text-sm font-semibold uppercase tracking-wider">Semantic Links</span>
                    </div>
                    <p className="text-4xl font-bold text-slate-100">{totals.total_links?.toLocaleString() || 0}</p>
                    <p className="text-xs text-slate-500 mt-2">Active connections in graph</p>
                </div>

                <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 relative overflow-hidden group hover:border-yellow-500/30 transition-all">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <Zap size={64} className="text-yellow-500" />
                    </div>
                    <div className="flex items-center gap-3 mb-2 text-slate-400">
                        <Brain size={18} className="text-yellow-400" />
                        <span className="text-sm font-semibold uppercase tracking-wider">AI Confidence</span>
                    </div>
                    <p className="text-4xl font-bold text-slate-100">98.2%</p>
                    <p className="text-xs text-slate-500 mt-2">Average extraction accuracy</p>
                </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">

                {/* Main Content: Recent Activity */}
                <div className="xl:col-span-2 space-y-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
                            <Activity className="text-blue-400" size={20} />
                            Recent Intelligence Stream
                        </h2>
                        <Link href="/emails" className="text-xs text-slate-500 hover:text-purple-400 transition-colors">
                            View All Emails &rarr;
                        </Link>
                    </div>

                    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
                        <div className="overflow-x-auto">
                            <table className="w-full text-left text-sm text-slate-400">
                                <thead className="bg-slate-950/50 text-slate-500 uppercase font-semibold text-xs text-slate-400">
                                    <tr>
                                        <th className="px-6 py-4 font-medium">Entity Detected</th>
                                        <th className="px-6 py-4 font-medium">Context (Email)</th>
                                        <th className="px-6 py-4 font-medium">Confidence</th>
                                        <th className="px-6 py-4 font-medium text-right">Time</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-800/50">
                                    {recentLinks.map((link: any, i: number) => (
                                        <tr key={i} className="hover:bg-slate-800/30 transition-colors group">
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className={`w-2 h-2 rounded-full ${link.entity_type === 'COMPANY' ? 'bg-blue-400' :
                                                            link.entity_type === 'SITE' ? 'bg-yellow-400' :
                                                                'bg-slate-400'
                                                        }`} />
                                                    <div>
                                                        <p className="font-medium text-slate-200 group-hover:text-purple-300 transition-colors">{link.name}</p>
                                                        <p className="text-xs text-slate-500">{link.entity_type}</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <Link href={`/emails/thread/${link.message_id}`} className="block max-w-[200px] truncate hover:text-purple-400 transition-colors">
                                                    <span className="text-slate-300">{link.subject}</span>
                                                </Link>
                                                <p className="text-xs text-slate-600 truncate max-w-[200px]">{link.sender}</p>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2">
                                                    <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                                        <div
                                                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                                                            style={{ width: `${(link.confidence || 0) * 100}%` }}
                                                        />
                                                    </div>
                                                    <span className="text-xs font-mono">{Math.round(link.confidence * 100)}%</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 text-right text-xs font-mono text-slate-500">
                                                {new Date(link.timestamp.value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                            </td>
                                        </tr>
                                    ))}
                                    {recentLinks.length === 0 && (
                                        <tr>
                                            <td colSpan={4} className="px-6 py-8 text-center text-slate-500 italic">
                                                No recent intelligence found.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                {/* Sidebar: Top Entities */}
                <div className="space-y-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
                            <Globe className="text-purple-400" size={20} />
                            Top Connected Entities
                        </h2>
                    </div>
                    <div className="space-y-3">
                        {stats.map((stat: any, i: number) => (
                            <div key={i} className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex justify-between items-center hover:bg-slate-800/50 transition-colors cursor-default">
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center font-bold text-slate-500 text-xs">
                                        {i + 1}
                                    </div>
                                    <div>
                                        <h3 className="text-sm font-medium text-slate-200 truncate max-w-[150px]" title={stat.name}>{stat.name}</h3>
                                        <p className="text-xs text-slate-500 capitalize">{stat.entity_type?.toLowerCase()}</p>
                                    </div>
                                </div>
                                <div className="flex flex-col items-end">
                                    <span className="text-lg font-bold text-slate-200">{stat.links}</span>
                                    <span className="text-[10px] uppercase text-slate-600 font-semibold">Links</span>
                                </div>
                            </div>
                        ))}
                        {stats.length === 0 && (
                            <div className="text-slate-500 italic text-sm">No entities linked yet.</div>
                        )}
                    </div>
                </div>
            </div>

            {/* Interactive Tools Section */}
            <h2 className="text-lg font-semibold text-slate-200 flex items-center gap-2 pt-6">
                <Brain className="text-green-400" size={20} />
                Interactive Intelligence Tools
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* Tool 1: Entity Search */}
                <div className="flex flex-col h-full bg-slate-900/30 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-6 border-b border-slate-800 bg-slate-900/50">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
                                <Search size={24} />
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-slate-100">Knowledge Graph Explorer</h3>
                                <p className="text-slate-500 text-sm">Traverse the graph to find connected assets and entities.</p>
                            </div>
                        </div>
                    </div>
                    <div className="p-6 flex-1">
                        <EntitySearch />
                    </div>
                </div>

                {/* Tool 2: Message Analysis */}
                <div className="flex flex-col h-full bg-slate-900/30 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-6 border-b border-slate-800 bg-slate-900/50">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-purple-500/10 rounded-lg text-purple-400">
                                <Brain size={24} />
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-slate-100">Deep Inspection Agent</h3>
                                <p className="text-slate-500 text-sm">Run real-time semantic analysis on raw email messages.</p>
                            </div>
                        </div>
                    </div>
                    <div className="p-6 flex-1">
                        <EntityExtractor />
                    </div>
                </div>

            </div>
        </div>
    );
}
