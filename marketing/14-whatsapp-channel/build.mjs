// WhatsApp channel assets: icon (640x640) and, once the invite link exists, a QR poster.
//   node 14-whatsapp-channel/build.mjs                      -> icon only
//   LINK="https://whatsapp.com/channel/XXXX" node 14-whatsapp-channel/build.mjs   -> icon + QR poster
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import QRCode from 'qrcode';
import { sealSvg } from '../shared/seal.js';
import { render } from '../shared/render.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));
const tmp = n => path.join(DIR, n);

// Icon: WhatsApp crops channel icons to a circle, so the seal sits well inside the circle's safe area.
fs.writeFileSync(tmp('icon.html'), `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"></head>
<body style="width:640px;height:640px;background:#060B14;display:flex;align-items:center;justify-content:center">${sealSvg('#60A5FA', 330)}<script>window.ready=true</script></body></html>`);
await render(tmp('icon.html'), 640, 640, tmp('channel-icon.png'));
fs.rmSync(tmp('icon.html'));

if (process.env.LINK) {
  const qr = await QRCode.toString(process.env.LINK, { type: 'svg', margin: 0, errorCorrectionLevel: 'M', color: { dark: '#060B14', light: '#FFFFFF' } });
  fs.writeFileSync(tmp('poster.html'), `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
body{width:1080px;height:1350px;background:#060B14;color:#F3F6FA;font-family:var(--sans);padding:110px 96px;box-sizing:border-box}
h1{font:400 92px/1.02 var(--serif);margin-top:60px} p{font-size:36px;line-height:1.4;color:#C5D0DE;margin-top:28px}
.q{margin-top:70px;width:420px;height:420px;background:#fff;border-radius:28px;padding:34px;box-sizing:border-box}.q svg{width:100%;height:100%}
.s{font:500 30px var(--mono);margin-top:28px;letter-spacing:.06em;color:#60A5FA}</style></head><body>
<div style="display:flex;align-items:center;gap:22px;font:400 56px var(--serif)">${sealSvg('#60A5FA', 80)}Vedha</div>
<h1>Signal/Noise, on WhatsApp.</h1><p>One short note a week on what actually matters for office networks. No fear, no jargon.</p>
<div class="q">${qr}</div><div class="s">SCAN TO FOLLOW · YOUR NUMBER STAYS PRIVATE</div><script>window.ready=true</script></body></html>`);
  await render(tmp('poster.html'), 1080, 1350, tmp('channel-poster.png'));
  fs.rmSync(tmp('poster.html'));
}
