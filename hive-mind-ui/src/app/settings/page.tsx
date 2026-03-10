import { Settings, Database, Mail, Shield, RefreshCw, Clock, Server, Key } from 'lucide-react';

export const dynamic = 'force-dynamic';

const SettingRow = ({ label, value, sub }: { label: string; value: string; sub?: string }) => (
    <div className="flex items-center justify-between py-3.5 border-b border-slate-800/60 last:border-0">
        <div>
            <p className="text-sm font-medium text-slate-200">{label}</p>
            {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
        </div>
        <span className="text-sm text-slate-400 font-mono bg-slate-800 px-3 py-1 rounded-md">{value}</span>
    </div>
);

const Section = ({ icon: Icon, title, color, children }: { icon: any; title: string; color: string; children: React.ReactNode }) => (
    <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-800 flex items-center gap-2">
            <Icon size={16} className={color} />
            <h2 className="text-sm font-semibold text-slate-200">{title}</h2>
        </div>
        <div className="px-5">{children}</div>
    </div>
);

const Command = ({ label, cmd }: { label: string; cmd: string }) => (
    <div className="py-3.5 border-b border-slate-800/60 last:border-0">
        <p className="text-xs font-semibold text-slate-400 mb-1">{label}</p>
        <code className="block text-xs text-green-400 bg-slate-900 px-3 py-2 rounded-md font-mono">{cmd}</code>
    </div>
);

export default function SettingsPage() {
    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <h1 className="text-3xl font-bold text-slate-100 flex items-center gap-3">
                    <Settings className="text-slate-400" />
                    Settings &amp; Configuration
                </h1>
                <p className="text-slate-500 mt-1">System configuration, pipeline controls, and operational references.</p>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {/* GCP Config */}
                <Section icon={Server} title="GCP Configuration" color="text-blue-400">
                    <SettingRow label="Project ID" value="augos-core-data" />
                    <SettingRow label="Region" value="us-central1" />
                    <SettingRow label="BigQuery Dataset" value="hive_mind_core" sub="All HiveMind tables" />
                    <SettingRow label="GCS Raw Lake" value="augos-core-data-raw-email-lake" sub="JSON email archive" />
                    <SettingRow label="Pub/Sub Topic" value="gmail-ingest-topic" sub="Gmail push notifications" />
                </Section>

                {/* AI Models */}
                <Section icon={Database} title="AI Models" color="text-purple-400">
                    <SettingRow label="Classifier" value="gemini-2.0-flash-exp" sub="Layer 2 classification via BQML" />
                    <SettingRow label="Embeddings" value="text-embedding-004" sub="Semantic search & similarity" />
                    <SettingRow label="Vertex Conn" value="augos-core-data.us.vertex-ai" />
                    <SettingRow label="L2 Cost" value="~$0.03 / 1,000 emails" sub="Each batch job" />
                    <SettingRow label="Embed Cost" value="~$0.000005 / email" sub="BUSINESS emails only" />
                </Section>

                {/* Pipeline Commands */}
                <Section icon={RefreshCw} title="Pipeline Commands" color="text-green-400">
                    <Command label="Full pipeline (fire & forget)"
                        cmd="nohup python3 HiveMind/hivemind_pipeline.py > /tmp/hivemind_pipeline.log 2>&1 &" />
                    <Command label="Layer 1 only (domain rules, free)"
                        cmd="python3 HiveMind/src/sql/run_classifier.py --layer1" />
                    <Command label="Layer 2 AI classification"
                        cmd="python3 HiveMind/src/sql/run_classifier.py --layer2 --batch 1000 --loops 500" />
                    <Command label="Run all AI agents"
                        cmd="python3 HiveMind/src/sql/run_all_agents.py --batch 200" />
                    <Command label="Check pipeline progress"
                        cmd="tail -f /tmp/hivemind_pipeline.log" />
                </Section>

                {/* Gmail Watch */}
                <Section icon={Mail} title="Gmail Watch" color="text-pink-400">
                    <SettingRow label="Watch Expiry" value="Every 7 days" sub="Auto-renewed by Cloud Scheduler" />
                    <SettingRow label="Scheduler" value="Mon 06:00 UTC" sub="hive-mind-watch-renewal job" />
                    <SettingRow label="Pub/Sub Topic" value="gmail-ingest-topic" />
                    <SettingRow label="Label Filter" value="INBOX" sub="Only INBOX messages ingested" />
                    <div className="py-3.5">
                        <p className="text-xs font-semibold text-slate-400 mb-1">Manual renewal (if needed)</p>
                        <code className="block text-xs text-green-400 bg-slate-900 px-3 py-2 rounded-md font-mono">
                            python3 HiveMind/activate_watch_all_users.py
                        </code>
                    </div>
                </Section>

                {/* Governance */}
                <Section icon={Shield} title="Governance" color="text-red-400">
                    <SettingRow label="Rule Table" value="dim_governance_rules" />
                    <SettingRow label="Match Types" value="EXACT_EMAIL / DOMAIN_WILDCARD" />
                    <SettingRow label="Rule Types" value="ALLOW / BLOCK / MARKETING / PERSONAL / SYSTEM" />
                    <SettingRow label="L1 Rules" value="30+ seed rules" sub="Gmail, Yahoo, Mailchimp, SendGrid…" />
                    <SettingRow label="Auto-rules" value="Unsubscribe Agent" sub="Adds MARKETING rule after each unsubscribe" />
                </Section>

                {/* Credentials */}
                <Section icon={Key} title="Credentials" color="text-yellow-400">
                    <SettingRow label="Service Account" value="hive-mind-admin.json" sub="HiveMind/credentials/ (gitignored)" />
                    <SettingRow label="DWD Required" value="Yes" sub="Google Admin Console → Domain-Wide Delegation" />
                    <SettingRow label="Scopes" value="gmail.readonly + gmail.modify" />
                    <SettingRow label="UI Auth" value="GOOGLE_APPLICATION_CREDENTIALS env var" sub="Set in .env.local for Next.js" />
                    <div className="py-3.5">
                        <p className="text-xs font-semibold text-slate-400 mb-1">Deploy to Cloud</p>
                        <code className="block text-xs text-green-400 bg-slate-900 px-3 py-2 rounded-md font-mono">
                            bash HiveMind/deploy_gcloud.sh
                        </code>
                    </div>
                </Section>
            </div>
        </div>
    );
}
