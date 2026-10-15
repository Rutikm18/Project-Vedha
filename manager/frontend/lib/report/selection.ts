/**
 * Finding selection for the report — pure, order-independent set operations.
 *
 * The report page holds the operator's chosen findings as a `Set<string>` of
 * finding ids. These helpers keep that state honest (toggle, bulk by severity)
 * and derive the two facts the surfaces need: a stable cache key for the scoped
 * report-document query, and whether the selection is a strict subset (⇒ send
 * `finding_ids`) rather than the whole engagement (⇒ omit it, full report).
 */
import type { ReportFinding } from "./report-document";
import { severityKey, type SeverityKey } from "./presentation";

/** Stable key for a selection, independent of insertion order — for query caching
 *  and the `finding_ids` param. */
export function selectionKey(ids: Iterable<string>): string {
  return [...new Set(ids)].sort().join(",");
}

/** Add the id when absent, remove it when present. */
export function toggle(selected: ReadonlySet<string>, id: string): Set<string> {
  const next = new Set(selected);
  if (next.has(id)) next.delete(id);
  else next.add(id);
  return next;
}

export function allIds(findings: readonly ReportFinding[]): Set<string> {
  return new Set(findings.map((f) => f.id));
}

export function idsOfSeverity(
  findings: readonly ReportFinding[],
  severity: SeverityKey,
): string[] {
  return findings.filter((f) => severityKey(f.severity) === severity).map((f) => f.id);
}

/** Tri-state of a severity's findings within the selection, for the bulk toggle. */
export function severityState(
  selected: ReadonlySet<string>,
  findings: readonly ReportFinding[],
  severity: SeverityKey,
): "none" | "some" | "all" {
  const ids = idsOfSeverity(findings, severity);
  if (ids.length === 0) return "none";
  const chosen = ids.filter((id) => selected.has(id)).length;
  return chosen === 0 ? "none" : chosen === ids.length ? "all" : "some";
}

/** Add or remove every finding of one severity. */
export function setSeverity(
  selected: ReadonlySet<string>,
  findings: readonly ReportFinding[],
  severity: SeverityKey,
  on: boolean,
): Set<string> {
  const next = new Set(selected);
  for (const id of idsOfSeverity(findings, severity)) {
    if (on) next.add(id);
    else next.delete(id);
  }
  return next;
}

/** A non-empty selection that is smaller than the whole engagement. Only then is
 *  the report scoped; all-selected reports as the full engagement (param omitted),
 *  and an empty selection builds nothing. */
export function isStrictSubset(selected: ReadonlySet<string>, total: number): boolean {
  return selected.size > 0 && total > 0 && selected.size < total;
}
