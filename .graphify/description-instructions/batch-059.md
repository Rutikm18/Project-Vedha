# Node Description Batch 60 of 134

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

- "findings_page_urgencyreasons": "urgencyReasons()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L771 | neighbors=[page.tsx, getSlaColor()]
- "findings_page_usecountup": "useCountUp()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L783 | neighbors=[page.tsx, FixFirstStrip()]
- "frontend_proxy_ispublic": "isPublic()" | kind=code-symbol | source=manager/frontend/proxy.ts:L14 | neighbors=[proxy.ts, proxy()]
- "frontend_proxy_proxy": "proxy()" | kind=code-symbol | source=manager/frontend/proxy.ts:L19 | neighbors=[proxy.ts, isPublic()]
- "graph_analyzer_priority": "_priority()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L285 | neighbors=[analyzer.py, .identify_chokepoints()]
- "graph_analyzer_safe_float": "_safe_float()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L278 | neighbors=[analyzer.py, .score_path()]
- "graph_builder_service_node_id": "service_node_id()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L44 | neighbors=[builder.py, .build_asset_graph()]
- "graph_demo_demoservice": "DemoService" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L37 | neighbors=[demo.py, generate_demo_dataset()]
- "graph_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/graph/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "graph_neo4j_client_neo4jclient_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L61 | neighbors=[Neo4jClient, Open the driver and verify connectivity…]
- "hooks_usecountup_usecountup": "useCountUp()" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L3 | neighbors=[DashboardCharts.tsx, useCountUp.ts]
- "hooks_usemousegradient_usemousegradient": "useMouseGradient()" | kind=code-symbol | source=manager/frontend/hooks/useMouseGradient.ts:L3 | neighbors=[useMouseGradient.ts, page.tsx]
- "id_page_displaydate": "displayDate()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L91 | neighbors=[page.tsx, OverviewTab()]
- "id_page_engagementdetailpage": "EngagementDetailPage()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L412 | neighbors=[page.tsx, statusColor()]
- "id_page_overviewtab": "OverviewTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L99 | neighbors=[page.tsx, displayDate()]
- "id_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L34 | neighbors=[page.tsx, EngagementDetailPage()]
- "id_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/[id]/route.ts:L7 | neighbors=[route.ts, fail()]
- "id_route_put": "PUT()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/route.ts:L30 | neighbors=[route.ts, fail()]
- "lib_adapters_engstatustoapi": "engStatusToApi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L25 | neighbors=[adapters.ts, toApiEngagementPatch()]
- "lib_adapters_engstatustoui": "engStatusToUi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L22 | neighbors=[adapters.ts, toUiEngagement()]
- "lib_adapters_evidencetoui": "evidenceToUi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L100 | neighbors=[adapters.ts, toUiFinding()]
- "lib_adapters_severitytopriority": "severityToPriority()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L96 | neighbors=[adapters.ts, toUiFinding()]
- "lib_adapters_touiagent": "toUiAgent()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L177 | neighbors=[adapters.ts, route.ts]
- "lib_agents_store_genfieldagentid": "genFieldAgentId()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L355 | neighbors=[agents-store.ts, registerAgent()]
- "lib_agents_store_getagent": "getAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L398 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_agents_store_getallagents": "getAllAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L394 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_ai_engine_chat": "chat()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L487 | neighbors=[ai-engine.ts, getClient()]
- "lib_ai_engine_hallucinationguard": "hallucinationGuard" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L289 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_llmreportgenerator": "llmReportGenerator" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L206 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_reportsection": "ReportSection" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L9 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_vulnprioritizer": "vulnPrioritizer" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L97 | neighbors=[ai-engine.ts, route.ts]
- "lib_assistant_parseadvisor": "parseAdvisor()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L31 | neighbors=[route.ts, assistant.ts]
- "lib_assistant_preferredtext": "preferredText()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L129 | neighbors=[assistant.ts, cveRecordToFactCard()]
- "lib_assistant_publicseverity": "publicSeverity()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L135 | neighbors=[assistant.ts, cveRecordToFactCard()]
- "lib_auth_store_generateotp": "generateOtp()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L24 | neighbors=[auth-store.ts, route.ts]
- "lib_auth_store_verifyotp": "verifyOtp()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L38 | neighbors=[auth-store.ts, route.ts]
- "lib_auth_store_verifytoken": "verifyToken()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L64 | neighbors=[auth-middleware.ts, auth-store.ts]
- "lib_backend_safejson": "safeJson()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L67 | neighbors=[backend.ts, backend()]
- "lib_cases_store_getcasebyid": "getCaseById()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L231 | neighbors=[cases-store.ts, readCases()]
- "lib_clients_store_client": "Client" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L27 | neighbors=[clients-store.ts, tenant-server.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-059.json

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
