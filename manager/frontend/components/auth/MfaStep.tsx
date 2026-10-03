"use client";

/**
 * The code step of sign-in, shared by the operator and portal login pages.
 *
 *   verify  — the account has two-step sign-in: enter the app code, or a
 *             recovery code if the phone is lost.
 *   enroll  — the organisation requires it and the account has none yet: scan a
 *             QR code (or type the key), confirm a code, keep the recovery codes.
 *
 * Talks only to the page's own login route (`endpoint`), which keeps the
 * challenge token in an httpOnly cookie (lib/mfa-login.ts).
 */
import React, { useCallback, useEffect, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, Check, Copy, Download, KeyRound, Loader2, LockKeyhole, Smartphone } from "lucide-react";
import QRCode from "qrcode";
import { copyText } from "../../lib/clipboard";

export type MfaMode = "verify" | "enroll";

interface Props {
  mode: MfaMode;
  endpoint: string;
  /** Signed in: leave the login page. */
  onDone: () => void;
  /** Back to email and password (the challenge expired, or the user chose to). */
  onRestart: (message?: string) => void;
  /** Smaller headings for a narrow card (the portal sign-in). */
  compact?: boolean;
}

type StepResponse = {
  ok?: boolean; error?: string; code?: string; retryAfter?: number;
  secret?: string; otpauth_uri?: string; account?: string; recovery_codes?: string[];
};

async function post(endpoint: string, body: object): Promise<{ status: number; data: StepResponse }> {
  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify(body),
  });
  return { status: res.status, data: await res.json().catch(() => ({})) as StepResponse };
}

/** Groups a base32 key in fours so it can be typed without losing place. */
export function groupKey(secret: string): string {
  return secret.replace(/(.{4})/g, "$1 ").trim();
}

export interface SetupKey { secret: string; uri: string; account: string; svg: string }

/** The QR code is drawn here, so the key never goes to a third-party QR service. */
export function qrSvg(uri: string): Promise<string> {
  return QRCode.toString(uri, { type: "svg", margin: 1, errorCorrectionLevel: "M" });
}

export function recoveryCodesText(codes: string[], account?: string, today = new Date()): string {
  return [
    "Vedha recovery codes",
    ...(account ? [`Account: ${account}`] : []),
    `Created: ${today.toISOString().slice(0, 10)}`,
    "Each code works once. Keep them somewhere safe and offline.",
    "",
    ...codes,
    "",
  ].join("\n");
}

/** QR code plus the typed-in fallback key. */
export function SetupKeyBlock({ setup }: { setup: SetupKey }) {
  return (
    <>
      <div className="mfa-qr" role="img" aria-label="QR code to add Vedha to your authenticator app"
        dangerouslySetInnerHTML={{ __html: setup.svg }} />
      <div className="mfa-setup-text">
        <strong>1. Scan with your app</strong>
        <small>Can&apos;t scan? Add an account manually with this key (time-based):</small>
        <code className="mfa-key">{groupKey(setup.secret)}</code>
        <strong>2. Enter the code it shows</strong>
      </div>
    </>
  );
}

/** One-time display of recovery codes, with copy, download and a "saved" check. */
export function RecoveryCodesBlock({ codes, account, saved, onSaved }: {
  codes: string[]; account?: string; saved: boolean; onSaved: (saved: boolean) => void;
}) {
  const [copied, setCopied] = useState(false);
  const copy = async () => {
    // If the clipboard is blocked the codes stay on screen to write down.
    if (await copyText(codes.join("\n"))) { setCopied(true); onSaved(true); }
  };
  const download = () => {
    const url = URL.createObjectURL(new Blob([recoveryCodesText(codes, account)], { type: "text/plain" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = "vedha-recovery-codes.txt";
    a.click();
    URL.revokeObjectURL(url);
    onSaved(true);
  };
  return (
    <>
      <ol className="mfa-recovery-list" aria-label="Recovery codes">
        {codes.map((c) => <li key={c}><code>{c}</code></li>)}
      </ol>
      <div className="mfa-row">
        <button type="button" className="mfa-secondary" onClick={() => void copy()}>
          {copied ? <><Check size={15} /> Copied</> : <><Copy size={15} /> Copy</>}
        </button>
        <button type="button" className="mfa-secondary" onClick={download}>
          <Download size={15} /> Download .txt
        </button>
      </div>
      <label className="mfa-confirm">
        <input type="checkbox" checked={saved} onChange={(e) => onSaved(e.target.checked)} />
        <span>I have stored these codes somewhere safe</span>
      </label>
    </>
  );
}

export function MfaStep({ mode, endpoint, onDone, onRestart, compact = false }: Props) {
  const rootClass = compact ? "mfa-step compact" : "mfa-step";
  const [code, setCode] = useState("");
  const [useRecovery, setUseRecovery] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [setup, setSetup] = useState<SetupKey | null>(null);
  const [recoveryCodes, setRecoveryCodes] = useState<string[] | null>(null);
  const [saved, setSaved] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  // Read by `fail` without making it (and the enrolment effect) depend on the toggle.
  const recoveryRef = useRef(false);
  useEffect(() => { recoveryRef.current = useRecovery; }, [useRecovery]);

  const fail = useCallback((data: StepResponse) => {
    switch (data.code) {
      case "mfa_expired":
        onRestart("That sign-in took too long. Enter your password again to get a new code step.");
        return;
      case "rate_limited":
        setError(`Too many attempts. Try again in ${data.retryAfter ?? 60} seconds.`);
        return;
      case "invalid_code":
        setError(mode === "enroll"
          ? "That code does not match. Check that your phone's clock is set automatically, then try the newest code."
          : recoveryRef.current
            ? "That recovery code was not accepted. Each one works only once — check it, or try another."
            : "That code was not accepted. Codes change every 30 seconds — try the newest one. After five wrong codes you will need to sign in again.");
        return;
      case "backend_unavailable":
        setError("Sign-in is temporarily unavailable. Please try again shortly.");
        return;
      default:
        setError(data.error || "The code could not be checked.");
    }
  }, [mode, onRestart]);

  // Enrolment: fetch a new secret once and draw its QR code locally (the key
  // never leaves this page for a third-party QR service).
  useEffect(() => {
    if (mode !== "enroll") return;
    let active = true;
    (async () => {
      setBusy(true);
      try {
        const { data } = await post(endpoint, { step: "enroll_setup" });
        if (!active) return;
        if (!data.secret || !data.otpauth_uri) { fail(data); return; }
        const svg = await qrSvg(data.otpauth_uri);
        if (active) setSetup({ secret: data.secret, uri: data.otpauth_uri, account: data.account ?? "", svg });
      } catch {
        if (active) setError("Vedha could not reach the authentication service. Check your connection and retry.");
      } finally {
        if (active) setBusy(false);
      }
    })();
    return () => { active = false; };
  }, [endpoint, fail, mode]);

  useEffect(() => { inputRef.current?.focus(); }, [useRecovery, setup]);

  const submit = useCallback(async (event: React.FormEvent) => {
    event.preventDefault();
    const value = code.trim();
    if (!value) { setError(useRecovery ? "Enter one of your recovery codes." : "Enter the 6-digit code from your app."); return; }
    setBusy(true);
    setError(null);
    try {
      const { data } = await post(endpoint, { step: mode === "verify" ? "verify" : "enroll_enable", code: value });
      if (!data.ok) { fail(data); setCode(""); return; }
      if (data.recovery_codes?.length) setRecoveryCodes(data.recovery_codes);
      else onDone();
    } catch {
      setError("Vedha could not reach the authentication service. Check your connection and retry.");
    } finally {
      setBusy(false);
    }
  }, [code, endpoint, fail, mode, onDone, useRecovery]);

  // ── recovery codes, shown once after enrolment ─────────────────────────────
  if (recoveryCodes) {
    return (
      <div className={rootClass}>
        <div className="login-form-heading">
          <span className="login-form-icon"><KeyRound size={22} /></span>
          <h2>Save your recovery codes</h2>
          <p>If you lose your phone, each of these signs you in once. This is the only time they are shown.</p>
        </div>
        <RecoveryCodesBlock codes={recoveryCodes} account={setup?.account} saved={saved} onSaved={setSaved} />
        <button className="login-submit" type="button" disabled={!saved} onClick={onDone}>
          Continue to Vedha <ArrowRight size={17} />
        </button>
      </div>
    );
  }

  const enrolling = mode === "enroll";
  return (
    <div className={rootClass}>
      <div className="login-form-heading">
        <span className="login-form-icon"><Smartphone size={22} /></span>
        <h2>{enrolling ? "Set up two-step sign-in" : "Enter your sign-in code"}</h2>
        <p>
          {enrolling
            ? "Your organisation requires a code from an authenticator app (Google Authenticator, Microsoft Authenticator, 1Password and similar)."
            : useRecovery
              ? "Enter one of the recovery codes you saved when you set up two-step sign-in. Each works once."
              : "Open your authenticator app and enter the 6-digit code shown for Vedha."}
        </p>
      </div>

      {error && (
        <div className="login-error" role="alert" aria-live="polite">
          <LockKeyhole size={16} />
          <span>{error}</span>
        </div>
      )}

      {enrolling && (
        <div className="mfa-setup" aria-busy={!setup}>
          {setup ? <SetupKeyBlock setup={setup} /> : (
            <span className="mfa-loading"><Loader2 size={16} className="animate-spin" /> Preparing your key…</span>
          )}
        </div>
      )}

      <form onSubmit={submit} className="login-form">
        <label htmlFor="mfa-code">
          <span>{useRecovery ? "Recovery code" : "6-digit code"}</span>
          <input
            id="mfa-code"
            ref={inputRef}
            value={code}
            onChange={(e) => setCode(useRecovery ? e.target.value.toUpperCase() : e.target.value.replace(/[^\d ]/g, ""))}
            placeholder={useRecovery ? "XXXXX-XXXXX" : "123 456"}
            autoComplete="one-time-code"
            inputMode={useRecovery ? "text" : "numeric"}
            maxLength={useRecovery ? 16 : 7}
            className="mfa-code-input"
            disabled={busy || (enrolling && !setup)}
            required
          />
        </label>
        <button className="login-submit" type="submit" disabled={busy || (enrolling && !setup)}>
          {busy
            ? <><Loader2 size={17} className="animate-spin" /> Checking…</>
            : enrolling ? <>Turn on and sign in <ArrowRight size={17} /></> : <>Verify <ArrowRight size={17} /></>}
        </button>
      </form>

      <div className="mfa-links">
        {!enrolling && (
          <button type="button" onClick={() => { setUseRecovery((v) => !v); setCode(""); setError(null); }}>
            {useRecovery ? "Use a code from my app" : "Lost your phone? Use a recovery code"}
          </button>
        )}
        <button type="button" onClick={() => onRestart()}>
          <ArrowLeft size={13} /> Start again
        </button>
      </div>
    </div>
  );
}
