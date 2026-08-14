# Node Description Batch 44 of 186

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

- "frontend_eslint_config": "eslint.config.mjs" | kind=code-symbol | source=manager/frontend/eslint.config.mjs:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, eslintConfig, 298a9d4 trim frontend to 7 core pages; …]
- "graph_analyzer_pathanalyzer_score_path": ".score_path()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L199 | neighbors=[PathAnalyzer, ._materialise_path(), _safe_float(), Risk score 0–100 from: sum of exploit C…]
- "graph_builder_exploit_complexity": "exploit_complexity()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L70 | neighbors=[builder.py, _enum_value(), .add_exploit_edges(), Edge cost for an EXPLOITS edge. Derived…]
- "graph_builder_graphbuilder_add_credential_edges": "._add_credential_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L244 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), CREDENTIAL_REUSE edges between assets s…]
- "graph_builder_graphbuilder_add_network_edges": ".add_network_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L208 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), Add CONNECTS_TO (directed reachability)…]
- "graph_builder_graphbuilder_build_from_db": ".build_from_db()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L265 | neighbors=[GraphBuilder, .build_asset_graph(), .sync_to_neo4j(), Load assets/services/findings for an en…]
- "graph_neo4j_client": "neo4j_client.py" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Neo4jClient, Neo4jClient — thin, optional wrapper ar…, 298a9d4 trim frontend to 7 core pages; …]
- "graph_neo4j_client_neo4jclient_run": ".run()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L87 | neighbors=[Neo4jClient, .ensure_schema(), .run_write(), Run a Cypher statement and return recor…]
- "hooks_usemousegradient": "useMouseGradient.ts" | kind=code-symbol | source=manager/frontend/hooks/useMouseGradient.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, useMouseGradient(), page.tsx, 298a9d4 trim frontend to 7 core pages; …]
- "lib_adapters_toapiengagementcreate": "toApiEngagementCreate()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L61 | neighbors=[route.ts, adapters.ts, normalizeList(), engagement-adapters.test.ts]
- "lib_adapters_touiengagement": "toUiEngagement()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L31 | neighbors=[route.ts, route.ts, adapters.ts, engStatusToUi()]
- "lib_agents_store_registeragent": "registerAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L362 | neighbors=[agents-store.ts, genFieldAgentId(), readFieldAgents(), writeFieldAgents()]
- "lib_agents_store_writefieldagents": "writeFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L350 | neighbors=[agents-store.ts, registerAgent(), updateAgentLastSeen(), ensureDataDir()]
- "lib_ai_engine_getclient": "getClient()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L422 | neighbors=[ai-engine.ts, chat(), generateReport(), triageFindings()]
- "lib_backend_cookiefrom": "cookieFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L76 | neighbors=[backend.ts, bearerFrom(), route.ts, backend-auth.test.ts]
- "lib_clients_store_createclient": "createClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L87 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_clients_store_updateclient": "updateClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L105 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_errors_diagnosespawnerror": "diagnoseSpawnError()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L244 | neighbors=[tool-runners.ts, errors.ts, VedhaError, AdversaError]
- "lib_httpx_parser_httpxjsonldecoder_decode": ".decode()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L116 | neighbors=[HttpxJsonlDecoder, .push(), parseHttpxJsonLine(), .finish()]
- "lib_job_store_createjob": "createJob()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L41 | neighbors=[job-store.ts, genJobId(), readJobs(), writeJobs()]
- "lib_nuclei_parser_nucleiseveritytoseverity": "nucleiSeverityToSeverity()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L71 | neighbors=[tool-runners.ts, nuclei-parser.ts, nucleiMatchToFinding(), parsers.test.ts]
- "lib_permissions_store_adduser": "addUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L60 | neighbors=[permissions-store.ts, read(), write(), route.ts]
- "lib_permissions_store_isemailallowed": "isEmailAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L48 | neighbors=[auth-middleware.ts, permissions-store.ts, read(), route.ts]
- "lib_severity_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L29 | neighbors=[FactCard.tsx, page.tsx, severity.ts, page.tsx]
- "lib_severity_toseverity": "toSeverity()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L117 | neighbors=[PatchComparisonMatrix.tsx, SlaStatus.tsx, severity.ts, sev()]
- "lib_target_parser_parsetargets": "parseTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L72 | neighbors=[scanner.ts, target-parser.ts, estimateHostCount(), isValidTarget()]
- "logout_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/logout/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, POST(), 2885afa Add comprehensive probe testing…]
- "main_scripts_delta_scanner_delta": "Delta" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L69 | neighbors=[delta_scanner.py, .to_dict(), .diff(), One security-relevant change between tw…]
- "main_scripts_device_classifier_classify_from_results": "classify_from_results()" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L201 | neighbors=[device_classifier.py, classify_device(), Convenience adapter: extract classifier…, Convenience adapter: extract classifier…]
- "main_scripts_findings_as_dict": "_as_dict()" | kind=code-symbol | source=probe/main_scripts/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "main_scripts_findings_by_target": "_by_target()" | kind=code-symbol | source=probe/main_scripts/findings.py:L552 | neighbors=[findings.py, _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_ntlm_relay()]
- "main_scripts_findings_load_facts_jsonl": "load_facts_jsonl()" | kind=code-symbol | source=probe/main_scripts/findings.py:L668 | neighbors=[findings.py, _main(), Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…]
- "main_scripts_findings_rule_smb": "_rule_smb()" | kind=code-symbol | source=probe/main_scripts/findings.py:L230 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_snmp": "_rule_snmp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L253 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_tls": "_rule_tls()" | kind=code-symbol | source=probe/main_scripts/findings.py:L175 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_udp_amplification": "_rule_udp_amplification()" | kind=code-symbol | source=probe/main_scripts/findings.py:L284 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_web": "_rule_web()" | kind=code-symbol | source=probe/main_scripts/findings.py:L395 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L142 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …]
- "main_scripts_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L125 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…]
- "main_scripts_iot_scanner_iotscanner": "IoTScanner" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L443 | neighbors=[iot_scanner.py, BaseScanner, .scan_target(), Surveys a target for IoT/embedded devic…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-043.json

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
