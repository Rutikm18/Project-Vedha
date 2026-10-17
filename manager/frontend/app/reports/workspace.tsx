"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { AlertTriangle, FileText, LockKeyhole } from "lucide-react";

import { PageShell } from "../../components/PageShell";
import { PortalReportsWorkspace } from "../portal/reports/workspace";
import { AiReportPanel } from "../../components/report/AiReportPanel";
import { CanonicalReportDocument } from "../../components/report/CanonicalReportDocument";
import { FindingSelectionPanel } from "../../components/report/FindingSelectionPanel";
import { ReportExportMenu, type ReportPrintMode } from "../../components/report/ReportExportMenu";
import { DataState, EmptyState, SkeletonRows } from "../../components/states/DataState";
import { fetchJson, isUnauthorized } from "../../lib/fetcher";
import { findingRefs } from "../../lib/report/presentation";
import { isStrictSubset, selectionKey } from "../../lib/report/selection";
import type { ReportDocument } from "../../lib/report/report-document";

/** Debounce a changing value so rapid selection toggles don't refetch per click. */
function useDebounced<T>(value: T, ms: number): T {
  const [settled, setSettled] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setSettled(value), ms);
    return () => clearTimeout(timer);
  }, [value, ms]);
  return settled;
}

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

  // The whole engagement: the selection picker's finding list and the default view.
  const fullReportQ = useQuery({
    queryKey: ["canonical-report-document", engagementId],
    queryFn: () => fetchJson<ReportDocument>(
      `/api/engagements/${encodeURIComponent(engagementId)}/report-document`,
    ),
    enabled: Boolean(engagementId),
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });
  const fullReport = fullReportQ.data;

  // Per-session finding selection. Defaults to all; resets when the engagement changes.
  const allFindingIds = useMemo(
    () => (fullReport ? fullReport.findings.map((f) => f.id) : []),
    [fullReport],
  );
  const total = allFindingIds.length;
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const initedFor = useRef<string>("");
  useEffect(() => {
    if (fullReport && initedFor.current !== engagementId) {
      setSelected(new Set(allFindingIds));
      initedFor.current = engagementId;
    }
  }, [fullReport, engagementId, allFindingIds]);

  const subset = isStrictSubset(selected, total);
  const noneSelected = total > 0 && selected.size === 0;
  const scopeKey = subset ? selectionKey(selected) : "";
  const appliedKey = useDebounced(scopeKey, 300);

  // The scoped document: Manager recomputes the summary, roll-ups and findings for
  // the subset, so every surface stays consistent. Only a strict subset is fetched;
  // all-selected reuses the full report (param omitted, cached).
  const scopedQ = useQuery({
    queryKey: ["canonical-report-document", engagementId, appliedKey],
    queryFn: () => fetchJson<ReportDocument>(
      `/api/engagements/${encodeURIComponent(engagementId)}/report-document?finding_ids=${encodeURIComponent(appliedKey)}`,
    ),
    enabled: Boolean(engagementId) && appliedKey.length > 0,
    placeholderData: keepPreviousData,
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });

  const report = subset ? (scopedQ.data ?? fullReport) : fullReport;
  const refs = useMemo(
    () => (fullReport ? findingRefs(fullReport) : new Map<string, string>()),
    [fullReport],
  );
  const selectedIds = useMemo(() => Array.from(selected), [selected]);
  const loading = engagementsQ.isLoading || (Boolean(engagementId) && fullReportQ.isLoading);
  const error = engagementsQ.error || fullReportQ.error;
  const scoping = subset && scopedQ.isFetching;

  return (
    <PageShell
      title="Reports"
      subtitle="Vulnerability assessment report"
      headerActions={
        <ReportExportMenu
          engagementId={report?.engagement.id}
          disabled={!report || loading || noneSelected}
          findingIds={subset ? selectedIds : undefined}
          onPrint={printReport}
        />
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
          {scoping ? <span>Scoping to selected findings…</span>
            : fullReportQ.isFetching && !fullReportQ.isLoading ? <span>Refreshing the record…</span> : null}
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
          if (engagementId) void fullReportQ.refetch();
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
              {fullReport && (
                <FindingSelectionPanel
                  findings={fullReport.findings}
                  refs={refs}
                  selected={selected}
                  onChange={setSelected}
                />
              )}

              {noneSelected ? (
                <div className="report-scope-note" data-tone="empty" role="status">
                  <AlertTriangle size={14} />
                  <span>
                    No findings selected. Choose at least one finding above — export, print and the
                    AI draft are disabled until something is selected.
                  </span>
                </div>
              ) : subset ? (
                <div className="report-scope-note" data-tone="scoped" role="status">
                  <FileText size={14} />
                  <span>
                    This report is scoped to <strong>{selected.size}</strong> of {total} findings.
                    Metrics, exports and the AI draft reflect only the selected findings.
                  </span>
                </div>
              ) : null}

              <AiReportPanel
                key={report.engagement.id}
                engagementId={report.engagement.id}
                findingCount={noneSelected ? 0 : report.summary.total_findings}
                selectedFindingIds={subset ? selectedIds : undefined}
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
