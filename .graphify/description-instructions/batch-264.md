# Node Description Batch 265 of 380

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "reports_page_executivetab": "ExecutiveTab()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L411 | neighbors=[page.tsx]
- "reports_page_fieldlabel": "FieldLabel()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L246 | neighbors=[page.tsx]
- "reports_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L41 | neighbors=[page.tsx]
- "reports_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L51 | neighbors=[page.tsx]
- "reports_page_findingstab": "FindingsTab()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L533 | neighbors=[page.tsx]
- "reports_page_findingstable": "FindingsTable()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L177 | neighbors=[page.tsx]
- "reports_page_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L52 | neighbors=[page.tsx]
- "reports_page_findingtable": "FindingTable()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L134 | neighbors=[page.tsx]
- "reports_page_fmtdatetime": "fmtDatetime()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L68 | neighbors=[page.tsx]
- "reports_page_frameworks": "frameworks" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L55 | neighbors=[page.tsx]
- "reports_page_heat_style": "HEAT_STYLE" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L322 | neighbors=[page.tsx]
- "reports_page_horizon_style": "HORIZON_STYLE" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L376 | neighbors=[page.tsx]
- "reports_page_matrix_col_axis": "MATRIX_COL_AXIS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L314 | neighbors=[page.tsx]
- "reports_page_matrix_cols": "MATRIX_COLS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L313 | neighbors=[page.tsx]
- "reports_page_matrix_heat": "MATRIX_HEAT" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L316 | neighbors=[page.tsx]
- "reports_page_matrix_rows": "MATRIX_ROWS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L312 | neighbors=[page.tsx]
- "reports_page_metric": "Metric()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L95 | neighbors=[page.tsx]
- "reports_page_metriccard": "MetricCard()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L53 | neighbors=[page.tsx]
- "reports_page_plainremediation": "plainRemediation()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L92 | neighbors=[page.tsx]
- "reports_page_portalreport": "PortalReport" | kind=code-symbol | neighbors=[ReportContent]
- "reports_page_portalreportspage": "PortalReportsPage()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L5 | neighbors=[page.tsx]
- "reports_page_priocolor": "prioColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L538 | neighbors=[page.tsx]
- "reports_page_priorityitem": "PriorityItem()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L152 | neighbors=[page.tsx]
- "reports_page_rationalestrip": "RationaleStrip()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L241 | neighbors=[page.tsx]
- "reports_page_remtext": "remText()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L73 | neighbors=[page.tsx]
- "reports_page_report_tabs": "REPORT_TABS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L77 | neighbors=[page.tsx]
- "reports_page_reportfindingcard": "ReportFindingCard()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L257 | neighbors=[page.tsx]
- "reports_page_reportmodal": "ReportModal()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L648 | neighbors=[page.tsx]
- "reports_page_reporttab": "ReportTab" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L26 | neighbors=[page.tsx]
- "reports_page_reporttype": "ReportType" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L14 | neighbors=[page.tsx]
- "reports_page_sectionblock": "SectionBlock()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L117 | neighbors=[page.tsx]
- "reports_page_sev_order": "SEV_ORDER" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L27 | neighbors=[page.tsx]
- "reports_page_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L73 | neighbors=[page.tsx]
- "reports_page_sevchip": "SevChip()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L38 | neighbors=[page.tsx]
- "reports_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L15 | neighbors=[page.tsx]
- "reports_page_severitybar": "SeverityBar()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L77 | neighbors=[page.tsx]
- "reports_page_severitystrip": "SeverityStrip()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L108 | neighbors=[page.tsx]
- "reports_page_sevs": "SEVS" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L26 | neighbors=[page.tsx]
- "reports_page_sevstrip": "SevStrip()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L109 | neighbors=[page.tsx]
- "reports_page_signal": "Signal()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L225 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-264.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
