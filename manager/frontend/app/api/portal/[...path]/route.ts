/**
 * Catch-all BFF proxy for the customer portal. Forwards /api/portal/<path> to the
 * FastAPI /portal/<path> using the vedha_portal_token cookie. FastAPI enforces
 * client-role + engagement scoping, so this layer only carries the token through.
 *
 * (login / logout are their own more-specific routes and take precedence.)
 */
import { NextRequest, NextResponse } from "next/server";
import { backend, BackendError, cookieFrom } from "../../../../lib/backend";

function portalToken(req: Request): string | null {
  const h = req.headers.get("authorization") ?? "";
  if (h.startsWith("Bearer ")) return h.slice(7);
  return cookieFrom(req, "vedha_portal_token");
}

async function proxy(req: NextRequest, method: "GET" | "POST", path: string[]) {
  const token = portalToken(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });

  const sub = "/" + (path ?? []).join("/");
  const query: Record<string, string> = {};
  new URL(req.url).searchParams.forEach((v, k) => (query[k] = v));

  let body: unknown = undefined;
  if (method === "POST") {
    try {
      body = await req.json();
    } catch {
      body = {};
    }
  }

  try {
    const data = await backend(`/portal${sub}`, { method, token, body, query });
    return NextResponse.json(data ?? null);
  } catch (e) {
    if (e instanceof BackendError) {
      return NextResponse.json({ error: e.message }, { status: e.status });
    }
    return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status: 500 });
  }
}

export async function GET(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  return proxy(req, "GET", path);
}

export async function POST(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  return proxy(req, "POST", path);
}
