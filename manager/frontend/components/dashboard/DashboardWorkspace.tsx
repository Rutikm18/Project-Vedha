"use client";

import React from "react";
import { PageShell } from "../PageShell";
import { PortalShell } from "../portal/PortalShell";
import { DashboardCharts } from "../DashboardCharts";
import { DashboardGrid } from "./DashboardGrid";
import {
  OperatorConsoleProvider,
  PortalConsoleProvider,
  useConsoleQuery,
} from "../../lib/console-source";

export type DashboardSurface = "manager" | "portal";

function DashboardContent({ surface }: { surface: DashboardSurface }) {
  const agentsQuery = useConsoleQuery<Array<{ status?: string }>>("agents", {
    refetchInterval: 15_000,
  });
  const slaQuery = useConsoleQuery<{
    summary?: { breached: number; totalTracked: number };
  }>("sla", { refetchInterval: 60_000 });

  const agents = agentsQuery.data ?? [];
  const agentsOnline = agents.filter(
    (agent) => agent.status === "ONLINE" || agent.status === "BUSY",
  ).length;
  const breached = slaQuery.data?.summary?.breached ?? 0;
  const tracked = slaQuery.data?.summary?.totalTracked ?? 0;
  const Shell = surface === "portal" ? PortalShell : PageShell;

  return (
    <Shell
      title="Operations overview"
      subtitle="Open exposure, remediation clock, and fleet health"
      statusItems={[
        {
          label: "AGENTS",
          value: agentsQuery.isLoading ? "—" : `${agentsOnline}/${agents.length}`,
          color: agentsQuery.isLoading ? "var(--text-faint)" : "var(--accent)",
          ariaLabel: agentsQuery.isLoading
            ? "Agent status loading"
            : `${agentsOnline} of ${agents.length} agents online`,
        },
        {
          label: "SLA",
          value: slaQuery.isLoading
            ? "—"
            : tracked === 0
              ? "NONE TRACKED"
              : breached > 0
                ? `${breached} BREACHED`
                : "ON TRACK",
          color: slaQuery.isLoading
            ? "var(--text-faint)"
            : breached > 0
              ? "var(--sev-critical-color)"
              : "var(--accent)",
          ariaLabel: slaQuery.isLoading
            ? "S L A status loading"
            : breached > 0
              ? `${breached} findings past their remediation deadline`
              : "All tracked findings within their remediation deadline",
        },
      ]}
    >
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
            <p style={{
              margin: "var(--space-1) 0 0",
              color: "var(--text-muted)",
              fontSize: "var(--fs-body-s)",
            }}>
              Historical movement, highest-risk work, and the latest assessment activity.
            </p>
          </div>
          <DashboardCharts />
        </section>
      </div>
    </Shell>
  );
}

export function DashboardWorkspace({
  surface = "manager",
  scopeLabel,
}: {
  surface?: DashboardSurface;
  scopeLabel?: string;
}) {
  if (surface === "portal") {
    return (
      <PortalConsoleProvider scopeLabel={scopeLabel}>
        <DashboardContent surface="portal" />
      </PortalConsoleProvider>
    );
  }
  return (
    <OperatorConsoleProvider>
      <DashboardContent surface="manager" />
    </OperatorConsoleProvider>
  );
}
