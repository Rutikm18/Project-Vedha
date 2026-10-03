/**
 * Report presentation layer — one reading of the canonical report document,
 * shared by the web report, PDF, Word and Excel renderers.
 *
 * Rules (the canonical record's, kept here):
 *  - Nothing is invented. Every value is recorded, or a disclosed deterministic
 *    derivation (counts, the highest-open-severity rating, SLA windows).
 *  - Absent stays absent. Helpers return only recorded values; callers list the
 *    missing ones once instead of printing "Not recorded" per field.
 *  - Everything that leaves this module as text has been masked.
 */
import { redact } from "./finding-model";
import type {
  ReportDocument,
  ReportEvidenceArtifact,
  ReportFinding,
} from "./report-document";

// ─── Masking ─────────────────────────────────────────────────────────────────

/** Mask secrets in recorded text. Existing `[REDACTED:…]` placeholders survive
 *  untouched, so text masked upstream is never double-masked into noise. */
export function mask(value: string): string {
  const placeholders: string[] = [];
  const protectedText = value.replace(/\[REDACTED:[^\]]+\]/g, (placeholder) => {
    const token = `__VEDHA_MASK_${placeholders.length}__`;
    placeholders.push(placeholder);
    return token;
  });
  return redact(protectedText).text.replace(
    /__VEDHA_MASK_(\d+)__/g,
    (_match, index: string) => placeholders[Number(index)] ?? "[REDACTED]",
  );
}

/** Masked, trimmed text of a recorded scalar; null when nothing is recorded. */
export function maskedText(value: unknown): string | null {
  if (value === null || value === undefined) return null;
  const text = mask(String(value).replace(/\u0000/g, "")).trim();
  return text ? text : null;
}

// ─── Severity and status ─────────────────────────────────────────────────────

export type SeverityKey = "critical" | "high" | "medium" | "low" | "info";
export const SEVERITIES: readonly SeverityKey[] = ["critical", "high", "medium", "low", "info"];

export const SEVERITY_LABEL: Record<SeverityKey, string> = {
  critical: "Critical", high: "High", medium: "Medium", low: "Low", info: "Informational",
};

/** Print palette (light paper). Matches the console's severity roles. */
export const SEVERITY_HEX: Record<SeverityKey, { fg: string; bg: string; ink: string }> = {
  critical: { fg: "#B91C1C", bg: "#FDECEC", ink: "#FFFFFF" },
  high: { fg: "#C2410C", bg: "#FEF0E6", ink: "#FFFFFF" },
  medium: { fg: "#A16207", bg: "#FEF7E0", ink: "#FFFFFF" },
  low: { fg: "#57534E", bg: "#F3F2F1", ink: "#FFFFFF" },
  info: { fg: "#475569", bg: "#EEF2F6", ink: "#FFFFFF" },
};

export const BRAND_HEX = { ink: "#0F172A", navy: "#12284B", accent: "#1D4ED8", muted: "#64748B", rule: "#D9DEE7", wash: "#F5F7FA", ok: "#0F766E" };

export function severityKey(value: string | null | undefined): SeverityKey {
  const key = String(value ?? "").trim().toLowerCase();
  if (key === "informational" || key === "information") return "info";
  return (SEVERITIES as readonly string[]).includes(key) ? key as SeverityKey : "info";
}

const OPEN_STATUSES = new Set(["open", "confirmed"]);

export function isOpenStatus(status: string | null | undefined): boolean {
  return OPEN_STATUSES.has(String(status ?? "").toLowerCase());
}

const STATUS_TEXT: Record<string, string> = {
  open: "Open",
  confirmed: "Confirmed",
  remediated: "Remediated",
  accepted: "Risk accepted",
  fp: "False positive",
  false_positive: "False positive",
  auto_resolved: "Auto-resolved",
};

export function statusLabel(status: string | null | undefined): string {
  const key = String(status ?? "").toLowerCase();
  return STATUS_TEXT[key] ?? humanize(key);
}

/** "closure_review_metadata_absent" → "Closure review metadata absent". */
export function humanize(value: string | null | undefined): string {
  const text = String(value ?? "").replace(/[_-]+/g, " ").replace(/\s+/g, " ").trim();
  return text ? text.charAt(0).toUpperCase() + text.slice(1) : "";
}

// ─── Ordering and references ─────────────────────────────────────────────────

function numeric(value: unknown): number | null {
  if (value === null || value === undefined || value === "") return null;
  const n = typeof value === "number" ? value : Number(value);
  return Number.isFinite(n) ? n : null;
}

/**
 * One issue found on one or more assets: findings with the same severity and
 * title. Scanners record an issue once per host; a report reads it once, with
 * the list of affected assets.
 */
export interface IssueGroup {
  key: string;
  title: string;
  severity: SeverityKey;
  /** Instances, open first, then by risk, then by asset. */
  findings: ReportFinding[];
  /** The first instance: its record represents the issue where all agree. */
  lead: ReportFinding;
  open: number;
  closed: number;
}

function byInstance(a: ReportFinding, b: ReportFinding): number {
  return Number(isOpenStatus(b.status)) - Number(isOpenStatus(a.status))
    || (numeric(b.risk_score) ?? -1) - (numeric(a.risk_score) ?? -1)
    || (numeric(b.cvss_score) ?? -1) - (numeric(a.cvss_score) ?? -1)
    || (assetLabel(a) ?? "").localeCompare(assetLabel(b) ?? "", "en", { numeric: true })
    || a.id.localeCompare(b.id);
}

/** Issues, most severe first; then those still open, then by highest risk. */
export function issueGroups(findings: readonly ReportFinding[]): IssueGroup[] {
  const groups = new Map<string, ReportFinding[]>();
  for (const f of findings) {
    const key = `${severityKey(f.severity)}|${f.title.trim().toLowerCase()}`;
    const list = groups.get(key);
    if (list) list.push(f);
    else groups.set(key, [f]);
  }
  const maxOf = (list: ReportFinding[], pick: (f: ReportFinding) => unknown) =>
    Math.max(-1, ...list.map((f) => numeric(pick(f)) ?? -1));
  return [...groups.entries()]
    .map(([key, list]) => {
      const sorted = [...list].sort(byInstance);
      const open = sorted.filter((f) => isOpenStatus(f.status)).length;
      return { key, title: sorted[0]!.title, severity: severityKey(sorted[0]!.severity), findings: sorted, lead: sorted[0]!, open, closed: sorted.length - open };
    })
    .sort((a, b) =>
      SEVERITIES.indexOf(a.severity) - SEVERITIES.indexOf(b.severity)
      || Number(b.open > 0) - Number(a.open > 0)
      || maxOf(b.findings, (f) => f.risk_score) - maxOf(a.findings, (f) => f.risk_score)
      || maxOf(b.findings, (f) => f.cvss_score) - maxOf(a.findings, (f) => f.cvss_score)
      || b.findings.length - a.findings.length
      || a.title.localeCompare(b.title),
    );
}

/** Presentation order: issue by issue, so an issue's references are contiguous. */
export function orderFindings(findings: readonly ReportFinding[]): ReportFinding[] {
  return issueGroups(findings).flatMap((g) => g.findings);
}

export function findingRef(index: number): string {
  return `F${String(index + 1).padStart(3, "0")}`;
}

/** Finding id → report reference (F001…), in presentation order. */
export function findingRefs(report: ReportDocument): Map<string, string> {
  return new Map(orderFindings(report.findings).map((f, i) => [f.id, findingRef(i)]));
}

// ─── Overall rating and metrics ──────────────────────────────────────────────

export interface OverallRating {
  level: SeverityKey | "none";
  label: string;
  basis: string;
}

/** Disclosed rule: the highest severity among findings that are still open. */
export function overallRating(report: ReportDocument): OverallRating {
  const open = report.findings.filter((f) => isOpenStatus(f.status));
  if (open.length === 0) {
    return {
      level: "none",
      label: "No open findings",
      basis: report.findings.length
        ? `All ${report.findings.length} recorded finding${report.findings.length === 1 ? " has" : "s have"} a closing disposition.`
        : "No findings are recorded for this engagement.",
    };
  }
  const level = SEVERITIES.find((s) => open.some((f) => severityKey(f.severity) === s)) ?? "info";
  const count = open.filter((f) => severityKey(f.severity) === level).length;
  return {
    level,
    label: SEVERITY_LABEL[level],
    basis: `Highest severity among ${open.length} open finding${open.length === 1 ? "" : "s"}: ${count} ${SEVERITY_LABEL[level].toLowerCase()}.`,
  };
}

export interface SeverityRow { severity: SeverityKey; total: number; open: number; closed: number }

export function severityRows(report: ReportDocument): SeverityRow[] {
  return SEVERITIES.map((severity) => {
    const all = report.findings.filter((f) => severityKey(f.severity) === severity);
    const open = all.filter((f) => isOpenStatus(f.status)).length;
    return { severity, total: all.length, open, closed: all.length - open };
  });
}

export interface StatusRow { status: string; label: string; count: number }

export function statusRows(report: ReportDocument): StatusRow[] {
  const counts = new Map<string, number>();
  for (const f of report.findings) {
    const key = String(f.status).toLowerCase();
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  const order = ["open", "confirmed", "accepted", "remediated", "fp", "false_positive"];
  const rank = (status: string) => (order.includes(status) ? order.indexOf(status) : order.length);
  return [...counts.entries()]
    .sort(([a], [b]) => rank(a) - rank(b) || a.localeCompare(b))
    .map(([status, count]) => ({ status, label: statusLabel(status), count }));
}

export interface KeyMetrics {
  total: number;
  open: number;
  closed: number;
  criticalHighOpen: number;
  exploitableOpen: number;
  slaBreached: number;
  slaAtRisk: number;
  assetsAffected: number;
  retestsPassed: number;
}

export function assetKey(f: ReportFinding): string | null {
  return f.asset?.id ?? f.asset?.ip_address ?? f.asset?.hostname ?? null;
}

export function keyMetrics(report: ReportDocument): KeyMetrics {
  const open = report.findings.filter((f) => isOpenStatus(f.status));
  return {
    total: report.findings.length,
    open: open.length,
    closed: report.findings.length - open.length,
    criticalHighOpen: open.filter((f) => ["critical", "high"].includes(severityKey(f.severity))).length,
    exploitableOpen: open.filter((f) => f.exploitable || f.exploit_validated).length,
    slaBreached: open.filter((f) => f.current_sla.state === "breached").length,
    slaAtRisk: open.filter((f) => f.current_sla.state === "at_risk").length,
    assetsAffected: new Set(open.map(assetKey).filter(Boolean)).size,
    retestsPassed: report.findings.filter((f) => f.closure.retest?.passed === true).length,
  };
}

// ─── Assets ──────────────────────────────────────────────────────────────────

/** "web01.example.com (192.0.2.10)" — whatever is recorded, masked. */
export function assetLabel(f: ReportFinding): string | null {
  const a = f.asset;
  if (!a) return null;
  const name = maskedText(a.fqdn) ?? maskedText(a.hostname);
  const ip = maskedText(a.ip_address);
  if (name && ip && name !== ip) return `${name} (${ip})`;
  return name ?? ip;
}

// ─── Dates ───────────────────────────────────────────────────────────────────

export function usableTimeZone(value: string | null | undefined): string {
  const zone = value || "UTC";
  try {
    new Intl.DateTimeFormat("en-GB", { timeZone: zone }).format(new Date(0));
    return zone;
  } catch {
    return "UTC";
  }
}

function parsed(value: string | null | undefined): Date | null {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** Calendar parts of an instant in a zone (fixed month names: ICU versions
 *  disagree on "Sep" vs "Sept"). */
function zoned(date: Date, timeZone: string): { day: string; month: string; year: string; hour: string; minute: string; zone: string } {
  const parts = Object.fromEntries(new Intl.DateTimeFormat("en-GB", {
    day: "2-digit", month: "numeric", year: "numeric", hour: "2-digit", minute: "2-digit",
    hourCycle: "h23", timeZone, timeZoneName: "short",
  }).formatToParts(date).map((p) => [p.type, p.value]));
  return {
    day: parts.day ?? "",
    month: MONTHS[Number(parts.month) - 1] ?? "",
    year: parts.year ?? "",
    hour: parts.hour ?? "",
    minute: parts.minute ?? "",
    zone: parts.timeZoneName ?? timeZone,
  };
}

/** "26 Sep 2026". Date-only values are read as calendar dates. */
export function formatDate(value: string | null | undefined, timeZone = "UTC"): string | null {
  if (!value) return null;
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    const [y, m, d] = value.split("-");
    return `${d} ${MONTHS[Number(m) - 1]} ${y}`;
  }
  const date = parsed(value);
  if (!date) return value;
  const z = zoned(date, timeZone);
  return `${z.day} ${z.month} ${z.year}`;
}

/** "26 Sep 2026, 14:00 IST". */
export function formatDateTime(value: string | null | undefined, timeZone = "UTC"): string | null {
  if (!value) return null;
  const date = parsed(value);
  if (!date || /^\d{4}-\d{2}-\d{2}$/.test(value)) return formatDate(value, timeZone);
  const z = zoned(date, timeZone);
  return `${z.day} ${z.month} ${z.year}, ${z.hour}:${z.minute} ${z.zone}`;
}

/** "72 hours" → "3 days" when it divides evenly. */
export function formatHours(hours: number | null | undefined): string | null {
  if (hours === null || hours === undefined || !Number.isFinite(hours)) return null;
  if (hours >= 48 && hours % 24 === 0) return `${hours / 24} days`;
  return `${Math.round(hours)} hour${Math.round(hours) === 1 ? "" : "s"}`;
}

// ─── Recorded values, readable ───────────────────────────────────────────────

export type Readable =
  | { kind: "text"; paragraphs: string[] }
  | { kind: "list"; items: string[] }
  | { kind: "pairs"; rows: Array<[string, string]> };

function inline(value: unknown): string {
  if (value === null || value === undefined) return "";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  if (Array.isArray(value)) return value.map(inline).filter(Boolean).join(", ");
  if (typeof value === "object") {
    return Object.entries(value as Record<string, unknown>)
      .filter(([key, item]) => key.toLowerCase() !== "raw" && item !== null && item !== undefined && item !== "")
      .map(([key, item]) => `${humanize(key)}: ${inline(item)}`)
      .join("; ");
  }
  return String(value);
}

/** A recorded value as prose, a list or label/value rows — never raw JSON. */
export function readable(value: unknown): Readable | null {
  if (value === null || value === undefined || value === "") return null;
  if (typeof value === "string") {
    const text = mask(value).trim();
    if (!text) return null;
    return { kind: "text", paragraphs: text.split(/\n{2,}/).map((p) => p.trim()).filter(Boolean) };
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return { kind: "text", paragraphs: [String(value)] };
  }
  if (Array.isArray(value)) {
    const items = value.map((item) => mask(inline(item)).trim()).filter(Boolean);
    return items.length ? { kind: "list", items } : null;
  }
  if (typeof value === "object") {
    const rows = Object.entries(value as Record<string, unknown>)
      .filter(([key, item]) => key.toLowerCase() !== "raw" && item !== null && item !== undefined && item !== "")
      .map(([key, item]) => [humanize(key), mask(inline(item)).trim()] as [string, string])
      .filter(([, item]) => item);
    return rows.length ? { kind: "pairs", rows } : null;
  }
  return null;
}

/** Plain-text rendering of `readable` for flat outputs (cells, single lines). */
export function readableText(value: unknown, separator = "\n"): string | null {
  const r = readable(value);
  if (!r) return null;
  if (r.kind === "text") return r.paragraphs.join(separator);
  if (r.kind === "list") return r.items.map((item) => `• ${item}`).join(separator);
  return r.rows.map(([k, v]) => `${k}: ${v}`).join(separator);
}

// ─── Per-finding presentation ────────────────────────────────────────────────

export interface Fact { label: string; value: string }

function percent(value: unknown): string | null {
  const n = numeric(value);
  if (n === null) return null;
  const p = n <= 1 ? n * 100 : n;
  return `${p < 1 ? p.toFixed(2) : p.toFixed(1)}%`;
}

/** Key facts for the finding header. Only recorded values. */
export function findingFacts(f: ReportFinding, timeZone = "UTC"): Fact[] {
  const facts: Array<Fact | null> = [];
  const add = (label: string, value: string | null | undefined) => {
    if (value) facts.push({ label, value });
  };
  const cvss = numeric(f.cvss_score);
  add("CVSS", cvss !== null ? cvss.toFixed(1) : null);
  add("CVSS vector", maskedText(f.cvss_vector));
  add("EPSS", percent(f.epss_score));
  const risk = numeric(f.risk_score);
  add("Risk score", risk !== null ? String(Math.round(risk * 10) / 10) : null);
  add("Exploitability", f.exploit_validated ? "Exploit validated" : f.exploitable ? "Exploitable" : null);
  add("Affected asset", assetLabel(f));
  add("Operating system", maskedText([f.asset?.os, f.asset?.os_version].filter(Boolean).join(" ")));
  add("Environment", maskedText(f.asset?.environment));
  add("CVE", f.cve_ids.length ? f.cve_ids.join(", ") : null);
  add("CWE", f.cwe_ids.length ? f.cwe_ids.join(", ") : null);
  add("MITRE ATT&CK", f.mitre_techniques.length ? f.mitre_techniques.join(", ") : null);
  add("First seen", formatDate(f.first_seen, timeZone));
  add("Last seen", formatDate(f.last_seen, timeZone));
  if (isOpenStatus(f.status) && f.current_sla.deadline) {
    add("Fix by", `${formatDate(f.current_sla.deadline, timeZone)} (${humanize(f.current_sla.state)})`);
  }
  add("Owner", maskedText(f.action_tracking.owner) ?? maskedText(f.action_tracking.assigned_to_email));
  return facts.filter((x): x is Fact => x !== null);
}

export interface NarrativeSection { key: string; title: string; body: Readable }

const NARRATIVE: Array<[keyof ReportFinding, string]> = [
  ["description", "Description"],
  ["technical_details", "Technical details"],
  ["impact", "Technical impact"],
  ["business_impact", "Business impact"],
  ["exploitation", "Exploitation and attack context"],
  ["reproduction_steps", "Reproduction or validation steps"],
  ["root_cause", "Root cause"],
  ["preconditions", "Preconditions"],
];

/** Recorded narrative sections, plus the titles of those not recorded. */
export function findingNarrative(f: ReportFinding): { sections: NarrativeSection[]; missing: string[] } {
  const sections: NarrativeSection[] = [];
  const missing: string[] = [];
  for (const [key, title] of NARRATIVE) {
    const body = readable(f[key]);
    if (body) sections.push({ key: String(key), title, body });
    else missing.push(title);
  }
  return { sections, missing };
}

export interface RemediationView {
  text: string | null;
  plans: Array<{ summary: string | null; steps: string[]; verification: string[]; longTerm: string[]; compensating: string | null; effort: string | null }>;
  recommendations: string[];
}

export function remediationView(f: ReportFinding): RemediationView {
  const seen = new Set<string>();
  const recommendations: string[] = [];
  for (const text of [
    ...f.remediation.recommendations.map((r) => r.text),
    ...f.remediation.recorded_recommendations,
  ]) {
    const masked = maskedText(text);
    if (masked && !seen.has(masked.toLowerCase())) {
      seen.add(masked.toLowerCase());
      recommendations.push(masked);
    }
  }
  return {
    text: maskedText(f.remediation.recorded_text),
    plans: f.remediation.reviewed_plans.map((plan) => ({
      summary: maskedText(plan.summary),
      steps: plan.steps.map((step) => stepText(step)).filter((s): s is string => Boolean(s)),
      verification: plan.verification.map(maskedText).filter((s): s is string => Boolean(s)),
      longTerm: plan.long_term_recommendations.map(maskedText).filter((s): s is string => Boolean(s)),
      compensating: maskedText(plan.compensating_controls),
      effort: maskedText(plan.effort),
    })),
    recommendations,
  };
}

/** A recorded plan step: its action/title text when present, else readable pairs. */
function stepText(step: Record<string, unknown>): string | null {
  for (const key of ["action", "title", "description", "command", "text"]) {
    const value = step[key];
    if (typeof value === "string" && value.trim()) {
      const extras = Object.entries(step)
        .filter(([k, v]) => k !== key && !["step", "order", "index", "raw"].includes(k) && typeof v === "string" && v.trim())
        .map(([k, v]) => `${humanize(k)}: ${v}`);
      return mask([value, ...extras].join(" — "));
    }
  }
  return readableText(step, "; ");
}

export interface EvidenceView {
  ref: string;
  label: string;
  type: string | null;
  tool: string | null;
  command: string | null;
  content: string;
  capturedAt: string | null;
  sourceHost: string | null;
  sha256: string | null;
  verified: boolean | null;
}

export function evidenceView(artifact: ReportEvidenceArtifact, ref: string): EvidenceView {
  const content = artifact.content === null || artifact.content === undefined
    ? ""
    : typeof artifact.content === "string"
      ? artifact.content
      : (() => {
          try { return JSON.stringify(stripRaw(artifact.content), null, 2); } catch { return String(artifact.content); }
        })();
  return {
    ref,
    label: maskedText(artifact.label) ?? `Evidence ${artifact.index}`,
    type: maskedText(artifact.evidence_type),
    tool: maskedText(artifact.tool),
    command: maskedText(artifact.command),
    // Keep the first line's indentation (aligned tool output); drop blank edges.
    content: mask(content).replace(/^(?:[ \t]*\r?\n)+/, "").trimEnd(),
    capturedAt: artifact.captured_at ?? artifact.timestamp,
    sourceHost: maskedText(artifact.source_host),
    sha256: artifact.sha256,
    verified: artifact.sha256_verified ?? null,
  };
}

function stripRaw(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(stripRaw);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value as Record<string, unknown>)
      .filter(([key]) => key.toLowerCase() !== "raw")
      .map(([key, item]) => [key, stripRaw(item)]));
  }
  return value;
}

/** First `maxLines` lines of evidence, with the honest count of what was cut. */
export function excerpt(text: string, maxLines: number, maxChars = 6000): { text: string; shownLines: number; totalLines: number; truncated: boolean } {
  const lines = text.split(/\r?\n/);
  let shown = lines.slice(0, maxLines).join("\n");
  let truncated = lines.length > maxLines;
  if (shown.length > maxChars) {
    shown = shown.slice(0, maxChars);
    truncated = true;
  }
  return { text: shown, shownLines: shown.split("\n").length, totalLines: lines.length, truncated };
}

export interface ClosureView {
  disposition: string;
  closed: boolean;
  resolvedAt: string | null;
  method: string | null;
  reviewedBy: string | null;
  retest: "Passed" | "Failed" | null;
  retestAt: string | null;
  reopened: number;
}

export function closureView(f: ReportFinding): ClosureView {
  const retest = f.closure.retest;
  return {
    disposition: statusLabel(f.closure.current_disposition || f.status),
    closed: f.closure.is_terminal,
    resolvedAt: f.closure.resolved_at,
    method: maskedText(f.closure.resolution_method) ? humanize(maskedText(f.closure.resolution_method)) : null,
    reviewedBy: maskedText(f.closure.reviewed_by),
    retest: retest?.passed === true ? "Passed" : retest?.passed === false ? "Failed" : null,
    retestAt: retest?.verified_at ?? retest?.completed_at ?? null,
    reopened: f.closure.reopened_count,
  };
}

// ─── Remediation roadmap ─────────────────────────────────────────────────────

export interface RoadmapItem {
  /** "F001" or "F001–F004" for an issue on several assets. */
  ref: string;
  title: string;
  severity: SeverityKey;
  /** Open instances of the issue. */
  count: number;
  /** One asset's label, or "12 assets". */
  asset: string | null;
  owner: string | null;
  /** Earliest recorded deadline among the open instances. */
  deadline: string | null;
  /** Worst SLA state among the open instances. */
  slaState: string | null;
}

export interface RoadmapBucket {
  priority: 1 | 2 | 3 | 4;
  title: string;
  severities: SeverityKey[];
  /** "within 3 days (current SLA policy)" when every item shares one window. */
  target: string | null;
  items: RoadmapItem[];
  /** Open findings in the bucket (instances, not issues). */
  findings: number;
}

const BUCKETS: Array<{ priority: 1 | 2 | 3 | 4; title: string; severities: SeverityKey[] }> = [
  { priority: 1, title: "Priority 1 — fix immediately", severities: ["critical"] },
  { priority: 2, title: "Priority 2 — fix next", severities: ["high"] },
  { priority: 3, title: "Priority 3 — plan the fix", severities: ["medium"] },
  { priority: 4, title: "Priority 4 — fix in routine maintenance", severities: ["low", "info"] },
];

const SLA_RANK = ["breached", "at_risk", "due_soon", "on_track"];

/** "F001" or "F001–F004, F009" for the instances of an issue. */
export function groupRef(group: IssueGroup, refs: Map<string, string>, only?: (f: ReportFinding) => boolean): string {
  return compactRefs(group.findings.filter((f) => !only || only(f)).map((f) => refs.get(f.id) ?? ""));
}

/** Asset label for one instance, or "N assets" for several. */
export function groupAssets(findings: readonly ReportFinding[]): string | null {
  const labels = [...new Set(findings.map(assetLabel).filter((x): x is string => Boolean(x)))];
  if (labels.length === 0) return null;
  return labels.length === 1 ? labels[0]! : `${labels.length} assets`;
}

/** Open issues grouped by priority. Targets come only from the recorded SLA. */
export function remediationRoadmap(report: ReportDocument): RoadmapBucket[] {
  const refs = findingRefs(report);
  const groups = issueGroups(report.findings).filter((g) => g.open > 0);
  return BUCKETS.map((bucket) => {
    const inBucket = groups.filter((g) => bucket.severities.includes(g.severity));
    const open = inBucket.flatMap((g) => g.findings.filter((f) => isOpenStatus(f.status)));
    const windows = new Set(open.map((f) => f.current_sla.hours_total).filter((h): h is number => typeof h === "number"));
    const allTracked = open.length > 0 && open.every((f) => typeof f.current_sla.hours_total === "number");
    const only = windows.size === 1 && allTracked ? formatHours([...windows][0]) : null;
    return {
      ...bucket,
      target: only ? `within ${only} of discovery (current SLA policy)` : null,
      findings: open.length,
      items: inBucket.map((g) => {
        const live = g.findings.filter((f) => isOpenStatus(f.status));
        const owners = [...new Set(live.map((f) => maskedText(f.action_tracking.owner) ?? maskedText(f.action_tracking.assigned_to_email)).filter(Boolean))];
        const deadlines = live.map((f) => f.current_sla.deadline).filter((d): d is string => Boolean(d)).sort();
        const states = live.map((f) => f.current_sla.state).filter((s) => SLA_RANK.includes(s)).sort((a, b) => SLA_RANK.indexOf(a) - SLA_RANK.indexOf(b));
        return {
          ref: groupRef(g, refs, (f) => isOpenStatus(f.status)),
          title: g.title,
          severity: g.severity,
          count: live.length,
          asset: groupAssets(live),
          owner: owners.length === 0 ? null : owners.length === 1 ? owners[0]! : "Several owners",
          deadline: deadlines[0] ?? null,
          slaState: states[0] ?? null,
        };
      }),
    };
  }).filter((bucket) => bucket.items.length > 0);
}

// ─── Top risks ───────────────────────────────────────────────────────────────

/** The most severe open issues. */
export function topRisks(report: ReportDocument, limit = 5): Array<{ ref: string; group: IssueGroup; finding: ReportFinding }> {
  const refs = findingRefs(report);
  return issueGroups(report.findings)
    .filter((g) => g.open > 0)
    .slice(0, limit)
    .map((group) => ({ ref: groupRef(group, refs, (f) => isOpenStatus(f.status)), group, finding: group.lead }));
}

/** Narrative sections every instance of an issue records identically. */
export function sharedNarrativeKeys(group: IssueGroup): Set<string> {
  const keys = new Set<string>();
  for (const [key] of NARRATIVE) {
    const first = JSON.stringify(group.lead[key] ?? null);
    if (group.findings.every((f) => JSON.stringify(f[key] ?? null) === first)) keys.add(String(key));
  }
  return keys;
}

// ─── Record gaps, de-duplicated ──────────────────────────────────────────────

export interface GapRow { code: string; label: string; count: number; refs: string[] }

export function gapInventory(report: ReportDocument): { reportLevel: GapRow[]; findingLevel: GapRow[] } {
  const refs = findingRefs(report);
  const reportCodes = [...new Set([...report.engagement.metadata_gaps, ...report.readiness.report_gaps])];
  const findingLevel = Object.entries(report.readiness.gap_counts)
    .map(([code, count]) => ({
      code,
      label: humanize(code),
      count,
      refs: (report.readiness.affected_finding_ids[code] ?? [])
        .map((id) => refs.get(id) ?? id)
        .sort(),
    }))
    .sort((a, b) => b.count - a.count || a.code.localeCompare(b.code));
  return {
    reportLevel: reportCodes.map((code) => ({ code, label: humanize(code), count: 1, refs: [] })),
    findingLevel,
  };
}

/** "F001–F004, F007" — compact ranges for long reference lists. */
export function compactRefs(refs: readonly string[]): string {
  const nums = [...new Set(refs)]
    .map((r) => /^F(\d+)$/.exec(r)?.[1])
    .map((n) => (n ? Number(n) : NaN));
  if (nums.some(Number.isNaN)) return [...new Set(refs)].join(", ");
  const sorted = [...new Set(nums)].sort((a, b) => a - b);
  const parts: string[] = [];
  for (let i = 0; i < sorted.length; i++) {
    const start = sorted[i]!;
    let end = start;
    while (i + 1 < sorted.length && sorted[i + 1] === end + 1) end = sorted[++i]!;
    const fmt = (n: number) => `F${String(n).padStart(3, "0")}`;
    parts.push(end > start + 1 ? `${fmt(start)}–${fmt(end)}` : end === start + 1 ? `${fmt(start)}, ${fmt(end)}` : fmt(start));
  }
  return parts.join(", ");
}

// ─── Document control ────────────────────────────────────────────────────────

/** True when the recorded document status says the report was issued. */
export function isIssued(report: ReportDocument): boolean {
  const status = String(report.engagement.recorded_report_metadata.document_status ?? "").toLowerCase();
  return ["final", "issued", "approved", "published"].includes(status) && Boolean(report.engagement.recorded_report_metadata.approved_by);
}

export function metadataText(report: ReportDocument, key: string): string | null {
  return maskedText(report.engagement.recorded_report_metadata[key]);
}

export const METHOD_FIELDS: Array<[string, string]> = [
  ["methodology", "Methodology"],
  ["risk_rating_method", "Risk-rating method"],
  ["testing_narrative", "Testing narrative"],
  ["tools_used", "Tools used"],
  ["segmentation_results", "Segmentation results"],
  ["environment_cleanup", "Environment cleanup"],
  ["evidence_retention_policy", "Evidence retention"],
  ["limitations", "Limitations"],
];

/** FIRST CVSS v3.1 qualitative scale — the reference the ratings align to. */
export const SEVERITY_DEFINITIONS: Array<{ severity: SeverityKey; cvss: string; meaning: string }> = [
  { severity: "critical", cvss: "9.0 – 10.0", meaning: "Direct, likely compromise of systems or data. Fix immediately." },
  { severity: "high", cvss: "7.0 – 8.9", meaning: "Serious weakness that an attacker can realistically use. Fix as a priority." },
  { severity: "medium", cvss: "4.0 – 6.9", meaning: "Weakness that needs other conditions or gives limited access. Plan the fix." },
  { severity: "low", cvss: "0.1 – 3.9", meaning: "Minor weakness or defence-in-depth gap. Fix in routine maintenance." },
  { severity: "info", cvss: "0.0", meaning: "Observation with no direct risk, recorded for awareness." },
];

// ─── Executive narrative ─────────────────────────────────────────────────────

/**
 * The executive summary's sentences, composed only from recorded counts and the
 * disclosed rating rule. Shared so every format says exactly the same thing.
 */
export function executiveNarrative(report: ReportDocument, timeZone = "UTC"): { sentences: string[]; ratingIndex: number } {
  const m = keyMetrics(report);
  const rating = overallRating(report);
  const rows = severityRows(report);
  const groups = issueGroups(report.findings);
  const client = maskedText(report.engagement.client) || "the client";
  const ranges = report.engagement.scope_cidrs.length;
  const window = [formatDate(report.engagement.start_time, timeZone), formatDate(report.engagement.end_time, timeZone)].filter(Boolean).join(" to ");
  const counts = rows.filter((r) => r.total > 0).map((r) => `${r.total} ${SEVERITY_LABEL[r.severity].toLowerCase()}`).join(", ");
  const sentences = [
    `This report presents the results of the vulnerability assessment of ${client}${ranges ? `, covering ${ranges} network range${ranges === 1 ? "" : "s"}` : ""}${window ? `, carried out from ${window}` : ""}.`,
    m.total
      ? `The assessment recorded ${m.total} finding${m.total === 1 ? "" : "s"}${groups.length < m.total ? ` across ${groups.length} distinct issue${groups.length === 1 ? "" : "s"}` : ""}${counts ? ` (${counts})` : ""}. ${m.open} remain${m.open === 1 ? "s" : ""} open and ${m.closed} ${m.closed === 1 ? "has" : "have"} a closing disposition.`
      : "The assessment recorded no findings.",
    rating.level === "none" ? `Overall risk: ${rating.label.toLowerCase()}. ${rating.basis}` : `Overall risk is rated ${rating.label.toUpperCase()}. ${rating.basis}`,
  ];
  const ratingIndex = 2;
  if (m.slaBreached) sentences.push(`${m.slaBreached} open finding${m.slaBreached === 1 ? " is" : "s are"} past the remediation deadline set by the current SLA policy.`);
  if (m.exploitableOpen) sentences.push(`${m.exploitableOpen} open finding${m.exploitableOpen === 1 ? " is" : "s are"} recorded as exploitable.`);
  return { sentences, ratingIndex };
}

/** "Priority 1: fix immediately — 4 findings (F001–F004), within 3 days…". */
export function priorityLines(report: ReportDocument): string[] {
  return remediationRoadmap(report).map((b) =>
    `${b.title.replace(/^Priority (\d) — /, "Priority $1: ")} — ${b.findings} finding${b.findings === 1 ? "" : "s"}${b.items.length < b.findings ? ` in ${b.items.length} issue${b.items.length === 1 ? "" : "s"}` : ""} (${b.items.map((i) => i.ref).join(", ")})${b.target ? `, ${b.target}` : ""}.`);
}

/** Facts for an issue: the lead's, with per-asset facts summarised when it
 *  affects several assets (earliest first-seen and fix-by). */
export function issueFacts(group: IssueGroup, timeZone = "UTC"): Fact[] {
  const facts = findingFacts(group.lead, timeZone);
  if (group.findings.length === 1) return facts;
  const PER_ASSET = new Set(["Affected asset", "Operating system", "Environment", "Fix by", "Owner", "First seen", "Last seen"]);
  const live = group.findings.filter((f) => isOpenStatus(f.status));
  const earliest = live.map((f) => f.current_sla.deadline).filter((d): d is string => Boolean(d)).sort()[0];
  const firstSeen = group.findings.map((f) => f.first_seen).filter((d): d is string => Boolean(d)).sort()[0];
  return [
    ...facts.filter((x) => !PER_ASSET.has(x.label)),
    { label: "Affected assets", value: String(group.findings.length) },
    ...(firstSeen ? [{ label: "First seen", value: formatDate(firstSeen, timeZone)! }] : []),
    ...(earliest ? [{ label: "Earliest fix-by", value: formatDate(earliest, timeZone)! }] : []),
  ];
}

/** "3 open · 2 remediated", or the single status for one finding. */
export function statusSummary(findings: readonly ReportFinding[]): string {
  const counts = new Map<string, number>();
  for (const f of findings) counts.set(statusLabel(f.status), (counts.get(statusLabel(f.status)) ?? 0) + 1);
  if (findings.length === 1) return [...counts.keys()][0] ?? "";
  return [...counts.entries()].map(([label, n]) => `${n} ${label.toLowerCase()}`).join(" · ");
}
