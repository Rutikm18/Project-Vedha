import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { NextRequest } from "next/server";

import { parseNetExecLog } from "../lib/netexec-parser";
import { parseOpenVASHelperOutput } from "../lib/openvas-client";
import { parseWhatWebOutput } from "../lib/whatweb-parser";
import {
  validateNetExecScanRequest,
  validateOpenVASScanRequest,
} from "../lib/scanner-request-validation";
import { POST as openVASPost } from "../app/api/scan/openvas/route";
import { GET as openVASGet } from "../app/api/scan/openvas/[taskId]/route";
import { POST as netExecPost } from "../app/api/scan/netexec/route";


describe("NetExec log parser", () => {
  test("parses supported SMB discovery output without inventing fields", () => {
    const output = [
      "SMB  192.168.61.5  445  DESKTOP-01  [*] Windows 10 Build 19041 x64 (name:DESKTOP-01) (domain:LAB) (signing:False) (SMBv1:True)",
    ].join("\n");

    const parsed = parseNetExecLog(output);

    assert.equal(parsed.discoveryLines, 1);
    assert.equal(parsed.recognizedDiscoveryLines, 1);
    assert.equal(parsed.status, "ok");
    assert.deepEqual(parsed.hosts, [{
      host: "192.168.61.5",
      hostname: "DESKTOP-01",
      domain: "LAB",
      os: "Windows 10 Build 19041 x64",
      signing: false,
      smbv1: true,
    }]);
  });

  test("keeps unknown SMB booleans undefined", () => {
    const parsed = parseNetExecLog(
      "SMB 10.0.0.2 445 HOST [*] Windows Server (name:HOST) (domain:LAB) (signing:None) (SMBv1:None)",
    );

    assert.equal(parsed.hosts[0].signing, undefined);
    assert.equal(parsed.hosts[0].smbv1, undefined);
  });

  test("marks only a successful null-auth line as a null session", () => {
    const output = [
      "SMB 10.0.0.3 445 FILE01 [*] Windows Server (name:FILE01) (domain:LAB) (signing:True) (SMBv1:False)",
      "SMB 10.0.0.3 445 FILE01 [*] Enumerated shares",
      "SMB 10.0.0.3 445 FILE01 [+] LAB\\:",
    ].join("\n");

    const parsed = parseNetExecLog(output, { successfulAuthIsNullSession: true });

    assert.equal(parsed.hosts[0].nullSession, true);
    assert.equal(parsed.candidateDiscoveryLines, 2);
    assert.equal(parsed.recognizedDiscoveryLines, 1);
    assert.equal(parsed.ignoredInformationalLines, 1);
    assert.equal(parsed.status, "ok");
  });

  test("reports a prefix-matched but unrecognized host line as schema mismatch", () => {
    const parsed = parseNetExecLog(
      "SMB 10.0.0.4 445 FILE02 [*] Windows Server name=FILE02 domain=LAB signing=False smbv1=False",
    );

    assert.equal(parsed.candidateDiscoveryLines, 1);
    assert.equal(parsed.recognizedDiscoveryLines, 0);
    assert.equal(parsed.unrecognizedDiscoveryLines, 1);
    assert.equal(parsed.status, "schema_mismatch");
    assert.deepEqual(parsed.hosts, []);
  });

  test("retains known hosts but marks mixed schemas degraded", () => {
    const output = [
      "SMB 10.0.0.5 445 FILE03 [*] Windows Server (name:FILE03) (domain:LAB) (signing:True) (SMBv1:False)",
      "SMB 10.0.0.6 445 FILE04 [*] Windows Server name=FILE04 domain=LAB signing=False smbv1=False",
    ].join("\n");
    const parsed = parseNetExecLog(output);

    assert.equal(parsed.hosts.length, 1);
    assert.equal(parsed.unrecognizedDiscoveryLines, 1);
    assert.equal(parsed.status, "degraded");
  });
});


describe("scanner request validation", () => {
  const openVASDefaults = {
    gvmHost: "openvas.internal",
    gvmPort: 9390,
    gvmUser: "scanner",
  };

  test("validates and normalizes every OpenVAS request field", () => {
    const result = validateOpenVASScanRequest({
      targets: [" 10.0.0.1 ", "10.0.0.1"],
      scanConfig: "full-fast",
      createFindings: true,
    }, openVASDefaults);

    assert.equal(result.ok, true);
    if (result.ok) {
      assert.deepEqual(result.value.targets, ["10.0.0.1"]);
      assert.equal(result.value.gvmHost, "openvas.internal");
      assert.equal(result.value.gvmPort, 9390);
      assert.equal(result.value.gvmUser, "scanner");
      assert.equal(result.value.createFindings, true);
    }
  });

  test("rejects caller-controlled OpenVAS connection identity", () => {
    for (const override of [
      { gvmPort: 9391 },
      { gvmHost: "attacker.example" },
      { gvmUser: "other-user" },
    ]) {
      const result = validateOpenVASScanRequest(
        { targets: ["10.0.0.1"], ...override },
        openVASDefaults,
      );
      assert.equal(result.ok, false);
    }
  });

  test("rejects invalid OpenVAS request field types", () => {
    assert.equal(validateOpenVASScanRequest({
      targets: ["10.0.0.1"], scanConfig: "unknown",
    }, openVASDefaults).ok, false);
    assert.equal(validateOpenVASScanRequest({
      targets: ["10.0.0.1"],
      createFindings: "yes",
    }, openVASDefaults).ok, false);
    assert.equal(validateOpenVASScanRequest({
      targets: ["999.0.0.1"],
    }, openVASDefaults).ok, false);
  });

  test("classifies an invalid OpenVAS environment default as configuration failure", () => {
    const result = validateOpenVASScanRequest(
      { targets: ["10.0.0.1"] },
      { ...openVASDefaults, gvmPort: Number.NaN },
    );

    assert.equal(result.ok, false);
    if (result.ok === false) assert.equal(result.source, "configuration");
  });

  test("rejects empty or unsupported NetExec checks", () => {
    assert.equal(validateNetExecScanRequest({
      targets: ["10.0.0.1"],
      checks: [],
    }).ok, false);
    assert.equal(validateNetExecScanRequest({
      targets: ["10.0.0.1"],
      checks: ["smb", "unsupported"],
    }).ok, false);
  });

  test("rejects invalid NetExec credential combinations and field types", () => {
    assert.equal(validateNetExecScanRequest({
      targets: ["10.0.0.1"],
      username: "operator",
      checks: ["smb"],
    }).ok, false);
    assert.equal(validateNetExecScanRequest({
      targets: ["10.0.0.1"],
      checks: ["shares"],
    }).ok, false);
    assert.equal(validateNetExecScanRequest({
      targets: ["10.0.0.1"],
      username: 7,
      password: "secret",
      checks: ["smb"],
    }).ok, false);
  });

  test("accepts a supported NetExec request and safe default checks", () => {
    const result = validateNetExecScanRequest({
      targets: ["FILE01", "10.0.0.0/24"],
    });

    assert.equal(result.ok, true);
    if (result.ok) {
      assert.deepEqual(result.value.checks, ["smb", "null-session"]);
    }
  });
});


describe("scanner route authentication", () => {
  const token = "manager-access-token";

  function unauthenticatedPost(url: string): NextRequest {
    return new NextRequest(url, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: "{}",
    });
  }

  function authenticatedPost(url: string, body: unknown): NextRequest {
    return new NextRequest(url, {
      method: "POST",
      headers: {
        authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
      body: JSON.stringify(body),
    });
  }

  async function withManagerIdentity(run: () => Promise<Response>): Promise<Response> {
    const previousFetch = globalThis.fetch;
    const previousLocalScannerFlag = process.env.ENABLE_LEGACY_LOCAL_SCANNERS;
    process.env.ENABLE_LEGACY_LOCAL_SCANNERS = "true";
    globalThis.fetch = async (input) => {
      assert.match(String(input), /\/auth\/me$/);
      return new Response(JSON.stringify({
        user_id: "user-1",
        tenant_id: "tenant-1",
        role: "manager",
        email: "you@yourorg.com",
        auth_type: "jwt",
        pat_id: null,
        scopes: [],
      }), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };
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

  test("OpenVAS launch rejects a request without bearer authentication", async () => {
    const response = await openVASPost(
      unauthenticatedPost("http://localhost/api/scan/openvas"),
    );
    assert.equal(response.status, 401);
  });

  test("OpenVAS polling rejects a request without bearer authentication", async () => {
    const response = await openVASGet(
      new NextRequest("http://localhost/api/scan/openvas/task-1"),
      { params: Promise.resolve({ taskId: "task-1" }) },
    );
    assert.equal(response.status, 401);
  });

  test("NetExec launch rejects a request without bearer authentication", async () => {
    const response = await netExecPost(
      unauthenticatedPost("http://localhost/api/scan/netexec"),
    );
    assert.equal(response.status, 401);
  });

  test("OpenVAS route rejects a non-integer port before launching", async () => {
    const response = await withManagerIdentity(() => openVASPost(authenticatedPost(
      "http://localhost/api/scan/openvas",
      { targets: ["10.0.0.1"], gvmPort: "9390" },
    )));
    assert.equal(response.status, 400);
  });

  test("NetExec route rejects an unsupported check before launching", async () => {
    const response = await withManagerIdentity(() => netExecPost(authenticatedPost(
      "http://localhost/api/scan/netexec",
      { targets: ["10.0.0.1"], checks: ["unsupported"] },
    )));
    assert.equal(response.status, 400);
  });
});


describe("WhatWeb output parser", () => {
  test("parses the JSON array emitted by --log-json=-", () => {
    const parsed = parseWhatWebOutput(JSON.stringify([
      {
        target: "https://example.test",
        plugins: { nginx: { version: ["1.24"] }, HTTPServer: {} },
      },
    ]));

    assert.equal(parsed.results.length, 1);
    assert.equal(parsed.invalidEntries, 0);
    assert.equal(parsed.results[0].target, "https://example.test");
  });

  test("reports schema-invalid entries while retaining valid entries", () => {
    const parsed = parseWhatWebOutput(JSON.stringify([
      { target: "https://example.test", plugins: { nginx: {} } },
      { target: "https://broken.test" },
    ]));

    assert.equal(parsed.results.length, 1);
    assert.equal(parsed.invalidEntries, 1);
  });

  test("rejects malformed and non-array output", () => {
    assert.throws(() => parseWhatWebOutput("{bad json"), /malformed JSON/);
    assert.throws(
      () => parseWhatWebOutput(JSON.stringify({ target: "https://example.test", plugins: {} })),
      /must be an array/,
    );
  });
});


describe("OpenVAS helper envelope", () => {
  test("accepts an explicit done response", () => {
    const findings = parseOpenVASHelperOutput(JSON.stringify({
      status: "done",
      findings: [],
    }));

    assert.deepEqual(findings, []);
  });

  test("surfaces readiness and terminal helper failures", () => {
    assert.throws(
      () => parseOpenVASHelperOutput(JSON.stringify({
        status: "error",
        reason: "RuntimeError",
        error: "scan config is unavailable; feed import has not completed",
      })),
      /feed import has not completed/,
    );
  });

  test("rejects missing terminal state and malformed JSON", () => {
    assert.throws(
      () => parseOpenVASHelperOutput(JSON.stringify({ findings: [] })),
      /terminal status/,
    );
    assert.throws(() => parseOpenVASHelperOutput("not-json"), /malformed JSON/);
    assert.throws(
      () => parseOpenVASHelperOutput(JSON.stringify({
        status: "done",
        findings: [{ title: "missing required fields" }],
      })),
      /invalid finding/,
    );
  });
});
