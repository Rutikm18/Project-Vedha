"use client";

import { FindingReport, ReportTimeZoneContext } from "./CanonicalReportDocument";
import { buildFindingsIndex } from "../../lib/report/findings-index";
import { SEVERITY, SEVERITY_ORDER } from "../../lib/severity";
import type { ReportDocument } from "../../lib/report/report-document";

function windowLabel(start?: string | null, end?: string | null): string {
  const day = (s?: string | null) => {
    if (!s) return null;
    const d = new Date(s);
    return Number.isNaN(d.getTime()) ? s : d.toISOString().slice(0, 10);
  };
  const a = day(start);
  const b = day(end);
  if (a && b) return `${a} → ${b}`;
  return a ?? b ?? "Not recorded";
}

/**
 * Standalone, audience-tuned Technical Findings Report: a cover, a scannable
 * findings index, then the elevated findings (reused from the canonical report).
 * Reuses the canonical finding renderer under its timezone provider so times
 * match the full report.
 */
export function TechnicalFindingsReport({ report }: { report: ReportDocument }) {
  const rows = buildFindingsIndex(report.findings);
  const counts = rows.reduce<Record<string, number>>((acc, r) => {
    acc[r.severity] = (acc[r.severity] ?? 0) + 1;
    return acc;
  }, {});
  const eng = report.engagement;
  const generated = report.document.generated_at
    ? report.document.generated_at.slice(0, 16).replace("T", " ")
    : "Not recorded";

  return (
    <ReportTimeZoneContext.Provider value={report.document.display_timezone}>
      <main className="cr-report cr-elevated cr-technical">
        <section className="cr-tech-cover">
          <div className="cr-tech-eyebrow">CONFIDENTIAL · TECHNICAL FINDINGS REPORT</div>
          <h1>{eng.name}</h1>
          <p className="cr-tech-sub">{eng.client ?? "Client not recorded"}</p>
          <ul className="cr-tech-counts">
            {SEVERITY_ORDER.map((s) =>
              counts[s] ? (
                <li key={s}><b style={{ color: SEVERITY[s].color }}>{counts[s]}</b> {SEVERITY[s].label}</li>
              ) : null,
            )}
          </ul>
          <dl className="cr-tech-meta">
            <div><dt>Assessor</dt><dd>{eng.assessor ?? "Not recorded"}</dd></div>
            <div><dt>Window</dt><dd>{windowLabel(eng.start_time, eng.end_time)}</dd></div>
            <div><dt>Findings</dt><dd>{report.findings.length}</dd></div>
            <div><dt>Generated</dt><dd>{generated} ({report.document.display_timezone})</dd></div>
          </dl>
        </section>

        <section className="cr-tech-index" aria-label="Findings index">
          <h2>Findings index</h2>
          {rows.length ? (
            <table className="cr-index-table">
              <thead>
                <tr><th>Ref</th><th>Finding</th><th>Severity</th><th>CVSS</th><th>EPSS</th><th>SLA</th><th>Status</th></tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.id}>
                    <td><a href={`#finding-${r.id}`}>{r.ref}</a></td>
                    <td className="cr-index-title"><a href={`#finding-${r.id}`}>{r.title}</a></td>
                    <td><span className="cr-index-sev" data-severity={r.severity.toLowerCase()}>{SEVERITY[r.severity].label}</span></td>
                    <td>{r.cvss}</td>
                    <td>{r.epss}</td>
                    <td data-tone={r.sla.tone}>{r.sla.label}</td>
                    <td>{r.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : <p className="cr-missing">No findings are recorded for this engagement.</p>}
        </section>

        <section className="cr-finding-list cr-tech-findings">
          {report.findings.map((finding, index) => (
            <FindingReport key={finding.id} finding={finding} ordinal={index + 1} />
          ))}
        </section>
      </main>
    </ReportTimeZoneContext.Provider>
  );
}
