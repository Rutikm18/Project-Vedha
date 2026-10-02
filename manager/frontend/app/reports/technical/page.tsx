"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Printer } from "lucide-react";

import { PageShell } from "../../../components/PageShell";
import { TechnicalFindingsReport } from "../../../components/report/TechnicalFindingsReport";
import { fetchJson, isUnauthorized } from "../../../lib/fetcher";
import type { ReportDocument } from "../../../lib/report/report-document";

interface EngagementOption { id: string; name: string; client?: string | null; }
interface EngagementList { engagements: EngagementOption[]; }

export default function TechnicalReportPage() {
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
    <PageShell title="Technical findings report" subtitle="Audience-tuned technical deliverable">
      <div className="report-controls no-print" style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap", marginBottom: 12 }}>
        <select value={engagementId} onChange={(e) => setSelectedId(e.target.value)} aria-label="Engagement">
          {engagements.map((e) => <option key={e.id} value={e.id}>{e.name}</option>)}
        </select>
        <button type="button" className="btn btn-secondary" onClick={() => window.print()} disabled={!report}>
          <Printer size={14} aria-hidden /> Print / PDF
        </button>
      </div>
      {loading ? (
        <p className="cr-missing">Loading the technical report…</p>
      ) : error ? (
        <p className="cr-missing">Could not load the report. {isUnauthorized(error) ? "Sign in and retry." : ""}</p>
      ) : report ? (
        <TechnicalFindingsReport report={report} />
      ) : (
        <p className="cr-missing">Select an engagement to generate its technical report.</p>
      )}
    </PageShell>
  );
}
