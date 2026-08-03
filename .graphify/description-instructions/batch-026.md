# Node Description Batch 27 of 131

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

- "graph_builder_rationale_266": "Load assets/services/findings for an engagement and build the graph." | kind=entity | source=manager/backend/app/graph/builder.py:L266 | neighbors=[.build_from_db(), Neo4jClient, Asset, Finding, Service]
- "graph_builder_rationale_295": "Mirror the current in-memory graph into Neo4j via batched writes." | kind=entity | source=manager/backend/app/graph/builder.py:L295 | neighbors=[.sync_to_neo4j(), Neo4jClient, Asset, Finding, Service]
- "graph_builder_rationale_53": "Normalise a value that may be an Enum, str, or None to a lowercase str." | kind=entity | source=manager/backend/app/graph/builder.py:L53 | neighbors=[_enum_value(), Neo4jClient, Asset, Finding, Service]
- "graph_builder_rationale_71": "Edge cost for an EXPLOITS edge. Derived from the CVSS Attack Complexity     comp" | kind=entity | source=manager/backend/app/graph/builder.py:L71 | neighbors=[exploit_complexity(), Neo4jClient, Asset, Finding, Service]
- "graph_demo_generate_demo_dataset": "generate_demo_dataset()" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L57 | neighbors=[demo.py, DemoAsset, DemoFinding, DemoService, Returns {engagement_id, assets, service…]
- "graph_visualizer": "visualizer.py" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _deterministic_layout(), GraphVisualizer, GraphVisualizer — serialise the attack …, 298a9d4 trim frontend to 7 core pages; …]
- "hooks_usecountup": "useCountUp.ts" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, DashboardCharts.tsx, useCountUp(), 298a9d4 trim frontend to 7 core pages; …]
- "lib_adapters_toapiengagementpatch": "toApiEngagementPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L210 | neighbors=[route.ts, adapters.ts, engStatusToApi(), normalizeList(), engagement-adapters.test.ts]
- "lib_assistant_cverecordtofactcard": "cveRecordToFactCard()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L104 | neighbors=[assistant.ts, preferredText(), publicSeverity(), security-context.ts, assistant.test.ts]
- "lib_assistant_detectfindingid": "detectFindingId()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L23 | neighbors=[AssistantDrawer.tsx, route.ts, assistant.ts, security-context.ts, assistant.test.ts]
- "lib_assistant_tofactcard": "toFactCard()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L46 | neighbors=[assistant.ts, isExploited(), plainWhyItMatters(), security-context.ts, assistant.test.ts]
- "lib_cases_store_writecases": "writeCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L226 | neighbors=[cases-store.ts, addComment(), createCase(), updateCase(), ensureDataDir()]
- "lib_detection_store_detectionstore": "detectionStore" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L421 | neighbors=[route.ts, detection-store.ts, route.ts, route.ts, route.ts]
- "lib_fetcher_errormessage": "errorMessage()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L84 | neighbors=[AssistantDrawer.tsx, page.tsx, page.tsx, fetcher.ts, DataState.tsx]
- "lib_fetcher_isunauthorized": "isUnauthorized()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L80 | neighbors=[page.tsx, page.tsx, fetcher.ts, page.tsx, DataState.tsx]
- "lib_finding_id_generatefindingid": "generateFindingId()" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L13 | neighbors=[scanner.ts, tool-runners.ts, finding-id.ts, findings-store.ts, testssl-parser.ts]
- "lib_findings_store_getfindingbyid": "getFindingById()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L75 | neighbors=[findings.ts, interactive.ts, findings-store.ts, getAllFindings(), findings-store.test.ts]
- "lib_findings_store_updatefinding": "updateFinding()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L132 | neighbors=[interactive.ts, findings-store.ts, ensureDir(), getAllFindings(), tools.ts]
- "lib_findings_store_updatefindingstatus": "updateFindingStatus()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L79 | neighbors=[interactive.ts, findings-store.ts, ensureDir(), getAllFindings(), findings-store.test.ts]
- "lib_job_store_writejobs": "writeJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L32 | neighbors=[job-store.ts, createJob(), markDispatched(), updateJobStatus(), ensureDir()]
- "lib_nmap_parser_parsenmapxml": "parseNmapXml()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L48 | neighbors=[tool-runners.ts, nmap-parser.ts, extractScripts(), toArray(), parsers.test.ts]
- "lib_openvas_client_runopenvasscanbackground": "runOpenVASScanBackground()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L133 | neighbors=[openvas-client.ts, boundedEnvMs(), parseOpenVASHelperOutput(), setTask(), startOpenVASScan()]
- "lib_permissions_store_getuser": "getUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L44 | neighbors=[permissions-store.ts, read(), isAdmin(), isScopeAllowed(), route.ts]
- "lib_permissions_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L35 | neighbors=[permissions-store.ts, addUser(), removeUser(), updateScopes(), ensureDir()]
- "lib_scanner_request_validation_validatenetexecscanrequest": "validateNetExecScanRequest()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L192 | neighbors=[scanner-request-validation.ts, isRecord(), validateSafeString(), validateScannerTargets(), scanner-adapters.test.ts]
- "lib_testssl_parser_parsetestssljsonchecked": "parseTestsslJsonChecked()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L56 | neighbors=[tool-runners.ts, testssl-parser.ts, parseTestsslJson(), mapSeverity(), parsers.test.ts]
- "models_base": "base.py" | kind=code-symbol | source=manager/backend/app/models/base.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Base, TimestampMixin, UUIDMixin, 298a9d4 trim frontend to 7 core pages; …]
- "models_exploit_approval": "exploit_approval.py" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, ApprovalStatus, ExploitApprovalRequest, 298a9d4 trim frontend to 7 core pages; …]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "pathid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, graphStore, GET(), 298a9d4 trim frontend to 7 core pages; …, graph-store.ts]
- "probe_pipeline_run_active": "_run_active()" | kind=code-symbol | source=probe/pipeline.py:L144 | neighbors=[pipeline.py, _Collector, .write(), _rollup(), _shared()]
- "results_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, GET(), 298a9d4 trim frontend to 7 core pages; …, detection-store.ts]
- "routers_agent_advisor_rationale_1": "agent_advisor.py — API for the agentic AI advisor (recommend-only).  POST /engag" | kind=entity | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[agent_advisor.py, AgentDecisionEngine, AgentUnavailableError, AgentRecommendation, Engagement]
- "routers_agents_get_job_status": "get_job_status()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L857 | neighbors=[agents.py, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…]
- "routers_agents_list_use_cases": "list_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L477 | neighbors=[agents.py, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…]
- "routers_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/routers/ai.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, dependencies.py, ai_generate(), ai_status()]
- "routers_attack_paths_build_analyzer": "_build_analyzer()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L175 | neighbors=[attack_paths.py, attack_graph(), blast_radius(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_list_chokepoints": "list_chokepoints()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L117 | neighbors=[attack_paths.py, _all_paths_to_critical(), _asset_labels(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_recompute_and_store": "_recompute_and_store()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L199 | neighbors=[attack_paths.py, list_attack_paths(), _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_detection_runs_rationale_1": "detection_runs.py — temporal detection API (\"what changed since last time\").  GE" | kind=entity | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[detection_runs.py, DetectionRun, Engagement, FindingStatus, Finding]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-026.json

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
