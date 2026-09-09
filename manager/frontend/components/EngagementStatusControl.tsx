"use client";

/**
 * EngagementStatusControl — change an engagement's lifecycle state in one click,
 * from the engagement header.
 *
 * The state was only reachable through the "Edit details" modal, so in practice
 * every engagement sat on Planning forever: changing it meant opening a form
 * about scope and dates and saving the whole thing.
 *
 * WHAT IS AND IS NOT A STATUS HERE. These four are the OPERATOR'S INTENT —
 * a decision a person makes and the platform records:
 *
 *     Planning → Active → (Paused) → Completed
 *
 * "Running" is deliberately NOT one of them. Whether a scan is executing right
 * now is an OBSERVED fact, derived from live scan jobs, and it belongs next to
 * this control rather than inside it (see `liveHint`). Storing it as a status
 * would let someone set "Running" with nothing running — a claim the platform
 * could not back, which is exactly the kind of thing a VA tool must not do.
 */

import React, { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Check, ChevronDown, Loader2 } from "lucide-react";
import { fetchJson } from "../lib/fetcher";
import { useToast } from "../hooks/useToast";

/** The UI tokens the rest of the app already uses (lib/adapters maps them to the
 *  backend's draft/active/paused/completed). Labels are the operator-facing words. */
export const ENGAGEMENT_STATES = [
  { value: "PLANNING",  label: "Planning",  hint: "Scope agreed, not started yet" },
  { value: "ONGOING",   label: "Ongoing",   hint: "Assessment underway" },
  { value: "RUNNING",   label: "Running",   hint: "Active scanning phase" },
  { value: "PAUSED",    label: "Paused",    hint: "Temporarily on hold" },
  { value: "COMPLETED", label: "Completed", hint: "Assessment finished" },
] as const;

export const STATUS_COLOR: Record<string, string> = {
  PLANNING:  "var(--sev-info-color)",
  // ACTIVE is the pre-0035 stored value. Kept so engagements created before the
  // lifecycle states existed still render with a colour instead of falling
  // through to grey.
  ACTIVE:    "var(--accent)",
  ONGOING:   "var(--accent)",
  RUNNING:   "var(--state-busy, var(--accent))",
  PAUSED:    "var(--sev-medium-color)",
  COMPLETED: "var(--nominal-color)",
};

export interface EngagementStatusControlProps {
  engagementId: string;
  status: string;
  /** Live, observed state shown beside the control — e.g. "1 scan running".
   *  Never conflated with the stored status. */
  liveHint?: string | null;
  /** Optional surface adapter. Defaults to the manager BFF. */
  updateStatus?: (next: string) => Promise<unknown>;
  invalidateKeys?: ReadonlyArray<readonly unknown[]>;
}

export function EngagementStatusControl({
  engagementId, status, liveHint, updateStatus, invalidateKeys,
}: EngagementStatusControlProps) {
  const [open, setOpen] = useState(false);
  const queryClient = useQueryClient();
  const toast = useToast();

  // Pre-0035 engagements are stored as ACTIVE, which is no longer offered in the
  // menu. Show it truthfully rather than mislabelling the engagement "Planning";
  // picking any menu entry migrates it forward.
  const current = ENGAGEMENT_STATES.find((s) => s.value === status)
    ?? (status === "ACTIVE"
      ? { value: "ACTIVE", label: "Active", hint: "Assessment underway (legacy state)" } as const
      : ENGAGEMENT_STATES[0]);

  const mutation = useMutation({
    // PATCH only the status. Sending the whole form here would let a stale copy
    // of scope or dates overwrite a change someone else just made.
    mutationFn: (next: string) => updateStatus
      ? updateStatus(next)
      : fetchJson(`/api/engagements/${engagementId}`, {
          method: "PUT",
          body: JSON.stringify({ status: next }),
        }),
    onSuccess: (_d, next) => {
      const keys = invalidateKeys ?? [["engagement", engagementId], ["engagements"]];
      keys.forEach((queryKey) => void queryClient.invalidateQueries({ queryKey }));
      const label = ENGAGEMENT_STATES.find((s) => s.value === next)?.label ?? next;
      toast.success("Status updated", `Engagement is now ${label}.`);
      setOpen(false);
    },
    onError: (e) => toast.error(
      "Could not update status",
      e instanceof Error ? e.message : "The change was not saved."),
  });

  const busy = mutation.isPending;

  return (
    <div style={{ position: "relative", display: "inline-flex", alignItems: "center", gap: 8 }}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        disabled={busy}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={`Engagement status: ${current.label}. Change it.`}
        className="focusable"
        style={{
          display: "inline-flex", alignItems: "center", gap: 6,
          height: 30, padding: "0 10px", borderRadius: 8,
          border: `0.5px solid ${STATUS_COLOR[current.value] ?? "var(--border-subtle)"}`,
          background: "transparent", cursor: busy ? "wait" : "pointer",
          color: STATUS_COLOR[current.value] ?? "var(--text-secondary)",
          fontSize: 12, fontWeight: 500,
        }}
      >
        {busy
          ? <Loader2 size={12} className="animate-spin" />
          : <span aria-hidden style={{
              width: 7, height: 7, borderRadius: 999,
              background: STATUS_COLOR[current.value] ?? "var(--text-muted)",
            }} />}
        {current.label}
        <ChevronDown size={12} style={{ opacity: 0.7 }} />
      </button>

      {liveHint && (
        <span className="muted" style={{ fontSize: 11 }}>{liveHint}</span>
      )}

      {open && (
        <>
          {/* click-away */}
          <div
            role="presentation"
            onClick={() => setOpen(false)}
            style={{ position: "fixed", inset: 0, zIndex: 40 }}
          />
          <ul
            role="listbox"
            aria-label="Engagement status"
            style={{
              position: "absolute", top: 36, left: 0, zIndex: 41, minWidth: 232,
              margin: 0, padding: 4, listStyle: "none",
              background: "var(--bg-panel)",
              border: "0.5px solid var(--border-default)",
              borderRadius: 10, boxShadow: "var(--shadow-lg, 0 8px 24px rgba(0,0,0,0.18))",
            }}
          >
            {ENGAGEMENT_STATES.map((s) => {
              const active = s.value === current.value;
              return (
                <li key={s.value}>
                  <button
                    type="button"
                    role="option"
                    aria-selected={active}
                    disabled={busy}
                    onClick={() => (active ? setOpen(false) : mutation.mutate(s.value))}
                    className="focusable"
                    style={{
                      display: "flex", alignItems: "flex-start", gap: 8, width: "100%",
                      padding: "8px 10px", borderRadius: 7, border: "none",
                      background: active ? "var(--accent-ghost)" : "transparent",
                      cursor: busy ? "wait" : "pointer", textAlign: "left",
                    }}
                  >
                    <span aria-hidden style={{
                      width: 7, height: 7, borderRadius: 999, marginTop: 5, flexShrink: 0,
                      background: STATUS_COLOR[s.value],
                    }} />
                    <span style={{ minWidth: 0, flex: 1 }}>
                      <span style={{ display: "block", fontSize: 12.5, fontWeight: 500,
                                     color: "var(--text-primary)" }}>
                        {s.label}
                      </span>
                      <span style={{ display: "block", fontSize: 11, color: "var(--text-muted)" }}>
                        {s.hint}
                      </span>
                    </span>
                    {active && <Check size={13} style={{ color: "var(--accent)", marginTop: 3 }} />}
                  </button>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </div>
  );
}
