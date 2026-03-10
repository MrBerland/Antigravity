import { getGovernanceRules } from '@/actions/governance';
import { Shield } from 'lucide-react';
import { AddRuleButton, DeleteRuleButton } from './actions';

export const dynamic = 'force-dynamic';

const TYPE_STYLES: Record<string, string> = {
    BLOCK: 'bg-red-500/10 text-red-400 border-red-500/20',
    ALLOW: 'bg-green-500/10 text-green-400 border-green-500/20',
    MARKETING: 'bg-pink-500/10 text-pink-400 border-pink-500/20',
    PERSONAL: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    SYSTEM: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
};

export default async function GovernancePage() {
    const rules = await getGovernanceRules();

    const grouped = rules.reduce((acc, r) => {
        acc[r.rule_type] = (acc[r.rule_type] ?? 0) + 1;
        return acc;
    }, {} as Record<string, number>);

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                        <Shield className="text-purple-400" />
                        Governance Rules
                    </h1>
                    <p className="text-slate-500 mt-1">
                        Global allow/block/classify patterns applied before AI classification.
                    </p>
                </div>
                <AddRuleButton />
            </div>

            {/* Stats row */}
            <div className="flex flex-wrap gap-3">
                {Object.entries(grouped).map(([type, count]) => {
                    const style = TYPE_STYLES[type] ?? 'bg-slate-700 text-slate-400 border-slate-600';
                    return (
                        <span key={type} className={`inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-full border ${style}`}>
                            {count} {type}
                        </span>
                    );
                })}
                <span className="text-xs text-slate-500 self-center ml-1">{rules.length} rules total</span>
            </div>

            {/* Rules Table */}
            <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm text-slate-400">
                    <thead className="bg-slate-900 text-slate-500 uppercase text-[10px] font-semibold tracking-wider border-b border-slate-800">
                        <tr>
                            <th className="px-5 py-3.5">Pattern</th>
                            <th className="px-5 py-3.5">Type</th>
                            <th className="px-5 py-3.5">Match Logic</th>
                            <th className="px-5 py-3.5">Added By</th>
                            <th className="px-5 py-3.5">Notes</th>
                            <th className="px-5 py-3.5 text-right">Delete</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60">
                        {rules.map((rule) => {
                            const typeStyle = TYPE_STYLES[rule.rule_type] ?? 'bg-slate-700 text-slate-400';
                            return (
                                <tr key={rule.rule_id} className="hover:bg-slate-900/60 transition-colors">
                                    <td className="px-5 py-3 font-mono text-slate-200 text-sm">{rule.pattern}</td>
                                    <td className="px-5 py-3">
                                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${typeStyle}`}>
                                            {rule.rule_type}
                                        </span>
                                    </td>
                                    <td className="px-5 py-3 text-slate-500 text-xs">{rule.match_type}</td>
                                    <td className="px-5 py-3 text-slate-500 text-xs">{rule.added_by}</td>
                                    <td className="px-5 py-3 text-slate-400 text-xs max-w-xs truncate" title={rule.notes}>{rule.notes}</td>
                                    <td className="px-5 py-3 text-right">
                                        <DeleteRuleButton ruleId={rule.rule_id} />
                                    </td>
                                </tr>
                            );
                        })}
                        {rules.length === 0 && (
                            <tr>
                                <td colSpan={6} className="px-5 py-12 text-center text-slate-500 italic">
                                    No governance rules defined. Add one above.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
