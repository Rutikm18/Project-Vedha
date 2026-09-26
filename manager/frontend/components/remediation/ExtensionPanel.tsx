"use client";

/**
 * ExtensionPanel — deadline extensions for one finding or one fix bundle.
 *
 * Portal: the customer requests a later due date (reason required; a
 * compensating control is required for critical/high/KEV — the backend enforces
 * it too), and can withdraw while pending.
 * Operator: approve (optionally with a different date) or reject, with a note.
 * Every transition lands on the finding timeline and the audit log server-side.
 */
import React, { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { CalendarPlus, Check, Clock, X } from "lucide-react";
import {
  fmtIst, minExtensionDate, type ExtensionRequest, type RemediationApi,
} from "../../lib/remediation";

export interface ExtensionSubject {
  type: "finding" | "bundle";
  findingId?: string;
  fixKey?: string;
  fixRef?: string;
  /** Current due date (ISO) — the request must be later than this. */
  currentDue?: string | null;
  /** Any member critical/high or on CISA KEV → compensating control required. */
  serious?: boolean;
}

function related(r: ExtensionRequest, s: ExtensionSubject): boolean {
  if (s.type === "bundle") return r.fix_key === s.fixKey;
  return r.finding_id === s.findingId || (s.findingId ? r.member_finding_ids.includes(s.findingId) : false);
}

const STATUS_LABEL: Record<ExtensionRequest["status"], string> = {
  pending: "Pending review", approved: "Approved", rejected: "Rejected", withdrawn: "Withdrawn",
};

function errorText(e: unknown): string {
  return e instanceof Error ? e.message : String(e ?? "");
}

function RequestRow({ r, api, onDone }: { r: ExtensionRequest; api: RemediationApi; onDone: () => void }) {
  const [note, setNote] = useState("");
  const [date, setDate] = useState("");
  const decide = useMutation({
    mutationFn: (action: "approve" | "reject") => api.decide(r.id, action, {
      note, due_at: action === "approve" && date ? new Date(`${date}T18:29:00Z`).toISOString() : undefined,
    }),
    onSuccess: onDone,
  });
  const withdraw = useMutation({ mutationFn: () => api.withdraw(r.id), onSuccess: onDone });
  const operator = api.surface === "manager";

  return (
    <li className="rm-ext-row" data-status={r.status}>
      <div className="rm-ext-head">
        <span className="rm-ext-status" data-status={r.status}>{STATUS_LABEL[r.status]}</span>
        {r.fix_ref && <span className="rm-chip rm-chip--muted">{r.fix_ref}</span>}
        <span className="rm-ext-dates">
          {fmtIst(r.current_due_at)} → <strong>{fmtIst(r.decided_due_at ?? r.requested_due_at)}</strong>
        </span>
      </div>
      <p><strong>Reason:</strong> {r.reason}</p>
      {r.compensating_control && <p><strong>Compensating control:</strong> {r.compensating_control}</p>}
      {r.decision_note && <p><strong>Decision:</strong> {r.decision_note} {r.decided_at && <em>({fmtIst(r.decided_at)})</em>}</p>}
      <p className="rm-ext-meta">Requested {fmtIst(r.requested_at)} · covers {r.member_finding_ids.length} finding{r.member_finding_ids.length === 1 ? "" : "s"}</p>

      {operator && r.status === "pending" && (
        <div className="rm-ext-decide">
          <label>
            <span>Decision note (required)</span>
            <textarea value={note} onChange={(e) => setNote(e.target.value)} rows={2}
                      placeholder="e.g. Approved until the vendor patch; keep 445 blocked at the edge." />
          </label>
          <label>
            <span>Grant a different date (optional)</span>
            <input type="date" value={date} min={minExtensionDate(r.current_due_at)} onChange={(e) => setDate(e.target.value)} />
          </label>
          <div className="rm-ext-actions">
            <button type="button" className="btn btn-primary" disabled={note.trim().length < 3 || decide.isPending}
                    onClick={() => decide.mutate("approve")}><Check size={13} aria-hidden />Approve</button>
            <button type="button" className="btn btn-secondary" disabled={note.trim().length < 3 || decide.isPending}
                    onClick={() => decide.mutate("reject")}><X size={13} aria-hidden />Reject</button>
          </div>
          {decide.error && <p className="rm-error">{errorText(decide.error)}</p>}
        </div>
      )}
      {!operator && r.status === "pending" && (
        <div className="rm-ext-actions">
          <button type="button" className="btn btn-secondary" disabled={withdraw.isPending}
                  onClick={() => withdraw.mutate()}>Withdraw request</button>
          {withdraw.error && <p className="rm-error">{errorText(withdraw.error)}</p>}
        </div>
      )}
    </li>
  );
}

function RequestForm({ api, subject, onDone }: { api: RemediationApi; subject: ExtensionSubject; onDone: () => void }) {
  const [date, setDate] = useState("");
  const [reason, setReason] = useState("");
  const [control, setControl] = useState("");
  const create = useMutation({
    mutationFn: () => api.requestExtension({
      subject_type: subject.type,
      finding_id: subject.type === "finding" ? subject.findingId : undefined,
      fix_key: subject.type === "bundle" ? subject.fixKey : undefined,
      // End of the chosen day in IST (18:29 UTC).
      requested_due_at: new Date(`${date}T18:29:00Z`).toISOString(),
      reason,
      compensating_control: control.trim() || undefined,
    }),
    onSuccess: () => { setDate(""); setReason(""); setControl(""); onDone(); },
  });
  const controlMissing = Boolean(subject.serious) && control.trim().length === 0;
  const valid = date && reason.trim().length >= 10 && !controlMissing;

  return (
    <form className="rm-ext-form" onSubmit={(e) => { e.preventDefault(); if (valid) create.mutate(); }}>
      <p className="rm-ext-intro">
        Current due date: <strong>{fmtIst(subject.currentDue)}</strong>. Ask for more time if the fix cannot land by then —
        your security team reviews every request.
      </p>
      <label>
        <span>New due date</span>
        <input type="date" required value={date} min={minExtensionDate(subject.currentDue)} onChange={(e) => setDate(e.target.value)} />
      </label>
      <label>
        <span>Why more time is needed (at least 10 characters)</span>
        <textarea required rows={2} value={reason} onChange={(e) => setReason(e.target.value)}
                  placeholder="e.g. Waiting for the vendor patch; change freeze until month end." />
      </label>
      <label>
        <span>Compensating control{subject.serious ? " (required for critical, high or known-exploited findings)" : " (optional)"}</span>
        <textarea rows={2} value={control} onChange={(e) => setControl(e.target.value)}
                  placeholder="e.g. Port 445 blocked from user VLANs; alerting on SMBv1 negotiation." />
      </label>
      <button type="submit" className="btn btn-primary" disabled={!valid || create.isPending}>
        <CalendarPlus size={13} aria-hidden />Request extension
      </button>
      {create.error && <p className="rm-error">{errorText(create.error)}</p>}
    </form>
  );
}

export function ExtensionPanel({
  api, engagementId, subject,
}: { api: RemediationApi; engagementId: string; subject: ExtensionSubject }) {
  const qc = useQueryClient();
  const key = ["remediation-extensions", api.surface, engagementId];
  const { data, isLoading } = useQuery({
    queryKey: key,
    queryFn: () => api.extensions(engagementId),
    enabled: Boolean(engagementId) || api.surface === "portal",
    staleTime: 15_000,
  });
  const refresh = () => {
    void qc.invalidateQueries({ queryKey: key });
    void qc.invalidateQueries({ queryKey: ["finding-remediation"] });
    void qc.invalidateQueries({ queryKey: ["remediation-bundles"] });
  };
  const items = (data?.items ?? []).filter((r) => related(r, subject));
  const pending = items.some((r) => r.status === "pending");
  const portal = api.surface === "portal";

  return (
    <section className="rm-ext">
      <h4><Clock size={14} aria-hidden /> Due date & extensions</h4>
      {isLoading && <p className="rm-muted">Loading requests…</p>}
      {!isLoading && items.length === 0 && !portal && <p className="rm-muted">No extension has been requested.</p>}
      {items.length > 0 && <ul className="rm-ext-list">{items.map((r) => <RequestRow key={r.id} r={r} api={api} onDone={refresh} />)}</ul>}
      {portal && !pending && <RequestForm api={api} subject={subject} onDone={refresh} />}
    </section>
  );
}
