"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { PageShell } from "../components/PageShell";
import { DashboardGrid } from "../components/dashboard/DashboardGrid";
import { DashboardCharts } from "../components/DashboardCharts";
import { fetchJson } from "../lib/fetcher";
import { OperatorConsoleProvider, consoleQueryKey } from "../lib/console-source";

/* The dashboard body is the redesigned console (DashboardGrid): live ledger,
   posture dial, SLA clock, patch matrix, exposure meters, and the live agent
   monitor. DashboardCharts keeps only non-duplicated signals below it: assets,
   validation count, historical trend, highest-risk findings, and activity. */
export default function Dashboard() {
  // Live probe count for the header status chip. It must use the SAME key the
  // Agent Monitor panel does, or React Query treats them as two datasets and
  // fetches the identical endpoint twice. Since the panels moved behind the
  // console seam, that key comes from consoleQueryKey — hand-writing ["agents"]
  // here silently doubled the request.
  const agentsQuery = useQuery({
    queryKey: consoleQueryKey("operator", "agents"),
    queryFn: () => fetchJson<any[]>("/api/agents/register"),
    refetchInterval: 15_000,
  });
  const agents = agentsQuery.data ?? [];
  const agentsOnline = agents.filter((a: any) => a?.status === "ONLINE" || a?.status === "BUSY").length;

  // SLA breach count for the header chip — shares <SlaStatus/>'s cache entry, so
  // both come from one deduped request.
  const slaQuery = useQuery({
    queryKey: consoleQueryKey("operator", "sla"),
    queryFn: () => fetchJson<{ summary?: { breached: number; totalTracked: number } }>("/api/findings/sla-summary"),
    refetchInterval: 60_000,
  });
  const breached = slaQuery.data?.summary?.breached ?? 0;
  const tracked = slaQuery.data?.summary?.totalTracked ?? 0;

  const agentsLoading = agentsQuery.isLoading;
  const slaLoading = slaQuery.isLoading;

  const statusItems = [
    {
      label: "AGENTS",
      value: agentsLoading ? "—" : `${agentsOnline}/${agents.length}`,
      color: agentsLoading ? "var(--text-faint)" : "var(--accent)",
      ariaLabel: agentsLoading
        ? "Agent status loading"
        : `${agentsOnline} of ${agents.length} agents online`,
    },
    {
      label: "SLA",
      value: slaLoading ? "—"
        : tracked === 0 ? "NONE TRACKED"
        : breached > 0 ? `${breached} BREACHED`
        : "ON TRACK",
      color: slaLoading ? "var(--text-faint)"
        : breached > 0 ? "var(--sev-critical-color)"
        : "var(--accent)",
      ariaLabel: slaLoading
        ? "S L A status loading"
        : breached > 0
          ? `${breached} findings past their remediation deadline`
          : "All tracked findings within their remediation deadline",
    },
  ];

  return (
    <PageShell
      title="Operations overview"
      subtitle="Open exposure, remediation clock, and fleet health"
      statusItems={statusItems}
    >
      <OperatorConsoleProvider>
      <div className="console-scope" style={{ display: "flex", flexDirection: "column" }}>
        <DashboardGrid />

        <section
          aria-labelledby="trends-heading"
          style={{
            marginTop: "var(--space-7)",
            paddingTop: "var(--space-6)",
            borderTop: "var(--hairline) solid var(--border-strong)",
          }}
        >
          <div style={{ marginBottom: "var(--space-4)" }}>
            <h2
              id="trends-heading"
              style={{
                margin: 0,
                fontFamily: "var(--font-display)",
                fontSize: 16,
                fontWeight: 650,
                letterSpacing: "-0.015em",
                color: "var(--text-primary)",
              }}
            >
              Trends and response queue
            </h2>
            <p style={{ margin: "var(--space-1) 0 0", color: "var(--text-muted)", fontSize: "var(--fs-body-s)" }}>
              Historical movement, highest-risk work, and the latest assessment activity.
            </p>
          </div>
          <DashboardCharts />
        </section>
      </div>
      </OperatorConsoleProvider>
    </PageShell>
  );
}
