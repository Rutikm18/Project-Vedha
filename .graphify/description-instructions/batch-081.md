# Node Description Batch 82 of 104

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

- "probe_pipeline_ip_key": "_ip_key()" | kind=code-symbol | source=probe/pipeline.py:L243 | neighbors=[pipeline.py]
- "probe_pipeline_main": "main()" | kind=code-symbol | source=probe/pipeline.py:L356 | neighbors=[pipeline.py]
- "probe_pipeline_rationale_133": "Make a per-host scanner instance share ONE rate limiter + semaphore with all" | kind=entity | source=probe/pipeline.py:L133 | neighbors=[_shared()]
- "probe_pipeline_rationale_252": "Make a raw banner safe and readable for the summary line.      Many services ans" | kind=entity | source=probe/pipeline.py:L252 | neighbors=[_clean()]
- "probe_pipeline_render_summary": "_render_summary()" | kind=code-symbol | source=probe/pipeline.py:L316 | neighbors=[pipeline.py]
- "probe_pipeline_run_passive": "_run_passive()" | kind=code-symbol | source=probe/pipeline.py:L227 | neighbors=[pipeline.py]
- "probe_run_scan_rationale_42": "# NOTE: credentialed collectors (ssh_collector, windows_collector) are run" | kind=entity | source=probe/run_scan.py:L42 | neighbors=[run_scan.py]
- "probes_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L6 | neighbors=[route.ts]
- "prompts_exploit_builder": "exploit-builder.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/exploit-builder.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …]
- "protocol": "Protocol" | kind=code-symbol | neighbors=[AIClient]
- "register_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L12 | neighbors=[route.ts]
- "reject_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L5 | neighbors=[route.ts]
- "reports_page_compliancecontrol": "ComplianceControl" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L12 | neighbors=[page.tsx]
- "reports_page_complianceframework": "ComplianceFramework" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L10 | neighbors=[page.tsx]
- "reports_page_complianceframeworkdata": "ComplianceFrameworkData" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L22 | neighbors=[page.tsx]
- "reports_page_compliancereport": "ComplianceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L609 | neighbors=[page.tsx]
- "reports_page_evidencestats": "evidenceStats" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L35 | neighbors=[page.tsx]
- "reports_page_evidencesummary": "EvidenceSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L717 | neighbors=[page.tsx]
- "reports_page_executivesummary": "ExecutiveSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L546 | neighbors=[page.tsx]
- "reports_page_frameworks": "frameworks" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L55 | neighbors=[page.tsx]
- "reports_page_priocolor": "prioColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L538 | neighbors=[page.tsx]
- "reports_page_reportspage": "ReportsPage()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L780 | neighbors=[page.tsx]
- "reports_page_reporttype": "ReportType" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L9 | neighbors=[page.tsx]
- "reports_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L524 | neighbors=[page.tsx]
- "reports_page_statuslabel": "statusLabel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L531 | neighbors=[page.tsx]
- "request_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L7 | neighbors=[route.ts]
- "results_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L5 | neighbors=[route.ts]
- "routers_ad_ad_assessment_status": "ad_assessment_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L99 | neighbors=[ad.py]
- "routers_ad_launch_ad_assessment": "launch_ad_assessment()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L64 | neighbors=[ad.py]
- "routers_agent_advisor_run_advisor": "run_advisor()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L50 | neighbors=[agent_advisor.py]
- "routers_agents_list_agents": "list_agents()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L332 | neighbors=[agents.py]
- "routers_ai_report_generate_report": "generate_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L61 | neighbors=[ai_report.py]
- "routers_ai_report_report_status": "report_status()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L89 | neighbors=[ai_report.py]
- "routers_analytics_exposure": "exposure()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L43 | neighbors=[analytics.py]
- "routers_detection_configure_siem": "configure_siem()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L61 | neighbors=[detection.py]
- "routers_detection_get_coverage": "get_coverage()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L148 | neighbors=[detection.py]
- "routers_detection_get_gaps": "get_gaps()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L187 | neighbors=[detection.py]
- "routers_detection_run_validation": "run_validation()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L96 | neighbors=[detection.py]
- "routers_engagements_get_engagement": "get_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L431 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_assets": "list_engagement_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L603 | neighbors=[engagements.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-081.json

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
