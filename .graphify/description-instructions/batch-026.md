# Node Description Batch 27 of 336

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

- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=probe/tests/test_probe_core.py:L189 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()]
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L948 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_network_va_resolves()]
- "tests_test_remediation_kb_f": "_f()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L11 | neighbors=[test_remediation_kb.py, .test_cve_without_keyword_is_patch(), .test_keyword_categories(), .test_order_specificity_anon_ftp_beats_…, .test_unmatched_is_generic(), .test_missing_os_defaults_to_generic()]
- "tests_test_remediation_routes_fakedb": "_FakeDB" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L65 | neighbors=[test_remediation_routes.py, .execute(), .flush(), .__init__(), execute() returns the next queued resul…, .test_ai_available_caches_ai_plan()]
- "tests_test_result_archive": "test_result_archive.py" | kind=code-symbol | source=probe/tests/test_result_archive.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, task_runner.py, _job(), _ok_result(), _reset_archive_latch(), _runner()]
- "tests_test_rsync_scanner": "test_rsync_scanner.py" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, scanner_base.py, _FakeSock, TestHandshake, TestParity]
- "tests_test_run_all_reconcile": "test_run_all_reconcile.py" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, run_all.py, scan_funnel.py, test_advertised_dynamic_ports_extractio…, test_open_tcp_ports_ignores_non_open_an…, test_reconcile_folds_in_only_reachable_…]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks": "TestTheScopeGateStillWorks" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L72 | neighbors=[test_run_scoped_fact_scope.py, The exemption must be narrow. These are…, .test_an_unknown_scanner_gets_no_exempt…, .test_excluded_cidr_still_wins(), .test_hostname_target_is_still_refused(), .test_out_of_scope_finding_is_still_rej…]
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
- "activity_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L1 | neighbors=[ApiActivity, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "agent_agent_wait_for_manager": "_wait_for_manager()" | kind=code-symbol | source=probe/agent/agent.py:L247 | neighbors=[agent.py, main(), Bounded reachability preflight. Proceed…, _dbg(), _manager_reachable(), say()]
- "agent_cli_cmd_auth_login": "cmd_auth_login()" | kind=code-symbol | source=probe/agent/cli.py:L239 | neighbors=[cli.py, CliError, ConfigStore, .set_profile(), _env(), ManagerClient]
- "agent_engine_applied_tuning": "_applied_tuning()" | kind=code-symbol | source=probe/agent/engine.py:L387 | neighbors=[engine.py, _scan_method_for(), _build_run_stats(), Serialize effective limits without ever…, Serialize effective limits without ever…, Serialize effective limits without ever…]
- "agent_engine_job_runtime_seconds": "_job_runtime_seconds()" | kind=code-symbol | source=probe/agent/engine.py:L230 | neighbors=[engine.py, _clamp(), Return the effective whole-job deadline…, run_scan(), Return the effective whole-job deadline…, Return the effective whole-job deadline…]
- "agent_engine_leaselosterror": "LeaseLostError" | kind=code-symbol | source=probe/agent/engine.py:L550 | neighbors=[engine.py, RuntimeError, Raised when Manager fencing revokes the…, _run_with_cancellation(), Raised when Manager fencing revokes the…, Raised when Manager fencing revokes the…]
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=probe/agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_integration.py]
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L547 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job(), ._archive_result(), Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…]
- "agent_transport_transport_bootstrap": ".bootstrap()" | kind=code-symbol | source=probe/agent/transport.py:L409 | neighbors=[Register using a manager-side shared bo…, Transport, .save_state(), TransportError, Register using a manager-side shared bo…, Register using a manager-side shared bo…]
- "agent_transport_transport_is_authenticated": ".is_authenticated()" | kind=code-symbol | source=probe/agent/transport.py:L268 | neighbors=[True if we have both an agent_id and a …, Transport, True if we have both an agent_id and a …, True if we have both an agent_id and a …, True if we have both an agent_id and a …, True if we have both an agent_id and a …]
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L293 | neighbors=[use_cases.py, Return (scan_type, profile, intensity) …, normalize_intensity(), use_case_for_code(), Return (scan_type, profile, intensity) …, Return (scan_type, profile, intensity) …]
- "auth_portal_scope": "portal_scope.py" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L1 | neighbors=[dependencies.py, assert_client(), client_scoped(), require_client(), resolve_scope(), scoped_engagement()]
- "commands_logout": "logout.ts" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L1 | neighbors=[clearSession(), loadSession(), buildLogoutCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_status": "status.ts" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildStatusCommand(), ScanRow, STATUS_COLOR, d1b4dd3 trim frontend to 7 core pages; …]
- "commands_whoami": "whoami.ts" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildWhoamiCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@21ebc4647fbc8013300844481aacf06393192c11": "21ebc46 feat(detection): unified prioritization engine (risk_score for every fi…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, 0236a60 fix(detection): full EPSS catal…, prioritization.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@22e4f8d2c085fe3c93a07a9eec8b728ac9e197f3": "22e4f8d chore: update version" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@3565ada02b223c451ee7c0a953852dcddf688973": "3565ada fix(ingest): NUL-safe result submission + network-service hygiene findi…" | kind=Commit | source=git | neighbors=[transport.py, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, f3bb8db feat(manager): cross-worker WS …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-026.json

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
