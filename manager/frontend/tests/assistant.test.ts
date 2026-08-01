import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { NextRequest } from "next/server";
import { cveRecordToFactCard, detectFindingId, toFactCard } from "../lib/assistant";
import { POST as brainPost } from "../app/api/brain/route";

describe("detectFindingId", () => {
  test("finds a UUID anywhere in pasted text", () => {
    const id = "3f9a1c2e-1b2c-4d5e-8f90-abcdef012345";
    assert.equal(detectFindingId(`please explain ${id} thanks`), id);
  });
  test("finds a CVE id", () => {
    assert.equal(detectFindingId("what about CVE-2024-3094?"), "CVE-2024-3094");
  });
  test("returns null when nothing looks like an id", () => {
    assert.equal(detectFindingId("explain the kerberoast finding"), null);
  });
});

describe("toFactCard", () => {
  const ui = {
    id: "3f9a1c2e-1b2c-4d5e-8f90-abcdef012345",
    title: "Unconstrained Delegation on DC01",
    severity: "CRITICAL", cvss: "9.8", cvssVector: "AV:N", category: "AD",
    status: "OPEN", affectedHost: "10.10.10.5", riskScore: 940,
    epssScore: 0.72, kevListed: true, activelyExploited: true,
    remediation: ["Remove unconstrained delegation from DC01"],
  };
  test("maps real fields into the fact card (no invented numbers)", () => {
    const fc = toFactCard(ui);
    assert.equal(fc.risk, 940);
    assert.equal(fc.kev, true);
    assert.equal(fc.epssPct, 72);
    assert.equal(fc.whatToDo, "Remove unconstrained delegation from DC01");
    assert.equal(fc.host, "10.10.10.5");
    assert.equal(fc.source, "finding");
    assert.deepEqual(fc.affectedAssets, ["10.10.10.5"]);
  });
  test("degrades gracefully when remediation is empty", () => {
    const fc = toFactCard({ ...ui, remediation: [] });
    assert.match(fc.whatToDo, /No remediation has been recorded/);
  });
});

describe("public CVE brief", () => {
  test("uses official record facts without claiming organizational exposure", () => {
    const card = cveRecordToFactCard({
      cveMetadata: { cveId: "CVE-2024-3094", state: "PUBLISHED" },
      containers: {
        cna: {
          descriptions: [{ lang: "en", value: "Malicious code was discovered in affected XZ Utils releases." }],
          affected: [{ vendor: "Tukaani", product: "XZ Utils" }],
          metrics: [{ cvssV3_1: { baseScore: 10, baseSeverity: "CRITICAL" } }],
          solutions: [{ lang: "en", value: "Downgrade to a known-good release." }],
          references: [{ name: "Vendor advisory", url: "https://example.test/advisory" }],
        },
      },
    }, "CVE-2024-3094");

    assert.equal(card.source, "cve");
    assert.equal(card.severity, "CRITICAL");
    assert.equal(card.cvss, "10");
    assert.match(card.whyItMatters, /has not confirmed/);
    assert.deepEqual(card.affectedAssets, []);
    assert.equal(card.remediationSteps[0], "Downgrade to a known-good release.");
  });

  test("provides safe validation steps when the public record has no solution", () => {
    const card = cveRecordToFactCard({
      cveMetadata: { cveId: "CVE-2025-12345", state: "PUBLISHED" },
      containers: { cna: { descriptions: [{ lang: "en", value: "Example vulnerability." }] } },
    }, "CVE-2025-12345");

    assert.equal(card.severity, "UNKNOWN");
    assert.match(card.remediationSteps[0], /Confirm whether/);
    assert.match(card.evidenceStatus, /not evidence/);
  });
});

describe("AI Brain authentication", () => {
  test("rejects an unauthenticated request before using an AI provider", async () => {
    const response = await brainPost(new NextRequest("http://localhost/api/brain", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        messages: [{ role: "user", content: "summarize current exposure" }],
      }),
    }));

    assert.equal(response.status, 401);
  });

  test("rejects an invalid engagement identifier before calling dependencies", async () => {
    const response = await brainPost(new NextRequest("http://localhost/api/brain", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "vedha_token=test-browser-session",
      },
      body: JSON.stringify({
        engagementId: "../../another-tenant",
        messages: [{ role: "user", content: "summarize current exposure" }],
      }),
    }));

    assert.equal(response.status, 400);
  });

  test("rejects conversations that exceed the aggregate context bound", async () => {
    const response = await brainPost(new NextRequest("http://localhost/api/brain", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "vedha_token=test-browser-session",
      },
      body: JSON.stringify({
        messages: Array.from({ length: 5 }, () => ({
          role: "user",
          content: "x".repeat(5_000),
        })),
      }),
    }));

    assert.equal(response.status, 400);
  });
});
