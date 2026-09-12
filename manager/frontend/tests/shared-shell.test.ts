import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("customer and manager use one canonical visual shell", () => {
  const portalShell = readFileSync(join(process.cwd(), "components/portal/PortalShell.tsx"), "utf8");
  assert.match(portalShell, /<PageShell/);
  assert.match(portalShell, /surface="portal"/);
  assert.doesNotMatch(portalShell, /<header|<aside|<footer|PortalSidebar/);
});
