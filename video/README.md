# Vedha 30-second film

A deterministic, code-rendered brand film. `src/film.js` exports a pure `renderFrame(ctx, frame, cfg)`: it uses no clock and no `Math.random()`, so the same frame always gives the same pixels. `render.mjs` serves this folder locally, drives Chromium with Playwright, pulls each frame off the canvas and stitches the frames with ffmpeg.

## Status

- [x] Phase 0: recon (`RECON.md`, `claims.md`)
- [x] Phase 1: animatic, 4:5 at 540×675, final captions and timing, placeholder console
- [ ] Phase 2: scene polish and real console UI (blocked on the website repo; see RECON.md)
- [ ] Phase 3: all formats, SFX, SRT, stills, hook variants, 15 s cutdown
- [ ] Phase 4: QA gate

## Commands

```bash
cd video
npm install                                   # fonts + playwright-core only
node render.mjs --mode animatic               # out/vedha_animatic_4x5_540x675.mp4 + contact sheet
node render.mjs --mode master                 # 1080x1350 master (silent)
node render.mjs --mode master --still 450 --out out/f450.png   # one frame
```

Uses the pre-installed Chromium at `/opt/pw-browsers`; set `CHROMIUM_PATH` to override.

## Editing

- **Copy:** `src/copy.en.json` (`src/copy.hi.json` needs native-speaker review). Scenes contain no strings.
- **Timing:** `src/timeline.js`. Every beat is a frame number at 30 fps.
- **Layout per format:** `src/layouts.js`
- **Colours, fonts, the seal:** `src/brand.js` (seal path copied verbatim from `manager/frontend/public/brand/vedha-mark.svg`)
- **Illustrative UI data:** `src/data.illustrative.json` (RFC 5737 IPs, `.example` hostnames)

## Needs human review

- Hindi copy (native speaker), and वेध / "to pierce through" (cultural check). The dot lattice is a pulli-style visual reference only.
- Product claims: "7-day", "partner", "office networks" (see `claims.md`)
- The console in scenes 5 and 6 is a placeholder, not the real marketing-site UI
