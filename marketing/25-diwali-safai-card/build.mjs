// #25 Diwali Safai card, English + Hindi, partner-branded (1080x1350). No religious imagery (brand guardrail).
//   PARTNER="Sharma IT Services" node 25-diwali-safai-card/build.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sealSvg } from '../shared/seal.js';
import { render } from '../shared/render.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const partner = process.env.PARTNER || '[Partner firm name]';
const COPY = {
  en: { k: 'DIWALI SAFAI · OFFICE NETWORK', h: 'This Diwali, close the doors nobody remembers.',
    items: ['Remote logins left open', 'Folders anyone can open', 'Devices nobody can name'],
    cta: `Book a 7-day network health check with ${partner}`, by: 'CHECKS BY' },
  hi: { k: 'दिवाली सफ़ाई · ऑफ़िस नेटवर्क', h: 'इस दिवाली, वे दरवाज़े बंद करें जिन्हें कोई याद नहीं रखता।',
    items: ['खुले छोड़े गए रिमोट लॉगिन', 'ऐसे फ़ोल्डर जिन्हें कोई भी खोल सकता है', 'ऐसे डिवाइस जिन्हें कोई पहचानता नहीं'],
    cta: `${partner} के साथ 7-दिन का नेटवर्क हेल्थ चेक बुक करें`, by: 'CHECKS BY' },
};
let dots = ''; for (let y = 24; y < 1350; y += 36) for (let x = 24; x < 1080; x += 36) dots += `<circle cx="${x}" cy="${y}" r="2.6" fill="rgba(243,246,250,.13)"/>`;
for (const [lang, c] of Object.entries(COPY)) {
  const html = `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
body{width:1080px;height:1350px;background:#060B14;color:#F3F6FA;font-family:var(--sans);position:relative;overflow:hidden}
.p{position:absolute;left:88px;top:84px;font:600 34px var(--sans)}
.k{position:absolute;left:88px;top:220px;font:500 28px var(--mono);letter-spacing:.08em;color:#60A5FA}
h1{position:absolute;left:88px;right:88px;top:270px;font:400 ${lang === 'hi' ? 74 : 92}px/1.08 var(--serif);margin:0}
ul{position:absolute;left:88px;right:88px;top:${lang === 'hi' ? 680 : 700}px;list-style:none;padding:0;margin:0}
li{display:flex;align-items:center;gap:26px;font:500 40px/1.3 var(--sans);margin:0 0 26px}
li i{width:34px;height:34px;border:3px solid #60A5FA;border-radius:8px;flex:none}
.cta{position:absolute;left:88px;right:88px;bottom:220px;background:#1D4ED8;border-radius:28px;padding:30px 36px;font:600 ${lang === 'hi' ? 36 : 38}px/1.3 var(--sans)}
.f{position:absolute;left:88px;right:88px;bottom:96px;display:flex;justify-content:space-between;align-items:center;font:500 26px var(--mono);color:#C5D0DE}
.f .b{display:flex;gap:12px;align-items:center;font:400 34px var(--serif);color:#F3F6FA}
</style></head><body><svg style="position:absolute;inset:0" width="1080" height="1350">${dots}</svg>
<div class="p">${partner}</div><div class="k">${c.k}</div><h1>${c.h}</h1>
<ul>${c.items.map(t => `<li><i></i>${t}</li>`).join('')}</ul>
<div class="cta">${c.cta}</div>
<div class="f"><div style="display:flex;gap:14px;align-items:center">${c.by}<span class="b">${sealSvg('#60A5FA', 44)}Vedha</span></div><div>vedhasec.com</div></div>
<script>window.ready=true</script></body></html>`;
  const f = path.join(DIR, `${lang}.html`); fs.writeFileSync(f, html);
  await render(f, 1080, 1350, path.join(DIR, `diwali_safai_${lang}${lang === 'hi' ? '_NEEDS_REVIEW' : ''}.png`)); fs.rmSync(f);
}
