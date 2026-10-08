// Presentation mockup of the card system (not for print).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { render } from '../shared/render.mjs';
const DIR = path.dirname(fileURLToPath(import.meta.url));
// Show trim only: crop the 3 mm bleed off each render with background-position.
const card = (file, x, y, rot, z) => `<div class="c" style="left:${x}px;top:${y}px;transform:rotate(${rot}deg);z-index:${z};background-image:url(/cards/out/${file})"></div>`;
const html = `<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/shared/brand.css"><style>
body{width:2000px;height:1160px;background:#DCE3EC;position:relative;overflow:hidden;font-family:var(--sans)}
.c{position:absolute;width:840px;height:481px;border-radius:6px;background-size:896px 538px;background-position:-28px -28px;
   box-shadow:0 2px 3px rgba(6,11,20,.18),0 18px 40px rgba(6,11,20,.22)}
.l{position:absolute;font:500 22px var(--mono);letter-spacing:.08em;color:#475569}
</style></head><body>
${card('founder-a_89x51_back.png', 120, 110, -4, 1)}
${card('founder-a_89x51_front.png', 330, 300, 3, 2)}
${card('sample-partner_89x51_back.png', 1080, 140, 3, 1)}
${card('sample-partner_89x51_front.png', 1000, 520, -2, 2)}
<div class="l" style="left:140px;top:1080px">FOUNDER CARD · 89 × 51 MM · FRONT (DAY) + BACK (NIGHT)</div>
<div class="l" style="left:1020px;top:1080px">PARTNER CARD · CO-BRANDED · SAME BACK</div>
<script>window.ready=true</script></body></html>`;
fs.writeFileSync(path.join(DIR, 'mockup.html'), html);
await render(path.join(DIR, 'mockup.html'), 2000, 1160, path.join(DIR, 'mockup.png'));
fs.rmSync(path.join(DIR, 'mockup.html'));
