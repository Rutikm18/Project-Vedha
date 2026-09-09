/**
 * Server-side client for the VEDHA Python backend (FastAPI).
 *
 * This is the integration seam: the Next.js `app/api/*` route handlers act as a
 * BFF (backend-for-frontend) and call FastAPI through this module, forwarding the
 * caller's JWT. The browser never talks to FastAPI directly (no CORS), and the
 * FastAPI JWT is the single source of auth.
 *
 * Configure with BACKEND_INTERNAL_URL (e.g. http://api:8000 inside compose).
 */
const BASE = (process.env.BACKEND_INTERNAL_URL ?? "http://localhost:18080").replace(/\/$/, "");

export class BackendError extends Error {
  status: number;
  /** Seconds to wait before retrying, parsed from the backend's Retry-After
   *  header (set on 429/503). Undefined when the backend didn't send one. */
  retryAfter?: number;
  constructor(status: number, message: string, retryAfter?: number) {
    super(message);
    this.status = status;
    this.retryAfter = retryAfter;
  }
}

export interface BackendOpts {
  method?: string;
  token?: string | null;
  body?: unknown;
  rawBody?: BodyInit | null;
  headers?: HeadersInit;
  query?: Record<string, string | number | boolean | undefined>;
}

/** Low-level transport used by method-complete BFF routes. */
export async function backendResponse(path: string, opts: BackendOpts = {}): Promise<Response> {
  const url = new URL(BASE + path);
  if (opts.query) {
    for (const [k, v] of Object.entries(opts.query)) {
      if (v !== undefined) url.searchParams.set(k, String(v));
    }
  }
  const headers = new Headers(opts.headers);
  if (opts.token) headers.set("Authorization", `Bearer ${opts.token}`);

  let requestBody: BodyInit | undefined;
  if (opts.rawBody !== undefined && opts.rawBody !== null) {
    requestBody = opts.rawBody;
  } else if (opts.body !== undefined) {
    headers.set("Content-Type", "application/json");
    requestBody = JSON.stringify(opts.body);
  }

  const init: RequestInit & { duplex?: "half" } = {
    method: opts.method ?? "GET",
    headers,
    body: requestBody,
    cache: "no-store",
  };
  if (requestBody instanceof ReadableStream) init.duplex = "half";
  return fetch(url.toString(), init);
}

/** Call a FastAPI endpoint, forwarding the operator's bearer token. */
export async function backend<T = unknown>(path: string, opts: BackendOpts = {}): Promise<T> {
  const res = await backendResponse(path, opts);

  const text = await res.text();
  const data = text ? safeJson(text) : null;
  if (!res.ok) {
    const detail = (data && (data.detail ?? data.error)) || res.statusText;
    const retryHeader = res.headers.get("retry-after");
    const retryAfter = retryHeader && /^\d+$/.test(retryHeader.trim())
      ? Number(retryHeader.trim())
      : undefined;
    throw new BackendError(
      res.status,
      typeof detail === "string" ? detail : JSON.stringify(detail),
      retryAfter,
    );
  }
  return data as T;
}

function safeJson(t: string): any {
  try {
    return JSON.parse(t);
  } catch {
    return { raw: t };
  }
}

/** Read one cookie without depending on framework-specific request types. */
export function cookieFrom(req: Request, name: string): string | null {
  const cookie = req.headers.get("cookie");
  if (!cookie) return null;
  const prefix = `${name}=`;
  const value = cookie
    .split(";")
    .map((part) => part.trim())
    .find((part) => part.startsWith(prefix))
    ?.slice(prefix.length);
  if (!value) return null;
  try {
    return decodeURIComponent(value);
  } catch {
    return null;
  }
}

/**
 * Extract the operator token. Authorization remains supported for CLI/API
 * clients; browser sessions use an HttpOnly cookie so JavaScript cannot read it.
 */
export function bearerFrom(req: Request): string | null {
  const h = req.headers.get("authorization") ?? "";
  if (h.startsWith("Bearer ")) return h.slice(7);
  return cookieFrom(req, "vedha_token");
}
