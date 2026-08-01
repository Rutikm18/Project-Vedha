import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { bearerFrom, cookieFrom } from "../lib/backend";

describe("BFF session token extraction", () => {
  test("reads browser sessions from an HttpOnly-compatible cookie header", () => {
    const request = new Request("http://localhost/api/findings", {
      headers: { cookie: "theme=dark; vedha_token=cookie.jwt.value; tenant=acme" },
    });

    assert.equal(cookieFrom(request, "vedha_token"), "cookie.jwt.value");
    assert.equal(bearerFrom(request), "cookie.jwt.value");
  });

  test("keeps bearer authorization for API clients and gives it precedence", () => {
    const request = new Request("http://localhost/api/findings", {
      headers: {
        authorization: "Bearer cli.jwt.value",
        cookie: "vedha_token=cookie.jwt.value",
      },
    });

    assert.equal(bearerFrom(request), "cli.jwt.value");
  });

  test("rejects a malformed encoded cookie instead of throwing", () => {
    const request = new Request("http://localhost/api/findings", {
      headers: { cookie: "vedha_token=%E0%A4%A" },
    });

    assert.equal(bearerFrom(request), null);
  });
});
