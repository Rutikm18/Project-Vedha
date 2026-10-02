/**
 * findings-index.ts — build the scannable "findings index" rows for the
 * standalone Technical Findings Report. Order is preserved (so refs F001… line
 * up with the rendered findings); it re-presents existing fields only.
 */
import { toSeverity, type Severity } from "../severity";
import { epssPercent, formatSlaCountdown, type SlaCountdown } from "./risk-band";

export interface FindingIndexRow {
  ref: string;
  id: string;
  title: string;
  severity: Severity;
  cvss: string;
  epss: string;
  sla: SlaCountdown;
  status: string;
}

interface IndexFinding {
  id: string;
  title: string;
  severity: string;
  status: string;
  cvss_score?: number | string | null;
  epss_score?: number | string | null;
  current_sla?: { state?: string | null; hours_remaining?: number | null } | null;
}

function num(v: number | string | null | undefined): number | null {
  const n = typeof v === "string" ? Number(v) : v;
  return typeof n === "number" && Number.isFinite(n) ? n : null;
}

export function buildFindingsIndex(findings: IndexFinding[]): FindingIndexRow[] {
  return findings.map((f, i) => {
    const cvss = num(f.cvss_score);
    return {
      ref: `F${String(i + 1).padStart(3, "0")}`,
      id: f.id,
      title: f.title,
      severity: toSeverity(f.severity),
      cvss: cvss === null ? "—" : cvss.toFixed(1),
      epss: epssPercent(num(f.epss_score)) ?? "—",
      sla: formatSlaCountdown(f.current_sla),
      status: f.status,
    };
  });
}
