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
/** Read per call (not frozen at import) so a test or a restarted process sees the
 *  current value. */
function baseUrl(): string {
  return (process.env.BACKEND_INTERNAL_URL ?? "http://localhost:18080").replace(/\/$/, "");
}

/**
 * How long a read (GET/HEAD) waits for FastAPI to START answering. Without it
 * Node waits 300 s and then reports only "fetch failed". Only the wait for the
 * response headers is bounded, never the body, so a large download streams for as
 * long as it needs. Writes are not bounded here: some (AI report refinement)
 * legitimately wait on a model for minutes. BACKEND_READ_TIMEOUT_MS overrides;
 * 0 turns the bound off.
 */
const DEFAULT_READ_TIMEOUT_MS = 60_000;

function readTimeoutMs(): number {
  const raw = process.env.BACKEND_READ_TIMEOUT_MS;
  const n = raw === undefined || raw.trim() === "" ? NaN : Number(raw);
  return Number.isFinite(n) && n >= 0 ? n : DEFAULT_READ_TIMEOUT_MS;
}

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
  /** Override the read timeout for this call (ms); 0 = no bound. */
  timeoutMs?: number;
}

// Node's fetch reports every transport failure as TypeError("fetch failed") and
// hides the reason in `cause`. These are the reasons, grouped by what an operator
// should do about them.
const RESET_CODES = new Set(["ECONNRESET", "EPIPE", "UND_ERR_SOCKET", "UND_ERR_CLOSED"]);
const TIMEOUT_CODES = new Set([
  "ETIMEDOUT", "UND_ERR_CONNECT_TIMEOUT", "UND_ERR_HEADERS_TIMEOUT", "UND_ERR_BODY_TIMEOUT",
]);
const DNS_CODES = new Set(["ENOTFOUND", "EAI_AGAIN"]);

/** The low-level code behind a fetch failure ("ECONNREFUSED", "UND_ERR_SOCKET"…). */
export function networkErrorCode(err: unknown): string | undefined {
  let e: any = err;
  for (let depth = 0; e && depth < 4; depth++) {
    if (typeof e.code === "string") return e.code;
    if (Array.isArray(e.errors) && typeof e.errors[0]?.code === "string") return e.errors[0].code;
    e = e.cause;
  }
  return undefined;
}

/**
 * Turn a transport failure into a BackendError an operator can act on: the right
 * HTTP status (503 down, 502 dropped, 504 too slow) and a sentence that names the
 * cause, instead of a 500 that says only "fetch failed". The internal address is
 * deliberately left out of the message (it reaches the browser); the server log
 * carries the detail.
 */
export function backendUnreachable(err: unknown, opts: { timedOut?: boolean; timeoutMs?: number } = {}): BackendError {
  const code = networkErrorCode(err);
  if (opts.timedOut || (code && TIMEOUT_CODES.has(code))) {
    const ms = opts.timedOut ? opts.timeoutMs ?? 0 : 0;
    const secs = ms >= 1000 ? ` within ${Math.round(ms / 1000)} s` : ms > 0 ? ` within ${ms} ms` : "";
    return new BackendError(504,
      `Manager API did not answer${secs}${code ? ` (${code})` : ""}: it is overloaded or a database query is stuck.`, 5);
  }
  if (code === "ECONNREFUSED") {
    return new BackendError(503,
      "Manager API refused the connection (ECONNREFUSED): it is down or restarting.", 5);
  }
  if (code && RESET_CODES.has(code)) {
    return new BackendError(502,
      `Manager API dropped the connection mid-request (${code}): an API worker may have crashed or been restarted.`, 5);
  }
  if (code && DNS_CODES.has(code)) {
    return new BackendError(503,
      `Manager API address could not be resolved (${code}): check BACKEND_INTERNAL_URL.`, 5);
  }
  const detail = code ?? ((err as Error)?.message || "unknown error");
  return new BackendError(502, `Manager API unreachable (${detail}).`, 5);
}

function logUnreachable(method: string, path: string, attempt: number, err: unknown, mapped: BackendError) {
  // One structured line per failure, for `docker compose logs frontend`. No query
  // string and no token.
  console.error(JSON.stringify({
    event: "backend.unreachable", method, path: path.split("?")[0], attempt,
    code: networkErrorCode(err) ?? null, status: mapped.status, message: mapped.message,
  }));
}

/** Low-level transport used by method-complete BFF routes. */
export async function backendResponse(path: string, opts: BackendOpts = {}): Promise<Response> {
  const url = new URL(baseUrl() + path);
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

  const method = (init.method ?? "GET").toUpperCase();
  const isRead = method === "GET" || method === "HEAD";
  const timeoutMs = opts.timeoutMs ?? (isRead ? readTimeoutMs() : 0);
  // A read is retried once when the connection was dropped: it is safe to repeat,
  // and the usual cause (a pooled keep-alive socket the server had just closed, or
  // a worker that was restarted) is gone on the second try.
  const attempts = isRead ? 2 : 1;
  for (let attempt = 1; ; attempt++) {
    const controller = new AbortController();
    let timedOut = false;
    const timer = timeoutMs > 0
      ? setTimeout(() => { timedOut = true; controller.abort(); }, timeoutMs)
      : undefined;
    try {
      // The timer is cleared once headers arrive, so it never cuts a streaming body.
      return await fetch(url.toString(), { ...init, signal: controller.signal });
    } catch (err) {
      const mapped = backendUnreachable(err, { timedOut, timeoutMs });
      logUnreachable(method, path, attempt, err, mapped);
      const code = networkErrorCode(err);
      if (attempt < attempts && !timedOut && code !== undefined && RESET_CODES.has(code)) continue;
      throw mapped;
    } finally {
      if (timer) clearTimeout(timer);
    }
  }
}

/** Call a FastAPI endpoint, forwarding the operator's bearer token. */
export async function backend<T = unknown>(path: string, opts: BackendOpts = {}): Promise<T> {
  const res = await backendResponse(path, opts);

  let text: string;
  try {
    text = await res.text();
  } catch (err) {
    // The worker died after sending headers (the body was cut off).
    const mapped = backendUnreachable(err);
    logUnreachable((opts.method ?? "GET").toUpperCase(), path, 1, err, mapped);
    throw mapped;
  }
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

/**
 * Forward the browser's X-Forwarded-For (set by the Caddy edge) on a
 * server-to-server call. Without it FastAPI sees only this container's IP, so a
 * per-IP limit becomes ONE bucket shared by every user. The backend believes the
 * header only because this BFF is a trusted proxy on the private network.
 */
export function forwardedFor(req: Request): HeadersInit {
  const xff = req.headers.get("x-forwarded-for");
  return xff ? { "X-Forwarded-For": xff } : {};
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
