import { fileURLToPath } from "url";
import path from "path";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const frontendRoot = path.resolve(__dirname);

// Single source of truth for the displayed app version.
// 1. Docker/CI build passes it via NEXT_PUBLIC_APP_VERSION (from repo-root VERSION).
// 2. Local `next dev` falls back to reading repo-root VERSION directly.
// 3. Otherwise "dev".
function resolveAppVersion() {
  if (process.env.NEXT_PUBLIC_APP_VERSION) return process.env.NEXT_PUBLIC_APP_VERSION;
  try {
    const v = fs.readFileSync(path.resolve(frontendRoot, "../../VERSION"), "utf8").trim();
    if (v) return v;
  } catch {
    /* VERSION not in build context (e.g. Docker) — rely on the env var above */
  }
  return "dev";
}
const APP_VERSION = resolveAppVersion();

const securityHeaders = [
  {
    key: "Content-Security-Policy",
    value: "base-uri 'self'; form-action 'self'; frame-ancestors 'none'; object-src 'none'",
  },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
];

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  // Don't leak the framework in response headers ("X-Powered-By: Next.js").
  poweredByHeader: false,
  // Never ship readable browser source maps to the client, so "View source"
  // exposes only minified bundles, not original component code.
  productionBrowserSourceMaps: false,
  // PDFKit performs font subsetting at request time. Keep it as a traced Node
  // dependency instead of bundling its fontkit runtime into route chunks.
  serverExternalPackages: ["pdfkit"],
  // The Docker build sets NEXT_SKIP_TYPECHECK=1: CI runs `tsc --noEmit` on every
  // change, so the server does not repeat the (slow, memory-hungry) check.
  // Local `npm run build` still type-checks.
  typescript: {
    ignoreBuildErrors: process.env.NEXT_SKIP_TYPECHECK === "1",
  },
  // Images are served as-is (`images.unoptimized`) and next/image is not used, so
  // sharp's native libvips builds (about 45 MB, for glibc AND musl) can never run.
  // Keep them out of the standalone trace.
  outputFileTracingExcludes: {
    "*": ["node_modules/@img/**", "node_modules/sharp/**"],
  },
  env: {
    NEXT_PUBLIC_APP_VERSION: APP_VERSION,
  },
  images: {
    unoptimized: true,
  },
  turbopack: {
    root: frontendRoot,
  },
  async headers() {
    return [{ source: "/(.*)", headers: securityHeaders }];
  },
};

export default nextConfig;
