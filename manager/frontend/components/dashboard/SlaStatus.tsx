// manager/frontend/components/dashboard/SlaStatus.tsx
"use client";

/**
 * SlaStatus — remediation clock, per finding.
 *
 * Design decisions:
 *  - The four state counts are buttons, not decoration. On a real console the
 *    first thing anyone does after seeing "6 breached" is try to see those six;
 *    making the number the control removes a step instead of adding a filter
 *    bar somewhere else.
 *  - Rows are ordered worst-first (breached → at risk → due soon → on track,
 *    then by time remaining). An SLA list sorted by anything else makes the
 *    reader do the triage the software should have done.
 *  - The bar fills as time is *consumed*, so a full bar always means "out of
 *    time" regardless of what the policy window was.
 *
 * The server decides state, deadline and hours remaining. This component never
 * recomputes a deadline from the clock: client drift would silently disagree
 * with the policy engine.
 */
import React, { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Clock } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { SEVERITY, Severity, toSeverity } from "../../lib/severity";
import { SeverityChip, Meter } from "../console/Primitives";

type SlaState = "breached" | "at_risk" | "due_soon" | "on_track";

interface SlaItem {
  id: string; title: string; severity: Severity;
  deadline: string | null; hoursRemaining: number | null;
  hoursTotal: number | null; state: SlaState;
}
interface SlaSummary {
  summary: { breached: number; atRisk: number; dueSoon: number; onTrack: number; totalTracked: number };
  items: SlaItem[];
}

const STATE: Record<SlaState, { label: string; color: string; bg: string; edge: string; rank: number }> = {
  breached: { label: "Breached", color: "var(--sev-critical-color)", bg: "var(--sev-critical-bg)", edge: "var(--sev-critical-edge)", rank: 0 },
  at_risk:  { label: "At risk",  color: "var(--sev-high-color)",     bg: "var(--sev-high-bg)",     edge: "var(--sev-high-edge)",     rank: 1 },
  due_soon: { label: "Due soon", color: "var(--sev-medium-color)",   bg: "var(--sev-medium-bg)",   edge: "var(--sev-medium-edge)",   rank: 2 },
  on_track: { label: "On track", color: "var(--accent)",             bg: "var(--accent-bg)",       edge: "var(--accent-edge)",       rank: 3 },
};

const VISIBLE_ROWS = 8;

/** Time left, or "Overdue" once the window has closed. */
function timeLabel(item: SlaItem): string {
  if (item.state === "breached") return "Overdue";
  const h = item.hoursRemaining ?? 0;
  if (h < 1) return "<1h";
  if (h < 24) return `${Math.round(h)}h`;
  if (h < 24 * 14) return `${Math.round(h / 24)}d`;
  return `${Math.round(h / 168)}w`;
}

/** Share of the SLA window already consumed. 100 = out of time. */
function elapsedPct(item: SlaItem): number {
  if (item.state === "breached") return 100;
  if (!item.hoursTotal || item.hoursRemaining == null) return 0;
  return Math.max(0, Math.min(100, ((item.hoursTotal - item.hoursRemaining) / item.hoursTotal) * 100));
}

function deadlineTitle(item: SlaItem): string | undefined {
  if (!item.deadline) return undefined;
  const d = new Date(item.deadline);
  return Number.isNaN(d.getTime()) ? undefined : `Due ${d.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" })}`;
}

/* ----------------------------------------------------------- state button */

function StateCell({
  state, value, active, onToggle, isLast,
}: { state: SlaState; value: number; active: boolean; onToggle: () => void; isLast: boolean }) {
  const st = STATE[state];
  const disabled = value === 0;
  return (
    <button
      type="button"
      onClick={onToggle}
      disabled={disabled}
      aria-pressed={active}
      className="focusable"
      style={{
        flex: 1, minWidth: 84, minHeight: 68, padding: "13px 12px",
        display: "flex", flexDirection: "column", alignItems: "center", gap: 5,
        background: active ? st.bg : "transparent",
        border: "none",
        borderRight: isLast ? "none" : "0.5px solid var(--border-subtle)",
        borderBottom: `2px solid ${active ? st.color : "transparent"}`,
        cursor: disabled ? "default" : "pointer",
        transition: "background var(--dur-fast) var(--ease-out)",
        font: "inherit",
      }}
    >
      <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
        {state === "breached" && value > 0 && <span className="pulse-dot" aria-hidden />}
        <span
          className="num"
          style={{
            fontFamily: "var(--font-display)", fontSize: 24, fontWeight: 650, lineHeight: 1,
            color: disabled ? "var(--text-faint)" : st.color,
          }}
        >
          {value}
        </span>
      </span>
      <span style={{ fontFamily: "var(--font-ui)", fontSize: 10.5, fontWeight: 500, color: "var(--text-muted)" }}>
        {st.label}
      </span>
      {!disabled && <span className="sr-only">{active ? "Showing only" : "Show only"} {st.label.toLowerCase()} findings</span>}
    </button>
  );
}

/* ---------------------------------------------------------------- one row */

function SlaRowView({ item }: { item: SlaItem }) {
  const st = STATE[item.state];
  const pct = elapsedPct(item);
  const sevKey = toSeverity(item.severity);

  return (
    <div
      className="console-row"
      style={{
        "--rail": st.color,
        display: "flex", alignItems: "center", gap: 12, padding: "11px 20px 11px 22px",
      } as React.CSSProperties}
      title={deadlineTitle(item)}
    >
      <SeverityChip severity={sevKey} />

      <div style={{ flex: 1, minWidth: 0 }}>
        <div
          style={{
            fontFamily: "var(--font-ui)", fontSize: 12.5, color: "var(--text-primary)",
            whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", marginBottom: 6,
          }}
        >
          {item.title}
        </div>
        <Meter
          value={pct}
          color={st.color}
          height={3}
          ticks
          pulse={item.state === "breached"}
          label={`${SEVERITY[sevKey].label} finding, ${st.label.toLowerCase()} — ${Math.round(pct)}% of the remediation window used`}
        />
      </div>

      <span
        className="num-mono"
        style={{ fontSize: 11, fontWeight: 700, color: st.color, flexShrink: 0, minWidth: 60, textAlign: "right", letterSpacing: "-0.01em" }}
      >
        {timeLabel(item)}
      </span>
    </div>
  );
}

/* ----------------------------------------------------------------- card */

export function SlaStatus() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["sla-summary"],
    queryFn: () => fetchJson<SlaSummary>("/api/findings/sla-summary"),
    refetchInterval: 60_000,
  });

  const [filter, setFilter] = useState<SlaState | null>(null);
  const [expanded, setExpanded] = useState(false);

  const items = useMemo(() => data?.items ?? [], [data?.items]);
  const ordered = useMemo(
    () =>
      [...items].sort(
        (a, b) =>
          STATE[a.state].rank - STATE[b.state].rank ||
          (a.hoursRemaining ?? Infinity) - (b.hoursRemaining ?? Infinity) ||
          SEVERITY[toSeverity(a.severity)].rank - SEVERITY[toSeverity(b.severity)].rank
      ),
    [items]
  );
  const shown = useMemo(
    () => (filter ? ordered.filter((i) => i.state === filter) : ordered),
    [ordered, filter]
  );

  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={4} height={44} /></div>;
  if (error) return <ErrorState title="SLA status didn't load. The findings API returned an error." onRetry={() => refetch()} />;

  const s = data?.summary;
  if (!s || s.totalTracked === 0) {
    return (
      <div style={{ padding: 28 }}>
        <EmptyState
          icon={Clock}
          title="Nothing under SLA yet"
          hint="Open and confirmed findings show up here with the clock running on their remediation deadline."
        />
      </div>
    );
  }

  const counts: Record<SlaState, number> = {
    breached: s.breached, at_risk: s.atRisk, due_soon: s.dueSoon, on_track: s.onTrack,
  };
  const visible = expanded ? shown : shown.slice(0, VISIBLE_ROWS);
  const hidden = shown.length - visible.length;

  return (
    <>
      <div
        role="group"
        aria-label="Filter by SLA state"
        style={{ display: "flex", borderBottom: "0.5px solid var(--border-subtle)", background: "var(--bg-surface)" }}
      >
        {(Object.keys(STATE) as SlaState[]).map((k, i, arr) => (
          <StateCell
            key={k}
            state={k}
            value={counts[k]}
            active={filter === k}
            onToggle={() => { setFilter(filter === k ? null : k); setExpanded(false); }}
            isLast={i === arr.length - 1}
          />
        ))}
      </div>

      {filter && (
        <div
          style={{
            display: "flex", alignItems: "center", gap: 10, padding: "8px 20px",
            borderBottom: "0.5px solid var(--border-subtle)",
            fontFamily: "var(--font-ui)", fontSize: 11.5, color: "var(--text-muted)",
          }}
        >
          Showing {shown.length} {STATE[filter].label.toLowerCase()}
          <button
            type="button"
            className="focusable"
            onClick={() => setFilter(null)}
            style={{ marginLeft: "auto", background: "none", border: "none", padding: "4px 2px", color: "var(--accent)", cursor: "pointer", font: "inherit" }}
          >
            Clear filter
          </button>
        </div>
      )}

      {visible.map((it) => <SlaRowView key={it.id} item={it} />)}

      {hidden > 0 && (
        <button
          type="button"
          className="focusable"
          onClick={() => setExpanded(true)}
          style={{
            width: "100%", minHeight: 44, padding: "12px 20px", background: "none",
            border: "none", borderTop: "0.5px solid var(--border-subtle)",
            color: "var(--accent)", cursor: "pointer",
            fontFamily: "var(--font-ui)", fontSize: 12, textAlign: "left",
          }}
        >
          Show {hidden} more
        </button>
      )}
    </>
  );
}
