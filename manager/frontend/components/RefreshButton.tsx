"use client";

/**
 * RefreshButton — a header control that reloads the current page after a short
 * delay.
 *
 * WHY THE DELAY. The trigger for this is enrolling a vedha-agent: the probe
 * completes enrollment against the API a moment after the UI action, so an
 * instant reload frequently re-renders BEFORE the write has landed and the new
 * agent still looks missing. Waiting ~2s lets the backend settle, and the
 * spinner makes the wait legible instead of feeling like a dead click.
 *
 * Cancellable on a second click — a reload the user has changed their mind about
 * should not still fire. The timer is cleared on unmount so a queued reload can
 * never outlive the page that scheduled it.
 */

import React, { useCallback, useEffect, useRef, useState } from "react";
import { RefreshCw } from "lucide-react";

export interface RefreshButtonProps {
  /** Seconds to wait before reloading. */
  delaySeconds?: number;
  /** 30 matches the operator header; the portal header uses 28. */
  size?: number;
  /** Called just before the reload — e.g. to invalidate a query cache. */
  onBeforeRefresh?: () => void;
}

export function RefreshButton({
  delaySeconds = 2, size = 30, onBeforeRefresh,
}: RefreshButtonProps) {
  const [pending, setPending] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const stop = useCallback(() => {
    if (timer.current !== null) {
      clearTimeout(timer.current);
      timer.current = null;
    }
  }, []);

  // A queued reload must not outlive the page that scheduled it.
  useEffect(() => stop, [stop]);

  const start = useCallback(() => {
    if (pending) {                     // second click cancels
      stop();
      setPending(false);
      return;
    }
    setPending(true);
    timer.current = setTimeout(() => {
      timer.current = null;
      onBeforeRefresh?.();
      if (typeof window !== "undefined") window.location.reload();
    }, delaySeconds * 1000);
  }, [pending, delaySeconds, stop, onBeforeRefresh]);

  const label = pending ? "Refreshing — click to cancel" : "Refresh page";

  return (
    <button
      onClick={start}
      aria-label={label}
      title={label}
      aria-live="polite"
      style={{
        display: "flex", alignItems: "center", justifyContent: "center",
        width: size, height: size,
        borderRadius: size >= 30 ? 8 : 7, flexShrink: 0,
        border: "0.5px solid var(--border-subtle)",
        background: pending ? "var(--accent-ghost)" : "transparent",
        cursor: "pointer",
        color: pending ? "var(--accent)" : "var(--text-muted)",
        transition: "all 0.18s var(--ease-spring)",
        fontFamily: "var(--font-mono)", fontSize: 10,
      }}
    >
      {/* Spinner only — the countdown digits read as an error code at this size,
          and the delay is short enough that "working" is the whole message. */}
      <RefreshCw
        size={size >= 30 ? 13 : 12}
        className={pending ? "animate-spin" : undefined}
      />
    </button>
  );
}
