/**
 * Page state that survives client-side navigation and tab reloads.
 *
 * A module-level store (not component state) so leaving a page — and even an
 * in-flight request that finishes after the component unmounted — does not lose
 * data. Selected keys are mirrored to sessionStorage (this tab only, gone when the
 * tab closes) and wiped on logout or session expiry by `clearSessionState()`.
 */
import { useCallback, useSyncExternalStore } from "react";

const PREFIX = "vedha.session.";
type Listener = () => void;
type Entry = { value: unknown; persist: boolean; listeners: Set<Listener>; hydrated: boolean };
const store = new Map<string, Entry>();

function entry(key: string, initial: unknown, persist: boolean): Entry {
  let e = store.get(key);
  if (!e) {
    e = { value: initial, persist, listeners: new Set(), hydrated: false };
    store.set(key, e);
  }
  return e;
}

function hydrate(key: string, e: Entry): void {
  if (e.hydrated || typeof window === "undefined") return;
  e.hydrated = true;
  if (!e.persist) return;
  try {
    const raw = window.sessionStorage.getItem(PREFIX + key);
    if (raw != null) e.value = JSON.parse(raw);
  } catch { /* storage blocked or corrupt: start from the initial value */ }
}

function write(key: string, e: Entry): void {
  if (!e.persist || typeof window === "undefined") return;
  try { window.sessionStorage.setItem(PREFIX + key, JSON.stringify(e.value)); } catch { /* quota/blocked */ }
}

/** Like useState, backed by the shared store. `persist: false` keeps it in memory only. */
export function useSessionState<T>(
  key: string, initial: T, opts: { persist?: boolean } = {},
): [T, (next: T | ((current: T) => T)) => void] {
  const persist = opts.persist ?? true;
  const e = entry(key, initial, persist);
  const value = useSyncExternalStore(
    (listener) => { e.listeners.add(listener); return () => { e.listeners.delete(listener); }; },
    () => { hydrate(key, e); return e.value as T; },
    () => initial,
  );
  const set = useCallback((next: T | ((current: T) => T)) => {
    const cur = entry(key, initial, persist);
    hydrate(key, cur);
    cur.value = typeof next === "function" ? (next as (c: T) => T)(cur.value as T) : next;
    write(key, cur);
    cur.listeners.forEach((l) => l());
  }, [key, initial, persist]);
  return [value, set];
}

/** Forget everything (logout, expired session). */
export function clearSessionState(): void {
  store.clear();
  if (typeof window === "undefined") return;
  try {
    Object.keys(window.sessionStorage)
      .filter((k) => k.startsWith(PREFIX))
      .forEach((k) => window.sessionStorage.removeItem(k));
  } catch { /* ignore */ }
}
