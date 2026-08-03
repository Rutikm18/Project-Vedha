# Node Description Batch 23 of 131

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

- "lib_cases_store_readcases": "readCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L213 | neighbors=[cases-store.ts, addComment(), createCase(), getCaseById(), ensureDataDir(), updateCase()]
- "lib_clients_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L66 | neighbors=[clients-store.ts, createClient(), read(), updateClient(), updateClientSettings(), ensureDir()]
- "lib_errors_adversaerror": "AdversaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, .constructor(), .render(), .toJSON(), diagnoseSpawnError()]
- "lib_errors_vedhaerror": "VedhaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, diagnoseSpawnError(), .constructor(), .render(), .toJSON()]
- "lib_findings_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L22 | neighbors=[findings-store.ts, deleteFinding(), getAllFindings(), saveFindings(), updateFinding(), updateFindingStatus()]
- "lib_graph_store_graphstore": "graphStore" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L329 | neighbors=[route.ts, route.ts, route.ts, route.ts, graph-store.ts, route.ts]
- "lib_httpx_parser_parsehttpxjsonline": "parseHttpxJsonLine()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L41 | neighbors=[httpx-parser.ts, .decode(), isOptionalNumber(), isOptionalString(), normalizePort(), parsers.test.ts]
- "lib_netexec_parser": "netexec-parser.ts" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), scanner-adapters.test.ts]
- "lib_scan_events": "scan-events.ts" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, broadcastToScan(), Callback, scanListeners, subscribeScan(), 298a9d4 trim frontend to 7 core pages; …]
- "lib_scanner_request_validation_validateopenvasscanrequest": "validateOpenVASScanRequest()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L112 | neighbors=[scanner-request-validation.ts, isRecord(), validateHost(), validateSafeString(), validateScannerTargets(), scanner-adapters.test.ts]
- "lib_security_context_resolvesecurityreference": "resolveSecurityReference()" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L37 | neighbors=[route.ts, route.ts, route.ts, security-context.ts, publicCveRecord(), SecurityContextError]
- "lib_testssl_parser_parsetestssljson": "parseTestsslJson()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L44 | neighbors=[testssl-parser.ts, parseTestsslJsonChecked(), parseTestsslOutput(), parsers.test.ts, tool-runners.ts, mapSeverity()]
- "lib_whatweb_parser": "whatweb-parser.ts" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, parseWhatWebOutput(), WhatWebParseResult, WhatWebResult, scanner-adapters.test.ts]
- "models_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/models/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, Finding, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "models_scan_job": "scan_job.py" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanJob, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, recent_activity(), Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L114 | neighbors=[agent_ws.py, _agent_token_from_websocket(), _claim_pushed_job(), Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…]
- "routers_agents_enqueue_agent_job": "enqueue_agent_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L902 | neighbors=[agents.py, _agent_can_execute_job(), _encrypt_scope_for_agent(), _job_params_contain_secret(), _job_reachability_scope(), _resolve_scan_type()]
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L137 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…]
- "routers_agents_required_scan_type": "_required_scan_type()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L91 | neighbors=[agents.py, _agent_can_execute_job(), Resolve the capability a probe must adv…, _resolve_scan_type(), Resolve the capability a probe must adv…, Resolve the capability a probe must adv…]
- "routers_agents_scope_is_reachable": "_scope_is_reachable()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L101 | neighbors=[agents.py, _agent_can_execute_job(), Return whether a probe's declared netwo…, refresh_agent_registration(), Return whether a probe's declared netwo…, Return whether a probe's declared netwo…]
- "routers_analytics_rationale_1": "Dashboard exposure analytics endpoint.  Serves protocol-risk + zone-health aggre" | kind=entity | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[analytics.py, Asset, Engagement, FindingStatus, Finding, Service]
- "routers_probe_enrollment_secret_hash": "_secret_hash()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L36 | neighbors=[probe_enrollment.py, activate_enrollment(), _authenticated_request(), create_enrollment_request(), generate_enroll_token(), refresh_device_token()]
- "scanner_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/scanner/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "scanner_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/scanner/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "scanner_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed(), Run masscan over the given target specs…, _parse_masscan_json()]
- "scanner_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, OSError, .__init__(), _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "scanner_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/scanner/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…, Listen-only discovery. No active probin…]
- "scanner_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/scanner/scanner_base.py:L358 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…]
- "scanner_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L328 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()]
- "scanner_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L112 | neighbors=[udp_scanner.py, BaseScanner, .__init__(), ._probe(), .scan_target(), ._send_recv()]
- "scanner_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L119 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_memcached_stats(), interpret_ntp_monlist(), _ntp_monlist_probe(), .scan_target()]
- "scanner_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "schemas_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, AiGenerateRequest, AiGenerateResponse, AiMessage, AiProviderStatus, AiStatusResponse]
- "schemas_ai_aigeneraterequest": "AiGenerateRequest" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L18 | neighbors=[ai.py, BaseModel, .validate_bounded_input(), AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_finding_findingpatch": "FindingPatch" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L20 | neighbors=[finding.py, BaseModel, All fields optional — PATCH semantics., DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_seed_with_retry": "_seed_with_retry()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L294 | neighbors=[seed_admin.py, main(), Exponential-backoff retry for transient…, log_error(), log_warn(), _seed_once()]
- "services_job_result_service_promote_assets": "_promote_assets()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L322 | neighbors=[job_result_service.py, process_job_result(), Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…, Upsert discovered hosts/services into t…]
- "services_scope_crypto": "scope_crypto.py" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt…, 2885afa Add comprehensive probe testing…]
- "tests_engagement_adapters_test": "engagement-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/engagement-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, adapters.ts, toApiEngagementCreate(), toApiEngagementPatch(), toApiFindingPatch(), toUiFinding()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-022.json

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
