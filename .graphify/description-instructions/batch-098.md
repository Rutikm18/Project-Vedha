# Node Description Batch 99 of 227

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

- "native_dns_recon_nativeptrsweep": "nativePtrSweep()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L147 | neighbors=[dns-recon.ts, tool-runners.ts]
- "native_dns_recon_safe": "safe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L49 | neighbors=[dns-recon.ts, nativeDnsRecon()]
- "native_http_probe_nativehttpprobe": "nativeHttpProbe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L248 | neighbors=[tool-runners.ts, http-probe.ts]
- "native_port_scan_groupresults": "groupResults()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L261 | neighbors=[tool-runners.ts, port-scan.ts]
- "native_port_scan_resolveports": "resolvePorts()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L131 | neighbors=[port-scan.ts, nativePortScan()]
- "native_tls_info_nativetlsinfo": "nativeTlsInfo()" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L38 | neighbors=[tls-info.ts, tool-runners.ts]
- "oserror": "OSError" | kind=code-symbol | neighbors=[NmapExecutionError, NmapExecutionError]
- "path_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L45 | neighbors=[route.ts, proxy()]
- "path_route_patch": "PATCH()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/customer-access/[...path]/route.ts:L40 | neighbors=[route.ts, proxy()]
- "path_route_portaltoken": "portalToken()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L11 | neighbors=[route.ts, proxy()]
- "path_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L50 | neighbors=[route.ts, proxy()]
- "portscan_family_of": "family_of()" | kind=code-symbol | source=portscan.py:L83 | neighbors=[portscan.py, ._attempt()]
- "portscan_parse_ports": "parse_ports()" | kind=code-symbol | source=portscan.py:L199 | neighbors=[portscan.py, main()]
- "portscan_portscanner_init": ".__init__()" | kind=code-symbol | source=portscan.py:L113 | neighbors=[PortScanner, RateLimiter]
- "portscan_portscanner_record": "._record()" | kind=code-symbol | source=portscan.py:L124 | neighbors=[PortScanner, ._attempt()]
- "portscan_ratelimiter_wait": ".wait()" | kind=code-symbol | source=portscan.py:L101 | neighbors=[.scan_port(), RateLimiter]
- "prompts_exploit_builder": "exploit-builder.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/exploit-builder.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "reopen_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L11 | neighbors=[route.ts, POST()]
- "reopen_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L16 | neighbors=[route.ts, fail()]
- "reports_page_fmtdate": "fmtDate()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L27 | neighbors=[page.tsx, PortalReports()]
- "reports_page_formatdate": "formatDate()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L84 | neighbors=[page.tsx, ReportsPage()]
- "reports_page_portalreports": "PortalReports()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L179 | neighbors=[page.tsx, fmtDate()]
- "reports_page_reportcontent": "ReportContent" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L15 | neighbors=[page.tsx, PortalReport]
- "reports_page_reportspage": "ReportsPage()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L297 | neighbors=[page.tsx, formatDate()]
- "routers_activity_recent_activity": "recent_activity()" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L41 | neighbors=[activity.py, ActivityItem]
- "routers_ad_set_job_status": "_set_job_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L201 | neighbors=[ad.py, _run_ad_assessment_and_save()]
- "routers_agent_advisor_list_recommendations": "list_recommendations()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L72 | neighbors=[agent_advisor.py, _rec_dict()]
- "routers_agent_advisor_rec_dict": "_rec_dict()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L31 | neighbors=[agent_advisor.py, list_recommendations()]
- "routers_agent_ws_rationale_44": "Persistent WebSocket for probe → manager push communication.      Query params:" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L44 | neighbors=[ScanJob, agent_websocket_endpoint()]
- "routers_agents_enqueuejobrequest_validate_intensity": "._validate_intensity()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L320 | neighbors=[EnqueueJobRequest, _normalize_intensity_name()]
- "routers_agents_heartbeat": "heartbeat()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L761 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_agents_job_params_contain_secret": "_job_params_contain_secret()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L74 | neighbors=[agents.py, enqueue_agent_job()]
- "routers_agents_rationale_548": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L548 | neighbors=[list_use_cases(), bootstrap_agent()]
- "routers_agents_register_agent": "register_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L665 | neighbors=[agents.py, AgentRegisterResponse]
- "routers_agents_submit_job_result": "submit_job_result()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1195 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_ai_report_approve_report": "approve_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L136 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_get_draft": "get_draft()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L119 | neighbors=[ai_report.py, _output_out()]
- "routers_ai_report_output_out": "_output_out()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L228 | neighbors=[ai_report.py, get_draft()]
- "routers_ai_report_reject_report": "reject_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L158 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_set_job": "_set_job()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L420 | neighbors=[ai_report.py, _run_generation()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-098.json

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
