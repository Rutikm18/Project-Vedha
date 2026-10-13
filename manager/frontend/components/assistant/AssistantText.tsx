"use client";

import React, { useMemo, useState } from "react";
import { Check, Copy } from "lucide-react";
import { copyText } from "../../lib/clipboard";
import { parseInline, parseMarkdown, type Block, type Inline, type ListItem } from "../../lib/assistant-markdown";

function renderInlines(nodes: Inline[], key: string): React.ReactNode[] {
  return nodes.map((node, i) => {
    const k = `${key}.${i}`;
    switch (node.t) {
      case "text": return <React.Fragment key={k}>{node.text}</React.Fragment>;
      case "br": return <br key={k} />;
      case "code": return <code key={k} className="md-code">{node.text}</code>;
      case "strong": return <strong key={k}>{renderInlines(node.children, k)}</strong>;
      case "em": return <em key={k}>{renderInlines(node.children, k)}</em>;
      case "del": return <del key={k}>{renderInlines(node.children, k)}</del>;
      case "link": return (
        <a key={k} href={node.href} target="_blank" rel="noopener noreferrer">
          {renderInlines(node.children, k)}
        </a>
      );
    }
  });
}

/** Inline Markdown (bold, italic, code, links) for short strings such as list items. */
export function InlineText({ text }: { text: string }) {
  const nodes = useMemo(() => parseInline(text), [text]);
  return <>{renderInlines(nodes, "i")}</>;
}

function CopyButton({ value, label, className = "md-copy" }: { value: string; label: string; className?: string }) {
  const [state, setState] = useState<"idle" | "copied" | "failed">("idle");
  return (
    <button
      type="button"
      className={className}
      data-state={state}
      aria-label={state === "copied" ? "Copied" : state === "failed" ? "Copy failed" : label}
      title={state === "failed" ? "Copy failed — select the text and copy it manually" : label}
      onClick={() => {
        void copyText(value).then((ok) => {
          setState(ok ? "copied" : "failed");
          window.setTimeout(() => setState("idle"), 1600);
        });
      }}
    >
      {state === "copied" ? <Check size={13} aria-hidden /> : <Copy size={13} aria-hidden />}
      <span>{state === "copied" ? "Copied" : state === "failed" ? "Failed" : "Copy"}</span>
    </button>
  );
}

/** Copy a whole answer (the Markdown the model wrote). */
export function CopyAnswerButton({ content }: { content: string }) {
  return <CopyButton value={content} label="Copy answer" className="md-copy md-copy-answer" />;
}

function Items({ items, keyPrefix }: { items: ListItem[]; keyPrefix: string }) {
  return (
    <>
      {items.map((item, i) => (
        <li key={i}>
          {renderInlines(item.inlines, `${keyPrefix}.${i}`)}
          {item.children.map((child, c) => <BlockView key={c} block={child} keyPrefix={`${keyPrefix}.${i}.${c}`} />)}
        </li>
      ))}
    </>
  );
}

function BlockView({ block, keyPrefix }: { block: Block; keyPrefix: string }) {
  switch (block.t) {
    case "heading": {
      const Tag = (`h${Math.min(block.level + 2, 6)}`) as "h3" | "h4" | "h5" | "h6";
      return <Tag className={`md-h md-h${block.level}`}>{renderInlines(block.inlines, keyPrefix)}</Tag>;
    }
    case "p": return <p>{renderInlines(block.inlines, keyPrefix)}</p>;
    case "hr": return <hr />;
    case "ul": return <ul><Items items={block.items} keyPrefix={keyPrefix} /></ul>;
    case "ol": return <ol start={block.start}><Items items={block.items} keyPrefix={keyPrefix} /></ol>;
    case "quote": return (
      <blockquote>
        {block.blocks.map((b, i) => <BlockView key={i} block={b} keyPrefix={`${keyPrefix}.${i}`} />)}
      </blockquote>
    );
    case "code": return (
      <figure className="md-pre">
        <figcaption>
          <span>{block.lang || "code"}</span>
          <CopyButton value={block.text} label="Copy code" />
        </figcaption>
        <pre tabIndex={0}><code>{block.text}</code></pre>
        {!block.closed && <small className="md-truncated">The reply ended here — it may have been cut off by the length limit.</small>}
      </figure>
    );
    case "table": return (
      <div className="md-table-wrap" role="region" aria-label="Table" tabIndex={0}>
        <table>
          <thead>
            <tr>{block.head.map((cell, c) => (
              <th key={c} style={block.align[c] ? { textAlign: block.align[c]! } : undefined}>
                {renderInlines(cell, `${keyPrefix}.h${c}`)}
              </th>
            ))}</tr>
          </thead>
          <tbody>
            {block.rows.map((row, r) => (
              <tr key={r}>{row.map((cell, c) => (
                <td key={c} style={block.align[c] ? { textAlign: block.align[c]! } : undefined}>
                  {renderInlines(cell, `${keyPrefix}.${r}.${c}`)}
                </td>
              ))}</tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

/** Renders an assistant reply (Markdown) as structured, readable UI. */
export function AssistantText({ content }: { content: string }) {
  const blocks = useMemo(() => parseMarkdown(content), [content]);
  return (
    <div className="assistant-structured-text">
      {blocks.map((block, i) => <BlockView key={i} block={block} keyPrefix={`b${i}`} />)}
    </div>
  );
}
