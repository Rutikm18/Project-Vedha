/**
 * Organisation policy settings (Settings → Access & Security / Scanning / New
 * customers). The server owns the rules and validates every field; these helpers
 * only shape what the forms send and read, and turn server errors into sentences.
 */

export interface AuthPolicy {
  ip_allowlist: string[];
  ip_allowlist_applies_to_portal: boolean;
  operator_session_max_hours: number | null;
  customer_session_max_hours: number | null;
  mfa_required_for_operators: boolean;
  mfa_required_for_customers: boolean;
}

export interface BlackoutWindow {
  name: string;
  kind: "weekly" | "once";
  timezone: string;
  days: number[];
  start: string | null;
  end: string | null;
  starts_at: string | null;
  ends_at: string | null;
}

export interface ScanPolicy {
  blackouts: BlackoutWindow[];
  admin_override: boolean;
  global_exclusions: string[];
}

export type LockSeverity = "critical" | "high" | "medium" | "low" | "info";
export type LockFeature = "ai_assistant" | "compliance" | "remediation" | "reports";

export interface CustomerDefaults {
  poc_locked_severities: LockSeverity[];
  poc_locked_features: LockFeature[];
  poc_duration_days: number;
  support_contact: string;
}

export const DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] as const;

/** One entry per non-empty line or comma, trimmed. */
export function listFromText(text: string): string[] {
  return text.split(/[\n,]+/).map((s) => s.trim()).filter(Boolean);
}

export function textFromList(list: readonly string[]): string {
  return list.join("\n");
}

/** "" -> null (no limit), otherwise a whole number of hours, or NaN when it is not one. */
export function hoursFromInput(value: string): number | null {
  const v = value.trim();
  if (v === "") return null;
  return /^\d+$/.test(v) ? Number(v) : Number.NaN;
}

export function newBlackout(timezone: string): BlackoutWindow {
  return { name: "", kind: "weekly", timezone, days: [4], start: "18:00", end: "23:00", starts_at: null, ends_at: null };
}

/** A datetime-local value ("2026-10-10T09:00", the browser's own zone) as an ISO instant. */
export function localInputToIso(value: string): string | null {
  if (!value) return null;
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
}

/** An ISO instant as a datetime-local value in the browser's zone. */
export function isoToLocalInput(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export function windowSummary(w: BlackoutWindow): string {
  if (w.kind === "once") {
    const f = (iso: string | null) => (iso ? new Date(iso).toLocaleString() : "?");
    return `${f(w.starts_at)} to ${f(w.ends_at)}`;
  }
  const days = [...w.days].sort().map((d) => DAY_LABELS[d]).join(", ");
  return `${days}, ${w.start} to ${w.end} (${w.timezone})`;
}

/**
 * The server answers a validation failure with a JSON list of {field, message}
 * (carried in an error string by the proxy). Turn it into one line per problem;
 * anything else is returned as it is.
 */
export function formatPolicyError(message: string): string[] {
  try {
    const parsed = JSON.parse(message) as unknown;
    if (Array.isArray(parsed)) {
      const lines = parsed.map((e) => {
        const item = e as { field?: string; message?: string };
        const text = String(item.message ?? "").replace(/^Value error, /, "");
        return item.field ? `${labelFor(item.field)}: ${text}` : text;
      }).filter(Boolean);
      if (lines.length) return lines;
    }
  } catch { /* not JSON */ }
  return [message];
}

function labelFor(field: string): string {
  const head = field.split(".")[0];
  const labels: Record<string, string> = {
    ip_allowlist: "Allowed networks",
    operator_session_max_hours: "Operator session limit",
    customer_session_max_hours: "Customer session limit",
    blackouts: "Blackout windows",
    global_exclusions: "Global exclusions",
    poc_duration_days: "POC length",
    support_contact: "Support contact",
  };
  const base = labels[head] ?? head;
  const rest = field.split(".").slice(1).join(" ");
  return rest ? `${base} (${rest})` : base;
}

/** Fill a new-customer plan draft from the organisation's defaults. */
export function applyCustomerDefaults<T extends { lockedSeverities: string[]; lockedFeatures: string[]; durationDays: number }>(
  draft: T, defaults: CustomerDefaults,
): T {
  return {
    ...draft,
    lockedSeverities: [...(defaults.poc_locked_severities ?? [])],
    lockedFeatures: [...(defaults.poc_locked_features ?? [])],
    durationDays: defaults.poc_duration_days,
  };
}
