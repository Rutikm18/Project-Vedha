import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../../../lib/backend";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string; jobId: string }> },
) {
  const token = bearerFrom(request);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id, jobId } = await params;
  try {
    const result = await backend<{
      status: string;
      progress?: number;
      result?: { sections?: string[]; completed_at?: string };
    }>(`/engagements/${id}/ai-report/status/${jobId}`, { token });
    return NextResponse.json({
      ...result,
      completedSections: result.result?.sections ?? [],
      completedAt: result.result?.completed_at,
    });
  } catch (error) {
    const code = error instanceof BackendError ? error.status : 502;
    return NextResponse.json({ error: error instanceof Error ? error.message : "Report status unavailable" }, { status: code });
  }
}
