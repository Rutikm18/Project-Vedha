"use client";

import React, { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Brain, CheckCircle2, ChevronRight, Cloud, Database, Eraser,
  LockKeyhole, Send, Server, ShieldCheck, Sparkles, TriangleAlert,
} from "lucide-react";
import { PageShell } from "../../components/PageShell";
import { fetchJson } from "../../lib/fetcher";
import { FactCard } from "../../components/assistant/FactCard";
import { AssistantText } from "../../components/assistant/AssistantText";
import type { FactCardVM } from "../../lib/assistant";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  provider?: string;
  model?: string;
  factCard?: FactCardVM;
}

interface AiStatus {
  provider: "ollama" | "openrouter" | "anthropic";
  model: string;
  configured: boolean;
  privacy: "local" | "cloud";
  reason?: string;
  providers: Array<{
    id: "ollama" | "openrouter" | "anthropic";
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
    prompt: "Explain CVE-2021-44228, including what it is, potential organizational impact, severity and score, remediation, and what must be validated.",
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

function providerLabel(provider?: string) {
  if (provider === "openrouter") return "OpenRouter";
  if (provider === "anthropic") return "Anthropic";
  return "Ollama";
}

export default function AIBrainPage() {
  const [messages, setMessages] = useState<Message[]>([WELCOME]);
  const [input, setInput] = useState("");
  const [engagementId, setEngagementId] = useState("");
  const [provider, setProvider] = useState<AiStatus["provider"] | null>(null);
  const [model, setModel] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const endRef = useRef<HTMLDivElement>(null);

  const statusQuery = useQuery({
    queryKey: ["ai-status"],
    queryFn: () => fetchJson<AiStatus>("/api/ai/status"),
    refetchInterval: 30_000,
  });
  const engagementsQuery = useQuery({
    queryKey: ["engagements"],
    queryFn: () => fetchJson<{ engagements?: Engagement[] }>("/api/engagements"),
  });
  const status = statusQuery.data;
  const engagements = engagementsQuery.data?.engagements ?? [];
  const selectedProvider = status?.providers.find((item) => item.id === (provider ?? status.provider));
  const selectedModel = model || selectedProvider?.default_model || status?.model || "";

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
    const user: Message = { id: crypto.randomUUID(), role: "user", content };
    const conversation = [...messages.filter((message) => message.id !== "welcome"), user];
    setMessages((current) => [...current, user]);
    setInput("");
    setSending(true);
    setError(null);
    try {
      const response = await fetchJson<{ content?: string; error?: string; provider?: string; model?: string; factCard?: FactCardVM }>("/api/brain", {
        method: "POST",
        body: JSON.stringify({
          messages: conversation.map(({ role, content: messageContent }) => ({ role, content: messageContent })),
          engagementId: engagementId || undefined,
          provider: selectedProvider?.id,
          model: selectedModel || undefined,
        }),
      });
      setMessages((current) => [...current, {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.content || "The configured model returned no content.",
        provider: response.provider,
        model: response.model,
        factCard: response.factCard,
      }]);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "The AI runtime could not complete this request.");
    } finally {
      setSending(false);
      textareaRef.current?.focus();
    }
  }

  const selectedEngagement = engagements.find((engagement) => engagement.id === engagementId);
  const ready = selectedProvider?.configured ?? false;
  const selectedPrivacy = selectedProvider?.privacy ?? status?.privacy;

  return (
    <PageShell
      title="AI Brain"
      subtitle="Evidence-grounded security advisor"
      statusItems={[
        {
          label: "RUNTIME",
          value: status ? providerLabel(selectedProvider?.id ?? status.provider).toUpperCase() : "CHECKING",
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
                <select id="brain-engagement" value={engagementId} onChange={(event) => setEngagementId(event.target.value)}>
                  <option value="">No engagement selected</option>
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
                    {message.model && <span>{providerLabel(message.provider)} · {message.model}</span>}
                  </header>
                  {message.factCard && <FactCard vm={message.factCard} />}
                  {message.role === "assistant"
                    ? <AssistantText content={message.content} />
                    : <p>{message.content}</p>}
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
              <div><strong>Manager AI runtime</strong><small>{ready ? (selectedProvider?.id === "ollama" ? "Free · open model · local" : "Manager-configured cloud") : "Needs configuration"}</small></div>
              <span className="brain-runtime-dot" />
            </header>
            <div className="brain-runtime-selectors">
              <label htmlFor="brain-provider">
                <span>Provider</span>
                <select
                  id="brain-provider"
                  value={provider ?? status?.provider ?? ""}
                  onChange={(event) => {
                    const next = event.target.value as AiStatus["provider"];
                    const option = status?.providers.find((item) => item.id === next);
                    setProvider(next);
                    setModel(option?.default_model ?? "");
                  }}
                  disabled={!status}
                >
                  {(status?.providers ?? []).map((item) => (
                    <option value={item.id} key={item.id} disabled={!item.configured}>
                      {item.label}{item.configured ? "" : " · not configured"}
                    </option>
                  ))}
                </select>
              </label>
              <label htmlFor="brain-model">
                <span>Model</span>
                <select
                  id="brain-model"
                  value={selectedModel}
                  onChange={(event) => setModel(event.target.value)}
                  disabled={!selectedProvider?.configured}
                >
                  {(selectedProvider?.models ?? []).map((item) => <option value={item} key={item}>{item}</option>)}
                </select>
              </label>
            </div>
            <dl>
              <div><dt>Execution</dt><dd>Manager only</dd></div>
              <div><dt>Data path</dt><dd>{selectedPrivacy === "local" ? "Local · no API fee" : "Cloud provider"}</dd></div>
              <div><dt>Grounding</dt><dd>{selectedEngagement ? selectedEngagement.name : "General only"}</dd></div>
            </dl>
            {!ready && <p>{selectedProvider?.reason || status?.reason || "AI runtime status is unavailable."}</p>}
          </section>

          <section className="brain-guardrails">
            <header><ShieldCheck size={15} /><span>Reasoning guardrails</span></header>
            {[
              "Uses recorded facts when engagement context is selected",
              "Separates confirmed evidence from hypotheses",
              "Keeps recommendations defensive and non-destructive",
              "Never receives provider credentials from the browser",
              "Public CVE data is not treated as proof of client exposure",
            ].map((item) => <div key={item}><CheckCircle2 size={13} /><span>{item}</span></div>)}
          </section>

          <section className="brain-context-note">
            <Database size={15} />
            <div><strong>Context boundary</strong><p>Only the first 20 recorded findings are summarized for each request. Verify high-impact decisions in the finding detail view.</p></div>
          </section>
        </aside>
      </div>
    </PageShell>
  );
}
