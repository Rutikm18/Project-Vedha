"use client";

/**
 * PostureScorecard — the dashboard headline for security posture.
 *
 * Reads /api/analytics/posture (backend services/posture.py is authoritative;
 * this only formats). Shows Posture Score + grade, plus Risk Index and
 * Exploitable Score, each with a prev→now delta arrow.
 */
import React from "react";
import { useQuery } from "@tanstack/react-query";
import { ShieldCheck, TrendingDown, TrendingUp, Minus } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";

export interface Scores {
  risk_index: number; exploitable_score: number; posture_score: number; grade: string;
}
export interface MatrixRow {
  severity: string; prev_open: number; new: number; resolved: number; now_open: number; net: number;
}
export interface Posture {
  has_runs: boolean;
  scores?: Scores;
  scores_prev?: Scores | null;
  matrix?: MatrixRow[];
  risk_burned_down?: number;
  resolved_count?: number; new_count?: number; persisting_count?: number;
}

export function usePosture() {
  return useQuery({
    queryKey: ["posture"],
    queryFn: () => fetchJson<Posture>("/api/analytics/posture"),
    refetchInterval: 60_000,
  });
}

const GRADE_COLOR: Record<string, string> = {
  A: "var(--nominal-color)", B: "var(--accent)", C: "var(--sev-medium-color)",
  D: "var(--sev-high-color)", F: "var(--sev-critical-color)",
};

/** Delta arrow. `improvedWhenLower` flips arrow meaning for risk-type metrics. */
function Delta({ now, prev, improvedWhenLower }: { now?: number; prev?: number; improvedWhenLower: boolean }) {
  if (prev == null || now == null) return null;
  const diff = Math.round((now - prev) * 10) / 10;
  if (diff === 0) return <span style={{ color: "var(--text-muted)", display: "inline-flex", alignItems: "center", gap: 2 }}><Minus size={12} /> 0</span>;
  const better = improvedWhenLower ? diff < 0 : diff > 0;
  const color = better ? "var(--nominal-color)" : "var(--sev-high-color)";
  const Icon = diff < 0 ? TrendingDown : TrendingUp;
  return <span style={{ color, display: "inline-flex", alignItems: "center", gap: 2, fontSize: 12 }}><Icon size={12} /> {Math.abs(diff)}</span>;
}

function StatCard({ label, value, delta }: { label: string; value: React.ReactNode; delta?: React.ReactNode }) {
  return (
    <div style={{ flex: 1, minWidth: 120, padding: 14, borderRadius: 10, background: "var(--bg-hover)", display: "flex", flexDirection: "column", gap: 4 }}>
      <span style={{ fontSize: 11, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: 0.5 }}>{label}</span>
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
        <span style={{ fontSize: 22, fontWeight: 700, color: "var(--text-primary)" }}>{value}</span>
        {delta}
      </div>
    </div>
  );
}

export function PostureScorecard() {
  const { data, isLoading, error, refetch } = usePosture();
  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={2} height={64} /></div>;
  if (error) return <ErrorState title="Couldn't load posture." onRetry={() => refetch()} />;
  if (!data?.has_runs || !data.scores) {
    return <div style={{ padding: 24 }}><EmptyState icon={ShieldCheck} title="No scan history yet" hint="Posture and patch comparison appear after your first completed scan." /></div>;
  }
  const s = data.scores;
  const p = data.scores_prev ?? undefined;
  return (
    <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
      <StatCard
        label="Posture Score"
        value={<span style={{ color: GRADE_COLOR[s.grade] ?? "var(--text-primary)" }}>{s.posture_score} · {s.grade}</span>}
        delta={<Delta now={s.posture_score} prev={p?.posture_score} improvedWhenLower={false} />}
      />
      <StatCard label="Risk Index" value={s.risk_index} delta={<Delta now={s.risk_index} prev={p?.risk_index} improvedWhenLower />} />
      <StatCard label="Exploitable" value={s.exploitable_score} delta={<Delta now={s.exploitable_score} prev={p?.exploitable_score} improvedWhenLower />} />
    </div>
  );
}
