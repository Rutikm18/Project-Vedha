# Phase 0: recon

> **Update (owner feedback):** the Devanagari is **वेद्या**, not वेध, and the film now focuses on the assets owners pay to protect (see `CHECKPOINTS.md`). The music is an original in-code score (see `MUSIC.md`).

Repo inspected: `Rutikm18/Project-Vedha` (the product: probe + manager). Recon date: 2026-10-04.

## Conflicts between the brief and the repo (the repo wins)

1. **There is no marketing site in this repo.** `public/index.html`, `public/story/index.html`, `vercel.json` and `public/favicon.svg` do not exist. No other repo this account can reach holds them either. As a result:
   - **Terrain algorithm:** none to copy. The film's lattice and contours are new code: a seeded value-noise field with marching squares in `src/film.js`. **Check them against the live vedhasec.com hero.**
   - **Story page copy ("Open Door"):** not available. The film's terms (door, path, pierce) come from the brief only.
   - **Marketing console (4 tabs, hold-to-verify about 600 ms, pupil fills teal, regenerating report):** not in this repo. The product dashboard (`manager/frontend`, Next.js) is a different UI and needs the full backend and database to show data. **The console in the animatic is a placeholder wireframe**, built only from the tab names, controls and states the brief lists.
2. **Fonts.** The product uses **system fonts only** (`docs/design/design-system.md`: "No external webfonts"). Geist, Instrument Serif and Tiro Devanagari Hindi don't appear anywhere in the repo. The film uses them as the brief asks, loaded locally from `@fontsource` packages under OFL 1.1 (see THIRD_PARTY.md). **Confirm that the website really uses them.**
3. **Blue on Night.** The repo's mark SVG switches to `#60A5FA` in dark mode, and so does the dark `--accent`. On Night the film uses `#60A5FA` for the seal and route. `#1D4ED8` is used on Day, including the CTA. Pure `#1D4ED8` on `#060B14` is about 2.6:1, too dim for the mark.
4. **Night colour.** The product's dark canvas is `#0F1117`, not `#060B14`. The film keeps the brief's `#060B14` (the site's, per the brief) and uses the product's dark panel colours inside the console.
5. **Text colours on Day.** The product uses `#0F172A` as primary text. The brief asks for `#060B14`. The film uses `#060B14` for captions and the product tokens inside the console.
6. **Branch.** The brief says `video/vedha-30s`; this session must push to `claude/cool-cannon-l598dk`. All work lives there.
7. **TEAM_SIZE was left blank (`__`).** The brief says to use Playwright + ffmpeg when unsure, so the film uses that pipeline. Remotion is not used.

## Extracted tokens

| Token | Value | Source |
|---|---|---|
| Blue (action) | `#1D4ED8` light, `#60A5FA` dark | `globals.css` `--accent`; `vedha-mark.svg` |
| Teal (verified only) | `#0F766E` light, `#5EEAD4` dark | `--nominal-color`: "reserved for resolved state only" |
| Purple (AI only) | `#7C3AED` | `--machine-color`, **not used** |
| Day canvas | `#F3F6FA` | `--bg-root` (light) |
| Panel / border | `#FFFFFF` / `#DCE3EC` | `--bg-panel`, `--border-subtle` |
| Dark panel | `#161820`, surface `#1C1F28` | dark tokens |
| Ease out | `cubic-bezier(.16,1,.3,1)` | `--ease-out` (matches the brief) |

## The seal

From `manager/frontend/public/brand/vedha-mark.svg`, viewBox 0 0 100 100, used verbatim in `src/brand.js`:

- body with V-notch: `M28 6H39L50 24L61 6H72A22 22 0 0 1 94 28V72A22 22 0 0 1 72 94H28A22 22 0 0 1 6 72V28A22 22 0 0 1 28 6Z`
- eye (even-odd cut-out): `M18 53Q50 21 82 53Q50 85 18 53Z`
- pupil: circle at (50, 53), r = 11

The animation only interpolates parameters of this path. The notch depth goes from 0 to 18 and the eye opening from 0 to 1. At rest, every frame draws the exact repo geometry.

## Grade scale (real)

`manager/backend/app/services/posture.py`: `_GRADE_BANDS = ((90,"A"),(75,"B"),(55,"C"),(35,"D"),(0,"F"))`. Colours come from `GRADE_VAR` in `manager/frontend/lib/portal-client.ts`: B uses `--nominal-color` (teal) and C uses `--sev-medium-color`. The film shows **C → B** after the fix, as illustrative data.

## Product facts: what the repo supports

| Brief fact | In repo? |
|---|---|
| 7-day check | Partly. The operator plan panel has POC presets `[7, 14, 30]` days (`components/customers/PlanPanel.tsx`), and the default is 14. Nothing names it a "7-day network health check". |
| Delivered through local partners | **Not found.** |
| Office networks, not cloud | **Not found** as copy. The probe architecture (runs inside the client network) fits it. |
| वेध = "to pierce through" | **Not found.** |
| Console tabs, hold-to-verify | **Not found** (they are marketing-site features). |
| info@vedhasec.com, vedhasec.com | Domain found in `docs/STATUS.md`. Email not found. |

## Assumptions

- The website brand (fonts, Night `#060B14`, lattice hero) matches the brief, though I can't verify it here.
- The illustrative findings (printer admin page, camera default login, router password) match what the product detects. The detection engine has `default_creds_catalog.py` and posture rules, so this seems plausible.
- 540×675 animatic is padded to 540×676: H.264 4:2:0 needs even dimensions.

## Blocking questions (none block the animatic)

1. Can you add the **website repo** (or `public/index.html`) to this session? I need it to copy the real terrain algorithm, the console DOM and CSS for scenes 5 and 6, and the story copy. Without it, scenes 5 and 6 stay a faithful-to-the-brief replica, flagged as such.
2. **TEAM_SIZE?** I defaulted to Playwright + ffmpeg, which works either way.
3. Can you confirm the **"7-day" and "partner"** positioning? The repo's POC default is 14 days.
