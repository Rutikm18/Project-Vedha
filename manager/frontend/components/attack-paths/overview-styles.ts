/**
 * Styles for the attack-paths overview: the triage tiles, the engagement ladder, the jewel
 * meter and the "fix first" card. One string, rendered once by <AttackPathStyles />.
 *
 * Layout follows the container, not the viewport: the sidebar takes 216 px, so the panel is
 * narrower than the window. `apxp` is the whole panel body (two columns from 760 px); `apx` is
 * the ladder itself (a row stacks its name above its facts under 560 px).
 *
 * Marks that carry meaning (connectors, outlines) use --text-muted, which reaches 3:1; the
 * border tokens do not (see tests/attack-paths-contrast.test.ts). Type sizes are the tokens.
 */
export const OVERVIEW_STYLES = `
.apxp { container: apxp / inline-size; }

/* ── triage tiles ─────────────────────────────────────────────── */
.apx-tiles { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border-bottom: var(--hairline) solid var(--border-subtle); }
.apx-tile { padding: var(--space-3) var(--space-5); min-width: 0; border-right: var(--hairline) solid var(--border-subtle); border-top: 3px solid transparent; }
.apx-tile:last-child { border-right: 0; }
.apx-tile[data-tone="critical"] { border-top-color: var(--sev-critical-color); }
.apx-tile[data-tone="high"] { border-top-color: var(--sev-high-color); }
.apx-tile-label { font-size: var(--fs-body-s); color: var(--text-secondary); }
.apx-tile-value { display: flex; align-items: baseline; gap: 6px; margin: 2px 0; color: var(--text-primary); }
.apx-tile-value > span { font-size: var(--fs-display-m); font-weight: 600; letter-spacing: -0.02em; line-height: 1.1; }
.apx-tile-value > small { font-size: var(--fs-body); color: var(--text-muted); }
.apx-tile-sub { font-size: var(--fs-body-s); color: var(--text-muted); line-height: 1.4; }
.apx-skel { height: 92px; }
@container apxp (max-width: 640px) {
  .apx-tiles { grid-template-columns: minmax(0, 1fr); }
  .apx-tile { border-right: 0; border-bottom: var(--hairline) solid var(--border-subtle); }
  .apx-tile:last-child { border-bottom: 0; }
}

/* ── ladder and card side by side ─────────────────────────────── */
.apx-split { display: grid; grid-template-columns: minmax(0, 1fr); }
.apx-focus { border-top: var(--hairline) solid var(--border-subtle); background: var(--bg-surface); padding: var(--space-4) var(--space-5); min-width: 0; }
@container apxp (min-width: 760px) {
  .apx-split[data-focus="true"] { grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr); }
  .apx-split[data-focus="true"] .apx-focus { border-top: 0; border-left: var(--hairline) solid var(--border-subtle); }
}

/* ── ladder rows ──────────────────────────────────────────────── */
.apx { container: apx / inline-size; min-width: 0; }
.apo-li { display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; }
.apo-compute { margin-right: var(--space-5); white-space: nowrap; display: inline-flex; align-items: center; gap: 6px; }
.apx-spin { animation: apx-spin 0.9s linear infinite; }
@keyframes apx-spin { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .apx-spin { animation: none; } }
.apo-row { display: grid; grid-template-columns: minmax(0, 11rem) minmax(0, 1fr) 16px; gap: var(--space-1) var(--space-4); align-items: center; padding: var(--space-3) var(--space-5); text-decoration: none; color: inherit; }
.apo-name { min-width: 0; display: grid; gap: 2px; }
.apo-name strong { font-size: var(--fs-body); font-weight: 650; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.apo-status { font-size: var(--fs-label); letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); white-space: nowrap; }
.apo-facts { min-width: 0; display: grid; gap: 4px; }
.apo-line { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; }
.apo-headline { font-size: var(--fs-body); font-weight: 650; color: var(--text-primary); }
.apo-ways { font-size: var(--fs-body-s); color: var(--text-secondary); }
.apo-ways::before { content: "·"; margin-right: 10px; color: var(--text-muted); }
.apo-detail { font-size: var(--fs-body-s); color: var(--text-secondary); line-height: 1.45; }
.apo-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px; font-size: var(--fs-label); color: var(--text-muted); }
.apo-trend { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; font-size: var(--fs-body-s); color: var(--text-secondary); }
.apx-spark { display: block; flex-shrink: 0; }
.apo-chip { display: inline-flex; align-items: center; gap: 4px; padding: 1px 7px; border-radius: 999px; border: var(--hairline) solid var(--border-default); background: var(--bg-surface); color: var(--text-secondary); white-space: nowrap; }
.apo-chip[data-tone="weak"] { color: var(--sev-medium-color); border-color: var(--sev-medium-color); }
.apo-chip[data-tone="firm"] { color: var(--nominal-color); border-color: var(--nominal-color); }
.apo-go { color: var(--text-muted); flex-shrink: 0; }
.apo-note { margin: 0; padding: var(--space-3) var(--space-5); font-size: var(--fs-label); line-height: 1.5; color: var(--text-muted); border-top: var(--hairline) solid var(--border-subtle); }
@container apx (max-width: 560px) {
  .apo-li { grid-template-columns: minmax(0, 1fr); }
  .apo-compute { margin: 0 var(--space-5) var(--space-3); justify-self: start; }
  .apo-row { grid-template-columns: minmax(0, 1fr) 16px; }
  .apo-ways::before { content: none; }
  .apo-name { grid-column: 1; }
  .apo-facts { grid-column: 1 / -1; grid-row: 2; }
  .apo-go { grid-column: 2; grid-row: 1; }
}

/* ── jewel meter: one diamond per crown jewel ────────────────── */
.apx-meter { display: inline-flex; align-items: center; gap: 2px; }
.apx-meter svg { display: block; flex-shrink: 0; }
.apx-meter-more { font-size: var(--fs-label); color: var(--text-muted); margin-left: 3px; }

/* ── "fix first" card ─────────────────────────────────────────── */
.apx-focus h4 { margin: 0; font-size: var(--fs-label); letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); font-weight: 600; }
.apx-focus-who { font-size: var(--fs-body); font-weight: 650; color: var(--text-primary); margin: 2px 0 var(--space-3); }
.apx-lead { font-size: var(--fs-body-s); color: var(--text-secondary); line-height: 1.45; margin: 0 0 var(--space-3); }
.apx-chain { list-style: none; margin: 0 0 var(--space-2); padding: 0; }
.apx-chain > li { display: grid; grid-template-columns: 22px minmax(0, 1fr); gap: 0 10px; position: relative; padding-bottom: var(--space-3); }
.apx-chain > li:last-child { padding-bottom: 0; }
.apx-chain > li::before { content: ""; position: absolute; left: 10px; top: 22px; bottom: 0; width: 2px; background: var(--text-muted); opacity: 0.7; }
.apx-chain > li:last-child::before, .apx-chain > li[data-gap="true"]::before { display: none; }
.apx-node { width: 22px; height: 22px; display: grid; place-items: center; background: var(--bg-surface); position: relative; }
.apx-role { font-size: var(--fs-label); font-weight: 650; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-secondary); }
.apx-role[data-role="fix"] { color: var(--accent); }
.apx-role[data-role="jewel"] { color: var(--sev-high-color); }
.apx-role[data-role="exposed"] { color: var(--sev-critical-color); }
.apx-host { font-size: var(--fs-body); font-weight: 600; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.apx-hop { font-size: var(--fs-label); color: var(--text-muted); margin-top: 2px; line-height: 1.4; }
.apx-hop[data-tone="weak"] { color: var(--sev-medium-color); }
/* Tailwind's reset makes every svg a block; this one sits in the sentence. */
.apx-hop svg { display: inline-block; vertical-align: -1px; margin-right: 3px; }
.apx-more { font-size: var(--fs-label); color: var(--text-muted); padding: 0 0 var(--space-3) 32px; }
.apx-bars { margin-top: var(--space-4); padding-top: var(--space-3); border-top: var(--hairline) solid var(--border-subtle); }
.apx-bar { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 2px 10px; align-items: baseline; margin: var(--space-2) 0 0; }
.apx-bar-name { font-size: var(--fs-body-s); font-weight: 600; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.apx-bar-val { font-size: var(--fs-body-s); font-weight: 650; color: var(--text-primary); font-variant-numeric: tabular-nums; }
.apx-track { grid-column: 1 / -1; height: 6px; border-radius: 3px; background: var(--track-bg); position: relative; overflow: hidden; }
.apx-track > i { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 3px; background: var(--accent); }
.apx-bar-sub { grid-column: 1 / -1; font-size: var(--fs-label); color: var(--text-muted); }
.apx-cap { font-size: var(--fs-label); color: var(--text-muted); margin: var(--space-2) 0 0; line-height: 1.45; }
.apx-quiet { font-size: var(--fs-body-s); color: var(--text-muted); margin: 0; }
.apx-open { display: inline-flex; align-items: center; gap: 4px; margin-top: var(--space-3); font-size: var(--fs-body-s); font-weight: 650; color: var(--accent); text-decoration: none; }
`;
