// #15 "CERT-In's 15 controls, accurately": web guide (index.html) + one-page A4 PDF, both generated
// from 13-certin-controls/mapping.csv so the public claims can never drift from the verified mapping.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sealSvg } from '../shared/seal.js';
import { renderPrint } from '../shared/render.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));

// Minimal CSV parser (quoted fields).
const parse = t => { const rows = []; let r = [], f = '', q = false;
  for (let i = 0; i < t.length; i++) { const c = t[i];
    if (q) { if (c === '"' && t[i + 1] === '"') { f += '"'; i++; } else if (c === '"') q = false; else f += c; }
    else if (c === '"') q = true; else if (c === ',') { r.push(f); f = ''; } else if (c === '\n') { r.push(f); rows.push(r); r = []; f = ''; } else if (c !== '\r') f += c; }
  if (f || r.length) { r.push(f); rows.push(r); } return rows; };
const [, ...rows] = parse(fs.readFileSync(path.join(DIR, '../13-certin-controls/mapping.csv'), 'utf8')).filter(r => r.length > 2);

// Public wording. "NOT OFFERED" is shown simply as not covered by Vedha's check (no internal reasons published).
// Drawn icons (font glyphs like the half-circle are missing from the brand fonts). Shape + words, never colour alone.
const ic = k => `<svg width="11" height="11" viewBox="0 0 12 12" aria-hidden="true" style="vertical-align:-1px;margin-right:6px">${
  k === 'ev' ? '<circle cx="6" cy="6" r="5" fill="#1D4ED8"/>'
  : k === 'pa' ? '<circle cx="6" cy="6" r="4.4" fill="none" stroke="#1D4ED8" stroke-width="1.3"/><path d="M6 1.6A4.4 4.4 0 0 1 6 10.4Z" fill="#1D4ED8"/>'
  : '<circle cx="6" cy="6" r="4.4" fill="none" stroke="#8EA0B5" stroke-width="1.3"/>'}</svg>`;
const NOT = 'Not in Vedha’s check';
const LEVEL = {
  EVIDENCE: { label: 'Network evidence', icon: ic('ev'), cls: 'ev' },
  PARTIAL: { label: 'Partly', icon: ic('pa'), cls: 'pa' },
  'NOT OFFERED': { label: NOT, icon: ic('no'), cls: 'no' },
  'NOT COVERED': { label: NOT, icon: ic('no'), cls: 'no' },
};
const PLAIN = { // owner-readable "what Vedha shows" per control (from the mapping, simplified)
  1: 'Every device it can see on the office network, what it is, and which ports are open.',
  2: 'Services reachable on the network and from outside, plus risky network settings. Email filtering is not checked.',
  3: '—', 4: 'Risky settings on file sharing, remote desktop, encryption and similar services.', 5: '—', 6: '—', 7: '—', 8: '—', 9: '—',
  10: 'Shared folders or databases anyone on the network can read. Backups are not checked.',
  11: 'A dated, evidence-backed report and re-check you can put in your audit file.',
  12: '—', 13: 'Remote logins and anonymous access visible on the network. User accounts and MFA are not checked.', 14: '—',
  15: 'A network vulnerability assessment with evidence and a re-check after fixes. It is evidence for the auditor, not the audit.',
};
const name = r => r[1].replace(/\s*\[order to verify\]/, '');
const counts = rows.reduce((a, r) => (a[LEVEL[r[2]].cls]++, a), { ev: 0, pa: 0, no: 0 });

const css = `
:root{--blue:#1D4ED8;--night:#060B14;--day:#F3F6FA;--ink:#0F172A;--ink2:#475569;--line:#DCE3EC}
body{font-family:var(--sans);color:var(--ink);background:#fff}
h1,h2{font-family:var(--serif);font-weight:400}
table{border-collapse:collapse;width:100%}
th{font:500 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink2);text-align:left;border-bottom:1.5px solid var(--ink)}
td{border-bottom:1px solid var(--line);vertical-align:top}
.lv{white-space:nowrap;font-weight:500}.lv i{font-style:normal;margin-right:6px}
.ev i{color:var(--blue)}.pa i{color:var(--blue)}.no{color:var(--ink2)}.no i{color:#8EA0B5}
.note{color:var(--ink2)}`;

// ---------- one-page PDF (A4) ----------
const pdfRows = rows.map(r => `<tr><td class="n">${r[0]}</td><td>${name(r)}</td><td class="lv ${LEVEL[r[2]].cls}">${LEVEL[r[2]].icon}${LEVEL[r[2]].label}</td><td class="note">${PLAIN[+r[0]]}</td></tr>`).join('');
fs.writeFileSync(path.join(DIR, 'onepager.html'), `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
@page{size:210mm 297mm;margin:0}${css}
html,body{width:210mm;height:297mm}body{padding:13mm 14mm;box-sizing:border-box;font-size:8.7pt}
.top{display:flex;justify-content:space-between;align-items:center}.brand{display:flex;gap:8px;align-items:center;font:400 17pt var(--serif)}
h1{font-size:22pt;line-height:1.05;margin:7mm 0 2.5mm}.sub{font-size:9.6pt;color:var(--ink2);max-width:165mm;line-height:1.45}
.sum{display:flex;gap:5mm;margin:4.5mm 0 3.5mm}.sum div{border:1px solid var(--line);border-radius:6px;padding:2.2mm 3.5mm;flex:1;font-size:8.4pt}.sum b{font:400 17pt var(--serif);display:block}
td{padding:1.25mm 2mm;line-height:1.3}td.n{font-family:var(--mono);color:var(--ink2);width:7mm}th{padding:2mm}
.foot{position:absolute;left:14mm;right:14mm;bottom:9mm;font-size:7.6pt;color:var(--ink2);line-height:1.45;border-top:1px solid var(--line);padding-top:3mm}
</style></head><body>
<div class="top"><div class="brand">${sealSvg('#1D4ED8', 30)}Vedha</div><div style="font:500 8pt var(--mono);color:var(--ink2)">VEDHASEC.COM · INFO@VEDHASEC.COM</div></div>
<h1>CERT-In's 15 controls for MSMEs,<br>and what a Vedha check gives you evidence for</h1>
<div class="sub">CERT-In's guideline CISG-2025-03 (1 Sep 2025) sets 15 elemental controls with 45 recommendations for MSMEs, and asks for a baseline audit by a <b>CERT-In empanelled auditor</b>. Vedha's 7-day network health check is not that audit. It gives you and your auditor network evidence for some controls. This page says exactly which.</div>
<div class="sum"><div><b>${counts.ev}</b>controls with network evidence</div><div><b>${counts.pa}</b>controls partly</div><div><b>${counts.no}</b>controls not in Vedha's check: your IT partner or auditor covers these</div></div>
<table><thead><tr><th>#</th><th>Control</th><th>Vedha</th><th>What the check shows</th></tr></thead><tbody>${pdfRows}</tbody></table>
<div class="foot">Not legal advice and not a compliance attestation. Vedha is not a CERT-In empanelled auditor and does not certify anyone. Control names are from public summaries of CISG-2025-03; check the official PDF at cert-in.org.in. Office networks only, not cloud. Version 1 · October 2026.</div>
</body></html>`);
await renderPrint(path.join(DIR, 'onepager.html'), 210, 297, { pdf: path.join(DIR, 'certin-15-controls-onepager.pdf'), png: path.join(DIR, 'onepager-preview.png'), dpi: 110 });
fs.rmSync(path.join(DIR, 'onepager.html'));

// ---------- web guide ----------
const webRows = rows.map(r => `<tr><td>${r[0]}</td><td>${name(r)}</td><td class="lv ${LEVEL[r[2]].cls}">${LEVEL[r[2]].icon}${LEVEL[r[2]].label}</td><td class="note">${PLAIN[+r[0]]}</td></tr>`).join('');
fs.writeFileSync(path.join(DIR, 'index.html'), `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CERT-In's 15 controls for MSMEs, accurately · Vedha</title>
<meta name="description" content="What CERT-In's 15 elemental controls for MSMEs ask for, and exactly which ones a Vedha network check gives evidence for. No overclaiming.">
<style>:root{--sans:"Geist Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--serif:"Instrument Serif",Georgia,serif;--mono:"Geist Mono",ui-monospace,monospace}${css}
body{margin:0;padding:0 16px;line-height:1.6}main{max-width:760px;margin:0 auto;padding:40px 0 80px}
h1{font-size:clamp(34px,6vw,52px);line-height:1.05;margin:24px 0 12px}h2{font-size:30px;margin:44px 0 8px}
p,li{font-size:17px}.lead{font-size:19px;color:var(--ink2)}
.tablewrap{overflow-x:auto}td,th{padding:10px 8px}td:first-child{font-family:var(--mono);color:var(--ink2)}
.cta{display:inline-block;margin-top:16px;background:var(--blue);color:#fff;text-decoration:none;padding:14px 22px;border-radius:999px;font-weight:600}
.cta:focus-visible{outline:3px solid #60A5FA;outline-offset:3px}.small{font-size:14px;color:var(--ink2)}
@media (max-width:560px){td.note{display:none}}
</style></head><body><main>
<a href="https://vedhasec.com" style="display:flex;gap:10px;align-items:center;color:inherit;text-decoration:none;font:400 24px var(--serif)">${sealSvg('#1D4ED8', 32)}Vedha</a>
<h1>CERT-In's 15 controls for MSMEs, accurately</h1>
<p class="lead">In September 2025 CERT-In published 15 "elemental" cyber defence controls for MSMEs. Here's what they are, what they ask for, and exactly which ones a Vedha check gives you evidence for, including the ones it doesn't.</p>

<h2>What CERT-In published</h2>
<ul><li><b>CISG-2025-03</b>, dated 1 September 2025: <i>15 Elemental Cyber Defense Controls for MSMEs</i>.</li>
<li>15 controls, broken into 45 baseline recommendations.</li>
<li>It asks MSMEs to have a <b>baseline audit by a CERT-In empanelled auditing organisation</b> against these controls. Read the exact wording in the official PDF on cert-in.org.in.</li></ul>

<h2>The 15 controls, and what Vedha shows</h2>
<p>Vedha gives <b>network evidence for ${counts.ev}</b> controls and <b>part of ${counts.pa} more</b>. The other ${counts.no} need other work, and that's normal: no single tool covers all 15.</p>
<div class="tablewrap"><table><thead><tr><th>#</th><th>Control</th><th>Vedha</th><th class="note">What the check shows</th></tr></thead><tbody>${webRows}</tbody></table></div>
<p class="small">${ic('ev')}network evidence · ${ic('pa')}partly · ${ic('no')}not in Vedha's check. The icon and the words always say the same thing.</p>

<h2>What this means for you</h2>
<ol><li><b>A Vedha check is not the CERT-In audit.</b> Only an empanelled auditor can do that. Vedha gives you and your auditor evidence: what's on the network, what's open, the proof, and a re-check after fixes.</li>
<li><b>Start where the risk is visible.</b> Asset management, configurations and vulnerability assessment are where a network check gives the most, fastest.</li>
<li><b>Plan the rest with your IT partner.</b> Training, incident response, logging, backups, passwords, patching and physical security need their own work.</li></ol>

<h2>Common questions</h2>
<p><b>Does Vedha make us CERT-In compliant?</b><br>No. Nobody honest can promise that from a network check. Vedha gives evidence for some controls; an empanelled auditor assesses all of them.</p>
<p><b>Does it cover cloud, email or laptops away from the office?</b><br>No. Office networks only.</p>
<p><b>Who does the check?</b><br>Your IT partner, using Vedha, over 7 days.</p>
<a class="cta" href="https://vedhasec.com/?utm_source=guide&utm_medium=web&utm_campaign=certin_15">Book your 7-day check</a>
<p class="small" style="margin-top:32px">Not legal advice and not a compliance attestation. Vedha is not a CERT-In empanelled auditor. Control names are from public summaries of CISG-2025-03; the official PDF is the authority. Version 1, October 2026. <a href="certin-15-controls-onepager.pdf">Download the one-page PDF</a>.</p>
</main></body></html>`);
console.log('counts', counts);
