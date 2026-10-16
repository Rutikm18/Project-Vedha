/**
 * The audit log: shapes, filter state and wording. The server records and verifies; this
 * file maps its snake_case JSON to UI shapes and builds the queries and export links.
 */

export type AuditOutcome = "success" | "failure" | "denied";

export interface AuditEntry {
  id: string;
  timestamp: string;
  action: string;
  label: string;
  category: string;
  categoryLabel: string;
  outcome: AuditOutcome;
  actor: { id: string; type: string | null; label: string | null };
  resourceType: string | null;
  resourceId: string | null;
  engagementId: string | null;
  engagementName: string | null;
  ipAddress: string | null;
  userAgent: string | null;
  requestId: string | null;
  detail: Record<string, unknown> | null;
  changes: Record<string, { before: unknown; after: unknown }> | null;
  chainPosition: number | null;
  entryHash: string | null;
}

export interface AuditPage { items: AuditEntry[]; nextCursor: string | null }

export interface CustomerAuditEntry {
  id: string; timestamp: string; label: string; category: string; categoryLabel: string;
  outcome: AuditOutcome; who: string; whoIsVedha: boolean; ipAddress: string | null;
}
export interface CustomerAuditPage { items: CustomerAuditEntry[]; nextCursor: string | null }

export interface AuditFacets {
  categories: { key: string; label: string; count: number }[];
  outcomes: { key: AuditOutcome; count: number }[];
}

export interface AuditIntegrity {
  ok: boolean;
  entriesChecked: number;
  oldest: string | null;
  newest: string | null;
  firstProblem: { position: number; entryId: string; reason: string } | null;
  retentionDays: number;
  minimumRetentionDays: number;
  checkedAt: string;
}

export function mapAuditEntry(e: any): AuditEntry {
  return {
    id: e.id, timestamp: e.timestamp, action: e.action, label: e.label,
    category: e.category, categoryLabel: e.category_label, outcome: e.outcome,
    actor: { id: e.actor?.id ?? "", type: e.actor?.type ?? null, label: e.actor?.label ?? null },
    resourceType: e.resource_type ?? null, resourceId: e.resource_id ?? null,
    engagementId: e.engagement_id ?? null, engagementName: e.engagement_name ?? null,
    ipAddress: e.ip_address ?? null, userAgent: e.user_agent ?? null, requestId: e.request_id ?? null,
    detail: e.detail ?? null, changes: e.changes ?? null,
    chainPosition: e.chain_position ?? null, entryHash: e.entry_hash ?? null,
  };
}

export function mapAuditPage(p: any): AuditPage {
  return { items: (p?.items ?? []).map(mapAuditEntry), nextCursor: p?.next_cursor ?? null };
}

export function mapCustomerPage(p: any): CustomerAuditPage {
  return {
    items: (p?.items ?? []).map((e: any) => ({
      id: e.id, timestamp: e.timestamp, label: e.label, category: e.category,
      categoryLabel: e.category_label, outcome: e.outcome, who: e.who,
      whoIsVedha: Boolean(e.who_is_vedha), ipAddress: e.ip_address ?? null,
    })),
    nextCursor: p?.next_cursor ?? null,
  };
}

export function mapIntegrity(i: any): AuditIntegrity {
  return {
    ok: Boolean(i?.ok), entriesChecked: i?.entries_checked ?? 0,
    oldest: i?.oldest ?? null, newest: i?.newest ?? null,
    firstProblem: i?.first_problem
      ? { position: i.first_problem.position, entryId: i.first_problem.entry_id, reason: i.first_problem.reason }
      : null,
    retentionDays: i?.retention_days ?? 365, minimumRetentionDays: i?.minimum_retention_days ?? 180,
    checkedAt: i?.checked_at ?? "",
  };
}

// ── filters ─────────────────────────────────────────────────────────────────

export interface AuditFilterState {
  /** YYYY-MM-DD, read as a UTC day. */
  from: string;
  to: string;
  category: string;
  outcome: "" | AuditOutcome;
  q: string;
  actor: string;
  ip: string;
}

export const EMPTY_FILTERS: AuditFilterState = { from: "", to: "", category: "", outcome: "", q: "", actor: "", ip: "" };

const DAY = /^\d{4}-\d{2}-\d{2}$/;

/** The query string for the list, facets and export, from the filter state. */
export function auditQuery(f: AuditFilterState, extra: Record<string, string | number | undefined> = {}): string {
  const p = new URLSearchParams();
  if (DAY.test(f.from)) p.set("from", `${f.from}T00:00:00Z`);
  if (DAY.test(f.to)) p.set("to", `${f.to}T23:59:59.999Z`);
  if (f.category) p.set("category", f.category);
  if (f.outcome) p.set("outcome", f.outcome);
  if (f.q.trim()) p.set("q", f.q.trim());
  if (f.actor.trim()) p.set("actor", f.actor.trim());
  if (f.ip.trim()) p.set("ip", f.ip.trim());
  for (const [k, v] of Object.entries(extra)) if (v !== undefined && v !== "") p.set(k, String(v));
  return p.toString();
}

export function hasFilters(f: AuditFilterState): boolean {
  return Object.values(f).some((v) => v !== "");
}

/** Number of filters in force, for the "Clear (n)" control. */
export function filterCount(f: AuditFilterState): number {
  return Object.values(f).filter((v) => v !== "").length;
}

export type Period = "24h" | "7d" | "30d" | "all";

/** A quick period as UTC days, relative to `now`. "all" clears both ends. */
export function periodRange(period: Period, now: Date = new Date()): { from: string; to: string } {
  if (period === "all") return { from: "", to: "" };
  const days = { "24h": 1, "7d": 7, "30d": 30 }[period];
  const from = new Date(now.getTime() - days * 86_400_000);
  return { from: from.toISOString().slice(0, 10), to: "" };
}

export function exportHref(f: AuditFilterState, format: "csv" | "json"): string {
  return `/api/audit-logs/export?${auditQuery(f, { format })}`;
}

// ── wording ────────────────────────────────────────────────────────────────────

/** 2026-10-16 08:21:04 UTC — audit evidence is read in UTC. */
export function formatUtc(value: string): string {
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return `${d.toISOString().slice(0, 19).replace("T", " ")} UTC`;
}

export const OUTCOME_LABEL: Record<AuditOutcome, string> = {
  success: "Succeeded", failure: "Failed", denied: "Refused",
};

export function actorName(e: Pick<AuditEntry, "actor">): string {
  const { label, id, type } = e.actor;
  if (label) return label;
  if (type === "anonymous") return "Not signed in";
  if (type === "system") return "System";
  return id.length > 12 ? `${id.slice(0, 8)}…` : id;
}

/** Changes as "field: before → after" lines, in field order. */
export function changeLines(changes: AuditEntry["changes"]): { field: string; before: string; after: string }[] {
  if (!changes) return [];
  const show = (v: unknown) => (v === null || v === undefined ? "—" : typeof v === "object" ? JSON.stringify(v) : String(v));
  return Object.entries(changes).map(([field, c]) => ({ field, before: show(c?.before), after: show(c?.after) }));
}

export function integritySentence(i: AuditIntegrity): string {
  if (i.entriesChecked === 0) return "No entries yet, so nothing to verify.";
  if (i.ok) return `Tamper check passed: ${i.entriesChecked.toLocaleString("en")} entries verified in order.`;
  const p = i.firstProblem;
  return `Tamper check failed${p ? ` at entry ${p.position}: ${p.reason}` : ""}. Treat the log from that point as untrusted.`;
}

/** What each field of an entry answers, and the controls it supports. These are the
 *  requirements an auditor typically maps the field to, not a claim of certification. */
export const RECORDED_FIELDS: { field: string; answers: string; controls: string }[] = [
  { field: "Time (UTC)", answers: "When it happened", controls: "PCI DSS 10.2.2 · NIST AU-3 · ISO 27001 A.8.15" },
  { field: "Actor, type and identity", answers: "Who did it (identity kept as it was at the time)", controls: "PCI DSS 10.2.2 · NIST AU-3 · HIPAA 164.312(b)" },
  { field: "Action and resource", answers: "What was done, and to what", controls: "PCI DSS 10.2.2 · NIST AU-2, AU-3" },
  { field: "Outcome", answers: "Whether it worked, failed, or was refused", controls: "PCI DSS 10.2.2, 10.2.1.4 · NIST AU-3" },
  { field: "Source address and user agent", answers: "Where it came from", controls: "PCI DSS 10.2.2 · CERT-In logging directions" },
  { field: "Request ID", answers: "Ties the entry to the request's other logs", controls: "NIST AU-3 · ISO 27001 A.8.15" },
  { field: "Before / after", answers: "What a change replaced", controls: "NIST AU-3(1) · SOC 2 CC8.1" },
  { field: "Chain position and hash", answers: "Shows nothing was altered or removed", controls: "PCI DSS 10.3.4 · NIST AU-9(3) · ISO 27001 A.8.15" },
];
