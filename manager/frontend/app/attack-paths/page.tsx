"use client";

import { use } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { EnvironmentAttackWorkspace } from "../../components/attack-paths/EnvironmentAttackWorkspace";
import { Route as RouteIcon } from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { DataState, EmptyState, SkeletonRows } from "../../components/states/DataState";
import { AttackPathStyles } from "../../components/attack-paths/AttackPathStyles";
import { AttackPathsTiles, AttackPathsTilesSkeleton } from "../../components/attack-paths/AttackPathsTiles";
import { OverviewFootnote, OverviewList } from "../../components/attack-paths/OverviewList";
import { useComputeAttackPaths } from "../../components/attack-paths/useComputeAttackPaths";
import { BetaNotice } from "../engagements/[id]/attack-paths/Panels";
import { fetchJson } from "../../lib/fetcher";
import { overviewSummary, type Overview } from "../../lib/attack-paths";

/** Every engagement's stored attack-path result in one place (operators). Each row
 *  opens that engagement's Attack paths page, where the routes are computed and read. */
function LegacyAttackPathsOverviewPage() {
  const query = useQuery({
    queryKey: ["attack-paths-overview"],
    queryFn: () => fetchJson<Overview>("/api/attack-paths/overview?limit=200"),
  });
  const rows = query.data?.engagements ?? [];
  const compute = useComputeAttackPaths();

  return (
    <PageShell
      title="Attack paths"
      headerActions={<span className="badge badge-info" title="Attack paths is in beta">Beta</span>}
      subtitle="How an attacker could reach your crown jewels, per engagement"
    >
      <nav className="attack-path-modes" aria-label="Attack-path scope"><Link className="btn btn-secondary" href="/attack-paths">Open environment chains</Link><Link href="/attack-paths?mode=overview" aria-current="page">Engagement overview</Link></nav>
      <div style={{ display: "grid", gap: "var(--space-4)", width: "100%" }}>
        <section className="panel apxp" aria-label="Attack paths, all engagements">
          <AttackPathStyles />
          <header className="panel-head" style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <RouteIcon size={15} aria-hidden="true" />
            <h2 className="panel-title" style={{ margin: 0 }}>Engagements</h2>
            <span className="panel-note num" style={{ marginLeft: "auto" }}>{overviewSummary(query.data)}</span>
          </header>
          <div style={{ padding: "var(--space-3) var(--space-5)" }}><BetaNotice /></div>
          <DataState
            loading={query.isLoading}
            error={query.error}
            isEmpty={!query.isLoading && !query.error && rows.length === 0}
            onRetry={() => void query.refetch()}
            skeleton={<><AttackPathsTilesSkeleton /><div style={{ padding: "var(--space-4)" }}><SkeletonRows rows={4} height={64} /></div></>}
            empty={<EmptyState title="No engagements yet" hint="Create an engagement and run a scan; attack paths are computed per engagement." />}
          >
            <AttackPathsTiles summary={query.data?.summary} />
            <OverviewList rows={rows} compute={compute} />
            <OverviewFootnote />
          </DataState>
        </section>
      </div>
    </PageShell>
  );
}

export default function AttackPathsOverviewPage({ searchParams }: { searchParams: Promise<{mode?:string|string[]}> }) {
  const query=use(searchParams);
  return query.mode!=="overview" ? <EnvironmentAttackWorkspace/> : <LegacyAttackPathsOverviewPage/>;
}
