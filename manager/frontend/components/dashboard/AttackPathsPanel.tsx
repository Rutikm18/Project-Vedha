"use client";

import React from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { DataState, EmptyState, SkeletonRows } from "../states/DataState";
import { AttackPathStyles } from "../attack-paths/AttackPathStyles";
import { AttackPathsTiles, AttackPathsTilesSkeleton } from "../attack-paths/AttackPathsTiles";
import { FixFirstCard } from "../attack-paths/FixFirstCard";
import { OverviewFootnote, OverviewList } from "../attack-paths/OverviewList";
import { useConsoleQuery } from "../../lib/console-source";
import { overviewState, overviewSummary, type Overview } from "../../lib/attack-paths";

const SHOWN_ON_DASHBOARD = 5;

/** The dashboard's Attack paths (Beta) section: three triage tiles, the engagements ranked (exposed
 *  first, then most crown jewels reachable, then the ones that cannot be assessed), and the "fix
 *  first" card for the top one. Reads stored results only; it never triggers a computation.
 *  Loading, failure and "no engagements" are three different claims and are shown as such. */
export function AttackPathsPanel() {
  const query = useConsoleQuery<Overview>("attackPaths", { refetchInterval: 120_000 });
  const rows = query.data?.engagements ?? [];
  const shown = rows.slice(0, SHOWN_ON_DASHBOARD);
  const total = query.data?.total ?? rows.length;
  const top = shown[0];
  // The card needs a route or an exposed jewel to talk about; anything else has nothing to fix.
  const focusRow = top && ["exposed", "reachable"].includes(overviewState(top)) ? top : null;

  return (
    <div className="apxp">
      <AttackPathStyles />
      <DataState
        loading={query.isLoading}
        error={query.error}
        isEmpty={!query.isLoading && !query.error && rows.length === 0}
        onRetry={() => void query.refetch()}
        skeleton={<><AttackPathsTilesSkeleton /><div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={3} height={64} /></div></>}
        empty={<EmptyState title="No engagements yet" hint="Create an engagement and run a scan; attack paths are computed per engagement." />}
      >
        <AttackPathsTiles summary={query.data?.summary} />
        <div className="apx-split" data-focus={focusRow ? "true" : "false"}>
          <OverviewList rows={shown} />
          {focusRow && <FixFirstCard row={focusRow} />}
        </div>
        <OverviewFootnote />
        <div style={{ padding: "var(--space-3) var(--space-5)", display: "flex", alignItems: "center", justifyContent: "space-between", gap: "var(--space-3)", flexWrap: "wrap" }}>
          <span style={{ fontSize: "var(--fs-body-s)", color: "var(--text-muted)" }}>
            {overviewSummary(query.data)}{total > shown.length ? ` · showing ${shown.length} of ${total}` : ""}
          </span>
          <Link href="/attack-paths" className="focusable" style={{ display: "inline-flex", alignItems: "center", gap: 4, fontSize: "var(--fs-body-s)", fontWeight: 650, color: "var(--accent)", textDecoration: "none" }}>
            All engagements <ArrowRight size={13} aria-hidden="true" />
          </Link>
        </div>
      </DataState>
    </div>
  );
}
