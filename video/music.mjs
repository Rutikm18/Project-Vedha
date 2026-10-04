// Original score for the Vedha film, synthesized in code (no samples, no licensed music).
// Deterministic: seeded noise only, so the same code writes the same WAV every time.
//
// Musical idea (see MUSIC.md): Raag Bhupali over a tanpura drone, Sa = D.
// The "path" phrase climbs S R G P D and stops on Dha, unresolved: the door is still open.
// When the fix is verified, the same phrase returns and lands on high Sa: the door is closed.
//
//   node music.mjs                 -> out/audio/score.wav (48 kHz stereo)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { T, FPS, DURATION } from './src/timeline.js';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SR = 48000;
const LEN = Math.round((DURATION / FPS) * SR);
const L = new Float32Array(LEN), R = new Float32Array(LEN);
const sec = frames => frames / FPS;

function mulberry32(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rnd = mulberry32(2026);

// ---- tuning: just intonation, Sa = D3 ----
const SA = 146.83;
const RATIO = { S: 1, R: 9 / 8, G: 5 / 4, P: 3 / 2, D: 5 / 3 };
const note = (n, oct = 0) => SA * RATIO[n] * 2 ** oct; // oct 0 = D3 octave, 1 = D4 ...

function add(buf, i, v) { if (i >= 0 && i < LEN) buf[i] += v; }
function put(t0, samples, gain, pan) { // equal-power pan, -1..1
  const s0 = Math.round(t0 * SR), gl = gain * Math.cos((pan + 1) * Math.PI / 4), gr = gain * Math.sin((pan + 1) * Math.PI / 4);
  for (let i = 0; i < samples.length; i++) { add(L, s0 + i, samples[i] * gl); add(R, s0 + i, samples[i] * gr); }
}

// ---- voices ----
// Plucked string (Karplus-Strong). `buzz` adds the tanpura's jawari shimmer.
function pluck(freq, dur, { decay = 0.996, bright = 0.5, buzz = 0 } = {}) {
  const n = Math.round(dur * SR), period = SR / freq, N = Math.floor(period), frac = period - N;
  const ring = new Float32Array(N + 2);
  for (let i = 0; i < ring.length; i++) ring[i] = rnd() * 2 - 1;
  // soften the excitation
  for (let k = 0; k < 2; k++) for (let i = 1; i < ring.length; i++) ring[i] = ring[i] * bright + ring[i - 1] * (1 - bright);
  const out = new Float32Array(n);
  let idx = 0;
  for (let i = 0; i < n; i++) {
    const a = ring[idx % ring.length], b = ring[(idx + 1) % ring.length];
    const y = a + (b - a) * frac;
    let v = y;
    if (buzz > 0) v = Math.tanh(y * (1 + buzz * 3)) * (0.7 + 0.3 * Math.sin(i / SR * 2 * Math.PI * 0.35));
    out[i] = v;
    ring[idx % ring.length] = decay * 0.5 * (a + b);
    idx++;
  }
  const fadeIn = Math.min(n, 48);
  for (let i = 0; i < fadeIn; i++) out[i] *= i / fadeIn;
  for (let i = Math.max(0, n - 2400); i < n; i++) out[i] *= (n - i) / 2400;
  return out;
}

// Bansuri-like flute: soft sine stack, breath, slow vibrato after the attack.
function flute(freq, dur, { attack = 0.12, release = 0.5, glideFrom = 0 } = {}) {
  const n = Math.round((dur + release) * SR), out = new Float32Array(n);
  let ph = 0, lp = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    const vib = t > 0.35 ? 1 + 0.004 * Math.sin(2 * Math.PI * 5.2 * t) * Math.min(1, (t - 0.35) * 2) : 1;
    const f = (glideFrom && t < 0.18 ? glideFrom + (freq - glideFrom) * (t / 0.18) : freq) * vib;
    ph += 2 * Math.PI * f / SR;
    const env = t < attack ? t / attack : t < dur ? 1 : Math.max(0, 1 - (t - dur) / release);
    lp += 0.04 * ((rnd() * 2 - 1) - lp); // breath, low-passed
    out[i] = env * (Math.sin(ph) + 0.22 * Math.sin(2 * ph) + 0.06 * Math.sin(3 * ph) + 0.35 * lp * (0.6 + 0.4 * env));
  }
  return out;
}

// Small bell: inharmonic partials, exponential decay.
function bell(freq, dur = 2.4) {
  const n = Math.round(dur * SR), out = new Float32Array(n);
  const parts = [[1, 1, 1.6], [2.0, 0.45, 1.0], [2.76, 0.3, 0.7], [5.4, 0.12, 0.35]];
  for (let i = 0; i < n; i++) {
    const t = i / SR; let v = 0;
    for (const [m, a, d] of parts) v += a * Math.sin(2 * Math.PI * freq * m * t) * Math.exp(-t / d);
    out[i] = v * Math.min(1, t * 400);
  }
  return out;
}

// Low pitched membrane ("thock"): the pierce.
function thock(f0 = 110, f1 = 48, dur = 0.7) {
  const n = Math.round(dur * SR), out = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR, f = f1 + (f0 - f1) * Math.exp(-t / 0.06);
    ph += 2 * Math.PI * f / SR;
    out[i] = Math.sin(ph) * Math.exp(-t / 0.22) + (i < 240 ? (rnd() * 2 - 1) * (1 - i / 240) * 0.3 : 0);
  }
  return out;
}

// Soft high membrane tick ("ta"): the steady pulse while the console works.
function tick(f = 520) {
  const n = Math.round(0.18 * SR), out = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR; ph += 2 * Math.PI * f * (1 + 0.3 * Math.exp(-t / 0.01)) / SR;
    out[i] = Math.sin(ph) * Math.exp(-t / 0.045);
  }
  return out;
}

// ---- the score ----
// Tanpura drone: Pa(low) Sa Sa Sa(low), every 2.4 s, from 0 to the CTA.
for (let t = 0, k = 0; t < sec(T.ctaAt) + 0.01; t += 2.4, k++) {
  const fade = Math.min(1, (t + 0.3) / 3);
  [[note('P', -1), 0], [note('S'), 0.55], [note('S'), 1.1], [note('S', -1), 1.65]].forEach(([f, dt], j) =>
    put(t + dt, pluck(f, 4.2, { decay: 0.9985, bright: 0.3, buzz: 0.4 }), 0.1 * fade, j % 2 ? 0.35 : -0.35));
}

// 1 Hook: one dot pulses (a soft high ping), then the door opens on Re, left hanging.
put(sec(T.pulseAt), bell(note('S', 2), 1.6), 0.05, 0.3);
put(sec(T.gapOpenAt), flute(note('R', 1), 0.9, { release: 0.9 }), 0.11, 0);

// 2 Path: one pluck per small thing (G, P, D), then the path phrase climbs and stops on Dha.
[[T.item1At, 'G'], [T.item2At, 'P'], [T.item3At, 'D']].forEach(([fr, n], i) =>
  put(sec(fr), pluck(note(n, 1), 2.2, { decay: 0.997, bright: 0.8 }), 0.2, -0.3 + i * 0.3));
const PHRASE = ['S', 'R', 'G', 'P', 'D'];
PHRASE.forEach((n, i) => put(sec(T.routeAt) + i * 0.3, flute(note(n, 1), i === 4 ? 1.1 : 0.26, { release: i === 4 ? 0.6 : 0.12 }), 0.12, 0));

// 3 Pierce: the strike is a low thock with Sa underneath; the name arrives on a warm Ga.
put(sec(T.strikeAt), thock(), 0.4, 0);
put(sec(T.strikeAt), pluck(note('S', -1), 3, { decay: 0.998, bright: 0.4, buzz: 0.3 }), 0.25, 0);
put(sec(T.whatAt), flute(note('G', 1), 1.2, { release: 0.8, glideFrom: note('R', 1) }), 0.1, 0);

// 3b Checkpoints: counted out, one soft pluck per checkpoint, climbing S to high S.
['S', 'R', 'G', 'P', 'D'].map(n => note(n, 1)).concat([note('S', 2)]).forEach((f, i) =>
  put(sec(T.checkItemsAt + i * T.checkStagger), pluck(f, 1.6, { decay: 0.996, bright: 0.85 }), 0.13, -0.4 + i * 0.16));

// 4 Partner: a second voice joins, a long Ga rising to Pa.
put(sec(T.partnerAt), flute(note('G', 1), 0.7, { release: 0.2 }), 0.1, -0.15);
put(sec(T.partnerAt) + 0.7, flute(note('P', 1), 1.0, { release: 0.6 }), 0.1, -0.15);

// 5 Console: a steady, unhurried pulse (90 bpm) while it finds and proves.
for (let t = sec(T.findingsAt); t < sec(T.snapAt) - 0.05; t += 60 / 90) put(t, tick(), 0.07, 0.2);
put(sec(T.attackAt), pluck(note('P', 0), 1.4, { bright: 0.6 }), 0.12, 0.1);
// The partner ticks the fix; the hold-to-verify ring swells on Dha...
put(sec(T.tickAt), tick(880), 0.08, 0);
put(sec(T.holdAt), flute(note('D', 1), sec(T.holdDur), { attack: sec(T.holdDur) * 0.9, release: 0.1 }), 0.1, 0);
// ...and verification resolves the path phrase home to high Sa, with the two-note chime (Pa -> Sa).
PHRASE.concat(['S+']).forEach((n, i) => {
  const f = n === 'S+' ? note('S', 2) : note(n, 1);
  put(sec(T.tealAt) + i * 0.11, flute(f, n === 'S+' ? 1.8 : 0.1, { attack: 0.03, release: n === 'S+' ? 1.0 : 0.08 }), 0.11, 0);
});
put(sec(T.tealAt) + 0.55, bell(note('P', 2), 2.2), 0.07, -0.2);
put(sec(T.tealAt) + 0.8, bell(note('S', 3), 2.6), 0.06, 0.2);

// 6 Report: three doors close, descending (D, P, G); a quiet bell when it is verified.
[[0, 'D'], [1, 'P'], [2, 'G']].forEach(([i, n]) => put(sec(T.doorsAt + i * T.doorStagger), pluck(note(n, 1), 1.4, { bright: 0.7 }), 0.12, 0.2 - i * 0.2));
put(sec(T.verifiedAt), bell(note('S', 2), 2), 0.05, 0);

// 7 CTA: Bhupali's signature close, G R S, landing on Sa with the drone; then it rings out.
put(sec(T.ctaAt) + 0.1, flute(note('G', 1), 0.3, { release: 0.1 }), 0.11, 0);
put(sec(T.ctaAt) + 0.4, flute(note('R', 1), 0.3, { release: 0.1 }), 0.11, 0);
put(sec(T.ctaAt) + 0.7, flute(note('S', 1), 1.0, { release: 0.7 }), 0.12, 0);
put(sec(T.ctaAt) + 0.7, pluck(note('S', -1), 1.9, { decay: 0.998, bright: 0.4, buzz: 0.5 }), 0.22, -0.2);
put(sec(T.ctaAt) + 0.7, pluck(note('P', -1), 1.9, { decay: 0.998, bright: 0.4, buzz: 0.5 }), 0.16, 0.2);

// ---- room: a small Schroeder reverb, then a gentle fade so the final frames are quiet ----
function reverb(x, seedDelay) {
  const combs = [1557, 1617, 1491, 1422].map(d => ({ d: d + seedDelay, buf: new Float32Array(d + seedDelay), i: 0, lp: 0 }));
  const aps = [225, 556].map(d => ({ d, buf: new Float32Array(d), i: 0 }));
  const y = new Float32Array(x.length);
  for (let n = 0; n < x.length; n++) {
    let s = 0;
    for (const c of combs) { const o = c.buf[c.i]; c.lp = o * 0.8 + c.lp * 0.2; c.buf[c.i] = x[n] + c.lp * 0.82; c.i = (c.i + 1) % c.d; s += o; }
    s *= 0.25;
    for (const a of aps) { const o = a.buf[a.i]; const v = -0.5 * s + o; a.buf[a.i] = s + 0.5 * o; a.i = (a.i + 1) % a.d; s = v; }
    y[n] = s;
  }
  return y;
}
const wl = reverb(L, 0), wr = reverb(R, 23);
const tailStart = Math.round((sec(T.stillFrom) - 0.6) * SR);
let peak = 0;
for (let i = 0; i < LEN; i++) {
  const fade = i < tailStart ? 1 : Math.max(0, 1 - (i - tailStart) / (LEN - tailStart));
  const fadeIn = Math.min(1, i / (0.05 * SR));
  L[i] = (L[i] * 0.78 + wl[i] * 0.32) * fade * fadeIn; R[i] = (R[i] * 0.78 + wr[i] * 0.32) * fade * fadeIn;
  peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
}

// ---- write 16-bit WAV (peak-normalised to -3 dBFS; loudness is set later by ffmpeg) ----
const g = peak > 0 ? 0.708 / peak : 1;
const data = Buffer.alloc(LEN * 4);
for (let i = 0; i < LEN; i++) {
  data.writeInt16LE(Math.round(Math.max(-1, Math.min(1, L[i] * g)) * 32767), i * 4);
  data.writeInt16LE(Math.round(Math.max(-1, Math.min(1, R[i] * g)) * 32767), i * 4 + 2);
}
const h = Buffer.alloc(44);
h.write('RIFF', 0); h.writeUInt32LE(36 + data.length, 4); h.write('WAVE', 8); h.write('fmt ', 12);
h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(2, 22); h.writeUInt32LE(SR, 24);
h.writeUInt32LE(SR * 4, 28); h.writeUInt16LE(4, 32); h.writeUInt16LE(16, 34); h.write('data', 36); h.writeUInt32LE(data.length, 40);
const out = path.join(ROOT, process.argv[2] || 'out/audio/score.wav');
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, Buffer.concat([h, data]));
console.log('wrote', out);
