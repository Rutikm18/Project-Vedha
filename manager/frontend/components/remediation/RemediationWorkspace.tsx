"use client";

/**
 * RemediationWorkspace — fix bundles for an engagement (operator + portal).
 *
 * "By fix": one card per unit of work — the change, its target state, the hosts
 * it covers (per-host checklist), its due date and where that date comes from.
 * "By host": the same data pivoted for teams that own servers. Everything is
 * computed server-side (app/remediation/bundles.py) — this view only renders.
 */
import React, { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Boxes, ChevronDown, Download, RefreshCw, Server, Sparkles, Wrench } from "lucide-react";
import { PageShell } from "../PageShell";
import { PortalShell } from "../portal/PortalShell";
import { PlanLockPanel } from "../portal/PlanLock";
import { isFeatureLocked } from "../../lib/entitlements";
import { usePortalEntitlement } from "../../lib/portal-client";
import { DataState, EmptyState, SkeletonRows } from "../states/DataState";
import { createReportsWorkspaceApi } from "../../lib/reports-workspace-api";
import {
  DUE_SOURCE_LABEL, TYPE_LABEL, createRemediationApi, fmtIst,
  type Bundle, type PlanOs, type RemediationApi, type RemediationPlan, type RemediationSurface,
} from "../../lib/remediation";
import { ExtensionPanel, ExtensionQueue } from "./ExtensionPanel";
import { SlaPolicyEditor } from "./SlaPolicyEditor";
import { DueBadge, PlanView, StepsByTier, UrgencyChip } from "./PlanView";

const OS_NAME: Record<string, string> = { windows: "Windows", linux: "Linux", macos: "macOS", generic: "Appliance / generic" };

function BundleCard({
  bundle, api, engagementId, open, onToggle, highlight,
}: {
  bundle: Bundle; api: RemediationApi; engagementId: string; open: boolean; onToggle: () => void; highlight: boolean;
}) {
  const osKeys = Object.keys(bundle.steps_by_os);
  const [os, setOs] = useState<string>(osKeys[0] ?? "generic");
  const [refined, setRefined] = useState<RemediationPlan | null>(null);
  const refine = useMutation({
    mutationFn: () => api.refineBundle(engagementId, bundle.fix_key, os as PlanOs),
    onSuccess: (r) => setRefined(r.plan),
  });
  const pct = bundle.progress.total ? Math.round((bundle.progress.closed / bundle.progress.total) * 100) : 100;
  const operator = api.surface === "manager";

  return (
    <article className="rm-bundle" data-highlight={highlight || undefined} id={`fix-${bundle.fix_key}`}>
      <button type="button" className="rm-bundle-head" onClick={onToggle} aria-expanded={open}>
        <span className="rm-bundle-ref">{bundle.ref}</span>
        <span className="rm-bundle-main">
          <strong>{bundle.title}</strong>
          <span className="rm-chips">
            <span className="rm-chip">{TYPE_LABEL[bundle.remediation_type] ?? bundle.remediation_type}</span>
            {bundle.status === "open" && <UrgencyChip label={bundle.urgency} />}
            <span className="rm-chip rm-chip--muted">Target: {bundle.target_state}</span>
            {bundle.status === "open"
              ? <DueBadge at={bundle.due_at} source={bundle.due_source} />
              : <span className="rm-tag rm-tag--ok">Done</span>}
          </span>
        </span>
        <span className="rm-progress">
          <span>{bundle.progress.closed}/{bundle.progress.total} closed · {bundle.hosts.length} host{bundle.hosts.length === 1 ? "" : "s"}</span>
          <span className="rm-progress-bar"><i style={{ width: `${pct}%` }} /></span>
          <ChevronDown size={14} aria-hidden style={{ transform: open ? "rotate(180deg)" : undefined }} />
        </span>
      </button>

      {open && (
        <div className="rm-bundle-body">
          {osKeys.length > 1 && (
            <div className="rm-os-tabs" role="group" aria-label="Steps for platform">
              {osKeys.map((k) => (
                <button key={k} type="button" className="rm-chip" aria-pressed={os === k}
                        style={os === k ? { borderColor: "var(--accent)", color: "var(--accent)" } : undefined}
                        onClick={() => { setOs(k); setRefined(null); }}>
                  {OS_NAME[k] ?? k}
                </button>
              ))}
            </div>
          )}

          {refined
            ? <PlanView plan={refined} headerExtra={<span className="rm-tag rm-tag--ai"><Sparkles size={11} aria-hidden />AI-refined for {bundle.hosts.length} host{bundle.hosts.length === 1 ? "" : "s"} · not yet approved</span>} />
            : <StepsByTier steps={bundle.steps_by_os[os] ?? []} />}

          {operator && (
            <div className="rm-actions">
              <button type="button" className="btn btn-secondary" disabled={refine.isPending} onClick={() => refine.mutate()}>
                {refine.isPending ? <RefreshCw size={13} className="spin" aria-hidden /> : <Sparkles size={13} aria-hidden />}
                Refine this bundle with AI
              </button>
              {refine.error && <p className="rm-error">{refine.error instanceof Error ? refine.error.message : String(refine.error)}</p>}
            </div>
          )}

          <section className="rm-verify">
            <h4>How closure is proven</h4>
            <p><strong>{bundle.verification_check.scanner}</strong> — {bundle.verification_check.check}</p>
            <p className="rm-expected">Expected: {bundle.verification_check.expected}</p>
          </section>

          <section>
            <h4 className="rm-section-h">Host checklist</h4>
            <div className="rm-table-wrap">
              <table className="rm-table">
                <thead><tr><th>Host</th><th>IP</th><th>OS</th><th>Ports</th><th>Findings</th><th>Status</th><th>Due (IST)</th><th>Date source</th></tr></thead>
                <tbody>
                  {bundle.hosts.map((h) => (
                    <tr key={h.ip}>
                      <td><strong>{h.host}</strong></td>
                      <td>{h.ip}</td>
                      <td>{h.os}</td>
                      <td>{h.ports.join(", ") || "—"}</td>
                      <td>{h.finding_ids.length}</td>
                      <td><span className="rm-host-status" data-status={h.status}>{h.status.replace("_", " ")}</span></td>
                      <td>{h.status === "closed" ? (h.closed_at ? `Closed ${fmtIst(h.closed_at)}` : "Closed") : fmtIst(h.due_at)}</td>
                      <td>{h.due_source ? DUE_SOURCE_LABEL[h.due_source] ?? h.due_source : "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {bundle.excluded.length > 0 && (
              <p className="rm-muted">{bundle.excluded.length} finding{bundle.excluded.length === 1 ? "" : "s"} excluded ({[...new Set(bundle.excluded.map((e) => e.reason))].join(", ")}).</p>
            )}
          </section>

          <div className="rm-closeout">
            <section><h4>If the fix cannot land in time</h4><p>{bundle.compensating_controls}</p></section>
          </div>

          {bundle.status === "open" && (
            <ExtensionPanel api={api} engagementId={engagementId}
                            subject={{ type: "bundle", fixKey: bundle.fix_key, fixRef: bundle.ref, currentDue: bundle.due_at,
                                       serious: bundle.kev || bundle.max_severity === "critical" || bundle.max_severity === "high" }} />
          )}
        </div>
      )}
    </article>
  );
}

export function RemediationWorkspace({ surface = "manager" }: { surface?: RemediationSurface }) {
  // A customer's plan can lock Remediation & fix bundles; the server answers 403
  // either way, this just explains it instead of showing an error.
  const plan = usePortalEntitlement(surface === "portal");
  if (surface === "portal" && isFeatureLocked(plan.data, "remediation")) {
    return (
      <PortalShell title="Remediation" subtitle="Fix bundles, owners' checklists and due dates">
        <PlanLockPanel feature="remediation" />
      </PortalShell>
    );
  }
  return <RemediationWorkspaceBody surface={surface} />;
}

function RemediationWorkspaceBody({ surface }: { surface: RemediationSurface }) {
  const params = useSearchParams();
  const api = useMemo(() => createRemediationApi(surface), [surface]);
  const reports = useMemo(() => createReportsWorkspaceApi(surface), [surface]);
  const [selId, setSelId] = useState(params.get("engagement") ?? "");
  const [view, setView] = useState<"fix" | "host">("fix");
  const focusFix = params.get("fix");
  const [openKey, setOpenKey] = useState<string | null>(focusFix);

  const engQ = useQuery({
    queryKey: ["remediation", surface, "engagements"],
    queryFn: () => reports.engagements<{ engagements: Array<{ id: string; name: string; client?: string }> }>(),
  });
  const engs = engQ.data?.engagements ?? [];
  const engId = selId || engs[0]?.id || "";
  const bQ = useQuery({
    queryKey: ["remediation-bundles", surface, engId, view],
    queryFn: () => api.bundles(engId, view),
    enabled: Boolean(engId),
  });

  useEffect(() => {
    if (!focusFix || !bQ.data) return;
    document.getElementById(`fix-${focusFix}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [focusFix, bQ.data]);

  const Shell = surface === "portal" ? PortalShell : PageShell;
  const s = bQ.data?.summary;
  // A tracker is built from the bundles; with none there is nothing to download.
  const exportable = (s?.bundles ?? 0) > 0;
  return (
    <Shell title="Remediation" subtitle="Fix bundles, owners' checklists and due dates — grounded in what the scan recorded">
      <div className="rm-ws">
        <div className="rm-ws-controls">
          {surface === "manager" ? (
            <label>
              <span>Engagement</span>
              <select value={engId} onChange={(e) => { setSelId(e.target.value); setOpenKey(null); }}>
                {engs.map((e) => <option key={e.id} value={e.id}>{e.name}{e.client && e.client !== "—" ? ` · ${e.client}` : ""}</option>)}
              </select>
            </label>
          ) : <span />}
          <div className="rm-actions">
            <div className="rm-seg" role="group" aria-label="View">
              <button type="button" aria-pressed={view === "fix"} onClick={() => setView("fix")}><Wrench size={12} aria-hidden /> By fix</button>
              <button type="button" aria-pressed={view === "host"} onClick={() => setView("host")}><Server size={12} aria-hidden /> By host</button>
            </div>
            {engId && (exportable ? (
              <>
                <a className="btn btn-secondary" href={api.exportUrl(engId, "xlsx")} download><Download size={13} aria-hidden /> Excel tracker</a>
                <a className="btn btn-secondary" href={api.exportUrl(engId, "csv")} download><Download size={13} aria-hidden /> CSV</a>
              </>
            ) : (
              // Nothing to put in a tracker yet: say so rather than download an empty file.
              <>
                <button type="button" className="btn btn-secondary" aria-disabled="true" title="Nothing to export yet" onClick={(e) => e.preventDefault()}><Download size={13} aria-hidden /> Excel tracker</button>
                <button type="button" className="btn btn-secondary" aria-disabled="true" title="Nothing to export yet" onClick={(e) => e.preventDefault()}><Download size={13} aria-hidden /> CSV</button>
              </>
            ))}
          </div>
        </div>

        {surface === "manager" && engId && <SlaPolicyEditor engagementId={engId} />}
        {surface === "manager" && engId && <ExtensionQueue api={api} engagementId={engId} />}

        <DataState
          loading={engQ.isLoading || bQ.isLoading} error={engQ.error || bQ.error}
          isEmpty={!engId || (view === "fix" ? !(bQ.data?.bundles?.length) : !(bQ.data?.hosts?.length))}
          onRetry={() => { void engQ.refetch(); void bQ.refetch(); }}
          skeleton={<SkeletonRows rows={5} height={72} />}
          empty={<EmptyState icon={Boxes} title="Nothing to remediate" hint="Bundles appear once a scan produces findings for this engagement." />}
        >
          {s && (
            <div className="rm-metrics">
              <div className="rm-metric"><small>Open fixes</small><strong>{s.open_bundles}</strong><span>{s.done_bundles} done</span></div>
              <div className="rm-metric"><small>Open findings</small><strong>{s.open_findings}</strong><span>{s.closed_findings} closed</span></div>
              <div className="rm-metric"><small>Hosts</small><strong>{s.hosts}</strong><span>in the checklist</span></div>
              <div className="rm-metric"><small>Act now</small><strong>{s.act}</strong><span>CISA SSVC “Act”</span></div>
              <div className="rm-metric"><small>Due dates from</small><strong style={{ fontSize: 15 }}>{DUE_SOURCE_LABEL[bQ.data!.sla_source] ?? bQ.data!.sla_source}</strong><span>approved extensions override</span></div>
            </div>
          )}

          {view === "fix" && (
            <div className="rm-bundles">
              {(bQ.data?.bundles ?? []).map((b) => (
                <BundleCard key={b.fix_key} bundle={b} api={api} engagementId={engId}
                            open={openKey === b.fix_key} highlight={focusFix === b.fix_key}
                            onToggle={() => setOpenKey((k) => (k === b.fix_key ? null : b.fix_key))} />
              ))}
            </div>
          )}

          {view === "host" && (
            <div className="rm-table-wrap">
              <table className="rm-table">
                <thead><tr><th>Host</th><th>IP</th><th>OS</th><th>Open fixes</th><th>Next due (IST)</th><th>Fixes</th></tr></thead>
                <tbody>
                  {(bQ.data?.hosts ?? []).map((h) => (
                    <tr key={h.ip}>
                      <td><strong>{h.host}</strong></td>
                      <td>{h.ip}</td>
                      <td>{h.os}</td>
                      <td>{h.open_count}</td>
                      <td>{fmtIst(h.next_due_at)}</td>
                      <td>
                        <div className="rm-chips">
                          {h.bundles.map((b) => (
                            <button key={b.fix_key} type="button" className="rm-chip" title={`${b.title} — ${b.target_state}`}
                                    onClick={() => { setView("fix"); setOpenKey(b.fix_key); }}>
                              <span className="rm-host-status" data-status={b.status}>{b.ref}</span>
                              {b.status !== "closed" && b.due_at ? ` · ${fmtIst(b.due_at)}` : ""}
                            </button>
                          ))}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </DataState>
      </div>
    </Shell>
  );
}
