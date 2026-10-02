import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {
  SCOPE_PRESETS, createPayload, describeScopes, patStatus, patWarnings, sortPats,
} from "../lib/api-keys";

const now = new Date("2026-10-02T12:00:00Z");
const daysAgo = (n: number) => new Date(now.getTime() - n * 86_400_000).toISOString();
const daysAhead = (n: number) => new Date(now.getTime() + n * 86_400_000).toISOString();

// Mirror of ALLOWED_PAT_SCOPES in manager/backend/app/auth/pat.py. The page once sent
// "read"/"write", which the backend rejects, so no key could ever be created.
const BACKEND_SCOPES = new Set(["api:*", "api:read", "api:write", "probe:read", "probe:write", "probe:register", "engagement:read", "engagement:write"]);

test("every preset uses only scopes the backend accepts", () => {
  for (const p of SCOPE_PRESETS) for (const s of p.scopes) assert.ok(BACKEND_SCOPES.has(s), `${p.id}: ${s}`);
});

test("the backend scope list in this test still matches the backend", () => {
  const src = fs.readFileSync(path.resolve(__dirname, "../../backend/app/auth/pat.py"), "utf8");
  const block = src.slice(src.indexOf("ALLOWED_PAT_SCOPES"), src.indexOf("}", src.indexOf("ALLOWED_PAT_SCOPES")));
  const found = new Set([...block.matchAll(/"([a-z]+:[a-z*]+)"/g)].map((m) => m[1]));
  assert.deepEqual([...found].sort(), [...BACKEND_SCOPES].sort());
});

test("the first preset is the least privileged and read only", () => {
  assert.deepEqual(SCOPE_PRESETS[0].scopes, ["api:read"]);
});

test("the create request carries a trimmed name, real scopes and an expiry", () => {
  assert.deepEqual(createPayload("  ci-scanner  ", "readwrite", 30),
    { name: "ci-scanner", scopes: ["api:read", "api:write"], expires_in_days: 30 });
  assert.deepEqual(createPayload("x", "nonsense" as never, 7).scopes, ["api:read"]);
});

test("scopes are described in plain words", () => {
  assert.equal(describeScopes(["api:read"]), "Read only");
  assert.equal(describeScopes(["api:write", "api:read"]), "Read and write");
  assert.equal(describeScopes(["api:*"]), "Full access");
  assert.equal(describeScopes(SCOPE_PRESETS[2].scopes), "Probe or agent");
  assert.equal(describeScopes(["probe:read"]), "probe:read");
  assert.equal(describeScopes([]), "No scopes");
});

test("status: revoked beats expired beats active", () => {
  assert.equal(patStatus({ created_at: daysAgo(5), revoked_at: daysAgo(1), expires_at: daysAgo(2) }, now), "revoked");
  assert.equal(patStatus({ created_at: daysAgo(50), expires_at: daysAgo(1) }, now), "expired");
  assert.equal(patStatus({ created_at: daysAgo(5), expires_at: daysAhead(30) }, now), "active");
  assert.equal(patStatus({ created_at: daysAgo(5) }, now), "active");
});

test("warnings: never-expiring and long-unused live keys, nothing for dead ones", () => {
  assert.deepEqual(patWarnings({ created_at: daysAgo(5), expires_at: null, last_used_at: daysAgo(1) }, now), ["no_expiry"]);
  assert.deepEqual(patWarnings({ created_at: daysAgo(200), expires_at: daysAhead(10), last_used_at: daysAgo(120) }, now), ["unused"]);
  assert.deepEqual(patWarnings({ created_at: daysAgo(200), expires_at: daysAhead(10), last_used_at: null }, now), ["unused"]);
  assert.deepEqual(patWarnings({ created_at: daysAgo(10), expires_at: daysAhead(10), last_used_at: null }, now), []);
  assert.deepEqual(patWarnings({ created_at: daysAgo(500), revoked_at: daysAgo(1) }, now), []);
  assert.deepEqual(patWarnings({ created_at: daysAgo(500), expires_at: daysAgo(1) }, now), []);
});

test("sorting puts live keys first and revoked last, newest first within a group", () => {
  const a = { id: "a", created_at: daysAgo(10), expires_at: daysAhead(5) };
  const b = { id: "b", created_at: daysAgo(2), expires_at: daysAhead(5) };
  const c = { id: "c", created_at: daysAgo(1), revoked_at: daysAgo(0) };
  const d = { id: "d", created_at: daysAgo(20), expires_at: daysAgo(1) };
  assert.deepEqual(sortPats([c, d, a, b], now).map((p) => p.id), ["b", "a", "d", "c"]);
});
