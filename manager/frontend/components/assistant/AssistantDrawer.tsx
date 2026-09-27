"use client";
import React, { useState, useEffect, useCallback } from "react";
import { Brain, Loader2, Search, Send, ShieldCheck, Sparkles, X, Zap } from "lucide-react";
import { useAssistant } from "./AssistantProvider";
import { FactCard } from "./FactCard";
import { AdvisorFlow } from "./AdvisorFlow";
import { ModelSwitcher, type ModelSelection } from "./ModelSwitcher";
import { detectFindingId, type FactCardVM, type AdvisorVM } from "../../lib/assistant";
import { fetchJson, errorMessage } from "../../lib/fetcher";
import { AssistantText } from "./AssistantText";

type Msg = { role: "user" | "assistant"; content: string };
type Served = { provider: string; model: string; fallback: boolean };
type ExplainResponse = {
  factCard: FactCardVM;
  advisor?: AdvisorVM | null;
  narration: string | null;
  served?: Served | null;
};

export function AssistantDrawer() {
  const { open, findingId, findingIds, close } = useAssistant();
  const [input, setInput] = useState("");
  const [activeId, setActiveId] = useState<string | null>(findingId);
  const [card, setCard] = useState<FactCardVM | null>(null);
  const [advisor, setAdvisor] = useState<AdvisorVM | null>(null);
  const [narration, setNarration] = useState<string | null>(null);
  const [thread, setThread] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(Boolean(findingId));
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<ModelSelection | null>(null);
  const [served, setServed] = useState<Served | null>(null);

  const explainId = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    setActiveId(id);
    setThread([]);
    setCard(null);
    setAdvisor(null);
    setNarration(null);
    setServed(null);
    try {
      const d = await fetchJson<ExplainResponse>(
        "/api/assistant/explain",
        {
          method: "POST",
          body: JSON.stringify({
            findingId: id,
            provider: selectedModel?.provider,
            model: selectedModel?.model,
          }),
        },
      );
      setCard(d.factCard);
      setAdvisor(d.advisor ?? null);
      setNarration(d.narration);
      setServed(d.served ?? null);
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      setLoading(false);
    }
  }, [selectedModel]);

  useEffect(() => {
    if (!open || !findingId) return;
    let cancelled = false;

    fetchJson<ExplainResponse>(
      "/api/assistant/explain",
      {
        method: "POST",
        body: JSON.stringify({
          findingId,
          provider: selectedModel?.provider,
          model: selectedModel?.model,
        }),
      },
    )
      .then((data) => {
        if (cancelled) return;
        setCard(data.factCard);
        setAdvisor(data.advisor ?? null);
        setNarration(data.narration);
        setServed(data.served ?? null);
      })
      .catch((cause) => {
        if (!cancelled) setError(errorMessage(cause));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // Re-fetch only when the drawer opens for a finding; the model is read as a
    // live snapshot (changing it re-queries via the input, not this effect).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, findingId]);

  const sendFollowup = useCallback(
    async (text: string) => {
      if (!activeId) return;
      const next = [...thread, { role: "user" as const, content: text }];
      setThread(next);
      setInput("");
      setLoading(true);
      try {
        const d = await fetchJson<{
          content?: string;
          error?: string;
          provider?: string;
          model?: string;
          fallback?: boolean;
        }>("/api/assistant/chat", {
          method: "POST",
          body: JSON.stringify({
            findingId: activeId,
            messages: next,
            provider: selectedModel?.provider,
            model: selectedModel?.model,
          }),
        });
        setThread([...next, { role: "assistant", content: d.content ?? `[${d.error ?? "no reply"}]` }]);
        if (d.provider && d.model) {
          setServed({ provider: d.provider, model: d.model, fallback: Boolean(d.fallback) });
        }
      } catch (e) {
        setThread([...next, { role: "assistant", content: `[${errorMessage(e)}]` }]);
      } finally {
        setLoading(false);
      }
    },
    [activeId, selectedModel, thread],
  );

  const sendGeneral = useCallback(async (text: string) => {
    const next = [...thread, { role: "user" as const, content: text }];
    setThread(next);
    setInput("");
    setLoading(true);
    setError(null);
    try {
      const response = await fetchJson<{
        content?: string;
        provider?: string;
        model?: string;
        fallback?: boolean;
      }>("/api/brain", {
        method: "POST",
        body: JSON.stringify({
          messages: next,
          ...(findingIds.length > 0 ? { findingIds } : {}),
          provider: selectedModel?.provider,
          model: selectedModel?.model,
        }),
      });
      setThread([...next, { role: "assistant", content: response.content ?? "The model returned no response." }]);
      if (response.provider && response.model) {
        setServed({
          provider: response.provider,
          model: response.model,
          fallback: Boolean(response.fallback),
        });
      }
    } catch (cause) {
      setError(errorMessage(cause));
    } finally {
      setLoading(false);
    }
  }, [findingIds, selectedModel, thread]);

  const submit = () => {
    const text = input.trim();
    if (!text) return;
    const id = detectFindingId(text);
    if (id) {
      explainId(id);
      setInput("");
      return;
    }
    if (activeId) void sendFollowup(text);
    else void sendGeneral(text);
  };

  if (!open) return null;
  return (
    <>
      <div onClick={close} className="assistant-drawer-backdrop" />
      <aside role="dialog" aria-modal="true" aria-label="Ask Vedha assistant" className="assistant-drawer">
        <header className="assistant-drawer-header">
          <span className="assistant-drawer-logo"><Brain size={17} /></span>
          <div>
            <strong>Vedha Security Advisor</strong>
            <ModelSwitcher value={selectedModel} onChange={setSelectedModel} />
          </div>
          <button aria-label="Close assistant" onClick={close} className="btn btn-ghost" style={{ height: 30, width: 30, padding: 0 }}>
            <X size={16} />
          </button>
        </header>

        <div className="assistant-drawer-body">
          {findingIds.length > 1 && (
            <div className="assistant-model-note" role="status">
              Grounded on {findingIds.length} selected findings. Vedha resolves their current tenant-scoped records on the server before asking the model.
            </div>
          )}
          {!card && !loading && !error && (
            <div className="assistant-drawer-welcome">
              <span><Sparkles size={18} /></span>
              <h3>{findingIds.length > 1 ? "Prioritize the selected findings." : "Understand risk. Decide what to fix."}</h3>
              <p>{findingIds.length > 1
                ? "Ask for a risk-ranked summary, shared remediation themes, or a safe rollout order. Only the selected records are added as organizational evidence."
                : "Paste any published CVE or a Vedha finding ID. The answer separates public vulnerability facts from verified organizational exposure."}</p>
              <div>
                {(findingIds.length > 1 ? [
                  "Prioritize these findings and explain why",
                  "Group these by remediation approach",
                  "Propose a safe validation order",
                ] : [
                  "Explain CVE-2021-44228",
                  "What should I remediate first?",
                  "How do I validate a critical finding?",
                ]).map((prompt) => <button type="button" key={prompt} onClick={() => setInput(prompt)}>{prompt}</button>)}
              </div>
            </div>
          )}
          {error && <div className="brain-error"><ShieldCheck size={15} /><div><strong>Request could not be completed</strong><span>{error}</span></div></div>}
          {card && <FactCard vm={card} compact />}
          {served?.fallback && (
            <div className="assistant-fallback-chip" role="status">
              <Zap size={12} />
              <span>Answered by <code>{served.model}</code> — the selected provider was unavailable, so an approved fallback served this response.</span>
            </div>
          )}
          {card && advisor && <AdvisorFlow vm={advisor} />}
          {card && !advisor && narration && <div className="assistant-narration"><AssistantText content={narration} /></div>}
          {card && !advisor && !narration && <div className="assistant-model-note">The grounded brief above remains available even when the advisor model is offline.</div>}
          {thread.map((m, i) => (
            <div key={i} className="assistant-thread-message" data-role={m.role}>
              {m.role === "assistant" ? <AssistantText content={m.content} /> : m.content}
            </div>
          ))}
          {loading && <div className="assistant-thinking"><span /><span /><span /> Analyzing evidence and remediation…</div>}
        </div>

        <footer className="assistant-drawer-composer">
          <div>
            <Search size={15} />
            <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submit(); }
            }}
            placeholder={loading
              ? "Analyzing…"
              : activeId
                ? "Ask about impact, score, evidence, or remediation…"
                : findingIds.length > 1
                  ? `Ask about the ${findingIds.length} selected findings…`
                  : "Paste CVE-YYYY-NNNN or ask a security question…"}
            aria-label="Assistant input"
            disabled={loading}
            rows={2}
            />
          </div>
          <button
            className="btn btn-primary assistant-send-btn"
            onClick={submit}
            disabled={loading || !input.trim()}
            aria-label={loading ? "Sending…" : "Send"}
            title={!input.trim() ? "Type a message to send" : undefined}
          >
            {loading ? <Loader2 size={15} className="animate-spin" /> : <Send size={17} />}
          </button>
          <small><ShieldCheck size={11} /> Public CVE data does not prove client exposure · Shift+Enter for a new line</small>
        </footer>
      </aside>
    </>
  );
}
