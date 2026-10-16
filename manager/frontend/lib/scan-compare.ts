/**
 * Two-scan comparison: types and wording. The server decides what is new, fixed,
 * changed and unchanged (GET /findings/compare); this file only shapes and words it.
 */

export type CompareTab = "new" | "fixed" | "changed" | "unchanged";
export type CompareExportFormat = "csv" | "json";

export interface CompareScanRef {
  reference: string | null; useCaseId: string | null; intensity: string | null;
  scannedAt: string | null; jobId: string | null; runId: string | null;
}

/** A finding as one scan saw it. */
export interface CompareSnapshot {
  severity: string | null; riskScore: number | null; status: string | null;
}

export interface CompareChange<F> {
  finding: F;
  before: CompareSnapshot;
  after: CompareSnapshot;
  severityChanged: boolean;
  statusChanged: boolean;
  riskDelta: number | null;
}

export interface CompareSummary {
  total: number;
  bySeverity: Record<string, number>;
  averageRisk: number | null;
  /** False when a severity had to come from today's finding (a scan that predates snapshots). */
  fromSnapshot: boolean;
}

export interface CompareResult<F extends { id: string }> {
  a: CompareScanRef | null;
  b: CompareScanRef | null;
  counts: { new: number; fixed: number; stillPresent: number; changed: number };
  summaryA: CompareSummary | null;
  summaryB: CompareSummary | null;
  new: F[];
  fixed: F[];
  stillPresent: F[];
  changed: CompareChange<F>[];
}

export const COMPARE_TABS: readonly { key: CompareTab; label: string; hint: string }[] = [
  { key: "new", label: "New", hint: "In the target scan, not in the baseline" },
  { key: "fixed", label: "Fixed", hint: "In the baseline, gone from the target" },
  { key: "changed", label: "Changed", hint: "In both, but severity, risk score or status moved" },
  { key: "unchanged", label: "Unchanged", hint: "In both, nothing moved" },
];

export interface CompareTabCounts { new: number; fixed: number; changed: number; unchanged: number }

/** `unchanged` is what is still present minus what changed. */
export function tabCounts(result: Pick<CompareResult<{ id: string }>, "counts">): CompareTabCounts {
  const { new: added, fixed, stillPresent, changed } = result.counts;
  return { new: added, fixed, changed, unchanged: Math.max(0, stillPresent - changed) };
}

/** Open on the worst news first: something new, else something that moved, else a fix. */
export function defaultTab(counts: CompareTabCounts): CompareTab {
  if (counts.new > 0) return "new";
  if (counts.changed > 0) return "changed";
  if (counts.fixed > 0) return "fixed";
  return "unchanged";
}

/** Findings still present whose state did not move. */
export function unchangedFindings<F extends { id: string }>(result: CompareResult<F>): F[] {
  const moved = new Set(result.changed.map((c) => c.finding.id));
  return result.stillPresent.filter((f) => !moved.has(f.id));
}

/** "+120", "−40", "±0", or an em dash when either side has no score. */
export function formatDelta(delta: number | null | undefined): string {
  if (delta === null || delta === undefined) return "—";
  if (delta === 0) return "±0";
  const rounded = Math.round(delta * 10) / 10;
  return `${rounded > 0 ? "+" : "−"}${Math.abs(rounded)}`;
}

/** One sentence that says what the comparison found. */
export function compareHeadline(
  counts: CompareTabCounts, a: CompareScanRef | null, b: CompareScanRef | null,
): string {
  const from = a?.reference ?? "the baseline";
  const to = b?.reference ?? "the target";
  if (counts.new + counts.fixed + counts.changed === 0) {
    return `Nothing moved between ${from} and ${to}: the same findings, in the same state.`;
  }
  const parts = [
    counts.new ? `${counts.new} new` : null,
    counts.fixed ? `${counts.fixed} fixed` : null,
    counts.changed ? `${counts.changed} changed` : null,
  ].filter(Boolean);
  return `${parts.join(", ")} between ${from} and ${to}.`;
}

/** Net movement in the number of findings the scans saw. */
export function netChange(a: CompareSummary | null, b: CompareSummary | null): number | null {
  return a && b ? b.total - a.total : null;
}

/** True when the "baseline" ran after the "target": almost always a mix-up. */
export function baselineIsNewer(a: CompareScanRef | null, b: CompareScanRef | null): boolean {
  if (!a?.scannedAt || !b?.scannedAt) return false;
  return new Date(a.scannedAt).getTime() > new Date(b.scannedAt).getTime();
}

/** A list the server capped: how many exist versus how many arrived. */
export function truncatedBy(total: number, received: number): number {
  return Math.max(0, total - received);
}

export function compareExportHref(
  surface: "manager" | "portal", a: string, b: string, format: CompareExportFormat,
  engagementId?: string | null,
): string {
  const query = new URLSearchParams({ a, b, format });
  if (surface === "manager" && engagementId) query.set("engagement_id", engagementId);
  const base = surface === "portal"
    ? "/api/portal/workspace/findings/compare/export"
    : "/api/findings/compare/export";
  return `${base}?${query.toString()}`;
}

const word = (value: string | null) => (value ? value.replace(/_/g, " ").toLowerCase() : "—");

/** What moved for one changed finding, as short phrases. */
export function snapshotLine(change: CompareChange<unknown>): string[] {
  const out: string[] = [];
  const { before, after } = change;
  if (change.severityChanged) out.push(`Severity ${word(before.severity)} → ${word(after.severity)}`);
  if (change.riskDelta !== null && change.riskDelta !== 0) {
    out.push(`Risk ${before.riskScore} → ${after.riskScore} (${formatDelta(change.riskDelta)})`);
  }
  if (change.statusChanged) out.push(`Status ${word(before.status)} → ${word(after.status)}`);
  return out;
}
