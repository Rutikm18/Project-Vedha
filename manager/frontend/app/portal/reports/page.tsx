"use client";

import React, { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  FileText, Download, Loader2, ShieldAlert, BarChart3, FileArchive, Printer,
} from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { Timestamp } from "../../../components/portal/Timestamp";
import { DataState, SkeletonRows, EmptyState } from "../../../components/states/DataState";
import {
  portalApi, SEVERITY_VAR, GRADE_VAR,
  type PortalEngagement, type PortalSummary, type PortalTrends, type PortalFinding, type PortalReport,
} from "../../../lib/portal-client";

interface ReportContent extends PortalReport { content: string; }

type Tab = "executive" | "findings" | "documents";
const TABS: Array<{ id: Tab; label: string; icon: React.ElementType }> = [
  { id: "executive", label: "Executive", icon: BarChart3 },
  { id: "findings", label: "Findings", icon: FileText },
  { id: "documents", label: "Documents", icon: FileArchive },
];

const SEVS = ["critical", "high", "medium", "low", "info"] as const;
const SEV_ORDER: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };

function fmtDate(v?: string | null) {
  if (!v) return "Not recorded";
  const d = new Date(v);
  return Number.isNaN(d.getTime()) ? "Not recorded"
    : new Intl.DateTimeFormat("en", { dateStyle: "medium" }).format(d);
}

function Metric({ label, value, detail, tone = "var(--accent)" }: {
  label: string; value: string | number; detail: string; tone?: string;
}) {
  return (
    <article className="report-metric" style={{ "--report-tone": tone } as React.CSSProperties}>
      <small>{label}</small><strong>{value}</strong><span>{detail}</span>
    </article>
  );
}

function SeverityStrip({ bySeverity }: { bySeverity: Record<string, number> }) {
  const values = SEVS.filter((s) => s !== "info").map((severity) => ({ severity, count: bySeverity[severity] ?? 0 }));
  const denom = Math.max(1, values.reduce((sum, v) => sum + v.count, 0));
  return (
    <div className="report-severity">
      <div className="report-severity-bar" aria-label="Open findings by severity">
        {values.filter((v) => v.count > 0).map((v) => (
          <span key={v.severity} title={`${v.severity}: ${v.count}`}
            style={{ width: `${(v.count / denom) * 100}%`, background: SEVERITY_VAR[v.severity] }} />
        ))}
      </div>
      <div className="report-severity-key">
        {values.map((v) => (
          <span key={v.severity}><i style={{ background: SEVERITY_VAR[v.severity] }} />
            <span style={{ textTransform: "capitalize" }}>{v.severity}</span> <strong>{v.count}</strong></span>
        ))}
      </div>
    </div>
  );
}

function TopFindings({ findings }: { findings: PortalFinding[] }) {
  if (!findings.length) return <p className="report-missing">No open findings are recorded for your engagement.</p>;
  return (
    <div className="report-table-wrap">
      <table className="report-table">
        <thead><tr><th>Risk</th><th>Finding</th><th>CVSS</th><th>Status</th></tr></thead>
        <tbody>
          {findings.slice(0, 10).map((f) => (
            <tr key={f.id}>
              <td><span className="report-severity-pill" style={{ color: SEVERITY_VAR[f.severity], textTransform: "capitalize" }}>{f.severity}</span><small>{f.risk_score ?? "—"}</small></td>
              <td><strong>{f.title}</strong>{f.cve_ids?.length ? <small>{f.cve_ids.join(", ")}</small> : null}</td>
              <td>{f.cvss_score ?? "—"}</td>
              <td style={{ textTransform: "capitalize" }}>{f.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ExecutiveDoc({ summary, trends, findings }: {
  summary: PortalSummary; trends: PortalTrends; findings: PortalFinding[];
}) {
  const p = summary.posture;
  const openCrit = summary.severity_counts?.critical ?? 0;
  const openHigh = summary.severity_counts?.high ?? 0;
  const posture = openCrit > 0 ? "Immediate action required"
    : openHigh > 0 ? "Elevated risk"
    : summary.open_findings > 0 ? "Managed attention required"
    : "No open findings recorded";
  const priorities = [
    openCrit > 0 ? `Assign owners and remediation dates to ${openCrit} critical finding${openCrit === 1 ? "" : "s"}.` : null,
    openHigh > 0 ? `Prioritise ${openHigh} high-severity finding${openHigh === 1 ? "" : "s"} in the current cycle.` : null,
    summary.pending_requests > 0 ? `${summary.pending_requests} scan request${summary.pending_requests === 1 ? "" : "s"} awaiting your security team's approval.` : null,
    summary.open_findings > 0 ? "Retest and verify remediations before findings are closed." : "No open findings — maintain posture with periodic scans.",
  ].filter(Boolean) as string[];

  const top = [...findings]
    .filter((f) => f.status === "open" || f.status === "confirmed")
    .sort((a, b) => (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9) || (b.risk_score ?? 0) - (a.risk_score ?? 0));

  return (
    <>
      <section className="report-hero">
        <div>
          <small>EXECUTIVE RISK POSITION</small>
          <h2>{posture}</h2>
          <p>This view summarises your engagement&apos;s current recorded findings and posture. It does not assert that untested assets are secure.</p>
        </div>
        <ShieldAlert size={30} />
      </section>

      <div className="report-metric-grid">
        <Metric label="Posture grade" value={p.grade || "—"} detail={`Score ${p.posture_score ?? 0}/100`}
          tone={GRADE_VAR[p.grade] ?? "var(--accent)"} />
        <Metric label="Risk index" value={p.risk_index ?? 0} detail="0 low · 100 high" tone="var(--sev-high-color)" />
        <Metric label="Open findings" value={summary.open_findings ?? 0} detail="Awaiting remediation" tone="var(--sev-critical-color)" />
        <Metric label="Closed findings" value={summary.closed_findings ?? 0} detail="Verified / remediated" tone="var(--nominal-color)" />
      </div>

      <section className="report-section">
        <header><div><small>RISK DISTRIBUTION</small><h3>Open findings by severity</h3></div></header>
        <SeverityStrip bySeverity={trends.by_severity} />
      </section>

      <section className="report-section">
        <header><div><small>DECISION QUEUE</small><h3>Priority actions</h3></div></header>
        <ol className="report-priorities">{priorities.map((item) => <li key={item}>{item}</li>)}</ol>
      </section>

      <section className="report-section">
        <header><div><small>TOP EXPOSURES</small><h3>Highest-risk open findings</h3></div><span>Showing up to 10</span></header>
        <TopFindings findings={top} />
      </section>
    </>
  );
}

function DocumentsTab({ reports, onView, loadingId }: {
  reports: PortalReport[]; onView: (id: string, el: HTMLElement) => void; loadingId: string | null;
}) {
  if (!reports.length) {
    return <div className="panel"><EmptyState icon={FileArchive} title="No documents yet"
      hint="Approved assessment reports for your engagement will appear here." /></div>;
  }
  return (
    <div className="panel">
      {reports.map((r) => (
        <div key={r.id} className="console-row" style={{ display: "flex", alignItems: "center",
          justifyContent: "space-between", padding: "12px 16px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <FileText style={{ width: 20, height: 20, color: "var(--accent)" }} />
            <div>
              <div style={{ fontSize: 13, fontWeight: 500, textTransform: "capitalize", color: "var(--text-primary)" }}>
                {r.output_type.replace(/_/g, " ")}
              </div>
              <div style={{ fontSize: 11, color: "var(--text-muted)" }}>
                <Timestamp value={r.generated_at} relative /> · {r.model}
              </div>
            </div>
          </div>
          <button onClick={(e) => onView(r.id, e.currentTarget)} disabled={loadingId === r.id}
            aria-label={`View ${r.output_type.replace(/_/g, " ")} report`} className="btn btn-ghost">
            {loadingId === r.id ? <Loader2 className="animate-spin" style={{ width: 16, height: 16 }} />
              : <Download style={{ width: 16, height: 16 }} />}
            View
          </button>
        </div>
      ))}
    </div>
  );
}

export default function PortalReports() {
  const [tab, setTab] = useState<Tab>("executive");
  const [open, setOpen] = useState<ReportContent | null>(null);
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const triggerRef = useRef<HTMLElement | null>(null);

  const eng = useQuery({ queryKey: ["portal", "engagement"], queryFn: () => portalApi<PortalEngagement>("/engagement") });
  const summary = useQuery({ queryKey: ["portal", "summary"], queryFn: () => portalApi<PortalSummary>("/summary") });
  const trends = useQuery({ queryKey: ["portal", "trends"], queryFn: () => portalApi<PortalTrends>("/trends") });
  const findings = useQuery({ queryKey: ["portal", "findings"], queryFn: () => portalApi<PortalFinding[]>("/findings") });
  const reports = useQuery({ queryKey: ["portal", "reports"], queryFn: () => portalApi<PortalReport[]>("/reports") });

  useEffect(() => {
    if (!open) return;
    dialogRef.current?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(null); };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open]);

  const closeModal = () => { setOpen(null); triggerRef.current?.focus(); };

  async function view(id: string, el: HTMLElement) {
    triggerRef.current = el;
    setLoadingId(id);
    try { setOpen(await portalApi<ReportContent>(`/reports/${id}`)); }
    finally { setLoadingId(null); }
  }

  const loading = eng.isLoading || summary.isLoading || trends.isLoading;
  const error = eng.error || summary.error || trends.error;

  const printAction = (
    <button className="btn btn-secondary no-print" onClick={() => window.print()}>
      <Printer style={{ width: 14, height: 14 }} /> Print / PDF
    </button>
  );

  return (
    <PortalShell title="Reports" subtitle="Your assessment deliverables" headerActions={printAction}>
      <div className="report-controls no-print" role="tablist" aria-label="Report view">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button key={id} role="tab" aria-selected={tab === id} data-active={tab === id} onClick={() => setTab(id)}>
            <Icon size={14} />{label}
          </button>
        ))}
      </div>

      {tab === "documents" ? (
        <DataState
          loading={reports.isLoading}
          error={reports.error}
          isEmpty={(reports.data ?? []).length === 0}
          onRetry={() => reports.refetch()}
          onLogin={() => { window.location.href = "/portal/login"; }}
          skeleton={<div className="panel" style={{ padding: 16 }}><SkeletonRows rows={4} /></div>}
          empty={<div className="panel"><EmptyState icon={FileArchive} title="No documents yet"
            hint="Approved assessment reports for your engagement will appear here." /></div>}
        >
          <DocumentsTab reports={reports.data ?? []} onView={view} loadingId={loadingId} />
        </DataState>
      ) : (
        <DataState
          loading={loading}
          error={error}
          isEmpty={!eng.data || !summary.data || !trends.data}
          onRetry={() => { eng.refetch(); summary.refetch(); trends.refetch(); findings.refetch(); }}
          onLogin={() => { window.location.href = "/portal/login"; }}
          skeleton={<SkeletonRows rows={5} height={92} />}
          empty={<div className="panel"><EmptyState icon={FileText} title="No engagement data yet"
            hint="Report figures appear once your engagement has recorded data." /></div>}
        >
          {eng.data && summary.data && trends.data && (
            <div className="report-document">
              <header className="report-cover">
                <div>
                  <span><BarChart3 size={15} /> LIVE DATA</span>
                  <h1>{eng.data.name}</h1>
                  <p>Security Assessment · Customer view</p>
                </div>
                <dl>
                  <div><dt>Status</dt><dd style={{ textTransform: "capitalize" }}>{eng.data.status}</dd></div>
                  <div><dt>Scope</dt><dd>{eng.data.scope_cidr_count} range{eng.data.scope_cidr_count === 1 ? "" : "s"}</dd></div>
                  <div><dt>Generated</dt><dd>{fmtDate(new Date().toISOString())}</dd></div>
                </dl>
              </header>
              <div className="report-boundary">
                <FileText size={17} /><div><strong>Evidence boundary</strong><span>
                  Figures reflect your engagement&apos;s currently recorded findings. Missing data is stated explicitly rather than assumed secure.
                </span></div>
              </div>

              {tab === "executive" && (
                <ExecutiveDoc summary={summary.data} trends={trends.data} findings={findings.data ?? []} />
              )}
              {tab === "findings" && (
                <section className="report-section">
                  <header><div><small>ALL FINDINGS</small><h3>Recorded findings, risk-ranked</h3></div>
                    <span>{(findings.data ?? []).length} total</span></header>
                  <TopFindings findings={[...(findings.data ?? [])].sort(
                    (a, b) => (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9) || (b.risk_score ?? 0) - (a.risk_score ?? 0),
                  ).slice(0, 25)} />
                </section>
              )}

              <footer className="report-footer"><FileText size={13} /> Generated from your Vedha engagement records · Human review recommended</footer>
            </div>
          )}
        </DataState>
      )}

      {open && (
        <div onClick={closeModal} style={{ position: "fixed", inset: 0, zIndex: 50,
          display: "flex", alignItems: "center", justifyContent: "center",
          background: "var(--modal-backdrop)", padding: 16 }}>
          <div ref={dialogRef} role="dialog" aria-modal="true"
            aria-label={`${open.output_type.replace(/_/g, " ")} report`} tabIndex={-1}
            onClick={(e) => e.stopPropagation()} className="panel animate-scale-in"
            style={{ display: "flex", maxHeight: "80vh", width: "100%", maxWidth: 768,
              flexDirection: "column", outline: "none" }}>
            <div className="panel-head" style={{ justifyContent: "space-between" }}>
              <div className="panel-title" style={{ textTransform: "capitalize" }}>
                {open.output_type.replace(/_/g, " ")}
              </div>
              <button onClick={closeModal} aria-label="Close report"
                style={{ color: "var(--text-muted)", background: "none", border: "none",
                  cursor: "pointer", fontSize: 14 }}>✕</button>
            </div>
            <pre style={{ overflow: "auto", whiteSpace: "pre-wrap", padding: "16px 18px",
              fontSize: 13, color: "var(--text-secondary)", fontFamily: "var(--font-mono)" }}>
              {open.content}
            </pre>
          </div>
        </div>
      )}
    </PortalShell>
  );
}
