import { getDashboardStats, getVelocityData } from '@/actions/dashboard';
import {
  ArrowUpRight, Activity, Users, Mail, ShieldAlert,
  Clock, AlertTriangle, CheckCircle, Briefcase, TrendingUp
} from 'lucide-react';
import IngestionVelocityChart from '@/components/IngestionVelocityChart';
import Link from 'next/link';

export const dynamic = 'force-dynamic';

const StatCard = ({ title, value, sub, icon: Icon, accent }: {
  title: string;
  value: string | number;
  sub?: string;
  icon: any;
  accent: string;
}) => (
  <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl hover:border-slate-700 transition-colors">
    <div className="flex justify-between items-start mb-4">
      <div className={`p-2.5 rounded-xl ${accent}`}>
        <Icon size={18} />
      </div>
    </div>
    <p className="text-3xl font-bold text-slate-100 tabular-nums leading-none">{value}</p>
    <p className="text-sm font-medium text-slate-500 mt-1">{title}</p>
    {sub && <p className="text-xs text-slate-600 mt-0.5">{sub}</p>}
  </div>
);

export default async function Dashboard() {
  const stats = await getDashboardStats();
  const velocityData = await getVelocityData();

  const hasPendingWork = stats.pending > 0;
  const pipelineHealthy = stats.pctClassified >= 90;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-slate-100">Hive Mind</h1>
          <p className="text-slate-500 mt-1">Real-time ingestion and intelligence metrics.</p>
        </div>
        {/* Pipeline Status */}
        <div className={`flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-medium ${hasPendingWork
          ? 'bg-yellow-500/5 border-yellow-500/20 text-yellow-400'
          : 'bg-green-500/5 border-green-500/20 text-green-400'
          }`}>
          {hasPendingWork
            ? <><AlertTriangle size={14} /> {stats.pending.toLocaleString()} pending</>
            : <><CheckCircle size={14} /> Pipeline clear</>
          }
        </div>
      </div>

      {/* Pipeline warning banner */}
      {hasPendingWork && (
        <div className="flex items-start gap-3 bg-yellow-500/5 border border-yellow-500/15 rounded-xl px-5 py-4">
          <AlertTriangle size={16} className="text-yellow-400 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-semibold text-yellow-400">
              {stats.pending.toLocaleString()} emails pending classification
              {' '}({stats.pctClassified}% classified so far)
            </p>
            <p className="text-xs text-slate-500 mt-0.5">
              Run the pipeline to classify them and power the intelligence agents.
            </p>
          </div>
          <code className="text-xs text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-lg whitespace-nowrap self-center">
            python3 HiveMind/hivemind_pipeline.py
          </code>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Total Ingested"
          value={stats.totalIngested.toLocaleString()}
          sub="All time"
          icon={Mail}
          accent="bg-blue-500/10 text-blue-400"
        />
        <StatCard
          title="Business Signal"
          value={stats.business.toLocaleString()}
          sub={`${stats.totalIngested > 0 ? Math.round((stats.business / stats.totalIngested) * 100) : 0}% of corpus`}
          icon={TrendingUp}
          accent="bg-green-500/10 text-green-400"
        />
        <StatCard
          title="Governance Blocks"
          value={stats.blocked.toLocaleString()}
          sub="Noise suppressed"
          icon={ShieldAlert}
          accent="bg-red-500/10 text-red-400"
        />
        <StatCard
          title="Active Mailboxes"
          value={stats.activeUsers}
          sub="Watched (last 7d)"
          icon={Users}
          accent="bg-purple-500/10 text-purple-400"
        />
      </div>

      {/* Classification progress bar */}
      {stats.totalIngested > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl px-6 py-4 space-y-3">
          <div className="flex justify-between items-center text-sm">
            <span className="text-slate-400 font-medium">Classification Progress</span>
            <div className="flex items-center gap-4 text-xs text-slate-500">
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-green-500" />
                {stats.classified.toLocaleString()} classified
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-yellow-500" />
                {stats.pending.toLocaleString()} pending
              </span>
            </div>
          </div>
          <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-green-500 to-blue-500 rounded-full transition-all duration-700"
              style={{ width: `${stats.pctClassified}%` }}
            />
          </div>
          <p className="text-xs text-slate-600">{stats.pctClassified}% of corpus classified</p>
        </div>
      )}

      {/* Chart + Quick Links row */}
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
        <div className="xl:col-span-3">
          <IngestionVelocityChart initialData={velocityData} />
        </div>

        {/* Quick links panel */}
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Quick Actions</h3>
          {[
            { href: '/activity', label: 'Live Feed', sub: 'Watch events in real-time', icon: Activity, color: 'text-green-400' },
            { href: '/emails/reports', label: 'Reports', sub: 'Agent outputs & classification', icon: TrendingUp, color: 'text-blue-400' },
            { href: '/emails/knowledge', label: 'Knowledge Base', sub: 'Most asked questions & best answers', icon: Briefcase, color: 'text-yellow-400' },
            { href: '/emails/intelligence', label: 'Knowledge Graph', sub: 'Entity links & semantic search', icon: Briefcase, color: 'text-purple-400' },
            { href: '/emails/governance', label: 'Governance Rules', sub: 'Add allow/block patterns', icon: ShieldAlert, color: 'text-red-400' },
            { href: '/emails/ops', label: 'Ops War Room', sub: 'Stalled threads & bottlenecks', icon: AlertTriangle, color: 'text-orange-400' },
          ].map(({ href, label, sub, icon: Icon, color }) => (

            <Link
              key={href}
              href={href}
              className="flex items-center gap-3 bg-slate-900 border border-slate-800 rounded-xl px-4 py-3 hover:border-slate-700 hover:bg-slate-800/50 transition-colors group"
            >
              <Icon size={16} className={color} />
              <div className="min-w-0">
                <p className="text-sm font-medium text-slate-200 group-hover:text-white transition-colors">{label}</p>
                <p className="text-xs text-slate-500 truncate">{sub}</p>
              </div>
              <ArrowUpRight size={14} className="text-slate-600 group-hover:text-slate-400 ml-auto shrink-0 transition-colors" />
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
