/* The launcher must NOT ship its own rate/concurrency/timeout envelope.
 *
 * It used to send all four unconditionally, so the probe's intensity preset
 * (probe/workflow/intensity.py) was always discarded while its port BREADTH
 * survived. "Aggressive" therefore ran `deep`'s 65,535 ports at 600 pps /
 * 2.0 s instead of the 150 pps / 4.0 s that breadth was tuned for — a
 * lower-ACCURACY mode, not just a faster one (port_scanner.py:474 measured
 * 69 false `filtered` at a rate less than half that). */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { buildScanLaunchRequest } from "../lib/scan-launch";

const ENVELOPE = ["rate", "concurrency", "timeout", "disc_timeout"] as const;

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

/* Now that the launcher sends nothing but a name, the rate shown on the dial is
 * DISPLAY ONLY — it no longer causes the number it reports. That is exactly the
 * condition under which a label drifts from the thing it describes, silently and
 * for a long time, so pin the two together. */
const ALIAS: Record<string, string> = { stealth: "light", normal: "standard", aggressive: "deep" };

test("the intensity dial reports the rate the probe preset actually uses", (t) => {
  let presets: string;
  try {
    presets = readFileSync(join(process.cwd(), "../../probe/workflow/intensity.py"), "utf8");
  } catch {
    return t.skip("probe tree not present in this checkout");
  }

  const page = readFileSync(join(process.cwd(), "app/scan/page.tsx"), "utf8");

  for (const [uiName, presetName] of Object.entries(ALIAS)) {
    const block = presets.split(`"${presetName}": {`)[1]?.split("},")[0];
    assert.ok(block, `no ${presetName} preset found`);
    const rate = Number(/"rate":\s*([\d.]+)/.exec(block)?.[1]);
    assert.ok(Number.isFinite(rate), `no rate in ${presetName}`);

    const shown = /pps:\s*"(\d+) pps"/.exec(page.split(`id: "${uiName}"`)[1] ?? "")?.[1];
    assert.equal(
      Number(shown), rate,
      `dial shows ${shown} pps for ${uiName} but ${presetName} probes at ${rate}`,
    );
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
