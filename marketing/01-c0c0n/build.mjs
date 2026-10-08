// Partner Zero QR card for c0c0n: 3.5 x 2 in business card (1050 x 600 px = 300 dpi), PNG + print PDF.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import QRCode from 'qrcode';
import { sealSvg } from '../shared/seal.js';
import { render } from '../shared/render.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
// UTM-tagged so analytics (#6) can count card scans separately.
const URL_ = 'https://vedhasec.com/?utm_source=c0c0n&utm_medium=qr_card&utm_campaign=partner_zero';
const qr = await QRCode.toString(URL_, { type: 'svg', margin: 0, errorCorrectionLevel: 'M', color: { dark: '#060B14', light: '#F3F6FA' } });

const html = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css">
<style>
body { width: 1050px; height: 600px; background: var(--night); color: var(--day); font-family: var(--sans); overflow: hidden; position: relative; }
.dots { position: absolute; inset: 0; background-image: radial-gradient(rgba(243,246,250,.16) 2.2px, transparent 2.6px); background-size: 34px 34px; background-position: 17px 17px; }
.left { position: absolute; left: 64px; top: 58px; width: 560px; }
.brand { display: flex; align-items: center; gap: 18px; }
.brand span { font-family: var(--serif); font-size: 52px; }
h1 { font-family: var(--serif); font-weight: 400; font-size: 92px; line-height: 1; margin-top: 46px; }
p { font-size: 29px; line-height: 1.35; margin-top: 20px; color: #DCE3EC; }
.who { position: absolute; left: 64px; bottom: 50px; font-family: var(--mono); font-size: 19px; letter-spacing: .06em; color: var(--blue-night); }
.right { position: absolute; right: 64px; top: 70px; width: 300px; text-align: center; }
.qr { background: var(--day); border-radius: 22px; padding: 22px; }
.qr svg { width: 256px; height: 256px; display: block; }
.scan { font-weight: 600; font-size: 26px; margin-top: 22px; }
.url { font-family: var(--mono); font-size: 21px; margin-top: 8px; color: #DCE3EC; }
</style></head><body><div class="dots"></div>
<div class="left">
  <div class="brand">${sealSvg('#60A5FA', 64)}<span>Vedha</span></div>
  <h1>Be Partner Zero.</h1>
  <p>Run one of the first Vedha 7-day network health checks for a client, with the founders beside you.</p>
</div>
<div class="who">IT FIRMS · INSTALLERS · ISO / CA CONSULTANTS · AUDITORS</div>
<div class="right"><div class="qr">${qr}</div><div class="scan">Scan to talk to us</div><div class="url">info@vedhasec.com</div></div>
<script>window.ready = true;</script></body></html>`;
fs.writeFileSync(path.join(DIR, 'partner-zero-card.html'), html);
await render(path.join(DIR, 'partner-zero-card.html'), 1050, 600, path.join(DIR, 'partner-zero-card.png'), path.join(DIR, 'partner-zero-card.pdf'), [3.5, 2]);
