# Vedha marketing workspace

Deliverables for the **Vedha Action Plan** (4 Oct 2026, @Hemang), one folder per task. Everything here is a **draft for a founder to review**: nothing is sent, published or signed from this repo.

Rules followed throughout (from the film brief and claims register):
- No guarantees ("secure", "protected", "100%", "compliant", "certified").
- No unsourced numbers. Every statistic carries its source, its date and the exact credit line.
- Product claims only where the code or `NETWORK_VA_USE_CASES.md` supports them. Owner-confirmed scope: **no backup, password or patching checks**.
- `[CONFIRM: …]` marks a fact only a founder can supply. Never publish with one left in.

## Tracker

| # | Pri | Task | What's here | Status |
|---|---|---|---|---|
| 1 | P0 | c0c0n go/no-go | `01-c0c0n/DECISION.md`, `partner-zero-card.png/.pdf` (print 3.5×2 in) | Ready for decision |
| 2 | P0 | Founder headlines + first post (T1) | `02-founder-linkedin/LINKEDIN.md` | Drafted (add names) |
| 3 | P0 | 50 partner prospects | `03-partner-prospects/prospects.csv` (55) + README | Drafted (verify list) |
| 4 | P0 | Replace stale site stats | `04-site-stats/STATS.md` | Drafted (copy exact wording from reports) |
| 5 | P0 | Signal/Noise #1 (DBIR) | `05-signal-noise-1/SIGNAL_NOISE_1.md` (LinkedIn, email, WhatsApp) | Drafted |
| 6 | P0 | Analytics + "How did you hear about us?" | `06-analytics/` (ANALYTICS.md + tested heardFrom.js) | Drafted (apply in site repo) |
| 7 | P0 | Price list + partner margin model | `07-pricing/margin_model.xlsx` (example numbers) | Ready for your numbers + sign-off |
| 8 | P0 | Deck slide 8 + competitive analysis pricing | `08-deck-pricing/SLIDE_8.md` | Template (fill after #7) |
| 9 | P0 | Data-use clause (for counsel) | `09-data-use-clause/DATA_USE_CLAUSE.md` + T7 line | Draft for counsel |
| 10 | P0 | Partner Zero messages (T3) | `10-partner-zero-messages/MESSAGES.md` | Drafted (fill the offer) |
| 11 | P0 | Discovery call script (T4 + unprompted recall) | `11-discovery-calls/CALL_SCRIPT.md` | Drafted |
| 12 | P0 | Open Door share card | `12-open-door-card/` | Not started |
| 13–29 | P1/P2 | See the action plan | Folders created as each starts | Not started |

## Rendering assets

```bash
cd marketing && npm install
node 01-c0c0n/build.mjs        # each task folder has its own build script where it makes images or PDFs
```

Uses the pre-installed Chromium; fonts are local (OFL), and the QR codes are generated offline (`qrcode`).
