import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";

import { GET as getFindings } from "../app/api/findings/route";

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe("findings BFF filters", () => {
  test("forwards canonical detection and exploit-validation filters", async () => {
    let requestedUrl = "";
    globalThis.fetch = async (input) => {
      requestedUrl = String(input);
      return new Response(JSON.stringify({
        items: [], total: 0, page: 1, page_size: 20, pages: 1,
      }), { status: 200, headers: { "content-type": "application/json" } });
    };

    const response = await getFindings(new NextRequest(
      "http://localhost/api/findings?paginated=true&detection_status=missed&exploit_validated=true",
      { headers: { authorization: "Bearer operator-token" } },
    ));

    assert.equal(response.status, 200);
    const forwarded = new URL(requestedUrl);
    assert.equal(forwarded.pathname, "/findings");
    assert.equal(forwarded.searchParams.get("detection_status"), "missed");
    assert.equal(forwarded.searchParams.get("exploit_validated"), "true");
  });

  test("does not invent filters when they are absent", async () => {
    let requestedUrl = "";
    globalThis.fetch = async (input) => {
      requestedUrl = String(input);
      return new Response(JSON.stringify({
        items: [], total: 0, page: 1, page_size: 20, pages: 1,
      }), { status: 200, headers: { "content-type": "application/json" } });
    };

    const response = await getFindings(new NextRequest(
      "http://localhost/api/findings?paginated=true",
      { headers: { authorization: "Bearer operator-token" } },
    ));

    assert.equal(response.status, 200);
    const forwarded = new URL(requestedUrl);
    assert.equal(forwarded.searchParams.has("detection_status"), false);
    assert.equal(forwarded.searchParams.has("exploit_validated"), false);
  });
});
