# Node Description Batch 163 of 227

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

- "portal_page_legend": "Legend()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L209 | neighbors=[page.tsx]
- "portal_page_metric": "Metric()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L13 | neighbors=[page.tsx]
- "portal_page_panel": "Panel()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L27 | neighbors=[page.tsx]
- "portal_page_portaloverview": "PortalOverview()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L36 | neighbors=[page.tsx]
- "portal_page_queuestat": "QueueStat()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L218 | neighbors=[page.tsx]
- "portal_page_sev_order": "SEV_ORDER" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L14 | neighbors=[page.tsx]
- "portal_page_sevs": "SEVS" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L13 | neighbors=[page.tsx]
- "portal_portalshell_footerclock": "FooterClock()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L244 | neighbors=[PortalShell.tsx]
- "portal_portalshell_nav": "NAV" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L20 | neighbors=[PortalShell.tsx]
- "portal_portalshell_portalshellprops": "PortalShellProps" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L28 | neighbors=[PortalShell.tsx]
- "portal_portalshell_portalsidebar": "PortalSidebar()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L38 | neighbors=[PortalShell.tsx]
- "portal_portalshell_sessiontimer": "SessionTimer()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L252 | neighbors=[PortalShell.tsx]
- "portscan_ratelimiter_init": ".__init__()" | kind=code-symbol | source=portscan.py:L96 | neighbors=[RateLimiter]
- "portscan_rationale_74": "Map a connect()-time OSError to (state, reason). Unknown stays visible     as ('" | kind=entity | source=portscan.py:L74 | neighbors=[classify_os_error()]
- "probes_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L6 | neighbors=[route.ts]
- "register_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L12 | neighbors=[route.ts]
- "reject_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L4 | neighbors=[route.ts]
- "reports_page_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L68 | neighbors=[page.tsx]
- "reports_page_compliancecontrol": "ComplianceControl" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L12 | neighbors=[page.tsx]
- "reports_page_complianceframework": "ComplianceFramework" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L10 | neighbors=[page.tsx]
- "reports_page_complianceframeworkdata": "ComplianceFrameworkData" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L22 | neighbors=[page.tsx]
- "reports_page_compliancereport": "ComplianceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L267 | neighbors=[page.tsx]
- "reports_page_documentstab": "DocumentsTab()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L144 | neighbors=[page.tsx]
- "reports_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L17 | neighbors=[page.tsx]
- "reports_page_evidencereport": "EvidenceReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L230 | neighbors=[page.tsx]
- "reports_page_evidencestats": "evidenceStats" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L35 | neighbors=[page.tsx]
- "reports_page_evidencesummary": "EvidenceSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L717 | neighbors=[page.tsx]
- "reports_page_executivedoc": "ExecutiveDoc()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L86 | neighbors=[page.tsx]
- "reports_page_executivereport": "ExecutiveReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L155 | neighbors=[page.tsx]
- "reports_page_executivesummary": "ExecutiveSummary()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L546 | neighbors=[page.tsx]
- "reports_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L32 | neighbors=[page.tsx]
- "reports_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L52 | neighbors=[page.tsx]
- "reports_page_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L60 | neighbors=[page.tsx]
- "reports_page_findingtable": "FindingTable()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L134 | neighbors=[page.tsx]
- "reports_page_frameworks": "frameworks" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L55 | neighbors=[page.tsx]
- "reports_page_metric": "Metric()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L98 | neighbors=[page.tsx]
- "reports_page_plainremediation": "plainRemediation()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L92 | neighbors=[page.tsx]
- "reports_page_portalreport": "PortalReport" | kind=code-symbol | neighbors=[ReportContent]
- "reports_page_priocolor": "prioColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L538 | neighbors=[page.tsx]
- "reports_page_report_tabs": "REPORT_TABS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L77 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-162.json

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
