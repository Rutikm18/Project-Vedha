// #19 Jugaad & Sons, Diwali Safai edition: 10 cards (1080x1350) with code-drawn illustrations + a contact sheet.
// Fictional business, real doors: every item is something Vedha's network check finds (see README.md).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sealSvg } from '../shared/seal.js';
import { render } from '../shared/render.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const items = JSON.parse(fs.readFileSync(path.join(DIR, 'items.json'), 'utf8'));
const INK = '#0F172A', BLUE = '#1D4ED8', SOFT = '#DCE3EC';
const s = `fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"`;
const b = `fill="none" stroke="${BLUE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"`;
// Line illustrations, 400x320 viewBox, ink with one blue accent (the "door" in each).
const ICON = {
  monitor: `<rect x="70" y="40" width="260" height="170" rx="14" ${s}/><path d="M170 210v40M120 260h160" ${s}/><rect x="175" y="80" width="50" height="90" rx="4" ${b}/><path d="M175 80l-24 12v90l24-12" ${b}/><circle cx="212" cy="128" r="4" fill="${BLUE}"/>`,
  folder: `<path d="M60 90h100l25 25h155v150H60z" ${s}/><rect x="170" y="150" width="60" height="48" rx="6" ${b}/><path d="M182 150v-20a18 18 0 0 1 36 0" ${b} transform="translate(22 0) rotate(-25 200 130)"/>`,
  camera: `<path d="M90 90h170l40 40-40 40H90z" ${s}/><circle cx="270" cy="130" r="14" ${s}/><path d="M150 170v70M110 240h80" ${s}/><path d="M300 70c30 20 30 100 0 120M325 50c45 30 45 140 0 160" ${b}/>`,
  router: `<rect x="70" y="150" width="260" height="80" rx="14" ${s}/><path d="M120 150V80M280 150V80" ${s}/><circle cx="120" cy="190" r="7" fill="${INK}"/><circle cx="150" cy="190" r="7" fill="${INK}"/><path d="M230 175h50v30h-50z" ${b}/><path d="M255 175l-15-15" ${b}/>`,
  database: `<ellipse cx="200" cy="80" rx="110" ry="32" ${s}/><path d="M90 80v150c0 18 50 32 110 32s110-14 110-32V80" ${s}/><path d="M90 155c0 18 50 32 110 32s110-14 110-32" ${s}/><path d="M250 130l40-40M290 90h-25M290 90v25" ${b}/>`,
  server: `<rect x="130" y="40" width="140" height="230" rx="12" ${s}/><path d="M155 90h90M155 130h90M155 170h90" ${s}/><circle cx="240" cy="230" r="9" fill="${BLUE}"/><path d="M60 270h280" ${s}/><path d="M85 270l25-50h30" ${s}/>`,
  upload: `<path d="M80 230v40h240v-40" ${s}/><path d="M200 220V70M150 120l50-50 50 50" ${s}/><rect x="235" y="150" width="70" height="56" rx="6" ${b}/><path d="M248 150v-22a22 22 0 0 1 44 0" ${b} transform="rotate(-25 270 140)"/>`,
  printer: `<rect x="70" y="120" width="260" height="110" rx="14" ${s}/><path d="M120 120V60h160v60M120 230v40h160v-40" ${s}/><rect x="250" y="145" width="50" height="34" rx="4" ${b}/><path d="M262 162h26" ${b}/>`,
  unknown: `<rect x="60" y="120" width="80" height="80" rx="10" ${s}/><rect x="160" y="100" width="80" height="120" rx="10" ${s}/><rect x="260" y="130" width="80" height="70" rx="10" ${b}/><path d="M287 152a13 13 0 1 1 18 12c-5 2-5 6-5 10" ${b}/><circle cx="300" cy="186" r="4" fill="${BLUE}"/>`,
  wifi: `<path d="M80 130c70-60 170-60 240 0M115 165c45-40 125-40 170 0M150 200c25-22 75-22 100 0" ${s}/><circle cx="200" cy="232" r="10" fill="${INK}"/><path d="M90 270h220" ${b}/>`,
};
// Background: the film's dot lattice, with a door-shaped gap behind the illustration's accent.
const lattice = () => { let d = ''; for (let y = 20; y < 560; y += 34) for (let x = 20; x < 1080; x += 34) d += `<circle cx="${x}" cy="${y}" r="2.6" fill="${SOFT}"/>`; return d; };

const card = (it, i) => `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
body{width:1080px;height:1350px;background:#FFFFFF;color:${INK};font-family:var(--sans);position:relative;overflow:hidden}
.k{position:absolute;left:80px;top:72px;font:500 26px var(--mono);letter-spacing:.08em;color:${BLUE}}
h1{position:absolute;left:80px;right:80px;top:120px;font:400 66px/1.05 var(--serif)}
.art{position:absolute;left:0;right:0;top:330px;height:540px}
.art svg.l{position:absolute;inset:0}
.art svg.i{position:absolute;left:290px;top:40px;width:500px;height:400px}
.story{position:absolute;left:80px;right:80px;top:850px;font:400 32px/1.42 var(--sans);color:#1E293B}
.fix{position:absolute;left:80px;right:80px;top:1035px;border:3px solid ${BLUE};border-radius:22px;padding:24px 30px;font:500 30px/1.38 var(--sans)}
.fix span{display:block;font:500 22px var(--mono);letter-spacing:.08em;color:${BLUE};margin-bottom:6px}
.f{position:absolute;left:80px;right:80px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font:500 22px var(--mono);color:#475569}
.f .b{display:flex;gap:12px;align-items:center;font:400 32px var(--serif);color:${INK}}
</style></head><body>
<div class="k">JUGAAD &amp; SONS · DIWALI SAFAI ${i + 1}/10</div>
<h1>${it.title}</h1>
<div class="art"><svg class="l" viewBox="0 0 1080 540">${lattice()}</svg><svg class="i" viewBox="0 0 400 320">${ICON[it.icon]}</svg></div>
<div class="story">${it.story}</div>
<div class="fix"><span>THE FIX</span>${it.fix}</div>
<div class="f"><div class="b">${sealSvg('#1D4ED8', 40)}Vedha</div><div>FICTIONAL BUSINESS · REAL DOORS · VEDHASEC.COM</div></div>
<script>window.ready=true</script></body></html>`;

const OUT = path.join(DIR, 'cards'); fs.mkdirSync(OUT, { recursive: true });
for (const [i, it] of items.entries()) {
  const f = path.join(DIR, `c${i}.html`); fs.writeFileSync(f, card(it, i));
  await render(f, 1080, 1350, path.join(OUT, `jugaad_${String(i + 1).padStart(2, '0')}.png`)); fs.rmSync(f);
}
