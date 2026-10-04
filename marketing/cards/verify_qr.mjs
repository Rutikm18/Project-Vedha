// QR QA: decode every card back with an independent reader (jsQR) the way a phone sees it:
// area-averaged (blurred) at 60%, 40% and 30% of print resolution (~ card held 15-30 cm from a phone camera).
// Final check is still a real phone on the printer's proof (DESIGN.md).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import jsQR from 'jsqr';
import { PNG } from 'pngjs';
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), 'out');
const blur = (png, s) => {
  const w = Math.round(png.width * s), h = Math.round(png.height * s), d = new Uint8ClampedArray(w * h * 4), f = 1 / s;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const a = [0, 0, 0, 0]; let n = 0;
    for (let yy = Math.floor(y * f); yy < Math.min(png.height, Math.floor((y + 1) * f)); yy++)
      for (let xx = Math.floor(x * f); xx < Math.min(png.width, Math.floor((x + 1) * f)); xx++) { const i = (yy * png.width + xx) * 4; for (let k = 0; k < 4; k++) a[k] += png.data[i + k]; n++; }
    for (let k = 0; k < 4; k++) d[(y * w + x) * 4 + k] = a[k] / Math.max(1, n);
  }
  return { d, w, h };
};
let ok = 0, bad = 0;
for (const f of fs.readdirSync(OUT).filter(f => f.endsWith('_back.png'))) {
  const png = PNG.sync.read(fs.readFileSync(path.join(OUT, f))); const row = [];
  for (const s of [0.6, 0.4, 0.3]) {
    const { d, w, h } = blur(png, s); const r = jsQR(d, w, h);
    const good = r && (r.data.startsWith('BEGIN:VCARD') || r.data.startsWith('https://vedhasec.com/'));
    row.push(`${s * 100}%:${good ? 'ok' : 'FAIL'}`); good ? ok++ : bad++;
  }
  console.log(f.padEnd(34), row.join('  '));
}
console.log(`${ok} decoded, ${bad} failed`); process.exitCode = bad ? 1 : 0;
