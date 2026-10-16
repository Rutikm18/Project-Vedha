/**
 * Types and wording for the risk-score explanation returned by
 * GET /findings/{id}/risk-explanation (operators) and
 * GET /portal/workspace/findings/{id}/risk-explanation (customers).
 *
 * The backend owns the maths (services/risk_rank.explain_risk_rank). Everything here is
 * presentation: it never recomputes a score, it only words what the server returned.
 */

export interface RiskInput {
  key: string;
  label: string;
  /** What was used: a recorded value, or null when nothing was recorded. */
  raw: string | number | boolean | null;
  /** 0-1 after normalisation. */
  normalized: number;
  /** Weight inside its dimension (the inputs of a dimension sum to 1). */
  weight: number;
  contribution: number;
  /** `recorded`: a real value. `default`: not recorded, the documented neutral value was used. */
  source: "recorded" | "default" | "derived";
  note: string;
}

export interface RiskDimension {
  key: "impact" | "exploit" | "context" | "evidence";
  label: string;
  /** Share of the additive score (0.40 / 0.25 / 0.20 / 0.15). */
  weight: number;
  /** 0-1 weighted value of this dimension. */
  value: number;
  /** value × weight × 1000. */
  points: number;
  inputs: RiskInput[];
}

export interface PriorityRule {
  id: string;
  priority: string;
  condition: string;
  matched: boolean;
  decisive: boolean;
}

export interface PriorityExplanation {
  priority: string | null;
  label: string | null;
  rule: string;
  reason: string;
  inputs: Record<string, unknown>;
  rules: PriorityRule[];
}

export interface RiskExplanation {
  model_version: string;
  score: number;
  max: number;
  severity: string;
  dimensions: RiskDimension[];
  additive_score: number;
  band: { floor: number; ceiling: number; position: number };
  placement: { formula: string; result: number };
  defaults_used: string[];
  context: {
    asset: { ip_address: string | null; hostname: string | null; criticality: string | null } | null;
    internet_exposure_source: string;
    service_exposure: string | null;
  };
  stored_score: number | null;
  stored_in_sync: boolean;
  priority: PriorityExplanation;
}

const pct = (n: number, digits = 0) => `${(n * 100).toFixed(digits)}%`;

/** A short, honest rendering of the value that went into one input. */
export function formatInputValue(input: Pick<RiskInput, "key" | "raw" | "source">): string {
  const { key, raw, source } = input;
  if (raw === null || raw === undefined || source === "default") {
    return "Not recorded";
  }
  switch (key) {
    case "cvss": return `${Number(raw).toFixed(1)} / 10`;
    case "epss": return `${pct(Number(raw), 1)} chance of exploitation`;
    case "confidence": return `${raw}%`;
    case "kev": return raw ? "Listed" : "Not listed";
    case "exploit_validated": return raw ? "Validated" : "Not validated";
    case "internet_facing": return raw ? "Internet-facing" : "Not internet-facing";
    case "auth_gap": return raw ? "No authentication enforced" : "Authentication enforced";
    case "severity":
    case "asset_criticality":
    case "verification":
      return String(raw).replace(/^./, (c) => c.toUpperCase());
    default: return String(raw);
  }
}

/** Points to one decimal, with an explicit sign for the "+" column. */
export function formatPoints(points: number): string {
  return `+${points.toFixed(1)}`;
}

/** One sentence per default, so a reader sees exactly what was assumed. */
export function defaultsSummary(explanation: RiskExplanation): string | null {
  const defaults = explanation.dimensions.flatMap((d) => d.inputs).filter((i) => i.source === "default");
  if (defaults.length === 0) return null;
  const names = defaults.map((i) => i.label.toLowerCase());
  const list = names.length > 2 ? `${names.slice(0, -1).join(", ")} and ${names[names.length - 1]}` : names.join(" and ");
  return `${defaults.length} input${defaults.length === 1 ? " was" : "s were"} not recorded for this finding (${list}), so the documented neutral value was used for ${defaults.length === 1 ? "it" : "each"}. Recording them can raise or lower the score.`;
}

/** The band sentence: why a Critical can never rank below a High. */
export function bandSentence(explanation: RiskExplanation): string {
  const { floor, ceiling } = explanation.band;
  const sev = explanation.severity.replace(/^./, (c) => c.toUpperCase());
  return `${sev} findings are ranked between ${floor} and ${ceiling}, so severity always orders the queue first and the score orders findings within a severity.`;
}

/** The arithmetic of the last step, written out with the real numbers. */
export function placementSentence(explanation: RiskExplanation): string {
  const { floor, ceiling, position } = explanation.band;
  return `${floor} + ${position.toFixed(4)} × (${ceiling} − ${floor}) = ${explanation.score}`;
}
