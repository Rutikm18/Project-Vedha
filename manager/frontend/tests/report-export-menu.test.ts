/* Regression (production, 2 Oct 2026): clicking "Export" on the Reports page
 * opened nothing. The menu lives in the PageShell header, whose tools/scroll
 * wrappers clip overflow (overflow: hidden / overflow-x: auto) inside a 50 px
 * bar — the format list opened below the header and was clipped out of sight.
 * The list must render outside the header (portal) at viewport coordinates. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { exportMenuPosition } from "../components/report/ReportExportMenu";

const source = readFileSync(join(process.cwd(), "components/report/ReportExportMenu.tsx"), "utf8");

test("the format list is portaled to <body>, not left inside the clipping header", () => {
  assert.match(source, /createPortal\(/);
  assert.match(source, /document\.body/);
  assert.doesNotMatch(source, /<details/);           // the old in-place <details> popover is gone
});

test("the list is placed at viewport coordinates under the button, right-aligned", () => {
  // Button 120 px wide at x 600–720, bottom edge at y 42, in a 1280 px window.
  const pos = exportMenuPosition({ left: 600, right: 720, bottom: 42 }, 1280);
  assert.deepEqual(pos, { top: 50, left: 440, width: 280 });   // right edge 720, 8 px gap
});

test("the list never runs off a narrow screen", () => {
  const phone = exportMenuPosition({ left: 20, right: 110, bottom: 42 }, 360);
  assert.equal(phone.left, 14);                                 // clamped to the 14 px gutter
  assert.ok(phone.left + phone.width <= 360 - 14);
});
