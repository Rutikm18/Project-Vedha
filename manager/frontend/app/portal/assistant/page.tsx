"use client";

/**
 * Portal → Assistant. A chat about the customer's OWN assessment.
 *
 * Two boundaries, both enforced server-side (app/routers/portal.py):
 *   DATA    — grounding context is assembled from this client's engagement via
 *             client_scoped(); the request body carries no context, so nothing
 *             here can widen what the model sees.
 *   SUBJECT — the `client_assistant` task restricts the model to information
 *             security and declines anything else.
 *
 * Replies are NOT operator-reviewed — a deliberate product decision, unlike the
 * reports and remediation routes which are review-gated. Because of that, every
 * answer is labelled AI-generated and unverified. That label is the honest
 * mitigation and should not be removed.
 */

import React, { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  AlertTriangle, Bot, Loader2, Send, Sparkles, User as UserIcon,
} from "lucide-react";
import { PortalShell } from "../../../components/portal/PortalShell";
import { Timestamp } from "../../../components/portal/Timestamp";
import { portalApi, type PortalFinding } from "../../../lib/portal-client";

interface Turn {
  id: string;
  role: "user" | "assistant";
  content: string;
  at: string;
  model?: string;
  grounded?: boolean;
}

interface AssistantReply {
  content: string;
  provider: string;
  model: string;
  grounded: boolean;
  generated_at: string;
}

const STARTERS = [
  "Which of my findings should I fix first, and why?",
  "Explain my highest-risk finding in plain language.",
  "What does SMB signing do, and why does it matter here?",
  "How do I verify a fix actually worked?",
];

const MAX_CHARS = 4000;

export default function PortalAssistant() {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);
  // Monotonic turn ids. React 19's purity rule rejects Date.now() here, and a
  // counter is the better key anyway — two turns in the same millisecond
  // would otherwise collide.
  const nextId = useRef(0);

  const findings = useQuery({
    queryKey: ["portal", "findings"],
    queryFn: () => portalApi<PortalFinding[]>("/findings"),
  });
  const open = (findings.data ?? []).filter(
    (f) => f.status === "open" || f.status === "confirmed");

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [turns, busy]);

  async function ask(text: string) {
    const question = text.trim();
    if (!question || busy) return;
    setError(null);

    const mine: Turn = {
      id: `u-${nextId.current++}`, role: "user", content: question,
      at: new Date().toISOString(),
    };
    const history = [...turns, mine];
    setTurns(history);
    setDraft("");
    setBusy(true);

    try {
      const reply = await portalApi<AssistantReply>("/assistant/chat", {
        method: "POST",
        body: {
          messages: history.map((t) => ({ role: t.role, content: t.content })),
        },
      });
      setTurns((prev) => [...prev, {
        id: `a-${nextId.current++}`, role: "assistant", content: reply.content,
        at: reply.generated_at, model: reply.model, grounded: reply.grounded,
      }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "The assistant is unavailable right now.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <PortalShell
      title="Assistant"
      subtitle="Ask about your findings, scans and how to fix them."
    >
      {/* what this is, and what it is not */}
      <div className="panel" style={{ display: "flex", gap: 12, alignItems: "flex-start", padding: 14 }}>
        <AlertTriangle size={15} style={{ color: "var(--sev-medium-color)", flexShrink: 0, marginTop: 2 }} />
        <div>
          <strong style={{ display: "block", marginBottom: 2 }}>AI-generated and unverified</strong>
          <span className="muted" style={{ fontSize: 12.5, lineHeight: 1.55 }}>
            Answers are produced by a language model from your recorded assessment data.
            They are <strong>not</strong> reviewed by your security team before you see
            them, and can be wrong or incomplete. Your findings, scans and reports remain
            the authoritative record. This assistant answers security questions only.
          </span>
        </div>
      </div>

      <div className="panel" style={{ marginTop: 16, display: "flex", flexDirection: "column",
                                      minHeight: 420 }}>
        <div className="panel-head" style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Sparkles size={15} style={{ color: "var(--accent)" }} />
          <h2 className="panel-title">Conversation</h2>
          <span className="muted" style={{ marginLeft: "auto", fontSize: 11 }}>
            {open.length} open finding{open.length === 1 ? "" : "s"} in context
          </span>
        </div>

        <div style={{ flex: 1, padding: 16, display: "flex", flexDirection: "column", gap: 14 }}>
          {turns.length === 0 && (
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              <p className="muted" style={{ fontSize: 13, margin: 0 }}>
                Try one of these, or ask your own security question:
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {STARTERS.map((s) => (
                  <button key={s} className="btn btn-secondary focusable"
                    onClick={() => ask(s)} disabled={busy}
                    style={{ fontSize: 12, height: 30, padding: "0 12px", textAlign: "left" }}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {turns.map((t) => (
            <div key={t.id} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
              <div style={{ flexShrink: 0, marginTop: 2 }}>
                {t.role === "user"
                  ? <UserIcon size={15} style={{ color: "var(--text-muted)" }} />
                  : <Bot size={15} style={{ color: "var(--accent)" }} />}
              </div>
              <div style={{ minWidth: 0, flex: 1 }}>
                <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 3 }}>
                  <strong style={{ fontSize: 12 }}>
                    {t.role === "user" ? "You" : "Assistant"}
                  </strong>
                  <Timestamp value={t.at} />
                  {t.role === "assistant" && t.model && (
                    <span className="muted" style={{ fontSize: 11 }}>· {t.model}</span>
                  )}
                </div>
                <div style={{ fontSize: 13, lineHeight: 1.65, whiteSpace: "pre-wrap",
                              color: "var(--text-secondary)" }}>
                  {t.content}
                </div>
              </div>
            </div>
          ))}

          {busy && (
            <div className="muted" style={{ display: "flex", gap: 8, alignItems: "center", fontSize: 12.5 }}>
              <Loader2 className="animate-spin" size={14} /> Thinking…
            </div>
          )}
          {error && (
            <div style={{ fontSize: 12.5, color: "var(--sev-high-color)" }} role="alert">{error}</div>
          )}
          <div ref={endRef} />
        </div>

        <form
          onSubmit={(e) => { e.preventDefault(); ask(draft); }}
          style={{ display: "flex", gap: 8, padding: 14, borderTop: "1px solid var(--border)" }}
        >
          <textarea
            className="textarea-base"
            value={draft}
            maxLength={MAX_CHARS}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); ask(draft); }
            }}
            placeholder="Ask a security question about your assessment…"
            aria-label="Ask the assistant"
            rows={2}
            style={{ flex: 1, resize: "vertical", fontSize: 13 }}
            disabled={busy}
          />
          <button type="submit" className="btn btn-primary focusable"
            disabled={busy || !draft.trim()}
            aria-label="Send"
            style={{ alignSelf: "flex-end", height: 32, padding: "0 14px" }}>
            <Send size={14} /> Send
          </button>
        </form>
      </div>
    </PortalShell>
  );
}
