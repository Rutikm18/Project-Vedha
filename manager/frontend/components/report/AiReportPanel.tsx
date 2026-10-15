"use client";

import React, { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  AlertTriangle,
  CheckCircle2,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Zap,
} from "lucide-react";

import { fetchJson, isUnauthorized } from "../../lib/fetcher";

interface AiReportJobStart {
  job_id: string;
  jobId?: string;
  status: string;
}

interface AiReportJobStatus {
  status: string;
  progress?: number;
  result?: {
    stage?: string;
    error?: string;
    sections?: number;
  };
}

interface AiReportDraft {
  id: string;
  output_type: string;
  finding_id?: string | null;
  model: string;
  output: string;
  review_status: string;
  validation?: {
    valid?: boolean;
    confidence?: number;
    issues?: string[];
  } | null;
  generated_at: string;
}

interface AiReportDraftList {
  count?: number;
  sections?: AiReportDraft[];
  drafts?: AiReportDraft[];
  pendingReview?: number;
}

function reportStatusActive(status?: string): boolean {
  return status === "queued" || status === "pending" || status === "running";
}

function reportSectionLabel(value: string): string {
  return value.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatDatetime(value?: string): string {
  if (!value) return "Not recorded";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return `${new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "medium",
    timeZone: "UTC",
  }).format(date)} UTC`;
}

/**
 * Existing review-gated AI workflow. It remains outside the canonical report
 * and is excluded from print: generated prose is never treated as report fact.
 */
export function AiReportPanel({ engagementId, findingCount, selectedFindingIds }: {
  engagementId: string;
  findingCount: number;
  /** When a strict subset is selected, the per-finding write-ups are scoped to these ids. */
  selectedFindingIds?: string[];
}) {
  const [jobId, setJobId] = useState("");

  const draftsQ = useQuery({
    queryKey: ["ai-report-drafts", engagementId],
    queryFn: () => fetchJson<AiReportDraftList>(
      `/api/engagements/${encodeURIComponent(engagementId)}/ai-report/draft`,
    ),
    enabled: Boolean(engagementId),
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });

  const statusQ = useQuery({
    queryKey: ["ai-report-job", engagementId, jobId],
    queryFn: () => fetchJson<AiReportJobStatus>(
      `/api/engagements/${encodeURIComponent(engagementId)}/ai-report/status/${encodeURIComponent(jobId)}`,
    ),
    enabled: Boolean(jobId),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return !status || reportStatusActive(status) ? 2_000 : false;
    },
    retry: (count, error) => !isUnauthorized(error) && count < 2,
  });

  const jobStatus = statusQ.data?.status;
  const refetchDrafts = draftsQ.refetch;
  React.useEffect(() => {
    if (jobStatus === "completed") void refetchDrafts();
  }, [jobStatus, refetchDrafts]);

  const genMut = useMutation({
    mutationFn: () => fetchJson<AiReportJobStart>(
      `/api/engagements/${encodeURIComponent(engagementId)}/ai-report/generate`, {
      method: "POST",
      body: JSON.stringify({
        maxFindings: Math.min(Math.max(findingCount, 1), 50),
        ...(selectedFindingIds && selectedFindingIds.length
          ? { selected_finding_ids: selectedFindingIds }
          : {}),
      }),
    }),
    onSuccess: (job) => setJobId(job.jobId ?? job.job_id),
  });

  const reviewMut = useMutation({
    mutationFn: (action: { kind: "approve" | "reject"; ids?: string[]; feedback?: string }) =>
      fetchJson(`/api/engagements/${encodeURIComponent(engagementId)}/ai-report/${action.kind}`, {
        method: "POST",
        body: JSON.stringify({
          output_ids: action.ids,
          ...(action.kind === "reject" ? { feedback: action.feedback, regenerate: true } : {}),
        }),
      }),
    onSuccess: () => { void refetchDrafts(); },
  });

  function reject(ids: string[]) {
    const feedback = window.prompt("What should change? (the section is regenerated with this feedback)");
    if (feedback && feedback.trim().length >= 3) reviewMut.mutate({ kind: "reject", ids, feedback: feedback.trim() });
  }

  const drafts = draftsQ.data?.drafts ?? draftsQ.data?.sections ?? [];
  const active = genMut.isPending || reportStatusActive(jobStatus);
  const generationError = genMut.error instanceof Error
    ? genMut.error.message
    : reviewMut.error instanceof Error
      ? reviewMut.error.message
      : statusQ.error instanceof Error
      ? statusQ.error.message
      : jobStatus === "failed"
        ? statusQ.data?.result?.error || "Report generation failed."
        : null;

  return (
    <section className="no-print" style={{
      border: "1px solid var(--border-default)", borderRadius: 10,
      background: "color-mix(in srgb, var(--accent) 3%, var(--bg-panel))",
      padding: "14px 16px", marginBottom: 18,
    }} aria-labelledby="ai-report-heading">
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
            <Sparkles size={14} style={{ color: "var(--accent)" }} />
            <strong id="ai-report-heading" style={{ fontSize: 13 }}>AI-assisted report draft</strong>
          </div>
          <p style={{ margin: "4px 0 0 21px", fontSize: 10.5, color: "var(--text-muted)" }}>
            Manager loads canonical engagement records server-side. Generated sections remain internal until human approval.
            {selectedFindingIds && selectedFindingIds.length
              ? ` Write-ups are scoped to the ${selectedFindingIds.length} selected finding${selectedFindingIds.length === 1 ? "" : "s"}.`
              : ""}
          </p>
        </div>
        <button
          className="btn btn-primary"
          style={{ fontSize: 11, padding: "5px 12px", display: "flex", alignItems: "center", gap: 5 }}
          onClick={() => genMut.mutate()}
          disabled={active || findingCount === 0}
        >
          {active ? <RefreshCw size={11} className="spin" /> : <Zap size={11} />}
          {active ? "Generating…" : drafts.length ? "Generate new draft" : "Generate draft"}
        </button>
      </div>

      {active && (
        <div role="status" aria-live="polite" style={{
          display: "flex", alignItems: "center", gap: 8, marginTop: 12,
          padding: "9px 11px", borderRadius: 7, background: "var(--bg-surface)",
          border: "1px solid var(--border-subtle)", fontSize: 11.5, color: "var(--text-secondary)",
        }}>
          <RefreshCw size={13} className="spin" />
          {genMut.isPending
            ? "Authorizing and queuing the report job…"
            : `Manager is generating a review-gated draft${statusQ.data?.progress != null ? ` · ${statusQ.data.progress}%` : "…"}`}
        </div>
      )}

      {generationError && !active && (
        <div role="alert" style={{
          marginTop: 12, display: "flex", gap: 8, alignItems: "flex-start",
          padding: "9px 11px", borderRadius: 7, background: "var(--sev-critical-bg)",
          border: "1px solid var(--sev-critical-color)",
        }}>
          <AlertTriangle size={14} style={{ color: "var(--sev-critical-color)", flexShrink: 0, marginTop: 1 }} />
          <span style={{ fontSize: 11.5, color: "var(--text-primary)" }}>{generationError}</span>
        </div>
      )}

      {jobStatus === "completed" && (
        <div role="status" aria-live="polite" style={{
          marginTop: 12, display: "flex", gap: 8, alignItems: "flex-start",
          padding: "9px 11px", borderRadius: 7, background: "var(--sev-low-bg)",
          border: "1px solid var(--sev-low-color)",
        }}>
          <CheckCircle2 size={14} style={{ color: "var(--sev-low-color)", flexShrink: 0, marginTop: 1 }} />
          <span style={{ fontSize: 11.5, color: "var(--text-primary)" }}>
            Draft generation completed. These sections are pending human review and are not client-visible.
          </span>
        </div>
      )}

      <div style={{ marginTop: 14, borderTop: "1px solid var(--border-subtle)", paddingTop: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 7, marginBottom: drafts.length ? 8 : 0 }}>
          <ShieldCheck size={13} style={{ color: "var(--accent)" }} />
          <strong style={{ fontSize: 11.5 }}>Pending review</strong>
          <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>
            {draftsQ.isLoading ? "Loading…" : `${drafts.length} section${drafts.length === 1 ? "" : "s"}`}
          </span>
          {drafts.length > 0 && (
            <button className="btn" style={{ marginLeft: "auto", fontSize: 11, padding: "3px 10px" }}
              disabled={reviewMut.isPending}
              onClick={() => reviewMut.mutate({ kind: "approve" })}>
              Approve all
            </button>
          )}
        </div>

        {draftsQ.error && (
          <p role="alert" style={{ margin: 0, fontSize: 11.5, color: "var(--sev-high-color)" }}>
            {draftsQ.error instanceof Error ? draftsQ.error.message : "Pending drafts could not be loaded."}
          </p>
        )}

        {!draftsQ.isLoading && !draftsQ.error && drafts.length === 0 && (
          <p style={{ margin: 0, fontSize: 11.5, color: "var(--text-muted)" }}>
            No generated sections are awaiting review.
          </p>
        )}

        <div style={{ display: "grid", gap: 8 }}>
          {drafts.map((draft) => {
            const invalid = draft.validation?.valid === false;
            return (
              <details key={draft.id} style={{
                border: "1px solid var(--border-subtle)", borderRadius: 7,
                background: "var(--bg-panel)", overflow: "hidden",
              }}>
                <summary style={{
                  display: "flex", alignItems: "center", gap: 8, cursor: "pointer",
                  padding: "9px 11px", fontSize: 11.5, color: "var(--text-primary)",
                }}>
                  <strong>{reportSectionLabel(draft.output_type)}</strong>
                  {invalid && (
                    <span style={{
                      fontSize: 9, fontWeight: 800, color: "var(--sev-critical-color)",
                      border: "1px solid var(--sev-critical-color)", borderRadius: 4, padding: "1px 5px",
                    }}>VALIDATION REVIEW</span>
                  )}
                  <span style={{ marginLeft: "auto", color: "var(--text-muted)", fontSize: 10 }}>
                    {draft.model} · {formatDatetime(draft.generated_at)}
                  </span>
                </summary>
                <pre style={{
                  margin: 0, padding: "11px 12px", maxHeight: 260, overflow: "auto",
                  whiteSpace: "pre-wrap", wordBreak: "break-word", fontFamily: "var(--font-mono)",
                  fontSize: 11, lineHeight: 1.6, color: "var(--text-secondary)",
                  borderTop: "1px solid var(--border-subtle)",
                }}>{draft.output}</pre>
                <div style={{ display: "flex", gap: 8, padding: "8px 12px", borderTop: "1px solid var(--border-subtle)" }}>
                  <button className="btn" style={{ fontSize: 11, padding: "3px 10px" }}
                    disabled={reviewMut.isPending}
                    onClick={() => reviewMut.mutate({ kind: "approve", ids: [draft.id] })}>Approve</button>
                  <button className="btn" style={{ fontSize: 11, padding: "3px 10px" }}
                    disabled={reviewMut.isPending}
                    onClick={() => reject([draft.id])}>Reject &amp; regenerate</button>
                </div>
                {invalid && (draft.validation?.issues?.length ?? 0) > 0 && (
                  <ul style={{ margin: 0, padding: "9px 28px", color: "var(--sev-high-color)", fontSize: 10.5 }}>
                    {draft.validation!.issues!.map((issue) => <li key={issue}>{issue}</li>)}
                  </ul>
                )}
              </details>
            );
          })}
        </div>
      </div>
    </section>
  );
}
