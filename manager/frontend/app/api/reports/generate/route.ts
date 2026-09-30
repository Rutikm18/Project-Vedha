import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../lib/backend";

export const dynamic = "force-dynamic";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const ALLOWED_KEYS = new Set(["engagementId", "sections", "maxFindings"]);
const ALLOWED_SECTIONS = new Set(["technical_finding", "remediation"]);

interface GenerateBody {
  engagementId: string;
  sections?: string[];
  maxFindings?: number;
}

function parseBody(value: unknown): GenerateBody | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const body = value as Record<string, unknown>;
  if (Object.keys(body).some((key) => !ALLOWED_KEYS.has(key))) return null;
  if (typeof body.engagementId !== "string" || !UUID.test(body.engagementId)) return null;
  if (
    body.sections !== undefined
    && (!Array.isArray(body.sections)
      || body.sections.some((section) => typeof section !== "string" || !ALLOWED_SECTIONS.has(section)))
  ) return null;
  if (
    body.maxFindings !== undefined
    && (typeof body.maxFindings !== "number"
      || !Number.isInteger(body.maxFindings)
      || body.maxFindings < 1
      || body.maxFindings > 50)
  ) return null;
  return body as unknown as GenerateBody;
}

/**
 * Compatibility endpoint for the Reports workspace.
 *
 * The browser may choose the engagement and bounded generation options only.
 * Manager re-loads the engagement and findings from PostgreSQL, then enforces
 * tenant scope, RBAC, persistence, and human review. Caller-supplied report
 * facts are deliberately rejected rather than forwarded to a model.
 */
export async function POST(request: Request): Promise<Response> {
  const token = bearerFrom(request);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });

  const body = parseBody(await request.json().catch(() => null));
  if (!body) {
    return NextResponse.json(
      { error: "Body must contain only a valid engagementId, optional sections, and maxFindings (1-50)." },
      { status: 400 },
    );
  }

  const sections = body.sections ?? [];
  try {
    const result = await backend<{ job_id: string; status: string }>(
      `/engagements/${body.engagementId}/ai-report/generate`,
      {
        method: "POST",
        token,
        body: {
          include_technical: sections.length === 0 || sections.includes("technical_finding"),
          include_remediation: sections.length === 0 || sections.includes("remediation"),
          max_findings: body.maxFindings ?? 10,
        },
      },
    );
    return NextResponse.json({ ...result, jobId: result.job_id }, { status: 202 });
  } catch (error) {
    const status = error instanceof BackendError ? error.status : 502;
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Report generation failed" },
      { status },
    );
  }
}
