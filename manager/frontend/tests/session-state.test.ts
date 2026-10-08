import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

const read = (p: string) => readFileSync(join(process.cwd(), p), "utf8");

test("AI Brain keeps its conversation in the shared session store, not component state", () => {
  const page = read("app/aibrain/workspace.tsx");
  assert.match(page, /useSessionState<Message\[\]>\(`aibrain\.\$\{surface\}\.messages`/);
  assert.doesNotMatch(page, /useState<Message\[\]>/);
  assert.match(page, /\{ persist: false \}/); // sending/error are never persisted
});

test("saved conversations are wiped on logout and session expiry", () => {
  assert.match(read("lib/fetcher.ts"), /clearSessionState\(\)/);
  assert.match(read("components/PageShell.tsx"), /clearSessionState\(\)/);
});
