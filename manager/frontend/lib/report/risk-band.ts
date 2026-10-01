/**
 * risk-band.ts — pure helpers that re-present a finding's existing triage signals
 * for the header risk-band. Nothing is invented or re-scored; absent signals
 * return a neutral placeholder so the band degrades quietly.
 */

export interface SlaCountdown {
  label: string;
  tone: "ok" | "warn" | "overdue" | "none";
}

function fmtDur(hours: number): string {
  if (hours < 24) return `${Math.round(hours)}h`;
  const d = hours / 24;
  return `${d % 1 === 0 ? d.toFixed(0) : d.toFixed(1)}d`;
}

export function formatSlaCountdown(
  sla?: { state?: string | null; hours_remaining?: number | null } | null,
): SlaCountdown {
  if (!sla) return { label: "—", tone: "none" };
  const h = sla.hours_remaining;
  if (typeof h === "number") {
    if (h <= 0) return { label: `Overdue ${fmtDur(Math.abs(h))}`, tone: "overdue" };
    return { label: `${fmtDur(h)} left`, tone: h <= 48 ? "warn" : "ok" };
  }
  const state = (sla.state ?? "").toLowerCase();
  if (!state) return { label: "—", tone: "none" };
  if (state.includes("overdue") || state.includes("breach")) return { label: "Overdue", tone: "overdue" };
  return { label: state.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()), tone: "ok" };
}

/** EPSS probability (0–1, or already a percent) → a compact percent label. */
export function epssPercent(epss?: number | null): string | null {
  if (typeof epss !== "number") return null;
  const pct = epss <= 1 ? epss * 100 : epss;
  return `${pct >= 10 ? Math.round(pct) : Math.round(pct * 10) / 10}%`;
}

/** The strongest recorded exploit signal, or null. */
export function exploitFlag(f: { exploit_validated?: boolean | null; exploitable?: boolean | null }): string | null {
  if (f.exploit_validated) return "Exploit validated";
  if (f.exploitable) return "Exploitable";
  return null;
}
