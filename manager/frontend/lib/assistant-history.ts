// Remembered Security Advisor conversations.
//
// Closing the drawer, reloading the tab or opening Explain again used to throw the
// conversation away, so "explain more" could not refer to anything. Conversations are now
// kept per finding (and one for general questions) in session storage — this tab only,
// wiped on logout by clearSessionState() — and restored when the drawer opens again.
import type { AdvisorVM, FactCardVM } from "./assistant";

export type StoredMsg = { role: "user" | "assistant"; content: string };

export type ConversationSnapshot = {
  /** Finding id / CVE the conversation is about; null for general questions. */
  activeId: string | null;
  card: FactCardVM | null;
  advisor: AdvisorVM | null;
  narration: string | null;
  served: { provider: string; model: string; fallback: boolean } | null;
  thread: StoredMsg[];
  updatedAt: number;
};

export type ConversationStore = {
  /** Keys, most recently used first. */
  order: string[];
  items: Record<string, ConversationSnapshot>;
};

export const EMPTY_STORE: ConversationStore = { order: [], items: {} };
export const HISTORY_LIMITS = { conversations: 8, messages: 40 } as const;
export const GENERAL_KEY = "general";

export const keyFor = (activeId: string | null) => (activeId ? String(activeId).toLowerCase() : GENERAL_KEY);

/** The conversation to show when the drawer opens. For a finding, that finding's own
 *  conversation (nothing else); for a plain open, the one used most recently. */
export function pickConversation(store: ConversationStore | null | undefined, findingId: string | null): ConversationSnapshot | null {
  if (!store) return null;
  const key = findingId ? keyFor(findingId) : store.order[0];
  const snap = key ? store.items[key] : undefined;
  if (!snap) return null;
  if (findingId && !snap.card) return null;                // nothing worth restoring without the brief
  return snap;
}

export function saveConversation(
  store: ConversationStore | null | undefined,
  snap: Omit<ConversationSnapshot, "updatedAt">,
  now: number = Date.now(),
): ConversationStore {
  const base = store ?? EMPTY_STORE;
  const key = keyFor(snap.activeId);
  const items = { ...base.items, [key]: { ...snap, thread: snap.thread.slice(-HISTORY_LIMITS.messages), updatedAt: now } };
  const order = [key, ...base.order.filter((k) => k !== key)];
  for (const dropped of order.splice(HISTORY_LIMITS.conversations)) delete items[dropped];
  return { order, items };
}

export function forgetConversation(store: ConversationStore | null | undefined, activeId: string | null): ConversationStore {
  const base = store ?? EMPTY_STORE;
  const key = keyFor(activeId);
  if (!(key in base.items)) return base;
  const items = { ...base.items };
  delete items[key];
  return { order: base.order.filter((k) => k !== key), items };
}
