import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { formatSlaCountdown, epssPercent, exploitFlag } from "../lib/report/risk-band";

describe("formatSlaCountdown", () => {
  test("comfortable time remaining -> ok, shows days", () => {
    const r = formatSlaCountdown({ hours_remaining: 120 });
    assert.equal(r.tone, "ok");
    assert.equal(r.label, "5d left");
  });
  test("<= 48h remaining -> warn", () => {
    assert.equal(formatSlaCountdown({ hours_remaining: 10 }).tone, "warn");
    assert.equal(formatSlaCountdown({ hours_remaining: 10 }).label, "10h left");
  });
  test("negative hours -> overdue", () => {
    const r = formatSlaCountdown({ hours_remaining: -30 });
    assert.equal(r.tone, "overdue");
    assert.match(r.label, /^Overdue /);
  });
  test("no hours -> falls back to state; null -> none", () => {
    assert.equal(formatSlaCountdown({ state: "overdue" }).tone, "overdue");
    assert.equal(formatSlaCountdown({ state: "on_track" }).tone, "ok");
    assert.equal(formatSlaCountdown(null).tone, "none");
    assert.equal(formatSlaCountdown({}).tone, "none");
  });
});

describe("epssPercent", () => {
  test("fraction -> whole percent", () => assert.equal(epssPercent(0.97), "97%"));
  test("small fraction -> one decimal", () => assert.equal(epssPercent(0.023), "2.3%"));
  test("null/undefined -> null", () => {
    assert.equal(epssPercent(null), null);
    assert.equal(epssPercent(undefined), null);
  });
});

describe("exploitFlag", () => {
  test("validated wins over exploitable", () => {
    assert.equal(exploitFlag({ exploit_validated: true, exploitable: true }), "Exploit validated");
  });
  test("exploitable", () => assert.equal(exploitFlag({ exploitable: true }), "Exploitable"));
  test("none", () => assert.equal(exploitFlag({}), null));
});
