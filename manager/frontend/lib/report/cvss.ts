/**
 * cvss.ts — decode a raw CVSS vector string into readable, ordered metric chips.
 *
 * The canonical report prints `cvss_vector` raw (e.g. "CVSS:3.1/AV:N/AC:L/…").
 * This turns it into labelled values an engineer can scan, without re-scoring or
 * inventing anything: unknown metrics are dropped, unknown values fall back to
 * the raw code, and empty/garbage input yields an empty list. Tolerates CVSS 3.0,
 * 3.1 and 4.0 (prefix optional).
 */

export interface CvssMetric {
  /** Metric key, e.g. "AV". */
  key: string;
  /** Full code, e.g. "AV:N". */
  code: string;
  /** Human label, e.g. "Attack Vector". */
  label: string;
  /** Raw value letter, e.g. "N". */
  value: string;
  /** Human value, e.g. "Network" (falls back to the raw letter if unknown). */
  valueLabel: string;
}

const METRICS: Record<string, { label: string; values: Record<string, string> }> = {
  AV: { label: "Attack Vector", values: { N: "Network", A: "Adjacent", L: "Local", P: "Physical" } },
  AC: { label: "Attack Complexity", values: { L: "Low", H: "High" } },
  AT: { label: "Attack Requirements", values: { N: "None", P: "Present" } }, // v4
  PR: { label: "Privileges Required", values: { N: "None", L: "Low", H: "High" } },
  UI: { label: "User Interaction", values: { N: "None", R: "Required", P: "Passive", A: "Active" } },
  S:  { label: "Scope", values: { U: "Unchanged", C: "Changed" } }, // v3
  C:  { label: "Confidentiality", values: { H: "High", L: "Low", N: "None" } },
  I:  { label: "Integrity", values: { H: "High", L: "Low", N: "None" } },
  A:  { label: "Availability", values: { H: "High", L: "Low", N: "None" } },
  VC: { label: "Vuln. Confidentiality", values: { H: "High", L: "Low", N: "None" } }, // v4
  VI: { label: "Vuln. Integrity", values: { H: "High", L: "Low", N: "None" } },
  VA: { label: "Vuln. Availability", values: { H: "High", L: "Low", N: "None" } },
  SC: { label: "Subsequent Confidentiality", values: { H: "High", L: "Low", N: "None" } },
  SI: { label: "Subsequent Integrity", values: { H: "High", L: "Low", N: "None" } },
  SA: { label: "Subsequent Availability", values: { H: "High", L: "Low", N: "None" } },
};

/** Presentation order: v3 base, with v4 metrics interleaved where they belong. */
const ORDER = ["AV", "AC", "AT", "PR", "UI", "S", "C", "I", "A", "VC", "VI", "VA", "SC", "SI", "SA"];

export function decodeCvssVector(vector: string | null | undefined): CvssMetric[] {
  if (!vector || typeof vector !== "string") return [];
  const body = vector.trim().replace(/^CVSS:\d+\.\d+\//i, "");
  const found = new Map<string, string>();
  for (const pair of body.split("/")) {
    const [rawKey, rawVal] = pair.trim().split(":");
    if (!rawKey || !rawVal) continue;
    const key = rawKey.toUpperCase();
    if (METRICS[key]) found.set(key, rawVal.toUpperCase());
  }
  const out: CvssMetric[] = [];
  for (const key of ORDER) {
    const value = found.get(key);
    if (value === undefined) continue;
    const meta = METRICS[key];
    out.push({ key, code: `${key}:${value}`, label: meta.label, value, valueLabel: meta.values[value] ?? value });
  }
  return out;
}
