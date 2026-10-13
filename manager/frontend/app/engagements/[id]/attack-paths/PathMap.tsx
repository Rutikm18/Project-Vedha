"use client";

import { useMemo } from "react";
import { layoutPathMap, MAP, truncateLabel, type MapEdge, type MapNode, type PathSummary } from "../../../../lib/attack-paths";

const MAX_ROUTES_DRAWN = 12;

function edgePath(e: MapEdge): string {
  if (e.backward) {
    // A step against the flow (routes disagree about direction): arc over the top.
    return `M ${e.x1} ${e.y1} C ${e.x1 + 70} ${e.y1 - 46}, ${e.x2 - 70} ${e.y2 - 46}, ${e.x2} ${e.y2}`;
  }
  const dx = Math.max(24, (e.x2 - e.x1) / 2);
  return `M ${e.x1} ${e.y1} C ${e.x1 + dx} ${e.y1}, ${e.x2 - dx} ${e.y2}, ${e.x2} ${e.y2}`;
}

function roleTag(n: MapNode): string {
  const tags: string[] = [];
  if (n.isEntry) tags.push("ENTRY");
  if (n.isTarget) tags.push("CROWN JEWEL");
  if (n.isChoke) tags.push("FIX HERE");
  return tags.join(" · ");
}

/**
 * The highest-risk routes drawn together: entry points left, crown jewels right,
 * shared hosts where routes converge. Each role is written in the box as well as
 * coloured, and the table beside it lists the same routes for keyboard and screen
 * reader users.
 */
export function PathMap({
  items, chokeIds, selectedId,
}: {
  items: PathSummary[];
  chokeIds: ReadonlySet<string>;
  selectedId: string | null;
}) {
  const map = useMemo(() => layoutPathMap(items, chokeIds, MAX_ROUTES_DRAWN), [items, chokeIds]);
  if (map.nodes.length === 0) return null;

  const selected = items.find((p) => p.id === selectedId) ?? null;
  const onSelected = new Set(selected?.nodes.map((n) => n.asset_id) ?? []);
  const summary = `Route map: ${map.shown} route${map.shown === 1 ? "" : "s"} across ${map.nodes.length} hosts. `
    + "The same routes are listed in the table.";

  return (
    <div className="ap-map-scroll" role="region" aria-label="Route map (scrollable)" tabIndex={0}>
      <svg className="ap-map" role="img" aria-label={summary} width={map.width} height={map.height}
        viewBox={`0 0 ${map.width} ${map.height}`}>
        <defs>
          <marker id="ap-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--text-muted)" />
          </marker>
          <marker id="ap-arrow-sel" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--accent)" />
          </marker>
        </defs>
        {map.edges.map((e) => {
          const isSel = !!selected && e.paths.includes(selected.id);
          return (
            <path key={e.key} className="ap-edge" d={edgePath(e)}
              data-selected={isSel} data-backward={e.backward} data-dim={!!selected && !isSel}
              markerEnd={`url(#${isSel ? "ap-arrow-sel" : "ap-arrow"})`}
              style={{ strokeWidth: isSel ? undefined : 1 + 0.5 * Math.min(e.paths.length - 1, 3) }} />
          );
        })}
        {map.nodes.map((n) => {
          const tag = roleTag(n);
          return (
            <g key={n.id} className="ap-node" transform={`translate(${n.x} ${n.y})`}
              data-entry={n.isEntry} data-target={n.isTarget} data-choke={n.isChoke}
              data-dim={!!selected && !onSelected.has(n.id)}>
              <title>{`${n.label}${tag ? ` — ${tag.toLowerCase()}` : ""}`}</title>
              <rect width={MAP.nodeWidth} height={MAP.nodeHeight} rx={6} />
              <text x={8} y={tag ? 15 : 22} fontSize={12}>{truncateLabel(n.label)}</text>
              {tag && <text className="ap-tag" x={8} y={28}>{tag}</text>}
            </g>
          );
        })}
      </svg>
    </div>
  );
}
