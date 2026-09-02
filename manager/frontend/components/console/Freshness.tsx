"use client";
import React, { useEffect, useState } from "react";

/** "Updated 12s ago" + a stale flag, read from React Query's dataUpdatedAt.
 *  Purely presentational — it never triggers a fetch. */
export function Freshness({
  updatedAt, isFetching, staleAfterMs = 180_000,
}: { updatedAt?: number; isFetching?: boolean; staleAfterMs?: number }) {
  const [, tick] = useState(0);
  useEffect(() => {
    const t = setInterval(() => tick((n) => n + 1), 10_000);
    return () => clearInterval(t);
  }, []);

  if (!updatedAt) return null;
  const age = Date.now() - updatedAt;
  const stale = age > staleAfterMs;
  const label =
    age < 60_000 ? `${Math.max(1, Math.round(age / 1000))}s ago`
    : age < 3_600_000 ? `${Math.round(age / 60_000)}m ago`
    : `${Math.round(age / 3_600_000)}h ago`;

  return (
    <span
      style={{
        display: "inline-flex", alignItems: "center", gap: "var(--space-1)",
        fontFamily: "var(--font-ui)", fontSize: "var(--fs-label)",
        color: stale ? "var(--fresh-stale)" : "var(--fresh-ok)",
      }}
      title={new Date(updatedAt).toLocaleString()}
    >
      <span aria-hidden style={{
        width: 5, height: 5, borderRadius: "var(--r-pill)",
        background: "currentColor", opacity: isFetching ? 1 : 0.55,
      }} />
      <span className="sr-only">Data last updated </span>
      {isFetching ? "Updating…" : label}
      {stale && !isFetching && <span className="sr-only"> — this may be out of date</span>}
    </span>
  );
}
