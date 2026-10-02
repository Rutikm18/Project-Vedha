import { decodeCvssVector } from "../../lib/report/cvss";
import { epssPercent, exploitFlag, formatSlaCountdown } from "../../lib/report/risk-band";

/** Structural subset of ReportFinding that the band reads. Scores may arrive as
 *  number or string in the canonical model, so they are coerced defensively. */
interface RiskBandFinding {
  cvss_score?: number | string | null;
  cvss_vector?: string | null;
  epss_score?: number | string | null;
  risk_score?: number | string | null;
  exploitable?: boolean | null;
  exploit_validated?: boolean | null;
  current_sla?: { state?: string | null; hours_remaining?: number | null } | null;
}

function num(v: number | string | null | undefined): number | null {
  const n = typeof v === "string" ? Number(v) : v;
  return typeof n === "number" && Number.isFinite(n) ? n : null;
}

/**
 * Compact triage band for a finding header. Surfaces signals already recorded on
 * the finding (CVSS, risk, EPSS, exploit, SLA, decoded vector) so an engineer can
 * triage at a glance. It invents nothing — absent signals are simply omitted.
 */
export function FindingRiskBand({ finding }: { finding: RiskBandFinding }) {
  const cvss = num(finding.cvss_score);
  const risk = num(finding.risk_score);
  const epss = epssPercent(num(finding.epss_score));
  const vector = decodeCvssVector(finding.cvss_vector);
  const exploit = exploitFlag(finding);
  const sla = formatSlaCountdown(finding.current_sla);

  return (
    <div className="cr-riskband" role="group" aria-label="Finding triage summary">
      {cvss !== null && <span className="cr-rb-item cr-rb-cvss"><b>CVSS</b>{cvss.toFixed(1)}</span>}
      {risk !== null && <span className="cr-rb-item"><b>Risk</b>{Math.round(risk)}</span>}
      {epss && <span className="cr-rb-item"><b>EPSS</b>{epss}</span>}
      {exploit && <span className="cr-rb-item cr-rb-exploit">{exploit}</span>}
      {sla.tone !== "none" && (
        <span className="cr-rb-item cr-rb-sla" data-tone={sla.tone}><b>SLA</b>{sla.label}</span>
      )}
      {vector.length > 0 && (
        <span className="cr-rb-vector">
          {vector.map((m) => (
            <span key={m.key} className="cr-rb-metric" title={`${m.label}: ${m.valueLabel}`}>{m.code}</span>
          ))}
        </span>
      )}
    </div>
  );
}
