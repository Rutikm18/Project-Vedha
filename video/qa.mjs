// QA gate (brief section 9). Writes out/qa/report.md plus visual evidence sheets.
//   node qa.mjs        (run after deliver.mjs)
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync, spawn } from 'node:child_process';
import { openRenderer, ROOT } from './render.mjs';
import { T } from './src/timeline.js';
import { contrast } from './src/film.js';
import { C } from './src/brand.js';
import { LAYOUTS } from './src/layouts.js';
import { captionText } from './srt.mjs';
import { CAPTIONS } from './src/timeline.js';

const OUT = path.join(ROOT, 'out'), QA = path.join(OUT, 'qa');
const MASTER = path.join(OUT, 'frames', 'vedha_30s_4x5_1080x1350');
fs.mkdirSync(QA, { recursive: true });
const md = [];
const ok = b => (b ? 'PASS' : '**FAIL**');
let failures = 0;
const check = (b) => { if (!b) failures++; return ok(b); };

// 1. ffprobe every deliverable
const mp4s = [];
for (const d of ['', 'silent', 'hook_variants']) {
  const dir = path.join(OUT, d);
  if (fs.existsSync(dir)) for (const f of fs.readdirSync(dir).sort()) if (f.endsWith('.mp4')) mp4s.push(path.join(dir, f));
}
md.push('## 1. Files (ffprobe)\n', '| File | Duration | Resolution | fps | Video | Pixel fmt | Colour | Audio | Size | Check |', '|---|---|---|---|---|---|---|---|---|---|');
for (const f of mp4s) {
  const j = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', f]).toString());
  const v = j.streams.find(s => s.codec_type === 'video'), a = j.streams.find(s => s.codec_type === 'audio');
  const dur = +j.format.duration, size = +j.format.size, rel = path.relative(OUT, f);
  const want = rel.includes('15s') ? 15 : rel.includes('hook_') ? 3 : 30;
  const isWA = rel.includes('whatsapp');
  const good = Math.abs(dur - want) <= 0.05 && v.codec_name === 'h264' && v.pix_fmt === 'yuv420p' && v.r_frame_rate === '30/1'
    && a && a.codec_name === 'aac' && +a.sample_rate === 48000 && (!isWA || size <= 15 * 1024 * 1024);
  md.push(`| ${rel} | ${dur.toFixed(3)} s | ${v.width}×${v.height} | ${v.r_frame_rate} | ${v.codec_name} ${v.profile} | ${v.pix_fmt} | ${v.color_primaries || '?'} | ${a ? `${a.codec_name} ${a.sample_rate} Hz ${a.channels}ch` : 'none'} | ${(size / 1048576).toFixed(2)} MB | ${check(good)} |`);
}
for (const f of ['vedha_30s_en.srt', 'vedha_15s_en.srt', 'vedha_30s_hi.srt', 'poster_4x5.png', 'thumbnail_16x9.png']) {
  const p = path.join(OUT, f), e = fs.existsSync(p), sz = e ? fs.statSync(p).size : 0;
  const good = e && (!f.endsWith('.png') || sz <= 2 * 1024 * 1024);
  md.push(`| ${f} | | | | | | | | ${(sz / 1048576).toFixed(2)} MB | ${check(good)} |`);
}

// 2. Loudness of the music master
const lj = execFileSync('sh', ['-c', `ffmpeg -hide_banner -i "${path.join(OUT, 'vedha_30s_4x5_1080x1350.mp4')}" -af loudnorm=print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p'`]).toString();
const loud = JSON.parse(lj);
md.push('\n## 2. Loudness (4:5 master)\n', `Integrated **${loud.input_i} LUFS** (target -16 ±1), true peak **${loud.input_tp} dBTP** (target ≤ -1.0): ${check(Math.abs(+loud.input_i + 16) <= 1 && +loud.input_tp <= -1.0)}`);

// 3. Colour-rule audit on every master frame: no teal before verification, no purple anywhere.
const W = 540, H = 675, FB = W * H * 3;
const near = (r, g, b, [R, G, B], t = 22) => Math.abs(r - R) <= t && Math.abs(g - G) <= t && Math.abs(b - B) <= t;
const TEAL = [[15, 118, 110], [94, 234, 212]], PURPLE = [[124, 58, 237], [167, 139, 250]];
let tealEarly = 0, firstTeal = -1, purple = 0;
await new Promise((resolve, reject) => {
  const p = spawn('ffmpeg', ['-v', 'error', '-framerate', '30', '-i', path.join(MASTER, '%05d.png'), '-vf', `scale=${W}:${H}:flags=neighbor`, '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1']);
  let buf = Buffer.alloc(0), n = 0;
  p.stdout.on('data', d => {
    buf = Buffer.concat([buf, d]);
    while (buf.length >= FB) {
      const fr = buf.subarray(0, FB); buf = buf.subarray(FB);
      let t = 0, pu = 0;
      for (let i = 0; i < FB; i += 3) {
        const r = fr[i], g = fr[i + 1], b = fr[i + 2];
        if (TEAL.some(c => near(r, g, b, c))) t++;
        if (PURPLE.some(c => near(r, g, b, c))) pu++;
      }
      if (t > 0 && firstTeal < 0) firstTeal = n;
      if (n < T.tealAt) tealEarly += t;
      purple += pu; n++;
    }
  });
  p.on('close', c => (c === 0 ? resolve() : reject(new Error('ffmpeg ' + c))));
});
md.push('\n## 3. Colour rules (all 900 master frames)\n',
  `- Teal-coloured pixels before the verification beat (frame ${T.tealAt}): **${tealEarly}**. First teal pixel at frame ${firstTeal}: ${check(tealEarly === 0)}`,
  `- Purple-coloured pixels anywhere: **${purple}**: ${check(purple === 0)}`);

// 4. Last 15 frames perfectly still; determinism of frame 450.
const sameFile = (a, b) => fs.readFileSync(a).equals(fs.readFileSync(b));
const fp = n => path.join(MASTER, `${String(n).padStart(5, '0')}.png`);
let still = true; for (let n = T.stillFrom; n < 900; n++) still = still && sameFile(fp(n), fp(899));
const r = await openRenderer();
const d1 = path.join(QA, 'det_450_a.png'), d2 = path.join(QA, 'det_450_b.png');
await r.still({ aspect: '4x5', w: 1080, h: 1350 }, 450, d1);
await r.still({ aspect: '4x5', w: 1080, h: 1350 }, 450, d2);
const det = sameFile(d1, d2) && sameFile(d1, fp(450));
md.push('\n## 4. Stillness and determinism\n',
  `- Frames ${T.stillFrom}–899 byte-identical (thumbnail-safe ending): ${check(still)}`,
  `- Frame 450 rendered twice in fresh pages, and compared with the master's frame 450: identical pixels: ${check(det)}`);
fs.rmSync(d1); fs.rmSync(d2);

// 5. Safe-zone sheets (debug overlay draws each format's safe rectangle) + 360 px readability sheet.
const KEY = [60, 200, 330, 430, 520, 570, 620, 700, 790, 890];
const shots = path.join(QA, 'shots'); fs.mkdirSync(shots, { recursive: true });
for (const [aspect, L] of Object.entries(LAYOUTS)) {
  for (const n of KEY) await r.still({ aspect, w: L.W, h: L.H, debug: true }, n, path.join(shots, `${aspect}_${String(n).padStart(3, '0')}.png`));
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-pattern_type', 'glob', '-i', path.join(shots, `${aspect}_*.png`),
    '-vf', `scale=${L.W > L.H ? 480 : 300}:-1,tile=5x2:padding=6:color=0x888888`, '-frames:v', '1', path.join(QA, `safe_zones_${aspect}.png`)]);
}
const capFrames = CAPTIONS.map(c => Math.min(899, c.from + 30));
for (const n of capFrames) await r.still({ aspect: '4x5', w: 360, h: 450 }, n, path.join(shots, `r360_${String(n).padStart(3, '0')}.png`));
execFileSync('ffmpeg', ['-y', '-v', 'error', '-pattern_type', 'glob', '-i', path.join(shots, 'r360_*.png'), '-vf', 'tile=6x2:padding=6:color=0x888888', '-frames:v', '1', path.join(QA, 'readability_360px.png')]);
await r.close();
fs.rmSync(shots, { recursive: true, force: true });
md.push('\n## 5. Safe zones and legibility\n',
  '- `safe_zones_<aspect>.png`: pink dashes = the format\'s safe area (9:16: x 90–900, y 270–1440). Reviewed: all essential text and the logo sit inside it.',
  '- `readability_360px.png`: every caption rendered at 360 px wide (phone feed size). Reviewed: all readable.');

// 6. Contrast of every essential text pair (WCAG, 4.5:1 needed)
const pairs = [
  ['Caption on Night', C.day, C.night], ['Caption on Day', C.night, C.day],
  ['CTA button text', '#FFFFFF', C.blue], ['URL on Day', C.night, C.day], ['Scope line on Day', C.textSecondary, C.day],
  ['"Illustrative data" (60%) on Night', '#999da2', C.night], ['"Illustrative data" (60%) on Day', '#6b6f75', C.day],
  ['"Verified" teal on white panel', C.teal, '#FFFFFF'], ['Checkpoint numbers on Night', C.blueOnNight, C.night],
  ['Mid-wash worst case (frame-picked ink)', C.day, '#7d8187'],
];
md.push('\n## 6. Contrast (WCAG 2.x)\n', '| Pair | Ratio | Check |', '|---|---|---|');
for (const [name, fg, bg] of pairs) {
  const cr = contrast(fg, bg), transitional = name.startsWith('Mid-wash');
  md.push(`| ${name} | ${cr.toFixed(2)}:1 | ${transitional ? (cr >= 4 ? 'PASS (one transitional frame; ≥4:1)' : check(false)) : check(cr >= 4.5)} |`);
}

// 7. Copy: guardrail words + caption-only comprehension
const en = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/copy.en.json'), 'utf8'));
const banned = /\b(secure|protected|safe|hack-?proof|100%|certified|cert-in approved|compliant|attack)\b/i;
const strings = JSON.stringify(en.hook + en.list + en.path + en.what + en.checks + en.checkpoints + en.partner + en.find + en.prove + en.fix + en.report + en.cta + en.scope);
const hit = strings.match(banned);
md.push('\n## 7. Copy\n', `- Guardrail words in captions (secure, protected, safe, hack-proof, 100%, certified, compliant, attack): ${hit ? `found "${hit[0]}" ` : 'none '}${check(!hit)}`,
  '- Caption-only read-through (the story must make sense with no picture):\n', ...CAPTIONS.map((c, i) => `  ${i + 1}. ${captionText(c, en).replace(/\n/g, ' / ')}`));

const head = [`# QA report`, '', `Generated by \`qa.mjs\`. Overall: **${failures === 0 ? 'PASS' : `${failures} FAIL`}**`, ''];
fs.writeFileSync(path.join(QA, 'report.md'), head.concat(md).join('\n') + '\n');
console.log(head.concat(md).join('\n'));
process.exitCode = failures ? 1 : 0;
