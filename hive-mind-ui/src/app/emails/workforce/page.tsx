import { getWorkforcePulse, getUserProfiles } from '@/actions/workforce';
import { Briefcase, Clock, Zap, User } from 'lucide-react';

export default async function WorkforcePage() {
    const pulse = await getWorkforcePulse();
    const profiles = await getUserProfiles();

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <Briefcase className="text-purple-400" />
                        Workforce Intelligence
                    </h1>
                    <p className="text-slate-500 mt-1">
                        AI-driven analysis of team focus, skills, and time allocation.
                    </p>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-400 flex items-center gap-2">
                    <Zap size={16} className="text-yellow-400" />
                    <span>Analysis: Active</span>
                </div>
            </div>

            {/* Pulse Grid */}
            <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-2">Team Pulse (Last 7 Days)</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
                {pulse.map((item: any, i: number) => (
                    <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col gap-2 hover:border-blue-500/30 transition-colors">
                        <div className="flex justify-between items-start">
                            <span className="bg-blue-500/10 text-blue-300 text-xs px-2 py-1 rounded-full font-semibold">
                                {item.category}
                            </span>
                            <div className="flex items-center gap-1 text-slate-400 text-xs">
                                <Clock size={12} />
                                <span>~{Math.round(item.estimated_hours_communication * 10) / 10} hrs</span>
                            </div>
                        </div>
                        <h3 className="text-lg font-medium text-slate-100 truncate" title={item.user_email}>
                            {item.user_email.split('@')[0]}
                        </h3>
                        <p className="text-xs text-slate-500">{item.email_volume} Activities Analyzed</p>
                    </div>
                ))}
                {pulse.length === 0 && (
                    <div className="text-slate-500 italic col-span-3 text-center py-8">
                        No work patterns detected yet. Run the analysis agent.
                    </div>
                )}
            </div>

            {/* Profiles Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden mb-8">
                <div className="p-4 border-b border-slate-800 flex justify-between items-center">
                    <h2 className="text-sm font-semibold text-slate-200">Enriched User Directory</h2>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm text-slate-400">
                        <thead className="bg-slate-950 text-slate-500 uppercase font-semibold text-xs">
                            <tr>
                                <th className="px-4 py-3">User</th>
                                <th className="px-4 py-3">Detected Role</th>
                                <th className="px-4 py-3">Skills Identified</th>
                                <th className="px-4 py-3">Last Updated</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800">
                            {profiles.map((profile: any, i: number) => (
                                <tr key={i} className="hover:bg-slate-800/50">
                                    <td className="px-4 py-3 font-medium text-slate-200 flex items-center gap-2">
                                        <div className="w-6 h-6 rounded-full bg-slate-800 flex items-center justify-center">
                                            <User size={12} />
                                        </div>
                                        {profile.email}
                                    </td>
                                    <td className="px-4 py-3">
                                        {profile.latest_detected_title || <span className="text-slate-600 italic">Unknown</span>}
                                    </td>
                                    <td className="px-4 py-3">
                                        <div className="flex gap-1 flex-wrap">
                                            {(profile.detected_skills || []).map((skill: string, j: number) => (
                                                <span key={j} className="bg-slate-800 text-slate-300 text-xs px-1.5 py-0.5 rounded">
                                                    {skill}
                                                </span>
                                            ))}
                                        </div>
                                    </td>
                                    <td className="px-4 py-3 text-xs">
                                        {new Date(profile.last_updated.value).toLocaleDateString()}
                                    </td>
                                </tr>
                            ))}
                            {profiles.length === 0 && (
                                <tr>
                                    <td colSpan={4} className="px-4 py-8 text-center text-slate-500 italic">
                                        No user profiles enriched yet.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
