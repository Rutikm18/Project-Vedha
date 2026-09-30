import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";

import { GET as getReportDocument } from "../app/api/engagements/[id]/report-document/route";

const originalFetch = globalThis.fetch;
const ENGAGEMENT_ID = "11111111-1111-4111-8111-111111111111";

afterEach(() => {
  globalThis.fetch = originalFetch;
});

function request(authenticated = true, headers: HeadersInit = {}): NextRequest {
  return new NextRequest(
    `http://localhost/api/engagements/${ENGAGEMENT_ID}/report-document`,
    {
      headers: {
        ...(authenticated ? { cookie: "vedha_token=operator-token" } : {}),
        ...Object.fromEntries(new Headers(headers).entries()),
      },
    },
  );
}

function invoke(authenticated = true, id = ENGAGEMENT_ID, headers: HeadersInit = {}) {
  return getReportDocument(request(authenticated, headers), {
    params: Promise.resolve({ id }),
  });
}

describe("canonical report-document BFF", () => {
  test("requires an authenticated operator before calling Manager", async () => {
    let fetchCalls = 0;
    globalThis.fetch = async () => {
      fetchCalls += 1;
      return new Response();
    };

    const response = await invoke(false);

    assert.equal(response.status, 401);
    assert.equal(fetchCalls, 0);
    assert.deepEqual(await response.json(), { error: "Not authenticated" });
  });

  test("forwards auth to the tenant-scoped endpoint and returns the contract unchanged", async () => {
    const canonical = {
      document: {
        schema_version: "1.0",
        generated_at: "2026-09-26T08:30:00Z",
        timezone: "UTC",
        snapshot_kind: "postgresql_repeatable_read_read_only",
        snapshot_guarantee: "repeatable_read",
        persisted: false,
      },
      engagement: { id: ENGAGEMENT_ID, name: "Assessment" },
      summary: { total_findings: 1 },
      findings: [{ id: "finding-1", title: "Recorded finding" }],
      compliance_rollup: { source: "recorded_finding_mappings_only" },
      readiness: { complete: false },
    };
    let requestedUrl = "";
    let authorization = "";
    let method = "";
    let cache: RequestCache | undefined;
    let body: BodyInit | null | undefined;
    globalThis.fetch = async (input, init) => {
      requestedUrl = String(input);
      authorization = new Headers(init?.headers).get("authorization") ?? "";
      method = init?.method ?? "";
      cache = init?.cache;
      body = init?.body;
      return new Response(JSON.stringify(canonical), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const response = await invoke();

    assert.equal(response.status, 200);
    assert.equal(requestedUrl, `http://localhost:18080/engagements/${ENGAGEMENT_ID}/report-document`);
    assert.equal(authorization, "Bearer operator-token");
    assert.equal(method, "GET");
    assert.equal(cache, "no-store");
    assert.equal(body, undefined);
    assert.equal(response.headers.get("cache-control"), "private, no-store");
    assert.deepEqual(await response.json(), canonical);
  });

  test("preserves Manager's indistinguishable missing or cross-tenant response", async () => {
    globalThis.fetch = async () => new Response(
      JSON.stringify({ detail: "Engagement not found" }),
      { status: 404, headers: { "content-type": "application/json" } },
    );

    const response = await invoke();

    assert.equal(response.status, 404);
    assert.deepEqual(await response.json(), { error: "Engagement not found" });
  });

  test("prefers an explicit bearer token and safely encodes the dynamic segment", async () => {
    const untrustedSegment = "../other?raw=true";
    let requestedUrl = "";
    let authorization = "";
    globalThis.fetch = async (input, init) => {
      requestedUrl = String(input);
      authorization = new Headers(init?.headers).get("authorization") ?? "";
      return new Response(JSON.stringify({ findings: [] }), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const response = await invoke(true, untrustedSegment, {
      authorization: "Bearer explicit-operator-token",
    });

    assert.equal(response.status, 200);
    assert.equal(authorization, "Bearer explicit-operator-token");
    assert.equal(
      requestedUrl,
      "http://localhost:18080/engagements/..%2Fother%3Fraw%3Dtrue/report-document",
    );
  });
});
