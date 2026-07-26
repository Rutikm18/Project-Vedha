import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { NextRequest, NextResponse } from "next/server";

import { POST as eyeWitnessPost } from "../app/api/scan/eyewitness/route";
import { POST as naabuPost } from "../app/api/scan/naabu/route";
import { POST as netExecPost } from "../app/api/scan/netexec/route";
import { POST as nmapPost } from "../app/api/scan/nmap/route";
import { POST as nucleiPost } from "../app/api/scan/nuclei/route";
import { POST as openVASPost } from "../app/api/scan/openvas/route";
import { GET as openVASGet } from "../app/api/scan/openvas/[taskId]/route";
import { POST as pipelinePost } from "../app/api/scan/pipeline/route";
import { GET as pipelineGet } from "../app/api/scan/pipeline/[scanId]/route";
import { GET as scanStreamGet } from "../app/api/scan/stream/[scanId]/route";
import { POST as testsslPost } from "../app/api/scan/testssl/route";
import { setTask } from "../lib/openvas-client";
import { withVerifiedBackend } from "../lib/with-backend";

const POST_ROUTES = [
  ["eyewitness", eyeWitnessPost],
  ["naabu", naabuPost],
  ["netexec", netExecPost],
  ["nmap", nmapPost],
  ["nuclei", nucleiPost],
  ["openvas", openVASPost],
  ["pipeline", pipelinePost],
  ["testssl", testsslPost],
] as const;

function postRequest(name: string, token?: string): NextRequest {
  return new NextRequest(`http://localhost/api/scan/${name}`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...(token ? { authorization: `Bearer ${token}` } : {}),
    },
    body: "{}",
  });
}

async function withIdentity(
  role: string,
  run: () => Promise<Response>,
  tenantId = "tenant-1",
): Promise<Response> {
  const previousFetch = globalThis.fetch;
  const previousLocalScannerFlag = process.env.ENABLE_LEGACY_LOCAL_SCANNERS;
  process.env.ENABLE_LEGACY_LOCAL_SCANNERS = "true";
  globalThis.fetch = async () => new Response(JSON.stringify({
    user_id: "user-1",
    tenant_id: tenantId,
    role,
    email: "operator@example.test",
    auth_type: "jwt",
    pat_id: null,
    scopes: [],
  }), { status: 200 });
  try {
    return await run();
  } finally {
    globalThis.fetch = previousFetch;
    if (previousLocalScannerFlag === undefined) {
      delete process.env.ENABLE_LEGACY_LOCAL_SCANNERS;
    } else {
      process.env.ENABLE_LEGACY_LOCAL_SCANNERS = previousLocalScannerFlag;
    }
  }
}

describe("local scanner authorization boundary", () => {
  for (const [name, handler] of POST_ROUTES) {
    test(`${name} rejects unauthenticated process launch`, async () => {
      const response = await handler(postRequest(name));
      assert.equal(response.status, 401);
    });
  }

  test("scanner status and event routes reject unauthenticated access", async () => {
    const routes = [
      openVASGet(
        new NextRequest("http://localhost/api/scan/openvas/task"),
        { params: Promise.resolve({ taskId: "task" }) },
      ),
      pipelineGet(
        new NextRequest("http://localhost/api/scan/pipeline/scan"),
        { params: Promise.resolve({ scanId: "scan" }) },
      ),
      scanStreamGet(
        new NextRequest("http://localhost/api/scan/stream/scan"),
        { params: Promise.resolve({ scanId: "scan" }) },
      ),
    ];
    for (const response of await Promise.all(routes)) {
      assert.equal(response.status, 401);
    }
  });

  test("read-only backend roles cannot start a local scanner", async () => {
    const response = await withIdentity("auditor", async () => {
      const handler = withVerifiedBackend(async () => NextResponse.json({ ok: true }));
      return handler(postRequest("test", "valid-token"));
    });
    assert.equal(response.status, 403);
  });

  test("authenticated local scanner launch is disabled by default", async () => {
    const previousFetch = globalThis.fetch;
    const previousLocalScannerFlag = process.env.ENABLE_LEGACY_LOCAL_SCANNERS;
    delete process.env.ENABLE_LEGACY_LOCAL_SCANNERS;
    globalThis.fetch = async () => new Response(JSON.stringify({
      user_id: "user-1",
      tenant_id: "tenant-1",
      role: "tester",
      email: "operator@example.test",
      auth_type: "jwt",
      pat_id: null,
      scopes: [],
    }), { status: 200 });
    try {
      const response = await nmapPost(postRequest("nmap", "valid-token"));
      assert.equal(response.status, 503);
    } finally {
      globalThis.fetch = previousFetch;
      if (previousLocalScannerFlag === undefined) {
        delete process.env.ENABLE_LEGACY_LOCAL_SCANNERS;
      } else {
        process.env.ENABLE_LEGACY_LOCAL_SCANNERS = previousLocalScannerFlag;
      }
    }
  });

  test("Nmap rejects option, script, and port injection before spawning", async () => {
    const invalidBodies = [
      { target: "-iL,/etc/passwd", scanType: "quick" },
      { target: "127.0.0.1", scanType: "quick", scripts: ["../../tmp/evil.nse"] },
      { target: "127.0.0.1", scanType: "targeted", ports: "80,--script=unsafe" },
    ];
    for (const body of invalidBodies) {
      const response = await withIdentity("tester", () => nmapPost(new NextRequest(
        "http://localhost/api/scan/nmap",
        {
          method: "POST",
          headers: {
            authorization: "Bearer valid-token",
            "content-type": "application/json",
          },
          body: JSON.stringify(body),
        },
      )));
      assert.equal(response.status, 400);
    }
  });

  test("pipeline refuses unused credentials instead of retaining them", async () => {
    const response = await withIdentity("tester", () => pipelinePost(new NextRequest(
      "http://localhost/api/scan/pipeline",
      {
        method: "POST",
        headers: {
          authorization: "Bearer valid-token",
          "content-type": "application/json",
        },
        body: JSON.stringify({
          targets: ["127.0.0.1"],
          credentials: { username: "admin", password: "secret" },
        }),
      },
    )));
    assert.equal(response.status, 400);
  });

  test("OpenVAS task polling is tenant isolated", async () => {
    setTask("task-other-tenant", {
      taskId: "task-other-tenant",
      ownerTenantId: "tenant-2",
      ownerUserId: "user-2",
      status: "done",
      progress: 100,
      findings: [],
    });
    const response = await withIdentity("manager", () => openVASGet(
      new NextRequest("http://localhost/api/scan/openvas/task-other-tenant", {
        headers: { authorization: "Bearer valid-token" },
      }),
      { params: Promise.resolve({ taskId: "task-other-tenant" }) },
    ));
    assert.equal(response.status, 404);
  });
});
