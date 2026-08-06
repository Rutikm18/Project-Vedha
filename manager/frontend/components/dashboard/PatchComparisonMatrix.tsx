// manager/frontend/components/dashboard/PatchComparisonMatrix.tsx
"use client";

/**
 * PatchComparisonMatrix — what actually changed between the last two scans.
 *
 * This is a ledger, so it stays a table: an analyst reads down a column to
 * find where risk moved, and cards or bars would break that. What the redesign
 * adds is hierarchy inside the table — zeros drop back to a faint tone so the
 * non-zero cells carry the eye, "New" and "Patched" are the only coloured
 * columns because they are the only ones describing movement, and Δ is a chip
 * rather than a bare arrow so its meaning survives greyscale.
 *
 * Shares the /api/analytics/posture query key with PostureScorecard — one
 * request feeds both.
 */
import React from "react";
import { GitCompareArrows } from "lucide-react";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { usePosture, MatrixRow } from "./PostureScorecard";
import { SEVERITY, toSeverity } from "../../lib/severity";
import { Meter } from "../console/Primitives";

const cell: React.CSSProperties = {
  padding: "9px 10px",
  textAlign: "right",
  fontFamily: "var(--font-mono)",
  fontVariantNumeric: "tabular-nums",
  fontSize: 12,
  color: "var(--text-primary)",
};

const head: React.CSSProperties = {
  ...cell,
  fontFamily: "var(--font-ui)",
  fontSize: 9.5,
  fontWeight: 600,
  letterSpacing: "0.09em",
  textTransform: "uppercase",
  color: "var(--text-muted)",
  paddingBottom: 8,
};

/** Zeros recede so the eye lands on movement. */
function n(v: number, color?: string): React.CSSProperties {
  return { ...cell, color: v === 0 ? "var(--text-faint)" : color ?? "var(--text-primary)" };
}

function NetChip({ net }: { net: number }) {
  if (net === 0) {
    return <span className="chip num" style={{ color: "var(--text-faint)", background: "transparent" }}>0</span>;
  }
  const better = net < 0;
  return (
    <span
      className="chip num"
      style={{
        color: better ? "var(--nominal-color)" : "var(--sev-high-color)",
        background: better ? "var(--nominal-bg)" : "var(--sev-high-bg)",
        borderColor: better ? "var(--nominal-edge)" : "var(--sev-high-edge)",
      }}
    >
      <span aria-hidden>{better ? "↓" : "↑"}</span>
      {Math.abs(net)}
      <span className="sr-only">{better ? "fewer than" : "more than"} the previous scan</span>
    </span>
  );
}

export function PatchComparisonMatrix() {
  const { data, isLoading, error, refetch } = usePosture();

  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={5} height={34} /></div>;
  if (error) return <ErrorState title="Patch comparison didn't load. The analytics service returned an error." onRetry={() => refetch()} />;
  if (!data?.has_runs || !data.matrix) {
    return (
      <div style={{ padding: 28 }}>
        <EmptyState
          icon={GitCompareArrows}
          title="Nothing to compare yet"
          hint="A patch comparison needs two completed scans on the same scope."
        />
      </div>
    );
  }

  const rows = data.matrix
    .filter((r) => r.prev_open || r.new || r.resolved || r.now_open)
    .sort((a, b) => SEVERITY[toSeverity(a.severity)].rank - SEVERITY[toSeverity(b.severity)].rank);

  if (rows.length === 0) {
    return (
      <div style={{ padding: 28 }}>
        <EmptyState icon={GitCompareArrows} title="No change between scans" hint="Neither scan found open findings on this scope." />
      </div>
    );
  }

  const totals = rows.reduce(
    (acc, r) => ({
      prev_open: acc.prev_open + r.prev_open,
      new: acc.new + r.new,
      resolved: acc.resolved + r.resolved,
      now_open: acc.now_open + r.now_open,
      net: acc.net + r.net,
    }),
    { prev_open: 0, new: 0, resolved: 0, now_open: 0, net: 0 }
  );

  const closedShare = totals.prev_open > 0 ? (totals.resolved / totals.prev_open) * 100 : 0;

  return (
    <div style={{ padding: "12px 16px 6px" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <caption className="sr-only">
          Findings by severity, comparing the previous scan with the latest scan.
        </caption>
        <thead>
          <tr>
            <th scope="col" style={{ ...head, textAlign: "left" }}>Severity</th>
            <th scope="col" style={head}>Was</th>
            <th scope="col" style={head}>New</th>
            <th scope="col" style={head}>Patched</th>
            <th scope="col" style={head}>Now</th>
            <th scope="col" style={{ ...head, paddingRight: 0 }}>Net</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r: MatrixRow) => {
            const k = toSeverity(r.severity);
            const m = SEVERITY[k];
            return (
              <tr key={r.severity} style={{ borderTop: "0.5px solid var(--border-subtle)" }}>
                <th
                  scope="row"
                  style={{
                    ...cell, textAlign: "left", fontFamily: "var(--font-ui)", fontWeight: 600,
                    color: "var(--text-primary)", paddingLeft: 0,
                  }}
                >
                  <span style={{ display: "inline-flex", alignItems: "center", gap: 7 }}>
                    <span aria-hidden style={{ color: m.color, fontSize: 9 }}>{m.sigil}</span>
                    {m.label}
                  </span>
                </th>
                <td style={n(r.prev_open, "var(--text-secondary)")}>{r.prev_open}</td>
                <td style={n(r.new, "var(--sev-high-color)")}>{r.new}</td>
                <td style={n(r.resolved, "var(--nominal-color)")}>{r.resolved}</td>
                <td style={n(r.now_open)}>{r.now_open}</td>
                <td style={{ ...cell, paddingRight: 0 }}><NetChip net={r.net} /></td>
              </tr>
            );
          })}
          <tr style={{ borderTop: "0.5px solid var(--border-strong)" }}>
            <th scope="row" style={{ ...head, textAlign: "left", paddingLeft: 0, paddingTop: 10, color: "var(--text-secondary)" }}>
              All severities
            </th>
            <td style={{ ...n(totals.prev_open, "var(--text-secondary)"), paddingTop: 10 }}>{totals.prev_open}</td>
            <td style={{ ...n(totals.new, "var(--sev-high-color)"), paddingTop: 10 }}>{totals.new}</td>
            <td style={{ ...n(totals.resolved, "var(--nominal-color)"), paddingTop: 10 }}>{totals.resolved}</td>
            <td style={{ ...n(totals.now_open), paddingTop: 10, fontWeight: 700 }}>{totals.now_open}</td>
            <td style={{ ...cell, paddingRight: 0, paddingTop: 10 }}><NetChip net={totals.net} /></td>
          </tr>
        </tbody>
      </table>

      {/* ---- what the numbers add up to, in one line ---------------------- */}
      <div style={{ marginTop: 14, paddingTop: 12, borderTop: "0.5px solid var(--border-subtle)", display: "flex", flexDirection: "column", gap: 8 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
          <span className="eyebrow">Closed since last scan</span>
          <span className="num-mono" style={{ marginLeft: "auto", fontSize: 12, fontWeight: 700, color: "var(--nominal-color)" }}>
            {Math.round(closedShare)}%
          </span>
        </div>
        <Meter
          value={closedShare}
          color="var(--nominal-color)"
          height={4}
          label={`${totals.resolved} of ${totals.prev_open} previously open findings patched`}
        />
        <p style={{ margin: 0, fontFamily: "var(--font-ui)", fontSize: 11.5, color: "var(--text-muted)", lineHeight: 1.5 }}>
          {totals.resolved} patched, {totals.new} newly found
          {typeof data.persisting_count === "number" ? `, ${data.persisting_count} still open from before` : ""}.
          {typeof data.risk_burned_down === "number" && data.risk_burned_down > 0 && (
            <>
              {" "}Risk burned down:{" "}
              <span className="num-mono" style={{ color: "var(--nominal-color)", fontWeight: 700 }}>
                {Math.round(data.risk_burned_down)}
              </span>
              .
            </>
          )}
        </p>
      </div>
    </div>
  );
}
