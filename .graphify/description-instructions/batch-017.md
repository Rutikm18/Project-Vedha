# Node Description Batch 18 of 104

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

- "routers_engagements_import_facts": "import_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L293 | neighbors=[engagements.py, _parse_probe_file(), _promote_from_facts(), _read_capped(), _refresh_overview_cache(), Offline ingest path: upload a probe's s…]
- "scanid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/stream/[scanId]/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, scan-events.ts, subscribeScan(), scan-pipeline.ts, getPipeline(), GET()]
- "scanner_db_dial": "dial()" | kind=code-symbol | source=probe-go/scanner/db.go:L59 | neighbors=[db.go, probeMongo(), probeMSSQL(), probeMysql(), probePostgres(), probeRedis()]
- "scanner_db_probedb": "ProbeDB()" | kind=code-symbol | source=probe-go/scanner/db.go:L22 | neighbors=[db.go, probeMongo(), probeMSSQL(), probeMysql(), probePostgres(), probeRedis()]
- "scanner_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/scanner/db_scanner.py:L227 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "scanner_fingerprint_fingerprint": "Fingerprint()" | kind=code-symbol | source=probe-go/scanner/fingerprint.go:L135 | neighbors=[fingerprint.go, expandBackrefs(), firstLine(), matchSignature(), sanitize(), sendProbe()]
- "scanner_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/scanner/mass_scan.py:L139 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "scanner_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/scanner/scanner_base.py:L358 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…]
- "scanner_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L328 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()]
- "scanner_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…, workflow_engine.py]
- "scanner_types": "types.go" | kind=code-symbol | source=probe-go/scanner/types.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, HostResult, PortResult, Result, newResult(), ptr()]
- "scanner_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L80 | neighbors=[udp_scanner.py, BaseScanner, .__init__(), ._probe(), .scan_target(), ._send_recv()]
- "scanner_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "schemas_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, EngagementCreate, EngagementDetail, EngagementFilter, EngagementOut, FindingSummary]
- "schemas_finding_findingpatch": "FindingPatch" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L20 | neighbors=[finding.py, BaseModel, DetectionStatus, FindingSeverity, FindingStatus, All fields optional — PATCH semantics.]
- "siem_config_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, detection-store.ts, detectionStore, SIEMConfig, GET(), POST()]
- "states_datastate_emptystate": "EmptyState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L36 | neighbors=[page.tsx, Exposure.tsx, SlaStatus.tsx, page.tsx, page.tsx, DataState.tsx]
- "taskid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/openvas/[taskId]/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, findings-store.ts, createFinding(), openvas-client.ts, getTask(), GET()]
- "tests_test_agents_testotprofilegate": "TestOTProfileGate" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L87 | neighbors=[test_agents.py, ScanJobType, .test_allows_passive_discovery_on_ot_en…, .test_blocks_active_scan_type_on_ot_eng…, .test_blocks_explicit_active_scan_type_…, .test_it_and_iot_profiles_unaffected()]
- "tests_test_ai_engine_asset": "_asset()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L36 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher(), .test_predict_priority_uses_fallback_wh…]
- "tests_test_ai_engine_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L170 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_ai_engine_rationale_1": "Unit tests for the AI engine (Prompt 8).  The Anthropic client is mocked (no API" | kind=entity | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus, test_ai_engine.py]
- "tests_test_db_scanner_testmysqlxvsoracle": "TestMysqlxVsOracle" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L53 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle(), .test_oracle_rejects_garbage_with_type_…, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_engagement_lists": "test_engagement_lists.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user(), Unit tests for the dashboard list endpo…]
- "tests_test_exploit_engine_testmetasploitrpcclient_make_client": "._make_client()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L183 | neighbors=[TestMetasploitRPCClient, .test_get_job_status_running(), .test_kill_job(), .test_list_modules_exploit(), .test_run_module_error_raises(), .test_run_module_returns_job_id()]
- "tests_test_integration_testscopevalidationpipeline": "TestScopeValidationPipeline" | kind=code-symbol | source=probe/tests/test_integration.py:L165 | neighbors=[test_integration.py, Phase 1: combined scope validation (val…, .test_accepts_in_scope_rejects_out_of_s…, .test_all_excluded_returns_empty(), .test_excludes_override_scope(), .test_merge_exclusions_deduplicates()]
- "tests_test_integration_testwebsocketmessageprotocol": "TestWebSocketMessageProtocol" | kind=code-symbol | source=probe/tests/test_integration.py:L273 | neighbors=[test_integration.py, Phase 2: WebSocket message parsing., .test_heartbeat_message(), .test_hello_message(), .test_job_push_message(), .test_result_message()]
- "tests_test_nessus_scanner_mock_response": "_mock_response()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L25 | neighbors=[test_nessus_scanner.py, test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()]
- "tests_test_probe_core_testclamp": "TestClamp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L716 | neighbors=[test_probe_core.py, .test_bad_value_uses_default(), .test_clamped_high(), .test_clamped_low(), .test_in_range(), .test_none_uses_default()]
- "tests_test_probe_core_testengagementmodes": "TestEngagementModes" | kind=code-symbol | source=probe/tests/test_probe_core.py:L418 | neighbors=[test_probe_core.py, .test_assessment(), .test_re_scan(), .test_service_specific_invalid_raises(), .test_service_specific_valid(), .test_triage()]
- "tests_test_scope_validator_testfetchengagementscope": "TestFetchEngagementScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L132 | neighbors=[test_scope_validator.py, .test_http_get_raises(), .test_http_get_returns_incomplete(), .test_http_get_returns_none(), .test_returns_excludes(), .test_returns_scope_from_http_get()]
- "tools_installer_managedpath": "managedPath()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L48 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), isManaged(), removeTool()]
- "tools_issue_license": "issue_license.py" | kind=code-symbol | source=probe/tools/issue_license.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, _b64(), issue(), keygen(), main()]
- "use_cases_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/use-cases/route.ts:L1 | neighbors=[0557559 scanner: real use-case library,…, backend.ts, backend(), with-backend.ts, withBackend(), GET]
- "vuln_tasks": "tasks.py" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, database.py, _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment(), Background tasks triggered after a vuln…]
- "websocket_manager": "manager.py" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, AgentConnectionManager, ConnectionManager, GraphWebSocketManager, WebSocket manager for real-time graph u…]
- "websocket_manager_graphwebsocketmanager_handle_client": ".handle_client()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L236 | neighbors=[GraphWebSocketManager, .connect(), .disconnect(), .send_personal(), ._handle_message(), Handle a new WebSocket client connectio…]
- "workers_outbox_event": "Event" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L42 | neighbors=[outbox.py, _claim_batch(), OutboxEvent, ScanResult, main(), run_worker()]
- "workers_reaper": "reaper.py" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, config.py, database.py, reap_once(), run_reaper(), reaper.py — requeue jobs abandoned by a…]
- "workflow_router": "router.py" | kind=code-symbol | source=probe/workflow/router.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, test_probe_core.py, looks_like_http(), looks_like_tls(), route_branches(), router.py — dynamic Gate-5 branch routi…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-017.json

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
