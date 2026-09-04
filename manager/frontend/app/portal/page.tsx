"use client";

/**
 * Portal → Dashboard. The SAME console the operator sees, scoped to this
 * customer's one engagement.
 *
 * There is deliberately almost no layout code here. The body is
 * <DashboardGrid/> + <DashboardCharts/> — the very components app/page.tsx
 * renders — wrapped in PortalConsoleProvider, which points their data lookups at
 * /api/portal/* instead of the operator API. FastAPI pins those routes to the
 * caller's engagement, and the portal routes delegate to the operator handlers,
 * so the response shapes are identical and one component can render either side.
 *
 * The consequence, which was the whole point: a change to the operator dashboard
 * appears here automatically. If you find yourself copying a panel into this
 * file, add it to the shared component and give it an endpoint in both providers
 * instead — a copy diverges the first time either side is edited.
 *
 * Panels with no customer-scoped equivalent (the engagement switcher) resolve to
 * `unavailable` through the source and omit themselves; they are not errors.
 */

import React from "react";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { Radar } from "lucide-react";
import { PortalShell } from "../../components/portal/PortalShell";
import { DashboardGrid } from "../../components/dashboard/DashboardGrid";
import { DashboardCharts } from "../../components/DashboardCharts";
import { PortalConsoleProvider } from "../../lib/console-source";
import { portalApi, usePortalEngagement, type PortalSummary } from "../../lib/portal-client";

export default function PortalOverview() {
  const eng = usePortalEngagement();
  const summary = useQuery({
    queryKey: ["portal", "summary"],
    queryFn: () => portalApi<PortalSummary>("/summary"),
    refetchInterval: 60_000,
  });

  const running = summary.data?.running_jobs ?? 0;
  const statusItems = [
    {
      label: "OPEN",
      value: summary.data ? String(summary.data.open_findings) : "—",
      color: (summary.data?.open_findings ?? 0) > 0
        ? "var(--sev-high-color)" : "var(--accent)",
    },
    {
      label: "SCANS",
      value: running > 0 ? `${running} RUNNING` : "IDLE",
      color: running > 0 ? "var(--accent)" : "var(--text-faint)",
    },
  ];

  const requestAction = (
    <Link href="/portal/scans" className="btn btn-primary"
      style={{ height: 30, padding: "0 12px", fontSize: 12, textDecoration: "none" }}>
      <Radar style={{ width: 14, height: 14 }} /> Request scan
    </Link>
  );

  return (
    <PortalShell
      title="Overview"
      subtitle={eng.data?.name ?? "Your security posture"}
      statusItems={statusItems}
      headerActions={requestAction}
      live={running > 0}
    >
      <PortalConsoleProvider scopeLabel={eng.data?.name}>
        <div className="console-scope" style={{ display: "flex", flexDirection: "column" }}>
          <DashboardGrid />

          <section
            aria-labelledby="portal-trends-heading"
            style={{
              marginTop: "var(--space-7)",
              paddingTop: "var(--space-6)",
              borderTop: "var(--hairline) solid var(--border-strong)",
            }}
          >
            <h2
              id="portal-trends-heading"
              style={{
                margin: "0 0 var(--space-4)",
                fontFamily: "var(--font-ui)",
                fontSize: "var(--fs-body)",
                fontWeight: 600,
                letterSpacing: "0.08em",
                textTransform: "uppercase",
                color: "var(--text-muted)",
              }}
            >
              Trends and activity
            </h2>
            <DashboardCharts />
          </section>
        </div>
      </PortalConsoleProvider>
    </PortalShell>
  );
}
