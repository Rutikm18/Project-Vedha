"use client";

import React from "react";

function plain(value: string) {
  return value.replace(/\*\*/g, "").replace(/`/g, "").trim();
}

/** Small, dependency-free renderer for the constrained headings/lists emitted by the advisor. */
export function AssistantText({ content }: { content: string }) {
  const lines = content.split(/\r?\n/);
  return (
    <div className="assistant-structured-text">
      {lines.map((raw, index) => {
        const line = raw.trim();
        if (!line) return <span className="assistant-text-space" key={index} />;
        if (/^#{1,3}\s+/.test(line)) return <h4 key={index}>{plain(line.replace(/^#{1,3}\s+/, ""))}</h4>;
        const numbered = line.match(/^(\d+)[.)]\s+(.+)$/);
        if (numbered) return <div className="assistant-text-step" key={index}><span>{numbered[1]}</span><p>{plain(numbered[2])}</p></div>;
        if (/^[-*]\s+/.test(line)) return <div className="assistant-text-bullet" key={index}><span>•</span><p>{plain(line.replace(/^[-*]\s+/, ""))}</p></div>;
        return <p key={index}>{plain(line)}</p>;
      })}
    </div>
  );
}
