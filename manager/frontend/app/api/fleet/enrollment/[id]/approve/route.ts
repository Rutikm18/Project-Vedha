/**
 * One-click probe approval — BFF proxy.
 *   POST → /probe-enrollment/requests/{id}/approve
 * Body: { probe_name?: string | null }. No verification code; the backend
 * auto-fills name (vedha_agent_NN), capabilities, and scope from the device.
 */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../../../lib/backend";

export async function POST(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { id } = await params;
  const body = await req.json().catch(() => ({}));
  try {
    const result = await backend(`/probe-enrollment/requests/${id}/approve`, {
      token, method: "POST", body,
    });
    return NextResponse.json(result);
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 500;
    return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status });
  }
}
