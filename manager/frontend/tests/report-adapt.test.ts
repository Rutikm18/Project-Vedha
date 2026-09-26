import { test } from "node:test";
import assert from "node:assert/strict";

import { toRawFinding, deriveDetectionMethod, toReportAssets } from "../lib/report/adapt";

// A minimal UI-Finding-shaped object (as toUiFinding would produce).
const uiBase = {
  id: "VDH-1", title: "t", severity: "CRITICAL", status: "OPEN",
  affectedHost: "web-01", discoveredAt: "2026-08-20T09:00:00Z",
  description: "d", technicalDetails: "td", impact: "i",
  evidence: [{ label: "l", content: "c" }], remediation: ["fix it"],
  mitre: [], riskScore: 900, cvss: "9.8", cvssVector: "",
  activelyExploited: false, detectionCoverage: "BLIND",
  epssScore: 0, epssPercentile: 0, epssRecorded: false,
  exploitValidated: false, verificationState: null,
  assetContext: null,
};
const U = (o: Record<string, unknown>) => ({ ...uiBase, ...o });

test("detectionMethod: validated exploit ⇒ exploit", () => {
  assert.equal(deriveDetectionMethod(U({ exploitValidated: true })), "exploit");
});
test("detectionMethod: confirmed verification ⇒ behavioural", () => {
  assert.equal(deriveDetectionMethod(U({ verificationState: "confirmed" })), "behavioural");
});
test("detectionMethod: corroborated verification ⇒ inference", () => {
  assert.equal(deriveDetectionMethod(U({ verificationState: "corroborated" })), "inference");
});
test("detectionMethod: detectionCoverage is ignored (blue-team signal, not validation)", () => {
  // BLIND is detection coverage, not how the finding was proven — must stay Unverified.
  assert.equal(deriveDetectionMethod(U({ detectionCoverage: "BLIND" })), undefined);
});
test("detectionMethod: nothing recorded ⇒ undefined (honest 'Unverified')", () => {
  assert.equal(deriveDetectionMethod(U({})), undefined);
});

test("assets: empty when no asset context", () => {
  assert.deepEqual(toReportAssets(U({})), []);
});
test("assets: one row derived from asset context", () => {
  const rows = toReportAssets(U({
    assetContext: { hostname: "web-01", ipAddress: "10.0.0.5", environment: "internal", owner: "ops" },
  }));
  assert.equal(rows.length, 1);
  assert.equal(rows[0].host, "web-01");
  assert.equal(rows[0].ip, "10.0.0.5");
  assert.equal(rows[0].internetReachable, false);
});

test("epss: mapped only when recorded", () => {
  assert.equal(toRawFinding(U({ epssScore: 0.7, epssRecorded: true })).epss, 0.7);
  assert.equal(toRawFinding(U({ epssScore: 0, epssRecorded: false })).epss, undefined);
});
test("internetReachable: dmz environment ⇒ true", () => {
  assert.equal(
    toRawFinding(U({ assetContext: { hostname: "h", environment: "DMZ" } })).internetReachable,
    true,
  );
});
test("toRawFinding: preserves required fields for assess()", () => {
  const r = toRawFinding(U({ exploitValidated: true }));
  assert.equal(r.id, "VDH-1");
  assert.equal(r.exploitValidated, true);
  assert.equal(r.detectionMethod, "exploit");
});

test("toRawFinding: prefers backend detectionMethod over derivation", () => {
  // No local signals → derivation is undefined; the backend value must win.
  assert.equal(toRawFinding(U({ detectionMethod: "version" })).detectionMethod, "version");
});

test("toRawFinding: passes through backend verification block and KEV date", () => {
  const r = toRawFinding(U({ verification: { expected: "no longer offered" }, kevDateAdded: "2024-01-15" }));
  assert.equal(r.verification?.expected, "no longer offered");
  assert.equal(r.kevAddedAt, "2024-01-15");
});

test("toRawFinding: prefers backend internetReachable", () => {
  assert.equal(toRawFinding(U({ internetReachable: true })).internetReachable, true);
});

// ── applyBundles: report findings grounded in their fix bundle ───────────────
import { applyBundles } from "../lib/report/adapt";
import type { Bundle } from "../lib/remediation";

const bundle = {
  fix_key: "abcdef123456", ref: "FIX-ABCDEF", recipe_id: "POSTURE-SMB-V1-ENABLED", product_family: "smb",
  title: "Disable SMBv1 on 2 hosts", remediation_type: "mitigation", risk_response: "mitigate",
  target_state: "SMBv1 disabled; SMB 2/3 only", effort: "low", remediation_risk: "medium",
  steps_by_os: {
    windows: [
      { step: 1, tier: "containment", title: "Block SMB", description: "Block 445.", commands_for_os: [],
        pre_checks: [], reboot_required: null, downtime: "none expected", rollback: "", risk: "low" },
      { step: 2, tier: "fix", title: "Disable SMBv1", description: "Turn it off.",
        commands_for_os: ["Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force"],
        pre_checks: [], reboot_required: false, downtime: "brief", rollback: "set back to $true", risk: "medium" },
    ],
  },
  verification_check: { scanner: "smb_scan", check: "no NT1 dialect", expected: "SMB2/3 only",
    manual_command: "Get-SmbServerConfiguration" },
  compensating_controls: "", references: [], resolves: ["VDH-1"], open_finding_ids: ["VDH-1"], excluded: [],
  hosts: [{ host: "fs1", ip: "10.0.0.1", os: "Windows Server 2019", os_family: "windows", ports: [445],
    finding_ids: ["VDH-1"], status: "open", due_at: "2026-10-01T00:00:00Z", due_source: "engagement", closed_at: null }],
  open_count: 1, closed_count: 0, due_at: "2026-10-01T00:00:00Z", due_source: "engagement", urgency: "attend",
  progress: { closed: 0, total: 1 }, status: "open", max_severity: "critical", kev: false,
} as unknown as Bundle;

test("applyBundles: tiers, verification, due date and fix ref come from the bundle", () => {
  const [f] = applyBundles([toRawFinding(U({}))], [bundle]);
  assert.equal(f.fixRef, "FIX-ABCDEF");
  assert.equal(f.dueAt, "2026-10-01T00:00:00Z");
  assert.equal(f.verification?.expected, "SMB2/3 only");
  const tiers = (f.remediation as Array<{ tier?: string }>).map((r) => r.tier);
  assert.deepEqual(tiers, ["containment", "fix"]);
  assert.match(String((f.remediation[1] as { action?: string }).action), /^Disable SMBv1 — Turn it off\.\nCommands: .*EnableSMB1Protocol/);
});

test("applyBundles: a finding outside every bundle is unchanged", () => {
  const raw = toRawFinding(U({ id: "OTHER" }));
  assert.deepEqual(applyBundles([raw], [bundle])[0], raw);
});

test("toRawFinding: compliance objects are flattened to strings (no render crash)", () => {
  const raw = toRawFinding(U({ compliance: [{ framework: "PCI DSS 4.0", controls: ["Req 2.2.1", "Req 4.2.1"], rationale: "x" }] }));
  assert.deepEqual(raw.compliance, ["PCI DSS 4.0: Req 2.2.1", "PCI DSS 4.0: Req 4.2.1"]);
});

test("applyBundles: shared multi-host wording is rewritten for the finding's own host", () => {
  const multi = JSON.parse(JSON.stringify(bundle)) as Bundle;
  multi.steps_by_os.windows[1].description = "Disable SMBv1 on each host in the checklist (the OS listed per host).";
  multi.verification_check.check = "no NT1 dialect on each host's IP:445";
  const [f] = applyBundles([toRawFinding(U({}))], [multi]);
  assert.match(String((f.remediation[1] as { action?: string }).action), /on fs1 \(Windows Server 2019\)/);
  assert.match(String(f.verification?.method), /10\.0\.0\.1:445/);
});
