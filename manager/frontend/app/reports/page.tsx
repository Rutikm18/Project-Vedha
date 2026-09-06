"use client";

import React, { useCallback, useMemo, useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import {
  Activity, AlertTriangle, ArrowDownRight, ArrowUpRight, BarChart3, CheckCircle2, ChevronDown,
  ChevronRight, Copy, FileSearch, FileText, Fingerprint, Flame,
  Globe, Lock, Minus, Printer, RefreshCw, Shield, ShieldAlert, ShieldCheck,
  Sparkles, Target, Terminal, Zap,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { DataState, EmptyState, SkeletonRows } from "../../components/states/DataState";
import { fetchJson, isUnauthorized } from "../../lib/fetcher";
import {
  SEV_COLOR, SEV_PALETTE, SEVERITY_ORDER, toSeverity, riskScoreColor,
  type Severity,
} from "../../lib/severity";
import {
  type ScoreDomain, type Confidence, type RemediationGroup,
  type Scorecard, type ReportFinding, type ReportDecision,
} from "../../lib/prompts/report";
import { type ReportResult } from "../../lib/ai-engine";
import { FindingsSection, EvidenceArtifact } from "../../components/report/FindingReport";
import { toRawFinding } from "../../lib/report/adapt";
import "../../styles/report-finding.css"; // after globals.css (imported in app/layout.tsx)

// ─── Types ────────────────────────────────────────────────────────────────────

type ReportTab = "executive" | "technical" | "evidence" | "cve" | "coverage";

interface Engagement {
  id: string; name: string; client: string; status: string;
  startDate: string; endDate: string; scopeCidrs: string[];
  assessor: string; description: string; assetCount: number;
  findingCount: number; findingsBySeverity: Record<Exclude<Severity, "INFO">, number>;
}

interface EvidenceItem { label: string; content: string; type?: string; }

interface Finding {
  id: string; title: string; severity: Severity; status: string;
  affectedHost: string; discoveredAt: string; description: string;
  technicalDetails: string; evidence: EvidenceItem[];
  impact: string; remediation: Array<string | { title?: string; description?: string; step?: string }>;
  mitre: Array<{ id: string; name: string }>; cwe?: Array<{ id: string; name: string }>;
  cve?: string[]; riskScore: number; cvss: string; cvssVector?: string;
  activelyExploited: boolean; detectionCoverage: string; reproductionSteps?: string;
}

interface FindingPage { items: Finding[]; total: number; page: number; pageSize: number; pages: number; }
interface FindingSummary { total: number; criticalOpen: number; validated: number; blind: number; averageRisk: number; }
interface ActivityItem { id: string; timestamp: string; actor: string; action: string; detail: string; }

// ─── Constants ────────────────────────────────────────────────────────────────

const TABS: Array<{ id: ReportTab; label: string; icon: React.ElementType }> = [
  { id: "executive",  label: "Executive",          icon: BarChart3 },
  { id: "technical",  label: "Technical Findings", icon: FileSearch },
  { id: "evidence",   label: "Evidence Vault",     icon: Fingerprint },
  { id: "cve",        label: "CVE Intelligence",   icon: Globe },
  { id: "coverage",   label: "MITRE Coverage",     icon: ShieldCheck },
];

// ─── Helpers ──────────────────────────────────────────────────────────────────

function fmtDate(v?: string) {
  if (!v) return "Not recorded";
  const d = new Date(v);
  return isNaN(d.getTime()) ? "Not recorded" : new Intl.DateTimeFormat("en", { dateStyle: "medium" }).format(d);
}
function fmtDatetime(v?: string) {
  if (!v) return "—";
  const d = new Date(v);
  return isNaN(d.getTime()) ? "—" : new Intl.DateTimeFormat("en", { dateStyle: "short", timeStyle: "short" }).format(d);
}
function remText(s: Finding["remediation"][number]) {
  return typeof s === "string" ? s : s.description || s.step || s.title || "";
}
function parseCvss(v: string): number | null {
  const m = v?.match(/(\d+\.\d+)/); return m ? parseFloat(m[1]) : null;
}
function cvssColor(n: number | null) {
  if (n === null) return SEV_PALETTE.SLATE;
  if (n >= 9) return SEV_PALETTE.RED;
  if (n >= 7) return SEV_PALETTE.ORANGE;
  if (n >= 4) return SEV_PALETTE.AMBER;
  return SEV_PALETTE.STONE;
}

// ─── Atoms ────────────────────────────────────────────────────────────────────

function SevBadge({ sev }: { sev: Severity }) {
  const c = SEV_COLOR[sev];
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", padding: "2px 8px",
      borderRadius: 4, border: `1px solid ${c}44`, background: `${c}16`,
      color: c, fontSize: 10, fontWeight: 800, fontFamily: "var(--font-mono)",
      letterSpacing: "0.06em",
    }}>{sev}</span>
  );
}

function StatusPill({ status }: { status: string }) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", padding: "2px 8px",
      borderRadius: 4, background: "var(--bg-surface)", border: "1px solid var(--border-subtle)",
      color: "var(--text-muted)", fontSize: 10, fontWeight: 700, letterSpacing: "0.04em",
    }}>{status.toUpperCase().replace(/_/g, " ")}</span>
  );
}

function CopyBtn({ text }: { text: string }) {
  const [done, setDone] = useState(false);
  const click = useCallback(() => {
    void navigator.clipboard.writeText(text).then(() => { setDone(true); setTimeout(() => setDone(false), 1400); });
  }, [text]);
  return (
    <button onClick={click} title="Copy" style={{
      display: "inline-flex", alignItems: "center", justifyContent: "center",
      width: 24, height: 24, borderRadius: 5, border: "1px solid var(--border-subtle)",
      background: "transparent", color: "var(--text-muted)", cursor: "pointer",
    }}>
      {done ? <CheckCircle2 size={11} style={{ color: "var(--nominal-color)" }} /> : <Copy size={11} />}
    </button>
  );
}

function Metric({ label, value, note, tone = "var(--accent)" }: {
  label: string; value: string | number; note: string; tone?: string;
}) {
  return (
    <div className="rpt-metric">
      <small>{label}</small>
      <strong style={{ color: tone }}>{value}</strong>
      <span>{note}</span>
    </div>
  );
}

// ─── Severity strip ───────────────────────────────────────────────────────────

function SevStrip({ eng }: { eng: Engagement }) {
  const rows = (["CRITICAL", "HIGH", "MEDIUM", "LOW"] as const).map(s => ({ s, n: eng.findingsBySeverity[s] ?? 0 }));
  const total = Math.max(1, rows.reduce((a, r) => a + r.n, 0));
  return (
    <div>
      <div style={{ display: "flex", height: 10, borderRadius: 99, overflow: "hidden", background: "var(--bg-hover)", gap: 2 }}>
        {rows.filter(r => r.n > 0).map(r => (
          <span key={r.s} title={`${r.s}: ${r.n}`} style={{ flex: `${(r.n / total) * 100}`, background: SEV_COLOR[r.s] }} />
        ))}
      </div>
      <div style={{ display: "flex", gap: 20, marginTop: 10, flexWrap: "wrap" }}>
        {rows.map(r => (
          <span key={r.s} style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 11, color: "var(--text-secondary)" }}>
            <i style={{ width: 7, height: 7, borderRadius: "50%", background: SEV_COLOR[r.s], display: "inline-block" }} />
            {r.s} <strong style={{ color: "var(--text-primary)" }}>{r.n}</strong>
          </span>
        ))}
      </div>
    </div>
  );
}


// ─── Evidence block ───────────────────────────────────────────────────────────

function EvidBlock({ item }: { item: EvidenceItem }) {
  const [open, setOpen] = useState(false);
  const long = item.content.length > 300;
  const shown = open || !long ? item.content : item.content.slice(0, 300) + "\n…";
  return (
    <div style={{ border: "1px solid #1E293B", borderRadius: 7, overflow: "hidden" }}>
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "7px 12px", background: "#0F172A", borderBottom: "1px solid #1E293B",
      }}>
        <span style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11, fontWeight: 600, color: "#64748B", fontFamily: "var(--font-mono)" }}>
          <Terminal size={12} style={{ color: "#475569" }} />
          {item.label}
          {item.type && (
            <span style={{ fontSize: 9, fontWeight: 700, padding: "1px 5px", borderRadius: 3, background: "#1E293B", color: "#64748B" }}>{item.type}</span>
          )}
        </span>
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <CopyBtn text={item.content} />
          {long && (
            <button onClick={() => setOpen(!open)} style={{
              fontSize: 10, fontWeight: 700, padding: "2px 7px", borderRadius: 4,
              border: "1px solid #1E293B", background: "transparent", color: "#64748B", cursor: "pointer",
            }}>
              {open ? "Collapse" : "Expand"}
            </button>
          )}
        </div>
      </div>
      <pre style={{
        margin: 0, padding: "12px 14px", background: "#0B1120",
        fontFamily: "var(--font-mono)", fontSize: 11.5, lineHeight: 1.7,
        color: "#CBD5E1", overflowX: "auto", whiteSpace: "pre-wrap",
        wordBreak: "break-all", maxHeight: open ? "none" : 280, overflowY: open ? "visible" : "auto",
      }}>{shown}</pre>
    </div>
  );
}

// ─── Finding card ─────────────────────────────────────────────────────────────


// ─── AI report (deterministic scorecard · injection-fenced) ───────────────────

const DOMAIN_LABEL: Record<ScoreDomain, string> = {
  network: "Network",
  authentication: "Authentication",
  configuration: "Configuration",
  patch_management: "Patch mgmt",
  web_application: "Web app",
};

// Overall / domain scores are an open-risk index: 0–100, higher = worse.
function scoreColor(n: number): string {
  if (n >= 75) return SEV_PALETTE.RED;
  if (n >= 50) return SEV_PALETTE.ORANGE;
  if (n >= 25) return SEV_PALETTE.AMBER;
  return SEV_PALETTE.GREEN;
}

const CONF_STYLE: Record<Confidence, { color: string; label: string }> = {
  confirmed: { color: SEV_PALETTE.GREEN, label: "Confirmed" },
  likely:    { color: SEV_PALETTE.AMBER, label: "Likely" },
  potential: { color: SEV_PALETTE.SLATE, label: "Potential" },
};

const WINDOW_STYLE: Record<RemediationGroup["window"], { color: string; label: string }> = {
  immediate: { color: SEV_PALETTE.RED,    label: "Immediate" },
  "30_days": { color: SEV_PALETTE.ORANGE, label: "Within 30 days" },
  "90_days": { color: SEV_PALETTE.SLATE,  label: "Within 90 days" },
};

function EffortDot({ label, level }: { label: string; level: string }) {
  const col = level === "high" ? SEV_PALETTE.RED : level === "medium" ? SEV_PALETTE.AMBER : SEV_PALETTE.GREEN;
  return (
    <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>
      {label} <strong style={{ color: col, textTransform: "capitalize" }}>{level}</strong>
    </span>
  );
}

function ScorecardCard({ sc }: { sc: Scorecard }) {
  const d = sc.delta;
  const DeltaIcon = d.direction === "improved" ? ArrowDownRight : d.direction === "worsened" ? ArrowUpRight : Minus;
  const deltaColor = d.direction === "improved" ? SEV_PALETTE.GREEN : d.direction === "worsened" ? SEV_PALETTE.RED : "var(--text-muted)";
  return (
    <div className="rpt-section" style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 20, alignItems: "center" }}>
      {/* Overall */}
      <div style={{ textAlign: "center", minWidth: 120 }}>
        <div style={{ fontSize: 9, fontWeight: 800, color: "var(--text-muted)", letterSpacing: "0.1em", fontFamily: "var(--font-mono)" }}>OPEN RISK</div>
        <div style={{ fontSize: 46, fontWeight: 800, lineHeight: 1.05, color: scoreColor(sc.overall), fontFamily: "var(--font-mono)" }}>{sc.overall}</div>
        <div style={{ fontSize: 10, color: "var(--text-muted)" }}>of 100 · lower is better</div>
        {d.overall !== null && (
          <div style={{ display: "inline-flex", alignItems: "center", gap: 3, marginTop: 4, fontSize: 11, fontWeight: 700, color: deltaColor }}>
            <DeltaIcon size={12} /> {d.overall > 0 ? `+${d.overall}` : d.overall} vs. previous
          </div>
        )}
      </div>
      <div>
        {/* Domain split */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(96px, 1fr))", gap: 8, marginBottom: 12 }}>
          {(Object.keys(DOMAIN_LABEL) as ScoreDomain[]).map(key => {
            const dm = sc.domains[key];
            return (
              <div key={key} style={{ padding: "8px 10px", borderRadius: 7, border: "1px solid var(--border-subtle)", background: "var(--bg-panel)" }}>
                <div style={{ fontSize: 9.5, fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.04em" }}>{DOMAIN_LABEL[key]}</div>
                <div style={{ display: "flex", alignItems: "baseline", gap: 5, marginTop: 2 }}>
                  <span style={{ fontSize: 18, fontWeight: 800, fontFamily: "var(--font-mono)", color: scoreColor(dm.score) }}>{dm.score}</span>
                  <span style={{ fontSize: 10, color: "var(--text-muted)" }}>{dm.open} open</span>
                </div>
              </div>
            );
          })}
        </div>
        {/* Exploitability */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {([
            ["Open", sc.exploitability.open, "var(--text-secondary)"],
            ["On KEV", sc.exploitability.kev, SEV_PALETTE.RED],
            ["Exploit-validated", sc.exploitability.validated, SEV_PALETTE.ORANGE],
            ["EPSS ≥ 0.5", sc.exploitability.epssHigh, SEV_PALETTE.AMBER],
          ] as const).map(([label, n, col]) => (
            <span key={label} style={{ display: "inline-flex", alignItems: "center", gap: 5, fontSize: 11, padding: "3px 9px", borderRadius: 20, border: "1px solid var(--border-subtle)", background: "var(--bg-surface)" }}>
              <strong style={{ color: col, fontFamily: "var(--font-mono)" }}>{n}</strong>
              <span style={{ color: "var(--text-muted)" }}>{label}</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

// Signal chip — a single element of the severity-justification strip. "hot"
// signals (KEV, high EPSS, internet exposure) are the ones that turn a score
// into urgency, so they read in critical colour.
function Signal({ label, value, hot }: { label: string; value?: React.ReactNode; hot?: boolean }) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 5, padding: "3px 9px", borderRadius: 4,
      fontSize: 10.5, whiteSpace: "nowrap",
      color: hot ? SEV_PALETTE.RED : "var(--text-secondary)",
      background: hot ? `${SEV_PALETTE.RED}14` : "var(--bg-hover)",
      border: `1px solid ${hot ? `${SEV_PALETTE.RED}44` : "var(--border-subtle)"}`,
    }}>
      {label}{value != null && <b style={{ fontFamily: "var(--font-mono)", color: hot ? SEV_PALETTE.RED : "var(--text-primary)" }}>{value}</b>}
    </span>
  );
}

// Severity justification — "critical" is an assertion until the reader sees the
// vector and exploit signals that produced it. All values are scanner facts.
function RationaleStrip({ f }: { f: ReportFinding }) {
  const signals: React.ReactNode[] = [];
  if (f.cvss != null) signals.push(<Signal key="cvss" label="CVSS " value={f.cvss.toFixed(1)} />);
  if (f.cvss_vector) signals.push(<Signal key="vec" label={f.cvss_vector} />);
  if (f.epss != null) signals.push(<Signal key="epss" label="EPSS " value={f.epss.toFixed(2)} hot={f.epss >= 0.5} />);
  if (f.kev) signals.push(<Signal key="kev" label="CISA KEV" hot />);
  if (f.exploit_validated) signals.push(<Signal key="val" label="Validated in test" />);
  if (f.internet_reachable) signals.push(<Signal key="net" label="Internet-reachable" hot />);
  if (signals.length === 0) return null;
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 7, marginTop: 10, paddingTop: 10, borderTop: "1px dashed var(--border-subtle)" }}>
      {signals}
    </div>
  );
}

function ReportFindingCard({ f }: { f: ReportFinding }) {
  const sev = toSeverity(f.severity);
  const sevColor = SEV_COLOR[sev];
  const conf = CONF_STYLE[f.confidence] ?? CONF_STYLE.potential;
  return (
    <div style={{ border: "1px solid var(--border-subtle)", borderLeft: `3px solid ${sevColor}`, borderRadius: 8, background: "var(--bg-panel)", padding: "14px 16px" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 8 }}>
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, fontWeight: 800, color: "var(--text-faint)" }}>{f.ref}</span>
        <SevBadge sev={sev} />
        <span style={{ fontSize: 9.5, fontWeight: 800, letterSpacing: "0.04em", padding: "2px 7px", borderRadius: 4, color: conf.color, background: `${conf.color}16`, border: `1px solid ${conf.color}33` }}>{conf.label.toUpperCase()}</span>
        <strong style={{ fontSize: 13.5, color: "var(--text-primary)", lineHeight: 1.35 }}>{f.title}</strong>
      </div>
      {f.affected_assets.length > 0 && (
        <div style={{ fontSize: 11, color: "var(--text-muted)", fontFamily: "var(--font-mono)", marginBottom: 4 }}>{f.affected_assets.join(" · ")}</div>
      )}
      <RationaleStrip f={f} />
      {f.severity_flag && (
        <div style={{ display: "flex", gap: 7, alignItems: "flex-start", marginTop: 10, padding: "8px 10px", borderRadius: 6, background: "var(--sev-medium-bg)", border: "1px solid var(--sev-medium-color)" }}>
          <AlertTriangle size={12} style={{ color: "var(--sev-medium-color)", flexShrink: 0, marginTop: 1 }} />
          <span style={{ fontSize: 11, color: "var(--text-primary)" }}>{f.severity_flag}</span>
        </div>
      )}
      <div style={{ marginTop: 12 }}>
        {[
          ["Business impact", f.business_impact],
          ["Why this severity", f.severity_rationale],
          ["Technical detail", f.technical_detail],
          ["Evidence", f.evidence_summary],
          ["Remediation", f.remediation_detail],
          ["Verification", f.verification],
          ["How this was established", f.validation_method],
        ].filter(([, v]) => v).map(([label, v]) => (
          <div key={label} style={{ marginBottom: 8 }}>
            <div className="fc-section-label">{label}</div>
            <p style={{ margin: "3px 0 0", fontSize: 12.5, color: "var(--text-secondary)", lineHeight: 1.6 }}>{v}</p>
          </div>
        ))}
      </div>
      {(f.compliance_refs.length > 0 || (f.references?.length ?? 0) > 0) && (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 6 }}>
          {f.compliance_refs.map(r => <span key={r} className="rpt-chip">{r}</span>)}
          {f.references?.map(r => (
            /^CVE-/i.test(r)
              ? <a key={r} href={`https://nvd.nist.gov/vuln/detail/${r}`} target="_blank" rel="noopener noreferrer" className="rpt-chip rpt-chip--cve">{r}</a>
              : <span key={r} className="rpt-chip">{r}</span>
          ))}
        </div>
      )}
    </div>
  );
}

// ── Exposure matrix: severity (how bad) × exploitability (how likely). The
// three top-left cells are where real exposure sits; all counts are derived
// from finding signals, not generated. ────────────────────────────────────────
const MATRIX_ROWS: Severity[] = ["CRITICAL", "HIGH", "MEDIUM", "LOW"];
const MATRIX_COLS = ["Weaponised", "Likely", "Theoretical"] as const;
const MATRIX_COL_AXIS = ["KEV or validated", "EPSS ≥ 0.50", "No known exploit"] as const;
// heat[rowIndex][colIndex]; higher = more worrying. Overridden to 0 when empty.
const MATRIX_HEAT = [
  [3, 2, 1], // critical
  [3, 2, 1], // high
  [2, 1, 1], // medium
  [1, 1, 0], // low
];
const HEAT_STYLE: Record<number, { bg: string; border: string; count: string }> = {
  0: { bg: "var(--bg-surface)", border: "var(--border-subtle)", count: "var(--text-muted)" },
  1: { bg: `${SEV_PALETTE.AMBER}12`, border: `${SEV_PALETTE.AMBER}38`, count: "var(--text-primary)" },
  2: { bg: `${SEV_PALETTE.ORANGE}18`, border: `${SEV_PALETTE.ORANGE}55`, count: SEV_PALETTE.ORANGE },
  3: { bg: `${SEV_PALETTE.RED}22`, border: `${SEV_PALETTE.RED}66`, count: SEV_PALETTE.RED },
};

function exploitCol(f: ReportFinding): 0 | 1 | 2 {
  if (f.kev || f.exploit_validated) return 0;
  if ((f.epss ?? 0) >= 0.5) return 1;
  return 2;
}

function ExposureMatrix({ findings }: { findings: ReportFinding[] }) {
  const grid = MATRIX_ROWS.map(() => [0, 0, 0]);
  for (const f of findings) {
    const r = MATRIX_ROWS.indexOf(toSeverity(f.severity));
    if (r >= 0) grid[r][exploitCol(f)]++;
  }
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ borderCollapse: "separate", borderSpacing: 3, width: "auto" }}>
        <thead>
          <tr>
            <td />
            {MATRIX_COLS.map((c, i) => (
              <th key={c} style={{ fontSize: 10.5, fontWeight: 700, color: "var(--text-muted)", padding: "4px 8px", textAlign: "center" }}>
                {c}<br /><span style={{ fontSize: 9, textTransform: "uppercase", letterSpacing: "0.04em" }}>{MATRIX_COL_AXIS[i]}</span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {MATRIX_ROWS.map((sev, r) => (
            <tr key={sev}>
              <th scope="row" style={{ textAlign: "right", paddingRight: 10 }}><SevBadge sev={sev} /></th>
              {grid[r].map((n, c) => {
                const heat = n === 0 ? 0 : MATRIX_HEAT[r][c];
                const s = HEAT_STYLE[heat];
                return (
                  <td key={c} style={{ width: 92, height: 52, textAlign: "center", verticalAlign: "middle", borderRadius: 5, background: s.bg, border: `1px solid ${s.border}` }}>
                    <span style={{ fontFamily: "var(--font-display)", fontSize: 19, fontWeight: 700, color: s.count }}>{n}</span>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ── Decision box: board-level calls, three horizons, owner slots. ─────────────
const HORIZON_STYLE: Record<string, { color: string; label: string }> = {
  this_week:    { color: SEV_PALETTE.RED,    label: "Decide this week" },
  this_month:   { color: SEV_PALETTE.ORANGE, label: "Decide this month" },
  this_quarter: { color: "var(--border-default)", label: "Decide this quarter" },
};

function DecisionBox({ decisions }: { decisions: ReportDecision[] }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 10, margin: "14px 0" }}>
      {decisions.map((d, i) => {
        const h = HORIZON_STYLE[d.horizon] ?? HORIZON_STYLE.this_quarter;
        return (
          <div key={i} style={{ background: "var(--bg-surface)", border: "1px solid var(--border-subtle)", borderTop: `2px solid ${h.color}`, borderRadius: 8, padding: "14px 16px" }}>
            <div style={{ fontSize: 10, color: "var(--text-muted)", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.05em" }}>{h.label}</div>
            <div style={{ fontFamily: "var(--font-display)", fontSize: 13.5, fontWeight: 700, color: "var(--text-primary)", lineHeight: 1.35, marginBottom: 6 }}>{d.ask}</div>
            <div style={{ fontSize: 12, color: "var(--text-secondary)", lineHeight: 1.55 }}>{d.rationale}</div>
            <div style={{ display: "flex", gap: 6, alignItems: "center", marginTop: 10, flexWrap: "wrap" }}>
              {d.fix_ids?.map(fx => <span key={fx} className="rpt-chip" style={{ fontSize: 9.5 }}>{fx}</span>)}
              <span style={{ marginLeft: "auto", padding: "2px 10px", border: "1px dashed var(--border-default)", borderRadius: 4, fontSize: 10, color: "var(--text-muted)" }}>Owner: ______</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function AiReportPanel({ eng, findings }: { eng: Engagement; findings: Finding[] }) {
  const [report, setReport] = useState<ReportResult | null>(null);
  const genMut = useMutation({
    mutationFn: () => fetchJson<ReportResult>("/api/reports/generate", {
      method: "POST",
      body: JSON.stringify({
        engagement: { name: eng.name, client: eng.client, scopeCidrs: eng.scopeCidrs },
        findings,
      }),
    }),
    onSuccess: setReport,
  });
  const err = genMut.error instanceof Error ? genMut.error.message : genMut.error ? String(genMut.error) : null;

  return (
    <div style={{
      border: "1px solid var(--border-default)", borderRadius: 10,
      background: "color-mix(in srgb, var(--accent) 3%, var(--bg-panel))",
      padding: "14px 16px", marginBottom: 18,
    }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
          <Sparkles size={14} style={{ color: "var(--accent)" }} />
          <span style={{ fontSize: 13, fontWeight: 700 }}>AI Report Generation</span>
          <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>Claude Sonnet 4.6 · deterministic scorecard · injection-fenced</span>
        </div>
        <button className="btn btn-primary no-print" style={{ fontSize: 11, padding: "5px 12px", display: "flex", alignItems: "center", gap: 5 }}
          onClick={() => genMut.mutate()} disabled={genMut.isPending || findings.length === 0}>
          {genMut.isPending ? <RefreshCw size={11} className="spin" /> : <Zap size={11} />}
          {report ? "Regenerate" : "Generate report"}
        </button>
      </div>

      {genMut.isPending && (
        <p style={{ marginTop: 10, fontSize: 11.5, color: "var(--text-secondary)" }}>
          Composing a client-ready draft from {findings.length} finding{findings.length !== 1 ? "s" : ""} — scorecard is computed locally; the narrative is written by the model.
        </p>
      )}
      {err && !genMut.isPending && (
        <div style={{ marginTop: 10, display: "flex", gap: 8, alignItems: "flex-start", padding: "9px 11px", borderRadius: 7, background: "var(--sev-critical-bg)", border: "1px solid var(--sev-critical-color)" }}>
          <AlertTriangle size={14} style={{ color: "var(--sev-critical-color)", flexShrink: 0, marginTop: 1 }} />
          <span style={{ fontSize: 11.5, color: "var(--text-primary)" }}>{err}</span>
        </div>
      )}

      {report && (
        <div style={{ marginTop: 14 }}>
          {/* Verdict */}
          <div style={{ display: "flex", gap: 10, alignItems: "flex-start", marginBottom: 14 }}>
            <Target size={16} style={{ color: "var(--accent)", flexShrink: 0, marginTop: 3 }} />
            <h3 style={{ margin: 0, fontSize: 17, fontWeight: 750, color: "var(--text-primary)", lineHeight: 1.4 }}>{report.verdict}</h3>
          </div>

          {/* Board decisions — three horizons, owner slots */}
          {(report.decisions?.length ?? 0) > 0 && <DecisionBox decisions={report.decisions!} />}

          <ScorecardCard sc={report.scorecard} />

          {/* Exposure matrix — severity × exploitability */}
          <div className="rpt-section">
            <div className="rpt-section-head" style={{ marginBottom: 6 }}><small>EXPOSURE MATRIX</small><h3>How bad × how likely</h3></div>
            <p style={{ fontSize: 11.5, color: "var(--text-muted)", margin: "0 0 12px", maxWidth: 620, lineHeight: 1.5 }}>
              Severity is how bad a finding would be if used; exploitability is how likely it is to be used. The shaded top-left cells are where the real exposure sits.
            </p>
            <ExposureMatrix findings={report.findings} />
          </div>

          {/* Executive summary */}
          <div className="rpt-section">
            <div className="rpt-section-head"><small>EXECUTIVE SUMMARY</small><h3>Business risk position</h3></div>
            <div className="fc-prose">
              {report.executive_summary.split("\n\n").map((p, i) => <p key={i}>{p}</p>)}
            </div>
          </div>

          {/* Attack narrative */}
          {report.attack_narrative && (
            <div className="rpt-section">
              <div className="rpt-section-head"><small>ATTACK NARRATIVE</small><h3>How findings chain together</h3></div>
              <div className="fc-prose">
                {report.attack_narrative.split("\n\n").map((p, i) => <p key={i}>{p}</p>)}
              </div>
            </div>
          )}

          {/* Findings register — full records for the worst N, the rest tabulated */}
          {(() => {
            const nDetailed = report.findings_detailed ?? report.findings.length;
            const detailed = report.findings.slice(0, nDetailed);
            const rest = report.findings.slice(nDetailed);
            return (
              <div className="rpt-section">
                <div className="rpt-section-head" style={{ marginBottom: 0 }}><small>FINDINGS REGISTER</small><h3>{report.findings.length} finding{report.findings.length !== 1 ? "s" : ""}</h3><span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-muted)" }}>{detailed.length} full · {rest.length} tabulated</span></div>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {detailed.map(f => <ReportFindingCard key={f.ref} f={f} />)}
                </div>
                {rest.length > 0 && (
                  <div className="report-table-wrap" style={{ marginTop: 12 }}>
                    <table className="report-table">
                      <caption style={{ textAlign: "left", fontSize: 11, color: "var(--text-muted)", paddingBottom: 8 }}>Remaining open findings.</caption>
                      <thead><tr><th>Ref</th><th>Sev</th><th>Finding</th><th>Confidence</th><th className="num">Assets</th></tr></thead>
                      <tbody>
                        {rest.map(f => (
                          <tr key={f.ref}>
                            <td><span style={{ fontFamily: "var(--font-mono)", fontSize: 11, fontWeight: 700, color: "var(--text-secondary)" }}>{f.ref}</span></td>
                            <td><SevBadge sev={toSeverity(f.severity)} /></td>
                            <td><strong>{f.title}</strong></td>
                            <td>{(CONF_STYLE[f.confidence] ?? CONF_STYLE.potential).label}</td>
                            <td className="num">{f.affected_assets.length}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            );
          })()}

          {/* Remediation plan (fix-grouped) */}
          <div className="rpt-section">
            <div className="rpt-section-head" style={{ marginBottom: 0 }}><small>REMEDIATION PLAN</small><h3>Grouped by fix · {report.remediation_plan.length} unit{report.remediation_plan.length !== 1 ? "s" : ""} of work</h3></div>
            {report.immediate_window_empty_reason && (
              <p style={{ fontSize: 11.5, color: "var(--text-muted)", margin: "6px 0 0", lineHeight: 1.5 }}>
                <strong style={{ color: "var(--text-secondary)" }}>Immediate window empty:</strong> {report.immediate_window_empty_reason}
              </p>
            )}
            <div style={{ display: "flex", flexDirection: "column", gap: 8, marginTop: 10 }}>
              {report.remediation_plan.map(g => {
                const w = WINDOW_STYLE[g.window] ?? WINDOW_STYLE["90_days"];
                return (
                  <div key={g.fix_id} style={{ border: "1px solid var(--border-subtle)", borderRadius: 8, background: "var(--bg-panel)", padding: "12px 14px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 6 }}>
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, fontWeight: 800, color: "var(--text-faint)" }}>{g.fix_id}</span>
                      <span style={{ fontSize: 9.5, fontWeight: 800, letterSpacing: "0.04em", padding: "2px 7px", borderRadius: 4, color: w.color, background: `${w.color}16`, border: `1px solid ${w.color}33` }}>{w.label.toUpperCase()}</span>
                      <strong style={{ fontSize: 13, color: "var(--text-primary)" }}>{g.title}</strong>
                    </div>
                    <p style={{ margin: "0 0 8px", fontSize: 12.5, color: "var(--text-secondary)", lineHeight: 1.6 }}>{g.description}</p>
                    <div style={{ display: "flex", gap: 14, flexWrap: "wrap", alignItems: "center", marginBottom: 6 }}>
                      <EffortDot label="Effort" level={g.effort} />
                      <EffortDot label="Change risk" level={g.change_risk} />
                      <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>Assets <strong style={{ color: "var(--text-primary)", fontFamily: "var(--font-mono)" }}>{g.asset_count}</strong></span>
                      {g.resolves.length > 0 && (
                        <span style={{ display: "flex", gap: 4, flexWrap: "wrap", alignItems: "center" }}>
                          <span style={{ fontSize: 10.5, color: "var(--text-muted)" }}>Resolves</span>
                          {g.resolves.map(r => <span key={r} className="rpt-chip" style={{ fontSize: 9.5 }}>{r}</span>)}
                        </span>
                      )}
                    </div>
                    {g.verification && (
                      <div>
                        <div className="fc-section-label"><CheckCircle2 size={11} /> Verification</div>
                        <p style={{ margin: "3px 0 0", fontSize: 12, color: "var(--text-secondary)", lineHeight: 1.55 }}>{g.verification}</p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Controls observed + limitations */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 12 }}>
            <div className="rpt-section" style={{ marginBottom: 0 }}>
              <div className="rpt-section-head" style={{ marginBottom: 8 }}><small>WHAT HELD</small><h3><ShieldCheck size={13} style={{ color: SEV_PALETTE.GREEN }} /> Controls observed</h3></div>
              <ul style={{ margin: 0, paddingLeft: 18, display: "grid", gap: 6 }}>
                {report.controls_observed.map((c, i) => <li key={i} style={{ fontSize: 12, color: "var(--text-secondary)", lineHeight: 1.55 }}>{c}</li>)}
              </ul>
            </div>
            <div className="rpt-section" style={{ marginBottom: 0 }}>
              <div className="rpt-section-head" style={{ marginBottom: 8 }}><small>SCOPE BOUNDARY</small><h3><Lock size={13} style={{ color: "var(--text-muted)" }} /> Scope &amp; limitations</h3></div>
              {report.method && (
                <p style={{ fontSize: 12, color: "var(--text-secondary)", lineHeight: 1.55, margin: "0 0 10px" }}>{report.method}</p>
              )}
              <ul style={{ margin: 0, paddingLeft: 18, display: "grid", gap: 6 }}>
                {report.limitations.map((l, i) => <li key={i} style={{ fontSize: 12, color: "var(--text-secondary)", lineHeight: 1.55 }}>{l}</li>)}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Tab: Executive ───────────────────────────────────────────────────────────

function ExecTab({ eng, findings, summary }: { eng: Engagement; findings: Finding[]; summary: FindingSummary }) {
  const crit = eng.findingsBySeverity.CRITICAL ?? 0;
  const high = eng.findingsBySeverity.HIGH ?? 0;
  const posture = crit > 0 ? "Critical risk — immediate action required"
    : high > 0 ? "Elevated risk — remediation required"
    : summary.total > 0 ? "Risk managed — address findings"
    : "No findings recorded";

  const actions = [
    crit > 0 && `Assign owners and remediation deadlines to ${crit} critical finding${crit > 1 ? "s" : ""}.`,
    summary.validated > 0 && `Prioritise ${summary.validated} exploit-validated finding${summary.validated > 1 ? "s" : ""} — confirmed attack paths exist.`,
    summary.blind > 0 && `Address ${summary.blind} detection blind spot${summary.blind > 1 ? "s" : ""} — no SOC telemetry exists for these assets.`,
    summary.total > 0 && "Retest all remediated findings and retain verification evidence before closing.",
    !summary.total && "Commission an authorised assessment before drawing any security conclusion.",
  ].filter(Boolean) as string[];

  return (
    <>
      <AiReportPanel eng={eng} findings={findings} />

      {/* Risk position hero */}
      <div style={{
        display: "flex", justifyContent: "space-between", alignItems: "flex-start",
        gap: 20, padding: 20, borderRadius: 10, marginBottom: 16,
        background: "linear-gradient(135deg, var(--bg-surface), var(--bg-panel))",
        border: "1px solid var(--border-subtle)",
      }}>
        <div>
          <div style={{ fontSize: 9, fontWeight: 800, color: "var(--text-muted)", letterSpacing: "0.12em", fontFamily: "var(--font-mono)", textTransform: "uppercase" }}>RISK POSITION</div>
          <h2 style={{ margin: "6px 0 8px", fontSize: 22, fontWeight: 750, color: "var(--text-primary)" }}>{posture}</h2>
          <p style={{ margin: 0, fontSize: 12, color: "var(--text-secondary)", maxWidth: 640, lineHeight: 1.6 }}>
            All metrics are derived from Vedha scanner evidence for <strong>{eng.name}</strong>. Untested assets and controls are outside this report's scope.
          </p>
        </div>
        <ShieldAlert size={28} style={{ color: "var(--sev-critical-color)", flexShrink: 0 }} />
      </div>

      {/* Metrics */}
      <div className="rpt-metrics">
        <Metric label="Total findings" value={summary.total} note="All severities" tone={SEV_PALETTE.RED} />
        <Metric label="Critical open" value={summary.criticalOpen} note="Open / confirmed" tone={SEV_PALETTE.RED} />
        <Metric label="Exploit validated" value={summary.validated} note="Evidence-backed" tone={SEV_PALETTE.ORANGE} />
        <Metric label="Avg risk score" value={summary.averageRisk} note="0–1000 composite" tone={SEV_PALETTE.VIOLET} />
      </div>

      {/* Severity distribution */}
      <div className="rpt-section">
        <div className="rpt-section-head"><small>RISK DISTRIBUTION</small><h3>Severity profile</h3></div>
        <SevStrip eng={eng} />
      </div>

      {/* Priority actions */}
      <div className="rpt-section">
        <div className="rpt-section-head"><small>DECISION QUEUE</small><h3>Priority management actions</h3></div>
        <ol style={{ margin: 0, paddingLeft: 22, display: "grid", gap: 8 }}>
          {actions.map(a => (
            <li key={a} style={{ fontSize: 12.5, color: "var(--text-primary)", lineHeight: 1.6 }}>{a}</li>
          ))}
        </ol>
      </div>

      {/* Top findings table */}
      <div className="rpt-section">
        <div className="rpt-section-head" style={{ marginBottom: 0 }}>
          <small>HIGHEST RISK</small><h3>Top findings</h3>
          <span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-muted)" }}>Top {Math.min(10, findings.length)} of {summary.total}</span>
        </div>
        {findings.length === 0 && <p className="report-missing">No findings recorded.</p>}
        <div className="report-table-wrap">
          <table className="report-table">
            <thead><tr><th>Sev</th><th>Finding</th><th>Asset</th><th>CVSS</th><th>Status</th></tr></thead>
            <tbody>
              {findings.slice(0, 10).map(f => {
                const sc = parseCvss(f.cvss);
                const sev = toSeverity(f.severity);
                return (
                  <tr key={f.id}>
                    <td><SevBadge sev={sev} /></td>
                    <td><strong>{f.title}</strong><small>{f.id}</small></td>
                    <td>{f.affectedHost}</td>
                    <td>{sc !== null ? <span style={{ color: cvssColor(sc), fontWeight: 700 }}>{sc.toFixed(1)}</span> : "—"}</td>
                    <td><StatusPill status={f.status} /></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

// ─── Tab: Technical Findings ──────────────────────────────────────────────────


// ─── Tab: Evidence Vault ──────────────────────────────────────────────────────

function EvidTab({ findings, activity, total }: { findings: Finding[]; activity: ActivityItem[]; total: number }) {
  const all = findings.flatMap(f => f.evidence.map(e => ({ ...e, finding: f })));
  const withEvid = findings.filter(f => f.evidence.length > 0).length;

  return (
    <>
      <div className="rpt-metrics">
        <Metric label="Evidence artifacts" value={all.length} note={`Across ${findings.length} findings`} />
        <Metric label="With evidence" value={withEvid} note={`${findings.length - withEvid} without`} />
        <Metric label="Activity events" value={activity.length} note="Latest recorded" />
        <Metric label="Loaded / total" value={`${findings.length}/${total}`} note="Finding coverage" />
      </div>

      <div className="rpt-section">
        <div className="rpt-section-head"><small>EVIDENCE INVENTORY</small><h3>Scanner artifacts — verbatim output</h3></div>
        {all.length === 0 && <p className="report-missing">No evidence artifacts in the loaded findings.</p>}
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {all.map((item, i) => (
            <div key={`${item.finding.id}-${i}`} style={{ border: "1px solid var(--border-subtle)", borderRadius: 8, overflow: "hidden" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "8px 12px", background: "var(--bg-surface)", borderBottom: "1px solid var(--border-subtle)" }}>
                <SevBadge sev={toSeverity(item.finding.severity)} />
                <span style={{ fontSize: 11, fontFamily: "var(--font-mono)", color: "var(--text-muted)" }}>{item.finding.id}</span>
                <span style={{ fontSize: 11, color: "var(--text-muted)" }}>·</span>
                <span style={{ fontSize: 11, color: "var(--text-secondary)" }}>{item.finding.affectedHost}</span>
                <span style={{ fontSize: 11, fontWeight: 600, color: "var(--text-secondary)", marginLeft: "auto" }}>{item.finding.title}</span>
              </div>
              <EvidBlock item={item} />
            </div>
          ))}
        </div>
      </div>

      <div className="rpt-section">
        <div className="rpt-section-head"><small>AUDIT TRAIL</small><h3>Assessment activity log</h3></div>
        {activity.length === 0 && <p className="report-missing">No activity recorded for this engagement.</p>}
        <div className="report-activity">
          {activity.map(e => (
            <article key={e.id}><Activity size={13} /><div><strong>{e.action}</strong><p>{e.detail}</p></div><time>{fmtDatetime(e.timestamp)}</time></article>
          ))}
        </div>
      </div>
    </>
  );
}

// ─── Tab: CVE Intelligence ────────────────────────────────────────────────────

function CveTab({ findings, total }: { findings: Finding[]; total: number }) {
  const withCve = findings.filter(f => f.cve && f.cve.length > 0);
  const allCves = [...new Set(findings.flatMap(f => f.cve ?? []))];
  const exploited = findings.filter(f => f.activelyExploited).length;

  return (
    <>
      <div className="rpt-metrics">
        <Metric label="Unique CVEs" value={allCves.length} note="Across loaded findings" tone={SEV_PALETTE.RED} />
        <Metric label="Findings with CVEs" value={withCve.length} note={`of ${findings.length} loaded`} tone={SEV_PALETTE.ORANGE} />
        <Metric label="Actively exploited" value={exploited} note="CISA KEV confirmed" tone={SEV_PALETTE.RED} />
        <Metric label="Total findings" value={total} note="Full scope" />
      </div>

      {exploited > 0 && (
        <div style={{ display: "flex", gap: 10, alignItems: "flex-start", padding: "11px 13px", borderRadius: 8, marginBottom: 14, background: `${SEV_PALETTE.RED}10`, border: `1px solid ${SEV_PALETTE.RED}33` }}>
          <Flame size={15} style={{ color: SEV_PALETTE.RED, flexShrink: 0, marginTop: 1 }} />
          <div><strong style={{ fontSize: 11, color: "var(--text-primary)", display: "block" }}>Active exploitation detected</strong><span style={{ fontSize: 11, color: "var(--text-secondary)", marginTop: 3, display: "block", lineHeight: 1.5 }}>{exploited} finding(s) are on the CISA KEV list — treat as P0 regardless of CVSS base score.</span></div>
        </div>
      )}

      <div className="rpt-section">
        <div className="rpt-section-head"><small>CVE INTELLIGENCE</small><h3>Findings with published vulnerability IDs</h3></div>
        {withCve.length === 0 && <p className="report-missing">No CVE IDs in loaded findings. CVEs appear when Vedha maps banner/CPE data to the NVD.</p>}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {withCve.map(f => {
            const sc = parseCvss(f.cvss);
            return (
              <div key={f.id} style={{ padding: "14px", borderRadius: 8, border: "1px solid var(--border-subtle)", background: "var(--bg-panel)" }}>
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 10 }}>
                  <div style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
                    <SevBadge sev={toSeverity(f.severity)} />
                    <div>
                      <div style={{ fontSize: 13.5, fontWeight: 700, color: "var(--text-primary)" }}>{f.title}</div>
                      <div style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 2, fontFamily: "var(--font-mono)" }}>{f.id} · {f.affectedHost}</div>
                    </div>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
                    {sc !== null && <span style={{ fontSize: 20, fontWeight: 800, fontFamily: "var(--font-mono)", color: cvssColor(sc) }}>{sc.toFixed(1)}</span>}
                    {f.activelyExploited && <span style={{ fontSize: 9, fontWeight: 800, color: SEV_PALETTE.RED, padding: "2px 6px", borderRadius: 4, background: `${SEV_PALETTE.RED}14` }}><Flame size={9} /> KEV</span>}
                  </div>
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {f.cve!.map(cve => (
                    <a key={cve} href={`https://nvd.nist.gov/vuln/detail/${cve}`} target="_blank" rel="noopener noreferrer" className="rpt-chip rpt-chip--cve">
                      <Globe size={10} /> {cve}
                    </a>
                  ))}
                </div>
                {f.description && <p style={{ margin: "10px 0 0", fontSize: 12, color: "var(--text-secondary)", lineHeight: 1.55 }}>{f.description.slice(0, 220)}{f.description.length > 220 ? "…" : ""}</p>}
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}

// ─── Tab: MITRE Coverage ─────────────────────────────────────────────────────

function CoverageTab({ findings, total }: { findings: Finding[]; total: number }) {
  const techniques = useMemo(() => {
    const map = new Map<string, { name: string; findings: Finding[] }>();
    findings.forEach(f => f.mitre.forEach(t => {
      const e = map.get(t.id) ?? { name: t.name, findings: [] };
      e.findings.push(f); map.set(t.id, e);
    }));
    return [...map.entries()].sort(([a], [b]) => a.localeCompare(b));
  }, [findings]);

  const covered = findings.filter(f => f.detectionCoverage === "COVERED").length;
  const blind = findings.filter(f => f.detectionCoverage === "BLIND").length;

  return (
    <>
      <div style={{ display: "flex", gap: 10, alignItems: "flex-start", padding: "11px 13px", borderRadius: 8, marginBottom: 14, background: "var(--sev-medium-bg)", border: "1px solid var(--border-default)" }}>
        <AlertTriangle size={15} style={{ color: "var(--sev-medium-color)", flexShrink: 0, marginTop: 1 }} />
        <div><strong style={{ fontSize: 11, color: "var(--text-primary)", display: "block" }}>MITRE ATT&amp;CK mapping only — no inferred compliance verdicts</strong><span style={{ fontSize: 11, color: "var(--text-secondary)", marginTop: 3, display: "block" }}>Formal NIST, ISO 27001, or PCI DSS compliance requires an approved scope, tested controls, and a qualified reviewer.</span></div>
      </div>
      <div className="rpt-metrics">
        <Metric label="Techniques observed" value={techniques.length} note="Linked to findings" />
        <Metric label="SOC covered" value={covered} note="Telemetry confirmed" tone={SEV_PALETTE.GREEN} />
        <Metric label="Blind spots" value={blind} note="No alerting telemetry" tone={SEV_PALETTE.RED} />
        <Metric label="Coverage" value={total > 0 ? `${Math.round((covered / total) * 100)}%` : "N/A"} note="Of total findings" />
      </div>
      <div className="rpt-section">
        <div className="rpt-section-head"><small>ATT&amp;CK MAPPING</small><h3>Observed adversary techniques</h3><span style={{ marginLeft: "auto", fontSize: 10, color: "var(--text-muted)" }}>{techniques.length} techniques · {findings.length}/{total} loaded</span></div>
        {techniques.length === 0 && <p className="report-missing">No ATT&amp;CK references in the loaded findings.</p>}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 8 }}>
          {techniques.map(([id, { name, findings: fgs }]) => {
            const worst = fgs.reduce<Severity>((w, f) => {
              const fi = SEVERITY_ORDER.indexOf(toSeverity(f.severity));
              const wi = SEVERITY_ORDER.indexOf(w);
              return fi < wi ? toSeverity(f.severity) : w;
            }, "INFO");
            return (
              <a key={id} href={`https://attack.mitre.org/techniques/${id.replace(".", "/")}/`}
                 target="_blank" rel="noopener noreferrer"
                 style={{ display: "flex", flexDirection: "column", gap: 5, padding: "10px 12px", borderRadius: 7, textDecoration: "none",
                   border: `1px solid var(--border-subtle)`, borderLeft: `3px solid ${SEV_COLOR[worst]}`,
                   background: "var(--bg-panel)", transition: "background 0.1s" }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <code style={{ fontFamily: "var(--font-mono)", fontSize: 11, fontWeight: 700, color: "var(--accent)" }}>{id}</code>
                  <SevBadge sev={worst} />
                </div>
                <span style={{ fontSize: 11.5, fontWeight: 700, color: "var(--text-primary)", lineHeight: 1.3 }}>{name || "Unnamed technique"}</span>
                <span style={{ fontSize: 10, color: "var(--text-muted)" }}>{fgs.length} finding{fgs.length !== 1 ? "s" : ""}</span>
              </a>
            );
          })}
        </div>
      </div>
    </>
  );
}

// ─── Page root ────────────────────────────────────────────────────────────────

export default function ReportsPage() {
  const [selId, setSelId] = useState("");
  const [tab, setTab] = useState<ReportTab>("executive");

  const engQ = useQuery({ queryKey: ["engagements"], queryFn: () => fetchJson<{ engagements: Engagement[] }>("/api/engagements"), retry: (c, e) => !isUnauthorized(e) && c < 2 });
  const engs = engQ.data?.engagements ?? [];
  const engId = selId || engs[0]?.id || "";
  const eng = engs.find(e => e.id === engId);

  const findQ = useQuery({ queryKey: ["rpt-findings", engId], queryFn: () => fetchJson<FindingPage>(`/api/findings?paginated=true&engagement_id=${encodeURIComponent(engId)}&page=1&page_size=100&sort=risk`), enabled: Boolean(engId), retry: (c, e) => !isUnauthorized(e) && c < 2 });
  const sumQ  = useQuery({ queryKey: ["rpt-summary",  engId], queryFn: () => fetchJson<FindingSummary>(`/api/findings/summary?engagement_id=${encodeURIComponent(engId)}`), enabled: Boolean(engId), retry: (c, e) => !isUnauthorized(e) && c < 2 });
  const actQ  = useQuery({ queryKey: ["rpt-activity", engId], queryFn: () => fetchJson<ActivityItem[]>(`/api/activity?engagement_id=${encodeURIComponent(engId)}&limit=50`), enabled: Boolean(engId), retry: (c, e) => !isUnauthorized(e) && c < 2 });

  const findings = findQ.data?.items ?? [];
  const reportFindings = useMemo(() => findings.map(toRawFinding), [findings]);
  const summary: FindingSummary = sumQ.data ?? { total: eng?.findingCount ?? 0, criticalOpen: 0, validated: 0, blind: 0, averageRisk: 0 };
  const loading  = engQ.isLoading || (Boolean(engId) && (findQ.isLoading || sumQ.isLoading));
  const loadErr  = engQ.error || findQ.error || sumQ.error;

  return (
    <PageShell
      title="Reports"
      subtitle="Professional VAPT deliverables — grounded in verified scanner evidence"
      headerActions={
        <button className="btn btn-secondary no-print" onClick={() => window.print()} disabled={!eng}>
          <Printer size={14} /> Export PDF
        </button>
      }
    >
      {/* Warning banner */}
      <div className="reports-beta-banner">
        <AlertTriangle size={14} />
        <div>
          <strong>Assessment report workspace</strong>
          <span>Data is sourced from the selected engagement. Review evidence, scope, and wording before client delivery. AI-generated sections require human approval.</span>
        </div>
      </div>

      {/* Controls */}
      <div className="report-controls no-print">
        <label>
          <span>Engagement</span>
          <select value={engId} onChange={e => { setSelId(e.target.value); setTab("executive"); }}>
            {engs.map(e => <option key={e.id} value={e.id}>{e.name} · {e.client}</option>)}
          </select>
        </label>
        <div role="tablist">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button key={id} role="tab" aria-selected={tab === id} data-active={tab === id} onClick={() => setTab(id)}>
              <Icon size={13} />{label}
            </button>
          ))}
        </div>
      </div>

      <DataState
        loading={loading} error={loadErr} isEmpty={!eng}
        onRetry={() => { void engQ.refetch(); void findQ.refetch(); void sumQ.refetch(); }}
        skeleton={<SkeletonRows rows={5} height={88} />}
        empty={<EmptyState icon={FileText} title="No engagement available" hint="Create an engagement and run an assessment before generating a report." />}
      >
        {eng && (
          <main className="report-document">
            {/* Cover */}
            <header className="report-cover">
              <div>
                <span><CheckCircle2 size={13} /> LIVE DATA</span>
                <h1>{eng.name}</h1>
                <p>{eng.client} · Vulnerability Assessment &amp; Penetration Test Report</p>
              </div>
              <dl>
                <div><dt>Status</dt><dd>{eng.status}</dd></div>
                <div><dt>Assessment window</dt><dd>{fmtDate(eng.startDate)} — {fmtDate(eng.endDate)}</dd></div>
                <div><dt>Lead assessor</dt><dd>{eng.assessor || "Not recorded"}</dd></div>
                <div><dt>Scope</dt><dd>{eng.scopeCidrs.length ? eng.scopeCidrs.join(", ") : "Not recorded"}</dd></div>
                <div><dt>Assets in scope</dt><dd>{eng.assetCount}</dd></div>
                <div><dt>Total findings</dt><dd>{eng.findingCount}</dd></div>
              </dl>
            </header>

            {/* Evidence boundary notice */}
            <div className="report-boundary" style={{ marginBottom: 0 }}>
              <Lock size={15} />
              <div>
                <strong>Evidence boundary</strong>
                <span>Detailed sections load up to 100 of {summary.total} findings (ranked by risk). Aggregate metrics cover the full engagement. Missing data is stated explicitly — never inferred.</span>
              </div>
            </div>

            {/* Tab content */}
            <div style={{ padding: "20px 24px 24px" }}>
              {tab === "executive" && <ExecTab eng={eng} findings={findings} summary={summary} />}
              {tab === "technical" && <FindingsSection findings={reportFindings} total={summary.total} />}
              {tab === "evidence"  && <EvidTab findings={findings} activity={actQ.data ?? []} total={summary.total} />}
              {tab === "cve"       && <CveTab findings={findings} total={summary.total} />}
              {tab === "coverage"  && <CoverageTab findings={findings} total={summary.total} />}
            </div>

            <footer className="report-footer">
              <FileText size={12} />
              Vedha VAPT Platform · {eng.name} · Human review required before delivery
            </footer>
          </main>
        )}
      </DataState>
    </PageShell>
  );
}
