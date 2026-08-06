// manager/frontend/components/dashboard/PatchComparisonMatrix.tsx
"use client";

/**
 * PatchComparisonMatrix — what changed between the previous and latest scan.
 * Reads the shared /api/analytics/posture payload (same React Query key as the
 * scorecard, so one request feeds both). "Resolved" = present last scan, gone now.
 */
import React from "react";
import { GitCompareArrows } from "lucide-react";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { usePosture, MatrixRow } from "./PostureScorecard";

const SEV_COLOR: Record<string, string> = {
  critical: "var(--sev-critical-color)", high: "var(--sev-high-color)",
  medium: "var(--sev-medium-color)", low: "var(--accent)", info: "var(--text-muted)",
};

function netLabel(net: number): { text: string; color: string } {
  if (net < 0) return { text: `↓${Math.abs(net)}`, color: "var(--nominal-color)" };
  if (net > 0) return { text: `↑${net}`, color: "var(--sev-high-color)" };
  return { text: "0", color: "var(--text-muted)" };
}

export function PatchComparisonMatrix() {
  const { data, isLoading, error, refetch } = usePosture();
  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={5} height={30} /></div>;
  if (error) return <ErrorState title="Couldn't load patch comparison." onRetry={() => refetch()} />;
  if (!data?.has_runs || !data.matrix) {
    return <div style={{ padding: 24 }}><EmptyState icon={GitCompareArrows} title="Nothing to compare yet" hint="A patch comparison needs at least two completed scans." /></div>;
  }
  const rows = data.matrix.filter((r) => r.prev_open || r.new || r.resolved || r.now_open);
  const cell: React.CSSProperties = { padding: "6px 8px", fontSize: 12, textAlign: "right", color: "var(--text-primary)" };
  const head: React.CSSProperties = { ...cell, color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase", fontSize: 10 };
  return (
    <div style={{ padding: "4px 8px" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ ...head, textAlign: "left" }}>Severity</th>
            <th style={head}>Prev</th><th style={head}>New</th>
            <th style={head}>Patched</th><th style={head}>Now</th><th style={head}>Δ</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r: MatrixRow) => {
            const n = netLabel(r.net);
            return (
              <tr key={r.severity} style={{ borderTop: "1px solid var(--border-subtle, rgba(255,255,255,0.06))" }}>
                <td style={{ ...cell, textAlign: "left", color: SEV_COLOR[r.severity], fontWeight: 600, textTransform: "capitalize" }}>{r.severity}</td>
                <td style={cell}>{r.prev_open}</td>
                <td style={cell}>{r.new}</td>
                <td style={{ ...cell, color: "var(--nominal-color)" }}>{r.resolved}</td>
                <td style={cell}>{r.now_open}</td>
                <td style={{ ...cell, color: n.color }}>{n.text}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      {typeof data.risk_burned_down === "number" && data.risk_burned_down > 0 && (
        <div style={{ marginTop: 8, fontSize: 12, color: "var(--text-muted)" }}>
          Risk burned down: <span style={{ color: "var(--nominal-color)", fontWeight: 600 }}>{Math.round(data.risk_burned_down)}</span>
          {" "}({data.resolved_count} patched)
        </div>
      )}
    </div>
  );
}
