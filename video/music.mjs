// Original score for the Vedha film, synthesized in code (no samples, no licensed music).
// Deterministic: seeded noise only, so the same code writes the same WAV every time.
//
// Built on an excitement arc from music psychology (see MUSIC.md):
//   curiosity (sparse, rising) -> anticipation (riser + roll + a beat of silence) ->
//   arrival (impact + a 110 bpm groove: high arousal, positive valence) ->
//   a second, bigger anticipation -> PEAK exactly on "verified" -> a clean, confident end.
// Raag Bhupali (S R G P D, Sa = D): bright, consonant, Indian, never menacing.
//
//   node music.mjs [out/audio/score.wav]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { T, FPS, DURATION } from './src/timeline.js';
import { FOUND } from './src/film.js';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SR = 48000;
const LEN = Math.round((DURATION / FPS) * SR);
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
const noise = () => rnd() * 2 - 1;

// ---- tuning: just intonation, Sa = D3 ----
const SA = 146.83;
const RATIO = { S: 1, R: 9 / 8, G: 5 / 4, P: 3 / 2, D: 5 / 3 };
const note = (n, oct = 0) => SA * RATIO[n] * 2 ** oct;

// ---- tempo grid: 110 bpm, anchored on the pierce (frame 282 = 9.4 s); beat 24 lands on "verified" ----
const BPM = 110, BEAT = 60 / BPM, ANCHOR = sec(T.strikeAt);
const beat = k => ANCHOR + k * BEAT;
const PEAK = sec(T.tealAt);        // 22.5 s = beat 24
const END = beat(33);              // 27.4 s, just before the CTA settles

// ---- buses: drums, music (ducked by the kick for lift), lead (flute/bells, never ducked) ----
const bus = () => ({ L: new Float32Array(LEN), R: new Float32Array(LEN) });
const DR = bus(), MU = bus(), LD = bus();
function put(b, t0, samples, gain, pan = 0) {
  const s0 = Math.round(t0 * SR), gl = gain * Math.cos((pan + 1) * Math.PI / 4), gr = gain * Math.sin((pan + 1) * Math.PI / 4);
  for (let i = 0; i < samples.length; i++) { const j = s0 + i; if (j >= 0 && j < LEN) { b.L[j] += samples[i] * gl; b.R[j] += samples[i] * gr; } }
}
const kicks = [];

// ---- voices ----
function pluck(freq, dur, { decay = 0.996, bright = 0.5, buzz = 0 } = {}) {
  const n = Math.round(dur * SR), period = SR / freq, N = Math.floor(period), frac = period - N;
  const ring = new Float32Array(N + 2);
  for (let i = 0; i < ring.length; i++) ring[i] = noise();
  for (let k = 0; k < 2; k++) for (let i = 1; i < ring.length; i++) ring[i] = ring[i] * bright + ring[i - 1] * (1 - bright);
  const out = new Float32Array(n);
  for (let i = 0, idx = 0; i < n; i++, idx++) {
    const a = ring[idx % ring.length], b = ring[(idx + 1) % ring.length], y = a + (b - a) * frac;
    out[i] = buzz > 0 ? Math.tanh(y * (1 + buzz * 3)) : y;
    ring[idx % ring.length] = decay * 0.5 * (a + b);
  }
  for (let i = 0; i < Math.min(n, 48); i++) out[i] *= i / 48;
  for (let i = Math.max(0, n - 2400); i < n; i++) out[i] *= (n - i) / 2400;
  return out;
}
function flute(freq, dur, { attack = 0.08, release = 0.4, glideFrom = 0 } = {}) {
  const n = Math.round((dur + release) * SR), out = new Float32Array(n);
  let ph = 0, lp = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    const vib = t > 0.3 ? 1 + 0.004 * Math.sin(2 * Math.PI * 5.4 * t) * Math.min(1, (t - 0.3) * 2) : 1;
    const f = (glideFrom && t < 0.12 ? glideFrom + (freq - glideFrom) * (t / 0.12) : freq) * vib;
    ph += 2 * Math.PI * f / SR;
    const env = t < attack ? t / attack : t < dur ? 1 : Math.max(0, 1 - (t - dur) / release);
    lp += 0.04 * (noise() - lp);
    out[i] = env * (Math.sin(ph) + 0.22 * Math.sin(2 * ph) + 0.06 * Math.sin(3 * ph) + 0.3 * lp * (0.6 + 0.4 * env));
  }
  return out;
}
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
function kick(level = 1) {
  const n = Math.round(0.4 * SR), out = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR, f = 45 + 95 * Math.exp(-t / 0.035);
    ph += 2 * Math.PI * f / SR;
    out[i] = level * (Math.sin(ph) * Math.exp(-t / 0.2) + (i < 120 ? noise() * 0.25 * (1 - i / 120) : 0));
  }
  return out;
}
// Tabla dayan "na": a tuned membrane with the harmonic overtones the syahi gives it.
function na(f = note('S', 2), dur = 0.22, soft = false) {
  const n = Math.round(dur * SR), out = new Float32Array(n);
  const parts = soft ? [[1, 0.7, 0.07], [2, 0.25, 0.05]] : [[1, 0.6, 0.12], [2, 0.35, 0.09], [3, 0.2, 0.06], [4, 0.1, 0.04]];
  for (let i = 0; i < n; i++) {
    const t = i / SR; let v = 0;
    for (const [m, a, d] of parts) v += a * Math.sin(2 * Math.PI * f * m * t * (1 + 0.02 * Math.exp(-t / 0.01))) * Math.exp(-t / d);
    out[i] = v + (i < 60 ? noise() * 0.3 * (1 - i / 60) : 0);
  }
  return out;
}
// Tabla bayan "ge": a low bass stroke that bends down.
function ge() {
  const n = Math.round(0.5 * SR), out = new Float32Array(n); let ph = 0;
  for (let i = 0; i < n; i++) { const t = i / SR, f = 70 + 30 * Math.exp(-t / 0.12); ph += 2 * Math.PI * f / SR; out[i] = Math.sin(ph) * Math.exp(-t / 0.28); }
  return out;
}
function shaker(dur = 0.06) {
  const n = Math.round(dur * SR), out = new Float32Array(n); let prev = 0;
  for (let i = 0; i < n; i++) { const x = noise(); out[i] = (x - prev) * 0.5 * Math.min(1, i / 120) * Math.exp(-i / SR / (dur / 3)); prev = x; }
  return out;
}
// Bass: a soft, filtered saw pluck.
function bass(freq, dur = 0.24) {
  const n = Math.round(dur * SR), out = new Float32Array(n); let ph = 0, lp = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR; ph = (ph + freq / SR) % 1;
    const cut = 0.02 + 0.10 * Math.exp(-t / 0.05);
    lp += cut * ((2 * ph - 1) - lp);
    out[i] = lp * Math.min(1, t * 300) * Math.exp(-t / (dur * 0.6));
  }
  return out;
}
// Pad: three detuned saws per note through a one-pole low-pass; slow attack and release.
function pad(freqs, dur, { attack = 0.6, release = 1.2, cutoff = 0.06 } = {}) {
  const n = Math.round((dur + release) * SR), out = new Float32Array(n);
  const oscs = freqs.flatMap(f => [f * 0.996, f, f * 1.004]).map(f => ({ f, ph: rnd() }));
  let lp = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR; let v = 0;
    for (const o of oscs) { o.ph = (o.ph + o.f / SR) % 1; v += 2 * o.ph - 1; }
    lp += cutoff * (v / oscs.length - lp);
    const env = t < attack ? t / attack : t < dur ? 1 : Math.max(0, 1 - (t - dur) / release);
    out[i] = lp * env;
  }
  return out;
}
// Riser: noise through a sweeping band-pass plus a rising tone, swelling toward the hit.
function riser(dur) {
  const n = Math.round(dur * SR), out = new Float32Array(n); let low = 0, band = 0, ph = 0;
  for (let i = 0; i < n; i++) {
    const t = i / n, fc = 300 * Math.pow(20, t), F = 2 * Math.sin(Math.PI * fc / SR), q = 0.25;
    const x = noise(); low += F * band; const high = x - low - q * band; band += F * high;
    ph += 2 * Math.PI * (180 * Math.pow(4, t)) / SR;
    out[i] = (band * 0.9 + Math.sin(ph) * 0.15) * Math.pow(t, 2.2);
  }
  return out;
}
// Impact: a warm sub boom with a soft, low-passed splash. Big, not threatening.
function impact() {
  const n = Math.round(1.8 * SR), out = new Float32Array(n); let ph = 0, lp = 0;
  for (let i = 0; i < n; i++) {
    const t = i / SR, f = 38 + 60 * Math.exp(-t / 0.08);
    ph += 2 * Math.PI * f / SR; lp += 0.08 * (noise() - lp);
    out[i] = Math.sin(ph) * Math.exp(-t / 0.5) + lp * 1.6 * Math.exp(-t / 0.35);
  }
  return out;
}

// ---- the sonic logo: Sa -> Pa -> high Sa (a rising fifth then a fourth: open, confident, complete) ----
function sonicLogo(t, gain = 1, { question = false } = {}) {
  const notes = question ? [note('S', 1), note('P', 1)] : [note('S', 1), note('P', 1), note('S', 2)];
  notes.forEach((f, i) => {
    const at = t + i * BEAT / 2, last = i === notes.length - 1;
    put(LD, at, bell(f * 2, last ? 2.6 : 1.4), 0.07 * gain, -0.15 + i * 0.15);
    put(LD, at, flute(f, last ? (question ? 0.9 : 1.4) : BEAT / 2 - 0.04, { attack: 0.02, release: last ? 0.9 : 0.06 }), 0.11 * gain, 0);
  });
}

// ===================== THE SCORE =====================

// 1 Hook (0-3 s): curiosity. A pad breathes in; the logo asks a question (Sa -> Pa, unfinished);
// the door opens on a single held Re.
put(MU, 0.2, pad([note('S', -1), note('P', -1), note('G', 0)], 2.8, { attack: 2.0, release: 1.5, cutoff: 0.03 }), 0.16);
sonicLogo(0.6, 0.6, { question: true });
put(LD, sec(T.gapOpenAt), flute(note('R', 1), 0.8, { release: 0.8 }), 0.09, 0);

// 2 Discovery (3.2-9.4 s): a rising note for every device the scan finds (counting up = discovery),
// a heartbeat that slowly gets stronger, and one weighted hit for each thing that matters.
const SCALE = ['S', 'R', 'G', 'P', 'D'];
FOUND.forEach((fr, i) => {
  const n = SCALE[i % 5], oct = 1 + Math.floor(i / 5) * 0.5 >= 2 ? 2 : 1 + (i >= 5 ? 1 : 0);
  put(LD, sec(fr), pluck(note(n, oct), 0.9, { bright: 0.9, decay: 0.993 }), 0.08, -0.5 + (i / FOUND.length));
});
for (let k = -12; k < 0; k++) {
  const t = beat(k); if (t < 3.0) continue;
  const lvl = 0.25 + 0.5 * (k + 12) / 12;
  put(DR, t, kick(lvl), 0.5); kicks.push([t, lvl]);
}
put(MU, 3.0, pad([note('S', -1), note('P', -1), note('G', 0), note('R', 1)], 6.3, { attack: 1.5, release: 0.3, cutoff: 0.04 }), 0.14);
[[T.item1At, 'G'], [T.item2At, 'P'], [T.item3At, 'D']].forEach(([fr, n], i) => {
  put(DR, sec(fr), ge(), 0.35, 0);
  put(LD, sec(fr), pluck(note(n, 1), 2.0, { decay: 0.997, bright: 0.75 }), 0.22, -0.25 + i * 0.25);
});
for (let t = sec(T.item1At); t < beat(-0.2); t += BEAT / 2) put(DR, t, shaker(), 0.18, 0.4);   // shaker from the first finding
for (let k = -7; k < 0; k++) for (const h of [0, 0.5]) put(MU, beat(k + h), bass(note('S', -2)), 0.22); // bass pulse from the second
// The unresolved phrase climbs over the build and stops on Dha (the open door).
SCALE.forEach((n, i) => put(LD, beat(-4) + i * BEAT / 2, flute(note(n, 1), i === 4 ? 1.0 : BEAT / 2 - 0.05, { attack: 0.02, release: i === 4 ? 0.3 : 0.05 }), 0.1, 0));
// Anticipation: riser + an accelerating tabla roll, then a breath of silence before the strike.
put(MU, beat(-3), riser(beat(-0.12) - beat(-3)), 0.3);
{ let t = beat(-2), step = BEAT / 2; while (t < beat(-0.15)) { put(DR, t, na(note('S', 2), 0.12, true), 0.22 + 0.25 * (t - beat(-2)) / (2 * BEAT), 0.2); t += step; step = Math.max(BEAT / 8, step * 0.82); } }

// 3 Pierce (9.4 s): arrival. Impact, the full logo, and the groove begins.
put(DR, ANCHOR, impact(), 0.55); kicks.push([ANCHOR, 1]);
sonicLogo(ANCHOR, 1);
put(MU, ANCHOR, pluck(note('S', -1), 3, { decay: 0.998, bright: 0.4, buzz: 0.4 }), 0.22);

// The groove (beats 0-33): kick, tabla theka, shaker, bass ostinato, pads. A build and a gap before the peak.
const BASS = ['S', 'S', null, 'S', 'P', null, 'D', 'P'];               // eighths per bar
const CHORDS = [[note('S', -1), note('G', -1), note('P', -1), note('R', 0)], [note('D', -2), note('S', -1), note('G', -1), note('P', -1)]];
for (let k = 0; k < 33; k++) {
  const t = beat(k), inBuild = t >= sec(T.fixAt) && t < PEAK, peakHalf = t >= PEAK;
  const halfTime = k < 4;                                            // first bar after the strike: half-time
  if (t >= PEAK - BEAT * 0.25 && t < PEAK) continue;                   // the gap
  // kick: 1 and 3 (half-time: 1 only); four on the floor in the build; ghost on the and-of-4 every other bar after the peak
  const kb = k % 4;
  if ((halfTime ? kb === 0 : kb === 0 || kb === 2) || inBuild) { const lv = inBuild ? 0.8 : 1; put(DR, t, kick(lv), 0.62); kicks.push([t, lv]); }
  if (peakHalf && kb === 3 && Math.floor(k / 4) % 2) { put(DR, t + BEAT / 2, kick(0.5), 0.5); kicks.push([t + BEAT / 2, 0.5]); }
  // tabla: ge on 1, na on the off-beats, soft tin elsewhere
  if (kb === 0) put(DR, t, ge(), 0.3, -0.1);
  if (!halfTime) {
    put(DR, t + BEAT / 2, na(), peakHalf ? 0.26 : 0.2, 0.25);
    put(DR, t, na(note('S', 2), 0.1, true), 0.1, 0.25);
    for (const q of [0, 0.25, 0.5, 0.75]) put(DR, t + q * BEAT, shaker(0.05), (q === 0.5 ? 0.16 : 0.09) * (peakHalf ? 1.4 : 1), 0.45);
  }
  // bass ostinato (eighths); octave doubled after the peak
  for (const h of [0, 0.5]) {
    const n = BASS[(kb * 2 + (h ? 1 : 0)) % 8];
    if (n && !(t + h * BEAT >= PEAK - BEAT * 0.25 && t + h * BEAT < PEAK)) {
      put(MU, t + h * BEAT, bass(note(n, -2)), 0.32);
      if (peakHalf) put(MU, t + h * BEAT, bass(note(n, -1), 0.18), 0.12);
    }
  }
  // pads: a chord every two bars (Dadd9, then Bm7), brighter after the peak
  if (k % 8 === 0) put(MU, t, pad(CHORDS[(k / 8) % 2], BEAT * 8 - 0.1, { attack: 0.3, release: 0.4, cutoff: peakHalf ? 0.09 : 0.055 }), 0.2);
}

// 3b Checkpoints: one bright pluck on each checkpoint, climbing.
['S', 'G', 'P', 'S+'].forEach((n, i) => put(LD, sec(T.checkItemsAt + i * T.checkStagger), bell(n === 'S+' ? note('S', 3) : note(n, 2), 1.2), 0.06, -0.3 + i * 0.2));

// 4 Partner: a warm flute line joins (Ga - Pa - Dha - Pa).
[['G', 0, 1], ['P', 1, 1], ['D', 2, 1.5], ['P', 3.5, 1]].forEach(([n, at, len]) =>
  put(LD, sec(T.partnerAt) + at * BEAT, flute(note(n, 1), len * BEAT - 0.05, { release: 0.25 }), 0.1, -0.1));

// 5 Console: accents on Find and Prove; the evidence "lands" with a small bell.
put(LD, sec(T.findingsAt), pluck(note('P', 1), 1.2, { bright: 0.7 }), 0.15, 0.1);
put(LD, sec(T.proveAt), bell(note('P', 2), 1.4), 0.07, 0.1);
// The second, bigger anticipation: hold-to-verify swells on Dha, a riser and a roll, then the gap.
put(LD, sec(T.holdAt), flute(note('D', 1), PEAK - BEAT * 0.25 - sec(T.holdAt), { attack: 0.4, release: 0.05 }), 0.1, 0);
put(MU, sec(T.fixAt), riser(PEAK - BEAT * 0.25 - sec(T.fixAt)), 0.32);
{ let t = sec(T.fixAt), step = BEAT / 2; while (t < PEAK - BEAT * 0.3) { put(DR, t, na(note('S', 2), 0.1, true), 0.18 + 0.25 * (t - sec(T.fixAt)) / (PEAK - sec(T.fixAt)), -0.2); t += step; step = Math.max(BEAT / 8, step * 0.86); } }

// PEAK (22.5 s, "Verified"): the open phrase finally resolves to high Sa, the logo rings in octaves.
put(DR, PEAK, impact(), 0.6); kicks.push([PEAK, 1]);
put(LD, PEAK, flute(note('S', 2), 1.6, { attack: 0.02, release: 0.8, glideFrom: note('D', 1) }), 0.13, 0);
sonicLogo(PEAK + BEAT, 0.9);
put(LD, PEAK, bell(note('S', 3), 2.6), 0.07, 0.2);

// 6 Report: three doors close, descending (Dha, Pa, Ga); a quiet bell when it is verified.
[[0, 'D'], [1, 'P'], [2, 'G']].forEach(([i, n]) => put(LD, sec(T.doorsAt + i * T.doorStagger), pluck(note(n, 1), 1.2, { bright: 0.7 }), 0.13, 0.2 - i * 0.2));
put(LD, sec(T.verifiedAt), bell(note('S', 2), 1.8), 0.05, 0);

// 7 CTA: the groove lands on a final hit and the full logo; the chord rings out to silence.
put(DR, END, impact(), 0.45); kicks.push([END, 1]);
sonicLogo(END, 1);
put(MU, END, pad(CHORDS[0], 1.6, { attack: 0.05, release: 1.4, cutoff: 0.07 }), 0.22);
put(MU, END, pluck(note('S', -1), 2.2, { decay: 0.998, bright: 0.4, buzz: 0.5 }), 0.2);

// ---- mix: duck the music bus under each kick (lift), add room, fade the final frames ----
const duck = new Float32Array(LEN).fill(1);
for (const [t, lv] of kicks) {
  const s0 = Math.round(t * SR);
  for (let i = 0; i < 0.3 * SR && s0 + i < LEN; i++) duck[s0 + i] = Math.min(duck[s0 + i], 1 - 0.38 * lv * Math.exp(-i / SR / 0.09));
}
function reverb(x, seedDelay) {
  const combs = [1557, 1617, 1491, 1422].map(d => ({ d: d + seedDelay, buf: new Float32Array(d + seedDelay), i: 0, lp: 0 }));
  const aps = [225, 556].map(d => ({ d, buf: new Float32Array(d), i: 0 }));
  const y = new Float32Array(x.length);
  for (let n = 0; n < x.length; n++) {
    let s = 0;
    for (const c of combs) { const o = c.buf[c.i]; c.lp = o * 0.8 + c.lp * 0.2; c.buf[c.i] = x[n] + c.lp * 0.8; c.i = (c.i + 1) % c.d; s += o; }
    s *= 0.25;
    for (const a of aps) { const o = a.buf[a.i]; const v = -0.5 * s + o; a.buf[a.i] = s + 0.5 * o; a.i = (a.i + 1) % a.d; s = v; }
    y[n] = s;
  }
  return y;
}
const L = new Float32Array(LEN), R = new Float32Array(LEN);
for (let i = 0; i < LEN; i++) { L[i] = DR.L[i] + MU.L[i] * duck[i] + LD.L[i]; R[i] = DR.R[i] + MU.R[i] * duck[i] + LD.R[i]; }
const sendL = new Float32Array(LEN), sendR = new Float32Array(LEN);
for (let i = 0; i < LEN; i++) { sendL[i] = LD.L[i] + MU.L[i] * 0.5; sendR[i] = LD.R[i] + MU.R[i] * 0.5; }
const wl = reverb(sendL, 0), wr = reverb(sendR, 23);
const tailStart = Math.round((sec(T.stillFrom) - 0.6) * SR);
let peak = 0;
for (let i = 0; i < LEN; i++) {
  const fade = i < tailStart ? 1 : Math.max(0, 1 - (i - tailStart) / (LEN - tailStart));
  const fadeIn = Math.min(1, i / (0.05 * SR));
  L[i] = Math.tanh((L[i] + wl[i] * 0.35) * 1.1) * fade * fadeIn;
  R[i] = Math.tanh((R[i] + wr[i] * 0.35) * 1.1) * fade * fadeIn;
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
