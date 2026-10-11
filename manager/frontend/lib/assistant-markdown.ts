// Small, dependency-free Markdown parser for assistant replies.
//
// Models answer in Markdown: headings, nested lists, tables, fenced code, quotes,
// links. The old renderer understood only a few of those, so everything else showed
// up as raw pipes, backticks and asterisks. This parser produces a plain tree that a
// React component renders — no HTML strings, so nothing a model emits can inject
// markup, and links are limited to http(s).
//
// It is deliberately forgiving: an unterminated code fence (a reply cut off by the
// token limit) still renders as code, and unknown syntax falls back to plain text.

export type Inline =
  | { t: "text"; text: string }
  | { t: "br" }
  | { t: "code"; text: string }
  | { t: "strong"; children: Inline[] }
  | { t: "em"; children: Inline[] }
  | { t: "del"; children: Inline[] }
  | { t: "link"; href: string; children: Inline[] };

export type ListItem = { inlines: Inline[]; children: Block[] };

export type Block =
  | { t: "heading"; level: 1 | 2 | 3 | 4; inlines: Inline[] }
  | { t: "p"; inlines: Inline[] }
  | { t: "ul"; items: ListItem[] }
  | { t: "ol"; start: number; items: ListItem[] }
  | { t: "quote"; blocks: Block[] }
  | { t: "code"; lang: string; text: string; closed: boolean }
  | { t: "table"; align: Array<"left" | "center" | "right" | null>; head: Inline[][]; rows: Inline[][][] }
  | { t: "hr" };

// ── Inline ──────────────────────────────────────────────────────────────────

const SAFE_URL = /^https?:\/\/[^\s<>"']+$/i;

// Order matters: the first alternative that matches at the earliest position wins.
//  1 code span   2 **bold**   3 __bold__   4 ~~strike~~   5 *em*   6 _em_
//  7-8 [label](url)   9 bare URL
const INLINE_RE = new RegExp(
  [
    "(`+)([\\s\\S]*?[^`])\\1(?!`)",
    "\\*\\*(?=\\S)([\\s\\S]*?\\S)\\*\\*",
    "(?<![\\w_])__(?=\\S)([\\s\\S]*?\\S)__(?![\\w_])",
    "~~(?=\\S)([\\s\\S]*?\\S)~~",
    "\\*(?=[^\\s*])([\\s\\S]*?[^\\s*])\\*(?!\\*)",
    "(?<![\\w_])_(?=[^\\s_])([\\s\\S]*?[^\\s_])_(?![\\w_])",
    "\\[([^\\]\\n]+)\\]\\(([^)\\s]+)\\)",
    "(https?:\\/\\/[^\\s<>\"'`]+)",
  ].join("|"),
  "g",
);

// Sentence punctuation that belongs to the prose, not to a bare URL.
const URL_TAIL = /[.,;:!?)\]}'"]+$/;

export function parseInline(source: string): Inline[] {
  const out: Inline[] = [];
  const pushText = (text: string) => {
    if (!text) return;
    const parts = text.split("\n");
    parts.forEach((part, i) => {
      if (i > 0) out.push({ t: "br" });
      if (part) out.push({ t: "text", text: part });
    });
  };

  let last = 0;
  // A fresh regex per call: the recursive parseInline() below must not reset the
  // `lastIndex` of the loop that is still running in its caller.
  const re = new RegExp(INLINE_RE.source, "g");
  let m: RegExpExecArray | null;
  while ((m = re.exec(source)) !== null) {
    pushText(source.slice(last, m.index));
    last = m.index + m[0].length;

    if (m[1] !== undefined) {
      out.push({ t: "code", text: m[2].replace(/^ ([\s\S]*) $/, "$1") });
    } else if (m[3] !== undefined || m[4] !== undefined) {
      out.push({ t: "strong", children: parseInline(m[3] ?? m[4]) });
    } else if (m[5] !== undefined) {
      out.push({ t: "del", children: parseInline(m[5]) });
    } else if (m[6] !== undefined || m[7] !== undefined) {
      out.push({ t: "em", children: parseInline(m[6] ?? m[7]) });
    } else if (m[8] !== undefined) {
      if (SAFE_URL.test(m[9])) out.push({ t: "link", href: m[9], children: parseInline(m[8]) });
      else pushText(m[0]);                      // javascript:, data:, relative … stay inert text
    } else if (m[10] !== undefined) {
      const tail = URL_TAIL.exec(m[10]);
      const url = tail ? m[10].slice(0, tail.index) : m[10];
      const rest = tail ? m[10].slice(tail.index) : "";
      if (SAFE_URL.test(url)) out.push({ t: "link", href: url, children: [{ t: "text", text: url }] });
      else pushText(url);
      pushText(rest);
    }
  }
  pushText(source.slice(last));
  return out;
}

/** Plain text of an inline run — used for copy, table sizing and tests. */
export function inlineText(nodes: Inline[]): string {
  return nodes.map((n) => {
    switch (n.t) {
      case "text": case "code": return n.text;
      case "br": return "\n";
      default: return inlineText(n.children);
    }
  }).join("");
}

// ── Blocks ──────────────────────────────────────────────────────────────────

const FENCE = /^\s{0,3}(`{3,}|~{3,})\s*([\w+#.-]*)[^\n`]*$/;
const HEADING = /^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$/;
const HR = /^\s{0,3}([-*_])(?:\s*\1){2,}\s*$/;
const LIST = /^([ \t]*)([-*+]|\d{1,9}[.)])[ \t]+(.*)$/;
const QUOTE = /^\s{0,3}>\s?(.*)$/;
const TABLE_SEP = /^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$/;

const indentOf = (line: string) => line.match(/^[ \t]*/)![0].replace(/\t/g, "    ").length;
const isBlank = (line: string) => line.trim() === "";

function splitRow(line: string): string[] {
  let s = line.trim();
  if (s.startsWith("|")) s = s.slice(1);
  if (s.endsWith("|") && !s.endsWith("\\|")) s = s.slice(0, -1);
  return s.split(/(?<!\\)\|/).map((c) => c.trim().replace(/\\\|/g, "|"));
}

function alignOf(cell: string): "left" | "center" | "right" | null {
  const c = cell.trim();
  const l = c.startsWith(":"), r = c.endsWith(":");
  return l && r ? "center" : r ? "right" : l ? "left" : null;
}

function startsBlock(line: string, next?: string): boolean {
  return FENCE.test(line) || HEADING.test(line) || HR.test(line) || QUOTE.test(line) || LIST.test(line)
    || (line.includes("|") && next !== undefined && TABLE_SEP.test(next) && next.includes("-")
        && (next.includes("|") || line.trim().startsWith("|")));
}

function parseList(lines: string[], start: number): { block: Block; next: number } {
  const first = LIST.exec(lines[start])!;
  const base = indentOf(lines[start]);
  const ordered = /\d/.test(first[2]);
  const items: ListItem[] = [];
  let i = start;

  while (i < lines.length) {
    const line = lines[i];
    const m = LIST.exec(line);

    if (isBlank(line)) {
      // A blank line inside a list is fine when the list carries on after it.
      let j = i + 1;
      while (j < lines.length && isBlank(lines[j])) j++;
      if (j < lines.length && LIST.test(lines[j]) && indentOf(lines[j]) >= base) { i = j; continue; }
      if (j < lines.length && indentOf(lines[j]) > base && items.length && !startsBlock(lines[j], lines[j + 1])) {
        items[items.length - 1].inlines.push({ t: "br" }, ...parseInline(lines[j].trim()));
        i = j + 1; continue;
      }
      break;
    }

    if (m) {
      const ind = indentOf(line);
      if (ind < base) break;
      if (ind > base && items.length) {                      // nested list
        const nested = parseList(lines, i);
        items[items.length - 1].children.push(nested.block);
        i = nested.next; continue;
      }
      if (/\d/.test(m[2]) !== ordered) break;                // marker type changed → new list
      items.push({ inlines: parseInline(m[3]), children: [] });
      i++; continue;
    }

    // Continuation of the previous item (indented), but never a new block.
    if (items.length && indentOf(line) > base && !startsBlock(line, lines[i + 1])) {
      items[items.length - 1].inlines.push({ t: "br" }, ...parseInline(line.trim()));
      i++; continue;
    }
    // A fenced block indented under an item belongs to that item.
    if (items.length && indentOf(line) > base && FENCE.test(line)) {
      const nested = parseBlocks(lines, i, (l) => !isBlank(l) && indentOf(l) <= base);
      items[items.length - 1].children.push(...nested.blocks);
      i = nested.next; continue;
    }
    break;
  }

  const startNum = ordered ? Math.max(0, parseInt(first[2], 10)) : 1;
  return { block: ordered ? { t: "ol", start: startNum, items } : { t: "ul", items }, next: i };
}

function parseBlocks(lines: string[], start: number, stop?: (line: string) => boolean): { blocks: Block[]; next: number } {
  const blocks: Block[] = [];
  let i = start;

  while (i < lines.length) {
    const line = lines[i];
    if (stop && i > start && stop(line)) break;
    if (isBlank(line)) { i++; continue; }

    const fence = FENCE.exec(line);
    if (fence) {
      const marker = fence[1][0];
      const min = fence[1].length;
      const body: string[] = [];
      let j = i + 1, closed = false;
      while (j < lines.length) {
        const t = lines[j].trim();
        if (t.length >= min && t.split("").every((c) => c === marker)) { closed = true; j++; break; }
        body.push(lines[j]); j++;
      }
      // Remove the indentation the fence itself carried.
      const pad = Math.min(indentOf(line), ...body.filter((l) => !isBlank(l)).map(indentOf));
      blocks.push({ t: "code", lang: fence[2] || "", closed,
        text: body.map((l) => l.replace(/\t/g, "    ").slice(Math.min(pad, indentOf(l)))).join("\n").replace(/\s+$/, "") });
      i = j; continue;
    }

    const heading = HEADING.exec(line);
    if (heading) {
      // Four levels are enough for a chat bubble; # … #### map 1:1, deeper ones fold into 4.
      blocks.push({ t: "heading", level: Math.min(heading[1].length, 4) as 1 | 2 | 3 | 4, inlines: parseInline(heading[2]) });
      i++; continue;
    }

    if (HR.test(line)) { blocks.push({ t: "hr" }); i++; continue; }

    if (line.includes("|") && i + 1 < lines.length && TABLE_SEP.test(lines[i + 1]) && lines[i + 1].includes("-")
        && (lines[i + 1].includes("|") || line.trim().startsWith("|"))) {
      const head = splitRow(line);
      const align = splitRow(lines[i + 1]).map(alignOf);
      const rows: Inline[][][] = [];
      let j = i + 2;
      while (j < lines.length && !isBlank(lines[j]) && lines[j].includes("|")) {
        const cells = splitRow(lines[j]);
        rows.push(head.map((_, c) => parseInline(cells[c] ?? "")));
        j++;
      }
      blocks.push({ t: "table", align: head.map((_, c) => align[c] ?? null), head: head.map(parseInline), rows });
      i = j; continue;
    }

    if (QUOTE.test(line)) {
      const inner: string[] = [];
      let j = i;
      while (j < lines.length && QUOTE.test(lines[j])) { inner.push(QUOTE.exec(lines[j])![1]); j++; }
      blocks.push({ t: "quote", blocks: parseBlocks(inner, 0).blocks });
      i = j; continue;
    }

    if (LIST.test(line)) {
      const { block, next } = parseList(lines, i);
      blocks.push(block); i = next; continue;
    }

    // Paragraph: consecutive plain lines. A single newline is a visible line break,
    // because models use it for "Host: …\nPort: …" style lines.
    const para: string[] = [];
    let j = i;
    while (j < lines.length && !isBlank(lines[j]) && (j === i || !startsBlock(lines[j], lines[j + 1]))) {
      para.push(lines[j].trim()); j++;
    }
    blocks.push({ t: "p", inlines: parseInline(para.join("\n")) });
    i = j;
  }
  return { blocks, next: i };
}

export function parseMarkdown(source: string): Block[] {
  const text = String(source ?? "").replace(/\r\n?/g, "\n");
  return parseBlocks(text.split("\n"), 0).blocks;
}
