"use client";

import React from "react";

function stripMarks(value: string) {
  return value.replace(/\*\*/g, "").replace(/`/g, "").trim();
}

/** Render inline **bold** and `code` spans; strip any stray markers from plain runs.
 * The advisor emphasises the single most important phrase per answer (a host, a
 * severity, the key action) with **double asterisks** — rendering it as <strong>
 * (instead of stripping it to plain text) is what makes a structured brief scannable. */
function renderInline(text: string, keyPrefix: string): React.ReactNode[] {
  return text
    .split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
    .filter((part) => part.length > 0)
    .map((part, i) => {
      const key = `${keyPrefix}-${i}`;
      if (/^\*\*[^*]+\*\*$/.test(part)) return <strong key={key}>{part.slice(2, -2)}</strong>;
      if (/^`[^`]+`$/.test(part)) return <code key={key}>{part.slice(1, -1)}</code>;
      return <React.Fragment key={key}>{part.replace(/\*\*/g, "").replace(/`/g, "")}</React.Fragment>;
    });
}

/** Small, dependency-free renderer for the constrained headings/lists/emphasis emitted by the advisor. */
export function AssistantText({ content }: { content: string }) {
  const lines = content.split(/\r?\n/);
  return (
    <div className="assistant-structured-text">
      {lines.map((raw, index) => {
        const line = raw.trim();
        if (!line) return <span className="assistant-text-space" key={index} />;
        if (/^#{1,3}\s+/.test(line)) return <h4 key={index}>{stripMarks(line.replace(/^#{1,3}\s+/, ""))}</h4>;
        const numbered = line.match(/^(\d+)[.)]\s+(.+)$/);
        if (numbered) return <div className="assistant-text-step" key={index}><span>{numbered[1]}</span><p>{renderInline(numbered[2], `s${index}`)}</p></div>;
        if (/^[-*]\s+/.test(line)) return <div className="assistant-text-bullet" key={index}><span>•</span><p>{renderInline(line.replace(/^[-*]\s+/, ""), `b${index}`)}</p></div>;
        return <p key={index}>{renderInline(line, `p${index}`)}</p>;
      })}
    </div>
  );
}
