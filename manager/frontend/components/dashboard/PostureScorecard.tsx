// manager/frontend/components/dashboard/PostureScorecard.tsx
"use client";

/**
 * PostureScorecard — the one number a security lead reports upward.
 *
 * Design decision: posture gets a dial, not a third stat card. A grade is a
 * position on a bounded 0–100 scale, and a dial is the only shape that shows
 * position and headroom at once — "72 · C" as flat text tells you the score
 * but never how far off an A it is. Risk Index and Exploitable stay as plain
 * readouts beside it, because they are unbounded and a gauge would lie about
 * their ceiling.
 *
 * Backend services/posture.py is authoritative. This component formats only —
 * it never derives a grade or a delta the server didn't send.
 */
import React from "react";
import { useQuery } from "@tanstack/react-query";
import { ShieldCheck } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { Delta } from "../console/Primitives";

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

const GRADE: Record<string, { color: string; bg: string; edge: string; read: string }> = {
  A: { color: "var(--nominal-color)",     bg: "var(--nominal-bg)",     edge: "var(--nominal-edge)",     read: "Strong" },
  B: { color: "var(--accent)",            bg: "var(--accent-bg)",      edge: "var(--accent-edge)",      read: "Acceptable" },
  C: { color: "var(--sev-medium-color)",  bg: "var(--sev-medium-bg)",  edge: "var(--sev-medium-edge)",  read: "Needs work" },
  D: { color: "var(--sev-high-color)",    bg: "var(--sev-high-bg)",    edge: "var(--sev-high-edge)",    read: "Poor" },
  F: { color: "var(--sev-critical-color)",bg: "var(--sev-critical-bg)",edge: "var(--sev-critical-edge)",read: "Failing" },
};

/** 270° dial. pathLength=100 makes the dash maths score-in-percent directly. */
function Dial({ score, color }: { score: number; color: string }) {
  const pct = Math.max(0, Math.min(100, score));
  const ARC = 75; // 270° of a 360° circle, in pathLength units
  return (
    <svg viewBox="0 0 120 120" width={132} height={132} aria-hidden focusable="false" style={{ flexShrink: 0 }}>
      <circle
        cx="60" cy="60" r="46" fill="none" pathLength={100}
        stroke="rgba(128,128,128,0.18)" strokeWidth="7" strokeLinecap="round"
        strokeDasharray={`${ARC} 100`} transform="rotate(135 60 60)"
      />
      <circle
        cx="60" cy="60" r="46" fill="none" pathLength={100}
        stroke={color} strokeWidth="7" strokeLinecap="round"
        strokeDasharray={`${(ARC * pct) / 100} 100`} transform="rotate(135 60 60)"
        style={{ transition: "stroke-dasharray var(--dur-slow) var(--ease-out)" }}
      />
      {/* endpoint marker — the eye lands on it before it reads the number */}
      <circle
        cx="60" cy="14" r="2.6" fill={color}
        transform={`rotate(${135 + (270 * pct) / 100 + 90} 60 60)`}
        style={{ transition: "transform var(--dur-slow) var(--ease-out)" }}
      />
    </svg>
  );
}

function Readout({ label, value, delta, hint }: {
  label: string; value: React.ReactNode; delta?: React.ReactNode; hint: string;
}) {
  return (
    <div
      style={{
        flex: "1 1 130px", minWidth: 130, padding: "13px 15px", borderRadius: "var(--r-md)",
        background: "var(--bg-surface)", border: "0.5px solid var(--border-subtle)",
        display: "flex", flexDirection: "column", gap: 6,
      }}
    >
      <span className="eyebrow">{label}</span>
      <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
        <span className="num" style={{ fontFamily: "var(--font-display)", fontSize: 26, fontWeight: 600, letterSpacing: "-0.02em", color: "var(--text-primary)", lineHeight: 1 }}>
          {value}
        </span>
        {delta}
      </div>
      <span style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-muted)", lineHeight: 1.4 }}>{hint}</span>
    </div>
  );
}

export function PostureScorecard() {
  const { data, isLoading, error, refetch } = usePosture();

  if (isLoading) return <div style={{ padding: 18 }}><SkeletonRows rows={2} height={70} /></div>;
  if (error) return <ErrorState title="Posture didn't load. The analytics service returned an error." onRetry={() => refetch()} />;
  if (!data?.has_runs || !data.scores) {
    return (
      <div style={{ padding: 28 }}>
        <EmptyState
          icon={ShieldCheck}
          title="No scan history yet"
          hint="Posture and patch comparison appear after your first completed scan."
        />
      </div>
    );
  }

  const s = data.scores;
  const p = data.scores_prev ?? undefined;
  const g = GRADE[s.grade?.toUpperCase()] ?? GRADE.C;

  return (
    <div style={{ display: "flex", gap: 22, alignItems: "center", flexWrap: "wrap", padding: "18px 20px" }}>
      {/* ---- dial ---------------------------------------------------------- */}
      <div style={{ position: "relative", display: "grid", placeItems: "center" }}>
        <Dial score={s.posture_score} color={g.color} />
        <div style={{ position: "absolute", textAlign: "center", display: "flex", flexDirection: "column", alignItems: "center", gap: 2 }}>
          <span
            style={{
              fontFamily: "var(--font-display)", fontSize: 40, fontWeight: 600,
              lineHeight: 1, letterSpacing: "-0.04em", color: g.color,
            }}
          >
            {s.grade}
          </span>
          <span className="num-mono" style={{ fontSize: 12, color: "var(--text-secondary)", fontWeight: 600 }}>
            {s.posture_score}<span style={{ color: "var(--text-faint)" }}>/100</span>
          </span>
        </div>
        <span className="sr-only">Posture score {s.posture_score} out of 100, grade {s.grade} — {g.read}.</span>
      </div>

      {/* ---- verdict + supporting metrics ---------------------------------- */}
      <div style={{ flex: "1 1 300px", minWidth: 0, display: "flex", flexDirection: "column", gap: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
          <span className="chip" style={{ color: g.color, background: g.bg, borderColor: g.edge, fontSize: 11 }}>
            {g.read}
          </span>
          <Delta now={s.posture_score} prev={p?.posture_score} improvedWhenLower={false} />
          <span style={{ fontFamily: "var(--font-ui)", fontSize: 11.5, color: "var(--text-muted)" }}>
            {p ? "vs. previous scan" : "first scored scan — no comparison yet"}
          </span>
        </div>

        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <Readout
            label="Risk index"
            value={s.risk_index}
            delta={<Delta now={s.risk_index} prev={p?.risk_index} improvedWhenLower />}
            hint="Weighted open risk. Lower is better."
          />
          <Readout
            label="Exploitable"
            value={s.exploitable_score}
            delta={<Delta now={s.exploitable_score} prev={p?.exploitable_score} improvedWhenLower />}
            hint="Share of risk with known exploits. Lower is better."
          />
        </div>
      </div>
    </div>
  );
}
