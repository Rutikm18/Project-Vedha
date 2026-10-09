"use client";

import React from "react";
import Link from "next/link";
import { AlertTriangle, ChevronRight, Info } from "lucide-react";
import { formatCompact } from "../portal/Timestamp";
import { overviewLine, type OverviewRow, type OverviewState } from "../../lib/attack-paths";

// The rail colour carries state; the words carry the meaning (never colour alone).
const RAIL: Record<OverviewState, string> = {
  routes: "var(--sev-high-color)",
  empty: "var(--sev-medium-color)",
  not_computed: "var(--text-faint)",
};

export const OVERVIEW_STYLES = `
.apo-row { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) var(--space-5); text-decoration: none; color: inherit; }
.apo-main { flex: 1; min-width: 0; display: grid; gap: 3px; }
.apo-name { display: flex; align-items: baseline; gap: var(--space-2); min-width: 0; }
.apo-name strong { font-size: var(--fs-body); font-weight: 650; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.apo-status { font-size: 10.5px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); white-space: nowrap; }
.apo-headline { font-size: var(--fs-body); color: var(--text-primary); font-weight: 600; }
.apo-detail { font-size: var(--fs-body-s); color: var(--text-secondary); line-height: 1.45; }
.apo-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; font-size: 11px; color: var(--text-muted); }
.apo-chip { display: inline-flex; align-items: center; gap: 4px; padding: 1px 7px; border-radius: 999px; border: 0.5px solid var(--border-default); background: var(--bg-surface); color: var(--text-secondary); white-space: nowrap; }
.apo-chip[data-tone="weak"] { color: var(--sev-medium-color); border-color: var(--sev-medium-color); }
.apo-chip[data-tone="firm"] { color: var(--nominal-color); border-color: var(--nominal-color); }
.apo-go { color: var(--text-faint); flex-shrink: 0; }
.apo-note { margin: 0; padding: var(--space-3) var(--space-5); font-size: 11.5px; line-height: 1.5; color: var(--text-muted); border-top: var(--hairline) solid var(--border-subtle); }
`;

/** One engagement per row, each a link into that engagement's Attack paths page.
 *  Used by the dashboard section (a handful) and the /attack-paths page (all). */
export function OverviewList({ rows }: { rows: OverviewRow[] }) {
  return (
    <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
      <style>{OVERVIEW_STYLES}</style>
      {rows.map((row) => {
        const line = overviewLine(row);
        return (
          <li key={row.engagement_id}>
            <Link
              href={`/engagements/${encodeURIComponent(row.engagement_id)}/attack-paths`}
              className="console-row focusable apo-row"
              style={{ "--rail": RAIL[line.state] } as React.CSSProperties}
              aria-label={`${row.name}: ${line.headline}${line.detail ? `. ${line.detail}` : ""}`}
            >
              <div className="apo-main">
                <div className="apo-name">
                  <strong>{row.name}</strong>
                  <span className="apo-status">{row.status}</span>
                </div>
                <div>
                  <span className="apo-headline">{line.headline}</span>
                  {line.detail && <span className="apo-detail"> — {line.detail}</span>}
                </div>
                {(line.coverage || line.stale || row.computed_at) && (
                  <div className="apo-meta">
                    {line.coverage && (
                      <span className="apo-chip" data-tone={line.coverage.tone}>
                        {line.coverage.tone === "weak" ? <AlertTriangle size={11} aria-hidden="true" /> : <Info size={11} aria-hidden="true" />}
                        {line.coverage.label}
                      </span>
                    )}
                    {line.stale && <span className="apo-chip" data-tone="weak">{line.stale}</span>}
                    {row.computed_at && <span>computed {formatCompact(row.computed_at)}</span>}
                  </div>
                )}
              </div>
              <ChevronRight size={16} className="apo-go" aria-hidden="true" />
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

/** Said once under any list of rows: what zero routes and "not computed" do and do not mean. */
export function OverviewFootnote() {
  return (
    <p className="apo-note">
      Routes use only findings already marked exploitable and network reachability inferred from addressing.
      “No routes modelled” means the model had nothing to draw, not that the network is safe, and “not computed”
      means nobody has opened that engagement&apos;s Attack paths yet.
    </p>
  );
}
