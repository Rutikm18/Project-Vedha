# Node Description Batch 101 of 134

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "probe_pipeline_run_passive": "_run_passive()" | kind=code-symbol | source=probe/pipeline.py:L227 | neighbors=[pipeline.py]
- "probe_run_scan_rationale_42": "# NOTE: credentialed collectors (ssh_collector, windows_collector) are run" | kind=entity | source=probe/run_scan.py:L42 | neighbors=[run_scan.py]
- "probe_selftest_live_c": "_c()" | kind=code-symbol | source=probe/selftest_live.py:L28 | neighbors=[selftest_live.py]
- "probe_selftest_live_handler_do_get": ".do_GET()" | kind=code-symbol | source=probe/selftest_live.py:L53 | neighbors=[_Handler]
- "probe_selftest_live_handler_do_options": ".do_OPTIONS()" | kind=code-symbol | source=probe/selftest_live.py:L62 | neighbors=[_Handler]
- "probe_selftest_live_handler_log_message": ".log_message()" | kind=code-symbol | source=probe/selftest_live.py:L50 | neighbors=[_Handler]
- "probe_showcase_run_c": "_c()" | kind=code-symbol | source=probe/showcase_run.py:L24 | neighbors=[showcase_run.py]
- "probes_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L6 | neighbors=[route.ts]
- "protocol": "Protocol" | kind=code-symbol | neighbors=[AIClient]
- "register_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L12 | neighbors=[route.ts]
- "reject_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L4 | neighbors=[route.ts]
- "reports_page_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L68 | neighbors=[page.tsx]
- "reports_page_compliancecontrol": "ComplianceControl" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L12 | neighbors=[page.tsx]
- "reports_page_complianceframework": "ComplianceFramework" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L10 | neighbors=[page.tsx]
- "reports_page_complianceframeworkdata": "ComplianceFrameworkData" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L22 | neighbors=[page.tsx]
- "reports_page_compliancereport": "ComplianceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L267 | neighbors=[page.tsx]
- "reports_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L17 | neighbors=[page.tsx]
- "reports_page_evidencereport": "EvidenceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L230 | neighbors=[page.tsx]
- "reports_page_evidencestats": "evidenceStats" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L35 | neighbors=[page.tsx]
- "reports_page_evidencesummary": "EvidenceSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L717 | neighbors=[page.tsx]
- "reports_page_executivereport": "ExecutiveReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L155 | neighbors=[page.tsx]
- "reports_page_executivesummary": "ExecutiveSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L546 | neighbors=[page.tsx]
- "reports_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L32 | neighbors=[page.tsx]
- "reports_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L52 | neighbors=[page.tsx]
- "reports_page_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L60 | neighbors=[page.tsx]
- "reports_page_findingtable": "FindingTable()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L134 | neighbors=[page.tsx]
- "reports_page_frameworks": "frameworks" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L55 | neighbors=[page.tsx]
- "reports_page_metric": "Metric()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L98 | neighbors=[page.tsx]
- "reports_page_plainremediation": "plainRemediation()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L92 | neighbors=[page.tsx]
- "reports_page_priocolor": "prioColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L538 | neighbors=[page.tsx]
- "reports_page_report_tabs": "REPORT_TABS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L77 | neighbors=[page.tsx]
- "reports_page_reporttype": "ReportType" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L14 | neighbors=[page.tsx]
- "reports_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L15 | neighbors=[page.tsx]
- "reports_page_severitystrip": "SeverityStrip()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L108 | neighbors=[page.tsx]
- "reports_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L524 | neighbors=[page.tsx]
- "reports_page_statuslabel": "statusLabel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L531 | neighbors=[page.tsx]
- "reports_page_technicalreport": "TechnicalReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L198 | neighbors=[page.tsx]
- "request_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L7 | neighbors=[route.ts]
- "results_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L5 | neighbors=[route.ts]
- "routers_ad_ad_assessment_status": "ad_assessment_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L99 | neighbors=[ad.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-100.json

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
