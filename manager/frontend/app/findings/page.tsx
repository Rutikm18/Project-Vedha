"use client";

/* ═════════════════════════════════════════════════════════════════════════════
 * Findings workspace — analyst triage surface
 *
 * Design intent (why this file looks the way it does):
 *
 * 1. One decision per screen region. Strip = "what needs me now", queue =
 *    "what else exists", detail = "what do I do about this one". Nothing that
 *    belongs to one region is repeated in another.
 * 2. Severity is scanned vertically, not read. Each row carries a colour rail
 *    so the eye can run down the left edge without parsing badges.
 * 3. Badges are ranked and capped. An analyst can hold ~4 chips before the row
 *    becomes texture; the rest collapse into a hover-listed "+n".
 * 4. Time is computed once. A single clock feeds every SLA read in a render,
 *    so the strip, the row and the detail can never disagree by a tick.
 * 5. Keyboard first. SOC work is repetitive: "/" search, J/K move, Enter open,
 *    Esc close, [ / ] page. The mouse stays optional.
 * 6. The interface never claims more than the record holds. Missing enrichment
 *    reads as "not recorded", never as "clean" — kept verbatim from the
 *    original because it is a correctness property, not a copy choice.
 *
 * Palette, typefaces, spacing and radii come entirely from the existing token
 * layer (lib/severity + global CSS variables). No new colours, no new fonts.
 * ═══════════════════════════════════════════════════════════════════════════ */

import React, {
  useCallback,
  useDeferredValue,
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
} from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Activity, AlertTriangle, ArrowLeft, BadgeCheck, Brain, Check, CheckCircle,
  ChevronDown, ChevronLeft, ChevronRight, Copy, ExternalLink, EyeOff, FileText, Flag,
  Keyboard, Link2, ListChecks, LoaderCircle, RefreshCw, RotateCcw, Search, Server,
  Shield, SlidersHorizontal, Tag, Terminal, Wrench, X,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { PortalShell } from "../../components/portal/PortalShell";
import { consoleQueryKey } from "../../lib/console-source";
import { useAssistant } from "../../components/assistant/AssistantProvider";
import { useToast } from "../../hooks/useToast";
import { errorMessage, isUnauthorized } from "../../lib/fetcher";
import {
  createFindingsWorkspaceApi,
  portalFindingAssistantHref,
  type FindingsWorkspaceSurface,
} from "../../lib/findings-workspace-api";
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
type FindingsWorkspaceApi = ReturnType<typeof createFindingsWorkspaceApi>;

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
interface ComplianceRef { framework: string; controls?: string[]; refs?: string[]; rationale?: string; }
interface ExploitationView {
  status: "validated" | "not_validated" | string;
  maturity: string;
  actively_exploited: boolean;
  summary: string;
  note: string;
  signals?: Record<string, unknown>;
}
interface EvidenceFact { label: string; value: string; }
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
  evidenceSummary?: EvidenceFact[];
  exploitation?: ExploitationView | null;
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
  openTotal: number;
  criticalOpen: number;
  highOpen: number;
  mediumOpen: number;
  lowOpen: number;
  infoOpen: number;
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

/* ─── Tint scale ───────────────────────────────────────────────────────────
 * The previous code mixed twelve ad-hoc alpha percentages (3/6/7/8/13/15/19/
 * 20/25/27/33/40). Two chips meant to look identical did not, and nothing
 * told the next author which value to reach for. Six named steps, one job
 * each — every tinted surface in this file now resolves to one of them.
 * Semantic colours themselves still come from lib/severity (WCAG-AA source). */
const TINT = {
  wash:   4,   // large background washes behind a whole panel
  fill:   8,   // chip / pill body
  hairline: 16, // 1px borders on chips
  edge:   26,  // borders that must read as an outline, not a hint
  rail:   38,  // solid-ish accents: dots, rails, focus rings
} as const;

const tint = (color: string, strength: number) =>
  `color-mix(in srgb, ${color} ${strength}%, transparent)`;

/* ─── SLA ──────────────────────────────────────────────────────────────────
 * `breached` is returned as a boolean. Three call sites previously compared
 * the display string against "BREACHED", which silently breaks the moment
 * anyone translates or reworded the label. `now` is injected so every SLA
 * read in a single render shares one clock. */
const SLA_HOURS: Partial<Record<Severity, number>> = { CRITICAL: 24, HIGH: 72, MEDIUM: 168, LOW: 720 };

interface Sla { color: string; label: string; pct: number; breached: boolean; tracked: boolean; }

function getSlaColor(discoveredAt: string, severity: Severity, now: number = Date.now()): Sla {
  const slaH = SLA_HOURS[severity];
  if (!slaH) return { color: "var(--text-secondary)", label: "Not tracked", pct: 100, breached: false, tracked: false };
  const due = new Date(discoveredAt).getTime() + slaH * 3_600_000;
  const leftMs = due - now;
  const pct = Math.max(0, Math.min(100, (leftMs / (slaH * 3_600_000)) * 100));
  if (now > due) return { color: SEV_PALETTE.RED, label: "Breached", pct: 0, breached: true, tracked: true };
  const h = Math.round(leftMs / 3_600_000);
  const label = h < 24 ? `${h}h left` : `${Math.round(h / 24)}d left`;
  const color = pct < 10 ? SEV_PALETTE.RED : pct < 25 ? SEV_PALETTE.ORANGE : pct < 50 ? SEV_PALETTE.AMBER : SEV_PALETTE.GREEN;
  return { color, label, pct, breached: false, tracked: true };
}

/* One clock for the whole page. SLA is a live quantity; without this the
 * countdown only moved when React happened to re-render for another reason. */
function useNow(intervalMs = 60_000) {
  const snap = () => Math.floor(Date.now() / intervalMs) * intervalMs;
  const [now, setNow] = useState(snap);
  useEffect(() => {
    const id = window.setInterval(() => setNow(snap()), intervalMs);
    return () => window.clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [intervalMs]);
  return now;
}

function prefersReducedMotion() {
  return typeof window !== "undefined"
    && Boolean(window.matchMedia?.("(prefers-reduced-motion: reduce)").matches);
}

/* ─── Copy button ─────────────────────────────────────────────────────────
 * Was silent to screen readers and left no trace on failure. Now it reports
 * the outcome through a polite live region and degrades honestly when the
 * clipboard API is unavailable (non-secure origins, locked-down kiosks). */
function CopyBtn({ text, label = "command", showLabel = false }: { text: string; label?: string; showLabel?: boolean }) {
  const [state, setState] = useState<"idle" | "copied" | "failed">("idle");
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setState("copied");
    } catch {
      setState("failed");
    }
    window.setTimeout(() => setState("idle"), 2000);
  };
  return (
    <button
      type="button"
      className={`finding-copy-btn${showLabel ? " finding-copy-btn-labelled" : ""}`}
      data-state={state}
      aria-label={state === "copied" ? `Copied ${label}` : `Copy ${label}`}
      onClick={() => { void copy(); }}
    >
      {state === "copied" ? <Check size={12} aria-hidden /> : <Copy size={12} aria-hidden />}
      {showLabel && <span aria-hidden>{state === "copied" ? "Copied" : state === "failed" ? "Try again" : "Copy"}</span>}
      <span className="findings-sr-only" role="status">
        {state === "copied" ? "Copied" : state === "failed" ? "Copy blocked by the browser" : ""}
      </span>
    </button>
  );
}

/* ─── Badges ──────────────────────────────────────────────────────────────
 * All chips share one geometry (height, radius, letter-spacing) so a row of
 * mixed chips reads as a single band instead of a ransom note. */
function SevBadge({ s }: { s: Severity }) {
  const token = s.toLowerCase();
  return (
    <span className="chip chip-sev" style={{
      background: `var(--badge-${token}-bg)`,
      color: `var(--badge-${token}-text)`,
      borderColor: `var(--badge-${token}-edge)`,
    }}>{s}</span>
  );
}

/* Priority is response order, not technical severity. The plain-language
 * meaning always ships with the P-code so the signal is never colour-only
 * or acronym-only. */
function PriorityBadge({ priority, compact = false }: { priority: Priority; compact?: boolean }) {
  const color = PRIORITY_COLOR[priority];
  const label = PRIORITY_LABEL[priority];
  return (
    <span
      className="chip chip-priority"
      data-compact={compact || undefined}
      title={`${priority}: ${label} response priority`}
      style={{ color, background: tint(color, TINT.fill), borderColor: tint(color, TINT.hairline) }}
    >
      <b>{priority}</b>
      <span>{label}</span>
    </span>
  );
}

function RiskBadge({ score }: { score: number }) {
  const c = riskScoreColor(score);
  return (
    <span className="chip" style={{ color: c, background: tint(c, TINT.fill), borderColor: tint(c, TINT.hairline) }}>
      Risk {score}
    </span>
  );
}

function KevBadge() {
  return (
    <span className="chip" title="Listed in the CISA Known Exploited Vulnerabilities catalogue"
      style={{ color: SEV_PALETTE.RED, background: tint(SEV_PALETTE.RED, TINT.fill), borderColor: tint(SEV_PALETTE.RED, TINT.edge) }}>
      <AlertTriangle size={10} aria-hidden /> KEV
    </span>
  );
}

const VERIFICATION_META: Record<string, { label: string; color: string; strike?: boolean }> = {
  confirmed:    { label: "Confirmed",    color: SEV_PALETTE.GREEN },
  corroborated: { label: "Corroborated", color: SEV_PALETTE.GREEN },
  inferred:     { label: "Inferred",     color: SEV_PALETTE.SLATE },
  contradicted: { label: "Contradicted", color: SEV_PALETTE.SLATE, strike: true },
};

function VerificationBadge({ state }: { state?: string | null }) {
  if (!state) return null;
  const m = VERIFICATION_META[state.toLowerCase()];
  if (!m) return null;
  return (
    <span className="chip" title={`Evidence verdict: ${m.label}`} style={{
      color: m.color, background: tint(m.color, TINT.fill), borderColor: tint(m.color, TINT.hairline),
      textDecoration: m.strike ? "line-through" : "none",
    }}>{m.label}</span>
  );
}

function NeedsReviewChip() {
  return (
    <span className="chip" title="High stakes and uncertain — flagged for an analyst"
      style={{ color: SEV_PALETTE.AMBER, background: tint(SEV_PALETTE.AMBER, TINT.fill), borderColor: tint(SEV_PALETTE.AMBER, TINT.edge) }}>
      <Flag size={10} aria-hidden /> Needs review
    </span>
  );
}

function RegressionBadge() {
  return (
    <span className="chip" title="Reappeared after being resolved"
      style={{ color: SEV_PALETTE.RED, background: tint(SEV_PALETTE.RED, TINT.fill), borderColor: tint(SEV_PALETTE.RED, TINT.edge) }}>
      Regression
    </span>
  );
}

function AutoResolvedBadge({ reopenedCount }: { reopenedCount?: number }) {
  return (
    <span className="chip" title="Closed by coverage-gated auto-resolution"
      style={{ color: SEV_PALETTE.GREEN, background: tint(SEV_PALETTE.GREEN, TINT.fill), borderColor: tint(SEV_PALETTE.GREEN, TINT.hairline) }}>
      Auto-resolved{reopenedCount ? ` · reopened ${reopenedCount}×` : ""}
    </span>
  );
}

function StatusBadge({ s }: { s: FindingStatus }) {
  const c = STATUS_COLOR[s];
  return (
    <span className="chip" style={{ color: c, background: tint(c, TINT.fill), borderColor: tint(c, TINT.hairline) }}>
      {STATUS_LABEL[s]}
    </span>
  );
}

function DetectionPill({ cov }: { cov: DetectionCoverage }) {
  const c = COVERAGE_COLOR[cov];
  const Icon = cov === "COVERED" ? CheckCircle : cov === "PARTIAL" ? Shield : EyeOff;
  const copy = cov === "COVERED" ? "Detection covered" : cov === "PARTIAL" ? "Partial detection" : "Detection blind";
  return (
    <span className="chip" title={copy} style={{ color: c, background: tint(c, TINT.fill), borderColor: tint(c, TINT.hairline) }}>
      <Icon size={10} aria-hidden /> {copy}
    </span>
  );
}

/* ─── Ranked, capped signal row ───────────────────────────────────────────
 * Order is fixed by consequence, not by data order, so the same signal sits
 * in the same place on every row. Anything past the cap collapses into a
 * "+n" whose tooltip names what was hidden — nothing is lost, only deferred. */
type SignalChip = { key: string; label: string; node: React.ReactNode };

function signalChips(f: Finding): SignalChip[] {
  const out: SignalChip[] = [];
  if (f.kevStatusRecorded && f.kevListed) out.push({ key: "kev", label: "CISA KEV", node: <KevBadge /> });
  if (f.regression) out.push({ key: "regression", label: "Regression", node: <RegressionBadge /> });
  if (f.needsReview) out.push({ key: "review", label: "Needs review", node: <NeedsReviewChip /> });
  if (f.verificationState) {
    const m = VERIFICATION_META[f.verificationState.toLowerCase()];
    if (m) out.push({ key: "verify", label: m.label, node: <VerificationBadge state={f.verificationState} /> });
  }
  if (f.resolutionMethod === "auto") {
    out.push({ key: "auto", label: "Auto-resolved", node: <AutoResolvedBadge reopenedCount={f.reopenedCount} /> });
  }
  return out;
}

function ChipRow({ chips, max = 4, className = "" }: { chips: SignalChip[]; max?: number; className?: string }) {
  const shown = chips.slice(0, max);
  const hidden = chips.slice(max);
  return (
    <>
      {shown.map((c) => <React.Fragment key={c.key}>{c.node}</React.Fragment>)}
      {hidden.length > 0 && (
        <span className={`chip chip-overflow ${className}`} title={hidden.map((c) => c.label).join(" · ")}>
          +{hidden.length}
        </span>
      )}
    </>
  );
}

/* ─── Time formatting ─────────────────────────────────────────────────────
 * Three grains, three jobs: relative for scanning, absolute-to-the-second for
 * audit, calendar day for range summaries. Analysts read the first and cite
 * the second, so both ship on every event. */
function fmtEventTs(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

function fmtRelativeTs(iso: string, now: number = Date.now()): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  const secs = Math.floor((now - d.getTime()) / 1000);
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

function fmtEventDay(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" });
}

/* ─── Risk composition ────────────────────────────────────────────────────
 * Zero-weight factors used to render zero-width divs — invisible, but they
 * still consumed a legend slot and implied a contribution. They now drop out
 * of the bar and grey out in the legend, so "did not contribute" is legible.
 * Order stays fixed across findings: a moving legend cannot be compared. */
function RiskBreakdownBar({ breakdown, score }: { breakdown: RiskBreakdown; score: number }) {
  const segments = [
    { key: "cvss",    label: "Base severity",   color: "var(--chart-series-1)", value: Math.max(0, breakdown.cvss) },
    { key: "epss",    label: "Exploit odds",    color: "var(--chart-series-2)", value: Math.max(0, breakdown.epss) },
    { key: "exploit", label: "Exploit maturity", color: "var(--chart-series-3)", value: Math.max(0, breakdown.exploit) },
    { key: "lateral", label: "Lateral movement", color: "var(--chart-series-4)", value: Math.max(0, breakdown.lateral) },
    { key: "asset",   label: "Asset value",     color: "var(--chart-series-5)", value: Math.max(0, breakdown.asset) },
    { key: "kev",     label: "Known exploited", color: SEV_PALETTE.RED,         value: Math.max(0, breakdown.kev) },
  ];
  const recordedTotal = segments.reduce((total, segment) => total + segment.value, 0);
  const contributing = segments.filter((s) => s.value > 0);
  const summary = contributing.length
    ? contributing.map((s) => `${s.label} ${s.value}`).join(", ")
    : "No scoring factor is recorded";

  return (
    <div className="risk-breakdown">
      <div className="risk-breakdown-head">
        <span>What drives the {score} score</span>
        <span>{contributing.length} of {segments.length} factors recorded</span>
      </div>
      <div className="risk-breakdown-bar" role="img" aria-label={`Risk composition: ${summary}`}>
        {contributing.length === 0 ? <i data-empty style={{ width: "100%" }} /> : contributing.map((s) => (
          <i key={s.key} style={{ width: `${(s.value / recordedTotal) * 100}%`, background: s.color }} title={`${s.label}: ${s.value}`} />
        ))}
      </div>
      <ul className="risk-breakdown-legend">
        {segments.map((s) => (
          <li key={s.key} data-muted={s.value === 0 || undefined}>
            <i style={{ background: s.value > 0 ? s.color : "var(--border-strong)" }} />
            {s.label}
            <b>{s.value > 0 ? s.value : "—"}</b>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ─── Kill chain ──────────────────────────────────────────────────────────
 * Genuinely a sequence, so the numbered rail earns its place here (and only
 * here — nothing else in this file gets step markers). */
function KillChainViz({ steps }: { steps: KillChainStep[] }) {
  return (
    <ol className="kill-chain">
      {steps.map((step, i) => {
        const color = KILL_CHAIN_PHASE_COLOR[step.phase] ?? SEV_PALETTE.SLATE;
        return (
          <li key={`${step.phase}-${i}`} style={{ ["--rail" as string]: color }}>
            <div className="kill-chain-rail" aria-hidden>
              <i />
              {i < steps.length - 1 && <s />}
            </div>
            <div className="kill-chain-body">
              <div className="kill-chain-meta">
                <span style={{ color, background: tint(color, TINT.fill), borderColor: tint(color, TINT.hairline) }}>{step.phase}</span>
                {step.mitre && <code>{step.mitre}</code>}
              </div>
              <strong>{step.technique}</strong>
              <p>{step.description}</p>
            </div>
          </li>
        );
      })}
    </ol>
  );
}

/* ─── Triage legend ───────────────────────────────────────────────────────
 * Collapsed by default: it teaches the vocabulary once, then gets out of the
 * way. Three columns because the three concepts are peers, not a hierarchy. */
function TriageKey() {
  const severityMeaning: Array<{ severity: Severity; meaning: string }> = [
    { severity: "CRITICAL", meaning: "Immediate material exposure" },
    { severity: "HIGH", meaning: "Serious exploitable weakness" },
    { severity: "MEDIUM", meaning: "Time-bounded remediation" },
    { severity: "LOW", meaning: "Monitor and harden" },
    { severity: "INFO", meaning: "Context or hygiene signal" },
  ];
  const priorities: Priority[] = ["P0", "P1", "P2", "P3", "P4", "P5"];
  return (
    <details className="findings-triage-key">
      <summary>
        <span>
          <strong>How Vedha ranks a finding</strong>
          <small>Severity is impact. Priority is response order. Risk is the manager score out of 1000.</small>
        </span>
        <ChevronDown size={16} aria-hidden />
      </summary>
      <div className="findings-triage-key-body">
        <div className="findings-triage-concepts">
          <div><strong>Severity</strong><span>Technical consequence if the weakness is exploited.</span></div>
          <div><strong>Priority</strong><span>Response order after evidence, exploitability, asset context and SLA.</span></div>
          <div><strong>Risk</strong><span>Backend-computed ranking signal. It informs judgment, it does not replace it.</span></div>
        </div>
        <div className="findings-severity-key">
          {severityMeaning.map(({ severity, meaning }) => (
            <span key={severity}><i style={{ background: SEV_COLOR[severity] }} /><b>{severity}</b><em>{meaning}</em></span>
          ))}
        </div>
        <div className="findings-priority-key">
          {priorities.map((priority) => <PriorityBadge priority={priority} compact key={priority} />)}
        </div>
      </div>
    </details>
  );
}

/* ─── Evidence ────────────────────────────────────────────────────────────
 * Artifacts remain collapsible so long scanner output does not bury the next
 * decision. Inside each record, identity, provenance, command, masked output
 * and completeness follow the same order an analyst uses to validate proof. */
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
          <details className="finding-evidence-artifact" key={`${label}-${index}`} open={index === 0}>
            <summary>
              <ChevronDown size={14} aria-hidden />
              <div className="finding-evidence-identity">
                <span className="finding-evidence-kind">{presentation.kind}</span>
                <div>
                  <h4>{label}</h4>
                  <p>{presentation.lines.length.toLocaleString()} line{presentation.lines.length === 1 ? "" : "s"} recorded</p>
                </div>
              </div>
              <span onClick={(event) => event.stopPropagation()}>
                <CopyBtn text={presentation.copyText} label={`${label} masked contents`} showLabel />
              </span>
            </summary>

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
          </details>
        );
      })}
    </div>
  );
}

/* ─── Evidence: a plain key-facts table, raw artifacts behind a disclosure ──
 * evidence_summary (from the backend normalizer) is the glanceable view — short
 * label/value facts anyone can read at speed. The raw scanner artifacts are kept,
 * but demoted behind a disclosure so they never bury the point. */
function EvidenceFacts({ facts }: { facts: EvidenceFact[] }) {
  if (!facts.length) return null;
  return (
    <div className="finding-evidence-facts">
      <div className="finding-section-heading">
        <div><ListChecks size={15} aria-hidden /><h3>Key facts</h3></div>
        <span>{facts.length} fact{facts.length === 1 ? "" : "s"}</span>
      </div>
      <dl className="finding-fact-grid">
        {facts.map((fact, i) => (
          <div className="finding-fact" key={`${fact.label}-${i}`}>
            <dt>{fact.label}</dt>
            <dd>{fact.value}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

function EvidenceView({ finding }: { finding: Finding }) {
  const facts = finding.evidenceSummary ?? [];
  const rawCount = finding.evidence.length;
  // No clean facts → fall straight back to the raw gallery (or its empty state).
  if (!facts.length) return <EvidenceGallery evidence={finding.evidence} />;
  return (
    <div className="finding-evidence-wrap">
      <EvidenceFacts facts={facts} />
      {rawCount > 0 && (
        <details className="finding-evidence-raw">
          <summary><ChevronDown size={14} aria-hidden /> Raw evidence artifacts ({rawCount})</summary>
          <EvidenceGallery evidence={finding.evidence} />
        </details>
      )}
    </div>
  );
}

/* ─── Remediation ─────────────────────────────────────────────────────────
 * The OS selector defaults to the asset's own platform, so the common case
 * needs no interaction at all. */
function remediationOsFor(finding: Finding): RemediationOs {
  const value = (finding.assetContext?.os ?? "").toLowerCase();
  if (value.includes("windows")) return "windows";
  if (value.includes("mac") || value.includes("darwin")) return "macos";
  if (value.includes("linux") || value.includes("unix")) return "linux";
  return "generic";
}

// Fix-plan colour language: change-risk is a hazard scale (green→amber→red);
// effort is an ease scale (low effort reads positive/green). Both resolve to the
// same WCAG-AA palette + tint helpers every other chip in this file uses.
const REM_RISK_COLOR: Record<string, string> = {
  high: SEV_PALETTE.RED,
  medium: SEV_PALETTE.AMBER,
  low: SEV_PALETTE.GREEN,
};
const remRiskColor = (v: string | undefined) =>
  REM_RISK_COLOR[(v ?? "").toLowerCase()] ?? SEV_PALETTE.SLATE;
const effortColor = (v: string | undefined) => {
  const k = (v ?? "").toLowerCase();
  return k === "high" ? SEV_PALETTE.RED : k === "medium" ? SEV_PALETTE.AMBER : SEV_PALETTE.GREEN;
};
const pillStyle = (color: string) => ({
  color,
  background: tint(color, TINT.fill),
  borderColor: tint(color, TINT.hairline),
});

function RemediationPlanView({
  finding,
  api,
  surface,
}: {
  finding: Finding;
  api: FindingsWorkspaceApi;
  surface: FindingsWorkspaceSurface;
}) {
  const [os, setOs] = useState<RemediationOs>(() => remediationOsFor(finding));
  const { data, isLoading, isFetching, error, refetch } = useQuery({
    queryKey: ["finding-remediation", surface, finding.id, os],
    queryFn: () => api.remediation<RemediationPlanResponse>(finding.id, os),
    staleTime: 60_000,
  });

  if (isLoading) {
    return (
      <div className="finding-plan-loading" aria-busy="true">
        <SkeletonRows rows={4} height={72} />
      </div>
    );
  }
  if (error || !data) {
    return (
      <div className="finding-blank" data-tone="error">
        <AlertTriangle size={17} aria-hidden />
        <div>
          <strong>The remediation plan did not load</strong>
          <p>The finding record itself is unchanged.</p>
          <button type="button" className="findings-inline-action" onClick={() => { void refetch(); }}>
            <RotateCcw size={13} aria-hidden /> Try again
          </button>
        </div>
      </div>
    );
  }

  const plan = data.plan;
  const recordedNotes = finding.remediation
    .map((step) => typeof step === "string" ? step : step.description || step.title)
    .filter(Boolean);

  return (
    <div className="finding-remediation-view" data-refreshing={isFetching || undefined}>
      <header className="finding-remediation-header">
        <div>
          <div className="finding-remediation-title"><Wrench size={16} aria-hidden /><h3>Fix plan</h3></div>
          <p>{plan.summary}</p>
          <div className="finding-remediation-meta">
            <span>{data.source === "ai" ? "AI-generated operator plan" : "Vedha remediation knowledge base"}</span>
            <span className="finding-rem-pill" style={pillStyle(effortColor(plan.effort))}>Effort: {plan.effort}</span>
            <span className="finding-rem-pill" style={pillStyle(remRiskColor(plan.remediation_risk))}>Change risk: {plan.remediation_risk}</span>
            {data.generated_at && <span>Generated {fmtEventDay(data.generated_at)}</span>}
          </div>
        </div>
        <label className="finding-remediation-os">
          <span>Target platform</span>
          <select value={os} onChange={(event) => setOs(event.target.value as RemediationOs)}>
            <option value="generic">Generic or appliance</option>
            <option value="linux">Linux</option>
            <option value="windows">Windows</option>
            <option value="macos">macOS</option>
          </select>
        </label>
      </header>

      {recordedNotes.length > 0 && (
        <section className="finding-remediation-note">
          <h3>Guidance recorded on the finding</h3>
          {recordedNotes.map((note, index) => <p key={index}>{note}</p>)}
        </section>
      )}

      <section>
        <div className="finding-section-heading">
          <div><Terminal size={15} aria-hidden /><h3>Actions</h3></div>
          <span>{plan.steps.length} ordered step{plan.steps.length === 1 ? "" : "s"}</span>
        </div>
        <ol className="finding-remediation-steps">
          {plan.steps.map((step) => (
            <li key={step.step}>
              <div className="finding-remediation-step-number" aria-hidden>{step.step}</div>
              <div>
                <header>
                  <h4>{step.title}</h4>
                  <span className="finding-rem-pill" style={pillStyle(remRiskColor(step.risk))}>{step.risk} change risk</span>
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
                  <p className="finding-remediation-warning">
                    <AlertTriangle size={13} aria-hidden /> Unsafe generated commands were stripped before this plan was stored.
                  </p>
                )}
                {step.verification && (
                  <p className="finding-remediation-verify">
                    <CheckCircle size={13} aria-hidden /> <span><b>Verify:</b> {step.verification}</span>
                  </p>
                )}
              </div>
            </li>
          ))}
        </ol>
      </section>

      <div className="finding-remediation-closeout">
        <section>
          <h3>Verify and close</h3>
          {plan.verification.length ? (
            <ol>{plan.verification.map((item, index) => <li key={index}>{item}</li>)}</ol>
          ) : <p>No separate closeout check is recorded. Re-scan the asset and attach the result before closing.</p>}
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

/* ─── CVSS vector decoding ────────────────────────────────────────────────
 * A recorded vector like CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H is the
 * densest fact on the whole finding and the page previously rendered it as an
 * opaque string. Decoding is pure presentation of data already on the record —
 * nothing is inferred, and an unrecognised metric is dropped rather than guessed.
 * ─────────────────────────────────────────────────────────────────────────── */
const CVSS_METRIC: Record<string, { label: string; values: Record<string, string> }> = {
  AV: { label: "Attack vector",   values: { N: "Network", A: "Adjacent network", L: "Local", P: "Physical" } },
  AC: { label: "Attack complexity", values: { L: "Low", H: "High" } },
  PR: { label: "Privileges required", values: { N: "None", L: "Low", H: "High" } },
  UI: { label: "User interaction", values: { N: "Not required", R: "Required" } },
  S:  { label: "Scope",           values: { U: "Unchanged", C: "Changed" } },
  C:  { label: "Confidentiality impact", values: { H: "High", L: "Low", N: "None" } },
  I:  { label: "Integrity impact", values: { H: "High", L: "Low", N: "None" } },
  A:  { label: "Availability impact", values: { H: "High", L: "Low", N: "None" } },
};
/* Metrics that make a finding materially easier to reach or abuse. Flagged so an
 * analyst can see the aggravating factors without reading all eight rows. */
const CVSS_AGGRAVATING = new Set(["AV:N", "AC:L", "PR:N", "UI:N", "S:C", "C:H", "I:H", "A:H"]);

interface CvssMetric { key: string; label: string; value: string; raw: string; aggravating: boolean }

function decodeCvssVector(vector: string): { version: string | null; metrics: CvssMetric[] } {
  if (!vector) return { version: null, metrics: [] };
  const parts = vector.split("/").map((part) => part.trim()).filter(Boolean);
  let version: string | null = null;
  const metrics: CvssMetric[] = [];
  for (const part of parts) {
    const [key, value] = part.split(":");
    if (key === "CVSS") { version = value; continue; }
    const meta = CVSS_METRIC[key];
    if (!meta) continue;                       // unknown or temporal/environmental metric
    const readable = meta.values[value];
    if (!readable) continue;                   // unrecognised value: drop, never guess
    metrics.push({
      key, label: meta.label, value: readable, raw: part,
      aggravating: CVSS_AGGRAVATING.has(part),
    });
  }
  return { version, metrics };
}

/* ─── Reference sources ───────────────────────────────────────────────────
 * Every link is CONSTRUCTED from an identifier already stored on the finding —
 * a CVE id, a technique id, a CWE id, a CVSS vector. Nothing here asserts that
 * a source says anything in particular; each entry states only what the reader
 * will find there. A finding with no recorded identifiers yields no sources,
 * which is the honest result rather than a page of plausible-looking links.
 * ─────────────────────────────────────────────────────────────────────────── */
type SourceGroup = "Vulnerability record" | "Exploitation intelligence" | "Technique and weakness" | "Scoring";
interface SourceLink { group: SourceGroup; label: string; detail: string; href: string }

function techniqueUrl(id: string): string | null {
  const m = /^T(\d{4})(?:\.(\d{3}))?$/i.exec(id.trim());
  if (!m) return null;
  return m[2]
    ? `https://attack.mitre.org/techniques/T${m[1]}/${m[2]}/`
    : `https://attack.mitre.org/techniques/T${m[1]}/`;
}

function referenceSources(f: Finding): SourceLink[] {
  const out: SourceLink[] = [];
  const cves = [...new Set([...(f.cves ?? []), ...(f.tags ?? [])]
    .filter((v) => /^CVE-\d{4}-\d{4,7}$/i.test(v))
    .map((v) => v.toUpperCase()))];

  for (const cve of cves) {
    out.push({
      group: "Vulnerability record", label: `${cve} — NVD`,
      detail: "Authoritative description, CWE mapping, CVSS metrics and vendor references.",
      href: `https://nvd.nist.gov/vuln/detail/${cve}`,
    });
    out.push({
      group: "Vulnerability record", label: `${cve} — CVE Record`,
      detail: "The CNA's original record, including affected version ranges.",
      href: `https://www.cve.org/CVERecord?id=${cve}`,
    });
  }

  if (f.kevStatusRecorded && f.kevListed) {
    out.push({
      group: "Exploitation intelligence", label: "CISA Known Exploited Vulnerabilities",
      detail: "The catalogue entry and its federal remediation due date.",
      href: cves.length
        ? `https://www.cisa.gov/known-exploited-vulnerabilities-catalog?search_api_fulltext=${cves[0]}`
        : "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
    });
  }
  if (f.epssRecorded) {
    out.push({
      group: "Exploitation intelligence", label: "FIRST EPSS",
      detail: "How the exploit-prediction score is produced and what it does and does not claim.",
      href: "https://www.first.org/epss/model",
    });
  }

  for (const technique of f.mitre) {
    const href = techniqueUrl(technique.id);
    if (!href) continue;
    out.push({
      group: "Technique and weakness", label: `${technique.id} — ${technique.name}`,
      detail: "Adversary procedures, detection guidance and documented mitigations.",
      href,
    });
  }
  for (const raw of [...new Set((f.tags ?? []).filter((v) => /^CWE-\d+$/i.test(v)))]) {
    const id = raw.toUpperCase().replace("CWE-", "");
    out.push({
      group: "Technique and weakness", label: raw.toUpperCase(),
      detail: "The underlying weakness class, with common consequences and mitigations.",
      href: `https://cwe.mitre.org/data/definitions/${id}.html`,
    });
  }

  if (f.cvssVector) {
    const version = decodeCvssVector(f.cvssVector).version ?? "3.1";
    out.push({
      group: "Scoring", label: `CVSS v${version} calculator`,
      detail: "Re-score the recorded vector against your own environmental metrics.",
      href: `https://www.first.org/cvss/calculator/${version}#${f.cvssVector}`,
    });
  }
  return out;
}

const SOURCE_GROUP_ORDER: SourceGroup[] = [
  "Vulnerability record", "Exploitation intelligence", "Technique and weakness", "Scoring",
];

/* ─── Overview ────────────────────────────────────────────────────────────
 * Reordered from the original. An analyst opens a finding to decide, so the
 * decision row leads; explanation follows; identifiers sit last for citation.
 * The old order (description → impact → technical → decision context) made
 * them read three paragraphs before reaching the thing they came for. */
function FindingOverview({
  finding, related, sla, customerImpact, firstRemediation, onOpenTab,
}: {
  finding: Finding;
  related: Finding[];
  sla: Sla;
  customerImpact: string;
  firstRemediation?: string;
  onOpenTab: (tab: DetailTab) => void;
}) {
  const asset = finding.assetContext;
  const host = asset?.fqdn || asset?.hostname || asset?.ipAddress || finding.affectedHost;
  const confidence = finding.verificationConfidence == null ? "not scored" : `${finding.verificationConfidence}%`;
  const cvss = useMemo(() => decodeCvssVector(finding.cvssVector), [finding.cvssVector]);
  const sources = useMemo(() => referenceSources(finding), [finding]);

  return (
    <div className="finding-overview-view">

      <section className="finding-decision-row" aria-label="Decision summary">
        <article data-lead>
          <h3>Do this first</h3>
          <p>{firstRemediation || "Assign an owner, validate the finding, and record an approved plan."}</p>
          <button type="button" className="findings-inline-action" onClick={() => onOpenTab("remediation")}>
            <Wrench size={13} aria-hidden /> Open the full fix plan
          </button>
        </article>
        <article>
          <h3>Evidence</h3>
          <p>
            {(() => {
              const n = finding.evidenceSummary?.length || finding.evidence.length;
              return n ? `${n} evidence item${n === 1 ? "" : "s"} recorded.` : "Nothing attached.";
            })()} Verdict {finding.verificationState || "unassessed"} ({confidence}).
          </p>
          <button type="button" className="findings-inline-action" onClick={() => onOpenTab("evidence")}>
            <FileText size={13} aria-hidden /> Review the evidence
          </button>
        </article>
        <article>
          <h3>Exploitation</h3>
          <p>{finding.exploitation?.note
            ?? (finding.activelyExploited
              ? "Recorded as validated in the wild."
              : "Not validated. Absence of proof is not proof of absence.")}</p>
        </article>
        <article>
          <h3>Ownership</h3>
          <p>
            {finding.assignee ? `Assigned to ${finding.assignee}.` : "No owner assigned."}{" "}
            <b style={{ color: sla.color }}>{sla.tracked ? `SLA ${sla.label.toLowerCase()}` : "No SLA target"}</b>
          </p>
        </article>
      </section>

      <div className="finding-overview-layout">
        <div className="finding-overview-narrative">
          <section>
            <h3>Description</h3>
            <p className="finding-prose">{finding.description || "No description has been recorded."}</p>
          </section>

          <section>
            <h3>Impact</h3>
            <p className="finding-prose">{customerImpact}</p>
            {finding.impact && finding.businessImpact && finding.impact !== finding.businessImpact && (
              <p className="finding-prose finding-prose-secondary">{finding.impact}</p>
            )}
          </section>

          <section>
            <h3>Technical explanation</h3>
            <p className="finding-prose">
              {finding.technicalDetails || finding.verificationRationale
                || "No technical explanation is recorded. Review the evidence and the source scan before making a closure decision."}
            </p>

            {/* The recorded CVSS vector, decoded. This is the densest fact on the
                finding and it used to render as an opaque string in a table cell. */}
            {cvss.metrics.length > 0 && (
              <div className="finding-cvss-decode">
                <div className="finding-cvss-decode-head">
                  <h4>How the CVSS v{cvss.version ?? "3.1"} score is composed</h4>
                  <code>{finding.cvssVector}</code>
                </div>
                <ul>
                  {cvss.metrics.map((m) => (
                    <li key={m.key} data-aggravating={m.aggravating || undefined}>
                      <span>{m.label}</span>
                      <b>{m.value}</b>
                      <code>{m.raw}</code>
                    </li>
                  ))}
                </ul>
                <p>Highlighted rows are the metrics that make this easier to reach or more damaging to abuse.</p>
              </div>
            )}
          </section>

          {/* attackPath is delivered by the backend adapter and was rendered nowhere. */}
          {finding.attackPath && (
            <section>
              <h3>Attack path</h3>
              <p className="finding-prose">{finding.attackPath}</p>
            </section>
          )}

          <section>
            <h3>Sources and references</h3>
            {sources.length ? (
              <>
                <p className="finding-prose finding-prose-secondary">
                  Every link below is built from an identifier recorded on this finding. Vedha does not
                  assert what these sources say — open them to corroborate before you act.
                </p>
                <div className="finding-sources">
                  {SOURCE_GROUP_ORDER.filter((g) => sources.some((x) => x.group === g)).map((group) => (
                    <div className="finding-source-group" key={group}>
                      <h4>{group}</h4>
                      {sources.filter((x) => x.group === group).map((source) => (
                        <a
                          key={source.href + source.label}
                          className="finding-source"
                          href={source.href}
                          target="_blank"
                          rel="noreferrer noopener"
                        >
                          <span className="finding-source-label">
                            {source.label}
                            <ExternalLink size={11} aria-hidden />
                          </span>
                          <span className="finding-source-detail">{source.detail}</span>
                        </a>
                      ))}
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <p className="finding-data-missing">
                No CVE, technique, weakness or CVSS vector is recorded on this finding, so there is
                nothing to link to. Enrich the finding before citing external sources.
              </p>
            )}
          </section>
        </div>

        <aside className="finding-overview-facts">
          <div><Server size={15} aria-hidden /><h3>Affected system</h3></div>
          <dl>
            <div><dt>Host</dt><dd>{host || "Not recorded"}</dd></div>
            <div><dt>Platform</dt><dd>{[asset?.os, asset?.osVersion].filter(Boolean).join(" ") || "Not recorded"}</dd></div>
            <div><dt>Type</dt><dd>{asset?.assetType || "Not recorded"}</dd></div>
            <div><dt>Criticality</dt><dd>{asset?.criticality || "Not recorded"}</dd></div>
            <div><dt>Environment</dt><dd>{asset?.environment || "Not recorded"}</dd></div>
            <div><dt>Owner</dt><dd>{asset?.owner || finding.assignee || "Unassigned"}</dd></div>
          </dl>
        </aside>
      </div>

      <section className="finding-attack-context">
        <div className="finding-section-heading">
          <div><Link2 size={15} aria-hidden /><h3>Attack path and correlation</h3></div>
          <span>{finding.mitre.length} technique{finding.mitre.length === 1 ? "" : "s"} mapped</span>
        </div>
        <div className="finding-attack-context-grid">
          <div>
            <h4>MITRE ATT&amp;CK</h4>
            {finding.mitre.length ? finding.mitre.map((mapping) => (
              <div className="finding-mitre-row" key={mapping.id}><code>{mapping.id}</code><span>{mapping.name}</span></div>
            )) : <p className="finding-data-missing">No technique is mapped.</p>}
            {finding.tags && finding.tags.length > 0 && (
              <div className="finding-overview-tags">
                <Tag size={11} aria-hidden />
                {finding.tags.map((tag) => <span key={tag}>{tag}</span>)}
              </div>
            )}
          </div>
          <div>
            <h4>Kill chain</h4>
            {finding.killChain.length ? <KillChainViz steps={finding.killChain} /> : <p className="finding-data-missing">No kill-chain path is recorded.</p>}
          </div>
        </div>
        {related.length > 0 && (
          <div className="finding-related-list">
            <h4>Correlated findings</h4>
            {related.map((item) => (
              <div key={item.id}>
                <span style={{ background: SEV_COLOR[item.severity] }} aria-hidden />
                <code>{item.id}</code>
                <strong>{item.title}</strong>
                <RiskBadge score={item.riskScore} />
              </div>
            ))}
          </div>
        )}
      </section>

      <div className="finding-overview-technical-grid">
        <section>
          <h3>Scores and identifiers</h3>
          <dl>
            <div><dt>Manager risk</dt><dd style={{ color: riskScoreColor(finding.riskScore) }}>{finding.riskScore} / 1000</dd></div>
            <div><dt>CVSS</dt><dd>{finding.cvss || "Not recorded"}</dd></div>
            <div><dt>Vector</dt><dd><code>{finding.cvssVector || "Not recorded"}</code></dd></div>
            <div><dt>CVE</dt><dd>{finding.cves?.length ? finding.cves.join(", ") : "None recorded"}</dd></div>
            <div><dt>Category</dt><dd>{finding.category}</dd></div>
          </dl>
        </section>
        <section>
          <h3>Detection and timing</h3>
          <dl>
            <div><dt>Coverage</dt><dd>{finding.detectionCoverage}</dd></div>
            <div><dt>Verification</dt><dd>{finding.verificationState || "Unassessed"}</dd></div>
            <div><dt>Confidence</dt><dd>{confidence}</dd></div>
            <div><dt>First seen</dt><dd>{new Date(finding.discoveredAt).toLocaleString()}</dd></div>
            <div><dt>Last seen</dt><dd>{finding.lastSeen ? new Date(finding.lastSeen).toLocaleString() : "Not recorded"}</dd></div>
          </dl>
        </section>
      </div>
    </div>
  );
}

/* ─── Threat intel ────────────────────────────────────────────────────────
 * This panel existed in the original file but was unreachable: the tab strip
 * rendered only four tabs, so EPSS, KEV, exploit maturity, false-positive
 * probability and the composite score were dead UI. Restored as a real tab. */
function IntelPanel({ finding }: { finding: Finding }) {
  const f = finding;
  const maturityCopy = f.exploitMaturity === "WEAPONIZED"
    ? "A weaponized exploit ships in public toolchains. Exploitation is trivial for any attacker."
    : f.exploitMaturity === "POC"
      ? "Proof-of-concept code is public. It needs adaptation for production use but the barrier is already low."
      : "No public exploit code. The path is theoretical and would need custom development.";

  return (
    <div className="finding-intel-view">
      <section className="finding-intel-card">
        <header>
          <h3>Composite risk</h3>
          <span>Computed by the manager, displayed here only</span>
        </header>
        <div className="finding-intel-score">
          <strong style={{ color: riskScoreColor(f.riskScore) }}>{f.riskScore}</strong>
          <span>out of 1000</span>
        </div>
        <div className="finding-intel-meter" role="img" aria-label={`Composite risk ${f.riskScore} out of 1000`}>
          <i style={{ width: `${Math.min(100, Math.max(0, f.riskScore / 10))}%`, background: riskScoreColor(f.riskScore) }} />
        </div>
        <RiskBreakdownBar breakdown={f.riskBreakdown} score={f.riskScore} />
      </section>

      <div className="finding-intel-grid">
        <section className="finding-intel-card">
          <header>
            <h3>Exploit probability</h3>
            {f.epssRecorded
              ? <span style={{ color: epssColor(f.epssScore) }}>{(f.epssScore * 100).toFixed(1)}%</span>
              : <span>Not enriched</span>}
          </header>
          {f.epssRecorded ? (
            <>
              <div className="finding-intel-meter">
                <i style={{ width: `${Math.min(100, f.epssScore * 100)}%`, background: epssColor(f.epssScore) }} />
              </div>
              <p>{f.epssScore > 0.5
                ? `Top ${(100 - f.epssPercentile * 100).toFixed(1)}% most likely to be exploited in the next 30 days, per the FIRST.org model.`
                : "Treat EPSS as one prioritization signal. It estimates likelihood, it does not prove exploitation."}</p>
            </>
          ) : <p>Run vulnerability enrichment before using exploitation probability in a remediation decision.</p>}
        </section>

        <section className="finding-intel-card" data-alert={f.kevStatusRecorded && f.kevListed || undefined}>
          <header>
            <h3>CISA known exploited</h3>
            {f.kevStatusRecorded && f.kevListed
              ? <KevBadge />
              : <span>{f.kevStatusRecorded ? "Not listed" : "Not enriched"}</span>}
          </header>
          {f.kevListed && f.kevDateAdded && <p className="finding-intel-flag">Added to the catalogue {f.kevDateAdded}</p>}
          <p>{f.kevStatusRecorded
            ? f.kevListed
              ? "Actively exploited in the wild per CISA. Federal patching deadlines apply. Treat as top priority."
              : "The recorded enrichment did not find this CVE in the catalogue."
            : "Catalogue status has not been recorded. Do not read missing enrichment as not listed."}</p>
        </section>

        {f.exploitMaturityRecorded && (
          <section className="finding-intel-card">
            <header>
              <h3>Exploit maturity</h3>
              <span style={{ color: MATURITY_COLOR[f.exploitMaturity] }}>{f.exploitMaturity}</span>
            </header>
            <div className="finding-intel-chips">
              {f.pocAvailable && (
                <span className="chip" style={{ color: SEV_PALETTE.ORANGE, background: tint(SEV_PALETTE.ORANGE, TINT.fill), borderColor: tint(SEV_PALETTE.ORANGE, TINT.hairline) }}>Public proof of concept</span>
              )}
              {f.activelyExploited && (
                <span className="chip" style={{ color: SEV_PALETTE.RED, background: tint(SEV_PALETTE.RED, TINT.fill), borderColor: tint(SEV_PALETTE.RED, TINT.edge) }}>Active exploitation</span>
              )}
            </div>
            <p>{maturityCopy}</p>
          </section>
        )}

        {f.fpProbabilityRecorded && (
          <section className="finding-intel-card">
            <header>
              <h3>False-positive probability</h3>
              <span style={{ color: f.fpProbability < 0.1 ? SEV_PALETTE.GREEN : f.fpProbability < 0.3 ? SEV_PALETTE.AMBER : SEV_PALETTE.RED }}>
                {Math.round(f.fpProbability * 100)}%
              </span>
            </header>
            <div className="finding-intel-meter">
              <i style={{
                width: `${f.fpProbability * 100}%`,
                background: f.fpProbability < 0.1 ? SEV_PALETTE.GREEN : f.fpProbability < 0.3 ? SEV_PALETTE.AMBER : SEV_PALETTE.RED,
              }} />
            </div>
            <p>{f.fpProbability < 0.1
              ? "Very low. The finding is backed by exploitation evidence."
              : f.fpProbability < 0.3
                ? "Moderate. Correlate with further evidence before closing."
                : "Elevated. Validate before spending remediation effort."}</p>
          </section>
        )}

        <section className="finding-intel-card">
          <header>
            <h3>Detection coverage</h3>
            <DetectionPill cov={f.detectionCoverage} />
          </header>
          {f.detectionNote && <p>{f.detectionNote}</p>}
          {f.mitre.length ? (
            <ul className="finding-intel-coverage">
              {f.mitre.map((m) => (
                <li key={m.id}>
                  <code>{m.id}</code>
                  <span>{m.name}</span>
                  <b style={{ color: COVERAGE_COLOR[f.detectionCoverage] }}>{f.detectionCoverage}</b>
                </li>
              ))}
            </ul>
          ) : <p className="finding-data-missing">No technique is mapped, so coverage cannot be attributed.</p>}
        </section>
      </div>
    </div>
  );
}

/* ─── Compliance ──────────────────────────────────────────────────────────
 * Also unreachable in the original. Kept deliberately plain: a control
 * mapping is a citation, and citations should look like citations. */
function CompliancePanel({ compliance }: { compliance: ComplianceRef[] }) {
  if (!compliance.length) {
    return (
      <div className="finding-blank">
        <ListChecks size={17} aria-hidden />
        <div>
          <strong>No control mapping is recorded</strong>
          <p>Do not infer a control failure without an approved framework scope and test procedure.</p>
        </div>
      </div>
    );
  }
  return (
    <div className="finding-compliance-view">
      <div className="finding-section-heading">
        <div><ListChecks size={15} aria-hidden /><h3>Mapped controls</h3></div>
        <span>{compliance.length} framework{compliance.length === 1 ? "" : "s"}</span>
      </div>
      {compliance.map((c, i) => {
        const controls = c.controls ?? c.refs ?? [];
        return (
          <section key={`${c.framework}-${i}`}>
            <h4>{c.framework}</h4>
            {c.rationale && <p className="finding-compliance-rationale">{c.rationale}</p>}
            <ul>{controls.map((r, j) => <li key={j}>{r}</li>)}</ul>
          </section>
        );
      })}
    </div>
  );
}

/* ─── Lifecycle history ───────────────────────────────────────────────────*/
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

function eventActor(event: TimelineEvent): string {
  if (!event.actor) return event.actor_type === "user" ? "Unknown operator" : "Vedha system";
  if (event.actor_type !== "user") return event.actor;
  return `Operator ${event.actor.length > 12 ? `${event.actor.slice(0, 8)}…` : event.actor}`;
}

function eventNarrative(event: TimelineEvent): string {
  switch (event.event_type) {
    case "detected": return "Created the finding from recorded scan or detection evidence.";
    case "reaffirmed": return "Observed the same exposure again in a later assessment run.";
    case "confirmed": return "Confirmed the finding is valid and needs action.";
    case "remediated": return "Closed the finding as remediated after the fix was reported.";
    case "resolved": return "Closed automatically after coverage-proven clean runs.";
    case "accepted": return "Accepted the documented risk without marking the exposure fixed.";
    case "false_positive": return "Classified as a false positive after validation.";
    case "reopened": return "Reopened because the exposure returned or the prior decision changed.";
    case "risk_changed": return "Recalculated the CVSS or manager risk score.";
    case "verification_changed": return "Updated the evidence verification verdict.";
    case "note": return "Added an operator note to the record.";
    default: return event.from_status && event.to_status
      ? `Changed status from ${event.from_status} to ${event.to_status}.`
      : "Updated the finding record.";
  }
}

function eventDetailLabel(key: string): string {
  return key.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function HistoryTimeline({
  findingId,
  now,
  api,
  surface,
}: {
  findingId: string;
  now: number;
  api: FindingsWorkspaceApi;
  surface: FindingsWorkspaceSurface;
}) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["finding-events", surface, findingId],
    queryFn: () => api.events<FindingTimeline>(findingId),
    staleTime: 30_000,
  });

  if (isLoading) return <div className="finding-plan-loading" aria-busy="true"><SkeletonRows rows={3} height={64} /></div>;
  if (error) {
    return (
      <div className="finding-blank" data-tone="error">
        <AlertTriangle size={17} aria-hidden />
        <div>
          <strong>The history did not load</strong>
          <p>Stored events are unaffected.</p>
          <button type="button" className="findings-inline-action" onClick={() => { void refetch(); }}>
            <RotateCcw size={13} aria-hidden /> Try again
          </button>
        </div>
      </div>
    );
  }
  const events = data?.events ?? [];
  if (!events.length) {
    return (
      <div className="finding-blank">
        <Activity size={17} aria-hidden />
        <div>
          <strong>No lifecycle events yet</strong>
          <p>Every action recorded on this finding will appear here in order.</p>
        </div>
      </div>
    );
  }

  const first = events[0];
  const latest = events[events.length - 1];
  const latestColor = EVENT_COLOR[latest.event_type] ?? SEV_PALETTE.SLATE;

  return (
    <div className="finding-history-view">
      <header className="finding-history-summary">
        <div>
          <h3>Activity history</h3>
          <p>Operator actions and system observations, oldest first. The record is append-only.</p>
        </div>
        <dl>
          <div><dt>Events</dt><dd>{events.length}</dd></div>
          <div><dt>Period</dt><dd>{fmtEventDay(first.occurred_at)}{events.length > 1 ? ` – ${fmtEventDay(latest.occurred_at)}` : ""}</dd></div>
          <div><dt>Latest</dt><dd style={{ color: latestColor }}>{latest.label}</dd></div>
        </dl>
      </header>

      <ol className="finding-history-timeline">
        {events.map((ev, i) => {
          const color = EVENT_COLOR[ev.event_type] ?? SEV_PALETTE.SLATE;
          const last = i === events.length - 1;
          const isCurrent = last && events.length > 1;
          const reason = typeof ev.detail?.reason === "string" ? ev.detail.reason : null;
          const detailEntries = ev.detail
            ? Object.entries(ev.detail).filter(([key]) => key !== "approx" && key !== "reason" && key !== "note")
            : [];
          return (
            <li key={ev.id ?? `${ev.event_type}-${ev.occurred_at}-${i}`} style={{ ["--rail" as string]: color }} data-current={isCurrent || undefined}>
              <div className="finding-history-rail" aria-hidden>
                <i />
                {!last && <s />}
              </div>
              <article>
                <div className="finding-history-head">
                  <span title={fmtEventTs(ev.occurred_at)}>{fmtRelativeTs(ev.occurred_at, now)}</span>
                  <span className="chip" style={{ color, background: tint(color, TINT.fill), borderColor: tint(color, TINT.hairline) }}>{ev.label}</span>
                  {isCurrent && <span className="chip chip-current">Current</span>}
                  {ev.synthesized && <em title="Derived from the finding record, not a separately stored audit row">derived</em>}
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
            </li>
          );
        })}
      </ol>
    </div>
  );
}

/* ─── Finding detail ──────────────────────────────────────────────────────*/
type DetailTab = "overview" | "intel" | "evidence" | "remediation" | "compliance" | "history";

const WORKFLOW: { status: FindingStatus; label: string; color: string; hint: string }[] = [
  { status: "CONFIRMED",      label: "Confirm",            color: SEV_PALETTE.ORANGE, hint: "Record the evidence or analyst decision that confirms the finding." },
  { status: "REMEDIATED",     label: "Close as fixed",     color: SEV_PALETTE.GREEN,  hint: "Describe the fix applied and the verification performed." },
  { status: "ACCEPTED",       label: "Accept the risk",    color: SEV_PALETTE.AMBER,  hint: "Record the justification, the accountable owner, and the compensating control or review date." },
  { status: "FALSE_POSITIVE", label: "Mark false positive", color: "var(--text-secondary)", hint: "Record the validation evidence that disproves the finding." },
  { status: "OPEN",           label: "Reopen",             color: SEV_PALETTE.RED,    hint: "Record what changed, reappeared, or invalidated the previous decision." },
];

/* Editable starting points, not verdicts. Typing a defensible reason is the
 * slowest part of triage and the part most often skipped; a draft the analyst
 * must still complete is faster than a blank box and safer than a preset. */
const REASON_TEMPLATES: Partial<Record<FindingStatus, string[]>> = {
  CONFIRMED: [
    "Reproduced the exposure on the affected host. Evidence attached.",
    "Scan output and vendor advisory agree. Treating as valid.",
  ],
  REMEDIATED: [
    "Vendor patch applied and confirmed by a follow-up scan on ",
    "Configuration hardened and re-tested. The exposure no longer reproduces.",
  ],
  ACCEPTED: [
    "Risk accepted by the business owner until . Compensating control: ",
    "Asset is scheduled for decommission on . No fix will be applied.",
  ],
  FALSE_POSITIVE: [
    "Manual validation shows the affected component is not present.",
    "Scanner matched a back-ported package version. Vendor confirms the fix is applied.",
  ],
  OPEN: [
    "The exposure reappeared in the latest assessment run.",
    "The previous closure was recorded without evidence. Reopening for validation.",
  ],
};

function FindingDetail({
  f, allFindings, sla, now, onStatusChange, statusUpdating, onReopen, reopening, onClose,
  onExplain, api, surface,
}: {
  f: Finding;
  allFindings: Finding[];
  sla: Sla;
  now: number;
  onStatusChange: (id: string, s: FindingStatus, reason: string) => Promise<void>;
  statusUpdating: boolean;
  onReopen: (id: string, reason: string) => Promise<void>;
  reopening: boolean;
  onClose: () => void;
  onExplain: (id: string) => void;
  api: FindingsWorkspaceApi;
  surface: FindingsWorkspaceSurface;
}) {
  const [tab, setTab] = useState<DetailTab>("overview");
  const [pendingAction, setPendingAction] = useState<FindingStatus | null>(null);
  const [actionReason, setActionReason] = useState("");
  const reasonRef = useRef<HTMLTextAreaElement>(null);
  const tabRefs = useRef<Record<string, HTMLButtonElement | null>>({});

  const terminal = f.status === "REMEDIATED" || f.status === "ACCEPTED" || f.status === "FALSE_POSITIVE";
  const availableActions = terminal
    ? WORKFLOW.filter((action) => action.status === "OPEN")
    : WORKFLOW.filter((action) => action.status !== "OPEN" && action.status !== f.status);
  const actionBusy = statusUpdating || reopening;
  const reasonValid = actionReason.trim().length >= 3;

  const submitAction = async () => {
    if (!pendingAction || !reasonValid) return;
    const reason = actionReason.trim();
    try {
      if (pendingAction === "OPEN" && f.status === "REMEDIATED") {
        await onReopen(f.id, reason);
      } else {
        await onStatusChange(f.id, pendingAction, reason);
      }
    } catch {
      return; // The mutation already surfaces an actionable toast.
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
  const customerImpact = f.businessImpact || f.impact
    || "Business impact has not been recorded. Validate asset criticality, exposure and reachable attack paths before assigning impact.";
  const chips = signalChips(f);

  const tabs: { id: DetailTab; label: string; badge?: string }[] = [
    { id: "overview", label: "Overview" },
    { id: "intel", label: "Threat intel" },
    { id: "evidence", label: "Evidence", badge: (f.evidenceSummary?.length || f.evidence.length) ? String(f.evidenceSummary?.length || f.evidence.length) : undefined },
    { id: "remediation", label: "Fix plan" },
    { id: "compliance", label: "Compliance", badge: f.compliance.length ? String(f.compliance.length) : undefined },
    { id: "history", label: "History" },
  ];

  /* Roving tab focus. A tablist that cannot be driven with arrow keys is a
   * row of buttons wearing a tablist costume. */
  const onTabKeyDown = (event: React.KeyboardEvent, index: number) => {
    const step = event.key === "ArrowRight" ? 1 : event.key === "ArrowLeft" ? -1 : 0;
    let next = -1;
    if (step) next = (index + step + tabs.length) % tabs.length;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = tabs.length - 1;
    if (next < 0) return;
    event.preventDefault();
    setTab(tabs[next].id);
    tabRefs.current[tabs[next].id]?.focus();
  };

  return (
    <div className="finding-detail-panel">

      {/* Sticky identity bar — stays put through a 400-line evidence scroll,
          so "which finding am I in" and "explain this" never leave reach. */}
      <div className="finding-detail-bar">
        <span className="finding-detail-bar-dot" style={{ background: SEV_COLOR[f.severity] }} aria-hidden />
        <span className="finding-detail-bar-title" title={f.title}>{f.title}</span>
        <button type="button" className="btn btn-secondary finding-detail-explain" onClick={() => onExplain(f.id)}>
          <Brain size={13} aria-hidden /> Explain
        </button>
        <button type="button" className="finding-detail-close" onClick={onClose} aria-label="Close finding detail. Shortcut: Escape">
          <X size={15} aria-hidden />
        </button>
      </div>

      {/* Header */}
      <header className="finding-detail-header" style={{ background: `linear-gradient(160deg, ${tint(SEV_COLOR[f.severity], TINT.wash)} 0%, transparent 62%)` }}>
        <div className="finding-detail-badges">
          <SevBadge s={f.severity} />
          <StatusBadge s={f.status} />
          <PriorityBadge priority={f.aiTriage.priority} compact />
          <RiskBadge score={f.riskScore} />
          <ChipRow chips={chips} max={6} />
          {f.exploitMaturityRecorded && (
            <span className="chip" style={{
              color: MATURITY_COLOR[f.exploitMaturity],
              background: tint(MATURITY_COLOR[f.exploitMaturity], TINT.fill),
              borderColor: tint(MATURITY_COLOR[f.exploitMaturity], TINT.hairline),
            }}>{f.exploitMaturity}</span>
          )}
          <span className="chip" style={{ color: sla.color, background: tint(sla.color, TINT.fill), borderColor: tint(sla.color, TINT.hairline) }}>
            {sla.tracked ? `SLA ${sla.label.toLowerCase()}` : "No SLA target"}
          </span>
        </div>

        <h2 className="finding-detail-title">{f.title}</h2>

        <div className="finding-detail-meta">
          <code>{f.id}</code>
          <span>{f.category}</span>
          <span>{f.affectedHost}</span>
          {f.assignee && <b>@{f.assignee}</b>}
        </div>

        <div className="finding-detail-lifecycle">
          <span>First seen {new Date(f.discoveredAt).toLocaleDateString()}</span>
          {f.lastSeen && <span>Last seen {new Date(f.lastSeen).toLocaleDateString()}</span>}
          {f.resolvedAt && (
            <span style={{ color: SEV_PALETTE.GREEN }}>
              Resolved {new Date(f.resolvedAt).toLocaleDateString()}{f.resolutionMethod ? ` (${f.resolutionMethod})` : ""}
            </span>
          )}
          {f.regression && <span style={{ color: SEV_PALETTE.RED }}>Regressed</span>}
          {typeof f.reopenedCount === "number" && f.reopenedCount > 0 && (
            <span style={{ color: SEV_PALETTE.AMBER }}>Reopened {f.reopenedCount}×</span>
          )}
        </div>

        {cveIds.length > 0 && (
          <div className="finding-cve-list">{cveIds.map((cve) => <code key={cve}>{cve}</code>)}</div>
        )}
      </header>

      {hasAiTriage && (
        <div className="finding-ai-triage">
          <Brain size={14} aria-hidden />
          <div>
            <div className="finding-ai-triage-meta">
              <span>Vedha triage</span>
              <span>{Math.round(f.aiTriage.confidence * 100)}% confidence</span>
            </div>
            <p className="finding-ai-triage-reasoning">{f.aiTriage.reasoning}</p>
            {f.aiTriage.recommendation && (
              <p className="finding-ai-triage-recommendation"><b>Recommends</b> {f.aiTriage.recommendation}</p>
            )}
          </div>
        </div>
      )}

      {/* Action bar */}
      <section className="finding-action-bar" aria-label="Record a lifecycle action">
        <div>
          <strong>Record an action</strong>
          <span>Every decision joins the append-only history with its reason.</span>
        </div>
        <div className="finding-action-options">
          {availableActions.map((action) => (
            <button
              key={action.status}
              type="button"
              onClick={() => { setPendingAction(action.status); setActionReason(""); }}
              disabled={actionBusy}
              data-selected={pendingAction === action.status || undefined}
              style={{ borderColor: tint(action.color, TINT.edge), background: tint(action.color, TINT.fill), color: action.color }}
            >{action.label}</button>
          ))}
        </div>

        {pendingAction && (
          <div className="finding-action-composer">
            <div>
              <label htmlFor={`finding-action-reason-${f.id}`}>
                Why {WORKFLOW.find((action) => action.status === pendingAction)?.label.toLowerCase()}?
              </label>
              <p>{WORKFLOW.find((action) => action.status === pendingAction)?.hint}</p>
              {(REASON_TEMPLATES[pendingAction] ?? []).length > 0 && (
                <div className="finding-action-templates">
                  {(REASON_TEMPLATES[pendingAction] ?? []).map((template, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => {
                        setActionReason(template);
                        window.requestAnimationFrame(() => {
                          const el = reasonRef.current;
                          if (!el) return;
                          el.focus();
                          el.setSelectionRange(el.value.length, el.value.length);
                        });
                      }}
                    >{template.length > 46 ? `${template.slice(0, 46)}…` : template}</button>
                  ))}
                </div>
              )}
            </div>
            <textarea
              ref={reasonRef}
              id={`finding-action-reason-${f.id}`}
              value={actionReason}
              onChange={(event) => setActionReason(event.target.value)}
              onKeyDown={(event) => {
                if ((event.metaKey || event.ctrlKey) && event.key === "Enter") { event.preventDefault(); void submitAction(); }
                if (event.key === "Escape") { event.stopPropagation(); setPendingAction(null); setActionReason(""); }
              }}
              maxLength={1000}
              rows={3}
              placeholder="Write the evidence-based reason a reviewer would need…"
              autoFocus
            />
            <div className="finding-action-composer-footer">
              <span data-warn={!reasonValid && actionReason.length > 0 || undefined}>
                {reasonValid ? `${actionReason.length} / 1000` : "At least 3 characters"}
              </span>
              <button type="button" className="btn btn-ghost" onClick={() => { setPendingAction(null); setActionReason(""); }} disabled={actionBusy}>
                Cancel
              </button>
              <button type="button" className="btn btn-primary" onClick={() => { void submitAction(); }} disabled={actionBusy || !reasonValid} aria-busy={actionBusy}>
                {actionBusy ? <LoaderCircle className="findings-spinner" size={13} aria-hidden /> : <Check size={13} aria-hidden />} Record action
              </button>
            </div>
          </div>
        )}
      </section>

      {/* Tabs */}
      <div className="finding-detail-tabs" role="tablist" aria-label="Finding detail sections">
        {tabs.map((t, index) => (
          <button
            key={t.id}
            ref={(node) => { tabRefs.current[t.id] = node; }}
            id={`finding-tab-${t.id}-${f.id}`}
            role="tab"
            type="button"
            aria-selected={tab === t.id}
            aria-controls={`finding-panel-${f.id}`}
            tabIndex={tab === t.id ? 0 : -1}
            onClick={() => setTab(t.id)}
            onKeyDown={(event) => onTabKeyDown(event, index)}
            data-active={tab === t.id}
          >
            {t.label}
            {t.badge && <i>{t.badge}</i>}
          </button>
        ))}
      </div>

      <div
        id={`finding-panel-${f.id}`}
        role="tabpanel"
        aria-labelledby={`finding-tab-${tab}-${f.id}`}
        className="finding-detail-content"
      >
        {tab === "overview" && (
          <FindingOverview
            finding={f}
            related={related}
            sla={sla}
            customerImpact={customerImpact}
            firstRemediation={firstRemediation}
            onOpenTab={setTab}
          />
        )}
        {tab === "intel" && <IntelPanel finding={f} />}
        {tab === "evidence" && <EvidenceView finding={f} />}
        {tab === "remediation" && <RemediationPlanView finding={f} api={api} surface={surface} />}
        {tab === "compliance" && <CompliancePanel compliance={f.compliance} />}
        {tab === "history" && <HistoryTimeline findingId={f.id} now={now} api={api} surface={surface} />}
      </div>
    </div>
  );
}

/* ─── Urgency model ───────────────────────────────────────────────────────
 * `sla` is passed in rather than recomputed, so the strip, the row and the
 * detail panel can never disagree about the same finding within one render. */
function isUrgent(f: Finding, sla: Sla): boolean {
  if (f.status !== "OPEN" && f.status !== "CONFIRMED") return false;
  return f.activelyExploited || (f.kevStatusRecorded && f.kevListed) || sla.breached || f.severity === "CRITICAL";
}

function urgencyReasons(f: Finding, sla: Sla): string[] {
  const r: string[] = [];
  if (f.activelyExploited) r.push("Actively exploited");
  if (f.kevStatusRecorded && f.kevListed) r.push("CISA KEV");
  if (sla.breached) r.push("SLA breached");
  else if (sla.tracked && sla.pct < 25) r.push(`SLA ${sla.label}`);
  if (f.severity === "CRITICAL") r.push("Critical severity");
  return r;
}

/* "Why now" on a row. Capped at three: a fourth reason has never changed a
 * triage order, it only pushes the metrics grid off the fold. */
function decisionDrivers(f: Finding, sla: Sla): string[] {
  const drivers = urgencyReasons(f, sla);
  if (f.detectionCoverage === "BLIND") drivers.push("Detection blind spot");
  if (f.needsReview) drivers.push("Analyst review required");
  if (f.regression) drivers.push("Regression");
  if (f.verificationState?.toLowerCase() === "contradicted") drivers.push("Evidence contradicted");
  if (f.epssRecorded && f.epssScore >= 0.5) drivers.push(`EPSS ${(f.epssScore * 100).toFixed(0)}%`);
  return [...new Set(drivers)];
}

/* Counts up to `target`, honours reduced motion. Motion here is doing a job:
 * the number is the page's one deliberate animated moment, and it marks the
 * transition from "loading" to "this is your queue". */
function useCountUp(target: number, ms = 750) {
  const [n, setN] = useState(0);
  useEffect(() => {
    let raf = 0;
    if (prefersReducedMotion() || target <= 0) {
      raf = requestAnimationFrame(() => setN(target));
      return () => cancelAnimationFrame(raf);
    }
    const start = performance.now();
    const tick = (t: number) => {
      const p = Math.min(1, (t - start) / ms);
      setN(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, ms]);
  return n;
}

function spotlight(e: React.MouseEvent<HTMLElement>) {
  const r = e.currentTarget.getBoundingClientRect();
  e.currentTarget.style.setProperty("--mx", `${e.clientX - r.left}px`);
  e.currentTarget.style.setProperty("--my", `${e.clientY - r.top}px`);
}

/* ─── Fix-first strip ─────────────────────────────────────────────────────*/
function FixFirstStrip({
  findings, slaFor, total, loading, failed, onRetry, onSelect,
  exploitedActive, slaActive, onToggleExploited, onToggleSla,
  severityCounts, severityActive, onSelectSeverity, countsUnavailable,
}: {
  findings: Finding[];
  slaFor: (f: Finding) => Sla;
  total: number; loading: boolean; failed: boolean; onRetry: () => void; onSelect: (id: string) => void;
  exploitedActive: boolean; slaActive: boolean; onToggleExploited: () => void; onToggleSla: () => void;
  severityCounts: { severity: Severity; count: number }[];
  severityActive: Severity | "ALL";
  onSelectSeverity: (s: Severity) => void;
  countsUnavailable: boolean;
}) {
  const [expanded, setExpanded] = useState(false);

  const { urgent, openRisk, slaBreached, activeCount } = useMemo(() => {
    const openList = findings.filter((f) => f.status === "OPEN" || f.status === "CONFIRMED");
    const urgentList = openList
      .filter((f) => isUrgent(f, slaFor(f)))
      .sort((a, b) => (a.activelyExploited === b.activelyExploited ? b.riskScore - a.riskScore : a.activelyExploited ? -1 : 1));
    return {
      urgent: urgentList,
      openRisk: openList.reduce((s, f) => s + f.riskScore, 0),
      slaBreached: openList.filter((f) => slaFor(f).breached).length,
      activeCount: openList.filter((f) => f.activelyExploited).length,
    };
  }, [findings, slaFor]);

  const hasData = !loading && !failed;
  const accent = failed
    ? SEV_PALETTE.AMBER
    : !hasData
      ? "var(--border-accent)"
      : urgent.length === 0
        ? SEV_PALETTE.GREEN
        : (activeCount > 0 || slaBreached > 0) ? SEV_PALETTE.RED : SEV_PALETTE.ORANGE;

  const urgentN = useCountUp(hasData ? urgent.length : 0);
  const activeN = useCountUp(hasData ? activeCount : 0);
  const slaN = useCountUp(hasData ? slaBreached : 0);
  const openRiskN = useCountUp(hasData ? openRisk : 0);
  const visible = expanded ? urgent : urgent.slice(0, 3);

  return (
    <section
      className="findings-decision-strip gradient-frame spotlight"
      onMouseMove={spotlight}
      aria-labelledby="visible-triage-title"
      style={{ borderTopColor: accent }}
    >
      <div className="findings-strip-head">
        <div>
          <h2 id="visible-triage-title">Open findings by severity</h2>

          {/* Severity counts lead the strip. They come from the summary endpoint,
              so they count every open finding in the current engagement/agent
              scope — not just the twenty rows on this page. Each tile is also the
              severity filter, matching the clickable metrics beside it. */}
          <div className="findings-sev-counts" role="group" aria-label="Open findings by severity">
            {severityCounts.map(({ severity, count }) => {
              const color = SEV_COLOR[severity];
              const active = severityActive === severity;
              return (
                <button
                  type="button"
                  key={severity}
                  className="findings-sev-count"
                  aria-pressed={active}
                  onClick={() => onSelectSeverity(severity)}
                  title={`Filter the queue to ${severity.toLowerCase()} findings`}
                  style={{
                    borderColor: active ? color : tint(color, TINT.hairline),
                    background: active ? tint(color, TINT.fill) : "transparent",
                    ["--rail" as string]: color,
                  }}
                >
                  <strong style={{ color: countsUnavailable ? "var(--text-muted)" : color }}>
                    {countsUnavailable ? "—" : count.toLocaleString()}
                  </strong>
                  <span>{severity}</span>
                </button>
              );
            })}
          </div>

          <p>
            {failed
              ? "Vedha could not verify the current queue, so it makes no claim about safety."
              : loading
                ? "Waiting on finding and SLA signals."
                : `Counts cover every open finding in scope. The queue below shows ${findings.length} of ${total} matching findings.`}
          </p>
          {failed && (
            <button type="button" className="findings-inline-action" onClick={onRetry}>
              <RotateCcw size={13} aria-hidden /> Retry
            </button>
          )}
        </div>

        {hasData && (
          <div className="findings-strip-metrics">
            <div
              className="findings-triage-metric"
              title="Findings on this page that are actively exploited, KEV-listed, SLA-breached or critical"
            >
              <strong className={urgent.length ? "stat-glow" : undefined} style={{ color: accent }}>
                {urgentN.toLocaleString()}
              </strong>
              <span>Needs action</span>
            </div>
            <button
              type="button"
              className="findings-triage-metric"
              onClick={onToggleExploited}
              aria-pressed={exploitedActive}
              title="Filter the queue to confirmed exploitation"
            >
              <strong style={{ color: activeCount ? SEV_PALETTE.RED : "var(--text-primary)" }}>{activeN.toLocaleString()}</strong>
              <span>{activeCount > 0 && <i className="live-dot" style={{ color: SEV_PALETTE.RED }} aria-hidden />}Exploited</span>
            </button>
            <button
              type="button"
              className="findings-triage-metric"
              onClick={onToggleSla}
              aria-pressed={slaActive}
              title="Filter the queue to breached SLAs"
            >
              <strong style={{ color: slaBreached ? SEV_PALETTE.RED : "var(--text-primary)" }}>{slaN.toLocaleString()}</strong>
              <span>SLA breached</span>
            </button>
            <div className="findings-triage-metric" title="Sum of manager risk scores for open findings on this page">
              <strong>{openRiskN.toLocaleString()}</strong>
              <span>Open risk</span>
            </div>
          </div>
        )}
      </div>

      {hasData && urgent.length > 0 && (
        <div className="findings-urgent-grid">
          {visible.map((f) => {
            const reasons = urgencyReasons(f, slaFor(f));
            return (
              <button
                key={f.id}
                type="button"
                onClick={() => onSelect(f.id)}
                onMouseMove={spotlight}
                className="findings-urgent-item spotlight"
                aria-label={`Triage ${f.title}, risk ${f.riskScore} of 1000`}
              >
                <div>
                  <span className="findings-urgent-title">{f.title}</span>
                  <span className="findings-urgent-risk" style={{ color: riskScoreColor(f.riskScore) }}>{f.riskScore}</span>
                </div>
                <div className="findings-urgent-reasons">
                  {reasons.map((r) => <span key={r}>{r}</span>)}
                </div>
                <span className="findings-urgent-host">{f.affectedHost}</span>
              </button>
            );
          })}
          {urgent.length > 3 && (
            <button type="button" className="findings-urgent-more" onClick={() => setExpanded((p) => !p)} aria-expanded={expanded}>
              {expanded ? "Show fewer" : `Show ${urgent.length - 3} more`}
              <ChevronDown size={14} aria-hidden style={{ transform: expanded ? "rotate(180deg)" : "none" }} />
            </button>
          )}
        </div>
      )}
    </section>
  );
}

/* ─── Queue row ───────────────────────────────────────────────────────────
 * Memoised: a 30s poll re-renders the page, and re-rendering twenty rows that
 * did not change is the difference between a snappy list and a janky one. */
const FindingRow = React.memo(function FindingRow({
  f, sla, selected, onSelect,
}: {
  f: Finding; sla: Sla; selected: boolean; onSelect: (id: string) => void;
}) {
  const drivers = decisionDrivers(f, sla).slice(0, 3);
  const chips = signalChips(f);
  return (
    <article
      id={`finding-card-${f.id}`}
      className="finding-card"
      style={{ ["--rail" as string]: SEV_COLOR[f.severity] }}
      data-selected={selected || undefined}
      role="button"
      tabIndex={0}
      aria-current={selected || undefined}
      aria-expanded={selected}
      aria-label={`${f.title}. ${f.severity}. ${f.aiTriage.priority} ${PRIORITY_LABEL[f.aiTriage.priority]}. Risk ${f.riskScore} of 1000.`}
      onClick={() => onSelect(f.id)}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onSelect(f.id);
        }
      }}
    >
      <div className="finding-card-header">
        <div className="finding-card-badges">
          <SevBadge s={f.severity} />
          <StatusBadge s={f.status} />
          <PriorityBadge priority={f.aiTriage.priority} compact />
          <ChipRow chips={chips} max={3} />
        </div>
        <div className="finding-card-risk">
          <strong style={{ color: riskScoreColor(f.riskScore) }}>{f.riskScore}</strong>
          <span>risk</span>
        </div>
      </div>

      <h3 className="finding-card-title">{f.title}</h3>

      <div className="finding-card-context">
        <span className="finding-card-host" title={f.affectedHost}>{f.affectedHost}</span>
        <div className="finding-card-signals">
          <DetectionPill cov={f.detectionCoverage} />
          {f.exploitMaturityRecorded && (
            <span style={{ color: MATURITY_COLOR[f.exploitMaturity] }}>{f.exploitMaturity}</span>
          )}
        </div>
      </div>

      {drivers.length > 0 && (
        <div className="finding-card-drivers">
          <span>Why now</span>
          {drivers.map((driver) => <span className="finding-driver" key={driver}>{driver}</span>)}
        </div>
      )}

      <dl className="finding-card-metrics">
        <div>
          <dt>EPSS</dt>
          <dd style={{ color: f.epssRecorded ? epssColor(f.epssScore) : "var(--text-muted)" }}>
            {f.epssRecorded ? `${(f.epssScore * 100).toFixed(1)}%` : "Not recorded"}
          </dd>
        </div>
        <div>
          <dt>CVSS</dt>
          <dd>{f.cvss || "Not recorded"}</dd>
        </div>
        <div>
          <dt>SLA</dt>
          <dd style={{ color: sla.color }}>{sla.label}</dd>
        </div>
        <div>
          <dt>Evidence</dt>
          <dd>{f.verificationState ? f.verificationState : "Not verified"}</dd>
        </div>
      </dl>
    </article>
  );
});

/* ─── Styles ──────────────────────────────────────────────────────────────
 * Lifted out of the JSX so the page component reads as behaviour, not as a
 * 600-line string. Organised by layer: primitives → panels → queue → detail →
 * responsive. Every colour, face, radius and space resolves to an existing
 * design token; nothing new is introduced here.
 * ───────────────────────────────────────────────────────────────────────── */
const FINDINGS_CSS = `
/* ── 0. Primitives ───────────────────────────────────────────────────── */
.findings-sr-only {
  position: absolute; width: 1px; height: 1px; margin: -1px;
  padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
.findings-workspace ::selection,
.findings-decision-strip ::selection,
.findings-triage-key ::selection { color: var(--text-primary); background: var(--accent-ghost); }

/* One chip geometry for every chip in the page. Mixed heights and radii were
   what made the old badge rows read as noise rather than as a band. */
.chip {
  display: inline-flex; align-items: center; gap: 4px;
  height: 20px; padding: 0 7px;
  border: var(--hairline) solid transparent; border-radius: 5px;
  font: 700 9.5px/1 var(--font-mono); letter-spacing: .02em; white-space: nowrap;
}
.chip-sev { font-weight: 750; letter-spacing: .04em; }
.chip-priority { border-radius: 999px; font-family: var(--font-ui); font-size: 10px; }
.chip-priority b { font: 700 9.5px/1 var(--font-mono); }
.chip-priority span { font-weight: 650; }
.chip-priority[data-compact] { height: 19px; font-size: 9.5px; }
.chip-overflow { color: var(--text-secondary); background: var(--bg-app); border-color: var(--border-subtle); cursor: default; }
.chip-current { color: var(--accent); background: var(--accent-ghost); border-color: var(--border-accent); }

.finding-copy-btn {
  display: inline-grid; place-items: center; width: 24px; height: 24px; flex: 0 0 auto;
  border: 0; border-radius: 6px; color: var(--text-muted); background: transparent; cursor: pointer;
}
.finding-copy-btn:hover { color: var(--text-primary); background: var(--bg-hover); }
.finding-copy-btn[data-state="copied"] { color: var(--nominal-color); }
.finding-copy-btn[data-state="failed"] { color: var(--sev-high-color); }
.finding-copy-btn-labelled {
  display: inline-flex; width: auto; min-width: 60px; min-height: 30px; gap: 6px;
  border: var(--hairline) solid var(--border-default); border-radius: 7px; padding: 0 9px;
  background: var(--bg-panel); font: 600 10.5px/1 var(--font-ui);
}

/* Single focus treatment for the whole page — one visual language for
   "you are here" instead of five near-misses. */
.findings-workspace :focus-visible,
.findings-decision-strip :focus-visible,
.findings-triage-key :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.findings-spinner { animation: findings-spin 850ms linear infinite; }
@keyframes findings-spin { to { transform: rotate(360deg); } }

.finding-data-missing { color: var(--text-muted); font: 400 12px/1.5 var(--font-ui); }
.finding-blank {
  display: flex; gap: 12px; align-items: flex-start;
  border: var(--hairline) dashed var(--border-strong); border-radius: var(--r-lg);
  padding: 18px; background: var(--bg-surface);
}
.finding-blank svg { flex: 0 0 auto; margin-top: 2px; color: var(--text-muted); }
.finding-blank[data-tone="error"] svg { color: var(--sev-high-color); }
.finding-blank strong { display: block; color: var(--text-primary); font: 650 13.5px/1.4 var(--font-ui); }
.finding-blank p { max-width: 62ch; margin: 5px 0 0; color: var(--text-muted); font: 400 12.5px/1.55 var(--font-ui); }
.finding-plan-loading { display: grid; gap: 10px; }

.finding-section-heading { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
.finding-section-heading > div { display: flex; align-items: center; gap: 8px; }
.finding-section-heading svg { color: var(--accent); }
.finding-section-heading h3 { margin: 0; color: var(--text-primary); font: 650 14px/1.35 var(--font-ui); }
.finding-section-heading > span { color: var(--text-muted); font: 500 10px/1.3 var(--font-mono); }

.findings-inline-action,
.findings-clear-filter {
  display: inline-flex; min-height: 32px; align-items: center; justify-content: center; gap: 6px;
  border: var(--hairline) solid var(--border-subtle); border-radius: 8px; padding: 5px 10px;
  color: var(--text-secondary); background: transparent; font: 600 11.5px/1 var(--font-ui); cursor: pointer;
}
.findings-inline-action { margin-top: 10px; color: var(--accent); border-color: var(--border-accent); }
.findings-inline-action:hover, .findings-clear-filter:hover { color: var(--text-primary); background: var(--bg-hover); }

/* ── 1. Risk composition ─────────────────────────────────────────────── */
.risk-breakdown-head { display: flex; justify-content: space-between; gap: 12px; margin-bottom: 7px; }
.risk-breakdown-head span:first-child { color: var(--text-primary); font: 650 11.5px/1.3 var(--font-ui); }
.risk-breakdown-head span:last-child { color: var(--text-muted); font: 500 9.5px/1.3 var(--font-mono); }
.risk-breakdown-bar { display: flex; height: 8px; overflow: hidden; border-radius: 4px; background: var(--track-bg); }
.risk-breakdown-bar i { min-width: 3px; }
.risk-breakdown-bar i[data-empty] { background: var(--border-strong); }
.risk-breakdown-legend { display: flex; flex-wrap: wrap; gap: 6px 14px; margin: 9px 0 0; padding: 0; list-style: none; }
.risk-breakdown-legend li { display: flex; align-items: center; gap: 5px; color: var(--text-secondary); font: 500 10px/1.3 var(--font-ui); }
.risk-breakdown-legend li[data-muted] { color: var(--text-faint); }
.risk-breakdown-legend i { width: 7px; height: 7px; border-radius: 2px; }
.risk-breakdown-legend b { color: var(--text-primary); font: 650 10px/1.3 var(--font-mono); font-variant-numeric: tabular-nums; }
.risk-breakdown-legend li[data-muted] b { color: var(--text-faint); }

/* ── 2. Kill chain ───────────────────────────────────────────────────── */
.kill-chain { display: grid; margin: 0; padding: 0; list-style: none; }
.kill-chain li { display: grid; grid-template-columns: 22px minmax(0, 1fr); }
.kill-chain-rail { display: flex; flex-direction: column; align-items: center; }
.kill-chain-rail i { width: 9px; height: 9px; margin-top: 5px; border-radius: 50%; background: var(--rail); box-shadow: 0 0 0 3px color-mix(in srgb, var(--rail) 16%, transparent); }
.kill-chain-rail s { width: 1px; flex: 1; min-height: 14px; background: color-mix(in srgb, var(--rail) 26%, transparent); }
.kill-chain-body { padding: 0 0 12px 8px; }
.kill-chain-meta { display: flex; align-items: center; gap: 6px; margin-bottom: 3px; }
.kill-chain-meta span { border: var(--hairline) solid; border-radius: 3px; padding: 1px 5px; font: 650 9px/1.4 var(--font-mono); }
.kill-chain-meta code { color: var(--accent); font: 600 9px/1.4 var(--font-mono); }
.kill-chain-body strong { display: block; color: var(--text-primary); font: 650 12px/1.4 var(--font-ui); }
.kill-chain-body p { max-width: 66ch; margin: 2px 0 0; color: var(--text-secondary); font: 400 11.5px/1.5 var(--font-ui); }

/* ── 3. Triage legend ────────────────────────────────────────────────── */
.findings-triage-key {
  margin-bottom: var(--space-4); overflow: hidden;
  border: var(--hairline) solid var(--border-subtle); border-radius: var(--r-lg); background: var(--bg-panel);
}
.findings-triage-key summary {
  display: flex; min-height: 52px; align-items: center; justify-content: space-between; gap: var(--space-4);
  padding: 10px var(--space-5); color: var(--text-primary); cursor: pointer; list-style: none;
}
.findings-triage-key summary::-webkit-details-marker { display: none; }
.findings-triage-key summary > span { display: flex; min-width: 0; flex-direction: column; gap: 3px; }
.findings-triage-key summary strong { font: 650 13px/1.25 var(--font-ui); }
.findings-triage-key summary small { max-width: 88ch; color: var(--text-muted); font: 400 11.5px/1.4 var(--font-ui); }
.findings-triage-key summary svg { flex: 0 0 auto; color: var(--text-muted); transition: transform 180ms var(--ease-out); }
.findings-triage-key[open] summary { border-bottom: var(--hairline) solid var(--border-subtle); }
.findings-triage-key[open] summary svg { transform: rotate(180deg); }
.findings-triage-key-body {
  display: grid; grid-template-columns: minmax(250px, 1fr) minmax(320px, 1.3fr) minmax(260px, .9fr);
  gap: var(--space-5); align-items: start; padding: var(--space-5);
}
.findings-triage-concepts { display: grid; gap: 9px; }
.findings-triage-concepts > div { display: grid; grid-template-columns: 58px minmax(0, 1fr); gap: 10px; }
.findings-triage-concepts strong { color: var(--text-primary); font: 650 11px/1.4 var(--font-ui); }
.findings-triage-concepts span { color: var(--text-muted); font: 400 11px/1.45 var(--font-ui); }
.findings-severity-key { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 14px; }
.findings-severity-key > span { display: grid; grid-template-columns: 7px 56px minmax(0, 1fr); gap: 7px; align-items: center; min-width: 0; }
.findings-severity-key i { width: 7px; height: 7px; border-radius: 2px; }
.findings-severity-key b { color: var(--text-primary); font: 700 9px/1.3 var(--font-mono); letter-spacing: .03em; }
.findings-severity-key em { color: var(--text-muted); font: 400 10.5px/1.4 var(--font-ui); font-style: normal; }
.findings-priority-key { display: flex; flex-wrap: wrap; align-content: flex-start; gap: 6px; }

/* ── 4. Fix-first strip ──────────────────────────────────────────────── */
.findings-decision-strip {
  position: relative; overflow: hidden; margin-bottom: 16px; padding: 18px 20px;
  border: var(--hairline) solid var(--border-subtle); border-top: 2px solid var(--border-accent);
  border-radius: 12px; background: var(--bg-panel); box-shadow: var(--shadow-sm);
}
.findings-strip-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; flex-wrap: wrap; }
.findings-strip-head > div:first-child { min-width: 0; flex: 1 1 320px; }
.findings-strip-head h2 { margin: 0; color: var(--text-primary); font: 650 15px/1.3 var(--font-ui); }
.findings-strip-count { display: flex; align-items: center; gap: 10px; margin-top: 7px; }
.findings-strip-count strong { font: 800 30px/1 var(--font-display); font-variant-numeric: tabular-nums; }
.findings-strip-count span { color: var(--text-primary); font: 650 14px/1.35 var(--font-body); }
.findings-strip-head p { max-width: 70ch; margin: 7px 0 0; color: var(--text-muted); font: 400 12px/1.45 var(--font-ui); }
.findings-strip-metrics { display: flex; align-items: flex-start; gap: 6px; flex-wrap: wrap; }
.findings-triage-metric {
  display: grid; min-width: 88px; min-height: 46px; gap: 4px; justify-items: end;
  border: var(--hairline) solid transparent; border-radius: 9px; padding: 6px 10px;
  background: transparent; text-align: right;
}
button.findings-triage-metric { cursor: pointer; }
button.findings-triage-metric:hover { background: var(--bg-hover); }
.findings-triage-metric[aria-pressed="true"] { border-color: var(--border-accent); background: var(--accent-ghost); }
.findings-triage-metric strong { color: var(--text-primary); font: 700 19px/1 var(--font-mono); font-variant-numeric: tabular-nums; }
.findings-triage-metric span { display: flex; align-items: center; gap: 5px; color: var(--text-secondary); font: 600 9.5px/1.2 var(--font-ui); }
.findings-strip-mix { display: grid; gap: 5px; width: 132px; padding: 6px 0 0 10px; }
.findings-strip-mix .sev-bar { display: flex; height: 8px; overflow: hidden; border-radius: 4px; background: var(--bg-app); }
.findings-strip-mix span { color: var(--text-muted); font: 500 9.5px/1.2 var(--font-mono); text-align: right; }

/* Severity counts — the strip's lead statistic. A colour rail under each tile
   carries the severity without relying on the number's colour alone. */
.findings-sev-counts { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.findings-sev-count {
  display: grid; gap: 5px; justify-items: start; min-width: 86px;
  border: var(--hairline) solid transparent; border-radius: 9px;
  padding: 9px 12px 10px; background: transparent; cursor: pointer; text-align: left;
  border-bottom-width: 3px; border-bottom-color: var(--rail);
  transition: background 140ms var(--ease-out), border-color 140ms var(--ease-out);
}
.findings-sev-count:hover { background: var(--bg-hover); }
.findings-sev-count strong {
  font: 800 26px/1.05 var(--font-display); font-variant-numeric: tabular-nums;
}
.findings-sev-count span {
  color: var(--text-secondary); font: 700 8.5px/1.2 var(--font-mono); letter-spacing: .05em;
}

.findings-urgent-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(256px, 1fr)); gap: 10px; margin-top: 16px; }
.findings-urgent-item {
  display: grid; grid-template-columns: minmax(0, 1fr); gap: 7px;
  padding: 11px 13px; text-align: left; cursor: pointer;
  border: var(--hairline) solid var(--border-subtle); border-radius: 10px; background: var(--bg-app);
  transition: border-color 140ms var(--ease-out), transform 140ms var(--ease-out);
}
/* Grid items default to min-width:auto, so a nowrap host or title would widen the
   track instead of being ellipsised. This is what lets the truncation actually run. */
.findings-urgent-item > * { min-width: 0; }
.findings-urgent-item:hover { border-color: var(--border-strong); transform: translateY(-1px); }
.findings-urgent-item > div:first-child { display: flex; align-items: baseline; justify-content: space-between; gap: 8px; }
.findings-urgent-title { min-width: 0; overflow: hidden; color: var(--text-primary); font: 600 13px/1.35 var(--font-body); text-overflow: ellipsis; white-space: nowrap; }
.findings-urgent-risk { flex: 0 0 auto; font: 700 12px/1 var(--font-mono); font-variant-numeric: tabular-nums; }
.findings-urgent-reasons { display: flex; flex-wrap: wrap; gap: 5px; }
.findings-urgent-reasons span {
  border: var(--hairline) solid color-mix(in srgb, currentColor 20%, transparent); border-radius: 3px;
  padding: 1px 6px; color: var(--sev-critical-color); background: color-mix(in srgb, currentColor 8%, transparent);
  font: 650 9px/1.5 var(--font-mono);
}
.findings-urgent-host { overflow: hidden; color: var(--text-muted); font: 500 9.5px/1.3 var(--font-mono); text-overflow: ellipsis; white-space: nowrap; }
.findings-urgent-more {
  display: flex; align-items: center; justify-content: center; gap: 6px;
  border: var(--hairline) dashed var(--border-strong); border-radius: 10px; padding: 10px;
  color: var(--text-secondary); background: transparent; font: 600 11.5px/1 var(--font-ui); cursor: pointer;
}
.findings-urgent-more:hover { color: var(--text-primary); background: var(--bg-hover); }

/* ── 5. Filters ──────────────────────────────────────────────────────── */
.findings-filter-panel {
  border: var(--hairline) solid var(--border-subtle); border-radius: var(--r-lg);
  padding: var(--space-4); background: var(--bg-panel); box-shadow: var(--shadow-sm);
}
.findings-filter-header { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--space-3); margin-bottom: var(--space-3); }
.findings-filter-header > div:first-child { display: flex; align-items: center; gap: 8px; }
.findings-filter-header svg { flex: 0 0 auto; color: var(--text-muted); }
.findings-filter-header h2 { margin: 0 0 3px; color: var(--text-primary); font: 650 14.5px/1.25 var(--font-ui); }
.findings-filter-header p { margin: 0; color: var(--text-muted); font: 400 12px/1.4 var(--font-ui); }
.findings-search {
  display: flex; min-height: 42px; align-items: center; gap: 9px; margin-bottom: var(--space-3);
  border: var(--hairline) solid var(--border-strong); border-radius: 9px; padding: 0 10px 0 12px; background: var(--bg-app);
}
.findings-search:focus-within { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-ghost); }
.findings-search input {
  width: 100%; border: 0; outline: 0; color: var(--text-primary); background: transparent;
  font: 400 13px/1.4 var(--font-ui); caret-color: var(--accent);
}
.findings-search input::placeholder { color: var(--text-muted); opacity: 1; }
.findings-search kbd {
  flex: 0 0 auto; border: var(--hairline) solid var(--border-subtle); border-radius: 4px; padding: 2px 6px;
  color: var(--text-muted); background: var(--bg-panel); font: 600 10px/1.2 var(--font-mono);
}
.findings-search button { display: inline-grid; width: 24px; height: 24px; flex: 0 0 auto; place-items: center; border: 0; border-radius: 6px; color: var(--text-muted); background: transparent; cursor: pointer; }
.findings-search button:hover { color: var(--text-primary); background: var(--bg-hover); }
.findings-shortcuts { display: flex; flex-wrap: wrap; gap: 5px 12px; margin-bottom: var(--space-4); color: var(--text-faint); font: 500 10px/1.4 var(--font-ui); }
.findings-shortcuts span { display: inline-flex; align-items: center; gap: 5px; }
.findings-shortcuts b { color: var(--text-muted); font: 600 10px/1.2 var(--font-mono); }
.findings-scope-grid {
  display: grid; grid-template-columns: repeat(2, minmax(210px, 1fr)); gap: 12px;
  margin-bottom: var(--space-4); padding-bottom: var(--space-4); border-bottom: var(--hairline) solid var(--border-subtle);
}
.findings-filter-grid { display: grid; grid-template-columns: minmax(250px, 1.6fr) repeat(3, minmax(140px, .7fr)); gap: 12px; align-items: end; }
.findings-filter-group { min-width: 0; margin: 0; padding: 0; border: 0; }
.findings-filter-group legend, .findings-filter-label {
  display: block; margin-bottom: 6px; color: var(--text-muted);
  font: 650 10.5px/1.2 var(--font-ui); letter-spacing: .01em;
}
.findings-severity-controls { display: flex; min-height: 38px; gap: 5px; flex-wrap: wrap; }
.findings-severity-controls button, .findings-signal-filter {
  display: inline-flex; min-height: 34px; align-items: center; justify-content: center; gap: 6px;
  border-radius: 8px; padding: 6px 10px; font: 650 10.5px/1 var(--font-ui); cursor: pointer;
}
.findings-filter-control {
  width: 100%; min-height: 38px; border: var(--hairline) solid var(--border-subtle); border-radius: 8px;
  padding: 0 10px; color: var(--text-secondary); background: var(--bg-app);
  font: 500 12px/1.2 var(--font-ui); outline: none; cursor: pointer;
}
.findings-filter-control:hover { border-color: var(--border-strong); }
.findings-signal-filters {
  display: flex; align-items: center; gap: 7px; flex-wrap: wrap;
  margin-top: var(--space-3); padding-top: var(--space-3); border-top: var(--hairline) solid var(--border-subtle);
}
.findings-signal-filters > span:first-child { margin-right: 2px; color: var(--text-muted); font: 650 10.5px/1 var(--font-ui); }

/* ── 6. Queue ────────────────────────────────────────────────────────── */
/* Centred page column. The PageShell main element is full-bleed, so without this
   the workspace stretched across an ultrawide display and the queue drifted away
   from the detail panel. 1180px matches the campaign and scans screens. */
/* Width and centring come from .vedha-page-container in the shell, so the
   findings column widens on a large display instead of stranding margin. */
.findings-page { width: 100%; }
.findings-agent-refresh { display: flex; align-items: center; gap: 8px; }
.findings-agent-refresh-status {
  display: inline-flex; min-width: 0; align-items: center; gap: 6px;
  color: var(--text-secondary); font: 550 10.5px/1.3 var(--font-ui); white-space: nowrap;
}
.findings-agent-refresh-status i { width: 6px; height: 6px; flex: 0 0 auto; border-radius: 50%; background: var(--text-muted); }
.findings-agent-refresh-status[data-tone="active"] i { background: var(--nominal-color); }
.findings-agent-refresh-status[data-tone="error"] { color: var(--sev-medium-color); }
.findings-agent-refresh-status[data-tone="error"] i { background: var(--sev-medium-color); }
.findings-agent-refresh-button {
  display: inline-flex; min-height: 32px; align-items: center; justify-content: center; gap: 6px;
  border: var(--hairline) solid var(--border-default); border-radius: 7px; padding: 0 10px;
  color: var(--text-secondary); background: var(--bg-panel);
  font: 650 11px/1.2 var(--font-ui); white-space: nowrap; cursor: pointer;
}
.findings-agent-refresh-button:hover:not(:disabled) { border-color: var(--border-strong); background: var(--bg-hover); }
.findings-agent-refresh-button:disabled { color: var(--text-muted); cursor: wait; }
.findings-agent-refresh-button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.findings-workspace { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--space-4); align-items: start; }
.findings-workspace[data-detail="true"] { grid-template-columns: minmax(300px, 356px) minmax(0, 1fr); gap: 18px; }
/* Give the queue a share of the extra width on large displays rather than
   handing all of it to the detail pane. Pairs with the --page-max ladder. */
@media (min-width: 1600px) {
  .findings-workspace[data-detail="true"] { grid-template-columns: minmax(340px, 420px) minmax(0, 1fr); gap: 20px; }
  .findings-workspace[data-detail="true"] .finding-card-metrics { grid-template-columns: repeat(4, minmax(0, 1fr)); }
}
@media (min-width: 1920px) {
  .findings-workspace[data-detail="true"] { grid-template-columns: minmax(380px, 460px) minmax(0, 1fr); gap: 24px; }
}
.findings-queue { display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.findings-list { display: flex; flex-direction: column; gap: 6px; }
.findings-list[data-refreshing="true"] { opacity: .72; transition: opacity 160ms var(--ease-out); }

/* The rail is the scan target: severity is read down the left edge without
   parsing a single word. It replaces nothing — the badge stays for the
   colour-blind and screen-reader path — it just makes the column skimmable. */
.finding-card {
  position: relative; border: var(--hairline) solid var(--border-subtle); border-left: 3px solid var(--rail);
  border-radius: 10px; padding: 13px 14px; background: var(--bg-panel); cursor: pointer;
  transition: border-color 140ms var(--ease-out), background 140ms var(--ease-out);
}
.finding-card:hover { border-color: var(--border-strong); background: var(--bg-hover); }
.finding-card[data-selected] { border-color: var(--accent); border-left-color: var(--accent); background: var(--accent-ghost); }
.finding-card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.finding-card-badges { display: flex; min-width: 0; flex: 1; align-items: center; gap: 5px; flex-wrap: wrap; }
.finding-card-risk { display: grid; flex: 0 0 auto; gap: 2px; justify-items: end; }
.finding-card-risk strong { font: 750 17px/1 var(--font-mono); font-variant-numeric: tabular-nums; }
.finding-card-risk span { color: var(--text-muted); font: 600 9px/1 var(--font-ui); }
.finding-card-title {
  display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden;
  max-width: 62ch; margin: 10px 0 8px; color: var(--text-primary); font: 650 14.5px/1.4 var(--font-ui);
}
.finding-card-context { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.finding-card-host { min-width: 0; overflow: hidden; color: var(--text-muted); font: 500 11px/1.3 var(--font-mono); text-overflow: ellipsis; white-space: nowrap; }
.finding-card-signals { display: flex; flex: 0 0 auto; align-items: center; gap: 6px; font: 650 9.5px/1 var(--font-mono); }
.finding-card-drivers { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
.finding-card-drivers > span:first-child { color: var(--text-muted); font: 650 10px/1 var(--font-ui); }
.finding-driver {
  border: var(--hairline) solid var(--border-subtle); border-radius: 999px; padding: 3px 8px;
  color: var(--text-secondary); background: var(--bg-app); font: 600 10px/1 var(--font-ui);
}
.finding-card-metrics {
  display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px;
  margin: 11px 0 0; padding-top: 10px; border-top: var(--hairline) solid var(--border-subtle);
}
.finding-card-metrics > div { min-width: 0; }
.finding-card-metrics dt { color: var(--text-muted); font: 650 9px/1 var(--font-ui); }
.finding-card-metrics dd {
  margin: 4px 0 0; overflow: hidden; color: var(--text-primary);
  font: 650 11px/1.2 var(--font-mono); font-variant-numeric: tabular-nums;
  text-overflow: ellipsis; white-space: nowrap; text-transform: capitalize;
}
.findings-workspace[data-detail="true"] .finding-card-metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }

/* ── 7. Detail ───────────────────────────────────────────────────────── */
.finding-detail-column {
  position: sticky; top: var(--space-3); align-self: start; min-width: 0;
  max-height: calc(100dvh - 100px); overflow-y: auto; overscroll-behavior: contain;
  scrollbar-gutter: stable; scrollbar-width: thin; scrollbar-color: var(--border-strong) transparent;
}
.finding-detail-column::-webkit-scrollbar { width: 8px; }
.finding-detail-column::-webkit-scrollbar-track { background: transparent; }
.finding-detail-column::-webkit-scrollbar-thumb { border: 2px solid transparent; border-radius: 999px; background: var(--border-strong); background-clip: padding-box; }
.finding-detail-panel {
  overflow: hidden; border: var(--hairline) solid var(--border-default); border-radius: var(--r-lg);
  background: var(--bg-panel); box-shadow: var(--shadow-md);
  animation: finding-detail-enter 200ms var(--ease-out) both;
}
@keyframes finding-detail-enter {
  from { opacity: .9; transform: translateX(10px); }
  to { opacity: 1; transform: translateX(0); }
}
.finding-detail-bar {
  position: sticky; top: 0; z-index: 4; display: flex; align-items: center; gap: 10px;
  min-height: 44px; padding: 0 12px 0 16px;
  border-bottom: var(--hairline) solid var(--border-subtle);
  background: color-mix(in srgb, var(--bg-panel) 88%, transparent); backdrop-filter: blur(8px);
}
.finding-detail-bar-dot { width: 8px; height: 8px; flex: 0 0 auto; border-radius: 2px; }
.finding-detail-bar-title { min-width: 0; flex: 1; overflow: hidden; color: var(--text-primary); font: 650 12.5px/1.3 var(--font-ui); text-overflow: ellipsis; white-space: nowrap; }
.finding-detail-explain { height: 28px; flex: 0 0 auto; padding: 0 10px; font-size: 11px; }
.finding-detail-close { display: inline-grid; width: 30px; height: 30px; flex: 0 0 auto; place-items: center; border: 0; border-radius: 7px; color: var(--text-muted); background: transparent; cursor: pointer; }
.finding-detail-close:hover { color: var(--text-primary); background: var(--bg-hover); }
.finding-detail-header { padding: 16px 20px 18px; border-bottom: var(--hairline) solid var(--border-subtle); }
.finding-detail-badges { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
.finding-detail-title { max-width: 34ch; margin: 0; color: var(--text-primary); font: 700 20px/1.32 var(--font-ui); letter-spacing: -.018em; text-wrap: balance; }
.finding-detail-meta { display: flex; align-items: center; gap: 6px 12px; flex-wrap: wrap; margin-top: 8px; }
.finding-detail-meta code { color: var(--accent); font: 600 10.5px/1.4 var(--font-mono); }
.finding-detail-meta span { color: var(--text-secondary); font: 500 10.5px/1.4 var(--font-mono); }
.finding-detail-meta b { color: var(--accent); font: 600 10.5px/1.4 var(--font-mono); }
.finding-detail-lifecycle { display: flex; align-items: center; gap: 6px 14px; flex-wrap: wrap; margin-top: 10px; color: var(--text-muted); font: 500 10px/1.4 var(--font-mono); }
.finding-cve-list { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }
.finding-cve-list code { border: var(--hairline) solid var(--border-subtle); border-radius: 4px; padding: 2px 6px; color: var(--text-secondary); background: var(--bg-app); font: 600 9.5px/1.3 var(--font-mono); }

.finding-ai-triage { display: flex; align-items: flex-start; gap: 10px; padding: 13px 20px; border-bottom: var(--hairline) solid var(--border-subtle); background: var(--accent-ghost); }
.finding-ai-triage > svg { flex: 0 0 auto; margin-top: 2px; color: var(--accent); }
.finding-ai-triage > div { min-width: 0; flex: 1; }
.finding-ai-triage-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }
.finding-ai-triage-meta span:first-child { color: var(--accent); font: 700 9.5px/1.3 var(--font-mono); letter-spacing: .04em; }
.finding-ai-triage-meta span:last-child { color: var(--text-secondary); font: 500 9.5px/1.3 var(--font-mono); }
.finding-ai-triage-reasoning { max-width: 72ch; margin: 0; color: var(--text-primary); font: 400 12.5px/1.6 var(--font-ui); }
.finding-ai-triage-recommendation { max-width: 72ch; margin: 5px 0 0; color: var(--accent); font: 550 12.5px/1.55 var(--font-ui); }
.finding-ai-triage-recommendation b { font: 700 9.5px/1.4 var(--font-mono); letter-spacing: .03em; }

.finding-action-bar {
  display: grid; grid-template-columns: minmax(180px, .7fr) minmax(0, 1.3fr); gap: 12px 18px; align-items: center;
  padding: 12px 20px; border-bottom: var(--hairline) solid var(--border-subtle); background: var(--bg-panel);
}
.finding-action-bar > div:first-child { display: flex; min-width: 0; flex-direction: column; gap: 3px; }
.finding-action-bar strong { color: var(--text-primary); font: 650 12.5px/1.3 var(--font-ui); }
.finding-action-bar > div:first-child span { color: var(--text-muted); font: 400 11px/1.45 var(--font-ui); }
.finding-action-options { display: flex; justify-content: flex-end; gap: 6px; flex-wrap: wrap; }
.finding-action-options button {
  min-height: 34px; border: var(--hairline) solid; border-radius: 8px; padding: 7px 11px;
  font: 650 11.5px/1.2 var(--font-ui); cursor: pointer;
}
.finding-action-options button:disabled { cursor: wait; opacity: .5; }
.finding-action-options button[data-selected] { box-shadow: 0 0 0 3px color-mix(in srgb, currentColor 14%, transparent); }
.finding-action-composer {
  grid-column: 1 / -1; display: grid; grid-template-columns: minmax(200px, .7fr) minmax(0, 1.3fr);
  gap: 10px 18px; align-items: start; padding-top: 12px; border-top: var(--hairline) solid var(--border-subtle);
}
.finding-action-composer label { display: block; color: var(--text-primary); font: 650 12px/1.3 var(--font-ui); }
.finding-action-composer > div:first-child p { margin: 4px 0 0; color: var(--text-muted); font: 400 11px/1.45 var(--font-ui); }
.finding-action-templates { display: grid; gap: 4px; margin-top: 8px; }
.finding-action-templates button {
  border: var(--hairline) dashed var(--border-strong); border-radius: 7px; padding: 5px 8px;
  color: var(--text-secondary); background: transparent; font: 400 10.5px/1.35 var(--font-ui);
  text-align: left; cursor: pointer;
}
.finding-action-templates button:hover { color: var(--text-primary); border-style: solid; background: var(--bg-hover); }
.finding-action-composer textarea {
  width: 100%; min-height: 78px; resize: vertical; border: var(--hairline) solid var(--border-default);
  border-radius: 8px; padding: 10px 11px; color: var(--text-primary); background: var(--bg-app);
  font: 400 12px/1.5 var(--font-ui); caret-color: var(--accent);
}
.finding-action-composer textarea::placeholder { color: var(--text-muted); opacity: 1; }
.finding-action-composer-footer { grid-column: 2; display: flex; align-items: center; justify-content: flex-end; gap: 8px; }
.finding-action-composer-footer > span { margin-right: auto; color: var(--text-muted); font: 500 9.5px/1.2 var(--font-mono); }
.finding-action-composer-footer > span[data-warn] { color: var(--sev-high-color); }

.finding-detail-tabs {
  position: sticky; top: 44px; z-index: 3; display: flex; overflow-x: auto;
  border-bottom: var(--hairline) solid var(--border-default); background: var(--bg-panel); scrollbar-width: none;
}
.finding-detail-tabs::-webkit-scrollbar { display: none; }
.finding-detail-tabs button {
  display: inline-flex; min-height: 42px; align-items: center; gap: 6px; flex: 0 0 auto;
  border: 0; border-bottom: 2px solid transparent; padding: 0 15px;
  color: var(--text-secondary); background: transparent; font: 650 11.5px/1.2 var(--font-ui); cursor: pointer;
}
.finding-detail-tabs button:hover { color: var(--text-primary); background: var(--bg-hover); }
.finding-detail-tabs button[data-active="true"] { border-bottom-color: var(--accent); color: var(--text-primary); background: var(--accent-ghost); }
.finding-detail-tabs button i {
  display: inline-grid; min-width: 16px; height: 16px; place-items: center; padding: 0 4px;
  border-radius: 999px; color: var(--text-secondary); background: var(--bg-app);
  font: 700 9px/1 var(--font-mono); font-style: normal;
}
.finding-detail-tabs button[data-active="true"] i { color: var(--accent); background: var(--bg-panel); }
.finding-detail-tabs button:focus-visible { position: relative; z-index: 1; outline-offset: -3px; }
.finding-detail-content { padding: 20px; }

/* ── 8. Detail panels ────────────────────────────────────────────────── */
.finding-overview-view { display: grid; gap: 22px; }
.finding-overview-view h3 { margin: 0; color: var(--text-primary); font: 650 15px/1.35 var(--font-ui); letter-spacing: -.01em; }
.finding-overview-view h4 { margin: 0 0 9px; color: var(--text-primary); font: 650 12.5px/1.35 var(--font-ui); }
.finding-decision-row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; border: var(--hairline) solid var(--border-subtle); border-radius: 10px; overflow: hidden; }
.finding-decision-row article { padding: 13px 15px; background: var(--bg-surface); }
.finding-decision-row article + article { border-left: var(--hairline) solid var(--border-subtle); }
.finding-decision-row article[data-lead] { background: var(--accent-ghost); }
.finding-decision-row h3 { font: 650 10.5px/1.3 var(--font-ui); color: var(--text-muted); }
.finding-decision-row p { max-width: 46ch; margin: 6px 0 0; color: var(--text-primary); font: 450 12.5px/1.55 var(--font-ui); }
.finding-decision-row .findings-inline-action { margin-top: 9px; min-height: 28px; padding: 4px 9px; font-size: 11px; }
.finding-overview-layout { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(240px, .7fr); gap: 22px; align-items: start; }
.finding-overview-narrative { display: grid; gap: 16px; }
.finding-overview-narrative section + section { padding-top: 16px; border-top: var(--hairline) solid var(--border-subtle); }
.finding-overview-narrative p { max-width: 72ch; margin: 8px 0 0; color: var(--text-secondary); font: 400 13.5px/1.65 var(--font-ui); }
.finding-overview-facts { border: var(--hairline) solid var(--border-subtle); border-radius: 10px; padding: 14px; background: var(--bg-surface); }
.finding-overview-facts > div { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.finding-overview-facts > div svg { color: var(--accent); }
.finding-overview-facts h3 { font-size: 13px; }
.finding-overview-facts dl, .finding-overview-technical-grid dl { display: grid; margin: 0; }
.finding-overview-facts dl > div, .finding-overview-technical-grid dl > div {
  display: grid; grid-template-columns: minmax(84px, .6fr) minmax(0, 1fr); gap: 12px;
  padding: 8px 0; border-top: var(--hairline) solid var(--border-subtle);
}
.finding-overview-facts dt, .finding-overview-technical-grid dt { color: var(--text-muted); font: 600 11px/1.4 var(--font-ui); }
.finding-overview-facts dd, .finding-overview-technical-grid dd { min-width: 0; margin: 0; overflow-wrap: anywhere; color: var(--text-primary); font: 550 12px/1.5 var(--font-ui); }
.finding-overview-technical-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }
.finding-overview-technical-grid > section > h3 { margin-bottom: 8px; }
.finding-overview-technical-grid dd code { font: 500 10px/1.55 var(--font-mono); }
.finding-attack-context { padding-top: 18px; border-top: var(--hairline) solid var(--border-subtle); }
.finding-attack-context-grid { display: grid; grid-template-columns: minmax(210px, .7fr) minmax(0, 1.3fr); gap: 22px; }
.finding-mitre-row { display: grid; grid-template-columns: 70px minmax(0, 1fr); gap: 8px; padding: 6px 0; border-top: var(--hairline) solid var(--border-subtle); }
.finding-mitre-row code { color: var(--accent); font: 600 10px/1.4 var(--font-mono); }
.finding-mitre-row span { color: var(--text-secondary); font: 400 12px/1.45 var(--font-ui); }
.finding-overview-tags { display: flex; align-items: center; flex-wrap: wrap; gap: 5px; margin-top: 12px; color: var(--text-muted); }
.finding-overview-tags span { border: var(--hairline) solid var(--border-subtle); border-radius: 5px; padding: 3px 6px; color: var(--text-secondary); background: var(--bg-surface); font: 500 9px/1.2 var(--font-mono); }
.finding-related-list { margin-top: 18px; }
.finding-related-list > div { display: grid; grid-template-columns: 7px minmax(84px, .5fr) minmax(0, 1fr) auto; gap: 8px; align-items: center; padding: 7px 0; border-top: var(--hairline) solid var(--border-subtle); }
.finding-related-list > div > span { width: 7px; height: 7px; border-radius: 2px; }
.finding-related-list code { color: var(--accent); font: 500 9.5px/1.3 var(--font-mono); }
.finding-related-list strong { min-width: 0; overflow: hidden; color: var(--text-primary); font: 550 11.5px/1.3 var(--font-ui); text-overflow: ellipsis; white-space: nowrap; }

/* Reading measure and rhythm for the three narrative sections. Body copy on this
   page is what an analyst actually reads before a closure decision, so it gets a
   larger face and a longer line height than the surrounding metadata. */
.finding-prose {
  max-width: 74ch; margin: 8px 0 0; color: var(--text-secondary);
  font: 400 13.5px/1.7 var(--font-ui); white-space: pre-wrap; overflow-wrap: anywhere;
}
.finding-prose-secondary { margin-top: 10px; color: var(--text-muted); font-size: 12.5px; }

/* Decoded CVSS vector. */
.finding-cvss-decode {
  margin-top: 14px; border: var(--hairline) solid var(--border-subtle);
  border-radius: 10px; padding: 13px 14px; background: var(--bg-surface);
}
.finding-cvss-decode-head { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.finding-cvss-decode h4 { margin: 0; color: var(--text-primary); font: 650 12.5px/1.35 var(--font-ui); }
.finding-cvss-decode-head code { color: var(--accent); font: 600 10px/1.5 var(--font-mono); overflow-wrap: anywhere; }
.finding-cvss-decode ul {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 4px; margin: 11px 0 0; padding: 0; list-style: none;
}
.finding-cvss-decode li {
  display: grid; grid-template-columns: minmax(0, 1fr) auto auto; gap: 8px; align-items: center;
  border: var(--hairline) solid transparent; border-radius: 6px; padding: 5px 8px; background: var(--bg-app);
}
.finding-cvss-decode li[data-aggravating] {
  border-color: color-mix(in srgb, var(--sev-high-color) 24%, transparent);
  background: color-mix(in srgb, var(--sev-high-color) 6%, transparent);
}
.finding-cvss-decode li > span { min-width: 0; color: var(--text-muted); font: 500 10.5px/1.35 var(--font-ui); }
.finding-cvss-decode li > b { color: var(--text-primary); font: 650 11px/1.35 var(--font-ui); }
.finding-cvss-decode li[data-aggravating] > b { color: var(--sev-high-color); }
.finding-cvss-decode li > code { color: var(--text-faint); font: 500 9px/1.35 var(--font-mono); }
.finding-cvss-decode > p { margin: 9px 0 0; color: var(--text-muted); font: 400 11px/1.5 var(--font-ui); }

/* Sources. Each card states what the reader will find, so the link is a
   decision rather than a dare. */
.finding-sources { display: grid; gap: 14px; margin-top: 12px; }
.finding-source-group > h4 {
  margin: 0 0 7px; color: var(--text-muted);
  font: 700 9.5px/1.2 var(--font-mono); letter-spacing: .06em; text-transform: uppercase;
}
.finding-source {
  display: grid; gap: 3px; margin-bottom: 5px;
  border: var(--hairline) solid var(--border-subtle); border-left: 3px solid var(--border-accent);
  border-radius: 8px; padding: 9px 12px; background: var(--bg-surface); text-decoration: none;
  transition: border-color 140ms var(--ease-out), background 140ms var(--ease-out);
}
.finding-source:hover { border-color: var(--accent); border-left-color: var(--accent); background: var(--bg-hover); }
.finding-source-label {
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--accent); font: 650 12px/1.4 var(--font-ui);
}
.finding-source-detail { max-width: 72ch; color: var(--text-muted); font: 400 11.5px/1.5 var(--font-ui); }

.finding-intel-view { display: grid; gap: 14px; }
.finding-intel-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(268px, 1fr)); gap: 14px; }
.finding-intel-card { border: var(--hairline) solid var(--border-subtle); border-radius: 10px; padding: 14px 15px; background: var(--bg-surface); }
.finding-intel-card[data-alert] { border-color: color-mix(in srgb, var(--sev-critical-color) 26%, transparent); }
.finding-intel-card > header { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 10px; }
.finding-intel-card h3 { margin: 0; color: var(--text-primary); font: 650 13px/1.35 var(--font-ui); }
.finding-intel-card > header > span { color: var(--text-muted); font: 650 10px/1.3 var(--font-mono); }
.finding-intel-card p { max-width: 62ch; margin: 9px 0 0; color: var(--text-secondary); font: 400 11.5px/1.55 var(--font-ui); }
.finding-intel-score { display: flex; align-items: baseline; gap: 8px; margin-bottom: 9px; }
.finding-intel-score strong { font: 800 30px/1 var(--font-mono); font-variant-numeric: tabular-nums; }
.finding-intel-score span { color: var(--text-muted); font: 500 11px/1 var(--font-mono); }
.finding-intel-meter { height: 6px; overflow: hidden; border-radius: 3px; background: var(--track-bg); }
.finding-intel-meter i { display: block; height: 100%; border-radius: 3px; }
.finding-intel-card .risk-breakdown { margin-top: 14px; padding-top: 13px; border-top: var(--hairline) solid var(--border-subtle); }
.finding-intel-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.finding-intel-flag { color: var(--sev-critical-color) !important; font-family: var(--font-mono) !important; font-size: 10px !important; }
.finding-intel-coverage { display: grid; gap: 4px; margin: 10px 0 0; padding: 0; list-style: none; }
.finding-intel-coverage li { display: grid; grid-template-columns: 66px minmax(0, 1fr) auto; gap: 8px; align-items: center; border-radius: 5px; padding: 4px 7px; background: var(--bg-app); }
.finding-intel-coverage code { color: var(--accent); font: 600 9px/1.3 var(--font-mono); }
.finding-intel-coverage span { min-width: 0; overflow: hidden; color: var(--text-secondary); font: 400 10.5px/1.35 var(--font-ui); text-overflow: ellipsis; white-space: nowrap; }
.finding-intel-coverage b { font: 700 8.5px/1.3 var(--font-mono); }

.finding-compliance-view { display: grid; gap: 12px; }
.finding-compliance-view section { border: var(--hairline) solid var(--border-subtle); border-radius: 10px; padding: 12px 15px; background: var(--bg-surface); }
.finding-compliance-view h4 { margin: 0 0 8px; color: var(--accent); font: 650 11.5px/1.35 var(--font-mono); }
.finding-compliance-view ul { display: grid; gap: 4px; margin: 0; padding-left: 16px; }
.finding-compliance-view li { max-width: 76ch; color: var(--text-primary); font: 400 12.5px/1.5 var(--font-ui); }

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
.finding-evidence-artifact summary { display: flex; align-items: center; gap: 11px; padding: 11px 14px; cursor: pointer; list-style: none; }
.finding-evidence-artifact summary::-webkit-details-marker { display: none; }
.finding-evidence-artifact[open] summary { border-bottom: var(--hairline) solid var(--border-subtle); }
.finding-evidence-artifact summary > svg { flex: 0 0 auto; color: var(--text-muted); transition: transform 160ms var(--ease-out); }
.finding-evidence-artifact[open] summary > svg { transform: rotate(180deg); }
.finding-evidence-identity { display: flex; min-width: 0; flex: 1; align-items: center; gap: 10px; }
.finding-evidence-identity > div { min-width: 0; }
.finding-evidence-artifact h4 { margin: 0; overflow: hidden; color: var(--text-primary); font: 650 13.5px/1.35 var(--font-ui); text-overflow: ellipsis; white-space: nowrap; }
.finding-evidence-artifact summary p { margin: 3px 0 0; color: var(--text-muted); font: 500 9.5px/1.3 var(--font-mono); font-variant-numeric: tabular-nums; }
.finding-evidence-artifact[open] { border-color: var(--border-accent); }
.finding-evidence-artifact summary:hover { background: var(--bg-hover); }
.finding-evidence-kind {
  flex: 0 0 auto; border-radius: 5px; padding: 4px 6px;
  color: var(--machine-text); background: var(--machine-bg);
  font: 700 9px/1 var(--font-mono); letter-spacing: .035em;
}
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
.finding-evidence-code {
  max-height: 390px; overflow: auto;
  border-top: var(--hairline) solid var(--border-subtle); border-bottom: var(--hairline) solid var(--border-subtle);
  background: var(--bg-surface); scrollbar-width: thin; scrollbar-color: var(--border-strong) var(--bg-surface);
}
.finding-evidence-code > div { display: grid; grid-template-columns: 46px minmax(0, 1fr); min-height: 24px; }
.finding-evidence-code > div:hover { background: var(--bg-hover); }
.finding-evidence-code span {
  padding: 3px 10px 3px 0; color: var(--text-muted);
  font: 500 9px/1.7 var(--font-mono); text-align: right; user-select: none;
  font-variant-numeric: tabular-nums;
}
.finding-evidence-code code {
  padding: 3px 14px; border-left: var(--hairline) solid var(--border-subtle); color: var(--text-primary);
  font: 500 11px/1.7 var(--font-mono); white-space: pre-wrap; overflow-wrap: anywhere;
}
.finding-evidence-artifact-empty { padding: 22px 14px; border-top: var(--hairline) solid var(--border-subtle); border-bottom: var(--hairline) solid var(--border-subtle); color: var(--text-muted); background: var(--bg-surface); font: 400 11.5px/1.5 var(--font-ui); }
.finding-evidence-artifact > footer { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 14px; color: var(--text-muted); font: 500 9.5px/1.35 var(--font-ui); }

.finding-remediation-view { display: grid; gap: 20px; }
.finding-remediation-view[data-refreshing] { opacity: .75; }
.finding-remediation-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 22px; padding-bottom: 16px; border-bottom: var(--hairline) solid var(--border-subtle); }
.finding-remediation-title { display: flex; align-items: center; gap: 8px; }
.finding-remediation-title svg { color: var(--accent); }
.finding-remediation-view h3 { margin: 0; color: var(--text-primary); font: 650 14.5px/1.35 var(--font-ui); }
.finding-remediation-header > div > p { max-width: 72ch; margin: 8px 0 0; color: var(--text-secondary); font: 400 13px/1.6 var(--font-ui); }
.finding-remediation-meta { display: flex; flex-wrap: wrap; gap: 6px 12px; margin-top: 9px; color: var(--text-muted); font: 500 9.5px/1.3 var(--font-mono); }
.finding-remediation-os { display: grid; min-width: 168px; gap: 5px; }
.finding-remediation-os span { color: var(--text-muted); font: 650 10px/1.2 var(--font-ui); }
.finding-remediation-os select { min-height: 36px; border: var(--hairline) solid var(--border-default); border-radius: 8px; padding: 0 9px; color: var(--text-primary); background: var(--bg-app); font: 500 11.5px/1.2 var(--font-ui); }
.finding-remediation-note { border-radius: 9px; padding: 13px 14px; background: var(--bg-surface); }
.finding-remediation-note h3 { font-size: 12.5px; }
.finding-remediation-note p { max-width: 76ch; margin: 7px 0 0; color: var(--text-secondary); font: 400 12.5px/1.6 var(--font-ui); white-space: pre-wrap; }
.finding-remediation-steps { display: grid; margin: 0; padding: 0; list-style: none; }
.finding-remediation-steps > li { display: grid; grid-template-columns: 30px minmax(0, 1fr); gap: 13px; padding: 15px 0; border-top: var(--hairline) solid var(--border-subtle); }
.finding-remediation-step-number {
  display: grid; width: 30px; height: 30px; place-items: center; border-radius: 8px;
  color: var(--accent); background: var(--accent-ghost);
  border: var(--hairline) solid var(--border-accent);
  font: 700 11px/1 var(--font-mono);
}
.finding-remediation-steps header { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.finding-remediation-steps h4 { margin: 0; color: var(--text-primary); font: 650 13px/1.4 var(--font-ui); }
.finding-remediation-steps header span {
  display: inline-flex; align-items: center; height: 19px; flex: 0 0 auto; padding: 0 8px;
  border: var(--hairline) solid transparent; border-radius: 999px;
  color: var(--text-secondary); background: var(--bg-app); border-color: var(--border-subtle);
  font: 650 9.5px/1 var(--font-ui); white-space: nowrap;
}
.finding-remediation-steps header span[data-risk="medium"] {
  color: var(--sev-medium-color);
  background: color-mix(in srgb, var(--sev-medium-color) 9%, transparent);
  border-color: color-mix(in srgb, var(--sev-medium-color) 26%, transparent);
}
.finding-remediation-steps header span[data-risk="high"] {
  color: var(--sev-critical-color);
  background: color-mix(in srgb, var(--sev-critical-color) 9%, transparent);
  border-color: color-mix(in srgb, var(--sev-critical-color) 28%, transparent);
}
.finding-remediation-steps li p { max-width: 76ch; margin: 6px 0 0; color: var(--text-secondary); font: 400 12.5px/1.6 var(--font-ui); }
.finding-remediation-commands { display: grid; gap: 5px; margin-top: 10px; }
.finding-remediation-commands > div { display: flex; align-items: flex-start; gap: 8px; border: var(--hairline) solid var(--border-subtle); border-radius: 7px; padding: 6px 6px 6px 10px; background: var(--bg-surface); }
.finding-remediation-commands code { min-width: 0; flex: 1; overflow-wrap: anywhere; color: var(--text-primary); font: 500 10.5px/1.6 var(--font-mono); white-space: pre-wrap; }
.finding-remediation-verify, .finding-remediation-warning {
  display: flex; align-items: flex-start; gap: 8px;
  margin-top: 10px !important; padding: 8px 10px; border-radius: 7px;
  border: var(--hairline) solid transparent; font-size: 11.5px !important; line-height: 1.55 !important;
}
.finding-remediation-verify {
  color: var(--text-primary) !important;
  background: color-mix(in srgb, var(--nominal-color) 7%, transparent);
  border-color: color-mix(in srgb, var(--nominal-color) 24%, transparent);
}
.finding-remediation-verify svg { flex: 0 0 auto; margin-top: 2px; color: var(--nominal-color); }
.finding-remediation-verify b { color: var(--nominal-color); }
.finding-remediation-warning {
  color: var(--sev-high-color) !important;
  background: color-mix(in srgb, var(--sev-high-color) 8%, transparent);
  border-color: color-mix(in srgb, var(--sev-high-color) 26%, transparent);
}
.finding-remediation-warning svg { flex: 0 0 auto; margin-top: 2px; }
/* Commands are the part people copy wrong, so give them a terminal-grade well. */
.finding-remediation-commands > div { align-items: center; }
.finding-remediation-commands > div:hover { border-color: var(--border-accent); }
.finding-remediation-closeout { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border-top: var(--hairline) solid var(--border-subtle); border-bottom: var(--hairline) solid var(--border-subtle); }
.finding-remediation-closeout section { padding: 15px; }
.finding-remediation-closeout section + section { border-left: var(--hairline) solid var(--border-subtle); }
.finding-remediation-closeout h3 { font-size: 12.5px; }
.finding-remediation-closeout p, .finding-remediation-closeout li { color: var(--text-secondary); font: 400 11.5px/1.55 var(--font-ui); }
.finding-remediation-closeout p { margin: 7px 0 0; }
.finding-remediation-closeout ol, .finding-remediation-closeout ul { margin: 7px 0 0; padding-left: 17px; }

.finding-history-view { display: grid; gap: 16px; }
.finding-history-summary { display: flex; align-items: flex-start; justify-content: space-between; gap: 18px; padding-bottom: 14px; border-bottom: var(--hairline) solid var(--border-subtle); }
.finding-history-summary h3 { margin: 0; color: var(--text-primary); font: 650 14.5px/1.35 var(--font-ui); }
.finding-history-summary p { max-width: 60ch; margin: 6px 0 0; color: var(--text-muted); font: 400 12.5px/1.55 var(--font-ui); }
.finding-history-summary dl { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 10px 18px; margin: 0; }
.finding-history-summary dl > div { display: grid; gap: 3px; }
.finding-history-summary dt { color: var(--text-muted); font: 650 10px/1.25 var(--font-ui); }
.finding-history-summary dd { margin: 0; color: var(--text-primary); font: 600 11px/1.35 var(--font-mono); }
.finding-history-timeline { display: grid; margin: 0; padding: 0; list-style: none; }
.finding-history-timeline > li { display: grid; grid-template-columns: 22px minmax(0, 1fr); }
.finding-history-rail { display: flex; flex-direction: column; align-items: center; }
.finding-history-rail i { width: 9px; height: 9px; margin-top: 5px; border-radius: 50%; background: var(--rail); }
.finding-history-timeline > li[data-current] .finding-history-rail i { width: 11px; height: 11px; box-shadow: 0 0 0 3px color-mix(in srgb, var(--rail) 18%, transparent); }
.finding-history-rail s { width: 1px; flex: 1; min-height: 16px; background: color-mix(in srgb, var(--rail) 24%, transparent); }
.finding-history-timeline article { padding: 0 0 18px 10px; }
.finding-history-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 4px; }
.finding-history-head > span:first-child { color: var(--text-primary); font: 600 12px/1.3 var(--font-ui); }
.finding-history-head em { color: var(--text-faint); font: 400 9px/1.3 var(--font-mono); font-style: normal; }
.finding-history-action { max-width: 72ch; margin: 4px 0 0; color: var(--text-primary); font: 450 13px/1.55 var(--font-ui); }
.finding-history-actor { display: flex; flex-wrap: wrap; gap: 6px 12px; margin-top: 6px; color: var(--text-muted); font: 500 10px/1.4 var(--font-mono); }
.finding-history-actor span:first-child { color: var(--accent); }
.finding-history-timeline blockquote { display: grid; grid-template-columns: 56px minmax(0, 1fr); gap: 8px; margin: 9px 0 0; border: 0; border-radius: 7px; padding: 8px 10px; background: var(--bg-surface); }
.finding-history-timeline blockquote strong { color: var(--text-muted); font: 650 9.5px/1.5 var(--font-ui); }
.finding-history-timeline blockquote span { color: var(--text-primary); font: 400 12.5px/1.55 var(--font-ui); }
.finding-history-details { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0 0; }
.finding-history-details > div { display: flex; gap: 5px; border: var(--hairline) solid var(--border-subtle); border-radius: 5px; padding: 3px 7px; background: var(--bg-app); }
.finding-history-details dt { color: var(--text-muted); font: 600 9px/1.35 var(--font-ui); }
.finding-history-details dd { margin: 0; color: var(--text-secondary); font: 500 9px/1.35 var(--font-mono); }

/* ── 9. Engagement banner ────────────────────────────────────────────── */
.findings-scope-banner {
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  margin-bottom: 12px; padding: 10px 14px; border: var(--hairline) solid var(--border-accent);
  border-radius: 8px; background: var(--accent-ghost);
}
.findings-scope-banner > div { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; color: var(--text-primary); font: 400 12.5px/1.4 var(--font-ui); }
.findings-scope-banner a { color: var(--accent); font-size: 12px; text-decoration: none; }
.findings-scope-banner a:hover { text-decoration: underline; }

/* ── 10. Responsive ──────────────────────────────────────────────────── */
@media (max-width: 1180px) {
  .findings-triage-key-body { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .findings-priority-key { grid-column: 1 / -1; }
  .findings-filter-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .finding-decision-row { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .finding-decision-row article:nth-child(3) { border-left: 0; }
  .finding-decision-row article:nth-child(n+3) { border-top: var(--hairline) solid var(--border-subtle); }
  .finding-overview-layout, .finding-attack-context-grid { grid-template-columns: minmax(0, 1fr); }
  .finding-overview-facts { display: grid; grid-template-columns: 150px minmax(0, 1fr); gap: 14px; }
  .finding-overview-facts > div { align-items: flex-start; margin: 0; }
  .finding-remediation-closeout { grid-template-columns: minmax(0, 1fr); }
  .finding-remediation-closeout section + section { border-top: var(--hairline) solid var(--border-subtle); border-left: 0; }
  .finding-detail-header, .finding-ai-triage, .finding-action-bar { padding-right: 18px; padding-left: 18px; }
  .finding-detail-content { padding: 18px; }
}
@media (max-width: 920px) {
  .findings-workspace[data-detail="true"] { grid-template-columns: minmax(0, 1fr); }
  .finding-detail-column { position: static; max-height: none; overflow: visible; overscroll-behavior: auto; scrollbar-gutter: auto; }
  .findings-triage-key-body { grid-template-columns: minmax(0, 1fr); gap: var(--space-4); }
  .findings-priority-key { grid-column: auto; }
  .findings-workspace[data-detail="true"] .finding-card-metrics { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .finding-action-bar, .finding-action-composer { grid-template-columns: minmax(0, 1fr); }
  .finding-action-options { justify-content: flex-start; }
  .finding-action-composer-footer { grid-column: 1; }
  .finding-overview-technical-grid { grid-template-columns: minmax(0, 1fr); }
  .finding-overview-facts { display: block; }
  .finding-overview-facts > div { margin-bottom: 10px; }
  .findings-shortcuts { display: none; }
}
@media (max-width: 620px) {
  .findings-decision-strip { padding: 16px; }
  .findings-sev-counts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .findings-sev-count { min-width: 0; }
  .findings-strip-metrics { width: 100%; justify-content: space-between; }
  .findings-strip-mix { width: 100%; padding-left: 0; }
  .findings-filter-grid, .findings-scope-grid { grid-template-columns: minmax(0, 1fr); }
  .findings-filter-header { align-items: center; }
  .finding-card-header, .finding-card-context { align-items: flex-start; }
  .finding-card-context { flex-direction: column; gap: 8px; }
  .finding-card-metrics,
  .findings-workspace[data-detail="true"] .finding-card-metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .findings-severity-key, .finding-decision-row { grid-template-columns: minmax(0, 1fr); }
  .finding-decision-row article + article { border-left: 0; border-top: var(--hairline) solid var(--border-subtle); }
  .findings-triage-key summary, .findings-triage-key-body { padding: var(--space-4); }
  .finding-remediation-header, .finding-history-summary, .finding-evidence-summary { flex-direction: column; }
  .finding-remediation-os { width: 100%; }
  .finding-history-summary dl { justify-content: flex-start; }
  .finding-evidence-summary { gap: 14px; }
  .finding-evidence-summary dl { width: 100%; justify-content: space-between; }
  .finding-evidence-artifact summary { align-items: flex-start; }
  .finding-evidence-identity { align-items: flex-start; }
  .finding-evidence-output-heading, .finding-evidence-artifact > footer { align-items: flex-start; flex-direction: column; gap: 4px; }
  .finding-evidence-command { grid-template-columns: auto minmax(0, 1fr); }
  .finding-evidence-command code { grid-column: 1 / -1; }
  .finding-evidence-code > div { grid-template-columns: 36px minmax(0, 1fr); }
  .finding-evidence-code span { padding-right: 7px; }
  .finding-evidence-code code { padding-right: 10px; padding-left: 10px; font-size: 10.5px; }
  .finding-related-list > div { grid-template-columns: 7px minmax(0, 1fr) auto; }
  .finding-related-list code { display: none; }
  .finding-detail-header, .finding-ai-triage, .finding-action-bar { padding-right: 16px; padding-left: 16px; }
  .finding-detail-title { max-width: none; font-size: 18px; }
  .finding-detail-content { padding: 16px; }
  /* Touch targets reach 44px on the surfaces a thumb actually hits. */
  .findings-severity-controls button, .findings-signal-filter,
  .finding-action-options button, .findings-filter-control { min-height: 44px; }
}
@media (prefers-reduced-motion: reduce) {
  .findings-spinner { animation-duration: 1.6s; }
  .findings-triage-key summary svg, .finding-evidence-artifact summary > svg { transition: none; }
  .finding-detail-panel { animation: none; }
  .finding-card, .findings-urgent-item { transition: none; }
  .findings-urgent-item:hover { transform: none; }
}
`;

/* ─── Page ────────────────────────────────────────────────────────────────*/
export function FindingsWorkspace({ surface = "manager" }: { surface?: FindingsWorkspaceSurface }) {
  const { success, error: showError } = useToast();
  const queryClient = useQueryClient();
  const router = useRouter();
  const { explain } = useAssistant();
  const now = useNow();
  const api = useMemo(() => createFindingsWorkspaceApi(surface), [surface]);

  const locationSearch = useSyncExternalStore(subscribeToLocationChange, getLocationSearch, getServerLocationSearch);
  const deepLinkParams = new URLSearchParams(locationSearch);

  const [selectedOverride, setSelectedId] = useState<string | null | undefined>();
  const selectedId = selectedOverride === undefined ? deepLinkParams.get("finding") : selectedOverride;
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
  const engagementId = engagementOverride === undefined ? deepLinkParams.get("engagement") : engagementOverride;

  const searchRef = useRef<HTMLInputElement>(null);
  const detailRef = useRef<HTMLElement>(null);

  const queryString = new URLSearchParams({
    paginated: "true",
    page: String(page),
    page_size: String(FINDINGS_PER_PAGE),
    sort: sortBy,
  });
  if (deferredSearch) queryString.set("search", deferredSearch);
  if (filterSev !== "ALL") queryString.set("severity", filterSev);
  if (filterStatus !== "ALL") queryString.set("status", filterStatus);
  if (filterBlind) queryString.set("detection_status", "missed");
  if (filterExploited) queryString.set("exploit_validated", "true");
  if (filterSlaBreached) queryString.set("sla_breached", "true");
  if (filterNeedsReview) queryString.set("needs_review", "true");
  if (filterVerification !== "ALL") queryString.set("verification_state", filterVerification);
  if (engagementId) queryString.set("engagement_id", engagementId);
  if (filterAgentId) queryString.set("agent_id", filterAgentId);

  const { data, isLoading, isFetching, error, refetch } = useQuery({
    queryKey: [
      "findings-page", surface, page, deferredSearch, filterSev, filterStatus,
      filterBlind, filterExploited, filterSlaBreached, sortBy, engagementId,
      filterNeedsReview, filterVerification, filterAgentId,
    ],
    queryFn: () => api.list<FindingPage>(queryString.toString()),
    refetchInterval: 30_000,
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });

  const summaryParams = new URLSearchParams();
  if (engagementId) summaryParams.set("engagement_id", engagementId);
  if (filterAgentId) summaryParams.set("agent_id", filterAgentId);
  const summarySuffix = summaryParams.toString();
  const summaryQuery = useQuery({
    queryKey: ["findings-summary", surface, engagementId, filterAgentId],
    queryFn: () => api.summary<FindingSummary>(summarySuffix),
    refetchInterval: 30_000,
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });

  const findings = useMemo(() => data?.items ?? [], [data]);
  const total = data?.total ?? 0;
  const pageCount = data?.pages ?? 1;
  const currentPage = data?.page ?? page;
  const stats = summaryQuery.data ?? {
    total: 0, openTotal: 0, criticalOpen: 0, highOpen: 0, mediumOpen: 0,
    lowOpen: 0, infoOpen: 0, validated: 0, blind: 0, averageRisk: 0,
  };
  const severityCounts: { severity: Severity; count: number }[] = [
    { severity: "CRITICAL", count: stats.criticalOpen },
    { severity: "HIGH", count: stats.highOpen },
    { severity: "MEDIUM", count: stats.mediumOpen },
    { severity: "LOW", count: stats.lowOpen },
  ];

  /* One SLA read per finding per clock tick, shared by every consumer. */
  const slaMap = useMemo(() => {
    const map = new Map<string, Sla>();
    for (const f of findings) map.set(f.id, getSlaColor(f.discoveredAt, f.severity, now));
    return map;
  }, [findings, now]);
  const slaFor = useCallback(
    (f: Finding) => slaMap.get(f.id) ?? getSlaColor(f.discoveredAt, f.severity, now),
    [slaMap, now],
  );

  const engagementOptionsQuery = useQuery({
    queryKey: ["engagements", surface],
    queryFn: () => api.engagements<{ engagements: EngagementOption[] }>(),
    retry: (count, err) => !isUnauthorized(err) && count < 2,
  });
  const agentOptionsQuery = useQuery({
    queryKey: ["agents", surface],
    queryFn: () => api.agents<VedhaAgentOption[]>(),
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
  const engagementQuery = useQuery({
    queryKey: ["engagement-name", surface, engagementId],
    queryFn: () => api.engagement<{ engagement?: { name?: string } }>(engagementId ?? "current"),
    enabled: surface === "portal" || Boolean(engagementId),
    retry: false,
  });

  const inCurrentPage = findings.find((f) => f.id === selectedId) ?? null;
  const detailQuery = useQuery({
    queryKey: ["finding-detail", surface, selectedId],
    queryFn: () => api.detail<Finding>(selectedId ?? ""),
    enabled: Boolean(selectedId),
    retry: false,
  });
  const selected = detailQuery.data ?? inCurrentPage ?? null;
  /* A deep-linked finding that is not on this page used to render nothing at
   * all while it loaded, so the workspace silently collapsed back to one
   * column. The detail column now owns its own loading and error states. */
  const detailPending = Boolean(selectedId) && !selected && detailQuery.isLoading;
  const detailFailed = Boolean(selectedId) && !selected && Boolean(detailQuery.error);

  const invalidateFindingData = useCallback(() => {
    void queryClient.invalidateQueries({ queryKey: ["findings-page"] });
    void queryClient.invalidateQueries({ queryKey: ["findings-summary"] });
    void queryClient.invalidateQueries({ queryKey: ["finding-detail"] });
    void queryClient.invalidateQueries({ queryKey: ["finding-events"] });
    void queryClient.invalidateQueries({ queryKey: ["portal", "findings"] });
    for (const mode of ["operator", "portal"] as const) {
      for (const key of ["findingsSummary", "topFindings", "posture", "sla", "activity"] as const) {
        void queryClient.invalidateQueries({ queryKey: consoleQueryKey(mode, key) });
      }
    }
  }, [queryClient]);

  const statusMutation = useMutation({
    mutationFn: ({ id, status, reason }: { id: string; status: FindingStatus; reason: string }) =>
      api.update<Finding>(id, { status, actionReason: reason }),
    onError: (mutationError) => showError("Status update failed", errorMessage(mutationError)),
    onSuccess: (updated) => success("Status updated", `${updated.id} → ${STATUS_LABEL[updated.status]}`),
    onSettled: invalidateFindingData,
  });

  const reopenMutation = useMutation({
    mutationFn: ({ id, reason }: { id: string; reason: string }) =>
      api.reopen<Finding>(id, reason),
    onError: (mutationError) => showError("Reopen failed", errorMessage(mutationError)),
    onSuccess: (updated) => success("Finding reopened", `${updated.id} → open`),
    onSettled: invalidateFindingData,
  });

  const handleStatusChange = useCallback(async (id: string, newStatus: FindingStatus, reason: string) => {
    await statusMutation.mutateAsync({ id, status: newStatus, reason });
  }, [statusMutation]);
  const handleReopen = useCallback(async (id: string, reason: string) => {
    await reopenMutation.mutateAsync({ id, reason });
  }, [reopenMutation]);

  /* Refs keep the row callbacks referentially stable so React.memo holds
   * across the 30s poll. They are synced after commit rather than during
   * render: writing a ref while rendering is a React violation the compiler
   * rejects outright, and it costs nothing here because every reader is an
   * event handler or an effect — both of which run after this has flushed. */
  const selectedRef = useRef<string | null>(null);
  const findingsRef = useRef<Finding[]>(findings);
  const pageCountRef = useRef(1);
  useEffect(() => {
    selectedRef.current = selectedId;
    findingsRef.current = findings;
    pageCountRef.current = pageCount;
  });

  /* `setSelectedId` is a stable useState setter, but it is still declared:
   * the compiler lint infers it as a dependency and rejects an empty array
   * that omits it. Listing it is free — the identity never changes. */
  const toggleFinding = useCallback((id: string) => {
    setSelectedId(selectedRef.current === id ? null : id);
  }, [setSelectedId]);
  const openFinding = useCallback((id: string) => setSelectedId(id), [setSelectedId]);
  const closeDetail = useCallback(() => setSelectedId(null), [setSelectedId]);
  const explainFinding = useCallback((id: string) => {
    if (surface === "portal") {
      router.push(portalFindingAssistantHref(id));
      return;
    }
    explain(id);
  }, [explain, router, surface]);

  const moveSelection = useCallback((delta: number) => {
    const list = findingsRef.current;
    if (!list.length) return;
    const index = list.findIndex((f) => f.id === selectedRef.current);
    const next = index === -1
      ? (delta > 0 ? 0 : list.length - 1)
      : Math.min(list.length - 1, Math.max(0, index + delta));
    const target = list[next];
    setSelectedId(target.id);
    window.requestAnimationFrame(() => {
      document.getElementById(`finding-card-${target.id}`)?.scrollIntoView({
        block: "nearest",
        behavior: prefersReducedMotion() ? "auto" : "smooth",
      });
    });
  }, [setSelectedId]);

  /* Triage is repetitive keyboard work. Slash focuses search, J/K walk the
   * queue, Escape backs out, brackets page. Nothing is bound that would
   * collide with typing. */
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const el = event.target as HTMLElement | null;
      const typing = Boolean(el && (
        el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.tagName === "SELECT" || el.isContentEditable
      ));
      if (event.key === "Escape") {
        if (typing) { el?.blur(); return; }
        if (selectedRef.current) { setSelectedId(null); }
        return;
      }
      if (typing || event.metaKey || event.ctrlKey || event.altKey) return;
      if (event.key === "/") { event.preventDefault(); searchRef.current?.focus(); return; }
      if (event.key === "j" || event.key === "J") { event.preventDefault(); moveSelection(1); return; }
      if (event.key === "k" || event.key === "K") { event.preventDefault(); moveSelection(-1); return; }
      if (event.key === "[") { setSelectedId(null); setPage((p) => Math.max(1, p - 1)); return; }
      if (event.key === "]") { setSelectedId(null); setPage((p) => Math.min(pageCountRef.current, p + 1)); }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [moveSelection]);

  /* On a stacked viewport the detail panel opens below the fold, which reads
   * as "the click did nothing". Bring it into view. */
  useEffect(() => {
    if (!selectedId) return;
    if (typeof window === "undefined" || window.innerWidth > 920) return;
    detailRef.current?.scrollIntoView({ block: "start", behavior: prefersReducedMotion() ? "auto" : "smooth" });
  }, [selectedId]);

  const hasActiveFilters = Boolean(
    search.trim() || filterSev !== "ALL" || filterStatus !== "ALL" || filterBlind || filterExploited
    || filterSlaBreached || filterNeedsReview || filterVerification !== "ALL"
    || (surface === "manager" && Boolean(engagementId)) || filterAgentId,
  );
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
    if (surface === "manager") setEngagementId(null);
    setSortBy("risk");
    setPage(1);
    setSelectedId(null);
  };

  /* Any filter change invalidates the current selection's position in the
   * result set, so it is dropped in one place instead of at fifteen call
   * sites — the original repeated `setSelectedId(null)` on every control. */
  const applyFilter = (mutate: () => void) => {
    mutate();
    setPage(1);
    setSelectedId(null);
  };
  const Shell = surface === "portal" ? PortalShell : PageShell;

  return (
    <Shell
      title="Findings"
      subtitle="Triage, verify and remediate discovered vulnerabilities"
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
        { label: "CRITICAL OPEN",     value: summaryValue(stats.criticalOpen), color: summaryUnavailable ? "var(--text-muted)" : SEV_PALETTE.RED },
        { label: "EXPLOIT CONFIRMED", value: summaryValue(stats.validated),    color: summaryUnavailable ? "var(--text-muted)" : SEV_PALETTE.ORANGE },
        { label: "DETECTION BLIND",   value: summaryValue(stats.blind),        color: summaryUnavailable ? "var(--text-muted)" : SEV_PALETTE.AMBER },
        { label: "AVG RISK /1000",    value: summaryValue(stats.averageRisk),  color: summaryUnavailable ? "var(--text-muted)" : riskScoreColor(stats.averageRisk) },
      ]}
    >
      <style>{FINDINGS_CSS}</style>

      <div className="findings-page">
      <div className="findings-sr-only" role="status" aria-live="polite">
        {selected ? `Open finding: ${selected.title}` : ""}
      </div>

      {(surface === "portal" || engagementId) && (
        <div className="findings-scope-banner">
          <div>
            <Link2 size={14} color="var(--accent)" aria-hidden />
            <span>
              Scoped to <b>{engagementQuery.data?.engagement?.name ?? (engagementId ? `${engagementId.slice(0, 8)}…` : "assigned engagement")}</b>
              {" — "}{total} finding{total === 1 ? "" : "s"}
            </span>
            <Link href={surface === "portal" ? "/portal/scope" : `/engagements/${engagementId}`}>Open the engagement</Link>
          </div>
          {surface === "manager" && (
            <button
              type="button"
              className="btn btn-ghost"
              style={{ height: 28, fontSize: 12 }}
              onClick={() => {
                setEngagementId(null); setPage(1); setSelectedId(null);
                if (typeof window !== "undefined") window.history.replaceState(null, "", "/findings");
              }}
            >
              View all findings
            </button>
          )}
        </div>
      )}

      <TriageKey />

      <FixFirstStrip
        findings={findings}
        slaFor={slaFor}
        total={total}
        loading={isLoading || (isFetching && !data)}
        failed={Boolean(error)}
        onRetry={() => { void refetch(); }}
        onSelect={openFinding}
        exploitedActive={filterExploited}
        slaActive={filterSlaBreached}
        onToggleExploited={() => applyFilter(() => setFilterExploited((p) => !p))}
        onToggleSla={() => applyFilter(() => setFilterSlaBreached((p) => !p))}
        severityCounts={severityCounts}
        severityActive={filterSev}
        countsUnavailable={summaryUnavailable}
        onSelectSeverity={(s) => applyFilter(() => setFilterSev((current) => current === s ? "ALL" : s))}
      />

      <div className="findings-workspace" data-detail={selectedId ? "true" : "false"}>

        {/* ── Queue ── */}
        <div className="findings-queue">

          <section className="findings-filter-panel" aria-labelledby="finding-queue-title">
            <header className="findings-filter-header">
              <div>
                <SlidersHorizontal size={15} aria-hidden />
                <div>
                  <h2 id="finding-queue-title">Analyst queue</h2>
                  <p aria-live="polite">
                    {error
                      ? "Queue unavailable. Retry to verify the current state."
                      : isLoading
                        ? "Loading ranked findings…"
                        : total === 0
                          ? "Nothing matches the current scope."
                          : `${total.toLocaleString()} matching · page ${currentPage} of ${pageCount}`}
                  </p>
                </div>
              </div>
              {hasActiveFilters && (
                <button type="button" className="findings-clear-filter" onClick={clearFilters}>
                  <RotateCcw size={13} aria-hidden /> Clear
                </button>
              )}
            </header>

            <div className="findings-search">
              <Search size={15} color="var(--text-muted)" aria-hidden />
              <input
                ref={searchRef}
                value={search}
                onChange={(e) => applyFilter(() => setSearch(e.target.value))}
                placeholder="Search a title, CVE or finding ID"
                aria-label="Search findings"
              />
              {search
                ? <button type="button" onClick={() => applyFilter(() => setSearch(""))} aria-label="Clear the search"><X size={14} aria-hidden /></button>
                : <kbd aria-hidden>/</kbd>}
            </div>

            <div className="findings-shortcuts" aria-hidden>
              <span><Keyboard size={12} /></span>
              <span><b>J</b> <b>K</b> move</span>
              <span><b>Enter</b> open</span>
              <span><b>Esc</b> close</span>
              <span><b>[</b> <b>]</b> page</span>
            </div>

            <div className="findings-scope-grid">
              <label className="findings-filter-group">
                <span className="findings-filter-label">Engagement</span>
                <select
                  className="findings-filter-control"
                  value={surface === "portal"
                    ? (engagementOptionsQuery.data?.engagements?.[0]?.id ?? "")
                    : (engagementId ?? "")}
                  onChange={(event) => applyFilter(() => setEngagementId(event.target.value || null))}
                  disabled={surface === "portal" || engagementOptionsQuery.isLoading}
                  aria-label={surface === "portal" ? "Assigned engagement (locked to your session)" : "Filter by engagement"}
                >
                  <option value="">{surface === "portal" ? "Assigned engagement" : "All engagements"}</option>
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
                  onChange={(event) => applyFilter(() => setFilterAgentId(event.target.value))}
                  disabled={agentOptionsQuery.isLoading}
                >
                  <option value="">All Vedha agents</option>
                  {(agentOptionsQuery.data ?? []).map((agent) => (
                    <option key={agent.id} value={agent.id}>{agent.name} · {agent.status.toLowerCase()}</option>
                  ))}
                </select>
              </label>
            </div>

            <div className="findings-filter-grid">
              <fieldset className="findings-filter-group">
                <legend>Severity</legend>
                <div className="findings-severity-controls">
                  {(["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"] as const).map((s) => {
                    const active = filterSev === s;
                    const color = s === "ALL" ? "var(--accent)" : SEV_COLOR[s as Severity];
                    return (
                      <button
                        type="button"
                        key={s}
                        aria-pressed={active}
                        onClick={() => applyFilter(() => setFilterSev(s))}
                        style={{
                          border: `var(--hairline) solid ${active ? color : "var(--border-subtle)"}`,
                          background: active ? (s === "ALL" ? "var(--accent-ghost)" : tint(color, TINT.fill)) : "transparent",
                          color: active ? color : "var(--text-secondary)",
                        }}
                      >{s === "ALL" ? "All" : s}</button>
                    );
                  })}
                </div>
              </fieldset>

              <label className="findings-filter-group">
                <span className="findings-filter-label">Lifecycle</span>
                <select
                  className="findings-filter-control"
                  value={filterStatus}
                  onChange={(e) => applyFilter(() => setFilterStatus(e.target.value as FindingStatus | "ALL"))}
                >
                  {(["ALL", "OPEN", "CONFIRMED", "REMEDIATED", "ACCEPTED", "FALSE_POSITIVE"] as const).map((s) => (
                    <option key={s} value={s}>{s === "ALL" ? "All statuses" : STATUS_LABEL[s]}</option>
                  ))}
                </select>
              </label>

              <label className="findings-filter-group">
                <span className="findings-filter-label">Evidence</span>
                <select
                  className="findings-filter-control"
                  value={filterVerification}
                  onChange={(e) => applyFilter(() => setFilterVerification(e.target.value))}
                >
                  {["ALL", "confirmed", "corroborated", "inferred", "contradicted"].map((s) => (
                    <option key={s} value={s}>{s === "ALL" ? "All verdicts" : s.charAt(0).toUpperCase() + s.slice(1)}</option>
                  ))}
                </select>
              </label>

              <label className="findings-filter-group">
                <span className="findings-filter-label">Sort</span>
                <select
                  className="findings-filter-control"
                  value={sortBy}
                  onChange={(e) => applyFilter(() => setSortBy(e.target.value as typeof sortBy))}
                >
                  <option value="risk">Highest risk</option>
                  <option value="cvss">Highest CVSS</option>
                  <option value="epss">Highest EPSS</option>
                  <option value="date">Newest first</option>
                </select>
              </label>
            </div>

            <div className="findings-signal-filters" aria-label="Risk signal filters">
              <span>Signals</span>
              {([
                { key: "exploited", active: filterExploited, color: SEV_PALETTE.RED, icon: <BadgeCheck size={13} aria-hidden />, label: "Exploit confirmed", toggle: () => setFilterExploited((p) => !p) },
                { key: "blind", active: filterBlind, color: SEV_PALETTE.AMBER, icon: <EyeOff size={13} aria-hidden />, label: "Detection blind", toggle: () => setFilterBlind((p) => !p) },
                { key: "sla", active: filterSlaBreached, color: SEV_PALETTE.RED, icon: <AlertTriangle size={13} aria-hidden />, label: "SLA breached", toggle: () => setFilterSlaBreached((p) => !p) },
                { key: "review", active: filterNeedsReview, color: SEV_PALETTE.AMBER, icon: <Flag size={13} aria-hidden />, label: "Needs review", toggle: () => setFilterNeedsReview((p) => !p) },
              ]).map((signal) => (
                <button
                  key={signal.key}
                  type="button"
                  className="findings-signal-filter"
                  aria-pressed={signal.active}
                  onClick={() => applyFilter(signal.toggle)}
                  style={{
                    border: `var(--hairline) solid ${signal.active ? tint(signal.color, TINT.rail) : "var(--border-subtle)"}`,
                    background: signal.active ? tint(signal.color, TINT.fill) : "transparent",
                    color: signal.active ? signal.color : "var(--text-secondary)",
                  }}
                >{signal.icon} {signal.label}</button>
              ))}
            </div>
          </section>

          <div className="findings-list" data-refreshing={isFetching && !isLoading ? "true" : undefined}>
            <DataState
              loading={isLoading}
              error={error}
              isEmpty={findings.length === 0}
              onRetry={() => refetch()}
              skeleton={<SkeletonRows rows={6} height={104} />}
              empty={
                <EmptyState
                  icon={Shield}
                  title={hasActiveFilters ? "Nothing matches these filters" : "No findings yet"}
                  hint={hasActiveFilters
                    ? "Widen or clear a filter to see more."
                    : "Run a vulnerability scan on an in-scope target. Findings land here, ranked by risk."}
                />
              }
            >
              {findings.map((f) => (
                <FindingRow
                  key={f.id}
                  f={f}
                  sla={slaFor(f)}
                  selected={selectedId === f.id}
                  onSelect={toggleFinding}
                />
              ))}
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
                  aria-label="Previous page"
                >
                  <ChevronLeft size={14} aria-hidden />
                </button>
                <span>Page {currentPage} of {pageCount}</span>
                <button
                  type="button"
                  onClick={() => { setSelectedId(null); setPage((current) => Math.min(pageCount, current + 1)); }}
                  disabled={currentPage === pageCount}
                  aria-label="Next page"
                >
                  <ChevronRight size={14} aria-hidden />
                </button>
              </div>
            </nav>
          )}
        </div>

        {/* ── Detail ── */}
        {selectedId && (
          <aside key={selectedId} ref={detailRef} className="finding-detail-column" aria-label={selected ? `Details for ${selected.title}` : "Finding details"}>
            {selected ? (
              <FindingDetail
                f={selected}
                allFindings={findings}
                sla={slaFor(selected)}
                now={now}
                onStatusChange={handleStatusChange}
                statusUpdating={statusMutation.isPending}
                onReopen={handleReopen}
                reopening={reopenMutation.isPending}
                onClose={closeDetail}
                onExplain={explainFinding}
                api={api}
                surface={surface}
              />
            ) : detailFailed ? (
              <div className="finding-detail-panel" style={{ padding: 18 }}>
                <div className="finding-blank" data-tone="error">
                  <AlertTriangle size={17} aria-hidden />
                  <div>
                    <strong>That finding could not be loaded</strong>
                    <p>It may have been removed, or it sits outside your current scope.</p>
                    <button type="button" className="findings-inline-action" onClick={closeDetail}>
                      <ArrowLeft size={13} aria-hidden /> Back to the queue
                    </button>
                  </div>
                </div>
              </div>
            ) : detailPending ? (
              <div className="finding-detail-panel" style={{ padding: 18 }} aria-busy="true">
                <SkeletonRows rows={5} height={72} />
              </div>
            ) : null}
          </aside>
        )}
      </div>
      </div>
    </Shell>
  );
}

export default function FindingsPage() {
  return <FindingsWorkspace surface="manager" />;
}
