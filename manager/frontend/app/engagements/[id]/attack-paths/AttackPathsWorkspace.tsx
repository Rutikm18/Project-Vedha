"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, Layers, Loader2, Network, RefreshCw, Route as RouteIcon, ShieldCheck } from "lucide-react";
import { PageShell } from "../../../../components/PageShell";
import { DataState, ErrorState, SkeletonRows } from "../../../../components/states/DataState";
import { formatExact } from "../../../../components/portal/Timestamp";
import { useToast } from "../../../../hooks/useToast";
import { attackPathsApi } from "../../../../lib/attack-paths-api";
import { fixPointIds, targetExposed, zoneSummary, type Analysis, type Diagnostics } from "../../../../lib/attack-paths";
import { errorMessage, fetchJson } from "../../../../lib/fetcher";
import { PathMap } from "./PathMap";
import { ZoneMap } from "./ZoneMap";
import { BetaNotice, CoveragePanel, EmptyExplainer, ExposedCallout, FixFirstPanel, PathDetailPanel, PathTable, SuggestedTargetsNote } from "./Panels";
import { ATTACK_PATH_STYLES } from "./styles";

const PAGE_SIZE = 50;

export function AttackPathsWorkspace({ engagementId }: { engagementId: string }) {
  const qc = useQueryClient();
  const toast = useToast();
  const [picked, setPicked] = useState<string | null>(null);

  const engagement = useQuery({
    queryKey: ["engagement-name", engagementId],
    queryFn: () => fetchJson<{ name?: string }>(`/api/engagements/${encodeURIComponent(engagementId)}`),
    retry: false,
  });

  // The list first: a never-computed engagement is computed (and stored) by this read.
  const list = useQuery({
    queryKey: ["attack-paths", engagementId],
    queryFn: () => attackPathsApi.list(engagementId, { pageSize: PAGE_SIZE }),
  });
  const analysis = useQuery({
    queryKey: ["attack-path-analysis", engagementId],
    queryFn: () => attackPathsApi.analysis(engagementId),
    enabled: list.isSuccess,
  });

  // Read-only aggregation of the stored routes; after the list so a first read has stored something to group.
  const zones = useQuery({
    queryKey: ["attack-path-zones", engagementId],
    queryFn: () => attackPathsApi.zones(engagementId),
    enabled: list.isSuccess,
  });

  const items = list.data?.items ?? [];
  const activeId = picked && items.some((p) => p.id === picked) ? picked : items[0]?.id ?? null;

  const detail = useQuery({
    queryKey: ["attack-path", engagementId, activeId],
    queryFn: () => attackPathsApi.detail(engagementId, activeId as string),
    enabled: !!activeId,
  });

  const recompute = useMutation({
    mutationFn: () => attackPathsApi.list(engagementId, { refresh: true, pageSize: PAGE_SIZE }),
    onSuccess: (fresh) => {
      qc.setQueryData(["attack-paths", engagementId], fresh);
      setPicked(null);
      void qc.invalidateQueries({ queryKey: ["attack-path-analysis", engagementId] });
      void qc.invalidateQueries({ queryKey: ["attack-path-zones", engagementId] });
      void qc.invalidateQueries({ queryKey: ["attack-path", engagementId] });
      toast.success("Attack paths recomputed", `${fresh.total} route${fresh.total === 1 ? "" : "s"} from current findings and assets.`);
    },
    onError: (e) => toast.error("Could not recompute attack paths", errorMessage(e)),
  });

  const computed = analysis.data?.computed ? analysis.data : null;
  const choke = computed?.choke ?? null;
  const chokeIds = useMemo(() => fixPointIds(choke), [choke]);
  const exposed = useMemo(() => (choke?.targets ?? []).filter(targetExposed), [choke]);
  const whyEmpty: Diagnostics | null | undefined = list.data?.why_empty ?? computed?.diagnostics;
  const name = engagement.data?.name;

  return (
    <PageShell title="Attack paths" headerActions={<span className="badge badge-info" title="Attack paths is in beta">Beta</span>} subtitle={name ? `${name} · how an attacker could reach your crown jewels` : "How an attacker could reach your crown jewels"} hideRefresh>
      <style>{ATTACK_PATH_STYLES}</style>
      <div className="ap-page">
        <Link href={`/engagements/${encodeURIComponent(engagementId)}`} className="ap-back">
          <ArrowLeft size={14} /> Back to engagement
        </Link>

        {/* Status: what was computed, when, and the standing caveat on every route. */}
        <section className="ap-card" aria-label="Attack path status">
          <div className="ap-card-body">
            <div className="ap-status">
              <div className="ap-status-text">
                <strong>
                  {list.isLoading ? "Loading attack paths…"
                    : list.isError ? "Attack paths unavailable"
                    : list.data?.total === 0 && exposed.length > 0
                      ? `${exposed.length} crown jewel${exposed.length === 1 ? "" : "s"} directly exposed`
                      : `${list.data?.total ?? 0} modelled route${list.data?.total === 1 ? "" : "s"}`}
                </strong>
                <span>
                  {computed
                    ? <>Computed {formatExact(computed.computed_at)}
                      {choke && <> · <span className="ap-num">{choke.entry_points ?? 0}</span> entry point{choke.entry_points === 1 ? "" : "s"}
                        {" · "}<span className="ap-num">{choke.targets.length}</span> crown jewel{choke.targets.length === 1 ? "" : "s"}</>}</>
                    : list.isError ? "The stored paths could not be read."
                    : analysis.isLoading || list.isLoading ? "Reading the stored analysis…"
                    : "No analysis recorded yet."}
                </span>
              </div>
              <button type="button" className="btn btn-secondary" onClick={() => recompute.mutate()}
                disabled={recompute.isPending || list.isLoading}>
                {recompute.isPending ? <Loader2 size={14} className="ap-spin" /> : <RefreshCw size={14} />}
                {recompute.isPending ? "Recomputing…" : "Recompute paths"}
              </button>
            </div>
            <BetaNotice />
            <p className="ap-fine">
              Routes between subnets are inferred from addressing and the engagement scope, not read from
              firewall rules. A step marked “assumed” has not been observed. Paths refresh when a detection run
              changes the findings; Recompute forces it now. At most 5 routes are listed per entry point per
              crown jewel, so the count follows the entry points, not how exposed anything is.
            </p>
          </div>
        </section>

        <section className="ap-card" aria-label="What these paths do not cover">
          <header className="ap-card-head">
            <h2 className="ap-card-title"><ShieldCheck size={15} /> What these paths do not cover</h2>
            {computed && <span className="ap-card-meta">as of {formatExact(computed.computed_at)}</span>}
          </header>
          <div className="ap-card-body">
            {list.isError
              ? <p className="ap-fine">Coverage can&apos;t be shown until the attack paths load.</p>
              : analysis.isError
                ? <ErrorState title="Couldn't load coverage" detail={errorMessage(analysis.error)} onRetry={() => void analysis.refetch()} />
                : <CoveragePanel analysis={list.isLoading ? undefined : (analysis.data as Analysis | undefined)} />}
          </div>
        </section>

        <DataState
          loading={list.isLoading}
          error={list.error}
          isEmpty={list.data?.total === 0}
          onRetry={() => void list.refetch()}
          skeleton={<SkeletonRows rows={4} height={64} />}
          empty={exposed.length > 0 ? <ExposedCallout targets={exposed} /> : <EmptyExplainer diagnostics={whyEmpty} />}
        >
          {/* Decision first: what to fix. */}
          <section className="ap-card" aria-label="Fix first">
            <header className="ap-card-head">
              <h2 className="ap-card-title"><Layers size={15} /> Fix first</h2>
              {choke && <span className="ap-card-meta">ranked by modelled risk removed</span>}
            </header>
            <SuggestedTargetsNote analysis={analysis.data as Analysis | undefined} />
            {choke
              ? <FixFirstPanel choke={choke} />
              : analysis.isError
                ? <div className="ap-card-body"><p className="ap-fine">Fix-first ranking could not be loaded.</p></div>
                : analysis.isLoading || !analysis.data
                  ? <div className="ap-card-body"><SkeletonRows rows={2} height={28} /></div>
                  : <div className="ap-card-body"><p className="ap-fine">
                      The fix-first ranking has not been recorded for these paths. Recompute the paths to produce it.
                    </p></div>}
          </section>

          {(() => {
            const sum = zoneSummary(zones.data);
            if (zones.isLoading) {
              return <section className="ap-card" aria-label="Subnets"><div className="ap-card-body"><SkeletonRows rows={2} height={48} /></div></section>;
            }
            if (zones.isError) {
              return (
                <section className="ap-card" aria-label="Subnets">
                  <header className="ap-card-head"><h2 className="ap-card-title"><Network size={15} /> Where the routes go</h2></header>
                  <div className="ap-card-body"><p className="ap-fine">The subnet map could not be loaded. The routes below are unaffected.</p></div>
                </section>
              );
            }
            if (!zones.data || (zones.data.zones.length === 0 && sum.notes.length === 0)) return null;
            return (
              <section className="ap-card" aria-label="Subnets">
                <header className="ap-card-head">
                  <h2 className="ap-card-title"><Network size={15} /> Where the routes go</h2>
                  <span className="ap-card-meta">{zones.data.routes_considered ?? 0} listed route{zones.data.routes_considered === 1 ? "" : "s"}, grouped by subnet</span>
                </header>
                <div className="ap-card-body">
                  {sum.lead && <p className="ap-headline">{sum.lead}</p>}
                  <ZoneMap view={zones.data} />
                  {sum.notes.length > 0 && <ul className="ap-routes-lines">{sum.notes.map((n) => <li key={n}>{n}</li>)}</ul>}
                  <p className="ap-fine">
                    A subnet here is a range the analysis placed hosts in. Counts are of the stored routes, a capped list, so they say how
                    many listed routes use a step, not how exposed it is. A step marked assumed has not been observed.
                  </p>
                </div>
              </section>
            );
          })()}

          <section className="ap-card" aria-label="Route map">
            <header className="ap-card-head">
              <h2 className="ap-card-title"><RouteIcon size={15} /> How the routes converge</h2>
              <span className="ap-card-meta">
                {Math.min(items.length, 12)} highest-risk of {list.data?.total ?? 0} route{list.data?.total === 1 ? "" : "s"}
              </span>
            </header>
            <PathMap items={items} chokeIds={chokeIds} selectedId={activeId} />
            <div className="ap-card-body">
              <div className="ap-legend" aria-label="Legend">
                <span><i className="ap-swatch" data-kind="entry" /> Entry point</span>
                <span><i className="ap-swatch" data-kind="target" /> Crown jewel</span>
                <span><i className="ap-swatch" data-kind="choke" /> Fix here</span>
              </div>
            </div>
          </section>

          <div className="ap-split">
            <section className="ap-card" aria-label="Attack paths">
              <header className="ap-card-head">
                <h2 className="ap-card-title"><RouteIcon size={15} /> Routes</h2>
                <span className="ap-card-meta">
                  {list.data && list.data.total > items.length
                    ? `highest ${items.length} of ${list.data.total}, by risk`
                    : "by risk"}
                </span>
              </header>
              <PathTable items={items} selectedId={activeId} onSelect={setPicked} />
            </section>

            <section className="ap-card" aria-label="Selected route" aria-live="polite">
              <header className="ap-card-head">
                <h2 className="ap-card-title"><RouteIcon size={15} /> Step by step</h2>
              </header>
              <DataState
                loading={detail.isLoading}
                error={detail.error}
                onRetry={() => void detail.refetch()}
                skeleton={<div className="ap-card-body"><SkeletonRows rows={3} height={56} /></div>}
              >
                {detail.data && <PathDetailPanel detail={detail.data} />}
              </DataState>
            </section>
          </div>
        </DataState>
      </div>
    </PageShell>
  );
}
