/**
 * Typed fetch for React Query queryFns.
 *
 * Auto-injects the stored FastAPI JWT as Authorization: Bearer so callers
 * never have to think about auth headers. On 401/403 the token is cleared and
 * the browser is redirected to /login.
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

/** Read the stored FastAPI JWT from localStorage (client-side only). */
export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return (
    localStorage.getItem("vedha_token") ||
    sessionStorage.getItem("vedha_token") ||
    null
  );
}

/** Persist both storage slots + cookie so middleware can read it. */
export function storeToken(token: string, refreshToken?: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem("vedha_token", token);
  sessionStorage.setItem("vedha_token", token);
  // Cookie lets the Edge middleware check auth without JS
  document.cookie = `vedha_token=${token}; path=/; SameSite=Lax; max-age=${7 * 24 * 3600}`;
  if (refreshToken) {
    localStorage.setItem("vedha_refresh_token", refreshToken);
  }
}

/** Clear auth state and go to login. */
export function clearAuth(redirect = true): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem("vedha_token");
  localStorage.removeItem("vedha_refresh_token");
  sessionStorage.removeItem("vedha_token");
  document.cookie = "vedha_token=; path=/; max-age=0";
  if (redirect) window.location.href = "/login";
}

export async function fetchJson<T = unknown>(url: string, init?: RequestInit): Promise<T> {
  const token = getStoredToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init?.headers as Record<string, string> | undefined),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let res: Response;
  try {
    res = await fetch(url, { ...init, headers });
  } catch {
    throw new ApiError("Can't reach the server. Check your connection and try again.", 0);
  }

  if (res.status === 401 || res.status === 403) {
    // Try once with refresh token before giving up
    const refreshToken = typeof window !== "undefined"
      ? localStorage.getItem("vedha_refresh_token")
      : null;
    if (refreshToken && res.status === 401) {
      try {
        const rr = await fetch("/api/auth/login", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refreshToken }),
        });
        if (rr.ok) {
          const rd = await rr.json() as { token: string; refreshToken?: string };
          storeToken(rd.token, rd.refreshToken);
          // Retry the original request with the new token
          const retryHeaders = { ...headers, Authorization: `Bearer ${rd.token}` };
          const retry = await fetch(url, { ...init, headers: retryHeaders });
          if (retry.ok) {
            if (retry.status === 204) return undefined as T;
            return (await retry.json()) as T;
          }
        }
      } catch { /* fall through to error */ }
    }
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
