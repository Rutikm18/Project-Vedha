import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../../lib/backend";

// Report generation and all model execution are Manager-owned.
export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const token = bearerFrom(request);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  const body = await request.json().catch(() => ({})) as {
    sections?: string[];
    maxFindings?: number;
    max_findings?: number;
  };
  const sections = Array.isArray(body.sections) ? body.sections : [];

  try {
    const result = await backend<{ job_id: string; status: string }>(
      `/engagements/${id}/ai-report/generate`,
      {
        method: "POST",
        token,
        body: {
          include_technical: sections.length === 0 || sections.includes("technical_finding"),
          include_remediation: sections.length === 0 || sections.includes("remediation"),
          max_findings: body.max_findings ?? body.maxFindings ?? 10,
        },
      },
    );
    return NextResponse.json({ ...result, jobId: result.job_id }, { status: 202 });
  } catch (error) {
    const code = error instanceof BackendError ? error.status : 502;
    return NextResponse.json({ error: error instanceof Error ? error.message : "Report generation failed" }, { status: code });
  }
}
