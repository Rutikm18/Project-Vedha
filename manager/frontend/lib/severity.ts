/**
 * severity.ts — single source of truth for security semantic colors.
 *
 * These values are tuned for the app's LIGHT theme: each is used both as text
 * and as a low-alpha fill (`${color}15`), so every color meets WCAG AA (≥4.5:1)
 * as text on white. This replaces the previous neon hex (#FF1744 / #FFD600 /
 * #00E676) — the yellow/green of which were unreadable (~1.4:1) on light.
 *
 * Palette: distinct hues (red / orange / amber / green / sky / slate / violet)
 * so severity is never conveyed by lightness alone (color-not-only).
 */

export type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";
export type FindingStatus =
  | "OPEN" | "IN_REVIEW" | "IN_REMEDIATION" | "VERIFIED"
  | "CLOSED" | "ACCEPTED" | "FALSE_POSITIVE";
export type ExploitMaturity = "WEAPONIZED" | "POC" | "THEORETICAL";
export type DetectionCoverage = "COVERED" | "PARTIAL" | "BLIND";

// Core ramp — AA-compliant on white.
const RED = "#DC2626";     // rose/red-600   ~4.8:1
const ORANGE = "#C2410C";  // orange-700     ~5.4:1
const AMBER = "#B45309";   // amber-700      ~5.6:1
const GREEN = "#15803D";   // green-700      ~4.9:1
const SKY = "#0369A1";     // sky-700        ~5.4:1
const SLATE = "#64748B";   // slate-500 (neutral / not-applicable)
const VIOLET = "#7C3AED";  // violet-600     ~5.0:1
const BLUE = "#2563EB";    // blue-600 (in-progress / data)

export const SEV_COLOR: Record<Severity, string> = {
  CRITICAL: RED, HIGH: ORANGE, MEDIUM: AMBER, LOW: GREEN, INFO: SKY,
};

export const STATUS_COLOR: Record<FindingStatus, string> = {
  OPEN: RED, IN_REVIEW: ORANGE, IN_REMEDIATION: BLUE,
  VERIFIED: GREEN, CLOSED: SLATE, ACCEPTED: VIOLET, FALSE_POSITIVE: SLATE,
};

export const STATUS_LABEL: Record<FindingStatus, string> = {
  OPEN: "OPEN", IN_REVIEW: "IN REVIEW", IN_REMEDIATION: "REMEDIATING",
  VERIFIED: "VERIFIED", CLOSED: "CLOSED", ACCEPTED: "ACCEPTED", FALSE_POSITIVE: "FALSE POS.",
};

export const MATURITY_COLOR: Record<ExploitMaturity, string> = {
  WEAPONIZED: RED, POC: ORANGE, THEORETICAL: SLATE,
};

export const COVERAGE_COLOR: Record<DetectionCoverage, string> = {
  COVERED: GREEN, PARTIAL: AMBER, BLIND: RED,
};

export const PRIORITY_COLOR: Record<string, string> = {
  P0: RED, P1: ORANGE, P2: AMBER, P3: SLATE,
};

export const KILL_CHAIN_PHASE_COLOR: Record<string, string> = {
  "Reconnaissance": SLATE, "Initial Access": ORANGE, "Execution": RED,
  "Persistence": VIOLET, "Privilege Escalation": RED, "Defense Evasion": AMBER,
  "Credential Access": ORANGE, "Discovery": BLUE, "Lateral Movement": ORANGE,
  "Collection": BLUE, "Exfiltration": RED, "Impact": RED,
};

/** Composite risk (0–1000) → color. */
export function riskScoreColor(score: number): string {
  if (score >= 800) return RED;
  if (score >= 600) return ORANGE;
  if (score >= 400) return AMBER;
  return GREEN;
}

/** EPSS probability (0–1) → color. */
export function epssColor(score: number): string {
  if (score > 0.7) return RED;
  if (score > 0.4) return ORANGE;
  if (score > 0.1) return AMBER;
  return SLATE;
}

export const SEV_PALETTE = { RED, ORANGE, AMBER, GREEN, SKY, SLATE, VIOLET, BLUE };
