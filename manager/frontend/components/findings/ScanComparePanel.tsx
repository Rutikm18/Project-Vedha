"use client";

/**
 * Compare two scans. Pick a baseline and a target; the server says what is new, fixed,
 * changed and unchanged, and what each scan saw in total. Nothing is pre-selected: the
 * operator chooses both scans. Works for operators and for customers (the portal
 * transport is pinned to the customer's own engagement server-side).
 */
import { useMemo, useState, type ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, ArrowLeftRight, Download, GitCompare, Printer } from "lucide-react";
import type { ScanOption } from "../../lib/adapters";
import { errorMessage, isUnauthorized } from "../../lib/fetcher";
import { SEV_COLOR } from "../../lib/severity";
import {
  COMPARE_TABS, baselineIsNewer, compareExportHref, compareHeadline, defaultTab,
  netChange, snapshotLine, tabCounts, truncatedBy, unchangedFindings,
  type CompareChange, type CompareResult, type CompareScanRef, type CompareSummary, type CompareTab,
} from "../../lib/scan-compare";
import { SkeletonRows } from "../states/DataState";

const SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"] as const;
const PAGE = 50;

export interface CompareApi {
  compare: <T>(query: string) => Promise<T>;
}

export function ScanComparePanel<F extends { id: string }>({
  surface, scans, scansLoading, engagementId, api, renderFinding,
}: {
  surface: "manager" | "portal";
  scans: ScanOption[];
  scansLoading: boolean;
  engagementId: string | null;
  api: CompareApi;
  renderFinding: (finding: F) => ReactNode;
}) {
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [picked, setPicked] = useState<CompareTab | null>(null);
  const ready = Boolean(a) && Boolean(b) && a !== b;

  const query = useQuery({
    queryKey: ["finding-compare", surface, engagementId, a, b],
    queryFn: () => api.compare<CompareResult<F>>(new URLSearchParams({ a, b }).toString()),
    enabled: ready,
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });

  const value = (s: ScanOption) => s.reference ?? s.jobId;
  const label = (s: ScanOption) => {
    const when = s.scannedAt ? new Date(s.scannedAt).toLocaleDateString() : "";
    const bits = [s.reference ?? s.jobId.slice(0, 8), s.intensity, when].filter(Boolean);
    return `${bits.join(" · ")} — ${s.findings} finding${s.findings === 1 ? "" : "s"}`;
  };
  const swap = () => { setA(b); setB(a); setPicked(null); };

  return (
    <section className="scx" aria-label="Compare two scans">
      <style>{STYLES}</style>

      <header className="scx-head">
        <div>
          <h3><GitCompare size={15} aria-hidden /> Compare two scans</h3>
          <p>Choose a baseline and a target. You see what is new, what was fixed, and what changed in between.</p>
        </div>
        {ready && query.data && (
          <div className="scx-actions" data-print-hide>
            <a className="scx-btn" href={compareExportHref(surface, a, b, "csv", engagementId)} download>
              <Download size={13} aria-hidden /> CSV
            </a>
            <a className="scx-btn" href={compareExportHref(surface, a, b, "json", engagementId)} download>
              <Download size={13} aria-hidden /> JSON
            </a>
            <button type="button" className="scx-btn" onClick={printComparison}>
              <Printer size={13} aria-hidden /> Print / PDF
            </button>
          </div>
        )}
      </header>

      <div className="scx-pick" data-print-hide>
        <ScanSelect
          name="Baseline (earlier scan)" value={a} onChange={(v) => { setA(v); setPicked(null); }}
          scans={scans} loading={scansLoading} taken={b} valueOf={value} labelOf={label}
        />
        <button type="button" className="scx-swap" onClick={swap} disabled={!a && !b}
          aria-label="Swap baseline and target" title="Swap baseline and target">
          <ArrowLeftRight size={14} aria-hidden />
        </button>
        <ScanSelect
          name="Target (later scan)" value={b} onChange={(v) => { setB(v); setPicked(null); }}
          scans={scans} loading={scansLoading} taken={a} valueOf={value} labelOf={label}
        />
      </div>

      {!scansLoading && scans.length < 2 && (
        <p className="scx-hint">Comparing needs at least two scans. Run another scan, then come back.</p>
      )}
      {scans.length >= 2 && !ready && (
        <p className="scx-hint">
          {a && b && a === b
            ? "Pick two different scans to compare."
            : "Pick a baseline and a target scan to see the differences."}
        </p>
      )}
      {ready && query.isLoading && <SkeletonRows rows={3} height={72} />}
      {ready && query.error && (
        <p className="scx-hint" role="alert"><AlertTriangle size={13} aria-hidden /> {errorMessage(query.error)}</p>
      )}
      {ready && query.data && (
        <Result
          result={query.data} tab={picked} onTab={setPicked} renderFinding={renderFinding}
        />
      )}
    </section>
  );
}

function ScanSelect({ name, value, onChange, scans, loading, taken, valueOf, labelOf }: {
  name: string; value: string; onChange: (value: string) => void; scans: ScanOption[];
  loading: boolean; taken: string; valueOf: (s: ScanOption) => string; labelOf: (s: ScanOption) => string;
}) {
  return (
    <label className="scx-select">
      <span>{name}</span>
      <select value={value} onChange={(e) => onChange(e.target.value)} disabled={loading}>
        <option value="">Select a scan…</option>
        {scans.map((s) => (
          <option key={s.jobId} value={valueOf(s)} disabled={valueOf(s) === taken}>{labelOf(s)}</option>
        ))}
      </select>
    </label>
  );
}

function Result<F extends { id: string }>({ result, tab, onTab, renderFinding }: {
  result: CompareResult<F>; tab: CompareTab | null; onTab: (tab: CompareTab) => void;
  renderFinding: (finding: F) => ReactNode;
}) {
  const counts = tabCounts(result);
  const active = tab ?? defaultTab(counts);
  const net = netChange(result.summaryA, result.summaryB);
  const unchanged = useMemo(() => unchangedFindings(result), [result]);
  const newer = baselineIsNewer(result.a, result.b);

  return (
    <div className="scx-result">
      <h4 className="scx-print-title">
        Scan comparison: {result.a?.reference ?? "baseline"} → {result.b?.reference ?? "target"}
      </h4>
      <p className="scx-headline" aria-live="polite">
        {compareHeadline(counts, result.a, result.b)}
        {net !== null && net !== 0 && (
          <> The target saw <b>{Math.abs(net)} {net < 0 ? "fewer" : "more"}</b> finding{Math.abs(net) === 1 ? "" : "s"} in total.</>
        )}
      </p>
      {newer && (
        <p className="scx-note" role="note">
          <AlertTriangle size={13} aria-hidden /> The baseline ran after the target, so “new” and
          “fixed” read the wrong way round. Use the swap button to correct it.
        </p>
      )}

      <div className="scx-sides">
        <ScanCard title="Baseline" scan={result.a} summary={result.summaryA} />
        <ScanCard title="Target" scan={result.b} summary={result.summaryB} />
      </div>
      {(result.summaryA?.fromSnapshot === false || result.summaryB?.fromSnapshot === false) && (
        <p className="scx-note" role="note">
          One of these scans ran before per-scan snapshots were recorded, so its severity totals and
          “changed” comparison use each finding as it is today rather than as that scan saw it.
        </p>
      )}

      <div className="scx-tabs" role="tablist" aria-label="Comparison buckets">
        {COMPARE_TABS.map((t) => (
          <button
            key={t.key} type="button" role="tab" id={`scx-tab-${t.key}`}
            aria-selected={active === t.key} aria-controls="scx-panel" title={t.hint}
            data-kind={t.key} onClick={() => onTab(t.key)}
          >
            {t.label} <b>{counts[t.key]}</b>
          </button>
        ))}
      </div>

      <div id="scx-panel" role="tabpanel" aria-labelledby={`scx-tab-${active}`} className="scx-panel">
        <p className="scx-tab-hint">{COMPARE_TABS.find((t) => t.key === active)?.hint}.</p>
        {active === "changed"
          ? <ChangedList key="changed" items={result.changed} total={counts.changed} renderFinding={renderFinding} />
          : <FindingList
              key={active}
              items={active === "new" ? result.new : active === "fixed" ? result.fixed : unchanged}
              total={counts[active]}
              empty={EMPTY[active]}
              renderFinding={renderFinding}
            />}
      </div>
    </div>
  );
}

const EMPTY: Record<CompareTab, string> = {
  new: "Nothing new appeared in the target scan.",
  fixed: "Nothing from the baseline is gone.",
  changed: "No finding changed severity, risk score or status.",
  unchanged: "Every finding present in both scans changed.",
};

function More({ shown, total, received, onMore }: {
  shown: number; total: number; received: number; onMore: () => void;
}) {
  const hidden = Math.min(total, received) - shown;
  const capped = truncatedBy(total, received);
  return (
    <>
      {hidden > 0 && (
        <button type="button" className="scx-btn scx-more" onClick={onMore} data-print-hide>
          Show {Math.min(PAGE, hidden)} more ({hidden} hidden)
        </button>
      )}
      {capped > 0 && (
        <p className="scx-tab-hint">
          Showing the first {received} of {total}. The CSV and JSON exports contain every row.
        </p>
      )}
    </>
  );
}

function FindingList<F extends { id: string }>({ items, total, empty, renderFinding }: {
  items: F[]; total: number; empty: string; renderFinding: (finding: F) => ReactNode;
}) {
  const [shown, setShown] = useState(PAGE);
  if (items.length === 0) return <p className="scx-empty">{empty}</p>;
  return (
    <>
      {items.slice(0, shown).map((f) => <div key={f.id} className="scx-item">{renderFinding(f)}</div>)}
      <More shown={Math.min(shown, items.length)} total={total} received={items.length}
        onMore={() => setShown((n) => n + PAGE)} />
    </>
  );
}

function ChangedList<F extends { id: string }>({ items, total, renderFinding }: {
  items: CompareChange<F>[]; total: number; renderFinding: (finding: F) => ReactNode;
}) {
  const [shown, setShown] = useState(PAGE);
  if (items.length === 0) return <p className="scx-empty">{EMPTY.changed}</p>;
  return (
    <>
      {items.slice(0, shown).map((c) => (
        <div key={c.finding.id} className="scx-item">
          {renderFinding(c.finding)}
          <ul className="scx-moves" aria-label="What changed">
            {snapshotLine(c).map((m) => <li key={m}>{m}</li>)}
          </ul>
        </div>
      ))}
      <More shown={Math.min(shown, items.length)} total={total} received={items.length}
        onMore={() => setShown((n) => n + PAGE)} />
    </>
  );
}

function ScanCard({ title, scan, summary }: {
  title: string; scan: CompareScanRef | null; summary: CompareSummary | null;
}) {
  const when = scan?.scannedAt ? new Date(scan.scannedAt).toLocaleString() : "Time not recorded";
  const total = summary?.total ?? 0;
  const text = SEVERITIES.map((s) => `${summary?.bySeverity[s] ?? 0} ${s.toLowerCase()}`).join(", ");
  return (
    <article className="scx-card">
      <h5>{title}</h5>
      <strong>{scan?.reference ?? "Scan"}</strong>
      <span className="scx-card-meta">{[when, scan?.intensity].filter(Boolean).join(" · ")}</span>
      <div className="scx-card-total"><b>{total}</b> finding{total === 1 ? "" : "s"}
        {summary?.averageRisk != null && <span> · average risk {Math.round(summary.averageRisk)}</span>}
      </div>
      <div className="scx-bar" role="img" aria-label={`${title}: ${text}`}>
        {total === 0 ? <i data-empty style={{ width: "100%" }} /> : SEVERITIES.map((s) => {
          const n = summary?.bySeverity[s] ?? 0;
          return n > 0 ? <i key={s} style={{ width: `${(n / total) * 100}%`, background: SEV_COLOR[s] }} title={`${n} ${s.toLowerCase()}`} /> : null;
        })}
      </div>
      <ul className="scx-legend">
        {SEVERITIES.map((s) => (
          <li key={s} data-muted={!(summary?.bySeverity[s]) || undefined}>
            <i style={{ background: SEV_COLOR[s] }} aria-hidden />{summary?.bySeverity[s] ?? 0} {s.toLowerCase()}
          </li>
        ))}
      </ul>
    </article>
  );
}

/** Print just the comparison: the stylesheet below hides everything else while this class is set. */
function printComparison() {
  const root = document.documentElement;
  const done = () => { root.classList.remove("scx-printing"); window.removeEventListener("afterprint", done); };
  window.addEventListener("afterprint", done);
  root.classList.add("scx-printing");
  window.print();
}


const STYLES = `
.scx { display: flex; flex-direction: column; gap: 14px; margin-bottom: var(--space-4); padding: 16px; border: var(--hairline) solid var(--border-subtle); border-radius: 12px; background: var(--bg-surface); }
.scx-head { display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: space-between; gap: 10px 16px; }
.scx-head h3 { display: flex; align-items: center; gap: 7px; margin: 0; color: var(--text-primary); font: 700 14px/1.3 var(--font-ui); }
.scx-head p { margin: 3px 0 0; color: var(--text-muted); font: 500 12px/1.5 var(--font-ui); }
.scx-actions { display: flex; flex-wrap: wrap; gap: 6px; }
.scx-btn { display: inline-flex; align-items: center; gap: 6px; min-height: 30px; padding: 0 11px; border: var(--hairline) solid var(--border-subtle); border-radius: 8px; background: transparent; color: var(--text-secondary); font: 600 12px/1 var(--font-ui); text-decoration: none; cursor: pointer; }
.scx-btn:hover { border-color: var(--border-strong); color: var(--text-primary); }
.scx-pick { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); gap: 10px; align-items: end; }
.scx-select { display: flex; flex-direction: column; gap: 5px; min-width: 0; }
.scx-select > span { color: var(--text-muted); font: 650 10.5px/1.2 var(--font-ui); text-transform: uppercase; letter-spacing: .04em; }
.scx-select select { width: 100%; min-height: 36px; padding: 0 10px; border: var(--hairline) solid var(--border-subtle); border-radius: 8px; background: var(--bg-surface); color: var(--text-primary); font: 500 12.5px/1.2 var(--font-ui); text-overflow: ellipsis; }
.scx-swap { display: grid; place-items: center; width: 36px; height: 36px; border: var(--hairline) solid var(--border-subtle); border-radius: 8px; background: transparent; color: var(--text-secondary); cursor: pointer; }
.scx-swap:disabled { opacity: .4; cursor: default; }
.scx-hint, .scx-empty { display: flex; align-items: center; gap: 6px; margin: 0; color: var(--text-muted); font: 500 12px/1.5 var(--font-ui); }
.scx-result { display: flex; flex-direction: column; gap: 14px; }
.scx-print-title { display: none; margin: 0; font: 700 15px/1.3 var(--font-ui); }
.scx-headline { margin: 0; color: var(--text-primary); font: 600 13.5px/1.5 var(--font-ui); }
.scx-note { display: flex; align-items: flex-start; gap: 7px; margin: 0; padding: 9px 11px; border: var(--hairline) solid var(--sev-medium-color, var(--border-strong)); border-radius: 8px; color: var(--text-secondary); font: 500 12px/1.5 var(--font-ui); }
.scx-note svg { flex: none; margin-top: 2px; }
.scx-sides { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.scx-card { display: flex; flex-direction: column; gap: 5px; min-width: 0; padding: 12px 14px; border: var(--hairline) solid var(--border-subtle); border-radius: 10px; background: var(--bg-base, transparent); }
.scx-card h5 { margin: 0; color: var(--text-muted); font: 650 10.5px/1 var(--font-ui); text-transform: uppercase; letter-spacing: .05em; }
.scx-card strong { color: var(--text-primary); font: 700 13px/1.3 var(--font-mono); overflow-wrap: anywhere; }
.scx-card-meta { color: var(--text-muted); font: 500 11.5px/1.4 var(--font-ui); }
.scx-card-total { color: var(--text-secondary); font: 500 12px/1.4 var(--font-ui); }
.scx-card-total b { color: var(--text-primary); font: 700 18px/1 var(--font-mono); }
.scx-bar { display: flex; height: 8px; overflow: hidden; border-radius: 4px; background: var(--track-bg, var(--border-subtle)); }
.scx-bar i { min-width: 3px; }
.scx-bar i[data-empty] { background: var(--border-subtle); }
.scx-legend { display: flex; flex-wrap: wrap; gap: 4px 12px; margin: 2px 0 0; padding: 0; list-style: none; }
.scx-legend li { display: inline-flex; align-items: center; gap: 5px; color: var(--text-secondary); font: 500 11px/1.3 var(--font-ui); }
.scx-legend li[data-muted] { color: var(--text-faint, var(--text-muted)); }
.scx-legend i { width: 7px; height: 7px; border-radius: 2px; }
.scx-tabs { display: flex; flex-wrap: wrap; gap: 6px; border-bottom: var(--hairline) solid var(--border-subtle); padding-bottom: 8px; }
.scx-tabs button { display: inline-flex; align-items: baseline; gap: 6px; min-height: 32px; padding: 0 12px; border: var(--hairline) solid transparent; border-radius: 8px; background: transparent; color: var(--text-secondary); font: 600 12.5px/1 var(--font-ui); cursor: pointer; }
.scx-tabs button b { font: 700 12.5px/1 var(--font-mono); }
.scx-tabs button[aria-selected="true"] { border-color: var(--border-accent, var(--border-strong)); background: var(--accent-ghost, transparent); color: var(--accent, var(--text-primary)); }
.scx-tabs button[data-kind="new"][aria-selected="true"] { color: var(--sev-high-color, var(--accent)); }
.scx-tabs button[data-kind="fixed"][aria-selected="true"] { color: var(--nominal-color, var(--accent)); }
.scx-panel { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.scx-tab-hint { margin: 0; color: var(--text-muted); font: 500 11.5px/1.4 var(--font-ui); }
.scx-item { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.scx-moves { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 4px; padding: 0 0 0 10px; list-style: none; }
.scx-moves li { padding: 3px 9px; border-radius: 999px; background: var(--accent-ghost, var(--border-subtle)); color: var(--text-secondary); font: 600 11px/1.3 var(--font-ui); }
.scx-more { align-self: flex-start; }
@media (max-width: 720px) {
  .scx { padding: 12px; }
  .scx-pick { grid-template-columns: minmax(0, 1fr); }
  .scx-swap { justify-self: start; width: 44px; height: 44px; }
  .scx-sides { grid-template-columns: minmax(0, 1fr); }
  .scx-select select, .scx-btn, .scx-tabs button { min-height: 44px; }
}
@media print {
  html.scx-printing body * { visibility: hidden; }
  html.scx-printing .scx, html.scx-printing .scx * { visibility: visible; }
  html.scx-printing .scx { position: absolute; inset: 0 auto auto 0; width: 100%; border: 0; }
  html.scx-printing .scx [data-print-hide] { display: none; }
  html.scx-printing .scx-print-title { display: block; }
}
`;
