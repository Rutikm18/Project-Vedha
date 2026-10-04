# Vedha marketing workspace

Deliverables for the **Vedha Action Plan** (4 Oct 2026, @Hemang), one folder per task. Everything here is a **draft for a founder to review**: nothing is sent, published or signed from this repo.

Name: **Vedha (वेधा)**. Use this Devanagari spelling everywhere it appears.

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
| 12 | P0 | Open Door share card | `12-open-door-card/` (page + OG image) | Built (deploy to site) |
| 13 | P1 | CERT-In 15 controls: verified mapping | `13-certin-controls/MAPPING.md` + `mapping.csv` | Done (verify control order in PDF) |
| 14 | P1 | WhatsApp channel with opt-in | `14-whatsapp-channel/` (SETUP.md, icon, poster builder, consent log) | Ready to create (needs the phone) |
| 15 | P1 | "CERT-In's 15 controls, accurately" guide + one-page PDF | `15-certin-guide/` (index.html, PDF; built from #13's CSV) | Built (publish; verify control order) |
| 16 | P1 | Partner Zero checks #1 + #2, hours logged | `16-partner-zero-checks/` (runbook, debrief format, hours_log.csv) | Ready to run |
| 17 | P1 | Objection sheet | `17-objection-sheet/OBJECTIONS.md` | Drafted |
| 18 | P1 | 15 Controls Awareness Poll | `18-awareness-poll/POLL.md` | Ready to build the form |
| 19 | P1 | 10 Jugaad & Sons items + preview | `19-jugaad-and-sons/` (10 illustrated cards) | Built (send preview) |
| 20 | P1 | Shadowserver data + licence | `20-shadowserver/REQUEST.md` | Email ready |
| 21 | P1 | Recruit 15 Vedha Village members | `21-vedha-village/RECRUIT.md` | Ready |
| 22 | P1 | Launch Jugaad & Sons | `22-jugaad-launch/LAUNCH.md` (Mon–Thu schedule, targets) | Planned |
| 23 | P1 | Partner Kit v1 + Founding 10 page | `23-partner-kit/` (KIT.md, founding-10.html) | Built (fill the offer) |
| 24 | P1 | Doors Closed certificate | `24-doors-closed-certificate/` (A4 PDF template) | Built |
| 25 | P1 | Diwali Safai card EN + HI | `25-diwali-safai-card/` (partner-branded builder) | Built (Hindi review) |
| 26 | P2 | DPDP explainer | `26-dpdp-explainer/DPDP_EXPLAINER.md` | Draft for counsel |
| 27 | P2 | Poll results + 5 journalist pitches | `27-poll-results-press/PRESS.md` | Templates (needs poll data) |
| 28 | P2 | Village kickoff + Open Door Clinic | `28-village-kickoff/RUNSHEET.md` | Ready |
| 29 | P2 | Open Door Report Stage 1 | `29-open-door-report/` (8-page PDF template, data-driven charts) | Template (data pending) |
| — | Weekly | Scoreboard, Signal/Noise, retro | `weekly/SCOREBOARD.md` | Ready |
| — | Extra | Visiting card system (founder + partner, 2 sizes) | `cards/` (DESIGN.md, mockup, print PDFs in `cards/out/`) | Built (fill people.json, print proof) |

## Rendering assets

```bash
cd marketing && npm install
node 01-c0c0n/build.mjs        # each task folder has its own build script where it makes images or PDFs
```

Uses the pre-installed Chromium; fonts are local (OFL), and the QR codes are generated offline (`qrcode`).
