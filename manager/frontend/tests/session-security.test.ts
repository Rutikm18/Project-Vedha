import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, test } from "node:test";
import { forwardedFor } from "../lib/backend";

const read = (p: string) => readFileSync(join(process.cwd(), p), "utf8");

describe("client IP forwarding (login rate limit)", () => {
  test("forwards the edge's X-Forwarded-For", () => {
    const req = new Request("http://localhost/api/auth/login", {
      headers: { "x-forwarded-for": "198.51.100.7" },
    });
    assert.deepEqual(forwardedFor(req), { "X-Forwarded-For": "198.51.100.7" });
  });

  test("sends nothing when there is no edge header", () => {
    assert.deepEqual(forwardedFor(new Request("http://localhost/api/auth/login")), {});
  });

  test("both login routes forward it — else every user shares one IP bucket", () => {
    for (const route of ["app/api/auth/login/route.ts", "app/api/portal/login/route.ts"]) {
      assert.match(read(route), /headers: forwardedFor\(req\)/, route);
    }
  });
});

describe("refresh token handling", () => {
  test("refresh token travels in the body, never the query string", () => {
    for (const route of ["app/api/auth/login/route.ts", "app/api/portal/login/route.ts"]) {
      const src = read(route);
      assert.doesNotMatch(src, /query: \{ refresh_token/, route);
      assert.match(src, /body: \{ refresh_token: refreshToken \}/, route);
    }
  });

  test("sign-out revokes server-side from the route that holds the path-scoped cookie", () => {
    for (const route of ["app/api/auth/login/route.ts", "app/api/portal/login/route.ts"]) {
      const src = read(route);
      assert.match(src, /export async function DELETE/, route);
      assert.match(src, /"\/auth\/logout"/, route);
    }
    const shell = read("components/PageShell.tsx");
    assert.match(shell, /"\/api\/auth\/login", \{ method: "DELETE" \}/);
    assert.match(shell, /"\/api\/portal\/login", \{ method: "DELETE" \}/);
  });
});
