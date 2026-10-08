"use client";

/**
 * Settings → Account security: the signed-in user's own two-step sign-in.
 * Turn it on (scan a QR code, confirm a code, keep the recovery codes), replace
 * the recovery codes, or turn it off (password and a code).
 *
 * Calls go through plain fetch, not the shared fetchJson: that helper treats a
 * refused request as an expired session and signs the user out, which a mistyped
 * code must never do.
 */
import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, KeyRound, Loader2, ShieldCheck, ShieldOff, Smartphone, TriangleAlert } from "lucide-react";
import { RecoveryCodesBlock, SetupKeyBlock, qrSvg, type SetupKey } from "../auth/MfaStep";

export interface MfaStatus {
  enabled: boolean;
  enabled_at: string | null;
  recovery_codes_left: number;
  required_by_policy: boolean;
}

type Call = { ok: boolean; status: number; data: Record<string, unknown> };

async function call(base: string, action: string, body?: object): Promise<Call> {
  try {
    const res = await fetch(`${base}/${action}`, {
      method: body ? "POST" : "GET",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await res.json().catch(() => ({})) as Record<string, unknown>;
    return { ok: res.ok, status: res.status, data };
  } catch {
    return { ok: false, status: 0, data: { error: "Can't reach the server. Check your connection and try again." } };
  }
}

const message = (r: Call, fallback: string) =>
  r.status === 429 ? "Too many attempts. Wait a minute and try again."
    : typeof r.data.error === "string" && r.data.error ? r.data.error : fallback;

/** How many recovery codes are left, worded so a low count stands out. */
export function recoveryCodesNote(left: number): { text: string; low: boolean } {
  if (left === 0) return { text: "No recovery codes left — create new ones now", low: true };
  if (left <= 2) return { text: `Only ${left} recovery code${left === 1 ? "" : "s"} left — create new ones`, low: true };
  return { text: `${left} recovery codes left`, low: false };
}

type View = "idle" | "setup" | "codes" | "regenerate" | "disable";

export function AccountSecuritySection({ surface = "manager" }: { surface?: "manager" | "portal" }) {
  const base = surface === "portal" ? "/api/portal/mfa" : "/api/auth/mfa";
  const statusQuery = useQuery({
    queryKey: ["mfa-status", base],
    queryFn: async () => {
      const r = await call(base, "status");
      if (!r.ok) throw new Error(message(r, "Two-step sign-in status could not be loaded."));
      return r.data as unknown as MfaStatus;
    },
    retry: false,
  });
  const status = statusQuery.data ?? null;
  const loadError = statusQuery.error ? statusQuery.error.message : null;
  const load = () => statusQuery.refetch();
  const [view, setView] = useState<View>("idle");
  const [setup, setSetup] = useState<SetupKey | null>(null);
  const [codes, setCodes] = useState<string[] | null>(null);
  // Why codes are on screen: MFA was just turned on, or the codes were replaced.
  const [codesFor, setCodesFor] = useState<"enabled" | "replaced">("enabled");
  const [saved, setSaved] = useState(false);
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const reset = () => { setView("idle"); setCode(""); setPassword(""); setError(null); setSetup(null); };

  const startSetup = async () => {
    setBusy(true); setError(null); setNotice(null);
    const r = await call(base, "setup", {});
    if (r.ok && typeof r.data.otpauth_uri === "string" && typeof r.data.secret === "string") {
      const svg = await qrSvg(r.data.otpauth_uri);
      setSetup({ secret: r.data.secret, uri: r.data.otpauth_uri, account: String(r.data.account ?? ""), svg });
      setView("setup");
    } else setError(message(r, "Setup could not start."));
    setBusy(false);
  };

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!code.trim()) { setError("Enter the 6-digit code from your app."); return; }
    setBusy(true); setError(null);
    if (view === "setup" || view === "regenerate") {
      const r = await call(base, view === "setup" ? "enable" : "recovery-codes", { code: code.trim() });
      if (r.ok && Array.isArray(r.data.recovery_codes)) {
        setCodes(r.data.recovery_codes as string[]);
        setCodesFor(view === "setup" ? "enabled" : "replaced");
        setSaved(false);
        setView("codes");
        setCode("");
        await load();
      } else setError(message(r, "That code does not match."));
    } else if (view === "disable") {
      const r = await call(base, "disable", { password, code: code.trim() });
      if (r.ok) { reset(); setNotice("Two-step sign-in is off."); await load(); }
      else setError(message(r, "Password or code is incorrect."));
    }
    setBusy(false);
  };

  const heading = (
    <header className="settings-content-heading">
      <span><Smartphone size={18} /></span>
      <div>
        <h2>Account security</h2>
        <p>Two-step sign-in for your own account: a code from an authenticator app after your password.</p>
      </div>
    </header>
  );

  if (!status) {
    return (
      <div className="settings-panel animate-slide-in">
        {heading}
        <p className="settings-loading-msg">{loadError ?? "Loading…"}</p>
      </div>
    );
  }

  const codesNote = recoveryCodesNote(status.recovery_codes_left);
  const since = status.enabled_at ? new Intl.DateTimeFormat("en", { dateStyle: "medium" }).format(new Date(status.enabled_at)) : null;

  return (
    <div className="settings-panel animate-slide-in">
      {heading}

      <div className="mfa-status-card" data-on={status.enabled}>
        <span className="mfa-status-icon">{status.enabled ? <ShieldCheck size={18} /> : <ShieldOff size={18} />}</span>
        <div>
          <strong>{status.enabled ? "Two-step sign-in is on" : "Two-step sign-in is off"}</strong>
          <small>
            {status.enabled
              ? [since ? `Since ${since}` : null, codesNote.text].filter(Boolean).join(" · ")
              : status.required_by_policy
                ? "Your organisation requires it — you will be asked to set it up at your next sign-in."
                : "Anyone with your password can sign in. Turn it on to require a code from your phone as well."}
          </small>
        </div>
        {status.required_by_policy && <span className="badge badge-info">Required</span>}
      </div>

      {status.enabled && codesNote.low && view === "idle" && (
        <div className="settings-warning"><TriangleAlert size={14} /> {codesNote.text}. Each recovery code works once.</div>
      )}
      {notice && <p className="settings-feedback-msg"><CheckCircle2 size={12} /> {notice}</p>}
      {error && <div className="settings-warning" role="alert"><TriangleAlert size={14} /> {error}</div>}

      {view === "codes" && codes && (
        <div className="mfa-step mfa-panel">
          <h3><KeyRound size={15} /> Save your recovery codes</h3>
          <p className="policy-note">If you lose your phone, each of these signs you in once. This is the only time they are shown; any earlier codes no longer work.</p>
          <RecoveryCodesBlock codes={codes} account={setup?.account} saved={saved} onSaved={setSaved} />
          <button type="button" className="btn btn-primary" disabled={!saved}
            onClick={() => { setCodes(null); reset(); setNotice(codesFor === "enabled" ? "Two-step sign-in is on." : "New recovery codes are active."); }}>
            Done
          </button>
        </div>
      )}

      {view === "idle" && (
        <div className="mfa-actions">
          {!status.enabled ? (
            <button type="button" className="btn btn-primary" onClick={() => void startSetup()} disabled={busy}>
              {busy ? <Loader2 size={13} className="animate-spin" /> : <Smartphone size={13} />} Set up authenticator app
            </button>
          ) : (
            <>
              <button type="button" className="btn btn-secondary" onClick={() => { setView("regenerate"); setNotice(null); }}>
                <KeyRound size={13} /> New recovery codes
              </button>
              <button type="button" className="btn btn-danger-ghost" disabled={status.required_by_policy}
                title={status.required_by_policy ? "Your organisation requires two-step sign-in" : undefined}
                onClick={() => { setView("disable"); setNotice(null); }}>
                <ShieldOff size={13} /> Turn off
              </button>
              {status.required_by_policy && <span className="policy-muted">Required by your organisation, so it can&apos;t be turned off.</span>}
            </>
          )}
        </div>
      )}

      {(view === "setup" || view === "regenerate" || view === "disable") && (
        <form className="mfa-panel" onSubmit={(e) => void submit(e)}>
          {view === "setup" && setup && <div className="mfa-setup"><SetupKeyBlock setup={setup} /></div>}
          {view === "regenerate" && <p className="policy-note">Enter a code from your app. The new codes replace all the old ones.</p>}
          {view === "disable" && (
            <>
              <p className="policy-note">Confirm with your password and a code from your app (or a recovery code).</p>
              <label className="mfa-field">
                <span>Password</span>
                <input type="password" autoComplete="current-password" value={password}
                  onChange={(e) => setPassword(e.target.value)} className="input-base" required />
              </label>
            </>
          )}
          <label className="mfa-field">
            <span>{view === "disable" ? "Code" : "6-digit code"}</span>
            <input value={code} onChange={(e) => setCode(e.target.value)} className="input-base mfa-code-input"
              autoComplete="one-time-code" inputMode={view === "disable" ? "text" : "numeric"}
              placeholder={view === "disable" ? "123 456 or XXXXX-XXXXX" : "123 456"} maxLength={16} autoFocus />
          </label>
          <div className="mfa-actions">
            <button type="submit" className={view === "disable" ? "btn btn-danger" : "btn btn-primary"} disabled={busy}>
              {busy && <Loader2 size={13} className="animate-spin" />}
              {view === "setup" ? "Turn on" : view === "regenerate" ? "Create new codes" : "Turn off two-step sign-in"}
            </button>
            <button type="button" className="btn btn-secondary" onClick={reset} disabled={busy}>Cancel</button>
          </div>
        </form>
      )}
    </div>
  );
}
