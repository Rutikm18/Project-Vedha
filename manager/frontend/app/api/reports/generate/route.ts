import { NextResponse } from "next/server";
import { generateReport, type ReportSession, type ReportResult } from "../../../../lib/ai-engine";
import type { LiveFinding } from "../../../../lib/engine/types";
import { toSeverity } from "../../../../lib/severity";
import { backend, bearerFrom, cookieFrom, BackendError } from "../../../../lib/backend";

// The report is generated section by section (several sequential + parallel LLM
// calls), so it needs a longer budget than the default serverless timeout.
export const maxDuration = 300;
export const dynamic = "force-dynamic";

/**
 * POST /api/reports/generate
 *
 * The frontend report path — distinct from the backend Python draft/approve
 * flow. It takes the findings the Reports page already loaded, maps them onto
 * the engine finding shape, and runs the deterministic-scorecard report
 * contract (lib/prompts/report.ts) through generateReport. Returns the
 * ReportResult JSON the page renders. Nothing is persisted: this is a live,
 * on-demand draft that still requires human review before delivery.
 */

interface PageFinding {
  id: string;
  title: string;
  severity: string;
  status: string;
  affectedHost: string;
  discoveredAt?: string;
  evidence?: { label: string; content: string; type?: string }[];
  remediation?: Array<string | { title?: string; description?: string; step?: string }>;
  mitre?: { id: string; name: string }[];
  cve?: string[];
  cvss?: string;
  cvssVector?: string;
  activelyExploited?: boolean;
}

interface GenerateBody {
  engagement?: { id?: string; name?: string; client?: string; scopeCidrs?: string[] };
  findings?: PageFinding[];
}

function remText(s: NonNullable<PageFinding["remediation"]>[number]): string {
  return typeof s === "string" ? s : s.description || s.step || s.title || "";
}

// The Reports page's Finding shape carries no port/service/source, so status is
// the only structural signal to coerce. Everything maps to source 'agent';
// the report's per-domain split is therefore coarse, but the overall score
// (severity + KEV + validation) is unaffected.
function mapStatus(s: string): LiveFinding["status"] {
  const u = (s || "").toUpperCase();
  if (/VERIF|VALID/.test(u)) return "VERIFIED";
  if (/CLOSE|RESOLV|FIXED/.test(u)) return "CLOSED";
  if (/REMEDIA/.test(u)) return "IN_REMEDIATION";
  if (/REVIEW/.test(u)) return "IN_REVIEW";
  return "OPEN";
}

function toLiveFinding(f: PageFinding): LiveFinding {
  const rem = Array.isArray(f.remediation)
    ? f.remediation.map(remText).filter(Boolean).join("\n")
    : "";
  return {
    id: f.id,
    title: f.title,
    severity: toSeverity(f.severity),
    cvss: f.cvss || undefined,
    cvssVector: f.cvssVector || undefined,
    host: f.affectedHost,
    evidence: (f.evidence ?? []).map((e) => ({
      label: e.label,
      content: e.content,
      timestamp: new Date().toISOString(),
    })),
    source: "agent",
    cveIds: f.cve && f.cve.length ? f.cve : undefined,
    mitre: f.mitre && f.mitre.length ? f.mitre : undefined,
    remediation: rem || undefined,
    timestamp: f.discoveredAt || new Date().toISOString(),
    status: mapStatus(f.status),
    kev: Boolean(f.activelyExploited), // CISA KEV → doubles weight in buildScorecard
  };
}

export async function POST(req: Request): Promise<Response> {
  let body: GenerateBody;
  try {
    body = (await req.json()) as GenerateBody;
  } catch {
    return NextResponse.json({ error: "Request body must be valid JSON." }, { status: 400 });
  }

  const surface = req.headers.get("x-vedha-surface") === "portal" ? "portal" : "manager";
  const authorization = req.headers.get("authorization") ?? "";
  const portalToken = authorization.startsWith("Bearer ")
    ? authorization.slice(7)
    : cookieFrom(req, "vedha_portal_token");
  const token = surface === "portal" ? portalToken : bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  if (!body.engagement?.id) {
    return NextResponse.json({ error: "engagement.id is required" }, { status: 400 });
  }
  if (!Array.isArray(body.findings) || body.findings.length > 100) {
    return NextResponse.json({ error: "findings must contain at most 100 records" }, { status: 400 });
  }

  // Resolve the workspace with the credential that owns it. The portal route
  // ignores browser scope and returns only the engagement pinned in the JWT.
  try {
    const canonical = await backend<Record<string, unknown>>(
      surface === "portal"
        ? "/portal/workspace/engagement"
        : `/engagements/${encodeURIComponent(body.engagement.id)}`,
      { token },
    );
    if (String(canonical.id ?? "") !== body.engagement.id) {
      return NextResponse.json({ error: "Engagement scope mismatch" }, { status: 403 });
    }
  } catch (error) {
    const code = error instanceof BackendError ? error.status : 502;
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Engagement validation failed" },
      { status: code },
    );
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    return NextResponse.json(
      { error: "AI report generation is not configured (set ANTHROPIC_API_KEY)." },
      { status: 503 },
    );
  }

  const findings = (body.findings ?? []).map(toLiveFinding);
  if (findings.length === 0) {
    return NextResponse.json(
      { error: "No findings to report on for this engagement." },
      { status: 422 },
    );
  }

  const session: ReportSession = {
    clientName: body.engagement?.client || body.engagement?.name || "Client",
    scope: body.engagement?.scopeCidrs ?? [],
    findings,
    exploitResults: [],
    engagementType: "VAPT",
  };

  try {
    const report: ReportResult = await generateReport(session);
    return NextResponse.json(report);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
