"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { PageShell } from "../components/PageShell";
import { DashboardGrid } from "../components/dashboard/DashboardGrid";
import { DashboardCharts } from "../components/DashboardCharts";
import { fetchJson } from "../lib/fetcher";

/* The dashboard body is the redesigned console (DashboardGrid): live ledger,
   posture dial, SLA clock, patch matrix, exposure meters, and the live agent
   monitor. DashboardCharts (KPI/trend/donut + critical-findings table +
   activity feed) is retained below it so no operational data is lost.

   Note: DashboardCharts' KPI cards overlap the new ledger's open-findings and
   engagement counts — a deliberate, flagged redundancy to trim in a follow-up
   rather than delete real data here. */
export default function Dashboard() {
  // Live probe count for the header status chip. Shares the ["agents"] key with
  // the Agent Monitor panel, so React Query serves both from one request.
  const agentsQuery = useQuery({
    queryKey: ["agents"],
    queryFn: () => fetchJson<any[]>("/api/agents/register"),
    refetchInterval: 15_000,
  });
  const agents = agentsQuery.data ?? [];
  const agentsOnline = agents.filter((a: any) => a?.status === "ONLINE" || a?.status === "BUSY").length;

  // SLA breach count for the header chip — shares the ["sla-summary"] key with
  // <SlaStatus/>, so both come from one deduped request.
  const slaQuery = useQuery({
    queryKey: ["sla-summary"],
    queryFn: () => fetchJson<{ summary?: { breached: number; totalTracked: number } }>("/api/findings/sla-summary"),
    refetchInterval: 60_000,
  });
  const breached = slaQuery.data?.summary?.breached ?? 0;
  const tracked = slaQuery.data?.summary?.totalTracked ?? 0;

  const statusItems = [
    { label: "AGENTS", value: `${agentsOnline}/${agents.length}`, color: "var(--accent)" },
    ...(tracked > 0
      ? [{
          label: "SLA",
          value: breached > 0 ? `${breached} BREACHED` : "ON TRACK",
          color: breached > 0 ? "var(--sev-critical-color)" : "var(--accent)",
        }]
      : []),
  ];

  return (
    <PageShell
      title="Security posture"
      subtitle="Executive exposure, remediation urgency, and assessment health"
      statusItems={statusItems}
    >
      <div className="console-scope" style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        <DashboardGrid />
        <DashboardCharts />
      </div>
    </PageShell>
  );
}
