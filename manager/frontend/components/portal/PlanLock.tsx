"use client";

/* Portal plan locks — what the customer sees when their plan locks something.
   The server is the gate (app/services/portal_locks.py): locked findings never
   leave it and locked features answer 403. These components only explain it:
   a lock panel for a feature, and teaser rows that say how many findings of a
   locked severity exist — never their title, host, evidence or fix. */

import { useQuery } from "@tanstack/react-query";
import { Lock } from "lucide-react";

import {
  type LockFeature, type LockSeverity, type LockedTeaser, LOCK_FEATURES, teaserRows,
} from "../../lib/entitlements";
import { portalApi } from "../../lib/portal-client";

const SEVERITY: Record<LockSeverity, { label: string; color: string }> = {
  critical: { label: "Critical", color: "var(--sev-critical-color)" },
  high:     { label: "High",     color: "var(--sev-high-color)" },
  medium:   { label: "Medium",   color: "var(--sev-medium-color)" },
  low:      { label: "Low",      color: "var(--sev-low-color)" },
  info:     { label: "Info",     color: "var(--sev-info-color)" },
};

/** A locked feature: replaces the section's content. */
export function PlanLockPanel({ feature, title }: { feature: LockFeature; title?: string }) {
  const meta = LOCK_FEATURES.find((f) => f.id === feature)!;
  return (
    <section className="plk-panel" aria-labelledby={`plk-${feature}`}>
      <style>{STYLES}</style>
      <span className="plk-icon"><Lock size={18} aria-hidden /></span>
      <h3 id={`plk-${feature}`}>{title ?? meta.label}</h3>
      <p>{meta.lockedMessage}</p>
      <p className="plk-sub">Contact your security team to upgrade your plan.</p>
    </section>
  );
}

/** A short notice inside an open section (e.g. written reports withheld). */
export function PlanLockNotice({ children }: { children: React.ReactNode }) {
  return (
    <div className="plk-notice" role="note">
      <style>{STYLES}</style>
      <Lock size={13} aria-hidden />
      <span>{children}</span>
    </div>
  );
}

/** Teaser rows for locked findings: one row per locked severity that holds any. */
export function LockedFindingsTeaser() {
  const q = useQuery({
    queryKey: ["portal", "findings", "locked"],
    queryFn: () => portalApi<LockedTeaser>("/findings/locked"),
    staleTime: 30 * 1000,
  });
  const rows = teaserRows(q.data);
  if (!rows.length) return null;
  return (
    <section className="plk-teaser" aria-label="Locked findings">
      <style>{STYLES}</style>
      {rows.map(({ severity, count }) => (
        <div key={severity} className="plk-row">
          <span className="plk-sev" style={{ color: SEVERITY[severity].color }}>
            {SEVERITY[severity].label.toUpperCase()}
          </span>
          <span className="plk-what"><Lock size={12} aria-hidden />
            {count} locked finding{count === 1 ? "" : "s"}
          </span>
          <span className="plk-why">Available on a licensed plan</span>
        </div>
      ))}
      <p className="plk-foot">
        {q.data?.total} finding{q.data?.total === 1 ? " is" : "s are"} included in a licensed plan.
        Contact your security team to unlock {q.data?.total === 1 ? "it" : "them"}.
      </p>
    </section>
  );
}

const STYLES = `
.plk-panel { display: grid; justify-items: center; gap: 6px; text-align: center; padding: 34px 20px; border-radius: 14px; border: 0.5px dashed var(--border-default); background: var(--bg-panel); }
.plk-icon { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 11px; color: var(--sev-high-color); background: color-mix(in srgb, var(--sev-high-color) 10%, transparent); }
.plk-panel h3 { margin: 6px 0 0; font-size: 15px; color: var(--text-primary); }
.plk-panel p { margin: 0; max-width: 460px; color: var(--text-secondary); font-size: 12.5px; line-height: 1.55; }
.plk-panel .plk-sub { color: var(--text-muted); font-size: 11.5px; }
.plk-notice { display: flex; align-items: flex-start; gap: 8px; padding: 10px 12px; border-radius: 10px; border: 0.5px solid var(--border-subtle); background: var(--bg-panel); color: var(--text-secondary); font-size: 12px; line-height: 1.5; }
.plk-notice svg { flex-shrink: 0; margin-top: 2px; color: var(--sev-high-color); }
.plk-teaser { display: grid; border-radius: 12px; border: 0.5px solid var(--border-subtle); background: var(--bg-panel); overflow: hidden; }
.plk-row { display: grid; grid-template-columns: 92px minmax(0, 1fr) auto; align-items: center; gap: 12px; padding: 11px 14px; border-bottom: 0.5px solid var(--border-subtle); }
.plk-sev { font: 700 10.5px var(--font-mono); letter-spacing: 0.6px; }
.plk-what { display: inline-flex; align-items: center; gap: 7px; color: var(--text-secondary); font-size: 12.5px; }
.plk-why { color: var(--text-muted); font-size: 11.5px; }
.plk-foot { margin: 0; padding: 10px 14px; color: var(--text-muted); font-size: 11.5px; }
@media (max-width: 560px) { .plk-row { grid-template-columns: 1fr; gap: 3px; } }
`;
