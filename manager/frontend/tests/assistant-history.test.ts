/* Follow-ups must see what the user already read, and conversations must survive
 * closing the drawer. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { advisorToText, PREVIOUS_EXPLANATION_MAX_CHARS, type AdvisorVM, type FactCardVM } from "../lib/assistant";
import {
  EMPTY_STORE, forgetConversation, HISTORY_LIMITS, keyFor, pickConversation, saveConversation,
  type ConversationSnapshot,
} from "../lib/assistant-history";

const advisor: AdvisorVM = {
  whatIs: "lighttpd **1.4.54** falls in the affected range of CVE-2022-30780.",
  impact: ["Service disruption", "**Lateral movement** from the web server"],
  verify: { command: "lighttpd -v", statement: "Check the package changelog.", caveat: "Banner-inferred; backports possible." },
  patch: { available: "yes", summary: "Upgrade to 1.4.59-1 or later." },
  patchSteps: [
    { command: "sudo apt-get --only-upgrade install lighttpd", description: "Upgrade the package.", grounded: true },
    { command: null, description: "Restart the service.", grounded: false },
  ],
  improvements: ["Segment the web tier."],
};
const card = { id: "f-1", title: "lighttpd", cveIds: ["CVE-2022-30780"] } as unknown as FactCardVM;
const snap = (activeId: string | null, extra: Partial<ConversationSnapshot> = {}) => ({
  activeId, card: activeId ? card : null, advisor: null, narration: null, served: null,
  thread: [{ role: "user" as const, content: "hi" }, { role: "assistant" as const, content: "hello" }], ...extra,
});

test("the earlier Explain answer is turned into plain text the model can build on", () => {
  const text = advisorToText(advisor);
  assert.match(text, /What is the vulnerability: lighttpd 1\.4\.54 falls/);
  assert.match(text, /Impact:\n- Service disruption\n- Lateral movement/);
  assert.match(text, /How to verify: command: lighttpd -v \| Check the package changelog\. \| caveat: Banner-inferred/);
  assert.match(text, /Patch available: yes — Upgrade to 1\.4\.59-1/);
  assert.match(text, /1\. Upgrade the package\. \[sudo apt-get --only-upgrade install lighttpd\]/);
  assert.match(text, /2\. Restart the service\. \(general guidance, adapt to the environment\)/);
  assert.match(text, /Further hardening:\n- Segment the web tier\./);
  assert.doesNotMatch(text, /\*\*/);                                   // no markup noise
});

test("the explanation is capped well under the manager's context limit", () => {
  const huge = { ...advisor, impact: Array.from({ length: 400 }, (_, i) => `impact ${i} ${"x".repeat(100)}`) };
  assert.ok(advisorToText(huge).length <= PREVIOUS_EXPLANATION_MAX_CHARS);
  assert.ok(PREVIOUS_EXPLANATION_MAX_CHARS < 32_000);
});

test("the drawer sends the explanation with every follow-up, and the route forwards it as context", () => {
  const drawer = readFileSync(join(process.cwd(), "components/assistant/AssistantDrawer.tsx"), "utf8");
  assert.match(drawer, /previousExplanation: advisor \? advisorToText\(advisor\) : narration/);
  const route = readFileSync(join(process.cwd(), "app/api/assistant/chat/route.ts"), "utf8");
  assert.match(route, /previousExplanation \? \{ previousExplanation \}/);
  assert.match(route, /FOLLOWUP_MAX_TOKENS = 1_000/);                  // 600 cut answers off mid-sentence
});

test("conversations are kept per finding, newest first, and restored when it is opened again", () => {
  let store = saveConversation(EMPTY_STORE, snap("F-1"), 1);
  store = saveConversation(store, snap("CVE-2022-30780"), 2);
  assert.deepEqual(store.order, ["cve-2022-30780", "f-1"]);
  assert.equal(pickConversation(store, "F-1")?.thread.length, 2);       // key is case-insensitive
  assert.equal(pickConversation(store, "f-1")?.activeId, "F-1");
  assert.equal(pickConversation(store, "someone-else"), null);           // never another finding's chat
  assert.equal(pickConversation(store, null)?.activeId, "CVE-2022-30780"); // plain open → most recent
  // saving again moves it to the front
  store = saveConversation(store, snap("F-1"), 3);
  assert.equal(pickConversation(store, null)?.activeId, "F-1");
});

test("general questions have their own conversation", () => {
  const store = saveConversation(EMPTY_STORE, snap(null), 1);
  assert.equal(store.order[0], keyFor(null));
  assert.equal(pickConversation(store, null)?.thread[1].content, "hello");
});

test("a finding conversation without its brief is not restored", () => {
  const store = saveConversation(EMPTY_STORE, snap("F-1", { card: null }), 1);
  assert.equal(pickConversation(store, "F-1"), null);
});

test("history is bounded: 8 conversations, 40 messages each, oldest dropped", () => {
  let store = EMPTY_STORE;
  for (let i = 0; i < 12; i++) store = saveConversation(store, snap(`f-${i}`), i);
  assert.equal(store.order.length, HISTORY_LIMITS.conversations);
  assert.equal(Object.keys(store.items).length, HISTORY_LIMITS.conversations);
  assert.equal(store.items["f-0"], undefined);
  assert.ok(store.items["f-11"]);
  const long = Array.from({ length: 100 }, (_, i) => ({ role: (i % 2 ? "assistant" : "user") as "user" | "assistant", content: String(i) }));
  const kept = saveConversation(EMPTY_STORE, snap("f-x", { thread: long }), 1).items["f-x"].thread;
  assert.equal(kept.length, HISTORY_LIMITS.messages);
  assert.equal(kept[kept.length - 1].content, "99");                    // newest kept
});

test("New chat forgets exactly that conversation", () => {
  let store = saveConversation(EMPTY_STORE, snap("a"), 1);
  store = saveConversation(store, snap("b"), 2);
  const after = forgetConversation(store, "b");
  assert.deepEqual(after.order, ["a"]);
  assert.equal(pickConversation(after, null)?.activeId, "a");
  assert.equal(forgetConversation(after, "never-saved"), after);
});

test("the drawer restores on open, does not refetch a restored finding, and 'New chat' clears it", () => {
  const drawer = readFileSync(join(process.cwd(), "components/assistant/AssistantDrawer.tsx"), "utf8");
  assert.match(drawer, /pickConversation\(history, findingId\)/);
  assert.match(drawer, /loadedFor\.current === findingId/);
  assert.match(drawer, /forgetConversation\(current, activeId\)/);
  assert.match(drawer, /saveConversation\(current,/);
});
