# Node Description Batch 92 of 119

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

- "reports_page_reporttype": "ReportType" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L14 | neighbors=[page.tsx]
- "reports_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L15 | neighbors=[page.tsx]
- "reports_page_severitystrip": "SeverityStrip()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L108 | neighbors=[page.tsx]
- "reports_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L524 | neighbors=[page.tsx]
- "reports_page_statuslabel": "statusLabel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L531 | neighbors=[page.tsx]
- "reports_page_technicalreport": "TechnicalReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L198 | neighbors=[page.tsx]
- "request_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L7 | neighbors=[route.ts]
- "results_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L5 | neighbors=[route.ts]
- "routers_ad_ad_assessment_status": "ad_assessment_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L99 | neighbors=[ad.py]
- "routers_ad_launch_ad_assessment": "launch_ad_assessment()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L64 | neighbors=[ad.py]
- "routers_agent_advisor_run_advisor": "run_advisor()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L50 | neighbors=[agent_advisor.py]
- "routers_agents_agentregisterrequest_validate_network_segments": ".validate_network_segments()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L232 | neighbors=[AgentRegisterRequest]
- "routers_agents_list_agents": "list_agents()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L514 | neighbors=[agents.py]
- "routers_ai_report_generate_report": "generate_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L61 | neighbors=[ai_report.py]
- "routers_ai_report_report_status": "report_status()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L89 | neighbors=[ai_report.py]
- "routers_analytics_exposure": "exposure()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L43 | neighbors=[analytics.py]
- "routers_detection_configure_siem": "configure_siem()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L61 | neighbors=[detection.py]
- "routers_detection_get_coverage": "get_coverage()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L148 | neighbors=[detection.py]
- "routers_detection_get_gaps": "get_gaps()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L187 | neighbors=[detection.py]
- "routers_detection_run_validation": "run_validation()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L96 | neighbors=[detection.py]
- "routers_engagements_engagementupdate_normalize_name": ".normalize_name()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L496 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_dates": ".validate_dates()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L512 | neighbors=[EngagementUpdate]
- "routers_engagements_engagementupdate_validate_scopes": ".validate_scopes()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L506 | neighbors=[EngagementUpdate]
- "routers_engagements_get_engagement": "get_engagement()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L432 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_assets": "list_engagement_assets()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L626 | neighbors=[engagements.py]
- "routers_engagements_list_engagement_jobs": "list_engagement_jobs()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L598 | neighbors=[engagements.py]
- "routers_engagements_list_engagements": "list_engagements()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L371 | neighbors=[engagements.py]
- "routers_exploits_list_audit_logs": "list_audit_logs()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L338 | neighbors=[exploits.py]
- "routers_findings_finding_summary": "finding_summary()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L154 | neighbors=[findings.py]
- "routers_findings_list_findings": "list_findings()" | kind=code-symbol | source=manager/backend/app/routers/findings.py:L69 | neighbors=[findings.py]
- "routers_health_health": "health()" | kind=code-symbol | source=manager/backend/app/routers/health.py:L16 | neighbors=[health.py]
- "routers_vuln_scans_import_findings": "import_findings()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L216 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nessus_scan": "launch_nessus_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L67 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_launch_nuclei_scan": "launch_nuclei_scan()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L120 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_scan_status": "scan_status()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L166 | neighbors=[vuln_scans.py]
- "routers_vuln_scans_trigger_enrichment": "trigger_enrichment()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L195 | neighbors=[vuln_scans.py]
- "run_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/run/route.ts:L5 | neighbors=[route.ts]
- "scan_page_cat": "Cat" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L121 | neighbors=[page.tsx]
- "scan_page_cats": "CATS" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L120 | neighbors=[page.tsx]
- "scan_page_dispatchreceipt": "DispatchReceipt()" | kind=code-symbol | source=manager/frontend/app/scan/page.tsx:L505 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-091.json

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
