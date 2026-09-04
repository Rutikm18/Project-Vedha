"use client";

import React, { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  FileText, Download, Loader2, ShieldAlert, BarChart3, FileArchive,
  Printer, ExternalLink, CheckCircle, AlertTriangle, Clock, X,
} from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { Timestamp } from "../../../components/portal/Timestamp";
import { DataState, SkeletonRows, EmptyState } from "../../../components/states/DataState";
import {
  portalApi, usePortalEngagement, SEVERITY_VAR, GRADE_VAR,
  type PortalSummary, type PortalTrends, type PortalFinding, type PortalReport,
} from "../../../lib/portal-client";

interface ReportContent extends PortalReport { content: string; }

type Tab = "executive" | "findings" | "documents";
const TABS: Array<{ id: Tab; label: string; icon: React.ElementType }> = [
  { id: "executive", label: "Executive Summary", icon: BarChart3 },
  { id: "findings",  label: "All Findings",      icon: FileText },
  { id: "documents", label: "Documents",          icon: FileArchive },
];

const SEVS = ["critical", "high", "medium", "low", "info"] as const;
const SEV_ORDER: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };

function fmtDate(v?: string | null) {
  if (!v) return "—";
  const d = new Date(v);
  return Number.isNaN(d.getTime()) ? "—"
    : new Intl.DateTimeFormat("en", { day: "numeric", month: "long", year: "numeric" }).format(d);
}

// ── Reusable pieces ──────────────────────────────────────────────────────────

function SevChip({ severity }: { severity: string }) {
  const c = SEVERITY_VAR[severity] ?? SEVERITY_VAR.info;
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", padding: "2px 8px", borderRadius: 5,
      fontSize: 10, fontWeight: 700, fontFamily: "var(--font-mono)", textTransform: "capitalize",
      color: c, background: `color-mix(in srgb, ${c} 12%, transparent)`,
      border: `0.5px solid color-mix(in srgb, ${c} 30%, transparent)`,
      letterSpacing: "0.04em",
    }}>
      {severity}
    </span>
  );
}

function MetricCard({ label, value, sub, color }: {
  label: string; value: string | number; sub: string; color: string;
}) {
  return (
    <div style={{
      display: "flex", flexDirection: "column", gap: 4, padding: "16px 18px",
      borderRadius: 10, border: `1px solid var(--border-subtle)`,
      background: "var(--bg-surface)",
      borderLeft: `3px solid ${color}`,
    }}>
      <span style={{ fontSize: 9, fontWeight: 800, textTransform: "uppercase",
        letterSpacing: "0.10em", color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
        {label}
      </span>
      <strong style={{ fontSize: 28, fontWeight: 800, lineHeight: 1, color }}>
        {value}
      </strong>
      <span style={{ fontSize: 10.5, color: "var(--text-secondary)", lineHeight: 1.4 }}>
        {sub}
      </span>
    </div>
  );
}

function SeverityBar({ bySeverity }: { bySeverity: Record<string, number> }) {
  const values = SEVS.filter((s) => s !== "info").map((s) => ({
    s, count: bySeverity[s] ?? 0,
  }));
  const total = Math.max(1, values.reduce((a, v) => a + v.count, 0));
  const hasSome = values.some((v) => v.count > 0);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      <div style={{
        display: "flex", height: 18, borderRadius: 99, overflow: "hidden",
        background: "var(--bg-hover)", gap: 1,
      }} aria-label="Findings by severity">
        {hasSome
          ? values.filter((v) => v.count > 0).map((v) => (
              <div key={v.s} title={`${v.s}: ${v.count}`}
                style={{ width: `${(v.count / total) * 100}%`, background: SEVERITY_VAR[v.s] }} />
            ))
          : <div style={{ width: "100%", background: "var(--bg-hover)" }} />}
      </div>
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
        {values.map((v) => (
          <div key={v.s} style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span style={{
              width: 8, height: 8, borderRadius: 2, background: SEVERITY_VAR[v.s], flexShrink: 0,
            }} />
            <span style={{ fontSize: 11, color: "var(--text-secondary)", textTransform: "capitalize" }}>
              {v.s}
            </span>
            <span style={{ fontSize: 12, fontWeight: 700, color: "var(--text-primary)",
              fontFamily: "var(--font-mono)" }}>
              {v.count}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function SectionBlock({ eyebrow, title, children, aside }: {
  eyebrow: string; title: string; children: React.ReactNode; aside?: React.ReactNode;
}) {
  return (
    <section style={{
      border: "1px solid var(--border-subtle)", borderRadius: 10,
      background: "var(--bg-surface)", overflow: "hidden",
    }}>
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "14px 18px", borderBottom: "1px solid var(--border-subtle)",
        background: "var(--bg-panel)",
      }}>
        <div>
          <div style={{ fontSize: 9, fontWeight: 800, textTransform: "uppercase",
            letterSpacing: "0.12em", color: "var(--text-muted)", fontFamily: "var(--font-mono)",
            marginBottom: 3 }}>
            {eyebrow}
          </div>
          <h3 style={{ margin: 0, fontSize: 14, fontWeight: 700,
            color: "var(--text-primary)", fontFamily: "var(--font-display)" }}>
            {title}
          </h3>
        </div>
        {aside && <div style={{ color: "var(--text-muted)", fontSize: 11 }}>{aside}</div>}
      </div>
      <div style={{ padding: "18px" }}>
        {children}
      </div>
    </section>
  );
}

// ── Priority action cards ─────────────────────────────────────────────────────

function PriorityItem({ index, text, tone }: { index: number; text: string; tone: string }) {
  return (
    <div style={{
      display: "flex", gap: 12, alignItems: "flex-start",
      padding: "12px 14px", borderRadius: 8,
      border: `1px solid color-mix(in srgb, ${tone} 20%, var(--border-subtle))`,
      background: `color-mix(in srgb, ${tone} 5%, var(--bg-panel))`,
    }}>
      <span style={{
        flexShrink: 0, width: 22, height: 22, borderRadius: "50%",
        background: tone, color: "#fff", display: "flex", alignItems: "center",
        justifyContent: "center", fontSize: 10, fontWeight: 800, fontFamily: "var(--font-mono)",
        marginTop: 1,
      }}>
        {index}
      </span>
      <span style={{ fontSize: 12.5, color: "var(--text-primary)", lineHeight: 1.6 }}>
        {text}
      </span>
    </div>
  );
}

// ── Findings table (executive + findings tab) ─────────────────────────────────

function FindingsTable({ findings, max }: { findings: PortalFinding[]; max?: number }) {
  const list = max !== undefined ? findings.slice(0, max) : findings;
  if (!list.length) {
    return (
      <div style={{ padding: "24px 0", textAlign: "center", color: "var(--text-muted)",
        fontSize: 12, border: "1px dashed var(--border-default)", borderRadius: 8 }}>
        No findings recorded for your engagement.
      </div>
    );
  }
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", minWidth: 500, borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "var(--bg-panel)" }}>
            {["Severity", "Finding", "CVSS", "Risk", "Status"].map((h, i) => (
              <th key={h} style={{
                padding: "9px 12px", textAlign: i >= 2 ? "right" : "left",
                fontSize: 9, fontWeight: 800, textTransform: "uppercase", letterSpacing: "0.08em",
                color: "var(--text-muted)", fontFamily: "var(--font-mono)",
                borderBottom: "1px solid var(--border-default)",
              }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {list.map((f) => (
            <tr key={f.id} style={{ borderBottom: "1px solid var(--border-subtle)" }}>
              <td style={{ padding: "11px 12px", whiteSpace: "nowrap" }}>
                <SevChip severity={f.severity} />
              </td>
              <td style={{ padding: "11px 12px" }}>
                <div style={{ fontSize: 12.5, fontWeight: 600, color: "var(--text-primary)",
                  lineHeight: 1.4 }}>
                  {f.title}
                </div>
                {f.cve_ids && f.cve_ids.length > 0 && (
                  <div style={{ marginTop: 3, fontSize: 10, color: "var(--accent)",
                    fontFamily: "var(--font-mono)" }}>
                    {f.cve_ids.slice(0, 3).join(" · ")}
                    {f.cve_ids.length > 3 ? ` +${f.cve_ids.length - 3}` : ""}
                  </div>
                )}
              </td>
              <td style={{ padding: "11px 12px", textAlign: "right",
                fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--text-secondary)" }}>
                {f.cvss_score ?? "—"}
              </td>
              <td style={{ padding: "11px 12px", textAlign: "right",
                fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--text-secondary)" }}>
                {f.risk_score ?? "—"}
              </td>
              <td style={{ padding: "11px 12px", textAlign: "right",
                fontSize: 11, textTransform: "capitalize", color: "var(--text-muted)" }}>
                {f.status}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ── Finding detail card (Findings tab) ───────────────────────────────────────

/** Small uppercase field label used throughout the detailed finding entry. */
function FieldLabel({ children, color }: { children: React.ReactNode; color?: string }) {
  return (
    <div style={{ fontSize: 9, fontWeight: 800, textTransform: "uppercase",
      letterSpacing: "0.10em", color: color ?? "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
      {children}
    </div>
  );
}

/** A professional, self-contained finding record: identification, evidence,
 *  provenance (time + source), and the recommended action. Numbered so a reader
 *  can cite "F-03" the way a real assessment report is cross-referenced. */
function FindingCard({ f, index }: { f: PortalFinding; index: number }) {
  const sevColor = SEVERITY_VAR[f.severity] ?? SEVERITY_VAR.info;
  const ref = `F-${String(index + 1).padStart(2, "0")}`;
  const cves = f.cve_ids ?? [];

  return (
    <article style={{
      borderRadius: 10, border: "1px solid var(--border-subtle)",
      background: "var(--bg-surface)", overflow: "hidden",
      borderLeft: `4px solid ${sevColor}`,
    }}>
      {/* Header row — reference, severity, CVEs, title */}
      <div style={{
        display: "flex", alignItems: "flex-start", justifyContent: "space-between",
        gap: 12, padding: "14px 18px",
        borderBottom: "1px solid var(--border-subtle)",
        background: "var(--bg-panel)",
      }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
            <span style={{
              fontSize: 10, fontWeight: 800, fontFamily: "var(--font-mono)",
              letterSpacing: "0.06em", color: "var(--text-secondary)",
              padding: "2px 7px", borderRadius: 5, background: "var(--bg-hover)",
              border: "0.5px solid var(--border-default)",
            }}>
              {ref}
            </span>
            <SevChip severity={f.severity} />
            {cves.map((cve) => (
              <a key={cve} href={`https://nvd.nist.gov/vuln/detail/${cve}`}
                target="_blank" rel="noopener noreferrer"
                style={{
                  display: "inline-flex", alignItems: "center", gap: 3,
                  fontSize: 9, fontWeight: 700, fontFamily: "var(--font-mono)",
                  color: "var(--sev-high-color)", textDecoration: "none", letterSpacing: "0.04em",
                  padding: "2px 7px", borderRadius: 5,
                  background: `color-mix(in srgb, var(--sev-high-color) 8%, transparent)`,
                  border: `0.5px solid color-mix(in srgb, var(--sev-high-color) 25%, transparent)`,
                }}>
                {cve} <ExternalLink size={8} />
              </a>
            ))}
          </div>
          <h4 style={{ margin: "8px 0 0", fontSize: 14, fontWeight: 700,
            color: "var(--text-primary)", lineHeight: 1.35 }}>
            {f.title}
          </h4>
        </div>
      </div>

      {/* Scores row */}
      <div style={{
        display: "flex", gap: 0, borderBottom: "1px solid var(--border-subtle)",
        background: "var(--bg-panel)",
      }}>
        {[
          { label: "CVSS", value: f.cvss_score ?? "—", color: f.cvss_score !== null ? sevColor : "var(--text-muted)" },
          { label: "Risk score", value: f.risk_score ?? "—", color: f.risk_score !== null ? sevColor : "var(--text-muted)" },
          { label: "Status", value: f.status, color: "var(--text-secondary)" },
        ].map((item, i) => (
          <div key={item.label} style={{
            flex: 1, padding: "10px 16px",
            borderRight: i < 2 ? "1px solid var(--border-subtle)" : "none",
          }}>
            <FieldLabel>{item.label}</FieldLabel>
            <div style={{ marginTop: 4, fontSize: 16, fontWeight: 700,
              color: item.color, textTransform: "capitalize", fontFamily: "var(--font-mono)" }}>
              {item.value}
            </div>
          </div>
        ))}
      </div>

      {/* Body — observation, provenance, recommended action */}
      <div style={{ padding: "16px 18px", display: "flex", flexDirection: "column", gap: 16 }}>
        {/* Observation & evidence */}
        <div>
          <FieldLabel>Observation &amp; evidence</FieldLabel>
          <p style={{ margin: "7px 0 0", fontSize: 12.5, color: "var(--text-secondary)", lineHeight: 1.65 }}>
            {f.description
              ?? "This finding was recorded during the assessment. A detailed technical description was not captured for this item."}
          </p>
        </div>

        {/* Provenance grid — time, source, references, status */}
        <div style={{
          display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 14,
          padding: "13px 15px", borderRadius: 8,
          background: "var(--bg-panel)", border: "1px solid var(--border-subtle)",
        }}>
          <div>
            <FieldLabel>Identified</FieldLabel>
            <div style={{ marginTop: 4, fontSize: 11.5, color: "var(--text-secondary)" }}>
              <Timestamp value={f.first_seen} variant="exact" />
            </div>
          </div>
          <div>
            <FieldLabel>Source</FieldLabel>
            <div style={{ marginTop: 4, fontSize: 11.5, color: "var(--text-secondary)" }}>
              Vedha automated assessment
            </div>
          </div>
          <div>
            <FieldLabel>References</FieldLabel>
            <div style={{ marginTop: 4, fontSize: 11.5, color: "var(--text-secondary)",
              display: "flex", flexWrap: "wrap", gap: 6 }}>
              {cves.length > 0
                ? cves.map((cve) => (
                    <a key={cve} href={`https://nvd.nist.gov/vuln/detail/${cve}`}
                      target="_blank" rel="noopener noreferrer"
                      style={{ display: "inline-flex", alignItems: "center", gap: 3,
                        color: "var(--accent)", textDecoration: "none",
                        fontFamily: "var(--font-mono)", fontSize: 11 }}>
                      {cve} <ExternalLink size={9} />
                    </a>
                  ))
                : <span style={{ color: "var(--text-muted)" }}>No public CVE mapping</span>}
            </div>
          </div>
          <div>
            <FieldLabel>Current status</FieldLabel>
            <div style={{ marginTop: 4, fontSize: 11.5, color: "var(--text-secondary)",
              textTransform: "capitalize" }}>
              {f.status}
            </div>
          </div>
        </div>

        {/* Recommended action */}
        <div style={{
          padding: "12px 14px", borderRadius: 8,
          background: `color-mix(in srgb, var(--nominal-color) 6%, var(--bg-panel))`,
          border: `1px solid color-mix(in srgb, var(--nominal-color) 22%, transparent)`,
          borderLeft: `3px solid var(--nominal-color)`,
        }}>
          <FieldLabel color="var(--nominal-color)">
            <span style={{ display: "inline-flex", alignItems: "center", gap: 5 }}>
              <CheckCircle size={10} /> Recommended action
            </span>
          </FieldLabel>
          <p style={{ margin: "7px 0 0", fontSize: 12.5, color: "var(--text-primary)", lineHeight: 1.65 }}>
            {f.remediation
              ?? "Remediation guidance for this finding is being prepared by your security team."}
          </p>
        </div>
      </div>
    </article>
  );
}

// ── Executive tab ─────────────────────────────────────────────────────────────

function ExecutiveTab({ summary, trends, findings }: {
  summary: PortalSummary; trends: PortalTrends; findings: PortalFinding[];
}) {
  const p = summary.posture;
  const openCrit = summary.severity_counts?.critical ?? 0;
  const openHigh = summary.severity_counts?.high ?? 0;

  const riskStatement = openCrit > 0 ? "Immediate action required"
    : openHigh > 0 ? "Elevated risk — action recommended"
    : summary.open_findings > 0 ? "Managed — remediation in progress"
    : "Secure posture — no open findings";

  const riskColor = openCrit > 0 ? "var(--sev-critical-color)"
    : openHigh > 0 ? "var(--sev-high-color)"
    : summary.open_findings > 0 ? "var(--sev-medium-color)"
    : "var(--nominal-color)";

  const priorities = [
    openCrit > 0
      ? { text: `Assign owners and remediation dates to ${openCrit} critical finding${openCrit === 1 ? "" : "s"} immediately.`, tone: "var(--sev-critical-color)" }
      : null,
    openHigh > 0
      ? { text: `Prioritise ${openHigh} high-severity finding${openHigh === 1 ? "" : "s"} in the current remediation cycle.`, tone: "var(--sev-high-color)" }
      : null,
    summary.pending_requests > 0
      ? { text: `${summary.pending_requests} scan request${summary.pending_requests === 1 ? "" : "s"} await your security team's approval.`, tone: "var(--sev-medium-color)" }
      : null,
    summary.open_findings > 0
      ? { text: "Retest each remediated finding and verify the fix before closure.", tone: "var(--accent)" }
      : { text: "No open findings — maintain posture with periodic scheduled scans.", tone: "var(--nominal-color)" },
  ].filter(Boolean) as Array<{ text: string; tone: string }>;

  const topFindings = [...findings]
    .filter((f) => f.status === "open" || f.status === "confirmed")
    .sort((a, b) =>
      (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9) ||
      (b.risk_score ?? 0) - (a.risk_score ?? 0),
    );

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      {/* Risk position hero */}
      <div style={{
        display: "flex", alignItems: "flex-start", justifyContent: "space-between",
        gap: 20, padding: "22px 24px", borderRadius: 10,
        border: `1px solid color-mix(in srgb, ${riskColor} 22%, var(--border-subtle))`,
        background: `color-mix(in srgb, ${riskColor} 6%, var(--bg-surface))`,
      }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 9, fontWeight: 800, textTransform: "uppercase",
            letterSpacing: "0.12em", color: "var(--text-muted)", fontFamily: "var(--font-mono)",
            marginBottom: 10 }}>
            Executive Risk Position
          </div>
          <div style={{ fontSize: 22, fontWeight: 750, color: riskColor, lineHeight: 1.2,
            fontFamily: "var(--font-display)", letterSpacing: "-0.01em" }}>
            {riskStatement}
          </div>
          <p style={{ margin: "10px 0 0", fontSize: 12, color: "var(--text-secondary)",
            lineHeight: 1.65, maxWidth: 640 }}>
            This summary reflects your engagement&apos;s currently recorded findings and posture score.
            It does not assert that untested assets are secure — only assessed surfaces are represented.
          </p>
        </div>
        <ShieldAlert size={32} color={riskColor} style={{ flexShrink: 0, opacity: 0.7 }} />
      </div>

      {/* KPI metrics */}
      <div style={{
        display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10,
      }} className="report-kpi-grid">
        <MetricCard
          label="Posture grade" value={p.grade || "—"}
          sub={`Score ${p.posture_score ?? 0} / 100`}
          color={GRADE_VAR[p.grade] ?? "var(--accent)"}
        />
        <MetricCard
          label="Risk index" value={p.risk_index ?? 0}
          sub="Higher = more risk (0–100)"
          color="var(--sev-high-color)"
        />
        <MetricCard
          label="Open findings" value={summary.open_findings ?? 0}
          sub="Awaiting remediation"
          color="var(--sev-critical-color)"
        />
        <MetricCard
          label="Remediated" value={summary.closed_findings ?? 0}
          sub="Verified and closed"
          color="var(--nominal-color)"
        />
      </div>

      {/* Severity distribution */}
      <SectionBlock eyebrow="Risk distribution" title="Open findings by severity">
        <SeverityBar bySeverity={trends.by_severity} />
      </SectionBlock>

      {/* Priority actions */}
      {priorities.length > 0 && (
        <SectionBlock eyebrow="Decision queue" title="Priority actions">
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {priorities.map((item, i) => (
              <PriorityItem key={i} index={i + 1} text={item.text} tone={item.tone} />
            ))}
          </div>
        </SectionBlock>
      )}

      {/* Top findings */}
      <SectionBlock
        eyebrow="Top exposures" title="Highest-risk open findings"
        aside={topFindings.length > 10 ? `Showing 10 of ${topFindings.length}` : undefined}
      >
        <FindingsTable findings={topFindings} max={10} />
      </SectionBlock>
    </div>
  );
}

// ── Findings tab — card-per-finding ──────────────────────────────────────────

function FindingsTab({ findings }: { findings: PortalFinding[] }) {
  const sorted = [...findings].sort(
    (a, b) =>
      (SEV_ORDER[a.severity] ?? 9) - (SEV_ORDER[b.severity] ?? 9) ||
      (b.risk_score ?? 0) - (a.risk_score ?? 0),
  );
  if (!sorted.length) {
    return (
      <div style={{ padding: "40px", textAlign: "center", color: "var(--text-muted)",
        fontSize: 13, border: "1px dashed var(--border-default)", borderRadius: 10 }}>
        No findings recorded for your engagement.
      </div>
    );
  }

  // Count by severity for the register summary line.
  const bySev = SEVS.map((s) => ({ s, n: sorted.filter((f) => f.severity === s).length }))
    .filter((x) => x.n > 0);

  return (
    <SectionBlock
      eyebrow="Technical detail"
      title="Detailed findings register"
      aside={`${sorted.length} finding${sorted.length === 1 ? "" : "s"}`}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {/* Register summary: what's inside, ordered highest-risk first */}
        <div style={{ display: "flex", alignItems: "center", flexWrap: "wrap", gap: 14,
          paddingBottom: 12, borderBottom: "1px solid var(--border-subtle)" }}>
          <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
            Every recorded finding, ordered by risk. Each entry carries its evidence, time of
            identification, source and recommended action.
          </span>
          <div style={{ display: "flex", gap: 12, marginLeft: "auto", flexWrap: "wrap" }}>
            {bySev.map(({ s, n }) => (
              <span key={s} style={{ display: "inline-flex", alignItems: "center", gap: 5 }}>
                <span style={{ width: 8, height: 8, borderRadius: 2, background: SEVERITY_VAR[s] }} />
                <span style={{ fontSize: 11, color: "var(--text-secondary)", textTransform: "capitalize" }}>{s}</span>
                <span style={{ fontSize: 12, fontWeight: 700, fontFamily: "var(--font-mono)",
                  color: "var(--text-primary)" }}>{n}</span>
              </span>
            ))}
          </div>
        </div>

        {sorted.map((f, i) => <FindingCard key={f.id} f={f} index={i} />)}
      </div>
    </SectionBlock>
  );
}

// ── Documents tab ─────────────────────────────────────────────────────────────

function DocumentsTab({ reports, onView, loadingId }: {
  reports: PortalReport[]; onView: (id: string, el: HTMLElement) => void; loadingId: string | null;
}) {
  if (!reports.length) {
    return (
      <div className="panel">
        <EmptyState icon={FileArchive} title="No documents yet"
          hint="Approved assessment reports for your engagement will appear here." />
      </div>
    );
  }
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {reports.map((r) => (
        <div key={r.id} style={{
          display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "14px 18px", borderRadius: 10,
          border: "1px solid var(--border-subtle)", background: "var(--bg-surface)",
          gap: 12,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{
              width: 38, height: 38, borderRadius: 9,
              background: "var(--accent-ghost)", border: "0.5px solid var(--border-accent)",
              display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
            }}>
              <FileText size={16} color="var(--accent)" />
            </div>
            <div>
              <div style={{ fontSize: 13, fontWeight: 600, color: "var(--text-primary)",
                textTransform: "capitalize" }}>
                {r.output_type.replace(/_/g, " ")}
              </div>
              <div style={{ marginTop: 3, fontSize: 11, color: "var(--text-muted)",
                display: "flex", alignItems: "center", gap: 6 }}>
                <Clock size={10} />
                <Timestamp value={r.generated_at} relative />
                <span style={{ opacity: 0.5 }}>·</span>
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 9 }}>{r.model}</span>
              </div>
            </div>
          </div>
          <button
            onClick={(e) => onView(r.id, e.currentTarget)}
            disabled={loadingId === r.id}
            className="btn btn-secondary"
            aria-label={`View ${r.output_type.replace(/_/g, " ")}`}
            style={{ flexShrink: 0 }}
          >
            {loadingId === r.id
              ? <Loader2 className="animate-spin" size={14} />
              : <Download size={14} />}
            View
          </button>
        </div>
      ))}
    </div>
  );
}

// ── Report viewer modal ───────────────────────────────────────────────────────

function ReportModal({ report, onClose }: { report: ReportContent; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    ref.current?.focus();
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", h);
    return () => document.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div onClick={onClose} style={{
      position: "fixed", inset: 0, zIndex: 50, padding: 20,
      display: "flex", alignItems: "center", justifyContent: "center",
      background: "var(--modal-backdrop)",
    }}>
      <div ref={ref} role="dialog" aria-modal tabIndex={-1}
        aria-label={`${report.output_type.replace(/_/g, " ")} report`}
        onClick={(e) => e.stopPropagation()}
        className="panel animate-scale-in"
        style={{
          display: "flex", flexDirection: "column",
          maxHeight: "85vh", width: "100%", maxWidth: 800, outline: "none",
        }}>
        <div style={{
          display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "12px 16px", borderBottom: "0.5px solid var(--border-subtle)",
        }}>
          <div>
            <div style={{ fontSize: 13, fontWeight: 600, color: "var(--text-primary)",
              textTransform: "capitalize" }}>
              {report.output_type.replace(/_/g, " ")}
            </div>
            <div style={{ fontSize: 10, color: "var(--text-muted)", marginTop: 2 }}>
              {report.model}
            </div>
          </div>
          <button onClick={onClose} aria-label="Close"
            style={{ background: "none", border: "none", cursor: "pointer",
              color: "var(--text-muted)", display: "flex", padding: 4, borderRadius: 6 }}>
            <X size={16} />
          </button>
        </div>
        <pre style={{
          flex: 1, overflow: "auto", margin: 0,
          padding: "16px 20px", whiteSpace: "pre-wrap", wordBreak: "break-word",
          fontSize: 12, lineHeight: 1.7, color: "var(--text-secondary)",
          fontFamily: "var(--font-mono)",
        }}>
          {report.content}
        </pre>
      </div>
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function PortalReports() {
  const [tab, setTab] = useState<Tab>("executive");
  const [modal, setModal] = useState<ReportContent | null>(null);
  const [loadingId, setLoadingId] = useState<string | null>(null);
  const triggerRef = useRef<HTMLElement | null>(null);

  const eng     = usePortalEngagement();
  const summary = useQuery({ queryKey: ["portal", "summary"],  queryFn: () => portalApi<PortalSummary>("/summary") });
  const trends  = useQuery({ queryKey: ["portal", "trends"],   queryFn: () => portalApi<PortalTrends>("/trends") });
  const findings= useQuery({ queryKey: ["portal", "findings"], queryFn: () => portalApi<PortalFinding[]>("/findings") });
  const reports = useQuery({ queryKey: ["portal", "reports"],  queryFn: () => portalApi<PortalReport[]>("/reports") });

  async function viewDoc(id: string, el: HTMLElement) {
    triggerRef.current = el;
    setLoadingId(id);
    try { setModal(await portalApi<ReportContent>(`/reports/${id}`)); }
    finally { setLoadingId(null); }
  }

  const coreLoading = eng.isLoading || summary.isLoading || trends.isLoading;
  const coreError   = eng.error || summary.error || trends.error;

  return (
    <PortalShell
      title="Reports"
      subtitle={eng.data?.name ?? "Assessment deliverables"}
      headerActions={
        <button className="btn btn-secondary no-print" onClick={() => window.print()}>
          <Printer size={13} /> Print / PDF
        </button>
      }
    >
      {/* Tab bar */}
      <div role="tablist" aria-label="Report section" style={{
        display: "flex", gap: 4, marginBottom: 16, padding: "4px",
        background: "var(--bg-panel)", borderRadius: 10,
        border: "1px solid var(--border-subtle)", width: "fit-content",
      }}>
        {TABS.map(({ id, label, icon: Icon }) => {
          const active = tab === id;
          return (
            <button
              key={id} role="tab" aria-selected={active}
              onClick={() => setTab(id)}
              style={{
                display: "inline-flex", alignItems: "center", gap: 7,
                height: 34, padding: "0 14px", borderRadius: 7, border: "none",
                cursor: "pointer", fontSize: 12, fontWeight: 600, transition: "all 0.15s",
                background: active ? "var(--accent)" : "transparent",
                color: active ? "#fff" : "var(--text-secondary)",
                boxShadow: active ? "0 1px 4px rgba(0,0,0,0.15)" : "none",
              }}
            >
              <Icon size={13} />
              <span className="report-tab-label">{label}</span>
            </button>
          );
        })}
      </div>

      {/* Documents tab — separate data source */}
      {tab === "documents" && (
        <DataState
          loading={reports.isLoading} error={reports.error}
          isEmpty={(reports.data ?? []).length === 0}
          onRetry={() => reports.refetch()}
          onLogin={() => { window.location.href = "/portal/login"; }}
          skeleton={<div className="panel" style={{ padding: 16 }}><SkeletonRows rows={4} /></div>}
          empty={<div className="panel"><EmptyState icon={FileArchive} title="No documents yet"
            hint="Approved assessment reports for your engagement will appear here." /></div>}
        >
          <DocumentsTab reports={reports.data ?? []} onView={viewDoc} loadingId={loadingId} />
        </DataState>
      )}

      {/* Executive + Findings tabs — share the same data */}
      {tab !== "documents" && (
        <DataState
          loading={coreLoading} error={coreError}
          isEmpty={!eng.data || !summary.data || !trends.data}
          onRetry={() => { eng.refetch(); summary.refetch(); trends.refetch(); findings.refetch(); }}
          onLogin={() => { window.location.href = "/portal/login"; }}
          skeleton={<SkeletonRows rows={6} height={88} />}
          empty={<div className="panel"><EmptyState icon={FileText} title="No engagement data yet"
            hint="Report figures appear once your engagement has recorded data." /></div>}
        >
          {eng.data && summary.data && trends.data && (
            <div className="report-document-v2">
              {/* Cover */}
              <div className="report-cover-v2">
                <div className="report-cover-v2-left">
                  <div className="report-cover-v2-eyebrow">
                    <BarChart3 size={12} />
                    Security Assessment Report · Live data
                  </div>
                  <h1 className="report-cover-v2-title">{eng.data.name}</h1>
                  <p className="report-cover-v2-sub">Customer-facing engagement view</p>
                </div>
                <dl className="report-cover-v2-meta">
                  <div>
                    <dt>Status</dt>
                    <dd style={{ textTransform: "capitalize" }}>{eng.data.status}</dd>
                  </div>
                  <div>
                    <dt>Scope</dt>
                    <dd>{eng.data.scope_cidr_count} network range{eng.data.scope_cidr_count === 1 ? "" : "s"}</dd>
                  </div>
                  <div>
                    <dt>Generated</dt>
                    <dd>{fmtDate(new Date().toISOString())}</dd>
                  </div>
                  <div>
                    <dt>Open findings</dt>
                    <dd>{summary.data.open_findings}</dd>
                  </div>
                </dl>
              </div>

              {/* Evidence boundary notice */}
              <div className="report-notice">
                <AlertTriangle size={14} style={{ flexShrink: 0 }} />
                <div>
                  <strong>Evidence boundary</strong>
                  <span>
                    Figures reflect recorded findings from assessed targets only. Assets not included in scope
                    are not represented — their absence is not evidence of security.
                  </span>
                </div>
              </div>

              {/* Tab content */}
              <div className="report-body">
                {tab === "executive" && (
                  <ExecutiveTab
                    summary={summary.data}
                    trends={trends.data}
                    findings={findings.data ?? []}
                  />
                )}
                {tab === "findings" && (
                  <FindingsTab findings={findings.data ?? []} />
                )}
              </div>

              {/* Footer */}
              <div className="report-foot">
                <FileText size={11} />
                Generated from Vedha engagement records · Not a substitute for human review
              </div>
            </div>
          )}
        </DataState>
      )}

      {modal && <ReportModal report={modal} onClose={() => { setModal(null); triggerRef.current?.focus(); }} />}
    </PortalShell>
  );
}
