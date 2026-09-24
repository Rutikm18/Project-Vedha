import assert from "node:assert/strict";
import test from "node:test";

import {
  assetTags,
  filterAssetsByTags,
  formatDeadline,
  fragileReasons,
  parseManualTags,
  tagCounts,
  tagLabel,
  tagTone,
} from "../lib/intel";

const web = {
  id: "a",
  tags: {
    v: 1,
    auto: [
      { key: "role", value: "web", rule: "role.port", confidence: 0.6, evidence: "tcp/443 https", source: "auto" },
      { key: "exposure", value: "internet_facing", rule: "exposure.matrix", confidence: 0.9, evidence: "x", source: "auto" },
      { key: "zone", value: "10.0.0.0/24", rule: "zone.subnet", confidence: 1, evidence: "x", source: "auto" },
    ],
    manual: [{ key: "owner_team", value: "cards", source: "manual" }],
  },
};
const db = { id: "b", tags: { v: 1, auto: [{ key: "role", value: "database", source: "auto" }], manual: [] } };
const bare = { id: "c", tags: null };

test("assetTags flattens auto + manual, sorted by importance, zone last", () => {
  const tags = assetTags(web);
  assert.deepEqual(tags.map((t) => `${t.key}:${t.value}`), [
    "exposure:internet_facing", "role:web", "owner_team:cards", "zone:10.0.0.0/24",
  ]);
  assert.equal(tags.find((t) => t.key === "owner_team")?.source, "manual");
  assert.deepEqual(assetTags(bare), []);
});

test("tagLabel humanizes key and value", () => {
  assert.equal(tagLabel({ key: "exposure", value: "internet_facing" }), "Internet facing");
  assert.equal(tagLabel({ key: "compliance_scope", value: "pci_cde_candidate" }), "PCI CDE candidate");
  assert.equal(tagLabel({ key: "sector_fn", value: "swift" }), "SWIFT");
  assert.equal(tagLabel({ key: "owner_team", value: "Cards Ops" }), "owner team: Cards Ops");
});

test("tagTone flags risk-bearing tags", () => {
  assert.equal(tagTone({ key: "exposure", value: "internet_facing" }), "risk");
  assert.equal(tagTone({ key: "data_sensitivity", value: "restricted" }), "risk");
  assert.equal(tagTone({ key: "sector_fn", value: "hsm" }), "sector");
  assert.equal(tagTone({ key: "owner_team", value: "x", source: "manual" }), "manual");
  assert.equal(tagTone({ key: "role", value: "web" }), "neutral");
});

test("tagCounts and AND-filter", () => {
  const counts = tagCounts([web, db, bare]);
  assert.equal(counts.find((c) => c.tag === "role:web")?.count, 1);
  assert.equal(counts[0].count >= counts[counts.length - 1].count, true);
  assert.deepEqual(filterAssetsByTags([web, db, bare], []).map((a) => a.id), ["a", "b", "c"]);
  assert.deepEqual(filterAssetsByTags([web, db, bare], ["role:web", "owner_team:cards"]).map((a) => a.id), ["a"]);
  assert.deepEqual(filterAssetsByTags([web, db], ["role:web", "role:database"]).map((a) => a.id), []);
});

test("parseManualTags validates key:value lines", () => {
  assert.deepEqual(parseManualTags("owner_team: Cards\nbusiness_service:UPI switch\n\n"), {
    tags: [{ key: "owner_team", value: "Cards" }, { key: "business_service", value: "UPI switch" }],
    errors: [],
  });
  const bad = parseManualTags("Owner Team: x\nnovalue:\njustatext");
  assert.equal(bad.tags.length, 0);
  assert.equal(bad.errors.length, 3);
});

test("formatDeadline", () => {
  assert.equal(formatDeadline(1), "1 hour");
  assert.equal(formatDeadline(6), "6 hours");
  assert.equal(formatDeadline(72), "72 hours");
  assert.equal(formatDeadline(720), "30 days");
});

test("fragileReasons mirrors the backend guard", () => {
  const hsm = { id: "h", tags: { auto: [{ key: "sector_fn", value: "hsm" }], manual: [] } };
  assert.deepEqual(fragileReasons(hsm), ["sector_fn:hsm"]);
  const cleared = { id: "c", tags: { auto: [{ key: "sector_fn", value: "swift" }], manual: [{ key: "scan_policy", value: "standard" }] } };
  assert.deepEqual(fragileReasons(cleared), []);
  assert.deepEqual(fragileReasons(web), []);
});
