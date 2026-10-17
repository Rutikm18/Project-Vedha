"use client";

/* One line at the top of every portal page: the customer's plan, scans left
   and days left. It escalates from a quiet status line to a warning (running
   low) to an alert (expired, used up, or not activated) — the alert carries
   the same sentence the API returns when it refuses a scan, so the customer
   learns why before they try. */

import { AlertTriangle, CalendarClock, FlaskConical, ShieldCheck } from "lucide-react";
import { usePortalEntitlement } from "../../lib/portal-client";
import {
  MODE_META, PLAN_LABEL, STATE_LABEL, daysText, isRunningLow, modeShort, modeSummary, stateColor,
} from "../../lib/entitlements";

export function PlanStrip() {
  const { data: e } = usePortalEntitlement();
  if (!e) return null;

  const summary = modeSummary(e);
  const blocked = !e.can_scan;
  const low = isRunningLow(e);
  const tone = blocked ? stateColor(e.state) : low ? "var(--sev-medium-color)" : "var(--accent)";

  return (
    <div className="pst" data-tone={blocked ? "alert" : low ? "warn" : "ok"} role={blocked ? "alert" : "status"}
      style={{ ["--pst-tone" as string]: tone }}>
      <style>{STYLES}</style>
      <span className="pst-plan">
        {e.plan_type === "poc" ? <FlaskConical size={13} /> : <ShieldCheck size={13} />}
        {e.plan_type ? PLAN_LABEL[e.plan_type] : "No plan"}
        {e.state !== "active" && <em>{STATE_LABEL[e.state]}</em>}
      </span>
      {e.state !== "unconfigured" && (
        <>
          {/* Everything open and uncapped reads as one phrase; otherwise one chip per scan type in
              the plan (types not included are omitted). */}
          {summary.kind === "unlimited" ? (
            <span className="pst-mode" title={summary.names}>
              <ShieldCheck size={12} aria-hidden /> {summary.label}
            </span>
          ) : summary.modes.map((m) => (
            <span key={m} className="pst-mode" data-empty={!e.modes[m].can_scan}
              title={e.modes[m].reason ?? `${MODE_META[m].label}: ${modeShort(e.modes[m])}`}>
              <i style={{ background: MODE_META[m].color }} aria-hidden />
              {MODE_META[m].label} <b>{modeShort(e.modes[m])}</b>
            </span>
          ))}
          {e.scan_quota != null && (
            <span className="pst-mode">Overall <b>{e.scans_left ?? 0} of {e.scan_quota} left</b></span>
          )}
          <span className="pst-item"><CalendarClock size={13} /> {daysText(e)}</span>
        </>
      )}
      {(blocked || low) && (
        <span className="pst-msg">
          <AlertTriangle size={13} />
          {blocked ? e.reason : "Running low — contact your security team to extend your plan."}
        </span>
      )}
    </div>
  );
}

const STYLES = `
.pst { display: flex; align-items: center; gap: 8px 16px; flex-wrap: wrap; margin-bottom: 14px; padding: 9px 14px;
  border-radius: 10px; font-size: 12px; color: var(--text-secondary);
  background: color-mix(in srgb, var(--pst-tone) 6%, var(--bg-panel));
  border: 0.5px solid color-mix(in srgb, var(--pst-tone) 30%, var(--border-subtle)); }
.pst-plan { display: inline-flex; align-items: center; gap: 6px; font-weight: 700; color: var(--pst-tone); }
.pst-plan em { font-style: normal; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; padding: 1px 6px;
  border-radius: 5px; background: color-mix(in srgb, var(--pst-tone) 14%, transparent); }
.pst-item { display: inline-flex; align-items: center; gap: 6px; color: var(--text-primary); font-weight: 600; }
.pst-item svg { color: var(--text-muted); }
.pst-mode { display: inline-flex; align-items: center; gap: 6px; padding: 2px 9px; border-radius: 99px; background: var(--bg-panel); border: 0.5px solid var(--border-subtle); color: var(--text-secondary); font-size: 11.5px; }
.pst-mode i { width: 7px; height: 7px; border-radius: 50%; }
.pst-mode b { color: var(--text-primary); }
.pst-mode[data-empty="true"] b { color: var(--sev-high-color); }
.pst-msg { display: inline-flex; align-items: center; gap: 6px; color: var(--pst-tone); font-weight: 600; flex-basis: 100%; }
.pst[data-tone="ok"] .pst-msg { display: none; }
@media (min-width: 1100px) { .pst-msg { flex-basis: auto; margin-left: auto; } }
`;
