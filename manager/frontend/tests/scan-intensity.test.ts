/* The launcher ships no probe envelope, and the dial describes the envelope
 * the probe actually uses. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { INTENSITY } from "../lib/scan-intensity";
import { buildScanLaunchRequest } from "../lib/scan-launch";

const ENVELOPE = ["rate", "concurrency", "timeout", "disc_timeout"] as const;

function readRepoFile(relative: string): string | null {
  try {
    return readFileSync(join(process.cwd(), "../..", relative), "utf8");
  } catch {
    return null;
  }
}

for (const intensity of ["stealth", "normal", "aggressive"] as const) {
  test(`${intensity} sends intensity only, letting the probe preset supply the envelope`, () => {
    const { params } = buildScanLaunchRequest({
      engagement_id: "eng-1",
      use_case_id: "uc_network_va",
      intensity,
      targets: ["10.0.0.1"],
    });

    assert.equal(params.intensity, intensity);
    for (const knob of ENVELOPE) {
      assert.ok(!(knob in params), `${intensity} must not pin ${knob}`);
    }
  });
}

test("the dial's rate matches the probe preset each UI name maps to", (t) => {
  const agents = readRepoFile("manager/backend/app/routers/agents.py");
  const presets = readRepoFile("probe/workflow/intensity.py");
  if (agents === null || presets === null) return t.skip("manager or probe tree not present");

  const aliasBody = /_INTENSITY_ALIASES\s*=\s*\{([^}]*)\}/.exec(agents)?.[1];
  assert.ok(aliasBody, "_INTENSITY_ALIASES not found in agents.py");
  const alias: Record<string, string> = Object.fromEntries(
    [...aliasBody.matchAll(/"(\w+)":\s*"(\w+)"/g)].map((m) => [m[1], m[2]]),
  );

  for (const option of INTENSITY) {
    const presetName = alias[option.id];
    assert.ok(presetName, `manager has no alias for ${option.id}`);
    const block = presets.split(`"${presetName}": {`)[1]?.split("},")[0];
    assert.ok(block, `no ${presetName} preset in intensity.py`);
    const rate = Number(/"rate":\s*([\d.]+)/.exec(block)?.[1]);
    assert.equal(
      option.rate, rate,
      `dial shows ${option.rate} pps for ${option.id} but ${presetName} probes at ${rate}`,
    );
  }
});

test("dial copy carries no number a test cannot check", () => {
  for (const option of INTENSITY) {
    for (const n of option.why.match(/\d[\d,]*/g) ?? []) {
      assert.equal(n, "65,535", `${option.id} copy claims "${n}", which nothing verifies`);
    }
  }
});

test("an explicit operator override survives the named preset", () => {
  const { params } = buildScanLaunchRequest({
    engagement_id: "eng-1",
    use_case_id: "uc_network_va",
    intensity: "aggressive",
    targets: ["10.0.0.1"],
    params: { rate: 40, concurrency: 10 },
  });

  assert.equal(params.rate, 40);
  assert.equal(params.concurrency, 10);
  assert.equal(params.intensity, "aggressive");
});
