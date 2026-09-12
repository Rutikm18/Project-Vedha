# Node Description Batch 30 of 380

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

- "tests_test_outbox_reclaim_now": "_now()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L25 | neighbors=[test_outbox_reclaim.py, test_boundary_at_exactly_the_lease_is_r…, test_dead_letter_and_requeue_are_mutual…, test_dead_letter_stmt_targets_exhausted…, test_expired_processing_lock_is_reclaim…, test_fresh_processing_lock_is_not_recla…]
- "tests_test_portal_assistant_ask": "_ask()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L76 | neighbors=[test_portal_assistant.py, test_a_non_client_user_is_refused(), test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_model_failure_surfaces_its_status_…]
- "tests_test_portal_assistant_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L60 | neighbors=[test_portal_assistant.py, execute() → engagement, then findings, …, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_model_failure_surfaces_its_status_…]
- "tests_test_portal_finding_actions_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L34 | neighbors=[test_portal_finding_actions.py, test_customer_cannot_mutate_a_finding_o…, test_customer_transition_mutates_shared…, test_portal_assets_use_session_engageme…, test_portal_engagement_update_pins_sess…, test_portal_enrollment_binds_device_to_…]
- "tests_test_portal_read_testcreatescanrequest": "TestCreateScanRequest" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L242 | neighbors=[test_portal_read.py, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_operator_cannot_create(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict()]
- "tests_test_posture_trace": "test_posture_trace.py" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _asset(), _fact(), _outcome(), TestAbsentVersusClean, TestBehaviourPreserved]
- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=probe/tests/test_probe_core.py:L189 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()]
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L948 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_network_va_resolves()]
- "tests_test_raw_facts": "test_raw_facts.py" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L1 | neighbors=[25c014d feat: enhance campaign progress…, _db(), _row(), test_raw_facts_bounds_and_no_results(), test_raw_facts_filter_by_scanner(), test_raw_facts_grouped_by_scanner()]
- "tests_test_remediation_kb_f": "_f()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L11 | neighbors=[test_remediation_kb.py, .test_cve_without_keyword_is_patch(), .test_keyword_categories(), .test_order_specificity_anon_ftp_beats_…, .test_unmatched_is_generic(), .test_missing_os_defaults_to_generic()]
- "tests_test_remediation_routes_fakedb": "_FakeDB" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L65 | neighbors=[test_remediation_routes.py, .execute(), .flush(), .__init__(), execute() returns the next queued resul…, .test_ai_available_caches_ai_plan()]
- "tests_test_result_archive": "test_result_archive.py" | kind=code-symbol | source=probe/tests/test_result_archive.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, task_runner.py, _job(), _ok_result(), _reset_archive_latch(), _runner()]
- "tests_test_result_queue_q": "_q()" | kind=code-symbol | source=probe/tests/test_result_queue.py:L16 | neighbors=[test_result_queue.py, Clock, test_ack_removes_the_record(), test_age_prune_drops_stale_records(), test_backpressure_at_high_water(), test_enqueue_is_idempotent_by_job_id()]
- "tests_test_rsync_scanner": "test_rsync_scanner.py" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, scanner_base.py, _FakeSock, TestHandshake, TestParity]
- "tests_test_run_all_reconcile": "test_run_all_reconcile.py" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, run_all.py, scan_funnel.py, test_advertised_dynamic_ports_extractio…, test_open_tcp_ports_ignores_non_open_an…, test_reconcile_folds_in_only_reachable_…]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks": "TestTheScopeGateStillWorks" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L72 | neighbors=[test_run_scoped_fact_scope.py, The exemption must be narrow. These are…, .test_an_unknown_scanner_gets_no_exempt…, .test_excluded_cidr_still_wins(), .test_hostname_target_is_still_refused(), .test_out_of_scope_finding_is_still_rej…]
- "tests_test_scan_schedule_api_body": "_body()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L37 | neighbors=[test_scan_schedule_api.py, .test_creator_is_recorded(), .test_unknown_engagement_is_404(), .test_unknown_use_case_is_refused(), .test_valid_schedule_is_created_and_due…, .test_absurdly_long_interval_is_refused…]
- "tests_test_scanner_congestion_testcollapserecovery": "TestCollapseRecovery" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L525 | neighbors=[test_scanner_congestion.py, A collapsed window must be able to clim…, ._collapsed(), .test_backoff_is_still_meaningful(), .test_floor_scales_with_concurrency(), .test_old_behaviour_was_slow()]
- "tests_test_smb_ntlm_build_challenge": "_challenge()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L16 | neighbors=[test_smb_ntlm_build.py, Synthesize an NTLMSSP CHALLENGE (Type-2…, .test_end_to_end_framing_extracts_build…, .test_ntlm_os_build_shared_function(), .test_legacy_6_1_is_win7(), .test_no_version_field_yields_name_but_…]
- "tests_test_transport_testidentity": "TestIdentity" | kind=code-symbol | source=probe/tests/test_transport.py:L29 | neighbors=[test_transport.py, .test_agent_state_updates_preserve_scop…, .test_auth_header(), .test_clear_manager_binding_drops_pin_k…, .test_failed_atomic_replace_preserves_p…, .test_is_authenticated_false_initially()]
- "tests_test_transport_testsubmitresult": "TestSubmitResult" | kind=code-symbol | source=probe/tests/test_transport.py:L482 | neighbors=[test_transport.py, .test_2xx_variants_return_true(), .test_large_payload_is_gzipped(), .test_network_error_returns_false(), .test_permanent_client_errors_are_marke…, .test_retryable_client_errors_return_fa…]
- "tests_test_validation_endpoints": "test_validation_endpoints.py" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _mock_db(), test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids()]
- "tests_test_vantage_fusion_probe": "_probe()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L15 | neighbors=[test_vantage_fusion.py, Build a one-target probe exposure resul…, test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_…, test_external_vantage_open_makes_port_e…, test_fused_service_exposure_is_keyed_fo…]
- "tests_test_vuln_enrichment_make_http_mock": "_make_http_mock()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L52 | neighbors=[test_vuln_enrichment.py, Create a mock httpx.AsyncClient that re…, test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full()]
- "tests_test_wire_identity": "test_wire_identity.py" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L1 | neighbors=[2c53ae9 evasion(scanner): randomized sc…, 37376de hardening(scanner): OPSEC de-si…, 4733f24 evasion(scanner): --source-port…, TestChooseSourcePort, TestEvasionFlags, TestJitteredDelay]
- "tests_test_ws_claim_protocol": "test_ws_claim_protocol.py" | kind=code-symbol | source=probe/tests/test_ws_claim_protocol.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, agent.py, result_spool.py, test_busy_probe_declines_additional_off…, test_http_spool_flush_removes_only_mana…]
- "verify_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/verify/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, verifyOtp(), addUser(), getUser(), POST()]
- "vuln_enrichment_ttlcache": "TTLCache" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L27 | neighbors=[enrichment.py, LRU + TTL eviction. Expired keys are pu…, OrderedDict, .__contains__(), .get(), .__getitem__()]
- "websocket_manager_connectionmanager": "ConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L27 | neighbors=[manager.py, .broadcast(), .connect(), .disconnect(), .get_room_clients(), .__init__()]
- "websocket_manager_graphwebsocketmanager_handle_client": ".handle_client()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L362 | neighbors=[GraphWebSocketManager, .connect(), .disconnect(), .send_personal(), ._handle_message(), Handle a new WebSocket client connectio…]
- "workers_outbox_reclaim_stale": "_reclaim_stale()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L338 | neighbors=[outbox.py, Requeue events a dead worker left in PR…, _dead_letter_stale_stmt(), _requeue_stale_stmt(), _stale_cutoff(), run_worker()]
- "workflow_host_health": "host_health.py" | kind=code-symbol | source=probe/workflow/host_health.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, test_host_health.py, scanner_base.py, _env_int(), _heartbeat_interval(), _heartbeat_misses()]
- "workflow_intensity": "intensity.py" | kind=code-symbol | source=probe/workflow/intensity.py:L1 | neighbors=[engine.py, 22701ea Add tests for scanner parity an…, 42b7429 feat(probe): deep intensity get…, test_intensity_budget.py, test_probe_next_features.py, port_scanner.py]
- "workflow_workflow_engine_run_branch": "_run_branch()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L310 | neighbors=[workflow_engine.py, Run ONE deep-scan branch for one host: …, _record(), _record_reused(), _scan_one(), _split_cached()]
- "workflow_workflow_engine_scan_one": "_scan_one()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L95 | neighbors=[workflow_engine.py, Run one component without allowing a ta…, _run_branch(), Run one component without allowing a ta…, run_engagement(), _gather_per_host()]
- "activity_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L1 | neighbors=[ApiActivity, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "agent_agent_classify_connection_error": "_classify_connection_error()" | kind=code-symbol | source=probe/agent/agent.py:L145 | neighbors=[agent.py, _enroll_device(), main(), _manager_reachable(), _obtain_identity(), Map a low-level connection exception to…]
- "agent_agent_load_env": "_load_env()" | kind=code-symbol | source=probe/agent/agent.py:L79 | neighbors=[agent.py, main(), Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…]
- "agent_agent_poll_jobs_or_empty": "_poll_jobs_or_empty()" | kind=code-symbol | source=probe/agent/agent.py:L336 | neighbors=[agent.py, main(), Poll for work. Auth failures (Transport…, Poll for work. Auth failures (Transport…, Poll for work. Auth failures (Transport…, Poll for work. Auth failures (Transport…]
- "agent_cli_cmd_auth_login": "cmd_auth_login()" | kind=code-symbol | source=probe/agent/cli.py:L239 | neighbors=[cli.py, CliError, ConfigStore, .set_profile(), _env(), ManagerClient]

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
