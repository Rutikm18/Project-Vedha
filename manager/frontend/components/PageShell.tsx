"use client";

import React, { useState, useEffect, useCallback, useRef } from "react";
import { Menu, Sun, Moon, LogOut, User } from "lucide-react";
import { Sidebar } from "./Sidebar";
import { useTheme } from "./ThemeProvider";
import { clearAuth } from "../lib/fetcher";

interface PageShellProps {
  title: string;
  subtitle?: string;
  headerActions?: React.ReactNode;
  statusItems?: Array<{ label: string; value: string; color?: string }>;
  children: React.ReactNode;
  noPadding?: boolean;
}

export function PageShell({
  title, subtitle, headerActions, statusItems, children, noPadding,
}: PageShellProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [utcTime, setUtcTime]         = useState("");
  const [sessionTime, setSessionTime] = useState(0);
  const [userEmail, setUserEmail]     = useState<string | null>(null);
  const sessionStart = useRef<number | null>(null);

  // Read current user
  useEffect(() => {
    // One-time migration from builds that stored JWTs in browser storage.
    // End that legacy session so the next login receives HttpOnly cookies.
    if (localStorage.getItem("vedha_token") || localStorage.getItem("vedha_refresh_token")) {
      void fetch("/api/auth/logout", {
        method: "POST",
        credentials: "same-origin",
      }).finally(() => clearAuth(true));
      return;
    }
    fetch("/api/auth/me", { credentials: "same-origin" })
      .then((r) => (r.ok ? r.json() : null))
      .then((d: { email?: string } | null) => { if (d?.email) setUserEmail(d.email); })
      .catch(() => {});
  }, []);

  const handleLogout = useCallback(async () => {
    await fetch("/api/auth/logout", { method: "POST" }).catch(() => {});
    clearAuth(true);
  }, []);

  const { theme, toggleTheme } = useTheme();

  // UTC clock
  useEffect(() => {
    const tick = () =>
      setUtcTime(new Date().toISOString().replace("T", " ").slice(0, 19) + " UTC");
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  // Session timer
  useEffect(() => {
    sessionStart.current = Date.now();
    const id = setInterval(
      () => setSessionTime(Math.floor((Date.now() - (sessionStart.current ?? Date.now())) / 1000)),
      1000,
    );
    return () => clearInterval(id);
  }, []);

  const fmtSession = useCallback((s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
  }, []);

  return (
    <div style={{
      display: "flex",
      height: "100vh",
      fontFamily: "var(--font-body)",
      overflow: "hidden",
    }}>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="md:hidden"
          onClick={() => setSidebarOpen(false)}
          style={{
            position: "fixed",
            inset: 0,
            background: "var(--modal-backdrop)",
            zIndex: 40,
            backdropFilter: "blur(4px)",
            animation: "fadeIn 0.15s ease",
          }}
        />
      )}

      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        minWidth: 0,
      }}>
        {/* ── Header ── */}
        <header style={{
          height: 50,
          flexShrink: 0,
          background: "var(--bg-panel)",
          borderBottom: "0.5px solid var(--border-default)",
          boxShadow: "0 1px 0 rgba(15, 23, 42, 0.02)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 18px",
          gap: 12,
        }}>
          {/* Left */}
          <div style={{ display: "flex", alignItems: "center", gap: 8, minWidth: 0 }}>
            <button
              className="md:hidden"
              onClick={() => setSidebarOpen(true)}
              aria-label="Open sidebar"
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
                padding: 6,
                borderRadius: 6,
                flexShrink: 0,
                color: "var(--accent)",
                transition: "background 0.12s ease, transform 0.12s var(--ease-spring)",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "var(--accent-ghost)";
                e.currentTarget.style.transform = "scale(1.1)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "none";
                e.currentTarget.style.transform = "scale(1)";
              }}
            >
              <Menu size={17} />
            </button>

            <div style={{ display: "flex", alignItems: "center", gap: 5, minWidth: 0 }}>
              <span style={{
                fontFamily: "var(--font-display)",
                fontSize: 14,
                fontWeight: 600,
                color: "var(--text-primary)",
                flexShrink: 0,
                letterSpacing: 0,
              }}>
                {title}
              </span>
              {subtitle && (
                <>
                  <span style={{ color: "var(--text-faint)", flexShrink: 0, fontSize: 14, fontWeight: 300 }}>/</span>
                  <span style={{
                    fontSize: 13,
                    color: "var(--text-secondary)",
                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}>
                    {subtitle}
                  </span>
                </>
              )}
            </div>

            {/* Live indicator */}
            <span style={{
              width: 5,
              height: 5,
              borderRadius: "50%",
              background: "var(--accent)",
              flexShrink: 0,
              animation: "pulse 2s ease-in-out infinite",
              boxShadow: "0 0 6px var(--accent-glow)",
            }} />
          </div>

          {/* Right */}
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexShrink: 0 }}>
            {headerActions && (
              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                {headerActions}
              </div>
            )}

            {/* Status items */}
            {statusItems?.map((item, i) => (
              <React.Fragment key={i}>
                <div style={{ width: 0.5, height: 14, background: "var(--border-subtle)", flexShrink: 0 }} />
                <div style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 5,
                  minHeight: 24,
                  padding: "2px 7px",
                  background: "var(--bg-surface)",
                  border: "0.5px solid var(--border-subtle)",
                  borderRadius: 7,
                }}>
                  <span style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: 9,
                    color: "var(--text-muted)",
                    letterSpacing: 0.6,
                    fontWeight: 600,
                  }}>
                    {item.label}
                  </span>
                  <span style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: 10,
                    fontWeight: 600,
                    color: item.color ?? "var(--text-primary)",
                  }}>
                    {item.value}
                  </span>
                </div>
              </React.Fragment>
            ))}

            <div style={{ width: 0.5, height: 14, background: "var(--border-subtle)", flexShrink: 0 }} />

            {/* Session time */}
            <span style={{
              fontFamily: "var(--font-mono)",
              fontSize: 10,
              color: "var(--text-muted)",
              letterSpacing: 0.2,
            }}>
              {fmtSession(sessionTime)}
            </span>

            <div style={{ width: 0.5, height: 14, background: "var(--border-subtle)", flexShrink: 0 }} />

            {/* Theme toggle — rotates icon on hover */}
            <button
              onClick={toggleTheme}
              title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: 28,
                height: 28,
                borderRadius: 7,
                flexShrink: 0,
                border: "0.5px solid var(--border-subtle)",
                background: "transparent",
                cursor: "pointer",
                color: "var(--text-muted)",
                transition: "all 0.18s var(--ease-spring)",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = "var(--accent)";
                e.currentTarget.style.color = "var(--accent)";
                e.currentTarget.style.background = "var(--accent-ghost)";
                e.currentTarget.style.transform = "scale(1.1)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = "var(--border-subtle)";
                e.currentTarget.style.color = "var(--text-muted)";
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.transform = "scale(1)";
              }}
            >
              <span style={{
                display: "flex",
                transition: "transform 0.3s var(--ease-spring)",
              }}>
                {theme === "dark" ? <Sun size={12} /> : <Moon size={12} />}
              </span>
            </button>

            {/* User badge + logout */}
            {userEmail && (
              <>
                <div style={{ width: 0.5, height: 14, background: "var(--border-subtle)", flexShrink: 0 }} />
                <div style={{ display: "flex", alignItems: "center", gap: 5 }}>
                  <User size={10} color="var(--text-muted)" />
                  <span style={{
                    fontSize: 10,
                    color: "var(--text-secondary)",
                    maxWidth: 140,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}>
                    {userEmail}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  title="Sign out"
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: 26,
                    height: 26,
                    borderRadius: 7,
                    border: "0.5px solid var(--border-subtle)",
                    background: "transparent",
                    cursor: "pointer",
                    color: "var(--text-muted)",
                    transition: "all 0.15s",
                    flexShrink: 0,
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = "var(--sev-critical-color)";
                    e.currentTarget.style.color = "var(--sev-critical-color)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = "var(--border-subtle)";
                    e.currentTarget.style.color = "var(--text-muted)";
                  }}
                >
                  <LogOut size={11} />
                </button>
              </>
            )}
          </div>
        </header>

        {/* ── Content ── */}
        <main style={{
          flex: 1,
          overflowY: "auto",
          background: "var(--bg-app)",
          padding: noPadding ? 0 : "20px 24px",
        }}>
          {children}
        </main>

        {/* ── Footer ── */}
        <footer style={{
          height: 26,
          flexShrink: 0,
          background: "var(--bg-panel)",
          borderTop: "0.5px solid var(--border-subtle)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 18px",
          gap: 12,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            {[
              { label: "ENGINE", color: "var(--accent)" },
              { label: "API",    color: "var(--accent)" },
              { label: "DB",     color: "var(--accent)" },
            ].map((s, i) => (
              <React.Fragment key={i}>
                {i > 0 && <div style={{ width: 0.5, height: 9, background: "var(--border-subtle)" }} />}
                <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
                  <span style={{
                    width: 4,
                    height: 4,
                    borderRadius: "50%",
                    background: s.color,
                    display: "inline-block",
                    boxShadow: `0 0 3px ${s.color}`,
                  }} />
                  <span style={{ fontSize: 9, color: "var(--text-muted)", fontWeight: 500 }}>
                    {s.label}
                  </span>
                </div>
              </React.Fragment>
            ))}
          </div>

          <div style={{
            fontFamily: "var(--font-mono)",
            fontSize: 9,
            color: "var(--text-muted)",
          }}>
            {utcTime} · VEDHA v1.0
          </div>
        </footer>
      </div>
    </div>
  );
}
