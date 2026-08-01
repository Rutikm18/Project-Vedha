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
      className="btn btn-primary"
      style={{
        position: "fixed",
        right: 20,
        bottom: 20,
        zIndex: 50,
        height: 48,
        width: 48,
        borderRadius: 999,
        padding: 0,
        boxShadow: "var(--shadow-accent)",
      }}
    >
      <Sparkles size={20} />
    </button>
  );
}
