import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../lib/backend";
import { detectFindingId, type FactCardVM } from "../../../lib/assistant";
import { resolveSecurityReference, SecurityContextError } from "../../../lib/security-context";

interface AiMessage {
  role: "user" | "assistant";
  content: string;
}

interface ManagerAiResponse {
  content: string;
  provider: string;
  model: string;
  privacy: "local" | "cloud";
}

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const MAX_CONVERSATION_CHARS = 24_000;

function validMessages(value: unknown): value is AiMessage[] {
  return Array.isArray(value)
    && value.length > 0
    && value.length <= 24
    && value.reduce((total, message) => {
      if (!message || typeof message !== "object") return MAX_CONVERSATION_CHARS + 1;
      const content = (message as Record<string, unknown>).content;
      return total + (typeof content === "string" ? content.length : MAX_CONVERSATION_CHARS + 1);
    }, 0) <= MAX_CONVERSATION_CHARS
    && value.every((message) => {
      if (!message || typeof message !== "object") return false;
      const candidate = message as Record<string, unknown>;
      return (candidate.role === "user" || candidate.role === "assistant")
        && typeof candidate.content === "string"
        && candidate.content.length > 0
        && candidate.content.length <= 6_000;
    });
}

function evidenceText(value: unknown, maxLength: number): string {
  return String(value ?? "")
    .replace(/[\u0000-\u001f\u007f]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, maxLength);
}

export async function POST(req: Request) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });

  const body = await req.json().catch(() => null) as {
    messages?: unknown;
    engagementId?: string;
    provider?: "ollama" | "openrouter" | "anthropic";
    model?: string;
  } | null;
  if (!body || !validMessages(body.messages)) {
    return NextResponse.json({
      error: "messages[] must contain 1-24 messages, at most 6,000 characters each and 24,000 characters total",
    }, { status: 400 });
  }
  if (body.engagementId && !UUID.test(body.engagementId)) {
    return NextResponse.json({ error: "engagementId must be a valid UUID" }, { status: 400 });
  }

  try {
    let factCard: FactCardVM | undefined;
    const context: Record<string, unknown> = {};
    const latestUser = [...body.messages].reverse().find((message) => message.role === "user");
    const reference = latestUser ? detectFindingId(latestUser.content) : null;
    if (reference) {
      factCard = (await resolveSecurityReference({ reference, token })).factCard;
      context.securityBrief = factCard;
    }
    if (body.engagementId) {
      const data = await backend<{ items?: Array<Record<string, unknown>> } | Array<Record<string, unknown>>>(
        "/findings",
        {
          token,
          query: { engagement_id: body.engagementId, page: 1, page_size: 20 },
        },
      );
      const findings = Array.isArray(data) ? data : data.items ?? [];
      if (findings.length > 0) {
        const counts = findings.reduce<Record<string, number>>((acc, finding) => {
          const severity = evidenceText(finding.severity, 20) || "UNKNOWN";
          acc[severity] = (acc[severity] ?? 0) + 1;
          return acc;
        }, {});
        const evidence = findings.slice(0, 8).map((finding) => ({
          severity: evidenceText(finding.severity, 20) || "UNKNOWN",
          affectedHost: evidenceText(finding.affected_host, 180) || "unknown asset",
          title: evidenceText(finding.title, 240) || "Untitled",
        }));
        context.recordedEngagementEvidence = {
          findingCounts: counts,
          prioritizedFindings: evidence,
          evidenceWindow: "First 20 findings returned by Manager",
        };
      } else {
        context.recordedEngagementEvidence = {
          findingCounts: {},
          prioritizedFindings: [],
          limitation: "No recorded findings were returned for the selected engagement.",
        };
      }
    }

    const result = await backend<ManagerAiResponse>("/ai/generate", {
      method: "POST",
      token,
      body: {
        task: "advisor",
        messages: body.messages,
        context,
        provider: body.provider,
        model: body.model,
        max_tokens: 900,
      },
    });
    return NextResponse.json({
      content: result.content,
      factCard,
      provider: result.provider,
      model: result.model,
    });
  } catch (error) {
    const status = error instanceof BackendError || error instanceof SecurityContextError
      ? error.status
      : 502;
    const message = error instanceof Error ? error.message : "AI request failed";
    console.error("[brain] generation failed:", message);
    return NextResponse.json({ error: message }, { status });
  }
}
