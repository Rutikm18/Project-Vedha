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
import { useRouter } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Gauge, Timer, Activity, Shield, GitCompareArrows, Cpu } from "lucide-react";
import { Panel } from "../console/Primitives";
import { Freshness } from "../console/Freshness";
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

type AgentStatus = "ONLINE" | "BUSY" | "OFFLINE";
interface Agent { id?: string; name: string; status: AgentStatus; activity: string }

const AGENT_STATUS: Record<AgentStatus, { color: string; label: string; pulse: boolean }> = {
  ONLINE:  { color: "var(--nominal-color)", label: "Online",  pulse: false },
  BUSY:    { color: "var(--state-busy)",    label: "Busy",    pulse: true  },
  OFFLINE: { color: "var(--text-muted)",    label: "Offline", pulse: false },
};

function AgentRow({ agent }: { agent: Agent }) {
  const st = AGENT_STATUS[agent.status];
  return (
    <div className="console-row" style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", padding: "var(--space-3) var(--space-5)" }}>
      <span
        style={{
          width: 8, height: 8, borderRadius: 999, flexShrink: 0, background: st.color,
          boxShadow: st.pulse ? `0 0 0 3px color-mix(in srgb, ${st.color} 22%, transparent)` : "none",
        }}
        aria-hidden
      />
      <div style={{ minWidth: 0, flex: 1 }}>
        <div style={{ fontFamily: "var(--font-ui)", fontSize: "var(--fs-body)", fontWeight: 500, color: "var(--text-primary)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {agent.name}
        </div>
        <div style={{ fontFamily: "var(--font-ui)", fontSize: "var(--fs-label)", color: "var(--text-muted)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
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
  const [agentsExpanded, setAgentsExpanded] = React.useState(false);
  const agents: Agent[] = useMemo(
    () => (agentsQuery.data ?? []).map((a: any): Agent => ({
      id: a.id,
      name: a.name ?? "probe",
      status: a.status === "BUSY" ? "BUSY" : a.status === "ONLINE" ? "ONLINE" : "OFFLINE",
      activity: a.currentJobId
        ? `Running job ${String(a.currentJobId).slice(0, 8)}`
        : a.status === "ONLINE" ? "Idle — ready for work"
        : a.status === "BUSY" ? "Running a job"
        : "Not connected",
    }))
    .sort((a, b) =>
      ({ BUSY: 0, ONLINE: 1, OFFLINE: 2 }[a.status] - { BUSY: 0, ONLINE: 1, OFFLINE: 2 }[b.status])
      || a.name.localeCompare(b.name)),
    [agentsQuery.data],
  );

  return (
    <DataState
      loading={agentsQuery.isLoading}
      error={agentsQuery.error}
      isEmpty={agents.length === 0}
      onRetry={() => agentsQuery.refetch()}
      skeleton={<div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={3} height={52} /></div>}
      empty={<div style={{ padding: "var(--space-6)" }}><EmptyState icon={Cpu} title="No vedha-agents connected" hint="Deploy a vedha-agent to see live agent activity here." /></div>}
    >
      <ul role="list" style={{ listStyle: "none", margin: 0, padding: 0 }}>
        {agents.slice(0, agentsExpanded ? undefined : 6).map((a) => (
          <li key={a.id ?? a.name}><AgentRow agent={a} /></li>
        ))}
      </ul>
      {agents.length > 6 && (
        <button type="button" className="focusable" onClick={() => setAgentsExpanded((v) => !v)}
          style={{ width: "100%", minHeight: 44, padding: "var(--space-3) var(--space-5)",
            background: "none", border: "none", borderTop: "var(--hairline) solid var(--border-subtle)",
            color: "var(--accent)", cursor: "pointer", fontFamily: "var(--font-ui)",
            fontSize: "var(--fs-body-s)", textAlign: "left" }}>
          {agentsExpanded ? "Show fewer" : `Show all ${agents.length}`}
        </button>
      )}
    </DataState>
  );
}

/* ------------------------------------------------------------------- grid */

/** Reads a query's freshness straight from the React Query cache — no new
 *  subscription/fetch (spec: do not add a useQuery). Renders into a Panel note. */
function FreshNote({ qk, staleAfterMs }: { qk: unknown[]; staleAfterMs?: number }) {
  const st = useQueryClient().getQueryState(qk);
  if (!st?.dataUpdatedAt) return null;
  return (
    <Freshness
      updatedAt={st.dataUpdatedAt}
      isFetching={st.fetchStatus === "fetching"}
      staleAfterMs={staleAfterMs}
    />
  );
}

export function DashboardGrid() {
  const router = useRouter();
  return (
    <>
      <style>{`
        .console-band {
          display: grid;
          gap: var(--space-4);
          align-items: stretch;
          margin-bottom: var(--space-4);
        }
        .console-band > * { min-width: 0; }
        .console-band > * > .panel,
        .console-band > .panel { height: 100%; }

        .band-1 { grid-template-columns: minmax(0, 1fr); }
        .band-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .band-3 { grid-template-columns: minmax(340px, 1.35fr) minmax(240px, 1fr) minmax(240px, 1fr); }
        .band-4 { grid-template-columns: minmax(0, 1fr); }

        @media (max-width: 1280px) {
          .band-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .band-3 > :first-child { grid-column: span 2; }
        }
        @media (max-width: 900px) {
          .band-2, .band-3 { grid-template-columns: minmax(0, 1fr); }
          .band-3 > :first-child { grid-column: span 1; }
        }
        @media (max-width: 640px) {
          .console-band { gap: var(--space-3); margin-bottom: var(--space-3); }
        }
      `}</style>

      <div className="console-band band-1">
        <LiveOverview
          onSelectSeverity={(s) => router.push(`/findings?severity=${s}&status=open`)}
        />
      </div>

      <div className="console-band band-2">
        <Panel title="Security posture" eyebrow="Latest scan" icon={<Gauge size={13} />} headingLevel={3} note={<FreshNote qk={["posture"]} />}>
          <PostureScorecard />
        </Panel>
        <Panel title="Remediation SLA" eyebrow="Clock running" icon={<Timer size={13} />} headingLevel={3} note={<FreshNote qk={["sla-summary"]} />}>
          {/* SlaStatus reads useSearchParams() for its shareable ?sla= filter; that
              API bails static prerender unless wrapped in a Suspense boundary (Next 15). */}
          <React.Suspense fallback={<div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={4} height={46} /></div>}>
            <SlaStatus />
          </React.Suspense>
        </Panel>
      </div>

      <div className="console-band band-3">
        <Panel title="Scan-to-scan change" eyebrow="Previous vs latest" icon={<GitCompareArrows size={13} />} headingLevel={3} note={<FreshNote qk={["posture"]} />}>
          <PatchComparisonMatrix />
        </Panel>
        <Panel title="Protocol risk" eyebrow="Worst finding per service · higher is worse" icon={<Activity size={13} />} headingLevel={3} note={<FreshNote qk={["exposure"]} />}>
          <ProtocolRiskCard />
        </Panel>
        <Panel title="Zone health" eyebrow="Headroom per zone · higher is better · weakest first" icon={<Shield size={13} />} headingLevel={3} note={<FreshNote qk={["exposure"]} />}>
          <ZoneHealthCard />
        </Panel>
      </div>

      <div className="console-band band-4">
        <Panel title="Agent monitor" eyebrow="Live vedha-agent fleet" icon={<Cpu size={13} />} headingLevel={3} note={<FreshNote qk={["agents"]} staleAfterMs={60_000} />}>
          <AgentMonitor />
        </Panel>
      </div>
    </>
  );
}
