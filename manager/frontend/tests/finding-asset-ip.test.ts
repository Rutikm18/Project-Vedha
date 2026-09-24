import { test } from "node:test";
import assert from "node:assert/strict";
import { mapAsset, toUiFinding } from "../lib/adapters";

const base = { id: "f1", title: "t", severity: "high", status: "open", evidence: {} };

test("affected host is the asset IP, never the opaque asset UUID", () => {
  const f: any = toUiFinding({ ...base, asset_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    asset_ip: "192.168.1.78", asset_hostname: "nas" });
  assert.equal(f.affectedHost, "192.168.1.78");
  assert.equal(f.assetIp, "192.168.1.78");
  assert.equal(f.assetHostname, "nas");
});

test("a finding with an asset but no IP shows a dash, not the UUID", () => {
  const f: any = toUiFinding({ ...base, asset_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6" });
  assert.equal(f.affectedHost, "—");
  assert.equal(f.assetIp, null);
});

test("asset filter options map from the backend shape", () => {
  assert.deepEqual(
    mapAsset({ asset_id: "a", ip_address: "10.0.0.5", hostname: null, findings: 3 }),
    { assetId: "a", ip: "10.0.0.5", hostname: null, findings: 3 },
  );
});
