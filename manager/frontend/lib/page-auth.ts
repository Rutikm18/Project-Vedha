export type PageAuthSurface = "public" | "operator" | "portal";

const PUBLIC_PATHS = new Set(["/login", "/portal/login"]);
const PUBLIC_PREFIXES = ["/_next/", "/favicon", "/api/"];

/** Resolve which browser session owns a page before the request reaches React. */
export function pageAuthSurface(pathname: string): PageAuthSurface {
  if (PUBLIC_PATHS.has(pathname) || PUBLIC_PREFIXES.some((prefix) => pathname.startsWith(prefix))) {
    return "public";
  }
  if (pathname === "/portal" || pathname.startsWith("/portal/")) return "portal";
  return "operator";
}
