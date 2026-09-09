/** Method-complete BFF transport for the engagement-scoped customer portal. */
import { NextRequest, NextResponse } from "next/server";
import { backendResponse, cookieFrom } from "../../../../lib/backend";

export const dynamic = "force-dynamic";

type RouteContext = { params: Promise<{ path: string[] }> };

const REQUEST_HEADERS = ["accept", "content-type", "idempotency-key", "if-match", "x-correlation-id"] as const;
const RESPONSE_HEADERS = ["content-type", "content-disposition", "etag", "retry-after", "x-correlation-id"] as const;

function portalToken(req: Request): string | null {
  const authorization = req.headers.get("authorization") ?? "";
  if (authorization.startsWith("Bearer ")) return authorization.slice(7);
  return cookieFrom(req, "vedha_portal_token");
}

function pickHeaders(source: Headers, names: readonly string[]): Headers {
  const result = new Headers();
  for (const name of names) {
    const value = source.get(name);
    if (value) result.set(name, value);
  }
  return result;
}

async function proxyPortal(req: NextRequest, method: string, context: RouteContext) {
  const token = portalToken(req);
  if (!token) return NextResponse.json({ error: "Not authenticated" }, { status: 401 });

  const { path = [] } = await context.params;
  const safePath = path.map((segment) => encodeURIComponent(segment)).join("/");
  const query = new URL(req.url).search;
  const hasBody = method !== "GET" && method !== "HEAD" && req.body !== null;

  try {
    const upstream = await backendResponse(`/portal/${safePath}${query}`, {
      method,
      token,
      headers: pickHeaders(req.headers, REQUEST_HEADERS),
      rawBody: hasBody ? req.body : undefined,
    });
    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: pickHeaders(upstream.headers, RESPONSE_HEADERS),
    });
  } catch {
    return NextResponse.json({ error: "The portal service is temporarily unavailable" }, { status: 502 });
  }
}

export function GET(req: NextRequest, context: RouteContext) { return proxyPortal(req, "GET", context); }
export function HEAD(req: NextRequest, context: RouteContext) { return proxyPortal(req, "HEAD", context); }
export function POST(req: NextRequest, context: RouteContext) { return proxyPortal(req, "POST", context); }
export function PUT(req: NextRequest, context: RouteContext) { return proxyPortal(req, "PUT", context); }
export function PATCH(req: NextRequest, context: RouteContext) { return proxyPortal(req, "PATCH", context); }
export function DELETE(req: NextRequest, context: RouteContext) { return proxyPortal(req, "DELETE", context); }
