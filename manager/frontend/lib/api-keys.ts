/**
 * API key (personal access token) helpers for Settings → API Keys.
 *
 * Scopes must be ones the backend accepts (app/auth/pat.py ALLOWED_PAT_SCOPES);
 * the old page sent "read" and "write", which the backend refuses. The presets
 * below are the sensible bundles of the real scopes, least privilege first.
 */

export interface ScopePreset {
  id: "read" | "readwrite" | "probe";
  label: string;
  detail: string;
  scopes: string[];
}

export const SCOPE_PRESETS: ScopePreset[] = [
  { id: "read", label: "Read only", detail: "Reports, findings and dashboards. Cannot change anything.", scopes: ["api:read"] },
  { id: "readwrite", label: "Read and write", detail: "Everything your role can do: start scans, change findings, create engagements.", scopes: ["api:read", "api:write"] },
  { id: "probe", label: "Probe or agent", detail: "Enrol and run a probe. No access to findings or reports.",
    scopes: ["probe:read", "probe:write", "probe:register", "engagement:read", "engagement:write"] },
];

export const DEFAULT_PRESET: ScopePreset["id"] = "read";

export const EXPIRY_DAYS = [7, 30, 90, 365] as const;
export const DEFAULT_EXPIRY_DAYS = 90;

/** An unused key this old is worth revoking. */
export const STALE_AFTER_DAYS = 90;

export function createPayload(name: string, presetId: ScopePreset["id"], expiresInDays: number) {
  const preset = SCOPE_PRESETS.find((p) => p.id === presetId) ?? SCOPE_PRESETS[0];
  return { name: name.trim(), scopes: preset.scopes, expires_in_days: expiresInDays };
}

/** A short human label for a token's scopes. */
export function describeScopes(scopes: string[]): string {
  const set = new Set(scopes);
  if (set.has("api:*")) return "Full access";
  const match = SCOPE_PRESETS.find((p) => p.scopes.length === set.size && p.scopes.every((s) => set.has(s)));
  if (match) return match.label;
  return scopes.length ? scopes.join(", ") : "No scopes";
}

export interface PatLike {
  created_at: string;
  expires_at?: string | null;
  last_used_at?: string | null;
  revoked_at?: string | null;
}

export type PatStatus = "active" | "expired" | "revoked";

export function patStatus(pat: PatLike, now: Date = new Date()): PatStatus {
  if (pat.revoked_at) return "revoked";
  if (pat.expires_at && new Date(pat.expires_at) < now) return "expired";
  return "active";
}

const DAY_MS = 86_400_000;

/** Reasons to look twice at a live key: it never expires, or nobody has used it for a long time. */
export function patWarnings(pat: PatLike, now: Date = new Date()): Array<"no_expiry" | "unused"> {
  if (patStatus(pat, now) !== "active") return [];
  const out: Array<"no_expiry" | "unused"> = [];
  if (!pat.expires_at) out.push("no_expiry");
  const lastActivity = new Date(pat.last_used_at ?? pat.created_at).getTime();
  if (now.getTime() - lastActivity >= STALE_AFTER_DAYS * DAY_MS) out.push("unused");
  return out;
}

/** Live keys first, then expired, then revoked; newest first within each. */
export function sortPats<T extends PatLike>(pats: T[], now: Date = new Date()): T[] {
  const rank: Record<PatStatus, number> = { active: 0, expired: 1, revoked: 2 };
  return [...pats].sort((a, b) =>
    rank[patStatus(a, now)] - rank[patStatus(b, now)]
    || new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
}
