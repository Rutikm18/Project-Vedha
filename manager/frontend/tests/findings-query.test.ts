import assert from "node:assert/strict";
import { test } from "node:test";
import { findingChoice, findingFlag, findingPage } from "../lib/findings-query";

test("dashboard links normalize status and severity without allowing unknown values", () => {
  const link = new URL("https://vedha.test/findings?severity=CRITICAL&status=open");
  assert.equal(findingChoice(link.searchParams.get("severity"), ["ALL", "CRITICAL", "HIGH"], "ALL"), "CRITICAL");
  assert.equal(findingChoice(link.searchParams.get("status"), ["ALL", "OPEN", "CONFIRMED"], "ALL"), "OPEN");
  assert.equal(findingChoice("unsupported", ["ALL", "OPEN"], "ALL"), "ALL");
  assert.equal(findingChoice(null, ["risk", "date"], "risk"), "risk");
});

test("queue pagination rejects malformed, fractional, negative and unsafe pages", () => {
  for (const input of [null, "", "0", "-2", "1.5", "NaN", "Infinity", "9007199254740992"]) {
    assert.equal(findingPage(input), 1);
  }
  assert.equal(findingPage("4"), 4);
});

test("signal flags use explicit truth values", () => {
  assert.equal(findingFlag("true"), true);
  assert.equal(findingFlag("1"), true);
  for (const value of [null, "false", "0", "unexpected"]) assert.equal(findingFlag(value), false);
});
