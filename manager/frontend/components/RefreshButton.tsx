"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";
import { RefreshCw } from "lucide-react";
import { useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";

export interface RefreshButtonProps {
  delaySeconds?: number;
  size?: number;
  onBeforeRefresh?: () => void | Promise<unknown>;
}

/** Refetch active data and merge the route without discarding client work. */
export function RefreshButton({ delaySeconds = 0, size = 30, onBeforeRefresh }: RefreshButtonProps) {
  const queries = useQueryClient();
  const router = useRouter();
  const [phase, setPhase] = useState<"idle" | "queued" | "fetching" | "failed" | "done">("idle");
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const generation = useRef(0);
  const stop = useCallback(() => {
    if (timer.current) clearTimeout(timer.current);
    timer.current = null;
  }, []);
  useEffect(() => () => { stop(); generation.current++; }, [stop]);
  const start = () => {
    if (phase === "queued") { stop(); setPhase("idle"); return; }
    if (phase === "fetching") return;
    setPhase("queued");
    const request = ++generation.current;
    timer.current = setTimeout(async () => {
      timer.current = null;
      setPhase("fetching");
      try {
        await onBeforeRefresh?.();
        await queries.invalidateQueries({ refetchType: "none" });
        await queries.refetchQueries({ type: "active" }, { throwOnError: true });
        if (request !== generation.current) return;
        router.refresh();
        setPhase("done");
      } catch {
        if (request === generation.current) setPhase("failed");
      }
    }, delaySeconds * 1000);
  };
  const pending = phase === "queued" || phase === "fetching";
  const label = phase === "queued" ? "Refreshing — click to cancel" : phase === "fetching" ? "Refreshing data" : phase === "failed" ? "Retry refresh" : "Refresh data";
  return <>
    <button type="button" onClick={start} disabled={phase === "fetching"} aria-label={label} title={label} aria-busy={pending}
      style={{ display: "flex", alignItems: "center", justifyContent: "center", width: size, height: size,
        borderRadius: size >= 30 ? 8 : 7, flexShrink: 0, border: "0.5px solid var(--border-subtle)",
        background: pending ? "var(--accent-ghost)" : "transparent", cursor: "pointer",
        color: phase === "failed" ? "var(--sev-high-color)" : pending ? "var(--accent)" : "var(--text-muted)" }}>
      <RefreshCw size={size >= 30 ? 13 : 12} className={pending ? "animate-spin" : undefined} />
    </button>
    {phase === "failed" ? <span role="status" className="ui-refresh-error">Refresh failed. Retry.</span>
      : <span role="status" className="sr-only">{phase === "done" ? "Active data refreshed" : pending ? "Refreshing data" : ""}</span>}
  </>;
}
