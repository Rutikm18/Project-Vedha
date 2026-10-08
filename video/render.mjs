// Deterministic frame renderer: serves /video locally, drives headless Chromium with
// Playwright, and pulls each frame off the canvas as a PNG. No network at render time.
//
//   node render.mjs --aspect 4x5 --w 1080 --h 1350 --out out/frames/master   all 900 frames
//   node render.mjs --aspect 4x5 --still 450 --file out/f450.png            one frame
//   options: --lang hi  --hook B|C  --hookPx 88  --debug  --from 0 --to 90  --workers 6
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

export const ROOT = path.dirname(fileURLToPath(import.meta.url));
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2' };

export async function openRenderer() {
  const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' });
    fs.createReadStream(p).pipe(res);
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    // No network at render time: stop Chromium's own background traffic.
    args: ['--disable-background-networking', '--disable-component-update', '--disable-domain-reliability',
      '--disable-sync', '--no-pings', '--no-first-run', '--metrics-recording-only', '--disable-features=OptimizationHints,Translate'],
  });
  const port = server.address().port;

  async function page(opts) {
    const { aspect = '4x5', w = 1080, h = 1350, lang = 'en', hook = '', hookPx = '', debug = false } = opts;
    const pg = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    pg.on('console', m => m.type() === 'error' && console.error('console:', m.text()));
    pg.on('pageerror', e => { console.error('page error:', e.message); process.exitCode = 1; });
    const q = new URLSearchParams({ aspect, w, h, lang, hook, hookPx, debug: debug ? 1 : 0 });
    await pg.goto(`http://127.0.0.1:${port}/src/page.html?${q}`);
    await pg.waitForFunction('window.ready === true', null, { timeout: 30000 });
    return pg;
  }
  const grab = async (pg, n) => Buffer.from((await pg.evaluate(n => window.grab(n), n)).split(',')[1], 'base64');

  // Render frames [from, to) into outDir/00000.png ... (numbered from 0), across N pages.
  async function frames(opts, outDir, { from = 0, to = 900, workers = 6 } = {}) {
    fs.rmSync(outDir, { recursive: true, force: true });
    fs.mkdirSync(outDir, { recursive: true });
    const pages = await Promise.all(Array.from({ length: workers }, () => page(opts)));
    let next = from;
    await Promise.all(pages.map(async pg => {
      while (next < to) {
        const n = next++;
        fs.writeFileSync(path.join(outDir, `${String(n - from).padStart(5, '0')}.png`), await grab(pg, n));
      }
    }));
    await Promise.all(pages.map(p => p.close()));
  }
  async function still(opts, n, file) {
    const pg = await page(opts);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, await grab(pg, n));
    await pg.close();
  }
  async function poster(opts, file) {
    const pg = await page(opts);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, Buffer.from((await pg.evaluate(() => window.poster())).split(',')[1], 'base64'));
    await pg.close();
  }
  return { frames, still, poster, close: async () => { await browser.close(); server.close(); } };
}

// CLI
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const a = {};
  process.argv.slice(2).forEach((v, i, all) => { if (v.startsWith('--')) a[v.slice(2)] = all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true; });
  const opts = { aspect: a.aspect || '4x5', w: +(a.w || 1080), h: +(a.h || 1350), lang: a.lang || 'en', hook: a.hook || '', hookPx: a.hookPx || '', debug: !!a.debug };
  const r = await openRenderer();
  try {
    if (a.still) {
      for (const n of String(a.still).split(',').map(Number)) {
        const file = a.file && !String(a.still).includes(',') ? a.file : path.join(ROOT, 'out/stills', `${opts.aspect}_${opts.lang}_f${String(n).padStart(3, '0')}.png`);
        await r.still(opts, n, path.resolve(ROOT, file)); console.log('wrote', file);
      }
    } else {
      const t0 = Date.now();
      await r.frames(opts, path.resolve(ROOT, a.out || 'out/frames/tmp'), { from: +(a.from || 0), to: +(a.to || 900), workers: +(a.workers || 6) });
      console.log(`rendered in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
    }
  } finally { await r.close(); }
}
