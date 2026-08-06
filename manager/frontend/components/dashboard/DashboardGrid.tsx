// manager/frontend/components/dashboard/DashboardGrid.tsx
"use client";

/**
 * Dashboard composition.
 *
 * Layout is a hierarchy argument, not a packing problem. Tiers:
 *   1. Ledger      — full bleed. What is open, right now.
 *   2. Posture     — wide left, clock right. Are we winning, and what is late.
 *   3. Exposure    — three equal panels. Where the risk sits.
 *   4. Fleet       — live probe/agent state (kept from the previous dashboard;
 *                    it's real-time operational data the ledger doesn't cover).
 * Nothing below tier 1 competes with tier 1 for attention: smaller type, no
 * display numerals above 26px, no colour outside severity and state.
 *
 * The grid collapses at 1100px (two columns) and 720px (one), and every panel
 * is min-width:0 so long asset names truncate instead of forcing a scrollbar.
 */
import React, { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { Gauge, Timer, Activity, Shield, GitCompareArrows, Cpu } from "lucide-react";
import { Panel } from "../console/Primitives";
import { DataState, SkeletonRows, EmptyState } from "../states/DataState";
import { fetchJson } from "../../lib/fetcher";
import { LiveOverview } from "./LiveOverview";
import { PostureScorecard } from "./PostureScorecard";
import { SlaStatus } from "./SlaStatus";
import { PatchComparisonMatrix } from "./PatchComparisonMatrix";
import { ProtocolRiskCard, ZoneHealthCard } from "./ExposureCards";

/* ------------------------------------------------------------ Agent monitor
   Ported from the previous dashboard so live probe/agent state is preserved.
   Restyled onto the console-row primitive for visual parity with the redesign. */

type AgentStatus = "ACTIVE" | "THINKING" | "IDLE";
interface Agent { name: string; status: AgentStatus; activity: string }

const AGENT_STATUS: Record<AgentStatus, { color: string; label: string; pulse: boolean }> = {
  ACTIVE:   { color: "var(--nominal-color)",     label: "Online",  pulse: true  },
  THINKING: { color: "var(--sev-high-color)",    label: "Working", pulse: true  },
  IDLE:     { color: "var(--text-muted)",        label: "Offline", pulse: false },
};

function AgentRow({ agent }: { agent: Agent }) {
  const st = AGENT_STATUS[agent.status];
  return (
    <div className="console-row" style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 20px" }}>
      <span
        style={{
          width: 8, height: 8, borderRadius: 999, flexShrink: 0, background: st.color,
          boxShadow: st.pulse ? `0 0 0 3px color-mix(in srgb, ${st.color} 22%, transparent)` : "none",
        }}
        aria-hidden
      />
      <div style={{ minWidth: 0, flex: 1 }}>
        <div style={{ fontFamily: "var(--font-ui)", fontSize: 12.5, fontWeight: 500, color: "var(--text-primary)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {agent.name}
        </div>
        <div style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-muted)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {agent.activity}
        </div>
      </div>
      <span
        className="chip"
        style={{ color: st.color, background: "color-mix(in srgb, " + st.color + " 12%, transparent)", flexShrink: 0 }}
      >
        {st.label}
      </span>
    </div>
  );
}

function AgentMonitor() {
  const agentsQuery = useQuery({
    queryKey: ["agents"],
    queryFn: () => fetchJson<any[]>("/api/agents/register"),
    refetchInterval: 15_000,
  });
  const agents: Agent[] = useMemo(
    () => (agentsQuery.data ?? []).map((a: any) => ({
      name: a.name ?? "probe",
      status: a.status === "BUSY" ? "THINKING" : a.status === "ONLINE" ? "ACTIVE" : "IDLE",
      activity: a.currentJobId
        ? `Running job ${String(a.currentJobId).slice(0, 8)}`
        : a.status === "ONLINE" ? "Online — ready"
        : a.status === "BUSY" ? "Working…"
        : "Offline",
    })),
    [agentsQuery.data],
  );

  return (
    <DataState
      loading={agentsQuery.isLoading}
      error={agentsQuery.error}
      isEmpty={agents.length === 0}
      onRetry={() => agentsQuery.refetch()}
      skeleton={<div style={{ padding: 16 }}><SkeletonRows rows={3} height={44} /></div>}
      empty={<div style={{ padding: 24 }}><EmptyState icon={Cpu} title="No probes connected" hint="Deploy a probe to see live agent activity here." /></div>}
    >
      {agents.map((a, i) => <AgentRow key={`${a.name}-${i}`} agent={a} />)}
    </DataState>
  );
}

/* ------------------------------------------------------------------- grid */

export function DashboardGrid() {
  return (
    <>
      <style>{`
        .console-grid {
          display: grid;
          gap: 16px;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          align-items: start;
        }
        .console-grid > .span-2 { grid-column: span 2; }
        .console-grid > .span-3 { grid-column: span 3; }
        @media (max-width: 1100px) {
          .console-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .console-grid > .span-3 { grid-column: span 2; }
        }
        @media (max-width: 720px) {
          .console-grid { grid-template-columns: minmax(0, 1fr); }
          .console-grid > .span-2,
          .console-grid > .span-3 { grid-column: span 1; }
        }
      `}</style>

      <div className="console-grid">
        <div className="span-3"><LiveOverview /></div>

        <div className="span-2">
          <Panel title="Security posture" eyebrow="Latest scan" icon={<Gauge size={13} />} note="refreshes every minute">
            <PostureScorecard />
          </Panel>
        </div>

        <Panel title="Remediation SLA" eyebrow="Clock running" icon={<Timer size={13} />}>
          <SlaStatus />
        </Panel>

        <Panel title="Scan-to-scan change" eyebrow="Previous vs latest" icon={<GitCompareArrows size={13} />}>
          <PatchComparisonMatrix />
        </Panel>

        <Panel title="Protocol risk" eyebrow="Exposed services" icon={<Activity size={13} />}>
          <ProtocolRiskCard />
        </Panel>

        <Panel title="Zone health" eyebrow="By environment" icon={<Shield size={13} />}>
          <ZoneHealthCard />
        </Panel>

        <div className="span-3">
          <Panel title="Agent monitor" eyebrow="Live probe fleet" icon={<Cpu size={13} />}>
            <AgentMonitor />
          </Panel>
        </div>
      </div>
    </>
  );
}
