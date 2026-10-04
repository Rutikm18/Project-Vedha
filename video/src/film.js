// The film as a pure function of the frame number.
// renderFrame(ctx, frame, cfg) draws one frame; no wall-clock time, no Math.random().
// Same frame + same config = same pixels.
import { C, FONT, SEAL } from './brand.js';
import { T, SCENES, DURATION } from './timeline.js';
import { LAYOUTS } from './layouts.js';

// ---------- math ----------
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const prog = (f, at, dur) => clamp((f - at) / dur);

function bezier(x1, y1, x2, y2) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const sx = t => ((ax * t + bx) * t + cx) * t;
  const sy = t => ((ay * t + by) * t + cy) * t;
  const dx = t => (3 * ax * t + 2 * bx) * t + cx;
  return x => {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    let t = x;
    for (let i = 0; i < 8; i++) {
      const e = sx(t) - x, d = dx(t);
      if (Math.abs(e) < 1e-6) return sy(t);
      if (Math.abs(d) < 1e-6) break;
      t -= e / d;
    }
    let lo = 0, hi = 1; t = x;
    for (let i = 0; i < 30; i++) { const v = sx(t); if (v < x) lo = t; else hi = t; t = (lo + hi) / 2; }
    return sy(t);
  };
}
const easeOut = bezier(0.16, 1, 0.3, 1);            // ease-out-expo (brand --ease-out)
const easeInOut = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

function hex(c) { const n = parseInt(c.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
function mix(a, b, t) {
  const A = hex(a), B = hex(b);
  return `rgb(${A.map((v, i) => Math.round(lerp(v, B[i], t))).join(',')})`;
}
function lum(c) {
  const v = c.startsWith('rgb(') ? c.slice(4, -1).split(',').map(Number) : hex(c);
  const [r, g, b] = v.map(x => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
export function contrast(a, b) { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
function rgba(c, a) { const [r, g, b] = hex(c); return `rgba(${r},${g},${b},${a})`; }

function mulberry32(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ---------- world: lattice, devices, route, door (master 1080-wide coordinates) ----------
const COLS = 26, ROWS = 34, SP = 40, X0 = 40, Y0 = 15;
const node = (c, r) => [X0 + c * SP, Y0 + r * SP];
const DOOR = { c0: 4, c1: 6, r0: 19, r1: 22 };
const DOOR_C = node((DOOR.c0 + DOOR.c1) / 2, (DOOR.r0 + DOOR.r1) / 2);
const PULSE_DOT = [5, 21];

const DEVICES = [
  { id: 'REMOTE LOGIN', at: node(9, 14) },  // the way in (checkpoint 1)
  { id: 'FILE SERVER',  at: node(15, 9) },  // shares + a password never changed (2, 4)
  { id: 'ACCOUNTS',     at: node(21, 13) }, // the books (2)
  { id: 'BACKUPS',      at: node(21, 19) }, // the copy you recover from (3)
  { id: 'LAPTOPS',      at: node(4, 8) },
];
const dev = id => DEVICES.find(d => d.id === id).at;

// Edge -> door -> REMOTE LOGIN -> FILE SERVER -> ACCOUNTS -> BACKUPS, orthogonal along the lattice.
const ROUTE = [[-40, DOOR_C[1]], [dev('REMOTE LOGIN')[0], DOOR_C[1]], dev('REMOTE LOGIN'),
  [dev('FILE SERVER')[0], dev('REMOTE LOGIN')[1]], dev('FILE SERVER'),
  [dev('ACCOUNTS')[0], dev('FILE SERVER')[1]], dev('ACCOUNTS'), dev('BACKUPS')];
// The fix closes the remote login: the route snaps at the way in, the same door the hook opened.
const SNAP_IDX = 2;
const ROUTE_LEN = []; // cumulative
{ let L = 0; ROUTE_LEN.push(0); for (let i = 1; i < ROUTE.length; i++) { L += Math.hypot(ROUTE[i][0] - ROUTE[i - 1][0], ROUTE[i][1] - ROUTE[i - 1][1]); ROUTE_LEN.push(L); } }
const ROUTE_TOTAL = ROUTE_LEN[ROUTE_LEN.length - 1];
function routePoint(len) {
  len = clamp(len, 0, ROUTE_TOTAL);
  for (let i = 1; i < ROUTE.length; i++) {
    if (len <= ROUTE_LEN[i]) {
      const t = (len - ROUTE_LEN[i - 1]) / (ROUTE_LEN[i] - ROUTE_LEN[i - 1] || 1);
      return [lerp(ROUTE[i - 1][0], ROUTE[i][0], t), lerp(ROUTE[i - 1][1], ROUTE[i][1], t)];
    }
  }
  return ROUTE[ROUTE.length - 1];
}

// Contours: seeded value noise + marching squares, computed once.
const CONTOURS = (() => {
  const rnd = mulberry32(7);
  const G = 8, gw = 12, gh = 14;
  const grid = Array.from({ length: (gw + 1) * (gh + 1) }, () => rnd());
  const sm = t => t * t * (3 - 2 * t);
  const vn = (x, y) => {
    const gx = clamp(x / 1080 * gw, 0, gw - 1e-6), gy = clamp(y / 1350 * gh, 0, gh - 1e-6);
    const ix = Math.floor(gx), iy = Math.floor(gy), fx = sm(gx - ix), fy = sm(gy - iy);
    const v = (i, j) => grid[j * (gw + 1) + i];
    return lerp(lerp(v(ix, iy), v(ix + 1, iy), fx), lerp(v(ix, iy + 1), v(ix + 1, iy + 1), fx), fy);
  };
  const field = (x, y) => vn(x, y) * 0.75 + vn(x * 2.1 + 300, y * 2.1 + 170) * 0.25;
  const S = 24, nx = Math.ceil(1080 / S) + 1, ny = Math.ceil(1350 / S) + 1;
  const val = []; for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) val.push(field(i * S, j * S));
  const segs = [];
  for (const lvl of [0.32, 0.40, 0.48, 0.56, 0.64]) {
    for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
      const a = val[j * nx + i], b = val[j * nx + i + 1], c = val[(j + 1) * nx + i + 1], d = val[(j + 1) * nx + i];
      const x = i * S, y = j * S, p = [];
      const e = (v0, v1, x0, y0, x1, y1) => { const t = (lvl - v0) / (v1 - v0); p.push([lerp(x0, x1, t), lerp(y0, y1, t)]); };
      if ((a < lvl) !== (b < lvl)) e(a, b, x, y, x + S, y);
      if ((b < lvl) !== (c < lvl)) e(b, c, x + S, y, x + S, y + S);
      if ((c < lvl) !== (d < lvl)) e(c, d, x + S, y + S, x, y + S);
      if ((d < lvl) !== (a < lvl)) e(d, a, x, y + S, x, y);
      if (p.length >= 2) segs.push([p[0], p[1]]);
      if (p.length === 4) segs.push([p[2], p[3]]);
    }
  }
  return segs;
})();

// ---------- shared state of the story at frame f ----------
function story(f) {
  const wash = easeInOut(prog(f, T.washAt, T.washDur));
  const gapOpen = easeOut(prog(f, T.gapOpenAt, T.gapOpenDur));
  const heal = easeOut(prog(f, T.healAt, T.healDur));
  const gap = gapOpen * (1 - heal);
  // Pierce: radial displacement strength 0 -> 1 -> 0.35, relaxing to 0 in scene 4.
  let strength = 0;
  if (f >= T.displaceAt) {
    const a = prog(f, T.displaceAt, 6), b = prog(f, T.displaceAt + 6, T.displaceDur - 6);
    strength = f < T.displaceAt + 6 ? easeOut(a) : lerp(1, 0.35, easeOut(b));
    strength *= 1 - easeInOut(prog(f, T.partnerAt, 30));
  }
  const routeDraw = easeInOut(prog(f, T.routeAt, T.routeDur));
  const snap = easeOut(prog(f, T.snapAt, 10));
  // Text ink never interpolates (that would pass through zero contrast mid-wash):
  // each frame uses whichever of Day/Night text contrasts more with the current background.
  const bg = mix(C.night, C.day, wash);
  const ink = contrast(C.day, bg) >= contrast(C.night, bg) ? C.day : C.night;
  return { wash, gap, heal, strength, routeDraw, snap, teal: f >= T.tealAt, ink, bg };
}

// Map camera: push-ins in scenes 1-2, hold, zoom out in scene 4.
function camera(f) {
  if (f < 90) return lerp(1.0, 1.04, easeInOut(f / 90));
  if (f < 270) return lerp(1.04, 1.12, easeInOut((f - 90) / 180));
  if (f < T.partnerAt) return 1.12;
  return lerp(1.12, 1.0, easeInOut(prog(f, T.partnerAt, 30)));
}
const PIVOT = [540, 620];
// Each layout places the 1080x1350 map world on its canvas: screen = world.xy + p * world.s.
const toWorldScreen = (L, [x, y]) => [L.world.x + x * L.world.s, L.world.y + y * L.world.s];
const fromScreen = (L, [x, y]) => [(x - L.world.x) / L.world.s, (y - L.world.y) / L.world.s];

// ---------- drawing primitives ----------
function rrect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
}
function text(ctx, s, x, y, { font, color, alpha = 1, align = 'left', dy = 0, halo = null }) {
  if (alpha <= 0) return;
  ctx.save(); ctx.globalAlpha *= alpha; ctx.font = font; ctx.fillStyle = color;
  ctx.textAlign = align; ctx.textBaseline = 'alphabetic';
  if (halo) { ctx.save(); ctx.globalAlpha *= halo.alpha; ctx.strokeStyle = halo.color; ctx.lineWidth = halo.width; ctx.lineJoin = 'round'; ctx.strokeText(s, x, y + dy); ctx.restore(); }
  ctx.fillText(s, x, y + dy); ctx.restore();
}
function wrap(ctx, s, font, maxW) {
  ctx.save(); ctx.font = font;
  const words = s.split(' '), lines = []; let cur = '';
  for (const w of words) { const t = cur ? cur + ' ' + w : w; if (ctx.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t; }
  if (cur) lines.push(cur); ctx.restore(); return lines;
}
// Entrance: 10 frames, ease-out-expo, 16 px rise; exit: 6-frame fade, no movement.
function life(f, from, to, dur = 10) {
  const p = easeOut(prog(f, from, dur));
  const out = to == null ? 1 : 1 - prog(f, to - 6, 6);
  return { a: p * out, dy: (1 - p) * 16 };
}

function sealPath(notch, eye) {
  const ny = 6 + 18 * notch;
  const body = SEAL.body.replace('L50 24L', `L50 ${ny.toFixed(3)}L`);
  if (eye <= 0.001) return new Path2D(body);
  const k = 32 * eye;
  return new Path2D(`${body}M18 53Q50 ${53 - k} 82 53Q50 ${53 + k} 18 53Z`);
}
// The seal from the repo SVG; notch/eye animate open, pupil looks at (lx, ly) in -1..1.
function drawSeal(ctx, cx, cy, size, { notch = 1, eye = 1, pupil = 1, look = [0, 0], color, pupilColor, alpha = 1 }) {
  if (alpha <= 0) return;
  ctx.save(); ctx.globalAlpha *= alpha;
  ctx.translate(cx - size / 2, cy - size / 2); ctx.scale(size / 100, size / 100);
  ctx.fillStyle = color; ctx.fill(sealPath(notch, eye), 'evenodd');
  if (eye > 0.001 && pupil > 0) {
    const k = 32 * eye;
    ctx.save(); ctx.clip(new Path2D(`M18 53Q50 ${53 - k} 82 53Q50 ${53 + k} 18 53Z`));
    ctx.beginPath();
    ctx.arc(SEAL.pupil.cx + look[0] * 14, SEAL.pupil.cy + look[1] * 5, SEAL.pupil.r * pupil, 0, Math.PI * 2);
    ctx.fillStyle = pupilColor || color; ctx.fill(); ctx.restore();
  }
  ctx.restore();
}

function checkIcon(ctx, x, y, s, color, lw = 3) {
  ctx.save(); ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.beginPath(); ctx.moveTo(x - s * 0.45, y); ctx.lineTo(x - s * 0.1, y + s * 0.35); ctx.lineTo(x + s * 0.5, y - s * 0.35); ctx.stroke(); ctx.restore();
}
function chip(ctx, x, y, label, color, { check = false, alpha = 1, fontPx = 26 } = {}) {
  if (alpha <= 0) return;
  ctx.save(); ctx.globalAlpha *= alpha; ctx.font = `500 ${fontPx}px ${FONT.ui}`;
  const pad = 16, iw = check ? fontPx + 6 : 0, w = ctx.measureText(label).width + pad * 2 + iw, h = fontPx + 20;
  rrect(ctx, x, y, w, h, h / 2); ctx.fillStyle = rgba(color, 0.12); ctx.fill();
  ctx.strokeStyle = rgba(color, 0.5); ctx.lineWidth = 1.5; ctx.stroke();
  if (check) checkIcon(ctx, x + pad + fontPx * 0.4, y + h / 2, fontPx * 0.7, color);
  ctx.fillStyle = color; ctx.textBaseline = 'middle'; ctx.fillText(label, x + pad + iw, y + h / 2 + 1);
  ctx.restore(); return w;
}

// ---------- the map (lattice + contours + devices + route), reused full-frame and in the console ----------
function drawMap(ctx, f, S, { alpha = 1, mini = false, copy, pierce = [540, 560] }) {
  if (alpha <= 0) return;
  ctx.save(); ctx.globalAlpha *= alpha;
  const dotCol = S.wash > 0 ? mix('#F3F6FA', '#060B14', S.wash) : C.day;
  const dotA = lerp(0.18, 0.14, S.wash);
  const night = S.wash < 0.5;
  const blue = night ? C.blueOnNight : C.blue;
  const center = [540, 675], maxD = Math.hypot(540, 675);
  const displace = (x, y) => {
    if (S.strength <= 0 || mini) return [x, y];
    const dx = x - pierce[0], dy = y - pierce[1], d = Math.hypot(dx, dy) || 1, sg = 220;
    const o = 60 * S.strength * Math.exp(-((d / sg) ** 2));
    return [x + dx / d * o, y + dy / d * o];
  };

  // contours
  const cA = mini ? 0.6 : easeOut(prog(f, T.contoursAt, 20));
  if (cA > 0) {
    ctx.save(); ctx.strokeStyle = rgba(night ? C.day : C.night, 0.10 * cA); ctx.lineWidth = 1.25;
    ctx.beginPath();
    for (const [[x1, y1], [x2, y2]] of CONTOURS) { const a = displace(x1, y1), b = displace(x2, y2); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); }
    ctx.stroke(); ctx.restore();
  }

  // lattice
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
    let [x, y] = node(c, r);
    const delay = mini ? -99 : T.bloomFrom + Math.hypot(x - center[0], y - center[1]) / maxD * 20;
    const p = easeOut(prog(f, delay, 10));
    if (p <= 0) continue;
    let a = dotA * p, rad = 2.5 * (0.4 + 0.6 * p);
    const inGap = c >= DOOR.c0 && c <= DOOR.c1 && r >= DOOR.r0 && r <= DOOR.r1;
    if (inGap) { a *= 1 - S.gap; x += (c - 5) * 10 * S.gap; }
    [x, y] = displace(x, y);
    ctx.beginPath(); ctx.arc(x, y, rad, 0, Math.PI * 2); ctx.fillStyle = rgba(night ? C.day : C.night, a); ctx.fill();
  }
  // door sill under the gap
  if (S.gap > 0.01) {
    const [x0] = node(DOOR.c0 - 0.5, 0), [x1] = node(DOOR.c1 + 0.5, 0), [, ys] = node(0, DOOR.r1 + 0.6);
    ctx.save(); ctx.globalAlpha *= S.gap; ctx.strokeStyle = blue; ctx.lineWidth = 2.5; ctx.lineCap = 'round';
    ctx.shadowColor = rgba(C.blue, 0.35); ctx.shadowBlur = 10;
    ctx.beginPath(); ctx.moveTo(x0, ys); ctx.lineTo(x1, ys); ctx.stroke(); ctx.restore();
  }
  // the one dot that pulses blue in the hook
  if (!mini && f >= T.pulseAt && f < T.pulseAt + T.pulseDur) {
    const t = (f - T.pulseAt) / T.pulseDur, [x, y] = node(...PULSE_DOT);
    ctx.beginPath(); ctx.arc(x, y, 2.5 + 7 * Math.sin(t * Math.PI), 0, Math.PI * 2);
    ctx.fillStyle = rgba(C.blueOnNight, 0.9 * Math.sin(t * Math.PI)); ctx.fill();
  }

  // devices
  const devA = mini ? 1 : easeOut(prog(f, T.devicesAt, 12));
  if (devA > 0) {
    DEVICES.forEach(({ id, at }, i) => {
      const a = mini ? 1 : easeOut(prog(f, T.devicesAt + i * 3, 10));
      const [x, y] = displace(at[0], at[1]);
      const lit = { 'REMOTE LOGIN': T.item1At, 'BACKUPS': T.item3At, 'ACCOUNTS': T.routeAt + T.routeDur - 6 }[id];
      const hl = lit == null ? 0 : mini ? 1 : easeOut(prog(f, lit, 10));
      ctx.save(); ctx.globalAlpha *= a;
      rrect(ctx, x - 22, y - 22, 44, 44, 10); ctx.fillStyle = S.bg; ctx.fill();
      ctx.lineWidth = 2; ctx.strokeStyle = hl > 0 ? mix(night ? '#F3F6FA' : '#060B14', blue, hl) : rgba(night ? C.day : C.night, 0.55); ctx.stroke();
      if (id === 'FILE SERVER') { // key glyph: the password never changed
        const k = mini ? 1 : easeOut(prog(f, T.item2At, 10));
        if (k > 0) { // key glyph
          ctx.save(); ctx.globalAlpha *= k; ctx.strokeStyle = blue; ctx.lineWidth = 2.5;
          ctx.beginPath(); ctx.arc(x + 34, y - 30, 7, 0, Math.PI * 2); ctx.moveTo(x + 41, y - 30); ctx.lineTo(x + 60, y - 30); ctx.moveTo(x + 54, y - 30); ctx.lineTo(x + 54, y - 23); ctx.stroke(); ctx.restore();
        }
      }
      ctx.restore();
    });
  }

  // route
  const drawn = (mini ? 1 : S.routeDraw) * ROUTE_TOTAL;
  if (drawn > 0) {
    const cut = ROUTE_LEN[SNAP_IDX];
    const stroke = (from, to, a) => {
      if (to <= from || a <= 0) return;
      ctx.beginPath(); const p0 = displace(...routePoint(from)); ctx.moveTo(...p0);
      for (let i = 1; i < ROUTE.length; i++) if (ROUTE_LEN[i] > from && ROUTE_LEN[i] < to) ctx.lineTo(...displace(...ROUTE[i]));
      ctx.lineTo(...displace(...routePoint(to)));
      ctx.save(); ctx.globalAlpha *= a; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
      ctx.shadowColor = rgba(C.blue, 0.35); ctx.shadowBlur = 10; ctx.strokeStyle = blue; ctx.lineWidth = 3; ctx.stroke(); ctx.restore();
    };
    stroke(0, Math.min(drawn, cut - 18 * S.snap), 1);
    stroke(cut + 18 * S.snap, drawn, 1 - S.snap * 0.85);
  }

  // device labels on top of the route, each on a small backing in the page colour
  if (devA > 0) DEVICES.forEach(({ id, at }, i) => {
    const a = mini ? 1 : easeOut(prog(f, T.devicesAt + i * 3, 10));
    const [x, y] = displace(at[0], at[1]);
    ctx.save(); ctx.globalAlpha *= a; ctx.font = `500 28px ${FONT.mono}`;
    const w = ctx.measureText(id).width;
    rrect(ctx, x - w / 2 - 8, y + 30, w + 16, 36, 6); ctx.fillStyle = S.bg; ctx.fill(); ctx.restore();
    text(ctx, id, x, y + 56, { font: `500 28px ${FONT.mono}`, color: night ? C.day : C.night, alpha: 0.78 * a, align: 'center' });
  });
  ctx.restore();
}

// ---------- captions ----------
function caption(ctx, L, f, s, from, to, color) {
  const { a, dy } = life(f, from, to);
  if (a <= 0) return;
  const font = `500 ${L.capPx}px ${FONT.ui}`;
  // Too long for one line? Break at sentence ends first, so "With proof." never splits.
  let lines = wrap(ctx, s, font, L.capMaxW);
  const sentences = s.match(/[^.]+\.(\s|$)/g);
  if (lines.length > 1 && sentences && sentences.length > 1) lines = sentences.flatMap(t => wrap(ctx, t.trim(), font, L.capMaxW));
  // Mid-wash the background passes through grey: a halo in the opposite ink keeps captions >= 4.5:1.
  const w = story(f).wash, halo = w > 0 && w < 1 ? { color: color === C.day ? C.night : C.day, width: 8, alpha: Math.sin(w * Math.PI) } : null;
  lines.forEach((ln, i) => text(ctx, ln, L.capX, L.capBase - (lines.length - 1 - i) * L.capLH, { font, color, alpha: a, dy, halo }));
}

// ---------- scenes ----------
function sceneHook(ctx, f, S, L, copy) {
  const font = `400 ${copy.hookPx || L.hookPx}px ${FONT.display}`;
  const lines = copy.hook.split('\n').flatMap(t => wrap(ctx, t, font, L.hookMaxW));
  let w = 0; const out = 1 - prog(f, 84, 6);
  ctx.save(); ctx.font = font;
  lines.forEach((ln, li) => {
    let x = L.hookX; const y = L.hookY + li * L.hookLH;
    for (const word of ln.split(' ')) {
      const { a, dy } = life(f, T.hookTextAt + w * T.hookWordStagger, null);
      text(ctx, word, x, y, { font, color: C.day, alpha: a * out, dy });
      x += ctx.measureText(word + ' ').width; w++;
    }
  });
  ctx.restore();
}

function scenePath(ctx, f, S, L, copy) {
  const font = `500 ${L.capPx}px ${FONT.ui}`;
  const starts = [T.item1At, T.item2At, T.item3At];
  copy.list.forEach((s, i) => {
    const { a, dy } = life(f, starts[i], T.routeAt);
    text(ctx, s, L.capX, L.listBase + i * L.capLH, { font, color: C.day, alpha: a, dy });
  });
  caption(ctx, L, f, copy.path, T.routeAt, 270, C.day);
}

function scenePierceAndPartner(ctx, f, S, L, copy) {
  const s3in = easeOut(prog(f, T.sealAt, T.sealScaleDur));
  const toChecks = easeInOut(prog(f, T.checksAt, 18));
  const toPartner = easeInOut(prog(f, T.partnerAt, 24));
  const toConsole = easeInOut(prog(f, T.consoleAt, 12));
  if (toConsole >= 1) return;
  const at3 = (a, b, c) => lerp(lerp(a, b, toChecks), c, toPartner);
  const cx = at3(L.sealX, L.checkSealX, L.partnerSealX), cy = at3(L.sealY, L.checkSealY, L.partnerSealY);
  const size = at3(L.sealSize, L.checkSealSize, L.partnerSealSize) * lerp(0.85, 1, s3in);
  const notch = easeOut(prog(f, T.strikeAt, T.strikeDur));
  let eye = easeOut(prog(f, T.eyeAt, T.eyeDur));
  if (f >= T.blinkAt && f < T.blinkAt + T.blinkDur) eye *= Math.abs(Math.cos((f - T.blinkAt) / T.blinkDur * Math.PI));
  const pupil = easeOut(prog(f, T.pupilAt, 8));
  // pupil follows a comet that runs back along the route to the door (4-frame lag), then locks.
  const z = camera(f), toScreen = ([x, y]) => toWorldScreen(L, [PIVOT[0] + (x - PIVOT[0]) * z, PIVOT[1] + (y - PIVOT[1]) * z]);
  const cometAt = ff => routePoint(ROUTE_TOTAL * (1 - easeInOut(prog(ff, T.pupilAt, T.pupilLockAt - T.pupilAt))));
  let target = toScreen(cometAt(f - 4));
  if (f >= T.checksAt) target = [L.checkX + 40, L.checkY + 3 * L.checkLH];
  if (f >= T.partnerAt + 10) target = L.partnerNode;
  const dx = target[0] - cx, dy = target[1] - cy, d = Math.hypot(dx, dy) || 1;
  const look = [dx / d * Math.min(1, d / 300), dy / d * Math.min(1, d / 300)];
  // comet
  if (f >= T.pupilAt && f < T.pupilLockAt + 8) {
    const [x, y] = toScreen(cometAt(f)), a = 1 - prog(f, T.pupilLockAt, 8);
    const g = ctx.createRadialGradient(x, y, 0, x, y, 22); g.addColorStop(0, rgba(C.blueOnNight, 0.9 * a)); g.addColorStop(1, rgba(C.blueOnNight, 0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, 22, 0, Math.PI * 2); ctx.fill();
  }
  const alpha = s3in * (1 - toConsole);
  drawSeal(ctx, cx, cy, size, { notch, eye, pupil, look, color: C.blueOnNight, alpha });

  // name block
  const nOut = 1 - prog(f, T.checksAt - 6, 6);
  const nm = life(f, T.nameAt, null), dv = life(f, T.devaAt, null), gl = life(f, T.glossAt, null);
  text(ctx, copy.name, L.nameX, L.nameBase, { font: `400 ${L.namePx}px ${FONT.display}`, color: C.day, alpha: nm.a * nOut, dy: nm.dy, align: 'center' });
  ctx.save(); ctx.font = `400 ${L.devaPx}px ${FONT.deva}`; const dw = ctx.measureText(copy.devanagari).width;
  ctx.font = `500 ${L.glossPx}px ${FONT.mono}`; const gw = ctx.measureText(copy.gloss).width; ctx.restore();
  const gx = L.nameX - (dw + 28 + gw) / 2;
  text(ctx, copy.devanagari, gx, L.devaBase, { font: `400 ${L.devaPx}px ${FONT.deva}`, color: C.day, alpha: dv.a * nOut, dy: dv.dy });
  text(ctx, copy.gloss, gx + dw + 28, L.devaBase - 14, { font: `500 ${L.glossPx}px ${FONT.mono}`, color: C.day, alpha: 0.8 * gl.a * nOut, dy: gl.dy });
  caption(ctx, L, f, copy.what, T.whatAt, T.checksAt, C.day);

  // 3b: the checkpoints, numbered, one every 6 frames (examined, not yet verified: blue, never teal)
  if (f >= T.checksAt && f < T.partnerAt) {
    caption(ctx, L, f, copy.checks, T.checksAt + 3, T.partnerAt, C.day);
    copy.checkpoints.forEach((label, i) => {
      const { a, dy } = life(f, T.checkItemsAt + i * T.checkStagger, T.partnerAt);
      const y = L.checkY + i * L.checkLH;
      text(ctx, String(i + 1).padStart(2, '0'), L.checkX, y, { font: `500 30px ${FONT.mono}`, color: C.blueOnNight, alpha: a, dy });
      text(ctx, label, L.checkX + 64, y, { font: `500 ${L.checkPx}px ${FONT.ui}`, color: C.day, alpha: a, dy });
    });
  }

  // partner
  if (f >= T.partnerAt) {
    const a = easeOut(prog(f, T.partnerAt, 10)) * (1 - toConsole);
    const [px, py] = L.partnerNode;
    const pulse = 0.5 + 0.5 * Math.sin(prog(f, T.partnerAt + 10, 40) * Math.PI * 2);
    ctx.save(); ctx.globalAlpha *= a;
    ctx.beginPath(); ctx.arc(px, py, 34 + 10 * pulse, 0, Math.PI * 2); ctx.strokeStyle = rgba(C.blueOnNight, 0.25 * (1 - pulse)); ctx.lineWidth = 2; ctx.stroke();
    rrect(ctx, px - 26, py - 26, 52, 52, 12); ctx.fillStyle = C.night; ctx.fill(); ctx.strokeStyle = C.blueOnNight; ctx.lineWidth = 2.5; ctx.stroke();
    text(ctx, copy.partnerNodeLabel, px, py + 66, { font: `500 28px ${FONT.mono}`, color: C.day, alpha: 0.85, align: 'center' });
    // line node -> seal (24-frame draw)
    const lp = easeInOut(prog(f, T.partnerLineAt, T.partnerLineDur));
    const sx = cx + size * 0.5 + 12, sy = cy;
    const pts = [[px, py - 26], [px, sy], [sx, sy]];
    const L1 = Math.abs(py - 26 - sy), L2 = Math.abs(px - sx), tot = (L1 + L2) * lp;
    ctx.beginPath(); ctx.moveTo(...pts[0]);
    if (tot <= L1) ctx.lineTo(px, py - 26 - tot); else { ctx.lineTo(...pts[1]); ctx.lineTo(px - (tot - L1), sy); }
    ctx.strokeStyle = rgba(C.day, 0.6); ctx.lineWidth = 1.5; ctx.stroke();
    ctx.restore();
    caption(ctx, L, f, copy.partner, T.partnerAt + 4, T.consoleAt, C.day);
  }
}

function sceneConsole(ctx, f, S, L, copy, cfg) {
  const rise = easeOut(prog(f, T.consoleAt, 12));
  const out = 1 - easeInOut(prog(f, T.ctaAt, 8));
  if (rise <= 0 || out <= 0) return;
  const x = 0, y = 0, w = 920, h = 830;
  const dy = (1 - rise) * 60;
  const panelBg = mix('#161820', C.panel, S.wash);
  const ink = contrast('#F1F5F9', panelBg) >= contrast(C.textPrimary, panelBg) ? '#F1F5F9' : C.textPrimary;
  const sub = contrast('#94A3B8', panelBg) >= contrast(C.textSecondary, panelBg) ? '#94A3B8' : C.textSecondary;
  const blue = S.wash < 0.5 ? C.blueOnNight : C.blue;
  ctx.save(); ctx.globalAlpha *= rise * out;
  ctx.translate(L.console.x, L.console.y); ctx.scale(L.console.s, L.console.s); ctx.translate(0, dy);
  // gentle 2% drift
  const drift = 1 + 0.02 * easeInOut(prog(f, T.consoleAt, 240));
  ctx.translate(x + w / 2, y + h / 2); ctx.scale(drift, drift); ctx.translate(-(x + w / 2), -(y + h / 2));
  rrect(ctx, x, y, w, h, 22); ctx.fillStyle = panelBg; ctx.fill();
  ctx.strokeStyle = mix('#2A2F3C', C.border, S.wash); ctx.lineWidth = 1.5; ctx.stroke();

  // header: grade seal + grade
  const tealCol = S.wash < 0.5 ? C.tealOnNight : C.teal;
  drawSeal(ctx, x + 64, y + 62, 64, { color: blue, pupilColor: S.teal ? tealCol : blue });
  text(ctx, copy.name, x + 108, y + 74, { font: `400 40px ${FONT.display}`, color: ink });
  const g = easeOut(prog(f, T.gradeAt, 10));
  text(ctx, copy.ui.gradeLabel, x + w - 150, y + 52, { font: `500 22px ${FONT.mono}`, color: sub, align: 'right' });
  text(ctx, 'C', x + w - 64, y + 84, { font: `600 56px ${FONT.ui}`, color: mix('#FBBF24', '#A16207', S.wash), alpha: 1 - g, align: 'center' });
  text(ctx, 'B', x + w - 64, y + 84, { font: `600 56px ${FONT.ui}`, color: tealCol, alpha: g, align: 'center', dy: (1 - g) * 10 });

  // tabs
  const tab = f < T.attackAt ? 1 : f < T.reportAt ? 2 : 3;
  ctx.save(); ctx.font = `500 26px ${FONT.ui}`; let tx = x + 40;
  copy.ui.tabs.forEach((t, i) => {
    const tw = ctx.measureText(t).width;
    text(ctx, t, tx, y + 162, { font: `500 26px ${FONT.ui}`, color: i === tab ? ink : sub });
    if (i === tab) { ctx.fillStyle = blue; ctx.fillRect(tx, y + 178, tw, 3); }
    tx += tw + 40;
  });
  ctx.restore();
  ctx.fillStyle = mix('#2A2F3C', C.border, S.wash); ctx.fillRect(x, y + 181, w, 1.5);

  const bx = x + 40, by = y + 220, bw = w - 80;
  const fFind = 1 - prog(f, T.attackAt - 4, 6);
  const fAtk = prog(f, T.attackAt, 8) * (1 - prog(f, T.reportAt, 6));
  const fRep = prog(f, T.reportAt + 4, 8);

  // Findings
  if (fFind > 0) {
    ctx.save(); ctx.globalAlpha *= fFind;
    const n = Math.min(3, Math.floor(prog(f, T.findingsAt + 8, 24) * 3.999));
    text(ctx, String(n), bx, by + 90, { font: `400 110px ${FONT.display}`, color: ink });
    text(ctx, copy.ui.findingsTitle, bx + 80, by + 84, { font: `500 26px ${FONT.mono}`, color: sub });
    const rows = cfg.findings;
    rows.forEach((r, i) => {
      const { a, dy } = life(f, T.findingsAt + 8 + i * 8, null);
      const ry = by + 140 + i * 140;
      ctx.save(); ctx.globalAlpha *= a; ctx.translate(0, dy);
      rrect(ctx, bx, ry, bw, 124, 14); ctx.fillStyle = mix('#1C1F28', '#F8FAFC', S.wash); ctx.fill();
      ctx.save(); let tp = 32; ctx.font = `500 ${tp}px ${FONT.ui}`; while (tp > 22 && ctx.measureText(r.title).width > bw - 170) ctx.font = `500 ${--tp}px ${FONT.ui}`; ctx.restore();
      text(ctx, r.title, bx + 28, ry + 54, { font: `500 ${tp}px ${FONT.ui}`, color: ink });
      text(ctx, r.host, bx + 28, ry + 96, { font: `400 24px ${FONT.mono}`, color: sub });
      text(ctx, r.sev, bx + bw - 28, ry + 54, { font: `500 22px ${FONT.mono}`, color: sub, align: 'right' });
      ctx.restore();
    });
    ctx.restore();
  }

  // Attack use case: the map, inset, with the Proven chip; then the fix.
  if (fAtk > 0) {
    ctx.save(); ctx.globalAlpha *= fAtk;
    const mx = bx, my = by, mw = bw, mh = 470;
    rrect(ctx, mx, my, mw, mh, 14); ctx.fillStyle = mix('#0B111C', '#F8FAFC', S.wash); ctx.fill();
    ctx.save(); rrect(ctx, mx, my, mw, mh, 14); ctx.clip();
    const k = mh / 720, ox = (1080 - mw / k) / 2; // map window y 230..950 holds devices + door
    ctx.translate(mx, my); ctx.scale(k, k); ctx.translate(-ox, -230);
    drawMap(ctx, f, S, { mini: true, copy });
    ctx.restore();
    const proven = life(f, T.attackAt + 10, null);
    const chipX = mx + mw - 200, chipY = my + 20;
    chip(ctx, chipX, chipY, copy.chips.proven, blue, { alpha: proven.a * (1 - prog(f, T.snapAt, 6)) });
    chip(ctx, chipX, chipY, copy.chips.verified, tealCol, { check: true, alpha: easeOut(prog(f, T.tealAt, 8)) });

    // fix row
    const ry = my + mh + 30;
    const fx = life(f, T.fixAt, null);
    ctx.save(); ctx.globalAlpha *= fx.a; ctx.translate(0, fx.dy);
    rrect(ctx, bx, ry, 40, 40, 8); ctx.strokeStyle = sub; ctx.lineWidth = 2; ctx.stroke();
    const tick = easeOut(prog(f, T.tickAt, 8));
    if (tick > 0) { ctx.save(); ctx.globalAlpha *= tick; rrect(ctx, bx, ry, 40, 40, 8); ctx.fillStyle = blue; ctx.fill(); checkIcon(ctx, bx + 20, ry + 20, 24, '#FFFFFF'); ctx.restore(); }
    text(ctx, cfg.fixItem, bx + 60, ry + 30, { font: `500 28px ${FONT.ui}`, color: ink });
    // hold-to-verify ring
    const hx = bx + bw - 44, hy = ry + 20, hp = prog(f, T.holdAt, T.holdDur);
    ctx.beginPath(); ctx.arc(hx, hy, 30, 0, Math.PI * 2); ctx.strokeStyle = rgba(S.wash < 0.5 ? C.day : C.night, 0.2); ctx.lineWidth = 5; ctx.stroke();
    if (hp > 0) { ctx.beginPath(); ctx.arc(hx, hy, 30, -Math.PI / 2, -Math.PI / 2 + hp * Math.PI * 2); ctx.strokeStyle = f >= T.tealAt ? tealCol : blue; ctx.stroke(); }
    if (f >= T.tealAt) checkIcon(ctx, hx, hy, 26, tealCol, 4);
    text(ctx, copy.ui.holdToVerify, hx - 50, hy + 9, { font: `500 24px ${FONT.ui}`, color: sub, align: 'right' });
    ctx.restore();
    ctx.restore();
  }

  // Report
  if (fRep > 0) {
    ctx.save(); ctx.globalAlpha *= fRep;
    text(ctx, copy.ui.reportTitle, bx, by + 50, { font: `400 52px ${FONT.display}`, color: ink });
    cfg.findings.forEach((r, i) => {
      const ry = by + 110 + i * 130;
      const regen = life(f, T.reportAt + 4 + i * 3, null);
      ctx.save(); ctx.globalAlpha *= regen.a;
      rrect(ctx, bx, ry, bw, 106, 14); ctx.fillStyle = mix('#1C1F28', '#F8FAFC', S.wash); ctx.fill();
      // door icon: frame + a leaf that swings shut (outline, no fill)
      const c = easeOut(prog(f, T.doorsAt + i * T.doorStagger, 10));
      const dx0 = bx + 30, dy0 = ry + 24, lw = 40 * lerp(0.3, 1, c), sk = lerp(8, 0, c);
      ctx.save(); ctx.strokeStyle = ink; ctx.lineWidth = 2.5; ctx.lineJoin = 'round';
      ctx.strokeRect(dx0, dy0, 40, 58);
      ctx.beginPath(); ctx.moveTo(dx0, dy0); ctx.lineTo(dx0 + lw, dy0 + sk); ctx.lineTo(dx0 + lw, dy0 + 58 - sk); ctx.lineTo(dx0, dy0 + 58); ctx.closePath();
      ctx.fillStyle = mix('#1C1F28', '#F8FAFC', S.wash); ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(dx0 + lw - 8, dy0 + 31, 2.5, 0, Math.PI * 2); ctx.fillStyle = ink; ctx.fill();
      ctx.restore();
      text(ctx, r.closed, bx + 100, ry + 64, { font: `500 30px ${FONT.ui}`, color: ink });
      ctx.restore();
    });
    const v = life(f, T.verifiedAt, null);
    ctx.save(); ctx.globalAlpha *= v.a;
    const vy = by + 520;
    ctx.beginPath(); ctx.arc(bx + 22, vy - 10, 22, 0, Math.PI * 2); ctx.fillStyle = rgba(C.teal, 0.12); ctx.fill();
    checkIcon(ctx, bx + 22, vy - 10, 24, C.teal, 4);
    text(ctx, copy.ui.verifiedOn, bx + 60, vy, { font: `500 32px ${FONT.ui}`, color: C.teal });
    ctx.restore();
    ctx.restore();
  }
  ctx.restore();

  // captions + illustrative tag (outside the drifting frame; text never moves while read)
  const capCol = S.ink;
  caption(ctx, L, f, copy.find, T.findingsAt + 4, T.attackAt, capCol);
  caption(ctx, L, f, copy.prove, T.attackAt, T.fixAt, capCol);
  caption(ctx, L, f, copy.fix, T.fixAt, T.reportAt, capCol);
  caption(ctx, L, f, copy.report, T.reportAt, T.ctaAt, capCol);
  const tw = S.wash, tagHalo = tw > 0 && tw < 1 ? { color: capCol === C.day ? C.night : C.day, width: 6, alpha: Math.sin(tw * Math.PI) } : null;
  text(ctx, copy.illustrative, L.capX, L.tagBase, { font: `500 34px ${FONT.ui}`, color: capCol, alpha: 0.6 * rise * out, halo: tagHalo });
}

function sceneCTA(ctx, f, S, L, copy) {
  if (f < T.ctaAt) return;
  const st = i => life(f, T.ctaAt + 6 + i * T.ctaStagger, null, 12);
  const a0 = st(0), a1 = st(1), a2 = st(2), a3 = st(3), a4 = st(4);
  drawSeal(ctx, L.ctaSealX, L.ctaSealY + a0.dy, L.ctaSealSize, { color: C.blue, alpha: a0.a });
  text(ctx, copy.name, L.cx, L.ctaNameBase, { font: `400 ${L.ctaNamePx}px ${FONT.display}`, color: C.night, alpha: a1.a, dy: a1.dy, align: 'center' });
  const b = L.ctaBtn;
  ctx.save(); ctx.globalAlpha *= a2.a; ctx.translate(0, a2.dy);
  rrect(ctx, b.x, b.y, b.w, b.h, b.h / 2); ctx.fillStyle = C.blue; ctx.fill();
  text(ctx, copy.cta, L.cx, b.y + b.h / 2 + 17, { font: `500 ${L.ctaBtnPx}px ${FONT.ui}`, color: '#FFFFFF', align: 'center' });
  ctx.restore();
  text(ctx, copy.url, L.cx, L.ctaUrlBase, { font: `500 ${L.ctaUrlPx}px ${FONT.ui}`, color: C.night, alpha: a3.a, dy: a3.dy, align: 'center' });
  text(ctx, copy.scope, L.cx, L.ctaScopeBase, { font: `400 ${L.ctaScopePx}px ${FONT.ui}`, color: C.textSecondary, alpha: a4.a, dy: a4.dy, align: 'center' });
}

// ---------- animatic overlay ----------
function overlay(ctx, f, L, S) {
  const sc = SCENES.find(s => f >= s.from && f < s.to) || SCENES[SCENES.length - 1];
  const tc = `${String(Math.floor(f / 30)).padStart(2, '0')}:${String(f % 30).padStart(2, '0')}`;
  ctx.save();
  ctx.setLineDash([8, 8]); ctx.strokeStyle = 'rgba(255,80,160,.55)'; ctx.lineWidth = 2;
  ctx.strokeRect(...L.safeRect);
    ctx.setLineDash([]);
  ctx.fillStyle = 'rgba(255,80,160,.9)'; ctx.font = `500 24px ${FONT.mono}`; ctx.textAlign = 'right';
  ctx.fillText(`ANIMATIC · ${sc.name.toUpperCase()} · ${tc} · F${String(f).padStart(3, '0')}`, L.W - 24, 36);
  ctx.restore();
}

// ---------- entry ----------
export const storyAt = f => story(f);
export function renderFrame(ctx, frame, cfg) {
  const f = clamp(Math.round(frame), 0, DURATION - 1);
  const L = LAYOUTS[cfg.aspect];
  const copy = cfg.copy;
  const S = story(f);
  ctx.save();
  ctx.setTransform(cfg.width / L.W, 0, 0, cfg.height / L.H, 0, 0);
  ctx.fillStyle = S.bg; ctx.fillRect(0, 0, L.W, L.H);

  // map layer, under the camera
  const mapA = f < T.sealAt ? 1
    : f < T.checksAt ? lerp(1, 0.3, easeOut(prog(f, T.sealAt, 12)))
    : f < T.partnerAt ? lerp(0.3, 0.06, easeOut(prog(f, T.checksAt, 12)))
    : f < T.consoleAt ? lerp(0.06, 0.5, easeOut(prog(f, T.partnerAt, 20)))
    : lerp(0.5, 0.35, easeOut(prog(f, T.consoleAt, 12))) * (1 - prog(f, T.ctaAt, 8));
  ctx.save();
  const z = camera(f);
  ctx.translate(L.world.x, L.world.y); ctx.scale(L.world.s, L.world.s);
  ctx.translate(PIVOT[0], PIVOT[1]); ctx.scale(z, z); ctx.translate(-PIVOT[0], -PIVOT[1]);
  drawMap(ctx, f, S, { alpha: mapA, copy, pierce: fromScreen(L, [L.sealX, L.sealY]) });
  ctx.restore();

  if (f < 90) sceneHook(ctx, f, S, L, copy);
  if (f >= 90 && f < 270) scenePath(ctx, f, S, L, copy);
  if (f >= T.sealAt && f < T.consoleAt + 12) scenePierceAndPartner(ctx, f, S, L, copy);
  if (f >= T.consoleAt) sceneConsole(ctx, f, S, L, copy, cfg);
  sceneCTA(ctx, f, S, L, copy);

  if (cfg.debug) overlay(ctx, f, L, S);
  ctx.restore();
}

// Poster / thumbnail: the hook frame (door open, line fully read) plus the seal and the URL.
export function renderPoster(ctx, cfg) {
  const L = LAYOUTS[cfg.aspect];
  renderFrame(ctx, 80, { ...cfg, debug: false });
  ctx.save();
  ctx.setTransform(cfg.width / L.W, 0, 0, cfg.height / L.H, 0, 0);
  const sz = Math.round(L.W * 0.13), [sx, sy, sw] = L.safeRect;
  drawSeal(ctx, sx + sw - sz / 2, sy + sz / 2, sz, { color: C.blueOnNight });
  text(ctx, cfg.copy.url, L.capX, L.capBase, { font: `500 ${L.capPx * 0.75}px ${FONT.ui}`, color: C.day, alpha: 0.85 });
  ctx.restore();
}
