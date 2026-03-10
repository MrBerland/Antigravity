'use client';

import { useState, useTransition } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { getVelocityData } from '@/actions/dashboard';
import { Loader2 } from 'lucide-react';

const RANGES = ['24h', '7d', '30d'] as const;

export default function IngestionVelocityChart({ initialData }: { initialData: any[] }) {
    const [data, setData] = useState(initialData);
    const [range, setRange] = useState<typeof RANGES[number]>('24h');
    const [isPending, startTransition] = useTransition();

    const handleRangeChange = (newRange: typeof RANGES[number]) => {
        setRange(newRange);
        startTransition(async () => {
            const newData = await getVelocityData(newRange);
            setData(newData);
        });
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-[340px] flex flex-col">
            <div className="flex justify-between items-center mb-5">
                <div>
                    <h3 className="text-base font-semibold text-slate-100">Ingestion Velocity</h3>
                    <p className="text-xs text-slate-500 mt-0.5">All emails vs. clean business signal vs. blocked</p>
                </div>
                <div className="flex bg-slate-950 rounded-lg p-1 border border-slate-800">
                    {RANGES.map((r) => (
                        <button
                            key={r}
                            id={`velocity-range-${r}`}
                            onClick={() => handleRangeChange(r)}
                            disabled={isPending}
                            className={`px-3 py-1 rounded-md text-xs font-semibold transition-colors ${range === r
                                ? 'bg-slate-800 text-purple-400'
                                : 'text-slate-500 hover:text-slate-300 disabled:opacity-40'
                                }`}
                        >
                            {r.toUpperCase()}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex-1 min-h-0 relative">
                {isPending && (
                    <div className="absolute inset-0 z-10 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm rounded-lg">
                        <Loader2 size={20} className="animate-spin text-purple-400" />
                    </div>
                )}
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
                        <defs>
                            <linearGradient id="gradAll" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.25} />
                                <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="gradBusiness" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.25} />
                                <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="gradBlocked" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.2} />
                                <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                        <XAxis dataKey="name" stroke="#475569" tick={{ fontSize: 11 }} minTickGap={30} />
                        <YAxis stroke="#475569" tick={{ fontSize: 11 }} width={32} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9', borderRadius: '8px', fontSize: '12px' }}
                        />
                        <Legend
                            wrapperStyle={{ fontSize: '11px', color: '#94a3b8', paddingTop: '8px' }}
                            iconType="circle"
                            iconSize={8}
                        />
                        <Area type="monotone" dataKey="emails" name="All" stroke="#6366f1" strokeWidth={1.5} fillOpacity={1} fill="url(#gradAll)" />
                        <Area type="monotone" dataKey="business" name="Business" stroke="#22c55e" strokeWidth={1.5} fillOpacity={1} fill="url(#gradBusiness)" />
                        <Area type="monotone" dataKey="blocked" name="Blocked" stroke="#ef4444" strokeWidth={1.5} fillOpacity={1} fill="url(#gradBlocked)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
