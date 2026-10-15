import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";

import { GET as getReportDocument } from "../app/api/engagements/[id]/report-document/route";
import { POST as exportReport } from "../app/api/reports/export/route";
import {
  allIds,
  idsOfSeverity,
  isStrictSubset,
  selectionKey,
  setSeverity,
  severityState,
  toggle,
} from "../lib/report/selection";
import type { ReportFinding } from "../lib/report/report-document";
import { canonicalReport } from "./fixtures/canonical-report";

const originalFetch = globalThis.fetch;
const ENGAGEMENT_ID = "11111111-1111-4111-8111-111111111111";
const F1 = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa";
const F2 = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb";
const F3 = "cccccccc-cccc-4ccc-8ccc-cccccccccccc";

afterEach(() => {
  globalThis.fetch = originalFetch;
});

function finding(id: string, severity: string): ReportFinding {
  return { id, severity } as ReportFinding;
}

describe("report finding selection — helpers", () => {
  const findings = [finding(F1, "critical"), finding(F2, "high"), finding(F3, "high")];

  test("selectionKey is order-independent and de-duplicated", () => {
    assert.equal(selectionKey([F2, F1, F1]), [F1, F2].sort().join(","));
    assert.equal(selectionKey([F1, F2]), selectionKey([F2, F1]));
  });

  test("toggle adds then removes", () => {
    const once = toggle(new Set<string>(), F1);
    assert.ok(once.has(F1));
    assert.ok(!toggle(once, F1).has(F1));
  });

  test("setSeverity selects a whole band; severityState reports none/some/all", () => {
    const highs = setSeverity(new Set<string>(), findings, "high", true);
    assert.deepEqual([...highs].sort(), [F2, F3].sort());
    assert.equal(severityState(highs, findings, "high"), "all");
    assert.equal(severityState(new Set([F2]), findings, "high"), "some");
    assert.equal(severityState(new Set<string>(), findings, "high"), "none");
    assert.equal(severityState(new Set<string>(), findings, "low"), "none"); // no low findings
    assert.equal(setSeverity(highs, findings, "high", false).size, 0);
  });

  test("idsOfSeverity and allIds", () => {
    assert.deepEqual(idsOfSeverity(findings, "critical"), [F1]);
    assert.deepEqual([...allIds(findings)].sort(), [F1, F2, F3].sort());
  });

  test("isStrictSubset: empty, all, and zero-total are not subsets", () => {
    assert.equal(isStrictSubset(new Set(), 3), false);
    assert.equal(isStrictSubset(new Set([F1, F2, F3]), 3), false);
    assert.equal(isStrictSubset(new Set([F1]), 3), true);
    assert.equal(isStrictSubset(new Set([F1]), 0), false);
  });
});

describe("report-document BFF forwards the finding_ids scope", () => {
  function invoke(query: string) {
    const req = new NextRequest(
      `http://localhost/api/engagements/${ENGAGEMENT_ID}/report-document${query}`,
      { headers: { cookie: "vedha_token=operator-token" } },
    );
    return getReportDocument(req, { params: Promise.resolve({ id: ENGAGEMENT_ID }) });
  }

  test("appends finding_ids to the Manager path when present", async () => {
    let requestedUrl = "";
    globalThis.fetch = async (input) => {
      requestedUrl = String(input);
      return new Response(JSON.stringify({ findings: [] }), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const response = await invoke(`?finding_ids=${F1},${F2}`);

    assert.equal(response.status, 200);
    assert.equal(
      requestedUrl,
      `http://localhost:18080/engagements/${ENGAGEMENT_ID}/report-document?finding_ids=${F1}%2C${F2}`,
    );
  });

  test("omits the scope when no finding_ids is given (full-engagement, cached)", async () => {
    let requestedUrl = "";
    globalThis.fetch = async (input) => {
      requestedUrl = String(input);
      return new Response(JSON.stringify({ findings: [] }), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    await invoke("");

    assert.equal(
      requestedUrl,
      `http://localhost:18080/engagements/${ENGAGEMENT_ID}/report-document`,
    );
  });
});

describe("report export route honours the finding_ids scope", () => {
  function request(body: unknown, cookie = "vedha_token=operator-token"): NextRequest {
    return new NextRequest("http://localhost/api/reports/export", {
      method: "POST",
      headers: { "content-type": "application/json", ...(cookie ? { cookie } : {}) },
      body: JSON.stringify(body),
    });
  }

  test("re-fetches the scoped canonical document for a subset export", async () => {
    let requestedUrl = "";
    globalThis.fetch = async (input) => {
      requestedUrl = String(input);
      return new Response(JSON.stringify(canonicalReport), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const response = await exportReport(
      request({ format: "csv", engagementId: ENGAGEMENT_ID, findingIds: [F1, F2] }),
    );

    assert.equal(response.status, 200);
    assert.equal(
      requestedUrl,
      `http://localhost:18080/engagements/${ENGAGEMENT_ID}/report-document?finding_ids=${F1}%2C${F2}`,
    );
  });

  test("rejects a findingIds that is not an array of UUIDs, before any backend call", async () => {
    let calls = 0;
    globalThis.fetch = async () => {
      calls += 1;
      return new Response();
    };

    const response = await exportReport(
      request({ format: "csv", engagementId: ENGAGEMENT_ID, findingIds: ["not-a-uuid"] }),
    );

    assert.equal(response.status, 400);
    assert.equal(calls, 0);
  });

  test("omits the scope when findingIds is empty (whole engagement)", async () => {
    let requestedUrl = "";
    globalThis.fetch = async (input) => {
      requestedUrl = String(input);
      return new Response(JSON.stringify(canonicalReport), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    await exportReport(request({ format: "csv", engagementId: ENGAGEMENT_ID, findingIds: [] }));

    assert.equal(
      requestedUrl,
      `http://localhost:18080/engagements/${ENGAGEMENT_ID}/report-document`,
    );
  });
});
