/**
 * Wrapper for BFF route handlers that proxy to the FastAPI backend.
 *
 * Replaces the old `withAuth` (which verified a local OTP JWT + checked an
 * in-memory allowlist) for any route that now delegates to FastAPI. It just
 * extracts the bearer token and hands it to the handler — FastAPI itself
 * enforces auth, tenant isolation, and RBAC, so there's no second auth system.
 */
import { NextRequest, NextResponse } from "next/server";
import { backend, bearerFrom, BackendError } from "./backend";

export interface BackendCtx {
  token: string;
}

export interface VerifiedBackendUser {
  user_id: string;
  tenant_id: string;
  role: string;
  email: string | null;
  auth_type: string;
  pat_id: string | null;
  scopes: string[];
}

export interface VerifiedBackendCtx extends BackendCtx {
  user: VerifiedBackendUser;
}

type Handler<P = Record<string, string>> = (
  req: NextRequest,
  ctx: BackendCtx,
  params?: P,
) => Promise<Response> | Response;

export function withBackend<P = Record<string, string>>(
  handler: Handler<P>,
): (req: NextRequest, extra?: { params?: Promise<P> }) => Promise<Response> {
  return async (req, extra) => {
    const token = bearerFrom(req);
    if (!token) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }
    try {
      const params = extra?.params ? await extra.params : undefined;
      return await handler(req, { token }, params as P);
    } catch (e) {
      if (e instanceof BackendError) {
        return NextResponse.json({ error: e.message }, { status: e.status });
      }
      if (e instanceof SyntaxError) {
        return NextResponse.json({ error: "Request body must contain valid JSON." }, { status: 400 });
      }
      return NextResponse.json({ error: (e as Error)?.message ?? "backend error" }, { status: 500 });
    }
  };
}

type VerifiedHandler<P = Record<string, string>> = (
  req: NextRequest,
  ctx: VerifiedBackendCtx,
  params?: P,
) => Promise<Response> | Response;

const DEFAULT_SCANNER_ROLES = new Set(["admin", "manager", "tester"]);

/**
 * Authenticate local BFF work before it touches the filesystem or starts a
 * scanner process. Unlike proxy-only routes, these handlers cannot rely on a
 * downstream API call to validate the bearer token.
 */
export function withVerifiedBackend<P = Record<string, string>>(
  handler: VerifiedHandler<P>,
  allowedRoles: ReadonlySet<string> = DEFAULT_SCANNER_ROLES,
): (req: NextRequest, extra?: { params?: Promise<P> }) => Promise<Response> {
  return withBackend(async (req, { token }, params) => {
    const user = await backend<VerifiedBackendUser>("/auth/me", { token });
    const role = typeof user?.role === "string" ? user.role.toLowerCase() : "";

    if (
      !user
      || typeof user.user_id !== "string"
      || typeof user.tenant_id !== "string"
      || !allowedRoles.has(role)
    ) {
      return NextResponse.json(
        { error: "Your role is not permitted to run or inspect local scanner jobs." },
        { status: 403 },
      );
    }

    return handler(req, { token, user: { ...user, role } }, params);
  });
}

/**
 * Legacy manager-local scanners are an explicit deployment choice. The
 * canonical product path dispatches a scope-bound job to a Vedha probe.
 */
export function withVerifiedLocalScanner<P = Record<string, string>>(
  handler: VerifiedHandler<P>,
): (req: NextRequest, extra?: { params?: Promise<P> }) => Promise<Response> {
  return withVerifiedBackend(async (req, ctx, params) => {
    if (process.env.ENABLE_LEGACY_LOCAL_SCANNERS !== "true") {
      return NextResponse.json(
        {
          error: "Manager-local scanner routes are disabled. Dispatch this scan to a Vedha probe.",
        },
        { status: 503 },
      );
    }
    return handler(req, ctx, params);
  });
}
