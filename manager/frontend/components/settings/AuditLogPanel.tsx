"use client";

/**
 * The audit log, for operators (administrators) and for customers.
 *
 * Operators see the whole trail with every field, can filter and export it, and see whether
 * the tamper check passes. Customers see a narrower record of their own engagement: what
 * happened, who did it (Vedha staff as "Vedha analyst"), when and with what outcome, and
 * never an operator's address or internal detail.
 */
import { useState } from "react";
import { useInfiniteQuery, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  AlertTriangle, ChevronDown, Download, FileSearch, Lock, RefreshCw, ShieldCheck, X,
} from "lucide-react";
import { errorMessage, fetchJson } from "../../lib/fetcher";
import { portalApi } from "../../lib/portal-client";
import {
  EMPTY_FILTERS, OUTCOME_LABEL, RECORDED_FIELDS, actorName, auditQuery, changeLines, exportHref,
  filterCount, formatUtc, integritySentence, mapAuditPage, mapCustomerPage, mapIntegrity, periodRange,
  type AuditEntry, type AuditFacets, type AuditFilterState, type AuditOutcome, type Period,
} from "../../lib/audit-log";

const PAGE = 50;

function useFilters() {
  const [filters, setFilters] = useState<AuditFilterState>(EMPTY_FILTERS);
  const set = (patch: Partial<AuditFilterState>) => setFilters((f) => ({ ...f, ...patch }));
  return { filters, set, clear: () => setFilters(EMPTY_FILTERS) };
}

function OutcomeBadge({ outcome }: { outcome: AuditOutcome }) {
  return <span className="aud-outcome" data-outcome={outcome}>{OUTCOME_LABEL[outcome]}</span>;
}

// ── operators ─────────────────────────────────────────────────────────────────

export function OperatorAuditLog() {
  const { filters, set, clear } = useFilters();
  const [open, setOpen] = useState<string | null>(null);

  const list = useInfiniteQuery({
    queryKey: ["audit-log", "list", filters],
    initialPageParam: "",
    queryFn: async ({ pageParam }) => mapAuditPage(await fetchJson(
      `/api/audit-logs?${auditQuery(filters, { limit: PAGE, cursor: pageParam || undefined })}`)),
    getNextPageParam: (last) => last.nextCursor ?? undefined,
  });
  const facets = useQuery({
    queryKey: ["audit-log", "facets", filters],
    queryFn: async () => {
      const raw = await fetchJson<any>(`/api/audit-logs/facets?${auditQuery(filters)}`);
      return raw as AuditFacets;
    },
    placeholderData: (previous) => previous,
  });
  const entries = list.data?.pages.flatMap((p) => p.items) ?? [];
  const active = filterCount(filters);

  return (
    <div className="aud">
      <style>{STYLES}</style>
      <IntegrityStrip />

      <div className="aud-filters" role="search" aria-label="Filter the audit log">
        <PeriodChips filters={filters} set={set} />
        <label className="aud-field">
          <span>From (UTC)</span>
          <input type="date" value={filters.from} max={filters.to || undefined} onChange={(e) => set({ from: e.target.value })} />
        </label>
        <label className="aud-field">
          <span>To (UTC)</span>
          <input type="date" value={filters.to} min={filters.from || undefined} onChange={(e) => set({ to: e.target.value })} />
        </label>
        <label className="aud-field aud-grow">
          <span>Search</span>
          <input type="search" placeholder="Action, person, resource or request ID" value={filters.q}
            onChange={(e) => set({ q: e.target.value })} />
        </label>
        <label className="aud-field">
          <span>Person</span>
          <input type="text" placeholder="Email or ID" value={filters.actor} onChange={(e) => set({ actor: e.target.value })} />
        </label>
        <label className="aud-field">
          <span>Source address</span>
          <input type="text" placeholder="203.0.113.7" value={filters.ip} onChange={(e) => set({ ip: e.target.value })} />
        </label>
      </div>

      <div className="aud-chips" role="group" aria-label="Category">
        <button type="button" aria-pressed={filters.category === ""} onClick={() => set({ category: "" })}>All</button>
        {(facets.data?.categories ?? []).filter((c) => c.count > 0 || filters.category === c.key).map((c) => (
          <button key={c.key} type="button" aria-pressed={filters.category === c.key}
            onClick={() => set({ category: filters.category === c.key ? "" : c.key })}>
            {c.label} <b>{c.count.toLocaleString("en")}</b>
          </button>
        ))}
        <span className="aud-sep" aria-hidden />
        {(["success", "failure", "denied"] as const).map((o) => (
          <button key={o} type="button" data-outcome={o} aria-pressed={filters.outcome === o}
            onClick={() => set({ outcome: filters.outcome === o ? "" : o })}>
            {OUTCOME_LABEL[o]} <b>{(facets.data?.outcomes.find((x) => x.key === o)?.count ?? 0).toLocaleString("en")}</b>
          </button>
        ))}
        {active > 0 && (
          <button type="button" className="aud-clear" onClick={clear}><X size={12} aria-hidden /> Clear filters ({active})</button>
        )}
      </div>

      <div className="aud-bar">
        <span aria-live="polite">
          {list.isLoading ? "Loading…" : `${entries.length.toLocaleString("en")} shown${list.hasNextPage ? " · more available" : ""}`}
        </span>
        <span className="aud-bar-actions">
          <button type="button" className="aud-btn" onClick={() => void list.refetch()}><RefreshCw size={12} aria-hidden /> Refresh</button>
          <a className="aud-btn" href={exportHref(filters, "csv")} download><Download size={12} aria-hidden /> CSV</a>
          <a className="aud-btn" href={exportHref(filters, "json")} download><Download size={12} aria-hidden /> JSON</a>
        </span>
      </div>
      <p className="aud-note">Exports include every entry that matches the filters, not just the ones shown, and are themselves recorded here.</p>

      {list.error ? (
        <div className="aud-empty" role="alert"><AlertTriangle size={14} aria-hidden /> {errorMessage(list.error)}
          <button type="button" className="aud-btn" onClick={() => void list.refetch()}>Retry</button></div>
      ) : entries.length === 0 && !list.isLoading ? (
        <div className="aud-empty"><FileSearch size={14} aria-hidden />
          {active > 0 ? "No entries match these filters." : "Nothing has been recorded yet."}</div>
      ) : (
        <ol className="aud-list">
          {entries.map((e) => (
            <li key={e.id}>
              <Entry entry={e} open={open === e.id} onToggle={() => setOpen(open === e.id ? null : e.id)} />
            </li>
          ))}
        </ol>
      )}
      {list.hasNextPage && (
        <button type="button" className="aud-btn aud-more" disabled={list.isFetchingNextPage} onClick={() => void list.fetchNextPage()}>
          {list.isFetchingNextPage ? "Loading…" : "Load older entries"}
        </button>
      )}

      <RecordedFields />
    </div>
  );
}

function PeriodChips({ filters, set }: { filters: AuditFilterState; set: (p: Partial<AuditFilterState>) => void }) {
  const periods: { key: Period; label: string }[] = [
    { key: "24h", label: "24 hours" }, { key: "7d", label: "7 days" }, { key: "30d", label: "30 days" }, { key: "all", label: "All time" },
  ];
  const current = (p: Period) => {
    const r = periodRange(p);
    return r.from === filters.from && filters.to === "";
  };
  return (
    <div className="aud-period" role="group" aria-label="Period">
      {periods.map((p) => (
        <button key={p.key} type="button" aria-pressed={current(p.key)} onClick={() => set(periodRange(p.key))}>{p.label}</button>
      ))}
    </div>
  );
}

function IntegrityStrip() {
  const qc = useQueryClient();
  const integrity = useQuery({
    queryKey: ["audit-log", "integrity"],
    queryFn: async () => mapIntegrity(await fetchJson("/api/audit-logs/integrity")),
    staleTime: 60_000,
  });
  const i = integrity.data;
  return (
    <section className="aud-integrity" data-ok={i ? String(i.ok) : undefined} aria-label="Integrity and retention">
      <div className="aud-integrity-main">
        {i && !i.ok ? <AlertTriangle size={18} aria-hidden /> : <ShieldCheck size={18} aria-hidden />}
        <div>
          <strong>{integrity.isLoading ? "Checking integrity…" : i ? integritySentence(i) : "Integrity could not be checked."}</strong>
          <span>Each entry is chained to the one before it by the database, and entries cannot be edited or deleted. Only the retention job removes old ones.</span>
        </div>
        <button type="button" className="aud-btn" onClick={() => void qc.invalidateQueries({ queryKey: ["audit-log", "integrity"] })}>
          <RefreshCw size={12} aria-hidden /> Re-check
        </button>
      </div>
      {i && <Retention days={i.retentionDays} minimum={i.minimumRetentionDays} />}
    </section>
  );
}

function Retention({ days, minimum }: { days: number; minimum: number }) {
  const qc = useQueryClient();
  const [editing, setEditing] = useState(false);
  const [value, setValue] = useState(String(days));
  const save = useMutation({
    mutationFn: () => fetchJson("/api/org-settings/audit", { method: "PUT", body: JSON.stringify({ retention_days: Number(value) }) }),
    onSuccess: () => { setEditing(false); void qc.invalidateQueries({ queryKey: ["audit-log", "integrity"] }); },
  });
  const n = Number(value);
  const invalid = !Number.isInteger(n) || n < minimum || n > 3650;
  return (
    <div className="aud-retention">
      <Lock size={13} aria-hidden />
      {editing ? (
        <form onSubmit={(e) => { e.preventDefault(); if (!invalid) save.mutate(); }}>
          <label>Keep entries for <input type="number" min={minimum} max={3650} value={value}
            onChange={(e) => setValue(e.target.value)} aria-invalid={invalid} /> days</label>
          <button type="submit" className="aud-btn" disabled={invalid || save.isPending}>Save</button>
          <button type="button" className="aud-btn" onClick={() => { setEditing(false); setValue(String(days)); }}>Cancel</button>
          <small data-error={invalid || save.isError || undefined}>
            {save.isError ? errorMessage(save.error) : `Between ${minimum} and 3,650 days. ${minimum} is the legal minimum (CERT-In) and cannot be lowered.`}
          </small>
        </form>
      ) : (
        <>
          <span>Entries are kept for <b>{days} days</b>, then removed oldest-first. Minimum {minimum}.</span>
          <button type="button" className="aud-btn" onClick={() => setEditing(true)}>Change</button>
        </>
      )}
    </div>
  );
}

function Entry({ entry: e, open, onToggle }: { entry: AuditEntry; open: boolean; onToggle: () => void }) {
  const changes = changeLines(e.changes);
  return (
    <article className="aud-entry" data-open={open || undefined} data-outcome={e.outcome}>
      <button type="button" className="aud-entry-head" aria-expanded={open} onClick={onToggle}>
        <time dateTime={e.timestamp} title={e.timestamp}>{formatUtc(e.timestamp)}</time>
        <span className="aud-what"><strong>{e.label}</strong><code>{e.action}</code></span>
        <OutcomeBadge outcome={e.outcome} />
        <span className="aud-who">{actorName(e)}</span>
        <span className="aud-ip">{e.ipAddress ?? "—"}</span>
        <ChevronDown size={14} aria-hidden className="aud-chev" />
      </button>
      {open && (
        <div className="aud-detail">
          <dl>
            <Row k="Entry" v={e.id} mono />
            <Row k="Time" v={formatUtc(e.timestamp)} />
            <Row k="Action" v={`${e.label} (${e.action})`} />
            <Row k="Outcome" v={OUTCOME_LABEL[e.outcome]} />
            <Row k="Who" v={`${actorName(e)}${e.actor.type ? ` · ${e.actor.type}` : ""}`} />
            <Row k="Actor ID" v={e.actor.id} mono />
            <Row k="Resource" v={e.resourceType ? `${e.resourceType}${e.resourceId ? ` ${e.resourceId}` : ""}` : null} mono />
            <Row k="Engagement" v={e.engagementName ?? e.engagementId} />
            <Row k="Source address" v={e.ipAddress} mono />
            <Row k="User agent" v={e.userAgent} />
            <Row k="Request ID" v={e.requestId} mono />
            <Row k="Chain position" v={e.chainPosition?.toString() ?? null} />
            <Row k="Entry hash" v={e.entryHash} mono />
          </dl>
          {changes.length > 0 && (
            <table className="aud-changes">
              <caption>What changed</caption>
              <thead><tr><th>Field</th><th>Before</th><th>After</th></tr></thead>
              <tbody>{changes.map((c) => <tr key={c.field}><td>{c.field}</td><td>{c.before}</td><td>{c.after}</td></tr>)}</tbody>
            </table>
          )}
          {e.detail && Object.keys(e.detail).length > 0 && (
            <details open>
              <summary>Detail</summary>
              <pre>{JSON.stringify(e.detail, null, 2)}</pre>
            </details>
          )}
        </div>
      )}
    </article>
  );
}

function Row({ k, v, mono }: { k: string; v: string | null | undefined; mono?: boolean }) {
  if (!v) return null;
  return <div><dt>{k}</dt><dd data-mono={mono || undefined}>{v}</dd></div>;
}

function RecordedFields() {
  return (
    <details className="aud-recorded">
      <summary>What each entry records, and the controls it supports</summary>
      <table>
        <thead><tr><th>Field</th><th>Answers</th><th>Supports</th></tr></thead>
        <tbody>{RECORDED_FIELDS.map((r) => <tr key={r.field}><td>{r.field}</td><td>{r.answers}</td><td>{r.controls}</td></tr>)}</tbody>
      </table>
      <p>These are the requirements an auditor usually maps each field to. Recording them does not by itself make an organisation compliant.</p>
    </details>
  );
}

export function AdminOnlyNotice() {
  return (
    <div className="aud">
      <style>{STYLES}</style>
      <div className="aud-empty"><Lock size={14} aria-hidden /> The audit log is visible to administrators only. Ask an administrator for access or an export.</div>
    </div>
  );
}

// ── customers ─────────────────────────────────────────────────────────────────

export function CustomerAuditLog() {
  const { filters, set, clear } = useFilters();
  const list = useInfiniteQuery({
    queryKey: ["audit-log", "customer", filters],
    initialPageParam: "",
    queryFn: async ({ pageParam }) => mapCustomerPage(await portalApi<unknown>(
      `/audit-log?${auditQuery({ ...filters, q: "", actor: "", ip: "" }, { limit: PAGE, cursor: pageParam || undefined })}`)),
    getNextPageParam: (last) => last.nextCursor ?? undefined,
  });
  const entries = list.data?.pages.flatMap((p) => p.items) ?? [];
  const categories = Array.from(new Map(entries.map((e) => [e.category, e.categoryLabel])).entries());
  const active = filterCount({ ...filters, q: "", actor: "", ip: "" });

  return (
    <div className="aud">
      <style>{STYLES}</style>
      <p className="aud-note">
        A record of what happened in your engagement: scans, changes to findings and plans, and who signed in.
        Times are UTC. Entries cannot be edited or removed.
      </p>
      <div className="aud-filters" role="search" aria-label="Filter the activity record">
        <PeriodChips filters={filters} set={set} />
        <label className="aud-field"><span>From (UTC)</span>
          <input type="date" value={filters.from} max={filters.to || undefined} onChange={(e) => set({ from: e.target.value })} /></label>
        <label className="aud-field"><span>To (UTC)</span>
          <input type="date" value={filters.to} min={filters.from || undefined} onChange={(e) => set({ to: e.target.value })} /></label>
      </div>
      <div className="aud-chips" role="group" aria-label="Filter by result">
        {(["success", "failure", "denied"] as const).map((o) => (
          <button key={o} type="button" data-outcome={o} aria-pressed={filters.outcome === o}
            onClick={() => set({ outcome: filters.outcome === o ? "" : o })}>{OUTCOME_LABEL[o]}</button>
        ))}
        {categories.length > 1 && <span className="aud-sep" aria-hidden />}
        {categories.length > 1 && categories.map(([key, label]) => (
          <button key={key} type="button" aria-pressed={filters.category === key}
            onClick={() => set({ category: filters.category === key ? "" : key })}>{label}</button>
        ))}
        {active > 0 && <button type="button" className="aud-clear" onClick={clear}><X size={12} aria-hidden /> Clear filters ({active})</button>}
      </div>

      {list.error ? (
        <div className="aud-empty" role="alert"><AlertTriangle size={14} aria-hidden /> {errorMessage(list.error)}</div>
      ) : entries.length === 0 && !list.isLoading ? (
        <div className="aud-empty"><FileSearch size={14} aria-hidden /> {active > 0 ? "Nothing matches these filters." : "Nothing has been recorded yet."}</div>
      ) : (
        <ol className="aud-list">
          {entries.map((e) => (
            <li key={e.id}>
              <article className="aud-entry" data-outcome={e.outcome}>
                <div className="aud-entry-head" data-static>
                  <time dateTime={e.timestamp}>{formatUtc(e.timestamp)}</time>
                  <span className="aud-what"><strong>{e.label}</strong><small>{e.categoryLabel}</small></span>
                  <OutcomeBadge outcome={e.outcome} />
                  <span className="aud-who">{e.who}</span>
                  <span className="aud-ip">{e.ipAddress ?? ""}</span>
                </div>
              </article>
            </li>
          ))}
        </ol>
      )}
      {list.hasNextPage && (
        <button type="button" className="aud-btn aud-more" disabled={list.isFetchingNextPage} onClick={() => void list.fetchNextPage()}>
          {list.isFetchingNextPage ? "Loading…" : "Load older entries"}
        </button>
      )}
    </div>
  );
}

const STYLES = `
.aud { display: flex; flex-direction: column; gap: 14px; min-width: 0; container-type: inline-size; }
.aud-integrity { display: flex; flex-direction: column; gap: 10px; padding: 12px 14px; border: var(--hairline) solid var(--border-subtle); border-radius: 10px; background: var(--bg-surface); }
.aud-integrity[data-ok="true"] { border-color: color-mix(in srgb, var(--nominal-color) 40%, var(--border-subtle)); }
.aud-integrity[data-ok="false"] { border-color: var(--sev-critical-color); }
.aud-integrity-main { display: flex; align-items: flex-start; gap: 10px; }
.aud-integrity-main > svg { flex: none; margin-top: 2px; color: var(--nominal-color); }
.aud-integrity[data-ok="false"] .aud-integrity-main > svg { color: var(--sev-critical-color); }
.aud-integrity-main > div { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.aud-integrity strong { color: var(--text-primary); font: 650 13px/1.4 var(--font-ui); }
.aud-integrity span { color: var(--text-muted); font: 500 11.5px/1.5 var(--font-ui); }
.aud-retention { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; padding-top: 10px; border-top: var(--hairline) solid var(--border-subtle); color: var(--text-secondary); font: 500 12px/1.5 var(--font-ui); }
.aud-retention form { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.aud-retention input { width: 84px; min-height: 30px; padding: 0 8px; border: var(--hairline) solid var(--border-subtle); border-radius: 6px; background: var(--bg-surface); color: var(--text-primary); font: 500 12px/1 var(--font-mono); }
.aud-retention small { flex-basis: 100%; color: var(--text-muted); font: 500 11px/1.4 var(--font-ui); }
.aud-retention small[data-error] { color: var(--sev-critical-color); }
.aud-filters { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 10px; }
.aud-field { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.aud-field > span { color: var(--text-muted); font: 650 10.5px/1.2 var(--font-ui); text-transform: uppercase; letter-spacing: .04em; }
.aud-field input { min-height: 34px; padding: 0 10px; border: var(--hairline) solid var(--border-subtle); border-radius: 8px; background: var(--bg-surface); color: var(--text-primary); font: 500 12.5px/1 var(--font-ui); }
.aud-field input[type="text"] { width: 150px; }
.aud-grow { flex: 1 1 220px; }
.aud-grow input { width: 100%; }
.aud-period { display: inline-flex; border: var(--hairline) solid var(--border-subtle); border-radius: 8px; overflow: hidden; }
.aud-period button { min-height: 34px; padding: 0 11px; line-height: 1; border: 0; border-right: var(--hairline) solid var(--border-subtle); background: transparent; color: var(--text-secondary); font: 600 12px/1 var(--font-ui); cursor: pointer; }
.aud-period button:last-child { border-right: 0; }
.aud-period button[aria-pressed="true"] { background: var(--accent-ghost); color: var(--accent); }
.aud-chips { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
.aud-chips button { display: inline-flex; align-items: center; gap: 6px; min-height: 30px; padding: 0 11px; line-height: 1; border: var(--hairline) solid var(--border-subtle); border-radius: 999px; background: transparent; color: var(--text-secondary); font: 600 12px/1 var(--font-ui); cursor: pointer; }
.aud-chips button b { font: 700 11px/1 var(--font-mono); color: var(--text-muted); }
.aud-chips button[aria-pressed="true"] { border-color: var(--border-accent); background: var(--accent-ghost); color: var(--accent); }
.aud-chips button[data-outcome="failure"][aria-pressed="true"], .aud-chips button[data-outcome="denied"][aria-pressed="true"] { border-color: var(--sev-critical-color); color: var(--sev-critical-color); background: transparent; }
.aud-sep { width: 1px; height: 18px; background: var(--border-subtle); margin: 0 4px; }
.aud-clear { border-style: dashed !important; }
.aud-bar { display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap; color: var(--text-muted); font: 500 12px/1.4 var(--font-ui); }
.aud-bar-actions { display: inline-flex; flex-wrap: wrap; gap: 6px; }
.aud-btn { display: inline-flex; align-items: center; gap: 6px; min-height: 30px; padding: 0 11px; border: var(--hairline) solid var(--border-subtle); border-radius: 8px; background: transparent; color: var(--text-secondary); font: 600 12px/1 var(--font-ui); text-decoration: none; cursor: pointer; }
.aud-btn:hover:not(:disabled) { border-color: var(--border-strong); color: var(--text-primary); }
.aud-btn:disabled { opacity: .5; cursor: default; }
.aud-more { align-self: center; }
.aud-note { margin: -6px 0 0; color: var(--text-muted); font: 500 11.5px/1.5 var(--font-ui); }
.aud-empty { display: flex; align-items: center; gap: 8px; padding: 18px 14px; border: var(--hairline) dashed var(--border-subtle); border-radius: 10px; color: var(--text-muted); font: 500 12.5px/1.5 var(--font-ui); }
.aud-list { display: flex; flex-direction: column; gap: 4px; margin: 0; padding: 0; list-style: none; }
.aud-entry { border: var(--hairline) solid var(--border-subtle); border-radius: 8px; background: var(--bg-surface); }
.aud-entry[data-outcome="failure"], .aud-entry[data-outcome="denied"] { border-left: 3px solid var(--sev-critical-color); }
.aud-entry-head { display: grid; grid-template-columns: 172px minmax(0, 1fr) 84px minmax(0, 190px) 120px 16px; align-items: center; gap: 12px; width: 100%; padding: 9px 12px; border: 0; background: transparent; color: inherit; text-align: left; cursor: pointer; font: inherit; }
.aud-entry-head[data-static] { cursor: default; grid-template-columns: 172px minmax(0, 1fr) 84px minmax(0, 190px) 120px; }
.aud-entry-head time { color: var(--text-muted); font: 500 11px/1.4 var(--font-mono); }
.aud-what { display: flex; flex-direction: column; gap: 1px; min-width: 0; }
.aud-what strong { color: var(--text-primary); font: 650 12.5px/1.4 var(--font-ui); }
.aud-what code, .aud-what small { color: var(--text-muted); font: 500 10.5px/1.4 var(--font-mono); overflow-wrap: anywhere; }
.aud-what small { font-family: var(--font-ui); }
.aud-who { color: var(--text-secondary); font: 500 12px/1.4 var(--font-ui); overflow-wrap: anywhere; }
.aud-ip { color: var(--text-muted); font: 500 11px/1.4 var(--font-mono); overflow-wrap: anywhere; }
.aud-chev { color: var(--text-muted); transition: transform .15s; }
.aud-entry[data-open] .aud-chev { transform: rotate(180deg); }
.aud-outcome { justify-self: start; padding: 2px 8px; border-radius: 999px; font: 700 10.5px/1.4 var(--font-ui); border: var(--hairline) solid var(--border-subtle); color: var(--text-secondary); }
.aud-outcome[data-outcome="success"] { color: var(--nominal-color); }
.aud-outcome[data-outcome="failure"], .aud-outcome[data-outcome="denied"] { color: var(--sev-critical-color); border-color: var(--sev-critical-color); }
.aud-detail { display: flex; flex-direction: column; gap: 12px; padding: 4px 14px 14px 14px; border-top: var(--hairline) solid var(--border-subtle); }
.aud-detail dl { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 24px; margin: 12px 0 0; }
.aud-detail dl > div { display: flex; gap: 10px; min-width: 0; }
.aud-detail dt { flex: none; width: 104px; color: var(--text-muted); font: 600 11px/1.5 var(--font-ui); }
.aud-detail dd { margin: 0; min-width: 0; color: var(--text-primary); font: 500 12px/1.5 var(--font-ui); overflow-wrap: anywhere; }
.aud-detail dd[data-mono] { font-family: var(--font-mono); font-size: 11px; }
.aud-detail pre { margin: 6px 0 0; padding: 10px 12px; max-height: 260px; overflow: auto; border-radius: 8px; background: var(--bg-base, var(--track-bg)); color: var(--text-secondary); font: 500 11px/1.6 var(--font-mono); }
.aud-detail summary { color: var(--text-secondary); font: 650 12px/1.4 var(--font-ui); cursor: pointer; }
.aud-changes { width: 100%; border-collapse: collapse; font: 500 12px/1.5 var(--font-ui); }
.aud-changes caption { text-align: left; padding-bottom: 4px; color: var(--text-secondary); font: 650 12px/1.4 var(--font-ui); }
.aud-changes th, .aud-changes td { padding: 5px 8px; border-bottom: var(--hairline) solid var(--border-subtle); text-align: left; overflow-wrap: anywhere; }
.aud-changes th { color: var(--text-muted); font-weight: 650; }
.aud-recorded { border: var(--hairline) solid var(--border-subtle); border-radius: 10px; padding: 10px 14px; }
.aud-recorded summary { cursor: pointer; color: var(--text-secondary); font: 650 12.5px/1.4 var(--font-ui); }
.aud-recorded table { width: 100%; margin-top: 10px; border-collapse: collapse; font: 500 12px/1.5 var(--font-ui); }
.aud-recorded th, .aud-recorded td { padding: 6px 8px; border-bottom: var(--hairline) solid var(--border-subtle); text-align: left; vertical-align: top; }
.aud-recorded th { color: var(--text-muted); font-weight: 650; }
.aud-recorded p { margin: 10px 0 0; color: var(--text-muted); font: 500 11.5px/1.5 var(--font-ui); }
@container (max-width: 760px) {
  .aud-entry-head { grid-template-columns: minmax(0, 1fr) auto 16px; row-gap: 4px; }
  .aud-entry-head[data-static] { grid-template-columns: minmax(0, 1fr) auto; }
  .aud-entry-head time, .aud-who, .aud-ip { grid-column: 1 / -1; }
  .aud-entry-head time { grid-row: 1; }
  .aud-what { grid-column: 1; grid-row: 2; }
  .aud-outcome { grid-column: 2; grid-row: 2; }
  .aud-chev { grid-column: 3; grid-row: 2; }
  .aud-who { grid-row: 3; }
  .aud-ip { grid-row: 4; }
  .aud-detail dl { grid-template-columns: minmax(0, 1fr); }
  .aud-recorded table { display: block; overflow-x: auto; }
}
@media (max-width: 720px) {
  .aud-field input[type="text"], .aud-field input[type="date"] { width: 100%; }
  .aud-field { flex: 1 1 140px; }
  .aud-period { width: 100%; }
  .aud-period button { flex: 1; min-height: 44px; }
  .aud-btn, .aud-chips button { min-height: 44px; }
  .aud-integrity-main { flex-wrap: wrap; }
}
`;
