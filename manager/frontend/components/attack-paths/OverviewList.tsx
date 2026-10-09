"use client";

import React from "react";
import Link from "next/link";
import { AlertTriangle, ChevronRight, Info, Loader2, Play } from "lucide-react";
import { formatCompact } from "../portal/Timestamp";
import { canCompute, overviewLine, trendView, type OverviewRow, type OverviewState } from "../../lib/attack-paths";
import { JewelMeter } from "./JewelMeter";
import { Sparkline } from "./Sparkline";

// The rail colour carries state; the words carry the meaning (never colour alone).
const RAIL: Record<OverviewState, string> = {
  exposed: "var(--sev-critical-color)",
  reachable: "var(--sev-high-color)",
  unreachable: "var(--sev-medium-color)",
  no_targets: "var(--sev-medium-color)",
  unrecorded: "var(--text-muted)",
  not_computed: "var(--text-muted)",
};

/** One engagement per row, each a link into that engagement's Attack paths page. Used by the
 *  dashboard section (a handful) and the /attack-paths page (all). Needs <AttackPathStyles />.
 *  `compute` adds a Compute button to rows nobody has computed (or whose analysis recorded no per-jewel
 *  data); the button is a sibling of the link, never inside it, and does nothing until clicked. */
export function OverviewList({ rows, compute }: {
  rows: OverviewRow[];
  compute?: { run: (row: OverviewRow) => void; pendingId: string | null };
}) {
  return (
    <div className="apx">
      <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
        {rows.map((row) => {
          const line = overviewLine(row);
          const trend = trendView(row);
          const busy = compute?.pendingId === row.engagement_id;
          return (
            <li key={row.engagement_id} className="apo-li">
              <Link
                href={`/engagements/${encodeURIComponent(row.engagement_id)}/attack-paths`}
                className="console-row focusable apo-row"
                style={{ "--rail": RAIL[line.state] } as React.CSSProperties}
                aria-label={`${row.name}: ${line.headline}${line.ways ? `, ${line.ways}` : ""}${line.detail ? `. ${line.detail}` : ""}`}
              >
                <div className="apo-name">
                  <strong title={row.name}>{row.name}</strong>
                  <span className="apo-status">{row.status}</span>
                </div>
                <div className="apo-facts">
                  <div className="apo-line">
                    <JewelMeter row={row} />
                    <span className="apo-headline">{line.headline}</span>
                    {line.ways && <span className="apo-ways">{line.ways}</span>}
                  </div>
                  {line.detail && <div className="apo-detail">{line.detail}</div>}
                  {trend && (
                    <div className="apo-trend">
                      <Sparkline trend={trend} />
                      {trend.change && <span>{trend.change}</span>}
                      {trend.note && <span className="apo-chip" data-tone="weak" title={trend.note}>Inputs changed too</span>}
                    </div>
                  )}
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
              {compute && canCompute(row) && (
                <button type="button" className="btn btn-secondary apo-compute focusable" disabled={compute.pendingId !== null}
                  aria-label={busy ? `Computing attack paths for ${row.name}` : `Compute attack paths for ${row.name}`}
                  onClick={() => compute.run(row)}>
                  {busy ? <Loader2 size={13} className="apx-spin" aria-hidden="true" /> : <Play size={13} aria-hidden="true" />}
                  {busy ? "Computing…" : "Compute"}
                </button>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

/** Said once under any list of rows: what each kind of "nothing" does and does not mean. */
export function OverviewFootnote() {
  return (
    <p className="apo-note">
      “Reachable” means the model found a route using only findings already marked exploitable and network
      reachability inferred from addressing. “No modelled route” is not evidence the network is safe, and
      “can&apos;t be assessed” means there was nothing to model yet: nobody has opened that engagement&apos;s
      Attack paths, or no asset is marked critical. A change between two computations is a difference, not a
      verdict: seeing more of the network raises a count too.
    </p>
  );
}
