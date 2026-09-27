"use client";

import { createContext, useCallback, useContext, useMemo, useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  ClipboardCheck,
  Clock,
  Copy,
  FileCheck2,
  FileWarning,
  Fingerprint,
  History,
  Link2,
  ListChecks,
  LockKeyhole,
  Server,
  ShieldCheck,
  Terminal,
  Wrench,
} from "lucide-react";

import { redact } from "../../lib/report/finding-model";
import {
  executiveSummaryText,
  gapLabel,
  recordedValue,
  type ReportAutoResolutionCoverage,
  type ReportComplianceMapping,
  type ReportDetectionRunProvenance,
  type ReportDocument,
  type ReportEvidence,
  type ReportEvidenceArtifact,
  type ReportFinding,
  type ReportFindingEvent,
  type ReportRegulatoryProfile,
  type ReportRemediationPlan,
  type ReportRetestRecord,
} from "../../lib/report/report-document";
import { SEV_COLOR, toSeverity } from "../../lib/severity";

const CONTROL_FIELDS = [
  ["version", "Report version"],
  ["document_status", "Document status"],
  ["classification", "Classification"],
  ["prepared_by", "Prepared by"],
  ["prepared_at", "Prepared at"],
  ["reviewed_by", "Reviewed by"],
  ["reviewed_at", "Reviewed at"],
  ["approved_by", "Approved by"],
  ["approved_at", "Approved at"],
  ["issue_date", "Issue date"],
  ["reporting_period", "Reporting period"],
  ["distribution", "Distribution"],
] as const;

const CONTROL_TIME_FIELDS = new Set(["prepared_at", "reviewed_at", "approved_at", "issue_date"]);
const ReportTimeZoneContext = createContext("UTC");

function displayLabel(value: string): string {
  return value.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function usableTimeZone(value: string): string {
  try {
    new Intl.DateTimeFormat("en-GB", { timeZone: value }).format(new Date(0));
    return value;
  } catch {
    return "UTC";
  }
}

function formatTimestamp(value: string | null | undefined, timeZone: string): string | null {
  if (!value) return null;
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) return value;
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  const formatted = new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
    timeZone,
    timeZoneName: "short",
  }).format(parsed);
  return `${formatted} [${timeZone}]`;
}

function exactUtcTimestamp(value: string): string {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? value : parsed.toISOString();
}

function maskedRecordedValue(value: unknown): string | null {
  const text = recordedValue(value);
  return text ? redact(text).text : null;
}

function RecordedTime({ value }: { value: string | null | undefined }) {
  const timeZone = useContext(ReportTimeZoneContext);
  const formatted = formatTimestamp(value, timeZone);
  if (!formatted) return <span className="cr-unset">Not recorded</span>;
  const exactUtc = value && /^\d{4}-\d{2}-\d{2}$/.test(value) ? value : value ? exactUtcTimestamp(value) : null;
  return (
    <span className="cr-recorded-time">
      <time dateTime={value ?? undefined} title={value ?? undefined}>{formatted}</time>
      {exactUtc && <code>{exactUtc}</code>}
    </span>
  );
}

function RecordedBlock({ value, empty = "Not recorded" }: { value: unknown; empty?: string }) {
  const text = recordedValue(value);
  if (!text) return <p className="cr-unset cr-copy">{empty}</p>;
  const masked = redact(text);
  if (typeof value === "string") {
    return (
      <>
        <div className="cr-prose">
          {masked.text.split(/\n{2,}/).map((paragraph, index) => <p key={index}>{paragraph}</p>)}
        </div>
        {masked.total > 0 && <p className="cr-redaction-note">{masked.total} sensitive value{masked.total === 1 ? "" : "s"} masked.</p>}
      </>
    );
  }
  return (
    <>
      <pre className="cr-recorded-json">{masked.text}</pre>
      {masked.total > 0 && <p className="cr-redaction-note">{masked.total} sensitive value{masked.total === 1 ? "" : "s"} masked.</p>}
    </>
  );
}

function RecordedHttpUrl({ value }: { value: string | null }) {
  const text = recordedValue(value);
  if (!text) return <span className="cr-unset">Not recorded</span>;
  const masked = redact(text);
  let href: string | null = null;
  if (masked.total === 0) {
    try {
      const parsed = new URL(masked.text);
      if (parsed.protocol === "http:" || parsed.protocol === "https:") href = parsed.href;
    } catch {
      // A recorded non-URL remains visible as data, but never becomes a link.
    }
  }
  if (!href) return <span className="cr-source-url">{masked.text}</span>;
  return (
    <a className="cr-source-url" href={href} target="_blank" rel="noopener noreferrer">
      {masked.text}
    </a>
  );
}

function GapList({ gaps, empty }: { gaps: string[]; empty?: string }) {
  if (gaps.length === 0) {
    return empty ? <p className="cr-complete"><CheckCircle2 size={13} />{empty}</p> : null;
  }
  return (
    <ul className="cr-gap-list">
      {gaps.map((gap) => (
        <li key={gap}>
          <FileWarning size={12} aria-hidden="true" />
          <span>{gapLabel(gap)} <code>{gap}</code></span>
        </li>
      ))}
    </ul>
  );
}

function Chips({ values, tone }: { values: string[]; tone?: "accent" | "risk" }) {
  if (values.length === 0) return <span className="cr-unset">None recorded</span>;
  return (
    <span className="cr-chips">
      {values.map((value) => <span key={value} className="cr-chip" data-tone={tone}>{value}</span>)}
    </span>
  );
}

function CopyButton({ value }: { value: string }) {
  const [copied, setCopied] = useState(false);
  const copy = useCallback(() => {
    void navigator.clipboard.writeText(value).then(() => {
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1400);
    });
  }, [value]);
  return (
    <button type="button" className="vf-icon-btn no-print" onClick={copy} aria-label={copied ? "Copied" : "Copy masked evidence"}>
      {copied ? <CheckCircle2 size={12} className="vf-ok" /> : <Copy size={12} />}
    </button>
  );
}

function EvidenceArtifact({ artifact, reference }: {
  artifact: ReportEvidenceArtifact;
  reference: string;
}) {
  const content = useMemo(
    () => recordedValue(artifact.content) ?? "No evidence content recorded.",
    [artifact.content],
  );
  const masked = useMemo(() => redact(content), [content]);
  const maskedCommand = useMemo(
    () => artifact.command ? redact(artifact.command) : null,
    [artifact.command],
  );

  return (
    <figure className="vf-artifact cr-evidence-artifact">
      <figcaption className="vf-artifact-head">
        <span className="vf-artifact-id">{reference}</span>
        <Terminal size={12} aria-hidden="true" />
        <span className="vf-artifact-label">{artifact.label}</span>
        {artifact.evidence_type && <span className="vf-tag">{artifact.evidence_type}</span>}
        <span className="vf-artifact-tools"><CopyButton value={masked.text} /></span>
      </figcaption>

      {maskedCommand && (
        <div className="vf-artifact-cmd">
          <span className="vf-artifact-cmd-sigil" aria-hidden="true">$</span>
          <code>{maskedCommand.text}</code>
        </div>
      )}

      {maskedCommand && maskedCommand.total > 0 && (
        <p className="vf-artifact-note vf-artifact-note--mask">
          {maskedCommand.total} sensitive command value{maskedCommand.total === 1 ? "" : "s"} masked.
        </p>
      )}

      <pre className="vf-artifact-out" data-expanded="true">{masked.text}</pre>
      {masked.total > 0 && (
        <p className="vf-artifact-note vf-artifact-note--mask">
          {masked.total} recorded value{masked.total === 1 ? "" : "s"} masked in this view and print output
          {masked.hits.length ? ` — ${masked.hits.map((hit) => `${hit.count}× ${hit.kind}`).join(", ")}` : ""}.
        </p>
      )}

      <dl className="vf-provenance cr-provenance">
        <div><dt>Tool</dt><dd>{artifact.tool ?? <span className="vf-unset">not recorded</span>}</dd></div>
        <div><dt>Source</dt><dd>{artifact.source ?? <span className="vf-unset">not recorded</span>}</dd></div>
        <div><dt>Source host</dt><dd>{artifact.source_host ?? <span className="vf-unset">not recorded</span>}</dd></div>
        <div><dt>Recorded timestamp</dt><dd><RecordedTime value={artifact.timestamp} /></dd></div>
        <div><dt>Captured at</dt><dd><RecordedTime value={artifact.captured_at} /></dd></div>
        <div><dt>Captured by</dt><dd>{artifact.captured_by ?? <span className="vf-unset">not recorded</span>}</dd></div>
        <div><dt>Scan result ID</dt><dd>{artifact.scan_result_id ?? <span className="vf-unset">not recorded</span>}</dd></div>
        <div><dt>Scan job ID</dt><dd>{artifact.scan_job_id ?? <span className="vf-unset">not recorded</span>}</dd></div>
        <div><dt>Detection run ID</dt><dd>{artifact.detection_run_id ?? <span className="vf-unset">not recorded</span>}</dd></div>
        <div><dt>Timestamp basis</dt><dd>{artifact.timestamp_basis ?? <span className="vf-unset">not recorded</span>}</dd></div>
        <div className="cr-hash"><dt>SHA-256</dt><dd>{artifact.sha256 ?? <span className="vf-unset">not recorded</span>}</dd></div>
      </dl>
    </figure>
  );
}

function EvidenceSet({ evidence, prefix, empty }: {
  evidence: ReportEvidence;
  prefix: string;
  empty: string;
}) {
  return (
    <div className="cr-stack">
      {evidence.artifacts.length > 0 ? (
        <div className="vf-artifacts">
          {evidence.artifacts.map((artifact) => (
            <EvidenceArtifact
              key={`${prefix}-${artifact.index}`}
              artifact={artifact}
              reference={`${prefix}/E${String(artifact.index).padStart(2, "0")}`}
            />
          ))}
        </div>
      ) : <p className="cr-missing"><FileWarning size={13} />{empty}</p>}
      <GapList gaps={evidence.gaps} />
    </div>
  );
}

function EventRecord({ event, heading }: { event: ReportFindingEvent; heading?: string }) {
  return (
    <article className="cr-event">
      <div className="cr-event-head">
        <strong>{heading ?? event.label}</strong>
        <span className="cr-chip">{event.event_type}</span>
        {event.synthesized && <span className="cr-chip" data-tone="risk">Synthesized from finding fields</span>}
        <RecordedTime value={event.occurred_at} />
      </div>
      <dl className="cr-inline-meta">
        <div><dt>Event ID</dt><dd>{event.id ?? "Not stored"}</dd></div>
        <div><dt>Actor</dt><dd>{event.actor ?? "Not recorded"}</dd></div>
        <div><dt>Actor type</dt><dd>{event.actor_type}</dd></div>
        <div><dt>Status change</dt><dd>{event.from_status ?? "—"} → {event.to_status ?? "—"}</dd></div>
      </dl>
      {event.detail && <RecordedBlock value={event.detail} />}
    </article>
  );
}

function DetectionRunProvenance({ provenance, heading }: {
  provenance: ReportDetectionRunProvenance | null;
  heading: string;
}) {
  if (!provenance) {
    return (
      <div className="cr-subsection">
        <h5>{heading}</h5>
        <p className="cr-missing"><FileWarning size={13} />No {heading.toLowerCase()} provenance is recorded.</p>
      </div>
    );
  }
  return (
    <article className="cr-run-provenance">
      <div className="cr-plan-head">
        <div>
          <strong>{heading}</strong>
          <span>{provenance.run_id}</span>
        </div>
        <span className="cr-chip" data-tone="accent">{displayLabel(provenance.role)}</span>
      </div>
      <dl className="cr-meta-grid cr-meta-grid--compact">
        <div><dt>Scan result ID</dt><dd>{provenance.scan_result_id ?? "Not recorded"}</dd></div>
        <div><dt>SCN / scan job ID</dt><dd>{provenance.scan_job_id ?? "Not recorded"}</dd></div>
        <div><dt>Scan attempt ID</dt><dd>{provenance.scan_attempt_id ?? "Not recorded"}</dd></div>
        <div><dt>Agent ID</dt><dd>{provenance.agent_id ?? "Not recorded"}</dd></div>
        <div><dt>Scan type</dt><dd>{provenance.scan_type ?? "Not recorded"}</dd></div>
        <div><dt>Result validation</dt><dd>{provenance.scan_result_validation_state ?? "Not recorded"}</dd></div>
        <div><dt>Result recorded</dt><dd><RecordedTime value={provenance.scan_result_recorded_at} /></dd></div>
        <div><dt>Run trigger</dt><dd>{provenance.trigger}</dd></div>
        <div><dt>Run status</dt><dd>{provenance.status}</dd></div>
        <div><dt>Run started</dt><dd><RecordedTime value={provenance.started_at} /></dd></div>
        <div><dt>Run finished</dt><dd><RecordedTime value={provenance.finished_at} /></dd></div>
        <div><dt>Vulnerability DB version</dt><dd>{provenance.vuln_db_version ?? "Not recorded"}</dd></div>
        <div><dt>DB fetched at</dt><dd><RecordedTime value={provenance.vuln_db_fetched_at} /></dd></div>
        <div><dt>Facts</dt><dd>{provenance.facts_count}</dd></div>
        <div><dt>New / reaffirmed / current</dt><dd>{provenance.findings_new} / {provenance.findings_reaffirmed} / {provenance.findings_current}</dd></div>
        <div className="cr-wide cr-hash"><dt>Scan result checksum</dt><dd>{provenance.scan_result_checksum ?? "Not recorded"}</dd></div>
      </dl>
      <div className="cr-two-up cr-run-payloads">
        <div><h6>Recorded run coverage</h6><RecordedBlock value={provenance.recorded_coverage} empty="No run coverage payload recorded." /></div>
        <div><h6>Recorded run statistics</h6><RecordedBlock value={provenance.recorded_stats} empty="No run statistics recorded." /></div>
      </div>
    </article>
  );
}

function AutoResolutionCoverage({ coverage }: { coverage: ReportAutoResolutionCoverage }) {
  return (
    <div className="cr-subsection cr-coverage-proof">
      <h5>Recorded detection-run coverage</h5>
      <p className="cr-caution">
        <AlertTriangle size={13} />Coverage evidence only — the canonical record explicitly does not treat this as patch attestation.
      </p>
      <dl className="cr-meta-grid cr-meta-grid--compact">
        <div><dt>Run ID</dt><dd>{coverage.run_id}</dd></div>
        <div><dt>Scan result ID</dt><dd>{coverage.scan_result_id ?? "Not recorded"}</dd></div>
        <div><dt>Trigger</dt><dd>{coverage.trigger}</dd></div>
        <div><dt>Status</dt><dd>{coverage.status}</dd></div>
        <div><dt>Started</dt><dd><RecordedTime value={coverage.started_at} /></dd></div>
        <div><dt>Finished</dt><dd><RecordedTime value={coverage.finished_at} /></dd></div>
        <div><dt>Vulnerability DB version</dt><dd>{coverage.vuln_db_version ?? "Not recorded"}</dd></div>
        <div><dt>DB fetched at</dt><dd>{coverage.vuln_db_fetched_at ?? "Not recorded"}</dd></div>
        <div><dt>Facts</dt><dd>{coverage.facts_count}</dd></div>
        <div><dt>New / reaffirmed / current</dt><dd>{coverage.findings_new} / {coverage.findings_reaffirmed} / {coverage.findings_current}</dd></div>
      </dl>
      <div className="cr-two-up">
        <div><h6>Recorded coverage</h6><RecordedBlock value={coverage.recorded_coverage} empty="No run coverage payload recorded." /></div>
        <div><h6>Recorded run statistics</h6><RecordedBlock value={coverage.recorded_stats} empty="No run statistics recorded." /></div>
      </div>
    </div>
  );
}

function RetestRecord({ retest, findingRef }: {
  retest: ReportRetestRecord | null;
  findingRef: string;
}) {
  if (!retest) {
    return <p className="cr-missing"><FileWarning size={13} />No structured retest record is available.</p>;
  }
  const result = retest.passed === true ? "Passed" : retest.passed === false ? "Failed" : "Not recorded";
  return (
    <article className="cr-retest" data-passed={retest.passed ?? "unknown"}>
      <div className="cr-retest-head">
        <div>
          <h5>Structured retest verification</h5>
          <p>Before-and-after evidence and the recorded verification conditions.</p>
        </div>
        <span className="cr-chip" data-tone={retest.passed === true ? "accent" : "risk"}>Retest {result}</span>
      </div>
      <dl className="cr-meta-grid">
        <div><dt>Requested</dt><dd><RecordedTime value={retest.requested_at} /></dd></div>
        <div><dt>Started</dt><dd><RecordedTime value={retest.started_at} /></dd></div>
        <div><dt>Completed</dt><dd><RecordedTime value={retest.completed_at} /></dd></div>
        <div><dt>Verified</dt><dd><RecordedTime value={retest.verified_at} /></dd></div>
        <div><dt>Tested by</dt><dd>{maskedRecordedValue(retest.tested_by) ?? "Not recorded"}</dd></div>
        <div><dt>Verified by</dt><dd>{maskedRecordedValue(retest.verified_by) ?? "Not recorded"}</dd></div>
        <div><dt>Vantage point</dt><dd>{maskedRecordedValue(retest.vantage_point) ?? "Not recorded"}</dd></div>
        <div><dt>Method</dt><dd>{maskedRecordedValue(retest.method) ?? "Not recorded"}</dd></div>
        <div><dt>Change reference</dt><dd>{maskedRecordedValue(retest.change_reference) ?? "Not recorded"}</dd></div>
      </dl>
      <div className="cr-two-up cr-retest-conditions">
        <div><h6>Retest scope</h6><RecordedBlock value={retest.scope} /></div>
        <div><h6>Authentication context</h6><RecordedBlock value={retest.authentication_context} /></div>
        <div><h6>Tool configuration</h6><RecordedBlock value={retest.tool_configuration} /></div>
        <div><h6>Expected result</h6><RecordedBlock value={retest.expected_result} /></div>
        <div><h6>Actual result</h6><RecordedBlock value={retest.actual_result} /></div>
        <div><h6>Coverage comparison</h6><RecordedBlock value={retest.coverage_comparison} /></div>
        <div><h6>Residual risk</h6><RecordedBlock value={retest.residual_risk} /></div>
      </div>
      <div className="cr-retest-evidence">
        <section>
          <h6>Before remediation evidence</h6>
          <EvidenceSet evidence={retest.before_evidence} prefix={`${findingRef}/RETEST/BEFORE`} empty="No before-remediation retest evidence is recorded." />
        </section>
        <section>
          <h6>After remediation evidence</h6>
          <EvidenceSet evidence={retest.after_evidence} prefix={`${findingRef}/RETEST/AFTER`} empty="No after-remediation retest evidence is recorded." />
        </section>
      </div>
    </article>
  );
}

function RemediationPlan({ plan }: { plan: ReportRemediationPlan }) {
  return (
    <article className="cr-plan">
      <div className="cr-plan-head">
        <div>
          <strong>{maskedRecordedValue(plan.summary) ?? "Reviewed remediation plan"}</strong>
          <span>{plan.id}</span>
        </div>
        <span className="cr-chip" data-tone="accent"><CheckCircle2 size={10} />Reviewed</span>
      </div>
      <dl className="cr-inline-meta">
        <div><dt>Generated</dt><dd><RecordedTime value={plan.generated_at} /></dd></div>
        <div><dt>Source</dt><dd>{plan.source}</dd></div>
        <div><dt>Model</dt><dd>{plan.model ?? "Not recorded"}</dd></div>
        <div><dt>Operating system</dt><dd>{plan.os}</dd></div>
        <div><dt>Effort</dt><dd>{plan.effort ?? "Not recorded"}</dd></div>
        <div><dt>Remediation risk</dt><dd>{plan.remediation_risk ?? "Not recorded"}</dd></div>
      </dl>
      <div className="cr-two-up">
        <div>
          <h6>Recorded steps</h6>
          {plan.steps.length ? (
            <ol className="cr-plan-steps">
              {plan.steps.map((step, index) => <li key={index}><pre>{maskedRecordedValue(step)}</pre></li>)}
            </ol>
          ) : <p className="cr-unset">No plan steps recorded.</p>}
        </div>
        <div className="cr-stack">
          <div><h6>Verification instructions</h6>{plan.verification.length ? <ul>{plan.verification.map((item, index) => <li key={`${index}-${item}`}>{maskedRecordedValue(item)}</li>)}</ul> : <p className="cr-unset">Not recorded</p>}</div>
          <div><h6>Long-term recommendations</h6>{plan.long_term_recommendations.length ? <ul>{plan.long_term_recommendations.map((item, index) => <li key={`${index}-${item}`}>{maskedRecordedValue(item)}</li>)}</ul> : <p className="cr-unset">Not recorded</p>}</div>
          <div><h6>Compensating controls</h6><RecordedBlock value={plan.compensating_controls} /></div>
        </div>
      </div>
    </article>
  );
}

function ComplianceMapping({ mapping, index }: { mapping: ReportComplianceMapping; index: number }) {
  return (
    <article className="cr-mapping">
      <div className="cr-mapping-head">
        <strong>
          {mapping.framework ?? "Framework not recorded"}
          {mapping.framework_version ? ` ${mapping.framework_version}` : ""}
          {mapping.release ? ` · release ${mapping.release}` : ""}
        </strong>
        <span>{mapping.mapping_id ?? mapping.control_id ?? mapping.recorded_reference ?? `Mapping ${index + 1}`}</span>
      </div>
      <dl className="cr-meta-grid cr-meta-grid--compact">
        <div><dt>Mapping ID</dt><dd>{mapping.mapping_id ?? "Not recorded"}</dd></div>
        <div><dt>Framework version</dt><dd>{mapping.framework_version ?? "Not recorded"}</dd></div>
        <div><dt>Release</dt><dd>{mapping.release ?? "Not recorded"}</dd></div>
        <div><dt>Profile</dt><dd>{mapping.profile ?? "Not recorded"}</dd></div>
        <div><dt>Control</dt><dd>{mapping.control_id ?? "Not recorded"}</dd></div>
        <div><dt>Control title</dt><dd>{mapping.control_title ?? "Not recorded"}</dd></div>
        <div><dt>Relationship</dt><dd>{mapping.relationship ?? "Not recorded"}</dd></div>
        <div><dt>Applicability</dt><dd>{mapping.applicability ?? "Not recorded"}</dd></div>
        <div><dt>Assessment status</dt><dd>{mapping.assessment_status ?? "Not recorded"}</dd></div>
        <div><dt>Legacy recorded result</dt><dd>{mapping.result ?? "Not recorded"}</dd></div>
        <div><dt>Test IDs</dt><dd><Chips values={mapping.test_ids ?? []} /></dd></div>
        <div><dt>Mapping source</dt><dd>{mapping.mapping_source ?? "Not recorded"}</dd></div>
        <div><dt>Mapping version</dt><dd>{mapping.mapping_version ?? "Not recorded"}</dd></div>
        <div><dt>Mapped by</dt><dd>{mapping.mapped_by ?? "Not recorded"}</dd></div>
        <div><dt>Mapped at</dt><dd><RecordedTime value={mapping.mapped_at} /></dd></div>
        <div><dt>Reviewed by</dt><dd>{mapping.reviewed_by ?? "Not recorded"}</dd></div>
        <div><dt>Reviewed at</dt><dd><RecordedTime value={mapping.reviewed_at} /></dd></div>
        <div><dt>Assessor</dt><dd>{mapping.assessor ?? "Not recorded"}</dd></div>
        <div><dt>Assessed at</dt><dd><RecordedTime value={mapping.assessed_at} /></dd></div>
        <div><dt>Source field</dt><dd>{mapping.source_key}</dd></div>
        <div><dt>Source URL</dt><dd><RecordedHttpUrl value={mapping.source_url} /></dd></div>
        <div><dt>Recorded reference</dt><dd>{mapping.recorded_reference ?? "Not recorded"}</dd></div>
      </dl>
      <div className="cr-two-up">
        <div><h6>Recorded rationale</h6><RecordedBlock value={mapping.rationale} /></div>
        <div><h6>Evidence references</h6><Chips values={mapping.evidence_references} /></div>
      </div>
      <div className="cr-two-up cr-mapping-context">
        <div><h6>Scope</h6><RecordedBlock value={mapping.scope} /></div>
        <div><h6>Context</h6><RecordedBlock value={mapping.context} /></div>
        <div><h6>Limitations</h6><RecordedBlock value={mapping.limitations} /></div>
        <div><h6>Customer statement</h6><RecordedBlock value={mapping.customer_statement} /></div>
      </div>
    </article>
  );
}

function RegulatoryProfile({ profile, index }: { profile: ReportRegulatoryProfile; index: number }) {
  return (
    <article className="cr-regulatory-profile">
      <div className="cr-mapping-head">
        <strong>
          {profile.name ?? "Profile name not recorded"}
          {profile.version ? ` · ${profile.version}` : ""}
        </strong>
        <span>{profile.profile_id ?? profile.recorded_reference ?? `Profile ${index + 1}`}</span>
      </div>
      <dl className="cr-meta-grid cr-meta-grid--compact">
        <div><dt>Profile ID</dt><dd>{profile.profile_id ?? "Not recorded"}</dd></div>
        <div><dt>Version</dt><dd>{profile.version ?? "Not recorded"}</dd></div>
        <div><dt>Jurisdiction</dt><dd>{profile.jurisdiction ?? "Not recorded"}</dd></div>
        <div><dt>Applicability</dt><dd>{profile.applicability ?? "Not recorded"}</dd></div>
        <div><dt>Selected by</dt><dd>{maskedRecordedValue(profile.selected_by) ?? "Not recorded"}</dd></div>
        <div><dt>Selected at</dt><dd><RecordedTime value={profile.selected_at} /></dd></div>
        <div><dt>Reviewed by</dt><dd>{maskedRecordedValue(profile.reviewed_by) ?? "Not recorded"}</dd></div>
        <div><dt>Reviewed at</dt><dd><RecordedTime value={profile.reviewed_at} /></dd></div>
        <div><dt>Source URL</dt><dd><RecordedHttpUrl value={profile.source_url} /></dd></div>
        <div><dt>Recorded reference</dt><dd>{profile.recorded_reference ?? "Not recorded"}</dd></div>
      </dl>
      <div className="cr-two-up cr-mapping-context">
        <div><h6>Applicability rationale</h6><RecordedBlock value={profile.rationale} /></div>
        <div><h6>Recorded scope</h6><RecordedBlock value={profile.scope} /></div>
        <div><h6>Limitations</h6><RecordedBlock value={profile.limitations} /></div>
      </div>
    </article>
  );
}

function FindingReport({ finding, ordinal }: { finding: ReportFinding; ordinal: number }) {
  const severity = toSeverity(finding.severity);
  const findingRef = `F${String(ordinal).padStart(3, "0")}`;
  const closure = finding.closure;

  return (
    <article className="cr-finding" id={`finding-${finding.id}`} style={{ "--cr-severity": SEV_COLOR[severity] } as React.CSSProperties}>
      <header className="cr-finding-head">
        <span className="cr-finding-ordinal">{findingRef}</span>
        <div>
          <div className="cr-finding-tags">
            <span className="cr-severity" data-severity={severity.toLowerCase()}>{severity}</span>
            <span className="cr-status">{displayLabel(finding.status)}</span>
            {finding.verification.needs_review && <span className="cr-chip" data-tone="risk">Needs review</span>}
          </div>
          <h3>{finding.title}</h3>
          <p>{finding.id}</p>
        </div>
      </header>

      <section className="cr-finding-section">
        <h4><ListChecks size={14} />Description, technical detail, and recorded impact</h4>
        <div className="cr-two-up">
          <div><h5>Description</h5><RecordedBlock value={finding.description} empty="No description recorded." /></div>
          <div><h5>Technical details</h5><RecordedBlock value={finding.technical_details} empty="No technical details recorded." /></div>
          <div><h5>Technical impact</h5><RecordedBlock value={finding.impact} empty="No technical impact recorded." /></div>
          <div><h5>Business impact</h5><RecordedBlock value={finding.business_impact} empty="No business impact recorded." /></div>
          <div><h5>Exploitation and attack context</h5><RecordedBlock value={finding.exploitation} empty="No exploitation context recorded." /></div>
          <div><h5>Reproduction or validation steps</h5><RecordedBlock value={finding.reproduction_steps} empty="No reproduction or validation steps recorded." /></div>
          <div><h5>Root cause</h5><RecordedBlock value={finding.root_cause} empty="No root cause recorded." /></div>
          <div><h5>Preconditions</h5><RecordedBlock value={finding.preconditions} empty="No preconditions recorded." /></div>
        </div>
      </section>

      <section className="cr-finding-section">
        <h4><Fingerprint size={14} />Finding metadata</h4>
        <dl className="cr-meta-grid">
          <div><dt>Severity</dt><dd>{finding.severity}</dd></div>
          <div><dt>Status</dt><dd>{finding.status}</dd></div>
          <div><dt>CVSS score</dt><dd>{finding.cvss_score ?? "Not recorded"}</dd></div>
          <div><dt>CVSS vector</dt><dd>{finding.cvss_vector ?? "Not recorded"}</dd></div>
          <div><dt>EPSS score</dt><dd>{finding.epss_score ?? "Not recorded"}</dd></div>
          <div><dt>Risk score</dt><dd>{finding.risk_score ?? "Not recorded"}</dd></div>
          <div><dt>Exploitable</dt><dd>{finding.exploitable ? "Yes" : "No"}</dd></div>
          <div><dt>Exploit validated</dt><dd>{finding.exploit_validated ? "Yes" : "No"}</dd></div>
          <div><dt>Detection status</dt><dd>{finding.detection_status}</dd></div>
          <div><dt>Initial detection run</dt><dd>{finding.initial_detection_run_id ?? "Not recorded"}</dd></div>
          <div><dt>Latest observation run</dt><dd>{finding.detection_run_id ?? "Not recorded"}</dd></div>
          <div><dt>Detection DB version</dt><dd>{finding.detected_db_version ?? "Not recorded"}</dd></div>
          <div><dt>First seen</dt><dd><RecordedTime value={finding.first_seen} /></dd></div>
          <div><dt>Last seen</dt><dd><RecordedTime value={finding.last_seen} /></dd></div>
          <div><dt>Created</dt><dd><RecordedTime value={finding.created_at} /></dd></div>
          <div><dt>Updated</dt><dd><RecordedTime value={finding.updated_at} /></dd></div>
        </dl>
        <div className="cr-reference-row">
          <div><strong>CVEs</strong><Chips values={finding.cve_ids} tone="risk" /></div>
          <div><strong>CWEs</strong><Chips values={finding.cwe_ids} /></div>
          <div><strong>MITRE ATT&amp;CK</strong><Chips values={finding.mitre_techniques} tone="accent" /></div>
        </div>
      </section>

      <section className="cr-finding-section">
        <h4><Fingerprint size={14} />Detection and scan provenance</h4>
        <p className="cr-caution"><AlertTriangle size={13} />Initial discovery and latest observation are separate records. A later analyst update is not presented as scan evidence.</p>
        <div className="cr-two-up cr-run-grid">
          <DetectionRunProvenance provenance={finding.initial_detection_provenance} heading="Initial discovery scan" />
          <DetectionRunProvenance provenance={finding.latest_detection_provenance} heading="Latest observation scan" />
        </div>
      </section>

      <section className="cr-finding-section">
        <h4><Server size={14} />Affected asset</h4>
        {finding.asset ? (
          <dl className="cr-meta-grid">
            <div><dt>Asset ID</dt><dd>{finding.asset.id}</dd></div>
            <div><dt>IP address</dt><dd>{finding.asset.ip_address ?? "Not recorded"}</dd></div>
            <div><dt>Hostname</dt><dd>{finding.asset.hostname ?? "Not recorded"}</dd></div>
            <div><dt>FQDN</dt><dd>{finding.asset.fqdn ?? "Not recorded"}</dd></div>
            <div><dt>Type</dt><dd>{finding.asset.asset_type}</dd></div>
            <div><dt>Criticality</dt><dd>{finding.asset.criticality}</dd></div>
            <div><dt>Operating system</dt><dd>{[finding.asset.os, finding.asset.os_version].filter(Boolean).join(" ") || "Not recorded"}</dd></div>
            <div><dt>Environment</dt><dd>{finding.asset.environment ?? "Not recorded"}</dd></div>
            <div><dt>Owner</dt><dd>{finding.asset.owner ?? "Not recorded"}</dd></div>
            <div><dt>Last seen</dt><dd><RecordedTime value={finding.asset.last_seen} /></dd></div>
            <div className="cr-wide"><dt>Tags</dt><dd><RecordedBlock value={finding.asset.tags} empty="None recorded" /></dd></div>
          </dl>
        ) : <p className="cr-missing"><FileWarning size={13} />No asset context is recorded for this finding.</p>}
      </section>

      <section className="cr-finding-section">
        <h4><ClipboardCheck size={14} />Verification record and current SLA projection</h4>
        <div className="cr-two-up">
          <dl className="cr-meta-grid cr-meta-grid--compact">
            <div><dt>Verification state</dt><dd>{finding.verification.state ?? "Not recorded"}</dd></div>
            <div><dt>Confidence</dt><dd>{finding.verification.confidence ?? "Not recorded"}</dd></div>
            <div><dt>Method</dt><dd>{finding.verification.method ?? "Not recorded"}</dd></div>
            <div><dt>Needs review</dt><dd>{finding.verification.needs_review ? "Yes" : "No"}</dd></div>
            <div className="cr-wide"><dt>Rationale</dt><dd>{finding.verification.rationale ?? "Not recorded"}</dd></div>
          </dl>
          <div className="cr-projection">
            <h5><Clock size={12} />Current policy projection — not historical</h5>
            <dl className="cr-inline-meta">
              <div><dt>State</dt><dd>{finding.current_sla.state}</dd></div>
              <div><dt>Deadline</dt><dd><RecordedTime value={finding.current_sla.deadline} /></dd></div>
              <div><dt>Hours remaining</dt><dd>{finding.current_sla.hours_remaining ?? "Not tracked"}</dd></div>
              <div><dt>Policy hours</dt><dd>{finding.current_sla.hours_total ?? "Not tracked"}</dd></div>
              <div><dt>Calculated</dt><dd><RecordedTime value={finding.current_sla.calculated_at} /></dd></div>
              <div><dt>Basis</dt><dd>{finding.current_sla.policy_basis}</dd></div>
            </dl>
          </div>
        </div>
      </section>

      <section className="cr-finding-section">
        <h4><Clock size={14} />Action tracking and planned closure</h4>
        <dl className="cr-meta-grid">
          <div><dt>Action owner</dt><dd>{maskedRecordedValue(finding.action_tracking.owner) ?? "Not recorded"}</dd></div>
          <div><dt>Planned closure</dt><dd><RecordedTime value={finding.action_tracking.planned_closure_at} /></dd></div>
          <div><dt>Action reference</dt><dd>{maskedRecordedValue(finding.action_tracking.action_reference) ?? "Not recorded"}</dd></div>
          <div><dt>Tracking recorded at</dt><dd><RecordedTime value={finding.action_tracking.recorded_at} /></dd></div>
          <div className="cr-wide"><dt>Reason not yet closed</dt><dd><RecordedBlock value={finding.action_tracking.non_closure_reason} empty="No non-closure reason recorded." /></dd></div>
        </dl>
      </section>

      <section className="cr-finding-section">
        <h4><Terminal size={14} />Recorded evidence</h4>
        <EvidenceSet evidence={finding.evidence} prefix={findingRef} empty="No evidence artifact is recorded for this finding." />
      </section>

      <section className="cr-finding-section">
        <h4><Wrench size={14} />Remediation and recommendations</h4>
        <div className="cr-subsection">
          <h5>Recorded remediation text</h5>
          <RecordedBlock value={finding.remediation.recorded_text} empty="No remediation text recorded." />
          <dl className="cr-inline-meta cr-remediation-meta">
            <div><dt>Text updated at</dt><dd><RecordedTime value={finding.remediation.recorded_text_timestamp} /></dd></div>
            <div><dt>Text updated by</dt><dd>{maskedRecordedValue(finding.remediation.recorded_text_updated_by) ?? "Not recorded"}</dd></div>
          </dl>
          {finding.remediation.timestamp_gap && (
            <p className="cr-missing"><FileWarning size={13} />{gapLabel(finding.remediation.timestamp_gap)} <code>{finding.remediation.timestamp_gap}</code></p>
          )}
        </div>
        <div className="cr-subsection">
          <h5>Recorded recommendations</h5>
          {finding.remediation.recorded_recommendations.length ? (
            <ul className="cr-list">{finding.remediation.recorded_recommendations.map((recommendation, index) => <li key={`${index}-${recommendation}`}>{maskedRecordedValue(recommendation)}</li>)}</ul>
          ) : <p className="cr-unset">No recommendations recorded.</p>}
        </div>
        <div className="cr-stack">
          {finding.remediation.reviewed_plans.map((plan) => <RemediationPlan key={plan.id} plan={plan} />)}
        </div>
        <GapList gaps={finding.remediation.gaps} />
      </section>

      <section className="cr-finding-section cr-closure">
        <h4><FileCheck2 size={14} />Closure, retest, and disposition evidence</h4>
        <dl className="cr-meta-grid">
          <div><dt>Current disposition</dt><dd>{closure.current_disposition}</dd></div>
          <div><dt>Terminal disposition</dt><dd>{closure.is_terminal ? "Yes" : "No"}</dd></div>
          <div><dt>Resolved at</dt><dd><RecordedTime value={closure.resolved_at} /></dd></div>
          <div><dt>Resolution method</dt><dd>{closure.resolution_method ?? "Not recorded"}</dd></div>
          <div><dt>Resolution run ID</dt><dd>{closure.resolution_run_id ?? "Not recorded"}</dd></div>
          <div><dt>Resolution miss count</dt><dd>{closure.resolution_miss_count}</dd></div>
          <div><dt>Reopened count</dt><dd>{closure.reopened_count}</dd></div>
          <div><dt>Closure reviewed by</dt><dd>{maskedRecordedValue(closure.reviewed_by) ?? "Not recorded"}</dd></div>
        </dl>

        {!closure.is_terminal && (
          <p className="cr-caution"><AlertTriangle size={13} />The canonical record does not identify this finding as having a terminal disposition.</p>
        )}
        {closure.latest_terminal_event ? (
          <div className="cr-subsection">
            <h5>Latest terminal event</h5>
            <EventRecord event={closure.latest_terminal_event} heading={closure.latest_terminal_event.label} />
          </div>
        ) : (
          <p className="cr-missing"><FileWarning size={13} />No terminal event is recorded.</p>
        )}

        <div className="cr-subsection">
          <h5>Retest record</h5>
          <RetestRecord retest={closure.retest} findingRef={findingRef} />
        </div>

        <div className="cr-subsection">
          <h5>Recorded closure / post-fix evidence</h5>
          <EvidenceSet
            evidence={closure.recorded_closure_evidence}
            prefix={`${findingRef}/CLOSE`}
            empty="No closure, post-fix, retest, or contradiction evidence artifact is recorded."
          />
        </div>

        {closure.auto_resolution_coverage && <AutoResolutionCoverage coverage={closure.auto_resolution_coverage} />}

        <div className="cr-subsection">
          <h5><History size={12} />Terminal and reopen history</h5>
          {closure.terminal_and_reopen_history.length ? (
            <div className="cr-stack">
              {closure.terminal_and_reopen_history.map((event, index) => (
                <EventRecord key={event.id ?? `${event.event_type}-${event.occurred_at}-${index}`} event={event} />
              ))}
            </div>
          ) : <p className="cr-unset">No terminal or reopen events recorded.</p>}
        </div>
        <GapList gaps={closure.completeness_gaps} empty="No closure completeness gaps were identified by the canonical read model." />
      </section>

      <section className="cr-finding-section">
        <h4><ShieldCheck size={14} />Recorded compliance mappings</h4>
        <p className="cr-caution"><AlertTriangle size={13} />Mappings are recorded references only. They are not certification, attestation, or a compliance verdict.</p>
        {finding.compliance_mappings.length ? (
          <div className="cr-stack">
            {finding.compliance_mappings.map((mapping, index) => (
              <ComplianceMapping key={mapping.mapping_id ?? `${mapping.source_key}-${mapping.control_id ?? mapping.recorded_reference ?? index}`} mapping={mapping} index={index} />
            ))}
          </div>
        ) : <p className="cr-missing"><FileWarning size={13} />No finding-to-control mapping is recorded.</p>}
      </section>

      <section className="cr-finding-section">
        <h4><History size={14} />Complete finding lifecycle</h4>
        {finding.lifecycle.length ? (
          <div className="cr-stack">
            {finding.lifecycle.map((event, index) => (
              <EventRecord key={event.id ?? `${event.event_type}-${event.occurred_at}-${index}`} event={event} />
            ))}
          </div>
        ) : <p className="cr-unset">No lifecycle events recorded.</p>}
      </section>

      <section className="cr-finding-section cr-readiness">
        <h4><FileWarning size={14} />Finding readiness gaps</h4>
        <GapList gaps={finding.readiness_gaps} empty="No finding-level gaps were identified by the canonical read model." />
      </section>
    </article>
  );
}

function SectionHeading({ id, title, description }: { id: string; title: string; description: string }) {
  return (
    <header className="cr-section-head">
      <h2 id={id}>{title}</h2>
      <p>{description}</p>
    </header>
  );
}

export function CanonicalReportDocument({ report }: { report: ReportDocument }) {
  const metadata = report.engagement.recorded_report_metadata;
  const methodology = metadata.methodology;
  const limitations = metadata.limitations;
  const riskRatingMethod = metadata.risk_rating_method;
  const toolsUsed = metadata.tools_used;
  const testingNarrative = metadata.testing_narrative;
  const segmentationResults = metadata.segmentation_results;
  const environmentCleanup = metadata.environment_cleanup;
  const evidenceRetentionPolicy = metadata.evidence_retention_policy;
  const severityRows = Object.entries(report.summary.by_severity);
  const statusRows = Object.entries(report.summary.by_status);
  const statusKeys = Object.keys(report.summary.by_status);
  const configuredDisplayTimeZone = report.document.display_timezone || "UTC";
  const displayTimeZone = usableTimeZone(configuredDisplayTimeZone);
  const profileLabels = report.engagement.regulatory_profiles.map(
    (profile, index) => profile.name ?? profile.profile_id ?? profile.recorded_reference ?? `Profile ${index + 1}`,
  );

  return (
    <ReportTimeZoneContext.Provider value={displayTimeZone}>
    <article className="report-document cr-report" aria-label={`${report.engagement.name} vulnerability assessment report`}>
      <header className="report-cover cr-cover">
        <div className="cr-cover-main">
          <span><LockKeyhole size={13} />LIVE, NON-PERSISTED OPERATOR DRAFT</span>
          <h1>{report.engagement.name}</h1>
          <p>{report.engagement.client ?? "Client not recorded"} · Vulnerability assessment report</p>
          <div className="cr-cover-warning">
            This view is generated from the current read model. It is not an approved, published, or immutable report record.
          </div>
        </div>
        <dl>
          <div><dt>Engagement ID</dt><dd>{report.engagement.id}</dd></div>
          <div><dt>Schema version</dt><dd>{report.document.schema_version}</dd></div>
          <div><dt>Report version</dt><dd>{maskedRecordedValue(metadata.version) ?? "Not recorded"}</dd></div>
          <div><dt>Classification</dt><dd>{maskedRecordedValue(metadata.classification) ?? "Not recorded"}</dd></div>
          <div><dt>Generated at (exact)</dt><dd><code>{report.document.generated_at}</code> {report.document.timezone}</dd></div>
          <div><dt>Display timezone</dt><dd>{configuredDisplayTimeZone}{displayTimeZone !== configuredDisplayTimeZone ? ` (rendered as ${displayTimeZone})` : ""}</dd></div>
          <div><dt>Snapshot</dt><dd>{report.document.snapshot_kind} · persisted: {String(report.document.persisted)}</dd></div>
        </dl>
      </header>

      <nav className="cr-section-nav no-print" aria-label="Report sections">
        <a href="#document-control">Document control</a>
        <a href="#executive-summary">Executive summary</a>
        <a href="#scope-readiness">Scope &amp; readiness</a>
        <a href="#finding-register">Finding register</a>
        <a href="#closure-register">Retest &amp; closure</a>
        <a href="#compliance-matrix">Compliance mappings</a>
        <a href="#methodology-limitations">Methodology &amp; limitations</a>
      </nav>

      <div className="cr-report-body">
        <section className="cr-report-section" aria-labelledby="document-control">
          <SectionHeading id="document-control" title="Document control" description="Recorded engagement metadata and live document generation facts." />
          <dl className="cr-meta-grid">
            {CONTROL_FIELDS.map(([key, label]) => (
              <div key={key}>
                <dt>{label}</dt>
                <dd>{CONTROL_TIME_FIELDS.has(key)
                  ? <RecordedTime value={typeof metadata[key] === "string" ? metadata[key] : null} />
                  : maskedRecordedValue(metadata[key]) ?? "Not recorded"}</dd>
              </div>
            ))}
            <div><dt>Engagement status</dt><dd>{report.engagement.status}</dd></div>
            <div><dt>Lead assessor</dt><dd>{report.engagement.assessor ?? "Not recorded"}</dd></div>
            <div><dt>Engagement created</dt><dd><RecordedTime value={report.engagement.created_at} /></dd></div>
            <div><dt>Engagement updated</dt><dd><RecordedTime value={report.engagement.updated_at} /></dd></div>
            <div><dt>Document timezone</dt><dd>{report.document.timezone}</dd></div>
            <div><dt>Configured display timezone</dt><dd>{configuredDisplayTimeZone}</dd></div>
            <div><dt>Persisted report record</dt><dd>No</dd></div>
          </dl>
          <GapList gaps={report.engagement.metadata_gaps} empty="No document-control metadata gaps were identified by the canonical read model." />
        </section>

        <section className="cr-report-section" aria-labelledby="executive-summary">
          <SectionHeading id="executive-summary" title="Executive summary" description="Deterministic counts from the canonical finding set; no generated risk narrative." />
          <p className="cr-executive-copy">{executiveSummaryText(report.summary)}</p>
          <div className="cr-summary-strip">
            <div><span>Total findings</span><strong>{report.summary.total_findings}</strong></div>
            <div><span>Open or confirmed</span><strong>{report.summary.open_or_confirmed}</strong></div>
            <div><span>Terminal dispositions</span><strong>{report.summary.terminal}</strong></div>
            <div><span>Reopen history</span><strong>{report.summary.findings_with_reopen_history}</strong></div>
          </div>
          <div className="cr-two-up">
            <div className="cr-table-wrap">
              <table className="cr-table">
                <caption>Open and terminal findings by recorded severity</caption>
                <thead><tr><th scope="col">Severity</th><th scope="col">Total</th><th scope="col">Open / confirmed</th><th scope="col">Terminal</th></tr></thead>
                <tbody>{severityRows.map(([severity, count]) => (
                  <tr key={severity}>
                    <th scope="row">{displayLabel(severity)}</th>
                    <td>{count}</td>
                    <td>{report.summary.open_by_severity[severity] ?? 0}</td>
                    <td>{report.summary.terminal_by_severity[severity] ?? 0}</td>
                  </tr>
                ))}</tbody>
              </table>
            </div>
            <div className="cr-table-wrap">
              <table className="cr-table">
                <caption>Findings by recorded status</caption>
                <thead><tr><th scope="col">Status</th><th scope="col">Count</th></tr></thead>
                <tbody>{statusRows.map(([status, count]) => <tr key={status}><th scope="row">{displayLabel(status)}</th><td>{count}</td></tr>)}</tbody>
              </table>
            </div>
          </div>
          <p className="cr-caution"><AlertTriangle size={13} />“Terminal” is an operational disposition aggregate. Remediated, risk-accepted, and false-positive records remain distinct below and are not presented as a regulatory closure conclusion.</p>
          <div className="cr-table-wrap cr-subsection">
            <table className="cr-table">
              <caption>Recorded severity × status cross-tab</caption>
              <thead>
                <tr><th scope="col">Severity</th>{statusKeys.map((status) => <th scope="col" key={status}>{displayLabel(status)}</th>)}</tr>
              </thead>
              <tbody>
                {severityRows.map(([severity]) => (
                  <tr key={severity}>
                    <th scope="row">{displayLabel(severity)}</th>
                    {statusKeys.map((status) => <td key={status}>{report.summary.by_severity_status[severity]?.[status] ?? 0}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="cr-report-section" aria-labelledby="scope-readiness">
          <SectionHeading id="scope-readiness" title="Scope and record readiness" description="Recorded assessment boundary and explicit completeness gaps." />
          <div className="cr-two-up">
            <div>
              <h3>Assessment scope</h3>
              <dl className="cr-meta-grid cr-meta-grid--compact">
                <div><dt>Start time</dt><dd><RecordedTime value={report.engagement.start_time} /></dd></div>
                <div><dt>End time</dt><dd><RecordedTime value={report.engagement.end_time} /></dd></div>
                <div className="cr-wide"><dt>In-scope CIDRs</dt><dd><Chips values={report.engagement.scope_cidrs} tone="accent" /></dd></div>
                <div className="cr-wide"><dt>Excluded CIDRs</dt><dd><Chips values={report.engagement.excluded_cidrs} /></dd></div>
                <div className="cr-wide"><dt>Tags</dt><dd><Chips values={report.engagement.tags} /></dd></div>
                <div className="cr-wide"><dt>Selected regulatory profiles</dt><dd><Chips values={profileLabels} tone="accent" /></dd></div>
              </dl>
              <h4>Recorded engagement description</h4>
              <RecordedBlock value={report.engagement.description} />
            </div>
            <div className="cr-readiness-panel" data-complete={report.readiness.complete}>
              <h3>{report.readiness.complete ? <CheckCircle2 size={15} /> : <AlertTriangle size={15} />}Canonical record check</h3>
              <p>{report.readiness.complete
                ? "No configured completeness gaps were identified. This does not constitute approval for delivery."
                : "The live record contains gaps that require operator review before customer delivery."}</p>
              <GapList gaps={report.readiness.report_gaps} />
              {Object.keys(report.readiness.gap_counts).length > 0 && (
                <div className="cr-table-wrap">
                  <table className="cr-table">
                    <caption>Finding-level gap inventory</caption>
                    <thead><tr><th scope="col">Gap</th><th scope="col">Count</th><th scope="col">Affected finding IDs</th></tr></thead>
                    <tbody>
                      {Object.entries(report.readiness.gap_counts).map(([gap, count]) => (
                        <tr key={gap}>
                          <th scope="row"><span>{gapLabel(gap)}</span><code>{gap}</code></th>
                          <td>{count}</td>
                          <td><Chips values={report.readiness.affected_finding_ids[gap] ?? []} /></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </section>

        <section className="cr-report-section cr-findings-section" aria-labelledby="finding-register">
          <SectionHeading id="finding-register" title="Complete finding register" description={`${report.findings.length} canonical finding record${report.findings.length === 1 ? "" : "s"}, including evidence, remediation, closure, lifecycle, and mapping gaps.`} />
          {report.findings.length ? (
            <div className="cr-finding-list">
              {report.findings.map((finding, index) => <FindingReport key={finding.id} finding={finding} ordinal={index + 1} />)}
            </div>
          ) : <p className="cr-missing"><FileWarning size={13} />No findings are recorded for this engagement.</p>}
        </section>

        <section className="cr-report-section" aria-labelledby="closure-register">
          <SectionHeading id="closure-register" title="Retest and closure register" description="Document-level disposition, review, and before/after retest evidence derived from the complete finding set." />
          <div className="cr-table-wrap">
            <table className="cr-table cr-closure-register">
              <caption>Closure and retest status for every finding</caption>
              <thead>
                <tr>
                  <th scope="col">Finding</th>
                  <th scope="col">Severity / disposition</th>
                  <th scope="col">Closure record</th>
                  <th scope="col">Retest verification</th>
                  <th scope="col">History / gaps</th>
                </tr>
              </thead>
              <tbody>
                {report.findings.map((finding, index) => {
                  const retest = finding.closure.retest;
                  return (
                    <tr key={finding.id}>
                      <th scope="row"><a href={`#finding-${finding.id}`}>F{String(index + 1).padStart(3, "0")} · {finding.title}</a></th>
                      <td>{displayLabel(finding.severity)}<br />{displayLabel(finding.closure.current_disposition)}</td>
                      <td><RecordedTime value={finding.closure.resolved_at} />{finding.closure.resolution_method ?? "Method not recorded"}<br />{maskedRecordedValue(finding.closure.reviewed_by) ?? "Reviewer not recorded"}</td>
                      <td>{retest?.passed === true ? "Passed" : retest?.passed === false ? "Failed" : "Not recorded"}<br /><RecordedTime value={retest?.verified_at} />Before / after artifacts: {retest?.before_evidence.artifacts.length ?? 0} / {retest?.after_evidence.artifacts.length ?? 0}</td>
                      <td>Reopened: {finding.closure.reopened_count}<br /><Chips values={finding.closure.completeness_gaps} /></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>

        <section className="cr-report-section" aria-labelledby="compliance-matrix">
          <SectionHeading id="compliance-matrix" title="Versioned compliance mapping roll-up" description="Only mappings explicitly recorded on findings are included." />
          <p className="cr-caution"><AlertTriangle size={13} />This matrix is not a certification, audit opinion, or compliance verdict. Unrecorded controls are not inferred.</p>
          <dl className="cr-inline-meta">
            <div><dt>Source</dt><dd>{report.compliance_rollup.source}</dd></div>
            <div><dt>Recorded mappings</dt><dd>{report.compliance_rollup.mapping_count}</dd></div>
            <div><dt>Unmapped findings</dt><dd>{report.compliance_rollup.unmapped_finding_ids.length}</dd></div>
          </dl>
          <div className="cr-subsection">
            <h3>Selected regulatory profiles</h3>
            <p className="cr-caution"><AlertTriangle size={13} />A selected profile records applicability context only. It does not by itself establish compliance, and no conditional annexure or obligation is inferred.</p>
            {report.compliance_rollup.regulatory_profiles.length ? (
              <div className="cr-stack">
                {report.compliance_rollup.regulatory_profiles.map((profile, index) => (
                  <RegulatoryProfile key={profile.profile_id ?? profile.recorded_reference ?? `${profile.name ?? "profile"}-${index}`} profile={profile} index={index} />
                ))}
              </div>
            ) : <p className="cr-missing"><FileWarning size={13} />No regulatory profile selection is recorded.</p>}
          </div>
          {report.compliance_rollup.gap && <p className="cr-missing"><FileWarning size={13} />{report.compliance_rollup.gap}</p>}
          {report.compliance_rollup.frameworks.length ? (
            <div className="cr-stack">
              {report.compliance_rollup.frameworks.map((framework, index) => (
                <article className="cr-framework" key={`${framework.framework ?? "unrecorded"}-${framework.framework_version ?? index}`}>
                  <header>
                    <div><h3>{framework.framework ?? "Framework not recorded"}</h3><p>Version {framework.framework_version ?? "not recorded"}</p></div>
                    <span>{framework.mapping_count} mapping{framework.mapping_count === 1 ? "" : "s"} · {framework.finding_count} finding{framework.finding_count === 1 ? "" : "s"}</span>
                  </header>
                  <div className="cr-table-wrap">
                    <table className="cr-table">
                      <caption>Recorded controls for {framework.framework ?? "unrecorded framework"} {framework.framework_version ?? ""}</caption>
                      <thead><tr><th scope="col">Control ID</th><th scope="col">Control title</th><th scope="col">Recorded results</th><th scope="col">Finding IDs</th></tr></thead>
                      <tbody>
                        {framework.controls.map((control, controlIndex) => (
                          <tr key={`${control.control_id ?? "unrecorded"}-${controlIndex}`}>
                            <th scope="row">{control.control_id ?? "Not recorded"}</th>
                            <td>{control.control_title ?? "Not recorded"}</td>
                            <td><Chips values={control.recorded_results} /></td>
                            <td><Chips values={control.finding_ids} /></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </article>
              ))}
            </div>
          ) : <p className="cr-unset">No framework roll-up is available.</p>}
          {report.compliance_rollup.unmapped_finding_ids.length > 0 && (
            <div className="cr-subsection"><h3>Findings without recorded mappings</h3><Chips values={report.compliance_rollup.unmapped_finding_ids} /></div>
          )}
        </section>

        <section className="cr-report-section" aria-labelledby="methodology-limitations">
          <SectionHeading id="methodology-limitations" title="Methodology and limitations" description="Recorded report metadata only; missing boundaries are stated explicitly." />
          <div className="cr-method-grid">
            <div><h3>Methodology</h3><RecordedBlock value={methodology} empty="No methodology is recorded in report metadata." /></div>
            <div><h3>Risk-rating method</h3><RecordedBlock value={riskRatingMethod} empty="No risk-rating method is recorded in report metadata." /></div>
            <div><h3>Testing narrative</h3><RecordedBlock value={testingNarrative} empty="No testing narrative is recorded in report metadata." /></div>
            <div><h3>Tools used</h3><RecordedBlock value={toolsUsed} empty="No assessment tools are recorded in report metadata." /></div>
            <div><h3>Segmentation results</h3><RecordedBlock value={segmentationResults} empty="No segmentation-test results are recorded in report metadata." /></div>
            <div><h3>Environment cleanup</h3><RecordedBlock value={environmentCleanup} empty="No environment-cleanup record is present." /></div>
            <div><h3>Evidence retention policy</h3><RecordedBlock value={evidenceRetentionPolicy} empty="No evidence-retention policy is recorded." /></div>
            <div><h3>Limitations</h3><RecordedBlock value={limitations} empty="No limitations are recorded in report metadata." /></div>
          </div>
          <p className="cr-caution"><AlertTriangle size={13} />Absence of a recorded limitation does not establish that the assessment had no limitations.</p>
        </section>
      </div>

      <footer className="report-footer cr-footer">
        <Link2 size={12} />
        Vedha canonical schema {report.document.schema_version} · live read model · generated {formatTimestamp(report.document.generated_at, displayTimeZone) ?? report.document.generated_at} · exact {exactUtcTimestamp(report.document.generated_at)}
      </footer>
    </article>
    </ReportTimeZoneContext.Provider>
  );
}
