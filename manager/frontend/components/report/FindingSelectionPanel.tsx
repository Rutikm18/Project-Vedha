"use client";

import { useMemo, useState } from "react";
import { ChevronDown, ListChecks, Minus, Server } from "lucide-react";

import type { ReportFinding } from "../../lib/report/report-document";
import {
  assetLabel,
  isOpenStatus,
  orderFindings,
  SEVERITIES,
  SEVERITY_LABEL,
  severityKey,
  statusLabel,
  type SeverityKey,
} from "../../lib/report/presentation";
import {
  idsOfSeverity,
  selectionKey,
  setSeverity,
  severityState,
  toggle,
} from "../../lib/report/selection";

/**
 * Operator chrome (never printed): choose which findings the report, its exports
 * and the AI draft cover. State lives in the page; this panel only edits the set.
 */
export function FindingSelectionPanel({
  findings,
  refs,
  selected,
  onChange,
}: {
  findings: readonly ReportFinding[];
  refs: Map<string, string>;
  selected: ReadonlySet<string>;
  onChange: (next: Set<string>) => void;
}) {
  const [open, setOpen] = useState(false);
  const ordered = useMemo(() => orderFindings(findings), [findings]);
  const total = ordered.length;
  const count = ordered.filter((f) => selected.has(f.id)).length;

  const selectAll = () => onChange(new Set(ordered.map((f) => f.id)));
  const clear = () => onChange(new Set());

  return (
    <section className="fsel no-print" aria-labelledby="fsel-heading">
      <div className="fsel-head">
        <button
          type="button"
          className="fsel-toggle"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          <ListChecks size={15} aria-hidden />
          <strong id="fsel-heading">Findings in report</strong>
          <ChevronDown size={14} aria-hidden className="fsel-chevron" data-open={open} />
        </button>

        <span className="fsel-count" aria-live="polite">
          <strong>{count}</strong> of {total} selected
        </span>

        <div className="fsel-actions">
          <button type="button" className="btn btn-ghost btn-xs" onClick={selectAll} disabled={count === total}>
            Select all
          </button>
          <button type="button" className="btn btn-ghost btn-xs" onClick={clear} disabled={count === 0}>
            Clear
          </button>
        </div>
      </div>

      <div className="fsel-sev-chips" role="group" aria-label="Select findings by severity">
        {SEVERITIES.map((severity) => {
          const sevIds = idsOfSeverity(ordered, severity);
          if (sevIds.length === 0) return null;
          const state = severityState(selected, ordered, severity);
          return (
            <button
              key={severity}
              type="button"
              className="fsel-chip"
              data-severity={severity}
              data-state={state}
              aria-pressed={state === "all"}
              onClick={() => onChange(setSeverity(selected, ordered, severity, state !== "all"))}
            >
              <span className="fsel-chip-box" aria-hidden>
                {state === "all" ? "✓" : state === "some" ? <Minus size={10} /> : ""}
              </span>
              {SEVERITY_LABEL[severity]}
              <span className="fsel-chip-n">{sevIds.filter((id) => selected.has(id)).length}/{sevIds.length}</span>
            </button>
          );
        })}
      </div>

      {open && (
        <ul className="fsel-list">
          {ordered.map((finding) => {
            const sev = severityKey(finding.severity) as SeverityKey;
            const checked = selected.has(finding.id);
            return (
              <li key={finding.id} className="fsel-row" data-selected={checked}>
                <label>
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => onChange(toggle(selected, finding.id))}
                  />
                  <span className="fsel-row-ref">{refs.get(finding.id) ?? "—"}</span>
                  <span className="fsel-row-sev" data-severity={sev}>{SEVERITY_LABEL[sev]}</span>
                  <span className="fsel-row-title">{finding.title}</span>
                  {assetLabel(finding) && (
                    <span className="fsel-row-asset"><Server size={11} aria-hidden /> {assetLabel(finding)}</span>
                  )}
                  <span className="fsel-row-status" data-open={isOpenStatus(finding.status)}>
                    {statusLabel(finding.status)}
                  </span>
                </label>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}

/** Re-exported so callers can key a scoped query without importing the lib twice. */
export { selectionKey };
