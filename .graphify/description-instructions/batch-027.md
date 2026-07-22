# Node Description Batch 28 of 76

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

- "exploit_safety_validate_payload": "validate_payload()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L174 | neighbors=[safety.py, Raises SafetyViolationError if payload …, SafetyViolationError]
- "exploit_safety_validate_scope": "validate_scope()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L212 | neighbors=[safety.py, Raises OutOfScopeError if target_ip is …, OutOfScopeError]
- "findings_page_findingdetail": "FindingDetail()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L364 | neighbors=[page.tsx, getSlaColor(), riskScoreColor()]
- "graph_analyzer_pathanalyzer_exploit_info": "._exploit_info()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L67 | neighbors=[PathAnalyzer, .movement_graph(), Best (easiest) exploitable finding on a…]
- "graph_analyzer_pathanalyzer_find_blast_radius": ".find_blast_radius()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L250 | neighbors=[PathAnalyzer, .movement_graph(), Assets reachable (and thus at risk) if …]
- "graph_analyzer_pathanalyzer_identify_chokepoints": ".identify_chokepoints()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L218 | neighbors=[PathAnalyzer, _priority(), Assets that appear in more than ``thres…]
- "graph_analyzer_pathanalyzer_materialise_path": "._materialise_path()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L175 | neighbors=[PathAnalyzer, .find_paths_to_target(), .score_path()]
- "graph_analyzer_pathanalyzer_source_assets": "._source_assets()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L129 | neighbors=[PathAnalyzer, .find_paths_to_target(), .movement_graph()]
- "graph_builder_finding_node_id": "finding_node_id()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L48 | neighbors=[builder.py, .add_exploit_edges(), .build_asset_graph()]
- "graph_builder_graphbuilder_sync_to_neo4j": ".sync_to_neo4j()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L294 | neighbors=[GraphBuilder, .build_from_db(), Mirror the current in-memory graph into…]
- "graph_builder_is_internet_exposed": "is_internet_exposed()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L83 | neighbors=[builder.py, .build_asset_graph(), _enum_value()]
- "graph_builder_to_float": "_to_float()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L59 | neighbors=[builder.py, .add_exploit_edges(), .build_asset_graph()]
- "graph_neo4j_client": "neo4j_client.py" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Neo4jClient, Neo4jClient — thin, optional wrapper ar…]
- "graph_neo4j_client_neo4jclient_ensure_schema": ".ensure_schema()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L76 | neighbors=[Neo4jClient, .run(), Apply constraints + indexes (idempotent…]
- "graph_neo4j_client_neo4jclient_run_write": ".run_write()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L95 | neighbors=[Neo4jClient, .run(), Run a parametrised write with UNWIND ba…]
- "graph_visualizer_deterministic_layout": "_deterministic_layout()" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L18 | neighbors=[visualizer.py, .to_d3(), Numpy-free seed layout: place nodes on …]
- "graph_visualizer_graphvisualizer_to_d3": ".to_d3()" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L47 | neighbors=[GraphVisualizer, _deterministic_layout(), Build the D3 payload. ``compromised`` i…]
- "hooks_usecountup": "useCountUp.ts" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, DashboardCharts.tsx, useCountUp()]
- "hooks_usemousegradient": "useMouseGradient.ts" | kind=code-symbol | source=manager/frontend/hooks/useMouseGradient.ts:L1 | neighbors=[page.tsx, 298a9d4 trim frontend to 7 core pages; …, useMouseGradient()]
- "id_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/route.ts:L13 | neighbors=[route.ts, GET, PUT()]
- "lib_adapters_normalizelist": "normalizeList()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L206 | neighbors=[adapters.ts, toApiEngagementCreate(), toApiEngagementPatch()]
- "lib_adapters_toapiengagementcreate": "toApiEngagementCreate()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L61 | neighbors=[route.ts, adapters.ts, normalizeList()]
- "lib_agents_store_ensuredatadir": "ensureDataDir()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L338 | neighbors=[agents-store.ts, readFieldAgents(), writeFieldAgents()]
- "lib_agents_store_getagent": "getAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L398 | neighbors=[route.ts, agents-store.ts, readFieldAgents()]
- "lib_agents_store_updateagentlastseen": "updateAgentLastSeen()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L385 | neighbors=[agents-store.ts, readFieldAgents(), writeFieldAgents()]
- "lib_ai_engine_assetinput": "AssetInput" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L18 | neighbors=[route.ts, ai-engine.ts, route.ts]
- "lib_ai_engine_findinginput": "FindingInput" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L11 | neighbors=[route.ts, ai-engine.ts, route.ts]
- "lib_ai_engine_stripfences": "stripFences()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L427 | neighbors=[ai-engine.ts, generateReport(), triageFindings()]
- "lib_ai_engine_triagefindings": "triageFindings()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L431 | neighbors=[ai-engine.ts, getClient(), stripFences()]
- "lib_auth_store_verifytoken": "verifyToken()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L64 | neighbors=[auth-middleware.ts, auth-store.ts, route.ts]
- "lib_cases_store_addcomment": "addComment()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L296 | neighbors=[cases-store.ts, readCases(), writeCases()]
- "lib_cases_store_createcase": "createCase()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L235 | neighbors=[cases-store.ts, readCases(), writeCases()]
- "lib_cases_store_ensuredatadir": "ensureDataDir()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L208 | neighbors=[cases-store.ts, readCases(), writeCases()]
- "lib_cases_store_updatecase": "updateCase()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L258 | neighbors=[cases-store.ts, readCases(), writeCases()]
- "lib_clients_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L47 | neighbors=[clients-store.ts, read(), write()]
- "lib_clients_store_getclientbysubdomain": "getClientBySubdomain()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L82 | neighbors=[clients-store.ts, read(), tenant-server.ts]
- "lib_clients_store_slugify": "slugify()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L71 | neighbors=[clients-store.ts, createClient(), updateClient()]
- "lib_clients_store_updateclientsettings": "updateClientSettings()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L116 | neighbors=[clients-store.ts, read(), write()]
- "lib_fetcher_apierror": "ApiError" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L8 | neighbors=[fetcher.ts, .constructor(), fetchJson()]
- "lib_fetcher_clearauth": "clearAuth()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L42 | neighbors=[PageShell.tsx, fetcher.ts, fetchJson()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-027.json

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
