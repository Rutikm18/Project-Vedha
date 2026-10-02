import { test } from "node:test";
import assert from "node:assert/strict";
import {
  applyCustomerDefaults, formatPolicyError, hoursFromInput, isoToLocalInput, listFromText,
  localInputToIso, newBlackout, textFromList, windowSummary, type BlackoutWindow,
} from "../lib/org-settings";

test("lists come from lines or commas, trimmed, with blanks dropped", () => {
  assert.deepEqual(listFromText(" 10.0.0.0/8 \n\n192.168.1.5, 172.16.0.0/12 ,"), ["10.0.0.0/8", "192.168.1.5", "172.16.0.0/12"]);
  assert.deepEqual(listFromText(""), []);
  assert.equal(textFromList(["a", "b"]), "a\nb");
});

test("an hours field is empty (no limit), a whole number, or invalid", () => {
  assert.equal(hoursFromInput(""), null);
  assert.equal(hoursFromInput("  "), null);
  assert.equal(hoursFromInput("8"), 8);
  for (const bad of ["1.5", "-2", "abc", "8h"]) assert.ok(Number.isNaN(hoursFromInput(bad)), bad);
});

test("a one-off window round-trips through the browser's local input", () => {
  const iso = localInputToIso("2026-10-10T09:30");
  assert.ok(iso && iso.endsWith("Z"));
  assert.equal(isoToLocalInput(iso), "2026-10-10T09:30");
  assert.equal(localInputToIso(""), null);
  assert.equal(localInputToIso("garbage"), null);
  assert.equal(isoToLocalInput(null), "");
});

test("window summaries read naturally", () => {
  const weekly: BlackoutWindow = { ...newBlackout("Asia/Kolkata"), days: [4, 0], start: "18:00", end: "23:00" };
  assert.equal(windowSummary(weekly), "Mon, Fri, 18:00 to 23:00 (Asia/Kolkata)");
});

test("a new window starts as a sensible weekly one", () => {
  const w = newBlackout("UTC");
  assert.deepEqual([w.kind, w.timezone, w.days, w.start, w.end], ["weekly", "UTC", [4], "18:00", "23:00"]);
});

test("server validation errors become one sentence per problem", () => {
  const raw = JSON.stringify([
    { field: "ip_allowlist", message: "Value error, IP allowlist: 'nope' is not a valid CIDR or address" },
    { field: "blackouts.0.days", message: "a weekly window needs one or more distinct days" },
    { field: "operator_session_max_hours", message: "Input should be greater than or equal to 1" },
  ]);
  assert.deepEqual(formatPolicyError(raw), [
    "Allowed networks: IP allowlist: 'nope' is not a valid CIDR or address",
    "Blackout windows (0 days): a weekly window needs one or more distinct days",
    "Operator session limit: Input should be greater than or equal to 1",
  ]);
  assert.deepEqual(formatPolicyError("Forbidden"), ["Forbidden"]);
  assert.deepEqual(formatPolicyError("[]"), ["[]"]);
});

test("organisation defaults seed a new customer's plan draft without sharing arrays", () => {
  const defaults = { poc_locked_severities: ["critical"] as const, poc_locked_features: ["reports"] as const, poc_duration_days: 30, support_contact: "" };
  const draft = { lockedSeverities: ["critical", "high"], lockedFeatures: [] as string[], durationDays: 14, plan: "poc" };
  const out = applyCustomerDefaults(draft, { ...defaults, poc_locked_severities: [...defaults.poc_locked_severities], poc_locked_features: [...defaults.poc_locked_features] });
  assert.deepEqual([out.lockedSeverities, out.lockedFeatures, out.durationDays, out.plan], [["critical"], ["reports"], 30, "poc"]);
  assert.notEqual(out.lockedSeverities, draft.lockedSeverities);
});
