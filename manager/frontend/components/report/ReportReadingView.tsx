"use client";

/**
 * Reading view of the canonical report: what a security lead or a customer
 * reads first. Everything here comes from the shared presentation layer
 * (lib/report/presentation.ts), so the page, the PDF and the Word document say
 * the same thing. The complete canonical record of every finding stays one
 * click away (see CanonicalReportDocument).
 */
import { useMemo, useState } from "react";
import { ChevronRight, ShieldAlert, ShieldCheck, Terminal } from "lucide-react";

import {
  SEVERITY_LABEL,
  closureView,
  compactRefs,
  evidenceView,
  excerpt,
  executiveNarrative,
  findingNarrative,
  formatDate,
  formatDateTime,
  gapInventory,
  groupAssets,
  groupRef,
  isOpenStatus,
  issueFacts,
  issueFixBy,
  keyMetrics,
  maskedText,
  overallRating,
  priorityLines,
  remediationRoadmap,
  remediationView,
  severityRows,
  sharedNarrativeKeys,
  slaLabel,
  statusSummary,
  topRisks,
  type IssueGroup,
  type Readable,
  type SeverityKey,
} from "../../lib/report/presentation";
import type { ReportDocument, ReportEvidence, ReportFinding } from "../../lib/report/report-document";

export const issueAnchor = (index: number) => `issue-${index + 1}`;

export function SeverityPill({ severity, label }: { severity: SeverityKey | "none"; label?: string }) {
  return (
    <span className="rr-pill" data-severity={severity}>
      {label ?? (severity === "none" ? "None" : SEVERITY_LABEL[severity])}
    </span>
  );
}

function ReadableBlock({ body }: { body: Readable }) {
  if (body.kind === "text") return <div className="rr-prose">{body.paragraphs.map((p, i) => <p key={i}>{p}</p>)}</div>;
  if (body.kind === "list") return <ul className="rr-list">{body.items.map((item, i) => <li key={i}>{item}</li>)}</ul>;
  return (
    <dl className="rr-pairs">
      {body.rows.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}
    </dl>
  );
}

// ─── Cover ───────────────────────────────────────────────────────────────────

export function ReportCover({ report, tz, issued }: { report: ReportDocument; tz: string; issued: boolean }) {
  const meta = report.engagement.recorded_report_metadata;
  const rating = overallRating(report);
  const rows = severityRows(report);
  const max = Math.max(1, ...rows.map((r) => r.total));
  const period = maskedText(meta.reporting_period)
    ?? ([formatDate(report.engagement.start_time, tz), formatDate(report.engagement.end_time, tz)].filter(Boolean).join(" – ") || null);
  const facts: Array<[string, string | null]> = [
    ["Assessment period", period],
    ["Report version", maskedText(meta.version)],
    ["Classification", maskedText(meta.classification)],
    ["Document status", maskedText(meta.document_status) ?? (issued ? "Issued" : "Draft")],
    ["Prepared by", maskedText(meta.prepared_by) ?? maskedText(report.engagement.assessor)],
    ["Generated", formatDateTime(report.document.generated_at, tz)],
  ];
  return (
    <header className="rr-cover">
      <div className="rr-cover-main">
        <p className="rr-eyebrow">Vulnerability assessment report</p>
        <h1>{report.engagement.name}</h1>
        <p className="rr-cover-client" hidden={!report.engagement.client}>
          {report.engagement.client ? <>Prepared for <strong>{maskedText(report.engagement.client)}</strong></> : null}
        </p>
        {!issued && <p className="rr-draft-flag">Draft — not approved. Human review is required before delivery.</p>}
        <dl className="rr-cover-facts">
          {facts.filter(([, v]) => v).map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}
        </dl>
      </div>
      <aside className="rr-cover-rating" data-level={rating.level} aria-label="Overall risk">
        <span className="rr-label">Overall risk</span>
        <strong>{rating.label}</strong>
        <p>{rating.basis}</p>
        <ul className="rr-sev-bars" aria-label="Findings by severity">
          {rows.map((r) => (
            <li key={r.severity} data-severity={r.severity}>
              <span>{SEVERITY_LABEL[r.severity]}</span>
              <span className="rr-bar" aria-hidden="true">
                <i style={{ width: `${(r.open / max) * 100}%` }} data-part="open" />
                <i style={{ width: `${(r.closed / max) * 100}%` }} data-part="closed" />
              </span>
              <b>{r.open}<small>/{r.total}</small></b>
            </li>
          ))}
        </ul>
        <small className="rr-muted">Open / recorded. Rating rule: highest severity among open findings.</small>
      </aside>
    </header>
  );
}

// ─── Executive summary ───────────────────────────────────────────────────────

export function ExecutiveSummary({ report, tz, groups }: { report: ReportDocument; tz: string; groups: IssueGroup[] }) {
  const m = keyMetrics(report);
  const narrative = executiveNarrative(report, tz);
  const top = topRisks(report, 5);
  const priorities = priorityLines(report);
  const tiles: Array<{ label: string; value: number; tone: "neutral" | "risk" | "ok" | "warn" }> = [
    { label: "Open findings", value: m.open, tone: "neutral" },
    { label: "Critical and high open", value: m.criticalHighOpen, tone: m.criticalHighOpen ? "risk" : "ok" },
    { label: "Overdue against the SLA", value: m.slaBreached, tone: m.slaBreached ? "warn" : "ok" },
    { label: "Assets with open findings", value: m.assetsAffected, tone: "neutral" },
  ];
  return (
    <div className="rr-exec">
      <div className="rr-exec-copy">
        {narrative.sentences.map((s, i) => <p key={i} className={i === narrative.ratingIndex ? "rr-lead" : undefined}>{s}</p>)}
      </div>
      <div className="rr-tiles">
        {tiles.map((t) => (
          <div key={t.label} className="rr-tile" data-tone={t.tone}>
            <strong>{t.value}</strong>
            <span>{t.label}</span>
          </div>
        ))}
      </div>
      <div className="rr-two">
        <section>
          <h3 className="rr-h3">Top open risks</h3>
          {top.length ? (
            <ol className="rr-top">
              {top.map(({ ref, group }) => {
                const index = groups.indexOf(group);
                const live = group.findings.filter((f) => isOpenStatus(f.status));
                const fix = issueFixBy(group, tz);
                return (
                  <li key={group.key}>
                    <SeverityPill severity={group.severity} />
                    <div>
                      <a href={`#${issueAnchor(index)}`}>{group.title}</a>
                      <span className="rr-muted">{ref} · {groupAssets(live) ?? "asset not recorded"}{fix.text ? ` · fix by ${fix.text}` : ""}</span>
                    </div>
                  </li>
                );
              })}
            </ol>
          ) : <p className="rr-ok-note"><ShieldCheck size={14} />No findings are open.</p>}
        </section>
        <section>
          <h3 className="rr-h3">Recommended priorities</h3>
          {priorities.length ? <ul className="rr-list">{priorities.map((p) => <li key={p}>{p}</li>)}</ul> : <p className="rr-muted">Nothing outstanding.</p>}
        </section>
      </div>
    </div>
  );
}

// ─── Findings overview ───────────────────────────────────────────────────────

export function FindingsOverview({ groups, refs, total }: { groups: IssueGroup[]; refs: Map<string, string>; total: number }) {
  if (!groups.length) return <p className="rr-muted">No findings are recorded for this engagement.</p>;
  const anyCvss = groups.some((g) => g.findings.some((f) => f.cvss_score !== null && f.cvss_score !== ""));
  return (
    <>
      <p className="rr-muted">
        {total} finding{total === 1 ? "" : "s"}{groups.length < total ? ` across ${groups.length} distinct issues` : ""}, most severe first.
        {groups.length < total ? " An issue found on several assets is listed once." : ""}
      </p>
      <div className="rr-table-wrap">
        <table className="rr-table">
          <thead><tr><th scope="col">Ref</th><th scope="col">Finding</th><th scope="col">Severity</th>{anyCvss && <th scope="col">CVSS</th>}<th scope="col">Assets</th><th scope="col">Status</th></tr></thead>
          <tbody>
            {groups.map((g, i) => {
              const cvss = [...new Set(g.findings.map((f) => f.cvss_score).filter((v) => v !== null && v !== "").map(String))];
              return (
                <tr key={g.key}>
                  <td className="rr-ref">{groupRef(g, refs)}</td>
                  <td><a href={`#${issueAnchor(i)}`}>{g.title}</a></td>
                  <td><SeverityPill severity={g.severity} /></td>
                  {anyCvss && <td>{cvss.length === 0 ? "—" : cvss.length === 1 ? cvss[0] : "varies"}</td>}
                  <td>{groupAssets(g.findings) ?? "—"}</td>
                  <td data-open={g.open > 0}>{statusSummary(g.findings)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {!anyCvss && <p className="rr-muted rr-small">No CVSS scores are recorded for these findings.</p>}
    </>
  );
}

// ─── One issue ───────────────────────────────────────────────────────────────

function EvidenceExcerpts({ evidence, prefix, tz }: { evidence: ReportEvidence; prefix: string; tz: string }) {
  return (
    <div className="rr-evidence">
      {evidence.artifacts.map((artifact) => {
        const view = evidenceView(artifact, `${prefix}/E${String(artifact.index).padStart(2, "0")}`);
        return <EvidenceExcerpt key={view.ref} view={view} tz={tz} />;
      })}
    </div>
  );
}

function EvidenceExcerpt({ view, tz }: { view: ReturnType<typeof evidenceView>; tz: string }) {
  const [all, setAll] = useState(false);
  const cut = useMemo(() => excerpt(view.content || "No evidence content recorded.", 24), [view.content]);
  return (
    <figure className="rr-ev">
      <figcaption>
        <Terminal size={12} aria-hidden="true" />
        <b>{view.ref}</b>
        <span>{[view.label, view.tool, formatDateTime(view.capturedAt, tz)].filter(Boolean).join(" · ")}</span>
      </figcaption>
      {view.command && <pre className="rr-cmd"><span aria-hidden="true">$ </span>{view.command}</pre>}
      <pre className="rr-out">{all ? view.content : cut.text}</pre>
      <div className="rr-ev-foot">
        {cut.truncated && (
          <button type="button" className="rr-link no-print" onClick={() => setAll((v) => !v)}>
            {all ? "Show excerpt" : `Show all ${cut.totalLines} lines`}
          </button>
        )}
        {view.sha256 && <code title="SHA-256 of the recorded evidence">SHA-256 {view.sha256.slice(0, 16)}…{view.verified === true ? " · verified" : view.verified === false ? " · not verified" : ""}</code>}
      </div>
    </figure>
  );
}

export function IssueReading({ group, refs, tz }: { group: IssueGroup; refs: Map<string, string>; tz: string }) {
  const f = group.lead;
  const many = group.findings.length > 1;
  const ref = refs.get(f.id) ?? "";
  const facts = issueFacts(group, tz);
  const narrative = findingNarrative(f);
  const shared = many ? sharedNarrativeKeys(group) : null;
  const rem = remediationView(f);
  const closure = closureView(f);

  return (
    <div className="rr-issue-body">
      {facts.length > 0 && (
        <dl className="rr-facts">
          {facts.map((x) => <div key={x.label} data-wide={x.label === "CVSS vector" || undefined}><dt>{x.label}</dt><dd>{x.value}</dd></div>)}
        </dl>
      )}

      {!narrative.sections.some((x) => x.key === "description") && (
        <section className="rr-sec">
          <h4>Description</h4>
          <p className="rr-placeholder">No description has been recorded for this finding.</p>
        </section>
      )}
      {narrative.sections.map((section) => (
        <section key={section.key} className="rr-sec">
          <h4>{section.title}</h4>
          {shared && !shared.has(section.key) && <p className="rr-muted rr-small">As recorded for {ref}; other instances record this differently.</p>}
          <ReadableBlock body={section.body} />
        </section>
      ))}

      {f.evidence.artifacts.length > 0 && (
        <section className="rr-sec">
          <h4>{many ? `Evidence (representative, from ${ref})` : "Evidence"}</h4>
          <EvidenceExcerpts evidence={f.evidence} prefix={ref} tz={tz} />
        </section>
      )}

      {(rem.text || rem.plans.length > 0 || rem.recommendations.length > 0) && (
        <section className="rr-sec rr-remediation">
          <h4>Remediation</h4>
          {rem.text && <div className="rr-prose"><p>{rem.text}</p></div>}
          {rem.plans.map((plan, i) => (
            <div key={i} className="rr-plan">
              {plan.summary && <p><b>Reviewed plan:</b> {plan.summary}{plan.effort ? ` (effort: ${plan.effort})` : ""}</p>}
              {plan.steps.length > 0 && <ol className="rr-list">{plan.steps.map((s, j) => <li key={j}>{s}</li>)}</ol>}
              {plan.verification.length > 0 && <><p className="rr-sub">Verify the fix</p><ul className="rr-list">{plan.verification.map((s, j) => <li key={j}>{s}</li>)}</ul></>}
              {plan.longTerm.length > 0 && <><p className="rr-sub">Longer term</p><ul className="rr-list">{plan.longTerm.map((s, j) => <li key={j}>{s}</li>)}</ul></>}
              {plan.compensating && <p><b>Compensating controls:</b> {plan.compensating}</p>}
            </div>
          ))}
          {rem.recommendations.length > 0 && <><p className="rr-sub">Recommendations</p><ul className="rr-list">{rem.recommendations.map((s, j) => <li key={j}>{s}</li>)}</ul></>}
        </section>
      )}

      {!rem.text && rem.plans.length === 0 && rem.recommendations.length === 0 && (
        <section className="rr-sec">
          <h4>Remediation</h4>
          <p className="rr-placeholder">No remediation guidance has been recorded for this finding.</p>
        </section>
      )}

      {!many && (closure.closed || closure.retest || closure.reopened > 0) && (
        <p className="rr-closure" data-closed={closure.closed}>
          <ShieldCheck size={14} aria-hidden="true" />
          <span>
            <b>{closure.disposition}</b>
            {closure.resolvedAt ? ` on ${formatDate(closure.resolvedAt, tz)}` : ""}
            {closure.method ? ` · ${closure.method}` : ""}
            {closure.retest ? ` · retest ${closure.retest.toLowerCase()}${closure.retestAt ? ` ${formatDate(closure.retestAt, tz)}` : ""}` : ""}
            {closure.reviewedBy ? ` · reviewed by ${closure.reviewedBy}` : ""}
            {closure.reopened ? ` · reopened ${closure.reopened}×` : ""}
          </span>
        </p>
      )}

      {narrative.missing.length > 0 && (
        <p className="rr-missing rr-operator-only">Missing from the record (operator note): {narrative.missing.map((m) => m.toLowerCase()).join(", ")}.</p>
      )}
    </div>
  );
}

// ─── Roadmap and closure ─────────────────────────────────────────────────────

const SLA_TONE: Record<string, string> = { breached: "risk", at_risk: "warn", due_soon: "warn", on_track: "ok" };

export function RemediationRoadmap({ report, tz, groups }: { report: ReportDocument; tz: string; groups: IssueGroup[] }) {
  const roadmap = remediationRoadmap(report);
  if (!roadmap.length) return <p className="rr-ok-note"><ShieldCheck size={14} />No findings are open, so no remediation is outstanding.</p>;
  const anchorOf = (title: string, severity: SeverityKey) => issueAnchor(groups.findIndex((g) => g.title === title && g.severity === severity));
  const anyOwner = roadmap.some((b) => b.items.some((i) => i.owner));
  return (
    <div className="rr-roadmap">
      <p className="rr-muted">Target windows come only from the current SLA policy recorded for each finding; where none is recorded, no target is shown.</p>
      {!anyOwner && <p className="rr-callout">No remediation owners are recorded yet. Assign one per issue so every fix has someone accountable for it.</p>}
      {roadmap.map((bucket) => (
        <section key={bucket.priority} className="rr-bucket" data-severity={bucket.severities[0]}>
          <header>
            <h3>{bucket.title}</h3>
            <span>{bucket.findings} open finding{bucket.findings === 1 ? "" : "s"}{bucket.items.length < bucket.findings ? ` in ${bucket.items.length} issue${bucket.items.length === 1 ? "" : "s"}` : ""}{bucket.target ? ` · fix ${bucket.target}` : " · no SLA window recorded"}</span>
          </header>
          <div className="rr-table-wrap">
            <table className="rr-table">
              <thead><tr><th scope="col">Ref</th><th scope="col">Finding</th><th scope="col">Assets</th>{anyOwner && <th scope="col">Owner</th>}<th scope="col">Fix by</th><th scope="col">SLA</th></tr></thead>
              <tbody>
                {bucket.items.map((item) => (
                  <tr key={item.ref + item.title}>
                    <td className="rr-ref">{item.ref}</td>
                    <td><a href={`#${anchorOf(item.title, item.severity)}`}>{item.title}</a></td>
                    <td>{item.asset ?? "—"}</td>
                    {anyOwner && <td>{item.owner ?? "—"}</td>}
                    <td>{formatDate(item.deadline, tz) ?? "—"}</td>
                    <td>{item.slaState ? <span className="rr-tag" data-tone={SLA_TONE[item.slaState] ?? "neutral"}>{slaLabel(item.slaState)}</span> : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      ))}
    </div>
  );
}

export function ClosureRegister({ groups, refs, tz }: { groups: IssueGroup[]; refs: Map<string, string>; tz: string }) {
  const anyHistory = groups.some((g) => g.findings.some((f) => !isOpenStatus(f.status) || f.closure.retest || f.closure.reopened_count > 0));
  if (!anyHistory) {
    const n = groups.reduce((a, g) => a + g.findings.length, 0);
    return (
      <p className="rr-ok-note rr-neutral">
        {n
          ? `No finding has been closed, retested or reopened yet. ${n === 1 ? "The finding remains" : `All ${n} findings remain`} open; the remediation roadmap shows what to fix first.`
          : "No findings are recorded."}
      </p>
    );
  }
  return (
    <div className="rr-table-wrap">
      <table className="rr-table cr-closure-register">
        <caption>Closure and retest status for every finding</caption>
        <thead>
          <tr><th scope="col">Ref</th><th scope="col">Finding</th><th scope="col">Severity</th><th scope="col">Disposition</th><th scope="col">Resolved</th><th scope="col">Retest</th><th scope="col">History</th></tr>
        </thead>
        <tbody>
          {groups.map((g, i) => {
            const views = g.findings.map(closureView);
            const single = g.findings.length === 1;
            const retest = g.findings[0]!.closure.retest;
            const passed = views.filter((v) => v.retest === "Passed").length;
            const failed = views.filter((v) => v.retest === "Failed").length;
            const resolved = views.map((v) => v.resolvedAt).filter((d): d is string => Boolean(d)).sort();
            return (
              <tr key={g.key}>
                <td className="rr-ref">{groupRef(g, refs)}</td>
                <th scope="row"><a href={single ? `#finding-${g.lead.id}` : `#${issueAnchor(i)}`}>{g.title}</a></th>
                <td><SeverityPill severity={g.severity} /></td>
                <td data-open={g.open > 0}>{single ? views[0]!.disposition : statusSummary(g.findings)}</td>
                <td>{g.open === 0 && resolved.length ? formatDate(resolved[resolved.length - 1], tz) : "—"}</td>
                <td>
                  {single
                    ? <>{views[0]!.retest ?? "Not retested"}<br /><span className="rr-muted rr-small">Before / after artifacts: {retest?.before_evidence.artifacts.length ?? 0} / {retest?.after_evidence.artifacts.length ?? 0}</span></>
                    : passed || failed ? `${passed} passed, ${failed} failed` : "Not retested"}
                </td>
                <td>Reopened: {views.reduce((a, v) => a + v.reopened, 0)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ─── Readiness appendix ──────────────────────────────────────────────────────

export function ReadinessAppendix({ report }: { report: ReportDocument }) {
  const gaps = gapInventory(report);
  return (
    <div className="rr-readiness" data-complete={report.readiness.complete}>
      <p className="rr-readiness-head">
        {report.readiness.complete ? <ShieldCheck size={15} /> : <ShieldAlert size={15} />}
        {report.readiness.complete
          ? "No configured completeness gaps were identified. This does not constitute approval for delivery."
          : "The live record contains gaps that require operator review before customer delivery. Each gap is listed once with the findings it affects."}
      </p>
      {gaps.reportLevel.length > 0 && (
        <>
          <h3 className="rr-h3">Report-level gaps ({gaps.reportLevel.length})</h3>
          <ul className="rr-gap-chips">
            {gaps.reportLevel.map((g) => <li key={g.code} title={g.code}>{g.label}</li>)}
          </ul>
        </>
      )}
      {gaps.findingLevel.length > 0 && (
        <>
          <h3 className="rr-h3">Finding-level gaps</h3>
          <div className="rr-table-wrap">
            <table className="rr-table">
              <thead><tr><th scope="col">Gap</th><th scope="col">Findings affected</th><th scope="col">References</th></tr></thead>
              <tbody>
                {gaps.findingLevel.map((g) => (
                  <tr key={g.code}>
                    <td>{g.label}<br /><code className="rr-code">{g.code}</code></td>
                    <td>{g.count}</td>
                    <td>{compactRefs(g.refs)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

// ─── Record disclosure ───────────────────────────────────────────────────────

/**
 * The complete canonical record behind a finding. Small reports render it up
 * front (so print and search see it); large ones render it on first open.
 */
export function RecordDisclosure({ finding, label, summary, eager, children }: {
  finding: ReportFinding;
  label: string;
  summary?: React.ReactNode;
  eager: boolean;
  children: () => React.ReactNode;
}) {
  const [opened, setOpened] = useState(false);
  return (
    <details
      className="rr-record"
      id={`finding-${finding.id}`}
      onToggle={(e) => { if ((e.currentTarget as HTMLDetailsElement).open) setOpened(true); }}
    >
      <summary>
        <ChevronRight size={14} className="rr-chev" aria-hidden="true" />
        {summary ?? <span>{label}</span>}
      </summary>
      {(eager || opened) && <div className="rr-record-body">{children()}</div>}
    </details>
  );
}
