import React from "react";
import { meterCells, overviewState, type MeterCell, type OverviewRow } from "../../lib/attack-paths";

/** One diamond per crown jewel: filled = reachable, hollow = not, dashed = nothing to count.
 *  Shape carries it as well as colour, and the words beside the meter say the same thing, so
 *  this is decoration for a quick read and is hidden from assistive technology. */
function Diamond({ kind, tone }: { kind: MeterCell; tone: string }) {
  return (
    <svg width="14" height="14" viewBox="0 0 12 12" focusable="false">
      <path
        d="M6 .8 11.2 6 6 11.2.8 6z" strokeLinejoin="round"
        fill={kind === "reachable" ? tone : "none"}
        stroke={kind === "reachable" ? tone : "var(--text-muted)"}
        strokeWidth={kind === "reachable" ? 1 : 1.4}
        strokeDasharray={kind === "unknown" ? "2 2" : undefined}
      />
    </svg>
  );
}

export function JewelMeter({ row }: { row: OverviewRow }) {
  const { cells, more } = meterCells(row);
  const tone = overviewState(row) === "exposed" ? "var(--sev-critical-color)" : "var(--sev-high-color)";
  return (
    <span className="apx-meter" aria-hidden="true">
      {cells.map((kind, i) => <Diamond key={i} kind={kind} tone={tone} />)}
      {more > 0 && <span className="apx-meter-more">+{more}</span>}
    </span>
  );
}
