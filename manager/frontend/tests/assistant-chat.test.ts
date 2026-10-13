/* Assistant chat: long conversations must keep working, and replies must render as
 * structure — never raw Markdown, never injected markup. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { CHAT_LIMITS, trimThread } from "../lib/assistant";
import { AssistantText } from "../components/assistant/AssistantText";

type M = { role: "user" | "assistant"; content: string };
const turn = (i: number, len = 20): M => ({ role: i % 2 === 0 ? "user" : "assistant", content: `${i}:`.padEnd(len, "x") });

test("a short thread is sent unchanged", () => {
  const t = [turn(0), turn(1), turn(2)];
  assert.deepEqual(trimThread(t), t);
});

test("a long thread keeps only the newest turns the chat route accepts, starting on a user turn", () => {
  const t = Array.from({ length: 40 }, (_, i) => turn(i));
  const out = trimThread(t);
  assert.ok(out.length <= CHAT_LIMITS.messages);
  assert.equal(out[0].role, "user");
  assert.equal(out[out.length - 1], t[t.length - 1]);        // the question just asked is never dropped
});

test("big turns are clipped and the oldest are dropped until the total fits", () => {
  const big = (i: number): M => ({ role: i % 2 === 0 ? "user" : "assistant", content: "y".repeat(6_000) });
  const out = trimThread(Array.from({ length: 10 }, (_, i) => big(i)));
  assert.ok(out.every((m) => m.content.length <= CHAT_LIMITS.perMessage));
  assert.ok(out.reduce((n, m) => n + m.content.length, 0) <= CHAT_LIMITS.total);
  assert.equal(out[0].role, "user");
});

test("limits match the BFF chat route, so the two cannot drift apart", () => {
  const route = readFileSync(join(process.cwd(), "app/api/assistant/chat/route.ts"), "utf8");
  assert.match(route, new RegExp(`MAX_MESSAGES = ${CHAT_LIMITS.messages + 2}\\b`));      // route allows 16, client sends ≤ 14
  assert.match(route, /MAX_MESSAGE_CHARS = 4_000/);
  assert.match(route, /MAX_TOTAL_CHARS = 16_000/);
  assert.ok(CHAT_LIMITS.perMessage <= 4_000 && CHAT_LIMITS.total <= 16_000 && CHAT_LIMITS.messages <= 16);
});

const html = (md: string) => renderToStaticMarkup(React.createElement(AssistantText, { content: md }));

test("a rich reply renders as structure, with no raw Markdown left on the page", () => {
  const out = html([
    "## Summary", "", "**bold** and *italic* and `code`", "",
    "| a | b |", "| - | - |", "| 1 | 2 |", "",
    "- one", "  - two", "", "1. first", "2. second", "",
    "```bash", "echo hi", "```", "", "> quoted", "", "---", "", "[ok](https://example.com/x)",
  ].join("\n"));
  for (const tag of ["<h4", "<strong>", "<em>", "<table>", "<th", "<ul>", "<ol", "<figure", "<pre", "<blockquote>", "<hr/>", "<a "]) {
    assert.ok(out.includes(tag), `missing ${tag}`);
  }
  assert.doesNotMatch(out, /\*\*|```|\| a \||&gt; quoted|\| - \|/);
  assert.match(out, /rel="noopener noreferrer"/);
  assert.match(out, /target="_blank"/);
});

test("model output can never become markup or a script link", () => {
  const out = html("<script>alert(1)</script> <img src=x onerror=alert(1)> [x](javascript:alert(1))");
  assert.doesNotMatch(out, /<script|<img/);
  assert.doesNotMatch(out, /href="javascript:/i);
  assert.match(out, /&lt;script&gt;/);
});

test("a reply cut off inside a code fence says so", () => {
  const out = html("Run:\n```bash\nsudo systemctl stop smbd");
  assert.match(out, /sudo systemctl stop smbd/);
  assert.match(out, /cut off by the length limit/);
});

test("the drawer and Brain page scroll only the chat, and start new answers at their first line", () => {
  for (const file of ["components/assistant/AssistantDrawer.tsx", "app/aibrain/workspace.tsx"]) {
    const src = readFileSync(join(process.cwd(), file), "utf8");
    assert.match(src, /scrollChildToTop\(/, file);
    assert.doesNotMatch(src, /scrollIntoView\(/, file);             // would also scroll the page behind the chat
  }
});

test("the drawer lets people keep typing, retry a failed turn and start over", () => {
  const src = readFileSync(join(process.cwd(), "components/assistant/AssistantDrawer.tsx"), "utf8");
  assert.doesNotMatch(src, /disabled=\{loading\}\s*\n\s*rows=/);   // the box is not locked while waiting
  assert.match(src, /Try again/);
  assert.match(src, /Start a new chat/);
  assert.match(src, /trimThread\(/);
});
