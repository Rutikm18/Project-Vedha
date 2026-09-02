/**
 * severity.ts — single source of truth for security semantic colors.
 *
 * Values resolve through theme-aware CSS roles. Product blue is never reused
 * as "low"; teal means verified/healthy only, and machine output owns violet.
 */

export type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";
export type FindingStatus =
  | "OPEN" | "CONFIRMED" | "REMEDIATED" | "ACCEPTED" | "FALSE_POSITIVE";
export type ExploitMaturity = "WEAPONIZED" | "POC" | "THEORETICAL";
export type DetectionCoverage = "COVERED" | "PARTIAL" | "BLIND";

const RED = "var(--sev-critical-color)";
const ORANGE = "var(--sev-high-color)";
const AMBER = "var(--sev-medium-color)";
const STONE = "var(--sev-low-color)";
const GREEN = "var(--nominal-color)";
const SKY = "var(--sev-info-color)";
const SLATE = "var(--text-muted)";
const VIOLET = "var(--machine-color)";
const BLUE = "var(--accent)";

export const SEV_COLOR: Record<Severity, string> = {
  CRITICAL: RED, HIGH: ORANGE, MEDIUM: AMBER, LOW: STONE, INFO: SKY,
};

export const STATUS_COLOR: Record<FindingStatus, string> = {
  OPEN: RED, CONFIRMED: ORANGE, REMEDIATED: GREEN,
  // Accepted risk remains an unresolved exposure, so it uses caution amber.
  // Violet is reserved for machine-generated content.
  ACCEPTED: AMBER, FALSE_POSITIVE: SLATE,
};

export const STATUS_LABEL: Record<FindingStatus, string> = {
  OPEN: "OPEN", CONFIRMED: "CONFIRMED", REMEDIATED: "REMEDIATED",
  ACCEPTED: "ACCEPTED", FALSE_POSITIVE: "FALSE POS.",
};

export const MATURITY_COLOR: Record<ExploitMaturity, string> = {
  WEAPONIZED: RED, POC: ORANGE, THEORETICAL: SLATE,
};

export const COVERAGE_COLOR: Record<DetectionCoverage, string> = {
  COVERED: GREEN, PARTIAL: AMBER, BLIND: RED,
};

export const PRIORITY_COLOR: Record<string, string> = {
  P0: RED, P1: ORANGE, P2: AMBER, P3: STONE, P4: SLATE, P5: SLATE,
};

export const PRIORITY_LABEL: Record<string, string> = {
  P0: "Immediate", P1: "Urgent", P2: "Planned", P3: "Monitor", P4: "Low", P5: "Informational",
};

export const KILL_CHAIN_PHASE_COLOR: Record<string, string> = {
  "Reconnaissance": SLATE, "Initial Access": ORANGE, "Execution": RED,
  "Persistence": VIOLET, "Privilege Escalation": RED, "Defense Evasion": AMBER,
  "Credential Access": ORANGE, "Discovery": BLUE, "Lateral Movement": ORANGE,
  "Collection": BLUE, "Exfiltration": RED, "Impact": RED,
};

/** Manager finding risk (0–1000) → semantic response color. */
export function riskScoreColor(score: number): string {
  if (score >= 800) return RED;
  if (score >= 600) return ORANGE;
  if (score >= 400) return AMBER;
  return STONE;
}

/** EPSS probability (0–1) → color. */
export function epssColor(score: number): string {
  if (score > 0.7) return RED;
  if (score > 0.4) return ORANGE;
  if (score > 0.1) return AMBER;
  return SLATE;
}

export const SEV_PALETTE = { RED, ORANGE, AMBER, STONE, GREEN, SKY, SLATE, VIOLET, BLUE };

/* ═══════════════════════════════════════════════════════════════════════════
 *  Console severity model (added for the dashboard redesign)
 *
 *  The exports above are hex values tuned for the light theme and used across
 *  the findings/reports pages — left untouched. The model below is what the
 *  redesigned dashboard components consume: it reads through the app's
 *  theme-aware CSS custom properties (var(--sev-*-color)), so it renders
 *  correctly in BOTH light and dark, and it pairs every colour with a label
 *  and a colour-blind-safe sigil (colour never carries meaning alone).
 * ═══════════════════════════════════════════════════════════════════════════ */

import type { CSSProperties } from "react";

export interface SeverityMeta {
  /** 0 = worst. Sort ascending. */
  rank: number;
  /** Sentence-case label for prose and legends. */
  label: string;
  /** Colour-blind-safe shape cue rendered next to the label. */
  sigil: string;
  color: string;
  bg: string;
  edge: string;
}

export const SEVERITY: Record<Severity, SeverityMeta> = {
  CRITICAL: { rank: 0, label: "Critical", sigil: "◆", color: "var(--sev-critical-color)", bg: "var(--sev-critical-bg)", edge: "var(--sev-critical-edge)" },
  HIGH:     { rank: 1, label: "High",     sigil: "▲", color: "var(--sev-high-color)",     bg: "var(--sev-high-bg)",     edge: "var(--sev-high-edge)" },
  MEDIUM:   { rank: 2, label: "Medium",   sigil: "■", color: "var(--sev-medium-color)",   bg: "var(--sev-medium-bg)",   edge: "var(--sev-medium-edge)" },
  LOW:      { rank: 3, label: "Low",      sigil: "●", color: "var(--sev-low-color)",      bg: "var(--sev-low-bg)",      edge: "var(--sev-low-edge)" },
  INFO:     { rank: 4, label: "Info",     sigil: "▬", color: "var(--sev-info-color)",     bg: "var(--sev-info-bg)",     edge: "var(--sev-info-edge)" },
};

/** Worst → least severe. Use this instead of hand-written arrays. */
export const SEVERITY_ORDER: Severity[] = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"];

/** Backends have shipped `critical`, `Critical` and `CRITICAL`. Normalise here. */
export function toSeverity(raw: string | null | undefined): Severity {
  const k = (raw ?? "").toUpperCase().trim();
  return (SEVERITY_ORDER as string[]).includes(k) ? (k as Severity) : "INFO";
}

export function sev(raw: string | null | undefined): SeverityMeta {
  return SEVERITY[toSeverity(raw)];
}

/** CSS custom properties consumed by `.sev-chip` and `.legend-chip`. */
export function sevVars(s: Severity): CSSProperties {
  const m = SEVERITY[s];
  return { "--sev-color": m.color, "--sev-bg": m.bg, "--sev-edge": m.edge } as CSSProperties;
}
