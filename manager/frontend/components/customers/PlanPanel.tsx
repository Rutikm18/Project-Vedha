"use client";

/* Operator-side plan configuration for one customer: POC (a start date and a
   duration) or Licensed (a term and a licence key), plus the portal scan quota.
   The same form fields are reused by the "Add a customer" flow via
   <PlanFields>, so a new customer is created with a plan already in place. */

import { useEffect, useState } from "react";
import { CalendarClock, Clipboard, FlaskConical, Infinity as InfinityIcon, Loader2, Plus, RotateCcw, ShieldCheck } from "lucide-react";
import {
  type EntitlementAdmin, type EntitlementConfig, type PlanType,
  PLAN_LABEL, STATE_LABEL, dateInputValue, daysText, fmtDate, friendlyError,
  isoFromDateInput, scansText, stateColor, usageRatio,
} from "../../lib/entitlements";

export interface PlanDraft {
  plan: PlanType;
  start: string;           // yyyy-mm-dd
  durationDays: number;    // POC
  end: string;             // yyyy-mm-dd, licensed ("" = no end date)
  unlimited: boolean;
  quota: number;
  notes: string;
}

const POC_PRESETS = [7, 14, 30];

export function defaultDraft(): PlanDraft {
  return { plan: "poc", start: dateInputValue(new Date().toISOString()), durationDays: 14,
           end: "", unlimited: false, quota: 10, notes: "" };
}

export function draftFrom(e: EntitlementAdmin | null): PlanDraft {
  if (!e || !e.configured || !e.plan_type) return defaultDraft();
  const start = dateInputValue(e.starts_at) || defaultDraft().start;
  let durationDays = 14;
  if (e.plan_type === "poc" && e.starts_at && e.expires_at) {
    durationDays = Math.max(1, Math.round(
      (new Date(e.expires_at).getTime() - new Date(e.starts_at).getTime()) / 86_400_000));
  }
  return {
    plan: e.plan_type, start, durationDays,
    end: e.plan_type === "licensed" ? dateInputValue(e.expires_at) : "",
    unlimited: e.scan_quota == null, quota: e.scan_quota ?? 10, notes: e.notes ?? "",
  };
}

/** Client-side check so the operator sees a sentence, not a 422 array. */
export function draftError(d: PlanDraft): string | null {
  if (!d.start) return "Pick a start date.";
  if (d.plan === "poc" && (!Number.isFinite(d.durationDays) || d.durationDays < 1 || d.durationDays > 3650))
    return "POC duration must be between 1 and 3650 days.";
  if (d.plan === "licensed" && d.end && d.end <= d.start) return "The licence must end after it starts.";
  if (!d.unlimited && (!Number.isFinite(d.quota) || d.quota < 0 || d.quota > 100_000))
    return "Scan quota must be between 0 and 100,000.";
  return null;
}

export function configFromDraft(d: PlanDraft): EntitlementConfig {
  return {
    plan_type: d.plan,
    starts_at: isoFromDateInput(d.start),
    duration_days: d.plan === "poc" ? d.durationDays : null,
    expires_at: d.plan === "licensed" ? isoFromDateInput(d.end) : null,
    scan_quota: d.unlimited ? null : d.quota,
    notes: d.notes.trim() || null,
  };
}

export function PlanFields({ draft, onChange, compact = false }: {
  draft: PlanDraft; onChange: (d: PlanDraft) => void; compact?: boolean;
}) {
  const set = (patch: Partial<PlanDraft>) => onChange({ ...draft, ...patch });
  return (
    <div className="pln-fields" data-compact={compact}>
      <div className="pln-field pln-span">
        <span className="pln-label">Plan</span>
        <div className="pln-seg" role="radiogroup" aria-label="Plan type">
          {(["poc", "licensed"] as PlanType[]).map((p) => (
            <button key={p} type="button" role="radio" aria-checked={draft.plan === p}
              className="pln-seg-btn" data-on={draft.plan === p} onClick={() => set({ plan: p })}>
              {p === "poc" ? <FlaskConical size={13} /> : <ShieldCheck size={13} />}
              {p === "poc" ? "POC (trial)" : "Full use (licence)"}
            </button>
          ))}
        </div>
      </div>

      <label className="pln-field">
        <span className="pln-label">Starts</span>
        <input className="pln-input" type="date" value={draft.start}
          onChange={(e) => set({ start: e.target.value })} />
      </label>

      {draft.plan === "poc" ? (
        <div className="pln-field">
          <span className="pln-label">POC duration</span>
          <div className="pln-row">
            {POC_PRESETS.map((n) => (
              <button key={n} type="button" className="pln-chip" data-on={draft.durationDays === n}
                onClick={() => set({ durationDays: n })}>{n}d</button>
            ))}
            <input className="pln-input pln-num" type="number" min={1} max={3650} aria-label="Custom duration in days"
              value={draft.durationDays} onChange={(e) => set({ durationDays: Number(e.target.value) })} />
            <span className="pln-unit">days</span>
          </div>
        </div>
      ) : (
        <label className="pln-field">
          <span className="pln-label">Licence ends <span className="pln-opt">(blank = no end date)</span></span>
          <input className="pln-input" type="date" value={draft.end} min={draft.start}
            onChange={(e) => set({ end: e.target.value })} />
        </label>
      )}

      <div className="pln-field">
        <span className="pln-label">Portal scan quota</span>
        <div className="pln-row">
          <input className="pln-input pln-num" type="number" min={0} max={100000} aria-label="Scan quota"
            disabled={draft.unlimited} value={draft.unlimited ? "" : draft.quota}
            placeholder={draft.unlimited ? "∞" : undefined}
            onChange={(e) => set({ quota: Number(e.target.value) })} />
          <span className="pln-unit">scans</span>
          <label className="pln-check">
            <input type="checkbox" checked={draft.unlimited} onChange={(e) => set({ unlimited: e.target.checked })} />
            <InfinityIcon size={13} /> Unlimited
          </label>
        </div>
      </div>

      {!compact && (
        <label className="pln-field pln-span">
          <span className="pln-label">Notes <span className="pln-opt">(internal)</span></span>
          <input className="pln-input" maxLength={2000} placeholder="e.g. POC for Q4 renewal, contact: CISO"
            value={draft.notes} onChange={(e) => set({ notes: e.target.value })} />
        </label>
      )}
    </div>
  );
}

/** Usage summary: state badge, scans bar, days left. */
export function PlanSummary({ e }: { e: EntitlementAdmin }) {
  const ratio = usageRatio(e);
  const color = stateColor(e.state);
  return (
    <div className="pln-summary">
      <div className="pln-summary-top">
        <span className="pln-badge" style={{ color }}><span className="pln-dot" />{STATE_LABEL[e.state]}</span>
        {e.plan_type && <span className="pln-plan">{PLAN_LABEL[e.plan_type]}</span>}
        <span className="pln-days"><CalendarClock size={12} /> {daysText(e)}</span>
      </div>
      <div className="pln-usage">
        <span>{scansText(e)}</span>
        {ratio != null && (
          <span className="pln-bar" aria-hidden="true">
            <span className="pln-bar-fill" style={{ width: `${Math.round(ratio * 100)}%`, background: color }} />
          </span>
        )}
      </div>
      {e.reason && <div className="pln-reason">{e.reason}</div>}
    </div>
  );
}

export function PlanPanel({ engagementId, onSaved, onCopy, api }: {
  engagementId: string;
  onSaved: (e: EntitlementAdmin) => void;
  onCopy: (text: string) => void;
  api: <T>(path: string, init?: RequestInit) => Promise<T>;
}) {
  const base = `/api/engagements/${engagementId}/customer-access/entitlement`;
  const [ent, setEnt] = useState<EntitlementAdmin | null>(null);
  const [draft, setDraft] = useState<PlanDraft>(defaultDraft);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let live = true;
    api<EntitlementAdmin>(base)
      .then((e) => { if (live) { setEnt(e); setDraft(draftFrom(e)); } })
      .catch((e) => { if (live) setError(friendlyError(e, "Couldn't load the plan")); })
      .finally(() => { if (live) setLoading(false); });
    return () => { live = false; };
  }, [api, base]);

  async function run(label: string, path: string, method: string, body: unknown) {
    setSaving(label);
    setError(null);
    try {
      const e = await api<EntitlementAdmin>(path, { method, body: JSON.stringify(body) });
      setEnt(e);
      setDraft(draftFrom(e));
      onSaved(e);
    } catch (e) {
      setError(friendlyError(e, "Save failed"));
    } finally {
      setSaving(null);
    }
  }

  if (loading) return <div className="pln-panel pln-muted"><Loader2 size={14} className="animate-spin" /> Loading plan…</div>;

  const invalid = draftError(draft);
  return (
    <div className="pln-panel">
      {ent?.configured && <PlanSummary e={ent} />}

      <PlanFields draft={draft} onChange={setDraft} />

      {ent?.license_key && (
        <div className="pln-key">
          <span className="pln-label">Licence key</span>
          <code className="pln-mono">{ent.license_key}</code>
          <button type="button" className="pln-icon" aria-label="Copy licence key" onClick={() => onCopy(ent.license_key!)}>
            <Clipboard size={12} />
          </button>
          {ent.starts_at && <span className="pln-unit">issued for the term from {fmtDate(ent.starts_at)}</span>}
        </div>
      )}

      {(error || invalid) && <div className="pln-error" role="alert">{error ?? invalid}</div>}

      <div className="pln-actions">
        <button type="button" className="pln-save" disabled={!!saving || !!invalid}
          onClick={() => void run("save", base, "PUT", configFromDraft(draft))}>
          {saving === "save" ? <Loader2 size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
          {ent?.configured ? "Save plan" : "Activate plan"}
        </button>
        {ent?.configured && (
          <>
            {ent.scan_quota != null && (
              <button type="button" className="pln-mini" disabled={!!saving}
                onClick={() => void run("scans", `${base}/adjust`, "POST", { add_scans: 5 })}>
                <Plus size={12} /> 5 scans
              </button>
            )}
            {ent.expires_at != null && (
              <button type="button" className="pln-mini" disabled={!!saving}
                onClick={() => void run("days", `${base}/adjust`, "POST", { extend_days: 7 })}>
                <Plus size={12} /> 7 days
              </button>
            )}
            <button type="button" className="pln-mini" disabled={!!saving || ent.scans_used === 0}
              onClick={() => void run("reset", `${base}/adjust`, "POST", { reset_usage: true })}>
              <RotateCcw size={12} /> Reset usage
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export const PLAN_STYLES = `
.pln-panel { display: grid; gap: 14px; padding: 14px 16px 16px; background: var(--bg-surface); border-top: 0.5px solid var(--border-subtle); }
.pln-muted { color: var(--text-muted); font-size: 12px; display: flex; align-items: center; gap: 8px; }
.pln-fields { display: grid; grid-template-columns: minmax(150px, 190px) minmax(280px, auto) minmax(240px, 1fr); gap: 14px 18px; align-items: start; }
.pln-span { grid-column: 1 / -1; }
.pln-field { display: flex; flex-direction: column; gap: 6px; min-width: 0; }
.pln-label { color: var(--text-secondary); font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.pln-opt { text-transform: none; letter-spacing: 0; font-weight: 400; color: var(--text-muted); }
.pln-input { width: 100%; min-height: 40px; padding: 8px 11px; border-radius: 8px; border: 0.5px solid var(--border-default); background: var(--bg-panel); color: var(--text-primary); font-size: 12.5px; outline: none; box-sizing: border-box; color-scheme: light dark; }
.pln-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-ghost); }
.pln-input:disabled { opacity: 0.55; }
.pln-num { width: 76px; font-family: var(--font-mono); }
.pln-row { display: flex; align-items: center; gap: 6px; min-height: 40px; }
.pln-unit { color: var(--text-muted); font-size: 11px; }
.pln-seg { display: inline-flex; padding: 3px; gap: 3px; border-radius: 10px; background: var(--bg-panel); border: 0.5px solid var(--border-subtle); width: fit-content; }
.pln-seg-btn { display: inline-flex; align-items: center; gap: 6px; min-height: 34px; padding: 0 14px; border-radius: 8px; border: none; background: transparent; color: var(--text-secondary); font-size: 12px; font-weight: 600; cursor: pointer; }
.pln-seg-btn[data-on="true"] { background: var(--accent-ghost); color: var(--accent); box-shadow: inset 0 0 0 0.5px var(--border-accent); }
.pln-chip { min-height: 40px; padding: 0 11px; border-radius: 8px; border: 0.5px solid var(--border-subtle); background: var(--bg-panel); color: var(--text-secondary); font: 600 11.5px var(--font-mono); cursor: pointer; }
.pln-chip[data-on="true"] { color: var(--accent); border-color: var(--border-accent); background: var(--accent-ghost); }
.pln-check { display: inline-flex; align-items: center; gap: 5px; color: var(--text-secondary); font-size: 11.5px; cursor: pointer; margin-left: 4px; }
.pln-summary { display: grid; gap: 8px; padding: 12px 14px; border-radius: 10px; background: var(--bg-panel); border: 0.5px solid var(--border-subtle); }
.pln-summary-top { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.pln-badge { display: inline-flex; align-items: center; gap: 6px; font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; }
.pln-dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.pln-plan { font: 700 10px var(--font-mono); color: var(--text-secondary); border: 0.5px solid var(--border-subtle); border-radius: 5px; padding: 1px 6px; }
.pln-days { display: inline-flex; align-items: center; gap: 5px; color: var(--text-muted); font-size: 11.5px; margin-left: auto; }
.pln-usage { display: flex; align-items: center; gap: 12px; color: var(--text-primary); font-size: 12.5px; font-weight: 600; }
.pln-bar { flex: 1; height: 6px; border-radius: 99px; background: var(--border-subtle); overflow: hidden; max-width: 320px; }
.pln-bar-fill { display: block; height: 100%; border-radius: inherit; transition: width var(--dur-fast, .2s) ease; }
.pln-reason { color: var(--text-muted); font-size: 11.5px; line-height: 1.45; }
.pln-key { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.pln-mono { font-family: var(--font-mono); color: var(--accent); font-weight: 700; letter-spacing: 0.5px; }
.pln-icon { width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; border-radius: 7px; background: var(--bg-panel); border: 0.5px solid var(--border-subtle); color: var(--text-secondary); cursor: pointer; }
.pln-icon:hover { color: var(--accent); border-color: var(--border-accent); }
.pln-error { color: var(--sev-high-color); font-size: 12px; }
.pln-actions { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.pln-save { min-height: 38px; padding: 0 16px; display: inline-flex; align-items: center; gap: 7px; border: none; border-radius: 9px; cursor: pointer; font-size: 12.5px; font-weight: 700; color: #fff; background: var(--accent); }
.pln-save:disabled { opacity: 0.45; cursor: not-allowed; }
.pln-mini { min-height: 32px; display: inline-flex; align-items: center; gap: 5px; padding: 0 10px; border-radius: 8px; background: var(--bg-panel); border: 0.5px solid var(--border-subtle); color: var(--text-secondary); font-size: 11.5px; cursor: pointer; }
.pln-mini:hover:not(:disabled) { color: var(--accent); border-color: var(--border-accent); }
.pln-mini:disabled { opacity: 0.4; cursor: not-allowed; }
@media (max-width: 820px) {
  .pln-fields { grid-template-columns: 1fr; }
  .pln-row { flex-wrap: wrap; }
  .pln-days { margin-left: 0; }
}
`;
