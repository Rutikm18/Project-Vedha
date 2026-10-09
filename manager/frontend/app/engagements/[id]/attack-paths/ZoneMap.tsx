"use client";

import { useMemo } from "react";
import { layoutZoneMap, truncateLabel, ZONE, type ZoneEdge, type ZoneNode, type ZoneView } from "../../../../lib/attack-paths";

function edgePath(e: ZoneEdge): string {
  if (e.backward) {
    // Against the flow, or inside one column: an arc over the top, never hidden.
    return `M ${e.x1} ${e.y1} C ${e.x1 + 70} ${e.y1 - 56}, ${e.x2 - 70} ${e.y2 - 56}, ${e.x2} ${e.y2}`;
  }
  const dx = Math.max(24, (e.x2 - e.x1) / 2);
  return `M ${e.x1} ${e.y1} C ${e.x1 + dx} ${e.y1}, ${e.x2 - dx} ${e.y2}, ${e.x2} ${e.y2}`;
}

function hostsText(n: ZoneNode): string {
  if (n.hosts == null) return "hosts not recorded";
  const stale = (n.stale_hosts ?? 0) > 0 ? ` · ${n.stale_hosts} not seen recently` : "";
  return `${n.hosts} host${n.hosts === 1 ? "" : "s"}${stale}`;
}

/**
 * The stored routes aggregated into the subnets they cross: a subnet is a box (its range, how many hosts
 * were seen, and its roles in WORDS), a step between subnets is an arrow (dashed, and worded "assumed",
 * when it rests on an assumed link). At most twelve boxes, so this stays readable where a host-by-host
 * graph would not. The two tables below say exactly the same thing for keyboard and screen-reader users.
 */
export function ZoneMap({ view }: { view: ZoneView }) {
  const layout = useMemo(() => layoutZoneMap(view.zones, view.links), [view.zones, view.links]);
  if (layout.nodes.length === 0) return null;
  const label = `Subnet map: ${layout.nodes.length} subnet${layout.nodes.length === 1 ? "" : "s"} and ${layout.edges.length} step${layout.edges.length === 1 ? "" : "s"} between them. The same information is in the tables below.`;
  const byKey = new Map(layout.nodes.map((n) => [n.key, n]));

  return (
    <div>
      <div className="ap-map-scroll" role="region" aria-label="Subnet map (scrollable)" tabIndex={0}>
        <svg className="ap-map ap-zones" role="img" aria-label={label} width={layout.width} height={layout.height} viewBox={`0 0 ${layout.width} ${layout.height}`}>
          <defs>
            <marker id="ap-zone-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--text-muted)" />
            </marker>
          </defs>
          {/* Crossing steps share a midpoint, so a label on each would sit on the other. The count is the line's
              weight and the table's column; "assumed" is the dash, said in the legend and the table. */}
          {layout.edges.map((e) => (
            <g key={e.key} className="ap-zone-edge" data-weak={e.weak}>
              <path d={edgePath(e)} markerEnd="url(#ap-zone-arrow)" style={{ strokeWidth: 1.25 + 0.5 * Math.min(e.routes - 1, 4) }}>
                <title>{`${byKey.get(e.from)?.label} → ${byKey.get(e.to)?.label}: ${e.routes} listed route${e.routes === 1 ? "" : "s"}, ${e.basisLabel.toLowerCase()}`}</title>
              </path>
            </g>
          ))}
          {layout.nodes.map((n) => (
            <g key={n.key} className="ap-zone-node" transform={`translate(${n.x} ${n.y})`}
              data-entry={n.entry} data-jewel={n.jewel} data-fix={n.fix} data-inferred={n.inferred}>
              <title>{`${n.label}: ${hostsText(n)}${n.roles.length ? `. ${n.roles.join(", ")}` : ""}. ${n.routes} listed route${n.routes === 1 ? "" : "s"} pass through it.`}</title>
              <rect width={ZONE.boxWidth} height={ZONE.boxHeight} rx={8} />
              <text x={10} y={20} fontSize={12.5} fontWeight={650}>{truncateLabel(n.label, 24)}</text>
              <text className="ap-zone-sub" x={10} y={37} fontSize={11}>{hostsText(n)}</text>
              <text className="ap-tag" x={10} y={55}>{n.roles.length ? n.roles.join(" · ").toUpperCase() : "ON A ROUTE"}</text>
            </g>
          ))}
        </svg>
      </div>

      <div className="ap-legend" aria-label="Legend">
        <span><i className="ap-swatch" data-kind="entry" /> Entry subnet</span>
        <span><i className="ap-swatch" data-kind="target" /> Crown jewel subnet</span>
        <span><svg width="26" height="8" aria-hidden="true"><line x1="1" y1="4" x2="25" y2="4" stroke="var(--text-muted)" strokeWidth="1.5" /></svg> Step observed or within a subnet</span>
        <span><svg width="26" height="8" aria-hidden="true"><line x1="1" y1="4" x2="25" y2="4" stroke="var(--text-muted)" strokeWidth="1.5" strokeDasharray="6 4" /></svg> Step on an assumed link</span>
        <span>Thicker line = more listed routes</span>
      </div>

      <div className="ap-table-wrap" role="region" aria-label="Subnets (table)" tabIndex={0}>
        <table className="ap-table">
          <caption className="ap-sr">Subnets the listed routes touch</caption>
          <thead><tr><th scope="col">Subnet</th><th scope="col">Hosts seen</th><th scope="col">Role on the routes</th><th scope="col">Listed routes through it</th></tr></thead>
          <tbody>
            {layout.nodes.map((n) => (
              <tr key={n.key}>
                <td className="ap-host">{n.label}</td>
                <td>{n.hosts ?? "not recorded"}{(n.stale_hosts ?? 0) > 0 ? ` (${n.stale_hosts} not seen recently)` : ""}</td>
                <td>{n.roles.length ? n.roles.join(", ") : "On a route"}</td>
                <td className="ap-num">{n.routes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {layout.edges.length > 0 && (
        <div className="ap-table-wrap" role="region" aria-label="Steps between subnets (table)" tabIndex={0}>
          <table className="ap-table">
            <caption className="ap-sr">Steps between subnets taken by the listed routes</caption>
            <thead><tr><th scope="col">From</th><th scope="col">To</th><th scope="col">Listed routes</th><th scope="col">Basis</th></tr></thead>
            <tbody>
              {layout.edges.map((e) => (
                <tr key={e.key}>
                  <td className="ap-host">{byKey.get(e.from)?.label}</td>
                  <td className="ap-host">{byKey.get(e.to)?.label}</td>
                  <td className="ap-num">{e.routes}</td>
                  <td>{e.weak ? <span className="ap-chip" data-tone="weak">{e.basisLabel}</span> : e.basisLabel}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
