import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../../lib/backend";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const token = bearerFrom(request);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  try {
    const result = await backend<{ count: number; sections: unknown[] }>(
      `/engagements/${id}/ai-report/draft`,
      { token },
    );
    return NextResponse.json({
      ...result,
      drafts: result.sections,
      all: result.sections,
      total: result.count,
      pendingReview: result.count,
    });
  } catch (error) {
    const code = error instanceof BackendError ? error.status : 502;
    return NextResponse.json({ error: error instanceof Error ? error.message : "Draft unavailable" }, { status: code });
  }
}
