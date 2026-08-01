# Node Description Batch 41 of 119

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

- "graph_builder_to_float": "_to_float()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L59 | neighbors=[builder.py, .add_exploit_edges(), .build_asset_graph()]
- "graph_neo4j_client_neo4jclient_ensure_schema": ".ensure_schema()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L76 | neighbors=[Neo4jClient, .run(), Apply constraints + indexes (idempotent…]
- "graph_neo4j_client_neo4jclient_run_write": ".run_write()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L95 | neighbors=[Neo4jClient, .run(), Run a parametrised write with UNWIND ba…]
- "graph_visualizer_deterministic_layout": "_deterministic_layout()" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L18 | neighbors=[visualizer.py, .to_d3(), Numpy-free seed layout: place nodes on …]
- "graph_visualizer_graphvisualizer_to_d3": ".to_d3()" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L47 | neighbors=[GraphVisualizer, _deterministic_layout(), Build the D3 payload. ``compromised`` i…]
- "id_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/route.ts:L13 | neighbors=[route.ts, GET, PUT()]
- "lib_adapters_normalizelist": "normalizeList()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L229 | neighbors=[adapters.ts, toApiEngagementCreate(), toApiEngagementPatch()]
- "lib_adapters_toapifindingpatch": "toApiFindingPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L197 | neighbors=[route.ts, adapters.ts, engagement-adapters.test.ts]
- "lib_agents_store_ensuredatadir": "ensureDataDir()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L338 | neighbors=[agents-store.ts, readFieldAgents(), writeFieldAgents()]
- "lib_agents_store_updateagentlastseen": "updateAgentLastSeen()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L385 | neighbors=[agents-store.ts, readFieldAgents(), writeFieldAgents()]
- "lib_ai_engine_assetinput": "AssetInput" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L18 | neighbors=[ai-engine.ts, route.ts, route.ts]
- "lib_ai_engine_findinginput": "FindingInput" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L11 | neighbors=[ai-engine.ts, route.ts, route.ts]
- "lib_ai_engine_generatereport": "generateReport()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L471 | neighbors=[ai-engine.ts, getClient(), stripFences()]
- "lib_ai_engine_stripfences": "stripFences()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L426 | neighbors=[ai-engine.ts, generateReport(), triageFindings()]
- "lib_ai_engine_triagefindings": "triageFindings()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L430 | neighbors=[ai-engine.ts, getClient(), stripFences()]
- "lib_assistant_isexploited": "isExploited()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L31 | neighbors=[assistant.ts, plainWhyItMatters(), toFactCard()]
- "lib_assistant_plainwhyitmatters": "plainWhyItMatters()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L35 | neighbors=[assistant.ts, isExploited(), toFactCard()]
- "lib_cases_store_addcomment": "addComment()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L296 | neighbors=[cases-store.ts, readCases(), writeCases()]
- "lib_cases_store_createcase": "createCase()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L235 | neighbors=[cases-store.ts, readCases(), writeCases()]
- "lib_cases_store_ensuredatadir": "ensureDataDir()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L208 | neighbors=[cases-store.ts, readCases(), writeCases()]
- "lib_cases_store_updatecase": "updateCase()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L258 | neighbors=[cases-store.ts, readCases(), writeCases()]
- "lib_clients_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L47 | neighbors=[clients-store.ts, read(), write()]
- "lib_clients_store_getclientbysubdomain": "getClientBySubdomain()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L82 | neighbors=[clients-store.ts, read(), tenant-server.ts]
- "lib_clients_store_slugify": "slugify()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L71 | neighbors=[clients-store.ts, createClient(), updateClient()]
- "lib_clients_store_updateclientsettings": "updateClientSettings()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L116 | neighbors=[clients-store.ts, read(), write()]
- "lib_fetcher_apierror": "ApiError" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L7 | neighbors=[fetcher.ts, .constructor(), fetchJson()]
- "lib_fetcher_clearauth": "clearAuth()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L19 | neighbors=[PageShell.tsx, fetcher.ts, fetchJson()]
- "lib_fetcher_getstoredtoken": "getStoredToken()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L20 | neighbors=[page.tsx, fetcher.ts, fetchJson()]
- "lib_fetcher_storetoken": "storeToken()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L30 | neighbors=[fetcher.ts, fetchJson(), page.tsx]
- "lib_finding_id_resetcounters": "resetCounters()" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L20 | neighbors=[finding-id.ts, findings-store.test.ts, parsers.test.ts]
- "lib_findings_store_deletefinding": "deleteFinding()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L142 | neighbors=[findings-store.ts, ensureDir(), getAllFindings()]
- "lib_findings_store_getfindingstats": "getFindingStats()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L94 | neighbors=[findings-store.ts, getAllFindings(), findings-store.test.ts]
- "lib_graph_store_buildattackpaths": "buildAttackPaths()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L240 | neighbors=[graph-store.ts, edgesForPath(), scorePath()]
- "lib_job_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L20 | neighbors=[job-store.ts, readJobs(), writeJobs()]
- "lib_job_store_markdispatched": "markDispatched()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L73 | neighbors=[job-store.ts, readJobs(), writeJobs()]
- "lib_job_store_updatejobstatus": "updateJobStatus()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L83 | neighbors=[job-store.ts, readJobs(), writeJobs()]
- "lib_naabu_parser_groupnaaburesults": "groupNaabuResults()" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L30 | neighbors=[tool-runners.ts, naabu-parser.ts, parsers.test.ts]
- "lib_naabu_parser_parsenaabuline": "parseNaabuLine()" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L16 | neighbors=[tool-runners.ts, naabu-parser.ts, parsers.test.ts]
- "lib_netexec_parser_parsenetexeclog": "parseNetExecLog()" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L36 | neighbors=[netexec-parser.ts, parseBoolean(), scanner-adapters.test.ts]
- "lib_nmap_parser_extractscripts": "extractScripts()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L39 | neighbors=[nmap-parser.ts, toArray(), parseNmapXml()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-040.json

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
