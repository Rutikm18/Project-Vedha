"use client";

/**
 * "How this score is calculated": the whole working of a finding's 0-1000 risk score
 * and its P0-P5 response priority, from the server's own explanation. Nothing here is
 * computed in the browser. Shown to operators and customers alike.
 */
import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, Check, Minus } from "lucide-react";
import {
  bandSentence, defaultsSummary, formatInputValue, formatPoints, placementSentence,
  type RiskDimension, type RiskExplanation,
} from "../../lib/risk-explanation";

export interface RiskExplanationApi {
  riskExplanation: <T>(id: string) => Promise<T>;
}

export function RiskScorePanel({ findingId, api, surface }: {
  findingId: string;
  api: RiskExplanationApi;
  surface: "manager" | "portal";
}) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["finding-risk-explanation", surface, findingId],
    queryFn: () => api.riskExplanation<RiskExplanation>(findingId),
    staleTime: 30_000,
  });

  if (isLoading) return <p className="rsx-status" aria-busy="true">Loading the calculation…</p>;
  if (error || !data) {
    return (
      <div className="rsx-status" role="alert" data-tone="error">
        <AlertTriangle size={15} aria-hidden />
        <span>The calculation did not load. The score itself is unaffected.</span>
        <button type="button" onClick={() => { void refetch(); }}>Retry</button>
      </div>
    );
  }
  return <Calculation e={data} showStored={surface === "manager"} />;
}

/** The server's reason, closed with exactly one full stop. */
const sentence = (text: string) => `${text.trim().replace(/\.+$/, "")}.`;

function Calculation({ e, showStored }: { e: RiskExplanation; showStored: boolean }) {
  const defaults = defaultsSummary(e);
  return (
    <div className="rsx">
      <style>{STYLES}</style>

      <p className="rsx-lead">
        The score is built from four weighted dimensions, added up to a figure out of {e.max}, then
        placed inside the band for this finding&apos;s severity. Every input is listed with the value
        used and where it came from.
      </p>

      <ol className="rsx-steps">
        <li>
          <h4><span aria-hidden>1</span> What went in</h4>
          <div className="rsx-dims">
            {e.dimensions.map((d) => <Dimension key={d.key} d={d} />)}
          </div>
          {defaults && (
            <p className="rsx-defaults" role="note"><AlertTriangle size={13} aria-hidden /> {defaults}</p>
          )}
        </li>

        <li>
          <h4><span aria-hidden>2</span> Add the four dimensions</h4>
          <p className="rsx-sum">
            {e.dimensions.map((d, i) => (
              <span key={d.key}>{i > 0 ? " + " : ""}<b>{d.points.toFixed(1)}</b></span>
            ))}
            {" = "}<b>{e.additive_score.toFixed(1)}</b> of {e.max}
          </p>
        </li>

        <li>
          <h4><span aria-hidden>3</span> Place it in the {e.severity} band</h4>
          <p>{bandSentence(e)}</p>
          <p className="rsx-final">
            <code>{placementSentence(e)}</code>
            <strong aria-label={`Final score ${e.score} out of ${e.max}`}>{e.score}</strong>
          </p>
        </li>
      </ol>

      <Context e={e} />
      <Priority e={e} />

      {showStored && e.stored_score !== null && (
        <p className="rsx-stored" data-sync={e.stored_in_sync || undefined}>
          {e.stored_in_sync
            ? `The stored sort value (${Math.round(e.stored_score)}) matches this score.`
            : `The stored sort value is ${Math.round(e.stored_score)}, not ${e.score}. The queue order catches up the next time this engagement is scanned or prioritised.`}
        </p>
      )}
      <p className="rsx-version">Model {e.model_version}</p>
    </div>
  );
}

function Dimension({ d }: { d: RiskDimension }) {
  return (
    <details className="rsx-dim">
      <summary>
        <span className="rsx-dim-name">{d.label}</span>
        <span className="rsx-dim-weight">{Math.round(d.weight * 100)}% of the score</span>
        <span className="rsx-bar" aria-hidden><i style={{ width: `${Math.round(d.value * 100)}%` }} /></span>
        <span className="rsx-dim-val">{d.value.toFixed(2)}</span>
        <span className="rsx-dim-pts">{formatPoints(d.points)}</span>
      </summary>
      <table>
        <caption className="rsx-sr">Inputs to {d.label}</caption>
        <thead>
          <tr><th scope="col">Input</th><th scope="col">Value used</th><th scope="col">Scaled 0-1</th><th scope="col">Weight</th><th scope="col">Source</th></tr>
        </thead>
        <tbody>
          {d.inputs.map((i) => (
            <tr key={i.key}>
              <th scope="row">{i.label}<small>{i.note}</small></th>
              <td>{formatInputValue(i)}</td>
              <td className="rsx-num">{i.normalized.toFixed(2)}</td>
              <td className="rsx-num">{Math.round(i.weight * 100)}%</td>
              <td><span className="rsx-src" data-source={i.source}>{i.source === "default" ? "Default" : "Recorded"}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </details>
  );
}

function Context({ e }: { e: RiskExplanation }) {
  const a = e.context.asset;
  return (
    <section className="rsx-block" aria-label="Asset context used">
      <h4>Asset context used</h4>
      {a ? (
        <p>
          {a.hostname || a.ip_address || "The affected asset"}: criticality{" "}
          <b>{a.criticality ?? "not recorded"}</b>; internet exposure from{" "}
          <b>{e.context.internet_exposure_source}</b>
          {e.context.service_exposure ? <> (strongest service exposure: {e.context.service_exposure})</> : null}.
        </p>
      ) : (
        <p>This finding is not linked to an asset, so asset criticality and exposure were not available and the neutral value was used for each.</p>
      )}
    </section>
  );
}

function Priority({ e }: { e: RiskExplanation }) {
  const p = e.priority;
  return (
    <section className="rsx-block" aria-label="Response priority">
      <h4>Response priority</h4>
      {p.priority === null ? (
        <p>{sentence(p.reason)}</p>
      ) : (
        <>
          <p>
            <b>{p.priority} {p.label}</b>. {sentence(p.reason)} Priority is the order to respond in; it is
            separate from severity and from the score.
          </p>
          <ul className="rsx-rules">
            {p.rules.map((r) => (
              <li key={r.id} data-decisive={r.decisive || undefined} data-matched={r.matched || undefined}>
                {r.decisive ? <Check size={13} aria-hidden /> : <Minus size={13} aria-hidden />}
                <span className="rsx-rule-p">{r.priority}</span>
                <span>{r.condition}</span>
                <span className="rsx-rule-state">
                  {r.decisive ? "Decided this" : r.matched ? "Also true, but an earlier rule decided" : "Does not apply"}
                </span>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}

const STYLES = `
.rsx { display: grid; gap: 14px; color: var(--text-primary); }
.rsx-lead, .rsx p { margin: 0; color: var(--text-secondary); font: 400 12.5px/1.6 var(--font-ui); max-width: 78ch; }
.rsx-steps { margin: 0; padding: 0; list-style: none; display: grid; gap: 16px; }
.rsx-steps h4, .rsx-block h4 { margin: 0 0 8px; font: 650 13px/1.3 var(--font-ui); color: var(--text-primary); display: flex; align-items: center; gap: 8px; }
.rsx-steps h4 span { display: inline-grid; place-items: center; width: 20px; height: 20px; border-radius: 50%; background: var(--accent-ghost); color: var(--accent); font: 700 11px/1 var(--font-mono); }
.rsx-dims { display: grid; gap: 8px; }
.rsx-dim { border: var(--hairline) solid var(--border-subtle); border-radius: 9px; background: var(--bg-app); }
.rsx-dim > summary { display: grid; grid-template-columns: minmax(120px, 1.2fr) minmax(90px, .9fr) minmax(80px, 1fr) 40px 64px; align-items: center; gap: 12px; padding: 10px 12px; cursor: pointer; list-style: none; min-height: 44px; }
.rsx-dim > summary::-webkit-details-marker { display: none; }
.rsx-dim > summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 9px; }
.rsx-dim-name { font: 650 12.5px/1.3 var(--font-ui); }
.rsx-dim-weight { color: var(--text-muted); font: 500 11px/1.3 var(--font-ui); }
.rsx-bar { display: block; height: 7px; border-radius: 4px; background: var(--border-subtle); overflow: hidden; }
.rsx-bar i { display: block; height: 100%; background: var(--accent); }
.rsx-dim-val { font: 600 11.5px/1 var(--font-mono); color: var(--text-secondary); text-align: right; font-variant-numeric: tabular-nums; }
.rsx-dim-pts { font: 700 12.5px/1 var(--font-mono); text-align: right; font-variant-numeric: tabular-nums; }
.rsx-dim table { width: calc(100% - 24px); margin: 0 12px 12px; border-collapse: collapse; font: 400 11.5px/1.45 var(--font-ui); }
.rsx-dim th, .rsx-dim td { padding: 7px 8px; border-top: var(--hairline) solid var(--border-subtle); text-align: left; vertical-align: top; }
.rsx-dim thead th { color: var(--text-muted); font: 650 10px/1.2 var(--font-ui); text-transform: uppercase; letter-spacing: .04em; border-top: 0; }
.rsx-dim tbody th { font-weight: 600; color: var(--text-primary); }
.rsx-dim tbody th small { display: block; margin-top: 2px; color: var(--text-muted); font: 400 10.5px/1.4 var(--font-ui); }
.rsx-num { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
.rsx-src { display: inline-block; padding: 2px 7px; border: var(--hairline) solid var(--border-default); border-radius: 999px; font: 650 10px/1.3 var(--font-ui); color: var(--text-secondary); }
.rsx-src[data-source="default"] { color: var(--sev-medium-color); border-color: var(--sev-medium-color); }
.rsx-defaults { display: flex; gap: 8px; align-items: flex-start; margin-top: 10px !important; padding: 9px 11px; border: var(--hairline) solid var(--sev-medium-color); border-radius: 8px; background: var(--bg-surface); }
.rsx-defaults svg { flex: 0 0 auto; margin-top: 3px; color: var(--sev-medium-color); }
.rsx-sum { font: 500 13px/1.6 var(--font-mono) !important; color: var(--text-primary) !important; }
.rsx-final { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-top: 8px !important; padding: 10px 12px; border-radius: 9px; background: var(--bg-surface); }
.rsx-final code { font: 500 12px/1.4 var(--font-mono); color: var(--text-secondary); }
.rsx-final strong { font: 750 24px/1 var(--font-mono); font-variant-numeric: tabular-nums; }
.rsx-block { padding-top: 12px; border-top: var(--hairline) solid var(--border-subtle); display: grid; gap: 6px; }
.rsx-rules { margin: 6px 0 0; padding: 0; list-style: none; display: grid; gap: 4px; }
.rsx-rules li { display: grid; grid-template-columns: 14px 26px minmax(0, 1fr) auto; gap: 8px; align-items: baseline; padding: 6px 8px; border-radius: 7px; font: 400 11.5px/1.45 var(--font-ui); color: var(--text-muted); }
.rsx-rules li[data-matched] { color: var(--text-secondary); }
.rsx-rules li[data-decisive] { background: var(--accent-ghost); color: var(--text-primary); font-weight: 600; }
.rsx-rule-p { font: 700 10.5px/1.4 var(--font-mono); }
.rsx-rule-state { font: 500 10.5px/1.4 var(--font-ui); color: var(--text-muted); white-space: nowrap; }
.rsx-stored { padding: 8px 10px; border-radius: 8px; background: var(--bg-surface); font-size: 11.5px !important; }
.rsx-stored:not([data-sync]) { border: var(--hairline) solid var(--sev-medium-color); }
.rsx-version { font: 500 10px/1.4 var(--font-mono) !important; color: var(--text-muted) !important; }
.rsx-status { display: flex; gap: 8px; align-items: center; margin: 0; color: var(--text-muted); font: 400 12.5px/1.5 var(--font-ui); }
.rsx-status button { border: var(--hairline) solid var(--border-default); border-radius: 7px; padding: 4px 10px; background: transparent; color: var(--accent); cursor: pointer; font: 600 11.5px/1.2 var(--font-ui); }
.rsx-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
@media (max-width: 720px) {
  .rsx-dim > summary { grid-template-columns: 1fr auto; row-gap: 6px; }
  .rsx-dim-weight, .rsx-dim-val { display: none; }
  .rsx-bar { grid-column: 1 / -1; order: 3; }
  .rsx-dim table, .rsx-dim thead, .rsx-dim tbody, .rsx-dim tr, .rsx-dim th, .rsx-dim td { display: block; }
  .rsx-dim thead { display: none; }
  .rsx-dim tr { padding: 6px 0; border-top: var(--hairline) solid var(--border-subtle); }
  .rsx-dim th, .rsx-dim td { border: 0; padding: 2px 8px; }
  .rsx-rules li { grid-template-columns: 14px 26px minmax(0, 1fr); }
  .rsx-rule-state { grid-column: 3; white-space: normal; }
}
@media (pointer: coarse) { .rsx-status button { min-height: 44px; } }
`;
