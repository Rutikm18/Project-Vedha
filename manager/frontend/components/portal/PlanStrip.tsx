"use client";

/* One line at the top of every portal page: the customer's plan, scans left
   and days left. It escalates from a quiet status line to a warning (running
   low) to an alert (expired, used up, or not activated) — the alert carries
   the same sentence the API returns when it refuses a scan, so the customer
   learns why before they try. */

import { AlertTriangle, CalendarClock, FlaskConical, Radar, ShieldCheck } from "lucide-react";
import { usePortalEntitlement } from "../../lib/portal-client";
import {
  PLAN_LABEL, STATE_LABEL, daysText, isRunningLow, scansText, stateColor, usageRatio,
} from "../../lib/entitlements";

export function PlanStrip() {
  const { data: e } = usePortalEntitlement();
  if (!e) return null;

  const blocked = !e.can_scan;
  const low = isRunningLow(e);
  const tone = blocked ? stateColor(e.state) : low ? "var(--sev-medium-color)" : "var(--accent)";
  const ratio = usageRatio(e);

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
          <span className="pst-item">
            <Radar size={13} /> {scansText(e)}
            {ratio != null && (
              <span className="pst-bar" aria-hidden="true">
                <span style={{ width: `${Math.round((1 - ratio) * 100)}%` }} />
              </span>
            )}
          </span>
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
.pst-bar { width: 64px; height: 5px; border-radius: 99px; background: var(--border-subtle); overflow: hidden; }
.pst-bar span { display: block; height: 100%; background: var(--pst-tone); border-radius: inherit; }
.pst-msg { display: inline-flex; align-items: center; gap: 6px; color: var(--pst-tone); font-weight: 600; flex-basis: 100%; }
.pst[data-tone="ok"] .pst-msg { display: none; }
@media (min-width: 1100px) { .pst-msg { flex-basis: auto; margin-left: auto; } }
`;
