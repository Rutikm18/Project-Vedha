// Vedha visiting-card system: founder + partner cards, two sizes, print PDFs with bleed + 300 dpi previews.
// Design rationale and print spec: DESIGN.md. Data: people.json.
//   node cards/build.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import QRCode from 'qrcode';
import { sealSvg } from '../shared/seal.js';
import { renderPrint } from '../shared/render.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'out');
const BLEED = 3;                       // mm, every edge
const SAFE = 5;                        // mm inside trim: all text and the logo stay inside this
const SIZES = { '89x51': [89, 51], '90x55': [90, 55] };   // 3.5 x 2 in, and the common Indian 90 x 55
const { people } = JSON.parse(fs.readFileSync(path.join(DIR, 'people.json'), 'utf8'));

// Brand tokens (screen). Print values in DESIGN.md.
const T = { night: '#060B14', day: '#F3F6FA', paper: '#FFFFFF', blue: '#1D4ED8', blueNight: '#60A5FA',
  ink: '#0F172A', ink2: '#475569', dotDay: '#C5D0DE', dotNight: '#1C2330', nightText: '#F3F6FA', nightText2: '#C5D0DE' };

// The pulli-style lattice from the film. `gap` removes a door (3 x 4 dots) and draws its blue sill.
function lattice(wMm, hMm, { pitch = 2.6, r = 0.3, color, x0 = 0, y0 = 0, gap = null, sill = T.blueNight, fade = null }) {
  let dots = '';
  const cols = Math.floor((wMm - x0) / pitch), rows = Math.floor((hMm - y0) / pitch);
  for (let j = 0; j <= rows; j++) for (let i = 0; i <= cols; i++) {
    if (gap && i >= gap.c && i < gap.c + 3 && j >= gap.r && j < gap.r + 4) continue;
    const x = x0 + i * pitch, y = y0 + j * pitch;
    const op = fade ? Math.max(0, Math.min(1, (x - fade[0]) / (fade[1] - fade[0]))) : 1;
    if (op <= 0.02) continue;
    dots += `<circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="${r}" fill="${color}" opacity="${op.toFixed(2)}"/>`;
  }
  let s = '';
  if (gap) {
    const xa = x0 + (gap.c - 0.5) * pitch, xb = x0 + (gap.c + 2.5) * pitch, yy = y0 + (gap.r + 3.6) * pitch;
    s = `<line x1="${xa}" y1="${yy}" x2="${xb}" y2="${yy}" stroke="${sill}" stroke-width="0.35" stroke-linecap="round"/>`;
  }
  return `<svg width="${wMm}mm" height="${hMm}mm" viewBox="0 0 ${wMm} ${hMm}" style="position:absolute;left:0;top:0">${dots}${s}</svg>`;
}

// Lean vCard: only what "save contact" needs. Fewer characters = a lower QR version = bigger modules,
// which matters at 20 mm (the full vCard was version 10 with 0.35 mm modules and failed decode tests).
const vcard = p => ['BEGIN:VCARD', 'VERSION:3.0', `N:${p.name}`, `FN:${p.name}`, 'ORG:Vedha',
  `TEL:${p.phone.replace(/\s+/g, '')}`, `EMAIL:${p.email}`, 'END:VCARD'].join('\n');
const bookUrl = p => `https://vedhasec.com/?utm_source=partner&utm_medium=card&utm_campaign=partner_card&utm_content=${encodeURIComponent(p.slug)}`;

function page(wMm, hMm, body, { bg, guides }) {
  const W = wMm + 2 * BLEED, H = hMm + 2 * BLEED;
  const g = guides ? `<div class="g trim"></div><div class="g safe"></div>` : '';
  return `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
@page { size: ${W}mm ${H}mm; margin: 0 }
html, body { width: ${W}mm; height: ${H}mm; }
body { background: ${bg}; position: relative; overflow: hidden; }
.trim { position: absolute; left: ${BLEED}mm; top: ${BLEED}mm; width: ${wMm}mm; height: ${hMm}mm; }
.a { position: absolute; }
.g { position: absolute; pointer-events: none; z-index: 9 }
.g.trim { border: 0.2mm dashed #E11D48; }
.g.safe { left: ${BLEED + SAFE}mm; top: ${BLEED + SAFE}mm; width: ${wMm - 2 * SAFE}mm; height: ${hMm - 2 * SAFE}mm; border: 0.2mm dotted #F59E0B; }
</style></head><body>${body(W, H)}${g}</body></html>`;
}

// FRONT (Day): who. Name first, then role, then how to reach. Lattice complete: the "after" (doors closed).
function front(p, wMm, hMm, guides) {
  const isPartner = p.type === 'partner';
  return page(wMm, hMm, (W, H) => `
  ${lattice(W, H, { color: T.dotDay, x0: 1.3, y0: 1.3, fade: [BLEED + 46, BLEED + wMm - 4] })}
  <div class="trim">
    ${isPartner
      ? `<div class="a" style="left:${SAFE}mm;top:${SAFE}mm;font:500 10.5pt var(--sans);color:${T.ink}">${p.firm}</div>`
      : `<div class="a" style="left:${SAFE}mm;top:${SAFE - 0.4}mm;display:flex;align-items:center;gap:1.6mm">${sealSvg(T.blue, 25)}<span style="font:400 12pt var(--serif);color:${T.ink}">Vedha</span></div>`}
    <div class="a" style="left:${SAFE}mm;top:${hMm * 0.36}mm;width:${wMm * 0.62}mm">
      <div style="font:400 17pt/1.05 var(--serif);color:${T.ink}">${p.name}</div>
      <div style="margin-top:1.4mm;font:500 7pt var(--mono);letter-spacing:.08em;text-transform:uppercase;color:${T.ink2}">${p.role}</div>
    </div>
    <div class="a" style="left:${SAFE}mm;bottom:${SAFE}mm;font:400 8pt/1.5 var(--sans);color:${T.ink}">
      <div><span style="display:inline-block;width:4.2mm;font:500 7pt var(--mono);color:${T.ink2}">M</span>${p.phone}</div>
      <div><span style="display:inline-block;width:4.2mm;font:500 7pt var(--mono);color:${T.ink2}">E</span>${p.email}</div>
      <div><span style="display:inline-block;width:4.2mm;font:500 7pt var(--mono);color:${T.ink2}">W</span>vedhasec.com</div>
    </div>
    ${isPartner ? `<div class="a" style="right:${SAFE}mm;bottom:${SAFE}mm;display:flex;align-items:center;gap:1.2mm">
      <span style="font:500 7pt var(--mono);letter-spacing:.06em;color:${T.ink2}">CHECKS BY</span>${sealSvg(T.blue, 16)}<span style="font:400 10pt var(--serif);color:${T.ink}">Vedha</span></div>` : ''}
  </div>`, { bg: T.paper, guides });
}

// BACK (Night): the brand moment. Seal, name in two scripts, the promise, one action (the QR).
async function back(p, wMm, hMm, guides) {
  const isPartner = p.type === 'partner';
  const data = isPartner ? bookUrl(p) : vcard(p);
  const qr = await QRCode.toString(data, { type: 'svg', margin: 0, errorCorrectionLevel: 'M', color: { dark: '#060B14', light: '#FFFFFF' } });
  const tile = 24, qrMm = 20;            // 20 mm code (business-card minimum), 2 mm white quiet zone each side
  return page(wMm, hMm, (W, H) => `
  ${lattice(W, H, { color: T.dotNight, x0: 1.3, y0: 1.3 })}
  <div class="trim">
    <div class="a" style="left:${SAFE}mm;top:${SAFE}mm">${sealSvg(T.blueNight, 50)}</div>
    <div class="a" style="left:${SAFE}mm;top:${SAFE + 15}mm;display:flex;align-items:baseline;gap:2.4mm">
      <span style="font:400 22pt/1 var(--serif);color:${T.nightText}">Vedha</span>
      <span style="font:400 13pt/1 var(--serif);color:${T.nightText2}">वेधा</span>
    </div>
    <div class="a" style="left:${SAFE}mm;bottom:${SAFE}mm;font:500 9pt/1.35 var(--sans);color:${T.nightText}">
      <div>Find what's open.</div><div>Prove what's real.</div><div>Show the fix worked.</div>
    </div>
    <div class="a" style="right:${SAFE}mm;top:${SAFE}mm;width:${tile}mm;text-align:center">
      <div style="width:${tile}mm;height:${tile}mm;background:#fff;border-radius:1.6mm;display:flex;align-items:center;justify-content:center">
        <div style="width:${qrMm}mm;height:${qrMm}mm">${qr.replace('<svg', `<svg width="${qrMm}mm" height="${qrMm}mm"`)}</div>
      </div>
      <div style="margin-top:1.6mm;font:500 8pt var(--sans);color:${T.nightText2};white-space:nowrap">${isPartner ? 'Book a check' : 'Save contact'}</div>
    </div>
    <div class="a" style="right:${SAFE}mm;bottom:${SAFE}mm;font:500 8pt var(--mono);color:${T.nightText}">vedhasec.com</div>
  </div>`, { bg: T.night, guides });
}

fs.mkdirSync(OUT, { recursive: true });
const made = [];
for (const [sizeName, [w, h]] of Object.entries(SIZES)) {
  for (const p of people) {
    for (const side of ['front', 'back']) {
      for (const guides of [false, true]) {
        const html = side === 'front' ? front(p, w, h, guides) : await back(p, w, h, guides);
        const base = `${p.slug}_${sizeName}_${side}${guides ? '_guides' : ''}`;
        const file = path.join(OUT, `${base}.html`);
        fs.writeFileSync(file, html);
        await renderPrint(file, w + 2 * BLEED, h + 2 * BLEED, guides ? { png: path.join(OUT, `${base}.png`) } : { pdf: path.join(OUT, `${base}.pdf`), png: path.join(OUT, `${base}.png`) });
        fs.rmSync(file);
        made.push(base);
      }
    }
  }
}
console.log(`rendered ${made.length} files to cards/out/`);
