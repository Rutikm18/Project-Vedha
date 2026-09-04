# Node Description Batch 231 of 330

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

- "reports_page_executivesummary": "ExecutiveSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L546 | neighbors=[page.tsx]
- "reports_page_executivetab": "ExecutiveTab()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L411 | neighbors=[page.tsx]
- "reports_page_fieldlabel": "FieldLabel()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L246 | neighbors=[page.tsx]
- "reports_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L32 | neighbors=[page.tsx]
- "reports_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L42 | neighbors=[page.tsx]
- "reports_page_findingstab": "FindingsTab()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L533 | neighbors=[page.tsx]
- "reports_page_findingstable": "FindingsTable()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L177 | neighbors=[page.tsx]
- "reports_page_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L43 | neighbors=[page.tsx]
- "reports_page_findingtable": "FindingTable()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L134 | neighbors=[page.tsx]
- "reports_page_fmtdatetime": "fmtDatetime()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L65 | neighbors=[page.tsx]
- "reports_page_frameworks": "frameworks" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L55 | neighbors=[page.tsx]
- "reports_page_metric": "Metric()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L139 | neighbors=[page.tsx]
- "reports_page_metriccard": "MetricCard()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L53 | neighbors=[page.tsx]
- "reports_page_plainremediation": "plainRemediation()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L92 | neighbors=[page.tsx]
- "reports_page_portalreport": "PortalReport" | kind=code-symbol | neighbors=[ReportContent]
- "reports_page_priocolor": "prioColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L538 | neighbors=[page.tsx]
- "reports_page_priorityitem": "PriorityItem()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L152 | neighbors=[page.tsx]
- "reports_page_remtext": "remText()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L70 | neighbors=[page.tsx]
- "reports_page_report_tabs": "REPORT_TABS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L77 | neighbors=[page.tsx]
- "reports_page_reportmodal": "ReportModal()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L648 | neighbors=[page.tsx]
- "reports_page_reporttab": "ReportTab" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L21 | neighbors=[page.tsx]
- "reports_page_reporttype": "ReportType" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L14 | neighbors=[page.tsx]
- "reports_page_sectionblock": "SectionBlock()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L117 | neighbors=[page.tsx]
- "reports_page_sev_order": "SEV_ORDER" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L27 | neighbors=[page.tsx]
- "reports_page_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L101 | neighbors=[page.tsx]
- "reports_page_sevchip": "SevChip()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L38 | neighbors=[page.tsx]
- "reports_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L15 | neighbors=[page.tsx]
- "reports_page_severitybar": "SeverityBar()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L77 | neighbors=[page.tsx]
- "reports_page_severitystrip": "SeverityStrip()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L108 | neighbors=[page.tsx]
- "reports_page_sevs": "SEVS" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L26 | neighbors=[page.tsx]
- "reports_page_sevstrip": "SevStrip()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L153 | neighbors=[page.tsx]
- "reports_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L524 | neighbors=[page.tsx]
- "reports_page_statuslabel": "statusLabel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L531 | neighbors=[page.tsx]
- "reports_page_statuspill": "StatusPill()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L113 | neighbors=[page.tsx]
- "reports_page_tab": "Tab" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L19 | neighbors=[page.tsx]
- "reports_page_tabs": "TABS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L50 | neighbors=[page.tsx]
- "reports_page_technicalreport": "TechnicalReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L198 | neighbors=[page.tsx]
- "reports_page_techtab": "TechTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L618 | neighbors=[page.tsx]
- "reports_page_topfindings": "TopFindings()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L65 | neighbors=[page.tsx]
- "reports_page_vm_label": "VM_LABEL" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L87 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-230.json

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
