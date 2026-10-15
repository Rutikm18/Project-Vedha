# Report finding selection — design

**Date:** 2026-10-15
**Surface:** Operator console → Reports (the canonical live draft).

## Goal

Let an operator choose a subset of an engagement's findings and have **only those
findings** drive the on-screen report, both print modes, all four exports
(PDF / Word / Excel / CSV), and the AI draft generation. Metrics are **recomputed**
for the subset so the deliverable is genuinely a report of just those findings.
Selection is **per-session** (resets on reload / engagement change) — matching the
page's existing "live, non-persisted operator draft" model.

Decisions (confirmed with owner): scope = everything incl. AI; metrics = recompute;
persistence = per-session.

## Key architectural insight

The whole report hangs off one object: `ReportDocument` (`lib/report/report-document.ts`).
- The renderer (`CanonicalReportDocument`) and the four export builders
  (`lib/report/export-*.ts`) all derive from it.
- Print just paginates the already-rendered `.rr-report` DOM — so if the rendered
  document is scoped, print is scoped for free.
- The renderer consumes **backend-computed** aggregates directly:
  `report.summary.*` (`CanonicalReportDocument.tsx:1230`), `report.readiness.*`,
  `report.compliance_rollup.*`. These are built by `_summary` / `_readiness` /
  `_compliance_rollup` in `backend/app/services/report_document.py`, and the backend
  groups issues by **asset+port** while the frontend `issueGroups` groups by
  **severity+title**. Reproducing that aggregation in TypeScript would duplicate
  non-trivial logic and risk drift.

**Therefore: scope at the backend builder.** A `finding_ids` filter on
`load_report_document` lets `build_report_document` recompute summary, readiness,
compliance, and the findings list consistently. Every surface then consumes the
already-consistent scoped document. No TS reimplementation of aggregation.

## Data flow

```
Report page: fetch FULL report-document (picker list + default view)
           + fetch SCOPED report-document?finding_ids=… (when a strict subset is active, debounced)
  render  → CanonicalReportDocument(displayReport)   (print inherits the scoped DOM)
  export  → POST /api/reports/export {format, engagementId, findingIds}
             → BFF re-fetches report-document?finding_ids=… → buildReportExport (unchanged)
  AI      → POST …/ai-report/generate {selected_finding_ids}
             → _run_generation filters the findings query by id
```

`finding_ids` is sent as a comma-separated list of the **included** ids, and only
when a strict subset is selected (all-selected ⇒ param omitted ⇒ full report,
cached). Practical cap: suited to typical engagement sizes; very large selections
are out of scope for v1.

## Changes

### Backend (3 files)
1. `app/services/report_document.py` — `load_report_document(…, finding_ids: set[UUID] | None = None)`;
   filter `finding_rows` to the set right after it is loaded. Everything downstream
   recomputes.
2. `app/routers/report_document.py` — accept `finding_ids` query param (comma-separated
   UUIDs, invalid/blank ignored); parse to a set and pass through.
3. `app/routers/ai_report.py` — `GenerateRequest.selected_finding_ids: list[UUID] | None`;
   apply `.where(Finding.id.in_(…))` to the per-finding query in `_run_generation`.

### Frontend (7 files + CSS)
4. `app/api/engagements/[id]/report-document/route.ts` — forward `finding_ids` query.
5. `app/api/engagements/[id]/ai-report/generate/route.ts` — forward `selected_finding_ids`.
6. `app/api/reports/export/route.ts` — allow `findingIds` (UUID[]); forward as
   `finding_ids` when present and non-empty.
7. `lib/report/selection.ts` (NEW, pure + unit-tested) — selection helpers
   (serialize/sort key, toggle, bulk by-severity, derive subset/all flags).
8. `components/report/FindingSelectionPanel.tsx` (NEW, `no-print`) — collapsible panel:
   count + Select all / Clear + per-severity toggles + per-finding checkbox rows
   (ref, severity, title, asset, status).
9. `components/report/ReportExportMenu.tsx` — accept `findingIds`; send in POST body.
10. `components/report/AiReportPanel.tsx` — accept `selectedFindingIds`; send in body;
    cap by selected count.
11. `app/reports/workspace.tsx` — selection state (init to all; reset per engagement),
    debounced scoped query, `displayReport`, panel, scope banner, disable actions when
    nothing selected.
12. `styles/report-selection.css` (NEW) imported in `app/reports/layout.tsx`.

### Tests
- `tests/report-selection.test.ts` — selection helpers + export route forwards
  `finding_ids` + report-document route forwards it.
- `backend/tests/test_report_document_selection.py` — `load_report_document(finding_ids=…)`
  scopes findings and recomputes summary; endpoint parses the param; AI generate
  accepts `selected_finding_ids`.

## Out of scope (v1)
- Portal reports (`app/portal/reports/*`) — separate renderer/model; follow-up.
- Persisted / shared selection.
- AI executive-summary narrative stays whole-engagement; per-finding write-ups honor
  the selection (the concrete deliverable).
- `coverage_sheet` stays engagement-level — it describes what the scan checked, which
  is independent of which findings you choose to report.
