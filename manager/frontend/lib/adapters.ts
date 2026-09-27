/**
 * Contract adapters between the FastAPI backend (snake_case, its enums) and the
 * Vedha UI shapes (camelCase, its enums). All translation lives here so the BFF
 * route handlers stay thin and the UI components don't change.
 */

import type { EvidenceArtifact } from "./evidence-presentation";

// ── enums ──────────────────────────────────────────────────────────────────
const ENG_STATUS_TO_UI: Record<string, string> = {
  draft: "PLANNING",
  active: "ACTIVE",
  ongoing: "ONGOING",
  running: "RUNNING",
  paused: "PAUSED",
  completed: "COMPLETED",
};
const ENG_STATUS_TO_API: Record<string, string> = {
  PLANNING: "draft",
  ACTIVE: "active",
  ONGOING: "ongoing",
  RUNNING: "running",
  PAUSED: "paused",
  COMPLETED: "completed",
  ARCHIVED: "completed",
};

export function engStatusToUi(s?: string): string {
  return ENG_STATUS_TO_UI[s ?? ""] ?? "PLANNING";
}
export function engStatusToApi(s?: string): string {
  return ENG_STATUS_TO_API[s ?? ""] ?? "draft";
}

// ── Engagement ───────────────────────────────────────────────────────────────
// FastAPI EngagementOut / EngagementDetail → UI Engagement
export function toUiEngagement(api: any): any {
  const fs = api.finding_summary ?? {};
  const total = fs.total ?? 0;
  const done = api.status === "completed" ? 100 : Math.min(95, total ? Math.round((fs.remediated ?? 0) / total * 100) : 0);
  const roe = api.rules_of_engagement ?? {};
  return {
    id: api.id,
    name: api.name,
    client: roe.client ?? api.tenant_name ?? "—",
    status: engStatusToUi(api.status),
    startDate: api.start_time ?? "",
    endDate: api.end_time ?? "",
    scopeCidrs: api.scope_cidrs ?? [],
    excludedCidrs: api.excluded_cidrs ?? [],
    assessor: roe.assessor ?? "—",
    description: roe.description ?? "",
    assetCount: api.asset_count ?? 0,
    findingCount: total,
    findingsBySeverity: {
      CRITICAL: fs.critical ?? 0,
      HIGH: fs.high ?? 0,
      MEDIUM: fs.medium ?? 0,
      LOW: fs.low ?? 0,
    },
    progress: done,
    tags: roe.tags ?? [],
  };
}

// UI create form → FastAPI EngagementCreate body
export function toApiEngagementCreate(ui: any): any {
  const scope = normalizeList(ui.scopeCidrs);
  return {
    name: ui.name,
    scope_cidrs: scope,
    excluded_cidrs: normalizeList(ui.excludedCidrs),
    start_time: ui.startDate || null,
    end_time: ui.endDate || null,
    // The UI carries client/assessor/tags that FastAPI doesn't model as columns —
    // park them in rules_of_engagement so nothing is lost.
    rules_of_engagement: {
      client: ui.client ?? null,
      assessor: ui.assessor ?? null,
      description: ui.description ?? null,
      tags: ui.tags ?? [],
      credentials: ui.credentials ?? [],
    },
  };
}

// ── Finding ────────────────────────────────────────────────────────────────
const SEV_TO_UI: Record<string, string> = {
  critical: "CRITICAL", high: "HIGH", medium: "MEDIUM", low: "LOW", info: "INFO",
};
// FastAPI DetectionStatus → UI DetectionCoverage
const DETECTION_TO_UI: Record<string, string> = {
  detected: "COVERED", prevented: "COVERED", missed: "BLIND", unknown: "PARTIAL",
};
const FIND_STATUS_TO_UI: Record<string, string> = {
  open: "OPEN",
  confirmed: "CONFIRMED",
  remediated: "REMEDIATED",
  accepted: "ACCEPTED",
  fp: "FALSE_POSITIVE",
};
function severityToPriority(sev: string): string {
  return sev === "CRITICAL" ? "P0" : sev === "HIGH" ? "P1" : sev === "MEDIUM" ? "P2" : "P3";
}

function evidenceString(value: unknown): string {
  if (typeof value === "string") return value;
  if (value === undefined) return "";
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

function optionalEvidenceString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim() ? value : undefined;
}

function evidenceToUi(value: unknown): EvidenceArtifact[] {
  if (Array.isArray(value)) {
    return value.map((item, index) => {
      if (typeof item === "string") {
        return { label: `Evidence artifact ${index + 1}`, content: item };
      }
      if (!item || typeof item !== "object") {
        return { label: `Evidence artifact ${index + 1}`, content: evidenceString(item) };
      }

      const record = item as Record<string, unknown>;
      return {
        label: optionalEvidenceString(record.label) ?? `Evidence artifact ${index + 1}`,
        content: evidenceString(record.content ?? record.output ?? record.value ?? record),
        type: optionalEvidenceString(record.type),
        tool: optionalEvidenceString(record.tool),
        source: optionalEvidenceString(record.source),
        command: optionalEvidenceString(record.command),
        timestamp: optionalEvidenceString(record.timestamp),
        capturedAt: optionalEvidenceString(record.capturedAt ?? record.captured_at),
        capturedBy: optionalEvidenceString(record.capturedBy ?? record.captured_by),
        sourceHost: optionalEvidenceString(record.sourceHost ?? record.source_host),
        sha256: optionalEvidenceString(record.sha256),
      };
    });
  }
  if (!value || typeof value !== "object") return [];

  const record = value as Record<string, unknown>;
  const source = optionalEvidenceString(record.tool ?? record.engine ?? record.source ?? record.scan_type);
  return [{
    label: source ? `${source} evidence` : "Structured scanner evidence",
    content: evidenceString(record),
    type: "json",
    tool: source,
    timestamp: optionalEvidenceString(record.timestamp),
    capturedAt: optionalEvidenceString(record.capturedAt ?? record.captured_at),
    capturedBy: optionalEvidenceString(record.capturedBy ?? record.captured_by),
    sourceHost: optionalEvidenceString(record.sourceHost ?? record.source_host),
    sha256: optionalEvidenceString(record.sha256),
  }];
}

// FastAPI Finding → the UI's rich Finding shape. Real backend fields are mapped;
// fields the backend doesn't produce yet (kill chain, AI triage narrative, evidence)
// default to safe empty values so the detail view renders without errors.
export function toUiFinding(api: any): any {
  const severity = SEV_TO_UI[api.severity] ?? "INFO";
  const cvss = api.cvss_score != null ? Number(api.cvss_score) : 0;
  const epss = api.epss_score != null ? Number(api.epss_score) : 0;
  // The backend composite risk contract is 0–1000. If enrichment has not run,
  // normalize CVSS (0–10) onto that same display scale.
  // `risk_rank` is recalculated by the Manager's canonical non-saturating
  // formula on every response. Prefer it over legacy persisted scores so rows
  // written under the old clipping formula do not keep displaying 1000/1000.
  const risk = api.risk_rank != null
    ? Number(api.risk_rank)
    : api.risk_score != null
      ? Number(api.risk_score)
      : cvss * 100;
  return {
    id: api.id,
    title: api.title ?? "Untitled finding",
    severity,
    cvss: api.cvss_score != null ? String(api.cvss_score) : "—",
    cvssVector: api.cvss_vector ?? "",
    category: api.category ?? api.finding_type ?? "General",
    status: FIND_STATUS_TO_UI[String(api.status ?? "open").toLowerCase()] ?? "OPEN",
    // IP first; never fall back to the opaque asset UUID.
    affectedHost: api.affected_host ?? api.asset_ip ?? api.asset_hostname ?? "—",
    assetIp: api.asset_ip ?? api.asset_context?.ip_address ?? null,
    // Needed by engagement-scoped panels (fix bundles, deadline extensions).
    engagementId: api.engagement_id ?? null,
    assetHostname: api.asset_hostname ?? api.asset_context?.hostname ?? null,
    discoveredAt: api.first_seen ?? api.created_at ?? api.discovered_at ?? "",
    description: api.description ?? "",
    technicalDetails: api.technical_details ?? "",
    attackPath: api.attack_path ?? "",
    evidence: evidenceToUi(api.evidence),
    // Clean, deterministic "key facts" from the backend evidence_summary service —
    // the glanceable view. Raw artifacts (evidence above) stay behind a disclosure.
    evidenceSummary: Array.isArray(api.evidence_summary) ? api.evidence_summary : [],
    impact: api.impact ?? "",
    businessImpact: api.business_impact ?? "",
    // Honest exploitation posture block (finding_content): validated vs
    // "Not validated. Absence of proof is not proof of absence." + KEV/EPSS framing.
    exploitation: api.exploitation ?? null,
    remediation: api.remediation ? [api.remediation] : [],
    compliance: Array.isArray(api.compliance) ? api.compliance : [],
    mitre: (api.mitre_techniques ?? []).map((m: any) =>
      typeof m === "string" ? { id: m, name: m } : m),
    cve: api.cve_ids ?? [],
    cves: api.cve_ids ?? [],
    riskScore: Math.round(risk),
    riskBreakdown: api.risk_breakdown ?? {
      cvss, epss: Math.round(epss * 100), kev: api.kev_listed ? 100 : 0,
      exploit: 0, asset: 0, lateral: 0,
    },
    epssScore: epss,
    epssPercentile: api.epss_percentile ?? 0,
    epssRecorded: api.epss_score != null,
    kevListed: api.kev_listed ?? false,
    kevStatusRecorded: api.kev_listed != null,
    kevDateAdded: api.kev_added_at ?? api.kev_date_added ?? undefined,
    exploitMaturity: api.exploit_maturity ?? "THEORETICAL",
    exploitMaturityRecorded: api.exploit_maturity != null,
    pocAvailable: api.poc_available ?? false,
    // Keep these signals distinct. Reproducing an exploit in an authorised
    // assessment is not the same claim as exploitation in the wild or KEV.
    // (Backend now emits actively_exploited directly; prefer it over derivation.)
    activelyExploited: api.actively_exploited ?? api.kev_listed ?? false,
    exploitedInWild: api.actively_exploited ?? false,
    exploitValidated: api.exploit_validated ?? false,
    detectionCoverage: DETECTION_TO_UI[api.detection_status] ?? "PARTIAL",
    detectionNote: api.detection_note ?? undefined,
    fpProbability: api.fp_probability ?? 0,
    fpProbabilityRecorded: api.fp_probability != null,
    relatedFindings: api.related_findings ?? [],
    killChain: Array.isArray(api.kill_chain) ? api.kill_chain : [],
    assignee: api.assignee ?? undefined,
    tags: api.tags ?? api.cve_ids ?? [],
    aiTriage: api.ai_triage ?? {
      priority: severityToPriority(severity),
      reasoning: "",
      recommendation: "",
      confidence: 0,
    },
    // ── P2/P4 verification + lifecycle surfacing ──
    verificationState: api.verification_state ?? null,
    verificationConfidence: api.verification_confidence ?? null,
    verificationRationale: api.verification_rationale ?? null,
    // ── Phase 3 report enrichment (backend-computed; the report adapter prefers
    //    these over its own client-side derivations). ──
    detectionMethod: api.detection_method ?? undefined,
    verification: api.verification ?? undefined,
    internetReachable: api.internet_reachable ?? undefined,
    needsReview: api.needs_review ?? false,
    riskRank: api.risk_rank ?? null,
    resolutionMethod: api.resolution_method ?? null,
    reopenedCount: api.reopened_count ?? 0,
    resolvedAt: api.resolved_at ?? null,
    lastSeen: api.updated_at ?? null,
    // `evidence.regression` is set by the engine when a resolved finding reappears.
    regression:
      api.evidence && typeof api.evidence === "object" && !Array.isArray(api.evidence)
        ? Boolean((api.evidence as Record<string, unknown>).regression)
        : false,
    assetContext: api.asset_context ? {
      id: api.asset_context.id,
      ipAddress: api.asset_context.ip_address ?? null,
      hostname: api.asset_context.hostname ?? null,
      fqdn: api.asset_context.fqdn ?? null,
      os: api.asset_context.os ?? null,
      osVersion: api.asset_context.os_version ?? null,
      assetType: api.asset_context.asset_type ?? "unknown",
      criticality: api.asset_context.criticality ?? "unknown",
      owner: api.asset_context.owner ?? null,
      environment: api.asset_context.environment ?? null,
    } : null,
    // The scan that most recently produced/confirmed this finding (per-scan-findings).
    // Lets the UI label each finding with its SCN reference / intensity / use-case.
    scan: api.scan ? {
      reference: api.scan.reference ?? null,
      useCaseId: api.scan.use_case_id ?? null,
      intensity: api.scan.intensity ?? null,
      scannedAt: api.scan.scanned_at ?? null,
      jobId: api.scan.job_id ?? null,
      runId: api.scan.run_id ?? null,
    } : null,
    // What the FILTERED scan did to this finding (new|reaffirmed|resolved); set only
    // when the list is filtered by ?scan=.
    scanOutcome: api.scan_outcome ?? null,
  };
}

/** One scan option for the findings "filter by scan" control + compare picker
 *  (backend /findings/scans). */
export interface ApiScanOption {
  job_id: string;
  reference: string | null;
  use_case_id: string | null;
  intensity: string | null;
  scanned_at: string | null;
  status: string | null;
  findings: number;
}

export interface ScanOption {
  jobId: string;
  reference: string | null;
  useCaseId: string | null;
  intensity: string | null;
  scannedAt: string | null;
  status: string | null;
  findings: number;
}

export function mapScanOption(s: ApiScanOption): ScanOption {
  return {
    jobId: s.job_id,
    reference: s.reference ?? null,
    useCaseId: s.use_case_id ?? null,
    intensity: s.intensity ?? null,
    scannedAt: s.scanned_at ?? null,
    status: s.status ?? null,
    findings: s.findings ?? 0,
  };
}

/** Backend FindingScanRef (snake_case) → the UI scan block. */
export function mapScanRef(ref: any) {
  if (!ref) return null;
  return {
    reference: ref.reference ?? null,
    useCaseId: ref.use_case_id ?? null,
    intensity: ref.intensity ?? null,
    scannedAt: ref.scanned_at ?? null,
    jobId: ref.job_id ?? null,
    runId: ref.run_id ?? null,
  };
}

/** Backend /findings/compare result → the UI compare shape. Shared by the BFF
 *  proxy (manager surface) and the portal transport so both map identically. */
export function mapCompareResult(data: any) {
  return {
    a: mapScanRef(data?.a),
    b: mapScanRef(data?.b),
    counts: {
      new: data?.counts?.new ?? 0,
      fixed: data?.counts?.fixed ?? 0,
      stillPresent: data?.counts?.still_present ?? 0,
    },
    new: (data?.new ?? []).map(toUiFinding),
    fixed: (data?.fixed ?? []).map(toUiFinding),
    stillPresent: (data?.still_present ?? []).map(toUiFinding),
  };
}

// ── Agent / probe ────────────────────────────────────────────────────────────
// Backend /agents rows are snake_case with a lowercase status enum
// (online|offline|busy) plus a derived `online` bool. The UI expects camelCase
// and an uppercase status. A probe that is reachable AND running a job reads as
// BUSY; reachable+idle as ONLINE; unreachable as OFFLINE.
export function toUiAgent(api: any): any {
  const busy = String(api.status ?? "").toLowerCase() === "busy" || api.current_job_id != null;
  return {
    id: api.id,
    name: api.name,
    location: api.location ?? null,
    status: api.online ? (busy ? "BUSY" : "ONLINE") : "OFFLINE",
    online: !!api.online,
    capabilities: api.capabilities ?? [],
    networkSegments: api.network_segments ?? [],
    lastHeartbeat: api.last_heartbeat ?? null,
    currentJobId: api.current_job_id ?? null,
  };
}

// UI finding-triage patch → FastAPI FindingPatch body
const FIND_STATUS_TO_API: Record<string, string> = {
  OPEN: "open", CONFIRMED: "confirmed", REMEDIATED: "remediated",
  ACCEPTED: "accepted", FP: "fp", FALSE_POSITIVE: "fp", "FALSE-POSITIVE": "fp",
};
export function toApiFindingPatch(ui: any): any {
  const out: any = {};
  if (ui.status) out.status = FIND_STATUS_TO_API[String(ui.status).toUpperCase()] ?? "open";
  if (ui.actionReason != null) out.action_reason = String(ui.actionReason);
  if (ui.notes != null) out.notes = ui.notes;
  if (ui.remediation != null) out.remediation = ui.remediation;
  if (typeof ui.exploitable === "boolean") out.exploitable = ui.exploitable;
  return out;
}

// UI engagement-detail patch → FastAPI EngagementUpdate body.
// Column fields go top-level; the UI-only fields (client/assessor/description/tags)
// live in rules_of_engagement, sent as a PARTIAL the backend shallow-merges — so
// editing one of them never drops the others (or the stored credentials).
export function toApiEngagementPatch(ui: any): any {
  const out: any = {};
  if (ui.name != null) out.name = ui.name;
  if (ui.status != null) out.status = engStatusToApi(ui.status);
  if (ui.scopeCidrs != null) out.scope_cidrs = normalizeList(ui.scopeCidrs);
  if (ui.excludedCidrs != null) out.excluded_cidrs = normalizeList(ui.excludedCidrs);
  if (ui.startDate !== undefined) out.start_time = ui.startDate || null;
  if (ui.endDate !== undefined) out.end_time = ui.endDate || null;

  const roe: Record<string, unknown> = {};
  if (ui.client != null) roe.client = ui.client;
  if (ui.assessor != null) roe.assessor = ui.assessor;
  if (ui.description != null) roe.description = ui.description;
  if (ui.tags != null) roe.tags = Array.isArray(ui.tags) ? ui.tags : normalizeList(ui.tags);
  if (Object.keys(roe).length) out.rules_of_engagement = roe;

  return out;
}

function normalizeList(v: unknown): string[] {
  if (Array.isArray(v)) return v.map((x) => String(x).trim()).filter(Boolean);
  if (typeof v === "string") return v.split(/[\n,]/).map((x) => x.trim()).filter(Boolean);
  return [];
}

/** Affected-asset option for the findings IP filter (backend /findings/assets). */
export interface ApiFindingAsset {
  asset_id: string;
  ip_address: string;
  hostname?: string | null;
  findings: number;
}

export interface FindingAssetOption {
  assetId: string;
  ip: string;
  hostname: string | null;
  findings: number;
}

export function mapAsset(a: ApiFindingAsset): FindingAssetOption {
  return { assetId: a.asset_id, ip: a.ip_address, hostname: a.hostname ?? null, findings: a.findings };
}

// ─── Grouped findings (GET /findings/groups) ─────────────────────────────────
// Similar findings collapsed into one-fix units. The operator BFF maps on the
// server; the portal maps the raw backend payload in the browser — same adapter.

export type FindingGroupKind = "rule" | "product" | "title";

interface ApiFindingGroupMember {
  id: string; title: string; severity: string; status: string;
  asset_ip?: string | null; asset_hostname?: string | null; port?: number | null;
  cve_ids?: string[] | null; risk?: number | null; cvss?: number | null;
}

interface ApiFindingGroup {
  engagement_id: string;
  key: string; kind: FindingGroupKind; label: string; severity: string;
  severity_counts?: Record<string, number>; status_counts?: Record<string, number>;
  finding_count: number; open_count: number; host_count: number; unassigned_count?: number;
  hosts?: { ip?: string | null; hostname?: string | null }[];
  ports?: number[]; port_count?: number; cve_count?: number; cves?: string[];
  max_risk?: number | null; max_cvss?: number | null; max_epss?: number | null;
  kev?: boolean; exploit_validated?: boolean;
  first_seen?: string | null; last_seen?: string | null;
  top_finding_id: string;
  members?: ApiFindingGroupMember[]; members_truncated?: boolean;
}

export interface ApiFindingGroupPage {
  items?: ApiFindingGroup[]; total?: number; page?: number; page_size?: number;
  pages?: number; finding_total?: number; truncated?: boolean;
}

export interface FindingGroupMember {
  id: string; title: string; severity: string; status: string;
  assetIp: string | null; assetHostname: string | null; port: number | null;
  cveIds: string[]; risk: number; cvss: number | null;
}

export interface FindingGroup {
  /** Groups never span engagements; `key` is the identity within one. */
  engagementId: string;
  key: string; kind: FindingGroupKind; label: string; severity: string;
  severityCounts: Record<string, number>; statusCounts: Record<string, number>;
  findingCount: number; openCount: number; hostCount: number; unassignedCount: number;
  hosts: { ip: string | null; hostname: string | null }[];
  ports: number[]; portCount: number; cveCount: number; cves: string[];
  maxRisk: number; maxCvss: number | null; maxEpss: number | null;
  kev: boolean; exploitValidated: boolean;
  firstSeen: string | null; lastSeen: string | null;
  topFindingId: string;
  members: FindingGroupMember[]; membersTruncated: boolean;
}

export interface FindingGroupPage {
  items: FindingGroup[]; total: number; page: number; pageSize: number;
  pages: number; findingTotal: number; truncated: boolean;
}

const sevUi = (s: string | undefined) => SEV_TO_UI[String(s ?? "").toLowerCase()] ?? "INFO";

export function mapFindingGroup(g: ApiFindingGroup): FindingGroup {
  const severityCounts: Record<string, number> = {};
  for (const [k, v] of Object.entries(g.severity_counts ?? {})) severityCounts[sevUi(k)] = v;
  const statusCounts: Record<string, number> = {};
  for (const [k, v] of Object.entries(g.status_counts ?? {})) {
    statusCounts[FIND_STATUS_TO_UI[k] ?? k.toUpperCase()] = v;
  }
  return {
    engagementId: g.engagement_id,
    key: g.key,
    kind: g.kind,
    label: g.label,
    severity: sevUi(g.severity),
    severityCounts,
    statusCounts,
    findingCount: g.finding_count ?? 0,
    openCount: g.open_count ?? 0,
    hostCount: g.host_count ?? 0,
    unassignedCount: g.unassigned_count ?? 0,
    hosts: (g.hosts ?? []).map((h) => ({ ip: h.ip ?? null, hostname: h.hostname ?? null })),
    ports: g.ports ?? [],
    portCount: g.port_count ?? (g.ports ?? []).length,
    cveCount: g.cve_count ?? 0,
    cves: g.cves ?? [],
    maxRisk: g.max_risk ?? 0,
    maxCvss: g.max_cvss ?? null,
    maxEpss: g.max_epss ?? null,
    kev: Boolean(g.kev),
    exploitValidated: Boolean(g.exploit_validated),
    firstSeen: g.first_seen ?? null,
    lastSeen: g.last_seen ?? null,
    topFindingId: g.top_finding_id,
    members: (g.members ?? []).map((m) => ({
      id: m.id,
      title: m.title,
      severity: sevUi(m.severity),
      status: FIND_STATUS_TO_UI[String(m.status ?? "open").toLowerCase()] ?? "OPEN",
      assetIp: m.asset_ip ?? null,
      assetHostname: m.asset_hostname ?? null,
      port: m.port ?? null,
      cveIds: m.cve_ids ?? [],
      risk: m.risk ?? 0,
      cvss: m.cvss ?? null,
    })),
    membersTruncated: Boolean(g.members_truncated),
  };
}

export function mapFindingGroupPage(p: ApiFindingGroupPage): FindingGroupPage {
  return {
    items: (p.items ?? []).map(mapFindingGroup),
    total: p.total ?? 0,
    page: p.page ?? 1,
    pageSize: p.page_size ?? 20,
    pages: p.pages ?? 1,
    findingTotal: p.finding_total ?? 0,
    truncated: Boolean(p.truncated),
  };
}
