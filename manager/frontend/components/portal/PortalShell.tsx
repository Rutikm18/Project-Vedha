"use client";

/**
 * PortalShell — the customer-facing console shell. Mirrors the operator PageShell's
 * chrome (theme tokens, sidebar, header with session/theme, footer) so the User
 * Portal looks like the same product, but with a LIMITED nav (Dashboard, Findings,
 * Scans, Reports) and portal auth. Everything is theme-token driven, so light/dark
 * follows the app toggle just like the main dashboard.
 */
import React, { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Shield, LayoutDashboard, Bug, Radar, FileText, LogOut, Menu, Sun, Moon, User, Settings,
  Target, Sparkles, Cpu,
} from "lucide-react";
import { useTheme } from "../ThemeProvider";
import { RefreshButton } from "../RefreshButton";
import { usePortalEngagement } from "../../lib/portal-client";

const APP_VERSION = process.env.NEXT_PUBLIC_APP_VERSION ?? "dev";

const NAV = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/portal" },
  { icon: Bug,             label: "Findings",  href: "/portal/findings" },
  { icon: Radar,           label: "Scans",     href: "/portal/scans" },
  { icon: Cpu,             label: "Probe",     href: "/portal/fleet" },
  // Scope is READ-ONLY here on purpose (see app/portal/scope/page.tsx): it is the
  // authorisation record for active scanning, so only the security team changes it.
  { icon: Target,          label: "Scope",     href: "/portal/scope" },
  { icon: FileText,        label: "Reports",   href: "/portal/reports" },
  { icon: Sparkles,        label: "Assistant", href: "/portal/assistant" },
  { icon: Settings,        label: "Settings",  href: "/portal/settings" },
];

interface PortalShellProps {
  title: string;
  subtitle?: string;
  headerActions?: React.ReactNode;
  statusItems?: Array<{ label: string; value: string; color?: string }>;
  /** When true the header status dot pulses (something is actively running). */
  live?: boolean;
  children: React.ReactNode;
}

function PortalSidebar({ open, onClose, engName, engStatus }: {
  open: boolean;
  onClose: () => void;
  engName?: string;
  engStatus?: string;
}) {
  const pathname = usePathname();

  return (
    <aside
      className={[
        "fixed md:static z-50",
        "transition-transform duration-200 ease-in-out",
        open ? "translate-x-0" : "-translate-x-full md:translate-x-0",
      ].join(" ")}
      style={{
        width: 216, background: "var(--bg-panel)",
        borderRight: "0.5px solid var(--border-default)",
        display: "flex", flexDirection: "column", height: "100vh",
        flexShrink: 0, overflowY: "auto",
      }}
    >
      <div style={{
        padding: "20px 16px 14px", borderBottom: "0.5px solid var(--border-subtle)",
        display: "flex", alignItems: "center", gap: 10, flexShrink: 0,
      }}>
        <div style={{
          width: 32, height: 32, borderRadius: 8, background: "var(--accent-ghost)",
          border: "0.5px solid var(--border-accent)", display: "flex",
          alignItems: "center", justifyContent: "center", flexShrink: 0,
        }}>
          <Shield size={15} color="var(--accent)" strokeWidth={2} />
        </div>
        <div>
          <div style={{
            fontFamily: "var(--font-display)", fontSize: 13, fontWeight: 700,
            color: "var(--text-primary)", letterSpacing: 2, lineHeight: 1,
          }}>
            VEDHA
          </div>
          <div style={{ fontSize: 9, color: "var(--text-muted)", fontWeight: 500,
            letterSpacing: 0.3, marginTop: 3 }}>
            User Portal
          </div>
        </div>
      </div>

      {/* Engagement context — always visible so the customer knows which engagement they're in */}
      {engName && (
        <div style={{
          padding: "10px 16px", borderBottom: "0.5px solid var(--border-subtle)",
          flexShrink: 0,
        }}>
          <div style={{ fontSize: 9, fontWeight: 700, color: "var(--text-faint)",
            letterSpacing: 1.4, textTransform: "uppercase", marginBottom: 6 }}>
            Engagement
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
            <span style={{
              width: 7, height: 7, borderRadius: "50%", flexShrink: 0,
              background: engStatus === "active" ? "var(--nominal-color)" : "var(--text-muted)",
              boxShadow: engStatus === "active" ? "0 0 5px var(--nominal-color)" : "none",
            }} />
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: 12, fontWeight: 600, color: "var(--text-primary)",
                overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {engName}
              </div>
              {engStatus && (
                <div style={{ fontSize: 10, color: "var(--text-muted)", textTransform: "capitalize",
                  marginTop: 1 }}>
                  {engStatus}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <nav style={{ paddingTop: 10, flex: 1 }}>
        <div style={{
          padding: "5px 16px 4px", fontSize: 9, fontWeight: 700,
          color: "var(--text-faint)", letterSpacing: 1.4, textTransform: "uppercase",
        }}>
          Overview
        </div>
        {NAV.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onClose}
              aria-current={isActive ? "page" : undefined}
              className="portal-nav-link"
            >
              <Icon className="portal-nav-icon" size={14} />
              <span className="portal-nav-label">{item.label}</span>
              {isActive && (
                <span style={{ width: 4, height: 4, borderRadius: "50%",
                  background: "var(--accent)", boxShadow: "0 0 5px var(--accent-glow)" }} />
              )}
            </Link>
          );
        })}
      </nav>

      <div style={{ padding: "12px 16px", borderTop: "0.5px solid var(--border-subtle)",
        flexShrink: 0, fontFamily: "var(--font-mono)", fontSize: 9,
        color: "var(--text-muted)" }}>
        VEDHA v{APP_VERSION} · Secure Portal
      </div>
    </aside>
  );
}

export function PortalShell({
  title, subtitle, headerActions, statusItems, live, children,
}: PortalShellProps) {
  const router = useRouter();
  const { theme, toggleTheme } = useTheme();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const eng = usePortalEngagement();

  const logout = useCallback(async () => {
    await fetch("/api/portal/logout", { method: "POST" }).catch(() => {});
    router.push("/portal/login");
  }, [router]);

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "var(--font-body)",
      overflow: "hidden" }}>
      {sidebarOpen && (
        <div className="md:hidden" onClick={() => setSidebarOpen(false)}
          style={{ position: "fixed", inset: 0, background: "var(--modal-backdrop)",
            zIndex: 40, backdropFilter: "blur(4px)" }} />
      )}

      <PortalSidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        engName={eng.data?.name}
        engStatus={eng.data?.status}
      />

      <div style={{ flex: 1, display: "flex", flexDirection: "column",
        overflow: "hidden", minWidth: 0 }}>
        <header style={{
          height: 50, flexShrink: 0, background: "var(--bg-panel)",
          borderBottom: "0.5px solid var(--border-default)", display: "flex",
          alignItems: "center", justifyContent: "space-between",
          padding: "0 18px", gap: 12,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, minWidth: 0 }}>
            <button className="md:hidden" onClick={() => setSidebarOpen(true)}
              aria-label="Open sidebar"
              style={{ background: "none", border: "none", cursor: "pointer",
                padding: 6, color: "var(--accent)" }}>
              <Menu size={17} />
            </button>
            <span style={{ fontFamily: "var(--font-display)", fontSize: 14,
              fontWeight: 600, color: "var(--text-primary)" }}>
              {title}
            </span>
            {subtitle && (
              <>
                <span style={{ color: "var(--text-faint)", fontSize: 14, fontWeight: 300 }}>/</span>
                <span style={{ fontSize: 13, color: "var(--text-secondary)",
                  whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                  {subtitle}
                </span>
              </>
            )}
            <span aria-label={live ? "Scan running" : "Idle"} title={live ? "Scan running" : "Idle"}
              style={{ width: 5, height: 5, borderRadius: "50%",
                background: live ? "var(--accent)" : "var(--text-faint)",
                animation: live ? "pulse 2s ease-in-out infinite" : "none",
                boxShadow: live ? "0 0 6px var(--accent-glow)" : "none" }} />
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: 10, flexShrink: 0 }}>
            {headerActions && (
              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>{headerActions}</div>
            )}
            {statusItems?.map((item, i) => (
              <React.Fragment key={i}>
                <div style={{ width: 0.5, height: 14, background: "var(--border-subtle)" }} />
                <div style={{ display: "flex", alignItems: "center", gap: 5,
                  padding: "2px 7px", background: "var(--bg-surface)",
                  border: "0.5px solid var(--border-subtle)", borderRadius: 7 }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 9,
                    color: "var(--text-muted)", letterSpacing: 0.6, fontWeight: 600 }}>
                    {item.label}
                  </span>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 10,
                    fontWeight: 600, color: item.color ?? "var(--text-primary)" }}>
                    {item.value}
                  </span>
                </div>
              </React.Fragment>
            ))}

            <div style={{ width: 0.5, height: 14, background: "var(--border-subtle)" }} />
            {/* Reload after a short delay — a newly enrolled vedha-agent lands in
                the API a moment after the UI action, so an instant reload can miss it. */}
            <RefreshButton size={28} />
            <button onClick={toggleTheme}
              aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
              title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
              style={{ display: "flex", alignItems: "center", justifyContent: "center",
                width: 28, height: 28, borderRadius: 7,
                border: "0.5px solid var(--border-subtle)", background: "transparent",
                cursor: "pointer", color: "var(--text-muted)" }}>
              {theme === "dark" ? <Sun size={12} /> : <Moon size={12} />}
            </button>

            <div style={{ width: 0.5, height: 14, background: "var(--border-subtle)" }} />
            <div style={{ display: "flex", alignItems: "center", gap: 5 }}>
              <User size={10} color="var(--text-muted)" />
              <span style={{ fontSize: 10, color: "var(--text-secondary)" }}>Customer</span>
            </div>
            <button onClick={logout} aria-label="Sign out" title="Sign out"
              style={{ display: "flex", alignItems: "center", justifyContent: "center",
                width: 26, height: 26, borderRadius: 7,
                border: "0.5px solid var(--border-subtle)", background: "transparent",
                cursor: "pointer", color: "var(--text-muted)" }}>
              <LogOut size={11} />
            </button>
          </div>
        </header>

        <main className="console-scope" style={{ flex: 1, overflowY: "auto",
          background: "var(--bg-app)", userSelect: "text",
          padding: "var(--page-pad-y) var(--page-pad-x)" }}>
          <div className="vedha-page-container">{children}</div>
        </main>

        <footer style={{ height: 26, flexShrink: 0, background: "var(--bg-panel)",
          borderTop: "0.5px solid var(--border-subtle)", display: "flex",
          alignItems: "center", justifyContent: "flex-end", padding: "0 18px" }}>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: 9,
            color: "var(--text-muted)" }}>
            <FooterClock /> · VEDHA Secure Portal
          </div>
        </footer>
      </div>
    </div>
  );
}

/* Leaf clocks own their own 1s interval, so a tick re-renders only the clock —
   not the whole shell and its children — every second. */
function FooterClock() {
  const [utc, setUtc] = useState("");
  useEffect(() => {
    const tick = () => setUtc(new Date().toISOString().replace("T", " ").slice(0, 19) + " UTC");
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);
  return <>{utc}</>;
}
