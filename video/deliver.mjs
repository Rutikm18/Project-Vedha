// Builds every deliverable in out/: score, all formats, silent masters, WhatsApp cut,
// 15 s cutdown, Hindi review cut, hook variants, SRTs, poster, thumbnail, contact sheet.
//
//   node deliver.mjs            everything (about 5 to 10 minutes)
//   node deliver.mjs --only 4x5 master + derived files only
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync, spawn } from 'node:child_process';
import { openRenderer, ROOT } from './render.mjs';
import { buildSrt } from './srt.mjs';

const OUT = path.join(ROOT, 'out');
const FR = path.join(OUT, 'frames');
const AUD = path.join(OUT, 'audio');
const only = process.argv.includes('--only') ? process.argv[process.argv.indexOf('--only') + 1] : null;
// Async ffmpeg: a blocking call would freeze the event loop and starve Playwright's browser pipe.
const ff = (...args) => new Promise((resolve, reject) => {
  const p = spawn('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-nostdin', ...args], { stdio: ['ignore', 'inherit', 'inherit'] });
  p.on('close', c => (c === 0 ? resolve() : reject(new Error(`ffmpeg exited ${c}`))));
});
const json = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8'));
for (const d of [OUT, FR, AUD, path.join(OUT, 'silent'), path.join(OUT, 'hook_variants'), path.join(OUT, 'qa')]) fs.mkdirSync(d, { recursive: true });

const FORMATS = [
  { aspect: '4x5', w: 1080, h: 1350, name: 'vedha_30s_4x5_1080x1350' },
  { aspect: '9x16', w: 1080, h: 1920, name: 'vedha_30s_9x16_1080x1920' },
  { aspect: '1x1', w: 1080, h: 1080, name: 'vedha_30s_1x1_1080x1080' },
  { aspect: '16x9', w: 1920, h: 1080, name: 'vedha_30s_16x9_1920x1080' },
].filter(f => !only || f.aspect === only);

// H.264 High, yuv420p, CFR 30, BT.709, +faststart, AAC 48 kHz stereo 192 kbps (Appendix C).
async function encode(frames, out, { audio = null, seconds = 30, pattern = '%05d.png', vf = null, crf = 17, extra = [] } = {}) {
  const aIn = audio ? ['-i', audio] : ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo'];
  await ff('-framerate', '30', '-i', path.join(frames, pattern), ...aIn, '-t', String(seconds),
    ...(vf ? ['-vf', vf] : []),
    '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', String(crf), '-preset', 'slow', '-r', '30', '-fps_mode', 'cfr',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', ...extra,
    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-shortest', '-movflags', '+faststart', out);
  console.log('wrote', path.relative(ROOT, out));
}

const t0 = Date.now();

// 1. Score: synthesize, then two-pass loudness normalisation to -16 LUFS, true peak <= -1.5 dBTP.
execFileSync('node', [path.join(ROOT, 'music.mjs'), 'out/audio/score.wav'], { stdio: 'inherit' });
const ln = (() => { try { const s = execFileSync('sh', ['-c', `ffmpeg -hide_banner -i "${path.join(AUD, 'score.wav')}" -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p'`]).toString(); return JSON.parse(s); } catch { return null; } })();
const SCORE = path.join(AUD, 'score_master.wav');
await ff('-i', path.join(AUD, 'score.wav'), '-af', ln
  ? `loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=${ln.input_i}:measured_TP=${ln.input_tp}:measured_LRA=${ln.input_lra}:measured_thresh=${ln.input_thresh}:offset=${ln.target_offset}:linear=true`
  : 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', SCORE);

const r = await openRenderer();
try {
  // 2. Masters in every format (music + silent).
  for (const F of FORMATS) {
    const dir = path.join(FR, F.name);
    const t = Date.now();
    await r.frames(F, dir);
    console.log(`${F.name}: 900 frames in ${((Date.now() - t) / 1000).toFixed(0)} s`);
    await encode(dir, path.join(OUT, `${F.name}.mp4`), { audio: SCORE });
    await encode(dir, path.join(OUT, 'silent', `${F.name}_silent.mp4`));
    if (F.aspect !== '4x5') fs.rmSync(dir, { recursive: true, force: true }); // keep disk use low
  }

  const MASTER = path.join(FR, 'vedha_30s_4x5_1080x1350');
  if (fs.existsSync(MASTER)) {
    // 3. WhatsApp: 720x900, iterate CRF until <= 15 MB.
    const wa = path.join(OUT, 'vedha_30s_4x5_whatsapp_720x900.mp4');
    for (const crf of [23, 25, 27, 29, 31]) {
      await encode(MASTER, wa, { audio: SCORE, vf: 'scale=720:900:flags=lanczos', crf, extra: ['-maxrate', '3M', '-bufsize', '6M'] });
      if (fs.statSync(wa).size <= 15 * 1024 * 1024) break;
    }

    // 4. 15 s cutdown: the whole story in miniature.
    // hook -> scan + first finding -> seal + "7-day check" -> evidence + verified fix -> CTA (held still)
    const SEG = [[0, 100], [104, 170], [304, 362], [600, 725], [825, 900]];
    const cut = path.join(FR, 'cutdown_15s');
    fs.rmSync(cut, { recursive: true, force: true }); fs.mkdirSync(cut, { recursive: true });
    let k = 0;
    const link = src => fs.copyFileSync(path.join(MASTER, `${String(src).padStart(5, '0')}.png`), path.join(cut, `${String(k++).padStart(5, '0')}.png`));
    for (const [a, b] of SEG) for (let f = a; f < b; f++) link(f);
    while (k < 450) link(899); // last 15 frames: perfectly still
    const cutWav = path.join(AUD, 'cutdown_15s.wav');
    const parts = SEG.map(([a, b], i) => `[0:a]atrim=${a / 30}:${b / 30},asetpts=PTS-STARTPTS,afade=t=in:d=0.06,afade=t=out:st=${(b - a) / 30 - 0.08}:d=0.08[s${i}]`);
    await ff('-i', SCORE, '-filter_complex', `${parts.join(';')};${SEG.map((_, i) => `[s${i}]`).join('')}concat=n=${SEG.length}:v=0:a=1,apad=whole_dur=15[a]`, '-map', '[a]', '-t', '15', cutWav);
    await encode(cut, path.join(OUT, 'vedha_15s_4x5_1080x1350.mp4'), { audio: cutWav, seconds: 15 });
    // Cutdown SRT: shift each cue into its segment, drop cues that fall outside.
    const offsets = []; let acc = 0; for (const [a, b] of SEG) { offsets.push([a, b, acc - a]); acc += b - a; }
    const mapCut = (from, to) => {
      for (const [a, b, off] of offsets) if (from < b && to > a) {
        const s = Math.max(from, a) + off, e = Math.min(to, b) + off;
        return e - s >= 20 ? [s, b === 900 ? 450 : e] : null;
      }
      return null;
    };
    fs.writeFileSync(path.join(OUT, 'vedha_15s_en.srt'), buildSrt({ ...json('src/copy.en.json') }, mapCut));

    // 5. Hook variants (first 3 s): A main hook, B the three findings, C the promise.
    const A = path.join(OUT, 'hook_variants', 'hook_A_door.mp4');
    await encode(MASTER, A, { audio: SCORE, seconds: 3 });
    for (const [hook, file, px] of [['B', 'hook_B_findings.mp4', 60], ['C', 'hook_C_promise.mp4', 80]]) {
      const dir = path.join(FR, `hook_${hook}`);
      await r.frames({ aspect: '4x5', w: 1080, h: 1350, hook, hookPx: px }, dir, { from: 0, to: 90 });
      await encode(dir, path.join(OUT, 'hook_variants', file), { audio: SCORE, seconds: 3 });
    }

    // 6. Contact sheet: every 30th frame of the master.
    await ff('-framerate', '30', '-i', path.join(MASTER, '%05d.png'), '-vf', "select='not(mod(n\\,30))',scale=270:-1,tile=6x5:padding=6:margin=6:color=0x222222", '-frames:v', '1', path.join(OUT, 'qa', 'contact_sheet.png'));
  }

  if (!only) {
    // 7. Hindi: needs native-speaker review; do not publish unreviewed.
    const hi = path.join(FR, 'vedha_30s_hi');
    await r.frames({ aspect: '4x5', w: 1080, h: 1350, lang: 'hi' }, hi);
    await encode(hi, path.join(OUT, 'vedha_30s_hi_NEEDS_REVIEW.mp4'), { audio: SCORE });
    fs.writeFileSync(path.join(OUT, 'vedha_30s_hi.srt'), buildSrt({ ...json('src/copy.en.json'), ...json('src/copy.hi.json') }));

    // 8. Animatic (review overlay), 540x675 padded to 676.
    const an = path.join(FR, 'animatic');
    await r.frames({ aspect: '4x5', w: 540, h: 675, debug: true }, an);
    await encode(an, path.join(OUT, 'vedha_animatic_4x5_540x675.mp4'), { audio: SCORE, vf: 'pad=ceil(iw/2)*2:ceil(ih/2)*2' });
  }

  // 9. SRT, poster, thumbnail.
  fs.writeFileSync(path.join(OUT, 'vedha_30s_en.srt'), buildSrt(json('src/copy.en.json')));
  if (!only || only === '4x5') await r.poster({ aspect: '4x5', w: 1080, h: 1350 }, path.join(OUT, 'poster_4x5.png'));
  if (!only || only === '16x9') await r.poster({ aspect: '16x9', w: 1920, h: 1080 }, path.join(OUT, 'thumbnail_16x9.png'));
} finally {
  await r.close();
}
// 10. Docs travel with the files.
for (const f of ['README.md', 'claims.md', 'THIRD_PARTY.md', 'post_copy.md', 'MUSIC.md', 'CHECKPOINTS.md']) fs.copyFileSync(path.join(ROOT, f), path.join(OUT, f));
console.log(`done in ${((Date.now() - t0) / 60000).toFixed(1)} min`);
