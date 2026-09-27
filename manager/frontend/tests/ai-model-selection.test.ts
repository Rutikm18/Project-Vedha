import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { parseAiModelSelection } from "../lib/ai-model-selection";

describe("parseAiModelSelection", () => {
  test("accepts the Manager provider catalog and safe model identifiers", () => {
    assert.deepEqual(parseAiModelSelection("openai", "gpt-5-mini"), {
      provider: "openai",
      model: "gpt-5-mini",
    });
    assert.deepEqual(parseAiModelSelection(undefined, undefined), {});
  });

  test("rejects unknown providers and unsafe model identifiers", () => {
    assert.equal(parseAiModelSelection("shell", "model"), null);
    assert.equal(parseAiModelSelection("ollama", "model; rm"), null);
    assert.equal(parseAiModelSelection("ollama", ""), null);
  });
});
