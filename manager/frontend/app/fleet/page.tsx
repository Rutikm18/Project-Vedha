"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  CheckCircle2, Clipboard, Clock3, Fingerprint, Laptop, Loader2,
  Network, RadioTower, RefreshCw, ShieldCheck,
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

// Map an enrollment state to a color + human word. Status is never conveyed by
// color alone — the word (and an aria-label) always accompany the dot.
function stateBadge(state: string): { color: string; label: string } {
  const s = (state || "").toLowerCase();
  if (s.includes("activ") || s.includes("approv") || s.includes("online")) {
    return { color: "var(--nominal-color)", label: state || "active" };
  }
  if (s.includes("expire") || s.includes("revok") || s.includes("denied")) {
    return { color: "var(--text-faint)", label: state || "expired" };
  }
  return { color: "var(--sev-medium-color)", label: state || "pending" };
}

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
    // eslint-disable-next-line react-hooks/set-state-in-effect -- mount fetch + 5s poll; setState happens after an await, not synchronously
    void load();
    const timer = window.setInterval(() => void load(), 5000);
    return () => window.clearInterval(timer);
  }, [load]);

  const request = data.requests.find((row) => row.request_id === selected) ?? null;
  const capabilities = useMemo(() => request?.capabilities ?? [], [request]);
  const managerUrl = data.manager_url || "https://manager.example.com";
  // Two ways to run the same installer: pipe-to-shell for a fresh host, and a
  // run-only command for operators who already downloaded install.sh (inspect-first).
  const installCommand = `curl --proto '=https' --tlsv1.2 -fsS https://downloads.vedha.example/probe/install.sh | sudo sh -s -- --manager ${managerUrl}`;
  const runCommand = `sudo sh install.sh --manager ${managerUrl}`;

  const copyCommand = (cmd: string) =>
    void navigator.clipboard.writeText(cmd).then(() => toast.success("Command copied"));

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
      <style>{STYLES}</style>
      <div className="flt-page">

        {/* ── Add a probe ── */}
        <section className="flt-card">
          <div className="flt-card-head">
            <span className="flt-head-icon"><ShieldCheck size={17} /></span>
            <div>
              <strong className="flt-head-title">Add a probe</strong>
              <div className="flt-head-sub">The command contains no PAT, admin secret, Site scope, or job ID.</div>
            </div>
          </div>
          <div className="flt-cmds">
            <div className="flt-cmd">
              <span className="flt-cmd-label">New host — download &amp; run in one command</span>
              <div className="flt-install">
                <code className="flt-code">{installCommand}</code>
                <button
                  className="flt-icon-btn"
                  aria-label="Copy install command for a new host"
                  onClick={() => copyCommand(installCommand)}
                >
                  <Clipboard size={15} />
                </button>
              </div>
            </div>
            <div className="flt-cmd">
              <span className="flt-cmd-label">Already downloaded install.sh — run it</span>
              <div className="flt-install">
                <code className="flt-code">{runCommand}</code>
                <button
                  className="flt-icon-btn"
                  aria-label="Copy run command for an already-downloaded installer"
                  onClick={() => copyCommand(runCommand)}
                >
                  <Clipboard size={15} />
                </button>
              </div>
            </div>
          </div>
          {!data.manager_url && (
            <p className="flt-warn">Set MANAGER_PUBLIC_URL on the frontend before copying this command in production.</p>
          )}
        </section>

        {/* ── Pending + Approve ── */}
        <div className="flt-grid">

          {/* Pending requests */}
          <section className="flt-card flt-card-flush">
            <header className="flt-list-head">
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <RadioTower size={15} color="var(--accent)" />
                <strong className="flt-head-title">Pending requests</strong>
                <span className="flt-count">{data.requests.length}</span>
              </div>
              <button className="flt-icon-btn" onClick={() => void load()} aria-label="Refresh pending probes">
                <RefreshCw size={14} />
              </button>
            </header>

            {loading ? (
              <div className="flt-empty"><Loader2 size={15} className="animate-spin" /> Loading pending requests…</div>
            ) : data.requests.length === 0 ? (
              <div className="flt-empty-block">
                <RadioTower size={22} color="var(--text-faint)" />
                <div className="flt-empty-title">No devices waiting</div>
                <div className="flt-empty-hint">Run the install command on a host — its key fingerprint will appear here for approval.</div>
              </div>
            ) : data.requests.map((row) => {
              const badge = stateBadge(row.state);
              const isSel = selected === row.request_id;
              return (
                <button
                  key={row.request_id}
                  className="flt-req"
                  data-sel={isSel}
                  onClick={() => { setSelected(row.request_id); setForm((v) => ({ ...v, probe_name: row.hostname_hint ?? v.probe_name })); }}
                >
                  <div className="flt-req-top">
                    <strong className="flt-req-name">{row.hostname_hint || "Unnamed device"}</strong>
                    <span
                      className="flt-state"
                      aria-label={`Enrollment state: ${badge.label}`}
                      style={{ color: badge.color }}
                    >
                      <span className="flt-dot" style={{ background: badge.color }} />
                      {badge.label}
                    </span>
                  </div>
                  <div className="flt-req-meta">
                    <span><Laptop size={11} /> {row.platform} / {row.architecture} · agent {row.agent_version}</span>
                    <span className="flt-mono"><Fingerprint size={11} /> {row.fingerprint.slice(0, 16)}…</span>
                    <span className="flt-mono"><Clock3 size={11} /> expires {new Date(row.expires_at).toLocaleString()}</span>
                  </div>
                </button>
              );
            })}
          </section>

          {/* Approve Site policy */}
          <section className="flt-card">
            <div className="flt-card-head">
              <span className="flt-head-icon"><Network size={16} /></span>
              <div>
                <strong className="flt-head-title">Approve Site policy</strong>
                <div className="flt-head-sub">Verify the code and fingerprint out of band before authorizing reachability.</div>
              </div>
            </div>

            {!request ? (
              <div className="flt-empty-block">
                <ShieldCheck size={22} color="var(--text-faint)" />
                <div className="flt-empty-title">Select a pending request</div>
                <div className="flt-empty-hint">Pick a device on the left to review and approve its Site policy.</div>
              </div>
            ) : (
              <form onSubmit={approve} className="flt-form">
                <label className="flt-field">
                  <span className="flt-label">Verification code</span>
                  <input className="flt-input flt-mono" required minLength={8} placeholder="ABCD-EFGH" value={form.user_code} onChange={(e) => setForm({ ...form, user_code: e.target.value })} />
                </label>
                <label className="flt-field">
                  <span className="flt-label">Probe name</span>
                  <input className="flt-input" required value={form.probe_name} onChange={(e) => setForm({ ...form, probe_name: e.target.value })} />
                </label>
                <label className="flt-field">
                  <span className="flt-label">Site name</span>
                  <input className="flt-input" required placeholder="Mumbai office" value={form.site_name} onChange={(e) => setForm({ ...form, site_name: e.target.value })} />
                </label>
                <label className="flt-field">
                  <span className="flt-label">Location</span>
                  <input className="flt-input" placeholder="IN-MH" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} />
                </label>
                <label className="flt-field flt-full">
                  <span className="flt-label">Authorized CIDRs</span>
                  <input className="flt-input flt-mono" required placeholder="10.20.0.0/16, 2001:db8:1::/64" value={form.authorized_cidrs} onChange={(e) => setForm({ ...form, authorized_cidrs: e.target.value })} />
                </label>
                <label className="flt-field flt-full">
                  <span className="flt-label">Excluded CIDRs</span>
                  <input className="flt-input flt-mono" placeholder="10.20.10.0/24" value={form.excluded_cidrs} onChange={(e) => setForm({ ...form, excluded_cidrs: e.target.value })} />
                </label>
                <div className="flt-caps">Capabilities approved: <strong>{capabilities.join(", ") || "none"}</strong></div>
                <button disabled={submitting} className="flt-submit" type="submit">
                  {submitting ? <Loader2 size={15} className="animate-spin" /> : <CheckCircle2 size={15} />} Approve and activate
                </button>
              </form>
            )}
          </section>
        </div>
      </div>
    </PageShell>
  );
}

const STYLES = `
.flt-page { padding: 18px; overflow-y: auto; height: 100%; display: grid; gap: 14px; }

.flt-card { border: 0.5px solid var(--border-subtle); border-radius: 12px; background: var(--bg-panel); padding: 16px; }
.flt-card-flush { padding: 0; overflow: hidden; }

.flt-card-head { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.flt-head-icon { width: 32px; height: 32px; border-radius: 9px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; background: var(--accent-ghost); border: 0.5px solid var(--border-accent); color: var(--accent); }
.flt-head-title { color: var(--text-primary); font-size: 13px; font-weight: 600; }
.flt-head-sub { color: var(--text-muted); font-size: 11px; margin-top: 2px; line-height: 1.4; }

.flt-cmds { display: grid; gap: 12px; }
.flt-cmd { display: grid; gap: 6px; }
.flt-cmd-label { color: var(--text-secondary); font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.flt-install { display: flex; gap: 8px; align-items: stretch; }
.flt-code { flex: 1; min-width: 0; padding: 11px; border-radius: 8px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); color: var(--accent); font: 11px var(--font-mono); overflow-x: auto; white-space: nowrap; }
.flt-warn { margin: 8px 0 0; color: var(--sev-medium-color); font-size: 10.5px; line-height: 1.4; }

.flt-icon-btn { width: 40px; height: 40px; flex-shrink: 0; display: inline-flex; align-items: center; justify-content: center; border-radius: 8px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); color: var(--text-secondary); cursor: pointer; transition: color var(--dur-fast) ease, border-color var(--dur-fast) ease, background var(--dur-fast) ease; }
.flt-icon-btn:hover { color: var(--accent); border-color: var(--border-accent); background: var(--accent-ghost); }

.flt-grid { display: grid; grid-template-columns: minmax(280px, .85fr) minmax(360px, 1.15fr); gap: 14px; align-items: start; }

.flt-list-head { padding: 13px 14px; display: flex; align-items: center; justify-content: space-between; border-bottom: 0.5px solid var(--border-subtle); }
.flt-count { font: 700 10px var(--font-mono); color: var(--text-muted); background: var(--bg-surface); border: 0.5px solid var(--border-subtle); border-radius: 5px; padding: 1px 6px; }

.flt-empty { padding: 20px; color: var(--text-muted); font-size: 12px; display: flex; align-items: center; gap: 8px; }
.flt-empty-block { padding: 30px 20px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 6px; }
.flt-empty-title { color: var(--text-secondary); font-size: 12.5px; font-weight: 600; }
.flt-empty-hint { color: var(--text-muted); font-size: 11px; line-height: 1.5; max-width: 300px; }

.flt-req { width: 100%; text-align: left; padding: 13px 14px; border: 0; border-bottom: 0.5px solid var(--border-subtle); border-left: 2px solid transparent; background: transparent; cursor: pointer; transition: background var(--dur-fast) ease, border-color var(--dur-fast) ease; }
.flt-req:hover { background: var(--bg-surface); }
.flt-req[data-sel="true"] { background: var(--accent-ghost); border-left-color: var(--accent); }
.flt-req-top { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.flt-req-name { color: var(--text-primary); font-size: 13px; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.flt-state { display: inline-flex; align-items: center; gap: 5px; font-size: 9.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; flex-shrink: 0; }
.flt-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.flt-req-meta { margin-top: 8px; display: grid; gap: 5px; color: var(--text-muted); font-size: 11px; }
.flt-req-meta span { display: inline-flex; align-items: center; gap: 5px; }
.flt-mono { font-family: var(--font-mono); }

.flt-form { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.flt-field { display: flex; flex-direction: column; gap: 6px; }
.flt-full { grid-column: 1 / -1; }
.flt-label { color: var(--text-secondary); font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.flt-input { width: 100%; min-height: 44px; padding: 10px 12px; border-radius: 8px; border: 0.5px solid var(--border-default); background: var(--bg-surface); color: var(--text-primary); font-size: 12.5px; outline: none; box-sizing: border-box; transition: border-color var(--dur-fast) ease, box-shadow var(--dur-fast) ease; }
.flt-input::placeholder { color: var(--text-faint); }
.flt-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-ghost); }
.flt-caps { grid-column: 1 / -1; color: var(--text-muted); font-size: 11px; }
.flt-caps strong { color: var(--text-secondary); font-weight: 600; }
.flt-submit { grid-column: 1 / -1; min-height: 44px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; border: none; border-radius: 10px; cursor: pointer; font-size: 13px; font-weight: 700; color: #fff; background: linear-gradient(180deg, var(--accent-hover, var(--accent)), var(--accent)); box-shadow: 0 3px 16px var(--accent-glow); transition: transform var(--dur-fast) ease, box-shadow var(--dur-fast) ease, filter var(--dur-fast) ease; }
.flt-submit:hover:not(:disabled) { transform: translateY(-1px); filter: brightness(1.05); }
.flt-submit:active:not(:disabled) { transform: translateY(0); }
.flt-submit:disabled { opacity: 0.4; cursor: not-allowed; box-shadow: none; }

@media (max-width: 900px) {
  .flt-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 560px) {
  .flt-form { grid-template-columns: minmax(0, 1fr); }
}
`;
