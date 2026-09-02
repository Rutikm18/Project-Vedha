/**
 * Reopen an auto/manually-resolved finding — BFF proxy to FastAPI.
 *   POST → /findings/{id}/reopen  (409 unless the finding is `remediated`)
 *
 * Native route-handler signature (Next 16 validates dynamic-segment context).
 */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../lib/backend";
import { toUiFinding } from "../../../../../lib/adapters";

function fail(e: unknown) {
  const status = e instanceof BackendError ? e.status : 500;
  return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status });
}

export async function POST(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  try {
    const body = await req.json().catch(() => undefined);
    const updated = await backend<unknown>(`/findings/${id}/reopen`, {
      token,
      method: "POST",
      body,
    });
    return NextResponse.json(toUiFinding(updated));
  } catch (e) {
    return fail(e);
  }
}
