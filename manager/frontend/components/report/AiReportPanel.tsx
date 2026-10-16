"use client";

import React, { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
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
export function AiReportPanel({ engagementId, findingCount }: {
  engagementId: string;
  findingCount: number;
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

  // Collapsed to one line until something needs a person: a draft awaiting review, a running
  // job, or an error. The report itself is what the page is for.
  const needsAttention = drafts.length > 0 || active || Boolean(generationError) || jobStatus === "completed";
  const [chosen, setChosen] = useState<boolean | null>(null);
  const expanded = chosen ?? needsAttention;

  const summary = draftsQ.isLoading ? "Loading…"
    : active ? "Generating a review-gated draft…"
    : drafts.length ? `${drafts.length} section${drafts.length === 1 ? "" : "s"} awaiting review`
    : "No sections awaiting review";

  return (
    <section className="arp no-print" aria-labelledby="ai-report-heading">
      <style>{STYLES}</style>
      <div className="arp-head">
        <button type="button" className="arp-toggle" aria-expanded={expanded} aria-controls="arp-body"
          onClick={() => setChosen(!expanded)}>
          <Sparkles size={14} aria-hidden />
          <span>
            <strong id="ai-report-heading">AI-assisted report draft</strong>
            <small data-attention={drafts.length > 0 || undefined}>{summary}</small>
          </span>
          <ChevronDown size={14} aria-hidden className="arp-chev" />
        </button>
        <button
          type="button"
          className="btn btn-primary arp-generate"
          onClick={() => genMut.mutate()}
          disabled={active || findingCount === 0}
          title={findingCount === 0 ? "Record at least one finding first" : undefined}
        >
          {active ? <RefreshCw size={12} className="spin" aria-hidden /> : <Zap size={12} aria-hidden />}
          {active ? "Generating…" : drafts.length ? "Generate new draft" : "Generate draft"}
        </button>
      </div>

      {expanded && (
        <div id="arp-body" className="arp-body">
          <p className="arp-lead">
            Drafts are written from the engagement&apos;s recorded findings. They stay internal, and out of the
            report and any export, until a person approves them.
          </p>

          {active && (
            <div role="status" aria-live="polite" className="arp-note">
              <RefreshCw size={13} className="spin" aria-hidden />
              {genMut.isPending
                ? "Authorizing and queuing the report job…"
                : `Generating a review-gated draft${statusQ.data?.progress != null ? ` · ${statusQ.data.progress}%` : "…"}`}
            </div>
          )}

          {generationError && !active && (
            <div role="alert" className="arp-note" data-tone="error">
              <AlertTriangle size={14} aria-hidden />
              <span>{generationError}</span>
            </div>
          )}

          {jobStatus === "completed" && !active && (
            <div role="status" aria-live="polite" className="arp-note" data-tone="ok">
              <CheckCircle2 size={14} aria-hidden />
              <span>Draft generation completed. These sections are pending human review and are not client-visible.</span>
            </div>
          )}

          <div className="arp-review">
            <div className="arp-review-head">
              <ShieldCheck size={13} aria-hidden />
              <strong>Pending review</strong>
              <span>{draftsQ.isLoading ? "Loading…" : `${drafts.length} section${drafts.length === 1 ? "" : "s"}`}</span>
              {drafts.length > 0 && (
                <button type="button" className="btn arp-small" disabled={reviewMut.isPending}
                  onClick={() => reviewMut.mutate({ kind: "approve" })}>
                  Approve all
                </button>
              )}
            </div>

            {draftsQ.error && (
              <p role="alert" className="arp-error">
                {draftsQ.error instanceof Error ? draftsQ.error.message : "Pending drafts could not be loaded."}
              </p>
            )}

            {!draftsQ.isLoading && !draftsQ.error && drafts.length === 0 && (
              <p className="arp-empty">No generated sections are awaiting review.</p>
            )}

            <div className="arp-drafts">
              {drafts.map((draft) => {
                const invalid = draft.validation?.valid === false;
                return (
                  <details key={draft.id} className="arp-draft">
                    <summary>
                      <strong>{reportSectionLabel(draft.output_type)}</strong>
                      {invalid && <span className="arp-flag">VALIDATION REVIEW</span>}
                      <span className="arp-when">{draft.model} · {formatDatetime(draft.generated_at)}</span>
                    </summary>
                    <pre>{draft.output}</pre>
                    <div className="arp-actions">
                      <button type="button" className="btn arp-small" disabled={reviewMut.isPending}
                        onClick={() => reviewMut.mutate({ kind: "approve", ids: [draft.id] })}>Approve</button>
                      <button type="button" className="btn arp-small" disabled={reviewMut.isPending}
                        onClick={() => reject([draft.id])}>Reject &amp; regenerate</button>
                    </div>
                    {invalid && (draft.validation?.issues?.length ?? 0) > 0 && (
                      <ul className="arp-issues">
                        {draft.validation!.issues!.map((issue) => <li key={issue}>{issue}</li>)}
                      </ul>
                    )}
                  </details>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

const STYLES = `
.arp { border: var(--hairline) solid var(--border-subtle); border-radius: 10px; background: var(--bg-panel); margin-bottom: 14px; }
.arp-head { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; padding: 8px 12px; }
.arp-toggle { flex: 1 1 240px; display: flex; align-items: center; gap: 10px; min-height: 38px; padding: 0; border: 0; background: transparent; color: var(--text-primary); text-align: left; cursor: pointer; font: inherit; }
.arp-toggle > svg:first-child { flex: none; color: var(--ai-color, #7c3aed); }
.arp-toggle > span { display: flex; flex-direction: column; gap: 1px; min-width: 0; flex: 1; }
.arp-toggle strong { font: 650 13px/1.3 var(--font-ui); }
.arp-toggle small { color: var(--text-muted); font: 500 11.5px/1.3 var(--font-ui); }
.arp-toggle small[data-attention] { color: var(--sev-medium-color); font-weight: 650; }
.arp-chev { flex: none; color: var(--text-muted); transition: transform .15s; }
.arp-toggle[aria-expanded="true"] .arp-chev { transform: rotate(180deg); }
.arp-generate { display: inline-flex; align-items: center; gap: 6px; min-height: 34px; padding: 0 14px; font: 650 12px/1 var(--font-ui); }
.arp-body { display: flex; flex-direction: column; gap: 12px; padding: 0 14px 14px; border-top: var(--hairline) solid var(--border-subtle); }
.arp-lead { margin: 12px 0 0; color: var(--text-muted); font: 500 12px/1.5 var(--font-ui); }
.arp-note { display: flex; align-items: flex-start; gap: 8px; padding: 9px 11px; border-radius: 8px; background: var(--bg-surface); border: var(--hairline) solid var(--border-subtle); color: var(--text-secondary); font: 500 12px/1.5 var(--font-ui); }
.arp-note svg { flex: none; margin-top: 2px; }
.arp-note[data-tone="error"] { border-color: var(--sev-critical-color); background: var(--sev-critical-bg); color: var(--text-primary); }
.arp-note[data-tone="error"] svg { color: var(--sev-critical-color); }
.arp-note[data-tone="ok"] svg { color: var(--nominal-color); }
.arp-review { border-top: var(--hairline) solid var(--border-subtle); padding-top: 12px; }
.arp-review-head { display: flex; align-items: center; flex-wrap: wrap; gap: 7px; margin-bottom: 8px; }
.arp-review-head svg { color: var(--accent); }
.arp-review-head strong { font: 650 12px/1.3 var(--font-ui); }
.arp-review-head span { color: var(--text-muted); font: 500 11.5px/1.3 var(--font-ui); }
.arp-small { margin-left: auto; min-height: 30px; padding: 0 12px; font: 650 11.5px/1 var(--font-ui); }
.arp-actions .arp-small { margin-left: 0; }
.arp-empty, .arp-error { margin: 0; color: var(--text-muted); font: 500 12px/1.5 var(--font-ui); }
.arp-error { color: var(--sev-high-color); }
.arp-drafts { display: grid; gap: 8px; }
.arp-draft { border: var(--hairline) solid var(--border-subtle); border-radius: 8px; background: var(--bg-panel); overflow: hidden; }
.arp-draft > summary { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; padding: 9px 11px; cursor: pointer; color: var(--text-primary); font: 500 12px/1.4 var(--font-ui); }
.arp-when { margin-left: auto; color: var(--text-muted); font: 500 10.5px/1.4 var(--font-ui); }
.arp-flag { padding: 1px 6px; border: 1px solid var(--sev-critical-color); border-radius: 4px; color: var(--sev-critical-color); font: 800 9px/1.4 var(--font-ui); }
.arp-draft pre { margin: 0; padding: 11px 12px; max-height: 260px; overflow: auto; white-space: pre-wrap; word-break: break-word; border-top: var(--hairline) solid var(--border-subtle); color: var(--text-secondary); font: 500 11px/1.6 var(--font-mono); }
.arp-actions { display: flex; flex-wrap: wrap; gap: 8px; padding: 8px 12px; border-top: var(--hairline) solid var(--border-subtle); }
.arp-issues { margin: 0; padding: 9px 28px; color: var(--sev-high-color); font: 500 11px/1.5 var(--font-ui); }
@media (max-width: 720px) {
  .arp-generate, .arp-small { min-height: 44px; }
  .arp-generate { width: 100%; justify-content: center; }
  .arp-toggle { min-height: 44px; }
  .arp-when { margin-left: 0; flex-basis: 100%; }
}
`;
