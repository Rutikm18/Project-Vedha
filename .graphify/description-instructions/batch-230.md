# Node Description Batch 231 of 332

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

- "native_port_scan_nativescanopts": "NativeScanOpts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L209 | neighbors=[port-scan.ts]
- "native_port_scan_port_names": "PORT_NAMES" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L111 | neighbors=[port-scan.ts]
- "native_port_scan_portrange": "PortRange" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L129 | neighbors=[port-scan.ts]
- "native_port_scan_top_1000_tcp": "TOP_1000_TCP" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L23 | neighbors=[port-scan.ts]
- "native_tls_info_tlsinforesult": "TlsInfoResult" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L14 | neighbors=[tls-info.ts]
- "native_tls_info_weak_protocols": "WEAK_PROTOCOLS" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L36 | neighbors=[tls-info.ts]
- "native_tls_info_weak_signatures": "WEAK_SIGNATURES" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L35 | neighbors=[tls-info.ts]
- "ordereddict": "OrderedDict" | kind=code-symbol | neighbors=[TTLCache]
- "pathid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L5 | neighbors=[route.ts]
- "pats_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/auth/pats/route.ts:L5 | neighbors=[route.ts]
- "pats_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/auth/pats/route.ts:L10 | neighbors=[route.ts]
- "portal_layout_nav": "NAV" | kind=code-symbol | source=manager/frontend/app/portal/layout.tsx:L7 | neighbors=[layout.tsx]
- "portal_layout_portallayout": "PortalLayout()" | kind=code-symbol | source=manager/frontend/app/portal/layout.tsx:L6 | neighbors=[layout.tsx]
- "portal_page_dashboardskeleton": "DashboardSkeleton()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L189 | neighbors=[page.tsx]
- "portal_page_kpi": "Kpi()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L16 | neighbors=[page.tsx]
- "portal_page_legend": "Legend()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L209 | neighbors=[page.tsx]
- "portal_page_metric": "Metric()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L13 | neighbors=[page.tsx]
- "portal_page_panel": "Panel()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L27 | neighbors=[page.tsx]
- "portal_page_portaloverview": "PortalOverview()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L33 | neighbors=[page.tsx]
- "portal_page_queuestat": "QueueStat()" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L218 | neighbors=[page.tsx]
- "portal_page_sev_order": "SEV_ORDER" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L14 | neighbors=[page.tsx]
- "portal_page_sevs": "SEVS" | kind=code-symbol | source=manager/frontend/app/portal/page.tsx:L13 | neighbors=[page.tsx]
- "portal_portalshell_footerclock": "FooterClock()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L298 | neighbors=[PortalShell.tsx]
- "portal_portalshell_nav": "NAV" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L23 | neighbors=[PortalShell.tsx]
- "portal_portalshell_portalshellprops": "PortalShellProps" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L36 | neighbors=[PortalShell.tsx]
- "portal_portalshell_portalsidebar": "PortalSidebar()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L46 | neighbors=[PortalShell.tsx]
- "portal_portalshell_sessiontimer": "SessionTimer()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L252 | neighbors=[PortalShell.tsx]
- "portal_timestamp_timestampprops": "TimestampProps" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L68 | neighbors=[Timestamp.tsx]
- "portscan_ratelimiter_init": ".__init__()" | kind=code-symbol | source=portscan.py:L96 | neighbors=[RateLimiter]
- "portscan_rationale_74": "Map a connect()-time OSError to (state, reason). Unknown stays visible     as ('" | kind=entity | source=portscan.py:L74 | neighbors=[classify_os_error()]
- "probes_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L6 | neighbors=[route.ts]
- "prompts_report_domains": "DOMAINS" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L123 | neighbors=[report.ts]
- "prompts_report_effort": "Effort" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L31 | neighbors=[report.ts]
- "prompts_report_remediationgroup": "RemediationGroup" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L93 | neighbors=[report.ts]
- "prompts_report_reportfinding": "ReportFinding" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L76 | neighbors=[report.ts]
- "prompts_report_reportvalidation": "ReportValidation" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L316 | neighbors=[report.ts]
- "prompts_report_scorecard": "Scorecard" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L63 | neighbors=[report.ts]
- "prompts_report_sev_rank": "SEV_RANK" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L127 | neighbors=[report.ts]
- "prompts_report_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L29 | neighbors=[report.ts]
- "prompts_report_severity_weight": "SEVERITY_WEIGHT" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L119 | neighbors=[report.ts]

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
