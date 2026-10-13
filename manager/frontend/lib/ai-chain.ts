/**
 * The Manager's automatic AI provider chain, as shown on the AI Brain page and in
 * Settings → AI runtime. The chain is built and ordered on the server (premium →
 * budget → free → local); this module only describes it for people.
 */

export type ProviderId = "ollama" | "local_openai" | "openrouter" | "anthropic" | "openai" | "gemini" | "groq";

/** One provider in the Manager's automatic chain, in the order it is tried. */
export interface ChainEntry {
  provider: ProviderId;
  model: string;
  tier: "premium" | "budget" | "free" | "local";
  state: "healthy" | "cooling" | "blocked" | "probing";
  reason?: string | null;
  retry_in_s?: number | null;
  spend_today_usd?: number | null;
  daily_cap_usd?: number | null;
}

export function providerLabel(provider?: string | null): string {
  if (provider === "openai") return "OpenAI";
  if (provider === "openrouter") return "OpenRouter";
  if (provider === "anthropic") return "Anthropic";
  if (provider === "gemini") return "Google Gemini";
  if (provider === "local_openai") return "In-house model";
  if (provider === "groq") return "Groq";
  return "Ollama";
}

export const TIER_LABEL: Record<ChainEntry["tier"], string> = {
  premium: "Premium", budget: "Budget", free: "Free · masked", local: "Local",
};

export const REASON_LABEL: Record<string, string> = {
  rate_limit: "rate limited", headroom: "limit reached", overloaded: "overloaded",
  timeout: "timed out", network: "unreachable", spend_cap: "monthly spend cap",
  billing: "out of credit", auth: "key rejected", probe_in_flight: "recovering",
};

export function chainStateText(entry: ChainEntry): string {
  if (entry.state === "healthy") return "ready";
  if (entry.state === "probing") return "recovering";
  const reason = REASON_LABEL[entry.reason ?? ""] ?? entry.reason ?? entry.state;
  return entry.retry_in_s ? `${reason} · ${Math.ceil(entry.retry_in_s / 60)} min` : reason;
}

/** The first entry that is not cooling down: what will most likely answer next. */
export function nextUp(chain: ChainEntry[]): ChainEntry | undefined {
  return chain.find((e) => e.state === "healthy" || e.state === "probing") ?? chain[0];
}

/** "$1.20 of $20 today", or null when no cap is set for this provider. */
export function spendText(entry: ChainEntry): string | null {
  if (entry.daily_cap_usd == null) return null;
  return `$${(entry.spend_today_usd ?? 0).toFixed(2)} of $${entry.daily_cap_usd} today`;
}

export interface ChainSummary {
  total: number;
  ready: number;
  cooling: number;
  blocked: number;
}

export function chainSummary(chain: ChainEntry[]): ChainSummary {
  const count = (...states: ChainEntry["state"][]) => chain.filter((e) => states.includes(e.state)).length;
  return { total: chain.length, ready: count("healthy", "probing"), cooling: count("cooling"), blocked: count("blocked") };
}

/** What an operator can do about a provider that is not answering; null when nothing is needed. */
export function fixHint(entry: ChainEntry): string | null {
  if (entry.state === "healthy" || entry.state === "probing") return null;
  switch (entry.reason) {
    case "billing": return "Out of credit. Add credit with the provider.";
    case "auth": return "The key was rejected. Check it in the server settings.";
    case "spend_cap": return "Daily or monthly spend cap reached. It resumes when the cap resets.";
    case "rate_limit":
    case "headroom": return "Over its rate limit. It recovers on its own.";
    default: return entry.state === "cooling" ? "Cooling down after errors. It is retried automatically." : null;
  }
}

/** The server setting that adds each provider to the chain. */
export const PROVIDER_ENV: Record<ProviderId, string> = {
  anthropic: "ANTHROPIC_API_KEY",
  openai: "OPENAI_API_KEY",
  gemini: "GEMINI_API_KEY",
  groq: "GROQ_API_KEY",
  openrouter: "OPENROUTER_API_KEY",
  ollama: "OLLAMA_BASE_URL",
  local_openai: "LOCAL_LLM_BASE_URL",
};
