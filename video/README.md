# Vedha 30-second film

A deterministic, code-rendered brand film. `src/film.js` exports a pure `renderFrame(ctx, frame, cfg)`: it uses no clock and no `Math.random()`, so the same frame always gives the same pixels. `render.mjs` drives headless Chromium with Playwright; `deliver.mjs` encodes everything with ffmpeg; `music.mjs` composes the score in code; `qa.mjs` runs the QA gate.

## The film in one breath

*Every office has one door nobody remembers.* A scan sweeps the office and keeps counting: there's more on your network than you think. Three things light up, each named for what's at stake: **the accounts PC with remote login left open, client files anyone on the Wi-Fi can open, billing data readable without a password**. The Vedha seal opens its eye and pierces through: **four checkpoints**, what your business runs on. A partner you trust runs the check. The console finds what's open, proves it with evidence, and shows the fix worked: the door from the first three seconds closes, and the music resolves at the same moment. Book your 7-day check.

- Why these assets and checkpoints: `CHECKPOINTS.md` (research + product mapping)
- What the music means: `MUSIC.md`
- What every claim rests on: `claims.md`
- Repo findings and conflicts with the brief: `RECON.md`

## Improvement pass (2026-10-04)

Reviewed against how the film is really watched: on a phone, mostly muted, with most viewers leaving early.

| Problem found | Why it matters | Change |
|---|---|---|
| The evidence (the proof, Vedha's differentiator) was 24 px text in the console, about 8 px on a phone | If the proof can't be read, "Prove what's real" is just a claim | A 44 px **evidence callout** in plain words, which becomes a teal **Verified** card at the fix |
| The brand appeared only at 9 s | Google's ABCD research: brand within the first 5 s for ad recall; most feed viewers leave early | A small seal in the safe corner from 0.5 s, handing over to the big reveal |
| 1.2 s with no message between the hook and the first finding | Muted viewers need a continuous line of meaning | The hook line now stays until the scan starts finding devices |
| The 15 s cutdown skipped the discovery, now the heart of the story | A cutdown has to tell the same story, shorter | Re-cut: hook → scan + first finding → seal → evidence + fix → CTA |
| The device counter showed "0" over the hook | A zero reads as "nothing here", the opposite of the point | The counter appears with the first device found |

## Commands

```bash
cd video
npm install                 # fonts + playwright-core only (no root-level deps)
node deliver.mjs            # everything into out/ (~15 min)
node deliver.mjs --only 4x5 # just the 4:5 master and what derives from it
node qa.mjs                 # QA gate -> out/qa/report.md
node music.mjs              # just the score -> out/audio/score.wav
node render.mjs --aspect 9x16 --w 1080 --h 1920 --still 450 --file out/f450.png --debug
```

Uses the pre-installed Chromium at `/opt/pw-browsers`; set `CHROMIUM_PATH` to override. Needs ffmpeg with libx264.

## Outputs (`out/`, gitignored)

| File | What |
|---|---|
| `vedha_30s_4x5_1080x1350.mp4` | Master (LinkedIn feed), with music |
| `vedha_30s_9x16_1080x1920.mp4` | Reels / Shorts / WhatsApp Status, recomposed (not cropped) for app overlays |
| `vedha_30s_1x1_1080x1080.mp4`, `vedha_30s_16x9_1920x1080.mp4` | Square; website / YouTube |
| `silent/*_silent.mp4` | Silent masters for every format (silent AAC track included) |
| `vedha_30s_4x5_whatsapp_720x900.mp4` | ≤ 15 MB for inline WhatsApp |
| `vedha_15s_4x5_1080x1350.mp4` + `vedha_15s_en.srt` | Cutdown: hook → seal → console → CTA |
| `vedha_30s_en.srt` | Captions generated from the same timeline as the film |
| `vedha_30s_hi_NEEDS_REVIEW.mp4` + `vedha_30s_hi.srt` | Hindi: **needs native-speaker review; do not publish unreviewed** |
| `hook_variants/` | A (door), B (the three findings), C (the promise): 3 s each |
| `poster_4x5.png`, `thumbnail_16x9.png` | Hook frame + seal + URL |
| `qa/` | `report.md`, contact sheet, safe-zone sheets, 360 px readability sheet |

## Editing

- **Copy:** `src/copy.en.json` (`src/copy.hi.json` overrides; missing keys fall back to English). Scenes contain no strings.
- **Timing:** `src/timeline.js` drives the picture, the music cues and the SRT together.
- **Layouts per format:** `src/layouts.js`
- **Colours, fonts, the seal:** `src/brand.js` (seal copied verbatim from `manager/frontend/public/brand/vedha-mark.svg`)
- **Illustrative UI data:** `src/data.illustrative.json` (RFC 5737 IPs, `.example` hostnames, each finding mapped to a shipped check)

## Needs human review before publishing

1. **The name वेधा and its gloss.** The owner set the Devanagari name to **वेधा**. The on-screen gloss "TO PIERCE THROUGH" is kept from the brief. Have a Sanskrit/Marathi speaker confirm the gloss reads right with वेधा (the verb "to pierce" is वेध, from the root *vyadh*; the Sanskrit word वेधस्, nominative वेधाः, means "creator, wise one"). To change it, edit `gloss` in `src/copy.en.json`.
2. **Product claims:** "7-day", "delivered by a partner", "office networks, not cloud" (see `claims.md`).
3. **Hindi copy:** native-speaker review.
4. **Cultural check:** Raag Bhupali / tanpura score (`MUSIC.md`); the dot lattice is a pulli-style visual reference only, with no religious iconography.
5. **Console UI** in scenes 5 and 6 is a faithful-to-the-brief replica, not a capture of the marketing site (not in this repo).
6. **Partner co-branding:** none in the film; add only with the partner's approval.
