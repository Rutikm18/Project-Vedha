// SRT captions straight from timeline.js + copy.*.json, so subtitles always match the film.
import { CAPTIONS, FPS } from './src/timeline.js';

const ts = f => {
  const ms = Math.round(f / FPS * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`;
};

export function captionText(c, copy) {
  switch (c.key) {
    case 'list': return c.i == null ? copy.list.join('\n') : copy.list[c.i];
    case 'name': return `${copy.name} (${copy.devanagari}): ${copy.gloss.toLowerCase()}.\n${copy.what}`;
    case 'checks': {
      const cp = copy.checkpoints;
      // two per line keeps every subtitle line short enough to read in one glance
      const pairs = []; for (let i = 0; i < cp.length; i += 2) pairs.push(cp.slice(i, i + 2).join(' · '));
      return [copy.checks, ...pairs].join('\n');
    }
    case 'cta': return `${copy.cta}. ${copy.url}\n${copy.scope}`;
    default: return copy[c.key];
  }
}

// `map` turns film frames into output frames (for the cutdown); return null to drop a cue.
export function buildSrt(copy, map = (from, to) => [from, to]) {
  let n = 0;
  return CAPTIONS.map(c => {
    const r = map(c.from, c.to);
    return r ? `${++n}\n${ts(r[0])} --> ${ts(r[1])}\n${captionText(c, copy)}\n` : null;
  }).filter(Boolean).join('\n');
}
