/**
 * finding-model.ts — the assessment layer between a scanner record and a
 * client-deliverable finding.
 *
 * Everything exported here is DERIVED from recorded scanner facts. Nothing is
 * inferred, softened or invented. Where a fact is absent the model says so
 * (`null`, or a `Gap`) so the UI can print "Not recorded" instead of guessing —
 * a report that quietly fills its own holes is worse than one with holes in it.
 *
 * Three ideas drive the whole file:
 *
 *   1. Severity ≠ priority. CVSS rates how bad a flaw is in the abstract; it
 *      says nothing about whether anyone is actually exploiting it or whether
 *      the host is even reachable. FIRST says this explicitly. So we publish
 *      both: CVSS as recorded, and a priority we compute and can justify.
 *
 *   2. Detection method decides confidence. "The banner said 2.4.49" and "we
 *      executed code" are not the same claim, and a client who reboots
 *      production over the first one will not trust the second one next time.
 *
 *   3. Evidence is a custody artifact. It needs a tool, a time, an operator and
 *      a hash — and it must not carry the client's own secrets into a PDF that
 *      gets emailed around.
 */

import { SEVERITY, SEVERITY_ORDER, toSeverity, type Severity } from "../severity";

/* ═══════════════════════════════════════════════════════════════════════════
 * 1. Input shape — a superset of what the findings API returns today.
 *    Every enrichment field is optional, so this drops in against the current
 *    payload and lights up progressively as the scanner records more.
 * ═══════════════════════════════════════════════════════════════════════════ */

export interface RawEvidence {
  label: string;
  content: string;
  type?: string;
  /* — provenance (chain of custody) — */
  tool?: string;
  command?: string;
  capturedAt?: string;
  capturedBy?: string;
  sourceHost?: string;
  sha256?: string;
}

export interface RawAsset {
  host: string;
  ip?: string;
  port?: number;
  service?: string;
  version?: string;
  environment?: string;
  owner?: string;
  internetReachable?: boolean;
}

export type RemediationTier = "containment" | "fix" | "hardening";

export interface RawRemediation {
  tier?: RemediationTier;
  action?: string;
  title?: string;
  description?: string;
  step?: string;
  owner?: string;
  effort?: "low" | "medium" | "high";
  downtime?: string;
  rollback?: string;
}

export interface RawVerification {
  method?: string;
  command?: string;
  expected?: string;
  retain?: string;
}

export interface RawFinding {
  id: string;
  title: string;
  severity: string;
  status: string;
  affectedHost: string;
  discoveredAt: string;
  description: string;
  technicalDetails: string;
  evidence: RawEvidence[];
  impact: string;
  remediation: Array<string | RawRemediation>;
  mitre: Array<{ id: string; name: string }>;
  cwe?: Array<{ id: string; name: string }>;
  cve?: string[];
  riskScore: number;
  cvss: string;
  cvssVector?: string;
  activelyExploited: boolean;
  detectionCoverage: string;
  reproductionSteps?: string;

  /* — enrichment, all optional — */
  assets?: RawAsset[];
  epss?: number;
  epssPercentile?: number;
  kevAddedAt?: string;
  exploitValidated?: boolean;
  exploitPublic?: boolean;
  internetReachable?: boolean;
  detectionMethod?: DetectionMethod;
  severityRationale?: string;
  severityAdjustedFrom?: string;
  rootCause?: string;
  prerequisites?: string[];
  attackPath?: string[];
  verification?: RawVerification;
  compliance?: string[];
  advisories?: Array<{ label: string; url: string }>;
  assignedTo?: string;
  dueAt?: string;
  retestedAt?: string;
}

/* ═══════════════════════════════════════════════════════════════════════════
 * 2. Confidence — how the finding was established.
 *    This is the single most abused field in automated reporting. A version
 *    banner is an indicator, not proof: distros backport security patches
 *    without bumping the advertised version, so "Apache 2.4.49" on a patched
 *    RHEL box is a false positive waiting to burn your credibility.
 * ═══════════════════════════════════════════════════════════════════════════ */

export type DetectionMethod =
  | "exploit"
  | "behavioural"
  | "configuration"
  | "credentialed"
  | "version"
  | "banner"
  | "inference";

export type ConfidenceLevel = "CONFIRMED" | "LIKELY" | "POTENTIAL";

export interface Confidence {
  level: ConfidenceLevel;
  label: string;
  /** What the assessor actually did. Goes in the report verbatim. */
  basis: string;
  /** The honest limitation of that method, or null when there isn't one. */
  caveat: string | null;
}

const DETECTION: Record<DetectionMethod, Confidence> = {
  exploit: {
    level: "CONFIRMED",
    label: "Confirmed",
    basis: "Exploited in a controlled test; the described outcome was observed directly.",
    caveat: null,
  },
  behavioural: {
    level: "CONFIRMED",
    label: "Confirmed",
    basis: "The service responded in a way only a vulnerable build produces. No exploit code was run.",
    caveat: null,
  },
  configuration: {
    level: "CONFIRMED",
    label: "Confirmed",
    basis: "Read from the live configuration on the host.",
    caveat: null,
  },
  credentialed: {
    level: "CONFIRMED",
    label: "Confirmed",
    basis: "Authenticated inspection of the installed package and patch level.",
    caveat: null,
  },
  version: {
    level: "LIKELY",
    label: "Likely",
    basis: "Matched an advertised version against the vendor's affected range.",
    caveat:
      "Distributions backport fixes without changing the version string. Confirm the build or package release before scheduling downtime.",
  },
  banner: {
    level: "POTENTIAL",
    label: "Potential",
    basis: "Inferred from a service banner alone; no version or behaviour was confirmed.",
    caveat:
      "Banners are trivially altered and frequently stale. Treat as a lead to verify, not as a confirmed exposure.",
  },
  inference: {
    level: "POTENTIAL",
    label: "Potential",
    basis: "Derived from adjacent evidence rather than tested directly.",
    caveat: "Not independently verified. Confirm before reporting to a third party.",
  },
};

export function confidenceOf(f: RawFinding): Confidence {
  if (f.exploitValidated) return DETECTION.exploit;
  const m = f.detectionMethod;
  if (m && DETECTION[m]) return DETECTION[m];
  // No method recorded — refuse to imply proof we don't have.
  return {
    level: "POTENTIAL",
    label: "Unverified",
    basis: "Detection method not recorded.",
    caveat:
      "The scanner did not record how this was established. Confirm the method and re-rate before delivery.",
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
 * 3. CVSS vector → attacker capability.
 *    A vector string is precise and unreadable. The same string, expanded,
 *    answers the only two questions a reader has: what does the attacker need,
 *    and what do they walk away with. Supports 3.x and 4.0.
 * ═══════════════════════════════════════════════════════════════════════════ */

export interface VectorMetric {
  key: string;
  value: string;
  name: string;
  reading: string;
  /** Metrics that make exploitation easier — worth surfacing in colour. */
  aggravating: boolean;
}

export interface VectorReading {
  version: "3.x" | "4.0" | "unknown";
  metrics: VectorMetric[];
  /** "What the attacker needs" — ordered, plain English. */
  prerequisites: string[];
  /** "What the attacker gets" — ordered, plain English. */
  outcomes: string[];
  reach: "network" | "adjacent" | "local" | "physical" | null;
  needsCredentials: boolean | null;
  needsUserAction: boolean | null;
}

const METRIC_NAME: Record<string, string> = {
  AV: "Attack vector", AC: "Attack complexity", AT: "Attack requirements",
  PR: "Privileges required", UI: "User interaction", S: "Scope",
  C: "Confidentiality", I: "Integrity", A: "Availability",
  VC: "Confidentiality", VI: "Integrity", VA: "Availability",
  SC: "Downstream confidentiality", SI: "Downstream integrity", SA: "Downstream availability",
};

const METRIC_VALUE: Record<string, Record<string, string>> = {
  AV: { N: "Network", A: "Adjacent network", L: "Local", P: "Physical" },
  AC: { L: "Low", H: "High" },
  AT: { N: "None", P: "Present" },
  PR: { N: "None", L: "Low", H: "High" },
  UI: { N: "None", R: "Required", P: "Passive", A: "Active" },
  S:  { U: "Unchanged", C: "Changed" },
  C: { H: "High", L: "Low", N: "None" }, I: { H: "High", L: "Low", N: "None" },
  A: { H: "High", L: "Low", N: "None" },
  VC: { H: "High", L: "Low", N: "None" }, VI: { H: "High", L: "Low", N: "None" },
  VA: { H: "High", L: "Low", N: "None" },
  SC: { H: "High", L: "Low", N: "None" }, SI: { H: "High", L: "Low", N: "None" },
  SA: { H: "High", L: "Low", N: "None" },
};

/** Metric values that widen the window for an attacker. */
const AGGRAVATING = new Set(["AV:N", "AC:L", "AT:N", "PR:N", "UI:N", "S:C", "C:H", "I:H", "A:H", "VC:H", "VI:H", "VA:H"]);

const PREREQ: Record<string, string> = {
  "AV:N": "Network reachability to the service — no foothold needed",
  "AV:A": "A position on the same network segment",
  "AV:L": "Local access to the host, e.g. a shell or a logged-in session",
  "AV:P": "Physical access to the device",
  "PR:N": "No credentials",
  "PR:L": "Any ordinary user account",
  "PR:H": "An administrative account",
  "UI:R": "A user to open or click something",
  "UI:P": "A user to be doing something ordinary at the time — no targeting needed",
  "UI:A": "A user to be talked into performing the action",
  "AC:H": "Conditions outside the attacker's control, such as a race or a leaked value",
  "AT:P": "A specific deployment condition to be met",
};

const OUTCOME: Record<string, string> = {
  "C:H": "Full read of the data the service holds",
  "C:L": "Partial read of the data the service holds",
  "I:H": "Ability to modify or destroy data",
  "I:L": "Limited ability to modify data",
  "A:H": "Ability to take the service offline",
  "A:L": "Degraded service availability",
  "S:C": "Impact beyond this component — the blast radius crosses a trust boundary",
};

export function readVector(vector?: string | null): VectorReading | null {
  if (!vector || !/^CVSS:/i.test(vector)) return null;
  const parts = vector.split("/").filter(Boolean);
  const head = parts.shift() ?? "";
  const version = /4\.0/.test(head) ? "4.0" : /3\.[01]/.test(head) ? "3.x" : "unknown";

  const map = new Map<string, string>();
  const metrics: VectorMetric[] = [];
  for (const p of parts) {
    const [k, v] = p.split(":");
    if (!k || !v) continue;
    map.set(k, v);
    const name = METRIC_NAME[k];
    if (!name) continue; // temporal/environmental extras — kept out of the plain-English pass
    metrics.push({
      key: k, value: v, name,
      reading: METRIC_VALUE[k]?.[v] ?? v,
      aggravating: AGGRAVATING.has(`${k}:${v}`),
    });
  }
  if (!metrics.length) return null;

  const get = (k: string) => (map.has(k) ? `${k}:${map.get(k)}` : null);
  const pick = (keys: string[], table: Record<string, string>) =>
    keys.map(get).filter(Boolean).map(t => table[t as string]).filter(Boolean) as string[];

  // 4.0 renames C/I/A to VC/VI/VA. Normalise so one lookup table serves both.
  for (const [from, to] of [["VC", "C"], ["VI", "I"], ["VA", "A"]] as const) {
    if (map.has(from) && !map.has(to)) map.set(to, map.get(from)!);
  }

  const av = map.get("AV") ?? null;
  const pr = map.get("PR") ?? null;
  const ui = map.get("UI") ?? null;

  return {
    version,
    metrics,
    prerequisites: pick(["AV", "PR", "UI", "AC", "AT"], PREREQ),
    outcomes: pick(["C", "I", "A", "S"], OUTCOME),
    reach: av === "N" ? "network" : av === "A" ? "adjacent" : av === "L" ? "local" : av === "P" ? "physical" : null,
    needsCredentials: pr === null ? null : pr !== "N",
    needsUserAction: ui === null ? null : ui !== "N",
  };
}

/** One sentence a non-technical reader can carry into a meeting. */
export function attackerStatement(f: RawFinding, v: VectorReading | null, assetCount: number): string | null {
  if (!v || !v.outcomes.length) return null;
  const who = v.needsCredentials === false ? "An unauthenticated attacker" : "An attacker with a valid account";
  const where =
    v.reach === "network" ? (f.internetReachable ? "reaching this service from the internet" : "reaching this service over the network")
    : v.reach === "adjacent" ? "on the same network segment"
    : v.reach === "local" ? "already on the host"
    : v.reach === "physical" ? "with physical access to the device"
    : "with access to this service";

  // S:C describes blast radius, not an attacker action — it gets its own sentence.
  const crossesBoundary = v.outcomes.some(o => o.startsWith("Impact beyond"));
  const gets = v.outcomes
    .filter(o => !o.startsWith("Impact beyond"))
    .map(o => o.replace(/^Ability to /, "").replace(/^Full read of/, "read all of").replace(/^Partial read of/, "read part of"));
  if (!gets.length) return null;

  const scope = assetCount > 1 ? ` This applies to ${assetCount} hosts in scope.` : "";
  const boundary = crossesBoundary ? " The impact does not stop at this component — it crosses a trust boundary." : "";
  return `${who} ${where} can ${joinList(gets).toLowerCase()}.${boundary}${scope}`;
}

function joinList(items: string[]): string {
  if (items.length <= 1) return items[0] ?? "";
  return `${items.slice(0, -1).join(", ")} and ${items[items.length - 1]}`;
}

/* ═══════════════════════════════════════════════════════════════════════════
 * 4. Priority — the fix-first question, answered and shown its working.
 *    Severity says how bad. Priority folds in whether it is being exploited,
 *    whether we proved it, and whether an attacker can even reach it.
 * ═══════════════════════════════════════════════════════════════════════════ */

export type PriorityCode = "P0" | "P1" | "P2" | "P3" | "P4";

export interface Priority {
  code: PriorityCode;
  label: string;
  /** Every clause that pushed this up. Shown to the reader — no black boxes. */
  drivers: string[];
  /** Facts that would normally raise it but are absent. */
  dampeners: string[];
}

const PRIORITY_LABEL: Record<PriorityCode, string> = {
  P0: "Fix now", P1: "Fix this week", P2: "Fix this month",
  P3: "Scheduled", P4: "Track only",
};

export function priorityOf(f: RawFinding): Priority {
  const sev = toSeverity(f.severity);
  const rank = SEVERITY[sev].rank; // 0 = critical
  const v = readVector(f.cvssVector);

  const kev = Boolean(f.activelyExploited);
  const validated = Boolean(f.exploitValidated);
  const epssHigh = (f.epss ?? 0) >= 0.5;
  const exposed = f.internetReachable ?? (f.assets?.some(a => a.internetReachable) ?? false);
  const noAuth = v?.needsCredentials === false;

  const drivers: string[] = [];
  if (kev) drivers.push("Listed on the CISA Known Exploited Vulnerabilities catalog");
  if (validated) drivers.push("Exploitation reproduced during this assessment");
  if (epssHigh) drivers.push(`EPSS ${(f.epss ?? 0).toFixed(2)} — high probability of exploitation in the next 30 days`);
  if (exposed) drivers.push("Reachable from the internet");
  if (noAuth) drivers.push("No authentication required");
  if (f.exploitPublic && !validated && !kev) drivers.push("Public exploit code exists");

  const dampeners: string[] = [];
  if (!kev && !validated && !epssHigh) dampeners.push("No exploitation signal recorded");
  if (!exposed && f.internetReachable === false) dampeners.push("Not reachable from the internet");
  if (v?.needsCredentials) dampeners.push("Requires valid credentials");
  if (v?.needsUserAction) dampeners.push("Requires a user to act");

  const weaponised = kev || validated;
  let code: PriorityCode;
  if (rank <= 1 && weaponised && (exposed || noAuth)) code = "P0";
  else if (rank === 0 || (rank === 1 && (weaponised || epssHigh))) code = "P1";
  else if (rank === 1 || (rank === 2 && (weaponised || epssHigh))) code = "P2";
  else if (rank === 2) code = "P3";
  else code = "P4";

  // Floor for anything with a live exploitation signal. A low-severity flaw that
  // is being exploited in the wild still has to be scheduled — CISA BOD 22-01
  // requires KEV entries to be remediated regardless of CVSS, and "track only"
  // is the wrong answer to "someone is using this today".
  if (weaponised && code > "P2") {
    code = "P2";
    drivers.push(`Raised to P2: a ${SEVERITY[sev].label.toLowerCase()}-severity issue with a live exploitation signal is still scheduled work`);
  }

  return { code, label: PRIORITY_LABEL[code], drivers, dampeners };
}

/* ═══════════════════════════════════════════════════════════════════════════
 * 5. Remediation clock. Default policy, stated as policy — not dressed up as
 *    a regulatory requirement it isn't.
 * ═══════════════════════════════════════════════════════════════════════════ */

export const SLA_DAYS: Record<PriorityCode, number | null> = {
  P0: 3, P1: 7, P2: 30, P3: 90, P4: null,
};

export type SlaState = "breached" | "due-soon" | "on-track" | "no-target" | "closed";

export interface Sla {
  state: SlaState;
  dueAt: Date | null;
  daysRemaining: number | null;
  note: string;
}

export function slaOf(f: RawFinding, priority: PriorityCode, now = new Date()): Sla {
  const closed = /remediated|accepted|false_positive|\bfp\b|closed/i.test(f.status);
  if (closed) return { state: "closed", dueAt: null, daysRemaining: null, note: "Closed — no target date applies." };

  const explicit = f.dueAt ? new Date(f.dueAt) : null;
  const due: Date | null = explicit && !isNaN(explicit.getTime()) ? explicit : null;
  if (!due) {
    return {
      state: "no-target",
      dueAt: null,
      daysRemaining: null,
      note: "No authoritative remediation deadline was returned by the Manager SLA service.",
    };
  }

  // Round away from zero on both sides. ceil() alone turns "half a day late"
  // into -0, which is not < 0, so a breached finding would report as on track.
  const diff = (due.getTime() - now.getTime()) / 86_400_000;
  const remaining = diff < 0 ? Math.floor(diff) : Math.ceil(diff);
  const state: SlaState = remaining < 0 ? "breached" : remaining <= 2 ? "due-soon" : "on-track";
  const note =
    state === "breached" ? `Past the configured target by ${Math.abs(remaining)} day${Math.abs(remaining) === 1 ? "" : "s"}.`
    : state === "due-soon" ? `Due in ${remaining} day${remaining === 1 ? "" : "s"}.`
    : `${remaining} days remaining against the configured target.`;
  return { state, dueAt: due, daysRemaining: remaining, note };
}

/* ═══════════════════════════════════════════════════════════════════════════
 * 6. Evidence hygiene.
 *
 *    (a) Provenance: a screenshot with no tool, time or operator is an
 *        assertion, not evidence. Say when that's what we have.
 *    (b) Redaction: scanner output routinely contains the client's own keys,
 *        hashes and session tokens. A PDF gets forwarded; secrets in it become
 *        a second incident. Mask by default, reveal deliberately.
 * ═══════════════════════════════════════════════════════════════════════════ */

export interface Provenance {
  complete: boolean;
  fields: Array<{ label: string; value: string | null }>;
  /** Non-null when custody is incomplete — rendered as a visible warning. */
  gap: string | null;
}

export function provenanceOf(e: RawEvidence): Provenance {
  const fields = [
    { label: "Tool", value: e.tool ?? null },
    { label: "Source", value: e.sourceHost ?? null },
    { label: "Captured", value: e.capturedAt ?? null },
    { label: "Operator", value: e.capturedBy ?? null },
    { label: "SHA-256", value: e.sha256 ?? null },
  ];
  const missing = fields.filter(f => !f.value).map(f => f.label);
  return {
    complete: missing.length === 0,
    fields,
    gap: missing.length
      ? `Custody incomplete — ${missing.join(", ").toLowerCase()} not recorded. This artifact will not stand up to a challenge.`
      : null,
  };
}

interface RedactionRule {
  kind: string;
  re: RegExp;
  /** Receives (match, ...groups) exactly as String.replace does. */
  to: (...args: string[]) => string;
}

/* Order runs specific → general, so a broad key/value rule never re-redacts
   something a narrower rule already labelled.

   Three details worth keeping:

   • No \b on the key/value rule. `\bsecret` cannot match inside
     `aws_secret_access_key`, because `_` is a word character and there is no
     boundary between `_` and `s` — which is exactly how the most common cloud
     credential in scanner output survives naive redaction. The leading
     [A-Za-z0-9_.-]* consumes the prefix instead.
   • The separator tolerates a closing quote, so JSON bodies ("api_key":"…")
     are covered. API responses are most of what a web scanner captures.
   • The URL password is greedy to the last @ before the host, because real
     passwords contain @ and a lazy match leaks the tail. */
const RULES: RedactionRule[] = [
  { kind: "private key",
    re: /-----BEGIN[^-]*PRIVATE KEY-----[\s\S]*?-----END[^-]*PRIVATE KEY-----/g,
    to: () => "[REDACTED: private key]" },

  { kind: "credentials in a URL",
    re: /(:\/\/)[^\s/:@]+:[^\s/]+@/g,
    to: (_m, scheme) => `${scheme}[REDACTED: credentials]@` },

  { kind: "credential",
    re: /([A-Za-z0-9_.-]*(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|authorization|credential|token)[A-Za-z0-9_.-]*)(["']?\s*[:=]\s*)("[^"]*"|'[^']*'|(?:Bearer|Basic|Negotiate)\s+\S+|[^\s,;&)]+)/gi,
    to: (_m, key, sep) => `${key}${sep}[REDACTED: credential]` },

  { kind: "credential",
    re: /(<\s*[A-Za-z0-9_.:-]*(?:password|secret|token|apikey)[A-Za-z0-9_.:-]*\s*>)[^<]+/gi,
    to: (_m, tag) => `${tag}[REDACTED: credential]` },

  { kind: "auth header",
    re: /\b(Bearer|Basic|Negotiate)\s+[A-Za-z0-9+/=._~-]{8,}/gi,
    to: (_m, scheme) => `${scheme} [REDACTED: credential]` },

  { kind: "signed token",
    re: /\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{4,}/g,
    to: () => "[REDACTED: token]" },

  { kind: "AWS access key",
    re: /\b(?:AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b/g,
    to: () => "[REDACTED: AWS access key]" },

  { kind: "password hash",
    re: /\b[a-fA-F0-9]{32}:[a-fA-F0-9]{32}\b/g,
    to: () => "[REDACTED: password hash]" },
];

export interface Redaction { text: string; hits: Array<{ kind: string; count: number }>; total: number; }

export function redact(input: string): Redaction {
  let text = input;
  const hits: Array<{ kind: string; count: number }> = [];
  for (const rule of RULES) {
    let count = 0;
    text = text.replace(rule.re, (...args: unknown[]) => {
      count++;
      // replace() passes (match, ...groups, offset, subject). Filtering on
      // typeof === "string" would keep the whole subject as a trailing group;
      // cut at the offset instead, which is the first number in the list.
      const offset = args.findIndex(a => typeof a === "number");
      const groups = (offset === -1 ? args : args.slice(0, offset)) as string[];
      return rule.to(...groups);
    });
    if (!count) continue;
    const seen = hits.find(h => h.kind === rule.kind);
    if (seen) seen.count += count; else hits.push({ kind: rule.kind, count });
  }
  return { text, hits, total: hits.reduce((a, h) => a + h.count, 0) };
}

/* ═══════════════════════════════════════════════════════════════════════════
 * 7. Remediation, normalised into three tiers.
 *    "Patch it" is not a remediation plan when the patch lands in six weeks.
 *    Containment buys the time; the fix closes it; hardening stops the next one.
 * ═══════════════════════════════════════════════════════════════════════════ */

export interface RemediationStep {
  tier: RemediationTier;
  action: string;
  owner: string | null;
  effort: string | null;
  downtime: string | null;
  rollback: string | null;
}

export const TIER_META: Record<RemediationTier, { label: string; when: string }> = {
  containment: { label: "Contain", when: "Reduces exposure today, before the fix is ready" },
  fix:         { label: "Fix",     when: "Closes the vulnerability permanently" },
  hardening:   { label: "Harden",  when: "Prevents the same class of issue recurring" },
};

export function remediationSteps(f: RawFinding): RemediationStep[] {
  return f.remediation
    .map((r): RemediationStep | null => {
      if (typeof r === "string") {
        const action = r.trim();
        return action ? { tier: "fix", action, owner: null, effort: null, downtime: null, rollback: null } : null;
      }
      const action = (r.action ?? r.description ?? r.step ?? r.title ?? "").trim();
      if (!action) return null;
      return {
        tier: r.tier ?? "fix",
        action,
        owner: r.owner ?? null,
        effort: r.effort ?? null,
        downtime: r.downtime ?? null,
        rollback: r.rollback ?? null,
      };
    })
    .filter((s): s is RemediationStep => s !== null);
}

/* ═══════════════════════════════════════════════════════════════════════════
 * 8. Delivery readiness.
 *    A finding that cannot be reproduced, verified or evidenced should never
 *    reach a client. This tells the assessor exactly what is missing, per
 *    finding, before they hit Export.
 * ═══════════════════════════════════════════════════════════════════════════ */

export interface Gap { field: string; why: string; blocking: boolean; }

export function readinessOf(f: RawFinding): { gaps: Gap[]; blocking: number; ready: boolean } {
  const gaps: Gap[] = [];
  const add = (field: string, why: string, blocking = true) => gaps.push({ field, why, blocking });

  if (!f.description?.trim() && !f.technicalDetails?.trim()) add("Description", "Nothing describes what the issue is.");
  if (!f.evidence?.length) add("Evidence", "No artifact supports the claim.");
  if (!remediationSteps(f).length) add("Remediation", "No fix is given, so the client cannot act.");
  if (!f.verification?.expected?.trim()) add("Verification", "No pass criteria, so a retest cannot be judged.");
  if (!f.affectedHost?.trim() && !f.assets?.length) add("Affected assets", "No host is named.");

  if (!f.reproductionSteps?.trim()) add("Reproduction", "The client cannot independently confirm the issue.", false);
  if (!f.impact?.trim()) add("Business impact", "The reader is left to work out why it matters.", false);
  if (!f.cvssVector) add("CVSS vector", "The severity cannot be checked against its inputs.", false);
  if (!f.detectionMethod && !f.exploitValidated) add("Detection method", "Confidence in the finding cannot be stated.", false);
  if (f.evidence?.some(e => !provenanceOf(e).complete)) add("Evidence custody", "One or more artifacts lack tool, time, operator or hash.", false);

  const blocking = gaps.filter(g => g.blocking).length;
  return { gaps, blocking, ready: blocking === 0 };
}

/* ═══════════════════════════════════════════════════════════════════════════
 * 9. The assembled view model consumed by the UI.
 * ═══════════════════════════════════════════════════════════════════════════ */

export interface AssessedFinding {
  raw: RawFinding;
  severity: Severity;
  cvssScore: number | null;
  vector: VectorReading | null;
  confidence: Confidence;
  priority: Priority;
  sla: Sla;
  assets: RawAsset[];
  remediation: RemediationStep[];
  readiness: ReturnType<typeof readinessOf>;
  attackerStatement: string | null;
}

export function parseCvss(v?: string | null): number | null {
  const m = v?.match(/(\d+(?:\.\d+)?)/);
  if (!m) return null;
  const n = parseFloat(m[1]);
  return n >= 0 && n <= 10 ? n : null;
}

export function assess(f: RawFinding, now = new Date()): AssessedFinding {
  const vector = readVector(f.cvssVector);
  const priority = priorityOf(f);
  const assets: RawAsset[] =
    f.assets?.length ? f.assets : f.affectedHost ? [{ host: f.affectedHost, internetReachable: f.internetReachable }] : [];
  return {
    raw: f,
    severity: toSeverity(f.severity),
    cvssScore: parseCvss(f.cvss),
    vector,
    confidence: confidenceOf(f),
    priority,
    sla: slaOf(f, priority.code, now),
    assets,
    remediation: remediationSteps(f),
    readiness: readinessOf(f),
    attackerStatement: attackerStatement(f, vector, assets.length),
  };
}

/** Worst first, then by exploitation signal, then by CVSS. */
export function triageSort(a: AssessedFinding, b: AssessedFinding): number {
  const p = a.priority.code.localeCompare(b.priority.code);
  if (p !== 0) return p;
  const s = SEVERITY_ORDER.indexOf(a.severity) - SEVERITY_ORDER.indexOf(b.severity);
  if (s !== 0) return s;
  return (b.cvssScore ?? 0) - (a.cvssScore ?? 0);
}
