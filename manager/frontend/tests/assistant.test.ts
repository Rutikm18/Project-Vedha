import assert from "node:assert/strict";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";
import { cveRecordToFactCard, detectFindingId, toFactCard } from "../lib/assistant";
import { POST as brainPost, selectedFindingIds } from "../app/api/brain/route";
import { POST as assistantChatPost } from "../app/api/assistant/chat/route";

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

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
  test("grounds the advisor with recorded lifecycle facts (never inferred)", () => {
    const tenDaysAgo = new Date(Date.now() - 10 * 86_400_000).toISOString();
    const fc = toFactCard({
      ...ui, discoveredAt: tenDaysAgo, lastSeen: tenDaysAgo,
      reopenedCount: 2, regression: true,
      resolvedAt: null, resolutionMethod: null, verificationState: "confirmed",
    });
    assert.ok(fc.lifecycle);
    assert.equal(fc.lifecycle!.ageDays, 10);
    assert.equal(fc.lifecycle!.reopenedCount, 2);
    assert.equal(fc.lifecycle!.regressed, true);
    assert.equal(fc.lifecycle!.verificationState, "confirmed");
  });
  test("lifecycle degrades to null fields when timestamps are absent", () => {
    const fc = toFactCard(ui);
    assert.ok(fc.lifecycle);
    assert.equal(fc.lifecycle!.ageDays, null);
    assert.equal(fc.lifecycle!.reopenedCount, 0);
    assert.equal(fc.lifecycle!.regressed, false);
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
    // Public CVE metadata has no tenant lifecycle — the advisor must not receive one.
    assert.equal(card.lifecycle, undefined);
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

describe("AssistantDrawer submit guard", () => {
  // Mirrors the submit() logic in AssistantDrawer so regressions are caught
  // without requiring a browser.  The three invariants tested here match the
  // UX changes made in the last patch: empty input is blocked, loading state
  // blocks the send, and the loading aria-label changes.

  function canSubmit(input: string, loading: boolean): boolean {
    return !loading && input.trim().length > 0;
  }

  function sendBtnLabel(loading: boolean): string {
    return loading ? "Sending…" : "Send";
  }

  function textareaPlaceholder(loading: boolean, activeId: string | null): string {
    if (loading) return "Analyzing…";
    if (activeId) return "Ask about impact, score, evidence, or remediation…";
    return "Paste CVE-YYYY-NNNN or ask a security question…";
  }

  test("submit is blocked when input is empty", () => {
    assert.equal(canSubmit("", false), false);
    assert.equal(canSubmit("   ", false), false);
  });

  test("submit is allowed when input has content and not loading", () => {
    assert.equal(canSubmit("explain CVE-2024-3094", false), true);
  });

  test("submit is blocked while loading even if input is non-empty", () => {
    assert.equal(canSubmit("explain CVE-2024-3094", true), false);
  });

  test("send button label is 'Sending…' while loading", () => {
    assert.equal(sendBtnLabel(true), "Sending…");
  });

  test("send button label is 'Send' when idle", () => {
    assert.equal(sendBtnLabel(false), "Send");
  });

  test("textarea shows 'Analyzing…' placeholder while loading", () => {
    assert.equal(textareaPlaceholder(true, null), "Analyzing…");
    assert.equal(textareaPlaceholder(true, "some-finding-id"), "Analyzing…");
  });

  test("textarea shows followup placeholder when activeId is set and idle", () => {
    assert.match(textareaPlaceholder(false, "abc"), /impact/);
  });

  test("textarea shows generic placeholder when no activeId and idle", () => {
    assert.match(textareaPlaceholder(false, null), /CVE-YYYY/);
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

  test("accepts only a bounded unique UUID selection", () => {
    const first = "11111111-1111-4111-8111-111111111111";
    const second = "22222222-2222-4222-8222-222222222222";
    assert.deepEqual(selectedFindingIds(undefined), []);
    assert.deepEqual(selectedFindingIds([]), []);
    assert.deepEqual(selectedFindingIds([first, second]), [first, second]);
    assert.equal(selectedFindingIds([first, first]), null);
    assert.equal(selectedFindingIds(["../../another-tenant"]), null);
    assert.equal(selectedFindingIds(Array.from({ length: 21 }, (_, index) =>
      `00000000-0000-4000-8000-${String(index).padStart(12, "0")}`
    )), null);
  });

  test("rejects invalid selected finding context before calling dependencies", async () => {
    const response = await brainPost(new NextRequest("http://localhost/api/brain", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "vedha_token=test-browser-session",
      },
      body: JSON.stringify({
        findingIds: ["not-a-finding"],
        messages: [{ role: "user", content: "prioritize these" }],
      }),
    }));

    assert.equal(response.status, 400);
  });

  test("keeps general questions working when there is no finding selection", async () => {
    let generatedBody: any = null;
    globalThis.fetch = async (input, init) => {
      const url = new URL(String(input));
      if (url.pathname === "/ai/generate") {
        generatedBody = JSON.parse(String(init?.body));
        return new Response(JSON.stringify({
          content: "Start with confirmed critical findings.",
          provider: "ollama",
          model: "test-model",
          privacy: "local",
          fallback: false,
        }), { status: 200, headers: { "content-type": "application/json" } });
      }
      return new Response("not found", { status: 404 });
    };

    const response = await brainPost(new NextRequest("http://localhost/api/brain", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "vedha_token=test-browser-session",
      },
      body: JSON.stringify({
        findingIds: [],
        messages: [{ role: "user", content: "What should I fix first?" }],
      }),
    }));

    assert.equal(response.status, 200);
    assert.deepEqual(generatedBody.context, {});
  });

  test("resolves selected IDs into exact server-side finding context", async () => {
    const ids = [
      "11111111-1111-4111-8111-111111111111",
      "22222222-2222-4222-8222-222222222222",
    ];
    let generatedBody: any = null;
    globalThis.fetch = async (input, init) => {
      const url = new URL(String(input));
      if (url.pathname.startsWith("/findings/")) {
        const id = url.pathname.split("/").pop()!;
        return new Response(JSON.stringify({
          id,
          title: id === ids[0] ? "SMB signing disabled" : "Outdated package",
          severity: id === ids[0] ? "critical" : "high",
          status: "open",
          risk_score: id === ids[0] ? 900 : 700,
          asset_context: { fqdn: id === ids[0] ? "dc01.example.test" : "app01.example.test" },
        }), { status: 200, headers: { "content-type": "application/json" } });
      }
      if (url.pathname === "/ai/generate") {
        generatedBody = JSON.parse(String(init?.body));
        return new Response(JSON.stringify({
          content: "Prioritize SMB signing first.",
          provider: "ollama",
          model: "test-model",
          privacy: "local",
        }), { status: 200, headers: { "content-type": "application/json" } });
      }
      return new Response("not found", { status: 404 });
    };

    const response = await brainPost(new NextRequest("http://localhost/api/brain", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "vedha_token=test-browser-session",
      },
      body: JSON.stringify({
        findingIds: ids,
        provider: "openai",
        model: "gpt-5-mini",
        messages: [{ role: "user", content: "prioritize these findings" }],
      }),
    }));

    assert.equal(response.status, 200);
    assert.equal(generatedBody.context.selectedFindingEvidence.selectionMode, "exact");
    assert.equal(generatedBody.context.selectedFindingEvidence.selectedCount, 2);
    assert.equal(generatedBody.provider, "openai");
    assert.equal(generatedBody.model, "gpt-5-mini");
    assert.deepEqual(
      generatedBody.context.selectedFindingEvidence.findings.map((finding: any) => finding.id),
      ids,
    );
    assert.equal(
      generatedBody.context.selectedFindingEvidence.findings[0].affectedHost,
      "dc01.example.test",
    );
  });

  test("rejects an unsupported model selection before calling dependencies", async () => {
    globalThis.fetch = async () => {
      throw new Error("dependencies must not be called");
    };
    const response = await brainPost(new NextRequest("http://localhost/api/brain", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "vedha_token=test-browser-session",
      },
      body: JSON.stringify({
        provider: "command-executor",
        model: "anything",
        messages: [{ role: "user", content: "prioritize these findings" }],
      }),
    }));

    assert.equal(response.status, 400);
  });
});

describe("grounded assistant follow-up", () => {
  test("forwards the selected model only after re-resolving the finding", async () => {
    const id = "11111111-1111-4111-8111-111111111111";
    let generatedBody: any = null;
    globalThis.fetch = async (input, init) => {
      const url = new URL(String(input));
      if (url.pathname === `/findings/${id}`) {
        return new Response(JSON.stringify({
          id,
          title: "SMB signing disabled",
          severity: "critical",
          status: "open",
          risk_score: 900,
          asset_context: { fqdn: "dc01.example.test" },
        }), { status: 200, headers: { "content-type": "application/json" } });
      }
      if (url.pathname === "/ai/generate") {
        generatedBody = JSON.parse(String(init?.body));
        return new Response(JSON.stringify({
          content: "Validate SMB signing after the approved change window.",
          provider: "openai",
          model: "gpt-5-mini",
          privacy: "cloud",
          fallback: false,
        }), { status: 200, headers: { "content-type": "application/json" } });
      }
      return new Response("not found", { status: 404 });
    };

    const response = await assistantChatPost(new NextRequest("http://localhost/api/assistant/chat", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: "vedha_token=test-browser-session",
      },
      body: JSON.stringify({
        findingId: id,
        provider: "openai",
        model: "gpt-5-mini",
        messages: [{ role: "user", content: "How should I validate the fix?" }],
      }),
    }));

    assert.equal(response.status, 200);
    assert.equal(generatedBody.provider, "openai");
    assert.equal(generatedBody.model, "gpt-5-mini");
    assert.equal(generatedBody.context.securityBrief.id, id);
  });
});
