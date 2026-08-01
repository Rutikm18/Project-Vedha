# Node Description Batch 22 of 119

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

- "websocket_manager_agentconnectionmanager_push_job_to_first_online": ".push_job_to_first_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L203 | neighbors=[AgentConnectionManager, .online_agents_for_tenant(), .push_job(), Push a job to the first online agent in…, .unregister(), Push a job to the first online connecte…]
- "websocket_manager_graphwebsocketmanager_handle_message": "._handle_message()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L317 | neighbors=[GraphWebSocketManager, .handle_client(), .broadcast(), .send_personal(), Handle incoming WebSocket messages., Handle incoming WebSocket messages.]
- "workers_outbox_event": "Event" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L42 | neighbors=[outbox.py, _claim_batch(), OutboxEvent, ScanResult, main(), run_worker()]
- "workflow_report": "report.py" | kind=code-symbol | source=probe/workflow/report.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…, 298a9d4 trim frontend to 7 core pages; …]
- "workflow_router_route_branches": "route_branches()" | kind=code-symbol | source=probe/workflow/router.py:L71 | neighbors=[router.py, For every open port with a banner fact,…, looks_like_db(), looks_like_http(), looks_like_tls(), For every open port with a banner fact,…]
- "ad_adcs": "adcs.py" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L1 | neighbors=[ADCSChecker, CertTemplate, ADCSChecker — Active Directory Certific…, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "ad_ldap_enum_ldapenumerator_attr": "._attr()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L205 | neighbors=[LDAPEnumerator, .get_aces(), .get_computers(), .get_groups(), .get_users()]
- "ad_ldap_enum_ldapenumerator_get_aces": ".get_aces()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L311 | neighbors=[LDAPEnumerator, ._attr(), ._parse_security_descriptor(), ._require_conn(), Parse the nTSecurityDescriptor of an ob…]
- "ad_ldap_enum_ldapenumerator_get_groups": ".get_groups()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L267 | neighbors=[LDAPEnumerator, ADGroup, _as_list(), ._attr(), ._search()]
- "ad_ldap_enum_ldapenumerator_search": "._search()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L194 | neighbors=[LDAPEnumerator, .get_computers(), .get_groups(), .get_users(), ._require_conn()]
- "agent_agent_flush_spool_over_http": "_flush_spool_over_http()" | kind=code-symbol | source=probe/agent/agent.py:L600 | neighbors=[agent.py, say(), Retry durable result files using the ac…, _run_ws_push_loop(), _ws_http_poll_fallback()]
- "agent_agent_rejectjob": ".rejectJob()" | kind=code-symbol | source=probe-go/agent/agent.go:L566 | neighbors=[agent.py, mapToJob(), resultToMap(), str(), .runPollLoop()]
- "agent_agent_ws_heartbeat_sender": "_ws_heartbeat_sender()" | kind=code-symbol | source=probe/agent/agent.py:L580 | neighbors=[agent.py, Send periodic heartbeats over WebSocket., _run_ws_push_loop(), Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket.]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=probe/agent/cli.py:L274 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=probe/agent/cli.py:L59 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=probe/agent/cli.py:L33 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=probe/agent/cli.py:L46 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]
- "agent_cli_poll_job": "_poll_job()" | kind=code-symbol | source=probe/agent/cli.py:L478 | neighbors=[cli.py, cmd_scan_run(), cmd_validate(), CliError, .request()]
- "agent_cli_split_values": "split_values()" | kind=code-symbol | source=probe/agent/cli.py:L153 | neighbors=[cli.py, cmd_daemon_run(), cmd_engagements_create(), cmd_scan_run(), cmd_validate()]
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L157 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…]
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L235 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count concrete open services, not gener…, run_scan()]
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=probe/agent/engine.py:L67 | neighbors=[engine.py, _runtime_manifest(), Single factory for error result dicts —…, run_scan(), Single factory for error result dicts —…]
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L177 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Translate operator-supplied job params …]
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "agent_job_mapping_test_managerjob": "managerJob()" | kind=code-symbol | source=probe-go/agent/job_mapping_test.go:L166 | neighbors=[job_mapping_test.go, TestMapToJobFailsClosedOnUnverifiableSc…, TestMapToJobMergesAuthoritativeExclusio…, TestMapToJobResolvesCanonicalUseCases(), TestMapToJobUsesParamsScanTypeAndPreser…]
- "agent_license_licenseerror": "LicenseError" | kind=code-symbol | source=probe/agent/license.py:L32 | neighbors=[license.py, check_license(), .__init__(), Exception, verify_license()]
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=probe/agent/result_spool.py:L90 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists(), ._path(), Load a previously spooled result, retur…]
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L108 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .remove(), .save(), Attempt to upload a result with retries…]
- "agent_state_test_identitytestconfig": "identityTestConfig()" | kind=code-symbol | source=probe-go/agent/state_test.go:L66 | neighbors=[state_test.go, TestConfiguredIdentityRejectsPartialCre…, TestConfiguredIdentityTakesPrecedenceOv…, TestObtainIdentityPersistsAndReusesRegi…, TestObtainIdentityRecoversFromCorruptSt…]
- "agent_task_runner_taskrunner": "TaskRunner" | kind=code-symbol | source=probe/agent/task_runner.py:L41 | neighbors=[task_runner.py, Orchestrates one scan job's lifecycle. …, .__init__(), .run_job(), ._submit_or_spool()]
- "agent_task_runner_taskrunner_run_job": ".run_job()" | kind=code-symbol | source=probe/agent/task_runner.py:L88 | neighbors=[Execute a complete scan job lifecycle. …, TaskRunner, JobResult, ._submit_or_spool(), Execute a complete scan job lifecycle. …]
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L215 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError, Register the probe with the manager.   …]
- "ai_hallucination_hallucinationguard_validate": ".validate()" | kind=code-symbol | source=manager/backend/app/ai/hallucination.py:L101 | neighbors=[HallucinationGuard, .validate_cve_claims(), .validate_cvss_scores(), .validate_remediation_commands(), Run all relevant checks and return a co…]
- "ai_prioritizer_extract_features": "extract_features()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L72 | neighbors=[prioritizer.py, _to_float(), Build the model's feature vector from a…, .explain_prediction(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_fallback_score": ".fallback_score()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L204 | neighbors=[Weighted composite 0–1000 (same shape a…, VulnPrioritizer, .explain_prediction(), ._formula_contributions(), .predict_priority()]
- "ai_prioritizer_vulnprioritizer_predict_priority": ".predict_priority()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L148 | neighbors=[Return a 0–1000 priority score. Uses th…, VulnPrioritizer, .explain_prediction(), extract_features(), .fallback_score()]
- "app_config_settings": "Settings" | kind=code-symbol | source=manager/backend/app/config.py:L7 | neighbors=[config.py, get_settings(), .cors_origins(), .is_production(), BaseSettings]
- "assetid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/blast-radius/[assetId]/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "attack_graph_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-graph/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]
- "attack_paths_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/route.ts:L1 | neighbors=[GET(), graphStore, d1b4dd3 trim frontend to 7 core pages; …, graph-store.ts, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-021.json

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
