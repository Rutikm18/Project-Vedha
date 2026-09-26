// AI Engine: VulnPrioritizer · LLMReportGenerator · HallucinationGuard
// claude-sonnet-4-20250514 · temperature=0.3 · exponential backoff

import crypto from "crypto";

// ── Types ────────────────────────────────────────────────────────────────────

export type ReviewStatus = "pending" | "approved" | "rejected";
export type ReportSection = "executive_summary" | "technical_finding" | "remediation" | "sigma_explanation";

export interface FindingInput {
  id: string; title: string; severity: string;
  cvss: number; cveId?: string; affectedHost: string;
  exploitValidated: boolean; description?: string;
  evidence?: string; mitreTechnique?: string;
}

export interface AssetInput {
  id: string; label: string; criticality: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  internetExposed: boolean; zone: string; lateralReachableCount?: number;
  daysSinceLastPatch?: number;
}

export interface PriorityFeatures {
  cvss: number; epss: number; kevFlag: boolean;
  exploitValidated: boolean; assetCriticality: number;
  lateralReachableCount: number; daysSinceLastPatch: number;
}

export interface ShapExplanation {
  score: number;
  features: { name: string; value: number; contribution: number; pct: number }[];
  modelType: "xgboost" | "fallback_formula";
}

export interface LLMOutput {
  id: string;
  engagementId: string;
  section: ReportSection;
  promptHash: string;
  model: string;
  prompt: string;
  output: string;
  generatedAt: string;
  reviewStatus: ReviewStatus;
  reviewedBy?: string;
  reviewedAt?: string;
  rejectionFeedback?: string;
  hallucinationCheck?: HallucinationResult;
}

export interface HallucinationResult {
  valid: boolean;
  issues: string[];
  confidence: number;
}

export interface ReportJob {
  jobId: string; engagementId: string;
  status: "queued" | "running" | "completed" | "failed";
  progress: number; startedAt: string; completedAt?: string;
  sections: ReportSection[]; completedSections: ReportSection[];
  error?: string;
}

// ── VulnPrioritizer ──────────────────────────────────────────────────────────

const CRITICALITY_SCORE: Record<string, number> = {
  CRITICAL: 1.0, HIGH: 0.75, MEDIUM: 0.5, LOW: 0.25,
};

// Fallback formula weights (from Prompt 3)
const WEIGHTS = {
  cvss:              0.25,
  epss:              0.20,
  kevBonus:          0.20,
  exploitValidated:  0.15,
  assetCrit:         0.10,
  pathDepth:         0.05,
  lateralImpact:     0.05,
};

// Simulated EPSS scores (real service would call api.first.org/epss)
const EPSS_MOCK: Record<string, number> = {
  "CVE-2021-44228": 0.974, "CVE-2017-0144": 0.972,
  "CVE-2021-34527": 0.952, "CVE-2019-0708": 0.948,
  "CVE-2021-3156":  0.728, "CVE-2022-22965": 0.898,
  "CVE-2021-26855": 0.912,
};

// CISA KEV snapshot
const KEV_LIST = new Set([
  "CVE-2021-44228", "CVE-2017-0144", "CVE-2021-34527",
  "CVE-2019-0708", "CVE-2022-22965", "CVE-2021-26855",
]);

export const vulnPrioritizer = {
  // VulnPrioritizer.predict_priority → 0-1000
  predictPriority(finding: FindingInput, asset: AssetInput): number {
    const f = this._buildFeatures(finding, asset);
    const raw =
      f.cvss / 10 * WEIGHTS.cvss +
      f.epss        * WEIGHTS.epss +
      (f.kevFlag ? 1 : 0) * WEIGHTS.kevBonus +
      (f.exploitValidated ? 1 : 0) * WEIGHTS.exploitValidated +
      f.assetCriticality * WEIGHTS.assetCrit +
      Math.min(f.lateralReachableCount / 20, 1) * WEIGHTS.pathDepth +
      Math.min(f.daysSinceLastPatch / 365, 1) * WEIGHTS.lateralImpact;
    return Math.round(raw * 1000);
  },

  // VulnPrioritizer.explain_prediction → SHAP-style feature importances
  explainPrediction(finding: FindingInput, asset: AssetInput): ShapExplanation {
    const f = this._buildFeatures(finding, asset);
    const contribs = [
      { name: "CVSS Score",          value: f.cvss,                     raw: f.cvss / 10 * WEIGHTS.cvss },
      { name: "EPSS Probability",    value: f.epss,                     raw: f.epss * WEIGHTS.epss },
      { name: "KEV Flag",            value: f.kevFlag ? 1 : 0,          raw: (f.kevFlag ? 1 : 0) * WEIGHTS.kevBonus },
      { name: "Exploit Validated",   value: f.exploitValidated ? 1 : 0, raw: (f.exploitValidated ? 1 : 0) * WEIGHTS.exploitValidated },
      { name: "Asset Criticality",   value: f.assetCriticality,         raw: f.assetCriticality * WEIGHTS.assetCrit },
      { name: "Lateral Reach",       value: f.lateralReachableCount,    raw: Math.min(f.lateralReachableCount / 20, 1) * WEIGHTS.pathDepth },
      { name: "Days Since Patch",    value: f.daysSinceLastPatch,       raw: Math.min(f.daysSinceLastPatch / 365, 1) * WEIGHTS.lateralImpact },
    ];
    const total = contribs.reduce((s, c) => s + c.raw, 0);
    const score = this.predictPriority(finding, asset);
    return {
      score,
      modelType: "fallback_formula",
      features: contribs.map((c) => ({
        name: c.name, value: c.value,
        contribution: Math.round(c.raw * 1000),
        pct: total > 0 ? Math.round((c.raw / total) * 100) : 0,
      })).sort((a, b) => b.contribution - a.contribution),
    };
  },

  _buildFeatures(finding: FindingInput, asset: AssetInput): PriorityFeatures {
    return {
      cvss:                finding.cvss,
      epss:                finding.cveId ? (EPSS_MOCK[finding.cveId] ?? 0.1) : 0.1,
      kevFlag:             finding.cveId ? KEV_LIST.has(finding.cveId) : false,
      exploitValidated:    finding.exploitValidated,
      assetCriticality:    CRITICALITY_SCORE[asset.criticality] ?? 0.5,
      lateralReachableCount: asset.lateralReachableCount ?? 5,
      daysSinceLastPatch:  asset.daysSinceLastPatch ?? 90,
    };
  },
};

// ── LLM Report Generator ──────────────────────────────────────────────────────
// Removed. Report generation now runs on the backend
// (manager/backend/app/ai/engagement_report.py) so every model call goes through
// the AI gateway (hybrid pseudonymisation / sovereign models) and the AI audit
// chain. /api/reports/generate is a BFF proxy to it.

// ── HallucinationGuard ───────────────────────────────────────────────────────

const CVE_PATTERN  = /CVE-\d{4}-\d{4,7}/gi;
const CVSS_PATTERN = /(?:CVSS[:\s]+)?(\d+\.\d)/g;
const DESTRUCTIVE_PATTERNS = [
  /\brm\s+-rf?\b/i, /\bDROP\s+TABLE\b/i, /\bformat\s+[a-z]:\\/i,
  /\bshutdown\b/i, /\bdel\s+\/[sf]\b/i, /\btruncate\s+table\b/i,
  /\bmkfs\b/i, /\bwipefs\b/i, /\bdd\s+if=\/dev\/zero\b/i,
];

export const hallucinationGuard = {
  validateCveClaims(text: string, actualCveIds: string[]): HallucinationResult {
    const mentioned = Array.from(new Set((text.match(CVE_PATTERN) ?? []).map((c) => c.toUpperCase())));
    const actual = new Set(actualCveIds.map((c) => c.toUpperCase()));
    const hallucinated = mentioned.filter((c) => !actual.has(c));
    const issues = hallucinated.map((c) => `CVE mentioned but not in engagement data: ${c}`);
    return { valid: issues.length === 0, issues, confidence: issues.length === 0 ? 0.97 : Math.max(0.1, 1 - issues.length * 0.2) };
  },

  validateCvssScores(text: string, actualScores: Record<string, number>): HallucinationResult {
    const issues: string[] = [];
    let m: RegExpExecArray | null;
    CVSS_PATTERN.lastIndex = 0;
    while ((m = CVSS_PATTERN.exec(text)) !== null) {
      const score = parseFloat(m[1]);
      const knownScores = Object.values(actualScores);
      if (knownScores.length > 0 && !knownScores.some((s) => Math.abs(s - score) < 0.1)) {
        issues.push(`CVSS score ${score} not found in engagement data (known: ${knownScores.join(", ")})`);
      }
    }
    return { valid: issues.length === 0, issues, confidence: issues.length === 0 ? 0.95 : Math.max(0.1, 1 - issues.length * 0.15) };
  },

  validateRemediationCommands(text: string): HallucinationResult {
    const issues: string[] = [];
    for (const pattern of DESTRUCTIVE_PATTERNS) {
      const m = text.match(pattern);
      if (m) issues.push(`Potentially destructive command detected: "${m[0]}"`);
    }
    return { valid: issues.length === 0, issues, confidence: issues.length === 0 ? 1.0 : 0.0 };
  },

  validate(text: string, opts: { cveIds?: string[]; cvssScores?: Record<string, number> }): HallucinationResult {
    const results = [
      opts.cveIds ? this.validateCveClaims(text, opts.cveIds) : null,
      opts.cvssScores ? this.validateCvssScores(text, opts.cvssScores) : null,
      this.validateRemediationCommands(text),
    ].filter(Boolean) as HallucinationResult[];

    const issues = results.flatMap((r) => r.issues);
    const confidence = results.reduce((min, r) => Math.min(min, r.confidence), 1.0);
    return { valid: issues.length === 0, issues, confidence };
  },
};

// ── LLM Output Store ─────────────────────────────────────────────────────────

const llmOutputs = new Map<string, LLMOutput>();
const reportJobs = new Map<string, ReportJob>();

function genId() { return Math.random().toString(36).slice(2, 9).toUpperCase(); }
function hashPrompt(p: string) { return crypto.createHash("sha256").update(p).digest("hex").slice(0, 16); }

export const aiReportStore = {
  saveOutput(output: Omit<LLMOutput, "id" | "generatedAt">): LLMOutput {
    const o: LLMOutput = { id: genId(), generatedAt: new Date().toISOString(), ...output };
    llmOutputs.set(o.id, o);
    return o;
  },

  getOutput(id: string) { return llmOutputs.get(id) ?? null; },

  listOutputs(engagementId: string) {
    return [...llmOutputs.values()].filter((o) => o.engagementId === engagementId);
  },

  getDraft(engagementId: string): LLMOutput[] {
    return [...llmOutputs.values()]
      .filter((o) => o.engagementId === engagementId && o.reviewStatus === "pending")
      .sort((a, b) => b.generatedAt.localeCompare(a.generatedAt));
  },

  approve(id: string, reviewedBy: string): LLMOutput | null {
    const o = llmOutputs.get(id);
    if (!o) return null;
    const updated = { ...o, reviewStatus: "approved" as ReviewStatus, reviewedBy, reviewedAt: new Date().toISOString() };
    llmOutputs.set(id, updated);
    return updated;
  },

  reject(id: string, reviewedBy: string, feedback: string): LLMOutput | null {
    const o = llmOutputs.get(id);
    if (!o) return null;
    const updated = { ...o, reviewStatus: "rejected" as ReviewStatus, reviewedBy, reviewedAt: new Date().toISOString(), rejectionFeedback: feedback };
    llmOutputs.set(id, updated);
    return updated;
  },

  createJob(engagementId: string, sections: ReportSection[]): ReportJob {
    const job: ReportJob = {
      jobId: genId(), engagementId, status: "queued", progress: 0,
      startedAt: new Date().toISOString(), sections, completedSections: [],
    };
    reportJobs.set(job.jobId, job);
    return job;
  },

  updateJob(jobId: string, patch: Partial<ReportJob>): ReportJob | null {
    const j = reportJobs.get(jobId);
    if (!j) return null;
    const updated = { ...j, ...patch };
    reportJobs.set(jobId, updated);
    return updated;
  },

  getJob(jobId: string) { return reportJobs.get(jobId) ?? null; },

  hashPrompt,
};

// ── SDK-based AI functions (used by scanner pipeline + APIs) ────────────────

import Anthropic from '@anthropic-ai/sdk';
import type { LiveFinding } from './engine/types';
import { TRIAGE_SYSTEM_PROMPT } from './prompts/triage';
import type { ReportResult } from './prompts/report';

// ReportResult is now the deterministic-scorecard schema defined by the report
// contract (lib/prompts/report.ts). Re-exported so any importer of
// `ReportResult` from this module keeps resolving to the new shape.
export type { ReportResult };

function getClient(): Anthropic {
  return new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
}

function stripFences(text: string): string {
  return text.replace(/^```(?:json)?\s*/i, '').replace(/\s*```\s*$/, '').trim();
}

export async function triageFindings(findings: LiveFinding[]): Promise<LiveFinding[]> {
  if (!process.env.ANTHROPIC_API_KEY) return findings;
  if (findings.length === 0) return [];

  try {
    const client = getClient();
    const msg = await client.messages.create({
      model:      'claude-sonnet-4-6',
      max_tokens: 8192,
      system:     TRIAGE_SYSTEM_PROMPT,
      messages:   [{ role: 'user', content: JSON.stringify({ findings, timestamp: new Date().toISOString() }) }],
    });

    const text    = (msg.content[0] as { text: string }).text;
    const parsed  = JSON.parse(stripFences(text)) as {
      findings: {
        finding_id: string; severity: string; cvss_score: number;
        cvss_vector: string | null; cve_ids: string[];
        false_positive: boolean; false_positive_reason: string | null;
      }[];
    };

    // Merge enriched data back onto original findings by host+title match
    for (const enriched of parsed.findings) {
      const orig = findings.find((f) => f.id === enriched.finding_id);
      if (!orig) continue;
      orig.severity            = enriched.severity as LiveFinding['severity'];
      orig.cvss                = String(enriched.cvss_score);
      orig.cvssVector          = enriched.cvss_vector ?? undefined;
      orig.cveIds              = enriched.cve_ids;
      orig.falsePositive       = enriched.false_positive;
      orig.falsePositiveReason = enriched.false_positive_reason ?? undefined;
    }

    return findings.filter((f) => !f.falsePositive);
  } catch (err) {
    console.warn('[ai-engine] triageFindings failed, returning original findings:', err);
    return findings;
  }
}

export async function chat(
  messages: { role: string; content: string }[],
  systemContext?: string,
): Promise<string> {
  const client = getClient();
  const system = systemContext ?? 'You are a senior penetration tester assistant. You provide tactical, accurate security advice. You never provide guidance outside of authorized security testing.';
  const msg = await client.messages.create({
    model:      'claude-sonnet-4-6',
    max_tokens: 2048,
    system,
    messages:   messages as Anthropic.MessageParam[],
  });
  return (msg.content[0] as { text: string }).text;
}
