"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import {
  Bell, Bot, CheckCircle2, Cloud, Database, ExternalLink, FileKey2,
  Globe2, KeyRound, LockKeyhole, Mail, MessageCircle, Server, Settings2,
  ShieldCheck, SlidersHorizontal, TriangleAlert, Users,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { fetchJson } from "../../lib/fetcher";

interface AiStatus {
  provider: "ollama" | "openrouter" | "anthropic";
  model: string;
  configured: boolean;
  privacy: "local" | "cloud";
  reason?: string;
}

interface DeploymentStatus {
  checkedAt: string;
  environment: "production" | "development";
  apiReachable: boolean;
  cookieSecure: boolean;
  integrations: Record<"email" | "slack" | "jira", { configured: boolean; missing: string[] }>;
}

interface ConfigField {
  key: string;
  label: string;
  purpose: string;
  example: string;
  required?: boolean;
  secret?: boolean;
}

interface SlaPolicyResp {
  critical_hours: number;
  high_hours: number;
  medium_hours: number;
  low_hours: number;
  info_hours: number;
  is_custom: boolean;
}
type SlaForm = Omit<SlaPolicyResp, "is_custom">;

const INTEGRATIONS: Record<string, { title: string; note: string; fields: ConfigField[] }> = {
  email: {
    title: "Email delivery",
    note: "Used for finding, SLA, and report workflow notifications. STARTTLS on port 587 is the recommended baseline.",
    fields: [
      { key: "SMTP_HOST", label: "Server hostname", purpose: "Resolvable outbound SMTP host.", example: "smtp.company.com", required: true },
      { key: "SMTP_PORT", label: "Transport port", purpose: "587 for STARTTLS; 465 only for implicit TLS.", example: "587", required: true },
      { key: "SMTP_USER", label: "Service identity", purpose: "Dedicated least-privilege mail account.", example: "vedha-alerts@company.com", required: true },
      { key: "SMTP_PASS", label: "Service password", purpose: "Store only in the deployment secret manager.", example: "Secret value", required: true, secret: true },
      { key: "SMTP_FROM", label: "Sender address", purpose: "Visible From address; align it with SPF/DKIM policy.", example: "vedha@company.com", required: true },
      { key: "SMTP_TO", label: "Default recipients", purpose: "Comma-separated security distribution list.", example: "security@company.com" },
    ],
  },
  slack: {
    title: "Slack notifications",
    note: "Use a dedicated incoming webhook restricted to one incident or security channel. Rotate it if disclosed.",
    fields: [
      { key: "SLACK_WEBHOOK_URL", label: "Incoming webhook", purpose: "Secret delivery endpoint for configured notification events.", example: "Secret value", required: true, secret: true },
    ],
  },
  jira: {
    title: "Jira issue workflow",
    note: "Use a dedicated service account with permission to create and update issues only in the security project.",
    fields: [
      { key: "JIRA_URL", label: "Base URL", purpose: "Jira Cloud or Server origin; HTTPS required in production.", example: "https://company.atlassian.net", required: true },
      { key: "JIRA_EMAIL", label: "Service account", purpose: "Identity associated with the Jira API token.", example: "vedha-bot@company.com", required: true },
      { key: "JIRA_API_TOKEN", label: "API token", purpose: "Secret token; never place it in a browser field or source control.", example: "Secret value", required: true, secret: true },
      { key: "JIRA_PROJECT_KEY", label: "Project key", purpose: "Destination project for generated remediation tickets.", example: "SEC", required: true },
    ],
  },
};

function SectionTitle({ icon: Icon, title, detail, badge }: {
  icon: React.ElementType; title: string; detail: string; badge?: string;
}) {
  return (
    <header className="settings-content-heading">
      <span><Icon size={18} /></span>
      <div><h2>{title}</h2><p>{detail}</p></div>
      {badge && <span className="badge badge-info">{badge}</span>}
    </header>
  );
}

function ReadOnlyNotice() {
  return (
    <div className="settings-security-notice">
      <LockKeyhole size={15} />
      <div><strong>Server-managed configuration</strong><span>Values are read from deployment environment or secret storage. Vedha never sends secret values to this page.</span></div>
    </div>
  );
}

function AiRuntimeSection() {
  const query = useQuery({
    queryKey: ["ai-status"],
    queryFn: () => fetchJson<AiStatus>("/api/ai/status"),
    refetchInterval: 30_000,
  });
  const runtime = query.data;

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Bot} title="AI runtime" detail="Manager owns model execution, prompt policy, and provider credentials." badge="Manager only" />
      <ReadOnlyNotice />

      <div className="settings-runtime-hero" data-ready={runtime?.configured ?? false}>
        <span>{runtime?.privacy === "cloud" ? <Cloud size={21} /> : <Server size={21} />}</span>
        <div>
          <small>Effective runtime</small>
          <strong>{runtime ? `${runtime.provider.toUpperCase()} · ${runtime.model}` : "Checking configuration…"}</strong>
          <p>{runtime?.privacy === "local" ? "Prompts stay on the configured Ollama host." : "Prompts are sent to the configured cloud model provider."}</p>
        </div>
        <span className={`badge ${runtime?.configured ? "badge-success" : "badge-high"}`}>{runtime?.configured ? "Available" : "Action needed"}</span>
      </div>

      {runtime?.reason && <div className="settings-warning"><TriangleAlert size={14} /> {runtime.reason}</div>}

      <div className="settings-provider-grid">
        <article data-active={runtime?.provider === "ollama"}>
          <header><Server size={17} /><div><strong>Ollama</strong><small>Default · local · no API fee</small></div></header>
          <p>Best for private deployments and predictable cost. Run Ollama where the Manager API can reach it.</p>
          <dl>
            <div><dt>Provider</dt><dd>LLM_PROVIDER=ollama</dd></div>
            <div><dt>Endpoint</dt><dd>OLLAMA_BASE_URL</dd></div>
            <div><dt>Model</dt><dd>OLLAMA_MODEL</dd></div>
          </dl>
        </article>
        <article data-active={runtime?.provider === "openrouter"}>
          <header><Cloud size={17} /><div><strong>OpenRouter</strong><small>Cloud · free router available</small></div></header>
          <p>Use <code>openrouter/free</code> for zero-cost experimentation, subject to provider rate limits and data-handling terms.</p>
          <dl>
            <div><dt>Provider</dt><dd>LLM_PROVIDER=openrouter</dd></div>
            <div><dt>Secret</dt><dd>OPENROUTER_API_KEY</dd></div>
            <div><dt>Free model</dt><dd>OPENROUTER_MODEL=openrouter/free</dd></div>
          </dl>
        </article>
        <article data-active={runtime?.provider === "anthropic"}>
          <header><Bot size={17} /><div><strong>Anthropic</strong><small>Backward compatible</small></div></header>
          <p>Retained for existing deployments. Provider credentials remain server-only.</p>
          <dl>
            <div><dt>Provider</dt><dd>LLM_PROVIDER=anthropic</dd></div>
            <div><dt>Secret</dt><dd>ANTHROPIC_API_KEY</dd></div>
            <div><dt>Model</dt><dd>LLM_MODEL</dd></div>
          </dl>
        </article>
      </div>

      <div className="settings-decision-note">
        <ShieldCheck size={16} />
        <div><strong>Recommended production default</strong><p>Use Ollama when engagement evidence cannot leave your network. Use OpenRouter only after reviewing the selected model&apos;s data retention, region, and contractual controls.</p></div>
      </div>
    </div>
  );
}

function AccessSection({ status }: { status?: DeploymentStatus }) {
  const rows = [
    { icon: Users, title: "Role-based access", status: "Manager enforced", detail: "Admin, manager, tester, and analyst permissions are checked by the FastAPI resource routes." },
    { icon: KeyRound, title: "Interactive sessions", status: "JWT access + refresh", detail: "Browser requests use the Manager-issued access token; refresh material should be rotated and short-lived." },
    { icon: FileKey2, title: "Personal access tokens", status: "Available through API", detail: "Use PATs for probes and automation. Grant only required scopes, set expiry, and revoke unused tokens." },
    { icon: Database, title: "Tenant isolation", status: "Resource scoped", detail: "Findings are authorized through their parent engagement and tenant boundary." },
  ];
  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={ShieldCheck} title="Access and security" detail="Authentication boundaries, automation credentials, and tenant isolation." />
      <div className="settings-readiness-grid">
        <article data-ready={status?.apiReachable ?? false}><Server size={16} /><div><small>Manager API</small><strong>{status?.apiReachable ? "Reachable" : "Unavailable"}</strong></div></article>
        <article data-ready={status?.cookieSecure ?? false}><LockKeyhole size={16} /><div><small>Secure session cookie</small><strong>{status?.cookieSecure ? "Enforced" : "Disabled"}</strong></div></article>
        <article data-ready={status?.environment === "production"}><Cloud size={16} /><div><small>Runtime mode</small><strong>{status?.environment ?? "Checking…"}</strong></div></article>
      </div>
      {status && !status.cookieSecure && (
        <div className="settings-warning"><TriangleAlert size={14} /> AUTH_COOKIE_SECURE is disabled. This is acceptable only for local HTTP development; enable it for every HTTPS deployment.</div>
      )}
      <div className="settings-access-list">
        {rows.map(({ icon: Icon, title, status, detail }) => (
          <article key={title}><span><Icon size={16} /></span><div><header><strong>{title}</strong><span>{status}</span></header><p>{detail}</p></div></article>
        ))}
      </div>
      <div className="settings-decision-note">
        <KeyRound size={16} />
        <div><strong>Credential hygiene</strong><p>Never reuse administrator passwords for probes. Create a scoped PAT per probe, record its owner and expiry, and rotate it when a probe is rebuilt or transferred.</p></div>
      </div>
    </div>
  );
}

function IntegrationSection({ kind, status }: { kind: keyof typeof INTEGRATIONS; status?: DeploymentStatus }) {
  const integration = INTEGRATIONS[kind];
  const Icon = kind === "email" ? Mail : kind === "slack" ? MessageCircle : ExternalLink;
  const readiness = status?.integrations[kind];
  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle
        icon={Icon}
        title={integration.title}
        detail={integration.note}
        badge={readiness?.configured ? "Configured" : "Needs setup"}
      />
      <ReadOnlyNotice />
      <div className="settings-integration-status" data-ready={readiness?.configured ?? false}>
        {readiness?.configured ? <CheckCircle2 size={16} /> : <TriangleAlert size={16} />}
        <div>
          <strong>{readiness?.configured ? "Required environment fields are present" : "Configuration is incomplete"}</strong>
          <span>{readiness
            ? readiness.configured
              ? "Secret values remain server-side and are not exposed here."
              : `Missing: ${readiness.missing.join(", ")}`
            : "Checking server configuration…"}</span>
        </div>
      </div>
      <div className="settings-field-table">
        <div className="settings-field-table-head"><span>Field</span><span>Operational meaning</span><span>Expected value</span></div>
        {integration.fields.map((field) => (
          <div className="settings-field-row" key={field.key}>
            <div><strong>{field.label}</strong><code>{field.key}</code></div>
            <p>{field.purpose}</p>
            <div><span>{field.secret ? <><LockKeyhole size={11} /> Secret</> : field.example}</span>{field.required && <small>Required</small>}</div>
          </div>
        ))}
      </div>
      <div className="settings-warning"><TriangleAlert size={14} /> Presence is verified, but delivery testing remains unavailable until a Manager-side integration API and audited test event are implemented.</div>
    </div>
  );
}

const SLA_ROWS: Array<{ key: keyof SlaForm; severity: string; color: string; intent: string }> = [
  { key: "critical_hours", severity: "CRITICAL", color: "var(--sev-critical-color)", intent: "Immediate owner assignment and executive visibility" },
  { key: "high_hours", severity: "HIGH", color: "var(--sev-high-color)", intent: "Prioritized remediation in the active sprint" },
  { key: "medium_hours", severity: "MEDIUM", color: "var(--sev-medium-color)", intent: "Planned remediation with risk acceptance if deferred" },
  { key: "low_hours", severity: "LOW", color: "var(--sev-low-color)", intent: "Routine hardening and hygiene backlog" },
  { key: "info_hours", severity: "INFO", color: "var(--text-faint)", intent: "Informational — 0 hours means untracked (no SLA)" },
];

function SlaSection() {
  const { data, refetch } = useQuery({
    queryKey: ["sla-policy"],
    queryFn: () => fetchJson<SlaPolicyResp>("/api/sla-policy"),
  });
  const [form, setForm] = useState<SlaForm | null>(null);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  React.useEffect(() => {
    if (data) setForm({
      critical_hours: data.critical_hours, high_hours: data.high_hours,
      medium_hours: data.medium_hours, low_hours: data.low_hours, info_hours: data.info_hours,
    });
  }, [data]);

  async function save() {
    if (!form) return;
    setSaving(true); setMsg(null);
    try {
      await fetchJson("/api/sla-policy", { method: "PUT", body: JSON.stringify(form) });
      await refetch();
      setMsg("SLA policy saved — applies across every SLA surface.");
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={SlidersHorizontal} title="SLA and risk policy"
        detail="Per-severity remediation windows in hours (0 = untracked). Applies to the dashboard, finding detail, and the customer portal."
        badge={data?.is_custom ? "Custom" : "Defaults"} />
      <div className="settings-sla-list">
        {SLA_ROWS.map((row) => (
          <article key={row.key} style={{ "--severity": row.color } as React.CSSProperties}>
            <span /><div><strong>{row.severity}</strong><p>{row.intent}</p></div>
            <label style={{ display: "flex", alignItems: "center", gap: 8, justifySelf: "end" }}>
              <input type="number" min={0} max={8760} disabled={!form}
                value={form ? form[row.key] : ""}
                onChange={(e) => setForm((f) => (f ? { ...f, [row.key]: Math.max(0, Number(e.target.value) || 0) } : f))}
                style={{ width: 84, padding: "6px 8px", borderRadius: 7, textAlign: "right",
                  border: "0.5px solid var(--border-subtle)", background: "var(--bg-surface)",
                  color: "var(--text-primary)", font: "12px var(--font-mono)" }} />
              <span style={{ color: "var(--text-muted)", fontSize: 11 }}>hours</span>
            </label>
          </article>
        ))}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 12 }}>
        <button onClick={() => void save()} disabled={saving || !form}
          style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "8px 14px",
            borderRadius: 8, border: "0.5px solid var(--border-accent)", background: "var(--accent-ghost)",
            color: "var(--accent)", cursor: saving || !form ? "default" : "pointer", fontWeight: 600, fontSize: 12 }}>
          {saving ? "Saving…" : "Save SLA policy"}
        </button>
        {msg && <span style={{ fontSize: 11.5, color: "var(--text-muted)" }}>{msg}</span>}
      </div>
    </div>
  );
}

function NotificationsSection() {
  const rules = [
    ["Critical finding opened", "Immediate", "Email + Slack", true],
    ["High finding opened", "Near real-time", "Slack", true],
    ["SLA enters at-risk state", "At threshold", "Email + Slack", true],
    ["Finding status changed", "Digest", "Email", false],
    ["Report approved", "Immediate", "Email", true],
  ] as const;
  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Bell} title="Notification policy" detail="Effective default routing. Persistence and audited editing are not yet available." badge="Read only" />
      <div className="settings-notification-list">
        {rules.map(([event, cadence, channel, enabled]) => (
          <article key={event}>
            <span className="settings-rule-icon" data-enabled={enabled}>{enabled ? <CheckCircle2 size={15} /> : <Bell size={15} />}</span>
            <div><strong>{event}</strong><small>{cadence} · {channel}</small></div>
            <span className={`badge ${enabled ? "badge-success" : "badge-info"}`}>{enabled ? "Enabled" : "Disabled"}</span>
          </article>
        ))}
      </div>
    </div>
  );
}

export default function SettingsPage() {
  const [section, setSection] = useState("ai");
  const statusQuery = useQuery({
    queryKey: ["settings-status"],
    queryFn: () => fetchJson<DeploymentStatus>("/api/settings/status"),
    refetchInterval: 30_000,
  });
  const deployment = statusQuery.data;
  const sections = [
    { key: "workspace", label: "Workspace", icon: Globe2 },
    { key: "ai", label: "AI runtime", icon: Bot },
    { key: "access", label: "Access & security", icon: ShieldCheck },
    { key: "email", label: "Email", icon: Mail },
    { key: "slack", label: "Slack", icon: MessageCircle },
    { key: "jira", label: "Jira", icon: ExternalLink },
    { key: "sla", label: "SLA policy", icon: SlidersHorizontal },
    { key: "notifications", label: "Notifications", icon: Bell },
  ];

  return (
    <PageShell title="Settings" subtitle="Deployment configuration, integrations, and policy guardrails">
      <div className="settings-layout">
        <aside className="settings-nav">
          <div className="settings-nav-heading"><Settings2 size={14} /> Configuration</div>
          {sections.map(({ key, label, icon: Icon }) => (
            <button key={key} className="settings-nav-button" data-active={section === key} onClick={() => setSection(key)}>
              <Icon size={14} /><span>{label}</span>
            </button>
          ))}
        </aside>

        <div>
          {section === "workspace" && (
            <div className="settings-panel animate-slide-in">
              <SectionTitle icon={Globe2} title="Workspace configuration" detail="Engagement-specific client, scope, and assessment settings." />
              <div className="settings-workspace-card">
                <span><Globe2 size={20} /></span>
                <div><strong>Configuration belongs with each engagement</strong><p>Client identity, authorized targets, exclusions, assessment dates, owner, and tags are validated by the Manager API and edited inside the engagement workspace.</p></div>
                <Link href="/engagements" className="btn btn-primary">Open engagements</Link>
              </div>
              <div className="settings-decision-note"><Database size={16} /><div><strong>Why this is separated</strong><p>Deployment settings control infrastructure; engagement settings control authorized testing scope. Keeping them separate reduces accidental cross-engagement changes.</p></div></div>
              <div className="settings-readiness-grid">
                <article data-ready={deployment?.apiReachable ?? false}><Server size={16} /><div><small>Manager API</small><strong>{deployment?.apiReachable ? "Reachable" : "Unavailable"}</strong></div></article>
                <article data-ready={deployment?.cookieSecure ?? false}><LockKeyhole size={16} /><div><small>Secure cookie</small><strong>{deployment?.cookieSecure ? "Enforced" : "Local only"}</strong></div></article>
                <article data-ready={Boolean(deployment)}><CheckCircle2 size={16} /><div><small>Last verified</small><strong>{deployment ? new Date(deployment.checkedAt).toLocaleTimeString() : "Checking…"}</strong></div></article>
              </div>
            </div>
          )}
          {section === "ai" && <AiRuntimeSection />}
          {section === "access" && <AccessSection status={deployment} />}
          {(section === "email" || section === "slack" || section === "jira") && <IntegrationSection kind={section} status={deployment} />}
          {section === "sla" && <SlaSection />}
          {section === "notifications" && <NotificationsSection />}
        </div>
      </div>
    </PageShell>
  );
}
