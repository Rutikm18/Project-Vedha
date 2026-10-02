import assert from "node:assert/strict";
import { describe, test } from "node:test";

import { decodeCvssVector } from "../lib/report/cvss";

describe("decodeCvssVector", () => {
  test("decodes a CVSS 3.1 base vector (with prefix), in canonical order", () => {
    const m = decodeCvssVector("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H");
    const byKey = Object.fromEntries(m.map((x) => [x.key, x.valueLabel]));
    assert.equal(byKey.AV, "Network");
    assert.equal(byKey.AC, "Low");
    assert.equal(byKey.PR, "None");
    assert.equal(byKey.S, "Unchanged");
    assert.equal(byKey.C, "High");
    assert.equal(m[0].key, "AV");
    assert.equal(m[0].code, "AV:N");
    assert.equal(m[0].label, "Attack Vector");
  });

  test("works without the CVSS:x.y/ prefix", () => {
    const m = decodeCvssVector("AV:L/AC:H/PR:H/UI:R/S:C/C:L/I:N/A:N");
    assert.equal(m.find((x) => x.key === "AV")?.valueLabel, "Local");
    assert.equal(m.find((x) => x.key === "UI")?.valueLabel, "Required");
    assert.equal(m.find((x) => x.key === "S")?.valueLabel, "Changed");
  });

  test("decodes CVSS 4.0 metrics (AT, VC/VI/VA, SC/SI/SA)", () => {
    const m = decodeCvssVector("CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N");
    const keys = m.map((x) => x.key);
    assert.ok(keys.includes("AT"));
    assert.ok(keys.includes("VC"));
    assert.equal(m.find((x) => x.key === "VC")?.valueLabel, "High");
    assert.equal(m.find((x) => x.key === "AT")?.valueLabel, "None");
  });

  test("ignores unknown metrics and bad input", () => {
    assert.deepEqual(decodeCvssVector(null), []);
    assert.deepEqual(decodeCvssVector(undefined), []);
    assert.deepEqual(decodeCvssVector(""), []);
    assert.deepEqual(decodeCvssVector("garbage"), []);
    const m = decodeCvssVector("AV:N/XX:Z/AC:L");
    assert.deepEqual(m.map((x) => x.key), ["AV", "AC"]);
  });

  test("unknown metric VALUE falls back to the raw code", () => {
    const m = decodeCvssVector("AV:Q");
    assert.equal(m.length, 1);
    assert.equal(m[0].valueLabel, "Q");
  });
});
