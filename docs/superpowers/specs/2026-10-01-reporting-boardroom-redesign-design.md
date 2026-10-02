# Reporting "Boardroom Deliverable" Redesign — Design Spec

- **Date:** 2026-10-01
- **Status:** Approved design, pending implementation plan
- **Area:** `manager/frontend` reporting section (operator console + customer portal)
- **Direction:** Boardroom deliverable (premium, print/PDF-first, client-facing)

## 1. Problem & context

The reporting content model is already sophisticated — CVSS vectors, EPSS/KEV
signals, MITRE, evidence vaults, a 9-section finding model, and assessor-vs-client
modes. But the presentation reads "basic":

- **No data visualization.** `recharts@^3.8.1` is installed but used only on the
  dashboard (`components/DashboardCharts.tsx`); the report has zero charts. The one
  "chart" is a flex severity bar; the exposure "matrix" is an HTML `<table>`.
- **System fonts only** — display == body, headings are 13–16px; nothing reads as a
  premium deliverable.
- **Flat tables + generic repeated cards**, uniform small type, weak hierarchy.
- **The cover is a `<dl>` settings grid**, not a title page.
- **~150 inline `style={{}}` objects in `app/reports/page.tsx`** bypass the (solid)
  design-token system, so polish is uneven versus the cleanly-classed
  `components/report/FindingReport.tsx`.

Separately, users report **"can't export."** Investigation (see §7) shows the
export code on `main` is healthy; the failure is a **stale deploy over plain HTTP**
(client-side `crypto.randomUUID` in an older build), fixed on `main` by
`lib/uuid.ts#newId()`. One genuine code smell remains and is in scope.

## 2. Goals / non-goals

**Goals**
- Elevate the report to a premium, client-ready deliverable via a **visualization +
  typography + layout-system** pass — no content/data-model rebuild.
- Land in both surfaces through the existing shared component (`surface` prop);
  honor assessor-vs-client and print modes.
- Fix the in-scope export code smell; document the ops fix for the deploy issue.

**Non-goals (YAGNI)**
- No new backend endpoints — reuse existing scorecard / exposure / EPSS / summary.
- No interactive drill-down / cross-filtering (that is the "Operational dashboard"
  direction, explicitly not chosen).
- No PDF-generation library — keep `window.print()` + print CSS.
- Risk-over-time trend chart **only if** historical scan data is already available;
  otherwise omitted.
- Do not touch the detached `/reportsection/*` copy at the repo root (not imported
  by the app).

## 3. Current state (reference paths)

| Purpose | Path |
|---|---|
| Operator report page (1,115 lines) | `manager/frontend/app/reports/page.tsx` |
| Portal delegate | `manager/frontend/app/portal/reports/page.tsx` |
| Finding renderer (clean, class-driven) | `manager/frontend/components/report/FindingReport.tsx` |
| Export dropdown | `manager/frontend/components/report/ExportMenu.tsx` |
| Data contract (operator vs portal) | `manager/frontend/lib/reports-workspace-api.ts` |
| Download helper (robust) | `manager/frontend/lib/report/download.ts` |
| Word export | `manager/frontend/lib/report/export-word.ts` |
| Print-mode store | `manager/frontend/lib/print-mode.ts` |
| Insecure-context-safe id | `manager/frontend/lib/uuid.ts` (`newId()`) |
| Export URL builder | `manager/frontend/lib/remediation.ts` |
| Severity palette/tokens | `manager/frontend/lib/severity.ts` (`SEV_PALETTE`, `SEV_COLOR`) |
| Report CSS | `manager/frontend/styles/report-finding.css`, `app/globals.css` (`.report-*`, `.rpt-*`, `@media print`) |
| Existing recharts usage to mirror | `manager/frontend/components/DashboardCharts.tsx` |
| Export code-smell to fix | `manager/frontend/components/remediation/RemediationWorkspace.tsx` (~L188–189) |

Data is fetched with TanStack Query via `createReportsWorkspaceApi(surface)`:
engagements, findings (page of 100, risk-sorted, SLA-joined), per-status counts,
severity summary, scorecard (open-risk 0–100 + domain tiles + exploitability),
exposure matrix, and the AI report (`POST /api/reports/generate`, narrative only).
**All charts reuse these existing sources — no new fetches.**

> Implementation note: per `manager/frontend/AGENTS.md`, this is a customized
> Next.js — verify `next/font/local` and any Next API against
> `node_modules/next/dist/docs/` before writing code.

## 4. Architecture

Keep one shared implementation; the portal page keeps delegating
(`<ReportsWorkspace surface="portal" />`). Decompose the 1,115-line page into
focused, independently-testable units and move inline styles into token-driven CSS:

**New components** (`manager/frontend/components/report/`)
- `ReportCover.tsx` — title page (§5.1)
- `ExecutiveBand.tsx` — the viz band (§5.2), composes the charts below
- `charts/RiskGauge.tsx`, `charts/SeverityDonut.tsx`, `charts/ExploitScatter.tsx`,
  `charts/SlaAgingBar.tsx`, `charts/MitreHeatmap.tsx`, `charts/ExposureHeatmap.tsx`

**New lib**
- `lib/report/risk-grade.ts` — pure map of scorecard open-risk score → A–F grade

**New styles**
- `styles/report-cover.css`, `styles/report-charts.css` (token-driven; imported by
  the existing `app/reports/layout.tsx` and `app/portal/reports/layout.tsx` so the
  portal keeps the rules).

**Fonts** — self-hosted via `next/font/local` under `app/fonts/` (no external CDN,
for CSP/offline safety), wired to CSS vars `--font-display` / `--font-body`.

Each unit has one job, takes typed props (its slice of the report data), and renders
no data-fetching of its own — fetching stays in the page/workspace layer.

## 5. Detailed design

### 5.1 Cover / title page (`ReportCover`)
- Confidentiality banner (e.g. "CONFIDENTIAL — prepared for {client}").
- Engagement name, client, assessment window, assessor, scope summary, optional
  logo slot (falls back to a wordmark if none).
- **Risk grade A–F**, large and centered, derived from the existing scorecard
  open-risk score via `risk-grade.ts`. Both the letter and the 0–100 score are
  shown. Default thresholds (calibratable, not a placeholder):
  `A 0–9 · B 10–24 · C 25–44 · D 45–69 · F 70–100`, where higher score = more open
  risk. The score→grade direction is confirmed against `lib/severity.ts` / scorecard
  semantics during implementation.
- Severity-count strip (critical / high / medium / low).
- Print: the cover owns page 1 (`break-after: page`).

### 5.2 Executive viz band (`ExecutiveBand`, recharts)
Rendered once, directly under the cover, as the scannable executive summary. All
charts: SVG (print-safe), themed via `SEV_PALETTE` / CSS severity tokens,
light/dark aware (print forces light through the existing print-mode store), and
**given explicit width/height for print** (don't rely on `ResponsiveContainer`
alone in the print path).

| Chart | Source | Encoding |
|---|---|---|
| Risk gauge | scorecard open-risk 0–100 | radial gauge, grade color |
| Severity donut | severity summary counts | severity palette |
| "Fix-first" scatter | findings `epss` × `riskScore` | x=EPSS, y=risk, color=severity, size=CVSS; KEV flagged |
| SLA aging bar | findings SLA state/age buckets | stacked bar by severity |
| MITRE heatmap | findings `mitre[]` | tactic × technique grid, intensity by count/severity |
| Exposure heatmap | existing exposure matrix | severity × exploitability colored grid (replaces the HTML table) |

Each chart renders a clear empty state when its data is absent (e.g. no MITRE
mappings → omit the heatmap, don't render an empty grid).

### 5.3 Finding cards + tables
- Keep the 9-section `FindingReport` model. Add a severity-colored spine/accent and
  a compact at-a-glance header row: CVSS-vector chip, EPSS, KEV, SLA state,
  confidence. Collapsible on screen; **auto-expanded in print** (existing
  `usePrintMode`). Client mode continues to omit internal-only sections
  (evidence, reproduction, confidence, readiness nags).
- Tables (`.report-table`, `.vf-table`): zebra striping, sticky headers on screen,
  severity row emphasis, larger type; print-clean (no sticky, full borders).

### 5.4 Typography
- Self-hosted via `next/font/local`: **display serif** (cover + section headings) +
  **sans body** + existing **mono** for evidence. Default faces: Source Serif 4
  (display) and Inter (body) — both OFL, self-hostable; mono unchanged. Wire to
  `--font-display` / `--font-body` so the rest of the token system picks them up.
- Establish a real type scale: commanding cover title, confident section heads,
  readable body. Replaces today's "everything is 8.5–16px" flatness.

### 5.5 Token / inline-style cleanup
- Replace the ~150 inline `style={{}}` in `app/reports/page.tsx` with token-driven
  classes in the new/updated report CSS. Match the clean idiom of `FindingReport.tsx`.
  This is both a polish fix and what makes the page systematic and maintainable.

## 6. Operator vs portal / print behavior
- One component, `surface` prop selects transport (`reports-workspace-api`) and
  shell (`PageShell` vs `PortalShell`); portal engagement is pinned server-side.
- `FindingReport` assessor-vs-client mode is preserved; **client/PDF mode gets the
  full formal treatment** and omits internal sections.
- Print path reuses `lib/print-mode.ts` (forces light theme, opens cards, hides
  filters) and the existing `@media print` 100vh-release fix.

## 7. Export fix

**In scope (code):** `RemediationWorkspace.tsx` still uses a bare
`<a href={exportUrl} download>`, which silently saves a 401/500 error body *as* the
file. Replace it with a button that calls `lib/report/download.ts#downloadFile()`
(same robust path Reports uses: credentialed fetch, one refresh on 401, readable
errors), matching the Reports export UX.

**Out of scope (ops, documented):** the live "can't export" is a **stale deploy**.
`main`'s export is healthy (25 tests pass; `newId()` fallback works over plain HTTP),
but `docs/STATUS.md` shows prod 5 commits behind, and `.env` targets a plain-HTTP box
where an older build's `crypto.randomUUID` throws client-side.
**Resolution: redeploy current `main`** to that box and/or serve HTTPS (the
`./setup-https.sh` wizard), then verify all four formats export.

## 8. Error handling / edge cases
- Each chart degrades to an explicit empty state; absent data → omit the chart, never
  render an empty frame.
- No engagement selected / loading → existing skeleton/disabled states unchanged.
- Fonts: `next/font/local` with `display: swap`; never block render on a font.
- Charts must not break print pagination (explicit print dimensions; avoid 100vh).
- Redaction (`redact()`) in evidence is unchanged and still applied.

## 9. Testing
- `risk-grade.ts`: unit test the score→grade boundaries.
- Each chart: render with sample data (assert severity color mapping) + empty-data
  fallback test.
- Print-mode snapshot: cards expand, filters hidden, cover breaks to its own page.
- Client-mode test: internal-only sections omitted.
- Export: extend the existing 14 frontend export tests; add a `RemediationWorkspace`
  test asserting it calls `downloadFile()` (not a bare anchor).
- Manual pass: operator screen, portal screen, printed PDF, light + dark.

## 10. Risks & open questions
- **Score→grade direction** — confirm scorecard open-risk polarity during impl
  (default assumes higher = worse).
- **recharts in print** — set explicit print dimensions; verify in a real PDF.
- **Custom Next.js** — verify `next/font/local` against `node_modules/next/dist/docs/`.
- **Bundle size** — two self-hosted fonts + recharts in the report route; acceptable
  (recharts already a dependency), verify route bundle after.

## 11. Rollout
- Feature branch `feat/reporting-boardroom-redesign`.
- Incremental order: typography + token/inline-style cleanup → `ReportCover` →
  `ExecutiveBand` + charts → card/table elevation → Remediation export fix → tests.
- Update `docs/STATUS.md` (done/pending/needs-you/change log) when landed, per
  project convention.
