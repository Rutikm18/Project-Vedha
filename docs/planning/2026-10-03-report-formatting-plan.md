# Report formatting and presentation — plan (3 Oct 2026)

## Why

The reporting pipeline is accurate but reads like a database record, not a security report.

| Surface | What a reader sees today |
| --- | --- |
| Operator report (`/reports`) | ~7,000 px per finding. Every field of the canonical record is shown, so "Not recorded" appears dozens of times per finding and the same gap code is listed once per finding with a chip of every affected UUID. The cover shows schema internals (snapshot kind, schema version) and there is no overall rating, chart, findings table or remediation plan. |
| PDF / Word export | One line per field. Whole objects are printed as JSON (`Summary: {"total_findings":8,…}`) in a bitmap monospace font (Unifont). No cover, contents, tables, colour, header or footer. |
| Excel export | Correct sheets, but no column widths, frozen header, filter or severity colour. |

## What good looks like (research)

Public reports from NCC Group, Cure53, Bishop Fox and CREST-style deliverables share one shape, and the reporting guidance (CREST, PTES, NIST SP 800-115) asks for the same parts:

1. **Cover and document control**: client, scope, period, version, classification, status; approval trail.
2. **Executive summary** for non-technical readers: an overall risk rating, how many issues of each severity, the top risks in plain words, and progress.
3. **Scope and methodology**: what was tested and when, how, with what, and the limitations.
4. **Findings summary table**: one row per issue (ID, title, severity, CVSS, asset, status).
5. **One consistent page per finding**: severity banner, key facts (CVSS, CVE/CWE, asset, status), description, impact, evidence, steps, remediation.
6. **Remediation roadmap** by priority window, with owners and deadlines.
7. **Retest and closure** status per finding (verified fixed, risk accepted, open).
8. **Appendices**: risk-rating definitions, evidence integrity and provenance, compliance mapping, record gaps.

The deep audit record (run IDs, hashes, lifecycle, provenance) is valuable, but it belongs in an appendix or behind a disclosure, not inline in every finding.

## Principles kept from the current design

- **No fabrication.** Only recorded values and disclosed deterministic derivations (counts, highest-open-severity rating, SLA-based windows). No generated narrative is added by this work.
- **Absent stays absent.** Unrecorded fields are omitted from the reading view and summarised once ("Not recorded: root cause, preconditions") instead of repeated.
- **Honesty markers stay.** Draft status, "derived context — not assessed / not a certification" and the reporting-clock caveat remain, stated once per section.
- **Masking everywhere.** Every string goes through the existing `redact`/`maskText`; `raw` payloads never render.

## Design

One presentation layer, four renderers.

- `lib/report/presentation.ts` (pure, unit-tested): severity order and palette, finding refs (`F001`) in presentation order (severity, then open first, then risk), overall rating, severity and status counts, key metrics, top risks, remediation roadmap buckets, present-only finding facts and narrative sections, readable formatting of recorded JSON (lists and key/value lines instead of JSON), de-duplicated gap inventory.
- **PDF** (`lib/report/export-pdf.ts`): IBM Plex Sans and Mono (OFL), with the existing Unifont as a per-glyph fallback so CJK and other scripts still extract correctly. Cover with risk badge and draft watermark, document control, contents with page numbers and PDF bookmarks, executive summary with KPI tiles and severity chart, findings table, one section per finding with a coloured severity band and facts table, evidence excerpts in code blocks, roadmap, closure register, compliance, appendices. Running header and footer with page X of Y and classification.
- **Word** (`lib/report/export-docx.ts`): real styles (Title, Heading 1–3, table style, code), cover page, contents field, header and footer with page numbers, the same tables with severity shading.
- **Excel**: column widths, frozen and filtered header row, severity fills, and an executive block on the Overview sheet. Sheet names and order unchanged.
- **Operator web report**: cover with rating and severity bars; executive summary with KPI tiles, distribution and top risks; findings summary table; finding cards that show recorded content only, with the full audit record (metadata grid, provenance, verification, action tracking, mappings, lifecycle, gaps) in a collapsed "Audit record" disclosure; remediation roadmap; compact closure register; appendix with the de-duplicated gap inventory and document-control facts. Print gets a choice: customer copy (audit record collapsed) or full record.

## Tasks

1. Presentation layer and tests.
2. Fonts: add Plex Sans/Mono WOFF files and licence under `public/fonts`.
3. PDF renderer (layout kit: text runs with fallback font, tables with repeated headers, callouts, charts; then sections), with a text trace for tests.
4. Word renderer.
5. Excel styling.
6. Operator web report redesign (and print styles).
7. Update tests to the new structure, keeping masking, disclaimer and completeness invariants.
8. Visual check: render PDF and DOCX pages to images; screenshot the web report; iterate.
9. Full test, lint and type check; STATUS row; commit and push.
