/**
 * copyText — a clipboard write that works on every origin Vedha is served from.
 *
 * `navigator.clipboard` only exists in secure contexts (HTTPS or localhost). The
 * plain-HTTP deploy has none, so every copy button that called it directly threw
 * a TypeError and silently did nothing. This tries the async Clipboard API when
 * it is available and falls back to a hidden textarea + execCommand("copy").
 *
 * Resolves true only when a copy actually happened; never throws, so callers can
 * show honest success/failure feedback.
 */
export async function copyText(text: string): Promise<boolean> {
  if (typeof window === "undefined" || typeof document === "undefined") return false;
  const clip = typeof navigator !== "undefined" ? navigator.clipboard : undefined;
  if (window.isSecureContext && clip?.writeText) {
    try {
      await clip.writeText(text);
      return true;
    } catch {
      // Permission denied or document not focused — try the legacy path.
    }
  }
  return legacyCopy(text);
}

function legacyCopy(text: string): boolean {
  const active = document.activeElement as HTMLElement | null;
  // Inside a modal with a focus trap the textarea must live in the dialog, or
  // focus() is pulled back out and nothing ends up selected.
  const host = (active?.closest?.("[role='dialog']") as HTMLElement | null) ?? document.body;
  const area = document.createElement("textarea");
  area.value = text;
  area.setAttribute("readonly", "");
  area.setAttribute("aria-hidden", "true");
  Object.assign(area.style, {
    position: "fixed", top: "0", left: "0", opacity: "0", pointerEvents: "none",
  });
  host.appendChild(area);
  let ok = false;
  try {
    area.focus();
    area.select();
    area.setSelectionRange(0, text.length);
    ok = document.execCommand("copy");
  } catch {
    ok = false;
  } finally {
    host.removeChild(area);
    active?.focus?.();
  }
  return ok;
}
