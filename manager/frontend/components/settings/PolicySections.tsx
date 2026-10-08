"use client";

/**
 * Organisation policy forms for Settings: sign-in rules, scanning rules and the
 * defaults a new customer starts with. The server validates and enforces every
 * rule; a form saves only after the server confirms and shows exactly what it
 * stored. Only an admin may change a policy, so other roles see it read-only and
 * the page never sends a request the server would refuse (a refused request makes
 * the shared fetch helper treat the session as expired).
 */

import React, { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Ban, CalendarClock, Plus, ShieldCheck, Trash2, TriangleAlert, UserPlus } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import {
  DAY_LABELS, formatPolicyError, hoursFromInput, isoToLocalInput, listFromText, localInputToIso,
  newBlackout, textFromList, windowSummary,
  type AuthPolicy, type BlackoutWindow, type CustomerDefaults, type LockFeature, type LockSeverity, type ScanPolicy,
} from "../../lib/org-settings";

type Section = "auth" | "scan" | "customer-defaults";

/** The signed-in user's role, so forms know whether they may be edited. */
function useRole() {
  const q = useQuery({
    queryKey: ["me-role"],
    queryFn: () => fetchJson<{ role: string }>("/api/auth/me"),
    staleTime: 5 * 60_000,
  });
  return q.data?.role ?? null;
}

function usePolicy<T>(section: Section, enabled: boolean) {
  const qc = useQueryClient();
  const query = useQuery({
    queryKey: ["org-settings", section],
    queryFn: () => fetchJson<T>(`/api/org-settings/${section}`),
    enabled,
  });
  const [draft, setDraft] = useState<T | null>(null);
  const [errors, setErrors] = useState<string[]>([]);
  const [saved, setSaved] = useState(false);
  const current = draft ?? query.data ?? null;
  const dirty = draft !== null && JSON.stringify(draft) !== JSON.stringify(query.data);

  const save = useMutation({
    mutationFn: (value: T) => fetchJson<T>(`/api/org-settings/${section}`, { method: "PUT", body: JSON.stringify(value) }),
    onSuccess: (stored) => {
      qc.setQueryData(["org-settings", section], stored);   // show what the server stored
      setDraft(null); setErrors([]); setSaved(true);
    },
    onError: (e) => { setSaved(false); setErrors(formatPolicyError(e instanceof Error ? e.message : "Save failed")); },
  });
  const edit = (next: T) => { setSaved(false); setErrors([]); setDraft(next); };
  return { query, current, dirty, save, edit, discard: () => { setDraft(null); setErrors([]); }, errors, saved };
}

function Footer({ canEdit, dirty, pending, errors, saved, onSave, onDiscard }: {
  canEdit: boolean; dirty: boolean; pending: boolean; errors: string[]; saved: boolean;
  onSave: () => void; onDiscard: () => void;
}) {
  if (!canEdit) {
    return <p className="policy-note">Only an administrator can change this policy.</p>;
  }
  return (
    <div className="policy-footer">
      <button type="button" className="btn btn-primary btn-sm" onClick={onSave} disabled={!dirty || pending}>
        {pending ? "Saving…" : "Save changes"}
      </button>
      {dirty && <button type="button" className="btn btn-secondary btn-sm" onClick={onDiscard} disabled={pending}>Discard</button>}
      {dirty && <span className="policy-muted">Unsaved changes</span>}
      {saved && !dirty && <span role="status" className="policy-ok">Saved.</span>}
      {errors.length > 0 && (
        <ul role="alert" className="policy-errors">{errors.map((e) => <li key={e}>{e}</li>)}</ul>
      )}
    </div>
  );
}

const Field = ({ label, hint, children }: { label: string; hint?: string; children: React.ReactNode }) => (
  <label className="policy-field">
    <span className="policy-label">{label}</span>
    {children}
    {hint && <small>{hint}</small>}
  </label>
);

// ─── Authentication ──────────────────────────────────────────────────────────

export function AuthPolicySection() {
  const role = useRole();
  const isAdmin = role === "admin";
  const { query, current, dirty, save, edit, discard, errors, saved } = usePolicy<AuthPolicy>("auth", isAdmin);
  // Text the user has typed; null means "show the stored values".
  const [typed, setHours] = useState<{ op: string; cu: string } | null>(null);
  const hours = typed ?? {
    op: query.data?.operator_session_max_hours?.toString() ?? "",
    cu: query.data?.customer_session_max_hours?.toString() ?? "",
  };

  if (role === null || (isAdmin && !current)) return <p className="settings-loading-msg">Loading sign-in policy…</p>;
  if (!isAdmin) {
    return (
      <div className="policy-card">
        <h3><ShieldCheck size={15} /> Sign-in policy</h3>
        <p className="policy-note">Only an administrator can view or change the sign-in policy.</p>
      </div>
    );
  }
  const policy = current!;
  const setHoursField = (key: "op" | "cu", value: string) => {
    const next = { ...hours, [key]: value };
    setHours(next);
    const op = hoursFromInput(next.op), cu = hoursFromInput(next.cu);
    edit({ ...policy,
      operator_session_max_hours: Number.isNaN(op) ? (policy.operator_session_max_hours) : op,
      customer_session_max_hours: Number.isNaN(cu) ? (policy.customer_session_max_hours) : cu });
  };
  const invalidHours = (v: string) => v.trim() !== "" && Number.isNaN(hoursFromInput(v));

  return (
    <div className="policy-card">
      <h3><ShieldCheck size={15} /> Sign-in policy</h3>
      <Field label="Allowed networks"
        hint="One address or range per line, e.g. 203.0.113.0/24. Leave empty to allow sign-in from anywhere.">
        <textarea rows={4} spellCheck={false} placeholder="203.0.113.0/24&#10;198.51.100.7"
          value={textFromList(policy.ip_allowlist)}
          onChange={(e) => edit({ ...policy, ip_allowlist: listFromText(e.target.value) })} />
      </Field>
      <label className="policy-check">
        <input type="checkbox" checked={policy.ip_allowlist_applies_to_portal}
          onChange={(e) => edit({ ...policy, ip_allowlist_applies_to_portal: e.target.checked })} />
        <span>Also apply to customer portal sign-ins</span>
      </label>
      <p className="policy-note">
        <TriangleAlert size={12} /> Administrators can always sign in, from anywhere, so a wrong list cannot lock everyone out.
        Anyone else outside these networks sees “invalid credentials” rather than a hint that the password was right.
        The list is checked at sign-in and each time a session refreshes.
      </p>
      <div className="policy-block">
        <span className="policy-label">Two-step sign-in</span>
        <label className="policy-check">
          <input type="checkbox" checked={policy.mfa_required_for_operators ?? false}
            onChange={(e) => edit({ ...policy, mfa_required_for_operators: e.target.checked })} />
          <span>Require for operators (admins, managers, analysts, testers)</span>
        </label>
        <label className="policy-check">
          <input type="checkbox" checked={policy.mfa_required_for_customers ?? false}
            onChange={(e) => edit({ ...policy, mfa_required_for_customers: e.target.checked })} />
          <span>Require for customer portal users</span>
        </label>
        <p className="policy-note">
          Nobody is locked out: anyone without an authenticator app is walked through setting one up at their
          next sign-in. Sessions already open continue until they end. Someone who loses their phone can use a
          recovery code, or an administrator can reset their two-step sign-in from Team.
        </p>
      </div>
      <div className="policy-grid">
        <Field label="Operator session limit (hours)" hint="Sign in again after this long, however active. Empty = no limit.">
          <input inputMode="numeric" value={hours.op} aria-invalid={invalidHours(hours.op)}
            onChange={(e) => setHoursField("op", e.target.value)} placeholder="No limit" />
        </Field>
        <Field label="Customer session limit (hours)" hint="Same, for customer portal users.">
          <input inputMode="numeric" value={hours.cu} aria-invalid={invalidHours(hours.cu)}
            onChange={(e) => setHoursField("cu", e.target.value)} placeholder="No limit" />
        </Field>
      </div>
      <Footer canEdit dirty={dirty && !invalidHours(hours.op) && !invalidHours(hours.cu)}
        pending={save.isPending} errors={errors} saved={saved}
        onSave={() => save.mutate(policy)} onDiscard={() => { discard(); setHours(null); }} />
    </div>
  );
}

// ─── Scanning ────────────────────────────────────────────────────────────────

const browserZone = () => { try { return Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC"; } catch { return "UTC"; } };

export function ScanPolicySection() {
  const role = useRole();
  const canView = role === "admin" || role === "manager";
  const { current, dirty, save, edit, discard, errors, saved } = usePolicy<ScanPolicy>("scan", canView);
  if (role === null || (canView && !current)) return <p className="settings-loading-msg">Loading scanning policy…</p>;
  if (!canView) {
    return <div className="policy-card"><h3><CalendarClock size={15} /> Scanning policy</h3>
      <p className="policy-note">Only an administrator or manager can view the scanning policy.</p></div>;
  }
  const canEdit = role === "admin";
  const policy = current!;
  const setWindow = (i: number, w: BlackoutWindow) => edit({ ...policy, blackouts: policy.blackouts.map((x, j) => (j === i ? w : x)) });

  return (
    <div className="policy-card">
      <h3><CalendarClock size={15} /> Blackout windows</h3>
      <p className="policy-note">No scan can start inside a window. Customer-requested scans wait until it ends.</p>
      {policy.blackouts.length === 0 && <p className="policy-muted">No blackout windows.</p>}
      {policy.blackouts.map((w, i) => (
        <fieldset key={i} className="policy-window" disabled={!canEdit}>
          <legend>{w.name || "New window"} <span className="policy-muted">{w.name ? windowSummary(w) : ""}</span></legend>
          <div className="policy-grid">
            <Field label="Name"><input value={w.name} maxLength={80} placeholder="Month-end close"
              onChange={(e) => setWindow(i, { ...w, name: e.target.value })} /></Field>
            <Field label="Repeats">
              <select value={w.kind} onChange={(e) => setWindow(i, e.target.value === "once"
                ? { ...w, kind: "once", days: [], start: null, end: null, starts_at: null, ends_at: null }
                : { ...newBlackout(w.timezone), name: w.name })}>
                <option value="weekly">Every week</option><option value="once">Once</option>
              </select>
            </Field>
          </div>
          {w.kind === "weekly" ? (
            <>
              <div className="policy-days" role="group" aria-label="Days">
                {DAY_LABELS.map((d, idx) => (
                  <label key={d} className="policy-chip" data-on={w.days.includes(idx)}>
                    <input type="checkbox" checked={w.days.includes(idx)}
                      onChange={() => setWindow(i, { ...w, days: w.days.includes(idx) ? w.days.filter((x) => x !== idx) : [...w.days, idx].sort() })} />
                    {d}
                  </label>
                ))}
              </div>
              <div className="policy-grid">
                <Field label="From"><input type="time" value={w.start ?? ""} onChange={(e) => setWindow(i, { ...w, start: e.target.value })} /></Field>
                <Field label="Until" hint="Earlier than “from” means it runs past midnight."><input type="time" value={w.end ?? ""} onChange={(e) => setWindow(i, { ...w, end: e.target.value })} /></Field>
                <Field label="Time zone" hint="Daylight-saving changes are followed."><input value={w.timezone} onChange={(e) => setWindow(i, { ...w, timezone: e.target.value })} /></Field>
              </div>
            </>
          ) : (
            <div className="policy-grid">
              <Field label="Starts (your local time)"><input type="datetime-local" value={isoToLocalInput(w.starts_at)} onChange={(e) => setWindow(i, { ...w, starts_at: localInputToIso(e.target.value) })} /></Field>
              <Field label="Ends (your local time)"><input type="datetime-local" value={isoToLocalInput(w.ends_at)} onChange={(e) => setWindow(i, { ...w, ends_at: localInputToIso(e.target.value) })} /></Field>
            </div>
          )}
          {canEdit && <button type="button" className="btn btn-sm btn-danger-ghost" onClick={() => edit({ ...policy, blackouts: policy.blackouts.filter((_, j) => j !== i) })}><Trash2 size={12} /> Remove window</button>}
        </fieldset>
      ))}
      {canEdit && policy.blackouts.length < 20 && (
        <button type="button" className="btn btn-secondary btn-sm" onClick={() => edit({ ...policy, blackouts: [...policy.blackouts, newBlackout(browserZone())] })}>
          <Plus size={12} /> Add blackout window
        </button>
      )}
      <label className="policy-check">
        <input type="checkbox" disabled={!canEdit} checked={policy.admin_override}
          onChange={(e) => edit({ ...policy, admin_override: e.target.checked })} />
        <span>An administrator can still start a scan during a blackout (recorded in the audit log)</span>
      </label>

      <h3 style={{ marginTop: 18 }}><Ban size={15} /> Global exclusions</h3>
      <Field label="Never scan these" hint="One address or range per line, for every customer and engagement, e.g. your own management network.">
        <textarea rows={4} spellCheck={false} disabled={!canEdit} placeholder="10.250.0.0/16"
          value={textFromList(policy.global_exclusions)}
          onChange={(e) => edit({ ...policy, global_exclusions: listFromText(e.target.value) })} />
      </Field>
      <Footer canEdit={canEdit} dirty={dirty} pending={save.isPending} errors={errors} saved={saved}
        onSave={() => save.mutate(policy)} onDiscard={discard} />
    </div>
  );
}

// ─── New customers ───────────────────────────────────────────────────────────

const SEVERITIES: LockSeverity[] = ["critical", "high", "medium", "low", "info"];
const FEATURES: { id: LockFeature; label: string }[] = [
  { id: "ai_assistant", label: "AI assistant" }, { id: "reports", label: "Reports" },
  { id: "remediation", label: "Remediation & fix bundles" }, { id: "compliance", label: "Compliance briefs" },
];

export function CustomerDefaultsSection() {
  const role = useRole();
  const canView = role === "admin" || role === "manager";
  const { current, dirty, save, edit, discard, errors, saved } = usePolicy<CustomerDefaults>("customer-defaults", canView);
  const [days, setDays] = useState<string | null>(null);
  const shownDays = useMemo(() => days ?? String(current?.poc_duration_days ?? 14), [days, current]);
  if (role === null || (canView && !current)) return <p className="settings-loading-msg">Loading defaults…</p>;
  if (!canView) {
    return <div className="policy-card"><h3><UserPlus size={15} /> New customers</h3>
      <p className="policy-note">Only an administrator or manager can view these defaults.</p></div>;
  }
  const canEdit = role === "admin";
  const d = current!;
  const toggle = <T extends string>(list: T[], v: T): T[] => (list.includes(v) ? list.filter((x) => x !== v) : [...list, v]);
  const daysInvalid = !/^\d+$/.test(shownDays.trim());

  return (
    <div className="policy-card">
      <h3><UserPlus size={15} /> What a new customer starts with</h3>
      <p className="policy-note">Applies to customers you add from now on. Existing customers are never changed by editing this.</p>
      <div className="policy-block">
        <span className="policy-label">Lock findings of severity on a new trial (POC)</span>
        <div className="policy-days" role="group" aria-label="Locked severities">
          {SEVERITIES.map((s) => (
            <label key={s} className="policy-chip" data-on={d.poc_locked_severities.includes(s)}>
              <input type="checkbox" disabled={!canEdit} checked={d.poc_locked_severities.includes(s)}
                onChange={() => edit({ ...d, poc_locked_severities: toggle(d.poc_locked_severities, s) })} />
              {s[0].toUpperCase() + s.slice(1)}
            </label>
          ))}
        </div>
      </div>
      <div className="policy-block">
        <span className="policy-label">Lock features on a new trial</span>
        <div className="policy-days" role="group" aria-label="Locked features">
          {FEATURES.map((f) => (
            <label key={f.id} className="policy-chip" data-on={d.poc_locked_features.includes(f.id)}>
              <input type="checkbox" disabled={!canEdit} checked={d.poc_locked_features.includes(f.id)}
                onChange={() => edit({ ...d, poc_locked_features: toggle(d.poc_locked_features, f.id) })} />
              {f.label}
            </label>
          ))}
        </div>
      </div>
      <div className="policy-grid">
        <Field label="Trial length (days)">
          <input inputMode="numeric" disabled={!canEdit} value={shownDays} aria-invalid={daysInvalid}
            onChange={(e) => { setDays(e.target.value); if (/^\d+$/.test(e.target.value.trim())) edit({ ...d, poc_duration_days: Number(e.target.value) }); }} />
        </Field>
        <Field label="Support contact" hint="Shown to customers on lock panels and plan notices, e.g. security@yourcompany.com.">
          <input disabled={!canEdit} maxLength={200} value={d.support_contact} placeholder="Your security team"
            onChange={(e) => edit({ ...d, support_contact: e.target.value })} />
        </Field>
      </div>
      <Footer canEdit={canEdit} dirty={dirty && !daysInvalid} pending={save.isPending} errors={errors} saved={saved}
        onSave={() => save.mutate(d)} onDiscard={() => { discard(); setDays(null); }} />
    </div>
  );
}
