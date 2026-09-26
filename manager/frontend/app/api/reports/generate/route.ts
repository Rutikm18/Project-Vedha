import { NextResponse } from "next/server";
import { backend, bearerFrom, cookieFrom, BackendError } from "../../../../lib/backend";

// Report generation runs several model sections on the backend; give the proxy
// the same generous budget the in-process generator used to have.
export const maxDuration = 300;
export const dynamic = "force-dynamic";

/**
 * POST /api/reports/generate
 *
 * BFF proxy to the backend report generator (FastAPI
 * `POST /engagements/{id}/ai-report/engagement`, or the portal equivalent).
 *
 * This route used to call Anthropic directly from Next.js, which bypassed the
 * AI gateway (hybrid pseudonymisation, sovereign in-bank models), the AI audit
 * chain and the sector brief, and let the model invent the remediation grouping.
 * The backend now loads the findings itself (no browser-supplied payload, no
 * 100-finding cap), computes the scorecard and the fix-bundle roadmap
 * deterministically, and routes every model call through the gateway.
 */
interface GenerateBody {
  engagement?: { id?: string };
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
  if (surface === "manager" && !body.engagement?.id) {
    return NextResponse.json({ error: "engagement.id is required" }, { status: 400 });
  }

  const path = surface === "portal"
    ? "/portal/ai-report/engagement"
    : `/engagements/${encodeURIComponent(body.engagement!.id!)}/ai-report/engagement`;
  try {
    const report = await backend<Record<string, unknown>>(path, { method: "POST", token });
    return NextResponse.json(report);
  } catch (error) {
    const status = error instanceof BackendError ? error.status : 502;
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Report generation failed" },
      { status },
    );
  }
}
