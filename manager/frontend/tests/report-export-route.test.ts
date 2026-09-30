import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";

import { POST as exportReport } from "../app/api/reports/export/route";
import { canonicalReport } from "./fixtures/canonical-report";

const originalFetch = globalThis.fetch;
const ENGAGEMENT_ID = "11111111-1111-4111-8111-111111111111";

afterEach(() => {
  globalThis.fetch = originalFetch;
});
function request(
  body: unknown,
  cookie = "vedha_token=operator-token",
): NextRequest {
  return new NextRequest("http://localhost/api/reports/export", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...(cookie ? { cookie } : {}),
    },
    body: JSON.stringify(body),
  });
}

describe("canonical report export route", () => {
  test("denies an unauthenticated request before reading Manager data", async () => {
    let calls = 0;
    globalThis.fetch = async () => {
      calls += 1;
      return new Response();
    };

    const response = await exportReport(request({ format: "pdf", engagementId: ENGAGEMENT_ID }, ""));

    assert.equal(response.status, 401);
    assert.equal(calls, 0);
  });

  test("does not accept a portal-only cookie on the operator export endpoint", async () => {
    let calls = 0;
    globalThis.fetch = async () => {
      calls += 1;
      return new Response();
    };

    const response = await exportReport(request(
      { format: "pdf", engagementId: ENGAGEMENT_ID },
      "vedha_portal_token=portal-token",
    ));

    assert.equal(response.status, 401);
    assert.equal(calls, 0);
  });

  test("rejects extra caller-supplied report facts before a backend call", async () => {
    let calls = 0;
    globalThis.fetch = async () => {
      calls += 1;
      return new Response();
    };

    const response = await exportReport(request({
      format: "docx",
      engagementId: ENGAGEMENT_ID,
      findings: [{ title: "forged finding" }],
    }));

    assert.equal(response.status, 400);
    assert.equal(calls, 0);
  });

  test("reloads the canonical tenant-scoped document and forwards the operator token", async () => {
    const calls: Array<{ path: string; authorization: string }> = [];
    globalThis.fetch = async (input, init) => {
      const url = new URL(String(input));
      calls.push({
        path: url.pathname,
        authorization: new Headers(init?.headers).get("authorization") ?? "",
      });
      return new Response(JSON.stringify(canonicalReport), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const response = await exportReport(request({ format: "csv", engagementId: ENGAGEMENT_ID }));

    assert.equal(response.status, 200);
    assert.equal(response.headers.get("content-type"), "text/csv; charset=utf-8");
    assert.deepEqual(calls, [{
      path: `/engagements/${ENGAGEMENT_ID}/report-document`,
      authorization: "Bearer operator-token",
    }]);
    const text = Buffer.from(await response.arrayBuffer()).toString("utf8");
    assert.match(text, /First complete finding/);
  });

  for (const status of [403, 404]) {
    test(`propagates Manager ${status} without generating an export`, async () => {
      globalThis.fetch = async () => new Response(
        JSON.stringify({ detail: status === 403 ? "Forbidden" : "Not found" }),
        { status, headers: { "content-type": "application/json" } },
      );

      const response = await exportReport(request({ format: "xlsx", engagementId: ENGAGEMENT_ID }));

      assert.equal(response.status, status);
      assert.deepEqual(await response.json(), {
        error: status === 403 ? "Forbidden" : "Not found",
      });
    });
  }
});
