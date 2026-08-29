/**
 * Raw scanner facts — BFF proxy to FastAPI.
 *   GET → /engagements/{id}/raw-facts
 * Surfaces the raw ScanResult facts exactly as the vedha-agent/main_scripts
 * submitted them (grouped by scanner), so an operator can inspect what each
 * scanner actually collected per lifecycle phase. Operator-gated on the backend.
 * Forwards job_id / scanner / limit / max_facts filters straight through.
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
  const url = new URL(req.url);
  const query: Record<string, string> = {};
  for (const k of ["job_id", "scanner", "limit", "max_facts"]) {
    const v = url.searchParams.get(k);
    if (v) query[k] = v;
  }
  try {
    const data = await backend<unknown>(`/engagements/${id}/raw-facts`, { token, query });
    return NextResponse.json(data);
  } catch (e) {
    return fail(e);
  }
}
