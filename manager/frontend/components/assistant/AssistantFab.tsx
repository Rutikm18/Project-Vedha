"use client";
import React from "react";
import { Sparkles } from "lucide-react";
import { useAssistant } from "./AssistantProvider";

export function AssistantFab() {
  const { open, openBlank } = useAssistant();
  if (open) return null;
  return (
    <button
      aria-label="Open Ask Vedha assistant (Cmd/Ctrl-K)"
      title="Ask Vedha · ⌘K"
      onClick={openBlank}
      className="assistant-orb"
    >
      <Sparkles size={21} aria-hidden />
      <span className="assistant-orb__hint" aria-hidden>
        Ask Vedha<kbd>⌘K</kbd>
      </span>
    </button>
  );
}
