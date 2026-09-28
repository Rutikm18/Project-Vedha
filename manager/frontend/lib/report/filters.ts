/**
 * filters.ts — the Reports page's finding filters.
 *
 * Same vocabulary and query format as the Findings page (UI enum casing,
 * converted to the backend's by findings-query.ts), so "status = Risk accepted,
 * host 10.0.0." means the same findings on both pages — and in the report's
 * PDF, Word, Excel and CSV exports.
 *
 * A filtered report must SAY it is filtered: describeReportFilters() is printed
 * in the document, so a reader of "the report" can never mistake a subset for
 * the whole engagement.
 */
import { SEV_PALETTE, toFindingStatus, type FindingStatus, type Severity } from "../severity";

export interface ReportFilters {
  search: string;
  severity: Severity | "ALL";
  status: FindingStatus | "ALL";
  ip: string;
  /** SCN reference or scan-job id; "" = all scans. */
  scan: string;
  exploited: boolean;
  slaBreached: boolean;
}

export const DEFAULT_REPORT_FILTERS: ReportFilters = {
  search: "", severity: "ALL", status: "ALL", ip: "", scan: "", exploited: false, slaBreached: false,
};

export const REPORT_STATUSES: FindingStatus[] = ["OPEN", "CONFIRMED", "REMEDIATED", "ACCEPTED", "FALSE_POSITIVE"];

/**
 * How a finding's lifecycle state reads in a client deliverable. The console's
 * STATUS_LABEL ("REMEDIATED", "FALSE POS.") is operator shorthand; a report
 * reader wants to know "is this still a problem?" first.
 */
export const REPORT_STATUS: Record<FindingStatus, { label: string; tone: string; closed: boolean }> = {
  OPEN:           { label: "Open",                    tone: SEV_PALETTE.RED,    closed: false },
  CONFIRMED:      { label: "Open · confirmed",        tone: SEV_PALETTE.ORANGE, closed: false },
  REMEDIATED:     { label: "Closed · fixed",          tone: SEV_PALETTE.GREEN,  closed: true },
  ACCEPTED:       { label: "Risk accepted",           tone: SEV_PALETTE.AMBER,  closed: false },
  FALSE_POSITIVE: { label: "Closed · false positive", tone: SEV_PALETTE.SLATE,  closed: true },
};

export function reportStatus(raw: string | null | undefined) {
  const s = toFindingStatus(raw);
  return { key: s, ...REPORT_STATUS[s] };
}

export function isReportFiltered(f: ReportFilters): boolean {
  return Boolean(
    f.search.trim() || f.severity !== "ALL" || f.status !== "ALL" || f.ip.trim() || f.scan ||
    f.exploited || f.slaBreached,
  );
}

/** Findings-page style query (UI casing). Empty string when unfiltered. */
export function reportFilterQuery(f: ReportFilters): string {
  const q = new URLSearchParams();
  if (f.search.trim()) q.set("search", f.search.trim());
  if (f.severity !== "ALL") q.set("severity", f.severity);
  if (f.status !== "ALL") q.set("status", f.status);
  if (f.ip.trim()) q.set("asset_ip", f.ip.trim());
  if (f.scan) q.set("scan", f.scan);
  if (f.exploited) q.set("exploit_validated", "true");
  if (f.slaBreached) q.set("sla_breached", "true");
  return q.toString();
}

/** Human-readable filter summary, printed at the top of a filtered report. */
export function describeReportFilters(f: ReportFilters, scanLabel?: (value: string) => string): string[] {
  const out: string[] = [];
  if (f.status !== "ALL") out.push(`Status: ${REPORT_STATUS[f.status].label}`);
  if (f.severity !== "ALL") out.push(`Severity: ${f.severity.charAt(0)}${f.severity.slice(1).toLowerCase()}`);
  if (f.ip.trim()) out.push(`Host: ${f.ip.trim()}`);
  if (f.scan) out.push(`Scan: ${scanLabel ? scanLabel(f.scan) : f.scan}`);
  if (f.search.trim()) out.push(`Search: “${f.search.trim()}”`);
  if (f.exploited) out.push("Exploit confirmed only");
  if (f.slaBreached) out.push("Past target date only");
  return out;
}
