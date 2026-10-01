import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";
import { GET as listTokens, POST as createToken } from "../app/api/fleet/enroll-tokens/route";
import { DELETE as revokeToken } from "../app/api/fleet/enroll-tokens/[id]/route";
import { GET as releaseGet } from "../app/api/fleet/release/route";
import { managerHost } from "../app/fleet/AddAgent";

const originalFetch = globalThis.fetch;
afterEach(() => { globalThis.fetch = originalFetch; });

type Seen = { url: string; method: string; body: unknown; auth: string };

function stubBackend(response: unknown, status = 200): Seen[] {
  const seen: Seen[] = [];
  globalThis.fetch = async (input, init) => {
    seen.push({
      url: String(input),
      method: init?.method ?? "GET",
      body: init?.body ? JSON.parse(String(init.body)) : undefined,
      auth: new Headers(init?.headers).get("authorization") ?? "",
    });
    return status === 204
      ? new Response(null, { status })
      : new Response(JSON.stringify(response), { status, headers: { "content-type": "application/json" } });
  };
  return seen;
}

const auth = { authorization: "Bearer operator-token" };

describe("Fleet → Add agent BFF", () => {
  test("create forwards the engagement, fixes a 24 h lifetime and defaults the label", async () => {
    const seen = stubBackend({ id: "t1", token: "vet_x", commands: { one_line: "curl …" } }, 201);
    const res = await createToken(new NextRequest("http://localhost/api/fleet/enroll-tokens", {
      method: "POST", headers: auth,
      body: JSON.stringify({ engagement_id: "eng-1", name: "  ", expires_in_minutes: 999999, max_uses: 50 }),
    }));
    assert.equal(res.status, 201);
    assert.match(seen[0].url, /\/probe-enrollment\/enroll-tokens$/);
    assert.equal(seen[0].method, "POST");
    assert.equal(seen[0].auth, "Bearer operator-token");
    // the browser cannot stretch the lifetime or make it multi-use
    assert.deepEqual(seen[0].body, { name: "vedha-agent", engagement_id: "eng-1", expires_in_minutes: 1440 });
  });

  test("list passes the engagement filter through", async () => {
    const seen = stubBackend([]);
    await listTokens(new NextRequest("http://localhost/api/fleet/enroll-tokens?engagement_id=eng-9", { headers: auth }));
    assert.match(seen[0].url, /\/probe-enrollment\/enroll-tokens\?engagement_id=eng-9$/);
  });

  test("revoke maps to DELETE and returns 204", async () => {
    const seen = stubBackend(null, 204);
    const res = await revokeToken(
      new NextRequest("http://localhost/api/fleet/enroll-tokens/abc", { method: "DELETE", headers: auth }),
      { params: Promise.resolve({ id: "abc" }) },
    );
    assert.equal(res.status, 204);
    assert.equal(seen[0].method, "DELETE");
    assert.match(seen[0].url, /\/probe-enrollment\/enroll-tokens\/abc$/);
  });

  test("release status comes from the backend", async () => {
    const seen = stubBackend({ available: true, version: "1.0.338", manager_url: "https://api.vedhasec.com" });
    const res = await releaseGet(new NextRequest("http://localhost/api/fleet/release", { headers: auth }));
    assert.match(seen[0].url, /\/agent\/release$/);
    assert.equal((await res.json()).version, "1.0.338");
  });

  test("unauthenticated calls never reach the backend", async () => {
    const seen = stubBackend({});
    const res = await createToken(new NextRequest("http://localhost/api/fleet/enroll-tokens", {
      method: "POST", body: JSON.stringify({ engagement_id: "eng-1" }),
    }));
    assert.equal(res.status, 401);
    assert.equal(seen.length, 0);
  });
});

describe("Fleet install UI", () => {
  test("the placeholder download domain is gone", () => {
    for (const file of ["app/fleet/page.tsx", "app/fleet/AddAgent.tsx", "app/api/fleet/enrollment/route.ts"]) {
      const source = readFileSync(join(process.cwd(), file), "utf8");
      assert.doesNotMatch(source, /downloads\.vedha\.example|manager\.example\.com/, file);
    }
    const page = readFileSync(join(process.cwd(), "app/fleet/page.tsx"), "utf8");
    assert.match(page, /<AddAgent surface=\{surface\} api=\{api\} \/>/);
  });

  test("the portal never chooses an engagement for its token", () => {
    const adapter = readFileSync(join(process.cwd(), "lib/fleet-workspace-api.ts"), "utf8");
    assert.match(adapter, /portalApi<InstallToken>\("\/workspace\/fleet\/enroll-tokens", \{ method: "POST", body: \{ name \} \}\)/);
  });

  test("managerHost shows the host the agent dials", () => {
    assert.equal(managerHost("https://api.vedhasec.com"), "api.vedhasec.com");
    assert.equal(managerHost("http://10.0.0.5:18080/"), "10.0.0.5:18080");
    assert.equal(managerHost(""), "your Vedha manager");
  });
});
