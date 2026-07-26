# Node Description Batch 48 of 104

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

- "engine_tool_runners_httpbannergrab": "httpBannerGrab()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L311 | neighbors=[tool-runners.ts, nativeBannerGrab()]
- "engine_tool_runners_tcpbannergrab": "tcpBannerGrab()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L357 | neighbors=[tool-runners.ts, nativeBannerGrab()]
- "engine_types_evidence": "Evidence" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L77 | neighbors=[types.ts, findings-store.ts]
- "exploit_msf_client_metasploitrpcclient_disconnect": ".disconnect()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L53 | neighbors=[MetasploitRPCClient, ._call()]
- "exploit_msf_client_metasploitrpcclient_module_info": ".module_info()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L126 | neighbors=[MetasploitRPCClient, ._call()]
- "exploit_nuclei_exploit_nucleiexploitrunner_extract_evidence": "._extract_evidence()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L184 | neighbors=[NucleiExploitRunner, ._parse_poc_output()]
- "exploit_nuclei_exploit_nucleiexploitrunner_safe_template_check": ".safe_template_check()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L60 | neighbors=[NucleiExploitRunner, Parse template YAML and validate it con…]
- "exploit_nuclei_exploit_rationale_1": "NucleiExploitRunner — CVE PoC validation using Nuclei templates.  Enforces templ" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L1 | neighbors=[nuclei_exploit.py, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_121": "Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L121 | neighbors=[.run_cve_poc(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_161": "Parse nuclei JSONL output for a single CVE PoC result." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L161 | neighbors=[._parse_poc_output(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_49": "Run Nuclei CVE PoC templates against a single target.     Every template is safe" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L49 | neighbors=[NucleiExploitRunner, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_61": "Parse template YAML and validate it contains no write/delete/DoS actions." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L61 | neighbors=[.safe_template_check(), SafetyViolationError]
- "exploit_orchestrator_exploitorchestrator_audit": "._audit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L322 | neighbors=[ExploitOrchestrator, .execute()]
- "exploit_orchestrator_exploitorchestrator_generate_dns_callback_token": ".generate_dns_callback_token()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L255 | neighbors=[ExploitOrchestrator, Returns a unique FQDN for out-of-band D…]
- "exploit_safety_requires_approval": "requires_approval()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L239 | neighbors=[safety.py, True if this target requires human mana…]
- "findings_page_findingspage": "FindingsPage()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L714 | neighbors=[page.tsx, riskScoreColor()]
- "findings_page_getslacolor": "getSlaColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L93 | neighbors=[page.tsx, FindingDetail()]
- "findings_page_riskbadge": "RiskBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L137 | neighbors=[page.tsx, riskScoreColor()]
- "frontend_eslint_config": "eslint.config.mjs" | kind=code-symbol | source=manager/frontend/eslint.config.mjs:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, eslintConfig]
- "frontend_middleware_ispublic": "isPublic()" | kind=code-symbol | source=manager/frontend/middleware.ts:L14 | neighbors=[middleware.ts, middleware()]
- "frontend_middleware_middleware": "middleware()" | kind=code-symbol | source=manager/frontend/middleware.ts:L19 | neighbors=[middleware.ts, isPublic()]
- "frontend_postcss_config": "postcss.config.mjs" | kind=code-symbol | source=manager/frontend/postcss.config.mjs:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, config]
- "graph_analyzer_priority": "_priority()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L285 | neighbors=[analyzer.py, .identify_chokepoints()]
- "graph_analyzer_safe_float": "_safe_float()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L278 | neighbors=[analyzer.py, .score_path()]
- "graph_builder_service_node_id": "service_node_id()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L44 | neighbors=[builder.py, .build_asset_graph()]
- "graph_demo_demoservice": "DemoService" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L37 | neighbors=[demo.py, generate_demo_dataset()]
- "graph_neo4j_client_neo4jclient_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L61 | neighbors=[Neo4jClient, Open the driver and verify connectivity…]
- "hooks_usecountup_usecountup": "useCountUp()" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L3 | neighbors=[DashboardCharts.tsx, useCountUp.ts]
- "hooks_usemousegradient_usemousegradient": "useMouseGradient()" | kind=code-symbol | source=manager/frontend/hooks/useMouseGradient.ts:L3 | neighbors=[page.tsx, useMouseGradient.ts]
- "id_page_engagementdetailpage": "EngagementDetailPage()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L367 | neighbors=[page.tsx, statusColor()]
- "id_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L34 | neighbors=[page.tsx, EngagementDetailPage()]
- "id_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/[id]/route.ts:L7 | neighbors=[route.ts, fail()]
- "id_route_put": "PUT()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/route.ts:L30 | neighbors=[route.ts, fail()]
- "install_install_copyfile": "copyFile()" | kind=code-symbol | source=probe-go/install/install.go:L149 | neighbors=[install.go, Install()]
- "install_install_installlaunchd": "installLaunchd()" | kind=code-symbol | source=probe-go/install/install.go:L67 | neighbors=[install.go, Install()]
- "install_install_installsystemd": "installSystemd()" | kind=code-symbol | source=probe-go/install/install.go:L105 | neighbors=[install.go, Install()]
- "lib_adapters_engstatustoapi": "engStatusToApi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L25 | neighbors=[adapters.ts, toApiEngagementPatch()]
- "lib_adapters_engstatustoui": "engStatusToUi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L22 | neighbors=[adapters.ts, toUiEngagement()]
- "lib_adapters_severitytopriority": "severityToPriority()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L89 | neighbors=[adapters.ts, toUiFinding()]
- "lib_adapters_toapifindingpatch": "toApiFindingPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L174 | neighbors=[route.ts, adapters.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-047.json

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
