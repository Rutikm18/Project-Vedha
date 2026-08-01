/**
 * Ask Vedha — grounded follow-up chat about ONE finding.
 *   POST /api/assistant/chat  { findingId, messages[] }  → { content }
 * The finding is re-fetched server-side each call and injected as context, so the
 * model stays grounded and the client can never swap the "finding" out from under it.
 */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../lib/backend";
import { resolveSecurityReference, SecurityContextError } from "../../../../lib/security-context";

interface ManagerAiResponse {
  content: string;
  provider: string;
  model: string;
}
const MAX_MESSAGES = 16;
const MAX_MESSAGE_CHARS = 4_000;
const MAX_TOTAL_CHARS = 16_000;

export async function POST(req: Request) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });

  const body = (await req.json().catch(() => null)) as
    | { findingId?: string; messages?: { role: string; content: string }[] }
    | null;
  if (!body?.findingId || !Array.isArray(body.messages) || body.messages.length === 0) {
    return NextResponse.json({ error: "findingId and messages[] required" }, { status: 400 });
  }
  if (
    body.messages.length > MAX_MESSAGES
    || body.messages.some((message) =>
      !message
      || (message.role !== "user" && message.role !== "assistant")
      || typeof message.content !== "string"
      || message.content.length < 1
      || message.content.length > MAX_MESSAGE_CHARS)
    || body.messages.reduce((total, message) => total + message.content.length, 0) > MAX_TOTAL_CHARS
  ) {
    return NextResponse.json({ error: "Conversation exceeds the safe context limit" }, { status: 400 });
  }

  let factCard;
  try {
    factCard = (await resolveSecurityReference({ reference: body.findingId, token })).factCard;
  } catch (error) {
    const status = error instanceof BackendError || error instanceof SecurityContextError ? error.status : 502;
    return NextResponse.json({ error: error instanceof Error ? error.message : "Security context unavailable" }, { status });
  }

  try {
    const result = await backend<ManagerAiResponse>("/ai/generate", {
      method: "POST",
      token,
      body: {
        task: "security_followup",
        messages: body.messages.map((message) => ({
          role: message.role === "user" ? "user" : "assistant",
          content: message.content,
        })),
        context: { securityBrief: factCard },
        max_tokens: 600,
      },
    });
    return NextResponse.json({
      content: result.content,
      factCard,
      provider: result.provider,
      model: result.model,
    });
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 502;
    return NextResponse.json({ error: e instanceof Error ? e.message : "LLM error" }, { status });
  }
}
