import { test } from "node:test";
import assert from "node:assert/strict";
import {
  chainStateText, chainSummary, fixHint, nextUp, providerLabel, spendText, PROVIDER_ENV,
  type ChainEntry,
} from "../lib/ai-chain";

const e = (over: Partial<ChainEntry> = {}): ChainEntry => ({
  provider: "anthropic", model: "claude-x", tier: "premium", state: "healthy", ...over,
});

test("state text: ready, recovering, and a reason with minutes", () => {
  assert.equal(chainStateText(e()), "ready");
  assert.equal(chainStateText(e({ state: "probing" })), "recovering");
  assert.equal(chainStateText(e({ state: "cooling", reason: "rate_limit", retry_in_s: 100 })), "rate limited · 2 min");
  assert.equal(chainStateText(e({ state: "blocked", reason: "billing" })), "out of credit");
  assert.equal(chainStateText(e({ state: "blocked", reason: "weird" })), "weird");
});

test("next up is the first provider not cooling down, else the first", () => {
  const chain = [e({ provider: "anthropic", state: "blocked", reason: "billing" }),
                 e({ provider: "openai", state: "cooling" }),
                 e({ provider: "gemini", tier: "free" }),
                 e({ provider: "ollama", tier: "local" })];
  assert.equal(nextUp(chain)?.provider, "gemini");
  assert.equal(nextUp(chain.slice(0, 2))?.provider, "anthropic");
  assert.equal(nextUp([]), undefined);
});

test("spend is shown only when a cap is set", () => {
  assert.equal(spendText(e()), null);
  assert.equal(spendText(e({ daily_cap_usd: 20, spend_today_usd: 1.2 })), "$1.20 of $20 today");
  assert.equal(spendText(e({ daily_cap_usd: 10 })), "$0.00 of $10 today");
});

test("the summary counts ready, cooling and blocked", () => {
  const chain = [e(), e({ state: "probing" }), e({ state: "cooling" }), e({ state: "blocked" })];
  assert.deepEqual(chainSummary(chain), { total: 4, ready: 2, cooling: 1, blocked: 1 });
  assert.deepEqual(chainSummary([]), { total: 0, ready: 0, cooling: 0, blocked: 0 });
});

test("fix hints say what to do, and are absent for a working provider", () => {
  assert.equal(fixHint(e()), null);
  assert.match(fixHint(e({ state: "blocked", reason: "billing" }))!, /credit/i);
  assert.match(fixHint(e({ state: "blocked", reason: "auth" }))!, /key was rejected/i);
  assert.match(fixHint(e({ state: "cooling", reason: "rate_limit" }))!, /recovers/i);
  assert.match(fixHint(e({ state: "cooling", reason: "timeout" }))!, /retried/i);
});

test("every provider has a label and the server setting that adds it", () => {
  for (const id of Object.keys(PROVIDER_ENV)) {
    assert.ok(providerLabel(id).length > 0);
    assert.match(PROVIDER_ENV[id as keyof typeof PROVIDER_ENV], /^[A-Z_]+$/);
  }
});
