/**
 * RFC 4122 v4 id that works on plain-HTTP origins too.
 *
 * crypto.randomUUID() exists only in secure contexts (HTTPS or localhost), so a
 * portal opened as http://<server-ip> threw "crypto.randomUUID is not a
 * function" on every idempotent write (finding status, scans, extensions).
 * crypto.getRandomValues() is available everywhere, so fall back to it.
 */
export function newId(): string {
  const c = globalThis.crypto;
  if (typeof c?.randomUUID === "function") return c.randomUUID();
  const b = new Uint8Array(16);
  c.getRandomValues(b);
  b[6] = (b[6] & 0x0f) | 0x40; // version 4
  b[8] = (b[8] & 0x3f) | 0x80; // RFC 4122 variant
  const h = Array.from(b, (x) => x.toString(16).padStart(2, "0")).join("");
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
}
