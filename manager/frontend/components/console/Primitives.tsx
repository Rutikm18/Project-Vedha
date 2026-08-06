// manager/frontend/components/console/Primitives.tsx
"use client";

/**
 * Console primitives. Every dashboard card is built from these, so spacing,
 * hairlines, type scale and focus behaviour stay identical across the product
 * instead of being re-typed as inline styles in each component.
 */
import React from "react";
import { ArrowDown, ArrowUp, Minus } from "lucide-react";
import { SEVERITY, Severity, sevVars } from "../../lib/severity";

/* ------------------------------------------------------------------ Panel */

export function Panel({
  title, eyebrow, icon, rail, actions, note, footer, bodyPad = false, children,
}: {
  title: string;
  /** Small uppercase kicker above the title — say what the data *is*, not what it's called. */
  eyebrow?: string;
  icon?: React.ReactNode;
  /** State rail colour down the left edge. Set it only when state is real. */
  rail?: string;
  actions?: React.ReactNode;
  /** Right-aligned context in the header, e.g. "updated 2m ago". */
  note?: string;
  footer?: React.ReactNode;
  bodyPad?: boolean;
  children: React.ReactNode;
}) {
  return (
    <section
      className="panel"
      style={rail ? ({ "--rail": rail } as React.CSSProperties) : undefined}
      aria-label={title}
    >
      <header className="panel-head">
        {icon && (
          <span
            aria-hidden
            style={{
              width: 24, height: 24, borderRadius: 6, flexShrink: 0,
              display: "grid", placeItems: "center",
              background: "var(--bg-panel)", border: "0.5px solid var(--border-subtle)",
              color: rail ?? "var(--text-secondary)",
            }}
          >
            {icon}
          </span>
        )}
        <div style={{ minWidth: 0, display: "flex", flexDirection: "column", gap: 1 }}>
          {eyebrow && <span className="eyebrow">{eyebrow}</span>}
          <h2 className="panel-title">{title}</h2>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 10 }}>
          {note && <span className="panel-note num">{note}</span>}
          {actions}
        </div>
      </header>
      <div className="panel-body" style={bodyPad ? { padding: 16 } : undefined}>
        {children}
      </div>
      {footer && (
        <footer style={{ padding: "10px 18px", borderTop: "0.5px solid var(--border-subtle)", background: "var(--bg-surface)" }}>
          {footer}
        </footer>
      )}
    </section>
  );
}

/* ----------------------------------------------------------- SeverityChip */

export function SeverityChip({ severity, compact = false }: { severity: Severity; compact?: boolean }) {
  const m = SEVERITY[severity];
  return (
    <span className="chip sev-chip" style={sevVars(severity)}>
      <span className="sev-sigil" aria-hidden>{m.sigil}</span>
      {compact ? m.label.slice(0, 4) : m.label}
    </span>
  );
}

/* ------------------------------------------------------------------ Meter */

export function Meter({
  value, color, height = 5, ticks = false, label, pulse = false,
}: {
  /** 0–100. */
  value: number;
  color: string;
  height?: number;
  /** Quarter ticks — switch on when the reader needs to judge *how far*, not just direction. */
  ticks?: boolean;
  /** Accessible description; omit only when an adjacent label already says it. */
  label?: string;
  pulse?: boolean;
}) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div
      className="meter"
      style={{ height }}
      role={label ? "progressbar" : undefined}
      aria-label={label}
      aria-valuenow={label ? Math.round(pct) : undefined}
      aria-valuemin={label ? 0 : undefined}
      aria-valuemax={label ? 100 : undefined}
    >
      <div className={`meter-fill${pulse ? " sla-pulse" : ""}`} style={{ width: `${pct}%`, background: color }} />
      {ticks && <div className="meter-ticks" aria-hidden />}
    </div>
  );
}

/* ------------------------------------------------------------------ Delta */

/** Period-over-period change. `improvedWhenLower` flips which direction is good. */
export function Delta({
  now, prev, improvedWhenLower, unit = "",
}: { now?: number; prev?: number; improvedWhenLower: boolean; unit?: string }) {
  if (prev == null || now == null) return null;
  const diff = Math.round((now - prev) * 10) / 10;

  if (diff === 0) {
    return (
      <span className="chip num" style={{ color: "var(--text-muted)", background: "rgba(128,128,128,0.12)" }}>
        <Minus size={11} aria-hidden /> no change
      </span>
    );
  }

  const better = improvedWhenLower ? diff < 0 : diff > 0;
  const Icon = diff < 0 ? ArrowDown : ArrowUp;
  return (
    <span
      className="chip num"
      style={{
        color: better ? "var(--nominal-color)" : "var(--sev-high-color)",
        background: better ? "var(--nominal-bg)" : "var(--sev-high-bg)",
        borderColor: better ? "var(--nominal-edge)" : "var(--sev-high-edge)",
      }}
    >
      <Icon size={11} aria-hidden />
      {Math.abs(diff)}{unit}
      <span className="sr-only">
        {diff < 0 ? "down" : "up"} from {prev}{unit} last scan — {better ? "improving" : "worsening"}
      </span>
    </span>
  );
}

/* ------------------------------------------------------------- Readout row
   A label/value pair on a hairline grid. Replaces the four floating stat
   cards that every dashboard ships with. */

export function Readout({
  label, value, sub, color = "var(--text-primary)", size = 34, lead,
}: {
  label: string;
  value: React.ReactNode;
  sub?: React.ReactNode;
  color?: string;
  size?: number;
  /** Optional leading element, e.g. a pulse dot when the value is non-zero. */
  lead?: React.ReactNode;
}) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 7, minWidth: 0, padding: "16px 20px" }}>
      <span className="eyebrow">{label}</span>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        {lead}
        <span
          className="num"
          style={{
            fontFamily: "var(--font-display)", fontSize: size, fontWeight: 600,
            lineHeight: 0.95, letterSpacing: "-0.02em", color,
          }}
        >
          {value}
        </span>
      </div>
      {sub && <span style={{ fontFamily: "var(--font-ui)", fontSize: 11.5, color: "var(--text-muted)" }}>{sub}</span>}
    </div>
  );
}
