import assert from "node:assert/strict";
import test from "node:test";
import { isIP } from "node:net";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { parseScanIp, scanIpAllowed, deepScanAssetOptions } from "../lib/scan-target";
import { buildDeepScanLaunch } from "../lib/scan-launch";
import { deepTargetProblem, DeepScanCard } from "../components/portal/DeepScanCard";
import { ScanIntensityControl } from "../components/scan/ScanIntensityControl";

const scope = ["192.0.2.0/24", "2001:db8:1::/48"];

test("single-host parsing agrees with IP literals, permits host prefixes only", () => {
  for (const ip of ["0.0.0.0", "255.255.255.255", "192.0.2.6", "::", "::1", "2001:db8::a", "::ffff:192.0.2.5", "2001:db8:0:1:2:3:4:5"]) {
    assert.notEqual(isIP(ip), 0);
    assert.ok(parseScanIp(ip), ip);
    assert.ok(parseScanIp(`${ip}/${isIP(ip) === 4 ? 32 : 128}`), ip);
    assert.doesNotThrow(() => buildDeepScanLaunch({ engagementId: "e1", ip, audience: "operator" }));
  }
  for (const ip of ["", "host.example", "localhost", "garbage:ipv6", "123", "192.0.2.999", "192.0.2.01", "192.0.2.1/128", "::1/32", "::1/64", "192.0.2.0/24", "192.0.2.1,192.0.2.2", "192.0.2.1 192.0.2.2", "192.0.2.1-192.0.2.2", "fe80::1%en0", "[::1]", "::1//128"]) {
    assert.equal(parseScanIp(ip), null, ip);
    assert.throws(() => buildDeepScanLaunch({ engagementId: "e1", ip, audience: "operator" }), /exactly one host/, ip);
  }
});

test("deep scope rejects excluded and foreign IPs in both families, including IPv6 aliases", () => {
  assert.equal(scanIpAllowed("192.0.2.10", scope), true);
  assert.equal(scanIpAllowed("2001:db8:1::a", scope), true);
  assert.equal(scanIpAllowed("2001:db8:2::a", scope), false);
  assert.equal(scanIpAllowed("192.0.3.10", scope), false);
  assert.equal(scanIpAllowed("192.0.2.10", scope, ["192.0.2.8/29"]), false);
  assert.equal(scanIpAllowed("2001:db8:1::a", scope, ["2001:db8:1::/64"]), false);
  assert.equal(scanIpAllowed("192.0.2.10", []), false);
  assert.equal(scanIpAllowed("192.0.2.10", ["broken/24"]), false);
  assert.match(deepTargetProblem("2001:db8:1::a", scope, ["2001:0db8:0001:0:0:0:0:a/128"], true) ?? "", /already had/);
});

test("the picker contains only unique eligible IPs from the selected engagement response", () => {
  const assets = [
    { ip_address: "192.0.2.10", hostname: "db" }, { ip_address: "192.0.2.10" },
    { ip_address: "192.0.2.11" }, { ip_address: "192.0.3.10" }, { ip_address: "bad" },
  ];
  assert.deepEqual(deepScanAssetOptions(assets, scope, ["192.0.2.11/32"]), [assets[0]]);
  const html = renderToStaticMarkup(createElement(DeepScanCard, { plan: null, scope, assets, probeReady: true, launching: false, onLaunch() {} }));
  assert.match(html, /<select[^>]+id="deep-scan-ip"/);
  assert.doesNotMatch(html, /multiple=|<textarea/);
  assert.match(html, /Choose one discovered IP/);
  assert.match(html, /<button[^>]+disabled=""[^>]*>.*Launch deep scan/);
});

test("preset choices use native radios, keep all three visible, and expose unavailable choices", () => {
  const html = renderToStaticMarkup(createElement(ScanIntensityControl, { value: "normal", onChange() {}, allowed: ["normal", "stealth"] }));
  assert.equal((html.match(/type="radio"/g) ?? []).length, 3);
  assert.match(html, /checked=""[^>]+value="normal"/);
  assert.match(html, /disabled=""[^>]+value="aggressive"/);
  assert.match(html, /scanner-intensity-dial" aria-hidden="true"/);
  assert.match(html, /200 pps/);
  assert.match(html, /preset rate/);
  assert.doesNotMatch(html, /IDS|IPS|65,535/);
});
