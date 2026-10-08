"use client";

import React from "react";
import { DashboardCharts } from "../DashboardCharts";
import { PageShell } from "../PageShell";
import { PortalShell } from "../portal/PortalShell";
import { DashboardGrid } from "./DashboardGrid";
import { useConsoleQuery, useConsoleSource } from "../../lib/console-source";

interface AgentStatus { status?: string }
interface SlaPayload { summary?: { breached?: number; totalTracked?: number } }

/** The complete dashboard UI and header logic. The route pages only choose the
 * authenticated data source; every visual, status and interaction lives here. */
export function DashboardWorkspace() {
  const source = useConsoleSource();
  const agentsQuery = useConsoleQuery<AgentStatus[]>("agents", { refetchInterval: 15_000 });
  const slaQuery = useConsoleQuery<SlaPayload>("sla", { refetchInterval: 60_000 });

  const agents = agentsQuery.data ?? [];
  const agentsOnline = agents.filter((agent) => agent.status === "ONLINE" || agent.status === "BUSY").length;
  const breached = slaQuery.data?.summary?.breached ?? 0;
  const tracked = slaQuery.data?.summary?.totalTracked ?? 0;
  const statusItems = [
    {
      label: "AGENTS",
      value: (agentsQuery.isLoading || agentsQuery.error) ? "—" : `${agentsOnline}/${agents.length}`,
      color: (agentsQuery.isLoading || agentsQuery.error) ? "var(--text-faint)" : "var(--accent)",
      ariaLabel: agentsQuery.error ? "Agent status unavailable" : agentsQuery.isLoading ? "Agent status loading" : `${agentsOnline} of ${agents.length} agents online`,
    },
    {
      label: "SLA",
      value: (slaQuery.isLoading || slaQuery.error) ? "—" : tracked === 0 ? "NONE TRACKED" : breached > 0 ? `${breached} BREACHED` : "ON TRACK",
      color: (slaQuery.isLoading || slaQuery.error) ? "var(--text-faint)" : breached > 0 ? "var(--sev-critical-color)" : "var(--accent)",
      ariaLabel: slaQuery.error ? "S L A status unavailable" : slaQuery.isLoading ? "S L A status loading" : breached > 0
        ? `${breached} findings past their remediation deadline`
        : tracked === 0 ? "No S L A tracked findings" : "All tracked findings within their remediation deadline",
    },
  ];

  const content = (
    <div className="console-scope" style={{ display: "flex", flexDirection: "column" }}>
      {(agentsQuery.error || slaQuery.error) && <div role="status" className="ui-recovery">
        {agentsQuery.error && "Agent status unavailable. "}{slaQuery.error && "SLA status unavailable. "}
        Last known data may be out of date. <button type="button" className="btn btn-secondary" onClick={() => { void agentsQuery.refetch(); void slaQuery.refetch(); }}>Retry status</button>
      </div>}
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
          <h2 id="trends-heading" style={{
            margin: 0,
            fontFamily: "var(--font-display)",
            fontSize: 16,
            fontWeight: 650,
            letterSpacing: "-0.015em",
            color: "var(--text-primary)",
          }}>
            Trends and response queue
          </h2>
          <p style={{ margin: "var(--space-1) 0 0", color: "var(--text-muted)", fontSize: "var(--fs-body-s)" }}>
            Historical movement, highest-risk work, and the latest assessment activity.
          </p>
        </div>
        <DashboardCharts />
      </section>
    </div>
  );

  const shellProps = {
    title: "Operations overview",
    subtitle: source.scopeLabel,
    statusItems,
    children: content,
  };
  return source.mode === "portal" ? <PortalShell {...shellProps} live /> : <PageShell {...shellProps} />;
}
