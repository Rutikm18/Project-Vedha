// manager/frontend/components/dashboard/DashboardGrid.tsx
"use client";

/**
 * Dashboard composition.
 *
 * Layout is a hierarchy argument, not a packing problem. Tiers:
 *   1. Ledger      — full bleed. What is open, right now.
 *   2. Posture     — posture and scan change left, clock right. Are we winning,
 *                    what changed, and what is late.
 *   2b. Attack paths (Beta, operator console only) — how an attacker could reach the
 *                    crown jewels and what to fix first, per engagement. Absent on the
 *                    customer console.
 *   3. Exposure    — two equal panels. Where the risk sits.
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
import { useQueryClient } from "@tanstack/react-query";
import {
  Activity,
  AlertOctagon,
  CheckCircle2,
  ClockAlert,
  Cpu,
  Gauge,
  GitCompareArrows,
  Route,
  Shield,
  Timer,
  WifiOff,
} from "lucide-react";
import { Panel } from "../console/Primitives";
import { Freshness } from "../console/Freshness";
import { DataState, SkeletonRows, EmptyState } from "../states/DataState";
import { useConsoleCapability, useConsolePath, useConsoleQuery, useConsoleQueryKey, type ConsoleKey } from "../../lib/console-source";
import { LiveOverview } from "./LiveOverview";
import { PostureScorecard, usePostureScope } from "./PostureScorecard";
import { SlaStatus } from "./SlaStatus";
import { PatchComparisonMatrix } from "./PatchComparisonMatrix";
import { ProtocolRiskCard, ZoneHealthCard } from "./ExposureCards";
import { AttackPathsPanel } from "./AttackPathsPanel";
import { attackPathAttention, type Overview } from "../../lib/attack-paths";

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

interface AttentionFindingSummary { criticalOpen?: number; highOpen?: number }
interface AttentionSlaSummary { summary?: { breached?: number; atRisk?: number } }

function NeedsAttention({ onOpen }: { onOpen: (href: string) => void }) {
  const findingsPath = useConsolePath("findings");
  const fleetPath = useConsolePath("fleet");
  // Operator console only (the customer console has no such dataset). The same cached query the Attack paths
  // section reads, so this adds no request. Its failure is NOT counted below: the section says so itself, and
  // "urgent work cannot be assessed" is about measured signals.
  const canSeeAttackPaths = useConsoleCapability("viewAttackPaths");
  const attackPaths = useConsoleQuery<Overview>("attackPaths", { refetchInterval: 120_000, enabled: canSeeAttackPaths });
  const attackPathItem = canSeeAttackPaths ? attackPathAttention(attackPaths.data?.summary) : null;
  const findings = useConsoleQuery<AttentionFindingSummary>("findingsSummary", { refetchInterval: 60_000 });
  const sla = useConsoleQuery<AttentionSlaSummary>("sla", { refetchInterval: 60_000 });
  const agents = useConsoleQuery<Array<{ status?: string }>>("agents", { refetchInterval: 15_000 });

  const loading = findings.isLoading || sla.isLoading || agents.isLoading;
  const failed = [findings.error, sla.error, agents.error].filter(Boolean).length;
  const critical = findings.data?.criticalOpen ?? 0;
  const breached = sla.data?.summary?.breached ?? 0;
  const offline = (agents.data ?? []).filter((agent) => !["ONLINE", "BUSY"].includes(agent.status ?? "")).length;
  const items = [
    critical > 0 ? {
      label: `${critical} critical ${critical === 1 ? "finding" : "findings"}`,
      detail: "Triage and contain first",
      tone: "var(--sev-critical-color)",
      icon: AlertOctagon,
      href: `${findingsPath}?severity=CRITICAL&status=open`,
    } : null,
    breached > 0 ? {
      label: `${breached} SLA ${breached === 1 ? "breach" : "breaches"}`,
      detail: "Past remediation target",
      tone: "var(--sev-high-color)",
      icon: ClockAlert,
      href: `${findingsPath}?sla=breached`,
    } : null,
    offline > 0 ? {
      label: `${offline} ${offline === 1 ? "probe" : "probes"} offline`,
      detail: "Coverage may be incomplete",
      tone: "var(--sev-medium-color)",
      icon: WifiOff,
      href: fleetPath,
    } : null,
    // Last: a Beta model's reading never outranks something measured.
    attackPathItem ? {
      label: attackPathItem.label,
      detail: attackPathItem.detail,
      tone: attackPathItem.tone === "high" ? "var(--sev-high-color)" : "var(--sev-medium-color)",
      icon: Route,
      href: attackPathItem.href,
    } : null,
  ].filter(Boolean) as Array<{
    label: string; detail: string; tone: string; icon: React.ElementType; href: string;
  }>;

  if (loading && items.length === 0) {
    return (
      <section className="attention-strip attention-strip--loading" aria-label="Loading urgent work" aria-busy="true">
        <SkeletonRows rows={1} height={58} />
      </section>
    );
  }

  return (
    <section
      className="attention-strip"
      data-clear={(items.length === 0 && failed === 0) || undefined}
      aria-labelledby="attention-title"
    >
      <div className="attention-strip__intro">
        <span className="attention-strip__icon" aria-hidden>
          {items.length > 0 || failed > 0 ? <AlertOctagon size={16} /> : <CheckCircle2 size={16} />}
        </span>
        <div>
          <h2 id="attention-title">Needs attention now</h2>
          <p>
            {items.length > 0
              ? `Evidence-backed work ordered by immediate operational impact.${attackPathItem ? " Items marked Beta are modelled, not measured." : ""}`
              : failed > 0 ? "Urgent work cannot be fully assessed while signals are unavailable." : "No critical findings, SLA breaches, or offline probes are recorded."}
          </p>
        </div>
      </div>

      {items.length > 0 && (
        <div className="attention-strip__items">
          {items.map(({ label, detail, tone, icon: Icon, href }) => (
            <button key={href} type="button" title={`${label}. ${detail}`} onClick={() => onOpen(href)} style={{ "--attention-tone": tone } as React.CSSProperties}>
              <Icon size={15} aria-hidden />
              <span><strong>{label}</strong><small>{detail}</small></span>
            </button>
          ))}
        </div>
      )}
      {failed > 0 && (
        <span className="attention-strip__partial" role="status">
          {failed} live {failed === 1 ? "signal is" : "signals are"} temporarily unavailable.
        </span>
      )}
    </section>
  );
}

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
  const agentsQuery = useConsoleQuery<any[]>("agents", { refetchInterval: 15_000 });
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
function FreshNote({ dataset, staleAfterMs }: { dataset: ConsoleKey; staleAfterMs?: number }) {
  const st = useQueryClient().getQueryState(useConsoleQueryKey(dataset));
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
  const findingsPath = useConsolePath("findings");
  // Operator-only (Beta): the customer console has no attack-path view, so it gets no panel at all.
  const showAttackPaths = useConsoleCapability("viewAttackPaths");
  // Posture + patch comparison are the only per-engagement panels here; on a
  // multi-engagement console they must say which engagement, or an unlabelled
  // grade reads as the tenant's. Null on the customer console (one engagement,
  // already named in the header).
  const postureScope = usePostureScope();
  const postureEyebrow = postureScope ? `Latest scan · ${postureScope}` : "Latest scan";
  const matrixEyebrow = postureScope
    ? `Previous vs latest · ${postureScope}`
    : "Previous vs latest";
  return (
    <>
      <style>{`
        .console-band {
          display: grid;
          gap: var(--space-4);
          align-items: stretch;
          margin-bottom: var(--space-4);
        }
        .console-band:last-of-type { margin-bottom: 0; }
        .console-band > * { min-width: 0; }
        .console-band > * > .panel,
        .console-band > .panel { height: 100%; }

        .band-1 { grid-template-columns: minmax(0, 1fr); }
        .band-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start; }
        .band-2__stack { display: grid; min-width: 0; gap: var(--space-4); }
        .band-2__stack > .panel,
        .band-2 > .panel { height: auto; }
        .band-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .band-4 { grid-template-columns: minmax(0, 1fr); }

        @media (max-width: 900px) {
          .band-2, .band-3 { grid-template-columns: minmax(0, 1fr); }
        }
        @media (max-width: 640px) {
          .console-band { gap: var(--space-3); margin-bottom: var(--space-3); }
          .band-2__stack { gap: var(--space-3); }
          .console-band:last-of-type { margin-bottom: 0; }
        }
      `}</style>

      <NeedsAttention onOpen={(href) => router.push(href)} />

      <div className="console-band band-1">
        <LiveOverview
          onSelectSeverity={(s) => router.push(`${findingsPath}?severity=${s}&status=open`)}
        />
      </div>

      <div className="console-band band-2">
        <div className="band-2__stack">
          <Panel title="Security posture" eyebrow={postureEyebrow} icon={<Gauge size={13} />} headingLevel={3} note={<FreshNote dataset="posture" />}>
            <PostureScorecard />
          </Panel>
          <Panel title="Scan-to-scan change" eyebrow={matrixEyebrow} icon={<GitCompareArrows size={13} />} headingLevel={3} note={<FreshNote dataset="posture" />}>
            <PatchComparisonMatrix />
          </Panel>
        </div>
        <Panel title="Remediation SLA" eyebrow="Clock running" icon={<Timer size={13} />} headingLevel={3} note={<FreshNote dataset="sla" />}>
          {/* SlaStatus reads useSearchParams() for its shareable ?sla= filter; that
              API bails static prerender unless wrapped in a Suspense boundary (Next 15). */}
          <React.Suspense fallback={<div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={4} height={46} /></div>}>
            <SlaStatus />
          </React.Suspense>
        </Panel>
      </div>

      {showAttackPaths && (
        <div className="console-band band-4">
          <Panel
            title="Attack paths"
            eyebrow="How an attacker could reach your crown jewels"
            icon={<Route size={13} />}
            headingLevel={3}
            note={<><span className="badge badge-info" title="Attack paths is in beta">Beta</span> <FreshNote dataset="attackPaths" staleAfterMs={300_000} /></>}
          >
            <AttackPathsPanel />
          </Panel>
        </div>
      )}

      <div className="console-band band-3">
        <Panel title="Protocol risk" eyebrow="Worst finding on each exposed service" icon={<Activity size={13} />} headingLevel={3} note={<FreshNote dataset="exposure" />}>
          <ProtocolRiskCard />
        </Panel>
        <Panel title="Zone health" eyebrow="Headroom per zone · higher is better · weakest first" icon={<Shield size={13} />} headingLevel={3} note={<FreshNote dataset="exposure" />}>
          <ZoneHealthCard />
        </Panel>
      </div>

      <div className="console-band band-4">
        <Panel title="Agent monitor" eyebrow="Live vedha-agent fleet" icon={<Cpu size={13} />} headingLevel={3} note={<FreshNote dataset="agents" staleAfterMs={60_000} />}>
          <AgentMonitor />
        </Panel>
      </div>
    </>
  );
}
