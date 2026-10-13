// "How did you hear about us?" parsing for api/book.js: allow-listed values, bounded free text, UTM pass-through.
export const HEARD_FROM = ['it_partner', 'linkedin', 'whatsapp', 'friend', 'event', 'search', 'other'];

const clean = (v, max) => (typeof v === 'string' ? v.replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, max) : '');

export function parseHeardFrom(body = {}) {
  const value = clean(body.heard_from, 32);
  if (!HEARD_FROM.includes(value)) return { ok: false, error: 'Please tell us how you heard about us.' };
  const other = clean(body.heard_from_other, 120) || null;
  const utm = {};
  for (const k of ['utm_source', 'utm_medium', 'utm_campaign']) { const v = clean(body[k], 64); if (v) utm[k] = v; }
  return { ok: true, value, other, utm };
}
