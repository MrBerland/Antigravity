'use client';

import { useState, useTransition } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getVelocityData } from '@/actions/dashboard';
import { Loader2 } from 'lucide-react';

export default function IngestionVelocityChart({ initialData }: { initialData: any[] }) {
    const [data, setData] = useState(initialData);
    const [range, setRange] = useState('24h');
    const [isPending, startTransition] = useTransition();

    const handleRangeChange = (newRange: string) => {
        setRange(newRange);
        startTransition(async () => {
            const newData = await getVelocityData(newRange);
            setData(newData);
        });
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-[400px] flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-semibold text-slate-100">
                    Ingestion Velocity ({range.toUpperCase()})
                </h3>
                <div className="flex bg-slate-950 rounded-lg p-1 border border-slate-800">
                    {['24h', '7d', '30d'].map((r) => (
                        <button
                            key={r}
                            onClick={() => handleRangeChange(r)}
                            disabled={isPending}
                            className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${range === r
                                ? 'bg-slate-800 text-purple-400'
                                : 'text-slate-500 hover:text-slate-300'
                                }`}
                        >
                            {r.toUpperCase()}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex-1 min-h-0 relative">
                {isPending && (
                    <div className="absolute inset-0 z-10 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm transition-all">
                        <Loader2 className="animate-spin text-purple-500" />
                    </div>
                )}
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorEmails" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                        <XAxis
                            dataKey="name"
                            stroke="#64748b"
                            tick={{ fontSize: 12 }}
                            minTickGap={30}
                        />
                        <YAxis stroke="#64748b" tick={{ fontSize: 12 }} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9' }}
                            itemStyle={{ color: '#a78bfa' }}
                        />
                        <Area
                            type="monotone"
                            dataKey="emails"
                            stroke="#8b5cf6"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorEmails)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
