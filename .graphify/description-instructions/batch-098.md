# Node Description Batch 99 of 131

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "reports_page_findingtable": "FindingTable()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L134 | neighbors=[page.tsx] | lang=en
- "reports_page_frameworks": "frameworks" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L55 | neighbors=[page.tsx] | lang=en
- "reports_page_metric": "Metric()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L98 | neighbors=[page.tsx] | lang=en
- "reports_page_plainremediation": "plainRemediation()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L92 | neighbors=[page.tsx] | lang=en
- "reports_page_priocolor": "prioColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L538 | neighbors=[page.tsx] | lang=en
- "reports_page_report_tabs": "REPORT_TABS" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L77 | neighbors=[page.tsx] | lang=en
- "reports_page_reporttype": "ReportType" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L14 | neighbors=[page.tsx] | lang=en
- "reports_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L15 | neighbors=[page.tsx] | lang=en
- "reports_page_severitystrip": "SeverityStrip()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L108 | neighbors=[page.tsx] | lang=en
- "reports_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L524 | neighbors=[page.tsx] | lang=en
- "reports_page_statuslabel": "statusLabel()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L531 | neighbors=[page.tsx] | lang=en
- "reports_page_technicalreport": "TechnicalReport()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L198 | neighbors=[page.tsx] | lang=en
- "request_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L7 | neighbors=[route.ts] | lang=en
- "results_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L5 | neighbors=[route.ts] | lang=en
- "routers_ad_ad_assessment_status": "ad_assessment_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L99 | neighbors=[ad.py] | lang=en
- "routers_ad_launch_ad_assessment": "launch_ad_assessment()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L64 | neighbors=[ad.py] | lang=en
- "routers_agent_advisor_run_advisor": "run_advisor()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L50 | neighbors=[agent_advisor.py] | lang=en
- "routers_agent_ws_rationale_115": "Persistent WebSocket for probe → manager push communication.      Authentication" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L115 | neighbors=[agent_websocket_endpoint()] | lang=en
- "routers_agent_ws_rationale_41": "Read an agent bearer token exclusively from the non-logged auth header." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L41 | neighbors=[_agent_token_from_websocket()] | lang=en
- "routers_agent_ws_rationale_52": "Validate eligibility and atomically claim a WebSocket job offer." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L52 | neighbors=[_claim_pushed_job()] | lang=en
- "routers_agents_agentbootstraprequest_validate_network_segments": ".validate_network_segments()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L470 | neighbors=[AgentBootstrapRequest] | lang=en
- "routers_agents_agentregisterrequest_validate_network_segments": ".validate_network_segments()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L237 | neighbors=[AgentRegisterRequest] | lang=en
- "routers_agents_heartbeatrequest_require_fence_for_running_job": ".require_fence_for_running_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L262 | neighbors=[HeartbeatRequest] | lang=en
- "routers_agents_list_agents": "list_agents()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L640 | neighbors=[agents.py] | lang=en
- "routers_agents_rationale_105": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L105 | neighbors=[_scope_is_reachable()] | lang=pt
- "routers_agents_rationale_141": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L141 | neighbors=[_job_reachability_scope()] | lang=en
- "routers_agents_rationale_215": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L215 | neighbors=[_agent_can_execute_job()] | lang=en
- "routers_agents_rationale_407": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L407 | neighbors=[_encrypt_scope_for_agent()] | lang=en
- "routers_agents_rationale_445": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L445 | neighbors=[_agent_ownership_check()] | lang=en
- "routers_agents_rationale_478": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L478 | neighbors=[list_use_cases()] | lang=en
- "routers_agents_rationale_491": "Allows a probe to register without an admin-issued PAT.      The manager must ha" | kind=entity | source=manager/backend/app/routers/agents.py:L491 | neighbors=[bootstrap_agent()] | lang=en
- "routers_agents_rationale_858": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L858 | neighbors=[get_job_status()] | lang=en
- "routers_agents_rationale_92": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L92 | neighbors=[_required_scan_type()] | lang=en
- "routers_ai_ai_generate": "ai_generate()" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L19 | neighbors=[ai.py] | lang=en
- "routers_ai_ai_status": "ai_status()" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L13 | neighbors=[ai.py] | lang=en
- "routers_ai_report_generate_report": "generate_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L61 | neighbors=[ai_report.py] | lang=en
- "routers_ai_report_report_status": "report_status()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L89 | neighbors=[ai_report.py] | lang=en
- "routers_analytics_exposure": "exposure()" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L43 | neighbors=[analytics.py] | lang=en
- "routers_detection_configure_siem": "configure_siem()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L61 | neighbors=[detection.py] | lang=en
- "routers_detection_get_coverage": "get_coverage()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L148 | neighbors=[detection.py] | lang=en

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
