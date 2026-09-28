"use client";

/* Portal Settings → Plan & licence: the customer's own view of what the
   operator configured — plan, term, scan allowance and the licence key. */

import { Clipboard, FileBadge2, Loader2 } from "lucide-react";
import { useToast } from "../../hooks/useToast";
import { copyText } from "../../lib/clipboard";
import { PLAN_LABEL, fmtDate } from "../../lib/entitlements";
import { usePortalEntitlement } from "../../lib/portal-client";
import { PLAN_STYLES, PlanSummary } from "../customers/PlanPanel";

export function PlanLicenceSection() {
  const toast = useToast();
  const { data: e, isPending, error } = usePortalEntitlement();

  const rows: Array<[string, string]> = e ? [
    ["Plan", e.plan_type ? (e.plan_type === "poc" ? "Proof of concept (POC)" : "Licensed — full use") : "Not activated"],
    ["Starts", e.starts_at ? fmtDate(e.starts_at) : "—"],
    ["Ends", e.expires_at ? fmtDate(e.expires_at) : e.plan_type ? "No end date" : "—"],
    ["Scan allowance", e.scan_quota == null ? (e.plan_type ? "Unlimited" : "—") : `${e.scan_quota} scans`],
    ["Scans used", String(e.scans_used)],
    ["Scan intensity", "Stealth or Normal — aggressive scans are run by your security team"],
  ] : [];

  return (
    <div className="settings-panel animate-slide-in">
      <style>{PLAN_STYLES + STYLES}</style>
      <div className="pls-head">
        <span><FileBadge2 size={16} /></span>
        <div>
          <strong>Plan &amp; licence</strong>
          <p>What your security team has activated for this workspace.</p>
        </div>
      </div>

      {isPending ? (
        <div className="pls-muted"><Loader2 size={14} className="animate-spin" /> Loading your plan…</div>
      ) : error || !e ? (
        <div className="pls-muted">Your plan couldn’t be loaded. Try again in a moment.</div>
      ) : (
        <>
          <PlanSummary e={e} />
          <dl className="pls-grid">
            {rows.map(([k, v]) => (
              <div key={k}><dt>{k}</dt><dd>{v}</dd></div>
            ))}
          </dl>
          {e.license_key && (
            <div className="pls-key">
              <span>Licence key</span>
              <code>{e.license_key}</code>
              <button type="button" aria-label="Copy licence key" onClick={() => void copyText(e.license_key!)
                .then((ok) => (ok ? toast.success("Licence key copied") : toast.error("Copy failed")))}>
                <Clipboard size={13} />
              </button>
            </div>
          )}
          {e.plan_type && (
            <p className="pls-foot">
              To extend your {PLAN_LABEL[e.plan_type]}, add scans or move to a licence, contact your security team.
            </p>
          )}
        </>
      )}
    </div>
  );
}

const STYLES = `
.pls-head { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
.pls-head > span { width: 34px; height: 34px; border-radius: 9px; display: flex; align-items: center; justify-content: center; background: var(--accent-ghost); border: 0.5px solid var(--border-accent); color: var(--accent); }
.pls-head strong { color: var(--text-primary); font-size: 14px; }
.pls-head p { margin: 2px 0 0; color: var(--text-muted); font-size: 12px; }
.pls-muted { color: var(--text-muted); font-size: 12.5px; display: flex; align-items: center; gap: 8px; padding: 12px 0; }
.pls-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 10px; margin: 14px 0 0; }
.pls-grid > div { padding: 10px 12px; border-radius: 9px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); }
.pls-grid dt { color: var(--text-muted); font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.pls-grid dd { margin: 4px 0 0; color: var(--text-primary); font-size: 13px; font-weight: 600; line-height: 1.4; }
.pls-key { display: flex; align-items: center; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
.pls-key > span { color: var(--text-secondary); font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.pls-key code { font-family: var(--font-mono); color: var(--accent); font-weight: 700; letter-spacing: 0.5px; }
.pls-key button { width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; border-radius: 7px; background: var(--bg-surface); border: 0.5px solid var(--border-subtle); color: var(--text-secondary); cursor: pointer; }
.pls-foot { margin: 14px 0 0; color: var(--text-muted); font-size: 12px; }
`;
