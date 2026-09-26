/**
 * remediation.ts — contracts + transport for contextual remediation.
 *
 * One API for both surfaces (operator console and customer portal). The backend
 * computes everything (app/remediation/*): plans are asset-grounded, bundles and
 * due dates are deterministic, AI refinements are overlays behind a review gate.
 * The UI only renders — it never invents a date, a target or a grouping.
 */
import { fetchJson } from "./fetcher";
import { portalApi } from "./portal-client";

export type RemediationSurface = "manager" | "portal";
export type PlanOs = "generic" | "linux" | "windows" | "macos";
export type Tier = "containment" | "fix" | "hardening";
export type Urgency = "act" | "attend" | "track_star" | "track";
export type DueSource = "extension" | "engagement" | "tenant" | "default" | null;

export interface FactValue { value: string | number | null; source: "scan" | "asset_record" | "not_recorded"; }

export interface PlanStep {
  step: number;
  tier: Tier;
  title: string;
  description: string;
  commands?: Record<string, string[]> | null;
  commands_for_os: string[];
  pre_checks: string[];
  reboot_required: boolean | null;
  downtime: string;
  rollback: string;
  risk: "low" | "medium" | "high";
  unsafe_commands_removed?: boolean;
  ai_changed?: boolean;
  ai_added?: boolean;
}

export interface AiChange { field: string; step: number | null; before: unknown; after: unknown; }

export interface RemediationPlan {
  recipe_id?: string | null;
  recipe_version?: number | null;
  os: PlanOs;
  os_auto?: PlanOs | null;
  source: string;
  title?: string | null;
  summary: string;
  effort: "low" | "medium" | "high";
  remediation_risk: "low" | "medium" | "high";
  remediation_type?: string | null;
  risk_response?: string | null;
  target_state?: string | null;
  urgency?: { label: Urgency; drivers: string[]; framework?: string } | null;
  due?: { at: string | null; source: DueSource } | null;
  context?: Record<string, FactValue> | null;
  exposure?: string | null;
  steps: PlanStep[];
  verification: string[];
  verification_check?: { scanner: string; check: string; expected: string; manual_command: string } | null;
  long_term_recommendations: string[];
  compensating_controls: string;
  references?: string[];
  fragile_guard?: { active: boolean; reason: string | null } | null;
  provenance?: Record<string, unknown> | null;
  ai_changes?: AiChange[];
  sequencing_rationale?: string;
  model?: string | null;
}

export interface PlanResponse {
  finding_id: string;
  os: PlanOs;
  source: string;
  reviewed: boolean;
  cached: boolean;
  generated_at: string | null;
  model: string | null;
  stale: boolean;
  bundle: { fix_key: string; ref: string; recipe_id: string } | null;
  plan: RemediationPlan;
}

export interface BundleHost {
  host: string; ip: string; os: string; os_family: string; ports: number[]; finding_ids: string[];
  status: "open" | "closed" | "extension_approved" | "excluded";
  due_at: string | null; due_source: DueSource; closed_at: string | null;
}

export interface Bundle {
  fix_key: string; ref: string; recipe_id: string; product_family: string | null; title: string;
  remediation_type: string; risk_response: string; target_state: string; effort: string; remediation_risk: string;
  steps_by_os: Record<string, PlanStep[]>;
  verification_check: { scanner: string; check: string; expected: string; manual_command: string };
  compensating_controls: string; references: string[]; hosts: BundleHost[]; resolves: string[];
  open_finding_ids: string[]; excluded: { finding_id: string; reason: string }[];
  open_count: number; closed_count: number; due_at: string | null; due_source: DueSource;
  urgency: Urgency; progress: { closed: number; total: number }; status: "open" | "done";
  /** Worst severity among OPEN members, and whether any is on CISA KEV. */
  max_severity: string | null; kev: boolean;
}

export interface HostRow {
  host: string; ip: string; os: string; open_count: number; next_due_at: string | null;
  bundles: Array<{ fix_key: string; ref: string; recipe_id: string; title: string; target_state: string;
    remediation_type: string; urgency: Urgency; status: BundleHost["status"]; due_at: string | null;
    due_source: DueSource; finding_ids: string[]; ports: number[] }>;
}

export interface BundleSummary {
  bundles: number; open_bundles: number; done_bundles: number; open_findings: number;
  closed_findings: number; hosts: number; act: number;
}

export interface BundlesResponse {
  view: "fix" | "host"; sla_source: string; summary: BundleSummary; generated_at: string;
  bundles?: Bundle[]; hosts?: HostRow[];
}

export interface ExtensionRequest {
  id: string; engagement_id: string; subject_type: "finding" | "bundle"; finding_id: string | null;
  fix_key: string | null; fix_ref: string | null; member_finding_ids: string[];
  current_due_at: string | null; requested_due_at: string; reason: string; compensating_control: string | null;
  status: "pending" | "approved" | "rejected" | "withdrawn"; requested_by: string | null; requested_at: string | null;
  decided_by: string | null; decided_at: string | null; decided_due_at: string | null; decision_note: string | null;
}

export interface ExtensionCreate {
  subject_type: "finding" | "bundle"; finding_id?: string; fix_key?: string;
  requested_due_at: string; reason: string; compensating_control?: string;
}

const q = (params: Record<string, string | boolean | undefined>) => {
  const s = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== "") s.set(k, String(v));
  const out = s.toString();
  return out ? `?${out}` : "";
};

export function createRemediationApi(surface: RemediationSurface) {
  if (surface === "manager") {
    return {
      surface,
      plan: (findingId: string, os?: PlanOs) =>
        fetchJson<PlanResponse>(`/api/findings/${findingId}/remediation${q({ os })}`),
      refine: (findingId: string, os: PlanOs, opts: { force?: boolean; publish?: boolean } = {}) =>
        fetchJson<PlanResponse>(`/api/findings/${findingId}/remediation/refine${q({ os, force: opts.force, publish: opts.publish })}`,
          { method: "POST" }),
      publish: (findingId: string, os: PlanOs) =>
        fetchJson<PlanResponse>(`/api/findings/${findingId}/remediation/publish${q({ os })}`, { method: "POST" }),
      bundles: (engagementId: string, view: "fix" | "host") =>
        fetchJson<BundlesResponse>(`/api/engagements/${engagementId}/remediation/bundles${q({ view })}`),
      refineBundle: (engagementId: string, fixKey: string, os: PlanOs) =>
        fetchJson<{ plan: RemediationPlan; reviewed: boolean; stale: boolean; model: string | null }>(
          `/api/engagements/${engagementId}/remediation/bundles/${fixKey}/refine${q({ os })}`, { method: "POST" }),
      extensions: (engagementId: string, status?: string) =>
        fetchJson<{ items: ExtensionRequest[] }>(`/api/engagements/${engagementId}/extensions${q({ status })}`),
      decide: (requestId: string, action: "approve" | "reject", body: { note: string; due_at?: string }) =>
        fetchJson<ExtensionRequest>(`/api/extensions/${requestId}/${action}`, {
          method: "POST", body: JSON.stringify(body),
        }),
      requestExtension: async (body: ExtensionCreate): Promise<ExtensionRequest> => {
        void body;
        throw new Error("Deadline extensions are requested by the customer in the portal.");
      },
      withdraw: async (id: string): Promise<ExtensionRequest> => {
        void id;
        throw new Error("Only the requester can withdraw an extension request.");
      },
      exportUrl: (engagementId: string, format: "xlsx" | "csv") =>
        `/api/engagements/${engagementId}/remediation/export?format=${format}`,
    };
  }
  return {
    surface,
    plan: (findingId: string, os?: PlanOs) =>
      portalApi<PlanResponse>(`/findings/${findingId}/remediation${q({ os })}`),
    refine: async (): Promise<PlanResponse> => { throw new Error("Not available in the portal."); },
    publish: async (): Promise<PlanResponse> => { throw new Error("Not available in the portal."); },
    bundles: (engagementId: string, view: "fix" | "host") => {
      void engagementId;
      return portalApi<BundlesResponse>(`/remediation/bundles${q({ view })}`);
    },
    refineBundle: async (): Promise<{ plan: RemediationPlan; reviewed: boolean; stale: boolean; model: string | null }> => {
      throw new Error("Not available in the portal.");
    },
    extensions: (engagementId: string) => {
      void engagementId;   // the portal is pinned to the customer's engagement server-side
      return portalApi<{ items: ExtensionRequest[] }>("/extensions");
    },
    decide: async (): Promise<ExtensionRequest> => { throw new Error("Not available in the portal."); },
    requestExtension: (body: ExtensionCreate) =>
      portalApi<ExtensionRequest>("/extensions", { method: "POST", body, idempotencyKey: crypto.randomUUID() }),
    withdraw: (id: string) =>
      portalApi<ExtensionRequest>(`/extensions/${id}/withdraw`, { method: "POST", idempotencyKey: crypto.randomUUID() }),
    exportUrl: (engagementId: string, format: "xlsx" | "csv") => {
      void engagementId;
      return `/api/portal/remediation/export?format=${format}`;
    },
  };
}

export type RemediationApi = ReturnType<typeof createRemediationApi>;

// ── presentation helpers (pure; unit-tested) ─────────────────────────────────

const IST = new Intl.DateTimeFormat("en-IN", {
  timeZone: "Asia/Kolkata", day: "2-digit", month: "short", year: "numeric",
  hour: "2-digit", minute: "2-digit", hour12: false,
});

/** "11 Oct 2026, 12:00 IST" — every due date shows date AND time in the project zone. */
export function fmtIst(iso: string | null | undefined): string {
  if (!iso) return "No target";
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? "No target" : `${IST.format(d)} IST`;
}

export function dueState(iso: string | null | undefined, now: number = Date.now()):
  "overdue" | "due_soon" | "on_track" | "none" {
  if (!iso) return "none";
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return "none";
  if (t <= now) return "overdue";
  if (t - now <= 7 * 86_400_000) return "due_soon";
  return "on_track";
}

export const DUE_SOURCE_LABEL: Record<string, string> = {
  extension: "Approved extension",
  engagement: "Engagement SLA",
  tenant: "Organisation SLA",
  default: "Default SLA",
};

export const URGENCY_LABEL: Record<Urgency, string> = {
  act: "Act", attend: "Attend", track_star: "Track*", track: "Track",
};

export const TYPE_LABEL: Record<string, string> = {
  vendor_fix: "Vendor fix", workaround: "Workaround", mitigation: "Mitigation",
  none_available: "No fix available", no_fix_planned: "No fix planned",
};

export const TIER_LABEL: Record<Tier, string> = {
  containment: "Contain now", fix: "Fix properly", hardening: "Stop it recurring",
};

/** The fact rows worth showing in the context card, in reading order. */
export const CONTEXT_FIELDS: Array<[string, string]> = [
  ["host", "Host"], ["ip", "IP"], ["os_version", "OS"], ["port", "Port"], ["service_name", "Service"],
  ["product", "Product"], ["version", "Version"], ["criticality", "Criticality"], ["environment", "Environment"],
];

export function factText(ctx: Record<string, FactValue> | null | undefined, key: string): string {
  const f = ctx?.[key];
  if (!f || f.source === "not_recorded" || f.value === null || f.value === "") return "not recorded";
  return String(f.value);
}

/** Minimum valid extension date for the date picker: one day after the current due date. */
export function minExtensionDate(currentDue: string | null | undefined, now: number = Date.now()): string {
  const base = currentDue ? Math.max(new Date(currentDue).getTime(), now) : now;
  return new Date(base + 86_400_000).toISOString().slice(0, 10);
}
