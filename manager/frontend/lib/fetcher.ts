/**
 * Typed fetch for React Query queryFns.
 *
 * Browser authentication is carried by HttpOnly, same-site cookies. On a 401,
 * the client asks the BFF to rotate the session once and retries the request.
 */
export class ApiError extends Error {
  status: number;
  detail?: string;
  constructor(message: string, status: number, detail?: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

/** Clear auth state and go to login. */
export function clearAuth(redirect = true): void {
  if (typeof window === "undefined") return;
  // Remove credentials created by older builds. Current session cookies are
  // HttpOnly and are cleared by /api/auth/logout.
  localStorage.removeItem("vedha_token");
  localStorage.removeItem("vedha_refresh_token");
  sessionStorage.removeItem("vedha_token");
  if (redirect) window.location.href = "/login";
}

export async function fetchJson<T = unknown>(url: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init?.headers as Record<string, string> | undefined),
  };

  let res: Response;
  try {
    res = await fetch(url, { ...init, headers, credentials: "same-origin" });
  } catch {
    throw new ApiError("Can't reach the server. Check your connection and try again.", 0);
  }

  if (res.status === 401 || res.status === 403) {
    // Try once with the path-scoped HttpOnly refresh cookie before giving up.
    if (res.status === 401) {
      try {
        const rr = await fetch("/api/auth/login", {
          method: "PUT",
          credentials: "same-origin",
        });
        if (rr.ok) {
          const retry = await fetch(url, { ...init, headers, credentials: "same-origin" });
          if (retry.ok) {
            if (retry.status === 204) return undefined as T;
            return (await retry.json()) as T;
          }
        }
      } catch { /* fall through to error */ }
    }
    await fetch("/api/auth/logout", {
      method: "POST",
      credentials: "same-origin",
      keepalive: true,
    }).catch(() => {});
    clearAuth(true);
    throw new ApiError("Your session has expired. Please sign in again.", res.status);
  }

  if (!res.ok) {
    let detail: string | undefined;
    try {
      const body = await res.json();
      detail = body?.detail || body?.error || body?.message;
    } catch { /* non-JSON */ }
    throw new ApiError(detail || `Request failed (${res.status}).`, res.status, detail);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export function isUnauthorized(error: unknown): boolean {
  return error instanceof ApiError && (error.status === 401 || error.status === 403);
}

export function errorMessage(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error) return error.message;
  return "Something went wrong.";
}
