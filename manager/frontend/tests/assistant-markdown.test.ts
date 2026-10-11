/* The assistant's Markdown parser: everything a model commonly emits must become
 * structure (not raw pipes, backticks or asterisks), nothing may become markup,
 * and a reply cut off mid-fence must still render. */
import assert from "node:assert/strict";
import test from "node:test";

import { inlineText, parseInline, parseMarkdown, type Block } from "../lib/assistant-markdown";

const kinds = (blocks: Block[]) => blocks.map((b) => b.t);

test("headings, paragraphs and horizontal rules", () => {
  const b = parseMarkdown("## Summary\n\nFirst line\nsecond line\n\n---\n\n### Next");
  assert.deepEqual(kinds(b), ["heading", "p", "hr", "heading"]);
  assert.equal((b[0] as any).level, 2);
  // a single newline is a visible break, not a lost one
  assert.deepEqual((b[1] as any).inlines.map((n: any) => n.t), ["text", "br", "text"]);
});

test("inline: bold, italic, code, strike and snake_case stay intact", () => {
  const nodes = parseInline("**192.0.2.10** has *SMBv1* on `445`, ~~old~~ and snake_case_name");
  assert.deepEqual(nodes.map((n) => n.t), ["strong", "text", "em", "text", "code", "text", "del", "text"]);
  assert.equal(inlineText(nodes), "192.0.2.10 has SMBv1 on 445, old and snake_case_name");
  assert.equal(parseInline("2 * 3 * 4").every((n) => n.t === "text"), true);
});

test("links: markdown and bare URLs become links, trailing punctuation does not", () => {
  const nodes = parseInline("See [guide](https://learn.example.com/a?b=1) or https://example.com/x, then stop.");
  const links = nodes.filter((n) => n.t === "link") as Array<{ href: string }>;
  assert.deepEqual(links.map((l) => l.href), ["https://learn.example.com/a?b=1", "https://example.com/x"]);
  assert.equal(inlineText(nodes).endsWith(", then stop."), true);
  assert.equal(inlineText(parseInline("(https://example.com/x)")), "(https://example.com/x)");
});

test("links: only http(s) is ever a link", () => {
  for (const bad of ["[x](javascript:alert(1))", "[x](data:text/html;base64,AAAA)", "[x](/relative)", "[x](//evil.test)"]) {
    assert.equal(parseInline(bad).some((n) => n.t === "link"), false, bad);
  }
  // no raw HTML ever survives as a node: it is just text
  assert.deepEqual(parseInline("<img src=x onerror=alert(1)>").map((n) => n.t), ["text"]);
});

test("nested and ordered lists", () => {
  const [list] = parseMarkdown("- one\n  - two\n    - three\n- four") as any[];
  assert.equal(list.t, "ul");
  assert.equal(list.items.length, 2);
  assert.equal(list.items[0].children[0].t, "ul");
  assert.equal(list.items[0].children[0].items[0].children[0].items.length, 1);

  const [ol] = parseMarkdown("3. third\n4. fourth") as any[];
  assert.equal(ol.t, "ol");
  assert.equal(ol.start, 3);
  assert.equal(ol.items.length, 2);
});

test("a numbered list survives a code block between its items", () => {
  const b = parseMarkdown("1. Disable it:\n\n```powershell\nSet-X -Y\n```\n\n2. Verify it.");
  assert.deepEqual(kinds(b), ["ol", "code", "ol"]);
  assert.equal((b[2] as any).start, 2);
});

test("fenced code keeps its text and language; an unterminated fence still renders", () => {
  const [code] = parseMarkdown("```powershell\nGet-A | Select B # | not a table\n```") as any[];
  assert.equal(code.t, "code");
  assert.equal(code.lang, "powershell");
  assert.equal(code.text, "Get-A | Select B # | not a table");
  assert.equal(code.closed, true);

  const [cut] = parseMarkdown("Run:\n```bash\nsudo systemctl stop smbd") .slice(-1) as any[];
  assert.equal(cut.t, "code");
  assert.equal(cut.closed, false);
  assert.equal(cut.text, "sudo systemctl stop smbd");
});

test("tables: header, alignment, ragged rows", () => {
  const [t] = parseMarkdown("| Signal | Value |\n| :--- | ---: |\n| CVSS | 9.8 |\n| EPSS |") as any[];
  assert.equal(t.t, "table");
  assert.deepEqual(t.align, ["left", "right"]);
  assert.equal(t.head.length, 2);
  assert.equal(t.rows.length, 2);
  assert.equal(t.rows[1].length, 2);                      // padded, never undefined
  assert.equal(inlineText(t.rows[0][1]), "9.8");
  // a pipe in prose is not a table
  assert.deepEqual(kinds(parseMarkdown("use a | b to pipe")), ["p"]);
});

test("blockquote holds blocks", () => {
  const [q] = parseMarkdown("> **Note**\n> second line\n>\n> - item") as any[];
  assert.equal(q.t, "quote");
  assert.deepEqual(kinds(q.blocks), ["p", "ul"]);
});

test("a realistic reply parses into the expected structure", () => {
  const reply = [
    "## Executive summary", "", "**192.0.2.10** exposes *SMBv1*.", "",
    "### Why", "- Reachable from the internet", "  - no foothold needed", "",
    "| a | b |", "| - | - |", "| 1 | 2 |", "",
    "1. Fix it", "2. Re-scan", "", "```bash", "echo ok", "```", "", "> caution", "", "---", "", "https://example.com/x",
  ].join("\n");
  assert.deepEqual(kinds(parseMarkdown(reply)),
    ["heading", "p", "heading", "ul", "table", "ol", "code", "quote", "hr", "p"]);
});

test("empty and odd input never throws", () => {
  assert.deepEqual(parseMarkdown(""), []);
  assert.deepEqual(parseMarkdown("\n\n  \n"), []);
  for (const s of ["```", "|", "> ", "- ", "1.", "**", "[", "![x]()", "`", "#", "####### seven"]) {
    assert.doesNotThrow(() => parseMarkdown(s), s);
  }
});
