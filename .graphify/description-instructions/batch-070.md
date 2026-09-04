# Node Description Batch 71 of 332

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

- "exploit_msf_client_metasploitrpcclient_raw_call": "._raw_call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L157 | neighbors=[MetasploitRPCClient, ._call(), .connect(), MetasploitRPCError]
- "exploit_msf_client_metasploitrpcclient_run_module": ".run_module()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L83 | neighbors=[MetasploitRPCClient, ._call(), MetasploitRPCError, Execute a Metasploit module.         Re…]
- "exploit_msf_client_metasploitrpcclient_wait_for_job": ".wait_for_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L132 | neighbors=[MetasploitRPCClient, .get_job_status(), .kill_job(), Poll until job completes or max_wait ex…]
- "exploit_nuclei_exploit_nucleiexploitrunner_run_cve_poc": ".run_cve_poc()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L117 | neighbors=[NucleiExploitRunner, ._parse_poc_output(), Run Nuclei CVE PoC template against tar…, Run Nuclei CVE PoC template against tar…]
- "exploit_orchestrator_exploitorchestrator_check_approval_required": "._check_approval_required()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L287 | neighbors=[ExploitOrchestrator, .execute(), Creates and returns an ExploitApprovalR…, Creates and returns an ExploitApprovalR…]
- "exploit_orchestrator_exploitorchestrator_check_blast_radius": "._check_blast_radius()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L265 | neighbors=[ExploitOrchestrator, .execute(), Count running exploit jobs for this eng…, Count running exploit jobs for this eng…]
- "exploit_orchestrator_exploitorchestrator_select_exploit": ".select_exploit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L67 | neighbors=[ExploitOrchestrator, .execute(), Returns {module, payload, safe_check} f…, Returns {module, payload, safe_check} f…]
- "exploit_orchestrator_exploitorchestrator_validate_safety": ".validate_safety()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L103 | neighbors=[ExploitOrchestrator, .execute(), Raises SafetyViolationError if module o…, Raises SafetyViolationError if module o…]
- "exploit_orchestrator_exploitorchestrator_validate_scope": ".validate_scope()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L110 | neighbors=[ExploitOrchestrator, .execute(), Raises OutOfScopeError if target_ip not…, Raises OutOfScopeError if target_ip not…]
- "findings_page_findingdetail": "FindingDetail()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L75 | neighbors=[page.tsx, signalChips(), getSlaColor(), riskScoreColor()]
- "findings_page_getslacolor": "getSlaColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L251 | neighbors=[page.tsx, FindingDetail(), isUrgent(), urgencyReasons()]
- "findings_page_riskscorecolor": "riskScoreColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L107 | neighbors=[page.tsx, FindingDetail(), FindingsPage(), RiskBadge()]
- "frontend_eslint_config": "eslint.config.mjs" | kind=code-symbol | source=manager/frontend/eslint.config.mjs:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, eslintConfig, 298a9d4 trim frontend to 7 core pages; …]
- "graph_analyzer_pathanalyzer_score_path": ".score_path()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L199 | neighbors=[PathAnalyzer, ._materialise_path(), _safe_float(), Risk score 0–100 from: sum of exploit C…]
- "graph_builder_exploit_complexity": "exploit_complexity()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L70 | neighbors=[builder.py, _enum_value(), .add_exploit_edges(), Edge cost for an EXPLOITS edge. Derived…]
- "graph_builder_graphbuilder_add_credential_edges": "._add_credential_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L244 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), CREDENTIAL_REUSE edges between assets s…]
- "graph_builder_graphbuilder_add_network_edges": ".add_network_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L208 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), Add CONNECTS_TO (directed reachability)…]
- "graph_builder_graphbuilder_build_from_db": ".build_from_db()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L265 | neighbors=[GraphBuilder, .build_asset_graph(), .sync_to_neo4j(), Load assets/services/findings for an en…]
- "graph_neo4j_client": "neo4j_client.py" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Neo4jClient, Neo4jClient — thin, optional wrapper ar…, 298a9d4 trim frontend to 7 core pages; …]
- "graph_neo4j_client_neo4jclient_run": ".run()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L87 | neighbors=[Neo4jClient, .ensure_schema(), .run_write(), Run a Cypher statement and return recor…]
- "hooks_usemousegradient": "useMouseGradient.ts" | kind=code-symbol | source=manager/frontend/hooks/useMouseGradient.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, useMouseGradient(), page.tsx, 298a9d4 trim frontend to 7 core pages; …]
- "lib_adapters_toapiengagementcreate": "toApiEngagementCreate()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L65 | neighbors=[route.ts, adapters.ts, normalizeList(), engagement-adapters.test.ts]
- "lib_adapters_toapifindingpatch": "toApiFindingPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L235 | neighbors=[route.ts, adapters.ts, engagement-adapters.test.ts, findings-adapters.test.ts]
- "lib_adapters_touiengagement": "toUiEngagement()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L35 | neighbors=[route.ts, route.ts, adapters.ts, engStatusToUi()]
- "lib_agents_store_registeragent": "registerAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L362 | neighbors=[agents-store.ts, genFieldAgentId(), readFieldAgents(), writeFieldAgents()]
- "lib_agents_store_writefieldagents": "writeFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L350 | neighbors=[agents-store.ts, registerAgent(), updateAgentLastSeen(), ensureDataDir()]
- "lib_ai_engine_getclient": "getClient()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L432 | neighbors=[ai-engine.ts, chat(), generateReport(), triageFindings()]
- "lib_assistant_access_canmountassistant": "canMountAssistant()" | kind=code-symbol | source=manager/frontend/lib/assistant-access.ts:L12 | neighbors=[AssistantProvider.tsx, assistant-access.ts, isAssistantRoute(), operator-routes.test.ts]
- "lib_assistant_access_isassistantroute": "isAssistantRoute()" | kind=code-symbol | source=manager/frontend/lib/assistant-access.ts:L2 | neighbors=[AssistantProvider.tsx, assistant-access.ts, canMountAssistant(), operator-routes.test.ts]
- "lib_campaign_store_issafecampaignid": "isSafeCampaignId()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L87 | neighbors=[campaign-store.ts, getCampaign(), validateSnapshot(), campaign-store.test.ts]
- "lib_clients_store_createclient": "createClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L87 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_clients_store_updateclient": "updateClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L105 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_console_source_consolequerykey": "consoleQueryKey()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L139 | neighbors=[page.tsx, page.tsx, console-source.tsx, useConsoleQueryKey()]
- "lib_console_source_useconsolequerykey": "useConsoleQueryKey()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L144 | neighbors=[DashboardGrid.tsx, console-source.tsx, consoleQueryKey(), useConsoleSource()]
- "lib_console_source_useconsolesource": "useConsoleSource()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L131 | neighbors=[console-source.tsx, useConsoleCapability(), useConsoleQuery(), useConsoleQueryKey()]
- "lib_errors_diagnosespawnerror": "diagnoseSpawnError()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L244 | neighbors=[tool-runners.ts, errors.ts, VedhaError, AdversaError]
- "lib_httpx_parser_httpxjsonldecoder_decode": ".decode()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L116 | neighbors=[HttpxJsonlDecoder, .push(), parseHttpxJsonLine(), .finish()]
- "lib_job_store_createjob": "createJob()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L41 | neighbors=[job-store.ts, genJobId(), readJobs(), writeJobs()]
- "lib_nuclei_parser_nucleiseveritytoseverity": "nucleiSeverityToSeverity()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L71 | neighbors=[tool-runners.ts, nuclei-parser.ts, nucleiMatchToFinding(), parsers.test.ts]
- "lib_permissions_store_adduser": "addUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L60 | neighbors=[permissions-store.ts, read(), write(), route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-070.json

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
