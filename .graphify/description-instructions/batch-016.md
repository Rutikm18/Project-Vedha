# Node Description Batch 17 of 186

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

- "routers_agents_agentrefreshrequest": "AgentRefreshRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L270 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType] | lang=en
- "runtimeerror": "RuntimeError" | kind=code-symbol | neighbors=[LeaseLostError, HWBindError, AgentUnavailableError, LLMUnavailableError, StartupAbortError, PassiveListenerError] | lang=en
- "scanner_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=probe/scanner/port_scanner.py:L153 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, .classified(), .complete(), .degraded()] | lang=en
- "scanner_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/scanner/scanner_base.py:L645 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…] | lang=en
- "scanner_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L615 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()] | lang=en
- "scanner_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=probe/scanner/scanner_base.py:L484 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()] | lang=en
- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate, PersonalAccessTokenCreated] | lang=en
- "services_llm": "llm.py" | kind=code-symbol | source=manager/backend/app/services/llm.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, cac022c Everything is done and verified…, config.py] | lang=en
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, backend(), withBackend(), ApiSlaItem, ApiSlaSummary, GET] | lang=en
- "states_datastate_emptystate": "EmptyState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L36 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, page.tsx] | lang=en
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard] | lang=en
- "tests_test_ai_normalizer_testproposecandidates": "TestProposeCandidates" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L153 | neighbors=[test_ai_normalizer.py, .test_ai_assisted_flag_set_on_candidate…, .test_cache_hit_bypasses_client(), .test_client_failure_returns_empty(), .test_malformed_response_missing_produc…, .test_malformed_response_not_a_list_ret…] | lang=en
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, .test_run_without_connection_returns_em…, .test_run_write_noop_without_connection…, .test_sync_to_neo4j_noop_without_client…, PathAnalyzer, GraphBuilder] | lang=en
- "tests_test_auth_login_teststartupdiagnostics": "TestStartupDiagnostics" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L251 | neighbors=[test_auth_login.py, .test_bcrypt_round_trip_passes(), .test_cookie_config_fatal_in_production…, .test_cookie_config_ok_in_development(), .test_database_check_returns_fatal_on_c…, .test_jwt_secret_known_weak_is_fatal()] | lang=en
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _action(), pytest_addoption(), TestDetectionCorrelator, TestEDRParsing, TestSIEMParsing] | lang=en
- "tests_test_exploit_engine_rationale_1": "Unit tests for the exploitation engine.  All external connections (Metasploit RP" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "tests_test_exploit_engine_rationale_420": "Run against a live Metasploitable2 lab target.     Requires: msfrpcd running, Me" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L420 | neighbors=[TestMetasploitIntegration, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=pt
- "tests_test_exploit_engine_rationale_465": "Register --msf-host CLI option for integration tests." | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L465 | neighbors=[pytest_addoption(), MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "tests_test_http_lease": "test_http_lease.py" | kind=code-symbol | source=probe/tests/test_http_lease.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, engine.py, transport.py, test_engine_cancellation_stops_async_sc…] | lang=en
- "tests_test_main_scripts_correlation_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L13 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts(), test_correlations_are_evidence_backed(), test_legacy_windows_surface_smbv1_plus_…, test_no_legacy_surface_with_only_smbv1()] | lang=en
- "tests_test_main_scripts_coverage": "test_main_scripts_coverage.py" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, port_scanner.py, scanner_base.py, _closed(), _mk_scanner(), _scope()] | lang=en
- "tests_test_main_scripts_device_testclassifydevice": "TestClassifyDevice" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L17 | neighbors=[test_main_scripts_device.py, .test_domain_controller(), .test_iot_camera(), .test_network_device_router(), .test_printer(), .test_service_product_reinforces_server…] | lang=en
- "tests_test_main_scripts_errno": "test_main_scripts_errno.py" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _oserr(), test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_dns_failure_is_error_not_filtered(), test_errno_none_falls_back_to_os_error()] | lang=en
- "tests_test_new_scanners_make_scan_record": "_make_scan_record()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L312 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…] | lang=en
- "tests_test_new_scanners_testiotscanner": "TestIoTScanner" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L246 | neighbors=[test_new_scanners.py, .test_coap_get_wellknown_header(), .test_coap_get_wellknown_path(), .test_coap_response_parse_205(), .test_coap_response_parse_404(), .test_coap_response_parse_short()] | lang=en
- "tests_test_outbox_reclaim_now": "_now()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L25 | neighbors=[test_outbox_reclaim.py, test_boundary_at_exactly_the_lease_is_r…, test_dead_letter_and_requeue_are_mutual…, test_dead_letter_stmt_targets_exhausted…, test_expired_processing_lock_is_reclaim…, test_fresh_processing_lock_is_not_recla…] | lang=en
- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=probe/tests/test_probe_core.py:L189 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()] | lang=en
- "tests_test_syn_scanner": "test_syn_scanner.py" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, TestCapabilityDetection, TestChecksum, TestClassify, TestPacketRoundTrip] | lang=en
- "tests_test_transport_testsubmitresult": "TestSubmitResult" | kind=code-symbol | source=probe/tests/test_transport.py:L402 | neighbors=[test_transport.py, .test_2xx_variants_return_true(), .test_large_payload_is_gzipped(), .test_network_error_returns_false(), .test_permanent_client_errors_are_marke…, .test_retryable_client_errors_return_fa…] | lang=en
- "tests_test_validation_endpoints": "test_validation_endpoints.py" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _mock_db(), test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids()] | lang=en
- "tests_test_vuln_enrichment_make_http_mock": "_make_http_mock()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L52 | neighbors=[test_vuln_enrichment.py, Create a mock httpx.AsyncClient that re…, test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full()] | lang=en
- "tests_test_ws_claim_protocol": "test_ws_claim_protocol.py" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, result_spool.py, test_busy_probe_declines_additional_off…, test_http_spool_flush_removes_only_mana…] | lang=en
- "verify_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/verify/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, verifyOtp(), addUser(), getUser(), POST()] | lang=en
- "vuln_enrichment_ttlcache": "TTLCache" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L27 | neighbors=[enrichment.py, LRU + TTL eviction. Expired keys are pu…, OrderedDict, .__contains__(), .get(), .__getitem__()] | lang=en
- "websocket_manager": "manager.py" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, AgentConnectionManager, ConnectionManager] | lang=en
- "websocket_manager_graphwebsocketmanager": "GraphWebSocketManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L292 | neighbors=[manager.py, .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), .handle_client(), ._handle_message()] | lang=en
- "workflow_router": "router.py" | kind=code-symbol | source=probe/workflow/router.py:L1 | neighbors=[bb0ef3d feat(probe): route DB services …, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_router_db.py, looks_like_db(), looks_like_http()] | lang=en
- "activity_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L1 | neighbors=[ApiActivity, GET, backend.ts, backend(), with-backend.ts, withBackend()] | lang=en
- "agent_agent_check_anti_debug": "_check_anti_debug()" | kind=code-symbol | source=probe/agent/agent.py:L782 | neighbors=[agent.py, say(), Detect common debugging/tracing tools. …, _startup_gauntlet(), Detect common debugging/tracing tools. …, Detect common debugging/tracing tools. …] | lang=en
- "agent_agent_load_or_create_identity": "_load_or_create_identity()" | kind=code-symbol | source=probe/agent/agent.py:L830 | neighbors=[agent.py, say(), _obtain_identity(), Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…, Load the probe's X25519 identity from p…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-016.json

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
