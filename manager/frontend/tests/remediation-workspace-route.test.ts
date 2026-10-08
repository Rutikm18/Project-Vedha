import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";

import { POST as previewWorkspace } from "../app/api/findings/remediation-workspaces/preview/route";

const originalFetch = globalThis.fetch;
const FINDING_A = "11111111-1111-4111-8111-111111111111";
const FINDING_B = "22222222-2222-4222-8222-222222222222";
const SHA_A = "a".repeat(64);
const SHA_B = "b".repeat(64);

const canonical = {
  engagement_id: "55555555-5555-4555-8555-555555555555",
  catalog_version: "2026.09.1",
  context_sha256: SHA_A,
  generated_at: "2026-09-27T05:30:00Z",
  review_only: true,
  finding_count: 2,
  operation_count: 1,
  artifacts: [{
    artifact_id: "33333333-3333-4333-8333-333333333333",
    asset_id: "44444444-4444-4444-8444-444444444444",
    os_family: "linux",
    format: "bash",
    filename: "repair-web.sh",
    finding_ids: [FINDING_A, FINDING_B],
    context_sha256: SHA_A,
    content_sha256: SHA_B,
    content: "#!/usr/bin/env bash\necho review-only\n",
  }],
  blocked: [],
  advisory: null,
  warnings: [],
};

afterEach(() => {
  globalThis.fetch = originalFetch;
});

function request(body: unknown, authenticated = true): NextRequest {
  return new NextRequest(
    "http://localhost/api/findings/remediation-workspaces/preview",
    {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...(authenticated ? { cookie: "vedha_token=operator-token" } : {}),
      },
      body: typeof body === "string" ? body : JSON.stringify(body),
    },
  );
}

describe("remediation workspace preview BFF", () => {
  test("requires authentication before reading or forwarding input", async () => {
    let fetchCalls = 0;
    globalThis.fetch = async () => {
      fetchCalls += 1;
      return new Response();
    };

    const response = await previewWorkspace(request({ finding_ids: [FINDING_A] }, false));

    assert.equal(response.status, 401);
    assert.equal(fetchCalls, 0);
    assert.equal(response.headers.get("cache-control"), "private, no-store");
  });

  test("forwards only the validated selection and preserves the response contract", async () => {
    let requestedUrl = "";
    let authorization = "";
    let method = "";
    let cache: RequestCache | undefined;
    let forwardedBody: unknown;
    globalThis.fetch = async (input, init) => {
      requestedUrl = String(input);
      authorization = new Headers(init?.headers).get("authorization") ?? "";
      method = init?.method ?? "";
      cache = init?.cache;
      forwardedBody = JSON.parse(String(init?.body));
      return new Response(JSON.stringify(canonical), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const response = await previewWorkspace(request({
      finding_ids: [FINDING_A, FINDING_B],
      include_advisory: true,
    }));

    assert.equal(response.status, 200);
    assert.equal(requestedUrl, "http://localhost:18080/findings/remediation-workspaces/preview");
    assert.equal(authorization, "Bearer operator-token");
    assert.equal(method, "POST");
    assert.equal(cache, "no-store");
    assert.deepEqual(forwardedBody, {
      finding_ids: [FINDING_A, FINDING_B],
      include_advisory: true,
    });
    assert.equal(response.headers.get("cache-control"), "private, no-store");
    assert.deepEqual(await response.json(), canonical);
  });

  test("rejects malformed, duplicate, empty, and oversized selections before Manager", async () => {
    let fetchCalls = 0;
    globalThis.fetch = async () => {
      fetchCalls += 1;
      return new Response();
    };
    const tooMany = Array.from(
      { length: 21 },
      (_, index) => `00000000-0000-4000-8000-${String(index).padStart(12, "0")}`,
    );
    const invalidBodies = [
      { finding_ids: [] },
      { finding_ids: tooMany },
      { finding_ids: ["not-a-uuid"] },
      { finding_ids: [FINDING_A, FINDING_A] },
      { finding_ids: [FINDING_A], include_advisory: "yes" },
      { finding_ids: [FINDING_A], evidence: { forged: true } },
    ];

    for (const body of invalidBodies) {
      const response = await previewWorkspace(request(body));
      assert.equal(response.status, 400);
      assert.equal(response.headers.get("cache-control"), "private, no-store");
    }
    assert.equal(fetchCalls, 0);
  });

  test("rejects malformed JSON before Manager", async () => {
    let fetchCalls = 0;
    globalThis.fetch = async () => {
      fetchCalls += 1;
      return new Response();
    };

    const response = await previewWorkspace(request("{bad json"));

    assert.equal(response.status, 400);
    assert.equal(fetchCalls, 0);
  });

  test("preserves Manager validation failures without making them cacheable", async () => {
    globalThis.fetch = async () => new Response(
      JSON.stringify({ detail: "Selected findings must belong to one engagement" }),
      { status: 422, headers: { "content-type": "application/json" } },
    );

    const response = await previewWorkspace(request({ finding_ids: [FINDING_A, FINDING_B] }));

    assert.equal(response.status, 422);
    assert.equal(response.headers.get("cache-control"), "private, no-store");
    assert.deepEqual(await response.json(), {
      error: "Selected findings must belong to one engagement",
    });
  });
});
