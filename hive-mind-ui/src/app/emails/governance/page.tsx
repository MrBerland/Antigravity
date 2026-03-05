import { getGovernanceRules } from '@/actions/governance';
import { Shield, Plus, Trash2 } from 'lucide-react';

export default async function GovernancePage() {
    const rules = await getGovernanceRules();

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <Shield className="text-purple-400" />
                        Governance Rules
                    </h1>
                    <p className="text-slate-500 mt-1">Manage global Allow/Block lists for the Hive Mind.</p>
                </div>
                <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-medium transition-colors">
                    <Plus size={18} />
                    Add Rule
                </button>
            </div>

            {/* Filters (Placeholder) */}
            <div className="flex gap-4 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-400 flex items-center gap-2">
                    <span>All Rules</span>
                </div>
            </div>

            {/* Rules Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm text-slate-400">
                    <thead className="bg-slate-950 text-slate-200 uppercase text-xs font-semibold">
                        <tr>
                            <th className="px-6 py-4">Pattern</th>
                            <th className="px-6 py-4">Type</th>
                            <th className="px-6 py-4">Match Logic</th>
                            <th className="px-6 py-4">Notes</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {rules.map((rule) => (
                            <tr key={rule.rule_id} className="hover:bg-slate-800/50 transition-colors">
                                <td className="px-6 py-4 font-medium text-slate-200">{rule.pattern}</td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${rule.rule_type === 'BLOCK'
                                        ? 'bg-red-500/10 text-red-400'
                                        : 'bg-green-500/10 text-green-400'
                                        }`}>
                                        {rule.rule_type}
                                    </span>
                                </td>
                                <td className="px-6 py-4 text-slate-500">{rule.match_type}</td>
                                <td className="px-6 py-4">{rule.notes}</td>
                                <td className="px-6 py-4 text-right">
                                    <button className="text-slate-500 hover:text-red-400 transition-colors">
                                        <Trash2 size={18} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                        {rules.length === 0 && (
                            <tr>
                                <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                                    No governance rules defined.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
