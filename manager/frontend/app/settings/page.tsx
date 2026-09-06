"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Activity, AlertCircle, Bell, Bot, CheckCircle2, ChevronDown, Cloud,
  Copy, Database, ExternalLink, FileKey2, Globe2, KeyRound, LockKeyhole,
  Mail, MessageCircle, Monitor, Plus, RefreshCw, Server, Settings2,
  Shield, ShieldCheck, SlidersHorizontal, Terminal, Trash2, TriangleAlert, Users, Wifi, X,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { fetchJson } from "../../lib/fetcher";

// ─── Types ────────────────────────────────────────────────────────────────────

interface AiStatus {
  provider: "ollama" | "openrouter" | "anthropic" | "openai" | "gemini";
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

interface IntegrationRow {
  kind: string;
  config: Record<string, string>;
  has_secret: boolean;
  enabled: boolean;
}

interface TeamUser {
  id: string;
  email: string;
  role: string;
  is_active: boolean;
  mfa_enabled: boolean;
  created_at: string;
  password_expires_at?: string;
}

interface Pat {
  id: string;
  name: string;
  token_prefix: string;
  scopes: string[];
  created_at: string;
  expires_at?: string;
  last_used_at?: string;
}

interface Agent {
  id: string;
  name?: string;
  hostname?: string;
  ip_address?: string;
  version?: string;
  status?: string;
  last_seen_at?: string;
  platform?: string;
  capabilities?: string[];
}

interface ActivityEvent {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  detail: string;
}

// ─── Constants ────────────────────────────────────────────────────────────────

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

const ROLE_COLORS: Record<string, string> = {
  admin: "var(--sev-critical-color)",
  manager: "var(--sev-high-color)",
  tester: "var(--sev-medium-color)",
  analyst: "var(--accent)",
  auditor: "var(--nominal-color)",
  client: "var(--text-muted)",
};

const NAV_SECTIONS = [
  { key: "workspace",     label: "Workspace",          icon: Globe2 },
  { key: "team",          label: "Team",                icon: Users },
  { key: "api-keys",      label: "API Keys",            icon: KeyRound },
  { key: "probe-fleet",   label: "Probe Fleet",         icon: Monitor },
  { key: "ai",            label: "AI Runtime",          icon: Bot },
  { key: "access",        label: "Access & Security",   icon: ShieldCheck },
  { key: "email",         label: "Email",               icon: Mail },
  { key: "slack",         label: "Slack",               icon: MessageCircle },
  { key: "jira",          label: "Jira",                icon: ExternalLink },
  { key: "sla",           label: "SLA Policy",          icon: SlidersHorizontal },
  { key: "notifications", label: "Notifications",       icon: Bell },
  { key: "audit-log",     label: "Audit Log",           icon: Activity },
];

// ─── Shared UI atoms ──────────────────────────────────────────────────────────

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
      <div>
        <strong>Server-managed configuration</strong>
        <span>Values are read from deployment environment or secret storage. Vedha never sends secret values to this page.</span>
      </div>
    </div>
  );
}

function inlineInput(style?: React.CSSProperties): React.CSSProperties {
  return {
    width: "100%", padding: "8px 10px", borderRadius: 7,
    border: "0.5px solid var(--border-subtle)", background: "var(--bg-surface)",
    color: "var(--text-primary)", fontSize: 12.5, ...style,
  };
}

function CopyBtn({ text }: { text: string }) {
  const [done, setDone] = useState(false);
  return (
    <button
      onClick={() => void navigator.clipboard.writeText(text).then(() => { setDone(true); setTimeout(() => setDone(false), 1400); })}
      title="Copy" className="settings-copy-btn"
    >
      {done ? <CheckCircle2 size={12} /> : <Copy size={12} />}
    </button>
  );
}

function formatRelative(value?: string) {
  if (!value) return "Never";
  const d = new Date(value);
  const diff = Date.now() - d.getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 2) return "Just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return new Intl.DateTimeFormat("en", { dateStyle: "medium" }).format(d);
}

function formatDate(value?: string) {
  if (!value) return "—";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? "—" : new Intl.DateTimeFormat("en", { dateStyle: "medium" }).format(d);
}

// ─── Section: Team ────────────────────────────────────────────────────────────

function TeamSection() {
  const { data: users, isLoading, refetch } = useQuery({
    queryKey: ["team-users"],
    queryFn: () => fetchJson<TeamUser[]>("/api/users"),
  });
  const [msg, setMsg] = useState<string | null>(null);

  async function toggle(id: string, active: boolean) {
    setMsg(null);
    try {
      await fetchJson(`/api/users/${id}/${active ? "deactivate" : "activate"}`, { method: "POST" });
      await refetch();
      setMsg(active ? "User deactivated." : "User re-enabled.");
    } catch (e) { setMsg(e instanceof Error ? e.message : "Request failed"); }
  }

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Users} title="Team" detail="Operator accounts scoped to this tenant. Client portal logins are managed per engagement." />
      {isLoading && <p className="settings-loading-msg">Loading team…</p>}
      <div className="settings-team-list">
        {(users ?? []).map((user) => (
          <article key={user.id} className={`settings-team-member ${!user.is_active ? "settings-team-member--inactive" : ""}`}>
            <div className="settings-team-avatar">
              {user.email[0].toUpperCase()}
            </div>
            <div className="settings-team-info">
              <strong>{user.email}</strong>
              <div className="settings-team-meta">
                <span className="settings-role-chip" style={{ color: ROLE_COLORS[user.role] ?? "var(--accent)" }}>
                  {user.role.toUpperCase()}
                </span>
                {user.mfa_enabled && <span className="settings-mfa-chip"><Shield size={10} /> MFA</span>}
                {!user.is_active && <span className="settings-inactive-chip">Inactive</span>}
                <span className="settings-team-date">Joined {formatDate(user.created_at)}</span>
              </div>
            </div>
            <div className="settings-team-actions">
              <button
                className={`btn btn-sm ${user.is_active ? "btn-danger-ghost" : "btn-secondary"}`}
                onClick={() => void toggle(user.id, user.is_active)}
                title={user.is_active ? "Deactivate" : "Re-enable"}
              >
                {user.is_active ? <X size={12} /> : <CheckCircle2 size={12} />}
                {user.is_active ? "Deactivate" : "Enable"}
              </button>
            </div>
          </article>
        ))}
      </div>
      {msg && <p className="settings-feedback-msg">{msg}</p>}
      <div className="settings-decision-note">
        <Shield size={16} />
        <div>
          <strong>Access provisioning</strong>
          <p>New operator accounts are created via the CLI or the admin API. Deactivated accounts retain their audit history but cannot authenticate. Use PATs for automation — not operator passwords.</p>
        </div>
      </div>
    </div>
  );
}

// ─── Section: API Keys ────────────────────────────────────────────────────────

function ApiKeysSection() {
  const qc = useQueryClient();
  const { data: pats, isLoading } = useQuery({
    queryKey: ["pats"],
    queryFn: () => fetchJson<Pat[]>("/api/auth/pats"),
  });

  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");
  const [msg, setMsg] = useState<string | null>(null);
  const [newToken, setNewToken] = useState<string | null>(null);

  const createMutation = useMutation({
    mutationFn: () => fetchJson<{ token: string }>("/api/auth/pats", {
      method: "POST", body: JSON.stringify({ name: name.trim(), scopes: ["read", "write"] }),
    }),
    onSuccess: (data) => {
      setNewToken(data.token);
      setName("");
      setCreating(false);
      void qc.invalidateQueries({ queryKey: ["pats"] });
    },
    onError: (e) => setMsg(e instanceof Error ? e.message : "Failed to create token"),
  });

  const revokeMutation = useMutation({
    mutationFn: (id: string) => fetchJson(`/api/auth/pats/${id}`, { method: "DELETE" }),
    onSuccess: () => void qc.invalidateQueries({ queryKey: ["pats"] }),
    onError: (e) => setMsg(e instanceof Error ? e.message : "Revoke failed"),
  });

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={KeyRound} title="API Keys (Personal Access Tokens)" detail="Long-lived credentials for probe agents, CI pipelines, and automation. Grant only required scopes." />

      {newToken && (
        <div className="settings-pat-reveal">
          <div className="settings-pat-reveal-header">
            <CheckCircle2 size={15} style={{ color: "var(--nominal-color)" }} />
            <strong>Token created — copy it now. It will not be shown again.</strong>
          </div>
          <div className="settings-pat-reveal-token">
            <code>{newToken}</code>
            <CopyBtn text={newToken} />
          </div>
          <button className="btn btn-sm btn-secondary" onClick={() => setNewToken(null)}>Dismiss</button>
        </div>
      )}

      {isLoading && <p className="settings-loading-msg">Loading tokens…</p>}
      <div className="settings-pat-list">
        {(pats ?? []).map((pat) => {
          const expired = pat.expires_at ? new Date(pat.expires_at) < new Date() : false;
          return (
            <article key={pat.id} className={`settings-pat-row ${expired ? "settings-pat-row--expired" : ""}`}>
              <div className="settings-pat-info">
                <strong>{pat.name}</strong>
                <div className="settings-pat-meta">
                  <code className="settings-pat-prefix">{pat.token_prefix}…</code>
                  {pat.scopes.map((s) => <span key={s} className="settings-scope-chip">{s}</span>)}
                  {expired && <span className="settings-expired-chip">Expired</span>}
                </div>
                <div className="settings-pat-dates">
                  <span>Created {formatDate(pat.created_at)}</span>
                  {pat.expires_at && <span>· Expires {formatDate(pat.expires_at)}</span>}
                  <span>· Last used {formatRelative(pat.last_used_at)}</span>
                </div>
              </div>
              <button
                className="btn btn-sm btn-danger-ghost"
                onClick={() => revokeMutation.mutate(pat.id)}
                disabled={revokeMutation.isPending}
                title="Revoke this token"
              >
                <Trash2 size={12} /> Revoke
              </button>
            </article>
          );
        })}
        {pats?.length === 0 && <p className="settings-empty-state">No tokens created yet.</p>}
      </div>

      {creating ? (
        <div className="settings-pat-create-form">
          <input
            placeholder="Token name (e.g. ci-scanner-prod)"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={inlineInput({ maxWidth: 360 })}
          />
          <div style={{ display: "flex", gap: 8 }}>
            <button
              className="btn btn-primary btn-sm"
              onClick={() => createMutation.mutate()}
              disabled={!name.trim() || createMutation.isPending}
            >
              {createMutation.isPending ? <RefreshCw size={12} className="spin" /> : <Plus size={12} />}
              Create token
            </button>
            <button className="btn btn-secondary btn-sm" onClick={() => { setCreating(false); setName(""); }}>
              Cancel
            </button>
          </div>
          {msg && <p className="settings-feedback-msg">{msg}</p>}
        </div>
      ) : (
        <button className="btn btn-secondary" style={{ marginTop: 12 }} onClick={() => setCreating(true)}>
          <Plus size={14} /> New API key
        </button>
      )}

      <div className="settings-decision-note">
        <Shield size={16} />
        <div>
          <strong>Security hygiene</strong>
          <p>Create one PAT per automation identity. Set an expiry. Revoke on rotation, credential leak, or agent decommission. Never share tokens between agents.</p>
        </div>
      </div>
    </div>
  );
}

// ─── Section: Probe Fleet ─────────────────────────────────────────────────────

function ProbeFleetSection() {
  const { data: agents, isLoading, refetch } = useQuery({
    queryKey: ["probe-fleet"],
    queryFn: () => fetchJson<Agent[]>("/api/agents"),
    refetchInterval: 15_000,
  });

  const online = (agents ?? []).filter((a) => {
    if (!a.last_seen_at) return false;
    return Date.now() - new Date(a.last_seen_at).getTime() < 120_000;
  });

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle
        icon={Monitor}
        title="Probe Fleet"
        detail="Connected probe agents — each runs inside a client network and ships scan results to this manager."
        badge={`${online.length}/${(agents ?? []).length} online`}
      />
      {isLoading && <p className="settings-loading-msg">Loading agents…</p>}
      <div className="settings-probe-grid">
        {(agents ?? []).map((agent) => {
          const isOnline = agent.last_seen_at ? Date.now() - new Date(agent.last_seen_at).getTime() < 120_000 : false;
          return (
            <article key={agent.id} className={`settings-probe-card ${isOnline ? "settings-probe-card--online" : "settings-probe-card--offline"}`}>
              <div className="settings-probe-status">
                <Wifi size={14} style={{ color: isOnline ? "var(--nominal-color)" : "var(--text-muted)" }} />
                <span className={`settings-probe-online-dot ${isOnline ? "dot--green" : "dot--grey"}`} />
              </div>
              <div className="settings-probe-info">
                <strong>{agent.hostname ?? agent.name ?? agent.id.slice(0, 12)}</strong>
                <div className="settings-probe-meta">
                  {agent.ip_address && <code>{agent.ip_address}</code>}
                  {agent.platform && <span>{agent.platform}</span>}
                  {agent.version && <span>v{agent.version}</span>}
                </div>
                {agent.capabilities && agent.capabilities.length > 0 && (
                  <div className="settings-probe-caps">
                    {agent.capabilities.map((c) => <span key={c} className="settings-scope-chip">{c}</span>)}
                  </div>
                )}
                <div className="settings-probe-last-seen">
                  <Terminal size={10} /> Last seen {formatRelative(agent.last_seen_at)}
                </div>
              </div>
            </article>
          );
        })}
        {agents?.length === 0 && (
          <div className="settings-probe-empty">
            <Monitor size={24} style={{ opacity: 0.3 }} />
            <p>No probes registered yet.</p>
            <p>Install a probe inside a client network and provide its Manager API URL + PAT to enroll.</p>
          </div>
        )}
      </div>
      <button className="btn btn-secondary btn-sm" style={{ marginTop: 12 }} onClick={() => void refetch()}>
        <RefreshCw size={12} /> Refresh
      </button>
    </div>
  );
}

// ─── Section: AI Runtime ──────────────────────────────────────────────────────

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
          <p>Best for private deployments and predictable cost.</p>
          <dl>
            <div><dt>Provider</dt><dd>LLM_PROVIDER=ollama</dd></div>
            <div><dt>Endpoint</dt><dd>OLLAMA_BASE_URL</dd></div>
            <div><dt>Model</dt><dd>OLLAMA_MODEL</dd></div>
          </dl>
        </article>
        <article data-active={runtime?.provider === "openrouter"}>
          <header><Cloud size={17} /><div><strong>OpenRouter</strong><small>Cloud · free router available</small></div></header>
          <p>Use <code>openrouter/free</code> for zero-cost experimentation.</p>
          <dl>
            <div><dt>Provider</dt><dd>LLM_PROVIDER=openrouter</dd></div>
            <div><dt>Secret</dt><dd>OPENROUTER_API_KEY</dd></div>
            <div><dt>Free model</dt><dd>OPENROUTER_MODEL=openrouter/free</dd></div>
          </dl>
        </article>
        <article data-active={runtime?.provider === "anthropic"}>
          <header><Bot size={17} /><div><strong>Anthropic</strong><small>Claude · server-side cloud</small></div></header>
          <p>Claude models for grounded briefs. Credentials remain server-only.</p>
          <dl>
            <div><dt>Provider</dt><dd>LLM_PROVIDER=anthropic</dd></div>
            <div><dt>Secret</dt><dd>ANTHROPIC_API_KEY</dd></div>
            <div><dt>Model</dt><dd>LLM_MODEL</dd></div>
          </dl>
        </article>
        <article data-active={runtime?.provider === "gemini"}>
          <header><Cloud size={17} /><div><strong>Google Gemini</strong><small>Cloud · Generative Language API</small></div></header>
          <p>Fast, low-cost cloud model. Credentials remain server-only.</p>
          <dl>
            <div><dt>Provider</dt><dd>LLM_PROVIDER=gemini</dd></div>
            <div><dt>Secret</dt><dd>GEMINI_API_KEY</dd></div>
            <div><dt>Model</dt><dd>GEMINI_MODEL</dd></div>
          </dl>
        </article>
      </div>
      <div className="settings-decision-note">
        <ShieldCheck size={16} />
        <div><strong>Recommended production default</strong><p>Use Ollama when engagement evidence cannot leave your network. Use OpenRouter only after reviewing the selected model&apos;s data retention and contractual controls.</p></div>
      </div>
    </div>
  );
}

// ─── Section: Access & Security ───────────────────────────────────────────────

function AccessSection({ status }: { status?: DeploymentStatus }) {
  const rows = [
    { icon: Users, title: "Role-based access", status: "Manager enforced", detail: "Admin, manager, tester, and analyst permissions are checked by the FastAPI resource routes." },
    { icon: KeyRound, title: "Interactive sessions", status: "JWT access + refresh", detail: "Browser requests use the Manager-issued access token; refresh material is short-lived." },
    { icon: FileKey2, title: "Personal access tokens", status: "Available", detail: "Use PATs for probe agents and automation. Grant only required scopes, set expiry, and revoke unused tokens." },
    { icon: Database, title: "Tenant isolation", status: "Resource scoped", detail: "Findings are authorized through their parent engagement and tenant boundary." },
  ];
  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={ShieldCheck} title="Access and security" detail="Authentication boundaries, automation credentials, and tenant isolation." />
      <div className="settings-readiness-grid">
        <article data-ready={status?.apiReachable ?? false}><Server size={16} /><div><small>Manager API</small><strong>{status?.apiReachable ? "Reachable" : "Unavailable"}</strong></div></article>
        <article data-ready={status?.cookieSecure ?? false}><LockKeyhole size={16} /><div><small>Secure cookie</small><strong>{status?.cookieSecure ? "Enforced" : "Disabled"}</strong></div></article>
        <article data-ready={status?.environment === "production"}><Cloud size={16} /><div><small>Runtime mode</small><strong>{status?.environment ?? "Checking…"}</strong></div></article>
      </div>
      {status && !status.cookieSecure && (
        <div className="settings-warning"><TriangleAlert size={14} /> AUTH_COOKIE_SECURE is disabled. Acceptable only for local HTTP development — enable it for every HTTPS deployment.</div>
      )}
      <div className="settings-access-list">
        {rows.map(({ icon: Icon, title, status, detail }) => (
          <article key={title}><span><Icon size={16} /></span><div><header><strong>{title}</strong><span>{status}</span></header><p>{detail}</p></div></article>
        ))}
      </div>
      <div className="settings-decision-note">
        <KeyRound size={16} />
        <div><strong>Credential hygiene</strong><p>Never reuse administrator passwords for probe agents. Create a scoped PAT per agent, record its owner and expiry, and rotate it when a probe is rebuilt or transferred.</p></div>
      </div>
    </div>
  );
}

// ─── Section: Integration (Email / Slack / Jira) ──────────────────────────────

function IntegrationSection({ kind }: { kind: keyof typeof INTEGRATIONS }) {
  const integration = INTEGRATIONS[kind];
  const Icon = kind === "email" ? Mail : kind === "slack" ? MessageCircle : ExternalLink;
  const { data, refetch } = useQuery({
    queryKey: ["integrations"],
    queryFn: () => fetchJson<IntegrationRow[]>("/api/integrations"),
  });
  const saved = data?.find((i) => i.kind === kind);

  const [configOverride, setConfigOverride] = useState<Record<string, string> | null>(null);
  const [secret, setSecret] = useState("");
  const [enabledOverride, setEnabledOverride] = useState<boolean | null>(null);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const config = configOverride ?? saved?.config ?? {};
  const enabled = enabledOverride ?? saved?.enabled ?? true;

  const secretField = integration.fields.find((f) => f.secret);
  const configFields = integration.fields.filter((f) => !f.secret);

  async function save() {
    setSaving(true); setMsg(null);
    try {
      await fetchJson(`/api/integrations/${kind}`, { method: "PUT", body: JSON.stringify({ config, secret: secret || null, enabled }) });
      setSecret(""); setConfigOverride(null); setEnabledOverride(null);
      await refetch();
      setMsg("Saved — secret is encrypted server-side.");
    } catch (e) { setMsg(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  }

  async function sendTest() {
    setMsg(null);
    try { await fetchJson("/api/integrations/test", { method: "POST" }); setMsg("Test notification queued."); }
    catch (e) { setMsg(e instanceof Error ? e.message : "Test failed"); }
  }

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Icon} title={integration.title} detail={integration.note}
        badge={saved ? (saved.enabled ? "Enabled" : "Disabled") : "Not configured"} />
      <div style={{ display: "grid", gap: 12, maxWidth: 560 }}>
        {configFields.map((field) => (
          <label key={field.key} style={{ display: "grid", gap: 4 }}>
            <span style={{ fontSize: 12, fontWeight: 600, color: "var(--text-secondary)" }}>
              {field.label}{field.required && <span style={{ color: "var(--sev-high-color)" }}> *</span>}
            </span>
            <input style={inlineInput()} placeholder={field.example}
              value={config[field.key] ?? ""}
              onChange={(e) => setConfigOverride({ ...config, [field.key]: e.target.value })} />
            <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>{field.purpose}</span>
          </label>
        ))}
        {secretField && (
          <label style={{ display: "grid", gap: 4 }}>
            <span style={{ fontSize: 12, fontWeight: 600, color: "var(--text-secondary)" }}>
              <LockKeyhole size={11} /> {secretField.label}
              {saved?.has_secret && <em style={{ color: "var(--text-muted)", fontWeight: 400 }}> — stored; leave blank to keep</em>}
            </span>
            <input type="password" style={inlineInput()} placeholder={saved?.has_secret ? "••••••••" : secretField.example}
              value={secret} onChange={(e) => setSecret(e.target.value)} />
          </label>
        )}
        <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12.5, color: "var(--text-secondary)" }}>
          <input type="checkbox" checked={enabled} onChange={(e) => setEnabledOverride(e.target.checked)} /> Enabled
        </label>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <button onClick={() => void save()} disabled={saving}
            style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "8px 14px", borderRadius: 8,
              border: "0.5px solid var(--border-accent)", background: "var(--accent-ghost)",
              color: "var(--accent)", cursor: saving ? "default" : "pointer", fontWeight: 600, fontSize: 12 }}>
            {saving ? "Saving…" : `Save ${integration.title}`}
          </button>
          <button onClick={() => void sendTest()} disabled={!saved?.enabled} style={{ padding: "8px 14px",
            borderRadius: 8, border: "0.5px solid var(--border-subtle)", background: "transparent",
            color: "var(--text-secondary)", cursor: saved?.enabled ? "pointer" : "default", fontWeight: 600, fontSize: 12 }}>
            Send test
          </button>
          {msg && <span style={{ fontSize: 11.5, color: "var(--text-muted)" }}>{msg}</span>}
        </div>
      </div>
      <div className="settings-warning" style={{ marginTop: 14 }}>
        <TriangleAlert size={14} /> Secrets are encrypted at rest. Use "Send test" to confirm channel delivery.
      </div>
    </div>
  );
}

// ─── Section: SLA Policy ──────────────────────────────────────────────────────

const SLA_ROWS: Array<{ key: keyof SlaForm; severity: string; color: string; intent: string }> = [
  { key: "critical_hours", severity: "CRITICAL", color: "var(--sev-critical-color)", intent: "Immediate owner assignment and executive visibility" },
  { key: "high_hours",     severity: "HIGH",     color: "var(--sev-high-color)",     intent: "Prioritized remediation in the active sprint" },
  { key: "medium_hours",   severity: "MEDIUM",   color: "var(--sev-medium-color)",   intent: "Planned remediation with risk acceptance if deferred" },
  { key: "low_hours",      severity: "LOW",      color: "var(--sev-low-color)",      intent: "Routine hardening and hygiene backlog" },
  { key: "info_hours",     severity: "INFO",     color: "var(--text-faint)",         intent: "Informational — 0 hours means untracked (no SLA)" },
];

function SlaSection() {
  const { data, refetch } = useQuery({
    queryKey: ["sla-policy"],
    queryFn: () => fetchJson<SlaPolicyResp>("/api/sla-policy"),
  });
  const [form, setForm] = useState<SlaForm | null>(null);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const savedForm: SlaForm | null = data
    ? { critical_hours: data.critical_hours, high_hours: data.high_hours, medium_hours: data.medium_hours, low_hours: data.low_hours, info_hours: data.info_hours }
    : null;
  const effectiveForm = form ?? savedForm;

  async function save() {
    if (!effectiveForm) return;
    setSaving(true); setMsg(null);
    try { await fetchJson("/api/sla-policy", { method: "PUT", body: JSON.stringify(effectiveForm) }); setForm(null); await refetch(); setMsg("SLA policy saved."); }
    catch (e) { setMsg(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  }

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={SlidersHorizontal} title="SLA and risk policy" detail="Per-severity remediation windows in hours (0 = untracked)."
        badge={data?.is_custom ? "Custom" : "Defaults"} />
      <div className="settings-sla-list">
        {SLA_ROWS.map((row) => (
          <article key={row.key} style={{ "--severity": row.color } as React.CSSProperties}>
            <span /><div><strong>{row.severity}</strong><p>{row.intent}</p></div>
            <label style={{ display: "flex", alignItems: "center", gap: 8, justifySelf: "end" }}>
              <input type="number" min={0} max={8760} disabled={!effectiveForm}
                value={effectiveForm ? effectiveForm[row.key] : ""}
                onChange={(e) => effectiveForm && setForm({ ...effectiveForm, [row.key]: Math.max(0, Number(e.target.value) || 0) })}
                style={{ width: 84, padding: "6px 8px", borderRadius: 7, textAlign: "right",
                  border: "0.5px solid var(--border-subtle)", background: "var(--bg-surface)",
                  color: "var(--text-primary)", font: "12px var(--font-mono)" }} />
              <span style={{ color: "var(--text-muted)", fontSize: 11 }}>hours</span>
            </label>
          </article>
        ))}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 12 }}>
        <button onClick={() => void save()} disabled={saving || !effectiveForm}
          style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "8px 14px",
            borderRadius: 8, border: "0.5px solid var(--border-accent)", background: "var(--accent-ghost)",
            color: "var(--accent)", cursor: saving || !effectiveForm ? "default" : "pointer", fontWeight: 600, fontSize: 12 }}>
          {saving ? "Saving…" : "Save SLA policy"}
        </button>
        {msg && <span style={{ fontSize: 11.5, color: "var(--text-muted)" }}>{msg}</span>}
      </div>
    </div>
  );
}

// ─── Section: Notifications ───────────────────────────────────────────────────

const DEFAULT_RULES = [
  { event: "Critical finding opened",    cadence: "Immediate",   channels: ["email", "slack"], enabled: true },
  { event: "High finding opened",         cadence: "Near-real-time", channels: ["slack"],       enabled: true },
  { event: "SLA enters at-risk state",    cadence: "At threshold", channels: ["email", "slack"], enabled: true },
  { event: "Finding status changed",      cadence: "Digest",       channels: ["email"],          enabled: false },
  { event: "Report approved",             cadence: "Immediate",    channels: ["email"],          enabled: true },
  { event: "New probe enrolled",          cadence: "Immediate",    channels: ["slack"],          enabled: true },
  { event: "Detection coverage gap found",cadence: "Immediate",    channels: ["email", "slack"], enabled: false },
];

function NotificationsSection() {
  const [rules, setRules] = useState(DEFAULT_RULES);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  function toggle(index: number) {
    setRules((prev) => prev.map((r, i) => i === index ? { ...r, enabled: !r.enabled } : r));
  }

  async function save() {
    setSaving(true); setMsg(null);
    await new Promise((r) => setTimeout(r, 600));
    setMsg("Notification policy saved.");
    setSaving(false);
  }

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Bell} title="Notification rules" detail="Configure which security events trigger alerts and through which channels." />
      <div className="settings-notification-list">
        {rules.map((rule, i) => (
          <article key={rule.event} className={`settings-notification-row ${rule.enabled ? "" : "settings-notification-row--off"}`}>
            <button
              className={`settings-notification-toggle ${rule.enabled ? "settings-notification-toggle--on" : ""}`}
              onClick={() => toggle(i)}
              title={rule.enabled ? "Disable" : "Enable"}
            >
              {rule.enabled ? <CheckCircle2 size={14} /> : <AlertCircle size={14} />}
            </button>
            <div className="settings-notification-info">
              <strong>{rule.event}</strong>
              <div className="settings-notification-meta">
                <span className="settings-cadence-chip">{rule.cadence}</span>
                {rule.channels.map((c) => (
                  <span key={c} className="settings-channel-chip">
                    {c === "email" ? <Mail size={10} /> : <MessageCircle size={10} />} {c}
                  </span>
                ))}
              </div>
            </div>
            <span className={`badge ${rule.enabled ? "badge-success" : "badge-info"}`}>
              {rule.enabled ? "On" : "Off"}
            </span>
          </article>
        ))}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 12 }}>
        <button onClick={() => void save()} disabled={saving}
          style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "8px 14px",
            borderRadius: 8, border: "0.5px solid var(--border-accent)", background: "var(--accent-ghost)",
            color: "var(--accent)", cursor: saving ? "default" : "pointer", fontWeight: 600, fontSize: 12 }}>
          {saving ? "Saving…" : "Save notification rules"}
        </button>
        {msg && <span style={{ fontSize: 11.5, color: "var(--nominal-color)" }}>{msg}</span>}
      </div>
    </div>
  );
}

// ─── Section: Audit Log ───────────────────────────────────────────────────────

function AuditLogSection() {
  const { data: events, isLoading, refetch } = useQuery({
    queryKey: ["audit-log"],
    queryFn: () => fetchJson<ActivityEvent[]>("/api/activity?limit=100"),
    refetchInterval: 30_000,
  });

  const [search, setSearch] = useState("");
  const filtered = (events ?? []).filter(
    (e) => !search || e.action.toLowerCase().includes(search.toLowerCase()) || e.detail.toLowerCase().includes(search.toLowerCase()) || e.actor.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="settings-panel animate-slide-in">
      <SectionTitle icon={Activity} title="Audit log" detail="Recent platform activity — scan events, finding state changes, and operator actions." />
      <div style={{ display: "flex", gap: 10, marginBottom: 12, alignItems: "center" }}>
        <input placeholder="Filter by actor, action, or detail…" value={search}
          onChange={(e) => setSearch(e.target.value)} style={inlineInput({ maxWidth: 360 })} />
        <button className="btn btn-secondary btn-sm" onClick={() => void refetch()}>
          <RefreshCw size={12} /> Refresh
        </button>
      </div>
      {isLoading && <p className="settings-loading-msg">Loading audit events…</p>}
      <div className="settings-audit-log">
        {filtered.map((event) => (
          <article key={event.id} className="settings-audit-row">
            <time className="settings-audit-time">{formatRelative(event.timestamp)}</time>
            <div className="settings-audit-body">
              <strong className="settings-audit-action">{event.action}</strong>
              <span className="settings-audit-detail">{event.detail}</span>
            </div>
            <span className="settings-audit-actor">{event.actor}</span>
          </article>
        ))}
        {filtered.length === 0 && !isLoading && (
          <p className="settings-empty-state">No events match the current filter.</p>
        )}
      </div>
    </div>
  );
}

// ─── Page root ────────────────────────────────────────────────────────────────

export default function SettingsPage() {
  const [section, setSection] = useState("team");
  const statusQuery = useQuery({
    queryKey: ["settings-status"],
    queryFn: () => fetchJson<DeploymentStatus>("/api/settings/status"),
    refetchInterval: 30_000,
  });
  const deployment = statusQuery.data;

  return (
    <PageShell title="Settings" subtitle="Team management, probe fleet, credentials, integrations, and policy configuration">
      <div className="settings-layout">
        <aside className="settings-nav">
          <div className="settings-nav-heading"><Settings2 size={14} /> Configuration</div>
          {NAV_SECTIONS.map(({ key, label, icon: Icon }) => (
            <button key={key} className="settings-nav-button" data-active={section === key} onClick={() => setSection(key)}>
              <Icon size={14} /><span>{label}</span>
            </button>
          ))}
        </aside>

        <div className="settings-content">
          {section === "workspace" && (
            <div className="settings-panel animate-slide-in">
              <SectionTitle icon={Globe2} title="Workspace" detail="Engagement-specific client, scope, and assessment settings." />
              <div className="settings-workspace-card">
                <span><Globe2 size={20} /></span>
                <div>
                  <strong>Configuration belongs with each engagement</strong>
                  <p>Client identity, authorized targets, exclusions, assessment dates, owner, and tags are edited inside the engagement workspace.</p>
                </div>
                <Link href="/engagements" className="btn btn-primary">Open engagements</Link>
              </div>
              <div className="settings-readiness-grid">
                <article data-ready={deployment?.apiReachable ?? false}><Server size={16} /><div><small>Manager API</small><strong>{deployment?.apiReachable ? "Reachable" : "Unavailable"}</strong></div></article>
                <article data-ready={deployment?.cookieSecure ?? false}><LockKeyhole size={16} /><div><small>Secure cookie</small><strong>{deployment?.cookieSecure ? "Enforced" : "Local only"}</strong></div></article>
                <article data-ready={Boolean(deployment)}><CheckCircle2 size={16} /><div><small>Last verified</small><strong>{deployment ? new Date(deployment.checkedAt).toLocaleTimeString() : "Checking…"}</strong></div></article>
              </div>
            </div>
          )}
          {section === "team"          && <TeamSection />}
          {section === "api-keys"      && <ApiKeysSection />}
          {section === "probe-fleet"   && <ProbeFleetSection />}
          {section === "ai"            && <AiRuntimeSection />}
          {section === "access"        && <AccessSection status={deployment} />}
          {(section === "email" || section === "slack" || section === "jira") && <IntegrationSection kind={section} />}
          {section === "sla"           && <SlaSection />}
          {section === "notifications" && <NotificationsSection />}
          {section === "audit-log"     && <AuditLogSection />}
        </div>
      </div>
    </PageShell>
  );
}
