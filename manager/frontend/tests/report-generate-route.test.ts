import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";
import { POST as generateReport } from "../app/api/reports/generate/route";

const originalFetch = globalThis.fetch;
const ENGAGEMENT_ID = "11111111-1111-4111-8111-111111111111";
const JOB_ID = "22222222-2222-4222-8222-222222222222";

afterEach(() => {
  globalThis.fetch = originalFetch;
});

function request(body: unknown, authenticated = true): NextRequest {
  return new NextRequest("http://localhost/api/reports/generate", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...(authenticated ? { cookie: "vedha_token=operator-token" } : {}),
    },
    body: JSON.stringify(body),
  });
}

describe("report generation compatibility route", () => {
  test("requires an authenticated operator before reading or forwarding input", async () => {
    let fetchCalls = 0;
    globalThis.fetch = async () => {
      fetchCalls += 1;
      return new Response();
    };

    const response = await generateReport(request({ engagementId: ENGAGEMENT_ID }, false));

    assert.equal(response.status, 401);
    assert.equal(fetchCalls, 0);
    assert.deepEqual(await response.json(), { error: "Not authenticated" });
  });

  test("rejects caller-supplied engagement facts and findings", async () => {
    let fetchCalls = 0;
    globalThis.fetch = async () => {
      fetchCalls += 1;
      return new Response();
    };

    const response = await generateReport(request({
      engagementId: ENGAGEMENT_ID,
      engagement: { name: "forged client" },
      findings: [{ title: "forged finding", evidence: ["untrusted"] }],
    }));

    assert.equal(response.status, 400);
    assert.equal(fetchCalls, 0);
    assert.match((await response.json()).error, /only a valid engagementId/i);
  });

  test("forwards only bounded generation options to the tenant-scoped Manager endpoint", async () => {
    let requestedUrl = "";
    let requestedMethod = "";
    let authorization = "";
    let forwardedBody: unknown;
    globalThis.fetch = async (input, init) => {
      requestedUrl = String(input);
      requestedMethod = init?.method ?? "";
      authorization = new Headers(init?.headers).get("authorization") ?? "";
      forwardedBody = JSON.parse(String(init?.body));
      return new Response(JSON.stringify({ job_id: JOB_ID, status: "queued" }), {
        status: 202,
        headers: { "content-type": "application/json" },
      });
    };

    const response = await generateReport(request({
      engagementId: ENGAGEMENT_ID,
      sections: ["technical_finding"],
      maxFindings: 7,
    }));

    assert.equal(response.status, 202);
    assert.equal(
      requestedUrl,
      `http://localhost:18080/engagements/${ENGAGEMENT_ID}/ai-report/generate`,
    );
    assert.equal(requestedMethod, "POST");
    assert.equal(authorization, "Bearer operator-token");
    assert.deepEqual(forwardedBody, {
      include_technical: true,
      include_remediation: false,
      max_findings: 7,
    });
    assert.deepEqual(await response.json(), {
      job_id: JOB_ID,
      jobId: JOB_ID,
      status: "queued",
    });
  });

  test("preserves Manager authorization and tenant-scope failures", async () => {
    globalThis.fetch = async () => new Response(
      JSON.stringify({ detail: "Engagement not found" }),
      { status: 404, headers: { "content-type": "application/json" } },
    );

    const response = await generateReport(request({ engagementId: ENGAGEMENT_ID }));

    assert.equal(response.status, 404);
    assert.deepEqual(await response.json(), { error: "Engagement not found" });
  });
});
