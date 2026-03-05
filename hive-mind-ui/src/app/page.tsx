import { getDashboardStats, getVelocityData } from '@/actions/dashboard';
import { ArrowUpRight, Activity, Users, Mail, ShieldAlert } from 'lucide-react';
import IngestionVelocityChart from '@/components/IngestionVelocityChart';

const StatCard = ({ title, value, change, icon: Icon, trend }: any) => (
  <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
    <div className="flex justify-between items-start mb-4">
      <div className="p-2 bg-slate-800 rounded-lg text-slate-400">
        <Icon size={20} />
      </div>
      <div className={`flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-full ${trend === 'up' ? 'text-green-400 bg-green-500/10' : 'text-slate-400 bg-slate-800'
        }`}>
        {trend === 'up' ? <ArrowUpRight size={14} /> : null}
        {change}
      </div>
    </div>
    <h3 className="text-slate-500 text-sm font-medium mb-1">{title}</h3>
    <p className="text-2xl font-bold text-slate-100">{value}</p>
  </div>
);

export default async function Dashboard() {
  const stats = await getDashboardStats();
  const velocityData = await getVelocityData();

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-100 mb-2">Hive Mind Overview</h1>
        <p className="text-slate-500">Real-time ingestion and intelligence metrics.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Ingested"
          value={stats.totalIngested.toLocaleString()}
          change="Live"
          icon={Mail}
          trend="up"
        />
        <StatCard
          title="AI Processed"
          value={stats.processed.toLocaleString()}
          change="Pending AI"
          icon={Activity}
          trend="neutral"
        />
        <StatCard
          title="Governance Blocks"
          value={stats.blocked.toLocaleString()}
          change="Active"
          icon={ShieldAlert}
          trend="up"
        />
        <StatCard
          title="Active Users"
          value={stats.activeUsers}
          change="Stable"
          icon={Users}
          trend="neutral"
        />
      </div>

      {/* Main Chart */}
      <IngestionVelocityChart initialData={velocityData} />
    </div>
  );
}
