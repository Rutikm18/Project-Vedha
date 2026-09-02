"use client";

/**
 * Timestamp — one way to render a moment in the customer portal.
 *
 * WHY THIS EXISTS. The portal rendered time three different ways: reports showed
 * a full local datetime, scans showed "2h ago" with the exact value buried in a
 * detail panel, and findings showed nothing at all even though `first_seen` was
 * already in the API payload. For a VA record that is not cosmetic — "when was
 * this first seen?" and "when exactly did that scan run?" are evidentiary
 * questions, and "2h ago" cannot answer either one a week later.
 *
 * So: the EXACT local time is always the primary text. Relative age is a
 * secondary hint where it helps you scan a list, never a replacement. The
 * `title` carries the ISO-8601 UTC value, which is what someone correlating
 * against a log or another tool actually needs.
 */

import React from "react";

/** Exact local time, to the second. `—` for null/unparseable rather than a
 *  fabricated or silently-wrong date. */
export function formatExact(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString(undefined, {
    year: "numeric", month: "short", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  });
}

/** Compact local time for dense table cells — date + HH:MM:SS, no year noise
 *  for the current year. */
export function formatCompact(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  const sameYear = d.getFullYear() === new Date().getFullYear();
  return d.toLocaleString(undefined, {
    ...(sameYear ? {} : { year: "numeric" }),
    month: "short", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  });
}

export function formatRelative(iso: string | null | undefined): string {
  if (!iso) return "";
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return "";
  const s = Math.floor((Date.now() - t) / 1000);
  if (s < 0) return "scheduled";
  if (s < 60) return "just now";
  const m = Math.floor(s / 60); if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60); if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24); if (d < 30) return `${d}d ago`;
  const mo = Math.floor(d / 30); if (mo < 12) return `${mo}mo ago`;
  return `${Math.floor(mo / 12)}y ago`;
}

/** ISO-8601 UTC — the value to correlate against logs and other tools. */
export function isoUtc(iso: string | null | undefined): string {
  if (!iso) return "";
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? "" : d.toISOString();
}

export interface TimestampProps {
  value: string | null | undefined;
  /** Show the relative age underneath (lists) or after (inline). */
  relative?: boolean;
  /** `compact` drops the year in the current year — for table cells. */
  variant?: "exact" | "compact";
  /** Stack the relative hint below instead of inline. */
  block?: boolean;
  className?: string;
}

export function Timestamp({
  value, relative = false, variant = "compact", block = false, className,
}: TimestampProps) {
  const text = variant === "exact" ? formatExact(value) : formatCompact(value);
  const rel = relative ? formatRelative(value) : "";
  const utc = isoUtc(value);

  if (!value) return <span className="muted">—</span>;

  return (
    <span
      className={className}
      title={utc ? `${utc} (UTC)` : undefined}
      style={block ? { display: "inline-block" } : undefined}
    >
      <time dateTime={utc || undefined} className="num-mono">{text}</time>
      {rel && (
        <span
          className="muted"
          style={block
            ? { display: "block", fontSize: 11, marginTop: 1 }
            : { marginLeft: 6, fontSize: 11 }}
        >
          {rel}
        </span>
      )}
    </span>
  );
}
