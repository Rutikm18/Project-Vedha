/* A paused query (React Query pauses retries while the window is unfocused)
 * has no data yet. The shared hook must report it as loading — panels gated on
 * isLoading used to render the missing data as zeros ("0 open findings"). */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("useConsoleQuery treats a paused, data-less query as loading", () => {
  const src = readFileSync(join(process.cwd(), "lib/console-source.tsx"), "utf8");
  assert.match(src, /const waiting = query\.isPending && query\.fetchStatus !== "idle";/);
  assert.match(src, /isLoading: waiting/);
});
