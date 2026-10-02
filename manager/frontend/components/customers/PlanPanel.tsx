"use client";

/* Operator-side plan configuration for one customer: POC (a start date and a
   duration) or Licensed (a term and a licence key), plus the portal scan
   allowances — one per scan type (Stealth / Normal / Aggressive / Deep) and an
   optional overall cap. Deep = every port on exactly ONE asset, with a repeat
   policy. The same fields are reused by the "Add a customer" flow via
   <PlanFields>, so a new customer is created with a plan already in place. */

import { useEffect, useState } from "react";
import {
  CalendarClock, Clipboard, Crosshair, FlaskConical, Loader2, Lock, Plus, RotateCcw, ShieldCheck,
} from "lucide-react";
import {
  type DeepRepeatPolicy, type Entitlement, type EntitlementAdmin, type EntitlementConfig,
  type LockFeature, type LockSeverity, type PlanType, type ScanMode,
  LOCK_FEATURES, LOCKABLE_SEVERITIES, MODE_META, PLAN_LABEL, SCAN_MODES, STATE_LABEL,
  dateInputValue, daysText, fmtDate,
  friendlyError, isoFromDateInput, modeShort, stateColor,
} from "../../lib/entitlements";

type Allowance = "off" | "limited" | "unlimited";

export interface PlanDraft {
  plan: PlanType;
  start: string;           // yyyy-mm-dd
  durationDays: number;    // POC
  end: string;             // yyyy-mm-dd, licensed ("" = no end date)
  modes: Record<ScanMode, { allowance: Allowance; quota: number }>;
  totalCap: number | null; // null = no overall cap
  deepPolicy: DeepRepeatPolicy;
  notes: string;
  /** Portal locks: severities shown only as teaser rows, features that answer
   *  "available on a licensed plan". Enforced server-side. */
  lockedSeverities: LockSeverity[];
  lockedFeatures: LockFeature[];
}

/** A new POC starts with Critical + High locked; a new licence with nothing. */
function defaultLocks(plan: PlanType): LockSeverity[] {
  return plan === "poc" ? ["critical", "high"] : [];
}

function inOrder<T extends string>(chosen: T[], order: readonly T[]): T[] {
  return order.filter((v) => chosen.includes(v));
}

const POC_PRESETS = [7, 14, 30];

export function defaultDraft(): PlanDraft {
  return {
    plan: "poc", start: dateInputValue(new Date().toISOString()), durationDays: 14, end: "",
    // Light scans unlimited, a bounded normal allowance; the heavy types are
    // opt-in — they load the customer's network, so off until you choose them.
    modes: {
      stealth:    { allowance: "unlimited", quota: 10 },
      normal:     { allowance: "limited",   quota: 10 },
      aggressive: { allowance: "off",       quota: 2 },
      deep:       { allowance: "off",       quota: 1 },
    },
    totalCap: null, deepPolicy: "distinct", notes: "",
    lockedSeverities: defaultLocks("poc"), lockedFeatures: [],
  };
}

function allowanceOf(quota: number | null | undefined): Allowance {
  if (quota == null) return "unlimited";
  return quota > 0 ? "limited" : "off";
}

export function draftFrom(e: EntitlementAdmin | null): PlanDraft {
  const d = defaultDraft();
  if (!e || !e.configured || !e.plan_type) return d;
  let durationDays = 14;
  if (e.plan_type === "poc" && e.starts_at && e.expires_at) {
    durationDays = Math.max(1, Math.round(
      (new Date(e.expires_at).getTime() - new Date(e.starts_at).getTime()) / 86_400_000));
  }
  const modes = { ...d.modes };
  for (const m of SCAN_MODES) {
    const q = e.modes?.[m]?.quota;
    modes[m] = { allowance: allowanceOf(q), quota: q && q > 0 ? q : d.modes[m].quota };
  }
  return {
    plan: e.plan_type, start: dateInputValue(e.starts_at) || d.start, durationDays,
    end: e.plan_type === "licensed" ? dateInputValue(e.expires_at) : "",
    modes, totalCap: e.scan_quota ?? null, deepPolicy: e.deep_repeat_policy ?? "distinct",
    notes: e.notes ?? "",
    // An existing customer keeps exactly the locks it has — never re-locked by default.
    lockedSeverities: e.locked_severities ?? [], lockedFeatures: e.locked_features ?? [],
  };
}

/** Client-side check so the operator sees a sentence, not a 422 array. */
export function draftError(d: PlanDraft): string | null {
  if (!d.start) return "Pick a start date.";
  if (d.plan === "poc" && (!Number.isFinite(d.durationDays) || d.durationDays < 1 || d.durationDays > 3650))
    return "POC duration must be between 1 and 3650 days.";
  if (d.plan === "licensed" && d.end && d.end <= d.start) return "The licence must end after it starts.";
  for (const m of SCAN_MODES) {
    const a = d.modes[m];
    if (a.allowance === "limited" && (!Number.isInteger(a.quota) || a.quota < 1 || a.quota > 100_000))
      return `${MODE_META[m].label}: enter between 1 and 100,000 scans (or choose Off / Unlimited).`;
  }
  if (SCAN_MODES.every((m) => d.modes[m].allowance === "off"))
    return "Turn on at least one scan type.";
  if (d.totalCap != null && (!Number.isInteger(d.totalCap) || d.totalCap < 1 || d.totalCap > 100_000))
    return "The overall cap must be between 1 and 100,000.";
  return null;
}

export function configFromDraft(d: PlanDraft): EntitlementConfig {
  const q = (m: ScanMode) => {
    const a = d.modes[m];
    return a.allowance === "unlimited" ? null : a.allowance === "off" ? 0 : a.quota;
  };
  return {
    plan_type: d.plan,
    starts_at: isoFromDateInput(d.start),
    duration_days: d.plan === "poc" ? d.durationDays : null,
    expires_at: d.plan === "licensed" ? isoFromDateInput(d.end) : null,
    scan_quota: d.totalCap,
    stealth_quota: q("stealth"),
    normal_quota: q("normal"),
    aggressive_quota: q("aggressive"),
    deep_quota: q("deep"),
    deep_repeat_policy: d.deepPolicy,
    notes: d.notes.trim() || null,
    locked_severities: inOrder(d.lockedSeverities, LOCKABLE_SEVERITIES),
    locked_features: inOrder(d.lockedFeatures, LOCK_FEATURES.map((f) => f.id)),
  };
}

function AllowanceTable({ draft, onChange, usage, onTopUp, busy }: {
  draft: PlanDraft;
  onChange: (d: PlanDraft) => void;
  usage?: Entitlement | null;
  onTopUp?: (mode: ScanMode) => void;
  busy?: boolean;
}) {
  const setMode = (m: ScanMode, patch: Partial<PlanDraft["modes"][ScanMode]>) =>
    onChange({ ...draft, modes: { ...draft.modes, [m]: { ...draft.modes[m], ...patch } } });
  return (
    <div className="pln-field pln-span">
      <span className="pln-label">Scan allowances <span className="pln-opt">(what the customer may launch from the portal)</span></span>
      <div className="pln-table" role="table" aria-label="Scan allowances">
        {SCAN_MODES.map((m) => {
          const a = draft.modes[m];
          const live = usage?.modes?.[m];
          return (
            <div key={m} className="pln-trow" role="row" data-off={a.allowance === "off"}>
              <span className="pln-mode" role="cell">
                <i style={{ background: MODE_META[m].color }} aria-hidden />
                <span>
                  <strong>{MODE_META[m].label}{m === "deep" && <Crosshair size={11} />}</strong>
                  <small>{MODE_META[m].hint}</small>
                </span>
              </span>
              <span className="pln-seg pln-seg-sm" role="radiogroup" aria-label={`${MODE_META[m].label} allowance`}>
                {(["off", "limited", "unlimited"] as Allowance[]).map((opt) => (
                  <button key={opt} type="button" role="radio" aria-checked={a.allowance === opt}
                    className="pln-seg-btn" data-on={a.allowance === opt}
                    onClick={() => setMode(m, { allowance: opt })}>
                    {opt === "off" ? "Off" : opt === "limited" ? "Limited" : "Unlimited"}
                  </button>
                ))}
              </span>
              <span className="pln-row" role="cell">
                {a.allowance === "limited" ? (
                  <>
                    <input className="pln-input pln-num" type="number" min={1} max={100000}
                      aria-label={`${MODE_META[m].label} scan limit`} value={a.quota}
                      onChange={(e) => setMode(m, { quota: Number(e.target.value) })} />
                    <span className="pln-unit">scans</span>
                  </>
                ) : (
                  <span className="pln-unit">{a.allowance === "off" ? "Not included" : "No limit"}</span>
                )}
              </span>
              <span className="pln-used" role="cell">
                {live && live.enabled ? (
                  <>
                    <span>{live.used} used · {modeShort(live)}</span>
                    {onTopUp && live.quota != null && (
                      <button type="button" className="pln-mini pln-mini-xs" disabled={busy}
                        aria-label={`Add 5 ${MODE_META[m].label} scans`} onClick={() => onTopUp(m)}>
                        <Plus size={11} /> 5
                      </button>
                    )}
                  </>
                ) : <span className="pln-faint">—</span>}
              </span>
            </div>
          );
        })}
      </div>

      {draft.modes.deep.allowance !== "off" && (
        <div className="pln-deep">
          <strong><Crosshair size={12} /> Deep scan covers exactly one asset per scan.</strong>
          <div className="pln-seg" role="radiogroup" aria-label="Deep scan repeat policy">
            {([
              ["distinct", "Each deep scan must be a different asset"],
              ["repeat", "The same asset may be deep-scanned again"],
            ] as [DeepRepeatPolicy, string][]).map(([v, label]) => (
              <button key={v} type="button" role="radio" aria-checked={draft.deepPolicy === v}
                className="pln-seg-btn" data-on={draft.deepPolicy === v}
                onClick={() => onChange({ ...draft, deepPolicy: v })}>{label}</button>
            ))}
          </div>
        </div>
      )}

      <label className="pln-check pln-cap">
        <input type="checkbox" checked={draft.totalCap != null}
          onChange={(e) => onChange({ ...draft, totalCap: e.target.checked ? 20 : null })} />
        Also cap the total across all types
        {draft.totalCap != null && (
          <>
            <input className="pln-input pln-num" type="number" min={1} max={100000} aria-label="Overall scan cap"
              value={draft.totalCap} onChange={(e) => onChange({ ...draft, totalCap: Number(e.target.value) })} />
            <span className="pln-unit">scans</span>
          </>
        )}
      </label>
    </div>
  );
}

export function PlanFields({ draft, onChange, compact = false, usage, onTopUp, busy }: {
  draft: PlanDraft; onChange: (d: PlanDraft) => void; compact?: boolean;
  usage?: Entitlement | null; onTopUp?: (mode: ScanMode) => void; busy?: boolean;
}) {
  const set = (patch: Partial<PlanDraft>) => onChange({ ...draft, ...patch });
  return (
    <div className="pln-fields">
      <div className="pln-field pln-span">
        <span className="pln-label">Plan</span>
        <div className="pln-seg" role="radiogroup" aria-label="Plan type">
          {(["poc", "licensed"] as PlanType[]).map((p) => (
            <button key={p} type="button" role="radio" aria-checked={draft.plan === p}
              className="pln-seg-btn" data-on={draft.plan === p}
              // A customer without a saved plan takes that plan type's default
              // locks; an existing customer's locks never change silently.
              onClick={() => set(usage ? { plan: p } : { plan: p, lockedSeverities: defaultLocks(p) })}>
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
        <div className="pln-field pln-span2">
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
        <label className="pln-field pln-span2">
          <span className="pln-label">Licence ends <span className="pln-opt">(blank = no end date)</span></span>
          <input className="pln-input pln-date" type="date" value={draft.end} min={draft.start}
            onChange={(e) => set({ end: e.target.value })} />
        </label>
      )}

      <AllowanceTable draft={draft} onChange={onChange} usage={usage} onTopUp={onTopUp} busy={busy} />

      <PortalAccess draft={draft} onChange={onChange} />

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

const SEVERITY_LABEL: Record<LockSeverity, string> = {
  critical: "Critical", high: "High", medium: "Medium", low: "Low", info: "Info",
};

/** What the customer can open in the portal. Locked severities appear only as
 *  "available on a licensed plan" teaser rows; locked features show a lock
 *  panel. Takes effect on the customer's next request; change it at any time. */
function PortalAccess({ draft, onChange }: { draft: PlanDraft; onChange: (d: PlanDraft) => void }) {
  const toggle = <T extends string>(list: T[], value: T): T[] =>
    list.includes(value) ? list.filter((v) => v !== value) : [...list, value];
  return (
    <div className="pln-field pln-span pln-access">
      <span className="pln-label">Portal access</span>
      <p className="pln-access-hint">
        Locked findings show only their severity and a lock; their details never reach the customer.
        Changes apply on the customer&apos;s next page load.
      </p>
      <div className="pln-access-group" role="group" aria-label="Locked finding severities">
        <span className="pln-access-title"><Lock size={12} aria-hidden /> Lock findings of severity</span>
        <div className="pln-row pln-wrap">
          {LOCKABLE_SEVERITIES.map((sev) => (
            <label key={sev} className="pln-chip pln-lock-chip" data-on={draft.lockedSeverities.includes(sev)}>
              <input type="checkbox" checked={draft.lockedSeverities.includes(sev)}
                onChange={() => onChange({ ...draft, lockedSeverities: toggle(draft.lockedSeverities, sev) })} />
              {SEVERITY_LABEL[sev]}
            </label>
          ))}
        </div>
      </div>
      <div className="pln-access-group" role="group" aria-label="Locked portal features">
        <span className="pln-access-title"><Lock size={12} aria-hidden /> Lock features</span>
        <div className="pln-access-features">
          {LOCK_FEATURES.map((f) => (
            <label key={f.id} className="pln-feature" data-on={draft.lockedFeatures.includes(f.id)}>
              <input type="checkbox" checked={draft.lockedFeatures.includes(f.id)}
                onChange={() => onChange({ ...draft, lockedFeatures: toggle(draft.lockedFeatures, f.id) })} />
              <span><strong>{f.label}</strong><small>{f.description}</small></span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
}

/** Plan status + one chip per scan type + the assets already deep-scanned. */
export function PlanSummary({ e }: { e: Entitlement }) {
  const color = stateColor(e.state);
  return (
    <div className="pln-summary">
      <div className="pln-summary-top">
        <span className="pln-badge" style={{ color }}><span className="pln-dot" />{STATE_LABEL[e.state]}</span>
        {e.plan_type && <span className="pln-plan">{PLAN_LABEL[e.plan_type]}</span>}
        <span className="pln-days"><CalendarClock size={12} /> {daysText(e)}</span>
      </div>
      <div className="pln-chips">
        {SCAN_MODES.map((m) => {
          const a = e.modes?.[m];
          return (
            <span key={m} className="pln-mchip" data-off={!a?.enabled} data-empty={!!a?.enabled && !a.can_scan}
              title={a?.reason ?? undefined}>
              <i style={{ background: MODE_META[m].color }} aria-hidden />
              {MODE_META[m].label} <b>{modeShort(a)}</b>
            </span>
          );
        })}
        {e.scan_quota != null && <span className="pln-mchip">Overall <b>{e.scans_left ?? 0} of {e.scan_quota} left</b></span>}
      </div>
      {e.modes?.deep?.enabled && (
        <div className="pln-reason">
          Deep scan · {e.deep_repeat_policy === "distinct" ? "a different asset each time" : "repeats allowed"}
          {e.deep_scanned_targets.length > 0 && <> · done: {e.deep_scanned_targets.map((t) => t.replace(/\/(32|128)$/, "")).join(", ")}</>}
        </div>
      )}
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

      <PlanFields draft={draft} onChange={setDraft} usage={ent?.configured ? ent : null} busy={!!saving}
        onTopUp={(m) => void run(`top-${m}`, `${base}/adjust`, "POST", { add_scans: 5, mode: m })} />

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
            {ent.expires_at != null && (
              <button type="button" className="pln-mini" disabled={!!saving}
                onClick={() => void run("days", `${base}/adjust`, "POST", { extend_days: 7 })}>
                <Plus size={12} /> 7 days
              </button>
            )}
            <button type="button" className="pln-mini" disabled={!!saving || ent.scans_used === 0}
              title="Zero every counter and clear the deep-scan asset history"
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
.pln-fields { display: grid; grid-template-columns: minmax(150px, 190px) minmax(0, 1fr); gap: 14px 18px; align-items: start; }
.pln-span { grid-column: 1 / -1; }
.pln-field { display: flex; flex-direction: column; gap: 6px; min-width: 0; }
.pln-label { color: var(--text-secondary); font-size: 10.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.pln-opt { text-transform: none; letter-spacing: 0; font-weight: 400; color: var(--text-muted); }
.pln-input { width: 100%; min-height: 40px; padding: 8px 11px; border-radius: 8px; border: 0.5px solid var(--border-default); background: var(--bg-panel); color: var(--text-primary); font-size: 12.5px; outline: none; box-sizing: border-box; color-scheme: light dark; }
.pln-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-ghost); }
.pln-input:disabled { opacity: 0.55; }
.pln-num { width: 76px; font-family: var(--font-mono); }
.pln-date { max-width: 220px; }
.pln-row { display: flex; align-items: center; gap: 6px; min-height: 40px; }
.pln-wrap { flex-wrap: wrap; }
.pln-access { gap: 10px; }
.pln-access-hint { margin: 0; color: var(--text-muted); font-size: 11.5px; line-height: 1.5; max-width: 620px; }
.pln-access-group { display: grid; gap: 6px; }
.pln-access-title { display: inline-flex; align-items: center; gap: 6px; color: var(--text-secondary); font-size: 11.5px; font-weight: 600; }
.pln-lock-chip { display: inline-flex; align-items: center; gap: 6px; cursor: pointer; }
.pln-lock-chip input, .pln-feature input { accent-color: var(--sev-high-color); }
.pln-access-features { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px; }
.pln-feature { display: flex; align-items: flex-start; gap: 9px; padding: 9px 11px; border-radius: 9px; border: 0.5px solid var(--border-subtle); background: var(--bg-panel); cursor: pointer; }
.pln-feature[data-on="true"] { border-color: color-mix(in srgb, var(--sev-high-color) 45%, var(--border-subtle)); }
.pln-feature strong { display: block; color: var(--text-primary); font-size: 12px; }
.pln-feature small { display: block; margin-top: 2px; color: var(--text-muted); font-size: 11px; line-height: 1.4; }
.pln-unit { color: var(--text-muted); font-size: 11px; }
.pln-faint { color: var(--text-faint); }
.pln-seg { display: inline-flex; flex-wrap: wrap; padding: 3px; gap: 3px; border-radius: 10px; background: var(--bg-panel); border: 0.5px solid var(--border-subtle); width: fit-content; }
.pln-seg-btn { display: inline-flex; align-items: center; gap: 6px; min-height: 34px; padding: 0 14px; border-radius: 8px; border: none; background: transparent; color: var(--text-secondary); font-size: 12px; font-weight: 600; cursor: pointer; }
.pln-seg-btn[data-on="true"] { background: var(--accent-ghost); color: var(--accent); box-shadow: inset 0 0 0 0.5px var(--border-accent); }
.pln-seg-sm .pln-seg-btn { min-height: 30px; padding: 0 10px; font-size: 11.5px; }
.pln-chip { min-height: 40px; padding: 0 11px; border-radius: 8px; border: 0.5px solid var(--border-subtle); background: var(--bg-panel); color: var(--text-secondary); font: 600 11.5px var(--font-mono); cursor: pointer; }
.pln-chip[data-on="true"] { color: var(--accent); border-color: var(--border-accent); background: var(--accent-ghost); }
.pln-check { display: inline-flex; align-items: center; gap: 7px; color: var(--text-secondary); font-size: 12px; cursor: pointer; }
.pln-cap { margin-top: 4px; min-height: 40px; flex-wrap: wrap; }
.pln-table { display: grid; border: 0.5px solid var(--border-subtle); border-radius: 10px; overflow: hidden; background: var(--bg-panel); }
.pln-trow { display: grid; grid-template-columns: minmax(200px, 1.3fr) auto minmax(130px, 0.8fr) minmax(120px, 0.8fr); gap: 12px; align-items: center; padding: 8px 12px; border-bottom: 0.5px solid var(--border-subtle); }
.pln-trow:last-child { border-bottom: none; }
.pln-trow[data-off="true"] .pln-mode { opacity: 0.55; }
.pln-mode { display: flex; align-items: center; gap: 9px; min-width: 0; }
.pln-mode > i { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.pln-mode strong { display: inline-flex; align-items: center; gap: 5px; color: var(--text-primary); font-size: 12.5px; }
.pln-mode small { display: block; color: var(--text-muted); font-size: 10.5px; margin-top: 1px; }
.pln-used { display: inline-flex; align-items: center; gap: 8px; justify-content: flex-end; color: var(--text-secondary); font-size: 11.5px; font-family: var(--font-mono); }
.pln-deep { display: grid; gap: 8px; margin-top: 8px; padding: 10px 12px; border-radius: 10px; border: 0.5px dashed color-mix(in srgb, var(--sev-critical-color) 40%, var(--border-subtle)); background: color-mix(in srgb, var(--sev-critical-color) 4%, var(--bg-panel)); }
.pln-deep strong { display: inline-flex; align-items: center; gap: 6px; color: var(--text-primary); font-size: 12px; }
.pln-summary { display: grid; gap: 9px; padding: 12px 14px; border-radius: 10px; background: var(--bg-panel); border: 0.5px solid var(--border-subtle); }
.pln-summary-top { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.pln-badge { display: inline-flex; align-items: center; gap: 6px; font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; }
.pln-dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.pln-plan { font: 700 10px var(--font-mono); color: var(--text-secondary); border: 0.5px solid var(--border-subtle); border-radius: 5px; padding: 1px 6px; }
.pln-days { display: inline-flex; align-items: center; gap: 5px; color: var(--text-muted); font-size: 11.5px; margin-left: auto; }
.pln-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.pln-mchip { display: inline-flex; align-items: center; gap: 6px; padding: 4px 9px; border-radius: 99px; border: 0.5px solid var(--border-subtle); background: var(--bg-surface); color: var(--text-secondary); font-size: 11.5px; }
.pln-mchip i { width: 7px; height: 7px; border-radius: 50%; }
.pln-mchip b { color: var(--text-primary); font-weight: 700; }
.pln-mchip[data-off="true"] { opacity: 0.5; }
.pln-mchip[data-empty="true"] b { color: var(--sev-high-color); }
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
.pln-mini-xs { min-height: 24px; padding: 0 7px; font-size: 10.5px; }
.pln-mini:hover:not(:disabled) { color: var(--accent); border-color: var(--border-accent); }
.pln-mini:disabled { opacity: 0.4; cursor: not-allowed; }
@media (max-width: 900px) {
  .pln-fields { grid-template-columns: 1fr; }
  .pln-trow { grid-template-columns: 1fr; gap: 6px; }
  .pln-used { justify-content: flex-start; }
  .pln-row { flex-wrap: wrap; }
  .pln-days { margin-left: 0; }
}
`;
