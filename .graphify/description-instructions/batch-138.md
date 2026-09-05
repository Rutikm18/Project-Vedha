# Node Description Batch 139 of 336

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

- "prompts_report_reportdecision": "ReportDecision" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L126 | neighbors=[report.ts, page.tsx]
- "prompts_report_reportresult": "ReportResult" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L141 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_scorecard": "Scorecard" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L63 | neighbors=[report.ts, page.tsx]
- "prompts_report_scorecardinput": "ScorecardInput" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L43 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_validatereport": "validateReport()" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L398 | neighbors=[ai-engine.ts, report.ts]
- "prompts_report_verdictsummaryout": "VerdictSummaryOut" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L171 | neighbors=[ai-engine.ts, report.ts]
- "raw_facts_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/raw-facts/route.ts:L12 | neighbors=[route.ts, GET()]
- "raw_facts_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/raw-facts/route.ts:L17 | neighbors=[route.ts, fail()]
- "remediation_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L7 | neighbors=[route.ts, GET()]
- "remediation_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L15 | neighbors=[route.ts, fail()]
- "reopen_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L11 | neighbors=[route.ts, POST()]
- "reopen_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L16 | neighbors=[route.ts, fail()]
- "reports_page_cvsscolor": "cvssColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L79 | neighbors=[page.tsx, FindingCard()]
- "reports_page_cvssvector": "CvssVector()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L180 | neighbors=[page.tsx, parseCvssVector()]
- "reports_page_exploitcol": "exploitCol()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L614 | neighbors=[page.tsx, ExposureMatrix()]
- "reports_page_exposurematrix": "ExposureMatrix()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L620 | neighbors=[page.tsx, exploitCol()]
- "reports_page_formatdate": "formatDate()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L84 | neighbors=[page.tsx, ReportsPage()]
- "reports_page_parsecvss": "parseCvss()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L76 | neighbors=[page.tsx, FindingCard()]
- "reports_page_parsecvssvector": "parseCvssVector()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L86 | neighbors=[page.tsx, CvssVector()]
- "reports_page_portalreports": "PortalReports()" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L705 | neighbors=[page.tsx, fmtDate()]
- "reports_page_reportcontent": "ReportContent" | kind=code-symbol | source=manager/frontend/app/portal/reports/page.tsx:L17 | neighbors=[page.tsx, PortalReport]
- "reports_page_scorecardcard": "ScorecardCard()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L455 | neighbors=[page.tsx, scoreColor()]
- "reports_page_scorecolor": "scoreColor()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L427 | neighbors=[page.tsx, ScorecardCard()]
- "routers_activity_recent_activity": "recent_activity()" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L41 | neighbors=[activity.py, ActivityItem]
- "routers_ad_set_job_status": "_set_job_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L201 | neighbors=[ad.py, _run_ad_assessment_and_save()]
- "routers_agent_advisor_list_recommendations": "list_recommendations()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L72 | neighbors=[agent_advisor.py, _rec_dict()]
- "routers_agent_advisor_rec_dict": "_rec_dict()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L31 | neighbors=[agent_advisor.py, list_recommendations()]
- "routers_agent_ws_rationale_44": "Persistent WebSocket for probe → manager push communication.      Query params:" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L44 | neighbors=[ScanJob, agent_websocket_endpoint()]
- "routers_agents_enqueuejobrequest_validate_intensity": "._validate_intensity()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L356 | neighbors=[EnqueueJobRequest, _normalize_intensity_name()]
- "routers_agents_heartbeat": "heartbeat()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L855 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_agents_job_params_contain_secret": "_job_params_contain_secret()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L75 | neighbors=[agents.py, enqueue_agent_job()]
- "routers_agents_rationale_548": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L548 | neighbors=[list_use_cases(), bootstrap_agent()]
- "routers_agents_rationale_571": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L571 | neighbors=[_encrypt_scope_for_agent(), bootstrap_agent()]
- "routers_agents_rationale_609": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L609 | neighbors=[_agent_ownership_check(), list_intensities()]
- "routers_agents_rationale_620": "The numeric scan-hardness scale: 1 light, 2 standard, 3 deep." | kind=entity | source=manager/backend/app/routers/agents.py:L620 | neighbors=[list_intensities(), bootstrap_agent()]
- "routers_agents_register_agent": "register_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L759 | neighbors=[agents.py, AgentRegisterResponse]
- "routers_agents_submit_job_result": "submit_job_result()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L1528 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_ai_report_approve_report": "approve_report()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L136 | neighbors=[ai_report.py, _pending_outputs()]
- "routers_ai_report_get_draft": "get_draft()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L119 | neighbors=[ai_report.py, _output_out()]
- "routers_ai_report_output_out": "_output_out()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L228 | neighbors=[ai_report.py, get_draft()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-138.json

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
