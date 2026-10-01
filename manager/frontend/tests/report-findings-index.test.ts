import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { buildFindingsIndex } from "../lib/report/findings-index";

describe("buildFindingsIndex", () => {
  test("preserves order, builds refs, and formats cvss/epss/sla/severity", () => {
    const rows = buildFindingsIndex([
      { id: "a", title: "SQLi", severity: "critical", status: "OPEN", cvss_score: 9.8, epss_score: 0.97, current_sla: { hours_remaining: 10 } },
      { id: "b", title: "Info leak", severity: "low", status: "OPEN" },
    ]);
    assert.equal(rows.length, 2);
    assert.deepEqual([rows[0].ref, rows[1].ref], ["F001", "F002"]);
    assert.equal(rows[0].severity, "CRITICAL");
    assert.equal(rows[0].cvss, "9.8");
    assert.equal(rows[0].epss, "97%");
    assert.equal(rows[0].sla.tone, "warn");
    assert.equal(rows[0].id, "a");
  });

  test("absent fields render em-dash / none", () => {
    const [row] = buildFindingsIndex([{ id: "b", title: "x", severity: "low", status: "OPEN" }]);
    assert.equal(row.cvss, "—");
    assert.equal(row.epss, "—");
    assert.equal(row.sla.tone, "none");
    assert.equal(row.severity, "LOW");
  });

  test("string cvss_score is coerced", () => {
    const [row] = buildFindingsIndex([{ id: "c", title: "y", severity: "high", status: "OPEN", cvss_score: "7.5" }]);
    assert.equal(row.cvss, "7.5");
  });
});
