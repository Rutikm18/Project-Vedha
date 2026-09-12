import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

test("portal pages use the portal session and portal login gate", () => {
  const proxy = readFileSync(join(process.cwd(), "proxy.ts"), "utf8");
  assert.match(proxy, /"\/portal\/login"/);
  assert.match(proxy, /portalPage \? "vedha_portal_token" : "vedha_token"/);
  assert.match(proxy, /portalPage \? "\/portal\/login" : "\/login"/);
});
