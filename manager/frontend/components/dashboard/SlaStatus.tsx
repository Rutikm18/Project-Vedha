"use client";

/**
 * SlaStatus — live SLA tracker for the dashboard.
 *
 * Renders the tenant's SLA breach/at-risk state from the backend SLA policy
 * engine (/api/findings/sla-summary). The server is authoritative: it decides
 * each finding's state and hours remaining, so this component only formats —
 * it never recomputes deadlines (which would risk drifting from server policy).
 */
import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { Clock } from "lucide-react";

type Sev = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";
type SlaState = "breached" | "at_risk" | "due_soon" | "on_track";

interface SlaItem {
  id: string; title: string; severity: Sev;
  deadline: string | null; hoursRemaining: number | null;
  hoursTotal: number | null; state: SlaState;
}
interface SlaSummary {
  summary: { breached: number; atRisk: number; dueSoon: number; onTrack: number; totalTracked: number };
  items: SlaItem[];
}

const STATE_COLOR: Record<SlaState, string> = {
  breached:  "var(--sev-critical-color)",
  at_risk:   "var(--sev-high-color)",
  due_soon:  "var(--sev-medium-color)",
  on_track:  "var(--accent)",
};

const SEV_STYLE: Record<Sev, { color: string; bg: string }> = {
  CRITICAL: { color: "var(--sev-critical-color)", bg: "var(--sev-critical-bg)" },
  HIGH:     { color: "var(--sev-high-color)",     bg: "var(--sev-high-bg)"     },
  MEDIUM:   { color: "var(--sev-medium-color)",   bg: "var(--sev-medium-bg)"   },
  LOW:      { color: "var(--sev-low-color, var(--accent))", bg: "var(--bg-hover)" },
  INFO:     { color: "var(--text-muted)",         bg: "var(--bg-hover)"         },
};

/** Human label for hours remaining (or how far past due). */
function timeLabel(item: SlaItem): string {
  if (item.state === "breached") return "BREACHED";
  const h = item.hoursRemaining ?? 0;
  if (h < 24) return `${Math.max(0, Math.round(h))}h`;
  return `${Math.round(h / 24)}d`;
}

/** Progress toward the deadline (0 = just started, 100 = due now). */
function pct(item: SlaItem): number {
  if (item.state === "breached") return 100;
  if (!item.hoursTotal || item.hoursRemaining == null) return 0;
  const used = (item.hoursTotal - item.hoursRemaining) / item.hoursTotal;
  return Math.max(0, Math.min(100, used * 100));
}

function SummaryCell({ label, value, color, isLast }: { label: string; value: number; color: string; isLast: boolean }) {
  return (
    <div style={{
      padding: "14px 16px", textAlign: "center",
      borderRight: isLast ? "none" : "0.5px solid var(--border-subtle)",
    }}>
      <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 24, fontWeight: 700, color, lineHeight: 1, marginBottom: 4, fontVariantNumeric: "tabular-nums" }}>
        {value}
      </div>
      <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 10, color: "var(--text-muted)", fontWeight: 500 }}>
        {label}
      </div>
    </div>
  );
}

function SlaRowView({ item, isLast }: { item: SlaItem; isLast: boolean }) {
  const [hovered, setHovered] = useState(false);
  const color = STATE_COLOR[item.state];
  const sev = SEV_STYLE[item.severity] ?? SEV_STYLE.INFO;
  return (
    <div
      style={{
        display: "flex", alignItems: "center", gap: 12, padding: "10px 20px",
        borderBottom: isLast ? "none" : "0.5px solid var(--border-subtle)",
        transition: "background 0.12s ease",
        background: hovered ? "var(--bg-surface)" : "transparent",
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <span style={{
        fontFamily: "'Inter', sans-serif", fontSize: 10, fontWeight: 700, letterSpacing: 0.5,
        color: sev.color, background: sev.bg, borderRadius: 5, padding: "2px 7px",
        flexShrink: 0, textTransform: "uppercase" as const,
      }}>
        {item.severity}
      </span>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 12, color: "var(--text-primary)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", marginBottom: 5 }}>
          {item.title}
        </div>
        <div className="progress-track" style={{ height: 3 }}>
          <div className={`progress-fill ${item.state === "breached" ? "sla-pulse" : ""}`}
            style={{ width: `${pct(item)}%`, background: color }} />
        </div>
      </div>
      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 11, fontWeight: 700, color, flexShrink: 0, minWidth: 56, textAlign: "right" }}>
        {timeLabel(item)}
      </span>
    </div>
  );
}

export function SlaStatus() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["sla-summary"],
    queryFn: () => fetchJson<SlaSummary>("/api/findings/sla-summary"),
    refetchInterval: 60_000,
  });

  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={4} height={40} /></div>;
  if (error) return <ErrorState title="Couldn't load SLA status." onRetry={() => refetch()} />;

  const s = data?.summary;
  const items = data?.items ?? [];

  if (!s || s.totalTracked === 0) {
    return (
      <div style={{ padding: 24 }}>
        <EmptyState icon={Clock} title="No findings under SLA" hint="Open/confirmed findings appear here with their remediation deadlines." />
      </div>
    );
  }

  return (
    <>
      <div className="dashboard-summary-grid" style={{ borderBottom: "0.5px solid var(--border-subtle)", background: "var(--bg-surface)" }}>
        <SummaryCell label="Breached" value={s.breached}  color="var(--sev-critical-color)" isLast={false} />
        <SummaryCell label="At risk"  value={s.atRisk}    color="var(--sev-high-color)"     isLast={false} />
        <SummaryCell label="Due soon" value={s.dueSoon}   color="var(--sev-medium-color)"   isLast={false} />
        <SummaryCell label="On track" value={s.onTrack}   color="var(--accent)"             isLast={true}  />
      </div>
      {items.map((it, i) => (
        <SlaRowView key={it.id} item={it} isLast={i === items.length - 1} />
      ))}
    </>
  );
}
