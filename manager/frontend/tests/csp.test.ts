import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { buildScriptCsp, makeNonce, STATIC_DIRECTIVES } from "../lib/csp";

const root = path.resolve(__dirname, "..");

test("script-src carries the nonce and strict-dynamic, with no unsafe-inline", () => {
  const csp = buildScriptCsp("abc123", false);
  assert.match(csp, /script-src 'self' 'nonce-abc123' 'strict-dynamic'/);
  assert.doesNotMatch(csp, /unsafe-inline|unsafe-eval/);
});

test("unsafe-eval is allowed in development only", () => {
  assert.match(buildScriptCsp("n", true), /'unsafe-eval'/);
  assert.doesNotMatch(buildScriptCsp("n", false), /'unsafe-eval'/);
});

test("the policy keeps the framing / base / form / object directives", () => {
  const csp = buildScriptCsp("n", false);
  for (const d of ["base-uri 'self'", "form-action 'self'", "frame-ancestors 'none'", "object-src 'none'"]) {
    assert.ok(csp.includes(d), d);
  }
});

test("no upgrade-insecure-requests (plain-HTTP deployments must keep working)", () => {
  assert.doesNotMatch(buildScriptCsp("n", false), /upgrade-insecure-requests/);
});

test("every request gets a fresh nonce", () => {
  const seen = new Set(Array.from({ length: 50 }, () => makeNonce()));
  assert.equal(seen.size, 50);
  for (const n of seen) assert.match(n, /^[A-Za-z0-9+/=]+$/);
});

test("static CSP in next.config.mjs matches STATIC_DIRECTIVES", () => {
  const cfg = fs.readFileSync(path.join(root, "next.config.mjs"), "utf8");
  assert.ok(cfg.includes(`value: "${STATIC_DIRECTIVES}"`), "next.config.mjs CSP drifted from lib/csp.ts");
});

test("proxy applies the nonce CSP and the layout stamps its inline script", () => {
  const proxy = fs.readFileSync(path.join(root, "proxy.ts"), "utf8");
  assert.match(proxy, /buildScriptCsp\(/);
  assert.match(proxy, /"x-nonce"/);
  const layout = fs.readFileSync(path.join(root, "app/layout.tsx"), "utf8");
  assert.match(layout, /<script\s+nonce=\{nonce\}/);
});

test("no page or component adds an inline <script> without going through the nonce", () => {
  const offenders: string[] = [];
  const walk = (dir: string) => {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) { if (e.name !== "node_modules" && e.name !== ".next") walk(p); continue; }
      if (!/\.(tsx|jsx)$/.test(e.name)) continue;
      const src = fs.readFileSync(p, "utf8");
      for (const m of src.matchAll(/<script\b([^>]*)>/g)) {
        if (!/nonce=/.test(m[1])) offenders.push(path.relative(root, p));
      }
    }
  };
  for (const d of ["app", "components"]) walk(path.join(root, d));
  assert.deepEqual(offenders, []);
});
