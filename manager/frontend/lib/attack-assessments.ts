import { ApiError } from "./fetcher";

export interface AssessmentSnapshot {
  id: string;
  status: "queued" | "running" | "completed" | "failed";
  effective_as_of: string;
  failure_code: string | null;
  requires_reassessment: boolean;
}
export interface AssessmentLatest {
  can_compute: boolean;
  latest_request: AssessmentSnapshot | null;
  last_completed: AssessmentSnapshot | null;
  state: string;
}
export interface FindingAssessment {
  finding_id: string;
  title: string;
  severity: string;
  lifecycle: string;
  asset_label: string;
  service_endpoint?: string | null;
  rule_version?: string;
  goal: string;
  goal_state: "indeterminate" | "not_evaluated";
  rule_applicability: "candidate" | "unmapped";
  supported_proofs: number;
  prerequisites: Array<{ key: string; label: string; state: "supported" | "missing"; detail: string }>;
  next_action: string;
  owner_ref: string | null;
  verification_required: string;
}
export interface AssessmentPage {
  snapshot: AssessmentSnapshot;
  total: number;
  total_findings: number | null;
  page: number;
  page_size: number;
  items: FindingAssessment[];
  compute: string;
  coverage: string;
}

/** A denied feature must not log a valid operator out of the entire product. */
export async function assessmentRequest<T>(url: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  const request = () => fetch(url, { ...init, credentials: "same-origin", cache: "no-store" });
  try {
    response = await request();
    if (response.status === 401) {
      const refreshed = await fetch("/api/auth/login", { method: "PUT", credentials: "same-origin", cache: "no-store" });
      if (refreshed.ok) response = await request();
    }
  } catch {
    throw new ApiError("Cannot reach the assessment service. Check your connection and retry.", 0);
  }
  if (!response.ok) {
    let message = `Assessment request failed (${response.status}).`;
    try {
      const body = await response.json();
      const detail = body.error ?? body.detail;
      if (typeof detail === "string") message = detail;
    } catch { /* Preserve a useful status when the server sends a non-JSON error. */ }
    throw new ApiError(message, response.status);
  }
  return response.json() as Promise<T>;
}

export function assessmentBase(engagementId: string): string {
  return `/api/engagements/${encodeURIComponent(engagementId)}/attack-assessments`;
}
