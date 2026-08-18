/**
 * Browser-side client for the customer portal BFF (/api/portal/*). On a 401 it
 * bounces to the portal login. Every response is already engagement-scoped by
 * FastAPI — this layer just fetches and unwraps errors.
 */
import type { CSSProperties } from "react";
export async function portalApi<T>(
  path: string,
  opts: { method?: string; body?: unknown } = {},
): Promise<T> {
  const send = () =>
    fetch(`/api/portal${path}`, {
      method: opts.method ?? "GET",
      headers: { "Content-Type": "application/json" },
      body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
      cache: "no-store",
    });

  let res = await send();

  // Access token likely just expired (15 min). Rotate once with the path-scoped
  // refresh cookie and replay the request before giving up — so a customer isn't
  // kicked to login mid-task. Matches the operator fetcher's refresh-on-401.
  if (res.status === 401) {
    const rr = await fetch("/api/portal/login", { method: "PUT" }).catch(() => null);
    if (rr && rr.ok) {
      res = await send();
    }
    if (res.status === 401) {
      if (typeof window !== "undefined") window.location.href = "/portal/login";
      throw new Error("Not authenticated");
    }
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
  scope_cidrs: string[];
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
export interface PortalScanRequest {
  id: string;
  scan_type: string;
  status: string;
  targets: string[] | null;
  intensity: string | null;
  note: string | null;
  requested_at: string | null;
}
export interface PortalUseCase {
  use_case_id: string;
  display_name: string;
  description: string;
  profile: string | null;
  intensity?: string | null;
  expected_runtime_hint?: string | null;
}
export interface PortalSummary {
  posture: PortalPosture;
  open_findings: number;
  closed_findings: number;
  severity_counts: Record<string, number>;
  pending_requests: number;
  running_jobs: number;
}
export interface PortalTrendPoint { period: string; opened: number; closed: number }
export interface PortalTrends {
  by_severity: Record<string, number>;
  timeline: PortalTrendPoint[];
}

// Severity → the app's theme-aware colour token (tracks light/dark like the
// operator console, instead of the old hardcoded Tailwind palette).
export const SEVERITY_VAR: Record<string, string> = {
  critical: "var(--sev-critical-color)",
  high: "var(--sev-high-color)",
  medium: "var(--sev-medium-color)",
  low: "var(--sev-low-color)",
  info: "var(--sev-info-color)",
};

/** Inline style for a severity chip using theme tokens (with a tinted fill). */
export function severityChip(severity: string): CSSProperties {
  const c = SEVERITY_VAR[severity] ?? SEVERITY_VAR.info;
  return {
    color: c,
    background: `color-mix(in srgb, ${c} 12%, transparent)`,
    border: `0.5px solid color-mix(in srgb, ${c} 34%, transparent)`,
  };
}

export const GRADE_VAR: Record<string, string> = {
  A: "var(--sev-info-color)",
  B: "var(--nominal-color)",
  C: "var(--sev-medium-color)",
  D: "var(--sev-high-color)",
  F: "var(--sev-critical-color)",
};
