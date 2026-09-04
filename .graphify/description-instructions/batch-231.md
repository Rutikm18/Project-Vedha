# Node Description Batch 232 of 332

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

- "register_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L12 | neighbors=[route.ts]
- "reject_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L4 | neighbors=[route.ts]
- "remediation_route_supported_os": "SUPPORTED_OS" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L5 | neighbors=[route.ts]
- "reports_page_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L44 | neighbors=[page.tsx]
- "reports_page_aidraft": "AiDraft" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L46 | neighbors=[page.tsx]
- "reports_page_aijobstatus": "AiJobStatus" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L45 | neighbors=[page.tsx]
- "reports_page_aipanel": "AiPanel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L415 | neighbors=[page.tsx]
- "reports_page_compliancecontrol": "ComplianceControl" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L12 | neighbors=[page.tsx]
- "reports_page_complianceframework": "ComplianceFramework" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L10 | neighbors=[page.tsx]
- "reports_page_complianceframeworkdata": "ComplianceFrameworkData" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L22 | neighbors=[page.tsx]
- "reports_page_compliancereport": "ComplianceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L267 | neighbors=[page.tsx]
- "reports_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L123 | neighbors=[page.tsx]
- "reports_page_coveragetab": "CoverageTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L754 | neighbors=[page.tsx]
- "reports_page_cvetab": "CveTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L693 | neighbors=[page.tsx]
- "reports_page_documentstab": "DocumentsTab()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L586 | neighbors=[page.tsx]
- "reports_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L23 | neighbors=[page.tsx]
- "reports_page_evidblock": "EvidBlock()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L198 | neighbors=[page.tsx]
- "reports_page_evidenceitem": "EvidenceItem" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L30 | neighbors=[page.tsx]
- "reports_page_evidencereport": "EvidenceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L230 | neighbors=[page.tsx]
- "reports_page_evidencestats": "evidenceStats" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L35 | neighbors=[page.tsx]
- "reports_page_evidencesummary": "EvidenceSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L717 | neighbors=[page.tsx]
- "reports_page_evidtab": "EvidTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L646 | neighbors=[page.tsx]
- "reports_page_exectab": "ExecTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L523 | neighbors=[page.tsx]
- "reports_page_executivedoc": "ExecutiveDoc()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L86 | neighbors=[page.tsx]
- "reports_page_executivereport": "ExecutiveReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L155 | neighbors=[page.tsx]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-231.json

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
