/**
 * Operator BFF proxy for customer-access management. Forwards
 * /api/engagements/{id}/customer-access/<path> to FastAPI /engagements/{id}/<path>
 * (client-user, entitlement, entitlement/adjust, assign-agent, scan-requests,
 * scan-requests/{rid}/approve|reject)
 * using the operator's vedha_token. FastAPI enforces operator RBAC + tenant scope.
 */
import { NextRequest, NextResponse } from "next/server";
import { backend, BackendError, bearerFrom } from "../../../../../../lib/backend";

async function proxy(req: NextRequest, method: "GET" | "POST" | "PATCH" | "PUT", id: string, path: string[]) {
  const token = bearerFrom(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });

  // Encode each segment so a crafted path can't walk out of /engagements/{id}.
  const sub = "/" + (path ?? []).map((s) => encodeURIComponent(s)).join("/");
  let body: unknown = undefined;
  if (method !== "GET") {
    try {
      body = await req.json();
    } catch {
      body = {};
    }
  }
  try {
    const data = await backend(`/engagements/${encodeURIComponent(id)}${sub}`, { method, token, body });
    return NextResponse.json(data ?? null);
  } catch (e) {
    if (e instanceof BackendError) return NextResponse.json({ error: e.message }, { status: e.status });
    return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status: 500 });
  }
}

export async function GET(req: NextRequest, ctx: { params: Promise<{ id: string; path: string[] }> }) {
  const { id, path } = await ctx.params;
  return proxy(req, "GET", id, path);
}
export async function POST(req: NextRequest, ctx: { params: Promise<{ id: string; path: string[] }> }) {
  const { id, path } = await ctx.params;
  return proxy(req, "POST", id, path);
}
export async function PATCH(req: NextRequest, ctx: { params: Promise<{ id: string; path: string[] }> }) {
  const { id, path } = await ctx.params;
  return proxy(req, "PATCH", id, path);
}
export async function PUT(req: NextRequest, ctx: { params: Promise<{ id: string; path: string[] }> }) {
  const { id, path } = await ctx.params;
  return proxy(req, "PUT", id, path);
}
