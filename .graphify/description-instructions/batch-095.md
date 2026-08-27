# Node Description Batch 96 of 236

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

- "exploit_nuclei_exploit_rationale_121": "Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L121 | neighbors=[.run_cve_poc(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_161": "Parse nuclei JSONL output for a single CVE PoC result." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L161 | neighbors=[._parse_poc_output(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_49": "Run Nuclei CVE PoC templates against a single target.     Every template is safe" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L49 | neighbors=[NucleiExploitRunner, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_61": "Parse template YAML and validate it contains no write/delete/DoS actions." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L61 | neighbors=[.safe_template_check(), SafetyViolationError]
- "exploit_orchestrator_exploitorchestrator_audit": "._audit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L319 | neighbors=[ExploitOrchestrator, .execute()]
- "exploit_safety_requires_approval": "requires_approval()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L239 | neighbors=[safety.py, True if this target requires human mana…]
- "findings_page_findingspage": "FindingsPage()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1025 | neighbors=[page.tsx, riskScoreColor()]
- "findings_page_fixfirststrip": "FixFirstStrip()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L915 | neighbors=[page.tsx, useCountUp()]
- "findings_page_isurgent": "isUrgent()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L864 | neighbors=[page.tsx, getSlaColor()]
- "findings_page_riskbadge": "RiskBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L161 | neighbors=[page.tsx, riskScoreColor()]
- "findings_page_urgencyreasons": "urgencyReasons()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L870 | neighbors=[page.tsx, getSlaColor()]
- "findings_page_usecountup": "useCountUp()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L882 | neighbors=[page.tsx, FixFirstStrip()]
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
- "lib_adapters_touiagent": "toUiAgent()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L191 | neighbors=[adapters.ts, route.ts]
- "lib_agents_store_genfieldagentid": "genFieldAgentId()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L355 | neighbors=[agents-store.ts, registerAgent()]
- "lib_agents_store_getagent": "getAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L398 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_agents_store_getallagents": "getAllAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L394 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_ai_engine_chat": "chat()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L487 | neighbors=[ai-engine.ts, getClient()]
- "lib_ai_engine_hallucinationguard": "hallucinationGuard" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L289 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_llmreportgenerator": "llmReportGenerator" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L206 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_reportsection": "ReportSection" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L9 | neighbors=[ai-engine.ts, route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-095.json

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
