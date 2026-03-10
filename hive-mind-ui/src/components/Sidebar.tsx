'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Users, Activity, Settings, Mail, ShieldAlert, BarChart3, Database, Search, Briefcase, Flame, BookOpen, Telescope } from 'lucide-react';

import { clsx } from 'clsx';
import { useNavProgress } from './NavigationProgress';

// ── Spinner ────────────────────────────────────────────────────────────────
const Spinner = () => (
    <svg
        className="animate-spin text-blue-400"
        width={18}
        height={18}
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="Loading"
    >
        <circle
            className="opacity-20"
            cx="12" cy="12" r="10"
            stroke="currentColor"
            strokeWidth="3"
        />
        <path
            className="opacity-90"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
        />
    </svg>
);

// ── NavItem ────────────────────────────────────────────────────────────────
const NavItem = ({ href, icon: Icon, label }: { href: string; icon: any; label: string }) => {
    const pathname = usePathname();
    const { pendingHref, startNavigation } = useNavProgress();

    const isActive = pathname === href;
    const isPending = pendingHref === href;

    return (
        <Link
            href={href}
            onClick={() => {
                if (pathname !== href) startNavigation(href);
            }}
            className={clsx(
                'flex items-center gap-3 px-3 py-2 rounded-md transition-colors text-sm font-medium',
                isActive
                    ? 'bg-blue-600/10 text-blue-400'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800'
            )}
        >
            {/* Swap icon for spinner while this link is navigating */}
            <span className="shrink-0 relative flex items-center justify-center w-[18px] h-[18px]">
                <span
                    className={clsx(
                        'absolute inset-0 flex items-center justify-center transition-opacity duration-150',
                        isPending ? 'opacity-100' : 'opacity-0 pointer-events-none'
                    )}
                >
                    <Spinner />
                </span>
                <span
                    className={clsx(
                        'absolute inset-0 flex items-center justify-center transition-opacity duration-150',
                        isPending ? 'opacity-0' : 'opacity-100'
                    )}
                >
                    <Icon size={18} />
                </span>
            </span>
            <span>{label}</span>
        </Link>
    );
};

// ── NavGroup ───────────────────────────────────────────────────────────────
const NavGroup = ({ label, children }: { label: string; children: React.ReactNode }) => (
    <div className="mb-6">
        <h3 className="px-3 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
            {label}
        </h3>
        <div className="space-y-1">{children}</div>
    </div>
);

// ── Sidebar ────────────────────────────────────────────────────────────────
export default function Sidebar() {
    return (
        <div className="w-64 h-full bg-slate-900 border-r border-slate-800 flex flex-col">
            {/* Brand */}
            <div className="p-6 border-b border-slate-800">
                <div className="flex items-center gap-2 text-blue-500">
                    <Database size={24} />
                    <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                        Hive Mind
                    </span>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-700">
                <NavGroup label="Overview">
                    <NavItem href="/" icon={LayoutDashboard} label="Dashboard" />
                    <NavItem href="/activity" icon={Activity} label="Live Feed" />
                </NavGroup>

                <NavGroup label="Email Manager">
                    <NavItem href="/emails/reports" icon={BarChart3} label="Reports & Trends" />
                    <NavItem href="/emails/subscriptions" icon={Mail} label="Subscriptions" />
                    <NavItem href="/emails/quarantine" icon={Search} label="Quarantine Inspector" />
                    <NavItem href="/emails/governance" icon={ShieldAlert} label="Block List / Rules" />
                </NavGroup>

                <NavGroup label="Intelligence Unit">
                    <NavItem href="/emails/intelligence" icon={Database} label="Knowledge Graph" />
                    <NavItem href="/emails/knowledge" icon={BookOpen} label="Knowledge Base" />
                    <NavItem href="/emails/search" icon={Telescope} label="Semantic Search" />
                    <NavItem href="/emails/workforce" icon={Briefcase} label="Workforce Intelligence" />
                    <NavItem href="/emails/ops" icon={Flame} label="Ops War Room" />

                </NavGroup>

                <NavGroup label="Admin">
                    <NavItem href="/users" icon={Users} label="Domain Users" />
                    <NavItem href="/settings" icon={Settings} label="Settings" />
                </NavGroup>
            </nav>

            {/* User Footer */}
            <div className="p-4 border-t border-slate-800">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500" />
                    <div className="flex flex-col">
                        <span className="text-sm font-medium text-slate-200">Admin User</span>
                        <span className="text-xs text-slate-500">augos.io</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
