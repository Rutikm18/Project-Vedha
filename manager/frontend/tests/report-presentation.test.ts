import assert from "node:assert/strict";
import { describe, test } from "node:test";

import {
  closureView,
  compactRefs,
  evidenceView,
  excerpt,
  findingFacts,
  findingNarrative,
  findingRefs,
  formatHours,
  gapInventory,
  keyMetrics,
  mask,
  orderFindings,
  overallRating,
  readable,
  readableText,
  remediationRoadmap,
  remediationView,
  severityRows,
  statusRows,
  topRisks,
} from "../lib/report/presentation";
import { canonicalReport } from "./fixtures/canonical-report";
import { mixedReport } from "./fixtures/mixed-report";

describe("report presentation layer", () => {
  test("orders most severe first, open before closed, then by risk", () => {
    const titles = orderFindings(mixedReport.findings).map((f) => f.title);
    assert.deepEqual(titles, [
      "Critical open finding",
      "Second critical open finding",
      "High open finding",
      "High closed finding",
      "Medium open finding",
      "Sparse informational finding",
    ]);
    const refs = findingRefs(mixedReport);
    assert.equal(refs.get("f0000000-0000-4000-8000-000000000002"), "F001");
    assert.equal(refs.get("f0000000-0000-4000-8000-000000000006"), "F006");
  });

  test("rates the engagement by its highest open severity and says why", () => {
    const rating = overallRating(mixedReport);
    assert.equal(rating.level, "critical");
    assert.equal(rating.label, "Critical");
    assert.match(rating.basis, /5 open findings: 2 critical/);

    const closed = overallRating(canonicalReport);
    assert.equal(closed.level, "none");
    assert.match(closed.basis, /All 2 recorded findings have a closing disposition/);
  });

  test("counts severities, statuses and key metrics from the findings", () => {
    const rows = severityRows(mixedReport);
    assert.deepEqual(rows.find((r) => r.severity === "high"), { severity: "high", total: 2, open: 1, closed: 1 });
    assert.deepEqual(statusRows(mixedReport).map((r) => r.label), ["Open", "Confirmed", "Remediated"]);
    const m = keyMetrics(mixedReport);
    assert.equal(m.total, 6);
    assert.equal(m.open, 5);
    assert.equal(m.criticalHighOpen, 3);
    assert.equal(m.exploitableOpen, 1);
    assert.equal(m.slaBreached, 1);
    assert.equal(m.slaAtRisk, 1);
  });

  test("builds a roadmap from open findings with targets only from the recorded SLA", () => {
    const roadmap = remediationRoadmap(mixedReport);
    assert.deepEqual(roadmap.map((b) => b.priority), [1, 2, 3, 4]);
    assert.equal(roadmap[0]!.items.length, 2);
    assert.equal(roadmap[0]!.target, "within 3 days of discovery (current SLA policy)");
    assert.equal(roadmap[1]!.target, "within 7 days of discovery (current SLA policy)");
    // The sparse finding has no SLA window, so no target is invented.
    assert.equal(roadmap[3]!.target, null);
    assert.ok(roadmap.every((b) => b.items.every((i) => i.title !== "High closed finding")));
  });

  test("lists top open risks with their references", () => {
    assert.deepEqual(topRisks(mixedReport, 2).map((r) => r.ref), ["F001", "F002"]);
  });

  test("keeps only recorded facts and narrative, and names what is missing", () => {
    const sparse = mixedReport.findings.find((f) => f.title.startsWith("Sparse"))!;
    assert.deepEqual(findingFacts(sparse), []);
    const narrative = findingNarrative(sparse);
    assert.equal(narrative.sections.length, 0);
    assert.equal(narrative.missing.length, 8);

    const rich = canonicalReport.findings[0]!;
    const facts = findingFacts(rich);
    assert.ok(facts.some((f) => f.label === "Affected asset"));
    const full = findingNarrative(rich);
    assert.deepEqual(full.missing, []);
    const steps = full.sections.find((s) => s.key === "reproduction_steps")!;
    assert.deepEqual(steps.body, { kind: "list", items: ["Offer TLS 1.0", "Observe a successful handshake"] });
  });

  test("renders recorded objects as readable rows, never raw JSON, and drops raw payloads", () => {
    const r = readable({ zone: "external", raw: { secret: "must-not-render" }, ports: [443, 8443] });
    assert.deepEqual(r, { kind: "pairs", rows: [["Zone", "external"], ["Ports", "443, 8443"]] });
    assert.equal(readableText(["a", "b"]), "• a\n• b");
    assert.equal(readable(""), null);
    assert.equal(readable(null), null);
  });

  test("masks secrets everywhere and keeps existing placeholders", () => {
    assert.doesNotMatch(mask("password=hunter2-secret-value"), /hunter2-secret-value/);
    assert.equal(mask("[REDACTED: credential] stays"), "[REDACTED: credential] stays");
    const description = findingNarrative(canonicalReport.findings[0]!).sections[0]!;
    assert.doesNotMatch(JSON.stringify(description), /description-secret-report-value/);
    const artifact = evidenceView(canonicalReport.findings[0]!.evidence.artifacts[0]!, "F001/E01");
    assert.doesNotMatch(artifact.content, /evidence-secret-report-value/);
  });

  test("de-duplicates remediation recommendations", () => {
    const view = remediationView(canonicalReport.findings[0]!);
    assert.equal(view.text, "Disable TLS 1.0.");
    assert.equal(new Set(view.recommendations.map((r) => r.toLowerCase())).size, view.recommendations.length);
    assert.ok(view.plans[0]!.steps.length > 0);
  });

  test("summarises closure and retest per finding", () => {
    const c = closureView(canonicalReport.findings[0]!);
    assert.equal(c.disposition, "Remediated");
    assert.equal(c.retest, "Passed");
    assert.equal(c.closed, true);
  });

  test("de-duplicates record gaps and maps finding ids to references", () => {
    const gaps = gapInventory(mixedReport);
    assert.deepEqual(gaps.reportLevel.map((g) => g.code), ["report_methodology_absent"]);
    const closure = gaps.findingLevel.find((g) => g.code === "closure_review_metadata_absent")!;
    assert.equal(closure.count, 2);
    assert.deepEqual(closure.refs, ["F004", "F005"]);
    assert.equal(compactRefs(["F001", "F002", "F003", "F005", "F006"]), "F001–F003, F005, F006");
  });

  test("formats SLA windows and evidence excerpts honestly", () => {
    assert.equal(formatHours(72), "3 days");
    assert.equal(formatHours(36), "36 hours");
    const long = Array.from({ length: 50 }, (_, i) => `line ${i + 1}`).join("\n");
    const cut = excerpt(long, 10);
    assert.equal(cut.truncated, true);
    assert.equal(cut.shownLines, 10);
    assert.equal(cut.totalLines, 50);
  });
});

describe("report dates", () => {
  test("formats instants in the display zone with fixed month names", async () => {
    const { formatDate, formatDateTime } = await import("../lib/report/presentation");
    assert.equal(formatDate("2026-09-26T20:00:00Z", "Asia/Kolkata"), "27 Sep 2026");
    assert.equal(formatDate("2026-09-05"), "05 Sep 2026");
    assert.match(formatDateTime("2026-09-26T08:30:00Z", "Asia/Kolkata")!, /^26 Sep 2026, 14:00 /);
  });
});
