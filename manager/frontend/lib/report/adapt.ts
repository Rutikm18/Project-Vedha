/**
 * Converts the dashboard finding shape into the report model without inventing
 * facts that the Manager API did not return. The report model intentionally
 * renders absent values as gaps so an assessor can resolve them before export.
 */
import type {
  DetectionMethod,
  RawAsset,
  RawEvidence,
  RawFinding,
  RawRemediation,
} from "./finding-model";

type UnknownRecord = Record<string, unknown>;

function text(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? value.trim() : undefined;
}

function finite(value: unknown): number | undefined {
  const number = typeof value === "number" ? value : Number(value);
  return Number.isFinite(number) ? number : undefined;
}

export function deriveDetectionMethod(input: unknown): DetectionMethod | undefined {
  const finding = input && typeof input === "object" ? input as UnknownRecord : {};
  if (finding.exploitValidated === true) return "exploit";
  const state = text(finding.verificationState)?.toLowerCase();
  if (state === "confirmed") return "behavioural";
  if (state === "corroborated") return "configuration";
  return undefined;
}

export function toReportAssets(input: unknown): RawAsset[] {
  const finding = input && typeof input === "object" ? input as UnknownRecord : {};
  const context = finding.assetContext;
  if (!context || typeof context !== "object") return [];
  const asset = context as UnknownRecord;
  const host = text(asset.hostname) ?? text(asset.fqdn) ?? text(asset.ipAddress);
  if (!host) return [];
  return [{
    host,
    ip: text(asset.ipAddress),
    version: text(asset.osVersion) ?? text(asset.os),
    environment: text(asset.environment),
    owner: text(asset.owner),
    // Environment labels are not proof of reachability. Leave this unknown
    // until the backend returns an explicit exposure fact.
    internetReachable: typeof asset.internetReachable === "boolean"
      ? asset.internetReachable
      : undefined,
  }];
}

function evidence(value: unknown): RawEvidence[] {
  if (!Array.isArray(value)) return [];
  return value.flatMap((entry, index) => {
    if (!entry || typeof entry !== "object") return [];
    const item = entry as UnknownRecord;
    const content = typeof item.content === "string" ? item.content : "";
    return [{
      label: text(item.label) ?? `Evidence ${index + 1}`,
      content,
      type: text(item.type),
      tool: text(item.tool),
      command: text(item.command),
      capturedAt: text(item.capturedAt) ?? text(item.timestamp),
      capturedBy: text(item.capturedBy),
      sourceHost: text(item.sourceHost),
      sha256: text(item.sha256),
    }];
  });
}

function remediation(value: unknown): Array<string | RawRemediation> {
  if (!Array.isArray(value)) return [];
  return value.filter((step): step is string | RawRemediation =>
    typeof step === "string" || Boolean(step && typeof step === "object"),
  );
}

function stringList(value: unknown): string[] {
  return Array.isArray(value)
    ? value.filter((item): item is string => typeof item === "string" && item.trim().length > 0)
    : [];
}

export function toRawFinding(input: unknown, dueAt?: string | null): RawFinding {
  const finding = input && typeof input === "object" ? input as UnknownRecord : {};
  const epss = finding.epssRecorded === true ? finite(finding.epssScore) : undefined;
  const contextAssets = toReportAssets(finding);
  const cves = stringList(finding.cve ?? finding.cves);
  const attackPath = Array.isArray(finding.attackPath)
    ? stringList(finding.attackPath)
    : text(finding.attackPath)
      ? [text(finding.attackPath)!]
      : undefined;

  return {
    id: text(finding.id) ?? "unidentified-finding",
    title: text(finding.title) ?? "Untitled finding",
    severity: text(finding.severity) ?? "INFO",
    status: text(finding.status) ?? "OPEN",
    affectedHost: contextAssets[0]?.host ?? text(finding.affectedHost) ?? "",
    discoveredAt: text(finding.discoveredAt) ?? "",
    description: text(finding.description) ?? "",
    technicalDetails: text(finding.technicalDetails) ?? "",
    evidence: evidence(finding.evidence),
    impact: text(finding.businessImpact) ?? text(finding.impact) ?? "",
    remediation: remediation(finding.remediation),
    mitre: Array.isArray(finding.mitre)
      ? finding.mitre.filter((item): item is { id: string; name: string } =>
          Boolean(item && typeof item === "object" && text((item as UnknownRecord).id)),
        )
      : [],
    cwe: Array.isArray(finding.cwe)
      ? finding.cwe.filter((item): item is { id: string; name: string } =>
          Boolean(item && typeof item === "object" && text((item as UnknownRecord).id)),
        )
      : undefined,
    cve: cves,
    riskScore: finite(finding.riskScore) ?? 0,
    cvss: text(finding.cvss) ?? "",
    cvssVector: text(finding.cvssVector),
    activelyExploited: finding.exploitedInWild === true || finding.kevListed === true,
    exploitValidated: finding.exploitValidated === true,
    detectionCoverage: text(finding.detectionCoverage) ?? "",
    detectionMethod: deriveDetectionMethod(finding),
    assets: contextAssets,
    epss,
    epssPercentile: finding.epssRecorded === true ? finite(finding.epssPercentile) : undefined,
    kevAddedAt: text(finding.kevDateAdded),
    exploitPublic: finding.pocAvailable === true,
    internetReachable: contextAssets[0]?.internetReachable,
    reproductionSteps: text(finding.reproductionSteps),
    attackPath,
    dueAt: dueAt ?? undefined,
    assignedTo: text(finding.assignee),
    retestedAt: text(finding.resolvedAt),
  };
}
