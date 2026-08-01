"use client";

import React, { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Activity, AlertTriangle, BarChart3, CheckCircle2, ClipboardCheck,
  FileSearch, FileText, Fingerprint, Printer, ShieldAlert,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { DataState, EmptyState, SkeletonRows } from "../../components/states/DataState";
import { fetchJson, isUnauthorized } from "../../lib/fetcher";
import { SEV_COLOR, SEV_PALETTE } from "../../lib/severity";

type ReportType = "executive" | "technical" | "evidence" | "compliance";
type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";

interface Engagement {
  id: string;
  name: string;
  client: string;
  status: string;
  startDate: string;
  endDate: string;
  scopeCidrs: string[];
  assessor: string;
  description: string;
  assetCount: number;
  findingCount: number;
  findingsBySeverity: Record<Exclude<Severity, "INFO">, number>;
}

interface Finding {
  id: string;
  title: string;
  severity: Severity;
  status: string;
  affectedHost: string;
  discoveredAt: string;
  description: string;
  technicalDetails: string;
  evidence: Array<{ label: string; content: string }>;
  impact: string;
  remediation: Array<string | { title?: string; description?: string }>;
  mitre: Array<{ id: string; name: string }>;
  riskScore: number;
  cvss: string;
  exploitability?: string;
  activelyExploited: boolean;
  detectionCoverage: string;
}

interface FindingPage {
  items: Finding[];
  total: number;
  page: number;
  pageSize: number;
  pages: number;
}

interface FindingSummary {
  total: number;
  criticalOpen: number;
  validated: number;
  blind: number;
  averageRisk: number;
}

interface ActivityItem {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  detail: string;
  engagementId: string;
}

const REPORT_TABS: Array<{ id: ReportType; label: string; icon: React.ElementType }> = [
  { id: "executive", label: "Executive", icon: BarChart3 },
  { id: "technical", label: "Technical", icon: FileSearch },
  { id: "evidence", label: "Evidence", icon: Fingerprint },
  { id: "compliance", label: "Control evidence", icon: ClipboardCheck },
];

function formatDate(value?: string) {
  if (!value) return "Not recorded";
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? "Not recorded"
    : new Intl.DateTimeFormat("en", { dateStyle: "medium" }).format(date);
}

function plainRemediation(finding: Finding) {
  const first = finding.remediation[0];
  if (typeof first === "string") return first;
  return first?.description || first?.title || "No remediation guidance has been recorded.";
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

function SeverityStrip({ engagement }: { engagement: Engagement }) {
  const values = (["CRITICAL", "HIGH", "MEDIUM", "LOW"] as const).map((severity) => ({
    severity,
    count: engagement.findingsBySeverity[severity] ?? 0,
  }));
  const denominator = Math.max(1, values.reduce((sum, item) => sum + item.count, 0));
  return (
    <div className="report-severity">
      <div className="report-severity-bar" aria-label="Finding severity distribution">
        {values.filter((item) => item.count > 0).map((item) => (
          <span
            key={item.severity}
            title={`${item.severity}: ${item.count}`}
            style={{ width: `${(item.count / denominator) * 100}%`, background: SEV_COLOR[item.severity] }}
          />
        ))}
      </div>
      <div className="report-severity-key">
        {values.map((item) => (
          <span key={item.severity}><i style={{ background: SEV_COLOR[item.severity] }} />{item.severity} <strong>{item.count}</strong></span>
        ))}
      </div>
    </div>
  );
}

function FindingTable({ findings, limit = 10 }: { findings: Finding[]; limit?: number }) {
  if (!findings.length) return <p className="report-missing">No findings have been recorded for this engagement.</p>;
  return (
    <div className="report-table-wrap">
      <table className="report-table">
        <thead><tr><th>Risk</th><th>Finding</th><th>Asset</th><th>Status</th></tr></thead>
        <tbody>
          {findings.slice(0, limit).map((finding) => (
            <tr key={finding.id}>
              <td><span className="report-severity-pill" style={{ color: SEV_COLOR[finding.severity] }}>{finding.severity}</span><small>{finding.riskScore}</small></td>
              <td><strong>{finding.title}</strong><small>{finding.id}</small></td>
              <td>{finding.affectedHost}</td>
              <td>{finding.status.replaceAll("_", " ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ExecutiveReport({ engagement, findings, summary }: {
  engagement: Engagement; findings: Finding[]; summary: FindingSummary;
}) {
  const critical = engagement.findingsBySeverity.CRITICAL ?? 0;
  const high = engagement.findingsBySeverity.HIGH ?? 0;
  const posture = critical > 0 ? "Immediate action required" : high > 0 ? "Elevated risk" : summary.total > 0 ? "Managed attention required" : "No findings recorded";
  const priorities = [
    critical > 0 ? `Assign owners and remediation dates to ${critical} critical finding${critical === 1 ? "" : "s"}.` : null,
    summary.validated > 0 ? `Prioritize ${summary.validated} exploit-validated finding${summary.validated === 1 ? "" : "s"}.` : null,
    summary.blind > 0 ? `Close ${summary.blind} detection coverage gap${summary.blind === 1 ? "" : "s"} exposed during testing.` : null,
    summary.total > 0 ? "Retest remediated findings and retain verification evidence before closure." : "Run an authorized assessment before drawing a security conclusion.",
  ].filter(Boolean) as string[];

  return (
    <>
      <section className="report-hero">
        <div><small>EXECUTIVE RISK POSITION</small><h2>{posture}</h2><p>
          This view summarizes recorded Vedha evidence for <strong>{engagement.name}</strong>. It does not claim that untested assets or controls are secure.
        </p></div>
        <ShieldAlert size={30} />
      </section>
      <div className="report-metric-grid">
        <Metric label="Recorded findings" value={summary.total} detail="Selected engagement" tone={SEV_PALETTE.RED} />
        <Metric label="Critical open" value={summary.criticalOpen} detail="Open or confirmed" tone={SEV_PALETTE.RED} />
        <Metric label="Exploit validated" value={summary.validated} detail="Backed by validation state" tone={SEV_PALETTE.ORANGE} />
        <Metric label="Average risk" value={summary.averageRisk} detail="Composite score · 0–1000" tone={SEV_PALETTE.VIOLET} />
      </div>
      <section className="report-section">
        <header><div><small>RISK DISTRIBUTION</small><h3>Severity profile</h3></div></header>
        <SeverityStrip engagement={engagement} />
      </section>
      <section className="report-section">
        <header><div><small>DECISION QUEUE</small><h3>Priority actions derived from recorded data</h3></div></header>
        <ol className="report-priorities">{priorities.map((item) => <li key={item}>{item}</li>)}</ol>
      </section>
      <section className="report-section">
        <header><div><small>TOP EXPOSURES</small><h3>Highest-risk findings</h3></div><span>Showing up to 10</span></header>
        <FindingTable findings={findings} />
      </section>
    </>
  );
}

function TechnicalReport({ findings, total }: { findings: Finding[]; total: number }) {
  return (
    <section className="report-section">
      <header><div><small>TECHNICAL FINDINGS</small><h3>Verification and remediation detail</h3></div><span>Top {Math.min(25, findings.length)} of {total}</span></header>
      {!findings.length && <p className="report-missing">No technical findings have been recorded.</p>}
      <div className="report-finding-stack">
        {findings.slice(0, 25).map((finding, index) => (
          <article key={finding.id}>
            <header>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <div><small>{finding.id} · {finding.affectedHost}</small><h4>{finding.title}</h4></div>
              <b style={{ color: SEV_COLOR[finding.severity] }}>{finding.severity}</b>
            </header>
            <dl>
              <div><dt>CVSS</dt><dd>{finding.cvss || "Not recorded"}</dd></div>
              <div><dt>Risk score</dt><dd>{finding.riskScore}</dd></div>
              <div><dt>Status</dt><dd>{finding.status.replaceAll("_", " ")}</dd></div>
              <div><dt>Detection</dt><dd>{finding.detectionCoverage}</dd></div>
            </dl>
            <div className="report-copy-grid">
              <div><strong>Description</strong><p>{finding.description || "No description has been recorded."}</p></div>
              <div><strong>Impact</strong><p>{finding.impact || "No impact statement has been recorded."}</p></div>
              <div><strong>Remediation</strong><p>{plainRemediation(finding)}</p></div>
              <div><strong>Evidence</strong><p>{finding.evidence.length ? `${finding.evidence.length} evidence item(s) recorded.` : "No evidence item has been recorded."}</p></div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function EvidenceReport({ findings, activity, total }: {
  findings: Finding[]; activity: ActivityItem[]; total: number;
}) {
  const artifacts = findings.reduce((sum, finding) => sum + finding.evidence.length, 0);
  const withEvidence = findings.filter((finding) => finding.evidence.length > 0).length;
  return (
    <>
      <div className="report-metric-grid">
        <Metric label="Evidence artifacts" value={artifacts} detail={`Across ${findings.length} loaded findings`} />
        <Metric label="Findings with evidence" value={withEvidence} detail={`${Math.max(0, findings.length - withEvidence)} loaded without evidence`} />
        <Metric label="Activity events" value={activity.length} detail="Latest engagement events" />
        <Metric label="Coverage boundary" value={`${findings.length}/${total}`} detail="Loaded / total findings" />
      </div>
      <section className="report-section">
        <header><div><small>EVIDENCE INVENTORY</small><h3>Recorded artifacts</h3></div><span>Values are shown as stored</span></header>
        {!artifacts && <p className="report-missing">No structured finding evidence is recorded in the loaded result set.</p>}
        <div className="report-evidence-grid">
          {findings.flatMap((finding) => finding.evidence.map((item, index) => (
            <article key={`${finding.id}-${item.label}-${index}`}>
              <small>{finding.id} · {finding.severity}</small><strong>{item.label}</strong><pre>{item.content}</pre>
            </article>
          )))}
        </div>
      </section>
      <section className="report-section">
        <header><div><small>AUDIT TRAIL</small><h3>Recent engagement activity</h3></div><span>Latest {activity.length}</span></header>
        {!activity.length && <p className="report-missing">No scan or finding activity is recorded for this engagement.</p>}
        <div className="report-activity">
          {activity.map((item) => (
            <article key={item.id}><Activity size={14} /><div><strong>{item.action}</strong><p>{item.detail}</p></div><time>{formatDate(item.timestamp)}</time></article>
          ))}
        </div>
      </section>
    </>
  );
}

function ComplianceReport({ findings, total }: { findings: Finding[]; total: number }) {
  const techniques = useMemo(() => {
    const map = new Map<string, { name: string; findings: Set<string> }>();
    findings.forEach((finding) => finding.mitre.forEach((technique) => {
      const value = map.get(technique.id) ?? { name: technique.name, findings: new Set<string>() };
      value.findings.add(finding.id);
      map.set(technique.id, value);
    }));
    return [...map.entries()].sort(([a], [b]) => a.localeCompare(b));
  }, [findings]);
  return (
    <>
      <div className="report-boundary report-boundary-warning">
        <AlertTriangle size={17} /><div><strong>No inferred compliance verdicts</strong><span>
          Vedha currently records MITRE ATT&amp;CK references, not assessed NIST, ISO, PCI DSS, or CIS control outcomes. Formal compliance requires an approved control scope, test procedure, and reviewer sign-off.
        </span></div>
      </div>
      <section className="report-section">
        <header><div><small>RECORDED CONTROL EVIDENCE</small><h3>MITRE ATT&amp;CK technique coverage</h3></div><span>{techniques.length} technique(s) · {findings.length}/{total} findings loaded</span></header>
        {!techniques.length && <p className="report-missing">No MITRE ATT&amp;CK references have been recorded for the loaded findings.</p>}
        <div className="report-techniques">
          {techniques.map(([id, value]) => (
            <article key={id}><code>{id}</code><div><strong>{value.name || "Technique name not recorded"}</strong><small>{value.findings.size} linked finding(s)</small></div></article>
          ))}
        </div>
      </section>
    </>
  );
}

export default function ReportsPage() {
  const [selectedId, setSelectedId] = useState("");
  const [reportType, setReportType] = useState<ReportType>("executive");
  const engagementsQuery = useQuery({
    queryKey: ["engagements"],
    queryFn: () => fetchJson<{ engagements: Engagement[] }>("/api/engagements"),
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });
  const engagements = engagementsQuery.data?.engagements ?? [];
  const engagementId = selectedId || engagements[0]?.id || "";
  const engagement = engagements.find((item) => item.id === engagementId);
  const findingsQuery = useQuery({
    queryKey: ["report-findings", engagementId],
    queryFn: () => fetchJson<FindingPage>(`/api/findings?paginated=true&engagement_id=${encodeURIComponent(engagementId)}&page=1&page_size=100&sort=risk`),
    enabled: Boolean(engagementId),
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });
  const summaryQuery = useQuery({
    queryKey: ["findings-summary", engagementId],
    queryFn: () => fetchJson<FindingSummary>(`/api/findings/summary?engagement_id=${encodeURIComponent(engagementId)}`),
    enabled: Boolean(engagementId),
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });
  const activityQuery = useQuery({
    queryKey: ["activity", engagementId],
    queryFn: () => fetchJson<ActivityItem[]>(`/api/activity?engagement_id=${encodeURIComponent(engagementId)}&limit=50`),
    enabled: Boolean(engagementId),
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });
  const findings = findingsQuery.data?.items ?? [];
  const summary = summaryQuery.data ?? {
    total: engagement?.findingCount ?? 0,
    criticalOpen: 0,
    validated: 0,
    blind: 0,
    averageRisk: 0,
  };
  const loading = engagementsQuery.isLoading || (Boolean(engagementId) && (findingsQuery.isLoading || summaryQuery.isLoading));
  const loadError = engagementsQuery.error || findingsQuery.error || summaryQuery.error || activityQuery.error;

  return (
    <PageShell
      title="REPORTS"
      subtitle="ENGAGEMENT-GROUNDED · BETA"
      headerActions={<button className="btn btn-secondary no-print" onClick={() => window.print()} disabled={!engagement}><Printer size={14} /> Print / PDF</button>}
    >
      <div className="reports-beta-banner"><AlertTriangle size={15} /><div><strong>Beta reporting workspace</strong><span>All metrics below come from the selected engagement. Review evidence, wording, and scope before client delivery.</span></div></div>

      <div className="report-controls no-print">
        <label><span>Engagement</span><select value={engagementId} onChange={(event) => setSelectedId(event.target.value)}>
          {engagements.map((item) => <option key={item.id} value={item.id}>{item.name} · {item.client}</option>)}
        </select></label>
        <div role="tablist" aria-label="Report format">
          {REPORT_TABS.map(({ id, label, icon: Icon }) => (
            <button key={id} role="tab" aria-selected={reportType === id} data-active={reportType === id} onClick={() => setReportType(id)}><Icon size={14} />{label}</button>
          ))}
        </div>
      </div>

      <DataState
        loading={loading}
        error={loadError}
        isEmpty={!engagement}
        onRetry={() => { void engagementsQuery.refetch(); void findingsQuery.refetch(); void summaryQuery.refetch(); }}
        skeleton={<SkeletonRows rows={5} height={92} />}
        empty={<EmptyState icon={FileText} title="No engagement available" hint="Create an engagement and collect assessment evidence before generating a report." />}
      >
        {engagement && (
          <main className="report-document">
            <header className="report-cover">
              <div><span><CheckCircle2 size={15} /> LIVE DATA</span><h1>{engagement.name}</h1><p>{engagement.client} · Security Assessment Report</p></div>
              <dl>
                <div><dt>Status</dt><dd>{engagement.status}</dd></div>
                <div><dt>Assessment window</dt><dd>{formatDate(engagement.startDate)} — {formatDate(engagement.endDate)}</dd></div>
                <div><dt>Assessor</dt><dd>{engagement.assessor || "Not recorded"}</dd></div>
                <div><dt>Scope</dt><dd>{engagement.scopeCidrs.length ? engagement.scopeCidrs.join(", ") : "Not recorded"}</dd></div>
              </dl>
            </header>
            <div className="report-boundary">
              <FileText size={17} /><div><strong>Evidence boundary</strong><span>
                Findings are ranked by stored risk. Detailed sections load up to 100 of {summary.total} findings; aggregate metrics cover the full selected engagement. Missing data is stated explicitly.
              </span></div>
            </div>
            {reportType === "executive" && <ExecutiveReport engagement={engagement} findings={findings} summary={summary} />}
            {reportType === "technical" && <TechnicalReport findings={findings} total={summary.total} />}
            {reportType === "evidence" && <EvidenceReport findings={findings} activity={activityQuery.data ?? []} total={summary.total} />}
            {reportType === "compliance" && <ComplianceReport findings={findings} total={summary.total} />}
            <footer className="report-footer"><FileText size={13} /> Generated from Vedha live engagement records · Beta · Human review required</footer>
          </main>
        )}
      </DataState>
    </PageShell>
  );
}
