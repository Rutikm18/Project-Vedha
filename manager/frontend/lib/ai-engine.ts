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

// ── LLM Report Generator ─────────────────────────────────────────────────────

const MODEL = "claude-sonnet-4-20250514";
const MAX_TOKENS = 4096;

const SYSTEM_PROMPT = `You are Vedha's AI Report Engine — a professional security report writer for VAPT engagements.
CRITICAL RULES (never violate):
1. Only reference CVE IDs, CVSS scores, and technical details explicitly provided in the input data.
2. Never invent CVE IDs, asset names, IP addresses, or vulnerability details.
3. Never include remediation commands that are destructive (rm -rf, DROP TABLE, format, shutdown).
4. Write at a professional level suitable for CISO and Board audiences in executive sections.
5. All technical claims must be traceable to evidence in the provided input.`;

async function callAnthropicWithRetry(
  messages: { role: string; content: string }[],
  apiKey: string,
  maxRetries = 3
): Promise<string> {
  let lastErr: Error = new Error("Unknown error");
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": apiKey,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({ model: MODEL, max_tokens: MAX_TOKENS, temperature: 0.3, system: SYSTEM_PROMPT, messages }),
      });
      if (res.ok) {
        const data = await res.json() as { content: { text: string }[] };
        return data.content[0].text;
      }
      lastErr = new Error(`Anthropic API ${res.status}: ${await res.text()}`);
    } catch (e) {
      lastErr = e as Error;
    }
    if (attempt < maxRetries - 1) {
      await new Promise((r) => setTimeout(r, Math.pow(2, attempt) * 1000)); // exponential backoff
    }
  }
  throw lastErr;
}

// Simulated outputs when API key not configured
const SIMULATED: Record<ReportSection, (ctx: string) => string> = {
  executive_summary: (ctx) => `## Executive Summary\n\n[SIMULATED — configure ANTHROPIC_API_KEY for live generation]\n\nThis assessment of ${ctx} identified critical vulnerabilities across the network perimeter and internal segments. The most significant risk is the complete Domain Admin compromise chain via Kerberoasting and unconstrained delegation — an attacker with standard domain credentials can escalate to full domain compromise in under 30 minutes.\n\nKey risks for the Board:\n1. **Credential theft at scale**: 3 service accounts are Kerberoastable with RC4 encryption, enabling offline password cracking with no network-detectable footprint.\n2. **Detection gap**: 4 of 8 attack techniques executed during the assessment triggered zero SIEM or EDR alerts.\n3. **Lateral movement**: From a single compromised workstation, all 317 corporate assets are reachable within 3 hops.\n\nImmediate actions required: enforce AES-256 Kerberos encryption, enable SMB signing on all hosts, and deploy process injection detection rules in CrowdStrike.`,

  technical_finding: (ctx) => `## Technical Finding\n\n[SIMULATED — configure ANTHROPIC_API_KEY for live generation]\n\n**Finding**: ${ctx}\n\n### Technical Details\nThis vulnerability was confirmed through safe exploitation using non-destructive callback probes. The affected service account uses RC4-HMAC (Etype 23) encryption for Kerberos tickets, enabling offline dictionary attacks against the captured TGS hash.\n\n### Reproduction Steps\n1. Authenticate as any domain user\n2. Execute: GetUserSPNs.py corp.local/user:pass -dc-ip 10.0.0.10 -request\n3. Captured hash: \$krb5tgs\$23\$*svc_backup*...\n4. Crack offline: hashcat -m 13100 hash.txt rockyou.txt\n\n### Impact\nSuccessful exploitation provides credentials for svc_backup which is a member of Backup Operators — a path to Domain Admin via backup privilege abuse.`,

  remediation: (ctx) => `## Remediation Steps\n\n[SIMULATED — configure ANTHROPIC_API_KEY for live generation]\n\n**For**: ${ctx}\n\n1. **Immediately** enforce AES-256 encryption for all service accounts:\n   \`Set-ADUser svc_backup -KerberosEncryptionType AES256\`\n\n2. **Within 24 hours** rotate all service account passwords to 25+ character random strings:\n   \`Set-ADAccountPassword svc_backup -NewPassword (ConvertTo-SecureString -AsPlainText "$(New-Guid)$(New-Guid)" -Force)\`\n\n3. **Within 1 week** migrate all SPNed accounts to Group Managed Service Accounts (gMSA):\n   \`New-ADServiceAccount svc_backup_gMSA -DNSHostName corp.local -ManagedPasswordIntervalInDays 30\`\n\n4. **Within 2 weeks** disable RC4 domain-wide via GPO:\n   Computer Configuration → Windows Settings → Security Settings → Network Security → Configure encryption types allowed for Kerberos\n\n5. **Verification**: Confirm no Event 4769 with TicketEncryptionType=0x17 for 30 days`,

  sigma_explanation: (ctx) => `## Sigma Rule Explanation\n\n[SIMULATED — configure ANTHROPIC_API_KEY for live generation]\n\n**Rule**: ${ctx}\n\nThis Sigma rule detects Kerberoasting attacks by monitoring Windows Security Event 4769 (Kerberos Service Ticket Request) for tickets using RC4 encryption (Ticket Encryption Type 0x17), which is the weaker legacy algorithm that enables offline cracking.\n\n**Why this matters**: Attackers request service tickets using the deliberately chosen RC4 algorithm (even when AES is supported) because RC4 hashes are much faster to crack offline. The rule focuses on volume — more than 5 requests per hour from a single non-DC source is a strong indicator of automated Kerberoasting.\n\n**Tuning guidance**: Whitelist your domain controllers and known legacy service accounts that legitimately require RC4. Alert on the remaining population — false positive rate should be under 5% in most environments.`,
};

export const llmReportGenerator = {
  async generateExecutiveSummary(engagementSummary: {
    name: string; totalFindings: Record<string, number>; attackPathCount: number;
    detectionCoverage: number; topRisks: string[];
  }, apiKey?: string): Promise<string> {
    if (!apiKey) return SIMULATED.executive_summary(engagementSummary.name);

    const prompt = `Generate a 400-600 word executive summary for a CISO/Board audience for the following VAPT engagement:

Engagement: ${engagementSummary.name}
Findings by Severity: ${JSON.stringify(engagementSummary.totalFindings)}
Attack Paths Found: ${engagementSummary.attackPathCount}
Detection Coverage: ${engagementSummary.detectionCoverage}%
Top 3 Critical Risks: ${engagementSummary.topRisks.slice(0, 3).join(", ")}

Write a professional executive summary with: business impact, top risks (non-technical language), key metrics, and urgency level. Do not invent CVE IDs or technical details not provided above.`;

    return callAnthropicWithRetry([{ role: "user", content: prompt }], apiKey);
  },

  async generateTechnicalFinding(finding: FindingInput, asset: AssetInput, exploitEvidence: string, apiKey?: string): Promise<string> {
    if (!apiKey) return SIMULATED.technical_finding(finding.title);

    const prompt = `Write a detailed technical finding for a VAPT report:

Finding ID: ${finding.id}
Title: ${finding.title}
Severity: ${finding.severity}
CVSS: ${finding.cvss}
${finding.cveId ? `CVE: ${finding.cveId}` : ""}
Affected Host: ${finding.affectedHost} (${asset.label}, ${asset.zone} zone)
Asset Criticality: ${asset.criticality}
Exploit Validated: ${finding.exploitValidated}
MITRE Technique: ${finding.mitreTechnique ?? "N/A"}
Description: ${finding.description ?? ""}
Evidence: ${exploitEvidence}

Write: Technical description, step-by-step reproduction, evidence, business impact, MITRE reference. Only use the CVE ID and CVSS score provided above — do not invent others.`;

    return callAnthropicWithRetry([{ role: "user", content: prompt }], apiKey);
  },

  async generateRemediationSteps(finding: FindingInput, apiKey?: string): Promise<string> {
    if (!apiKey) return SIMULATED.remediation(finding.title);

    const prompt = `Generate numbered step-by-step remediation guide with commands for:

Finding: ${finding.title} (${finding.severity})
${finding.cveId ? `CVE: ${finding.cveId}` : ""}
CVSS: ${finding.cvss}
${finding.description ? `Context: ${finding.description}` : ""}

Rules: include specific CLI commands where applicable, include a verification step, order by priority (immediate → short-term → long-term), never include destructive commands (rm -rf, DROP TABLE, etc.).`;

    return callAnthropicWithRetry([{ role: "user", content: prompt }], apiKey);
  },

  async generateSigmaExplanation(sigmaYaml: string, technique: string, apiKey?: string): Promise<string> {
    if (!apiKey) return SIMULATED.sigma_explanation(technique);

    const prompt = `Explain the following Sigma detection rule in plain language for a SOC analyst who will deploy it:

Technique: ${technique}

Sigma Rule:
${sigmaYaml}

Explain: what event this rule detects, why this pattern indicates malicious activity, what log source it requires, tuning guidance for reducing false positives, and what an analyst should do when it fires.`;

    return callAnthropicWithRetry([{ role: "user", content: prompt }], apiKey);
  },
};

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
import {
  REPORT_SYSTEM_PROMPT,
  buildScorecard,
  buildReportUserMessage,
  validateReport,
  normaliseSeverity,
  type ScoreDomain,
  type ScorecardInput,
  type Confidence,
  type ReportResult,
  type ReportFinding,
  type FindingWriteupOut,
  type AttackNarrativeOut,
  type RemediationGroupingOut,
  type ControlsObservedOut,
  type LimitationsOut,
  type VerdictSummaryOut,
} from './prompts/report';
import { SECTION_PROMPTS, buildSectionInput, type SectionKey } from './prompts/report-sections';

export interface ReportSession {
  clientName:     string;
  scope:          string[];
  findings:       LiveFinding[];
  exploitResults: unknown[];
  engagementType: string;
  /** Overall score from the previous assessment, so the executive summary can
   *  describe the delta the prompt asks for. Omit for a first engagement. */
  previousOverall?: number | null;
}

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

// ── LiveFinding → report-contract adapters ─────────────────────────────────
// The scorecard is computed, not generated (see buildScorecard), but LiveFinding
// carries no explicit domain/EPSS/KEV. Map those here with a transparent
// heuristic (source + service + port) rather than an LLM guess — the whole point
// of the deterministic scorecard is a number no one had to invent.

const numOrNull = (v: string | undefined): number | null => {
  if (v == null || v === '') return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
};

function classifyDomain(f: LiveFinding): ScoreDomain {
  const src  = f.source;
  const svc  = `${f.service ?? ''} ${f.protocol ?? ''}`.toLowerCase();
  const port = f.port ?? 0;
  if (src === 'nuclei' || src === 'httpx' || src === 'whatweb' || src === 'ffuf'
      || /https?|www|web/.test(svc) || [80, 443, 8080, 8443, 8000, 8888].includes(port)) {
    return 'web_application';
  }
  if (['ssh-audit', 'smb-enum', 'ldap-enum', 'netbios-enum', 'rdp-fingerprint', 'rpc-enum'].includes(src)
      || /ssh|ldap|kerberos|smb|rdp|telnet|ftp|netbios|winrm|rpc|nfs/.test(svc)) {
    return 'authentication';
  }
  if (src === 'testssl' || /tls|ssl|snmp|cert/.test(svc)) return 'configuration';
  if ((f.cveIds?.length ?? 0) > 0 || src === 'openvas') return 'patch_management';
  return 'network';
}

// buildScorecard treats "open" | "confirmed" as live exposure; anything else
// drops out of the score.
function mapStatus(s: LiveFinding['status']): string {
  if (s === 'VERIFIED') return 'confirmed';
  if (s === 'CLOSED') return 'closed';
  return 'open'; // OPEN, IN_REVIEW, IN_REMEDIATION are still open exposure
}

function deriveConfidence(f: LiveFinding): Confidence {
  if (f.status === 'VERIFIED') return 'confirmed';
  if (f.kev || (f.cveIds?.length ?? 0) > 0 || f.cvss) return 'likely';
  return 'potential';
}

function toScorecardInput(session: ReportSession): ScorecardInput {
  return {
    previousOverall: session.previousOverall ?? null,
    findings: session.findings
      .filter((f) => !f.falsePositive)
      .map((f) => ({
        severity: normaliseSeverity(f.severity),
        cvss: numOrNull(f.cvss),
        epss: f.epss ?? null,       // absent, not zero — buildScorecard treats null as no-signal
        kev: Boolean(f.kev),        // CISA KEV membership doubles the weight
        exploitValidated: f.status === 'VERIFIED',
        status: mapStatus(f.status),
        domain: classifyDomain(f),
      })),
  };
}

// The findings handed to the model: grounded, structured, and carrying the
// confidence value the prompt is told to match (rule 5). This is the untrusted
// payload buildReportUserMessage fences.
function toModelFindings(session: ReportSession) {
  return session.findings
    .filter((f) => !f.falsePositive)
    .map((f) => ({
      finding_id: f.id,
      title: f.title,
      severity: normaliseSeverity(f.severity),
      confidence: deriveConfidence(f),
      validation_method: f.status === 'VERIFIED'
        ? 'Safely validated during testing'
        : `Observed via ${f.source}`,
      affected_assets: [f.port ? `${f.host}:${f.port}` : f.host],
      service: f.service ?? null,
      version: f.serviceVersion ?? null,
      protocol: f.protocol ?? null,
      cvss: numOrNull(f.cvss),
      cvss_vector: f.cvssVector ?? null,
      epss: f.epss ?? null,
      kev: Boolean(f.kev),
      cve_ids: f.cveIds ?? [],
      mitre: f.mitre ?? [],
      compliance: f.compliance ?? [],
      evidence: f.evidence ?? [],
      attack_path: f.attackPath ?? null,
      remediation_hint: f.remediation ?? null,
      status: mapStatus(f.status),
    }));
}

// ── Section orchestration (decomposed prompts, report-sections.ts) ──────────
// The report is generated section by section rather than in one call, because a
// single prompt asked for a verdict + N finding write-ups budgets its tokens
// against the section a board actually reads. Per-finding write-ups are bounded
// (top-N by severity; the rest are tabulated), and later sections consume the
// output of earlier ones (GENERATION_ORDER).

const REPORT_MODEL = 'claude-sonnet-4-6';
const MAX_FULL_WRITEUPS = 8; // full records for the worst N; the rest tabulate
const SEV_RANK_LOCAL: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3, info: 4 };

type ModelFinding = ReturnType<typeof toModelFindings>[number];
type RankedFinding = ModelFinding & { ref: string };

/** One section call: fenced input + the section's own system prompt and token
 *  cap. Fail-soft — a section that errors or returns unparseable JSON yields the
 *  fallback, so one bad section never fails the whole report. */
async function runSection<T>(
  client: Anthropic, key: SectionKey, payload: unknown, fallback: T,
): Promise<T> {
  try {
    const { prompt, maxTokens } = SECTION_PROMPTS[key];
    const msg = await client.messages.create({
      model: REPORT_MODEL,
      max_tokens: maxTokens,
      system: prompt,
      messages: [{ role: 'user', content: buildSectionInput(payload) }],
    });
    const text = (msg.content[0] as { text: string }).text;
    return JSON.parse(stripFences(text)) as T;
  } catch (err) {
    console.warn(`[ai-engine] report section "${key}" failed, using fallback:`, err);
    return fallback;
  }
}

function mapFindingForWriteup(f: RankedFinding, frameworks: string[]) {
  return {
    id: f.finding_id, ref: f.ref, title: f.title, severity: f.severity,
    confidence: f.confidence, validation_method: f.validation_method,
    cvss_score: f.cvss, cvss_vector: f.cvss_vector, epss_score: null,
    kev: null, exploit_validated: f.status === 'confirmed', internet_reachable: null,
    cve_ids: f.cve_ids, affected_assets: f.affected_assets, description: null,
    evidence_snippet: f.evidence?.[0]?.content ?? null, first_seen: null,
    existing_remediation: f.remediation_hint, compliance_candidates: frameworks,
  };
}

function fallbackWriteup(f: RankedFinding): FindingWriteupOut {
  const asset = f.affected_assets.join(', ') || 'the assessed host';
  return {
    ref: f.ref, title: f.title,
    business_impact: `Affects ${asset}. Automated write-up was unavailable; review the evidence and confirm the impact before delivery.`,
    technical_detail: 'Automated technical write-up was unavailable for this finding. See the captured evidence.',
    evidence_summary: f.evidence?.[0]?.content
      ? String(f.evidence[0].content).slice(0, 400)
      : 'No evidence snippet was captured for this finding.',
    severity_rationale: `Severity ${f.severity} as classified during the scan.`,
    severity_flag: null,
    remediation_detail: f.remediation_hint ?? 'Remediation guidance not available; consult the relevant vendor advisory.',
    verification: 'Re-run the scan against the affected assets and confirm the condition is no longer reported.',
    compliance_refs: [],
  };
}

function assembleFinding(f: RankedFinding, w: FindingWriteupOut): ReportFinding {
  return {
    finding_id: f.finding_id, ref: f.ref, title: w.title || f.title,
    severity: normaliseSeverity(f.severity), confidence: f.confidence,
    validation_method: f.validation_method, affected_assets: f.affected_assets,
    business_impact: w.business_impact, technical_detail: w.technical_detail,
    evidence_summary: w.evidence_summary, remediation_detail: w.remediation_detail,
    verification: w.verification, compliance_refs: w.compliance_refs ?? [],
    severity_rationale: w.severity_rationale, severity_flag: w.severity_flag ?? null,
    first_seen: null, references: f.cve_ids ?? [],
    cvss: f.cvss, cvss_vector: f.cvss_vector, epss: f.epss, kev: f.kev,
    exploit_validated: f.status === 'confirmed', internet_reachable: null,
  };
}

// Tabulated finding — carries the citable facts without a generated write-up.
function compactFinding(f: RankedFinding): ReportFinding {
  return {
    finding_id: f.finding_id, ref: f.ref, title: f.title,
    severity: normaliseSeverity(f.severity), confidence: f.confidence,
    validation_method: f.validation_method, affected_assets: f.affected_assets,
    business_impact: '', technical_detail: '', evidence_summary: '',
    remediation_detail: f.remediation_hint ?? '', verification: '',
    compliance_refs: [], references: f.cve_ids ?? [],
    cvss: f.cvss, cvss_vector: f.cvss_vector, epss: f.epss, kev: f.kev,
    exploit_validated: f.status === 'confirmed', internet_reachable: null,
  };
}

function groupingInput(rf: ReportFinding) {
  return {
    ref: rf.ref, title: rf.title, severity: rf.severity, confidence: rf.confidence,
    remediation_detail: rf.remediation_detail, affected_assets: rf.affected_assets,
    verification: rf.verification,
  };
}

function countSeverities(findings: ReportFinding[]) {
  const c: Record<string, number> = { critical: 0, high: 0, medium: 0, low: 0 };
  for (const f of findings) if (f.severity in c) c[f.severity]++;
  return c;
}

/** Section-by-section orchestrator — the primary path. */
async function generateReportSectioned(session: ReportSession): Promise<ReportResult> {
  const client = getClient();

  // Deterministic scorecard — computed, never generated.
  const scorecard = buildScorecard(toScorecardInput(session));
  const frameworks = Array.from(
    new Set(session.findings.flatMap((f) => (f.compliance ?? []).map((c) => c.framework))),
  );

  // Rank worst-first, assign stable F-01… refs, split into full write-ups vs. tail.
  const ranked: RankedFinding[] = [...toModelFindings(session)]
    .sort((a, b) => (SEV_RANK_LOCAL[a.severity] ?? 4) - (SEV_RANK_LOCAL[b.severity] ?? 4))
    .map((f, i) => ({ ...f, ref: `F-${String(i + 1).padStart(2, '0')}` }));
  const top = ranked.slice(0, MAX_FULL_WRITEUPS);
  const tail = ranked.slice(MAX_FULL_WRITEUPS);

  // 1. Finding write-ups — bounded and parallel (independent of each other).
  const writeups = await Promise.all(
    top.map((f) => runSection<FindingWriteupOut>(
      client, 'finding_writeup',
      { finding: mapFindingForWriteup(f, frameworks), asset_context: {}, frameworks },
      fallbackWriteup(f),
    )),
  );
  const findings: ReportFinding[] = [
    ...top.map((f, i) => assembleFinding(f, writeups[i])),
    ...tail.map(compactFinding),
  ];

  // 2. Attack narrative — no chain model available yet, so chains are empty and
  //    the prompt returns null rather than inventing one.
  const narrative = await runSection<AttackNarrativeOut>(
    client, 'attack_narrative',
    { chains: [], findings: top.map((f) => ({ ref: f.ref, title: f.title })) },
    { narrative: null, cheapest_break: null, preconditions: [], confidence_caveat: null },
  );

  // 3. Remediation grouping — consumes the finding refs + their remediation detail.
  const grouping = await runSection<RemediationGroupingOut>(
    client, 'remediation_grouping',
    { findings: findings.map(groupingInput), scorecard, constraints: {} },
    { groups: [], immediate_window_empty_reason: null },
  );

  // 4. Controls + limitations — independent, run in parallel.
  const lowConfidence = findings.filter((f) => f.confidence !== 'confirmed').length;
  const [controls, limits] = await Promise.all([
    runSection<ControlsObservedOut>(
      client, 'controls_observed',
      { controls_evidence: [], detection_results: {}, segmentation_tests: [], negative_findings: [] },
      { items: [{ control: 'No controls were specifically evidenced as effective within the tested scope.', test: '', result: '', evidence_ref: null }] },
    ),
    runSection<LimitationsOut>(
      client, 'limitations',
      { engagement: { window: 'Not specified', authorisation_ref: 'Not specified', methodologies: [], asset_count: session.findings.length },
        in_scope: session.scope, out_of_scope: [], exclusions: [], coverage: {}, low_confidence_count: lowConfidence },
      { method: '', limitations: [] },
    ),
  ]);

  // 5. Verdict + summary LAST — its decisions derive from the grouped plan (§4)
  //    and the narrative (§3), which is why it cannot run first.
  const vs = await runSection<VerdictSummaryOut>(
    client, 'verdict_and_summary',
    { engagement: { name: session.clientName, window: 'Not specified', scope_summary: session.scope.join(', '), asset_count: session.findings.length, locale: 'en' },
      scorecard, severity_counts: countSeverities(findings),
      remediation_plan: grouping.groups, top_chain: narrative.narrative, closed_since_last: 0 },
    { verdict: '', summary: '', decisions: [] },
  );

  const report: ReportResult = {
    verdict: vs.verdict,
    executive_summary: vs.summary,
    decisions: vs.decisions ?? [],
    attack_narrative: narrative.narrative,
    cheapest_break: narrative.cheapest_break,
    preconditions: narrative.preconditions ?? [],
    findings,
    findings_detailed: top.length,
    remediation_plan: grouping.groups ?? [],
    immediate_window_empty_reason: grouping.immediate_window_empty_reason ?? null,
    controls: controls.items ?? [],
    controls_observed: (controls.items ?? []).map((i) => [i.control, i.test, i.result].filter(Boolean).join(' — ')),
    limitations: limits.limitations ?? [],
    method: limits.method ?? '',
    scorecard,
  };

  const check = validateReport(report, { findingIds: session.findings.map((f) => f.id), frameworks });
  if (!check.valid) console.warn('[ai-engine] generateReport: structural validation issues:', check.issues);
  return report;
}

/** Single-call fallback (the original monolithic path) — used only if the
 *  sectioned orchestrator throws catastrophically. Keeps report generation
 *  resilient and the REPORT_SYSTEM_PROMPT contract exercised. */
async function generateReportSingleCall(session: ReportSession): Promise<ReportResult> {
  const client = getClient();
  const scorecard = buildScorecard(toScorecardInput(session));
  const complianceFrameworks = Array.from(
    new Set(session.findings.flatMap((f) => (f.compliance ?? []).map((c) => c.framework))),
  );
  const userMessage = buildReportUserMessage({
    engagement: { name: session.clientName, scope: session.scope, window: 'Not specified', authorisation_ref: 'Not specified' },
    scorecard, findings: toModelFindings(session),
    attackChains: [], controlsEvidence: [], complianceFrameworks, outOfScope: [],
  });
  const msg = await client.messages.create({
    model: REPORT_MODEL, max_tokens: 16000, system: REPORT_SYSTEM_PROMPT,
    messages: [{ role: 'user', content: userMessage }],
  });
  const text = (msg.content[0] as { text: string }).text;
  const report = JSON.parse(stripFences(text)) as ReportResult;
  report.findings = (report.findings ?? []).map((f) => ({ ...f, severity: normaliseSeverity(f.severity) }));
  report.remediation_plan = report.remediation_plan ?? [];
  report.scorecard = scorecard;
  return report;
}

export async function generateReport(session: ReportSession): Promise<ReportResult> {
  try {
    return await generateReportSectioned(session);
  } catch (err) {
    console.warn('[ai-engine] sectioned report generation failed, falling back to single call:', err);
    try {
      return await generateReportSingleCall(session);
    } catch (err2) {
      throw new Error(`Report generation failed: ${err2 instanceof Error ? err2.message : String(err2)}`);
    }
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
