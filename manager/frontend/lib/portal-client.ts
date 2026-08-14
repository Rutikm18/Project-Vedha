/**
 * Browser-side client for the customer portal BFF (/api/portal/*). On a 401 it
 * bounces to the portal login. Every response is already engagement-scoped by
 * FastAPI — this layer just fetches and unwraps errors.
 */
export async function portalApi<T>(
  path: string,
  opts: { method?: string; body?: unknown } = {},
): Promise<T> {
  const res = await fetch(`/api/portal${path}`, {
    method: opts.method ?? "GET",
    headers: { "Content-Type": "application/json" },
    body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
    cache: "no-store",
  });
  if (res.status === 401) {
    if (typeof window !== "undefined") window.location.href = "/portal/login";
    throw new Error("Not authenticated");
  }
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    throw new Error((data && (data.error || data.detail)) || res.statusText);
  }
  return data as T;
}

// ── shared shapes (mirror the FastAPI portal schemas) ──────────────────────────
export interface PortalEngagement {
  id: string;
  name: string;
  status: string;
  scope_cidr_count: number;
  has_assigned_agent: boolean;
}
export interface PortalPosture {
  risk_index: number;
  exploitable_score: number;
  posture_score: number;
  grade: string;
  open_findings: number;
}
export interface PortalFinding {
  id: string;
  title: string;
  description: string | null;
  severity: string;
  status: string;
  cvss_score: number | null;
  cve_ids: string[] | null;
  risk_score: number | null;
  remediation: string | null;
  first_seen: string | null;
}
export interface PortalReport {
  id: string;
  output_type: string;
  model: string;
  generated_at: string;
}
export interface PortalScan {
  id: string;
  kind: string;
  scan_type: string;
  status: string;
  at: string | null;
}

export const SEVERITY_STYLE: Record<string, string> = {
  critical: "bg-red-100 text-red-700 ring-red-600/20",
  high: "bg-orange-100 text-orange-700 ring-orange-600/20",
  medium: "bg-amber-100 text-amber-700 ring-amber-600/20",
  low: "bg-sky-100 text-sky-700 ring-sky-600/20",
  info: "bg-slate-100 text-slate-600 ring-slate-500/20",
};

export const GRADE_STYLE: Record<string, string> = {
  A: "text-emerald-600",
  B: "text-lime-600",
  C: "text-amber-600",
  D: "text-orange-600",
  F: "text-red-600",
};
