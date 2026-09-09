"use client";

import React, { useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  LayoutDashboard,
  Bug,
  Radar,
  FileText,
  Settings,
  Briefcase,
  Sparkles,
  Cpu,
} from "lucide-react";
import { PageShell } from "../PageShell";
import { Sidebar, type SidebarNavSection } from "../Sidebar";
import { usePortalEngagement } from "../../lib/portal-client";

const PORTAL_NAV_SECTIONS: SidebarNavSection[] = [
  {
    label: "OPERATIONS",
    items: [
      { icon: LayoutDashboard, label: "Dashboard", href: "/portal", exact: true },
      { icon: Radar, label: "Scanner", href: "/portal/scans" },
      { icon: Cpu, label: "Fleet", href: "/portal/fleet" },
      { icon: Briefcase, label: "Engagement", href: "/portal/scope" },
    ],
  },
  {
    label: "ANALYSIS",
    items: [
      { icon: Sparkles, label: "AI Brain", href: "/portal/assistant" },
      { icon: Bug, label: "Findings", href: "/portal/findings" },
    ],
  },
  {
    label: "MANAGEMENT",
    items: [
      { icon: FileText, label: "Reports", href: "/portal/reports", badge: "BETA" },
      { icon: Settings, label: "Settings", href: "/portal/settings" },
    ],
  },
];

interface PortalShellProps {
  title: string;
  subtitle?: string;
  headerActions?: React.ReactNode;
  statusItems?: Array<{ label: string; value: string; color?: string; ariaLabel?: string }>;
  /** Indicates that engagement work is actively running. */
  live?: boolean;
  children: React.ReactNode;
  noPadding?: boolean;
  hideRefresh?: boolean;
}

function EngagementContext({ name, status }: { name?: string; status?: string }) {
  if (!name) return null;

  const isActive = status?.toLowerCase() === "active";
  return (
    <section
      aria-label="Current engagement"
      style={{
        padding: "10px 16px",
        borderBottom: "0.5px solid var(--border-subtle)",
        flexShrink: 0,
      }}
    >
      <div style={{
        fontSize: 9,
        fontWeight: 700,
        color: "var(--text-faint)",
        letterSpacing: 1.4,
        textTransform: "uppercase",
        marginBottom: 6,
      }}>
        Current engagement
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
        <span style={{
          width: 7,
          height: 7,
          borderRadius: "50%",
          flexShrink: 0,
          background: isActive ? "var(--nominal-color)" : "var(--text-muted)",
          boxShadow: isActive ? "0 0 5px var(--nominal-color)" : "none",
        }} />
        <div style={{ minWidth: 0 }}>
          <div style={{
            fontSize: 12,
            fontWeight: 600,
            color: "var(--text-primary)",
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}>
            {name}
          </div>
          {status && (
            <div style={{
              fontSize: 10,
              color: "var(--text-muted)",
              textTransform: "capitalize",
              marginTop: 1,
            }}>
              {status}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

/**
 * Customer engagement shell. It deliberately composes the same PageShell and
 * Sidebar as the manager console; only navigation, identity, and auth differ.
 */
export function PortalShell({ live = false, ...props }: PortalShellProps) {
  const router = useRouter();
  const engagement = usePortalEngagement();

  const logout = useCallback(async () => {
    await fetch("/api/portal/logout", {
      method: "POST",
      credentials: "same-origin",
    }).catch(() => {});
    router.replace("/portal/login");
    router.refresh();
  }, [router]);

  return (
    <PageShell
      {...props}
      manageOperatorSession={false}
      userLabel="Customer"
      onLogout={logout}
      footerLabel="VEDHA Customer Workspace"
      contentClassName="console-scope"
      renderSidebar={({ open, onClose }) => (
        <Sidebar
          open={open}
          onClose={onClose}
          sections={PORTAL_NAV_SECTIONS}
          editionLabel="Customer"
          statusLabel={live ? "Work running" : "Engagement workspace"}
          context={(
            <EngagementContext
              name={engagement.data?.name}
              status={engagement.data?.status}
            />
          )}
        />
      )}
    />
  );
}
