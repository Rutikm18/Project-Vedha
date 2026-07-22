"use client";

import React, { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Network, Activity, Shield, Cpu, Clock, type LucideIcon,
} from "lucide-react";
import { PageShell } from "../components/PageShell";
import { DashboardCharts } from "../components/DashboardCharts";
import { LiveOverview } from "../components/dashboard/LiveOverview";
import { SlaStatus } from "../components/dashboard/SlaStatus";
import { ProtocolRiskCard, ZoneHealthCard } from "../components/dashboard/Exposure";
import { DataState, SkeletonRows, EmptyState } from "../components/states/DataState";
import { fetchJson } from "../lib/fetcher";
import { useMouseGradient } from "../hooks/useMouseGradient";

/* Attack-path, SLA, protocol-risk and zone-health analytics are being migrated
   off the old static mock data onto real backend endpoints. Until each endpoint
   ships, its widget renders an honest "coming soon" state — a security console
   must never present fabricated numbers as live state. */
type AgentStatus = "ACTIVE" | "THINKING" | "IDLE";

/* ─── Agent type ─── */
interface Agent { name: string; status: AgentStatus; activity: string; }

const AGENT_STATUS: Record<AgentStatus, { color: string; glow: string; pulse: boolean }> = {
  ACTIVE:   { color: "var(--accent)",           glow: "var(--accent-glow)",         pulse: true  },
  THINKING: { color: "var(--sev-high-color)",   glow: "var(--sev-high-glow)",       pulse: true  },
  IDLE:     { color: "var(--text-muted)",       glow: "transparent",                pulse: false },
};

/* ─── Sub-components ─── */
function SectionHeader({ icon, title, action, delay = 0 }: { icon: React.ReactNode; title: string; action?: React.ReactNode; delay?: number }) {
  return (
    <div className="stagger-item" style={{ animationDelay: `${delay}ms`, display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ color: "var(--accent)", display: "flex", transition: "transform 0.2s var(--ease-spring)" }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.transform = "scale(1.2) rotate(-5deg)"; }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.transform = "scale(1) rotate(0deg)"; }}
        >
          {icon}
        </div>
        <span style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, fontWeight: 600, color: "var(--text-primary)" }}>
          {title}
        </span>
      </div>
      {action}
    </div>
  );
}

/* Honest placeholder for analytics whose backend endpoint hasn't shipped yet.
   Keeps the widget's frame + heading so the layout is stable, but shows a clear
   "coming soon" message instead of mock numbers. */
function WidgetPlaceholder({ icon, title, hint }: { icon: LucideIcon; title: string; hint: string }) {
  return <div style={{ padding: 24 }}><EmptyState icon={icon} title={title} hint={hint} /></div>;
}

/* ─── Animated card wrapper with mouse glow ─── */
function GlowCard({ children, delay = 0, style }: { children: React.ReactNode; delay?: number; style?: React.CSSProperties }) {
  const { ref, onMouseMove, onMouseLeave } = useMouseGradient<HTMLDivElement>();
  const [hovered, setHovered] = useState(false);

  return (
    <div
      ref={ref}
      onMouseMove={onMouseMove}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => { onMouseLeave(); setHovered(false); }}
      className="stagger-item dashboard-card"
      style={{
        animationDelay: `${delay}ms`,
        background: "var(--bg-panel)",
        border: `0.5px solid ${hovered ? "var(--border-strong)" : "var(--border-subtle)"}`,
        borderRadius: 8,
        overflow: "hidden",
        position: "relative",
        transition: "border-color 0.18s ease, transform 0.18s var(--ease-out), box-shadow 0.2s ease",
        transform: hovered ? "translateY(-2px)" : "translateY(0)",
        boxShadow: hovered ? "var(--shadow-md)" : "var(--shadow-sm)",
        ...style,
      }}
    >
      {/* Mouse-follow glow overlay */}
      <div style={{
        position: "absolute", inset: 0, borderRadius: "inherit",
        pointerEvents: "none", zIndex: 0,
        opacity: hovered ? 0.35 : 0,
        transition: "opacity 0.2s ease",
        background: "radial-gradient(circle at var(--glow-x, 50%) var(--glow-y, 50%), var(--accent-glow) 0%, transparent 65%)",
      } as React.CSSProperties} />
      <div style={{ position: "relative", zIndex: 1, height: "100%" }}>
        {children}
      </div>
    </div>
  );
}

/* ─── Dashboard ─── */
/* One agent/probe row — extracted so its hover state is a proper top-level hook
   (calling useState inside .map breaks when the live agent count changes). */
function AgentRow({ agent, index, isLast }: { agent: Agent; index: number; isLast: boolean }) {
  const as_ = AGENT_STATUS[agent.status];
  const [rowHovered, setRowHovered] = useState(false);
  return (
    <div className="stagger-item"
      style={{
        animationDelay: `${300 + index * 40}ms`,
        display: "flex", alignItems: "center", gap: 12,
        padding: "13px 20px",
        borderBottom: isLast ? "none" : "0.5px solid var(--border-subtle)",
        transition: "background 0.12s ease",
        background: rowHovered ? "var(--bg-surface)" : "transparent",
        cursor: "default",
      }}
      onMouseEnter={() => setRowHovered(true)}
      onMouseLeave={() => setRowHovered(false)}
    >
      <div className="status-dot">
        {as_.pulse && (
          <span className="status-dot-ring" style={{ background: as_.glow, opacity: rowHovered ? 1 : 0.6, transition: "opacity 0.2s ease" }} />
        )}
        <span className={`status-dot-core ${as_.pulse ? "animate-pulse-dot" : ""}`} style={{ background: as_.color, width: 7, height: 7 }} />
      </div>
      <div style={{ minWidth: 0, flex: 1 }}>
        <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, fontWeight: 500, color: "var(--text-primary)", marginBottom: 2 }}>{agent.name}</div>
        <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-muted)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{agent.activity}</div>
      </div>
      <span style={{
        fontFamily: "'Inter', sans-serif", fontSize: 10, fontWeight: 700, color: as_.color,
        background: as_.pulse ? `color-mix(in srgb, ${as_.color} 12%, transparent)` : "var(--bg-hover)",
        borderRadius: 5, padding: "2px 7px", flexShrink: 0,
        transition: "transform 0.18s var(--ease-spring)", transform: rowHovered ? "scale(1.06)" : "scale(1)",
      }}>{agent.status}</span>
    </div>
  );
}

export default function Dashboard() {
  // Live probe/agent data (replaces the previous simulated count + mock list).
  const agentsQuery = useQuery({
    queryKey: ["agents"],
    // The BFF returns a bare array of UI-shaped agents (see /api/agents/register).
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
  const agentsOnline = agents.filter((a) => a.status !== "IDLE").length;

  // SLA breach count for the header chip — shares the ["sla-summary"] query key
  // with <SlaStatus/>, so React Query serves both from one deduped request.
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
      title="Dashboard"
      subtitle="Security Overview"
      statusItems={statusItems}
    >
      <div className="dashboard-stack">

        {/* LIVE situational awareness — real data from the API (not mock) */}
        <LiveOverview />

        {/* KPIs + Charts */}
        <DashboardCharts />

        {/* ── Attack Paths + Agent Monitor ── */}
        <div className="dashboard-main-grid">

          {/* Attack Paths */}
          <div>
            <SectionHeader delay={200} icon={<Network size={15} />} title="Attack Paths" />
            <GlowCard delay={240}>
              <WidgetPlaceholder
                icon={Network}
                title="Attack-path analysis coming soon"
                hint="Global attack-path aggregation isn't wired yet. Open an engagement's Attack Paths tab for per-engagement graphs."
              />
            </GlowCard>
          </div>

          {/* Agent Monitor */}
          <div>
            <SectionHeader delay={220} icon={<Cpu size={15} />} title="Agent Monitor" />
            <GlowCard delay={260} style={{ height: "auto" }}>
              <DataState
                loading={agentsQuery.isLoading}
                error={agentsQuery.error}
                isEmpty={agents.length === 0}
                onRetry={() => agentsQuery.refetch()}
                skeleton={<div style={{ padding: 16 }}><SkeletonRows rows={4} height={44} /></div>}
                empty={<div style={{ padding: 24 }}><EmptyState icon={Cpu} title="No probes connected" hint="Deploy a probe to see live agent activity here." /></div>}
              >
                {agents.map((agent, i) => (
                  <AgentRow key={`${agent.name}-${i}`} agent={agent} index={i} isLast={i === agents.length - 1} />
                ))}
              </DataState>
            </GlowCard>
          </div>
        </div>

        {/* ── SLA + Protocol + Zone ── */}
        <div className="dashboard-triple-grid">

          {/* SLA Tracker */}
          <div>
            <SectionHeader delay={360} icon={<Clock size={15} />} title="SLA Status" />
            <GlowCard delay={400}>
              <SlaStatus />
            </GlowCard>
          </div>

          {/* Protocol Risk */}
          <div>
            <SectionHeader delay={380} icon={<Activity size={15} />} title="Protocol Risk" />
            <GlowCard delay={420}>
              <ProtocolRiskCard />
            </GlowCard>
          </div>

          {/* Zone Health */}
          <div>
            <SectionHeader delay={400} icon={<Shield size={15} />} title="Zone Health" />
            <GlowCard delay={440}>
              <ZoneHealthCard />
            </GlowCard>
          </div>
        </div>

      </div>
    </PageShell>
  );
}
