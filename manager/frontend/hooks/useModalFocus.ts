"use client";

import { useEffect, type RefObject } from "react";

const FOCUSABLE = 'button:not(:disabled), a[href], input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])';

/** Protect a modal's focus and restore the surrounding UI on close. */
export function useModalFocus(
  ref: RefObject<HTMLElement | null>, open: boolean, close: () => void,
  returnSelector?: string, returnTarget?: RefObject<HTMLElement | null>,
) {
  useEffect(() => {
    const dialog = ref.current;
    if (!open || !dialog) return;
    const invoker = returnTarget?.current;
    const previous = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const siblings: Array<{ element: HTMLElement; inert: boolean }> = [];
    let branch: HTMLElement = dialog;
    while (branch.parentElement) {
      for (const sibling of Array.from(branch.parentElement.children)) {
        if (sibling !== branch && sibling instanceof HTMLElement && !sibling.hasAttribute("data-modal-backdrop")) {
          siblings.push({ element: sibling, inert: sibling.inert });
          sibling.inert = true;
        }
      }
      if (branch.parentElement === document.body) break;
      branch = branch.parentElement;
    }
    const controls = () => Array.from(dialog.querySelectorAll<HTMLElement>(FOCUSABLE))
      .filter((element) => element.getClientRects().length > 0 && !element.closest("[inert]"));
    (controls()[0] ?? dialog).focus();
    const keepFocus = (event: FocusEvent) => {
      if (!dialog.contains(event.target as Node)) (controls()[0] ?? dialog).focus();
    };
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        event.stopImmediatePropagation();
        close();
      } else if (event.key === "Tab") {
        const items = controls();
        const first = items[0];
        const last = items[items.length - 1];
        if (!first || (event.shiftKey ? document.activeElement === first : document.activeElement === last)) {
          event.preventDefault();
          (event.shiftKey ? last : first)?.focus();
        }
      }
    };
    document.addEventListener("keydown", onKey, true);
    document.addEventListener("focusin", keepFocus);
    return () => {
      document.removeEventListener("keydown", onKey, true);
      document.removeEventListener("focusin", keepFocus);
      for (const sibling of siblings) sibling.element.inert = sibling.inert;
      const fallback = returnSelector ? document.querySelector<HTMLElement>(returnSelector) : null;
      const target = invoker ?? (previous?.isConnected && previous !== document.body ? previous : fallback);
      // The invoker can be conditionally remounted when the dialog closes.
      requestAnimationFrame(() => {
        const restored = target?.isConnected ? target : returnSelector ? document.querySelector<HTMLElement>(returnSelector) : null;
        restored?.focus();
      });
    };
  }, [ref, open, close, returnSelector, returnTarget]);
}
