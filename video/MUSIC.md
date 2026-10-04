# The score: what it means and how it is made

An original piece, synthesized in code by `music.mjs`. It uses no samples, no stock or licensed music and no AI-generated audio, and the same code always writes the same file. It's normalised to **-16 LUFS integrated, true peak ≤ -1.5 dBTP**. A silent master is still delivered for every format (`out/silent/`).

## The idea

The music tells the same story as the picture, so it still makes sense with eyes closed.

- **Raag Bhupali** (S R G P D, a pentatonic scale with no Ma and no Ni). It is calm, open and traditionally associated with the evening, and every note in it is consonant. Nothing in the scale sounds like an alarm, which fits the brief: calm, exact, respectful, never frightening. It's familiar to an Indian ear without being a cliché.
- **Tanpura drone on Sa (D) and Pa.** This is the "ground" of Indian music: the office, steady underneath everything.
- **The open phrase and the closed phrase.** When the path forms, a flute climbs **S R G P D and stops on Dha**, one step short of home. The ear waits for a resolution that doesn't come. That unresolved note *is* the open door. When the fix is verified, **the same phrase returns and lands on high Sa**: the door is closed and the melody is complete. This is the musical version of the film's visual rhyme, where the gap opens in the hook and the same gap heals at the fix.

## Cue sheet (times come from `src/timeline.js`)

| Time | Picture | Music | Meaning |
|---|---|---|---|
| 0.0–3.0 | Lattice blooms; one dot pulses; the door opens | Tanpura fades in; a faint high ping on the pulse; a single flute **Re** as the gap opens, left hanging | A quiet office, and a question nobody has asked |
| 3.0 / 4.0 / 5.0 | Remote login, password, backup appear | Three soft plucks: **Ga, Pa, Dha** | Small things, each adding up |
| 7.0–8.6 | The route draws through to the accounts | Flute climbs **S R G P D**, stops on **Dha** | The path is real, and unresolved |
| 9.4 | The seal's V-notch strikes | A low, round **thock** with a low Sa | Vedha pierces through |
| 10.6 | "A 7-day network health check." | Flute glides Re → **Ga** | Warmth: this is help, not a threat |
| 12.8–13.8 | Six checkpoints appear | Six plucks climbing **S R G P D Ṡ**, one per checkpoint | Methodical: each one counted |
| 16.0 | "Delivered by a partner you already trust." | A second flute line, **Ga → Pa** | Someone joins you |
| 18.0–22.4 | Console finds and proves | A steady soft pulse at 90 bpm | Work being done, unhurried |
| 21.6–22.4 | Partner ticks the fix; hold-to-verify fills | Tick; flute swells on **Dha** | The held breath |
| **22.5** | **Verified**: route snaps, door heals, teal | The path phrase returns and **resolves to high Sa**; two-note bell **Pa → Sa** | The door is closed, and the melody is complete |
| 25.3–26.1 | Three doors close in the report; "Verified" | Descending plucks **Dha, Pa, Ga**; a quiet bell | Things settling |
| 27.6–28.2 | CTA | Bhupali's signature cadence **Ga Re Sa**, landing with the drone | Home |
| 29.0–30.0 | Last frames held still | Rings out to silence | Thumbnail-safe ending |

## Cultural review

Raag Bhupali and the tanpura are used respectfully as a musical language, with no religious text or chant. A musician familiar with Hindustani music should listen once before release. It's on the "needs human review" list.
