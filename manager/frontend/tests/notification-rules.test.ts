import { test } from "node:test";
import assert from "node:assert/strict";
import {
  changedEvents, effectiveRule, hasNoChannel, savePayload, setEnabled, toggleChannel,
  type NotificationRule, type RuleDraft,
} from "../lib/notification-rules";

const rule = (over: Partial<NotificationRule> = {}): NotificationRule => ({
  event: "critical_finding", label: "Critical finding opened", cadence: "Immediate",
  enabled: true, channels: ["email", "slack"], connected: true, is_custom: false, ...over,
});
const rules = [
  rule(),
  rule({ event: "high_finding", label: "High finding opened", channels: ["slack"] }),
  rule({ event: "coverage_gap", enabled: false, channels: ["email"], connected: false }),
];

test("with no draft every rule shows what the server holds", () => {
  assert.deepEqual(effectiveRule(rules[0], {}), rules[0]);
  assert.deepEqual(changedEvents(rules, {}), []);
});

test("toggling a channel off and back on is not a change", () => {
  let d: RuleDraft = toggleChannel(rules[0], {}, "slack");
  assert.deepEqual(effectiveRule(rules[0], d).channels, ["email"]);
  assert.deepEqual(changedEvents(rules, d), ["critical_finding"]);
  d = toggleChannel(rules[0], d, "slack");
  assert.deepEqual(effectiveRule(rules[0], d).channels, ["email", "slack"]);
  assert.deepEqual(changedEvents(rules, d), []);
});

test("adding a channel keeps the canonical order", () => {
  const d = toggleChannel(rules[1], {}, "email");
  assert.deepEqual(effectiveRule(rules[1], d).channels, ["email", "slack"]);
});

test("turning a rule off keeps its channels, and only that rule is saved", () => {
  const d = setEnabled(rules[0], {}, false);
  assert.equal(effectiveRule(rules[0], d).enabled, false);
  assert.deepEqual(effectiveRule(rules[0], d).channels, ["email", "slack"]);
  assert.deepEqual(savePayload(rules, d), {
    rules: [{ event: "critical_finding", enabled: false, channels: ["email", "slack"] }],
  });
});

test("edits to different rules stack and are saved together", () => {
  let d = setEnabled(rules[2], {}, true);
  d = toggleChannel(rules[1], d, "slack");
  assert.deepEqual(changedEvents(rules, d).sort(), ["coverage_gap", "high_finding"]);
  const payload = savePayload(rules, d);
  assert.equal(payload.rules.length, 2);
  assert.deepEqual(payload.rules.find((r) => r.event === "high_finding"), { event: "high_finding", enabled: true, channels: [] });
});

test("an enabled rule with no channel is flagged; a disabled one is not", () => {
  assert.equal(hasNoChannel(rule({ channels: [] })), true);
  assert.equal(hasNoChannel(rule({ enabled: false, channels: [] })), false);
  assert.equal(hasNoChannel(rule()), false);
});
