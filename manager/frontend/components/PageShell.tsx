"use client";

import React, { useState, useEffect, useCallback } from "react";
import { Menu, Sun, Moon, LogOut, User } from "lucide-react";
import { Sidebar } from "./Sidebar";
import { useTheme } from "./ThemeProvider";
import { RefreshButton } from "./RefreshButton";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { clearAuth } from "../lib/fetcher";
import { clearSessionState } from "../lib/session-state";

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
  surface?: "manager" | "portal";
  live?: boolean;
}

export function PageShell({
  title, subtitle, headerActions, statusItems, children, noPadding, hideRefresh,
  surface = "manager",
}: PageShellProps) {
  const pathname = usePathname();
  const detailParent = pathname.startsWith("/engagements/") ? { href: "/engagements", label: "Engagements" }
    : pathname.startsWith("/campaign/") ? { href: "/campaign", label: "VA Campaigns" } : null;
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const closeSidebar = useCallback(() => setSidebarOpen(false), []);
  const [utcTime, setUtcTime]         = useState("");
  const [userEmail, setUserEmail]     = useState<string | null>(
    surface === "portal" ? "Customer" : null,
  );

  // Read current user
  useEffect(() => {
    if (surface === "portal") {
      // Show who is signed in, not a generic "Customer".
      fetch("/api/portal/me", { credentials: "same-origin", cache: "no-store" })
        .then((r) => (r.ok ? r.json() : null))
        .then((d: { email?: string } | null) => { if (d?.email) setUserEmail(d.email); })
        .catch(() => {});
      return;
    }
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
  }, [surface]);

  const handleLogout = useCallback(async () => {
    clearSessionState();
    if (surface === "portal") {
      await fetch("/api/portal/login", { method: "DELETE" }).catch(() => {});
      window.location.href = "/portal/login";
      return;
    }
    await fetch("/api/auth/login", { method: "DELETE" }).catch(() => {});
    clearAuth(true);
  }, [surface]);

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
    <div className="vedha-shell" style={{
      display: "flex",
      height: "100dvh",
      fontFamily: "var(--font-body)",
      overflow: "hidden",
    }}>
      <style>{SHELL_RESPONSIVE_STYLES}</style>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="md:hidden"
          data-modal-backdrop
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

      <Sidebar open={sidebarOpen} onClose={closeSidebar} surface={surface} />

      <div className="vedha-shell-body" style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        minWidth: 0,
      }}>
        {/* ── Header ── */}
        <header className="vedha-page-header" style={{
          height: "auto",
          minHeight: 50,
          flexWrap: "wrap",
          flexShrink: 0,
          background: "var(--bg-panel)",
          borderBottom: "0.5px solid var(--border-default)",
          boxShadow: "0 1px 0 rgba(15, 23, 42, 0.02)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "8px 18px",
          gap: 12,
        }}>
          {/* Left */}
          <div className="vedha-page-header-left" style={{
            display: "flex", alignItems: "center", gap: 8,
            flex: "0 1 460px", minWidth: 0, overflow: "hidden",
          }}>
            <button
              className="md:hidden touch-icon"
              onClick={() => setSidebarOpen(true)}
              aria-label="Open sidebar"
              aria-expanded={sidebarOpen}
              aria-controls="operator-navigation"
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

            <div className="vedha-page-title-meta" style={{ display: "flex", alignItems: "center", gap: 7, minWidth: 0, flex: "1 1 auto" }}>
              <h1 style={{
                fontFamily: "var(--font-display)",
                fontSize: 14,
                fontWeight: 650,
                color: "var(--text-primary)",
                flexShrink: 0,
                letterSpacing: "-0.01em",
                margin: 0,
              }}>
                {title}
              </h1>
              {subtitle && (
                <>
                  <span className="vedha-page-title-divider" style={{ color: "var(--border-strong)", flexShrink: 0, fontSize: 13, fontWeight: 400 }}>/</span>
                  <span className="vedha-page-subtitle" style={{
                    // contain: its text must not size the title block — it fills
                    // whatever space is left and ellipsizes, never pushing the tools.
                    contain: "inline-size",
                    flex: "1 1 auto",
                    minWidth: 0,
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
          </div>

          {/* Right */}
          {/* Never paint over the title: the subtitle truncates first, then the
              page's own chips scroll sideways. Refresh / theme / account / sign
              out stay pinned and always reachable. */}
          <div className="vedha-page-header-tools" style={{
            display: "flex", alignItems: "center", gap: 10,
            flex: "1 1 520px", minWidth: 0, justifyContent: "flex-end", overflow: "hidden",
          }}>
            <div className="vedha-page-header-scroll" style={{
              display: "flex", alignItems: "center", gap: 10, minWidth: 0,
              width: 0, flex: "1 1 auto",
              overflowX: "auto", scrollbarWidth: "none",
            }}>
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

            </div>
            <div className="vedha-page-header-pinned" style={{ display: "flex", alignItems: "center", gap: 10, flex: "0 0 auto" }}>
              <div className="vedha-page-header-divider" style={{ width: 0.5, height: 16, background: "var(--border-subtle)", flexShrink: 0 }} />

              {/* Reload after a short delay — a newly enrolled vedha-agent lands in
                  the API a moment after the UI action, so an instant reload can miss it. */}
              {!hideRefresh && <RefreshButton size={30} />}

              {/* Theme toggle — rotates icon on hover */}
              <button
                className="touch-icon"
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
                  <div className="vedha-page-account" style={{ display: "flex", alignItems: "center", gap: 6, minWidth: 0 }}>
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
                    className="touch-icon"
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
          </div>
        </header>

        {/* ── Content ── */}
        <main className="vedha-page-main" style={{
          flex: 1,
          overflowY: "auto",
          background: "var(--bg-app)",
          // Gutters come from the shared ladder in globals.css so a tablet is not
          // paying desktop-sized margins. See "Responsive page container".
          padding: noPadding ? 0 : "var(--page-pad-y) var(--page-pad-x)",
        }}>
          {noPadding ? children : <div className="vedha-page-container">
            {detailParent && <nav aria-label="Breadcrumb" className="vedha-breadcrumb"><Link href={detailParent.href}>{detailParent.label}</Link><span aria-hidden>/</span><span aria-current="page">{title}</span></nav>}
            {children}
          </div>}
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
          <span style={{ fontSize: 9, color: "var(--text-muted)" }}>Vedha operator console</span>

          <div className="vedha-page-footer-time" style={{
            fontFamily: "var(--font-mono)",
            fontSize: 9,
            color: "var(--text-muted)",
          }}>
            {utcTime} · VEDHA v1.0{surface === "portal" ? " · Customer workspace" : ""}
          </div>
        </footer>
      </div>
    </div>
  );
}

const SHELL_RESPONSIVE_STYLES = `
.vedha-page-header-left { flex-shrink: 0; max-width: 100%; }
.vedha-page-header-tools { max-width: 100%; min-width: 0; overflow-x: auto; }
.vedha-page-header-tools > * { flex-shrink: 0; }

/* Tablet: 768px–1023px — sidebar always visible, but content is tighter */
.vedha-page-header-scroll::-webkit-scrollbar { display: none; }
.vedha-page-header-scroll > *, .vedha-page-header-tools > :not(.vedha-page-header-scroll) { flex-shrink: 0; }

@media (max-width: 1360px) {
  .vedha-page-title-divider, .vedha-page-subtitle { display: none; }
  .vedha-page-header-left { flex-basis: 220px !important; }
  .vedha-page-header-tools { flex-basis: 460px !important; }
  .vedha-page-account span { max-width: 104px !important; }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .vedha-page-title-divider, .vedha-page-subtitle { display: none; }
  .vedha-page-header { padding: 0 14px !important; }
  .vedha-page-main { padding: 16px 18px !important; }
  .vedha-page-footer { padding: 0 14px !important; }
  .vedha-page-footer-time { display: none; }
  .vedha-page-status { padding: 0 7px !important; }
}

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
    justify-content: flex-start !important;
    overflow: hidden !important;
  }
  .vedha-page-header-tools::-webkit-scrollbar { display: none; }
  .vedha-page-header-scroll {
    width: 0 !important;
    flex: 1 1 auto !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    overscroll-behavior-x: contain;
    scrollbar-width: none;
  }
  .vedha-page-header-pinned { gap: 6px !important; }
  .vedha-page-account span { display: none; }
  .vedha-page-header-actions, .vedha-page-status { flex-shrink: 0; }
  .vedha-page-header-divider { display: none; }
  .vedha-page-status { height: 26px !important; padding: 0 8px !important; }
  .vedha-page-main { padding: 16px !important; }
  .vedha-page-footer { padding: 0 12px !important; }
  .vedha-page-footer-time { display: none; }
}
@media (pointer: coarse) {
  .vedha-page-header button { min-width: 44px !important; min-height: 44px !important; }
}
`;
