"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Menu, Sun, Moon, LogOut, User } from "lucide-react";
import { Sidebar } from "./Sidebar";
import { useTheme } from "./ThemeProvider";
import { RefreshButton } from "./RefreshButton";
import { clearAuth } from "../lib/fetcher";

interface PageShellProps {
  title: string;
  subtitle?: string;
  headerActions?: React.ReactNode;
  statusItems?: Array<{ label: string; value: string; color?: string; ariaLabel?: string }>;
  children: React.ReactNode;
  noPadding?: boolean;
  /** Hide the header refresh control. For pages that already poll themselves —
   *  a manual refresh there is redundant and invites a reload mid-update. */
  hideRefresh?: boolean;
}

export function PageShell({
  title, subtitle, headerActions, statusItems, children, noPadding, hideRefresh,
}: PageShellProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [utcTime, setUtcTime]         = useState("");
  const [userEmail, setUserEmail]     = useState<string | null>(null);

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

  return (
    <div style={{
      display: "flex",
      height: "100vh",
      fontFamily: "var(--font-body)",
      overflow: "hidden",
    }}>
      <style>{SHELL_RESPONSIVE_STYLES}</style>
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
        <header className="vedha-page-header" style={{
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
          <div className="vedha-page-header-left" style={{ display: "flex", alignItems: "center", gap: 8, minWidth: 0 }}>
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

            <div className="vedha-page-title-meta" style={{ display: "flex", alignItems: "center", gap: 7, minWidth: 0 }}>
              <span style={{
                fontFamily: "var(--font-display)",
                fontSize: 14,
                fontWeight: 650,
                color: "var(--text-primary)",
                flexShrink: 0,
                letterSpacing: "-0.01em",
              }}>
                {title}
              </span>
              {subtitle && (
                <>
                  <span className="vedha-page-title-divider" style={{ color: "var(--border-strong)", flexShrink: 0, fontSize: 13, fontWeight: 400 }}>/</span>
                  <span className="vedha-page-subtitle" style={{
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

            {/* Live indicator — signals the console is connected and auto-refreshing */}
            <span
              title="Live — console connected, data auto-refreshing"
              aria-label="Live"
              style={{
                width: 5,
                height: 5,
                borderRadius: "50%",
                background: "var(--accent)",
                flexShrink: 0,
                animation: "pulse 2s ease-in-out infinite",
                boxShadow: "0 0 6px var(--accent-glow)",
              }}
            />
          </div>

          {/* Right */}
          <div className="vedha-page-header-tools" style={{ display: "flex", alignItems: "center", gap: 10, flexShrink: 0 }}>
            {headerActions && (
              <div className="vedha-page-header-actions" style={{ display: "flex", alignItems: "center", gap: 6 }}>
                {headerActions}
              </div>
            )}

            {/* Status items */}
            {statusItems?.map((item, i) => {
              const tone = item.color ?? "var(--text-primary)";
              return (
              <React.Fragment key={i}>
                <div className="vedha-page-header-divider" aria-hidden style={{ width: 0.5, height: 16, background: "var(--border-subtle)", flexShrink: 0 }} />
                <div
                  className="vedha-page-status"
                  role="img"
                  aria-label={item.ariaLabel ?? `${item.label} ${item.value}`}
                  style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                  height: 28,
                  padding: "0 10px",
                  background: `color-mix(in srgb, ${tone} 8%, transparent)`,
                  border: `0.5px solid color-mix(in srgb, ${tone} 28%, transparent)`,
                  borderRadius: 8,
                }}>
                  <span style={{
                    width: 6,
                    height: 6,
                    borderRadius: "50%",
                    background: tone,
                    flexShrink: 0,
                    boxShadow: `0 0 5px color-mix(in srgb, ${tone} 55%, transparent)`,
                  }} />
                  <span style={{
                    fontSize: 9,
                    color: "var(--text-muted)",
                    letterSpacing: "0.09em",
                    fontWeight: 700,
                    textTransform: "uppercase" as const,
                  }}>
                    {item.label}
                  </span>
                  <span style={{
                    fontSize: 11.5,
                    fontWeight: 650,
                    color: tone,
                    letterSpacing: "0.02em",
                  }}>
                    {item.value}
                  </span>
                </div>
              </React.Fragment>
              );
            })}

            <div className="vedha-page-header-divider" style={{ width: 0.5, height: 16, background: "var(--border-subtle)", flexShrink: 0 }} />

            {/* Reload after a short delay — a newly enrolled vedha-agent lands in
                the API a moment after the UI action, so an instant reload can miss it. */}
            {!hideRefresh && <RefreshButton size={30} />}

            {/* Theme toggle — rotates icon on hover */}
            <button
              onClick={toggleTheme}
              title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: 30,
                height: 30,
                borderRadius: 8,
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
                {theme === "dark" ? <Sun size={14} /> : <Moon size={14} />}
              </span>
            </button>

            {/* User badge + logout */}
            {userEmail && (
              <>
                <div className="vedha-page-header-divider" style={{ width: 0.5, height: 16, background: "var(--border-subtle)", flexShrink: 0 }} />
                <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <User size={14} color="var(--text-muted)" />
                  <span style={{
                    fontSize: 11,
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
                    width: 30,
                    height: 30,
                    borderRadius: 8,
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
                  <LogOut size={14} />
                </button>
              </>
            )}
          </div>
        </header>

        {/* ── Content ── */}
        <main className="vedha-page-main" style={{
          flex: 1,
          overflowY: "auto",
          background: "var(--bg-app)",
          padding: noPadding ? 0 : "20px 24px",
        }}>
          {children}
        </main>

        {/* ── Footer ── */}
        <footer className="vedha-page-footer" style={{
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

          <div className="vedha-page-footer-time" style={{
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

const SHELL_RESPONSIVE_STYLES = `
@media (max-width: 767px) {
  .vedha-page-header {
    height: auto !important;
    min-height: 50px;
    padding: 8px 12px !important;
    align-content: center;
    flex-wrap: wrap;
    gap: 6px !important;
  }
  .vedha-page-header-left { flex: 1 1 auto; max-width: 100%; }
  .vedha-page-title-divider, .vedha-page-subtitle { display: none; }
  .vedha-page-header-tools {
    flex: 1 0 100% !important;
    width: 100%;
    min-width: 0;
    gap: 6px !important;
    justify-content: flex-start;
    overflow-x: auto;
    overscroll-behavior-x: contain;
    scrollbar-width: none;
  }
  .vedha-page-header-tools::-webkit-scrollbar { display: none; }
  .vedha-page-header-actions, .vedha-page-status { flex-shrink: 0; }
  .vedha-page-header-divider { display: none; }
  .vedha-page-status { height: 26px !important; padding: 0 8px !important; }
  .vedha-page-main { padding: 16px !important; }
  .vedha-page-footer { padding: 0 12px !important; }
  .vedha-page-footer-time { display: none; }
}
`;
