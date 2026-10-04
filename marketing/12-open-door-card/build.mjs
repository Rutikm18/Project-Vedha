// Open Door share card: a deployable page (index.html) + its 1200x630 social preview (og-image.png).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sealSvg } from '../shared/seal.js';
import { render } from '../shared/render.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const SITE = 'https://vedhasec.com';
const url = (src, med) => `${SITE}/?utm_source=${src}&utm_medium=${med}&utm_campaign=open_door`;

// Shared visual: the lattice with one open door (as in the film).
const lattice = (cols, rows, sp, gap) => {
  let s = '';
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    if (c >= gap.c0 && c <= gap.c1 && r >= gap.r0 && r <= gap.r1) continue;
    s += `<circle cx="${sp / 2 + c * sp}" cy="${sp / 2 + r * sp}" r="2.4"/>`;
  }
  const x0 = sp / 2 + (gap.c0 - 0.5) * sp, x1 = sp / 2 + (gap.c1 + 0.5) * sp, y = sp / 2 + (gap.r1 + 0.6) * sp;
  return `<svg class="lattice" viewBox="0 0 ${cols * sp} ${rows * sp}" aria-hidden="true"><g fill="rgba(243,246,250,.18)">${s}</g><line x1="${x0}" y1="${y}" x2="${x1}" y2="${y}" stroke="#60A5FA" stroke-width="3" stroke-linecap="round"/></svg>`;
};

// 1. Social preview image
const og = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
body{width:1200px;height:630px;background:var(--night);color:var(--day);font-family:var(--sans);position:relative;overflow:hidden}
.lattice{position:absolute;right:-20px;top:-10px;width:620px;opacity:1}
.t{position:absolute;left:72px;top:150px;width:620px}
h1{font-family:var(--serif);font-weight:400;font-size:84px;line-height:1.02}
p{font-size:32px;margin-top:26px;color:#DCE3EC}
.b{position:absolute;left:72px;top:56px;display:flex;gap:16px;align-items:center;font-family:var(--serif);font-size:44px}
.u{position:absolute;left:72px;bottom:56px;font-family:var(--mono);font-size:26px;color:var(--blue-night)}
</style></head><body>${lattice(16, 17, 40, { c0: 6, c1: 8, r0: 9, r1: 12 })}
<div class="b">${sealSvg('#60A5FA', 56)}Vedha</div>
<div class="t"><h1>Every office has one door nobody remembers.</h1><p>Find yours in 7 days, with the IT partner you already trust.</p></div>
<div class="u">vedhasec.com</div><script>window.ready=true</script></body></html>`;
fs.writeFileSync(path.join(DIR, 'og.html'), og);
await render(path.join(DIR, 'og.html'), 1200, 630, path.join(DIR, 'og-image.png'));

// 2. The share page (static, no trackers; only the UTM tags on outgoing links)
const shareText = 'Every office has one door nobody remembers. Vedha finds yours in 7 days, with the IT partner you already trust.';
const itMsg = `Hi, can we get our office network checked? Vedha does a 7-day network health check through IT partners: ${url('open_door', 'it_person')}`;
const page = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Find your open door · Vedha</title>
<meta name="description" content="${shareText}">
<meta property="og:title" content="Every office has one door nobody remembers.">
<meta property="og:description" content="Find yours in 7 days, with the IT partner you already trust.">
<meta property="og:image" content="${SITE}/open-door/og-image.png">
<meta property="og:url" content="${SITE}/open-door/">
<meta name="twitter:card" content="summary_large_image">
<style>
:root{--blue:#1D4ED8;--blue-night:#60A5FA;--night:#060B14;--day:#F3F6FA;--sans:"Geist Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--serif:"Instrument Serif",Georgia,serif}
*{box-sizing:border-box;margin:0}
body{background:var(--night);color:var(--day);font-family:var(--sans);min-height:100vh;display:flex;justify-content:center;padding:24px 16px}
main{max-width:520px;width:100%}
.brand{display:flex;gap:12px;align-items:center;font-family:var(--serif);font-size:28px}
.card{margin-top:28px;border:1px solid rgba(243,246,250,.14);border-radius:20px;overflow:hidden;background:#0B111C}
.card .lattice{display:block;width:100%;height:auto;background:var(--night)}
.card .txt{padding:22px}
h1{font-family:var(--serif);font-weight:400;font-size:40px;line-height:1.05}
.card p{margin-top:12px;color:#C5D0DE;font-size:17px;line-height:1.5}
.btns{display:grid;gap:12px;margin-top:22px}
button,a.btn{all:unset;box-sizing:border-box;text-align:center;padding:16px;border-radius:999px;font-weight:600;font-size:17px;cursor:pointer}
.primary{background:var(--blue);color:#fff}
a.btn.secondary{border:1.5px solid rgba(243,246,250,.5);color:var(--day)}
button:focus-visible,a.btn:focus-visible{outline:3px solid var(--blue-night);outline-offset:3px}
.alt{margin-top:14px;font-size:14px;color:#94A3B8;text-align:center}
.alt a{color:var(--blue-night)}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:var(--day);color:var(--night);padding:10px 16px;border-radius:999px;font-size:14px;opacity:0;transition:opacity .2s}
.toast.on{opacity:1}
.scope{margin-top:28px;color:#94A3B8;font-size:14px;text-align:center}
</style></head>
<body><main>
  <div class="brand">${sealSvg('#60A5FA', 36)}Vedha</div>
  <div class="card">
    ${lattice(13, 9, 40, { c0: 5, c1: 7, r0: 3, r1: 6 })}
    <div class="txt">
      <h1>Every office has one door nobody remembers.</h1>
      <p>A remote login left open. A file share anyone can open. A server the internet can see. Vedha's 7-day network health check finds them, proves them, and shows the fix worked.</p>
    </div>
  </div>
  <div class="btns">
    <button class="primary" id="share">Share</button>
    <a class="btn secondary" id="it" href="https://wa.me/?text=${encodeURIComponent(itMsg)}" target="_blank" rel="noopener">Send to my IT person</a>
  </div>
  <p class="alt">Or: <a id="mail" href="mailto:?subject=${encodeURIComponent('Can we check our office network?')}&body=${encodeURIComponent(itMsg)}">email it</a> · <a href="https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url('linkedin', 'share'))}" target="_blank" rel="noopener">LinkedIn</a> · <a href="#" id="copy">copy link</a></p>
  <p class="scope">For office networks. Not cloud networks. · <a href="${url('open_door', 'page')}" style="color:var(--blue-night)">vedhasec.com</a></p>
</main>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
const link = ${JSON.stringify(url('share', 'native'))}, text = ${JSON.stringify(shareText)};
const toast = m => { const t = document.getElementById('toast'); t.textContent = m; t.classList.add('on'); setTimeout(() => t.classList.remove('on'), 1800); };
const copy = async () => { try { await navigator.clipboard.writeText(text + ' ' + link); toast('Link copied'); } catch { prompt('Copy this link:', link); } };
document.getElementById('share').onclick = async () => {
  if (navigator.share) { try { await navigator.share({ title: 'Find your open door', text, url: link }); return; } catch (e) { if (e.name === 'AbortError') return; } }
  window.open('https://wa.me/?text=' + encodeURIComponent(text + ' ' + ${JSON.stringify(url('whatsapp', 'share'))}), '_blank', 'noopener');
};
document.getElementById('copy').onclick = e => { e.preventDefault(); copy(); };
</script></body></html>`;
fs.writeFileSync(path.join(DIR, 'index.html'), page);
await render(path.join(DIR, 'index.html'), 390, 844, path.join(DIR, 'preview-mobile.png'));
