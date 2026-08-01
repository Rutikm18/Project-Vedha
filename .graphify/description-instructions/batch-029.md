# Node Description Batch 30 of 119

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

- "detection_engine_vuln_db_load_snapshot": "load_snapshot()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L119 | neighbors=[vuln_db.py, _content_hash(), SnapshotMeta, VulnDB]
- "detection_logger_attacklogger": "AttackLogger" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L23 | neighbors=[logger.py, .__init__(), .log_action(), AttackTimeline]
- "detection_siem_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L35 | neighbors=[siem.py, .parse_response(), .parse_response(), .parse_response()]
- "detection_siem_siemqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L68 | neighbors=[.query_alerts(), .query_alerts(), SIEMQueryEngine, .query_alerts()]
- "discovery_rate_limiter": "rate_limiter.py" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, RateLimiter, RateLimiter — enforces PPS limits per C…, 298a9d4 trim frontend to 7 core pages; …]
- "discovery_xml_parser_nmapxmlparser_parse_host": "._parse_host()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L53 | neighbors=[NmapXMLParser, .parse(), ._parse_port(), ParsedHost]
- "engine_tool_runners_iswindows": "isWindows()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L30 | neighbors=[tool-runners.ts, binName(), hasSystemBinary(), spawnOpts()]
- "engine_types_scansummary": "ScanSummary" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L119 | neighbors=[llm.ts, scanner.ts, types.ts, output.ts]
- "exploit_msf_client_metasploitrpcclient_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L38 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, Authenticate with msfrpcd and store the…]
- "exploit_msf_client_metasploitrpcclient_get_job_status": ".get_job_status()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L102 | neighbors=[MetasploitRPCClient, ._call(), .wait_for_job(), Returns {status, output, uuid}.]
- "exploit_msf_client_metasploitrpcclient_kill_job": ".kill_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L118 | neighbors=[MetasploitRPCClient, ._call(), .wait_for_job(), Returns True if job was successfully ki…]
- "exploit_msf_client_metasploitrpcclient_raw_call": "._raw_call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L157 | neighbors=[MetasploitRPCClient, ._call(), .connect(), MetasploitRPCError]
- "exploit_msf_client_metasploitrpcclient_run_module": ".run_module()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L83 | neighbors=[MetasploitRPCClient, ._call(), MetasploitRPCError, Execute a Metasploit module.         Re…]
- "exploit_msf_client_metasploitrpcclient_wait_for_job": ".wait_for_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L132 | neighbors=[MetasploitRPCClient, .get_job_status(), .kill_job(), Poll until job completes or max_wait ex…]
- "exploit_nuclei_exploit": "nuclei_exploit.py" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, NucleiExploitRunner, NucleiExploitRunner — CVE PoC validatio…, 298a9d4 trim frontend to 7 core pages; …]
- "exploit_nuclei_exploit_nucleiexploitrunner_parse_poc_output": "._parse_poc_output()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L160 | neighbors=[NucleiExploitRunner, ._extract_evidence(), .run_cve_poc(), Parse nuclei JSONL output for a single …]
- "findings_page_getslacolor": "getSlaColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L109 | neighbors=[page.tsx, FindingDetail(), isUrgent(), urgencyReasons()]
- "findings_page_riskscorecolor": "riskScoreColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L107 | neighbors=[page.tsx, FindingDetail(), FindingsPage(), RiskBadge()]
- "graph_analyzer_pathanalyzer_score_path": ".score_path()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L199 | neighbors=[PathAnalyzer, ._materialise_path(), _safe_float(), Risk score 0–100 from: sum of exploit C…]
- "graph_builder_exploit_complexity": "exploit_complexity()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L70 | neighbors=[builder.py, _enum_value(), .add_exploit_edges(), Edge cost for an EXPLOITS edge. Derived…]
- "graph_builder_graphbuilder_add_credential_edges": "._add_credential_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L244 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), CREDENTIAL_REUSE edges between assets s…]
- "graph_builder_graphbuilder_add_network_edges": ".add_network_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L208 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), Add CONNECTS_TO (directed reachability)…]
- "graph_builder_graphbuilder_build_from_db": ".build_from_db()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L265 | neighbors=[GraphBuilder, .build_asset_graph(), .sync_to_neo4j(), Load assets/services/findings for an en…]
- "graph_neo4j_client": "neo4j_client.py" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Neo4jClient, Neo4jClient — thin, optional wrapper ar…, 298a9d4 trim frontend to 7 core pages; …]
- "graph_neo4j_client_neo4jclient_run": ".run()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L87 | neighbors=[Neo4jClient, .ensure_schema(), .run_write(), Run a Cypher statement and return recor…]
- "hooks_usecountup": "useCountUp.ts" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, DashboardCharts.tsx, useCountUp(), 298a9d4 trim frontend to 7 core pages; …]
- "hooks_usemousegradient": "useMouseGradient.ts" | kind=code-symbol | source=manager/frontend/hooks/useMouseGradient.ts:L1 | neighbors=[page.tsx, d1b4dd3 trim frontend to 7 core pages; …, useMouseGradient(), 298a9d4 trim frontend to 7 core pages; …]
- "install_install_install": "Install()" | kind=code-symbol | source=probe-go/install/install.go:L20 | neighbors=[install.go, copyFile(), installLaunchd(), installSystemd()]
- "lib_adapters_toapiengagementpatch": "toApiEngagementPatch()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L210 | neighbors=[route.ts, adapters.ts, engStatusToApi(), normalizeList()]
- "lib_adapters_touiengagement": "toUiEngagement()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L31 | neighbors=[route.ts, route.ts, adapters.ts, engStatusToUi()]
- "lib_agents_store_registeragent": "registerAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L362 | neighbors=[agents-store.ts, genFieldAgentId(), readFieldAgents(), writeFieldAgents()]
- "lib_agents_store_writefieldagents": "writeFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L350 | neighbors=[agents-store.ts, registerAgent(), updateAgentLastSeen(), ensureDataDir()]
- "lib_ai_engine_getclient": "getClient()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L422 | neighbors=[ai-engine.ts, chat(), generateReport(), triageFindings()]
- "lib_clients_store_createclient": "createClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L87 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_clients_store_updateclient": "updateClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L105 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_errors_diagnosespawnerror": "diagnoseSpawnError()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L244 | neighbors=[tool-runners.ts, errors.ts, VedhaError, AdversaError]
- "lib_fetcher_errormessage": "errorMessage()" | kind=code-symbol | source=manager/frontend/lib/fetcher.ts:L84 | neighbors=[page.tsx, page.tsx, fetcher.ts, DataState.tsx]
- "lib_httpx_parser_httpxjsonldecoder_decode": ".decode()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L116 | neighbors=[HttpxJsonlDecoder, .push(), parseHttpxJsonLine(), .finish()]
- "lib_job_store_createjob": "createJob()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L41 | neighbors=[job-store.ts, genJobId(), readJobs(), writeJobs()]
- "lib_nuclei_parser_nucleiseveritytoseverity": "nucleiSeverityToSeverity()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L71 | neighbors=[tool-runners.ts, nuclei-parser.ts, nucleiMatchToFinding(), parsers.test.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-029.json

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
