/**
 * Ask Vedha — grounded "explain a finding" BFF.
 *   POST /api/assistant/explain  { findingId, mode? }
 *     → fetch the REAL finding (FastAPI), build a deterministic fact card,
 *       then have the LLM narrate it in plain English (grounded, no invented facts).
 * Degrades to fact-card-only when Manager's model runtime is unavailable.
 * Model policy and provider credentials stay in Manager.
 */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../lib/backend";
import { resolveSecurityReference, SecurityContextError } from "../../../../lib/security-context";
import { parseAdvisor } from "../../../../lib/assistant";

interface ManagerAiResponse {
  content: string;
  provider: string;
  model: string;
}

export async function POST(req: Request) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });

  const body = (await req.json().catch(() => null)) as { findingId?: string; mode?: string } | null;
  if (!body?.findingId) {
    return NextResponse.json({ error: "findingId is required" }, { status: 400 });
  }

  let resolved;
  try {
    resolved = await resolveSecurityReference({ reference: body.findingId, token });
  } catch (e) {
    const status = e instanceof BackendError || e instanceof SecurityContextError ? e.status : 500;
    return NextResponse.json({ error: (e as Error)?.message ?? "security reference not found" }, { status });
  }
  const { factCard } = resolved;

  try {
    const result = await backend<ManagerAiResponse>("/ai/generate", {
      method: "POST",
      token,
      body: {
        task: "advisor_flow",
        messages: [{
          role: "user",
          content: "Produce the advisor_flow JSON for this finding.",
        }],
        context: { securityBrief: factCard },
        max_tokens: 1600,
      },
    });
    const advisor = parseAdvisor(result.content);
    return NextResponse.json({
      factCard,
      advisor,
      narration: null,
      findingId: factCard.source === "finding" ? factCard.id : null,
      reference: factCard.cveIds[0] ?? factCard.id,
      provider: result.provider,
      model: result.model,
    });
  } catch (e) {
    // Narration is best-effort — degrade to the grounded fact card. Log the
    // reason so a silent "narration unavailable" is diagnosable (e.g. no API
    // credits, bad key, model id, network).
    console.error("[assistant/explain] LLM advisor flow failed:", e instanceof Error ? e.message : e);
    return NextResponse.json({
      factCard,
      advisor: null,
      narration: null,
      findingId: factCard.source === "finding" ? factCard.id : null,
      reference: factCard.cveIds[0] ?? factCard.id,
    });
  }
}
