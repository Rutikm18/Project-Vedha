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
import { ShieldCheck } from "lucide-react";
import { useConsoleQuery } from "../../lib/console-source";
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
  return useConsoleQuery<Posture>("posture", {
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

/** 270° dial. pathLength=100 makes the dash maths score-in-percent directly.
 *  The arc grows from empty on mount and re-tweens on every score change (the
 *  .dial-arc/.dial-tip transitions live in the panel's scoped <style>), so the
 *  eye tracks the delta, not just the resting value. A zero score is hidden by
 *  the wrapper's data-empty guard rather than drawn as a misleading sliver. */
function Dial({ score, color }: { score: number; color: string }) {
  const pct = Math.max(0, Math.min(100, score));
  const ARC = 75; // 270° of a 360° circle, in pathLength units

  // Render empty first, then advance to the real value one frame later so the
  // CSS transition has a delta to interpolate. Re-runs whenever the score moves;
  // under prefers-reduced-motion the global transition-kill makes it snap.
  const [shown, setShown] = React.useState(0);
  React.useEffect(() => {
    const id = requestAnimationFrame(() => setShown(pct));
    return () => cancelAnimationFrame(id);
  }, [pct]);

  return (
    <svg viewBox="0 0 120 120" width={132} height={132} aria-hidden focusable="false" style={{ flexShrink: 0 }}>
      <circle
        cx="60" cy="60" r="46" fill="none" pathLength={100}
        stroke="var(--track-bg)" strokeWidth="7" strokeLinecap="round"
        strokeDasharray={`${ARC} 100`} transform="rotate(135 60 60)"
      />
      <circle
        cx="60" cy="60" r="46" fill="none" pathLength={100}
        stroke={color} strokeWidth="7" strokeLinecap="round"
        strokeDasharray={`${(ARC * shown) / 100} 100`} transform="rotate(135 60 60)"
        className="dial-arc"
      />
      {/* endpoint marker — the eye lands on it before it reads the number. Its
          rotation rides a CSS transform (not the SVG attribute) so it tweens
          alongside the arc. */}
      <circle
        cx="60" cy="14" r="2.6" fill={color}
        className="dial-tip"
        style={{ transform: `rotate(${135 + (270 * shown) / 100 + 90}deg)` }}
      />
    </svg>
  );
}

function MetricTile({ label, value, delta, hint }: {
  label: string; value: React.ReactNode; delta?: React.ReactNode; hint: string;
}) {
  return (
    <div className="posture-metric">
      <span className="eyebrow">{label}</span>
      <div className="posture-metric-value">
        <span className="num" style={{ fontFamily: "var(--font-display)", fontSize: "var(--fs-display-m)", fontWeight: 600, letterSpacing: "-0.02em", color: "var(--text-primary)", lineHeight: 1 }}>
          {value}
        </span>
        {delta}
      </div>
      <span style={{ fontFamily: "var(--font-ui)", fontSize: "var(--fs-label)", color: "var(--text-muted)", lineHeight: 1.4 }}>{hint}</span>
    </div>
  );
}

export function PostureScorecard() {
  const { data, isLoading, error, refetch } = usePosture();

  if (isLoading) return <div style={{ padding: "var(--space-5)" }}><SkeletonRows rows={1} height={168} /></div>;
  if (error) return <ErrorState title="Posture didn't load. The analytics service returned an error." onRetry={() => refetch()} />;
  if (!data?.has_runs || !data.scores) {
    return (
      <div style={{ padding: "var(--space-6)" }}>
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
  const g = GRADE[s.grade?.toUpperCase()] ?? {
    color: "var(--text-muted)", bg: "var(--bg-surface)",
    edge: "var(--border-subtle)", read: "Ungraded",
  };

  return (
    <div className="posture-scorecard">
      {/* ---- dial ---------------------------------------------------------- */}
      <style>{`
        .posture-scorecard {
          container-type: inline-size;
          display: grid;
          grid-template-columns: 132px minmax(0, 1fr);
          gap: var(--space-5);
          align-items: center;
          padding: var(--space-5);
          box-sizing: border-box;
        }
        .posture-detail {
          min-width: 0;
          display: grid;
          gap: var(--space-4);
        }
        .posture-verdict {
          display: flex;
          align-items: center;
          gap: var(--space-3);
          min-height: 26px;
          flex-wrap: wrap;
        }
        .posture-comparison {
          display: inline-flex;
          align-items: center;
          gap: var(--space-2);
          min-width: 0;
          flex-wrap: wrap;
        }
        .posture-metrics {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          border-top: var(--hairline) solid var(--border-subtle);
        }
        .posture-metric {
          min-width: 0;
          display: flex;
          flex-direction: column;
          gap: var(--space-2);
          padding: var(--space-4) var(--space-4) 0 0;
        }
        .posture-metric + .posture-metric {
          border-left: var(--hairline) solid var(--border-subtle);
          padding-right: 0;
          padding-left: var(--space-4);
        }
        .posture-metric-value {
          display: flex;
          align-items: center;
          gap: var(--space-2);
          flex-wrap: wrap;
        }
        @container (max-width: 390px) {
          .posture-scorecard { grid-template-columns: 1fr; justify-items: center; }
          .posture-detail { width: 100%; }
          .posture-verdict { justify-content: center; text-align: center; }
        }
        @container (max-width: 300px) {
          .posture-metrics { grid-template-columns: 1fr; }
          .posture-metric { padding-right: 0; }
          .posture-metric + .posture-metric {
            border-top: var(--hairline) solid var(--border-subtle);
            border-left: 0;
            margin-top: var(--space-3);
            padding-left: 0;
          }
        }
        .posture-dial .dial-arc,
        .posture-dial .dial-tip {
          transition: stroke-dasharray .8s cubic-bezier(.22, 1, .36, 1),
                      transform        .8s cubic-bezier(.22, 1, .36, 1);
        }
        .posture-dial .dial-tip { transform-box: view-box; transform-origin: 60px 60px; }
        /* At zero the round line-cap + tip marker still paint a small wedge that
           reads as real progress — hide both until there's a score to show.
           (prefers-reduced-motion is handled by the global transition-kill.) */
        .posture-dial[data-empty="true"] .dial-arc,
        .posture-dial[data-empty="true"] .dial-tip { visibility: hidden; }
      `}</style>
      <div
        className="posture-dial"
        data-empty={s.posture_score === 0 ? "true" : "false"}
        style={{ position: "relative", display: "grid", placeItems: "center" }}
      >
        <Dial score={s.posture_score} color={g.color} />
        <div style={{ position: "absolute", textAlign: "center", display: "flex", flexDirection: "column", alignItems: "center", gap: 2 }}>
          <span
            style={{
              fontFamily: "var(--font-display)", fontSize: "var(--fs-display-l)", fontWeight: 600,
              lineHeight: 1, letterSpacing: "-0.04em", color: g.color,
            }}
          >
            {s.grade}
          </span>
          <span className="num-mono" style={{ fontSize: "var(--fs-body-s)", color: "var(--text-secondary)", fontWeight: 600 }}>
            {s.posture_score}<span style={{ color: "var(--text-faint)" }}>/100</span>
          </span>
        </div>
        <span className="sr-only">Posture score {s.posture_score} out of 100, grade {s.grade} — {g.read}.</span>
      </div>

      {/* ---- verdict + supporting metrics ---------------------------------- */}
      <div className="posture-detail">
        <div className="posture-verdict">
          <span className="chip" style={{ color: g.color, background: g.bg, borderColor: g.edge, fontSize: "var(--fs-label)" }}>
            {g.read}
          </span>
          <div className="posture-comparison">
            <Delta now={s.posture_score} prev={p?.posture_score} improvedWhenLower={false} />
            <span style={{ fontFamily: "var(--font-ui)", fontSize: "var(--fs-body-s)", color: "var(--text-muted)" }}>
              {p ? "vs. previous scan" : "first scored scan — no comparison yet"}
            </span>
          </div>
        </div>

        <div className="posture-metrics">
          <MetricTile
            label="Risk index"
            value={Number(s.risk_index ?? 0).toFixed(2)}
            delta={<Delta now={s.risk_index} prev={p?.risk_index} improvedWhenLower />}
            hint="Weighted open risk. Lower is better."
          />
          <MetricTile
            label="Exploitable"
            value={`${Number(s.exploitable_score ?? 0).toFixed(1)}%`}
            delta={<Delta now={s.exploitable_score} prev={p?.exploitable_score} improvedWhenLower />}
            hint="Share of risk with known exploits. Lower is better."
          />
        </div>
      </div>
    </div>
  );
}
