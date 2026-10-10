"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, ArrowRight } from "lucide-react";
import { SkeletonRows } from "../states/DataState";
import { fetchJson } from "../../lib/fetcher";
import {
  focusBars, focusLead, routeChainView, type ChainItem, type Focus, type FocusNode, type OverviewRow,
} from "../../lib/attack-paths";

/** Role is a shape and a word; colour only repeats it. A host on the fix list wears the fix mark. */
function NodeMark({ node, exposed }: { node: FocusNode | null; exposed?: boolean }) {
  if (exposed) {
    return <svg width="22" height="22" viewBox="0 0 12 12" aria-hidden="true"><path d="M6 .8 11.2 6 6 11.2.8 6z" fill="var(--sev-critical-color)" stroke="var(--sev-critical-color)" strokeLinejoin="round" /></svg>;
  }
  if (node?.on_fix_list) {
    return (
      <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true">
        <rect x="3" y="3" width="14" height="14" rx="4" fill="var(--accent)" />
        <path d="M7 10.2 9.2 12.4 13.2 7.8" fill="none" stroke="var(--accent-contrast)" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }
  if (node?.role === "jewel") {
    return <svg width="22" height="22" viewBox="0 0 12 12" aria-hidden="true"><path d="M6 .8 11.2 6 6 11.2.8 6z" fill="var(--sev-high-color)" stroke="var(--sev-high-color)" strokeLinejoin="round" /></svg>;
  }
  if (node?.role === "entry") {
    return (
      <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true">
        <circle cx="10" cy="10" r="7.5" fill="var(--bg-surface)" stroke="var(--text-secondary)" strokeWidth="1.8" />
        <path d="M5 10h7m-2.5-2.5L12 10l-2.5 2.5" fill="none" stroke="var(--text-secondary)" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }
  return <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="5" fill="var(--bg-surface)" stroke="var(--text-secondary)" strokeWidth="1.8" /></svg>;
}

function roleText(node: FocusNode): { text: string; tone: "fix" | "jewel" | "plain" } {
  const base = node.role === "entry" ? "Entry point" : node.role === "jewel" ? "Crown jewel" : "Host on the route";
  if (node.on_fix_list) return { text: `${base} · on the fix list`, tone: "fix" };
  return { text: base, tone: node.role === "jewel" ? "jewel" : "plain" };
}

function ChainRow({ item }: { item: ChainItem }) {
  if (item.kind === "gap") {
    return (
      <li data-gap="true" aria-label={`${item.hidden} more hosts on the route`}>
        <span />
        <div className="apx-hop">
          +{item.hidden} more {item.hidden === 1 ? "host" : "hosts"} on the route
          {item.weakHidden && " · includes an assumed link"}
        </div>
      </li>
    );
  }
  const { node, hop } = item;
  const role = roleText(node);
  return (
    <li>
      <span className="apx-node"><NodeMark node={node} /></span>
      <div style={{ minWidth: 0 }}>
        <div className="apx-role" data-role={role.tone === "plain" ? undefined : role.tone}>{role.text}</div>
        <div className="apx-host" title={node.label}>{node.label}</div>
        {hop && (
          <div className="apx-hop" data-tone={hop.weak ? "weak" : undefined}>
            {hop.weak && <AlertTriangle size={11} aria-hidden="true" />}
            {hop.step ? `${hop.step} · ` : ""}{hop.label}{hop.stale ? " · not seen recently" : ""}
            {hop.caveat ? ` — ${hop.caveat}` : ""}
          </div>
        )}
      </div>
    </li>
  );
}

/**
 * "Fix first" for one engagement (the top of the dashboard's ladder): the highest-risk stored
 * route as a short ordered list, then the hosts whose fix removes the most modelled risk as a
 * share of it. Read-only: it asks for stored results and never causes a computation. A failed
 * request leaves this card saying so and leaves the ladder beside it untouched.
 */
export function FixFirstCard({ row }: { row: OverviewRow }) {
  const query = useQuery({
    // computed_at is in the key so a recompute fetches again; nothing else refetches it.
    queryKey: ["attack-paths-focus", row.engagement_id, row.computed_at],
    queryFn: () => fetchJson<Focus>(`/api/attack-paths/focus/${encodeURIComponent(row.engagement_id)}`),
    staleTime: 60_000,
  });
  const href = `/engagements/${encodeURIComponent(row.engagement_id)}/attack-paths`;
  const focus = query.data;

  return (
    <aside className="apx-focus" aria-label={`Fix first for ${row.name}`} aria-busy={query.isLoading || undefined}>
      <h4>Fix first</h4>
      <div className="apx-focus-who" title={row.name}>{row.name}</div>
      {query.isLoading && <SkeletonRows rows={3} height={36} />}
      {query.error && !focus && (
        <p className="apx-quiet" role="status">
          Fix-first detail did not load.{" "}
          <button type="button" className="focusable" onClick={() => void query.refetch()}
            style={{ background: "none", border: 0, padding: 0, color: "var(--accent)", cursor: "pointer", font: "inherit", fontWeight: 650 }}>
            Retry
          </button>
        </p>
      )}
      {focus && <FocusBody focus={focus} />}
      <Link href={href} className="apx-open focusable">
        Open this engagement <ArrowRight size={13} aria-hidden="true" />
      </Link>
    </aside>
  );
}

function FocusBody({ focus }: { focus: Focus }) {
  const lead = focusLead(focus);
  const chain = routeChainView(focus.route);
  const bars = focusBars(focus);
  return (
    <>
      {lead && <p className="apx-lead">{lead}</p>}

      {focus.exposed.length > 0 && (
        <ol className="apx-chain" aria-label="Crown jewels exposed to the internet">
          {focus.exposed.map((e) => (
            <li key={e.asset_id}>
              <span className="apx-node"><NodeMark node={null} exposed /></span>
              <div style={{ minWidth: 0 }}>
                <div className="apx-role" data-role="exposed">Crown jewel · directly exposed</div>
                <div className="apx-host" title={e.label}>{e.label}</div>
              </div>
            </li>
          ))}
        </ol>
      )}

      {chain.length > 0 && (
        <>
          <ol className="apx-chain" aria-label="Highest-risk route">
            {chain.map((item, i) => <ChainRow key={i} item={item} />)}
          </ol>
          {!focus.route?.nodes.some((n) => n.on_fix_list) && (
            <p className="apx-cap">None of this route&apos;s hosts is on the fix list; the hosts to fix lie on other routes.</p>
          )}
          <p className="apx-cap">The highest-risk of the stored routes (a capped list, not a count of routes).</p>
        </>
      )}

      {focus.state !== "exposed" && (focus.fix?.exposed_targets?.length ?? 0) > 0 && (
        <p className="apx-cap" data-tone="weak">
          {focus.fix!.exposed_targets!.length === 1
            ? `${focus.fix!.exposed_targets![0].label} is a crown jewel exposed to the internet outright — fixing the hosts above does not protect it; remove its own exposure.`
            : `${focus.fix!.exposed_targets!.length} crown jewels are exposed to the internet outright — remove their own exposure, which fixing other hosts does not do.`}
        </p>
      )}

      {bars.length > 0 ? (
        <div className="apx-bars">
          <h4>Share of modelled risk removed</h4>
          <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
            {bars.map((b) => (
              <li key={b.key} className="apx-bar">
                <span className="apx-bar-name" title={b.name}>{b.name}</span>
                <span className="apx-bar-val">{b.value}</span>
                <span className="apx-track" aria-hidden="true"><i style={{ width: `${b.width}%` }} /></span>
                <span className="apx-bar-sub">{b.sub}</span>
              </li>
            ))}
          </ul>
          <p className="apx-cap">Each bar is that host fixed on its own, so the bars do not add up. A modelled ordering weight, not a probability.</p>
        </div>
      ) : focus.state === "reachable" && focus.fix && focus.fix.size > 1 ? (
        <p className="apx-quiet" style={{ marginTop: "var(--space-3)" }}>
          No single host removes any modelled risk on its own; the fixes have to be made together.
        </p>
      ) : null}
    </>
  );
}
