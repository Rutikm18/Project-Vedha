import React from "react";
import { overviewTiles, type OverviewSummary } from "../../lib/attack-paths";

/** The three triage tiles. Counts of engagements only, from a summary the server computed over
 *  ALL of the tenant's engagements (not just the rows below), so they never depend on how many
 *  rows are shown and never add up networks that are not alike. */
export function AttackPathsTiles({ summary }: { summary: OverviewSummary | null | undefined }) {
  const tiles = overviewTiles(summary);
  if (!tiles) return null;
  return (
    <div className="apx-tiles" role="group" aria-label="Attack paths summary">
      {tiles.map((t) => (
        <div key={t.key} className="apx-tile" data-tone={t.tone}>
          <div className="apx-tile-label">{t.label}</div>
          <div className="apx-tile-value">
            <span>{t.value}</span>
            {t.unit && <small>{t.unit}</small>}
          </div>
          <div className="apx-tile-sub">{t.sub}</div>
        </div>
      ))}
    </div>
  );
}

/** Same shape as the tiles, so the panel does not jump when the data lands. */
export function AttackPathsTilesSkeleton() {
  return <div className="apx-tiles apx-skel" aria-hidden="true" />;
}
