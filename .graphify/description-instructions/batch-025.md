# Node Description Batch 26 of 104

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

- "exploit_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…]
- "findings_page_riskscorecolor": "riskScoreColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L107 | neighbors=[page.tsx, FindingDetail(), FindingsPage(), RiskBadge()]
- "gaps_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/gaps/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, GET(), detection-store.ts, detectionStore]
- "graph_analyzer_pathanalyzer_score_path": ".score_path()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L199 | neighbors=[PathAnalyzer, ._materialise_path(), _safe_float(), Risk score 0–100 from: sum of exploit C…]
- "graph_builder_exploit_complexity": "exploit_complexity()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L70 | neighbors=[builder.py, _enum_value(), .add_exploit_edges(), Edge cost for an EXPLOITS edge. Derived…]
- "graph_builder_graphbuilder_add_credential_edges": "._add_credential_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L244 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), CREDENTIAL_REUSE edges between assets s…]
- "graph_builder_graphbuilder_add_network_edges": ".add_network_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L208 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), Add CONNECTS_TO (directed reachability)…]
- "graph_builder_graphbuilder_build_from_db": ".build_from_db()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L265 | neighbors=[GraphBuilder, .build_asset_graph(), .sync_to_neo4j(), Load assets/services/findings for an en…]
- "graph_neo4j_client_neo4jclient_run": ".run()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L87 | neighbors=[Neo4jClient, .ensure_schema(), .run_write(), Run a Cypher statement and return recor…]
- "graph_visualizer": "visualizer.py" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _deterministic_layout(), GraphVisualizer, GraphVisualizer — serialise the attack …]
- "install_install_install": "Install()" | kind=code-symbol | source=probe-go/install/install.go:L20 | neighbors=[install.go, copyFile(), installLaunchd(), installSystemd()]
- "jobid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, GET(), ai-engine.ts, aiReportStore]
- "lib_adapters_toapiengagementpatch": "toApiEngagementPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L187 | neighbors=[route.ts, adapters.ts, engStatusToApi(), normalizeList()]
- "lib_adapters_touiengagement": "toUiEngagement()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L31 | neighbors=[route.ts, route.ts, adapters.ts, engStatusToUi()]
- "lib_adapters_touifinding": "toUiFinding()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L96 | neighbors=[route.ts, route.ts, adapters.ts, severityToPriority()]
- "lib_agents_store_registeragent": "registerAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L362 | neighbors=[agents-store.ts, genFieldAgentId(), readFieldAgents(), writeFieldAgents()]
- "lib_agents_store_writefieldagents": "writeFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L350 | neighbors=[agents-store.ts, registerAgent(), updateAgentLastSeen(), ensureDataDir()]
- "lib_ai_engine_generatereport": "generateReport()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L472 | neighbors=[route.ts, ai-engine.ts, getClient(), stripFences()]
- "lib_ai_engine_getclient": "getClient()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L423 | neighbors=[ai-engine.ts, chat(), generateReport(), triageFindings()]
- "lib_auth_middleware_withauth": "withAuth()" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L15 | neighbors=[route.ts, auth-middleware.ts, route.ts, route.ts]
- "lib_clients_store_createclient": "createClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L87 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_clients_store_updateclient": "updateClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L105 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_errors_diagnosespawnerror": "diagnoseSpawnError()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L244 | neighbors=[tool-runners.ts, errors.ts, VedhaError, AdversaError]
- "lib_fetcher_isunauthorized": "isUnauthorized()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L107 | neighbors=[page.tsx, page.tsx, fetcher.ts, DataState.tsx]
- "lib_nuclei_parser_nucleimatchtofinding": "nucleiMatchToFinding()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L84 | neighbors=[nuclei-parser.ts, nucleiSeverityToSeverity(), route.ts, route.ts]
- "lib_nuclei_parser_nucleiseveritytoseverity": "nucleiSeverityToSeverity()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L71 | neighbors=[tool-runners.ts, nuclei-parser.ts, nucleiMatchToFinding(), parsers.test.ts]
- "lib_openvas_client_startopenvasscan": "startOpenVASScan()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L44 | neighbors=[openvas-client.ts, runOpenVASScanBackground(), setTask(), route.ts]
- "lib_permissions_store_adduser": "addUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L60 | neighbors=[permissions-store.ts, read(), write(), route.ts]
- "lib_permissions_store_isemailallowed": "isEmailAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L48 | neighbors=[auth-middleware.ts, permissions-store.ts, read(), route.ts]
- "lib_permissions_store_isscopeallowed": "isScopeAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L109 | neighbors=[permissions-store.ts, getUser(), read(), route.ts]
- "lib_testssl_parser_parsetestssloutput": "parseTestsslOutput()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L28 | neighbors=[testssl-parser.ts, parseTestsslJson(), route.ts, route.ts]
- "models_base": "base.py" | kind=code-symbol | source=manager/backend/app/models/base.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Base, TimestampMixin, UUIDMixin]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder.  Creates a ten…]
- "models_exploit_approval": "exploit_approval.py" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Enum, ApprovalStatus, ExploitApprovalRequest]
- "models_llm_output_rationale_13": "Every LLM generation is persisted here for human-in-the-loop review.      AI out" | kind=entity | source=manager/backend/app/models/llm_output.py:L13 | neighbors=[Base, TimestampMixin, ReviewStatus, LLMOutput]
- "models_tenant_tenant": "Tenant" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L11 | neighbors=[tenant.py, Base, Base, Idempotent admin seeder.  Creates a ten…]
- "native_dir_bust_nativedirbust": "nativeDirBust()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L113 | neighbors=[tool-runners.ts, dir-bust.ts, loadWordlist(), probe()]
- "native_dns_recon_nativednsrecon": "nativeDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L53 | neighbors=[tool-runners.ts, dns-recon.ts, attemptZoneTransfer(), safe()]
- "pathid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, graph-store.ts, graphStore, GET()]
- "probe_go_main_localscan": "localScan()" | kind=code-symbol | source=probe-go/main.go:L86 | neighbors=[main.go, renderReport(), run(), main()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-025.json

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
