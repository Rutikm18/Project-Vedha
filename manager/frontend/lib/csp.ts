/**
 * Script Content-Security-Policy, built per request with a fresh nonce.
 *
 * `script-src` is the directive that stops injected markup from running code:
 * only scripts carrying this request's nonce (and the scripts those load, via
 * 'strict-dynamic') execute. The directives in STATIC_DIRECTIVES mirror the
 * static CSP in next.config.mjs (which still covers responses the proxy does
 * not run on, such as /_next/static), so a page gets the full policy.
 *
 * We deliberately do NOT add `upgrade-insecure-requests` (plain-HTTP test and
 * on-prem deployments exist) or `default-src` (it would also gate images, fonts
 * and fetches the app depends on).
 */

/** A fresh, unguessable value for each request. */
export function makeNonce(): string {
  return Buffer.from(crypto.randomUUID()).toString("base64");
}

/** Keep in sync with the static CSP in next.config.mjs. */
export const STATIC_DIRECTIVES =
  "base-uri 'self'; form-action 'self'; frame-ancestors 'none'; object-src 'none'";

export function buildScriptCsp(nonce: string, isDev: boolean): string {
  // React reconstructs server stacks with eval() in development only.
  const dev = isDev ? " 'unsafe-eval'" : "";
  return `${STATIC_DIRECTIVES}; script-src 'self' 'nonce-${nonce}' 'strict-dynamic'${dev}`;
}
