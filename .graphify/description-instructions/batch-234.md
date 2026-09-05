# Node Description Batch 235 of 336

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

- "portal_page_sevs": "SEVS" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L13 | neighbors=[page.tsx]
- "portal_portalshell_footerclock": "FooterClock()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L299 | neighbors=[PortalShell.tsx]
- "portal_portalshell_nav": "NAV" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L23 | neighbors=[PortalShell.tsx]
- "portal_portalshell_portalshellprops": "PortalShellProps" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L36 | neighbors=[PortalShell.tsx]
- "portal_portalshell_portalsidebar": "PortalSidebar()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L46 | neighbors=[PortalShell.tsx]
- "portal_portalshell_sessiontimer": "SessionTimer()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L252 | neighbors=[PortalShell.tsx]
- "portal_timestamp_timestampprops": "TimestampProps" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L68 | neighbors=[Timestamp.tsx]
- "portscan_ratelimiter_init": ".__init__()" | kind=code-symbol | source=portscan.py:L96 | neighbors=[RateLimiter]
- "portscan_rationale_74": "Map a connect()-time OSError to (state, reason). Unknown stays visible     as ('" | kind=entity | source=portscan.py:L74 | neighbors=[classify_os_error()]
- "probes_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L6 | neighbors=[route.ts]
- "prompts_report_controlitem": "ControlItem" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L134 | neighbors=[report.ts]
- "prompts_report_domains": "DOMAINS" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L195 | neighbors=[report.ts]
- "prompts_report_effort": "Effort" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L31 | neighbors=[report.ts]
- "prompts_report_reportvalidation": "ReportValidation" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L388 | neighbors=[report.ts]
- "prompts_report_sev_rank": "SEV_RANK" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L199 | neighbors=[report.ts]
- "prompts_report_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L29 | neighbors=[report.ts]
- "prompts_report_severity_weight": "SEVERITY_WEIGHT" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L191 | neighbors=[report.ts]
- "register_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L12 | neighbors=[route.ts]
- "reject_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L4 | neighbors=[route.ts]
- "remediation_route_supported_os": "SUPPORTED_OS" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L5 | neighbors=[route.ts]
- "reports_page_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L49 | neighbors=[page.tsx]
- "reports_page_aidraft": "AiDraft" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L46 | neighbors=[page.tsx]
- "reports_page_aijobstatus": "AiJobStatus" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L45 | neighbors=[page.tsx]
- "reports_page_aipanel": "AiPanel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L415 | neighbors=[page.tsx]
- "reports_page_aireportpanel": "AiReportPanel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L688 | neighbors=[page.tsx]
- "reports_page_compliancecontrol": "ComplianceControl" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L12 | neighbors=[page.tsx]
- "reports_page_complianceframework": "ComplianceFramework" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L10 | neighbors=[page.tsx]
- "reports_page_complianceframeworkdata": "ComplianceFrameworkData" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L22 | neighbors=[page.tsx]
- "reports_page_compliancereport": "ComplianceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L267 | neighbors=[page.tsx]
- "reports_page_conf_style": "CONF_STYLE" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L434 | neighbors=[page.tsx]
- "reports_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L126 | neighbors=[page.tsx]
- "reports_page_coveragetab": "CoverageTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L1106 | neighbors=[page.tsx]
- "reports_page_cvetab": "CveTab()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L1045 | neighbors=[page.tsx]
- "reports_page_decisionbox": "DecisionBox()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L667 | neighbors=[page.tsx]
- "reports_page_documentstab": "DocumentsTab()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L586 | neighbors=[page.tsx]
- "reports_page_domain_label": "DOMAIN_LABEL" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L418 | neighbors=[page.tsx]
- "reports_page_effortdot": "EffortDot()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L446 | neighbors=[page.tsx]
- "reports_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L28 | neighbors=[page.tsx]
- "reports_page_evidblock": "EvidBlock()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L201 | neighbors=[page.tsx]
- "reports_page_evidenceitem": "EvidenceItem" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L35 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-234.json

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
