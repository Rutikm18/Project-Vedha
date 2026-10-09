import React from "react";
import { sparkline, type TrendView } from "../../lib/attack-paths";

/** Crown jewels reachable over the last computations. A 2px line from zero, a ringed end dot, and the
 *  numbers as the accessible name: the line is a glance, the text twin is the content. */
export function Sparkline({ trend }: { trend: TrendView }) {
  const W = 64, H = 20;
  const { segments, last } = sparkline(trend.values, W, H);
  return (
    <svg className="apx-spark" width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={trend.twin} focusable="false">
      <title>{trend.twin}</title>
      {segments.map((pts) => (
        <polyline key={pts} points={pts} fill="none" stroke="var(--text-muted)" strokeWidth="2"
          strokeLinecap="round" strokeLinejoin="round" />
      ))}
      {last && <circle cx={last.x} cy={last.y} r="4" fill="var(--text-primary)" stroke="var(--bg-panel)" strokeWidth="2" />}
    </svg>
  );
}
