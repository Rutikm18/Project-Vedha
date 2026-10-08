"use client";

import { useMemo } from "react";

import { EAGER_RECORD_LIMIT, IssueCard, ReportTimeZoneContext } from "./CanonicalReportDocument";
import { FindingsOverview, ReportCover } from "./ReportReadingView";
import { findingRefs, isIssued, issueGroups, usableTimeZone } from "../../lib/report/presentation";
import type { ReportDocument } from "../../lib/report/report-document";

/**
 * Technical Findings Report — for the engineers who fix things: the cover, a
 * findings index, then every issue with its evidence and remediation. Built
 * from the same pieces as the full report, so refs and wording match.
 */
export function TechnicalFindingsReport({ report }: { report: ReportDocument }) {
  const tz = usableTimeZone(report.document.display_timezone);
  const groups = useMemo(() => issueGroups(report.findings), [report.findings]);
  const refs = useMemo(() => findingRefs(report), [report]);
  const eager = report.findings.length <= EAGER_RECORD_LIMIT;

  return (
    <ReportTimeZoneContext.Provider value={tz}>
      <article className="report-document cr-report rr-report cr-technical" aria-label={`${report.engagement.name} technical findings report`}>
        <ReportCover report={report} tz={tz} issued={isIssued(report)} />
        <section className="cr-report-section rr-section" aria-labelledby="tech-index">
          <header className="cr-section-head"><h2 id="tech-index"><span className="rr-num">1</span>Findings index</h2><p>Most severe first. Each issue below carries its evidence and remediation.</p></header>
          <FindingsOverview groups={groups} refs={refs} total={report.findings.length} />
        </section>
        <section className="cr-report-section rr-section" aria-labelledby="tech-findings">
          <header className="cr-section-head"><h2 id="tech-findings"><span className="rr-num">2</span>Technical findings</h2><p>The complete canonical record of any finding is one click away.</p></header>
          {groups.length ? (
            <div className="rr-issues">
              {groups.map((group, index) => (
                <IssueCard key={group.key} group={group} index={index} refs={refs} tz={tz} eager={eager} />
              ))}
            </div>
          ) : <p className="cr-missing">No findings are recorded for this engagement.</p>}
        </section>
      </article>
    </ReportTimeZoneContext.Provider>
  );
}
