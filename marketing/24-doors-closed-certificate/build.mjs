// #24 Doors Closed certificate (A4 landscape). Owner's name biggest. Teal = verified (its only allowed use).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sealSvg } from '../shared/seal.js';
import { renderPrint } from '../shared/render.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const c = JSON.parse(fs.readFileSync(path.join(DIR, 'certificate.json'), 'utf8'));
const check = `<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#0F766E"/><path d="M7 12.5l3.2 3.2L17 9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
let dots = ''; for (let y = 6; y < 210; y += 5.2) for (let x = 6; x < 297; x += 5.2) dots += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="0.45" fill="#DCE3EC"/>`;
fs.writeFileSync(path.join(DIR, 'cert.html'), `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
@page{size:297mm 210mm;margin:0}html,body{width:297mm;height:210mm}
body{background:#fff;color:#0F172A;font-family:var(--sans);position:relative;overflow:hidden}
.frame{position:absolute;inset:10mm;border:0.5mm solid #0F172A;border-radius:3mm;background:#fff}
.in{position:absolute;inset:22mm 26mm}
.k{font:500 9pt var(--mono);letter-spacing:.14em;color:#475569}
.owner{font:400 46pt/1 var(--serif);margin-top:9mm}
.biz{font-size:13pt;color:#475569;margin-top:3mm}
.title{display:flex;align-items:center;gap:3mm;margin-top:10mm;font:400 22pt var(--serif);color:#0F766E}
.lead{font-size:11pt;margin-top:2mm;color:#1E293B;max-width:200mm;line-height:1.5}
ul{list-style:none;padding:0;margin:6mm 0 0}li{display:flex;gap:3mm;align-items:flex-start;font-size:11.5pt;margin:2.6mm 0;line-height:1.35}
.meta{position:absolute;left:0;right:0;bottom:0;display:flex;justify-content:space-between;align-items:flex-end;font-size:9.5pt;color:#475569}
.meta b{display:block;color:#0F172A;font-weight:500;font-size:10.5pt}
.seal{display:flex;align-items:center;gap:3mm;font:400 20pt var(--serif);color:#0F172A}
.disc{position:absolute;left:26mm;right:26mm;bottom:13mm;font-size:7.4pt;color:#64748B}
</style></head><body><svg style="position:absolute;inset:0" width="297mm" height="210mm" viewBox="0 0 297 210">${dots}</svg>
<div class="frame"></div><div class="in">
<div class="k">CERTIFICATE OF DOORS CLOSED · REF ${c.reference}</div>
<div class="owner">${c.owner}</div>
<div class="biz">${c.business}</div>
<div class="title">${check}Doors closed and re-checked</div>
<div class="lead">During a 7-day network health check (${c.checkWindow}), these doors were found on the office network, fixed with ${c.partner}, and verified closed on re-check on ${c.verifiedOn}.</div>
<ul>${c.doors.map(d => `<li>${check}<span>${d}</span></li>`).join('')}</ul>
<div class="meta"><div><b>${c.partner}</b>IT partner</div><div><b>${c.verifiedOn}</b>Verified on re-check</div><div class="seal">${sealSvg('#1D4ED8', 44)}Vedha</div></div>
</div>
<div class="disc">This records the specific findings listed above and their re-check on the date shown, on the office network in scope. It is not a security certification, an audit or a guarantee, and it does not cover anything outside that scope.</div>
</body></html>`);
await renderPrint(path.join(DIR, 'cert.html'), 297, 210, { pdf: path.join(DIR, 'doors-closed-certificate.pdf'), png: path.join(DIR, 'preview.png'), dpi: 110 });
fs.rmSync(path.join(DIR, 'cert.html'));
