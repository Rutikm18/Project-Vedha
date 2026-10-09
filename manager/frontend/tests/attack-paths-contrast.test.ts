import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";

/**
 * The attack-path views draw meaning with marks (route-map edges, chain connectors, jewel
 * outlines) and with coloured text. WCAG 1.4.11 asks 3:1 for the first and 1.4.3 asks 4.5:1 for
 * the second, against the surface they sit on. This reads the REAL tokens out of globals.css,
 * so changing a token below the line fails here instead of shipping.
 */
const ROOT = join(__dirname, "..");
const css = readFileSync(join(ROOT, "app/globals.css"), "utf8");

function block(selector: string): string {
  const start = css.indexOf(selector);
  assert.ok(start >= 0, `${selector} not found`);
  const open = css.indexOf("{", start);
  let depth = 0;
  for (let i = open; i < css.length; i++) {
    if (css[i] === "{") depth++;
    if (css[i] === "}" && --depth === 0) return css.slice(open + 1, i);
  }
  throw new Error(`${selector} is not closed`);
}

function tokens(theme: "light" | "dark"): Record<string, string> {
  const body = theme === "light" ? block(':root,\n:root[data-theme="light"]') : block(':root[data-theme="dark"]');
  const out: Record<string, string> = {};
  for (const m of body.matchAll(/--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})\b/g)) out[m[1]] = m[2];
  return out;
}

function luminance(hex: string): number {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export function contrast(a: string, b: string): number {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

const SURFACES = ["bg-panel", "bg-surface"] as const;
const THEMES = ["light", "dark"] as const;

test("the helper agrees with a known pair (black on white is 21:1)", () => {
  assert.equal(Math.round(contrast("#000000", "#FFFFFF")), 21);
});

for (const theme of THEMES) {
  const t = tokens(theme);
  for (const surface of SURFACES) {
    test(`${theme}: text tokens used by the attack-path views reach 4.5:1 on ${surface}`, () => {
      for (const name of ["text-primary", "text-secondary", "text-muted", "text-faint", "accent",
        "sev-critical-color", "sev-high-color", "sev-medium-color", "sev-low-color", "nominal-color"]) {
        assert.ok(t[name], `${theme}: --${name} missing`);
        assert.ok(contrast(t[name], t[surface]) >= 4.5, `${theme}: --${name} on --${surface} is ${contrast(t[name], t[surface]).toFixed(2)}:1`);
      }
    });

    test(`${theme}: --text-muted, the colour of route-map edges and chain connectors, reaches 3:1 on ${surface}`, () => {
      assert.ok(contrast(t["text-muted"], t[surface]) >= 3);
    });
  }
}

test("the border tokens do NOT reach 3:1, which is why edges and connectors must not use them", () => {
  // Documents the reason for the rule. If a border token is ever strengthened this fails, and the
  // rule below can be relaxed on purpose.
  for (const theme of THEMES) {
    const t = tokens(theme);
    assert.ok(contrast(t["border-default"], t["bg-panel"]) < 3);
    assert.ok(contrast(t["border-strong"], t["bg-panel"]) < 3);
  }
});

test("route-map edges, arrowheads and the chain connector are drawn in a token that reaches 3:1", () => {
  const styles = readFileSync(join(ROOT, "app/engagements/[id]/attack-paths/styles.ts"), "utf8");
  const map = readFileSync(join(ROOT, "app/engagements/[id]/attack-paths/PathMap.tsx"), "utf8");
  assert.match(styles, /\.ap-map \.ap-edge \{[^}]*stroke: var\(--text-muted\)/);
  assert.doesNotMatch(styles, /\.ap-edge \{[^}]*--border/);
  assert.match(map, /id="ap-arrow"[\s\S]*?fill="var\(--text-muted\)"/);
  assert.doesNotMatch(map, /fill="var\(--border/);
});
