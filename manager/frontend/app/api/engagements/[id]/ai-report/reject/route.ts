import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../../lib/backend";

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const token = bearerFrom(request);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  const body = await request.json().catch(() => ({})) as {
    outputId?: string;
    output_ids?: string[];
    feedback?: string;
    regenerate?: boolean;
  };
  if (!body.feedback?.trim()) {
    return NextResponse.json({ error: "feedback is required" }, { status: 400 });
  }
  const outputIds = body.output_ids ?? (body.outputId ? [body.outputId] : undefined);
  try {
    const result = await backend(`/engagements/${id}/ai-report/reject`, {
      method: "POST",
      token,
      body: { output_ids: outputIds, feedback: body.feedback.trim(), regenerate: body.regenerate ?? true },
    });
    return NextResponse.json(result);
  } catch (error) {
    const code = error instanceof BackendError ? error.status : 502;
    return NextResponse.json({ error: error instanceof Error ? error.message : "Rejection failed" }, { status: code });
  }
}
