# Node Description Batch 42 of 236

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

- "graph_analyzer_pathanalyzer_find_paths_to_target": ".find_paths_to_target()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L140 | neighbors=[PathAnalyzer, ._materialise_path(), .movement_graph(), ._source_assets(), Return scored attack paths from every s…] | lang=en
- "graph_builder_asset_node_id": "asset_node_id()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L40 | neighbors=[builder.py, ._add_credential_edges(), .add_exploit_edges(), .add_network_edges(), .build_asset_graph()] | lang=en
- "graph_builder_enum_value": "_enum_value()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L52 | neighbors=[builder.py, exploit_complexity(), .build_asset_graph(), is_internet_exposed(), Normalise a value that may be an Enum, …] | lang=en
- "graph_builder_rationale_1": "GraphBuilder — turns engagement assets/services/findings into an attack graph." | kind=entity | source=manager/backend/app/graph/builder.py:L1 | neighbors=[builder.py, Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_108": "Build the full multi-type attack graph. Returns the populated DiGraph         (a" | kind=entity | source=manager/backend/app/graph/builder.py:L108 | neighbors=[.build_asset_graph(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_184": "For each exploitable finding add an EXPLOITS edge Finding→Asset with         ``w" | kind=entity | source=manager/backend/app/graph/builder.py:L184 | neighbors=[.add_exploit_edges(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_209": "Add CONNECTS_TO (directed reachability) and SAME_SEGMENT edges from         segm" | kind=entity | source=manager/backend/app/graph/builder.py:L209 | neighbors=[.add_network_edges(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_245": "CREDENTIAL_REUSE edges between assets sharing a credential.         ``credential" | kind=entity | source=manager/backend/app/graph/builder.py:L245 | neighbors=[._add_credential_edges(), Neo4jClient, Asset, Finding, Service] | lang=pt
- "graph_builder_rationale_266": "Load assets/services/findings for an engagement and build the graph." | kind=entity | source=manager/backend/app/graph/builder.py:L266 | neighbors=[.build_from_db(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_295": "Mirror the current in-memory graph into Neo4j via batched writes." | kind=entity | source=manager/backend/app/graph/builder.py:L295 | neighbors=[.sync_to_neo4j(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_53": "Normalise a value that may be an Enum, str, or None to a lowercase str." | kind=entity | source=manager/backend/app/graph/builder.py:L53 | neighbors=[_enum_value(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_71": "Edge cost for an EXPLOITS edge. Derived from the CVSS Attack Complexity     comp" | kind=entity | source=manager/backend/app/graph/builder.py:L71 | neighbors=[exploit_complexity(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_demo_generate_demo_dataset": "generate_demo_dataset()" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L57 | neighbors=[demo.py, DemoAsset, DemoFinding, DemoService, Returns {engagement_id, assets, service…] | lang=en
- "graph_visualizer": "visualizer.py" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _deterministic_layout(), GraphVisualizer, GraphVisualizer — serialise the attack …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "hooks_usecountup": "useCountUp.ts" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, DashboardCharts.tsx, useCountUp(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "lib_adapters_toapiengagementpatch": "toApiEngagementPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L224 | neighbors=[route.ts, adapters.ts, engStatusToApi(), normalizeList(), engagement-adapters.test.ts] | lang=en
- "lib_assistant_cverecordtofactcard": "cveRecordToFactCard()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L147 | neighbors=[assistant.ts, preferredText(), publicSeverity(), security-context.ts, assistant.test.ts] | lang=en
- "lib_assistant_detectfindingid": "detectFindingId()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L66 | neighbors=[AssistantDrawer.tsx, route.ts, assistant.ts, security-context.ts, assistant.test.ts] | lang=en
- "lib_assistant_tofactcard": "toFactCard()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L89 | neighbors=[assistant.ts, isExploited(), plainWhyItMatters(), security-context.ts, assistant.test.ts] | lang=en
- "lib_backend_cookiefrom": "cookieFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L76 | neighbors=[backend.ts, bearerFrom(), route.ts, route.ts, backend-auth.test.ts] | lang=en
- "lib_cases_store_writecases": "writeCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L226 | neighbors=[cases-store.ts, addComment(), createCase(), updateCase(), ensureDataDir()] | lang=en
- "lib_detection_store_detectionstore": "detectionStore" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L421 | neighbors=[route.ts, detection-store.ts, route.ts, route.ts, route.ts] | lang=en
- "lib_fetcher_errormessage": "errorMessage()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L84 | neighbors=[AssistantDrawer.tsx, page.tsx, page.tsx, fetcher.ts, DataState.tsx] | lang=en
- "lib_fetcher_isunauthorized": "isUnauthorized()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L80 | neighbors=[page.tsx, page.tsx, fetcher.ts, page.tsx, DataState.tsx] | lang=en
- "lib_finding_id_generatefindingid": "generateFindingId()" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L13 | neighbors=[scanner.ts, tool-runners.ts, finding-id.ts, findings-store.ts, testssl-parser.ts] | lang=en
- "lib_findings_store_getfindingbyid": "getFindingById()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L75 | neighbors=[findings.ts, interactive.ts, findings-store.ts, getAllFindings(), findings-store.test.ts] | lang=en
- "lib_findings_store_updatefinding": "updateFinding()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L132 | neighbors=[interactive.ts, findings-store.ts, ensureDir(), getAllFindings(), tools.ts] | lang=en
- "lib_findings_store_updatefindingstatus": "updateFindingStatus()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L79 | neighbors=[interactive.ts, findings-store.ts, ensureDir(), getAllFindings(), findings-store.test.ts] | lang=en
- "lib_job_store_writejobs": "writeJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L32 | neighbors=[job-store.ts, createJob(), markDispatched(), updateJobStatus(), ensureDir()] | lang=en
- "lib_nmap_parser_parsenmapxml": "parseNmapXml()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L48 | neighbors=[tool-runners.ts, nmap-parser.ts, extractScripts(), toArray(), parsers.test.ts] | lang=en
- "lib_openvas_client_runopenvasscanbackground": "runOpenVASScanBackground()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L133 | neighbors=[openvas-client.ts, boundedEnvMs(), parseOpenVASHelperOutput(), setTask(), startOpenVASScan()] | lang=en
- "lib_permissions_store_getuser": "getUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L44 | neighbors=[permissions-store.ts, read(), isAdmin(), isScopeAllowed(), route.ts] | lang=en
- "lib_permissions_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L35 | neighbors=[permissions-store.ts, addUser(), removeUser(), updateScopes(), ensureDir()] | lang=en
- "lib_portal_client_portalengagement": "PortalEngagement" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L42 | neighbors=[portal-client.ts, page.tsx, page.tsx, page.tsx, page.tsx] | lang=en
- "lib_scanner_request_validation_validatenetexecscanrequest": "validateNetExecScanRequest()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L192 | neighbors=[scanner-request-validation.ts, isRecord(), validateSafeString(), validateScannerTargets(), scanner-adapters.test.ts] | lang=en
- "lib_severity_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L13 | neighbors=[Primitives.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx, severity.ts] | lang=en
- "lib_testssl_parser_parsetestssljsonchecked": "parseTestsslJsonChecked()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L56 | neighbors=[tool-runners.ts, testssl-parser.ts, parseTestsslJson(), mapSeverity(), parsers.test.ts] | lang=en
- "main_scripts_accuracy_evaluate_corpus": "evaluate_corpus()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L124 | neighbors=[accuracy.py, score_findings(), score_port_states(), _main(), Run the findings engine over a labeled …] | lang=en
- "main_scripts_accuracy_score_port_states": "score_port_states()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L94 | neighbors=[accuracy.py, evaluate_corpus(), OPEN precision/recall + overall state a…, _observed_states(), _ratio()] | lang=en
- "main_scripts_adaptive_timeout_adaptivetimeout": "AdaptiveTimeout" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L17 | neighbors=[adaptive_timeout.py, .__init__(), .observe(), .timeout(), from_rtts()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-041.json

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
