/** Operator-only surfaces where the AI assistant may be mounted. */
export function isAssistantRoute(pathname: string): boolean {
  return pathname !== "/login" && !pathname.startsWith("/portal");
}

export type AssistantAuthState = "checking" | "authenticated" | "anonymous";

/**
 * The assistant is privileged UI: a route match alone is never sufficient.
 * Keep it unmounted until the HttpOnly-cookie session has been verified.
 */
export function canMountAssistant(
  pathname: string,
  authState: AssistantAuthState,
): boolean {
  return authState === "authenticated" && isAssistantRoute(pathname);
}
