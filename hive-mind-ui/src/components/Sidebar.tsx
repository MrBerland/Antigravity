'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Users, Activity, Settings, Mail, ShieldAlert, BarChart3, Database, Search, Briefcase } from 'lucide-react';
import { clsx } from 'clsx';

const NavItem = ({ href, icon: Icon, label }: { href: string; icon: any; label: string }) => {
    const pathname = usePathname();
    const isActive = pathname === href;

    return (
        <Link
            href={href}
            className={clsx(
                'flex items-center gap-3 px-3 py-2 rounded-md transition-colors text-sm font-medium',
                isActive
                    ? 'bg-blue-600/10 text-blue-400'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800'
            )}
        >
            <Icon size={18} />
            <span>{label}</span>
        </Link>
    );
};

const NavGroup = ({ label, children }: { label: string; children: React.ReactNode }) => (
    <div className="mb-6">
        <h3 className="px-3 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
            {label}
        </h3>
        <div className="space-y-1">{children}</div>
    </div>
);

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
                    <NavItem href="/emails/workforce" icon={Briefcase} label="Workforce Intelligence" />
                    <NavItem href="/emails/ops" icon={ShieldAlert} label="Ops War Room" />
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
