"use client";

import React, { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  ArrowRight, Check, Eye, EyeOff, Fingerprint, Loader2,
  LockKeyhole, Shield, ShieldCheck,
} from "lucide-react";

export default function LoginPage() {
  return (
    <Suspense fallback={<div className="login-page" />}>
      <LoginForm />
    </Suspense>
  );
}

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const requestedPath = searchParams.get("next") || "/";
  const nextPath = requestedPath.startsWith("/") && !requestedPath.startsWith("//") ? requestedPath : "/";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const emailRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let active = true;
    fetch("/api/auth/me", { credentials: "same-origin" })
      .then((response) => {
        if (!active) return;
        if (response.ok) router.replace(nextPath);
        else emailRef.current?.focus();
      })
      .catch(() => { if (active) emailRef.current?.focus(); });
    return () => { active = false; };
  }, [nextPath, router]);

  const submit = useCallback(async (event: React.FormEvent) => {
    event.preventDefault();
    if (!email.trim() || !password) {
      setError("Enter your work email and password to continue.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim().toLowerCase(), password }),
      });
      const data = await response.json() as { ok?: boolean; error?: string };
      if (!response.ok || !data.ok) {
        setError(response.status === 401
          ? "Those credentials were not recognized. Check them and try again."
          : data.error || "Sign-in is temporarily unavailable.");
        return;
      }
      router.replace(nextPath);
      router.refresh();
    } catch {
      setError("Vedha could not reach the authentication service. Check your connection and retry.");
    } finally {
      setLoading(false);
    }
  }, [email, password, nextPath, router]);

  return (
    <main className="login-page">
      <section className="login-story" aria-label="Vedha security platform">
        <div className="login-story-orb login-story-orb-a" aria-hidden />
        <div className="login-story-orb login-story-orb-b" aria-hidden />

        <div className="login-brand">
          <span className="login-brand-mark"><Shield size={20} strokeWidth={2.2} /></span>
          <span>VEDHA</span>
          <span className="login-version">ENTERPRISE</span>
        </div>

        <div className="login-story-copy">
          <div className="login-eyebrow">
            <span className="login-live-dot" />
            Security exposure management
          </div>
          <h1>Turn technical evidence into confident decisions.</h1>
          <p>
            One trusted workspace for assessment scope, findings, attack paths,
            remediation ownership, and client-ready reporting.
          </p>

          <div className="login-trust-list">
            {[
              ["Tenant-isolated data", "Authorization is enforced at the resource boundary."],
              ["Evidence-grounded AI", "Recommendations remain traceable to recorded findings."],
              ["Auditable operations", "Assessment activity stays attributable and reviewable."],
            ].map(([title, detail]) => (
              <div className="login-trust-item" key={title}>
                <span><Check size={13} /></span>
                <div><strong>{title}</strong><small>{detail}</small></div>
              </div>
            ))}
          </div>
        </div>

        <div className="login-posture-card" aria-label="Platform trust posture">
          <div>
            <ShieldCheck size={18} />
            <span><strong>Protected workspace</strong><small>Encrypted transport · role-based access</small></span>
          </div>
          <span className="badge badge-success">Ready</span>
        </div>
      </section>

      <section className="login-access">
        <div className="login-form-wrap">
          <div className="login-mobile-brand">
            <span className="login-brand-mark"><Shield size={18} /></span>
            <span>VEDHA</span>
          </div>

          <div className="login-form-heading">
            <span className="login-form-icon"><Fingerprint size={22} /></span>
            <h2>Welcome back</h2>
            <p>Sign in to your organization&apos;s security workspace.</p>
          </div>

          {error && (
            <div className="login-error" role="alert" aria-live="polite">
              <LockKeyhole size={16} />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={submit} className="login-form">
            <label htmlFor="login-email">
              <span>Work email</span>
              <input
                id="login-email"
                ref={emailRef}
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="name@company.com"
                autoComplete="username"
                inputMode="email"
                disabled={loading}
                required
              />
            </label>

            <label htmlFor="login-password">
              <span>Password</span>
              <div className="login-password-field">
                <input
                  id="login-password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  disabled={loading}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((value) => !value)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                </button>
              </div>
            </label>

            <button className="login-submit" type="submit" disabled={loading}>
              {loading ? (
                <><Loader2 size={17} className="animate-spin" /> Verifying securely…</>
              ) : (
                <>Continue to Vedha <ArrowRight size={17} /></>
              )}
            </button>
          </form>

          <div className="login-assurance">
            <LockKeyhole size={13} />
            <span>Your credentials are sent only to your configured Vedha Manager.</span>
          </div>

          <footer className="login-footer">Vedha Security Platform · Authorized users only</footer>
        </div>
      </section>
    </main>
  );
}
