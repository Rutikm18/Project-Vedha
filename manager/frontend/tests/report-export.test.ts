import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, test } from "node:test";

import { cssColorToHex, escapeHtml, parseCssColor, pxToPt, reportFilename, wordDocument } from "../lib/report/export-word";
import { filenameFromDisposition } from "../lib/report/download";
import { createRemediationApi } from "../lib/remediation";

const root = join(fileURLToPath(import.meta.url), "..", "..");
const read = (p: string) => readFileSync(join(root, p), "utf8");

describe("Word export: colour flattening", () => {
  test("opaque rgb and hex pass through", () => {
    assert.equal(cssColorToHex("rgb(15, 23, 42)"), "#0f172a");
    assert.equal(cssColorToHex("#abc"), "#aabbcc");
    assert.equal(cssColorToHex("rgb(15 23 42)"), "#0f172a");
  });

  test("alpha is composited over white — Word has no rgba()", () => {
    assert.equal(cssColorToHex("rgba(255, 0, 0, 0.5)"), "#ff8080");
    assert.equal(cssColorToHex("#ff000080"), "#ff7f7f");
  });

  test("color-mix() output — color(srgb …) — is understood", () => {
    assert.deepEqual(parseCssColor("color(srgb 1 0 0 / 0.5)"), [255, 0, 0, 0.5]);
    assert.equal(cssColorToHex("color(srgb 0 0 1)"), "#0000ff");
  });

  test("transparent and unknown syntaxes emit nothing", () => {
    assert.equal(cssColorToHex("rgba(0, 0, 0, 0)"), null);
    assert.equal(cssColorToHex("transparent"), null);
    assert.equal(cssColorToHex("oklch(0.7 0.1 200)"), null);
    assert.equal(cssColorToHex(""), null);
  });

  test("px become pt", () => {
    assert.equal(pxToPt("16px"), "12pt");
    assert.equal(pxToPt("11.5px"), "8.6pt");
    assert.equal(pxToPt("normal"), null);
  });
});

describe("Word export: document", () => {
  test("wrapper is an Office HTML document in Print view, title escaped", () => {
    const doc = wordDocument(`Bank <VA> & "Q3"`, "<p>body</p>");
    assert.match(doc, /xmlns:w='urn:schemas-microsoft-com:office:word'/);
    assert.match(doc, /<w:View>Print<\/w:View>/);
    assert.match(doc, /<title>Bank &lt;VA&gt; &amp; &quot;Q3&quot;<\/title>/);
    assert.match(doc, /<div class='WordSection1'><p>body<\/p><\/div>/);
  });

  test("escapeHtml covers the five specials", () => {
    assert.equal(escapeHtml(`<a href="x">'&'</a>`), "&lt;a href=&quot;x&quot;&gt;&#39;&amp;&#39;&lt;/a&gt;");
  });

  test("filename is a safe slug with a timestamp", () => {
    const at = new Date(2026, 8, 28, 14, 5);
    assert.equal(reportFilename("Bank VA / Q3", "doc", at), "vedha-report-Bank-VA-Q3-20260928-1405.doc");
    assert.equal(reportFilename("///", "csv", at), "vedha-report-engagement-20260928-1405.csv");
  });
});

describe("Excel/CSV download", () => {
  test("filename is read from Content-Disposition", () => {
    assert.equal(filenameFromDisposition('attachment; filename="vedha-findings-x.csv"'), "vedha-findings-x.csv");
    assert.equal(filenameFromDisposition("attachment; filename=plain.xlsx"), "plain.xlsx");
    assert.equal(filenameFromDisposition("attachment; filename*=UTF-8''r%C3%A9port.xlsx"), "réport.xlsx");
    assert.equal(filenameFromDisposition(null), null);
  });

  test("CSV asks the tracker for the single findings sheet on both surfaces", () => {
    assert.equal(
      createRemediationApi("manager").exportUrl("e 1", "csv", "findings"),
      "/api/engagements/e%201/remediation/export?format=csv&sheet=findings",
    );
    assert.equal(createRemediationApi("portal").exportUrl("ignored", "csv", "findings"),
      "/api/portal/remediation/export?format=csv&sheet=findings");
    assert.equal(createRemediationApi("portal").exportUrl("ignored", "xlsx"),
      "/api/portal/remediation/export?format=xlsx");
  });
});

describe("PDF: the whole report prints, not one viewport", () => {
  const css = read("app/globals.css");
  const printBlocks = css.split("@media print").slice(1).map(b => b.slice(0, b.indexOf("\n}") + 2)).join("\n");

  test("print CSS releases the 100vh shell and its scrolling <main>", () => {
    for (const sel of [".vedha-shell", ".vedha-shell-body", ".vedha-page-main"]) {
      assert.ok(printBlocks.includes(sel), `${sel} must be released in print`);
    }
    assert.match(printBlocks, /height:\s*auto\s*!important/);
    assert.match(printBlocks, /overflow:\s*visible\s*!important/);
  });

  test("the shell elements carry the classes the print CSS targets", () => {
    const shell = read("components/PageShell.tsx");
    assert.match(shell, /className="vedha-shell"/);
    assert.match(shell, /className="vedha-shell-body"/);
    assert.match(shell, /className="vedha-page-main"/);
  });

  test("the portal reports route loads the report stylesheet too", () => {
    assert.match(read("app/portal/reports/layout.tsx"), /report-finding\.css/);
  });

  test("the findings register ignores filters and opens every card in print mode", () => {
    const src = read("components/report/FindingReport.tsx");
    assert.match(src, /const shown = printing \? assessed : filtered;/);
    assert.match(src, /open=\{printing \|\| open\.has\(a\.raw\.id\)\}/);
  });
});
