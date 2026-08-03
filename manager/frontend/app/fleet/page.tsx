"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  CheckCircle2, Clipboard, Clock3, Fingerprint, Laptop, Loader2,
  Network, RefreshCw, ShieldCheck,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { useToast } from "../../hooks/useToast";

interface EnrollmentRequest {
  request_id: string;
  state: string;
  hostname_hint: string | null;
  platform: string;
  architecture: string;
  agent_version: string;
  capabilities: string[];
  fingerprint: string;
  expires_at: string;
}

interface FleetResponse {
  requests: EnrollmentRequest[];
  manager_url: string;
}

const inputStyle = {
  width: "100%", padding: "9px 10px", borderRadius: 7,
  border: "1px solid var(--border-default)", background: "var(--bg-surface)",
  color: "var(--text-primary)", fontSize: 12,
} as const;

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error ?? response.statusText);
  return body as T;
}

export default function FleetPage() {
  const toast = useToast();
  const [data, setData] = useState<FleetResponse>({ requests: [], manager_url: "" });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [selected, setSelected] = useState<string | null>(null);
  const [form, setForm] = useState({
    user_code: "", probe_name: "", site_name: "", location: "",
    authorized_cidrs: "", excluded_cidrs: "",
  });

  const load = useCallback(async () => {
    try {
      const next = await fetchJson<FleetResponse>("/api/fleet/enrollment");
      setData(next);
      setSelected((current) => current && next.requests.some((row) => row.request_id === current)
        ? current : next.requests[0]?.request_id ?? null);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Could not load Fleet");
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    void load();
    const timer = window.setInterval(() => void load(), 5000);
    return () => window.clearInterval(timer);
  }, [load]);

  const request = data.requests.find((row) => row.request_id === selected) ?? null;
  const capabilities = useMemo(() => request?.capabilities ?? [], [request]);
  const managerUrl = data.manager_url || "https://manager.example.com";
  const installCommand = `curl --proto '=https' --tlsv1.2 -fsS https://downloads.vedha.example/probe/install.sh | sudo sh -s -- --manager ${managerUrl}`;

  async function approve(event: React.FormEvent) {
    event.preventDefault();
    if (!request) return;
    setSubmitting(true);
    try {
      await fetchJson("/api/fleet/enrollment", {
        method: "POST",
        body: JSON.stringify({
          user_code: form.user_code.trim().toUpperCase(),
          probe_name: form.probe_name.trim() || request.hostname_hint || `probe-${request.request_id.slice(0, 8)}`,
          site_name: form.site_name.trim(),
          location: form.location.trim() || null,
          authorized_cidrs: form.authorized_cidrs.split(",").map((v) => v.trim()).filter(Boolean),
          excluded_cidrs: form.excluded_cidrs.split(",").map((v) => v.trim()).filter(Boolean),
          approved_capabilities: capabilities,
          max_targets: 4096,
          max_job_seconds: 7200,
          max_rate_pps: 1000,
          update_channel: "stable",
        }),
      });
      toast.success("Probe approved; waiting for key-bound activation");
      setForm({ user_code: "", probe_name: "", site_name: "", location: "", authorized_cidrs: "", excluded_cidrs: "" });
      await load();
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Approval failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <PageShell title="Fleet" subtitle="Enroll and govern probe devices">
      <div style={{ padding: 18, overflowY: "auto", height: "100%", display: "grid", gap: 14 }}>
        <section style={{ padding: 16, border: "1px solid var(--border-subtle)", borderRadius: 12, background: "var(--bg-panel)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 9, marginBottom: 10 }}>
            <ShieldCheck size={18} color="var(--accent)" />
            <div><strong style={{ color: "var(--text-primary)" }}>Add a probe</strong><div style={{ color: "var(--text-muted)", fontSize: 11 }}>The command contains no PAT, admin secret, Site scope, or job ID.</div></div>
          </div>
          <div style={{ display: "flex", gap: 8, alignItems: "stretch" }}>
            <code style={{ flex: 1, padding: 11, borderRadius: 8, background: "var(--bg-surface)", color: "var(--accent)", fontSize: 11, overflowX: "auto", whiteSpace: "nowrap" }}>{installCommand}</code>
            <button className="btn-secondary" aria-label="Copy install command" onClick={() => void navigator.clipboard.writeText(installCommand).then(() => toast.success("Install command copied"))}><Clipboard size={14} /></button>
          </div>
          {!data.manager_url && <p style={{ margin: "8px 0 0", color: "var(--sev-medium-color)", fontSize: 10 }}>Set MANAGER_PUBLIC_URL on the frontend before copying this command in production.</p>}
        </section>

        <div style={{ display: "grid", gridTemplateColumns: "minmax(280px,.8fr) minmax(380px,1.2fr)", gap: 14, alignItems: "start" }}>
          <section style={{ border: "1px solid var(--border-subtle)", borderRadius: 12, background: "var(--bg-panel)", overflow: "hidden" }}>
            <header style={{ padding: "12px 14px", display: "flex", justifyContent: "space-between", borderBottom: "1px solid var(--border-subtle)" }}><strong style={{ color: "var(--text-primary)" }}>Pending requests</strong><button onClick={() => void load()} className="btn-secondary" aria-label="Refresh pending probes"><RefreshCw size={13} /></button></header>
            {loading ? <div style={{ padding: 22, color: "var(--text-muted)" }}><Loader2 size={15} className="animate-spin" /> Loading…</div> : data.requests.length === 0 ? <div style={{ padding: 22, color: "var(--text-muted)", fontSize: 12 }}>Run the install command; a key fingerprint will appear here.</div> : data.requests.map((row) => (
              <button key={row.request_id} onClick={() => { setSelected(row.request_id); setForm((v) => ({ ...v, probe_name: row.hostname_hint ?? v.probe_name })); }} style={{ width: "100%", textAlign: "left", padding: 13, border: 0, borderBottom: "1px solid var(--border-subtle)", background: selected === row.request_id ? "var(--accent-ghost)" : "transparent", cursor: "pointer" }}>
                <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}><strong style={{ color: "var(--text-primary)", fontSize: 12 }}>{row.hostname_hint || "Unnamed device"}</strong><span style={{ color: "var(--sev-medium-color)", fontSize: 9, textTransform: "uppercase" }}>{row.state}</span></div>
                <div style={{ marginTop: 7, display: "grid", gap: 4, color: "var(--text-muted)", fontSize: 10 }}><span><Laptop size={10} /> {row.platform} / {row.architecture} · agent {row.agent_version}</span><span><Fingerprint size={10} /> {row.fingerprint.slice(0, 16)}…</span><span><Clock3 size={10} /> expires {new Date(row.expires_at).toLocaleString()}</span></div>
              </button>
            ))}
          </section>

          <section style={{ padding: 16, border: "1px solid var(--border-subtle)", borderRadius: 12, background: "var(--bg-panel)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}><Network size={17} color="var(--accent)" /><div><strong style={{ color: "var(--text-primary)" }}>Approve Site policy</strong><div style={{ color: "var(--text-muted)", fontSize: 10 }}>Verify the code and fingerprint out of band before authorizing reachability.</div></div></div>
            {!request ? <p style={{ color: "var(--text-muted)", fontSize: 12 }}>Select a pending request.</p> : <form onSubmit={approve} style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 11 }}>
              <label style={{ color: "var(--text-secondary)", fontSize: 10 }}>Verification code<input style={inputStyle} required minLength={8} placeholder="ABCD-EFGH" value={form.user_code} onChange={(e) => setForm({ ...form, user_code: e.target.value })} /></label>
              <label style={{ color: "var(--text-secondary)", fontSize: 10 }}>Probe name<input style={inputStyle} required value={form.probe_name} onChange={(e) => setForm({ ...form, probe_name: e.target.value })} /></label>
              <label style={{ color: "var(--text-secondary)", fontSize: 10 }}>Site name<input style={inputStyle} required placeholder="Mumbai office" value={form.site_name} onChange={(e) => setForm({ ...form, site_name: e.target.value })} /></label>
              <label style={{ color: "var(--text-secondary)", fontSize: 10 }}>Location<input style={inputStyle} placeholder="IN-MH" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} /></label>
              <label style={{ gridColumn: "1 / -1", color: "var(--text-secondary)", fontSize: 10 }}>Authorized CIDRs<input style={inputStyle} required placeholder="10.20.0.0/16, 2001:db8:1::/64" value={form.authorized_cidrs} onChange={(e) => setForm({ ...form, authorized_cidrs: e.target.value })} /></label>
              <label style={{ gridColumn: "1 / -1", color: "var(--text-secondary)", fontSize: 10 }}>Excluded CIDRs<input style={inputStyle} placeholder="10.20.10.0/24" value={form.excluded_cidrs} onChange={(e) => setForm({ ...form, excluded_cidrs: e.target.value })} /></label>
              <div style={{ gridColumn: "1 / -1", color: "var(--text-muted)", fontSize: 10 }}>Capabilities approved: {capabilities.join(", ") || "none"}</div>
              <button disabled={submitting} className="btn-primary" style={{ gridColumn: "1 / -1", justifyContent: "center" }}>{submitting ? <Loader2 size={14} className="animate-spin" /> : <CheckCircle2 size={14} />} Approve and activate</button>
            </form>}
          </section>
        </div>
      </div>
    </PageShell>
  );
}
