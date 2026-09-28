/**
 * print-mode.ts — one app-wide "we are producing a document" switch.
 *
 * A report on screen is interactive: cards collapse, filters narrow the list,
 * evidence is truncated, the theme may be dark. A report on paper (PDF) or in
 * Word must be none of those. Components read `usePrintMode()` and render
 * their full, static form while it is true.
 *
 * Why a module store and not per-component beforeprint listeners:
 *   - beforeprint is not a React event, so a plain setState would still be
 *     queued when the browser paginates. `flushSync` commits before we return.
 *   - A listener added DURING a dispatch is not called for that dispatch. A
 *     card that mounts because the print pass cleared a filter would miss its
 *     own beforeprint. Reading a module snapshot at render cannot miss it.
 *   - The Word export needs the same state without a print dialog, so it is
 *     callable directly (enterPrintMode / exitPrintMode).
 *
 * Documents are always produced in the light theme; the user's theme is put
 * back afterwards.
 */
import { useSyncExternalStore } from "react";
import { flushSync } from "react-dom";

let printing = false;
let savedTheme: string | null = null;
const listeners = new Set<() => void>();
let wired = false;

function emit() {
  flushSync(() => { listeners.forEach(l => l()); });
}

export function enterPrintMode(): void {
  if (printing) return;
  printing = true;
  if (typeof document !== "undefined") {
    const root = document.documentElement;
    savedTheme = root.getAttribute("data-theme");
    root.setAttribute("data-theme", "light");
  }
  emit();
}

export function exitPrintMode(): void {
  if (!printing) return;
  printing = false;
  if (typeof document !== "undefined" && savedTheme !== null) {
    document.documentElement.setAttribute("data-theme", savedTheme);
  }
  savedTheme = null;
  emit();
}

export function isPrintMode(): boolean {
  return printing;
}

function subscribe(listener: () => void): () => void {
  if (!wired && typeof window !== "undefined") {
    // Registered once for the life of the page: covers the Export PDF button
    // and the browser's own Ctrl/Cmd+P alike.
    window.addEventListener("beforeprint", enterPrintMode);
    window.addEventListener("afterprint", exitPrintMode);
    wired = true;
  }
  listeners.add(listener);
  return () => { listeners.delete(listener); };
}

export function usePrintMode(): boolean {
  return useSyncExternalStore(subscribe, isPrintMode, () => false);
}
