"use client";

import React, { Suspense, useState, useEffect, useRef, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Shield, Eye, EyeOff, Loader, AlertTriangle, Lock } from "lucide-react";
import { storeToken } from "../../lib/fetcher";

export default function LoginPage() {
  return (
    <Suspense fallback={null}>
      <LoginForm />
    </Suspense>
  );
}

function LoginForm() {
  const router       = useRouter();
  const searchParams = useSearchParams();
  const next         = searchParams.get("next") || "/";

  const [email,    setEmail]    = useState("");
  const [password, setPassword] = useState("");
  const [showPwd,  setShowPwd]  = useState(false);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState<string | null>(null);
  const [focused,  setFocused]  = useState<"email" | "password" | null>(null);
  const emailRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const token = localStorage.getItem("vedha_token");
    if (token) router.replace(next);
    // Delay focus slightly to let mount animation settle
    const t = setTimeout(() => emailRef.current?.focus(), 400);
    return () => clearTimeout(t);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) { setError("Email and password are required"); return; }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim().toLowerCase(), password }),
      });
      const data = await res.json() as { token?: string; refreshToken?: string; error?: string };
      if (!res.ok || !data.token) {
        setError(data.error || "Invalid email or password");
        return;
      }
      storeToken(data.token, data.refreshToken);
      router.replace(next);
    } catch {
      setError("Cannot reach the server — check your connection");
    } finally {
      setLoading(false);
    }
  }, [email, password, next, router]);

  const inputBase: React.CSSProperties = {
    width: "100%",
    padding: "10px 12px",
    borderRadius: 8,
    background: "var(--bg-surface)",
    border: "0.5px solid var(--border-subtle)",
    color: "var(--text-primary)",
    fontSize: 13,
    outline: "none",
    boxSizing: "border-box",
    fontFamily: "var(--font-body)",
    transition: "border-color 0.15s ease, box-shadow 0.15s ease, background 0.15s ease",
  };

  const inputFocus: React.CSSProperties = {
    borderColor: "var(--accent)",
    boxShadow: "0 0 0 3px var(--accent-ghost)",
    background: "var(--bg-card)",
  };

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden",
    }}>
      {/* Ambient glow — large, soft, centered behind the card */}
      <div aria-hidden style={{
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        width: "70vmax",
        height: "70vmax",
        borderRadius: "50%",
        background: "radial-gradient(circle, var(--accent-glow) 0%, transparent 60%)",
        opacity: 0.6,
        pointerEvents: "none",
      }} />

      {/* Subtle grid overlay */}
      <div aria-hidden style={{
        position: "absolute",
        inset: 0,
        backgroundImage: `
          linear-gradient(rgba(124,108,255,0.02) 1px, transparent 1px),
          linear-gradient(90deg, rgba(124,108,255,0.02) 1px, transparent 1px)
        `,
        backgroundSize: "40px 40px",
        pointerEvents: "none",
      }} />

      <div style={{
        width: "100%",
        maxWidth: 380,
        padding: "0 16px",
        position: "relative",
        zIndex: 1,
        animation: "fadeIn 0.5s ease, slideUp 0.5s var(--ease-out)",
      }}>
        {/* Card */}
        <div style={{
          background: "var(--bg-panel)",
          border: "0.5px solid var(--border-subtle)",
          borderRadius: 16,
          padding: "40px 32px 32px",
          boxShadow: "0 24px 80px rgba(0,0,0,0.35)",
          position: "relative",
          overflow: "hidden",
        }}>
          {/* Top accent line */}
          <div style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: 1,
            background: "linear-gradient(90deg, transparent 0%, var(--border-accent) 50%, transparent 100%)",
            opacity: 0.6,
          }} />

          {/* Logo */}
          <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginBottom: 32,
          }}>
            <div style={{
              width: 44,
              height: 44,
              borderRadius: 12,
              background: "var(--accent-ghost)",
              border: "0.5px solid var(--border-accent)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginBottom: 12,
              boxShadow: "0 0 20px var(--accent-glow)",
              animation: "accentGlow 3s ease-in-out infinite",
            }}>
              <Shield size={20} color="var(--accent)" strokeWidth={2} />
            </div>
            <div style={{
              fontFamily: "var(--font-display)",
              fontSize: 20,
              fontWeight: 700,
              color: "var(--text-primary)",
              letterSpacing: 2,
            }}>
              VEDHA
            </div>
            <div style={{
              fontSize: 11,
              color: "var(--text-muted)",
              marginTop: 4,
              letterSpacing: 0.5,
            }}>
              Security Operations Platform
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Error state */}
            {error && (
              <div
                role="alert"
                className="animate-slide-in"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  padding: "10px 14px",
                  borderRadius: 8,
                  marginBottom: 20,
                  background: "var(--sev-critical-bg)",
                  border: "0.5px solid var(--sev-critical-color)",
                  fontSize: 12,
                  color: "var(--sev-critical-color)",
                  lineHeight: 1.4,
                }}
              >
                <AlertTriangle size={13} style={{ flexShrink: 0 }} />
                {error}
              </div>
            )}

            {/* Email */}
            <div style={{ marginBottom: 16 }}>
              <label style={{
                display: "block",
                fontSize: 10,
                fontWeight: 600,
                color: focused === "email" ? "var(--accent)" : "var(--text-secondary)",
                letterSpacing: 0.8,
                marginBottom: 6,
                transition: "color 0.15s ease",
              }}>
                Email
              </label>
              <input
                ref={emailRef}
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@vedha.io"
                autoComplete="email"
                required
                style={{
                  ...inputBase,
                  ...(focused === "email" ? inputFocus : {}),
                }}
                onFocus={() => setFocused("email")}
                onBlur={() => setFocused(null)}
              />
            </div>

            {/* Password */}
            <div style={{ marginBottom: 24 }}>
              <label style={{
                display: "block",
                fontSize: 10,
                fontWeight: 600,
                color: focused === "password" ? "var(--accent)" : "var(--text-secondary)",
                letterSpacing: 0.8,
                marginBottom: 6,
                transition: "color 0.15s ease",
              }}>
                Password
              </label>
              <div style={{ position: "relative" }}>
                <input
                  type={showPwd ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••"
                  autoComplete="current-password"
                  required
                  style={{
                    ...inputBase,
                    paddingRight: 38,
                    ...(focused === "password" ? inputFocus : {}),
                  }}
                  onFocus={() => setFocused("password")}
                  onBlur={() => setFocused(null)}
                />
                <button
                  type="button"
                  onClick={() => setShowPwd(!showPwd)}
                  tabIndex={-1}
                  aria-label={showPwd ? "Hide password" : "Show password"}
                  style={{
                    position: "absolute",
                    right: 10,
                    top: "50%",
                    transform: "translateY(-50%)",
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                    color: "var(--text-muted)",
                    padding: 4,
                    display: "flex",
                    transition: "color 0.15s ease",
                  }}
                  onMouseEnter={(e) => { e.currentTarget.style.color = "var(--accent)"; }}
                  onMouseLeave={(e) => { e.currentTarget.style.color = "var(--text-muted)"; }}
                >
                  {showPwd ? <EyeOff size={13} /> : <Eye size={13} />}
                </button>
              </div>
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              style={{
                width: "100%",
                padding: "11px 0",
                borderRadius: 9,
                background: loading ? "var(--bg-card)" : "var(--accent)",
                border: "none",
                color: loading ? "var(--text-muted)" : "#fff",
                fontWeight: 700,
                fontSize: 13,
                cursor: loading ? "not-allowed" : "pointer",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 8,
                transition: "background 0.15s ease, transform 0.15s var(--ease-spring), box-shadow 0.15s ease",
                boxShadow: loading ? "none" : "0 4px 16px var(--accent-glow)",
                fontFamily: "var(--font-body)",
              }}
              onMouseEnter={(e) => {
                if (!loading) {
                  e.currentTarget.style.transform = "translateY(-1px)";
                  e.currentTarget.style.boxShadow = "0 6px 24px var(--accent-glow)";
                }
              }}
              onMouseLeave={(e) => {
                if (!loading) {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow = "0 4px 16px var(--accent-glow)";
                }
              }}
            >
              {loading ? (
                <><Loader size={13} className="animate-spin" /> Signing in...</>
              ) : (
                <><Lock size={13} /> Sign in</>
              )}
            </button>
          </form>

          <div style={{
            textAlign: "center",
            marginTop: 20,
            fontSize: 10,
            color: "var(--text-faint)",
            fontFamily: "var(--font-mono)",
            letterSpacing: 0.3,
          }}>
            VEDHA Enterprise · v1.0
          </div>
        </div>

        {/* Credentials hint */}
        <div style={{
          textAlign: "center",
          marginTop: 14,
          fontSize: 10,
          color: "var(--text-muted)",
          fontFamily: "var(--font-mono)",
          opacity: 0.6,
        }}>
          Default: admin@vedha.io / ChangeMe123!
        </div>
      </div>
    </div>
  );
}
