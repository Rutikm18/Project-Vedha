"use client";

import React, { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Brain, CheckCircle2, ChevronRight, Cloud, Database, Eraser,
  LockKeyhole, Send, Server, ShieldCheck, Sparkles, TriangleAlert,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { PortalShell } from "../../components/portal/PortalShell";
import {
  createAIBrainWorkspaceApi,
  type AIBrainWorkspaceSurface,
} from "../../lib/aibrain-workspace-api";
import { FactCard } from "../../components/assistant/FactCard";
import { AssistantText } from "../../components/assistant/AssistantText";
import type { FactCardVM } from "../../lib/assistant";
import { newId } from "../../lib/uuid";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  provider?: string;
  model?: string;
  /** True when a lower tier than the first configured provider answered. */
  fallback?: boolean;
  factCard?: FactCardVM;
  /** Sector domain expert the answer was written as (null = general advisor). */
  skillLabel?: string | null;
  jurisdictions?: string[];
  /** Regulatory citations the Manager could not find in its compliance packs. */
  unverifiedCitations?: string[];
}

type ProviderId = "ollama" | "local_openai" | "openrouter" | "anthropic" | "openai" | "gemini" | "groq";

/** One provider in the Manager's automatic chain, in the order it is tried. */
interface ChainEntry {
  provider: ProviderId;
  model: string;
  tier: "premium" | "budget" | "free" | "local";
  state: "healthy" | "cooling" | "blocked" | "probing";
  reason?: string | null;
  retry_in_s?: number | null;
  spend_today_usd?: number | null;
  daily_cap_usd?: number | null;
}

interface AiStatus {
  provider: ProviderId | null;
  model: string;
  configured: boolean;
  privacy: "local" | "cloud";
  reason?: string;
  chain?: ChainEntry[];
  providers: Array<{
    id: ProviderId;
    label: string;
    configured: boolean;
    privacy: "local" | "cloud";
    default_model: string;
    models: string[];
    reason?: string;
  }>;
}

interface Engagement {
  id: string;
  name: string;
  client?: string;
  status?: string;
}

const STARTER_PROMPTS = [
  {
    title: "Analyze any CVE",
    prompt: "Explain CVE-2021-44228 in depth: summary paragraph, key facts, impact bullets, recorded severity and score, verification, ordered remediation actions, OS-specific hardening, and evidence gaps.",
  },
  {
    title: "Executive risk brief",
    prompt: "Summarize the highest-priority recorded risks for a client executive. Separate confirmed evidence from unknowns.",
  },
  {
    title: "Remediation sequence",
    prompt: "Create a remediation sequence for the selected engagement, prioritizing exploitability, business impact, and SLA urgency.",
  },
  {
    title: "Detection gaps",
    prompt: "Identify the most important detection coverage gaps in the selected engagement and suggest defensive validation steps.",
  },
];

const WELCOME: Message = {
  id: "welcome",
  role: "assistant",
  content: "Ask about any published CVE or select an engagement for organization-specific analysis. Public CVE metadata is never presented as proof that your organization is affected.",
};

function providerLabel(provider?: string | null) {
  if (provider === "openai") return "OpenAI";
  if (provider === "openrouter") return "OpenRouter";
  if (provider === "anthropic") return "Anthropic";
  if (provider === "gemini") return "Google Gemini";
  if (provider === "local_openai") return "In-house model";
  if (provider === "groq") return "Groq";
  return "Ollama";
}

const TIER_LABEL: Record<ChainEntry["tier"], string> = {
  premium: "Premium", budget: "Budget", free: "Free · masked", local: "Local",
};

const REASON_LABEL: Record<string, string> = {
  rate_limit: "rate limited", headroom: "limit reached", overloaded: "overloaded",
  timeout: "timed out", network: "unreachable", spend_cap: "monthly spend cap",
  billing: "out of credit", auth: "key rejected", probe_in_flight: "recovering",
};

function chainStateText(entry: ChainEntry): string {
  if (entry.state === "healthy") return "ready";
  if (entry.state === "probing") return "recovering";
  const reason = REASON_LABEL[entry.reason ?? ""] ?? entry.reason ?? entry.state;
  return entry.retry_in_s ? `${reason} · ${Math.ceil(entry.retry_in_s / 60)} min` : reason;
}

export function AIBrainWorkspace({ surface = "manager" }: { surface?: AIBrainWorkspaceSurface }) {
  const [messages, setMessages] = useState<Message[]>([WELCOME]);
  const [input, setInput] = useState("");
  const [engagementId, setEngagementId] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const endRef = useRef<HTMLDivElement>(null);
  const api = React.useMemo(() => createAIBrainWorkspaceApi(surface), [surface]);

  const statusQuery = useQuery({
    queryKey: ["ai-brain", surface, "status"],
    queryFn: () => api.status<AiStatus>(),
    refetchInterval: 30_000,
  });
  const engagementsQuery = useQuery({
    queryKey: ["ai-brain", surface, "engagements"],
    queryFn: () => api.engagements<{ engagements?: Engagement[] }>(),
  });
  const status = statusQuery.data;
  const engagements = engagementsQuery.data?.engagements ?? [];
  const effectiveEngagementId = engagementId || (surface === "portal" ? engagements[0]?.id ?? "" : "");
  const chain = status?.chain ?? [];
  // The Manager routes every request automatically; the first entry that is not
  // cooling down is what will most likely answer next.
  const nextUp = chain.find((entry) => entry.state === "healthy" || entry.state === "probing") ?? chain[0];

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [messages, sending]);

  useEffect(() => {
    if (!textareaRef.current) return;
    textareaRef.current.style.height = "auto";
    textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
  }, [input]);

  async function send(prompt?: string) {
    const content = (prompt ?? input).trim();
    if (!content || sending) return;
    const user: Message = { id: newId(), role: "user", content };
    const conversation = [...messages.filter((message) => message.id !== "welcome"), user];
    setMessages((current) => [...current, user]);
    setInput("");
    setSending(true);
    setError(null);
    try {
      const response = await api.send<{
        content?: string; error?: string; provider?: string; model?: string; factCard?: FactCardVM;
        fallback?: boolean;
        skillLabel?: string | null; skill_label?: string | null; jurisdictions?: string[];
        unverifiedCitations?: string[]; unverified_citations?: string[];
      }>({
          messages: conversation.map(({ role, content: messageContent }) => ({ role, content: messageContent })),
          engagementId: effectiveEngagementId || undefined,
        });
      setMessages((current) => [...current, {
        id: newId(),
        role: "assistant",
        content: response.content || "The configured model returned no content.",
        provider: response.provider,
        model: response.model,
        fallback: response.fallback ?? false,
        factCard: response.factCard,
        // Manager BFF returns camelCase; the portal backend returns snake_case.
        skillLabel: response.skillLabel ?? response.skill_label ?? null,
        jurisdictions: response.jurisdictions ?? [],
        unverifiedCitations: response.unverifiedCitations ?? response.unverified_citations ?? [],
      }]);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "The AI runtime could not complete this request.");
    } finally {
      setSending(false);
      textareaRef.current?.focus();
    }
  }

  const selectedEngagement = engagements.find((engagement) => engagement.id === effectiveEngagementId);
  const ready = chain.length > 0 || (status?.configured ?? false);
  const selectedPrivacy = nextUp ? (nextUp.tier === "local" ? "local" : "cloud") : status?.privacy;

  const Shell = surface === "portal" ? PortalShell : PageShell;

  return (
    <Shell
      title="AI Brain"
      subtitle="Evidence-grounded security advisor"
      statusItems={[
        {
          label: "RUNTIME",
          value: status ? (nextUp ? `AUTO · ${providerLabel(nextUp.provider).toUpperCase()}` : "NOT CONFIGURED") : "CHECKING",
          color: ready ? "var(--nominal-color)" : "var(--sev-high-color)",
        },
        {
          label: "PRIVACY",
          value: selectedPrivacy === "local" ? "LOCAL" : "CLOUD",
          color: selectedPrivacy === "local" ? "var(--nominal-color)" : "var(--accent)",
        },
      ]}
    >
      <div className="brain-layout">
        <section className="brain-main">
          <header className="brain-context-bar">
            <div>
              <span className="brain-context-icon"><Database size={15} /></span>
              <label htmlFor="brain-engagement">
                <span>Ground with engagement evidence</span>
                <select id="brain-engagement" value={effectiveEngagementId} onChange={(event) => setEngagementId(event.target.value)} disabled={surface === "portal"}>
                  {surface === "manager" && <option value="">No engagement selected</option>}
                  {engagements.map((engagement) => (
                    <option value={engagement.id} key={engagement.id}>{engagement.name} · {engagement.client || "No client"}</option>
                  ))}
                </select>
              </label>
            </div>
            <button
              type="button"
              className="brain-clear"
              onClick={() => { setMessages([WELCOME]); setError(null); }}
              title="Clear this conversation"
            >
              <Eraser size={14} /> Clear
            </button>
          </header>

          <div className="brain-conversation" aria-live="polite">
            {messages.length === 1 && (
              <div className="brain-starters">
                <div><Sparkles size={16} /><span>Start with a decision-focused question</span></div>
                <div className="brain-starter-grid">
                  {STARTER_PROMPTS.map((starter) => (
                    <button key={starter.title} onClick={() => void send(starter.prompt)} disabled={sending || !ready}>
                      <strong>{starter.title}</strong>
                      <span>{starter.prompt}</span>
                      <ChevronRight size={14} />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((message) => (
              <article className="brain-message" data-role={message.role} key={message.id}>
                <span className="brain-avatar">
                  {message.role === "assistant" ? <Brain size={16} /> : <ShieldCheck size={16} />}
                </span>
                <div>
                  <header>
                    <strong>{message.role === "assistant" ? "Vedha AI" : "You"}</strong>
                    {message.skillLabel && (
                      <span className="intel-skill" title="Answer framed by this sector's domain-expert skill">
                        {message.skillLabel}{message.jurisdictions?.length ? ` · ${message.jurisdictions.join(", ")}` : ""}
                      </span>
                    )}
                    {message.model && <span>{providerLabel(message.provider)} · {message.model}</span>}
                    {message.fallback && (
                      <span className="brain-fallback-badge" title="The first provider in the chain was unavailable, so the next one answered">
                        fallback
                      </span>
                    )}
                  </header>
                  {message.factCard && <FactCard vm={message.factCard} />}
                  {message.role === "assistant"
                    ? <AssistantText content={message.content} />
                    : <p>{message.content}</p>}
                  {message.unverifiedCitations && message.unverifiedCitations.length > 0 && (
                    <p className="intel-citation-warning" role="note">
                      Not found in Vedha&apos;s compliance library — verify before relying on:{" "}
                      {message.unverifiedCitations.join(", ")}
                    </p>
                  )}
                </div>
              </article>
            ))}

            {sending && (
              <article className="brain-message" data-role="assistant">
                <span className="brain-avatar"><Brain size={16} /></span>
                <div><header><strong>Vedha AI</strong></header><div className="brain-thinking"><span /><span /><span /> Analyzing recorded evidence…</div></div>
              </article>
            )}
            {error && (
              <div className="brain-error" role="alert">
                <TriangleAlert size={16} />
                <div><strong>AI request could not be completed</strong><span>{error}</span></div>
              </div>
            )}
            <div ref={endRef} />
          </div>

          <footer className="brain-composer">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  void send();
                }
              }}
              placeholder={ready ? "Paste CVE-YYYY-NNNN or ask about risk, impact, evidence, and remediation…" : "Configure the AI runtime in Settings to begin"}
              aria-label="Message AI Brain"
              disabled={!ready || sending}
              rows={1}
            />
            <button type="button" onClick={() => void send()} disabled={!ready || sending || !input.trim()} aria-label="Send message">
              <Send size={17} />
            </button>
            <div className="brain-composer-meta">
              <span><LockKeyhole size={11} /> Server-owned prompt · keys never reach the browser</span>
              <span>Enter to send · Shift+Enter for new line</span>
            </div>
          </footer>
        </section>

        <aside className="brain-rail">
          <section className="brain-runtime-card" data-ready={ready}>
            <header>
              <span>{selectedPrivacy === "local" ? <Server size={17} /> : <Cloud size={17} />}</span>
              <div><strong>Automatic AI runtime</strong><small>{ready ? "Tries each provider in order · no choice needed" : "Needs configuration"}</small></div>
              <span className="brain-runtime-dot" />
            </header>
            {chain.length > 0 && (
              <ol className="brain-chain" aria-label="Provider order">
                {chain.map((entry) => (
                  <li key={entry.provider} data-state={entry.state}>
                    <span className="brain-chain-dot" aria-hidden="true" />
                    <div>
                      <strong>{providerLabel(entry.provider)}</strong>
                      <small>{entry.model}</small>
                    </div>
                    <div className="brain-chain-meta">
                      <span>{TIER_LABEL[entry.tier]}</span>
                      <small>
                        {chainStateText(entry)}
                        {entry.daily_cap_usd != null && ` · $${(entry.spend_today_usd ?? 0).toFixed(2)}/$${entry.daily_cap_usd}`}
                      </small>
                    </div>
                  </li>
                ))}
              </ol>
            )}
            <dl>
              <div><dt>Execution</dt><dd>Manager only</dd></div>
              <div><dt>Data path</dt><dd>{selectedPrivacy === "local" ? "Local · no API fee" : "Cloud provider"}</dd></div>
              <div><dt>Grounding</dt><dd>{selectedEngagement ? selectedEngagement.name : "General only"}</dd></div>
            </dl>
            {!ready && <p>{status?.reason || "AI runtime status is unavailable."}</p>}
          </section>

          <section className="brain-guardrails">
            <header><ShieldCheck size={15} /><span>Reasoning guardrails</span></header>
            {[
              "Uses recorded facts when engagement context is selected",
              "Separates confirmed evidence from hypotheses",
              "Keeps recommendations defensive and non-destructive",
              "Never receives provider credentials from the browser",
              "Public CVE data is not treated as proof of client exposure",
              "Single-vulnerability briefs are structured and detailed (up to 600 words)",
            ].map((item) => <div key={item}><CheckCircle2 size={13} /><span>{item}</span></div>)}
          </section>

          <section className="brain-context-note">
            <Database size={15} />
            <div><strong>Context boundary</strong><p>Only the first 20 recorded findings are summarized for each request. Verify high-impact decisions in the finding detail view.</p></div>
          </section>
        </aside>
      </div>
    </Shell>
  );
}

export default function AIBrainPage() {
  return <AIBrainWorkspace />;
}
