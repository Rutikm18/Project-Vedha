/**
 * Integration upsert/remove — BFF proxy.
 *   PUT    → /integrations/{kind}   (add or update; secret encrypted server-side)
 *   DELETE → /integrations/{kind}
 */
import { NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "../../../../lib/backend";

export async function PUT(req: Request, { params }: { params: Promise<{ kind: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { kind } = await params;
  const body = await req.json().catch(() => ({}));
  try {
    return NextResponse.json(await backend(`/integrations/${kind}`, { token, method: "PUT", body }));
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 500;
    return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status });
  }
}

export async function DELETE(req: Request, { params }: { params: Promise<{ kind: string }> }) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  const { kind } = await params;
  try {
    await backend(`/integrations/${kind}`, { token, method: "DELETE" });
    return new NextResponse(null, { status: 204 });
  } catch (e) {
    const status = e instanceof BackendError ? e.status : 500;
    return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status });
  }
}
