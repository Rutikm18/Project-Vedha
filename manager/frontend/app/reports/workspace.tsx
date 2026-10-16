"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { FileText, LockKeyhole } from "lucide-react";

import { PageShell } from "../../components/PageShell";
import { PortalReportsWorkspace } from "../portal/reports/workspace";
import { AiReportPanel } from "../../components/report/AiReportPanel";
import { CanonicalReportDocument } from "../../components/report/CanonicalReportDocument";
import { ReportExportMenu, type ReportPrintMode } from "../../components/report/ReportExportMenu";
import { DataState, EmptyState, SkeletonRows } from "../../components/states/DataState";
import { fetchJson, isUnauthorized } from "../../lib/fetcher";
import type { ReportDocument } from "../../lib/report/report-document";

interface EngagementOption {
  id: string;
  name: string;
  client?: string | null;
}
interface EngagementList {
  engagements: EngagementOption[];
}

/**
 * Print the report as the customer copy (complete records collapsed, operator
 * readiness check left out) or as the complete record (every disclosure open).
 * Large reports render records on first open, so give React a moment.
 */
function printReport(mode: ReportPrintMode) {
  const root = document.querySelector<HTMLElement>(".rr-report");
  if (!root) return;
  root.dataset.print = mode;
  root.querySelectorAll<HTMLDetailsElement>("details").forEach((d) => {
    // Every affected asset prints; complete records only in the full copy.
    d.open = mode === "full" || d.classList.contains("rr-more-assets");
  });
  window.setTimeout(() => window.print(), mode === "full" ? 400 : 50);
}

function CanonicalReportsWorkspace() {
  const [selectedId, setSelectedId] = useState("");

  const engagementsQ = useQuery({
    queryKey: ["engagements"],
    queryFn: () => fetchJson<EngagementList>("/api/engagements"),
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });
  const engagements = engagementsQ.data?.engagements ?? [];
  const engagementId = selectedId || engagements[0]?.id || "";

  const reportQ = useQuery({
    queryKey: ["canonical-report-document", engagementId],
    queryFn: () => fetchJson<ReportDocument>(
      `/api/engagements/${encodeURIComponent(engagementId)}/report-document`,
    ),
    enabled: Boolean(engagementId),
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });

  const report = reportQ.data;
  const loading = engagementsQ.isLoading || (Boolean(engagementId) && reportQ.isLoading);
  const error = engagementsQ.error || reportQ.error;

  return (
    <PageShell
      title="Reports"
      subtitle="Vulnerability assessment report"
      headerActions={
        <ReportExportMenu engagementId={report?.engagement.id} disabled={!report || loading} onPrint={printReport} />
      }
    >
      <style>{STYLES}</style>
      <div className="rpt-bar no-print">
        <label className="rpt-pick">
          <span>Engagement</span>
          <select value={engagementId} onChange={(event) => setSelectedId(event.target.value)}>
            {engagements.map((engagement) => (
              <option key={engagement.id} value={engagement.id}>
                {engagement.name}{engagement.client ? ` · ${engagement.client}` : ""}
              </option>
            ))}
          </select>
        </label>
        <div className="rpt-state" role="status" aria-live="polite">
          <span className="rpt-chip"><LockKeyhole size={12} aria-hidden /> Live draft · not saved</span>
          {reportQ.isFetching && !reportQ.isLoading && <span>Refreshing the record…</span>}
        </div>
        <p className="rpt-note">
          Built from the engagement&apos;s current record. Missing evidence, closure proof, metadata and
          compliance mappings stay visible as gaps. Review before delivery to the customer.
        </p>
      </div>

      <DataState
        loading={loading}
        error={error}
        isEmpty={!engagementId || (!loading && !error && !report)}
        onRetry={() => {
          void engagementsQ.refetch();
          if (engagementId) void reportQ.refetch();
        }}
        skeleton={<SkeletonRows rows={6} height={92} />}
        empty={
          <EmptyState
            icon={FileText}
            title="No engagement report available"
            hint="Create an engagement and record assessment findings before opening the live report draft."
          />
        }
      >
        {report && (
          <>
            <div className="no-print" style={{ width: "min(1180px, 100%)", margin: "0 auto" }}>
              <AiReportPanel
                key={report.engagement.id}
                engagementId={report.engagement.id}
                findingCount={report.summary.total_findings}
              />
            </div>
            <CanonicalReportDocument report={report} />
          </>
        )}
      </DataState>
    </PageShell>
  );
}

const STYLES = `
.rpt-bar { display: grid; grid-template-columns: minmax(0, 420px) 1fr; align-items: end; gap: 6px 16px; width: min(1180px, 100%); margin: 0 auto 14px; }
.rpt-pick { display: grid; gap: 5px; min-width: 0; }
.rpt-pick > span { color: var(--text-muted); font: 650 10.5px/1.2 var(--font-ui); text-transform: uppercase; letter-spacing: .05em; }
.rpt-pick select { width: 100%; min-width: 0; min-height: 38px; padding: 0 10px; border: var(--hairline) solid var(--border-default); border-radius: 8px; background: var(--bg-panel); color: var(--text-primary); font: 500 13px/1.2 var(--font-ui); text-overflow: ellipsis; }
.rpt-state { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; min-height: 38px; color: var(--text-muted); font: 500 12px/1.3 var(--font-ui); }
.rpt-chip { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 999px; border: var(--hairline) solid var(--sev-medium-edge, var(--border-default)); background: var(--sev-medium-bg, transparent); color: var(--sev-medium-color); font: 650 11.5px/1.2 var(--font-ui); }
.rpt-note { grid-column: 1 / -1; margin: 0; max-width: 90ch; color: var(--text-muted); font: 500 12px/1.5 var(--font-ui); }
@media (max-width: 720px) {
  .rpt-bar { grid-template-columns: minmax(0, 1fr); }
  .rpt-pick select { min-height: 44px; }
  .rpt-state { min-height: 0; }
}
`;

export function ReportsWorkspace({ surface = "manager" }: {
  surface?: "manager" | "portal";
}) {
  return surface === "portal"
    ? <PortalReportsWorkspace />
    : <CanonicalReportsWorkspace />;
}

export default function ReportsPage() {
  return <ReportsWorkspace surface="manager" />;
}
