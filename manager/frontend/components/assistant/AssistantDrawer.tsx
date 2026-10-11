"use client";
import React, { useState, useEffect, useCallback, useRef } from "react";
import {
  AlertTriangle, Brain, Loader2, Maximize2, Minimize2, RotateCcw, Send, ShieldCheck,
  Sparkles, X, Zap,
} from "lucide-react";
import { useModalFocus } from "../../hooks/useModalFocus";
import { useAssistant } from "./AssistantProvider";
import { FactCard } from "./FactCard";
import { AdvisorFlow } from "./AdvisorFlow";
import { ModelSwitcher, type ModelSelection } from "./ModelSwitcher";
import { advisorToText, detectFindingId, trimThread, CHAT_LIMITS, type FactCardVM, type AdvisorVM } from "../../lib/assistant";
import {
  EMPTY_STORE, forgetConversation, pickConversation, saveConversation, type ConversationStore,
} from "../../lib/assistant-history";
import { useSessionState } from "../../lib/session-state";
import { fetchJson, errorMessage } from "../../lib/fetcher";
import { scrollChildToTop, scrollToEnd } from "../../lib/scroll";
import { AssistantText, CopyAnswerButton } from "./AssistantText";

type Msg = { role: "user" | "assistant"; content: string };
type Served = { provider: string; model: string; fallback: boolean };
type ExplainResponse = {
  factCard: FactCardVM;
  advisor?: AdvisorVM | null;
  narration: string | null;
  served?: Served | null;
};
type Failure =
  | { message: string; kind: "explain"; id: string }
  | { message: string; kind: "ask"; text: string; history: Msg[] };

const WIDE_KEY = "vedha.assistant.wide";
const GENERAL_STARTERS = [
  "Explain CVE-2021-44228",
  "What should I remediate first?",
  "How do I validate a critical finding?",
];
const FINDING_FOLLOWUPS = [
  "Is this exploitable in my environment?",
  "How do I verify the fix worked?",
  "What is the business impact?",
  "Give me the shortest safe fix",
];

function prefersReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
}

export function AssistantDrawer() {
  const { open, findingId, close } = useAssistant();
  const dialogRef = useRef<HTMLElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  // Bumped whenever the conversation is replaced, so an answer that arrives after
  // "New chat" (or after switching finding) is dropped instead of landing in the wrong thread.
  const seq = useRef(0);
  useModalFocus(dialogRef, open, close, ".assistant-orb");

  // Remembered conversations (this tab only). The drawer opens on the one for the finding
  // being explained, or on the most recent one, so closing it loses nothing.
  const [history, setHistory] = useSessionState<ConversationStore>("assistant.drawer.v1", EMPTY_STORE);
  const [restored] = useState(() => pickConversation(history, findingId));
  // The finding this mount has already loaded (or restored), so reopening never refetches it.
  const loadedFor = useRef<string | null>(restored?.card ? findingId : null);

  const [input, setInput] = useState("");
  const [activeId, setActiveId] = useState<string | null>(restored ? restored.activeId : findingId);
  const [card, setCard] = useState<FactCardVM | null>(restored?.card ?? null);
  const [advisor, setAdvisor] = useState<AdvisorVM | null>(restored?.advisor ?? null);
  const [narration, setNarration] = useState<string | null>(restored?.narration ?? null);
  const [thread, setThread] = useState<Msg[]>(restored?.thread ?? []);
  const [loading, setLoading] = useState(Boolean(findingId) && !restored);
  const [failure, setFailure] = useState<Failure | null>(null);
  const [selectedModel, setSelectedModel] = useState<ModelSelection | null>(null);
  const [served, setServed] = useState<Served | null>(restored?.served ?? null);
  // Only mounted after the client-side session check, so reading storage here is safe.
  const [wide, setWide] = useState(() => {
    try { return typeof window !== "undefined" && localStorage.getItem(WIDE_KEY) === "1"; } catch { return false; }
  });
  const toggleWide = () => setWide((current) => {
    const next = !current;
    try { localStorage.setItem(WIDE_KEY, next ? "1" : "0"); } catch { /* storage unavailable */ }
    return next;
  });

  const explainId = useCallback(async (id: string) => {
    const mine = ++seq.current;
    setLoading(true);
    setFailure(null);
    setActiveId(id);
    setThread([]);
    setCard(null);
    setAdvisor(null);
    setNarration(null);
    setServed(null);
    try {
      const d = await fetchJson<ExplainResponse>("/api/assistant/explain", {
        method: "POST",
        body: JSON.stringify({ findingId: id, provider: selectedModel?.provider, model: selectedModel?.model }),
      });
      if (mine !== seq.current) return;
      setCard(d.factCard);
      setAdvisor(d.advisor ?? null);
      setNarration(d.narration);
      setServed(d.served ?? null);
    } catch (e) {
      if (mine !== seq.current) return;
      loadedFor.current = null;                              // let the next open try again
      setFailure({ message: errorMessage(e), kind: "explain", id });
    } finally {
      if (mine === seq.current) setLoading(false);
    }
    // The model is read as a live snapshot: changing it applies to the next question.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Opening the drawer on a finding (the "Explain" button) loads its brief.
  // Deferred one tick: React Strict Mode mounts effects twice in development, and this way
  // the first mount is cancelled instead of sending the same request twice.
  useEffect(() => {
    if (!open || !findingId || loadedFor.current === findingId) return;
    const timer = window.setTimeout(() => {
      loadedFor.current = findingId;
      void explainId(findingId);
    }, 0);
    return () => window.clearTimeout(timer);
  }, [open, findingId, explainId]);

  const ask = useCallback(async (text: string, history: Msg[]) => {
    const mine = ++seq.current;
    const next = [...history, { role: "user" as const, content: text }];
    setThread(next);
    setInput("");
    setLoading(true);
    setFailure(null);
    try {
      const sent = trimThread(next);
      const reply = activeId
        ? await fetchJson<{ content?: string; error?: string }>("/api/assistant/chat", {
            method: "POST",
            body: JSON.stringify({
              findingId: activeId,
              messages: sent,
              // What the user has already read, so "explain more" has something to expand.
              previousExplanation: advisor ? advisorToText(advisor) : narration ?? undefined,
            }),
          })
        : await fetchJson<{ content?: string; error?: string }>("/api/brain", {
            method: "POST",
            body: JSON.stringify({ messages: sent, provider: selectedModel?.provider, model: selectedModel?.model }),
          });
      if (mine !== seq.current) return;
      setThread([...next, { role: "assistant", content: reply.content || "The model returned no response." }]);
    } catch (e) {
      if (mine !== seq.current) return;
      setFailure({ message: errorMessage(e), kind: "ask", text, history });
    } finally {
      if (mine === seq.current) setLoading(false);
    }
  }, [activeId, advisor, narration, selectedModel]);

  const retryFailure = () => {
    if (!failure) return;
    if (failure.kind === "explain") void explainId(failure.id);
    else void ask(failure.text, failure.history);
  };

  const submit = (override?: string) => {
    const text = (override ?? input).trim();
    if (!text || loading) return;
    const id = detectFindingId(text);
    if (id && id !== activeId) {
      setInput("");
      void explainId(id);
      return;
    }
    void ask(text, thread);
  };

  const reset = () => {
    seq.current++;
    loadedFor.current = null;
    setHistory((current) => forgetConversation(current, activeId));
    setActiveId(null);
    setCard(null); setAdvisor(null); setNarration(null); setServed(null);
    setThread([]); setFailure(null); setLoading(false); setInput("");
    inputRef.current?.focus();
  };

  // Remember the conversation once an answer has settled.
  useEffect(() => {
    if (loading || failure || (!card && thread.length === 0)) return;
    // A question still waiting for its answer is not worth restoring.
    if (thread.length > 0 && thread[thread.length - 1].role === "user") return;
    setHistory((current) => saveConversation(current, { activeId, card, advisor, narration, served, thread }));
  }, [loading, failure, activeId, card, advisor, narration, served, thread, setHistory]);

  // Scrolling: show the thinking indicator while waiting, and start a new answer at
  // its first line (landing on the end of a long answer is what made them unreadable).
  useEffect(() => {
    const body = bodyRef.current;
    if (!body) return;
    const behavior: ScrollBehavior = prefersReducedMotion() ? "auto" : "smooth";
    if (loading || failure) {
      scrollToEnd(body, behavior);
      return;
    }
    const last = thread.length - 1;
    if (last >= 0 && thread[last].role === "assistant") {
      const reply = body.querySelector<HTMLElement>(`[data-msg="${last}"]`);
      if (reply) scrollChildToTop(body, reply, behavior);
    }
  }, [thread, loading, failure]);

  // Grow the box with the text (up to ~6 lines), never beyond the drawer.
  useEffect(() => {
    const el = inputRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 150)}px`;
  }, [input, open]);

  if (!open) return null;

  const lastIsAssistant = thread.length > 0 && thread[thread.length - 1].role === "assistant";
  const showFollowups = Boolean(activeId && card && !loading && !failure && (thread.length === 0 || lastIsAssistant));
  const started = Boolean(card || thread.length || failure);
  const context = activeId
    ? `Finding · ${card?.cveIds[0] ?? card?.title ?? activeId}`
    : "General security questions";
  const remaining = CHAT_LIMITS.perMessage - input.length;

  return (
    <>
      <div data-modal-backdrop onClick={close} className="assistant-drawer-backdrop" />
      <aside ref={dialogRef} tabIndex={-1} role="dialog" aria-modal="true" aria-label="Ask Vedha assistant"
        className="assistant-drawer" data-wide={wide}>
        <header className="assistant-drawer-header">
          <span className="assistant-drawer-logo"><Brain size={18} /></span>
          <div className="assistant-drawer-title">
            <strong>Vedha Security Advisor</strong>
            <span title={context}>{context}</span>
          </div>
          <div className="assistant-drawer-tools">
            <ModelSwitcher value={selectedModel} onChange={setSelectedModel} />
            {started && (
              <button type="button" className="assistant-icon-btn" onClick={reset} aria-label="Start a new chat" title="New chat — clears this conversation">
                <RotateCcw size={15} />
              </button>
            )}
            <button type="button" className="assistant-icon-btn assistant-expand" onClick={toggleWide}
              aria-label={wide ? "Make the panel narrower" : "Make the panel wider"} aria-pressed={wide}
              title={wide ? "Narrower" : "Wider"}>
              {wide ? <Minimize2 size={15} /> : <Maximize2 size={15} />}
            </button>
            <button type="button" className="assistant-icon-btn" aria-label="Close assistant" onClick={close}>
              <X size={16} />
            </button>
          </div>
        </header>

        <div className="assistant-drawer-body" ref={bodyRef} aria-busy={loading}>
          {!started && !loading && (
            <div className="assistant-drawer-welcome">
              <span><Sparkles size={20} /></span>
              <h3>Understand risk. Decide what to fix.</h3>
              <p>Paste any published CVE or a Vedha finding ID. The answer separates public vulnerability facts from verified organizational exposure.</p>
              <div>
                {GENERAL_STARTERS.map((prompt) => (
                  <button type="button" key={prompt} onClick={() => submit(prompt)}>{prompt}</button>
                ))}
              </div>
            </div>
          )}

          {card && <FactCard vm={card} compact />}
          {served?.fallback && (
            <div className="assistant-fallback-chip" role="status">
              <Zap size={13} />
              <span>Answered by <code>{served.model}</code> — free fallback, the selected provider was out of credit.</span>
            </div>
          )}
          {card && advisor && <AdvisorFlow vm={advisor} />}
          {card && !advisor && narration && (
            <div className="assistant-msg" data-role="assistant">
              <div className="assistant-bubble"><AssistantText content={narration} /></div>
            </div>
          )}
          {card && !advisor && !narration && <div className="assistant-model-note">The grounded brief above remains available even when the advisor model is offline.</div>}

          {thread.map((m, i) => (
            <div key={i} className="assistant-msg" data-role={m.role} data-msg={i}>
              {m.role === "assistant" ? (
                <>
                  <div className="assistant-msg-head">
                    <span><Brain size={13} /> Vedha Advisor</span>
                    <CopyAnswerButton content={m.content} />
                  </div>
                  <div className="assistant-bubble"><AssistantText content={m.content} /></div>
                </>
              ) : (
                <div className="assistant-bubble">{m.content}</div>
              )}
            </div>
          ))}

          {loading && (
            <div className="assistant-thinking" role="status">
              <span /><span /><span />
              {activeId && !card && thread.length === 0 ? "Loading the finding and checking the evidence…" : "Analyzing evidence and remediation…"}
            </div>
          )}

          {failure && (
            <div className="assistant-failure" role="alert">
              <AlertTriangle size={16} />
              <div>
                <strong>That didn&apos;t go through</strong>
                <span>{failure.message}</span>
              </div>
              <button type="button" onClick={retryFailure}><RotateCcw size={13} /> Try again</button>
            </div>
          )}

          {showFollowups && (
            <div className="assistant-chips" aria-label="Suggested follow-up questions">
              {FINDING_FOLLOWUPS.map((q) => (
                <button type="button" key={q} onClick={() => submit(q)}>{q}</button>
              ))}
            </div>
          )}
        </div>

        <footer className="assistant-drawer-composer">
          <div className="assistant-composer-box">
            <textarea
              ref={inputRef}
              value={input}
              maxLength={CHAT_LIMITS.perMessage}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); submit(); }
              }}
              placeholder={activeId ? "Ask about impact, score, evidence, or remediation…" : "Paste CVE-YYYY-NNNN or ask a security question…"}
              aria-label="Assistant input"
              rows={1}
            />
            <button
              type="button"
              className="btn btn-primary assistant-send-btn"
              onClick={() => submit()}
              disabled={loading || !input.trim()}
              aria-label={loading ? "Waiting for the answer" : "Send"}
              title={loading ? "Waiting for the answer…" : !input.trim() ? "Type a message to send" : "Send (Enter)"}
            >
              {loading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
            </button>
          </div>
          <small>
            <span><ShieldCheck size={12} /> Public CVE data does not prove client exposure</span>
            <span>{remaining < 500 ? `${remaining} characters left` : "Enter to send · Shift+Enter for a new line"}</span>
          </small>
        </footer>
      </aside>
    </>
  );
}
