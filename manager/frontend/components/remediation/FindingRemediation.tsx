"use client";

/**
 * FindingRemediation — the Remediation tab of a finding (operator + portal).
 *
 * Shows the asset-grounded plan (OS auto-selected from the scan), the fix bundle
 * the finding belongs to, and — for operators — "Refine with AI" (gateway-routed,
 * unreviewed until approved) and "Approve for customer". A cached AI plan whose
 * facts changed since it was generated is flagged stale. The due date and the
 * extension workflow sit underneath.
 */
import React, { useMemo, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AlertTriangle, BadgeCheck, Boxes, RefreshCw, RotateCcw, Sparkles } from "lucide-react";
import { SkeletonRows } from "../states/DataState";
import { ExtensionPanel } from "./ExtensionPanel";
import { PlanView } from "./PlanView";
import { createRemediationApi, fmtIst, type PlanOs, type RemediationSurface } from "../../lib/remediation";

const OS_OPTIONS: Array<[PlanOs, string]> = [
  ["windows", "Windows"], ["linux", "Linux"], ["macos", "macOS"], ["generic", "Network appliance / generic"],
];

function errorText(e: unknown): string {
  return e instanceof Error ? e.message : String(e ?? "");
}

export function FindingRemediation({
  findingId, engagementId, surface, serious, recordedNotes = [],
}: {
  findingId: string;
  engagementId?: string | null;
  surface: RemediationSurface;
  /** critical/high or KEV — a compensating control is required for extensions. */
  serious: boolean;
  /** Free-text guidance recorded on the finding itself (shown when present). */
  recordedNotes?: string[];
}) {
  const api = useMemo(() => createRemediationApi(surface), [surface]);
  const qc = useQueryClient();
  const [os, setOs] = useState<PlanOs | undefined>(undefined);   // undefined → scanned OS
  const key = ["finding-remediation", surface, findingId, os ?? "auto"];
  const { data, isLoading, isFetching, error, refetch } = useQuery({
    queryKey: key, queryFn: () => api.plan(findingId, os), staleTime: 60_000,
  });
  const current = (data?.os ?? os ?? "generic") as PlanOs;
  const refresh = (next: unknown) => {
    qc.setQueryData(key, next);
    void qc.invalidateQueries({ queryKey: ["finding-remediation", surface, findingId] });
  };
  const refine = useMutation({
    mutationFn: () => api.refine(findingId, current, { force: true }),
    onSuccess: refresh,
  });
  const publish = useMutation({ mutationFn: () => api.publish(findingId, current), onSuccess: refresh });
  const operator = surface === "manager";

  if (isLoading) return <div aria-busy="true"><SkeletonRows rows={4} height={72} /></div>;
  if (error || !data) {
    return (
      <div className="finding-blank" data-tone="error">
        <AlertTriangle size={17} aria-hidden />
        <div>
          <strong>The remediation plan did not load</strong>
          <p>{errorText(error) || "The finding record itself is unchanged."}</p>
          <button type="button" className="findings-inline-action" onClick={() => { void refetch(); }}>
            <RotateCcw size={13} aria-hidden /> Try again
          </button>
        </div>
      </div>
    );
  }

  const isAi = data.source === "ai";
  return (
    <div className="rm-finding" data-refreshing={isFetching || undefined}>
      <div className="rm-toolbar">
        <div className="rm-source">
          {isAi
            ? <span className="rm-tag rm-tag--ai"><Sparkles size={11} aria-hidden />AI-refined plan{data.model ? ` · ${data.model}` : ""}</span>
            : <span className="rm-tag">Vedha knowledge base · grounded in scan facts</span>}
          {isAi && (data.reviewed
            ? <span className="rm-tag rm-tag--ok"><BadgeCheck size={11} aria-hidden />Approved for customer</span>
            : operator && <span className="rm-tag rm-tag--warn">Not yet approved — customers see the knowledge-base plan</span>)}
          {data.stale && <span className="rm-tag rm-tag--warn"><AlertTriangle size={11} aria-hidden />Stale: the asset changed since this was generated</span>}
          {data.generated_at && <span className="rm-muted">Generated {fmtIst(data.generated_at)}</span>}
        </div>
        <div className="rm-actions">
          <label className="rm-os">
            <span>Platform</span>
            <select value={current} onChange={(e) => setOs(e.target.value as PlanOs)}>
              {OS_OPTIONS.map(([v, l]) => (
                <option key={v} value={v}>{l}{data.plan.os_auto === v ? " (detected)" : ""}</option>
              ))}
            </select>
          </label>
          {operator && (
            <button type="button" className="btn btn-secondary" disabled={refine.isPending} onClick={() => refine.mutate()}>
              {refine.isPending ? <RefreshCw size={13} className="spin" aria-hidden /> : <Sparkles size={13} aria-hidden />}
              {isAi ? "Regenerate with AI" : "Refine with AI"}
            </button>
          )}
          {operator && isAi && !data.reviewed && !data.stale && (
            <button type="button" className="btn btn-primary" disabled={publish.isPending} onClick={() => publish.mutate()}>
              <BadgeCheck size={13} aria-hidden />Approve for customer
            </button>
          )}
        </div>
      </div>
      {(refine.error || publish.error) && <p className="rm-error">{errorText(refine.error || publish.error)}</p>}
      {refine.isPending && <p className="rm-muted">Refining through the AI gateway — the knowledge-base plan stays the floor; only the changes are shown as AI-refined.</p>}

      {data.bundle && engagementId && (
        <p className="rm-bundle-link">
          <Boxes size={13} aria-hidden />
          Part of fix bundle <strong>{data.bundle.ref}</strong> — one change that may close this finding on other hosts too.{" "}
          <Link href={`${surface === "portal" ? "/portal" : ""}/remediation?engagement=${engagementId}&fix=${data.bundle.fix_key}`}>Open bundle</Link>
        </p>
      )}

      {recordedNotes.length > 0 && (
        <section className="rm-notes">
          <h4>Guidance recorded on the finding</h4>
          {recordedNotes.map((n, i) => <p key={i}>{n}</p>)}
        </section>
      )}

      <PlanView plan={data.plan} />

      {(engagementId || surface === "portal") && (
        <ExtensionPanel api={api} engagementId={engagementId ?? ""}
                        subject={{ type: "finding", findingId, currentDue: data.plan.due?.at ?? null, serious }} />
      )}
    </div>
  );
}
