# The score: the emotion it is built to create, and why

An original piece, synthesized in code by `music.mjs`. It uses no samples, no stock or licensed music and no AI-generated audio, and the same code always writes the same file. It's normalised to **-16 LUFS, true peak ≤ -1.5 dBTP**. Silent masters are still delivered for every format (`out/silent/`).

## The emotion we want: curiosity → anticipation → excitement → confidence

This is Vedha's first film. People should finish it **energised and sure**, not scared. In Russell's circumplex model of affect, the target is the **high-arousal, positive-valence** corner (excited, alert, confident), not the high-arousal, negative corner (tense, afraid). Security marketing usually goes for the second. We deliberately don't.

| Principle (research) | What it says | How the score uses it |
|---|---|---|
| **Anticipation releases dopamine before the reward** (Salimpoor et al., *Nature Neuroscience* 2011) | The caudate releases dopamine while we *anticipate* a musical peak; the nucleus accumbens releases it *at* the peak | Two deliberate build-ups (riser + accelerating tabla roll + a beat of silence) before the two most important moments: the strike (9.4 s) and "Verified" (22.5 s) |
| **Expectation → tension → reward** (Huron, *Sweet Anticipation*, ITPRA theory) | Tension before an expected event makes the resolution feel better (contrastive valence) | The "open phrase" climbs S R G P D and stops on Dha, unresolved. It only resolves to high Sa when the fix is verified |
| **Tempo drives arousal, mode drives mood** (Husain, Thompson & Schellenberg, *Music Perception* 2002) | Faster tempo raises arousal; major mode lifts mood, independently | A 110 bpm groove from the strike onward, in Raag Bhupali. Its notes (S R G P D) sit on a bright, major-sounding pentatonic scale with no minor intervals |
| **Peak-end rule** (Kahneman & Fredrickson, 1993) | We remember an experience by its most intense moment and its end, not its average | The single biggest moment is "Verified". The end is a clean, confident sonic logo that rings out, never a fade-down or a sting of fear |
| **Sonic branding lifts recall and trust** (Audacy × Veritonic, 2023) | Ads with a sonic logo had higher recall and were rated more trustworthy | A three-note Vedha logo (Sa → Pa → high Sa, a rising fifth then a fourth: open, confident, complete), heard four times: as an unfinished question in the hook, in full at the strike, at the peak and at the end |
| **Audio-visual synchrony** | Sound that lands with the picture reads as intentional and holds attention | A note for **every device the scan finds**, a weighted hit for each thing that matters, one bell per checkpoint, and the groove's beat 24 lands exactly on "Verified" |

## The arc, second by second (times from `src/timeline.js`)

| Time | Picture | Music | Feeling |
|---|---|---|---|
| 0.0–3.0 | Lattice blooms; the door opens | Pad breathes in; the logo asks a question (Sa → Pa, unfinished); one held Re as the door opens | **Curiosity** |
| 3.2–4.9 | The scan finds 16 devices | One rising pluck per device found | **Discovery**: there's more here than I knew |
| 4.0 / 5.7 / 7.3 | Accounts PC, client files, billing data light up | A tabla bass stroke + pluck on each; a shaker, then a bass pulse join | **Stakes rising**: these are mine |
| 7.8–9.4 | The three things hold | The open phrase climbs and stops on Dha; riser + accelerating roll; a breath of silence | **Anticipation** (dopamine before the reward) |
| **9.4** | **The seal strikes** | **Impact + the full logo; the groove starts (half-time, then full)** | **Arrival, energy** |
| 12.7–14.3 | Four checkpoints | One bright bell per checkpoint, climbing, on the beat | Momentum, order |
| 16.0 | The partner | A warm flute line joins | Trust: someone with you |
| 18.0–21.5 | Findings, then evidence | The groove drives; small accents on Find and Prove | Focus, progress |
| 21.5–22.4 | The fix; hold-to-verify fills | Four on the floor, riser, roll, the flute swells on Dha… then a beat of silence | **Peak anticipation** |
| **22.5** | **Verified: teal, door heals, grade improves** | **Impact; the open phrase resolves to high Sa; the logo rings in octaves; the groove returns fuller** | **The peak**: relief and triumph |
| 25.3–26.1 | Report: three doors close | Descending plucks; a quiet bell | Satisfaction |
| 27.4–30.0 | Book your 7-day check | Final hit + the full logo; the chord rings out; still frames are quiet | **Confidence** (a strong end) |

## Why it stays respectful

- No minor keys, alarms, sirens, glitches or "hacker" sounds. The impacts are warm and low-passed: big, not threatening.
- Indian identity comes from the raga, the tabla theka (*ge*, *na*) and the bansuri-like flute, used as musical language, without religious text or chant.
- **Cultural review:** a musician familiar with Hindustani music should listen once. Bhupali is traditionally an evening raga; here it's used for its brightness, not its time of day.

## Sources

- Salimpoor et al. (2011), *Anatomically distinct dopamine release during anticipation and experience of peak emotion to music*, Nature Neuroscience: [summary](https://www.sciencedaily.com/releases/2011/01/110112111117.htm)
- Huron (2006), *Sweet Anticipation: Music and the Psychology of Expectation*, MIT Press: [book](https://mitpressbookstore.mit.edu/book/9780262582780); [ITPRA overview](https://www.frontiersin.org/articles/10.3389/fpsyg.2015.00079/full)
- Husain, Thompson & Schellenberg (2002), *Effects of musical tempo and mode on arousal, mood, and spatial abilities*, Music Perception 20(2): [paper](https://research.bond.edu.au/en/publications/effects-of-musical-tempo-and-mode-on-arousal-mood-and-spatial-abi/)
- Fredrickson & Kahneman (1993), duration neglect and the peak-end rule: [paper](https://bear.warrington.ufl.edu/brenner/mar7588/Papers/fredr-kahneman-jpsp1993.pdf)
- Audacy × Veritonic (2023), audio ad effectiveness and sonic branding: [press release](https://www.businesswire.com/news/home/20230213005383/en)
