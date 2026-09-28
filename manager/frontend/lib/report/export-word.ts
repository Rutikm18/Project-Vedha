/**
 * export-word.ts — the on-screen report as a Word document.
 *
 * Word opens an HTML document saved as .doc, but it knows nothing of CSS
 * variables, flex/grid, rgba() or color-mix(). So the export is taken from the
 * LIVE rendered report (in print mode: every card open, filters off, light
 * theme) and each element's computed style is flattened into plain inline CSS
 * Word understands. The result is what the PDF shows, not a second layout that
 * can drift from it.
 *
 * The pure helpers (colour flattening, the document wrapper, filenames) are
 * unit-tested; `exportReportToWord` is the DOM glue.
 */
import { enterPrintMode, exitPrintMode } from "../print-mode";
import { saveBlob } from "./download";

/** Parse a computed CSS colour into [r,g,b,a] (0-255, alpha 0-1), or null. */
export function parseCssColor(value: string): [number, number, number, number] | null {
  const v = value.trim().toLowerCase();
  if (!v || v === "transparent") return null;
  const hex = v.match(/^#([0-9a-f]{3,8})$/);
  if (hex) {
    let h = hex[1];
    if (h.length === 3 || h.length === 4) h = [...h].map(c => c + c).join("");
    const n = (i: number) => parseInt(h.slice(i, i + 2), 16);
    return [n(0), n(2), n(4), h.length === 8 ? n(6) / 255 : 1];
  }
  const rgb = v.match(/^rgba?\(([^)]+)\)$/);
  if (rgb) {
    const parts = rgb[1].split(/[\s,/]+/).filter(Boolean);
    if (parts.length < 3) return null;
    const ch = (p: string) => p.endsWith("%") ? parseFloat(p) * 2.55 : parseFloat(p);
    const a = parts[3] === undefined ? 1 : parts[3].endsWith("%") ? parseFloat(parts[3]) / 100 : parseFloat(parts[3]);
    return [ch(parts[0]), ch(parts[1]), ch(parts[2]), a];
  }
  // color-mix() computes to color(srgb r g b / a) with 0-1 channels.
  const srgb = v.match(/^color\(srgb\s+([^)]+)\)$/);
  if (srgb) {
    const [chans, alpha] = srgb[1].split("/");
    const c = chans.trim().split(/\s+/).map(parseFloat);
    if (c.length < 3 || c.some(Number.isNaN)) return null;
    return [c[0] * 255, c[1] * 255, c[2] * 255, alpha === undefined ? 1 : parseFloat(alpha)];
  }
  return null;
}

/**
 * A computed colour as an opaque #rrggbb, composited over white (the page).
 * Returns null for fully transparent / unparseable values — callers then emit
 * nothing and Word falls back to its default.
 */
export function cssColorToHex(value: string): string | null {
  const c = parseCssColor(value);
  if (!c) return null;
  const [r, g, b, a] = c;
  if (!(a > 0.01)) return null;
  const blend = (x: number) => Math.round(Math.min(255, Math.max(0, x * a + 255 * (1 - a))));
  return "#" + [r, g, b].map(x => blend(x).toString(16).padStart(2, "0")).join("");
}

/** px (computed) → pt, which Word lays out reliably. */
export function pxToPt(px: string): string | null {
  const n = parseFloat(px);
  if (!Number.isFinite(n)) return null;
  return `${Math.round(n * 0.75 * 10) / 10}pt`;
}

export function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));
}

/** Wrap body HTML in the Office-flavoured document Word opens in Print layout. */
export function wordDocument(title: string, bodyHtml: string): string {
  return [
    "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>",
    "<head><meta charset='utf-8'>",
    `<title>${escapeHtml(title)}</title>`,
    "<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom><w:DoNotOptimizeForBrowser/></w:WordDocument></xml><![endif]-->",
    "<style>",
    "@page WordSection1 { size: 8.27in 11.69in; margin: 0.75in 0.7in; }",
    "div.WordSection1 { page: WordSection1; }",
    "body { font-family: Calibri, Arial, sans-serif; font-size: 10.5pt; color: #0f172a; }",
    "table { border-collapse: collapse; }",
    "td, th { vertical-align: top; }",
    "pre, code { font-family: Consolas, 'Courier New', monospace; font-size: 8.5pt; white-space: pre-wrap; }",
    "a { color: #1d4ed8; }",
    "</style></head>",
    `<body><div class='WordSection1'>${bodyHtml}</div></body></html>`,
  ].join("");
}

/** "Bank VA / Q3" → "vedha-report-Bank-VA-Q3-20260928-1405.doc" */
export function reportFilename(name: string, ext: string, now: Date = new Date()): string {
  const slug = name.replace(/[^A-Za-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40) || "engagement";
  const p = (n: number) => String(n).padStart(2, "0");
  const stamp = `${now.getFullYear()}${p(now.getMonth() + 1)}${p(now.getDate())}-${p(now.getHours())}${p(now.getMinutes())}`;
  return `vedha-report-${slug}-${stamp}.${ext}`;
}

// ── DOM glue ─────────────────────────────────────────────────────────────────

/** Controls and decoration that have no place in a document. */
const STRIP = [
  ".no-print", "script", "style", "svg", "input", "select", "textarea",
  ".vf-chevron", ".vf-filters", ".vf-blockers", ".vf-notready",
  ".vf-artifact-tools", ".vf-icon-btn", ".vf-text-btn",
].join(",");

const SIDES = ["top", "right", "bottom", "left"] as const;

function inlineStyle(cs: CSSStyleDeclaration, tag: string): string {
  const out: string[] = [];
  const color = cssColorToHex(cs.color);
  if (color) out.push(`color:${color}`);
  const bg = cssColorToHex(cs.backgroundColor);
  if (bg && bg !== "#ffffff") out.push(`background:${bg}`);
  const fs = pxToPt(cs.fontSize);
  if (fs) out.push(`font-size:${fs}`);
  const fw = parseInt(cs.fontWeight, 10);
  if (fw >= 600) out.push("font-weight:bold");
  if (cs.fontStyle === "italic") out.push("font-style:italic");
  if (/mono|consolas|courier/i.test(cs.fontFamily)) out.push("font-family:Consolas,'Courier New',monospace");
  if (cs.textTransform === "uppercase") out.push("text-transform:uppercase");
  if (cs.textAlign === "center" || cs.textAlign === "right") out.push(`text-align:${cs.textAlign}`);
  if (cs.textDecorationLine.includes("underline")) out.push("text-decoration:underline");
  for (const side of SIDES) {
    const w = parseFloat(cs.getPropertyValue(`border-${side}-width`));
    const st = cs.getPropertyValue(`border-${side}-style`);
    const bc = cssColorToHex(cs.getPropertyValue(`border-${side}-color`));
    if (w > 0 && st !== "none" && st !== "hidden" && bc) out.push(`border-${side}:${pxToPt(`${w}px`)} ${st} ${bc}`);
  }
  // Only boxes carry padding/margin; inline runs would bloat every line.
  if (cs.display !== "inline") {
    const pad = SIDES.map(s => pxToPt(cs.getPropertyValue(`padding-${s}`)) ?? "0pt");
    if (pad.some(p => p !== "0pt")) out.push(`padding:${pad.join(" ")}`);
    const mt = pxToPt(cs.marginTop), mb = pxToPt(cs.marginBottom);
    if (mt && mt !== "0pt") out.push(`margin-top:${mt}`);
    if (mb && mb !== "0pt") out.push(`margin-bottom:${mb}`);
  }
  if (tag === "PRE" || cs.whiteSpace.startsWith("pre")) out.push("white-space:pre-wrap");
  return out.join(";");
}

/**
 * Build the .doc body from a rendered report element. Must be called while the
 * report is in print mode so hidden/collapsed content is in the DOM.
 */
export function reportElementToWordHtml(root: HTMLElement): string {
  const clone = root.cloneNode(true) as HTMLElement;
  const live = [root, ...Array.from(root.querySelectorAll<HTMLElement>("*"))];
  const copy = [clone, ...Array.from(clone.querySelectorAll<HTMLElement>("*"))];
  // Same tree, same order: flatten computed style onto each clone node.
  for (let i = 0; i < live.length && i < copy.length; i++) {
    const cs = window.getComputedStyle(live[i]);
    if (cs.display === "none" || cs.visibility === "hidden") {
      copy[i].setAttribute("data-word-strip", "");
      continue;
    }
    const style = inlineStyle(cs, live[i].tagName);
    copy[i].removeAttribute("class");
    if (style) copy[i].setAttribute("style", style); else copy[i].removeAttribute("style");
  }
  clone.querySelectorAll("[data-word-strip]").forEach(n => n.remove());
  // Remove controls AFTER the walk so the live/clone index pairing held.
  clone.querySelectorAll(STRIP).forEach(n => n.remove());
  // Card headers are <button>s on screen; in Word they are just headings.
  clone.querySelectorAll("button").forEach(btn => {
    const div = document.createElement("div");
    div.setAttribute("style", btn.getAttribute("style") ?? "");
    while (btn.firstChild) div.appendChild(btn.firstChild);
    btn.replaceWith(div);
  });
  clone.querySelectorAll("[hidden]").forEach(n => n.removeAttribute("hidden"));
  // Links must survive outside the app.
  clone.querySelectorAll<HTMLAnchorElement>("a[href]").forEach(a => {
    a.setAttribute("href", new URL(a.getAttribute("href")!, window.location.href).href);
  });
  return clone.innerHTML;
}

/** Render the report in print mode, capture it as a Word document, restore. */
export function exportReportToWord(root: HTMLElement, engagementName: string): void {
  let body: string;
  enterPrintMode();
  try {
    body = reportElementToWordHtml(root);
  } finally {
    exitPrintMode();
  }
  const html = wordDocument(`${engagementName} — VAPT report`, body);
  // BOM so Word detects UTF-8 (em dashes, ₹, non-Latin hostnames).
  saveBlob(new Blob(["\ufeff", html], { type: "application/msword" }), reportFilename(engagementName, "doc"));
}
