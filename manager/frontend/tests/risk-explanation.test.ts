import { test } from "node:test";
import assert from "node:assert/strict";
import {
  bandSentence, defaultsSummary, formatInputValue, formatPoints, placementSentence,
  type RiskDimension, type RiskExplanation, type RiskInput,
} from "../lib/risk-explanation";

const input = (over: Partial<RiskInput> = {}): RiskInput => ({
  key: "cvss", label: "CVSS", raw: 9.8, normalized: 0.98, weight: 0.8, contribution: 0.784,
  source: "recorded", note: "", ...over,
});

const dim = (over: Partial<RiskDimension> = {}): RiskDimension => ({
  key: "impact", label: "Impact", weight: 0.4, value: 0.9, points: 360, inputs: [input()], ...over,
});

const explanation = (over: Partial<RiskExplanation> = {}): RiskExplanation => ({
  model_version: "risk-rank-v1", score: 911, max: 1000, severity: "critical",
  dimensions: [dim()], additive_score: 806, band: { floor: 750, ceiling: 1000, position: 0.6452 },
  placement: { formula: "", result: 911 }, defaults_used: [],
  context: { asset: null, internet_exposure_source: "not recorded", service_exposure: null },
  stored_score: 911, stored_in_sync: true,
  priority: { priority: "P1", label: "Urgent", rule: "critical", reason: "", inputs: {}, rules: [] },
  ...over,
});

test("recorded values are worded, defaults are never shown as data", () => {
  assert.equal(formatInputValue(input()), "9.8 / 10");
  assert.equal(formatInputValue(input({ key: "epss", raw: 0.0312 })), "3.1% chance of exploitation");
  assert.equal(formatInputValue(input({ key: "kev", raw: true })), "Listed");
  assert.equal(formatInputValue(input({ key: "auth_gap", raw: false })), "Authentication enforced");
  assert.equal(formatInputValue(input({ key: "asset_criticality", raw: "high" })), "High");
  assert.equal(formatInputValue(input({ raw: null, source: "default" })), "Not recorded");
  assert.equal(formatInputValue(input({ raw: 5, source: "default" })), "Not recorded");
});

test("points carry an explicit sign and one decimal", () => {
  assert.equal(formatPoints(360), "+360.0");
  assert.equal(formatPoints(12.345), "+12.3");
});

test("defaults summary lists what was assumed, and is silent when nothing was", () => {
  assert.equal(defaultsSummary(explanation()), null);
  const one = explanation({ dimensions: [dim({ inputs: [input({ key: "epss", label: "EPSS", source: "default", raw: null })] })] });
  assert.match(defaultsSummary(one) ?? "", /^1 input was not recorded for this finding \(epss\)/);
  const three = explanation({
    dimensions: [dim({ inputs: ["A", "B", "C"].map((label) => input({ label, source: "default", raw: null })) })],
  });
  assert.match(defaultsSummary(three) ?? "", /3 inputs were not recorded .*\(a, b and c\)/);
});

test("the band and placement sentences use the server's numbers", () => {
  const e = explanation();
  assert.equal(placementSentence(e), "750 + 0.6452 × (1000 − 750) = 911");
  assert.match(bandSentence(e), /^Critical findings are ranked between 750 and 1000/);
});
