"use client";

import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, ChevronLeft, ChevronRight, Lock, RefreshCw, Search } from "lucide-react";
import { ApiError } from "../../lib/fetcher";
import { newId } from "../../lib/uuid";
import { assessmentBase, assessmentRequest, type AssessmentLatest, type AssessmentPage, type AssessmentSnapshot, type FindingAssessment } from "../../lib/attack-assessments";
import { EmptyState, ErrorState, SkeletonRows, Unauthorized } from "../states/DataState";
import { FindingChainExplorer } from "./FindingChainExplorer";
import "./attack-assessments.css";

export function AttackAssessmentsPanel({ engagementId, initialFindingId }: { engagementId: string; initialFindingId?: string }) {
  const [selection, setSelection] = useState<{ snapshotId: string | null; page: number; findingId: string | null }>({ snapshotId: null, page: 1, findingId: null });
  const client = useQueryClient();
  const base = assessmentBase(engagementId);
  // Every mount and poll rechecks access; evidence is not kept in an inactive query cache.
  const latest = useQuery({
    queryKey: ["attack-assessment-latest", engagementId],
    queryFn: () => assessmentRequest<AssessmentLatest>(base),
    gcTime: 0, staleTime: 0, retry: false,
    refetchInterval: (query) => ["queued", "running"].includes(query.state.data?.state ?? "") ? 2000 : 15000,
  });
  const completed = latest.data?.last_completed;
  const page = selection.snapshotId === completed?.id ? selection.page : 1;
  const selectedId = selection.snapshotId === completed?.id ? selection.findingId : initialFindingId ?? null;
  const changePage = (next: number) => setSelection({ snapshotId: completed?.id ?? null, page: next, findingId: null });
  const records = useQuery({
    queryKey: ["attack-assessment-records", engagementId, completed?.id, page],
    queryFn: () => assessmentRequest<AssessmentPage>(`${base}/${completed!.id}?page=${page}&page_size=20`),
    enabled: Boolean(completed) && !latest.error, gcTime: 0, staleTime: 0, retry: false,
  });
  const create = useMutation({
    mutationFn: () => assessmentRequest<AssessmentSnapshot>(base, { method: "POST", headers: { "Idempotency-Key": newId() } }),
    onSuccess: () => { void client.invalidateQueries({ queryKey: ["attack-assessment-latest", engagementId] }); },
  });
  const focused = useQuery({
    queryKey: ["attack-assessment-focus", engagementId, completed?.id, selectedId],
    queryFn: () => assessmentRequest<{ assessment: FindingAssessment }>(`${base}/${completed!.id}/findings/${encodeURIComponent(selectedId!)}`),
    enabled: Boolean(completed && selectedId) && !latest.error && !records.data?.items.some((item) => item.finding_id === selectedId),
    gcTime: 0, staleTime: 0, retry: false,
  });
  const focusMissing = focused.error instanceof ApiError && focused.error.status === 404;
  const error = latest.error ?? records.error ?? (focusMissing ? null : focused.error);
  if (error instanceof ApiError && error.status === 401) return <Unauthorized />;
  if (error instanceof ApiError && error.status === 403) return <EmptyState icon={Lock} title="Assessment access is restricted" hint="Ask your workspace administrator to review assessment permissions." />;
  if (error instanceof ApiError && error.status === 404) return <EmptyState icon={Search} title="Attack-path assessments are not available yet" hint="This workspace is not enabled for the assessment pilot." />;
  if (error) return <ErrorState title="Could not load assessments" detail={error.message} onRetry={() => { void latest.refetch(); void records.refetch(); }} />;
  if (latest.isPending) return <SkeletonRows rows={4} height={72} />;
  const pending = ["queued", "running"].includes(latest.data?.state ?? "");
  const items = records.data?.items ?? [];
  const selected = items.find((item) => item.finding_id === selectedId) ?? focused.data?.assessment ?? (selectedId && focused.isPending ? undefined : items[0]);
  const total = records.data?.total ?? 0;

  return <section className="attack-assessments" aria-label="Finding-driven attack-path assessments">
    <header className="assessment-heading">
      <div><h2>Finding-driven attack chains</h2><p>See which weakness enables each step and what evidence is missing.</p></div>
      <button type="button" className="btn btn-primary" disabled={pending || create.isPending || !latest.data?.can_compute} title={!latest.data?.can_compute ? "Your role can view assessments but cannot request them." : undefined} onClick={() => create.mutate()}>
        <RefreshCw size={15} aria-hidden="true" />{pending ? "Assessment queued" : create.isPending ? "Requesting assessment…" : completed ? "Reassess findings" : "Assess findings"}
      </button>
    </header>
    {create.error && <p role="alert" className="assessment-notice">{create.error instanceof ApiError && create.error.status === 403 ? "Your role can view assessments but cannot request a new one." : create.error.message}</p>}
    {pending && <p role="status" className="assessment-notice">A new assessment is being prepared. {completed ? "The last completed results remain available below." : "Results will appear when it finishes."}</p>}
    {latest.data?.state === "failed" && <p role="alert" className="assessment-notice"><AlertTriangle size={16} aria-hidden="true" />The latest assessment failed. {completed ? "Showing the last completed snapshot." : "Retry to request a new assessment."}</p>}
    {focusMissing && <p role="status" className="assessment-notice">The linked finding was not included in this snapshot. Reassess to include current findings.</p>}
    {completed?.requires_reassessment && <p role="status" className="assessment-notice">The assessment model has changed. Reassess before using these historical results.</p>}
    {!completed ? <EmptyState icon={Search} title={pending ? "Preparing the first assessment" : "No assessment has been run"} hint={latest.data?.can_compute ? "An empty result does not establish safety. Start an assessment to review findings and evidence gaps." : "An empty result does not establish safety. Ask an analyst to run an assessment."} /> : <>
      <div className="assessment-context"><span>Snapshot: {new Date(completed.effective_as_of).toLocaleString()}</span><span>Evidence coverage: incomplete</span><span>Attack chain: not observed</span></div>
      <details className="assessment-model-note"><summary>Candidate chains · how to interpret this view</summary><p className="assessment-qualification">This pilot checks evidence readiness. Missing data and unmapped rules cannot establish a supported path or an all-clear. Solid entity boxes show recorded context; interrupted connections remain unconfirmed.</p></details>
      {records.isPending ? <SkeletonRows rows={4} height={68} /> : total === 0 ? <EmptyState title="No findings were included in this snapshot" hint="Review the engagement's findings and capture a fresh assessment. This is not an all-clear." /> : <>
        <p className="assessment-count">{total} {total === 1 ? "finding" : "findings"} assessed from {records.data?.total_findings ?? total} recorded {(records.data?.total_findings ?? total) === 1 ? "finding" : "findings"}{records.data?.compute === "truncated" ? " · Input limit reached; assessment incomplete" : ""}</p>
        <div className="assessment-workspace">
          <div className="assessment-queue" aria-label="Assessed findings">
            {items.map((item) => <button type="button" key={item.finding_id} className="assessment-row" aria-pressed={selected?.finding_id === item.finding_id} onClick={() => {
              setSelection({ snapshotId: completed.id, page, findingId: item.finding_id });
              if (window.matchMedia("(max-width: 900px)").matches) document.getElementById("attack-assessment-proof")?.scrollIntoView({ block: "start", behavior: "instant" });
            }}>
              <span className="assessment-row-title">{item.title}</span><span className="assessment-row-meta">{item.asset_label} · {item.severity} · {item.rule_applicability === "unmapped" ? "Rule not mapped" : "Evidence needed"}</span>
            </button>)}
            <nav className="assessment-pagination" aria-label="Assessment pages">
              <button type="button" className="btn btn-secondary" aria-label="Previous assessment page" disabled={page === 1} onClick={() => changePage(page - 1)}><ChevronLeft size={16} /></button>
              <span>Page {page} of {Math.max(1, Math.ceil(total / 20))}</span>
              <button type="button" className="btn btn-secondary" aria-label="Next assessment page" disabled={page * 20 >= total} onClick={() => changePage(page + 1)}><ChevronRight size={16} /></button>
            </nav>
          </div>
          {!selected && selectedId && focused.isPending && <SkeletonRows rows={4} height={80} />}
          {selected && <FindingChainExplorer key={`${completed.id}:${selected.finding_id}`} finding={selected} engagementId={engagementId} />}
        </div>
      </>}
    </>}
  </section>;
}
