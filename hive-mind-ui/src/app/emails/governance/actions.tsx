'use client';

import { addGovernanceRule, deleteGovernanceRule } from '@/actions/governance';
import { Plus, Trash2, Loader2, X } from 'lucide-react';
import { useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';

// ── Add Rule Modal ────────────────────────────────────────────────────────────
export function AddRuleModal({ onClose }: { onClose: () => void }) {
    const [pattern, setPattern] = useState('');
    const [type, setType] = useState<'BLOCK' | 'ALLOW' | 'MARKETING' | 'PERSONAL' | 'SYSTEM'>('BLOCK');
    const [matchType, setMatchType] = useState<'DOMAIN_WILDCARD' | 'EXACT_EMAIL'>('DOMAIN_WILDCARD');
    const [notes, setNotes] = useState('');
    const [isPending, startTransition] = useTransition();
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!pattern.trim()) { setError('Pattern is required'); return; }
        setError('');
        startTransition(async () => {
            try {
                await addGovernanceRule(pattern.trim(), type, matchType, notes.trim());
                router.refresh();
                onClose();
            } catch (err: any) {
                setError(err.message ?? 'Failed to add rule');
            }
        });
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
            <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 w-full max-w-md shadow-2xl">
                <div className="flex justify-between items-center mb-5">
                    <h3 className="text-lg font-bold text-slate-100">Add Governance Rule</h3>
                    <button onClick={onClose} className="text-slate-500 hover:text-slate-200 transition-colors">
                        <X size={20} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Pattern */}
                    <div>
                        <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wide">Pattern</label>
                        <input
                            type="text"
                            value={pattern}
                            onChange={e => setPattern(e.target.value)}
                            placeholder={matchType === 'DOMAIN_WILDCARD' ? 'example.com' : 'user@example.com'}
                            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
                        />
                    </div>

                    {/* Match Type */}
                    <div>
                        <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wide">Match Type</label>
                        <div className="flex gap-2">
                            {(['DOMAIN_WILDCARD', 'EXACT_EMAIL'] as const).map(m => (
                                <button
                                    key={m}
                                    type="button"
                                    onClick={() => setMatchType(m)}
                                    className={`flex-1 py-1.5 rounded-lg text-xs font-semibold border transition-colors ${matchType === m ? 'bg-blue-600/20 border-blue-500 text-blue-400' : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200'}`}
                                >
                                    {m === 'DOMAIN_WILDCARD' ? 'Domain Wildcard' : 'Exact Email'}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Rule Type */}
                    <div>
                        <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wide">Rule Type</label>
                        <div className="flex flex-wrap gap-2">
                            {(['BLOCK', 'ALLOW', 'MARKETING', 'PERSONAL', 'SYSTEM'] as const).map(t => {
                                const colors: Record<string, string> = {
                                    BLOCK: 'bg-red-600/20 border-red-500 text-red-400',
                                    ALLOW: 'bg-green-600/20 border-green-500 text-green-400',
                                    MARKETING: 'bg-pink-600/20 border-pink-500 text-pink-400',
                                    PERSONAL: 'bg-purple-600/20 border-purple-500 text-purple-400',
                                    SYSTEM: 'bg-blue-600/20 border-blue-500 text-blue-400',
                                };
                                return (
                                    <button
                                        key={t}
                                        type="button"
                                        onClick={() => setType(t)}
                                        className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${type === t ? colors[t] : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200'}`}
                                    >
                                        {t}
                                    </button>
                                );
                            })}
                        </div>
                    </div>

                    {/* Notes */}
                    <div>
                        <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wide">Notes (optional)</label>
                        <input
                            type="text"
                            value={notes}
                            onChange={e => setNotes(e.target.value)}
                            placeholder="e.g. Marketing spam from partner"
                            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
                        />
                    </div>

                    {error && <p className="text-xs text-red-400">{error}</p>}

                    <div className="flex gap-3 pt-2">
                        <button type="button" onClick={onClose} className="flex-1 py-2 rounded-lg text-sm font-medium text-slate-400 hover:text-slate-200 border border-slate-700 hover:bg-slate-800 transition-colors">
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={isPending}
                            className="flex-1 py-2 rounded-lg text-sm font-semibold bg-blue-600 hover:bg-blue-500 text-white transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                        >
                            {isPending ? <Loader2 size={14} className="animate-spin" /> : <Plus size={14} />}
                            {isPending ? 'Adding…' : 'Add Rule'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

// ── Delete Button ─────────────────────────────────────────────────────────────
export function DeleteRuleButton({ ruleId }: { ruleId: string }) {
    const [isPending, startTransition] = useTransition();
    const router = useRouter();

    return (
        <button
            id={`delete-rule-${ruleId}`}
            disabled={isPending}
            onClick={() => {
                if (!confirm('Remove this governance rule?')) return;
                startTransition(async () => {
                    await deleteGovernanceRule(ruleId);
                    router.refresh();
                });
            }}
            className="text-slate-500 hover:text-red-400 transition-colors disabled:opacity-40"
            title="Delete rule"
        >
            {isPending ? <Loader2 size={16} className="animate-spin" /> : <Trash2 size={16} />}
        </button>
    );
}

// ── Add Rule Button (opens modal) ─────────────────────────────────────────────
export function AddRuleButton() {
    const [open, setOpen] = useState(false);
    return (
        <>
            <button
                id="add-governance-rule"
                onClick={() => setOpen(true)}
                className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
            >
                <Plus size={16} />
                Add Rule
            </button>
            {open && <AddRuleModal onClose={() => setOpen(false)} />}
        </>
    );
}
