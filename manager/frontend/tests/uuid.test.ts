/* newId must work where crypto.randomUUID is missing (plain-HTTP origins). */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { newId } from "../lib/uuid";

const V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

test("falls back to getRandomValues when randomUUID is absent", () => {
  const c = globalThis.crypto as Crypto & { randomUUID?: unknown };
  const saved = c.randomUUID;
  Object.defineProperty(c, "randomUUID", { value: undefined, configurable: true, writable: true });
  try {
    const ids = new Set(Array.from({ length: 200 }, newId));
    assert.equal(ids.size, 200);
    for (const id of ids) assert.match(id, V4);
  } finally {
    Object.defineProperty(c, "randomUUID", { value: saved, configurable: true, writable: true });
  }
});

test("no browser code calls crypto.randomUUID directly", () => {
  for (const f of ["lib/findings-workspace-api.ts", "lib/scanner-workspace-api.ts", "lib/remediation.ts",
                   "lib/engagement-workspace-api.ts", "app/aibrain/page.tsx"]) {
    assert.doesNotMatch(readFileSync(f, "utf8"), /crypto\.randomUUID\(/, f);
  }
});
