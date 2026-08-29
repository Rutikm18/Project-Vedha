/**
 * VA Campaigns live view — BFF proxy to FastAPI.
 *   GET → /engagements/{id}/campaign-progress
 * Returns per-probe jobs (status + safe raw-result summary), the detection
 * pipeline phases (Scanning → Aggregating → Detection → Correlation →
 * Prioritization → Remediation) and the findings with remediation guidance.
 */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../lib/backend";

function fail(e: unknown) {
  const status = e instanceof BackendError ? e.status : 500;
  return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status });
}

export async function GET(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  try {
    const data = await backend<unknown>(`/engagements/${id}/campaign-progress`, { token });
    return NextResponse.json(data);
  } catch (e) {
    return fail(e);
  }
}
