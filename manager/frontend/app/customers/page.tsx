"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  UserPlus, KeyRound, Power, Loader2, RefreshCw, Users, Clipboard, Globe, Eye, EyeOff, Link2,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { useToast } from "../../hooks/useToast";

interface Customer {
  id: string;
  email: string;
  is_active: boolean;
  engagement_id: string | null;
  engagement_name: string | null;
  portal_slug: string | null;
  created_at: string | null;
}
interface Engagement { id: string; name: string; status?: string }
interface ClientUserResp {
  id: string; email: string; is_active: boolean; engagement_id: string;
  portal_slug: string | null; temp_password?: string | null;
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error ?? body.detail ?? response.statusText);
  return body as T;
}

export default function CustomersPage() {
  const toast = useToast();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [engagements, setEngagements] = useState<Engagement[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [engId, setEngId] = useState("");
  const [email, setEmail] = useState("");
  // Shown ONCE after provision / reset — a temp password is never retrievable later.
  const [issued, setIssued] = useState<{ email: string; slug: string | null; password: string } | null>(null);
  // item 1: per-row password reveal. Backend stores the temp password encrypted at
  // rest and audits every reveal; null means the login predates encrypted storage.
  const [revealed, setRevealed] = useState<Record<string, string | null>>({});
  const [revealing, setRevealing] = useState<string | null>(null);

  const reveal = useCallback(async (c: Customer) => {
    if (c.id in revealed) {                        // second click hides it again
      setRevealed((r) => { const next = { ...r }; delete next[c.id]; return next; });
      return;
    }
    setRevealing(c.id);
    try {
      const r = await fetchJson<{ password: string | null }>(`/api/customers/${c.id}/reveal`);
      setRevealed((prev) => ({ ...prev, [c.id]: r.password }));
    } catch (e) {
      toast.error((e as Error).message);
    } finally {
      setRevealing(null);
    }
  }, [revealed, toast]);

  const load = useCallback(async () => {
    try {
      const [cs, es] = await Promise.all([
        fetchJson<Customer[]>("/api/customers"),
        fetchJson<{ engagements: Engagement[] }>("/api/engagements")
          .then((r) => r.engagements ?? [])
          .catch(() => [] as Engagement[]),
      ]);
      setCustomers(cs ?? []);
      setEngagements(es ?? []);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load customers");
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- mount fetch; setState happens after an await, not synchronously
    void load();
  }, [load]);

  const portalBase = typeof window !== "undefined" ? window.location.origin : "";

  // One customer login per engagement — only offer engagements without one yet.
  const takenEngagements = useMemo(
    () => new Set(customers.map((c) => c.engagement_id)),
    [customers],
  );
  const availableEngagements = useMemo(
    () => engagements.filter((e) => !takenEngagements.has(e.id)),
    [engagements, takenEngagements],
  );

  async function provision(event: React.FormEvent) {
    event.preventDefault();
    if (!engId || !email.trim()) return;
    setBusy(true);
    try {
      const r = await fetchJson<ClientUserResp>(
        `/api/engagements/${engId}/customer-access/client-user`,
        { method: "POST", body: JSON.stringify({ email: email.trim() }) },
      );
      setIssued({ email: r.email, slug: r.portal_slug, password: r.temp_password ?? "" });
      setEmail("");
      setEngId("");
      toast.success("Customer login created");
      await load();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Provisioning failed");
    } finally {
      setBusy(false);
    }
  }

  async function resetPassword(c: Customer) {
    if (!c.engagement_id) return;
    try {
      const r = await fetchJson<ClientUserResp>(
        `/api/engagements/${c.engagement_id}/customer-access/client-user`,
        { method: "PATCH", body: JSON.stringify({ reset_password: true }) },
      );
      setIssued({ email: c.email, slug: c.portal_slug, password: r.temp_password ?? "" });
      toast.success("Password reset");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Reset failed");
    }
  }

  async function toggleActive(c: Customer) {
    if (!c.engagement_id) return;
    try {
      await fetchJson(
        `/api/engagements/${c.engagement_id}/customer-access/client-user`,
        { method: "PATCH", body: JSON.stringify({ is_active: !c.is_active }) },
      );
      toast.success(c.is_active ? "Login disabled" : "Login enabled");
      await load();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Update failed");
    }
  }

  function copy(text: string) {
    navigator.clipboard?.writeText(text).then(
      () => toast.success("Copied"),
      () => toast.error("Copy failed"),
    );
  }

  // Builds a one-click access link. Credentials go in the URL fragment (#) which
  // is never sent to the server, never appears in server logs, and is erased by
  // the login page immediately before the API call fires.
  function buildAccessLink(userEmail: string, pw: string): string {
    const params = new URLSearchParams({ e: userEmail, p: pw });
    return `${portalBase}/portal/login#${params.toString()}`;
  }

  return (
    <PageShell title="Customers" subtitle="Provision customer portal logins and assign them an engagement">
      <style>{STYLES}</style>
      <div className="cus-page">

        {/* Add a customer */}
        <section className="cus-card">
          <div className="cus-head">
            <span className="cus-head-icon"><UserPlus size={17} /></span>
            <div>
              <strong className="cus-head-title">Add a customer</strong>
              <div className="cus-head-sub">Assign an engagement and issue a login. The password is shown once.</div>
            </div>
          </div>

          {issued && (
            <div className="cus-issued">
              <div className="cus-issued-row">
                <span className="cus-issued-label">Login</span>
                <code className="cus-mono">{issued.email}</code>
              </div>
              <div className="cus-issued-row">
                <span className="cus-issued-label">One-time password</span>
                <code className="cus-mono cus-pw">{issued.password || "(set by you)"}</code>
                {issued.password && (
                  <button className="cus-icon-btn" aria-label="Copy password" onClick={() => copy(issued.password)}><Clipboard size={14} /></button>
                )}
              </div>
              <div className="cus-issued-row">
                <span className="cus-issued-label">Portal</span>
                <code className="cus-mono">{portalBase}/portal/login</code>
                <button className="cus-icon-btn" aria-label="Copy portal URL" onClick={() => copy(`${portalBase}/portal/login`)}><Clipboard size={14} /></button>
              </div>
              {issued.password && (
                <div className="cus-issued-row">
                  <span className="cus-issued-label">Access link</span>
                  <code className="cus-mono cus-access-link">{buildAccessLink(issued.email, issued.password)}</code>
                  <button className="cus-icon-btn cus-icon-btn--accent" aria-label="Copy one-click access link"
                    onClick={() => copy(buildAccessLink(issued.email, issued.password))}>
                    <Link2 size={14} />
                  </button>
                </div>
              )}
              {issued.slug && (
                <div className="cus-issued-hint">
                  <Globe size={12} /> Handle <strong>{issued.slug}</strong> — becomes <code>{issued.slug}.portal.&lt;your-domain&gt;</code> once a domain is configured.
                </div>
              )}
              <button className="cus-dismiss" onClick={() => setIssued(null)}>Dismiss</button>
            </div>
          )}

          <form onSubmit={provision} className="cus-form">
            <label className="cus-field">
              <span className="cus-label">Engagement <span className="cus-star" aria-hidden="true">*</span></span>
              <select className="cus-input" required value={engId} onChange={(e) => setEngId(e.target.value)}>
                <option value="" disabled>Select an engagement…</option>
                {availableEngagements.map((e) => (
                  <option key={e.id} value={e.id}>{e.name}</option>
                ))}
              </select>
              {availableEngagements.length === 0 && !loading && (
                <span className="cus-hint">Every engagement already has a customer login. Create a new engagement first.</span>
              )}
            </label>
            <label className="cus-field">
              <span className="cus-label">Customer email <span className="cus-star" aria-hidden="true">*</span></span>
              <input className="cus-input" type="email" required placeholder="customer@company.com" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <button disabled={busy || !engId || !email.trim()} className="cus-submit" type="submit">
              {busy ? <Loader2 size={15} className="animate-spin" /> : <UserPlus size={15} />} Provision login
            </button>
          </form>
        </section>

        {/* Customer directory */}
        <section className="cus-card cus-card-flush">
          <header className="cus-list-head">
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <Users size={15} color="var(--accent)" />
              <strong className="cus-head-title">Customer logins</strong>
              <span className="cus-count">{customers.length}</span>
            </div>
            <button className="cus-icon-btn" onClick={() => void load()} aria-label="Refresh customers"><RefreshCw size={14} /></button>
          </header>

          {loading ? (
            <div className="cus-empty"><Loader2 size={15} className="animate-spin" /> Loading customers…</div>
          ) : customers.length === 0 ? (
            <div className="cus-empty-block">
              <Users size={22} color="var(--text-faint)" />
              <div className="cus-empty-title">No customers yet</div>
              <div className="cus-empty-hint">Provision a login above to give a customer access to their engagement portal.</div>
            </div>
          ) : (
            <div className="cus-table">
              <div className="cus-tr cus-th">
                <span>Customer</span><span>Engagement</span><span>Handle</span><span>Status</span><span>Actions</span>
              </div>
              {customers.map((c) => (
                <div key={c.id} className="cus-tr">
                  <span className="cus-mono cus-email">{c.email}</span>
                  <span className="cus-eng">{c.engagement_name ?? <em className="cus-faint">(engagement removed)</em>}</span>
                  <span className="cus-mono cus-slug">{c.portal_slug ?? "—"}</span>
                  <span>
                    <span className="cus-badge" data-on={c.is_active}>
                      <span className="cus-dot" /> {c.is_active ? "active" : "disabled"}
                    </span>
                  </span>
                  <span className="cus-actions">
                    <button className="cus-mini" onClick={() => void reveal(c)} disabled={revealing === c.id}
                      title={c.id in revealed ? "Hide password" : "Show password"}>
                      {revealing === c.id ? <Loader2 size={13} className="animate-spin" />
                        : (c.id in revealed ? <EyeOff size={13} /> : <Eye size={13} />)}
                      {c.id in revealed ? "Hide" : "Show"}
                    </button>
                    {c.id in revealed && (
                      <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                        <code className="cus-mono cus-pw">{revealed[c.id] ?? "(reset to reveal)"}</code>
                        {revealed[c.id] && (
                          <>
                            <button className="cus-icon-btn" aria-label="Copy password"
                              onClick={() => copy(revealed[c.id]!)}><Clipboard size={12} /></button>
                            <button className="cus-icon-btn cus-icon-btn--accent" aria-label="Copy one-click access link"
                              title="Copy access link (customer clicks → auto-login)"
                              onClick={() => copy(buildAccessLink(c.email, revealed[c.id]!))}>
                              <Link2 size={12} />
                            </button>
                          </>
                        )}
                      </span>
                    )}
                    <button className="cus-mini" onClick={() => void resetPassword(c)} disabled={!c.engagement_id} title="Reset password">
                      <KeyRound size={13} /> Reset
                    </button>
                    <button className="cus-mini" data-danger={c.is_active} onClick={() => void toggleActive(c)} disabled={!c.engagement_id} title={c.is_active ? "Disable login" : "Enable login"}>
                      <Power size={13} /> {c.is_active ? "Disable" : "Enable"}
                    </button>
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </PageShell>
  );
}

const STYLES = `
.cus-page { padding: 18px; overflow-y: auto; height: 100%; display: grid; gap: 14px; }
.cus-card { border: 0.5px solid var(--border-subtle); border-radius: 12px; background: var(--bg-panel); padding: 16px; }
.cus-card-flush { padding: 0; overflow: hidden; }
.cus-head { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.cus-head-icon { width: 32px; height: 32px; border-radius: 9px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; background: var(--accent-ghost); border: 0.5px solid var(--border-accent); color: var(--accent); }
.cus-head-title { color: var(--text-primary); font-size: 13px; font-weight: 600; }
.cus-head-sub { color: var(--text-muted); font-size: 11px; margin-top: 2px; line-height: 1.4; }

.cus-form { display: grid; grid-template-columns: 1fr 1fr auto; gap: 12px; align-items: end; }
.cus-field { display: flex; flex-direction: column; gap: 6px; }
.cus-label { color: var(--text-secondary); font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.cus-star { color: var(--sev-high-color, #e5484d); font-weight: 700; }
.cus-input { width: 100%; min-height: 44px; padding: 10px 12px; border-radius: 8px; border: 0.5px solid var(--border-default); background: var(--bg-surface); color: var(--text-primary); font-size: 12.5px; outline: none; box-sizing: border-box; transition: border-color var(--dur-fast) ease, box-shadow var(--dur-fast) ease; }
.cus-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-ghost); }
.cus-hint { color: var(--text-muted); font-size: 10px; margin-top: 2px; line-height: 1.4; }
.cus-submit { min-height: 44px; padding: 0 16px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; border: none; border-radius: 10px; cursor: pointer; font-size: 13px; font-weight: 700; color: #fff; background: linear-gradient(180deg, var(--accent-hover, var(--accent)), var(--accent)); box-shadow: 0 3px 16px var(--accent-glow); transition: transform var(--dur-fast) ease, filter var(--dur-fast) ease; white-space: nowrap; }
.cus-submit:hover:not(:disabled) { transform: translateY(-1px); filter: brightness(1.05); }
.cus-submit:disabled { opacity: 0.4; cursor: not-allowed; box-shadow: none; }

.cus-issued { margin-bottom: 14px; padding: 12px 14px; border-radius: 10px; background: var(--accent-ghost); border: 0.5px solid var(--border-accent); display: grid; gap: 8px; }
.cus-issued-row { display: flex; align-items: center; gap: 10px; }
.cus-issued-label { color: var(--text-secondary); font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; width: 130px; flex-shrink: 0; }
.cus-pw { color: var(--accent); font-weight: 700; }
.cus-issued-hint { color: var(--text-muted); font-size: 11px; display: flex; align-items: center; gap: 6px; line-height: 1.5; }
.cus-issued-hint code { font-family: var(--font-mono); color: var(--text-secondary); }
.cus-dismiss { justify-self: start; margin-top: 2px; background: transparent; border: 0.5px solid var(--border-default); color: var(--text-secondary); border-radius: 7px; padding: 5px 10px; font-size: 11px; cursor: pointer; }

.cus-mono { font-family: var(--font-mono); }
.cus-icon-btn { width: 30px; height: 30px; flex-shrink: 0; display: inline-flex; align-items: center; justify-content: center; border-radius: 7px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); color: var(--text-secondary); cursor: pointer; }
.cus-icon-btn:hover { color: var(--accent); border-color: var(--border-accent); }
.cus-icon-btn--accent { color: var(--accent); border-color: var(--border-accent); background: var(--accent-ghost); }
.cus-icon-btn--accent:hover { filter: brightness(1.1); }
.cus-access-link { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 240px; font-size: 10px; color: var(--accent); }

.cus-list-head { padding: 13px 14px; display: flex; align-items: center; justify-content: space-between; border-bottom: 0.5px solid var(--border-subtle); }
.cus-count { font: 700 10px var(--font-mono); color: var(--text-muted); background: var(--bg-surface); border: 0.5px solid var(--border-subtle); border-radius: 5px; padding: 1px 6px; }
.cus-empty { padding: 20px; color: var(--text-muted); font-size: 12px; display: flex; align-items: center; gap: 8px; }
.cus-empty-block { padding: 30px 20px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 6px; }
.cus-empty-title { color: var(--text-secondary); font-size: 12.5px; font-weight: 600; }
.cus-empty-hint { color: var(--text-muted); font-size: 11px; line-height: 1.5; max-width: 320px; }

.cus-table { display: grid; }
.cus-tr { display: grid; grid-template-columns: 1.6fr 1.2fr 1fr 0.8fr 1.4fr; gap: 10px; align-items: center; padding: 11px 14px; border-bottom: 0.5px solid var(--border-subtle); font-size: 12px; color: var(--text-primary); }
.cus-th { color: var(--text-muted); font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.cus-email { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cus-eng { color: var(--text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.cus-slug { color: var(--accent); }
.cus-faint { color: var(--text-faint); }
.cus-badge { display: inline-flex; align-items: center; gap: 5px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; color: var(--text-faint); }
.cus-badge[data-on="true"] { color: var(--nominal-color); }
.cus-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.cus-actions { display: flex; gap: 6px; flex-wrap: wrap; }
.cus-mini { display: inline-flex; align-items: center; gap: 5px; padding: 5px 9px; border-radius: 7px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); color: var(--text-secondary); font-size: 11px; cursor: pointer; transition: color var(--dur-fast) ease, border-color var(--dur-fast) ease; }
.cus-mini:hover:not(:disabled) { color: var(--accent); border-color: var(--border-accent); }
.cus-mini[data-danger="true"]:hover:not(:disabled) { color: var(--sev-high-color, #e5484d); border-color: var(--sev-high-color, #e5484d); }
.cus-mini:disabled { opacity: 0.4; cursor: not-allowed; }

@media (max-width: 820px) {
  .cus-form { grid-template-columns: 1fr; }
  .cus-tr { grid-template-columns: 1fr 1fr; gap: 6px; }
  .cus-th { display: none; }
}
`;
