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
