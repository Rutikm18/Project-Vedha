import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { presentEvidence } from "../lib/evidence-presentation";

describe("finding evidence presentation", () => {
  test("formats structured scanner evidence for line-by-line review", () => {
    const result = presentEvidence({
      label: "Scanner response",
      content: JSON.stringify({ port: 443, service: "https" }),
    });

    assert.equal(result.kind, "JSON");
    assert.match(result.copyText, /"port": 443/);
    assert.ok(result.lines.length > 1);
    assert.equal(result.truncated, false);
  });

  test("masks credentials in both captured output and collection commands", () => {
    const result = presentEvidence({
      label: "HTTP response",
      content: "Authorization: Bearer abcdefghijklmnop",
      command: "curl -H 'Authorization: Bearer abcdefghijklmnop' https://example.test",
    });

    assert.doesNotMatch(result.copyText, /abcdefghijklmnop/);
    assert.doesNotMatch(result.command ?? "", /abcdefghijklmnop/);
    assert.ok(result.redactions >= 2);
  });

  test("shows only recorded provenance and uses a stable UTC timestamp", () => {
    const result = presentEvidence({
      label: "Probe output",
      content: "443/tcp open",
      tool: "nmap",
      timestamp: "2026-09-06T12:30:00Z",
      sourceHost: "probe-01",
    });

    assert.deepEqual(result.provenance.map((item) => item.label), ["Tool", "Captured", "Source"]);
    assert.equal(result.provenance[1]?.value, "2026-09-06 12:30:00 UTC");
  });

  test("bounds long output without weakening the complete masked copy", () => {
    const content = Array.from({ length: 205 }, (_, index) => `line ${index + 1}`).join("\n");
    const result = presentEvidence({ label: "Terminal output", content });

    assert.equal(result.visibleLines.length, 200);
    assert.equal(result.lines.length, 205);
    assert.equal(result.truncated, true);
    assert.match(result.copyText, /line 205$/);
  });
});
