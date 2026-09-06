"use client";

import React, { useState, useCallback, useDeferredValue, useSyncExternalStore } from "react";
import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Copy, Check, Search, CheckCircle, Shield,
  AlertTriangle, BadgeCheck, ChevronDown, ChevronLeft, ChevronRight,
  EyeOff, Flag, Link2, LoaderCircle, RefreshCw, RotateCcw, Brain, Tag,
  FileText, Terminal, Wrench, X,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { useAssistant } from "../../components/assistant/AssistantProvider";
import { useToast } from "../../hooks/useToast";
import { errorMessage, fetchJson, isUnauthorized } from "../../lib/fetcher";
import { DataState, SkeletonRows, EmptyState } from "../../components/states/DataState";
import { presentEvidence, type EvidenceArtifact } from "../../lib/evidence-presentation";
import {
  SEV_COLOR, STATUS_COLOR, STATUS_LABEL, MATURITY_COLOR, COVERAGE_COLOR,
  PRIORITY_COLOR, PRIORITY_LABEL, KILL_CHAIN_PHASE_COLOR, riskScoreColor, epssColor, SEV_PALETTE,
} from "../../lib/severity";

/* ─── Types ─── */
type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";
type FindingStatus = "OPEN" | "CONFIRMED" | "REMEDIATED" | "ACCEPTED" | "FALSE_POSITIVE";
type ExploitMaturity = "WEAPONIZED" | "POC" | "THEORETICAL";
type DetectionCoverage = "COVERED" | "PARTIAL" | "BLIND";
type Priority = "P0" | "P1" | "P2" | "P3" | "P4" | "P5";
const FINDINGS_PER_PAGE = 20;
const AGENT_REFRESH_FEEDBACK_MS = 2_000;

/* Lifecycle audit-trail event (backend /api/findings/{id}/events, snake_case). */
type TimelineEvent = {
  id: string | null;
  event_type: string;
  label: string;
  actor: string | null;
  actor_type: string;
  from_status: string | null;
  to_status: string | null;
  detail: Record<string, unknown> | null;
  occurred_at: string;
  synthesized: boolean;
};
type FindingTimeline = { finding_id: string; events: TimelineEvent[] };

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
type RemediationOs = "generic" | "linux" | "windows" | "macos";
interface RemediationPlanStep {
  step: number;
  title: string;
  description: string;
  commands?: Record<string, string[]>;
  commands_for_os: string[];
  verification: string;
  risk: "low" | "medium" | "high";
  unsafe_commands_removed?: boolean;
}
interface RemediationPlanResponse {
  finding_id: string;
  os: RemediationOs;
  source: string;
  reviewed: boolean;
  cached: boolean;
  generated_at: string | null;
  model: string | null;
  plan: {
    category: string;
    os: RemediationOs;
    source: string;
    summary: string;
    effort: "low" | "medium" | "high";
    remediation_risk: "low" | "medium" | "high";
    steps: RemediationPlanStep[];
    verification: string[];
    long_term_recommendations: string[];
    compensating_controls: string;
  };
}
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
  evidence: EvidenceArtifact[];
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
  aiTriage: { priority: Priority; reasoning: string; recommendation: string; confidence: number };
  // ── P2/P4 verification + lifecycle ──
  verificationState?: string | null;
  verificationConfidence?: number | null;
  verificationRationale?: string | null;
  needsReview?: boolean;
  riskRank?: number | null;
  resolutionMethod?: string | null;
  reopenedCount?: number;
  resolvedAt?: string | null;
  lastSeen?: string | null;
  regression?: boolean;
  assetContext?: {
    id: string;
    ipAddress: string | null;
    hostname: string | null;
    fqdn: string | null;
    os: string | null;
    osVersion: string | null;
    assetType: string;
    criticality: string;
    owner: string | null;
    environment: string | null;
  } | null;
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

interface EngagementOption {
  id: string;
  name: string;
}

interface VedhaAgentOption {
  id: string;
  name: string;
  status: "ONLINE" | "BUSY" | "OFFLINE";
}

/* ─── Color Maps ─── */
// Semantic colors now come from the shared, WCAG-AA source of truth (lib/severity).
const tint = (color: string, strength: number) =>
  `color-mix(in srgb, ${color} ${strength}%, transparent)`;

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
function CopyBtn({ text, showLabel = false }: { text: string; showLabel?: boolean }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      type="button"
      aria-label={copied ? "Copied" : "Copy"}
      onClick={() => { navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 2000); }}
      className={showLabel ? "finding-evidence-copy" : undefined}
      style={showLabel ? undefined : { background: "none", border: "none", cursor: "pointer", color: copied ? "var(--nominal-color)" : "var(--text-muted)", padding: "2px 4px" }}>
      {copied ? <Check size={12} /> : <Copy size={12} />}
      {showLabel && <span>{copied ? "Copied" : "Copy"}</span>}
    </button>
  );
}

/* ─── Severity Badge ─── */
function SevBadge({ s }: { s: Severity }) {
  const token = s.toLowerCase();
  return (
    <span style={{
      fontFamily: "var(--font-mono)", fontSize: 10, padding: "2px 8px", borderRadius: 4,
      background: `var(--badge-${token}-bg)`, color: `var(--badge-${token}-text)`,
      border: `1px solid var(--badge-${token}-edge)`, fontWeight: 750,
    }}>{s}</span>
  );
}

/* Priority is response order, not technical severity. Always render the plain
 * language meaning so the P-code is never a color-only or acronym-only signal. */
function PriorityBadge({ priority, compact = false }: { priority: Priority; compact?: boolean }) {
  const color = PRIORITY_COLOR[priority];
  const label = PRIORITY_LABEL[priority];
  return (
    <span
      title={`${priority}: ${label} response priority`}
      style={{
        display: "inline-flex", alignItems: "center", gap: 4,
        fontFamily: "var(--font-ui)", fontSize: compact ? 9 : 10,
        padding: compact ? "2px 6px" : "3px 8px", borderRadius: 999,
        background: `color-mix(in srgb, ${color} 10%, transparent)`,
        color, border: `var(--hairline) solid color-mix(in srgb, ${color} 35%, transparent)`,
        fontWeight: 700, whiteSpace: "nowrap",
      }}
    >
      <span style={{ fontFamily: "var(--font-mono)" }}>{priority}</span>
      <span aria-hidden>·</span>
      <span>{label}</span>
    </span>
  );
}

/* ─── Risk Score Badge ─── */
function RiskBadge({ score }: { score: number }) {
  const c = riskScoreColor(score);
  return (
    <span style={{
      fontFamily: "var(--font-mono)", fontSize: 10, padding: "2px 8px", borderRadius: 4,
      background: tint(c, 8), color: c, border: `1px solid ${tint(c, 19)}`, fontWeight: 700,
    }}>
      RISK {score}/1000
    </span>
  );
}

/* ─── KEV Badge ─── */
function KevBadge() {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4,
      fontFamily: "var(--font-mono)", fontSize: 9, padding: "2px 6px", borderRadius: 4,
      background: tint(SEV_PALETTE.RED, 8), color: SEV_PALETTE.RED, border: `1px solid ${tint(SEV_PALETTE.RED, 33)}`,
      fontWeight: 700, letterSpacing: 0.5,
    }}>
      <AlertTriangle size={10} aria-hidden /> KEV
    </span>
  );
}

/* ─── Needs-review chip ─── */
function NeedsReviewChip({ show }: { show?: boolean }) {
  if (!show) return null;
  return (
    <span title="High-stakes + uncertain — flagged for an analyst" style={{
      fontFamily: "var(--font-mono)", fontSize: 9, padding: "2px 6px", borderRadius: 4,
      background: tint(SEV_PALETTE.AMBER, 8), color: SEV_PALETTE.AMBER,
      border: `1px solid ${tint(SEV_PALETTE.AMBER, 25)}`, fontWeight: 700,
    }}>NEEDS REVIEW</span>
  );
}

/* ─── Status Badge ─── */
function StatusBadge({ s, onClick }: { s: FindingStatus; onClick?: () => void }) {
  return (
    <span onClick={onClick} style={{
      fontFamily: "var(--font-mono)", fontSize: 10, padding: "2px 8px", borderRadius: 4,
      background: tint(STATUS_COLOR[s], 7), color: STATUS_COLOR[s], border: `1px solid ${tint(STATUS_COLOR[s], 19)}`,
      cursor: onClick ? "pointer" : "default",
    }}>
      {STATUS_LABEL[s]}
    </span>
  );
}

/* ─── Detection Coverage Pill ─── */
function DetectionPill({ cov }: { cov: DetectionCoverage }) {
  const c = COVERAGE_COLOR[cov];
  const Icon = cov === "COVERED" ? CheckCircle : cov === "PARTIAL" ? Shield : EyeOff;
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4,
      fontFamily: "var(--font-mono)", fontSize: 9, padding: "2px 6px", borderRadius: 4,
      background: tint(c, 7), color: c, border: `1px solid ${tint(c, 19)}`,
    }}>
      <Icon size={10} aria-hidden /> {cov}
    </span>
  );
}

/* ─── Risk Score Breakdown ─── */
function RiskBreakdownBar({ breakdown }: { breakdown: RiskBreakdown }) {
  const segments = [
    { key: "cvss",    label: "CVSS",    color: "var(--chart-series-1)", value: breakdown.cvss },
    { key: "epss",    label: "EPSS",    color: "var(--chart-series-2)", value: breakdown.epss },
    { key: "exploit", label: "EXPLOIT", color: "var(--chart-series-3)", value: breakdown.exploit },
    { key: "lateral", label: "LATERAL", color: "var(--chart-series-4)", value: breakdown.lateral },
    { key: "asset",   label: "ASSET",   color: "var(--chart-series-5)", value: breakdown.asset },
    { key: "kev",     label: "KEV",     color: SEV_PALETTE.RED, value: breakdown.kev },
  ];
  // Show contribution proportions without assuming whether the canonical score
  // is 0–100 or 0–1000. The score-scale decision is owned by the backend policy.
  const recordedTotal = segments.reduce((total, segment) => total + Math.max(0, segment.value), 0);
  return (
    <div>
      <div style={{ height: 8, display: "flex", borderRadius: 4, overflow: "hidden", marginBottom: 6 }}>
        {segments.map((s) => (
          <div key={s.key} style={{ width: `${recordedTotal ? (Math.max(0, s.value) / recordedTotal) * 100 : 0}%`, background: s.color }} title={`${s.label}: ${s.value}`} />
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
        const color = KILL_CHAIN_PHASE_COLOR[step.phase] ?? SEV_PALETTE.SLATE;
        return (
          <div key={i} style={{ display: "flex", gap: 0, alignItems: "stretch" }}>
            {/* Timeline line */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 24, flexShrink: 0 }}>
              <div style={{
                width: 10, height: 10, borderRadius: "50%", background: color,
                border: `2px solid ${tint(color, 25)}`, flexShrink: 0, marginTop: 4, zIndex: 1,
              }} />
              {i < steps.length - 1 && (
                <div style={{ width: 1, flex: 1, background: tint(color, 19), minHeight: 16 }} />
              )}
            </div>
            {/* Step content */}
            <div style={{ flex: 1, paddingBottom: i < steps.length - 1 ? 10 : 0, paddingLeft: 8 }}>
              <div style={{ display: "flex", gap: 6, alignItems: "center", marginBottom: 2 }}>
                <span style={{
                  fontFamily: "var(--font-mono)", fontSize: 9, color,
                  background: tint(color, 7), border: `1px solid ${tint(color, 15)}`,
                  padding: "1px 5px", borderRadius: 3,
                }}>{step.phase}</span>
                {step.mitre && (
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--accent)" }}>
                    {step.mitre}
                  </span>
                )}
              </div>
              <div style={{ fontFamily: "var(--font-ui)", fontSize: 12, fontWeight: 600, color: "var(--text-primary)", marginBottom: 1 }}>
                {step.technique}
              </div>
              <div style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.4 }}>
                {step.description}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

/* ─── Evidence artifacts ─── */
function EvidenceGallery({ evidence }: { evidence: Finding["evidence"] }) {
  if (!evidence.length) {
    return (
      <section className="finding-evidence-empty" aria-labelledby="finding-evidence-empty-title">
        <FileText size={20} aria-hidden />
        <div>
          <h3 id="finding-evidence-empty-title">No recorded evidence</h3>
          <p>Validate the finding and attach reproducible proof before it is used for remediation or client delivery.</p>
        </div>
      </section>
    );
  }

  const prepared = evidence.map((artifact) => ({ artifact, presentation: presentEvidence(artifact) }));
  const totalLines = prepared.reduce((total, item) => total + item.presentation.lines.length, 0);
  const totalRedactions = prepared.reduce((total, item) => total + item.presentation.redactions, 0);

  return (
    <div className="finding-evidence-view">
      <section className="finding-evidence-summary" aria-labelledby="finding-evidence-title">
        <div className="finding-evidence-summary-copy">
          <span className="finding-evidence-summary-icon"><FileText size={16} aria-hidden /></span>
          <div>
            <h3 id="finding-evidence-title">Evidence review</h3>
            <p>Scanner-captured proof is shown as recorded. Likely credentials and secrets are masked in this view and copied output.</p>
          </div>
        </div>
        <dl>
          <div><dt>Artifacts</dt><dd>{evidence.length}</dd></div>
          <div><dt>Lines</dt><dd>{totalLines.toLocaleString()}</dd></div>
          <div><dt>Masked</dt><dd>{totalRedactions}</dd></div>
        </dl>
      </section>

      {prepared.map(({ artifact, presentation }, index) => {
        const label = artifact.label.trim() || `Evidence artifact ${index + 1}`;
        return (
          <article className="finding-evidence-artifact" key={`${label}-${index}`}>
            <header>
              <div className="finding-evidence-identity">
                <span className="finding-evidence-kind">{presentation.kind}</span>
                <div>
                  <h3>{label}</h3>
                  <p>{presentation.lines.length.toLocaleString()} line{presentation.lines.length === 1 ? "" : "s"} recorded</p>
                </div>
              </div>
              <CopyBtn text={presentation.copyText} showLabel />
            </header>

            {presentation.provenance.length ? (
              <dl className="finding-evidence-provenance" aria-label={`${label} provenance`}>
                {presentation.provenance.map((item) => (
                  <div key={item.label}>
                    <dt>{item.label}</dt>
                    <dd title={item.title}>{item.value}</dd>
                  </div>
                ))}
              </dl>
            ) : (
              <p className="finding-evidence-provenance-empty">Capture source and timestamp were not recorded.</p>
            )}

            {presentation.command && (
              <div className="finding-evidence-command">
                <Terminal size={13} aria-hidden />
                <span>Command</span>
                <code>{presentation.command}</code>
              </div>
            )}

            <div className="finding-evidence-output-heading">
              <span>Captured output</span>
              <span>{presentation.redactions ? `${presentation.redactions} sensitive value${presentation.redactions === 1 ? "" : "s"} masked` : "No sensitive values detected"}</span>
            </div>
            {presentation.visibleLines.length ? (
              <div className="finding-evidence-code" role="region" aria-label={`${label} evidence content`} tabIndex={0}>
                {presentation.visibleLines.map((line, lineIndex) => (
                  <div key={lineIndex}>
                    <span aria-hidden>{lineIndex + 1}</span>
                    <code>{line || " "}</code>
                  </div>
                ))}
              </div>
            ) : (
              <div className="finding-evidence-artifact-empty">This artifact was recorded without output.</div>
            )}
            <footer>
              <span>Showing {presentation.visibleLines.length.toLocaleString()} of {presentation.lines.length.toLocaleString()} lines</span>
              <span>{presentation.truncated ? "Copy includes all masked lines." : "Displayed output is complete."}</span>
            </footer>
          </article>
        );
      })}
    </div>
  );
}

/* ─── Structured remediation plan ─── */
function remediationOsFor(finding: Finding): RemediationOs {
  const value = (finding.assetContext?.os ?? "").toLowerCase();
  if (value.includes("windows")) return "windows";
  if (value.includes("mac") || value.includes("darwin")) return "macos";
  if (value.includes("linux") || value.includes("unix")) return "linux";
  return "generic";
}

function RemediationPlanView({ finding }: { finding: Finding }) {
  const [os, setOs] = useState<RemediationOs>(() => remediationOsFor(finding));
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["finding-remediation", finding.id, os],
    queryFn: () => fetchJson<RemediationPlanResponse>(`/api/findings/${finding.id}/remediation?os=${os}`),
    staleTime: 60_000,
  });

  if (isLoading) return <div className="finding-data-missing finding-data-missing-large">Loading the validated remediation plan…</div>;
  if (error || !data) {
    return (
      <div className="finding-data-missing finding-data-missing-large">
        The remediation plan could not be loaded. The finding record is unchanged.
        <button className="findings-inline-action" onClick={() => { void refetch(); }}>Retry plan</button>
      </div>
    );
  }

  const plan = data.plan;
  const changeRiskColor = plan.remediation_risk === "high"
    ? SEV_PALETTE.RED
    : plan.remediation_risk === "medium" ? SEV_PALETTE.AMBER : "var(--text-secondary)";
  const recordedNotes = finding.remediation
    .map((step) => typeof step === "string" ? step : step.description || step.title)
    .filter(Boolean);

  return (
    <div className="finding-remediation-view">
      <header className="finding-remediation-header">
        <div>
          <div className="finding-remediation-title"><Wrench size={16} /><h3>Remediation plan</h3></div>
          <p>{plan.summary}</p>
          <div className="finding-remediation-meta">
            <span>Source: {data.source === "ai" ? "AI-generated operator plan" : "Vedha remediation knowledge base"}</span>
            <span>Effort: {plan.effort}</span>
            <span style={{ color: changeRiskColor }}>Change risk: {plan.remediation_risk}</span>
            {data.generated_at && <span>Generated {fmtEventDay(data.generated_at)}</span>}
          </div>
        </div>
        <label className="finding-remediation-os">
          Target platform
          <select value={os} onChange={(event) => setOs(event.target.value as RemediationOs)}>
            <option value="generic">Generic / appliance</option>
            <option value="linux">Linux</option>
            <option value="windows">Windows</option>
            <option value="macos">macOS</option>
          </select>
        </label>
      </header>

      {recordedNotes.length > 0 && (
        <section className="finding-remediation-note">
          <h3>Recorded finding guidance</h3>
          {recordedNotes.map((note, index) => <p key={index}>{note}</p>)}
        </section>
      )}

      <section className="finding-remediation-section">
        <div className="finding-section-heading">
          <div><Terminal size={15} /><h3>Remediation actions</h3></div>
          <span>{plan.steps.length} ordered step{plan.steps.length === 1 ? "" : "s"}</span>
        </div>
        <div className="finding-remediation-steps">
          {plan.steps.map((step) => (
            <article key={step.step}>
              <div className="finding-remediation-step-number">{step.step}</div>
              <div>
                <header>
                  <h4>{step.title}</h4>
                  <span data-risk={step.risk}>{step.risk} change risk</span>
                </header>
                <p>{step.description}</p>
                {step.commands_for_os.length > 0 && (
                  <div className="finding-remediation-commands">
                    {step.commands_for_os.map((command, index) => (
                      <div key={index}><code>{command}</code><CopyBtn text={command} /></div>
                    ))}
                  </div>
                )}
                {step.unsafe_commands_removed && (
                  <div className="finding-remediation-warning"><AlertTriangle size={13} /> Unsafe generated commands were removed before this plan was stored.</div>
                )}
                {step.verification && (
                  <div className="finding-remediation-verify"><CheckCircle size={13} /> <span><strong>Verify this step:</strong> {step.verification}</span></div>
                )}
              </div>
            </article>
          ))}
        </div>
      </section>

      <div className="finding-remediation-closeout">
        <section>
          <h3>Verification and closure</h3>
          {plan.verification.length ? (
            <ol>{plan.verification.map((item, index) => <li key={index}>{item}</li>)}</ol>
          ) : <p>No separate closeout check is recorded. Re-scan the affected asset and attach the result before closing.</p>}
        </section>
        <section>
          <h3>Compensating control</h3>
          <p>{plan.compensating_controls || "No compensating control is recorded for this plan."}</p>
        </section>
        <section>
          <h3>Further hardening</h3>
          {plan.long_term_recommendations.length ? (
            <ul>{plan.long_term_recommendations.map((item, index) => <li key={index}>{item}</li>)}</ul>
          ) : <p>No further hardening recommendation is recorded.</p>}
        </section>
      </div>
    </div>
  );
}

function FindingOverview({
  finding,
  related,
  sla,
  customerImpact,
  firstRemediation,
}: {
  finding: Finding;
  related: Finding[];
  sla: ReturnType<typeof getSlaColor>;
  customerImpact: string;
  firstRemediation?: string;
}) {
  const asset = finding.assetContext;
  const host = asset?.fqdn || asset?.hostname || asset?.ipAddress || finding.affectedHost;
  const confidence = finding.verificationConfidence == null ? "Not scored" : `${finding.verificationConfidence}%`;
  return (
    <div className="finding-overview-view">
      <div className="finding-overview-primary">
        <section>
          <h3>Summary</h3>
          <p>{finding.description || "No finding description has been recorded."}</p>
        </section>
        <section>
          <h3>Impact</h3>
          <p>{customerImpact}</p>
        </section>
        <section className="finding-overview-next-action">
          <h3>Recommended next action</h3>
          <p>{firstRemediation || "Assign an owner, validate the evidence, and record an approved remediation plan."}</p>
        </section>
      </div>

      <dl className="finding-overview-facts" aria-label="Affected asset and decision signals">
        <div><dt>Host</dt><dd>{host || "Not recorded"}</dd></div>
        <div><dt>Platform</dt><dd>{[asset?.os, asset?.osVersion].filter(Boolean).join(" ") || "Not recorded"}</dd></div>
        <div><dt>Owner</dt><dd>{asset?.owner || finding.assignee || "Unassigned"}</dd></div>
        <div><dt>Evidence</dt><dd>{finding.verificationState || "Unassessed"} · {confidence}</dd></div>
        <div><dt>Exploit status</dt><dd>{finding.activelyExploited ? "Validated exploitation" : "Not validated"}</dd></div>
        <div><dt>SLA</dt><dd style={{ color: sla.color }}>{sla.label}</dd></div>
      </dl>

      <details className="finding-overview-disclosure">
        <summary><span><Shield size={15} /> Technical details and scoring</span><ChevronDown size={16} aria-hidden /></summary>
        <div className="finding-overview-technical-grid">
          <section>
            <h3>Scoring and identifiers</h3>
            <dl>
              <div><dt>Manager risk</dt><dd style={{ color: riskScoreColor(finding.riskScore) }}>{finding.riskScore}/1000</dd></div>
              <div><dt>CVSS</dt><dd>{finding.cvss || "Not recorded"}</dd></div>
              <div><dt>CVSS vector</dt><dd><code>{finding.cvssVector || "Not recorded"}</code></dd></div>
              <div><dt>CVE identifiers</dt><dd>{finding.cves?.length ? finding.cves.join(", ") : "None recorded"}</dd></div>
              <div><dt>Category</dt><dd>{finding.category}</dd></div>
            </dl>
          </section>
          <section>
            <h3>Detection and verification</h3>
            <dl>
              <div><dt>Detection coverage</dt><dd>{finding.detectionCoverage}</dd></div>
              <div><dt>Verification state</dt><dd>{finding.verificationState || "Unassessed"}</dd></div>
              <div><dt>Confidence</dt><dd>{confidence}</dd></div>
              <div><dt>First seen</dt><dd>{new Date(finding.discoveredAt).toLocaleString()}</dd></div>
              <div><dt>Last seen</dt><dd>{finding.lastSeen ? new Date(finding.lastSeen).toLocaleString() : "Not recorded"}</dd></div>
            </dl>
          </section>
          <section className="finding-overview-risk-factors">
            <h3>Risk factors</h3>
            <RiskBreakdownBar breakdown={finding.riskBreakdown} />
          </section>
          <section className="finding-overview-technical-narrative">
            <h3>Technical explanation</h3>
            <p>{finding.technicalDetails || finding.verificationRationale || "No additional technical explanation is recorded. Review the evidence and source scan before making a closure decision."}</p>
          </section>
        </div>
      </details>

      <details className="finding-overview-disclosure">
        <summary><span><Link2 size={15} /> Attack path and correlated findings</span><ChevronDown size={16} aria-hidden /></summary>
        <div className="finding-attack-context">
          <div className="finding-attack-context-grid">
            <div>
              <h4>MITRE ATT&amp;CK</h4>
              {finding.mitre.length ? finding.mitre.map((mapping) => (
                <div className="finding-mitre-row" key={mapping.id}><code>{mapping.id}</code><span>{mapping.name}</span></div>
              )) : <p className="finding-data-missing">No MITRE ATT&amp;CK technique is mapped.</p>}
              {finding.tags && finding.tags.length > 0 && <div className="finding-overview-tags">{finding.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>}
            </div>
            <div>
              <h4>Kill chain</h4>
              {finding.killChain.length ? <KillChainViz steps={finding.killChain} /> : <p className="finding-data-missing">No kill-chain path has been recorded.</p>}
            </div>
          </div>
          {related.length > 0 && (
            <div className="finding-related-list">
              <h4>Correlated findings</h4>
              {related.map((item) => (
                <div key={item.id}><span style={{ background: SEV_COLOR[item.severity] }} /><code>{item.id}</code><strong>{item.title}</strong><RiskBadge score={item.riskScore} /></div>
              ))}
            </div>
          )}
        </div>
      </details>
    </div>
  );
}

/* ─── Finding Detail ─── */
/* ─── Finding lifecycle event history (detailed vertical audit-trail timeline) ─── */
const EVENT_COLOR: Record<string, string> = {
  detected: SEV_PALETTE.BLUE,
  reaffirmed: SEV_PALETTE.SLATE,
  confirmed: SEV_PALETTE.ORANGE,
  remediated: SEV_PALETTE.GREEN,
  resolved: SEV_PALETTE.GREEN,
  accepted: SEV_PALETTE.AMBER,
  false_positive: SEV_PALETTE.SLATE,
  reopened: SEV_PALETTE.RED,
  status_changed: SEV_PALETTE.SKY,
  verification_changed: SEV_PALETTE.SKY,
  risk_changed: SEV_PALETTE.AMBER,
  note: SEV_PALETTE.SLATE,
};

/* Full timestamp to the second: "2026-08-27 14:03:11" (local tz). */
function fmtEventTs(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

/* Human relative age — "just now", "5m ago", "3d ago", "4mo ago". This is the
   primary read a customer scans; the exact timestamp stays as secondary detail. */
function fmtRelativeTs(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  const secs = Math.floor((Date.now() - d.getTime()) / 1000);
  if (secs < 45) return "just now";
  const mins = Math.floor(secs / 60);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 7) return `${days}d ago`;
  const weeks = Math.floor(days / 7);
  if (weeks < 5) return `${weeks}w ago`;
  const months = Math.floor(days / 30);
  if (months < 12) return `${months}mo ago`;
  return `${Math.floor(days / 365)}y ago`;
}

/* Short calendar date for the summary strip: "27 Aug 2026". */
function fmtEventDay(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" });
}

function eventActor(event: TimelineEvent): string {
  if (!event.actor) return event.actor_type === "user" ? "Unknown operator" : "Vedha system";
  if (event.actor_type !== "user") return event.actor;
  return `Operator ${event.actor.length > 12 ? `${event.actor.slice(0, 8)}…` : event.actor}`;
}

function eventNarrative(event: TimelineEvent): string {
  switch (event.event_type) {
    case "detected": return "Created the finding from recorded scan or detection evidence.";
    case "reaffirmed": return "Observed the same exposure again in a later assessment run.";
    case "confirmed": return "Confirmed that the finding is valid and requires action.";
    case "remediated": return "Closed the finding as remediated after the fix was reported.";
    case "resolved": return "Closed the finding automatically after coverage-proven clean runs.";
    case "accepted": return "Accepted the documented risk without marking the exposure as fixed.";
    case "false_positive": return "Classified the finding as a false positive after validation.";
    case "reopened": return "Reopened the finding because the exposure returned or the prior decision changed.";
    case "risk_changed": return "Recalculated the finding's CVSS or Manager risk score.";
    case "verification_changed": return "Updated the evidence-verification verdict.";
    case "note": return "Added an operator note to the finding record.";
    default: return event.from_status && event.to_status
      ? `Changed lifecycle status from ${event.from_status} to ${event.to_status}.`
      : "Updated the finding record.";
  }
}

function eventDetailLabel(key: string): string {
  return key.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function HistoryTimeline({ findingId }: { findingId: string }) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["finding-events", findingId],
    queryFn: () => fetchJson<FindingTimeline>(`/api/findings/${findingId}/events`),
    staleTime: 30_000,
  });

  if (isLoading) return <div className="finding-data-missing">Loading event history…</div>;
  if (error) return <div className="finding-data-missing finding-data-missing-large">Could not load the event history for this finding.<button className="findings-inline-action" onClick={() => { void refetch(); }}>Retry history</button></div>;
  const events = data?.events ?? [];
  if (!events.length) {
    return <div className="finding-data-missing finding-data-missing-large">No lifecycle events are recorded for this finding yet.</div>;
  }

  // Events arrive oldest-first (chronological). The last one is the current state.
  const first = events[0];
  const latest = events[events.length - 1];
  const latestColor = EVENT_COLOR[latest.event_type] ?? SEV_PALETTE.SLATE;

  return (
    <div className="finding-history-view">
      <header className="finding-history-summary">
        <div>
          <h3>Activity history</h3>
          <p>Stored operator actions and system observations, ordered from oldest to newest.</p>
        </div>
        <dl>
          <div><dt>Events</dt><dd>{events.length}</dd></div>
          <div><dt>Period</dt><dd>{fmtEventDay(first.occurred_at)}{events.length > 1 ? ` – ${fmtEventDay(latest.occurred_at)}` : ""}</dd></div>
          <div><dt>Current action</dt><dd style={{ color: latestColor }}>{latest.label}</dd></div>
        </dl>
      </header>

      <div className="finding-history-timeline">
        {events.map((ev, i) => {
          const color = EVENT_COLOR[ev.event_type] ?? SEV_PALETTE.SLATE;
          const last = i === events.length - 1;
          const isCurrent = last && events.length > 1;
          const reason = typeof ev.detail?.reason === "string" ? ev.detail.reason : null;
          const detailEntries = ev.detail
            ? Object.entries(ev.detail).filter(([key]) => key !== "approx" && key !== "reason" && key !== "note")
            : [];
          return (
            <div key={ev.id ?? `${ev.event_type}-${ev.occurred_at}-${i}`} style={{ display: "flex", gap: 0, alignItems: "stretch" }}>
              {/* Timeline rail */}
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 24, flexShrink: 0 }}>
                <div style={{
                  width: isCurrent ? 12 : 10, height: isCurrent ? 12 : 10, borderRadius: "50%", background: color,
                  border: `2px solid ${color}${isCurrent ? "66" : "40"}`, flexShrink: 0, marginTop: 4, zIndex: 1,
                  boxShadow: isCurrent ? `0 0 0 3px ${tint(color, 9)}` : "none",
                }} />
                {!last && <div style={{ width: 1, flex: 1, background: tint(color, 19), minHeight: 18 }} />}
              </div>
              {/* Event content */}
              <article style={{ flex: 1, paddingBottom: last ? 0 : 18, paddingLeft: 10 }}>
                <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap", marginBottom: 3 }}>
                  <span title={fmtEventTs(ev.occurred_at)} style={{ fontFamily: "var(--font-ui)", fontSize: 12, color: "var(--text-primary)", fontWeight: 600 }}>
                    {fmtRelativeTs(ev.occurred_at)}
                  </span>
                  <span style={{
                    fontFamily: "var(--font-mono)", fontSize: 9, color,
                    background: tint(color, 7), border: `1px solid ${tint(color, 15)}`,
                    padding: "1px 6px", borderRadius: 3, fontWeight: 700, letterSpacing: 0.5,
                  }}>{ev.label}</span>
                  {isCurrent && (
                    <span style={{
                      fontFamily: "var(--font-mono)", fontSize: 8, color: "var(--accent)",
                      background: "var(--accent-ghost)", border: "1px solid var(--border-accent)",
                      padding: "1px 5px", borderRadius: 3, fontWeight: 700, letterSpacing: 0.5, textTransform: "uppercase",
                    }}>current</span>
                  )}
                  {ev.synthesized && (
                    <span title="Derived from the finding's own record, not a separately stored audit row" style={{ fontFamily: "var(--font-mono)", fontSize: 8, color: "var(--text-secondary)", opacity: 0.7 }}>
                      derived
                    </span>
                  )}
                </div>
                <p className="finding-history-action">{eventNarrative(ev)}</p>
                <div className="finding-history-actor">
                  <span>{eventActor(ev)}</span>
                  {ev.from_status && ev.to_status && <span>{ev.from_status} → {ev.to_status}</span>}
                  <time dateTime={ev.occurred_at}>{fmtEventTs(ev.occurred_at)}</time>
                </div>
                {reason && <blockquote><strong>Reason</strong><span>{reason}</span></blockquote>}
                {typeof ev.detail?.note === "string" && <blockquote><strong>Note</strong><span>{ev.detail.note}</span></blockquote>}
                {detailEntries.length > 0 && (
                  <dl className="finding-history-details">
                    {detailEntries.map(([k, v]) => (
                      <div key={k}><dt>{eventDetailLabel(k)}</dt><dd>{typeof v === "object" && v !== null ? JSON.stringify(v) : String(v)}</dd></div>
                    ))}
                  </dl>
                )}
              </article>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function FindingDetail({ f, allFindings, onStatusChange, statusUpdating, onReopen, reopening }: {
  f: Finding;
  allFindings: Finding[];
  onStatusChange: (id: string, s: FindingStatus, reason: string) => Promise<void>;
  statusUpdating: boolean;
  onReopen: (id: string, reason: string) => Promise<void>;
  reopening: boolean;
}) {
  const [tab, setTab] = useState<"overview" | "intel" | "evidence" | "remediation" | "compliance" | "history">("overview");
  const [pendingAction, setPendingAction] = useState<FindingStatus | null>(null);
  const [actionReason, setActionReason] = useState("");
  const { explain } = useAssistant();
  const sla = getSlaColor(f.discoveredAt, f.severity);

  const WORKFLOW: { status: FindingStatus; label: string }[] = [
    { status: "CONFIRMED",      label: "Confirm finding" },
    { status: "REMEDIATED",     label: "Close as remediated" },
    { status: "ACCEPTED",       label: "Accept risk" },
    { status: "FALSE_POSITIVE", label: "Mark false positive" },
    { status: "OPEN",           label: "Reopen finding" },
  ];
  const terminal = f.status === "REMEDIATED" || f.status === "ACCEPTED" || f.status === "FALSE_POSITIVE";
  const availableActions = terminal
    ? WORKFLOW.filter((action) => action.status === "OPEN")
    : WORKFLOW.filter((action) => action.status !== "OPEN" && action.status !== f.status);
  const actionBusy = statusUpdating || reopening;

  const submitAction = async () => {
    if (!pendingAction || actionReason.trim().length < 3) return;
    const reason = actionReason.trim();
    try {
      if (pendingAction === "OPEN" && f.status === "REMEDIATED") {
        await onReopen(f.id, reason);
      } else {
        await onStatusChange(f.id, pendingAction, reason);
      }
    } catch {
      return; // The mutation already presents the actionable error toast.
    }
    setPendingAction(null);
    setActionReason("");
  };

  const related = allFindings.filter((r) => r.id !== f.id && (f.relatedFindings ?? []).includes(r.id));
  const hasAiTriage = Boolean(f.aiTriage.reasoning || f.aiTriage.recommendation) && f.aiTriage.confidence > 0;
  const cveIds = [...new Set([...(f.cves ?? []), ...(f.tags ?? [])].filter((value) => /^CVE-\d{4}-\d{4,7}$/i.test(value)))];
  const firstRemediation = f.remediation
    .flatMap((step) => (typeof step === "string" ? step : step.description || step.title).split(/\n+/))
    .map((line) => line.replace(/^\s*(?:[-*•]|\d+[.)])\s*/, "").trim())
    .find(Boolean);
  const customerImpact = f.businessImpact || f.impact || "Business impact has not been recorded. Validate asset criticality, exposure, and reachable attack paths before assigning impact.";

  return (
    <div className="finding-detail-panel">

      {/* ── Header ── */}
      <div className="finding-detail-header">
        <div className="finding-detail-badges">
          <SevBadge s={f.severity} />
          <StatusBadge s={f.status} />
          <RiskBadge score={f.riskScore} />
          {f.kevStatusRecorded && f.kevListed && <KevBadge />}
          <NeedsReviewChip show={f.needsReview} />
          <PriorityBadge priority={f.aiTriage.priority} compact />
          <button
            className="btn btn-secondary"
            onClick={() => explain(f.id)}
            aria-label="Explain this finding in plain English"
            style={{ marginLeft: "auto", height: 26, padding: "0 10px", fontSize: 11 }}
          >
            <Brain size={13} /> Explain &amp; remediate
          </button>
        </div>
        <h2 className="finding-detail-title">{f.title}</h2>
        <div className="finding-detail-meta">
          <span>{f.affectedHost}</span>
          <span>{f.category}</span>
          <span>{f.id}</span>
          {f.assignee && <span style={{ color: "var(--accent)" }}>Owner: {f.assignee}</span>}
        </div>
        {cveIds.length > 0 && (
          <div className="finding-cve-list">{cveIds.map((cve) => <code key={cve}>{cve}</code>)}</div>
        )}
      </div>

      {/* ── AI Triage Panel ── */}
      {hasAiTriage && <details className="finding-ai-triage">
        <summary>
          <Brain size={13} color="var(--accent)" style={{ flexShrink: 0, marginTop: 1 }} />
          <span>AI triage</span>
          <small>{Math.round(f.aiTriage.confidence * 100)}% confidence</small>
          <ChevronDown size={15} aria-hidden />
        </summary>
        <div className="finding-ai-triage-content">
            <div className="finding-ai-triage-reasoning">{f.aiTriage.reasoning}</div>
            <div className="finding-ai-triage-recommendation">
              <span>Recommended: </span>
              {f.aiTriage.recommendation}
            </div>
        </div>
      </details>}

      {/* ── Workflow ── */}
      <section className="finding-action-bar" aria-label="Finding lifecycle actions">
        <div>
          <strong>Record an action</strong>
          <span>Every decision is added to the immutable activity history.</span>
        </div>
        <label className="finding-action-select">
          <span>Action</span>
          <select
            value={pendingAction ?? ""}
            onChange={(event) => {
              setPendingAction((event.target.value || null) as FindingStatus | null);
              setActionReason("");
            }}
            disabled={actionBusy}
          >
            <option value="">Choose an action…</option>
            {availableActions.map((action) => <option key={action.status} value={action.status}>{action.label}</option>)}
          </select>
        </label>
        {pendingAction && (
          <div className="finding-action-composer">
            <div>
              <label htmlFor={`finding-action-reason-${f.id}`}>
                Reason for {WORKFLOW.find((action) => action.status === pendingAction)?.label.toLowerCase()}
              </label>
              <p>
                {pendingAction === "REMEDIATED" && "Describe the applied fix and the verification performed."}
                {pendingAction === "ACCEPTED" && "Record the business justification, accountable owner, and compensating control or review date."}
                {pendingAction === "FALSE_POSITIVE" && "Record the validation evidence that disproves the finding."}
                {pendingAction === "CONFIRMED" && "Record the evidence or analyst decision that confirms the finding."}
                {pendingAction === "OPEN" && "Record what changed, reappeared, or invalidated the previous decision."}
              </p>
            </div>
            <textarea
              id={`finding-action-reason-${f.id}`}
              value={actionReason}
              onChange={(event) => setActionReason(event.target.value)}
              maxLength={1000}
              rows={3}
              placeholder="Add a concise, evidence-based reason…"
              autoFocus
            />
            <div className="finding-action-composer-footer">
              <span>{actionReason.length}/1000 · minimum 3 characters</span>
              <button type="button" className="btn btn-ghost" onClick={() => { setPendingAction(null); setActionReason(""); }} disabled={actionBusy}><X size={13} /> Cancel</button>
              <button type="button" className="btn btn-primary" onClick={() => { void submitAction(); }} disabled={actionBusy || actionReason.trim().length < 3} aria-busy={actionBusy}>
                {actionBusy ? <LoaderCircle className="findings-spinner" size={13} /> : <Check size={13} />} Record action
              </button>
            </div>
          </div>
        )}
      </section>

      {/* ── Tabs ── */}
      <div className="finding-detail-tabs" role="tablist" aria-label="Finding detail views">
        {(["overview", "evidence", "remediation", "history"] as const).map((t) => (
          <button
            key={t}
            id={`finding-tab-${t}-${f.id}`}
            role="tab"
            aria-selected={tab === t}
            aria-controls={`finding-panel-${f.id}`}
            onClick={() => setTab(t)}
            data-active={tab === t}
          >
            {t === "evidence" ? `Evidence (${f.evidence.length})` : t === "remediation" ? "Remediation plan" : t === "history" ? "History" : "Overview"}
          </button>
        ))}
      </div>

      <div
        id={`finding-panel-${f.id}`}
        role="tabpanel"
        aria-labelledby={`finding-tab-${tab}-${f.id}`}
        className="finding-detail-content"
      >

        {/* Overview tab */}
        {tab === "overview" && (
          <FindingOverview
            finding={f}
            related={related}
            sla={sla}
            customerImpact={customerImpact}
            firstRemediation={firstRemediation}
          />
        )}
        {false && tab === "overview" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 5 }}>DESCRIPTION</div>
              <div style={{ fontFamily: "var(--font-ui)", fontSize: 13, color: "var(--text-primary)", lineHeight: 1.6, marginBottom: 14 }}>{f.description || "No finding description has been recorded."}</div>

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
                      <span style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-primary)", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{r.title}</span>
                      <RiskBadge score={r.riskScore} />
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div>
              <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 5 }}>TECHNICAL DETAILS</div>
              <div style={{ fontFamily: "var(--font-ui)", fontSize: 13, color: "var(--text-primary)", lineHeight: 1.6, marginBottom: 12 }}>{f.technicalDetails || "No additional technical narrative has been recorded."}</div>

              <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 6 }}>MITRE ATT&CK</div>
              {!f.mitre.length && <div className="finding-data-missing">No MITRE ATT&amp;CK technique is mapped.</div>}
              {f.mitre.map((m) => (
                <div key={m.id} style={{ display: "flex", gap: 8, marginBottom: 4, alignItems: "center" }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--accent)", flexShrink: 0 }}>{m.id}</span>
                  <span style={{ fontFamily: "var(--font-ui)", fontSize: 12, color: "var(--text-secondary)" }}>{m.name}</span>
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
                {f.epssRecorded ? <div /> : <div className="finding-data-missing">EPSS enrichment is not recorded.</div>}
                <div style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-secondary)", marginTop: 8, lineHeight: 1.4 }}>
                  {f.epssRecorded ? f.epssScore > 0.5
                    ? `Top ${(100 - f.epssPercentile * 100).toFixed(1)}% most likely to be exploited in the next 30 days (FIRST.org model).`
                    : "Use EPSS as one prioritization signal; it does not prove exploitation."
                    : "Run vulnerability enrichment before using exploitation probability in a remediation decision."}
                </div>
              </div>

              {/* CISA KEV */}
              <div style={{ background: "var(--bg-panel)", border: `1px solid ${f.kevListed ? tint(SEV_PALETTE.RED, 20) : "var(--border-subtle)"}`, borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 4 }}>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>CISA KEV STATUS</div>
                  {f.kevStatusRecorded && f.kevListed ? <KevBadge /> : f.kevStatusRecorded ? (
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-muted)", background: "var(--bg-surface)", border: "var(--hairline) solid var(--border-subtle)", borderRadius: 3, padding: "1px 5px" }}>NOT LISTED</span>
                  ) : <span className="badge badge-info">NOT ENRICHED</span>}
                </div>
                {f.kevListed && f.kevDateAdded && (
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: SEV_PALETTE.RED }}>Added {f.kevDateAdded}</div>
                )}
                <div style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-secondary)", marginTop: 6, lineHeight: 1.4 }}>
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
                  <div style={{ height: 4, flex: 1, background: "var(--track-bg)", borderRadius: 2, overflow: "hidden", marginRight: 10 }}>
                    <div style={{ height: "100%", width: `${f.fpProbability * 100}%`, background: f.fpProbability < 0.1 ? SEV_PALETTE.GREEN : f.fpProbability < 0.3 ? SEV_PALETTE.AMBER : SEV_PALETTE.RED, borderRadius: 2 }} />
                  </div>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: f.fpProbability < 0.1 ? SEV_PALETTE.GREEN : SEV_PALETTE.AMBER, fontWeight: 700, flexShrink: 0 }}>
                    {Math.round(f.fpProbability * 100)}%
                  </span>
                </div>
                <div style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-secondary)", marginTop: 5 }}>
                  {f.fpProbability < 0.1 ? "Very low FP probability — finding confirmed via exploitation evidence." : f.fpProbability < 0.3 ? "Moderate — correlate with additional evidence before closing." : "Elevated — validate before remediation investment."}
                </div>
              </div>}
            </div>

            {/* Right: exploit intel + detection */}
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {/* Exploit maturity */}
              {f.exploitMaturityRecorded && <div style={{ background: "var(--bg-panel)", border: `1px solid ${tint(MATURITY_COLOR[f.exploitMaturity], 13)}`, borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)", marginBottom: 8 }}>EXPLOIT INTELLIGENCE</div>
                <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 8 }}>
                  <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                    <div style={{ width: 8, height: 8, borderRadius: "50%", background: MATURITY_COLOR[f.exploitMaturity] }} />
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: MATURITY_COLOR[f.exploitMaturity] }}>{f.exploitMaturity}</span>
                  </div>
                  {f.pocAvailable && (
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: SEV_PALETTE.ORANGE, background: tint(SEV_PALETTE.ORANGE, 8), border: `1px solid ${tint(SEV_PALETTE.ORANGE, 20)}`, borderRadius: 3, padding: "1px 5px" }}>
                      PoC PUBLIC
                    </span>
                  )}
                  {f.activelyExploited && (
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: SEV_PALETTE.RED, background: tint(SEV_PALETTE.RED, 8), border: `1px solid ${tint(SEV_PALETTE.RED, 25)}`, borderRadius: 3, padding: "1px 5px" }}>
                      ACTIVE EXPLOITATION
                    </span>
                  )}
                </div>
                <div style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.4 }}>
                  {f.exploitMaturity === "WEAPONIZED"
                    ? "Weaponized exploit available in public toolchains (Metasploit/Sliver/Cobalt Strike). Exploitation is trivial for any attacker."
                    : f.exploitMaturity === "POC"
                    ? "Proof-of-concept code publicly available. Requires adaptation for production exploit but significantly lowers attacker barrier."
                    : "No public exploit code. Theoretical attack path — requires custom exploit development."}
                </div>
              </div>}

              {/* Detection coverage */}
              <div style={{ background: "var(--bg-panel)", border: `1px solid ${tint(COVERAGE_COLOR[f.detectionCoverage], 13)}`, borderRadius: 6, padding: "12px 14px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--text-secondary)" }}>DETECTION COVERAGE</div>
                  <DetectionPill cov={f.detectionCoverage} />
                </div>
                {f.detectionNote && (
                  <div style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-secondary)", lineHeight: 1.4, marginBottom: 8 }}>{f.detectionNote}</div>
                )}
                <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                  {f.mitre.map((m) => (
                    <div key={m.id} style={{ display: "flex", gap: 6, alignItems: "center", padding: "3px 6px", background: "var(--bg-app)", borderRadius: 3 }}>
                      <span style={{ fontFamily: "var(--font-mono)", fontSize: 9, color: "var(--accent)", flexShrink: 0 }}>{m.id}</span>
                      <span style={{ fontFamily: "var(--font-ui)", fontSize: 10, color: "var(--text-secondary)", flex: 1 }}>{m.name}</span>
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
                <div style={{ height: 6, background: "var(--track-bg)", borderRadius: 3, overflow: "hidden" }}>
                  <div style={{ height: "100%", width: `${Math.min(100, Math.max(0, f.riskScore / 10))}%`, background: riskScoreColor(f.riskScore), borderRadius: 3 }} />
                </div>
                <div style={{ fontFamily: "var(--font-ui)", fontSize: 11, color: "var(--text-secondary)", marginTop: 6 }}>
                  Manager-computed 0–1000 score. The browser displays it but never recalculates the underlying risk.
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Evidence tab */}
        {tab === "evidence" && <EvidenceGallery evidence={f.evidence} />}

        {/* Remediation tab */}
        {tab === "remediation" && <RemediationPlanView finding={f} />}
        {false && tab === "remediation" && (
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
                <div />
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
                    <div key={j} style={{ fontFamily: "var(--font-ui)", fontSize: 13, color: "var(--text-primary)", lineHeight: 1.4 }}>· {r}</div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* History tab — detailed lifecycle audit trail */}
        {tab === "history" && <HistoryTimeline findingId={f.id} />}
      </div>
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
  const [filterNeedsReview, setFilterNeedsReview] = useState(false);
  const [filterVerification, setFilterVerification] = useState<string>("ALL");
  const [filterAgentId, setFilterAgentId] = useState<string>("");
  const [agentsRefreshing, setAgentsRefreshing] = useState(false);
  const [agentRefreshFeedback, setAgentRefreshFeedback] = useState<string | null>(null);
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
  if (filterNeedsReview) queryString.set("needs_review", "true");
  if (filterVerification !== "ALL") queryString.set("verification_state", filterVerification);
  if (engagementId) queryString.set("engagement_id", engagementId);
  if (filterAgentId) queryString.set("agent_id", filterAgentId);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: [
      "findings-page", page, deferredSearch, filterSev, filterStatus,
      filterBlind, filterExploited, filterSlaBreached, sortBy, engagementId,
      filterNeedsReview, filterVerification, filterAgentId,
    ],
    queryFn: () => fetchJson<FindingPage>(`/api/findings?${queryString}`),
    refetchInterval: 30_000,
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });
  const summaryParams = new URLSearchParams();
  if (engagementId) summaryParams.set("engagement_id", engagementId);
  if (filterAgentId) summaryParams.set("agent_id", filterAgentId);
  const summaryQuery = useQuery({
    queryKey: ["findings-summary", engagementId, filterAgentId],
    queryFn: () => fetchJson<FindingSummary>(
      `/api/findings/summary${summaryParams.size ? `?${summaryParams}` : ""}`,
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

  const engagementOptionsQuery = useQuery({
    queryKey: ["engagements"],
    queryFn: () => fetchJson<{ engagements: EngagementOption[] }>("/api/engagements"),
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });
  const agentOptionsQuery = useQuery({
    queryKey: ["agents"],
    queryFn: () => fetchJson<VedhaAgentOption[]>("/api/agents/register"),
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });
  const activeAgentCount = (agentOptionsQuery.data ?? []).filter((agent) => agent.status !== "OFFLINE").length;
  const registeredAgentCount = agentOptionsQuery.data?.length ?? 0;
  const refreshAgents = async () => {
    if (agentsRefreshing) return;
    setAgentsRefreshing(true);
    setAgentRefreshFeedback("Checking agent heartbeats…");
    try {
      const [result] = await Promise.all([
        agentOptionsQuery.refetch(),
        new Promise<void>((resolve) => window.setTimeout(resolve, AGENT_REFRESH_FEEDBACK_MS)),
      ]);
      if (result.error) throw result.error;
      const agents = result.data ?? [];
      const active = agents.filter((agent) => agent.status !== "OFFLINE").length;
      setAgentRefreshFeedback(`${active} active of ${agents.length} registered`);
    } catch (refreshError) {
      setAgentRefreshFeedback("Agent status unavailable — retry");
      showError("Agent refresh failed", errorMessage(refreshError));
    } finally {
      setAgentsRefreshing(false);
    }
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
    enabled: Boolean(selectedId),
    retry: false,
  });

  const statusMutation = useMutation({
    mutationFn: ({ id, status, reason }: { id: string; status: FindingStatus; reason: string }) =>
      fetchJson<Finding>(`/api/findings/${id}`, {
        method: "PUT",
        body: JSON.stringify({ status, actionReason: reason }),
      }),
    onError: (mutationError) => showError("Status update failed", errorMessage(mutationError)),
    onSuccess: (updated) => {
      success("Status updated", `${updated.id} → ${STATUS_LABEL[updated.status]}`);
    },
    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: ["findings-page"] });
      void queryClient.invalidateQueries({ queryKey: ["findings-summary"] });
      void queryClient.invalidateQueries({ queryKey: ["finding-detail"] });
      void queryClient.invalidateQueries({ queryKey: ["finding-events"] });
    },
  });

  const handleStatusChange = useCallback(async (id: string, newStatus: FindingStatus, reason: string) => {
    await statusMutation.mutateAsync({ id, status: newStatus, reason });
  }, [statusMutation]);

  const reopenMutation = useMutation({
    mutationFn: ({ id, reason }: { id: string; reason: string }) =>
      fetchJson<Finding>(`/api/findings/${id}/reopen`, {
        method: "POST",
        body: JSON.stringify({ reason }),
      }),
    onError: (mutationError) => showError("Reopen failed", errorMessage(mutationError)),
    onSuccess: (updated) => success("Finding reopened", `${updated.id} → OPEN`),
    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: ["findings-page"] });
      void queryClient.invalidateQueries({ queryKey: ["finding-detail"] });
      void queryClient.invalidateQueries({ queryKey: ["findings-summary"] });
      void queryClient.invalidateQueries({ queryKey: ["finding-events"] });
    },
  });

  const handleReopen = useCallback(async (id: string, reason: string) => {
    await reopenMutation.mutateAsync({ id, reason });
  }, [reopenMutation]);

  const selected = detailQuery.data ?? inCurrentPage ?? null;
  const hasActiveFilters = Boolean(
    search.trim()
    || filterSev !== "ALL"
    || filterStatus !== "ALL"
    || filterBlind
    || filterExploited
    || filterSlaBreached
    || filterNeedsReview
    || filterVerification !== "ALL"
    || engagementId
    || filterAgentId,
  );
  const advancedFilterCount = [
    filterSev !== "ALL",
    filterStatus !== "ALL",
    filterVerification !== "ALL",
    filterBlind,
    filterExploited,
    filterSlaBreached,
    filterNeedsReview,
  ].filter(Boolean).length;
  const summaryUnavailable = summaryQuery.isLoading || Boolean(summaryQuery.error);
  const summaryValue = (value: number) => summaryUnavailable ? "—" : value.toLocaleString();
  const clearFilters = () => {
    setSearch("");
    setFilterSev("ALL");
    setFilterStatus("ALL");
    setFilterBlind(false);
    setFilterExploited(false);
    setFilterSlaBreached(false);
    setFilterNeedsReview(false);
    setFilterVerification("ALL");
    setFilterAgentId("");
    setEngagementId(null);
    setSortBy("risk");
    setPage(1);
    setSelectedId(null);
  };

  return (
    <PageShell
      title="Findings"
      subtitle="Triage, verify, and remediate discovered vulnerabilities"
      headerActions={
        <div className="findings-agent-refresh">
          <span
            className="findings-agent-refresh-status"
            data-tone={agentsRefreshing ? "idle" : agentOptionsQuery.error ? "error" : activeAgentCount > 0 ? "active" : "idle"}
            role="status"
            aria-live="polite"
          >
            <i aria-hidden />
            {agentRefreshFeedback
              ?? (agentOptionsQuery.isLoading
                ? "Checking agent status…"
                : agentOptionsQuery.error
                  ? "Agent status unavailable"
                  : `${activeAgentCount} active of ${registeredAgentCount} registered`)}
          </span>
          <button
            type="button"
            className="findings-agent-refresh-button"
            onClick={() => { void refreshAgents(); }}
            disabled={agentsRefreshing}
            aria-busy={agentsRefreshing}
            aria-label="Refresh active Vedha agents and probes"
          >
            <RefreshCw className={agentsRefreshing ? "findings-spinner" : undefined} size={14} aria-hidden />
            {agentsRefreshing ? "Checking agents…" : "Refresh agents"}
          </button>
        </div>
      }
      statusItems={[
        { label: "CRITICAL OPEN",    value: summaryValue(stats.criticalOpen), color: summaryUnavailable ? "var(--text-muted)" : SEV_PALETTE.RED },
        { label: "EXPLOIT CONFIRMED", value: summaryValue(stats.validated),    color: summaryUnavailable ? "var(--text-muted)" : SEV_PALETTE.ORANGE },
        { label: "DETECTION BLIND",   value: summaryValue(stats.blind),        color: summaryUnavailable ? "var(--text-muted)" : SEV_PALETTE.AMBER },
        { label: "AVG RISK /1000",    value: summaryValue(stats.averageRisk),  color: summaryUnavailable ? "var(--text-muted)" : riskScoreColor(stats.averageRisk) },
      ]}
    >
      <style>{`
        .findings-workspace ::selection {
          color: var(--text-primary);
          background: var(--accent-ghost);
        }
        .findings-agent-refresh { display: flex; align-items: center; gap: 8px; }
        .findings-agent-refresh-status {
          display: inline-flex;
          min-width: 0;
          align-items: center;
          gap: 6px;
          color: var(--text-secondary);
          font: 550 10.5px/1.3 var(--font-ui);
          white-space: nowrap;
        }
        .findings-agent-refresh-status i { width: 6px; height: 6px; flex: 0 0 auto; border-radius: 50%; background: var(--text-muted); }
        .findings-agent-refresh-status[data-tone="active"] i { background: var(--nominal-color); }
        .findings-agent-refresh-status[data-tone="error"] { color: var(--sev-medium-color); }
        .findings-agent-refresh-status[data-tone="error"] i { background: var(--sev-medium-color); }
        .findings-agent-refresh-button {
          display: inline-flex;
          min-height: 32px;
          align-items: center;
          justify-content: center;
          gap: 7px;
          border: var(--hairline) solid var(--border-default);
          border-radius: 8px;
          padding: 0 10px;
          color: var(--text-primary);
          background: var(--bg-panel);
          font: 650 11px/1.2 var(--font-ui);
          white-space: nowrap;
          cursor: pointer;
        }
        .findings-agent-refresh-button:hover:not(:disabled) { border-color: var(--border-strong); background: var(--bg-hover); }
        .findings-agent-refresh-button:disabled { color: var(--text-muted); cursor: wait; }
        .findings-agent-refresh-button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
        .findings-workspace {
          display: grid;
          grid-template-columns: minmax(0, 1fr);
          gap: var(--space-4);
          align-items: start;
        }
        .findings-workspace[data-detail="true"] {
          grid-template-columns: minmax(288px, 332px) minmax(0, 1fr);
          gap: 20px;
        }
        .finding-detail-column {
          position: sticky;
          top: var(--space-3);
          max-height: calc(100dvh - 100px);
          overflow-y: auto;
          overscroll-behavior: contain;
          align-self: start;
          min-width: 0;
          scrollbar-gutter: stable;
          scrollbar-width: thin;
          scrollbar-color: var(--border-strong) transparent;
        }
        .finding-detail-column::-webkit-scrollbar { width: 8px; }
        .finding-detail-column::-webkit-scrollbar-track { background: transparent; }
        .finding-detail-column::-webkit-scrollbar-thumb {
          border: 2px solid transparent;
          border-radius: 999px;
          background: var(--border-strong);
          background-clip: padding-box;
        }
        .finding-detail-panel {
          overflow: hidden;
          border: var(--hairline) solid var(--border-default);
          border-radius: var(--r-lg);
          background: var(--bg-panel);
          box-shadow: var(--shadow-md);
          animation: finding-detail-enter 220ms var(--ease-out) both;
        }
        @keyframes finding-detail-enter {
          from { opacity: .86; transform: translateX(14px); box-shadow: var(--shadow-sm); }
          to { opacity: 1; transform: translateX(0); box-shadow: var(--shadow-md); }
        }
        .finding-detail-header {
          padding: 18px 22px;
          border-bottom: var(--hairline) solid var(--border-subtle);
        }
        .finding-detail-badges { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
        .finding-detail-title {
          max-width: 32ch;
          margin: 0;
          color: var(--text-primary);
          font: 700 20px/1.35 var(--font-ui);
          letter-spacing: -.018em;
          text-wrap: balance;
        }
        .finding-detail-meta {
          display: flex;
          gap: 4px 12px;
          flex-wrap: wrap;
          margin-top: 7px;
          overflow-wrap: anywhere;
          color: var(--text-secondary);
          font: 500 10.5px/1.5 var(--font-mono);
        }
        .finding-detail-meta > span + span::before { margin-right: 12px; color: var(--border-strong); content: "·"; }
        .finding-ai-triage {
          border-bottom: var(--hairline) solid var(--border-subtle);
          background: var(--accent-ghost);
        }
        .finding-ai-triage summary {
          display: flex;
          min-height: 42px;
          align-items: center;
          gap: 8px;
          padding: 0 22px;
          color: var(--text-primary);
          font: 650 12px/1.3 var(--font-ui);
          cursor: pointer;
          list-style: none;
        }
        .finding-ai-triage summary::-webkit-details-marker { display: none; }
        .finding-ai-triage summary small { margin-left: 2px; color: var(--text-muted); font: 500 10px/1.3 var(--font-mono); }
        .finding-ai-triage summary svg:last-child { margin-left: auto; color: var(--text-muted); transition: transform 180ms ease-out; }
        .finding-ai-triage[open] summary svg:last-child { transform: rotate(180deg); }
        .finding-ai-triage-content { min-width: 0; padding: 0 22px 14px 43px; }
        .finding-ai-triage-reasoning { max-width: 72ch; color: var(--text-primary); font: 450 13px/1.6 var(--font-ui); }
        .finding-ai-triage-recommendation { max-width: 72ch; margin-top: 5px; color: var(--accent); font: 550 13px/1.55 var(--font-ui); }
        .finding-ai-triage-recommendation > span { font: 700 9.5px/1.4 var(--font-mono); letter-spacing: .04em; }
        .finding-detail-tabs {
          position: sticky;
          top: 0;
          z-index: 3;
          display: flex;
          overflow-x: auto;
          border-bottom: var(--hairline) solid var(--border-default);
          background: var(--bg-panel);
          scrollbar-width: none;
        }
        .finding-detail-tabs::-webkit-scrollbar { display: none; }
        .finding-detail-tabs button {
          min-height: 42px;
          border: 0;
          border-bottom: 2px solid transparent;
          padding: 0 16px;
          color: var(--text-secondary);
          background: transparent;
          font: 650 11.5px/1.2 var(--font-ui);
          white-space: nowrap;
          cursor: pointer;
        }
        .finding-detail-tabs button:hover { color: var(--text-primary); background: var(--bg-hover); }
        .finding-detail-tabs button[data-active="true"] { border-bottom-color: var(--accent); color: var(--text-primary); background: var(--accent-ghost); }
        .finding-detail-tabs button:focus-visible { position: relative; z-index: 1; outline: 2px solid var(--accent); outline-offset: -3px; }
        .finding-detail-content { padding: 22px; }
        .findings-filter-panel {
          background: var(--bg-panel);
          border: var(--hairline) solid var(--border-subtle);
          border-radius: var(--r-lg);
          padding: var(--space-4);
        }
        .findings-filter-header {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: var(--space-3);
          margin-bottom: var(--space-3);
        }
        .findings-filter-header h2 {
          margin: 0 0 3px;
          color: var(--text-primary);
          font-size: 15px;
          line-height: 1.25;
        }
        .findings-filter-header p {
          margin: 0;
          color: var(--text-muted);
          font-size: 12px;
          line-height: 1.4;
        }
        .findings-clear-filter,
        .findings-inline-action {
          display: inline-flex;
          min-height: 34px;
          align-items: center;
          justify-content: center;
          gap: 6px;
          border: var(--hairline) solid var(--border-subtle);
          border-radius: 8px;
          padding: 6px 10px;
          color: var(--text-secondary);
          background: transparent;
          font: 600 12px/1 var(--font-ui);
          cursor: pointer;
        }
        .findings-inline-action { margin-top: 10px; color: var(--accent); border-color: var(--border-accent); }
        .findings-clear-filter:hover,
        .findings-inline-action:hover { color: var(--text-primary); background: var(--bg-hover); }
        .findings-search {
          display: flex;
          min-height: 42px;
          align-items: center;
          gap: 9px;
          margin-bottom: var(--space-4);
          border: var(--hairline) solid var(--border-strong);
          border-radius: 9px;
          padding: 0 12px;
          background: var(--bg-app);
        }
        .findings-search:focus-within { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-ghost); }
        .findings-search input {
          width: 100%;
          border: 0;
          outline: 0;
          color: var(--text-primary);
          background: transparent;
          font: 400 13px/1.4 var(--font-ui);
          caret-color: var(--accent);
        }
        .findings-search input::placeholder { color: var(--text-muted); opacity: 1; }
        .findings-scope-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(150px, 1fr));
          gap: 12px;
          margin-bottom: var(--space-3);
        }
        .findings-workspace[data-detail="true"] .findings-scope-grid,
        .findings-workspace[data-detail="true"] .findings-filter-grid { grid-template-columns: minmax(0, 1fr); }
        .findings-advanced-filters {
          border-top: var(--hairline) solid var(--border-subtle);
        }
        .findings-advanced-filters summary {
          display: flex;
          min-height: 38px;
          align-items: center;
          justify-content: space-between;
          gap: 10px;
          color: var(--text-secondary);
          font: 650 11.5px/1.3 var(--font-ui);
          cursor: pointer;
          list-style: none;
        }
        .findings-advanced-filters summary::-webkit-details-marker { display: none; }
        .findings-advanced-filters summary svg { color: var(--text-muted); transition: transform 180ms ease-out; }
        .findings-advanced-filters[open] summary svg { transform: rotate(180deg); }
        .findings-filter-grid {
          display: grid;
          grid-template-columns: minmax(260px, 1.5fr) repeat(2, minmax(145px, .7fr));
          gap: 12px;
          align-items: end;
          padding-top: var(--space-3);
          border-top: var(--hairline) solid var(--border-subtle);
        }
        .findings-filter-group { min-width: 0; margin: 0; padding: 0; border: 0; }
        .findings-filter-group legend,
        .findings-filter-label {
          display: block;
          margin-bottom: 6px;
          color: var(--text-muted);
          font: 700 10px/1.2 var(--font-ui);
          letter-spacing: .035em;
          text-transform: uppercase;
        }
        .findings-severity-controls { display: flex; min-height: 38px; gap: 5px; flex-wrap: wrap; }
        .findings-severity-controls button,
        .findings-signal-filter {
          display: inline-flex;
          min-height: 36px;
          align-items: center;
          justify-content: center;
          gap: 6px;
          border-radius: 8px;
          padding: 7px 10px;
          font: 700 10px/1 var(--font-ui);
          cursor: pointer;
        }
        .findings-filter-control {
          width: 100%;
          min-height: 38px;
          border: var(--hairline) solid var(--border-subtle);
          border-radius: 8px;
          padding: 0 10px;
          color: var(--text-secondary);
          background: var(--bg-app);
          font: 500 12px/1.2 var(--font-ui);
          outline: none;
          cursor: pointer;
        }
        .findings-filter-control:focus-visible,
        .findings-severity-controls button:focus-visible,
        .findings-signal-filter:focus-visible,
        .finding-card:focus-visible,
        .findings-clear-filter:focus-visible,
        .findings-inline-action:focus-visible,
        .findings-advanced-filters summary:focus-visible,
        .finding-overview-disclosure summary:focus-visible,
        .finding-ai-triage summary:focus-visible {
          outline: 2px solid var(--accent);
          outline-offset: 2px;
        }
        .findings-signal-filters {
          display: flex;
          align-items: center;
          gap: 7px;
          flex-wrap: wrap;
          margin-top: var(--space-3);
          padding-top: var(--space-3);
          border-top: var(--hairline) solid var(--border-subtle);
        }
        .findings-signal-filters > span {
          margin-right: 2px;
          color: var(--text-muted);
          font: 700 10px/1 var(--font-ui);
          letter-spacing: .035em;
          text-transform: uppercase;
        }
        .findings-spinner { animation: findings-spin 850ms linear infinite; }
        @keyframes findings-spin { to { transform: rotate(360deg); } }
        .finding-card {
          border: var(--hairline) solid var(--border-subtle);
          border-radius: 10px;
          padding: 12px 13px;
          background: var(--bg-panel);
          cursor: pointer;
        }
        .finding-card:hover { border-color: var(--border-strong); background: var(--bg-hover); }
        .finding-card[data-selected="true"] { border-color: var(--accent); background: var(--accent-ghost); }
        .finding-card-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 14px; }
        .finding-card-badges { display: flex; min-width: 0; flex: 1; align-items: center; gap: 5px; flex-wrap: wrap; }
        .finding-card-risk { flex: 0 0 auto; text-align: right; }
        .finding-card-risk strong { display: block; font: 750 16px/1 var(--font-mono); font-variant-numeric: tabular-nums; }
        .finding-card-risk span { display: block; margin-top: 4px; color: var(--text-muted); font: 700 9px/1 var(--font-ui); letter-spacing: .03em; text-transform: uppercase; }
        .finding-card-title { margin: 8px 0 5px; color: var(--text-primary); font: 650 14px/1.35 var(--font-ui); }
        .finding-card-context { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
        .finding-card-host { min-width: 0; overflow: hidden; color: var(--text-muted); font: 500 11px/1.3 var(--font-mono); text-overflow: ellipsis; white-space: nowrap; }
        .finding-card-meta {
          display: flex;
          gap: 5px 12px;
          flex-wrap: wrap;
          margin-top: 9px;
          padding-top: 8px;
          border-top: var(--hairline) solid var(--border-subtle);
          color: var(--text-secondary);
          font: 500 10.5px/1.35 var(--font-mono);
        }
        .finding-card-meta b { color: var(--text-muted); font-weight: 650; }
        .finding-card-meta i { font-style: normal; font-weight: 650; }
        .finding-card-alerts { display: flex; gap: 5px 10px; flex-wrap: wrap; margin-top: 7px; color: var(--sev-high-color); font: 600 10px/1.3 var(--font-ui); }
        .finding-card-alerts span { display: inline-flex; align-items: center; gap: 4px; }
        .finding-action-bar {
          display: grid;
          grid-template-columns: minmax(190px, .72fr) minmax(0, 1.28fr);
          gap: 12px 18px;
          align-items: center;
          padding: 12px 18px;
          border-bottom: var(--hairline) solid var(--border-subtle);
          background: var(--bg-panel);
        }
        .finding-action-bar > div:first-child { display: flex; min-width: 0; flex-direction: column; gap: 3px; }
        .finding-action-bar > div:first-child strong { color: var(--text-primary); font: 650 13px/1.3 var(--font-ui); }
        .finding-action-bar > div:first-child span { color: var(--text-muted); font: 400 11px/1.45 var(--font-ui); }
        .finding-action-select { display: grid; grid-template-columns: auto minmax(180px, 280px); align-items: center; justify-content: end; gap: 9px; }
        .finding-action-select > span { color: var(--text-muted); font: 650 10px/1.2 var(--font-ui); text-transform: uppercase; letter-spacing: .035em; }
        .finding-action-select select {
          min-height: 36px;
          border: var(--hairline) solid var(--border-default);
          border-radius: 8px;
          padding: 0 10px;
          color: var(--text-primary);
          background: var(--bg-app);
          font: 550 12px/1.2 var(--font-ui);
          cursor: pointer;
        }
        .finding-action-select select:disabled { cursor: wait; opacity: .55; }
        .finding-action-composer {
          grid-column: 1 / -1;
          display: grid;
          grid-template-columns: minmax(210px, .72fr) minmax(0, 1.28fr);
          gap: 10px 18px;
          align-items: start;
          padding-top: 12px;
          border-top: var(--hairline) solid var(--border-subtle);
        }
        .finding-action-composer label { display: block; color: var(--text-primary); font: 650 12px/1.3 var(--font-ui); }
        .finding-action-composer p { margin: 4px 0 0; color: var(--text-muted); font: 400 11px/1.45 var(--font-ui); }
        .finding-action-composer textarea {
          width: 100%;
          min-height: 78px;
          resize: vertical;
          border: var(--hairline) solid var(--border-default);
          border-radius: 8px;
          padding: 10px 11px;
          color: var(--text-primary);
          background: var(--bg-app);
          font: 400 12px/1.5 var(--font-ui);
          caret-color: var(--accent);
        }
        .finding-action-composer textarea::placeholder { color: var(--text-muted); opacity: 1; }
        .finding-action-composer-footer { grid-column: 2; display: flex; align-items: center; justify-content: flex-end; gap: 8px; }
        .finding-action-composer-footer > span { margin-right: auto; color: var(--text-muted); font: 500 9px/1.2 var(--font-mono); }

        .finding-overview-view { display: grid; gap: 18px; }
        .finding-overview-view h3 { margin: 0; color: var(--text-primary); font: 650 15.5px/1.35 var(--font-ui); letter-spacing: -.012em; }
        .finding-overview-view h4 { margin: 0; color: var(--text-primary); font: 650 12.5px/1.35 var(--font-ui); }
        .finding-overview-primary { display: grid; gap: 18px; }
        .finding-overview-primary section + section { padding-top: 18px; border-top: var(--hairline) solid var(--border-subtle); }
        .finding-overview-primary p,
        .finding-overview-technical-narrative p { max-width: 72ch; margin: 7px 0 0; color: var(--text-secondary); font: 400 14px/1.65 var(--font-ui); }
        .finding-overview-next-action h3 { color: var(--accent); }
        .finding-overview-next-action p { color: var(--text-primary); font-weight: 500; }
        .finding-overview-facts,
        .finding-overview-technical-grid dl { display: grid; gap: 0; margin: 0; }
        .finding-overview-facts { grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: var(--hairline) solid var(--border-subtle); border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-overview-facts > div,
        .finding-overview-technical-grid dl > div { display: grid; grid-template-columns: minmax(88px, .62fr) minmax(0, 1fr); gap: 12px; padding: 8px 0; border-top: var(--hairline) solid var(--border-subtle); }
        .finding-overview-facts > div { display: block; padding: 10px 12px; border-top: 0; }
        .finding-overview-facts > div:nth-child(3n + 1) { padding-left: 0; }
        .finding-overview-facts > div:nth-child(-n + 3) { border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-overview-facts dt,
        .finding-overview-technical-grid dt { color: var(--text-muted); font: 600 11px/1.4 var(--font-ui); }
        .finding-overview-facts dd,
        .finding-overview-technical-grid dd { min-width: 0; margin: 0; overflow-wrap: anywhere; color: var(--text-primary); font: 550 12px/1.5 var(--font-ui); }
        .finding-overview-facts dd { margin-top: 3px; }
        .finding-overview-technical-grid dd code { font: 500 10px/1.55 var(--font-mono); }
        .finding-overview-disclosure { border-top: var(--hairline) solid var(--border-subtle); }
        .finding-overview-disclosure summary { display: flex; min-height: 44px; align-items: center; justify-content: space-between; gap: 10px; color: var(--text-primary); font: 650 12.5px/1.3 var(--font-ui); cursor: pointer; list-style: none; }
        .finding-overview-disclosure summary::-webkit-details-marker { display: none; }
        .finding-overview-disclosure summary > span { display: inline-flex; align-items: center; gap: 7px; }
        .finding-overview-disclosure summary span svg { color: var(--accent); }
        .finding-overview-disclosure summary > svg { color: var(--text-muted); transition: transform 180ms ease-out; }
        .finding-overview-disclosure[open] summary > svg { transform: rotate(180deg); }
        .finding-overview-disclosure[open] summary { border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-overview-technical-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
        .finding-overview-technical-grid,
        .finding-attack-context { padding: 16px 0 2px; }
        .finding-overview-technical-grid > section > h3 { margin-bottom: 9px; }
        .finding-overview-risk-factors,
        .finding-overview-technical-narrative { grid-column: 1 / -1; }
        .finding-attack-context-grid { display: grid; grid-template-columns: minmax(220px, .72fr) minmax(0, 1.28fr); gap: 24px; }
        .finding-attack-context-grid h4, .finding-related-list h4 { margin-bottom: 9px; }
        .finding-mitre-row { display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 8px; padding: 6px 0; border-top: var(--hairline) solid var(--border-subtle); }
        .finding-mitre-row code { color: var(--accent); font: 600 10px/1.4 var(--font-mono); }
        .finding-mitre-row span { color: var(--text-secondary); font: 400 12px/1.45 var(--font-ui); }
        .finding-overview-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 12px; }
        .finding-overview-tags span { border: var(--hairline) solid var(--border-subtle); border-radius: 5px; padding: 3px 6px; color: var(--text-secondary); background: var(--bg-surface); font: 500 9px/1.2 var(--font-mono); }
        .finding-related-list { margin-top: 18px; }
        .finding-related-list > div { display: grid; grid-template-columns: 7px minmax(90px, .5fr) minmax(0, 1fr) auto; gap: 8px; align-items: center; padding: 7px 0; border-top: var(--hairline) solid var(--border-subtle); }
        .finding-related-list > div > span { width: 7px; height: 7px; border-radius: 2px; }
        .finding-related-list code { color: var(--accent); font: 500 9px/1.3 var(--font-mono); }
        .finding-related-list strong { overflow: hidden; color: var(--text-primary); font: 550 11px/1.3 var(--font-ui); text-overflow: ellipsis; white-space: nowrap; }

        .finding-evidence-view { display: grid; gap: 18px; }
        .finding-evidence-summary { display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; padding-bottom: 16px; border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-evidence-summary-copy { display: flex; min-width: 0; align-items: flex-start; gap: 10px; }
        .finding-evidence-summary-icon { display: grid; width: 32px; height: 32px; flex: 0 0 auto; place-items: center; border-radius: 8px; color: var(--accent); background: var(--accent-ghost); }
        .finding-evidence-summary h3 { margin: 0; color: var(--text-primary); font: 650 15px/1.35 var(--font-ui); }
        .finding-evidence-summary p { max-width: 64ch; margin: 5px 0 0; color: var(--text-secondary); font: 400 12.5px/1.55 var(--font-ui); }
        .finding-evidence-summary dl { display: flex; flex: 0 0 auto; gap: 18px; margin: 0; }
        .finding-evidence-summary dl > div { display: grid; min-width: 48px; gap: 3px; }
        .finding-evidence-summary dt { color: var(--text-muted); font: 650 9px/1.25 var(--font-ui); text-transform: uppercase; letter-spacing: .045em; }
        .finding-evidence-summary dd { margin: 0; color: var(--text-primary); font: 700 13px/1.3 var(--font-mono); font-variant-numeric: tabular-nums; }
        .finding-evidence-empty { display: flex; align-items: flex-start; gap: 11px; border: var(--hairline) solid var(--border-default); border-radius: 10px; padding: 17px 18px; background: var(--bg-surface); }
        .finding-evidence-empty > svg { flex: 0 0 auto; margin-top: 1px; color: var(--text-muted); }
        .finding-evidence-empty h3 { margin: 0; color: var(--text-primary); font: 650 14px/1.4 var(--font-ui); }
        .finding-evidence-empty p { max-width: 64ch; margin: 5px 0 0; color: var(--text-secondary); font: 400 12.5px/1.55 var(--font-ui); }
        .finding-evidence-artifact { overflow: hidden; border: var(--hairline) solid var(--border-default); border-radius: 10px; background: var(--bg-panel); }
        .finding-evidence-artifact > header { display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 12px 14px; border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-evidence-identity { display: flex; min-width: 0; align-items: center; gap: 10px; }
        .finding-evidence-kind { flex: 0 0 auto; border-radius: 5px; padding: 4px 6px; color: var(--machine-text); background: var(--machine-bg); font: 700 9px/1 var(--font-mono); letter-spacing: .035em; }
        .finding-evidence-artifact h3 { overflow: hidden; margin: 0; color: var(--text-primary); font: 650 13.5px/1.35 var(--font-ui); text-overflow: ellipsis; white-space: nowrap; }
        .finding-evidence-artifact header p { margin: 3px 0 0; color: var(--text-muted); font: 500 9.5px/1.3 var(--font-mono); font-variant-numeric: tabular-nums; }
        .finding-evidence-copy { display: inline-flex; min-height: 30px; flex: 0 0 auto; align-items: center; gap: 6px; border: var(--hairline) solid var(--border-default); border-radius: 7px; padding: 0 9px; color: var(--text-secondary); background: var(--bg-panel); cursor: pointer; font: 600 10.5px/1 var(--font-ui); }
        .finding-evidence-copy:hover { color: var(--text-primary); background: var(--bg-hover); }
        .finding-evidence-copy:focus-visible { outline: 0; box-shadow: var(--focus-ring); }
        .finding-evidence-provenance { display: flex; flex-wrap: wrap; gap: 10px 24px; margin: 0; padding: 10px 14px; border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-evidence-provenance > div { display: grid; max-width: 280px; min-width: 92px; gap: 3px; }
        .finding-evidence-provenance dt { color: var(--text-muted); font: 650 8.5px/1.2 var(--font-ui); text-transform: uppercase; letter-spacing: .045em; }
        .finding-evidence-provenance dd { overflow: hidden; margin: 0; color: var(--text-secondary); font: 500 10px/1.35 var(--font-mono); text-overflow: ellipsis; white-space: nowrap; }
        .finding-evidence-provenance-empty { margin: 0; padding: 9px 14px; border-bottom: var(--hairline) solid var(--border-subtle); color: var(--text-muted); font: 400 10.5px/1.45 var(--font-ui); }
        .finding-evidence-command { display: grid; grid-template-columns: auto auto minmax(0, 1fr); gap: 7px; align-items: start; padding: 9px 14px; border-bottom: var(--hairline) solid var(--border-subtle); background: var(--bg-surface); }
        .finding-evidence-command svg { margin-top: 1px; color: var(--machine-color); }
        .finding-evidence-command span { color: var(--text-muted); font: 650 9px/1.45 var(--font-ui); text-transform: uppercase; letter-spacing: .035em; }
        .finding-evidence-command code { overflow-wrap: anywhere; color: var(--text-primary); font: 500 10.5px/1.45 var(--font-mono); }
        .finding-evidence-output-heading { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 14px; background: var(--bg-surface); }
        .finding-evidence-output-heading span:first-child { color: var(--text-secondary); font: 650 9px/1.3 var(--font-ui); text-transform: uppercase; letter-spacing: .045em; }
        .finding-evidence-output-heading span:last-child { color: var(--text-muted); font: 500 9px/1.3 var(--font-ui); }
        .finding-evidence-code { max-height: 390px; overflow: auto; border-top: var(--hairline) solid var(--border-subtle); border-bottom: var(--hairline) solid var(--border-subtle); background: var(--bg-surface); scrollbar-color: var(--border-strong) var(--bg-surface); }
        .finding-evidence-code > div { display: grid; grid-template-columns: 46px minmax(0, 1fr); min-height: 24px; }
        .finding-evidence-code > div:hover { background: var(--bg-hover); }
        .finding-evidence-code span { padding: 3px 10px 3px 0; color: var(--text-muted); font: 500 9px/1.7 var(--font-mono); text-align: right; user-select: none; font-variant-numeric: tabular-nums; }
        .finding-evidence-code code { padding: 3px 14px; border-left: var(--hairline) solid var(--border-subtle); color: var(--text-primary); font: 500 11px/1.7 var(--font-mono); white-space: pre-wrap; overflow-wrap: anywhere; }
        .finding-evidence-artifact-empty { padding: 22px 14px; border-top: var(--hairline) solid var(--border-subtle); border-bottom: var(--hairline) solid var(--border-subtle); color: var(--text-muted); background: var(--bg-surface); font: 400 11.5px/1.5 var(--font-ui); }
        .finding-evidence-artifact > footer { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 14px; color: var(--text-muted); font: 500 9.5px/1.35 var(--font-ui); }

        .finding-remediation-view { display: grid; gap: 22px; }
        .finding-remediation-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 22px; padding-bottom: 16px; border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-remediation-title { display: flex; align-items: center; gap: 8px; }
        .finding-remediation-title svg { color: var(--accent); }
        .finding-remediation-header h3, .finding-remediation-section h3, .finding-remediation-note h3, .finding-remediation-closeout h3 { margin: 0; color: var(--text-primary); font: 650 15px/1.35 var(--font-ui); }
        .finding-remediation-header > div > p { max-width: 72ch; margin: 8px 0 0; color: var(--text-secondary); font: 400 13.5px/1.6 var(--font-ui); }
        .finding-remediation-meta { display: flex; flex-wrap: wrap; gap: 6px 12px; margin-top: 9px; color: var(--text-muted); font: 500 9px/1.3 var(--font-mono); text-transform: capitalize; }
        .finding-remediation-os { display: grid; min-width: 170px; gap: 5px; color: var(--text-muted); font: 650 9px/1.2 var(--font-ui); text-transform: uppercase; letter-spacing: .04em; }
        .finding-remediation-os select { min-height: 36px; border: var(--hairline) solid var(--border-default); border-radius: 8px; padding: 0 9px; color: var(--text-primary); background: var(--bg-app); font: 500 11px/1.2 var(--font-ui); }
        .finding-remediation-note { padding: 13px 14px; border-radius: 9px; background: var(--bg-surface); }
        .finding-remediation-note h3 { font-size: 13px; }
        .finding-remediation-note p { margin: 7px 0 0; color: var(--text-secondary); font: 400 12.5px/1.6 var(--font-ui); white-space: pre-wrap; }
        .finding-remediation-section { min-width: 0; }
        .finding-remediation-steps { display: grid; }
        .finding-remediation-steps > article { display: grid; grid-template-columns: 30px minmax(0, 1fr); gap: 12px; padding: 15px 0; border-top: var(--hairline) solid var(--border-subtle); }
        .finding-remediation-step-number { display: grid; width: 28px; height: 28px; place-items: center; border-radius: 7px; color: var(--accent); background: var(--accent-ghost); font: 700 10px/1 var(--font-mono); }
        .finding-remediation-steps article header { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
        .finding-remediation-steps h4 { margin: 0; color: var(--text-primary); font: 650 13.5px/1.4 var(--font-ui); }
        .finding-remediation-steps header span { color: var(--text-secondary); font: 600 9px/1.2 var(--font-ui); text-transform: uppercase; }
        .finding-remediation-steps header span[data-risk="medium"] { color: var(--sev-medium-color); }
        .finding-remediation-steps header span[data-risk="high"] { color: var(--sev-critical-color); }
        .finding-remediation-steps article p { margin: 6px 0 0; color: var(--text-secondary); font: 400 12.5px/1.6 var(--font-ui); }
        .finding-remediation-commands { display: grid; gap: 5px; margin-top: 10px; }
        .finding-remediation-commands > div { display: flex; align-items: flex-start; gap: 8px; border: var(--hairline) solid var(--border-subtle); border-radius: 7px; padding: 7px 8px 7px 10px; background: var(--bg-surface); }
        .finding-remediation-commands code { min-width: 0; flex: 1; overflow-wrap: anywhere; color: var(--text-primary); font: 500 10px/1.55 var(--font-mono); white-space: pre-wrap; }
        .finding-remediation-verify, .finding-remediation-warning { display: flex; align-items: flex-start; gap: 7px; margin-top: 9px; color: var(--text-secondary); font: 400 11.5px/1.5 var(--font-ui); }
        .finding-remediation-verify svg { flex: 0 0 auto; margin-top: 1px; color: var(--nominal-color); }
        .finding-remediation-warning { color: var(--sev-high-color); }
        .finding-remediation-warning svg { flex: 0 0 auto; margin-top: 1px; }
        .finding-remediation-closeout { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; border-top: var(--hairline) solid var(--border-subtle); border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-remediation-closeout section { padding: 15px; }
        .finding-remediation-closeout section + section { border-left: var(--hairline) solid var(--border-subtle); }
        .finding-remediation-closeout h3 { font-size: 13px; }
        .finding-remediation-closeout p, .finding-remediation-closeout li { color: var(--text-secondary); font: 400 11.5px/1.55 var(--font-ui); }
        .finding-remediation-closeout p { margin: 7px 0 0; }
        .finding-remediation-closeout ol, .finding-remediation-closeout ul { margin: 7px 0 0; padding-left: 18px; }

        .finding-history-view { display: grid; gap: 18px; }
        .finding-history-summary { display: flex; align-items: flex-start; justify-content: space-between; gap: 18px; padding-bottom: 15px; border-bottom: var(--hairline) solid var(--border-subtle); }
        .finding-history-summary h3 { margin: 0; color: var(--text-primary); font: 650 15px/1.35 var(--font-ui); }
        .finding-history-summary p { max-width: 60ch; margin: 6px 0 0; color: var(--text-muted); font: 400 12.5px/1.55 var(--font-ui); }
        .finding-history-summary dl { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 10px 18px; margin: 0; }
        .finding-history-summary dl > div { display: grid; gap: 3px; }
        .finding-history-summary dt { color: var(--text-muted); font: 650 10px/1.25 var(--font-ui); text-transform: uppercase; letter-spacing: .035em; }
        .finding-history-summary dd { margin: 0; color: var(--text-primary); font: 600 11px/1.35 var(--font-mono); }
        .finding-history-action { margin: 5px 0 0; color: var(--text-primary); font: 500 13.5px/1.5 var(--font-ui); }
        .finding-history-actor { display: flex; flex-wrap: wrap; gap: 6px 10px; margin-top: 6px; color: var(--text-muted); font: 500 10px/1.4 var(--font-mono); }
        .finding-history-actor span:first-child { color: var(--accent); }
        .finding-history-timeline blockquote { display: grid; grid-template-columns: 58px minmax(0, 1fr); gap: 8px; margin: 9px 0 0; border: 0; border-radius: 7px; padding: 8px 10px; background: var(--bg-surface); }
        .finding-history-timeline blockquote strong { color: var(--text-muted); font: 650 9px/1.4 var(--font-ui); text-transform: uppercase; }
        .finding-history-timeline blockquote span { color: var(--text-primary); font: 400 12.5px/1.55 var(--font-ui); }
        .finding-history-details { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0 0; }
        .finding-history-details > div { display: flex; gap: 4px; border: var(--hairline) solid var(--border-subtle); border-radius: 5px; padding: 3px 6px; background: var(--bg-app); }
        .finding-history-details dt { color: var(--text-muted); font: 600 9px/1.35 var(--font-ui); }
        .finding-history-details dd { margin: 0; color: var(--text-secondary); font: 500 9px/1.35 var(--font-mono); }
        @media (max-width: 1180px) {
          .findings-filter-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .finding-attack-context-grid { grid-template-columns: minmax(0, 1fr); }
          .finding-remediation-closeout { grid-template-columns: minmax(0, 1fr); }
          .finding-remediation-closeout section + section { border-top: var(--hairline) solid var(--border-subtle); border-left: 0; }
          .finding-detail-header { padding-right: 18px; padding-left: 18px; }
          .finding-ai-triage summary { padding-right: 18px; padding-left: 18px; }
          .finding-ai-triage-content { padding-right: 18px; padding-left: 39px; }
          .finding-detail-content { padding: 18px; }
        }
        @media (max-width: 920px) {
          .findings-workspace[data-detail="true"] { grid-template-columns: minmax(0, 1fr); }
          .finding-detail-column {
            position: static;
            max-height: none;
            overflow: visible;
            overscroll-behavior: auto;
            scrollbar-gutter: auto;
          }
          .finding-action-bar, .finding-action-composer { grid-template-columns: minmax(0, 1fr); }
          .finding-action-select { justify-content: start; }
          .finding-action-composer-footer { grid-column: 1; }
          .finding-overview-technical-grid { grid-template-columns: minmax(0, 1fr); }
          .finding-overview-risk-factors,
          .finding-overview-technical-narrative { grid-column: auto; }
        }
        @media (max-width: 620px) {
          .findings-filter-grid { grid-template-columns: minmax(0, 1fr); }
          .findings-scope-grid { grid-template-columns: minmax(0, 1fr); }
          .findings-filter-header { align-items: center; }
          .finding-card-header, .finding-card-context { align-items: flex-start; }
          .finding-card-context { flex-direction: column; gap: 8px; }
          .finding-overview-facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .finding-overview-facts > div:nth-child(3n + 1) { padding-left: 12px; }
          .finding-overview-facts > div:nth-child(2n + 1) { padding-left: 0; }
          .finding-overview-facts > div:nth-child(-n + 4) { border-bottom: var(--hairline) solid var(--border-subtle); }
          .finding-action-composer-footer { align-items: stretch; flex-wrap: wrap; }
          .finding-action-composer-footer > span { width: 100%; margin: 0; }
          .finding-remediation-header, .finding-history-summary, .finding-evidence-summary { flex-direction: column; }
          .finding-remediation-os { width: 100%; }
          .finding-history-summary dl { justify-content: flex-start; }
          .finding-evidence-summary { gap: 14px; }
          .finding-evidence-summary dl { width: 100%; justify-content: space-between; }
          .finding-evidence-artifact > header { align-items: flex-start; }
          .finding-evidence-identity { align-items: flex-start; }
          .finding-evidence-output-heading, .finding-evidence-artifact > footer { align-items: flex-start; flex-direction: column; gap: 4px; }
          .finding-evidence-command { grid-template-columns: auto minmax(0, 1fr); }
          .finding-evidence-command code { grid-column: 1 / -1; }
          .finding-evidence-code > div { grid-template-columns: 36px minmax(0, 1fr); }
          .finding-evidence-code span { padding-right: 7px; }
          .finding-evidence-code code { padding-right: 10px; padding-left: 10px; font-size: 10.5px; }
          .finding-related-list > div { grid-template-columns: 7px minmax(0, 1fr) auto; }
          .finding-related-list code { display: none; }
          .finding-detail-header { padding-right: 16px; padding-left: 16px; }
          .finding-ai-triage summary { padding-right: 16px; padding-left: 16px; }
          .finding-ai-triage-content { padding-right: 16px; padding-left: 37px; }
          .finding-detail-title { max-width: none; font-size: 18px; }
          .finding-detail-content { padding: 16px; }
        }
        @media (prefers-reduced-motion: reduce) {
          .findings-spinner { animation-duration: 1.6s; }
          .findings-advanced-filters summary svg,
          .finding-overview-disclosure summary > svg,
          .finding-ai-triage summary svg:last-child { transition: none; }
          .finding-detail-panel { animation: none; }
        }
      `}</style>
      {engagementId && (
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, flexWrap: "wrap", marginBottom: 12, padding: "10px 14px", background: "var(--accent-ghost)", border: "var(--hairline) solid var(--border-accent)", borderRadius: 8 }}>
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

      <div className="findings-workspace" data-detail={selected ? "true" : "false"}>

        {/* ── Left: List ── */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>

          {/* Filters */}
          <section className="findings-filter-panel" aria-labelledby="finding-queue-title">
            <header className="findings-filter-header">
              <div>
                <h2 id="finding-queue-title">Analyst queue</h2>
                <p aria-live="polite">
                  {error
                    ? "Queue unavailable — retry to verify the current state."
                    : isLoading
                      ? "Loading ranked findings…"
                      : total === 0
                        ? "No findings match the current scope."
                        : `${total.toLocaleString()} matching · page ${currentPage} of ${pageCount}`}
                </p>
              </div>
              {hasActiveFilters && (
                <button type="button" className="findings-clear-filter" onClick={clearFilters}>
                  <RotateCcw size={13} aria-hidden /> Clear filters
                </button>
              )}
            </header>

            <div className="findings-search">
              <Search size={15} color="var(--text-muted)" aria-hidden />
              <input value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); setSelectedId(null); }} placeholder="Search title, CVE, or finding ID…"
                aria-label="Search findings"
              />
            </div>

            <div className="findings-scope-grid" aria-label="Finding source scope">
              <label className="findings-filter-group">
                <span className="findings-filter-label">Engagement</span>
                <select
                  className="findings-filter-control"
                  value={engagementId ?? ""}
                  onChange={(event) => {
                    setEngagementId(event.target.value || null);
                    setPage(1);
                    setSelectedId(null);
                  }}
                  disabled={engagementOptionsQuery.isLoading}
                >
                  <option value="">All engagements</option>
                  {(engagementOptionsQuery.data?.engagements ?? []).map((engagement) => (
                    <option key={engagement.id} value={engagement.id}>{engagement.name}</option>
                  ))}
                </select>
              </label>

              <label className="findings-filter-group">
                <span className="findings-filter-label">Vedha agent</span>
                <select
                  className="findings-filter-control"
                  value={filterAgentId}
                  onChange={(event) => {
                    setFilterAgentId(event.target.value);
                    setPage(1);
                    setSelectedId(null);
                  }}
                  disabled={agentOptionsQuery.isLoading}
                >
                  <option value="">All Vedha agents</option>
                  {(agentOptionsQuery.data ?? []).map((agent) => (
                    <option key={agent.id} value={agent.id}>
                      {agent.name} · {agent.status.toLowerCase()}
                    </option>
                  ))}
                </select>
              </label>

              <label className="findings-filter-group">
                <span className="findings-filter-label">Sort</span>
                <select className="findings-filter-control" value={sortBy} onChange={(e) => { setSortBy(e.target.value as typeof sortBy); setPage(1); setSelectedId(null); }}>
                  <option value="risk">Risk: highest first</option>
                  <option value="cvss">CVSS: highest first</option>
                  <option value="epss">EPSS: highest first</option>
                  <option value="date">Newest first</option>
                </select>
              </label>
            </div>

            <details className="findings-advanced-filters">
              <summary>
                <span>More filters{advancedFilterCount > 0 ? ` · ${advancedFilterCount} active` : ""}</span>
                <ChevronDown size={15} aria-hidden />
              </summary>
              <div className="findings-filter-grid">
              <fieldset className="findings-filter-group">
                <legend>Severity</legend>
                <div className="findings-severity-controls">
                  {(["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"] as const).map((s) => (
                    <button type="button" key={s} aria-pressed={filterSev === s} onClick={() => { setFilterSev(s); setPage(1); setSelectedId(null); }} style={{
                      border: `1px solid ${filterSev === s ? (s === "ALL" ? "var(--accent)" : SEV_COLOR[s as Severity]) : "var(--border-subtle)"}`,
                      background: filterSev === s ? (s === "ALL" ? "var(--accent-ghost)" : tint(SEV_COLOR[s as Severity], 8)) : "transparent",
                      color: filterSev === s ? (s === "ALL" ? "var(--accent)" : SEV_COLOR[s as Severity]) : "var(--text-secondary)",
                    }}>{s === "ALL" ? "All" : s}</button>
                  ))}
                </div>
              </fieldset>

              <label className="findings-filter-group">
                <span className="findings-filter-label">Lifecycle</span>
                <select className="findings-filter-control" value={filterStatus} onChange={(e) => { setFilterStatus(e.target.value as FindingStatus | "ALL"); setPage(1); setSelectedId(null); }}>
                  {(["ALL", "OPEN", "CONFIRMED", "REMEDIATED", "ACCEPTED", "FALSE_POSITIVE"] as const).map((s) => (
                    <option key={s} value={s}>{s === "ALL" ? "All statuses" : STATUS_LABEL[s]}</option>
                  ))}
                </select>
              </label>

              <label className="findings-filter-group">
                <span className="findings-filter-label">Evidence</span>
                <select className="findings-filter-control" value={filterVerification} onChange={(e) => { setFilterVerification(e.target.value); setPage(1); setSelectedId(null); }}>
                  {["ALL", "confirmed", "corroborated", "inferred", "contradicted"].map((s) => (
                    <option key={s} value={s}>{s === "ALL" ? "All verdicts" : s.charAt(0).toUpperCase() + s.slice(1)}</option>
                  ))}
                </select>
              </label>

            </div>

            <div className="findings-signal-filters" aria-label="Risk signal filters">
              <span>Signals</span>
              <button type="button" className="findings-signal-filter" aria-pressed={filterExploited} onClick={() => { setFilterExploited((p) => !p); setPage(1); setSelectedId(null); }} style={{
                border: `1px solid ${filterExploited ? tint(SEV_PALETTE.RED, 40) : "var(--border-subtle)"}`,
                background: filterExploited ? tint(SEV_PALETTE.RED, 8) : "transparent",
                color: filterExploited ? SEV_PALETTE.RED : "var(--text-secondary)",
              }}><BadgeCheck size={13} aria-hidden /> Exploit confirmed</button>
              <button type="button" className="findings-signal-filter" aria-pressed={filterBlind} onClick={() => { setFilterBlind((p) => !p); setPage(1); setSelectedId(null); }} style={{
                border: `1px solid ${filterBlind ? tint(SEV_PALETTE.AMBER, 40) : "var(--border-subtle)"}`,
                background: filterBlind ? tint(SEV_PALETTE.AMBER, 8) : "transparent",
                color: filterBlind ? SEV_PALETTE.AMBER : "var(--text-secondary)",
              }}><EyeOff size={13} aria-hidden /> Detection blind</button>
              <button type="button" className="findings-signal-filter" aria-pressed={filterSlaBreached} onClick={() => { setFilterSlaBreached((p) => !p); setPage(1); setSelectedId(null); }} style={{
                border: `1px solid ${filterSlaBreached ? tint(SEV_PALETTE.RED, 40) : "var(--border-subtle)"}`,
                background: filterSlaBreached ? tint(SEV_PALETTE.RED, 8) : "transparent",
                color: filterSlaBreached ? SEV_PALETTE.RED : "var(--text-secondary)",
              }}><AlertTriangle size={13} aria-hidden /> SLA breached</button>
              <button type="button" className="findings-signal-filter" aria-pressed={filterNeedsReview} onClick={() => { setFilterNeedsReview((p) => !p); setPage(1); setSelectedId(null); }} style={{
                border: `1px solid ${filterNeedsReview ? tint(SEV_PALETTE.AMBER, 40) : "var(--border-subtle)"}`,
                background: filterNeedsReview ? tint(SEV_PALETTE.AMBER, 8) : "transparent",
                color: filterNeedsReview ? SEV_PALETTE.AMBER : "var(--text-secondary)",
              }}><Flag size={13} aria-hidden /> Needs review</button>
            </div>
            </details>
          </section>

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
              return (
                <div
                  key={f.id}
                  className="finding-card stagger-item"
                  data-selected={isSelected}
                  role="button"
                  tabIndex={0}
                  aria-expanded={isSelected}
                  aria-label={`${f.title}, ${f.severity}, ${f.aiTriage.priority} ${PRIORITY_LABEL[f.aiTriage.priority]}, risk ${f.riskScore} of 1000`}
                  onClick={() => setSelectedId(isSelected ? null : f.id)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") {
                      event.preventDefault();
                      setSelectedId(isSelected ? null : f.id);
                    }
                  }}
                >
                  <div className="finding-card-header">
                    <div className="finding-card-badges">
                      <SevBadge s={f.severity} />
                      <StatusBadge s={f.status} />
                      {f.kevStatusRecorded && f.kevListed && <KevBadge />}
                    </div>
                    <div className="finding-card-risk">
                      <strong style={{ color: riskScoreColor(f.riskScore) }}>{f.riskScore}</strong>
                      <span>Risk /1000</span>
                    </div>
                  </div>

                  <h3 className="finding-card-title">{f.title}</h3>

                  <div className="finding-card-context">
                    <span className="finding-card-host" title={f.affectedHost}>{f.affectedHost}</span>
                    <PriorityBadge priority={f.aiTriage.priority} compact />
                  </div>

                  <div className="finding-card-meta" aria-label="Finding signals">
                    <span><b>CVSS</b> {f.cvss || "—"}</span>
                    <span><b>EPSS</b> <i style={{ color: f.epssRecorded ? epssColor(f.epssScore) : "var(--text-muted)" }}>{f.epssRecorded ? `${(f.epssScore * 100).toFixed(1)}%` : "—"}</i></span>
                    <span><b>SLA</b> <i style={{ color: sla.color }}>{sla.label}</i></span>
                    <span><b>Evidence</b> {f.verificationState || "Unassessed"}</span>
                  </div>

                  {(f.activelyExploited || f.detectionCoverage === "BLIND" || f.needsReview || f.regression) && (
                    <div className="finding-card-alerts" aria-label="Attention signals">
                      {f.activelyExploited && <span><BadgeCheck size={12} /> Exploit confirmed</span>}
                      {f.detectionCoverage === "BLIND" && <span><EyeOff size={12} /> Detection blind</span>}
                      {f.needsReview && <span><Flag size={12} /> Needs review</span>}
                      {f.regression && <span><RotateCcw size={12} /> Regression</span>}
                    </div>
                  )}
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
          <aside
            key={selected.id}
            className="finding-detail-column"
            aria-label={`Details for ${selected.title}`}
          >
            <FindingDetail
              key={selected.id}
              f={selected}
              allFindings={findings}
              onStatusChange={handleStatusChange}
              statusUpdating={statusMutation.isPending}
              onReopen={handleReopen}
              reopening={reopenMutation.isPending}
            />
          </aside>
        )}
      </div>
    </PageShell>
  );
}
