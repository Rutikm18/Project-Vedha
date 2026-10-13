/** Styles for the attack-paths page. Tokens only (see DESIGN_SYSTEM.md): colour is
 *  always paired with a word, and nothing here depends on hover. */
export const ATTACK_PATH_STYLES = `
.ap-page { display: grid; gap: var(--space-4); padding: var(--space-4); max-width: 1320px; margin: 0 auto; width: 100%; }
.ap-back { display: inline-flex; align-items: center; gap: 6px; color: var(--text-secondary); font-size: 12px; text-decoration: none; width: fit-content; }
.ap-back:hover { color: var(--accent); }
.ap-card { background: var(--bg-panel); border: 0.5px solid var(--border-subtle); border-radius: var(--radius-lg); min-width: 0; }
.ap-card-head { display: flex; align-items: center; justify-content: space-between; gap: var(--space-3); flex-wrap: wrap; padding: var(--space-3) var(--space-4); border-bottom: 0.5px solid var(--border-subtle); }
.ap-card-title { display: flex; align-items: center; gap: var(--space-2); margin: 0; font-size: 13px; font-weight: 650; color: var(--text-primary); }
.ap-card-title svg { color: var(--accent); }
.ap-card-meta { font-size: 11.5px; color: var(--text-muted); }
.ap-card-body { padding: var(--space-4); display: grid; gap: var(--space-3); }
/* A table or map inside scrolls in its own wrapper; without this a grid track grows to its min-content and the text beside it overflows the card. */
.ap-card-body > * { min-width: 0; }

.ap-status { display: flex; align-items: center; justify-content: space-between; gap: var(--space-3); flex-wrap: wrap; }
.ap-status-text { display: grid; gap: 2px; font-size: 12px; color: var(--text-secondary); }
.ap-status-text strong { color: var(--text-primary); font-size: 13px; }
.ap-num { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
.ap-fine { margin: 0; font-size: 11.5px; line-height: 1.5; color: var(--text-muted); }
.ap-beta { color: var(--text-secondary); }

.ap-chip { display: inline-flex; align-items: center; gap: 5px; padding: 2px 8px; border-radius: var(--r-pill); font-size: 11px; font-weight: 600; border: 0.5px solid var(--border-default); background: var(--bg-surface); color: var(--text-secondary); white-space: nowrap; }
.ap-chip[data-tone="firm"] { color: var(--nominal-color); border-color: var(--nominal-color); }
.ap-chip[data-tone="weak"] { color: var(--sev-medium-color); border-color: var(--sev-medium-color); background: var(--sev-medium-bg); }
.ap-chip[data-tone="inferred"] { color: var(--text-secondary); }
.ap-chip[data-priority="critical"] { color: var(--sev-critical-color); border-color: var(--sev-critical-color); background: var(--sev-critical-bg); }
.ap-chip[data-priority="high"] { color: var(--sev-high-color); border-color: var(--sev-high-color); background: var(--sev-high-bg); }
.ap-chip[data-priority="medium"] { color: var(--sev-medium-color); border-color: var(--sev-medium-color); background: var(--sev-medium-bg); }

.ap-notes { display: grid; gap: var(--space-2); margin: 0; padding: 0; list-style: none; }
.ap-note { display: flex; gap: var(--space-2); align-items: flex-start; font-size: 12px; line-height: 1.5; color: var(--text-secondary); }
.ap-note svg { flex-shrink: 0; margin-top: 2px; }
.ap-note[data-tone="weak"] svg { color: var(--sev-medium-color); }
.ap-note[data-tone="inferred"] svg, .ap-note[data-tone="neutral"] svg { color: var(--text-faint); }
.ap-confidence { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-secondary); }

.ap-callout { display: grid; gap: var(--space-2); padding: var(--space-3) var(--space-4); border-radius: var(--radius-md); border: 0.5px solid var(--sev-medium-color); background: var(--sev-medium-bg); }
.ap-callout[data-tone="critical"] { border-color: var(--sev-critical-color); background: var(--sev-critical-bg); }
.ap-callout h3 { margin: 0; font-size: 13.5px; font-weight: 650; color: var(--text-primary); }
.ap-reasons { display: grid; gap: var(--space-3); margin: 0; padding: 0; list-style: none; }
.ap-reason { display: grid; gap: 2px; padding-left: var(--space-3); border-left: 2px solid var(--border-default); }
.ap-reason strong { font-size: 12.5px; color: var(--text-primary); }
.ap-reason span { font-size: 12px; color: var(--text-secondary); line-height: 1.5; }
.ap-reason em { font-style: normal; font-size: 12px; color: var(--text-muted); line-height: 1.5; }

.ap-headline { margin: 0; font-size: 15px; font-weight: 650; color: var(--text-primary); line-height: 1.4; }
.ap-routes-lines { display: grid; gap: 4px; margin: 0; padding: 0; list-style: none; font-size: 12px; color: var(--text-secondary); }

.ap-table-wrap { overflow-x: auto; }
.ap-table-wrap:focus-visible, .ap-map-scroll:focus-visible { box-shadow: var(--focus-ring); border-radius: var(--radius-md); outline: none; }
.ap-table { width: 100%; min-width: 560px; border-collapse: collapse; font-size: 12.5px; }
.ap-table th { text-align: left; font-size: 11px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); padding: 8px 12px; background: var(--bg-surface); border-bottom: 0.5px solid var(--border-subtle); white-space: nowrap; }
.ap-table td { padding: 10px 12px; border-bottom: 0.5px solid var(--border-subtle); vertical-align: middle; color: var(--text-secondary); }
.ap-table tr:last-child td { border-bottom: 0; }
.ap-host { font-family: var(--font-mono); color: var(--text-primary); overflow-wrap: anywhere; }
.ap-arrow { color: var(--text-faint); margin: 0 6px; }
/* The app's reset makes every svg block-level; an arrow between two host names must stay inline. */
.ap-page svg.ap-arrow, .ap-page svg.ap-inline-icon { display: inline-block; vertical-align: -2px; }
.ap-page svg.ap-inline-icon { margin-right: 4px; }
.ap-route-cell { min-width: 190px; }
.ap-share { display: grid; grid-template-columns: 72px auto; align-items: center; gap: 8px; min-width: 150px; }
.ap-bar { height: 6px; border-radius: 3px; background: var(--track-bg); overflow: hidden; }
.ap-bar > span { display: block; height: 100%; background: var(--accent); border-radius: 3px; }
.ap-rowbtn { all: unset; box-sizing: border-box; display: block; width: 100%; cursor: pointer; border-radius: var(--radius-sm); }
.ap-rowbtn:focus-visible { box-shadow: var(--focus-ring); }
.ap-row[data-selected="true"] td { background: var(--accent-ghost); }
.ap-row[data-selected="true"] td:first-child { box-shadow: inset 3px 0 0 var(--accent); }

.ap-split { display: grid; gap: var(--space-4); grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); align-items: start; }
@media (max-width: 1100px) { .ap-split { grid-template-columns: minmax(0, 1fr); } }

.ap-map-scroll { overflow: auto; padding: var(--space-3); }
.ap-map text { font-family: var(--font-body); fill: var(--text-primary); }
.ap-map .ap-tag { font-size: 8.5px; letter-spacing: 0.05em; fill: var(--text-muted); font-weight: 650; }
.ap-map .ap-node rect { fill: var(--bg-surface); stroke: var(--border-default); stroke-width: 1; }
.ap-map .ap-node[data-entry="true"] rect { stroke: var(--accent); }
.ap-map .ap-node[data-target="true"] rect { stroke: var(--sev-critical-color); stroke-width: 1.5; }
.ap-map .ap-node[data-choke="true"] rect { stroke-dasharray: 4 2; stroke: var(--sev-high-color); stroke-width: 1.5; }
.ap-map .ap-node[data-choke="true"] .ap-tag { fill: var(--sev-high-color); }
.ap-map .ap-node[data-target="true"] .ap-tag { fill: var(--sev-critical-color); }
.ap-map .ap-node[data-entry="true"] .ap-tag { fill: var(--accent); }
.ap-map .ap-node[data-dim="true"] { opacity: 0.35; }
/* Edges say which host connects to which, so they are content, not decoration: 3:1 against the panel (WCAG 1.4.11). The border tokens are 1.5 to 2.7:1. */
.ap-map .ap-edge { fill: none; stroke: var(--text-muted); stroke-width: 1.25; }
.ap-map .ap-edge[data-backward="true"] { stroke-dasharray: 3 3; }
.ap-map .ap-edge[data-selected="true"] { stroke: var(--accent); stroke-width: 2.5; }
.ap-map .ap-edge[data-dim="true"] { opacity: 0.3; }
/* Zone map: a subnet is a box, a step between subnets an arrow. Role is words; marks use --text-muted (3:1). */
.ap-zones .ap-zone-node rect { fill: var(--bg-surface); stroke: var(--text-muted); stroke-width: 1.25; }
.ap-zones .ap-zone-node[data-inferred="true"] rect { stroke-dasharray: 2 3; }
.ap-zones .ap-zone-node[data-entry="true"] rect { stroke: var(--accent); stroke-width: 2; }
.ap-zones .ap-zone-node[data-jewel="true"] rect { stroke: var(--sev-critical-color); stroke-width: 2; }
.ap-zones .ap-zone-node[data-entry="true"] .ap-tag { fill: var(--accent); }
.ap-zones .ap-zone-node[data-jewel="true"] .ap-tag { fill: var(--sev-critical-color); }
.ap-zones .ap-zone-node[data-fix="true"] .ap-tag { fill: var(--sev-high-color); }
.ap-zones .ap-zone-sub { fill: var(--text-secondary); }
.ap-zones .ap-zone-edge path { fill: none; stroke: var(--text-muted); }
.ap-zones .ap-zone-edge[data-weak="true"] path { stroke-dasharray: 6 4; }
.ap-legend { display: flex; flex-wrap: wrap; gap: var(--space-2) var(--space-4); font-size: 11.5px; color: var(--text-secondary); }
.ap-legend span { display: inline-flex; align-items: center; gap: 6px; }
.ap-swatch { width: 14px; height: 10px; border-radius: 2px; border: 1.5px solid var(--border-default); background: var(--bg-surface); }
.ap-swatch[data-kind="entry"] { border-color: var(--accent); }
.ap-swatch[data-kind="target"] { border-color: var(--sev-critical-color); }
.ap-swatch[data-kind="choke"] { border-color: var(--sev-high-color); border-style: dashed; }

.ap-hops { display: grid; gap: 0; margin: 0; padding: 0; list-style: none; }
.ap-hop { position: relative; display: grid; gap: 6px; padding: 0 0 var(--space-4) var(--space-5); border-left: 1.5px solid var(--border-default); margin-left: 8px; }
.ap-hop:last-child { border-left-color: transparent; padding-bottom: 0; }
.ap-hop::before { content: attr(data-step); position: absolute; left: -11px; top: -1px; width: 20px; height: 20px; border-radius: 50%; background: var(--bg-panel); border: 1.5px solid var(--border-default); font-size: 10.5px; font-weight: 650; display: grid; place-items: center; color: var(--text-secondary); font-family: var(--font-mono); }
.ap-hop-route { font-size: 12.5px; color: var(--text-primary); overflow-wrap: anywhere; }
.ap-hop-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.ap-hop-text { margin: 0; font-size: 12px; color: var(--text-secondary); line-height: 1.55; }
.ap-enabling-finding { display: grid; gap: 5px; padding: 12px 0; border-block: 1px solid var(--border-subtle); font-size: 12px; }
.ap-enabling-finding strong { font-weight: 550; color: var(--text-secondary); }
.ap-enabling-finding a { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; overflow-wrap: anywhere; }
.ap-enabling-finding span, .ap-enabling-finding p { color: var(--text-secondary); font-size: 11px; line-height: 1.6; margin: 0; overflow-wrap: anywhere; }
.ap-start { margin: 0 0 var(--space-3); font-size: 12.5px; color: var(--text-primary); }

.ap-empty { display: grid; place-items: center; gap: var(--space-2); padding: var(--space-7) var(--space-4); text-align: center; color: var(--text-muted); font-size: 12.5px; }
.ap-spin { animation: ap-spin 0.9s linear infinite; }
@keyframes ap-spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .ap-spin { animation: none; } }
.ap-sr { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
@media (pointer: coarse) { .ap-rowbtn, .ap-table td { min-height: 44px; } }
`;
