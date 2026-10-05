/**
 * Role claim of a FastAPI access token, read without verifying the signature.
 * FastAPI signed it a moment ago and enforces it on every call; the BFF only
 * peeks to keep the two sign-in doors apart (operators vs. portal customers).
 */
import jwt from "jsonwebtoken";

export function tokenRole(accessToken: string): string | null {
  const claims = jwt.decode(accessToken) as { role?: unknown } | null;
  return claims && typeof claims.role === "string" ? claims.role : null;
}

/** True only if the role claim is exactly "client" (a customer portal account). */
export function isClientToken(accessToken: string): boolean {
  return tokenRole(accessToken) === "client";
}
