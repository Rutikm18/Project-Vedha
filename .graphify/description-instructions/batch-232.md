# Node Description Batch 233 of 332

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
- "reports_page_vm_name": "VM_NAME" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L94 | neighbors=[page.tsx]
- "request_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L7 | neighbors=[route.ts]
- "results_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L5 | neighbors=[route.ts]
- "reveal_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/customers/[id]/reveal/route.ts:L8 | neighbors=[route.ts]
- "routers_ad_ad_assessment_status": "ad_assessment_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L99 | neighbors=[ad.py]
- "routers_ad_launch_ad_assessment": "launch_ad_assessment()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L64 | neighbors=[ad.py]
- "routers_agent_advisor_run_advisor": "run_advisor()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L50 | neighbors=[agent_advisor.py]
- "routers_agent_ws_rationale_115": "Persistent WebSocket for probe → manager push communication.      Authentication" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L115 | neighbors=[agent_websocket_endpoint()]
- "routers_agent_ws_rationale_41": "Read an agent bearer token exclusively from the non-logged auth header." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L41 | neighbors=[_agent_token_from_websocket()]
- "routers_agent_ws_rationale_52": "Validate eligibility and atomically claim a WebSocket job offer." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L52 | neighbors=[_claim_pushed_job()]
- "routers_agents_agentbootstraprequest_validate_network_segments": ".validate_network_segments()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L600 | neighbors=[AgentBootstrapRequest]
- "routers_agents_agentregisterrequest_validate_network_segments": ".validate_network_segments()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L189 | neighbors=[AgentRegisterRequest]
- "routers_agents_enqueuejobrequest_validate_uc": "._validate_uc()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L315 | neighbors=[EnqueueJobRequest]
- "routers_agents_heartbeatrequest_require_fence_for_running_job": ".require_fence_for_running_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L214 | neighbors=[HeartbeatRequest]
- "routers_agents_list_agents": "list_agents()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L780 | neighbors=[agents.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-232.json

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
