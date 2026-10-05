"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, FileText, Printer } from "lucide-react";

import { PageShell } from "../../components/PageShell";
import { PortalReportsWorkspace } from "../portal/reports/workspace";
import { AiReportPanel } from "../../components/report/AiReportPanel";
import { CanonicalReportDocument } from "../../components/report/CanonicalReportDocument";
import { ReportExportMenu } from "../../components/report/ReportExportMenu";
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
      subtitle="Canonical evidence report — complete live operator draft"
      headerActions={
        <div className="report-export-control no-print">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => window.print()}
            disabled={!report}
          >
            <Printer size={14} />Print complete draft
          </button>
          <ReportExportMenu engagementId={report?.engagement.id} disabled={!report || loading} />
        </div>
      }
    >
      <div className="reports-beta-banner no-print">
        <AlertTriangle size={14} />
        <div>
          <strong>Live, non-persisted operator draft</strong>
          <span>
            Every section below comes from the current canonical record. Missing evidence, closure proof,
            metadata, and compliance mappings remain visible gaps. Review before customer delivery.
          </span>
        </div>
      </div>

      <div className="report-controls no-print">
        <label>
          <span>Engagement</span>
          <select value={engagementId} onChange={(event) => setSelectedId(event.target.value)}>
            {engagements.map((engagement) => (
              <option key={engagement.id} value={engagement.id}>
                {engagement.name}{engagement.client ? ` · ${engagement.client}` : ""}
              </option>
            ))}
          </select>
        </label>
        {reportQ.isFetching && !reportQ.isLoading && (
          <span role="status" aria-live="polite">Refreshing canonical record…</span>
        )}
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
