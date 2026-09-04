"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Shield, Loader2, Eye, EyeOff, Zap } from "lucide-react";

export default function PortalLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [autoSigning, setAutoSigning] = useState(false);

  const doLogin = useCallback(async (em: string, pw: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/portal/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: em, password: pw }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        setAutoSigning(false);
        setError(
          data.code === "invalid_credentials"
            ? "Invalid email or password."
            : data.code === "not_a_client"
            ? "This login is not a customer portal account."
            : data.code === "rate_limited"
            ? "Too many attempts — please wait a moment and try again."
            : data.error || "Login failed.",
        );
        return;
      }
      router.push("/portal");
    } catch {
      setAutoSigning(false);
      setError("Network error — please try again.");
    } finally {
      setLoading(false);
    }
  }, [router]);

  // Auto-login from URL fragment: /portal/login#e=email@co.com&p=password
  // The fragment is read client-side only — it is never sent to any server —
  // and is cleared immediately so credentials don't survive in browser history.
  useEffect(() => {
    if (typeof window === "undefined") return;
    const hash = window.location.hash.slice(1);
    if (!hash) return;
    const params = new URLSearchParams(hash);
    const e = params.get("e");
    const p = params.get("p");
    if (!e || !p) return;
    // Erase fragment before anything async happens
    window.history.replaceState(null, "", window.location.pathname + window.location.search);
    setEmail(e);
    setPassword(p);
    setAutoSigning(true);
    void doLogin(e, p);
  }, [doLogin]);

  async function submit(ev: React.FormEvent) {
    ev.preventDefault();
    await doLogin(email, password);
  }

  return (
    <div className="console-scope" style={{
      minHeight: "100vh", display: "flex", alignItems: "center",
      justifyContent: "center", padding: 16, background: "var(--bg-app)",
      fontFamily: "var(--font-body)",
    }}>
      <div className="panel" style={{ width: "100%", maxWidth: 380, padding: 32 }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center",
          gap: 8, marginBottom: 24 }}>
          <div style={{ width: 44, height: 44, borderRadius: 10,
            background: "var(--accent-ghost)", border: "var(--hairline) solid var(--border-accent)",
            display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Shield style={{ width: 24, height: 24, color: "var(--accent)" }} />
          </div>
          <h1 style={{ fontFamily: "var(--font-display)", fontSize: 18, fontWeight: 600,
            color: "var(--text-primary)", margin: 0, letterSpacing: 1 }}>
            Vedha User Portal
          </h1>
          <p style={{ fontSize: 13, color: "var(--text-muted)", margin: 0 }}>
            Sign in to view your engagement
          </p>
        </div>

        {/* Auto-sign-in banner */}
        {autoSigning && (
          <div style={{
            display: "flex", alignItems: "center", gap: 8,
            padding: "10px 12px", borderRadius: 8, marginBottom: 16,
            background: "var(--accent-ghost)", border: "0.5px solid var(--border-accent)",
            color: "var(--accent)", fontSize: 12, fontWeight: 600,
          }}>
            <Zap size={14} />
            <span>Signing you in via access link…</span>
            <Loader2 size={13} style={{ marginLeft: "auto", animation: "spin 1s linear infinite" }} />
          </div>
        )}

        <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div>
            <label htmlFor="portal-email" className="eyebrow" style={{ display: "block", marginBottom: 6 }}>Email</label>
            <input id="portal-email" type="email" required autoComplete="email"
              value={email} onChange={(e) => setEmail(e.target.value)} className="input-base"
              placeholder="you@company.com" disabled={autoSigning} />
          </div>
          <div>
            <label htmlFor="portal-password" className="eyebrow" style={{ display: "block", marginBottom: 6 }}>Password</label>
            <div style={{ position: "relative" }}>
              <input id="portal-password" type={showPw ? "text" : "password"} required
                autoComplete="current-password" value={password}
                onChange={(e) => setPassword(e.target.value)} className="input-base"
                style={{ paddingRight: 40 }} placeholder="••••••••" disabled={autoSigning} />
              <button type="button" onClick={() => setShowPw((v) => !v)}
                aria-label={showPw ? "Hide password" : "Show password"}
                style={{ position: "absolute", right: 4, top: "50%", transform: "translateY(-50%)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  width: 28, height: 28, border: "none", background: "none",
                  cursor: "pointer", color: "var(--text-muted)" }}>
                {showPw ? <EyeOff style={{ width: 15, height: 15 }} /> : <Eye style={{ width: 15, height: 15 }} />}
              </button>
            </div>
          </div>
          {error && (
            <div role="alert" style={{ borderRadius: 8, padding: "9px 11px", fontSize: 13,
              color: "var(--sev-critical-color)",
              background: "color-mix(in srgb, var(--sev-critical-color) 10%, transparent)" }}>
              {error}
            </div>
          )}
          <button type="submit" disabled={loading || autoSigning} className="btn btn-primary"
            style={{ width: "100%", height: 40 }}>
            {loading && <Loader2 style={{ width: 16, height: 16 }} className="animate-spin" />}
            Sign in
          </button>
        </form>
      </div>
    </div>
  );
}
