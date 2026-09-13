/**
 * Guards for dashboard fields whose DISPLAY disagreed with their DATA.
 *
 * Each test below pins a defect where the console said something the backend
 * never claimed — the class of bug that matters most on a security console,
 * because an operator has no way to notice it from the screen alone.
 */
import assert from "node:assert/strict";
import test from "node:test";

import {
  findingStatusStyle, toFindingStatus, STATUS_BG, STATUS_COLOR, SEVERITY, toSeverity,
} from "../lib/severity";
import { normalizePortalDataset } from "../lib/console-source";
import { toUiFinding } from "../lib/adapters";

test("every status the adapter can emit has its own chip style", () => {
  // The dashboard used to key a local map on OPEN/IN_REVIEW/IN_REMEDIATION/
  // VERIFIED/CLOSED — a vocabulary the backend has never emitted. Four of the
  // five real statuses missed and fell back to the OPEN entry, so a REMEDIATED
  // finding was painted in the same critical red as a live one.
  for (const apiStatus of ["open", "confirmed", "remediated", "accepted", "fp"]) {
    const ui = toUiFinding({ id: "f", title: "t", severity: "high", status: apiStatus });
    const style = findingStatusStyle(ui.status);
    assert.ok(style.color, `${apiStatus} has no colour`);
    assert.ok(style.bg, `${apiStatus} has no background`);
    assert.ok(style.label, `${apiStatus} has no label`);
  }
});

test("a fixed finding never renders in the open-critical colour", () => {
  const open = findingStatusStyle("OPEN");
  const remediated = findingStatusStyle("REMEDIATED");
  const accepted = findingStatusStyle("ACCEPTED");
  const fp = findingStatusStyle("FALSE_POSITIVE");

  assert.notEqual(remediated.color, open.color);
  assert.notEqual(accepted.color, open.color);
  assert.notEqual(fp.color, open.color);
  // Remediated is the only one that earns the "nominal" (resolved) tone.
  assert.match(remediated.color, /nominal/);
});

test("status normalisation survives casing and the backend's fp spelling", () => {
  assert.equal(toFindingStatus("remediated"), "REMEDIATED");
  assert.equal(toFindingStatus("FALSE_POSITIVE"), "FALSE_POSITIVE");
  assert.equal(toFindingStatus("false-positive"), "FALSE_POSITIVE");
  assert.equal(toFindingStatus("fp"), "FALSE_POSITIVE");
  // Unknown falls back to OPEN — the safe direction on a security console:
  // over-reporting an exposure beats hiding one.
  assert.equal(toFindingStatus("something-new"), "OPEN");
  assert.equal(toFindingStatus(undefined), "OPEN");
});

test("STATUS_COLOR and STATUS_BG cover exactly the same statuses", () => {
  assert.deepEqual(Object.keys(STATUS_COLOR).sort(), Object.keys(STATUS_BG).sort());
});

/* ── Exposure analytics ─────────────────────────────────────────────────── */

test("both consoles see the same exposure shape", () => {
  // FastAPI answers snake_case; the operator BFF camelCases it. Without the
  // portal branch the two consoles disagreed about whether the protocol panel
  // was showing a partial view.
  const fromFastApi = {
    protocols: [{ name: "SMB", severity: "critical", value: 100, findings: 2, assets: 3 }],
    zones: [{ name: "PROD", score: 30, assets: 100, affected: 1 }],
    unattributed_findings: 7,
  };
  assert.deepEqual(normalizePortalDataset("exposure", fromFastApi), {
    protocols: fromFastApi.protocols,
    zones: fromFastApi.zones,
    unattributedFindings: 7,
  });
});

test("a missing exposure payload degrades to empty, not undefined", () => {
  assert.deepEqual(normalizePortalDataset("exposure", {}), {
    protocols: [],
    zones: [],
    unattributedFindings: 0,
  });
});

test("protocol severity maps onto the shared severity scale", () => {
  // The band used to be thresholded from the severity WEIGHT at 85/65/45, so
  // nothing could reach the 45-64 "Elevated" band and a medium read "Contained".
  // Reading severity directly removes that second, contradictory scale.
  for (const [sev, expected] of [
    ["critical", "Critical"], ["high", "High"], ["medium", "Medium"],
    ["low", "Low"], ["info", "Info"],
  ] as const) {
    assert.equal(SEVERITY[toSeverity(sev)].label, expected);
  }
});
