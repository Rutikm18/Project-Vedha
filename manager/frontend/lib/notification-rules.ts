/**
 * Draft-editing helpers for the Settings → Notifications matrix.
 *
 * The server is the source of truth. The page edits a draft layered over what the
 * server returned, saves only the rules that changed, and says "saved" only after
 * the server confirms.
 */

export const CHANNELS = ["email", "slack"] as const;
export type Channel = (typeof CHANNELS)[number];

export interface NotificationRule {
  event: string;
  label: string;
  cadence: string;
  enabled: boolean;
  channels: Channel[];
  /** False: nothing in the product emits this event yet. */
  connected: boolean;
  /** False: the default, never changed by this organisation. */
  is_custom: boolean;
}

export type RuleDraft = Record<string, { enabled: boolean; channels: Channel[] }>;

const ordered = (channels: readonly string[]): Channel[] =>
  CHANNELS.filter((c) => channels.includes(c));

/** The rule as it should display: the draft's choice if there is one, else the server's. */
export function effectiveRule(rule: NotificationRule, draft: RuleDraft): NotificationRule {
  const d = draft[rule.event];
  return d ? { ...rule, enabled: d.enabled, channels: ordered(d.channels) } : rule;
}

/** True when the draft's choice for this rule differs from what the server holds. */
function differs(rule: NotificationRule, d: RuleDraft[string]): boolean {
  return d.enabled !== rule.enabled || ordered(d.channels).join() !== ordered(rule.channels).join();
}

/** Events whose draft choice differs from the saved rule. */
export function changedEvents(rules: NotificationRule[], draft: RuleDraft): string[] {
  return rules.filter((r) => draft[r.event] && differs(r, draft[r.event])).map((r) => r.event);
}

export function setEnabled(rule: NotificationRule, draft: RuleDraft, enabled: boolean): RuleDraft {
  const cur = effectiveRule(rule, draft);
  return { ...draft, [rule.event]: { enabled, channels: cur.channels } };
}

export function toggleChannel(rule: NotificationRule, draft: RuleDraft, channel: Channel): RuleDraft {
  const cur = effectiveRule(rule, draft);
  const next = cur.channels.includes(channel)
    ? cur.channels.filter((c) => c !== channel)
    : ordered([...cur.channels, channel]);
  return { ...draft, [rule.event]: { enabled: cur.enabled, channels: next } };
}

/** The PUT body: only the rules that changed. */
export function savePayload(rules: NotificationRule[], draft: RuleDraft) {
  const changed = new Set(changedEvents(rules, draft));
  return {
    rules: rules
      .filter((r) => changed.has(r.event))
      .map((r) => ({ event: r.event, enabled: draft[r.event].enabled, channels: ordered(draft[r.event].channels) })),
  };
}

/** A rule that is on but has nowhere to go: worth a hint, since it would never be delivered. */
export function hasNoChannel(rule: NotificationRule): boolean {
  return rule.enabled && rule.channels.length === 0;
}
