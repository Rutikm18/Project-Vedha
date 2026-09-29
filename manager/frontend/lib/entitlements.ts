/* The customer's plan (POC / licensed) and portal scan quota — one shape for
   the operator Customers page and the customer portal. Mirrors
   app/schemas/portal.py::EntitlementOut; `null` quota / expiry = unlimited / none. */

export type PlanType = "poc" | "licensed";
export type ScanMode = "stealth" | "normal" | "aggressive" | "deep";
export type DeepRepeatPolicy = "distinct" | "repeat";

export const SCAN_MODES: ScanMode[] = ["stealth", "normal", "aggressive", "deep"];

/** One scan type's allowance. quota null = unlimited; enabled false = not in the plan. */
export interface ModeAllowance {
  enabled: boolean;
  quota: number | null;
  used: number;
  left: number | null;
  can_scan: boolean;
  reason: string | null;
}

export const MODE_META: Record<ScanMode, { label: string; hint: string; color: string }> = {
  stealth:    { label: "Stealth",    hint: "Low and slow, small port set",                 color: "#6ee7b7" },
  normal:     { label: "Normal",     hint: "Balanced default",                             color: "var(--accent)" },
  aggressive: { label: "Aggressive", hint: "~2,500 enterprise ports over the chosen scope", color: "var(--sev-high-color)" },
  deep:       { label: "Deep",       hint: "All 65,535 ports + full assessment, one asset", color: "var(--sev-critical-color)" },
};
export type EntitlementState = "unconfigured" | "not_started" | "expired" | "exhausted" | "active";

export interface Entitlement {
  state: EntitlementState;
  can_scan: boolean;
  reason: string | null;
  plan_type: PlanType | null;
  starts_at: string | null;
  expires_at: string | null;
  days_left: number | null;
  scan_quota: number | null;
  scans_used: number;
  scans_left: number | null;
  license_key: string | null;
  modes: Record<ScanMode, ModeAllowance>;
  deep_repeat_policy: DeepRepeatPolicy;
  deep_scanned_targets: string[];
}

export interface EntitlementAdmin extends Entitlement {
  configured: boolean;
  notes: string | null;
  updated_at: string | null;
}

export interface EntitlementConfig {
  plan_type: PlanType;
  starts_at?: string | null;
  duration_days?: number | null;
  expires_at?: string | null;
  scan_quota?: number | null;
  stealth_quota?: number | null;
  normal_quota?: number | null;
  aggressive_quota?: number | null;
  deep_quota?: number | null;
  deep_repeat_policy?: DeepRepeatPolicy;
  notes?: string | null;
}

export const PLAN_LABEL: Record<PlanType, string> = { poc: "POC", licensed: "Licensed" };

export const STATE_LABEL: Record<EntitlementState, string> = {
  unconfigured: "Not configured",
  not_started: "Not started",
  expired: "Expired",
  exhausted: "Quota used",
  active: "Active",
};

/** Token colour for a state — shared by the badge, the usage bar and banners. */
export function stateColor(state: EntitlementState): string {
  switch (state) {
    case "active": return "var(--nominal-color)";
    case "expired": return "var(--sev-critical-color)";
    case "exhausted": return "var(--sev-high-color)";
    case "not_started": return "var(--sev-medium-color)";
    default: return "var(--text-faint)";
  }
}

/** "∞" · "3 left" · "off" — compact per-type status. */
export function modeShort(m: ModeAllowance | undefined): string {
  if (!m || !m.enabled) return "off";
  if (m.left == null) return "∞";
  return `${m.left} left`;
}

/** Scan types the customer can run right now, in dial order. */
export function launchableModes(e: Entitlement | undefined | null): ScanMode[] {
  if (!e) return [];
  return SCAN_MODES.filter((m) => e.modes?.[m]?.can_scan);
}

/** "7 of 10 scans left" · "Unlimited scans". */
export function scansText(e: Pick<Entitlement, "scan_quota" | "scans_left" | "scans_used">): string {
  if (e.scan_quota == null) return `${e.scans_used} scan${e.scans_used === 1 ? "" : "s"} used`;
  const left = e.scans_left ?? 0;
  return `${left} of ${e.scan_quota} scan${e.scan_quota === 1 ? "" : "s"} left`;
}

/** "Ends in 9 days" · "Ends today" · "No end date" · "Ended 3 Sep 2026". */
export function daysText(e: Pick<Entitlement, "state" | "days_left" | "expires_at" | "starts_at">): string {
  if (e.state === "not_started" && e.starts_at) return `Starts ${fmtDate(e.starts_at)}`;
  if (e.expires_at == null) return "No end date";
  if (e.state === "expired") return `Ended ${fmtDate(e.expires_at)}`;
  const d = e.days_left ?? 0;
  if (d <= 1) return "Ends within a day";
  return `Ends in ${d} days`;
}

/** 0..1 share of the quota consumed; null when unlimited. */
export function usageRatio(e: Pick<Entitlement, "scan_quota" | "scans_used">): number | null {
  if (e.scan_quota == null) return null;
  if (e.scan_quota === 0) return 1;
  return Math.min(e.scans_used / e.scan_quota, 1);
}

/** Near the end — worth a warning banner before it bites. */
export function isRunningLow(e: Entitlement): boolean {
  if (e.state !== "active") return false;
  const lowDays = e.days_left != null && e.days_left <= 3;
  const lowTotal = e.scans_left != null && e.scans_left <= 1;
  // Low when every type still available is down to its last scan.
  const open = SCAN_MODES.map((m) => e.modes?.[m]).filter((m) => m?.can_scan);
  const lowModes = open.length > 0 && open.every((m) => m!.left != null && m!.left <= 1);
  return lowDays || lowTotal || lowModes;
}

export function fmtDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
}

/** `<input type="date">` value ↔ ISO instant at local midnight. */
export function dateInputValue(iso: string | null | undefined): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}
export function isoFromDateInput(value: string): string | null {
  if (!value) return null;
  const d = new Date(`${value}T00:00:00`);
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
}

/** FastAPI 422s arrive as a JSON array of issues; show the first message. */
export function friendlyError(e: unknown, fallback: string): string {
  const msg = e instanceof Error ? e.message : String(e ?? "");
  if (msg.startsWith("[")) {
    try {
      const first = JSON.parse(msg)[0];
      if (first?.msg) return String(first.msg).replace(/^Value error, /, "");
    } catch { /* fall through */ }
  }
  return msg || fallback;
}
