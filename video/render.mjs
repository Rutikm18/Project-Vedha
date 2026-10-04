// Deterministic renderer: serves /video locally, drives Chromium with Playwright,
// pulls each frame off the canvas as PNG, then stitches with ffmpeg.
//
//   node render.mjs --mode animatic            540x675 with the review overlay
//   node render.mjs --still 450 --out a.png    one frame
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) => {
  if (v.startsWith('--')) a.push([v.slice(2), all[i + 1] && !all[i + 1].startsWith('--') ? all[i + 1] : true]);
  return a;
}, []));

const MODES = {
  animatic: { w: 540, h: 675, aspect: '4x5', debug: 1, name: 'vedha_animatic_4x5_540x675' },
  master:   { w: 1080, h: 1350, aspect: '4x5', debug: 0, name: 'vedha_30s_4x5_1080x1350' },
};
const mode = MODES[args.mode || 'animatic'];
const lang = args.lang || 'en';
const OUT = path.resolve(ROOT, args.outdir || 'out');
const FRAMES = path.join(OUT, 'frames', mode.name);
const WORKERS = +(args.workers || 6);
const DURATION = 900;

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}/src/page.html?aspect=${mode.aspect}&w=${mode.w}&h=${mode.h}&debug=${mode.debug}&lang=${lang}`;

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  // No network at render time: stop Chromium's own background traffic.
  args: ['--disable-background-networking', '--disable-component-update', '--disable-domain-reliability',
    '--disable-sync', '--no-pings', '--no-first-run', '--metrics-recording-only', '--disable-features=OptimizationHints,Translate'] });
async function openPage() {
  const page = await browser.newPage({ viewport: { width: mode.w, height: mode.h }, deviceScaleFactor: 1 });
  page.on('console', m => m.type() === 'error' && console.error('console:', m.text()));
  page.on('requestfailed', r => console.error('request failed:', r.url(), r.failure()?.errorText));
  page.on('pageerror', e => { console.error('page error:', e.message); process.exitCode = 1; });
  await page.goto(base);
  await page.waitForFunction('window.ready === true', null, { timeout: 30000 });
  return page;
}
const grab = async (page, n) => Buffer.from((await page.evaluate(n => window.grab(n), n)).split(',')[1], 'base64');

try {
  if (args.still) {
    const page = await openPage();
    for (const n of String(args.still).split(',').map(Number)) {
      const out = args.out && !String(args.still).includes(',') ? args.out : path.join(OUT, 'stills', `${mode.name}_f${String(n).padStart(3, '0')}.png`);
      fs.mkdirSync(path.dirname(out), { recursive: true });
      fs.writeFileSync(out, await grab(page, n));
      console.log('wrote', out);
    }
  } else {
    fs.rmSync(FRAMES, { recursive: true, force: true });
    fs.mkdirSync(FRAMES, { recursive: true });
    const t0 = Date.now();
    const pages = await Promise.all(Array.from({ length: WORKERS }, openPage));
    let next = 0;
    await Promise.all(pages.map(async page => {
      while (next < DURATION) {
        const n = next++;
        fs.writeFileSync(path.join(FRAMES, `${String(n).padStart(5, '0')}.png`), await grab(page, n));
      }
    }));
    console.log(`rendered ${DURATION} frames in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
    const mp4 = path.join(OUT, `${mode.name}${lang === 'en' ? '' : '_' + lang}.mp4`);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error',
      '-framerate', '30', '-i', path.join(FRAMES, '%05d.png'),
      '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', '30',
      // H.264 4:2:0 needs even dimensions (675 -> 676 for the animatic).
      '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
      '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'slow', '-r', '30', '-fps_mode', 'cfr',
      '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
      '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', mp4], { stdio: 'inherit' });
    // contact sheet: every 30th frame, 6 across
    const sheet = path.join(OUT, 'qa', `${mode.name}_contact_sheet.png`);
    fs.mkdirSync(path.dirname(sheet), { recursive: true });
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', '30', '-i', path.join(FRAMES, '%05d.png'),
      '-vf', `select='not(mod(n\\,30))',scale=270:-1,tile=6x5:padding=6:margin=6:color=0x222222`, '-frames:v', '1', sheet], { stdio: 'inherit' });
    console.log('wrote', mp4, '\nwrote', sheet);
  }
} finally {
  await browser.close();
  server.close();
}
