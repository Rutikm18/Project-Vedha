/**
 * Two-step sign-in, shared by the operator and portal login routes.
 *
 * The login route takes one of four bodies:
 *   { email, password }              → session, or a code step is needed
 *   { step: "verify", code }         → app code or recovery code finishes sign-in
 *   { step: "enroll_setup" }         → the organisation requires MFA: new secret + QR URI
 *   { step: "enroll_enable", code }  → first code turns MFA on and signs in
 *
 * Between steps the backend's challenge token lives in an httpOnly cookie scoped
 * to the login route, so page scripts never see it. It lasts five minutes, the
 * same as the token itself.
 */
import type { NextResponse } from "next/server";
import { backend, BackendError, cookieFrom } from "./backend";

export interface SessionPair { access_token: string; refresh_token: string }

export type LoginBody = {
  email?: string;
  password?: string;
  step?: "verify" | "enroll_setup" | "enroll_enable";
  code?: string;
};

export type LoginOutcome =
  | { kind: "session"; tokens: SessionPair; recoveryCodes?: string[] }
  | { kind: "challenge"; mfa: "verify" | "enroll"; token: string }
  | { kind: "setup"; secret: string; otpauthUri: string; account: string };

const CHALLENGE_SECONDS = 5 * 60;

type BackendLogin = Partial<SessionPair> & {
  mfa_required?: boolean;
  mfa_enrollment_required?: boolean;
  mfa_token?: string;
  recovery_codes?: string[];
};

function asSession(d: BackendLogin): LoginOutcome {
  if (!d.access_token || !d.refresh_token) throw new BackendError(502, "Sign-in returned no session");
  return { kind: "session", tokens: { access_token: d.access_token, refresh_token: d.refresh_token }, recoveryCodes: d.recovery_codes };
}

/** Thrown for a code step with no (or an expired) challenge cookie. */
export const MFA_EXPIRED = "mfa_expired";

export async function runLoginStep(
  req: Request, body: LoginBody, challengeCookie: string, headers: HeadersInit,
): Promise<LoginOutcome> {
  if (body.step) {
    const token = cookieFrom(req, challengeCookie);
    if (!token) throw new BackendError(401, MFA_EXPIRED);
    if (body.step === "enroll_setup") {
      const d = await backend<{ secret: string; otpauth_uri: string; account: string }>(
        "/auth/mfa/enroll/setup", { method: "POST", body: { mfa_token: token }, headers });
      return { kind: "setup", secret: d.secret, otpauthUri: d.otpauth_uri, account: d.account };
    }
    const code = String(body.code ?? "").trim();
    if (!code) throw new BackendError(400, "Enter the code");
    const path = body.step === "verify" ? "/auth/mfa/verify" : "/auth/mfa/enroll/enable";
    return asSession(await backend<BackendLogin>(path, { method: "POST", body: { mfa_token: token, code }, headers }));
  }

  const d = await backend<BackendLogin>("/auth/login", {
    method: "POST", body: { email: body.email, password: body.password }, headers,
  });
  if ((d.mfa_required || d.mfa_enrollment_required) && d.mfa_token) {
    return { kind: "challenge", mfa: d.mfa_required ? "verify" : "enroll", token: d.mfa_token };
  }
  return asSession(d);
}

export function setChallengeCookie(res: NextResponse, name: string, path: string, token: string, secure: boolean) {
  res.cookies.set(name, token, { httpOnly: true, secure, sameSite: "strict", path, maxAge: CHALLENGE_SECONDS });
}

export function clearChallengeCookie(res: NextResponse, name: string, path: string, secure: boolean) {
  res.cookies.set(name, "", { httpOnly: true, secure, sameSite: "strict", path, maxAge: 0 });
}

/** Stable codes the sign-in pages branch on (never string-matching messages). */
export function loginErrorCode(e: BackendError, step: LoginBody["step"]): string {
  if (e.message === MFA_EXPIRED) return MFA_EXPIRED;
  if (e.status === 429) return "rate_limited";
  if (e.status >= 500) return "backend_unavailable";
  if (step) {
    // A spent, expired or over-used challenge reads the same as a wrong code at
    // the backend; the page offers "start again" for both.
    if (e.status === 401) return "invalid_code";
    if (e.status === 409) return MFA_EXPIRED;
    if (e.status === 400) return "invalid_code";
  }
  if (e.status === 401) return "invalid_credentials";
  return "login_failed";
}

export function readLoginBody(raw: unknown): LoginBody | null {
  if (!raw || typeof raw !== "object") return null;
  const b = raw as Record<string, unknown>;
  const step = b.step;
  if (step !== undefined && step !== "verify" && step !== "enroll_setup" && step !== "enroll_enable") return null;
  return {
    email: typeof b.email === "string" ? b.email : undefined,
    password: typeof b.password === "string" ? b.password : undefined,
    step: step as LoginBody["step"],
    code: typeof b.code === "string" ? b.code : undefined,
  };
}
