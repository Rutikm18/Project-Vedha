/**
 * Styles shared by the campaign views (pipeline, jobs, findings, raw facts, job queue). One
 * vocabulary: a card is a bordered panel; a section head is a title, a count and an optional
 * aside; a chip is a small labelled value. Status and severity always carry a word, never
 * colour alone. Everything wraps; at phone width controls reach 44px.
 */
export const CAMPAIGN_CSS = `
.cpg { display: flex; flex-direction: column; gap: 18px; min-width: 0; }
.cpg-card { border: var(--hairline) solid var(--border-subtle); border-radius: 12px; background: var(--bg-panel); min-width: 0; }
.cpg-head { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; margin: 0 0 10px; }
.cpg-head h3 { margin: 0; color: var(--text-primary); font: 700 13px/1.3 var(--font-ui); }
.cpg-head .cpg-count { color: var(--text-muted); font: 600 12px/1 var(--font-mono); }
.cpg-head .cpg-aside { margin-left: auto; color: var(--text-muted); font: 500 11.5px/1.3 var(--font-ui); }
.cpg-chip { display: inline-flex; align-items: center; gap: 5px; padding: 2px 8px; border-radius: 999px; border: var(--hairline) solid var(--border-subtle); background: var(--bg-surface); color: var(--text-secondary); font: 600 11px/1.4 var(--font-ui); white-space: nowrap; }
.cpg-chip[data-tone="accent"] { color: var(--accent); background: var(--accent-ghost); border-color: transparent; }
.cpg-chip[data-tone="warn"] { color: var(--sev-medium-color); background: var(--sev-medium-bg); border-color: var(--sev-medium-edge, transparent); }
.cpg-chip[data-tone="bad"] { color: var(--sev-critical-color); border-color: var(--sev-critical-color); background: transparent; }
.cpg-mono { font-family: var(--font-mono); }
.cpg-dim { color: var(--text-muted); font: 500 11.5px/1.4 var(--font-ui); }
.cpg-dim b { color: var(--text-secondary); font-weight: 650; }
.cpg-link { display: inline-flex; align-items: center; gap: 4px; color: var(--accent); font: 650 11.5px/1.3 var(--font-ui); text-decoration: none; }
.cpg-link:hover { text-decoration: underline; text-underline-offset: 3px; }
.cpg-sev { display: inline-flex; align-items: center; gap: 5px; padding: 1px 7px; border-radius: 5px; border: var(--hairline) solid currentColor; font: 800 9.5px/1.5 var(--font-ui); letter-spacing: .05em; text-transform: uppercase; }

/* status band */
.cpg-band { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 16px; padding: 12px 16px; }
.cpg-state { display: inline-flex; align-items: center; gap: 8px; }
.cpg-state i { width: 9px; height: 9px; border-radius: 50%; flex: none; }
.cpg-state i[data-live="true"] { animation: pulse 1.4s infinite; }
.cpg-state strong { color: var(--text-primary); font: 700 13px/1.3 var(--font-ui); }
.cpg-state small { color: var(--text-muted); font: 500 11px/1.3 var(--font-ui); }
.cpg-rollup { margin-left: auto; display: flex; flex-wrap: wrap; align-items: center; gap: 4px 14px; }
.cpg-rollup span { color: var(--text-muted); font: 500 11.5px/1.3 var(--font-ui); }
.cpg-rollup b { color: var(--text-primary); }
.cpg-links { display: flex; gap: 14px; }
.cpg-rollup + .cpg-links { margin-left: 4px; }
.cpg-reasons { display: flex; flex-direction: column; gap: 4px; padding: 10px 14px; border-radius: 10px; border: var(--hairline) solid var(--cpg-tone, var(--border-subtle)); background: var(--bg-panel); }
.cpg-reasons span { color: var(--text-secondary); font: 500 12px/1.5 var(--font-ui); }
.cpg-reasons span b { color: var(--cpg-tone); }
.cpg-reasons code { color: var(--text-faint); font: 500 10.5px/1.5 var(--font-mono); overflow-wrap: anywhere; }
.cpg-strip { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 16px; padding: 8px 14px; }
.cpg-strip .cpg-label { color: var(--text-faint); font: 700 10.5px/1 var(--font-ui); letter-spacing: .12em; text-transform: uppercase; }
.cpg-strip span { color: var(--text-muted); font: 500 12px/1.4 var(--font-ui); }
.cpg-strip b { color: var(--text-primary); }
.cpg-strip .cpg-end { margin-left: auto; font-family: var(--font-mono); font-size: 11px; }

/* pipeline */
.cpg-pipe-head { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: var(--hairline) solid var(--border-subtle); }
.cpg-pipe-head h3 { margin: 0; color: var(--text-primary); font: 700 13px/1.3 var(--font-ui); }
.cpg-pipe-head span { color: var(--text-muted); font: 600 11.5px/1 var(--font-mono); }
.cpg-track { height: 4px; background: var(--border-subtle); }
.cpg-track i { display: block; height: 100%; width: 100%; background: var(--accent); transform-origin: left center; transition: transform .6s; }
.cpg-phases { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 6px 0; margin: 0; padding: 14px 16px; list-style: none; }
.cpg-phase { display: flex; align-items: center; }
.cpg-phase > div { display: flex; flex-direction: column; align-items: center; gap: 5px; min-width: 84px; }
.cpg-phase i { width: 10px; height: 10px; border-radius: 50%; background: var(--border-accent); }
.cpg-phase[data-status="done"] i, .cpg-phase[data-status="active"] i { background: var(--accent); }
.cpg-phase[data-status="active"] i { box-shadow: 0 0 0 3px var(--accent-ghost); animation: pulse 1.4s infinite; }
.cpg-phase span { color: var(--text-secondary); font: 600 11px/1.3 var(--font-ui); text-align: center; }
.cpg-phase[data-status="pending"] span { color: var(--text-faint); }
.cpg-phase em { font-style: normal; color: var(--text-muted); font-family: var(--font-mono); }
.cpg-phase hr { width: 22px; height: 1px; margin: 0 0 18px; border: 0; background: var(--border-subtle); }
.cpg-phase[data-status="done"] hr { background: var(--accent); }
.cpg-sevs { display: flex; flex-wrap: wrap; gap: 6px 14px; padding: 10px 16px 12px; border-top: var(--hairline) solid var(--border-subtle); }
.cpg-sevs span { display: inline-flex; align-items: center; gap: 6px; color: var(--text-muted); font: 500 12px/1.3 var(--font-ui); }
.cpg-sevs i { width: 8px; height: 8px; border-radius: 2px; }
.cpg-sevs b { color: var(--text-primary); font-family: var(--font-mono); }
.cpg-sevs span[data-zero="true"] { color: var(--text-faint); }
.cpg-sevs span[data-zero="true"] b { color: var(--text-faint); }

/* jobs */
.cpg-jobs { display: flex; flex-direction: column; gap: 8px; }
.cpg-job { padding: 12px 16px; }
.cpg-job-top { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px; }
.cpg-job-top strong { color: var(--text-primary); font: 700 12.5px/1.3 var(--font-mono); }
.cpg-job-top .cpg-ref { margin-left: auto; color: var(--text-faint); font: 500 10.5px/1.3 var(--font-mono); }
.cpg-status { display: inline-flex; align-items: center; gap: 5px; color: var(--text-muted); font: 650 11px/1.3 var(--font-ui); text-transform: capitalize; }
.cpg-status i { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.cpg-status[data-status="running"] { color: var(--accent); }
.cpg-status[data-status="running"] i { animation: pulse 1.4s infinite; }
.cpg-status[data-status="completed"] { color: var(--nominal-color); }
.cpg-status[data-status="failed"] { color: var(--sev-critical-color); }
.cpg-status[data-status="cancelled"] { font-style: italic; }
.cpg-act { display: inline-flex; align-items: center; gap: 5px; min-height: 28px; padding: 0 10px; border-radius: 7px; border: var(--hairline) solid var(--border-subtle); background: transparent; color: var(--sev-high-color); font: 650 11px/1 var(--font-ui); cursor: pointer; }
.cpg-act:disabled { opacity: .6; cursor: wait; color: var(--text-faint); }
.cpg-facts { display: flex; flex-wrap: wrap; gap: 4px 14px; margin-top: 8px; color: var(--text-muted); font: 500 11.5px/1.4 var(--font-ui); }
.cpg-facts b { color: var(--text-secondary); }
.cpg-bar { height: 4px; margin-top: 10px; overflow: hidden; border-radius: 999px; background: var(--track-bg); }
.cpg-bar i { display: block; height: 100%; border-radius: 999px; transform-origin: left center; transition: transform var(--dur-base) var(--ease-out); }
.cpg-err { margin-top: 8px; color: var(--sev-high-color); font: 500 11.5px/1.4 var(--font-ui); }
.cpg-times { display: flex; flex-wrap: wrap; gap: 2px 14px; margin-top: 8px; color: var(--text-faint); font: 500 10.5px/1.5 var(--font-mono); }

/* findings */
.cpg-finds { display: flex; flex-direction: column; gap: 6px; }
.cpg-find { overflow: hidden; }
.cpg-find-head { display: grid; grid-template-columns: auto minmax(0, 1fr) auto auto; align-items: center; gap: 6px 10px; width: 100%; padding: 10px 14px; border: 0; background: transparent; color: inherit; text-align: left; cursor: pointer; font: inherit; }
.cpg-find-head strong { min-width: 0; color: var(--text-primary); font: 650 12.5px/1.4 var(--font-ui); overflow-wrap: anywhere; }
.cpg-find-meta { display: inline-flex; flex-wrap: wrap; justify-content: flex-end; gap: 6px; }
.cpg-find-body { padding: 2px 14px 14px; border-top: var(--hairline) solid var(--border-subtle); }
.cpg-steps { margin: 10px 0 0; padding-left: 18px; display: flex; flex-direction: column; gap: 6px; }
.cpg-steps li { color: var(--text-secondary); font: 500 12px/1.5 var(--font-ui); }
.cpg-cves { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.cpg-empty { margin: 0; padding: 14px 16px; border: var(--hairline) dashed var(--border-subtle); border-radius: 10px; color: var(--text-muted); font: 500 12.5px/1.5 var(--font-ui); }
.cpg-empty[data-tone="warn"] { color: var(--sev-medium-color); border-color: var(--sev-medium-edge, var(--border-subtle)); }
.cpg-empty[data-tone="bad"] { color: var(--sev-high-color); }

/* raw facts */
.cpg-raw-toggle { display: flex; align-items: center; gap: 10px; width: 100%; padding: 12px 16px; border: 0; background: transparent; color: inherit; text-align: left; cursor: pointer; font: inherit; }
.cpg-raw-text { display: flex; flex-wrap: wrap; align-items: baseline; gap: 2px 10px; flex: 1; min-width: 0; }
.cpg-raw-text strong { color: var(--text-primary); font: 700 12.5px/1.3 var(--font-ui); }
.cpg-raw-text span { color: var(--text-muted); font: 500 11.5px/1.4 var(--font-ui); }
.cpg-raw-toggle svg { flex: none; color: var(--text-faint); transition: transform .15s; }
.cpg-raw-toggle[aria-expanded="true"] svg { transform: rotate(180deg); }
.cpg-raw-body { padding: 0 16px 16px; border-top: var(--hairline) solid var(--border-subtle); }
.cpg-chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 12px 0; }
.cpg-chips button { min-height: 28px; padding: 0 11px; border-radius: 999px; border: var(--hairline) solid var(--border-subtle); background: transparent; color: var(--text-muted); font: 500 11px/1 var(--font-mono); cursor: pointer; }
.cpg-chips button[aria-pressed="true"] { border-color: var(--accent); background: var(--accent-ghost); color: var(--accent); }
.cpg-sub { border: var(--hairline) solid var(--border-subtle); border-radius: 10px; background: var(--bg-base, var(--bg-panel)); overflow: hidden; }
.cpg-sub > button { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; width: 100%; padding: 10px 14px; border: 0; background: transparent; color: inherit; text-align: left; cursor: pointer; font: inherit; }
.cpg-sub > button strong { color: var(--text-primary); font: 650 12px/1.3 var(--font-mono); }
.cpg-sub > button em { margin-left: auto; font-style: normal; color: var(--text-faint); }
.cpg-sub pre { margin: 0 14px 12px; padding: 12px; max-height: 420px; overflow: auto; border-radius: 8px; background: var(--bg-code, var(--bg-surface)); color: var(--text-secondary); font: 500 10.5px/1.5 var(--font-mono); }
.cpg-sub .cpg-scanners { display: flex; flex-wrap: wrap; gap: 4px 10px; padding: 0 14px 8px; color: var(--text-muted); font: 500 10.5px/1.4 var(--font-mono); }

/* job queue */
.cpg-q-filters { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 10px; margin-bottom: 10px; }
.cpg-q-filters select { min-height: 32px; padding: 0 9px; border-radius: 8px; border: var(--hairline) solid var(--border-subtle); background: var(--bg-panel); color: var(--text-secondary); font: 500 12px/1 var(--font-ui); }
.cpg-q-filters label { display: inline-flex; align-items: center; gap: 6px; color: var(--text-muted); font: 500 12px/1 var(--font-ui); cursor: pointer; }
.cpg-q-row { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 12px; padding: 9px 14px; border: var(--hairline) solid var(--border-subtle); border-radius: 10px; background: var(--bg-panel); }
.cpg-q-row strong { color: var(--text-primary); font: 650 12px/1.3 var(--font-ui); }
.cpg-q-row .cpg-ref { margin-left: auto; color: var(--text-faint); font: 500 10.5px/1.3 var(--font-mono); }
.cpg-q-list { display: flex; flex-direction: column; gap: 6px; }

@media (max-width: 720px) {
  .cpg-rollup { margin-left: 0; flex-basis: 100%; }
  .cpg-links { gap: 18px; flex-basis: 100%; padding-top: 8px; border-top: var(--hairline) solid var(--border-subtle); }
  .cpg-rollup + .cpg-links { margin-left: 0; }
  .cpg-link, .cpg-act { min-height: 44px; }
  .cpg-job-top .cpg-ref { margin-left: 0; flex-basis: 100%; }
  .cpg-find-head { grid-template-columns: auto minmax(0, 1fr) auto; }
  .cpg-find-head > .cpg-sev { grid-column: 1; grid-row: 1; }
  .cpg-find-head > strong { grid-column: 2; grid-row: 1; }
  .cpg-find-head > svg { grid-column: 3; grid-row: 1; }
  .cpg-find-meta { grid-column: 1 / -1; grid-row: 2; justify-content: flex-start; }
  .cpg-phases { gap: 10px 0; }
  .cpg-phase > div { min-width: 70px; }
  .cpg-phase hr { width: 12px; }
  .cpg-q-filters select { min-height: 44px; flex: 1 1 140px; }
  .cpg-q-filters label { min-height: 44px; }
  .cpg-q-row .cpg-ref { margin-left: 0; flex-basis: 100%; }
  .cpg-chips button { min-height: 44px; }
  .cpg-find-head, .cpg-raw-toggle, .cpg-sub > button { min-height: 44px; }
}
`;
