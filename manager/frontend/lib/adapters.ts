/**
 * Contract adapters between the FastAPI backend (snake_case, its enums) and the
 * Vedha UI shapes (camelCase, its enums). All translation lives here so the BFF
 * route handlers stay thin and the UI components don't change.
 */

// ── enums ──────────────────────────────────────────────────────────────────
const ENG_STATUS_TO_UI: Record<string, string> = {
  draft: "PLANNING",
  active: "ACTIVE",
  paused: "PAUSED",
  completed: "COMPLETED",
};
const ENG_STATUS_TO_API: Record<string, string> = {
  PLANNING: "draft",
  ACTIVE: "active",
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

function evidenceToUi(value: unknown): Array<{ label: string; content: string }> {
  if (Array.isArray(value)) return value;
  if (!value || typeof value !== "object") return [];
  return Object.entries(value as Record<string, unknown>).map(([label, content]) => ({
    label,
    content: typeof content === "string" ? content : JSON.stringify(content),
  }));
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
  const risk = api.risk_score != null ? Number(api.risk_score) : cvss * 100;
  return {
    id: api.id,
    title: api.title ?? "Untitled finding",
    severity,
    cvss: api.cvss_score != null ? String(api.cvss_score) : "—",
    cvssVector: api.cvss_vector ?? "",
    category: api.category ?? api.finding_type ?? "General",
    status: FIND_STATUS_TO_UI[String(api.status ?? "open").toLowerCase()] ?? "OPEN",
    affectedHost: api.affected_host ?? api.asset_ip ?? api.asset_id ?? "—",
    discoveredAt: api.created_at ?? api.discovered_at ?? new Date().toISOString(),
    description: api.description ?? "",
    technicalDetails: api.technical_details ?? "",
    attackPath: api.attack_path ?? "",
    evidence: evidenceToUi(api.evidence),
    impact: api.impact ?? "",
    businessImpact: api.business_impact ?? "",
    remediation: api.remediation ? [api.remediation] : [],
    compliance: Array.isArray(api.compliance) ? api.compliance : [],
    mitre: (api.mitre_techniques ?? []).map((m: any) =>
      typeof m === "string" ? { id: m, name: m } : m),
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
    kevDateAdded: api.kev_date_added ?? undefined,
    exploitMaturity: api.exploit_maturity ?? "THEORETICAL",
    exploitMaturityRecorded: api.exploit_maturity != null,
    pocAvailable: api.poc_available ?? false,
    activelyExploited: api.actively_exploited ?? api.exploit_validated ?? api.kev_listed ?? false,
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
