// Render a marketing HTML page to PNG (and optionally PDF) at an exact pixel size.
//   node shared/render.mjs <page.html> <width> <height> <out.png> [out.pdf]
// Fonts are served locally; no network at render time.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.png': 'image/png' };

// pdfIn = [widthInches, heightInches] scales the page to a physical print size (vector text stays sharp).
export async function render(page, w, h, png, pdf, pdfIn = null) {
  const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--disable-background-networking', '--disable-component-update', '--no-pings'] });
  try {
    const pg = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    pg.on('pageerror', e => { console.error('page error:', e.message); process.exitCode = 1; });
    await pg.goto(`http://127.0.0.1:${server.address().port}/${path.relative(ROOT, path.resolve(page))}`);
    await pg.waitForFunction('window.ready === true', null, { timeout: 20000 }).catch(() => {});
    await pg.evaluate(() => document.fonts.ready);
    if (png) { fs.mkdirSync(path.dirname(png), { recursive: true }); await pg.screenshot({ path: png, clip: { x: 0, y: 0, width: w, height: h } }); console.log('wrote', png); }
    if (pdf) {
      const o = pdfIn ? { width: `${pdfIn[0]}in`, height: `${pdfIn[1]}in`, scale: (pdfIn[0] * 96) / w } : { width: `${w}px`, height: `${h}px` };
      await pg.pdf({ path: pdf, ...o, printBackground: true, pageRanges: '1', margin: { top: 0, right: 0, bottom: 0, left: 0 } }); console.log('wrote', pdf);
    }
  } finally { await browser.close(); server.close(); }
}

// Print render: page laid out in mm; vector PDF at exactly wMm x hMm; PNG at `dpi`.
export async function renderPrint(page, wMm, hMm, { png, pdf, dpi = 300 } = {}) {
  const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--disable-background-networking', '--disable-component-update', '--no-pings'] });
  try {
    const cssW = wMm * 96 / 25.4, cssH = hMm * 96 / 25.4;
    const pg = await browser.newPage({ viewport: { width: Math.ceil(cssW), height: Math.ceil(cssH) }, deviceScaleFactor: dpi / 96 });
    pg.on('pageerror', e => { console.error('page error:', e.message); process.exitCode = 1; });
    const rel = path.relative(ROOT, path.resolve(page.split('?')[0])) + (page.includes('?') ? '?' + page.split('?')[1] : '');
    await pg.goto(`http://127.0.0.1:${server.address().port}/${rel}`);
    await pg.evaluate(() => document.fonts.ready);
    if (png) { fs.mkdirSync(path.dirname(png), { recursive: true }); await pg.screenshot({ path: png, clip: { x: 0, y: 0, width: cssW, height: cssH } }); }
    if (pdf) { fs.mkdirSync(path.dirname(pdf), { recursive: true }); await pg.pdf({ path: pdf, width: `${wMm}mm`, height: `${hMm}mm`, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } }); }
  } finally { await browser.close(); server.close(); }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [page, w, h, png, pdf] = process.argv.slice(2);
  await render(page, +w, +h, png, pdf);
}
