"use client";

import React, { useState, useCallback, useDeferredValue, useSyncExternalStore } from "react";
import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Copy, Check, Search, CheckCircle, Shield,
  ArrowUpDown, ChevronLeft, ChevronRight, Link2, Brain, Tag,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { useAssistant } from "../../components/assistant/AssistantProvider";
import { useToast } from "../../hooks/useToast";
import { errorMessage, fetchJson, isUnauthorized } from "../../lib/fetcher";
import { DataState, SkeletonRows, EmptyState } from "../../components/states/DataState";
import {
  SEV_COLOR, STATUS_COLOR, STATUS_LABEL, MATURITY_COLOR, COVERAGE_COLOR,
  PRIORITY_COLOR, KILL_CHAIN_PHASE_COLOR, riskScoreColor, epssColor, SEV_PALETTE,
} from "../../lib/severity";

/* ─── Types ─── */
type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";
type FindingStatus = "OPEN" | "CONFIRMED" | "REMEDIATED" | "ACCEPTED" | "FALSE_POSITIVE";
type ExploitMaturity = "WEAPONIZED" | "POC" | "THEORETICAL";
type DetectionCoverage = "COVERED" | "PARTIAL" | "BLIND";
const FINDINGS_PER_PAGE = 20;

function subscribeToLocationChange(onChange: () => void) {
  window.addEventListener("popstate", onChange);
  return () => window.removeEventListener("popstate", onChange);
}

function getLocationSearch() {
  return window.location.search;
}

function getServerLocationSearch() {
  return "";
}

interface RemStep {
  step: number; title: string; command?: string;
  description: string; estimatedHours: number;
  verification?: string; completed: boolean; completedBy?: string;
}
interface ComplianceRef { framework: string; refs: string[]; }
interface RiskBreakdown {
  cvss: number; epss: number; kev: number;
  exploit: number; asset: number; lateral: number;
}
interface KillChainStep {
  phase: string; technique: string; description: string; mitre?: string;
}
interface Finding {
  id: string; title: string; severity: Severity; cvss: string; cvssVector: string;
  category: string; status: FindingStatus; affectedHost: string; discoveredAt: string;
  description: string; technicalDetails: string; attackPath: string;
  evidence: { label: string; content: string }[];
  impact: string; businessImpact?: string;
  exploitability?: "EASY" | "MODERATE" | "DIFFICULT";
  remediation: (string | RemStep)[];
  compliance: ComplianceRef[];
  mitre: { id: string; name: string }[];
  riskScore: number;
  riskBreakdown: RiskBreakdown;
  epssScore: number;
  epssPercentile: number;
  epssRecorded: boolean;
  kevListed: boolean;
  kevStatusRecorded: boolean;
  kevDateAdded?: string;
  exploitMaturity: ExploitMaturity;
  exploitMaturityRecorded: boolean;
  pocAvailable: boolean;
  activelyExploited: boolean;
  detectionCoverage: DetectionCoverage;
  detectionNote?: string;
  fpProbability: number;
  fpProbabilityRecorded: boolean;
  relatedFindings?: string[];
  killChain: KillChainStep[];
  assignee?: string;
  tags?: string[];
  cves?: string[];
  aiTriage: { priority: "P0" | "P1" | "P2" | "P3"; reasoning: string; recommendation: string; confidence: number };
}

interface FindingPage {
  items: Finding[];
  total: number;
  page: number;
  pageSize: number;
  pages: number;
}

interface FindingSummary {
  total: number;
  criticalOpen: number;
  validated: number;
  blind: number;
  averageRisk: number;
}

/* ─── Color Maps ─── */
// Semantic colors now come from the shared, WCAG-AA source of truth (lib/severity).

/* ─── SLA helpers ─── */
const SLA_HOURS: Partial<Record<Severity, number>> = { CRITICAL: 24, HIGH: 72, MEDIUM: 168, LOW: 720 };

function getSlaColor(discoveredAt: string, severity: Severity) {
  const slaH = SLA_HOURS[severity];
  if (!slaH) return { color: "var(--text-secondary)", label: "N/A", pct: 100 };
  const due = new Date(discoveredAt).getTime() + slaH * 3_600_000;
  const now = Date.now();
  const leftMs = due - now;
  const pct = Math.max(0, Math.min(100, (leftMs / (slaH * 3_600_000)) * 100));
  if (now > due) return { color: SEV_PALETTE.RED, label: "BREACHED", pct: 0 };
  const h = Math.round(leftMs / 3_600_000);
  const label = h < 24 ? `${h}h` : `${Math.round(h / 24)}d`;
  const color = pct < 10 ? SEV_PALETTE.RED : pct < 25 ? SEV_PALETTE.ORANGE : pct < 50 ? SEV_PALETTE.AMBER : SEV_PALETTE.GREEN;
  return { color, label, pct };
}

// riskScoreColor imported from lib/severity (shared, AA-compliant palette).


/* ─── Copy Button ─── */
function CopyBtn({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      type="button"
      aria-label={copied ? "Copied command" : "Copy command"}
      onClick={() => { navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 2000); }}
      style={{ background: "none", border: "none", cursor: "pointer", color: copied ? "#059669" : "#64748B", padding: "2px 4px" }}>
      {copied ? <Check size={12} /> : <Copy size={12} />}
    </button>
  );
}

/* ─── Severity Badge ─── */
function SevBadge({ s }: { s: Severity }) {
  return (
    <span style={{
      fontFamily: "var(--font-mono)", fontSize: 10, padding: "2px 8px", borderRadius: 4,
      background: `${SEV_COLOR[s]}15`, color: SEV_COLOR[s], border: `1px solid ${SEV_COLOR[s]}30`,
    }}>{s}</span>
  );
}

/* ─── Risk Score Badge ─── */
function RiskBadge({ score }: { score: number }) {
  const c = riskScoreColor(score);
  return (
    <span style={{
      fontFamily: "var(--font-mono)", fontSize: 10, padding: "2px 8px", borderRadius: 4,
      background: `${c}15`, color: c, border: `1px solid ${c}30`, fontWeight: 700,
    }}>
      RISK {score}
    </span>
  );
}

/* ─── KEV Badge ─── */
function KevBadge() {
  return (
    <span style={{
      fontFamily: "var(--font-mono)", fontSize: 9, padding: "2px 6px", borderRadius: 4,
      background: `${SEV_PALETTE.RED}15`, color: SEV_PALETTE.RED, border: `1px solid ${SEV_PALETTE.RED}55`,
      fontWeight: 700, letterSpacing: 0.5,
    }}>
      ⚠ KEV
    </span>
  );
}

/* ─── Status Badge ─── */
function StatusBadge({ s, onClick }: { s: FindingStatus; onClick?: () => void }) {
  return (
    <span onClick={onClick} style={{
      fontFamily: "var(--font-mono)", fontSize: 10, padding: "2px 8px", borderRadius: 4,
      background: `${STATUS_COLOR[s]}12`, color: STATUS_COLOR[s], border: `1px solid ${STATUS_COLOR[s]}30`,
      cursor: onClick ? "pointer" : "default",
    }}>
      {STATUS_LABEL[s]}
    </span>
  );
}

/* ─── Detection Coverage Pill ─── */
function DetectionPill({ cov }: { cov: DetectionCoverage }) {
  const c = COVERAGE_COLOR[cov];
  const icon = cov === "COVERED" ? "◉" : cov === "PARTIAL" ? "◑" : "○";
  return (
    <span style={{
      fontFamily: "var(--font-mono)", fontSize: 9, padding: "2px 6px", borderRadius: 4,
      background: `${c}12`, color: c, border: `1px solid ${c}30`,
    }}>
      {icon} {cov}
    </span>
  );
}

/* ─── EPSS Bar ─── */
function EpssBar({ score, percentile }: { score: number; percentile: number }) {
  const pct = Math.round(score * 100);
  const color = epssColor(score);
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 3 }}>
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color }}>
          EPSS {(score * 100).toFixed(1)}%
        </span>
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>
          {Math.round(percentile * 100)}th pct
        </span>
      </div>
      <div style={{ height: 4, background: "rgba(100,116,139,0.2)", borderRadius: 2, overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 2, transition: "width 0.4s ease" }} />
      </div>
    </div>
  );
}

/* ─── Risk Score Breakdown ─── */
function RiskBreakdownBar({ breakdown }: { breakdown: RiskBreakdown }) {
  const segments = [
    { key: "cvss",    label: "CVSS",    color: SEV_PALETTE.ORANGE, value: breakdown.cvss },
    { key: "epss",    label: "EPSS",    color: SEV_PALETTE.BLUE,   value: breakdown.epss },
    { key: "kev",     label: "KEV",     color: SEV_PALETTE.RED,    value: breakdown.kev },
    { key: "exploit", label: "EXPLOIT", color: SEV_PALETTE.VIOLET, value: breakdown.exploit },
    { key: "asset",   label: "ASSET",   color: SEV_PALETTE.AMBER,  value: breakdown.asset },
    { key: "lateral", label: "LATERAL", color: SEV_PALETTE.GREEN,  value: breakdown.lateral },
  ];
  return (
    <div>
      <div style={{ height: 8, display: "flex", borderRadius: 4, overflow: "hidden", marginBottom: 6 }}>
        {segments.map((s) => (
          <div key={s.key} style={{ width: `${(s.value / 1000) * 100}%`, background: s.color }} title={`${s.label}: ${s.value}`} />
        ))}
      </div>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {segments.map((s) => (
          <div key={s.key} style={{ display: "flex", alignItems: "center", gap: 4 }}>
            <div style={{ width: 6, height: 6, borderRadius: 1, background: s.color }} />
            <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>
              {s.label} {s.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── Kill Chain Visualization ─── */
function KillChainViz({ steps }: { steps: KillChainStep[] }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
      {steps.map((step, i) => {
        const color = KILL_CHAIN_PHASE_COLOR[step.phase] ?? "#64748B";
        return (
          <div key={i} style={{ display: "flex", gap: 0, alignItems: "stretch" }}>
            {/* Timeline line */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 24, flexShrink: 0 }}>
              <div style={{
                width: 10, height: 10, borderRadius: "50%", background: color,
                border: `2px solid ${color}40`, flexShrink: 0, marginTop: 4, zIndex: 1,
                boxShadow: `0 0 6px ${color}60`,
              }} />
              {i < steps.length - 1 && (
                <div style={{ width: 1, flex: 1, background: `${color}30`, minHeight: 16 }} />
              )}
            </div>
            {/* Step content */}
            <div style={{ flex: 1, paddingBottom: i < steps.length - 1 ? 10 : 0, paddingLeft: 8 }}>
              <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 2 }}>
                <span style={{
                  fontFamily: "var(--font-mono)", fontSize: 9, color,
                  background: `${color}12`, border: `1px solid ${color}25`,
                  padding: "1px 5px", borderRadius: 3,
                }}>{step.phase}</span>
                {step.mitre && (
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--accent)" }}>
                    {step.mitre}
                  </span>
                )}
              </div>
              <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 12, fontWeight: 600, color: "var(--text-primary)", marginBottom: 1 }}>
                {step.technique}
              </div>
              <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.4 }}>
                {step.description}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ─── Remediation Checklist ─── */
function RemediationChecklist({ steps }: { steps: (string | RemStep)[] }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {steps.map((s, i) => {
        if (typeof s === "string") {
          return (
            <div key={i} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
              <span aria-hidden style={{ color: "var(--accent)", marginTop: 2 }}>•</span>
              <span style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, color: "var(--text-primary)", lineHeight: 1.5 }}>{s}</span>
            </div>
          );
        }
        const done = s.completed;
        return (
          <div key={i} style={{ background: "var(--bg-app)", border: `1px solid ${done ? "rgba(5,150,105,0.2)" : "var(--border-subtle)"}`, borderRadius: 6, padding: "10px 12px" }}>
            <div style={{ display: "flex", gap: 10, alignItems: "flex-start", marginBottom: s.command ? 8 : 0 }}>
              <div role="img" aria-label={done ? "Completed" : "Not completed"} style={{
                width: 16, height: 16, borderRadius: 4, flexShrink: 0, marginTop: 2,
                background: done ? "rgba(5,150,105,0.2)" : "transparent",
                border: `1.5px solid ${done ? "#059669" : "#E2E8F0"}`,
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>
                {done && <Check size={10} color="#059669" />}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, fontWeight: 600, color: done ? "#64748B" : "var(--text-primary)", textDecoration: done ? "line-through" : "none" }}>
                    Step {s.step}: {s.title}
                  </span>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>~{s.estimatedHours}h</span>
                </div>
                <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 12, color: "var(--text-secondary)", marginTop: 2 }}>{s.description}</div>
              </div>
            </div>
            {s.command && (
              <div style={{ background: "var(--bg-panel)", borderRadius: 4, padding: "6px 10px", display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 4 }}>
                <code style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--accent)", flex: 1, whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{s.command}</code>
                <CopyBtn text={s.command} />
              </div>
            )}
            {s.verification && (
              <div style={{ marginTop: 4, display: "flex", gap: 6, alignItems: "center" }}>
                <CheckCircle size={10} color="#059669" />
                <code style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "#059669" }}>Verify: {s.verification}</code>
              </div>
            )}
            {s.completedBy && (
              <div style={{ marginTop: 4, fontFamily: "var(--font-mono)", fontSize: 9, color: "#059669" }}>
                ✓ Completed by {s.completedBy}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

/* ─── Finding Detail ─── */
function FindingDetail({ f, allFindings, onStatusChange, statusUpdating }: {
  f: Finding;
  allFindings: Finding[];
  onStatusChange: (id: string, s: FindingStatus) => void;
  statusUpdating: boolean;
}) {
  const [tab, setTab] = useState<"overview" | "intel" | "evidence" | "remediation" | "compliance">("overview");
  const { explain } = useAssistant();
  const sla = getSlaColor(f.discoveredAt, f.severity);

  const WORKFLOW: { status: FindingStatus; label: string; color: string }[] = [
    { status: "OPEN",           label: "Reopen",       color: SEV_PALETTE.RED },
    { status: "CONFIRMED",      label: "Confirm",      color: SEV_PALETTE.ORANGE },
    { status: "REMEDIATED",     label: "Remediated",   color: SEV_PALETTE.GREEN },
    { status: "ACCEPTED",       label: "Accept Risk",  color: SEV_PALETTE.VIOLET },
    { status: "FALSE_POSITIVE", label: "False Pos.",   color: "var(--text-secondary)" },
  ];

  const related = allFindings.filter((r) => r.id !== f.id && (f.relatedFindings ?? []).includes(r.id));
  const pc = PRIORITY_COLOR[f.aiTriage.priority];
  const hasAiTriage = Boolean(f.aiTriage.reasoning || f.aiTriage.recommendation) && f.aiTriage.confidence > 0;
  const cveIds = [...new Set([...(f.cves ?? []), ...(f.tags ?? [])].filter((value) => /^CVE-\d{4}-\d{4,7}$/i.test(value)))];
  const firstRemediation = f.remediation.map((step) =>
    typeof step === "string" ? step : step.description || step.title,
  ).find(Boolean);
  const customerImpact = f.businessImpact || f.impact || "Business impact has not been recorded. Validate asset criticality, exposure, and reachable attack paths before assigning impact.";

  return (
    <div className="animate-scale-in" style={{ background: "var(--bg-app)", border: "1px solid var(--border-subtle)", borderRadius: 8, overflow: "hidden" }}>

      {/* ── Header ── */}
      <div style={{ padding: "14px 18px", borderBottom: "1px solid var(--border-subtle)", background: `linear-gradient(135deg, ${SEV_COLOR[f.severity]}08 0%, transparent 60%)` }}>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 8, alignItems: "center" }}>
          <SevBadge s={f.severity} />
          <StatusBadge s={f.status} />
          <RiskBadge score={f.riskScore} />
          {f.kevStatusRecorded && f.kevListed && <KevBadge />}
          <span style={{
            fontFamily: "var(--font-mono)", fontSize: 9,
            color: pc, background: `${pc}15`, border: `1px solid ${pc}30`,
            borderRadius: 4, padding: "2px 6px", fontWeight: 700,
          }}>
            {f.aiTriage.priority}
          </span>
          <DetectionPill cov={f.detectionCoverage} />
          {f.exploitMaturityRecorded && (
            <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: MATURITY_COLOR[f.exploitMaturity], background: `${MATURITY_COLOR[f.exploitMaturity]}12`, border: `1px solid ${MATURITY_COLOR[f.exploitMaturity]}25`, borderRadius: 4, padding: "2px 6px" }}>
              {f.exploitMaturity}
            </span>
          )}
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: sla.color, background: `${sla.color}10`, border: `1px solid ${sla.color}25`, borderRadius: 4, padding: "2px 6px" }}>
            SLA {sla.label}
          </span>
          <button
            className="btn btn-secondary"
            onClick={() => explain(f.id)}
            aria-label="Explain this finding in plain English"
            style={{ marginLeft: "auto", height: 26, padding: "0 10px", fontSize: 11 }}
          >
            <Brain size={13} /> Explain &amp; remediate
          </button>
        </div>
        <h2 style={{ fontFamily: "'Inter', sans-serif", fontSize: 17, fontWeight: 700, color: "var(--text-primary)", margin: 0, lineHeight: 1.3 }}>{f.title}</h2>
        <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-secondary)", marginTop: 5 }}>
          {f.id} · {f.category} · {f.affectedHost}
          {f.assignee && <span style={{ color: "var(--accent)", marginLeft: 8 }}>@{f.assignee}</span>}
        </div>
        {cveIds.length > 0 && (
          <div className="finding-cve-list">{cveIds.map((cve) => <code key={cve}>{cve}</code>)}</div>
        )}

        {/* Risk breakdown bar */}
        <div style={{ marginTop: 10 }}>
          <RiskBreakdownBar breakdown={f.riskBreakdown} />
        </div>

        {/* Business impact */}
        {f.businessImpact && (
          <div style={{ marginTop: 10, padding: "7px 10px", background: `${SEV_COLOR[f.severity]}08`, border: `1px solid ${SEV_COLOR[f.severity]}18`, borderRadius: 5 }}>
            <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: SEV_COLOR[f.severity] }}>BUSINESS IMPACT</span>
            <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 12, color: "var(--text-primary)", marginTop: 3 }}>{f.businessImpact}</div>
          </div>
        )}
      </div>

      <section className="finding-customer-summary">
        <header><div><Shield size={15} /><span>Customer decision brief</span></div><small>Recorded data only</small></header>
        <div>
          <article><small>ORGANIZATIONAL IMPACT</small><p>{customerImpact}</p></article>
          <article><small>RECOMMENDED FIRST ACTION</small><p>{firstRemediation || "Assign an owner to validate the finding and record an approved remediation plan."}</p></article>
          <article><small>EVIDENCE CONFIDENCE</small><p>{f.evidence.length ? `${f.evidence.length} evidence artifact${f.evidence.length === 1 ? "" : "s"} recorded.` : "No structured evidence artifact is recorded."} {f.activelyExploited ? "Exploitation was validated." : "Exploitation is not validated."}</p></article>
          <article><small>ACCOUNTABILITY</small><p>{f.assignee ? `Assigned to ${f.assignee}.` : "No remediation owner is assigned."} SLA: {sla.label}.</p></article>
        </div>
      </section>

      {/* ── AI Triage Panel ── */}
      {hasAiTriage && <div style={{ padding: "10px 18px", borderBottom: "1px solid var(--border-subtle)", background: "rgba(37,99,235,0.03)" }}>
        <div style={{ display: "flex", gap: 6, alignItems: "flex-start" }}>
          <Brain size={13} color="var(--accent)" style={{ flexShrink: 0, marginTop: 1 }} />
          <div style={{ flex: 1 }}>
            <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 4 }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--accent)" }}>AI TRIAGE</span>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>
                {Math.round(f.aiTriage.confidence * 100)}% confidence
              </span>
            </div>
            <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 12, color: "var(--text-primary)", lineHeight: 1.5, marginBottom: 5 }}>{f.aiTriage.reasoning}</div>
            <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 12, color: "#059669", lineHeight: 1.5 }}>
              <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "#059669" }}>RECOMMEND: </span>
              {f.aiTriage.recommendation}
            </div>
          </div>
        </div>
      </div>}

      {/* ── Workflow ── */}
      <div style={{ padding: "8px 18px", borderBottom: "1px solid var(--border-subtle)", display: "flex", gap: 5, flexWrap: "wrap", alignItems: "center" }}>
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>ADVANCE:</span>
        {WORKFLOW.map((w) => (
          <button
            key={w.status}
            onClick={() => onStatusChange(f.id, w.status)}
            disabled={f.status === w.status || statusUpdating}
            aria-busy={statusUpdating}
            style={{
            padding: "3px 9px", borderRadius: 4, cursor: f.status === w.status || statusUpdating ? "default" : "pointer",
            border: `1px solid ${f.status === w.status ? "var(--border-subtle)" : `${w.color}45`}`,
            background: f.status === w.status ? "transparent" : `${w.color}10`,
            color: f.status === w.status ? "var(--text-secondary)" : w.color,
            fontFamily: "var(--font-mono)", fontSize: 9, opacity: f.status === w.status ? 0.5 : 1,
          }}>{w.label}</button>
        ))}
      </div>

      {/* ── Tabs ── */}
      <div style={{ display: "flex", borderBottom: "1px solid var(--border-subtle)", overflowX: "auto" }}>
        {(["overview", "intel", "evidence", "remediation", "compliance"] as const).map((t) => (
          <button key={t} onClick={() => setTab(t)} style={{
            padding: "8px 14px", background: tab === t ? "rgba(37,99,235,0.04)" : "transparent",
            border: "none", borderBottom: tab === t ? "2px solid var(--accent)" : "2px solid transparent",
            color: tab === t ? "var(--text-primary)" : "var(--text-secondary)",
            fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: 0.8,
            cursor: "pointer", textTransform: "uppercase", whiteSpace: "nowrap",
          }}>
            {t === "remediation" ? `Remediation (${f.remediation.length})` : t === "intel" ? "Threat Intel" : t}
          </button>
        ))}
      </div>

      <div style={{ padding: "16px 18px" }}>

        {/* Overview tab */}
        {tab === "overview" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 5 }}>DESCRIPTION</div>
              <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, color: "var(--text-primary)", lineHeight: 1.6, marginBottom: 14 }}>{f.description || "No finding description has been recorded."}</div>

              <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 8 }}>KILL CHAIN</div>
              {f.killChain.length ? <KillChainViz steps={f.killChain} /> : <div className="finding-data-missing">No kill-chain path has been recorded.</div>}

              {related.length > 0 && (
                <div style={{ marginTop: 14 }}>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 6 }}>
                    <Link2 size={10} style={{ display: "inline", marginRight: 4 }} />CORRELATED FINDINGS
                  </div>
                  {related.map((r) => (
                    <div key={r.id} style={{ display: "flex", gap: 6, alignItems: "center", padding: "5px 8px", background: "var(--bg-panel)", borderRadius: 4, marginBottom: 4 }}>
                      <div style={{ width: 6, height: 6, borderRadius: "50%", background: SEV_COLOR[r.severity], flexShrink: 0 }} />
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--accent)" }}>{r.id}</span>
                      <span style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-primary)", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{r.title}</span>
                      <RiskBadge score={r.riskScore} />
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 5 }}>TECHNICAL DETAILS</div>
              <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, color: "var(--text-primary)", lineHeight: 1.6, marginBottom: 12 }}>{f.technicalDetails || "No additional technical narrative has been recorded."}</div>

              <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 6 }}>MITRE ATT&CK</div>
              {!f.mitre.length && <div className="finding-data-missing">No MITRE ATT&amp;CK technique is mapped.</div>}
              {f.mitre.map((m) => (
                <div key={m.id} style={{ display: "flex", gap: 8, marginBottom: 4, alignItems: "center" }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--accent)", flexShrink: 0 }}>{m.id}</span>
                  <span style={{ fontFamily: "'Inter', sans-serif", fontSize: 12, color: "var(--text-secondary)" }}>{m.name}</span>
                </div>
              ))}

              <div style={{ marginTop: 12 }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 5 }}>CVSS VECTOR</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-primary)", background: "var(--bg-panel)", padding: "6px 10px", borderRadius: 4, wordBreak: "break-all", lineHeight: 1.5 }}>
                  {f.cvssVector || "Not recorded"}
                </div>
              </div>

              {f.tags && f.tags.length > 0 && (
                <div style={{ marginTop: 12 }}>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 5 }}>
                    <Tag size={9} style={{ display: "inline", marginRight: 4 }} />TAGS
                  </div>
                  <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
                    {f.tags.map((t) => (
                      <span key={t} style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", background: "var(--bg-panel)", border: "1px solid var(--border-subtle)", borderRadius: 3, padding: "1px 5px" }}>{t}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Threat Intel tab */}
        {tab === "intel" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            {/* Left: scores */}
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {/* EPSS */}
              <div style={{ background: "var(--bg-panel)", border: "1px solid var(--border-subtle)", borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 8 }}>
                  EPSS · EXPLOIT PREDICTION SCORING
                </div>
                {f.epssRecorded ? <EpssBar score={f.epssScore} percentile={f.epssPercentile} /> : <div className="finding-data-missing">EPSS enrichment is not recorded.</div>}
                <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-secondary)", marginTop: 8, lineHeight: 1.4 }}>
                  {f.epssRecorded ? f.epssScore > 0.5
                    ? `Top ${(100 - f.epssPercentile * 100).toFixed(1)}% most likely to be exploited in the next 30 days (FIRST.org model).`
                    : "Use EPSS as one prioritization signal; it does not prove exploitation."
                    : "Run vulnerability enrichment before using exploitation probability in a remediation decision."}
                </div>
              </div>

              {/* CISA KEV */}
              <div style={{ background: "var(--bg-panel)", border: `1px solid ${f.kevListed ? `${SEV_PALETTE.RED}33` : "var(--border-subtle)"}`, borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>CISA KEV STATUS</div>
                  {f.kevStatusRecorded && f.kevListed ? <KevBadge /> : f.kevStatusRecorded ? (
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "#64748B", background: "rgba(100,116,139,0.1)", border: "1px solid rgba(100,116,139,0.2)", borderRadius: 3, padding: "1px 5px" }}>NOT LISTED</span>
                  ) : <span className="badge badge-info">NOT ENRICHED</span>}
                </div>
                {f.kevListed && f.kevDateAdded && (
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: SEV_PALETTE.RED }}>Added {f.kevDateAdded}</div>
                )}
                <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-secondary)", marginTop: 6, lineHeight: 1.4 }}>
                  {f.kevStatusRecorded ? f.kevListed
                    ? "Actively exploited in the wild per CISA. Mandatory patching deadline applies to federal agencies. Treat as highest priority."
                    : "The recorded enrichment did not identify this CVE in CISA KEV."
                    : "CISA KEV status has not been recorded. Do not interpret missing enrichment as not listed."}
                </div>
              </div>

              {/* FP probability */}
              {f.fpProbabilityRecorded && <div style={{ background: "var(--bg-panel)", border: "1px solid var(--border-subtle)", borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 6 }}>FALSE POSITIVE PROBABILITY</div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div style={{ height: 4, flex: 1, background: "rgba(100,116,139,0.2)", borderRadius: 2, overflow: "hidden", marginRight: 10 }}>
                    <div style={{ height: "100%", width: `${f.fpProbability * 100}%`, background: f.fpProbability < 0.1 ? SEV_PALETTE.GREEN : f.fpProbability < 0.3 ? SEV_PALETTE.AMBER : SEV_PALETTE.RED, borderRadius: 2 }} />
                  </div>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: f.fpProbability < 0.1 ? SEV_PALETTE.GREEN : SEV_PALETTE.AMBER, fontWeight: 700, flexShrink: 0 }}>
                    {Math.round(f.fpProbability * 100)}%
                  </span>
                </div>
                <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-secondary)", marginTop: 5 }}>
                  {f.fpProbability < 0.1 ? "Very low FP probability — finding confirmed via exploitation evidence." : f.fpProbability < 0.3 ? "Moderate — correlate with additional evidence before closing." : "Elevated — validate before remediation investment."}
                </div>
              </div>}
            </div>

            {/* Right: exploit intel + detection */}
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {/* Exploit maturity */}
              {f.exploitMaturityRecorded && <div style={{ background: "var(--bg-panel)", border: `1px solid ${MATURITY_COLOR[f.exploitMaturity]}22`, borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 8 }}>EXPLOIT INTELLIGENCE</div>
                <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 8 }}>
                  <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                    <div style={{ width: 8, height: 8, borderRadius: "50%", background: MATURITY_COLOR[f.exploitMaturity], boxShadow: `0 0 6px ${MATURITY_COLOR[f.exploitMaturity]}` }} />
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: MATURITY_COLOR[f.exploitMaturity] }}>{f.exploitMaturity}</span>
                  </div>
                  {f.pocAvailable && (
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: SEV_PALETTE.ORANGE, background: `${SEV_PALETTE.ORANGE}14`, border: `1px solid ${SEV_PALETTE.ORANGE}33`, borderRadius: 3, padding: "1px 5px" }}>
                      PoC PUBLIC
                    </span>
                  )}
                  {f.activelyExploited && (
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: SEV_PALETTE.RED, background: `${SEV_PALETTE.RED}14`, border: `1px solid ${SEV_PALETTE.RED}40`, borderRadius: 3, padding: "1px 5px" }}>
                      ACTIVE EXPLOITATION
                    </span>
                  )}
                </div>
                <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.4 }}>
                  {f.exploitMaturity === "WEAPONIZED"
                    ? "Weaponized exploit available in public toolchains (Metasploit/Sliver/Cobalt Strike). Exploitation is trivial for any attacker."
                    : f.exploitMaturity === "POC"
                    ? "Proof-of-concept code publicly available. Requires adaptation for production exploit but significantly lowers attacker barrier."
                    : "No public exploit code. Theoretical attack path — requires custom exploit development."}
                </div>
              </div>}

              {/* Detection coverage */}
              <div style={{ background: "var(--bg-panel)", border: `1px solid ${COVERAGE_COLOR[f.detectionCoverage]}22`, borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>DETECTION COVERAGE</div>
                  <DetectionPill cov={f.detectionCoverage} />
                </div>
                {f.detectionNote && (
                  <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.4, marginBottom: 8 }}>{f.detectionNote}</div>
                )}
                <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                  {f.mitre.map((m) => (
                    <div key={m.id} style={{ display: "flex", gap: 6, alignItems: "center", padding: "3px 6px", background: "var(--bg-app)", borderRadius: 3 }}>
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--accent)", flexShrink: 0 }}>{m.id}</span>
                      <span style={{ fontFamily: "'Inter', sans-serif", fontSize: 10, color: "var(--text-secondary)", flex: 1 }}>{m.name}</span>
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: COVERAGE_COLOR[f.detectionCoverage] }}>
                        {f.detectionCoverage}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Risk score context */}
              <div style={{ background: "var(--bg-panel)", border: "1px solid var(--border-subtle)", borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 6 }}>COMPOSITE RISK SCORE</div>
                <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 8 }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 28, fontWeight: 800, color: riskScoreColor(f.riskScore) }}>{f.riskScore}</span>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-secondary)" }}>/ 1000</span>
                </div>
                <div style={{ height: 6, background: "rgba(100,116,139,0.2)", borderRadius: 3, overflow: "hidden" }}>
                  <div style={{ height: "100%", width: `${f.riskScore / 10}%`, background: riskScoreColor(f.riskScore), borderRadius: 3 }} />
                </div>
                <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 11, color: "var(--text-secondary)", marginTop: 6 }}>
                  Composite score from the available finding signals. When enrichment is missing, Vedha uses the recorded CVSS-derived fallback.
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Evidence tab */}
        {tab === "evidence" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {!f.evidence.length && <div className="finding-data-missing finding-data-missing-large">No structured evidence is recorded. Validate the finding and attach reproducible proof before client delivery.</div>}
            {f.evidence.map((e, i) => (
              <div key={i} style={{ background: "var(--bg-app)", border: "1px solid var(--border-subtle)", borderRadius: 6, overflow: "hidden" }}>
                <div style={{ padding: "7px 12px", borderBottom: "1px solid var(--border-subtle)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-secondary)" }}>{e.label}</span>
                  <CopyBtn text={e.content} />
                </div>
                <pre style={{ margin: 0, padding: "12px", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-primary)", whiteSpace: "pre-wrap", wordBreak: "break-word", lineHeight: 1.6, maxHeight: 250, overflow: "auto" }}>
                  {e.content}
                </pre>
              </div>
            ))}
          </div>
        )}

        {/* Remediation tab */}
        {tab === "remediation" && (
          <div>
            {!f.remediation.length ? (
              <div className="finding-data-missing finding-data-missing-large">
                No remediation plan is recorded. Assign an owner, validate the vendor-supported fix, define rollback, and document retest evidence.
              </div>
            ) : (
              <>
                {f.remediation.some((step) => typeof step !== "string") && (
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--text-secondary)" }}>
                      {f.remediation.filter((step) => typeof step !== "string" && step.completed).length} structured steps completed
                    </span>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: SEV_PALETTE.AMBER }}>
                      {f.remediation.reduce((hours, step) => hours + (typeof step !== "string" ? step.estimatedHours : 0), 0)}h recorded estimate
                    </span>
                  </div>
                )}
                <RemediationChecklist steps={f.remediation} />
              </>
            )}
          </div>
        )}

        {/* Compliance tab */}
        {tab === "compliance" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {!f.compliance.length && <div className="finding-data-missing finding-data-missing-large">No compliance control mapping is recorded. Do not infer a control failure without an approved framework scope and test procedure.</div>}
            {f.compliance.map((c, i) => (
              <div key={i} style={{ background: "var(--bg-app)", border: "1px solid var(--border-subtle)", borderRadius: 6, padding: "10px 14px" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--accent)", marginBottom: 7 }}>{c.framework}</div>
                <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
                  {c.refs.map((r, j) => (
                    <div key={j} style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, color: "var(--text-primary)", lineHeight: 1.4 }}>· {r}</div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

/* ─── Fix-First Priority Queue (decision-first hero) ─── */
function isUrgent(f: Finding): boolean {
  if (f.status !== "OPEN" && f.status !== "CONFIRMED") return false;
  const breached = getSlaColor(f.discoveredAt, f.severity).label === "BREACHED";
  return f.activelyExploited || (f.kevStatusRecorded && f.kevListed) || breached || f.severity === "CRITICAL";
}

function urgencyReasons(f: Finding): string[] {
  const r: string[] = [];
  if (f.activelyExploited) r.push("Actively exploited");
  if (f.kevStatusRecorded && f.kevListed) r.push("CISA KEV");
  const sla = getSlaColor(f.discoveredAt, f.severity);
  if (sla.label === "BREACHED") r.push("SLA breached");
  else if (sla.pct < 25) r.push(`SLA ${sla.label}`);
  if (f.severity === "CRITICAL") r.push("Critical");
  return r;
}

function FixFirstStrip({ findings, onSelect, exploitedActive, slaActive, onToggleExploited, onToggleSla }: {
  findings: Finding[]; onSelect: (id: string) => void;
  exploitedActive: boolean; slaActive: boolean; onToggleExploited: () => void; onToggleSla: () => void;
}) {
  const open = findings.filter((f) => f.status === "OPEN" || f.status === "CONFIRMED");
  const urgent = open.filter(isUrgent).sort((a, b) => {
    if (a.activelyExploited !== b.activelyExploited) return a.activelyExploited ? -1 : 1;
    return b.riskScore - a.riskScore;
  });
  const openRisk = open.reduce((s, f) => s + f.riskScore, 0);
  const slaBreached = open.filter((f) => getSlaColor(f.discoveredAt, f.severity).label === "BREACHED").length;
  const activeCount = open.filter((f) => f.activelyExploited).length;
  const sev = (["CRITICAL", "HIGH", "MEDIUM", "LOW"] as Severity[]).map((s) => ({ s, n: open.filter((f) => f.severity === s).length }));
  const totalOpen = Math.max(1, open.length);
  const accent = urgent.length === 0 ? SEV_PALETTE.GREEN : (activeCount > 0 || slaBreached > 0) ? SEV_PALETTE.RED : SEV_PALETTE.ORANGE;

  return (
    <div className="animate-fade-up" style={{
      background: "var(--bg-panel)", border: "1px solid var(--border-subtle)", borderTop: `2px solid ${accent}`,
      borderRadius: 10, padding: "16px 18px", marginBottom: 16, boxShadow: "var(--shadow-sm)",
    }}>
      {/* Header: the answer + posture */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 16, marginBottom: urgent.length ? 14 : 0 }}>
        <div>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, letterSpacing: 1.4, color: "var(--text-secondary)", textTransform: "uppercase" }}>Current page triage</span>
          <div style={{ display: "flex", alignItems: "baseline", gap: 9, marginTop: 4 }}>
            <span style={{ fontFamily: "var(--font-display)", fontSize: 30, fontWeight: 800, color: accent, lineHeight: 1 }}>{urgent.length}</span>
            <span style={{ fontFamily: "var(--font-body)", fontSize: 14, color: "var(--text-primary)", fontWeight: 600 }}>
              {urgent.length === 0 ? "all clear — nothing needs immediate action" : `${urgent.length === 1 ? "finding needs" : "findings need"} action now`}
            </span>
          </div>
        </div>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-start", flexWrap: "wrap" }}>
          {[
            { label: "ACTIVELY EXPLOITED", value: activeCount, color: activeCount ? SEV_PALETTE.RED : "var(--text-secondary)", active: exploitedActive, onClick: onToggleExploited },
            { label: "SLA BREACHED", value: slaBreached, color: slaBreached ? SEV_PALETTE.RED : "var(--text-secondary)", active: slaActive, onClick: onToggleSla },
            { label: "OPEN RISK", value: openRisk.toLocaleString(), color: "var(--text-primary)", active: false, onClick: undefined as (() => void) | undefined },
          ].map((m) => {
            const inner = (
              <>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 20, fontWeight: 700, color: m.color, lineHeight: 1 }}>{m.value}</div>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginTop: 3, letterSpacing: 0.4 }}>{m.label}</div>
              </>
            );
            return m.onClick ? (
              <button key={m.label} onClick={m.onClick} aria-pressed={m.active} aria-label={`Filter list by ${m.label.toLowerCase()}`} title="Click to filter the list"
                style={{ textAlign: "right", cursor: "pointer", background: m.active ? "var(--accent-ghost)" : "transparent",
                  border: m.active ? "1px solid var(--border-accent)" : "1px solid transparent", borderRadius: 6, padding: "4px 8px" }}>
                {inner}
              </button>
            ) : (
              <div key={m.label} style={{ textAlign: "right", padding: "4px 8px" }}>{inner}</div>
            );
          })}
          <div style={{ width: 128 }}>
            <div style={{ height: 8, display: "flex", borderRadius: 4, overflow: "hidden", background: "var(--bg-app)" }}>
              {sev.map(({ s, n }) => n > 0 ? (
                <div key={s} style={{ width: `${(n / totalOpen) * 100}%`, background: SEV_COLOR[s] }} title={`${s}: ${n}`} />
              ) : null)}
            </div>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginTop: 4, textAlign: "right" }}>{open.length} open by severity</div>
          </div>
        </div>
      </div>

      {/* Top urgent findings — one-glance justification + direct triage */}
      {urgent.length > 0 && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(258px, 1fr))", gap: 10 }}>
          {urgent.slice(0, 3).map((f) => (
            <button key={f.id} onClick={() => onSelect(f.id)} className="card-hover" style={{
              textAlign: "left", cursor: "pointer", background: "var(--bg-app)", border: "1px solid var(--border-subtle)",
              borderLeft: `3px solid ${SEV_COLOR[f.severity]}`, borderRadius: 8, padding: "10px 12px",
              display: "flex", flexDirection: "column", gap: 7,
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
                <span style={{ fontFamily: "var(--font-body)", fontSize: 13, fontWeight: 600, color: "var(--text-primary)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{f.title}</span>
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, fontWeight: 700, color: riskScoreColor(f.riskScore), flexShrink: 0 }}>{f.riskScore}</span>
              </div>
              <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
                {urgencyReasons(f).map((r) => (
                  <span key={r} style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: SEV_PALETTE.RED, background: `${SEV_PALETTE.RED}12`, border: `1px solid ${SEV_PALETTE.RED}30`, borderRadius: 3, padding: "1px 6px" }}>{r}</span>
                ))}
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{f.affectedHost}</span>
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--accent)", fontWeight: 600, flexShrink: 0 }}>Triage →</span>
              </div>
            </button>
          ))}
          {urgent.length > 3 && (
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-secondary)", border: "1px dashed var(--border-subtle)", borderRadius: 8, padding: 10 }}>
              +{urgent.length - 3} more urgent
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/* ─── Main Page ─── */
export default function FindingsPage() {
  const { success, error: showError } = useToast();
  const queryClient = useQueryClient();
  const locationSearch = useSyncExternalStore(
    subscribeToLocationChange,
    getLocationSearch,
    getServerLocationSearch,
  );
  const deepLinkParams = new URLSearchParams(locationSearch);
  const [selectedOverride, setSelectedId] = useState<string | null | undefined>();
  const selectedId = selectedOverride === undefined
    ? deepLinkParams.get("finding")
    : selectedOverride;
  const [search, setSearch] = useState("");
  const deferredSearch = useDeferredValue(search.trim());
  const [filterSev, setFilterSev] = useState<Severity | "ALL">("ALL");
  const [filterStatus, setFilterStatus] = useState<FindingStatus | "ALL">("ALL");
  const [sortBy, setSortBy] = useState<"risk" | "cvss" | "epss" | "date">("risk");
  const [filterBlind, setFilterBlind] = useState(false);
  const [filterExploited, setFilterExploited] = useState(false);
  const [filterSlaBreached, setFilterSlaBreached] = useState(false);
  const [page, setPage] = useState(1);
  const [engagementOverride, setEngagementId] = useState<string | null | undefined>();
  // URL state is an external store. Local overrides let the operator clear a
  // deep link without an effect-driven render cascade.
  const engagementId = engagementOverride === undefined
    ? deepLinkParams.get("engagement")
    : engagementOverride;

  const queryString = new URLSearchParams({
    paginated: "true",
    page: String(page),
    page_size: String(FINDINGS_PER_PAGE),
    sort: sortBy,
  });
  if (deferredSearch) queryString.set("search", deferredSearch);
  if (filterSev !== "ALL") queryString.set("severity", filterSev);
  if (filterStatus !== "ALL") queryString.set("status", filterStatus);
  if (filterBlind) queryString.set("blind", "true");
  if (filterExploited) queryString.set("validated", "true");
  if (filterSlaBreached) queryString.set("sla_breached", "true");
  if (engagementId) queryString.set("engagement_id", engagementId);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: [
      "findings-page", page, deferredSearch, filterSev, filterStatus,
      filterBlind, filterExploited, filterSlaBreached, sortBy, engagementId,
    ],
    queryFn: () => fetchJson<FindingPage>(`/api/findings?${queryString}`),
    refetchInterval: 30_000,
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });
  const summaryQuery = useQuery({
    queryKey: ["findings-summary", engagementId],
    queryFn: () => fetchJson<FindingSummary>(
      `/api/findings/summary${engagementId ? `?engagement_id=${encodeURIComponent(engagementId)}` : ""}`,
    ),
    refetchInterval: 30_000,
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });
  const findings = data?.items ?? [];
  const total = data?.total ?? 0;
  const pageCount = data?.pages ?? 1;
  const currentPage = data?.page ?? page;
  const stats = summaryQuery.data ?? {
    total: 0,
    criticalOpen: 0,
    validated: 0,
    blind: 0,
    averageRisk: 0,
  };

  // Engagement context (for the scoped banner) + robust detail: if the selected
  // finding isn't on the current page (deep link, or another page), fetch it by id.
  const engagementQuery = useQuery({
    queryKey: ["engagement-name", engagementId],
    queryFn: () => fetchJson<{ engagement?: { name?: string } }>(`/api/engagements/${engagementId}`),
    enabled: Boolean(engagementId),
    retry: false,
  });
  const inCurrentPage = findings.find((f) => f.id === selectedId) ?? null;
  const detailQuery = useQuery({
    queryKey: ["finding-detail", selectedId],
    queryFn: () => fetchJson<Finding>(`/api/findings/${selectedId}`),
    enabled: Boolean(selectedId) && !inCurrentPage,
    retry: false,
  });

  const statusMutation = useMutation({
    mutationFn: ({ id, status }: { id: string; status: FindingStatus }) =>
      fetchJson<Finding>(`/api/findings/${id}`, {
        method: "PUT",
        body: JSON.stringify({ status }),
      }),
    onError: (mutationError) => showError("Status update failed", errorMessage(mutationError)),
    onSuccess: (updated) => {
      success("Status updated", `${updated.id} → ${STATUS_LABEL[updated.status]}`);
    },
    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: ["findings-page"] });
      void queryClient.invalidateQueries({ queryKey: ["findings-summary"] });
    },
  });

  const handleStatusChange = useCallback((id: string, newStatus: FindingStatus) => {
    statusMutation.mutate({ id, status: newStatus });
  }, [statusMutation]);

  const selected = inCurrentPage ?? detailQuery.data ?? null;
  const hasActiveFilters = Boolean(
    search.trim()
    || filterSev !== "ALL"
    || filterStatus !== "ALL"
    || filterBlind
    || filterExploited
    || filterSlaBreached,
  );

  return (
    <PageShell
      title="FINDINGS"
      subtitle="VAPT · THREAT INTEL · TRIAGE · REMEDIATION"
      statusItems={[
        { label: "CRITICAL OPEN", value: String(stats.criticalOpen), color: SEV_PALETTE.RED },
        { label: "VALIDATED",     value: String(stats.validated),    color: SEV_PALETTE.ORANGE },
        { label: "BLIND DETECT",  value: String(stats.blind),      color: SEV_PALETTE.AMBER },
        { label: "AVG RISK",      value: String(stats.averageRisk), color: riskScoreColor(stats.averageRisk) },
      ]}
    >
      {engagementId && (
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, flexWrap: "wrap", marginBottom: 12, padding: "10px 14px", background: "var(--accent-ghost)", border: "0.5px solid var(--border-accent)", borderRadius: 8 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13, color: "var(--text-primary)", flexWrap: "wrap" }}>
            <Link2 size={14} color="var(--accent)" />
            <span>Scoped to engagement <b>{engagementQuery.data?.engagement?.name ?? `${engagementId.slice(0, 8)}…`}</b> — {total} finding{total === 1 ? "" : "s"}</span>
            <Link href={`/engagements/${engagementId}`} style={{ color: "var(--accent)", fontSize: 12, textDecoration: "none" }}>← open engagement</Link>
          </div>
          <button className="btn btn-ghost" style={{ height: 28, fontSize: 12 }}
            onClick={() => { setEngagementId(null); setPage(1); setSelectedId(null); if (typeof window !== "undefined") window.history.replaceState(null, "", "/findings"); }}>
            View all findings
          </button>
        </div>
      )}

      <FixFirstStrip
        findings={findings}
        onSelect={(id) => setSelectedId(id)}
        exploitedActive={filterExploited}
        slaActive={filterSlaBreached}
        onToggleExploited={() => { setFilterExploited((p) => !p); setPage(1); }}
        onToggleSla={() => { setFilterSlaBreached((p) => !p); setPage(1); }}
      />

      <div style={{ display: "grid", gridTemplateColumns: selected ? "380px 1fr" : "1fr", gap: 16 }}>

        {/* ── Left: List ── */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>

          {/* Filters */}
          <div style={{ background: "var(--bg-app)", border: "1px solid var(--border-subtle)", borderRadius: 6, padding: "10px 12px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8, background: "var(--bg-panel)", border: "1px solid var(--border-subtle)", borderRadius: 4, padding: "5px 10px" }}>
              <Search size={11} color="#64748B" />
              <input value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); setSelectedId(null); }} placeholder="Search title, CVE, or finding ID…"
                aria-label="Search findings"
                style={{ background: "none", border: "none", outline: "none", color: "var(--text-primary)", fontFamily: "var(--font-mono)", fontSize: 11, width: "100%" }}
              />
            </div>

            {/* Severity filter */}
            <div style={{ display: "flex", gap: 4, flexWrap: "wrap", marginBottom: 6 }}>
              {(["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"] as const).map((s) => (
                <button key={s} aria-pressed={filterSev === s} onClick={() => { setFilterSev(s); setPage(1); setSelectedId(null); }} style={{
                  padding: "3px 8px", borderRadius: 3, cursor: "pointer", fontFamily: "var(--font-mono)", fontSize: 9,
                  border: `1px solid ${filterSev === s ? (s === "ALL" ? "var(--accent)" : SEV_COLOR[s as Severity]) : "var(--border-subtle)"}`,
                  background: filterSev === s ? (s === "ALL" ? "rgba(37,99,235,0.1)" : `${SEV_COLOR[s as Severity]}15`) : "transparent",
                  color: filterSev === s ? (s === "ALL" ? "var(--accent)" : SEV_COLOR[s as Severity]) : "var(--text-secondary)",
                }}>{s}</button>
              ))}
            </div>

            {/* Quick filters row */}
            <div style={{ display: "flex", gap: 6, alignItems: "center", flexWrap: "wrap" }}>
              <select value={filterStatus} onChange={(e) => { setFilterStatus(e.target.value as FindingStatus | "ALL"); setPage(1); setSelectedId(null); }}
                aria-label="Filter findings by status"
                style={{ background: "var(--bg-panel)", border: "1px solid var(--border-subtle)", borderRadius: 4, color: "var(--text-secondary)", fontFamily: "var(--font-mono)", fontSize: 10, padding: "3px 6px", outline: "none" }}>
                {["ALL", "OPEN", "CONFIRMED", "REMEDIATED", "ACCEPTED", "FALSE_POSITIVE"].map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
              <button aria-pressed={filterExploited} onClick={() => { setFilterExploited((p) => !p); setPage(1); setSelectedId(null); }} style={{
                padding: "3px 8px", borderRadius: 3, cursor: "pointer", fontFamily: "var(--font-mono)", fontSize: 9,
                border: `1px solid ${filterExploited ? `${SEV_PALETTE.RED}66` : "var(--border-subtle)"}`,
                background: filterExploited ? `${SEV_PALETTE.RED}14` : "transparent",
                color: filterExploited ? SEV_PALETTE.RED : "var(--text-secondary)",
              }}>✓ VALIDATED</button>
              <button aria-pressed={filterBlind} onClick={() => { setFilterBlind((p) => !p); setPage(1); setSelectedId(null); }} style={{
                padding: "3px 8px", borderRadius: 3, cursor: "pointer", fontFamily: "var(--font-mono)", fontSize: 9,
                border: `1px solid ${filterBlind ? `${SEV_PALETTE.RED}66` : "var(--border-subtle)"}`,
                background: filterBlind ? `${SEV_PALETTE.RED}14` : "transparent",
                color: filterBlind ? SEV_PALETTE.RED : "var(--text-secondary)",
              }}>○ BLIND</button>
              <button onClick={() => { setSortBy(sortBy === "risk" ? "cvss" : sortBy === "cvss" ? "epss" : sortBy === "epss" ? "date" : "risk"); setPage(1); setSelectedId(null); }}
                aria-label={`Sort findings by ${sortBy}; activate to change sort`}
                style={{ display: "flex", alignItems: "center", gap: 4, padding: "3px 8px", background: "transparent", border: "1px solid var(--border-subtle)", borderRadius: 4, color: "var(--text-secondary)", cursor: "pointer", fontFamily: "var(--font-mono)", fontSize: 9 }}>
                <ArrowUpDown size={9} /> {sortBy.toUpperCase()}
              </button>
            </div>
          </div>

          {/* Finding list */}
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <DataState
              loading={isLoading}
              error={error}
              isEmpty={findings.length === 0}
              onRetry={() => refetch()}
              skeleton={<SkeletonRows rows={6} height={92} />}
              empty={
                <EmptyState
                  icon={Shield}
                  title={hasActiveFilters ? "No findings match these filters" : "No findings yet"}
                  hint={hasActiveFilters
                    ? "Change or clear a filter to widen the result set."
                    : "Run a vulnerability scan on an in-scope target — findings appear here, ranked by risk."}
                />
              }
            >
            {findings.map((f) => {
              const sla = getSlaColor(f.discoveredAt, f.severity);
              const isSelected = selectedId === f.id;
              const pc = PRIORITY_COLOR[f.aiTriage.priority];
              return (
                <div
                  key={f.id}
                  className="card-hover stagger-item"
                  role="button"
                  tabIndex={0}
                  aria-expanded={isSelected}
                  onClick={() => setSelectedId(isSelected ? null : f.id)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") {
                      event.preventDefault();
                      setSelectedId(isSelected ? null : f.id);
                    }
                  }}
                  style={{
                    background: isSelected ? "rgba(37,99,235,0.03)" : "var(--bg-app)",
                    border: `1px solid ${isSelected ? "var(--accent)" : "var(--border-subtle)"}`,
                    borderLeft: `3px solid ${SEV_COLOR[f.severity]}`,
                    borderRadius: 6, padding: "10px 12px", cursor: "pointer",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 5 }}>
                    <div style={{ display: "flex", gap: 5, flexWrap: "wrap", flex: 1, alignItems: "center" }}>
                      <SevBadge s={f.severity} />
                      <StatusBadge s={f.status} />
                      {f.kevStatusRecorded && f.kevListed && <KevBadge />}
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: pc, background: `${pc}12`, border: `1px solid ${pc}25`, borderRadius: 3, padding: "1px 4px" }}>{f.aiTriage.priority}</span>
                    </div>
                    <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 2, flexShrink: 0 }}>
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, fontWeight: 700, color: riskScoreColor(f.riskScore) }}>{f.riskScore}</span>
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: "var(--text-secondary)" }}>RISK</span>
                    </div>
                  </div>

                  <div style={{ fontFamily: "'Inter', sans-serif", fontSize: 13, fontWeight: 600, color: "var(--text-primary)", lineHeight: 1.3, marginBottom: 5 }}>
                    {f.title}
                  </div>

                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 5 }}>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>{f.affectedHost}</span>
                    <div style={{ display: "flex", gap: 5, alignItems: "center" }}>
                      <DetectionPill cov={f.detectionCoverage} />
                      {f.exploitMaturityRecorded && <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: MATURITY_COLOR[f.exploitMaturity] }}>{f.exploitMaturity}</span>}
                    </div>
                  </div>

                  {/* EPSS mini */}
                  <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 4 }}>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>EPSS</span>
                    <div style={{ flex: 1, height: 3, background: "rgba(100,116,139,0.15)", borderRadius: 2, overflow: "hidden" }}>
                      <div style={{ height: "100%", width: `${f.epssScore * 100}%`, background: epssColor(f.epssScore), borderRadius: 2 }} />
                    </div>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>{(f.epssScore * 100).toFixed(0)}%</span>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: SEV_PALETTE.ORANGE }}>CVSS {f.cvss}</span>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: sla.color }}>{sla.label}</span>
                  </div>

                  {/* Risk bar */}
                  <div style={{ height: 2, background: "rgba(100,116,139,0.15)", borderRadius: 1, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: `${f.riskScore / 10}%`, background: riskScoreColor(f.riskScore), borderRadius: 1 }} />
                  </div>
                </div>
              );
            })}

            </DataState>
          </div>

          {total > 0 && (
            <nav className="findings-pagination" aria-label="Findings pagination">
              <div>
                Showing <strong>{(currentPage - 1) * FINDINGS_PER_PAGE + 1}</strong>–
                <strong>{Math.min(currentPage * FINDINGS_PER_PAGE, total)}</strong> of{" "}
                <strong>{total}</strong>
              </div>
              <span>20 per page</span>
              <div className="findings-pagination-controls">
                <button
                  type="button"
                  onClick={() => { setSelectedId(null); setPage((current) => Math.max(1, current - 1)); }}
                  disabled={currentPage === 1}
                  aria-label="Previous findings page"
                >
                  <ChevronLeft size={14} />
                </button>
                <span>Page {currentPage} of {pageCount}</span>
                <button
                  type="button"
                  onClick={() => { setSelectedId(null); setPage((current) => Math.min(pageCount, current + 1)); }}
                  disabled={currentPage === pageCount}
                  aria-label="Next findings page"
                >
                  <ChevronRight size={14} />
                </button>
              </div>
            </nav>
          )}
        </div>

        {/* ── Right: Detail ── */}
        {selected && (
          <div style={{ minWidth: 0 }}>
            <FindingDetail
              f={selected}
              allFindings={findings}
              onStatusChange={handleStatusChange}
              statusUpdating={statusMutation.isPending}
            />
          </div>
        )}
      </div>
    </PageShell>
  );
}
