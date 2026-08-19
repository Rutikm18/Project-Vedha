# Node Description Batch 23 of 227

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

- "scanner_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L286 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), ._icmp_timestamp(), .__init__(), .scan_target()]
- "scanner_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L324 | neighbors=[PortScanner, _family_of(), ._build(), ._scan_port(), One connect() and its classification. A…, One connect() and its classification. A…]
- "scanner_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L596 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…, Send one UDP datagram and await the fir…]
- "schemas_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, AiGenerateRequest, AiGenerateResponse]
- "scripts_startup_validator_run_all_validators": "run_all_validators()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L396 | neighbors=[startup_validator.py, Run all validators. Use in FastAPI life…, CheckResult, DatabaseConnectivityValidator, RedisConnectivityValidator, ValidationReport]
- "services_agent_policy": "agent_policy.py" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L1 | neighbors=[bc08715 feat(agent): risk-tier action c…, ecbb4ad feat(agent): rules-of-engagemen…, classify_action(), Decision, _deny(), evaluate_action()]
- "services_llm_managerllmservice_dispatch": "._dispatch()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L251 | neighbors=[ManagerLlmService, AiRuntimeError, ._anthropic(), ._ollama(), ._openai(), ._openrouter()]
- "services_remediation_kb": "remediation_kb.py" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, classify_finding(), _cves(), os_key(), recipe_for_finding()]
- "tests_test_adaptive_rate_testwindowstatemachine": "TestWindowStateMachine" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L27 | neighbors=[test_adaptive_rate.py, .test_congestion_avoidance_grows_sublin…, .test_initial_window(), .test_loss_halves_window(), .test_loss_sets_ssthresh_to_half(), .test_recovery_after_loss_enters_conges…]
- "tests_test_agents_testpromoteassets": "TestPromoteAssets" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L693 | neighbors=[test_agents.py, Discovery results → assets/services pro…, .test_creates_asset_and_services_with_c…, .test_dedupes_duplicate_services_in_sam…, .test_empty_result_is_noop(), .test_skips_host_without_ip()]
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "tests_test_auth_login_make_user": "_make_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L44 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future(), .test_raises_expired_password()]
- "tests_test_auth_login_testreasoncodes": "TestReasonCodes" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L223 | neighbors=[test_auth_login.py, Ensure every exception class has the ex…, .test_bcrypt_failure_code(), .test_database_failure_code(), .test_disabled_tenant_code(), .test_disabled_user_code()]
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L90 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_loaders": "test_loaders.py" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, TestLoadEpssErrors, TestLoadKevErrors, TestLoadSnapshotErrors, _valid_epss(), _valid_kev()]
- "tests_test_loaders_testloadsnapshoterrors": "TestLoadSnapshotErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L55 | neighbors=[test_loaders.py, .setup_method(), .test_content_hash_mismatch_raises_valu…, .test_error_message_mentions_re_sync(), .test_hash_mismatch_message_truncates_h…, .test_malformed_json_raises()]
- "tests_test_main_scripts_coverage_mk_scanner": "_mk_scanner()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L27 | neighbors=[test_main_scripts_coverage.py, _scope(), .test_adaptive_estimator_is_shared_and_…, .test_fixed_timeout_flag_disables_the_e…, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…]
- "tests_test_main_scripts_datastore_probe": "test_main_scripts_datastore_probe.py" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, service_banner.py, _svc(), test_elasticsearch_and_couchdb_win_over…, test_ladder_includes_safe_datastore_pro…, test_memcached_probe_response_yields_un…]
- "tests_test_main_scripts_statemodel": "test_main_scripts_statemodel.py" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, test_backward_compatible_old_style_cons…, test_canonical_states_are_the_six_docum…, test_explicit_first_class_value_wins_ov…, test_semantics_in_data_are_promoted_to_…]
- "tests_test_new_scanners_testdeltaengine_write_jsonl": "._write_jsonl()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L379 | neighbors=[TestDeltaEngine, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_nuclei_scanner": "test_nuclei_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, FakeProcess, _finding_line(), test_missing_binary_is_a_reported_failu…, test_nonzero_exit_retains_and_marks_par…, test_nonzero_exit_without_findings_rais…]
- "tests_test_os_fingerprint_testttlinference": "TestTtlInference" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L192 | neighbors=[test_os_fingerprint.py, .test_hop_estimate(), .test_os_family_linux(), .test_os_family_network(), .test_os_family_unknown_on_none(), .test_os_family_windows()]
- "tests_test_pat_auth": "test_pat_auth.py" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, test_new_pat_token_shape_and_hash_stabi…, test_pat_builder_rejects_unknown_scope(), test_pat_builder_returns_token_once_and…, test_pat_builder_supports_non_expiring_…, test_pat_scope_allows_probe_cli_paths()]
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L911 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_ot_passive()]
- "tests_test_remediation_routes_fakedb": "_FakeDB" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L64 | neighbors=[test_remediation_routes.py, .execute(), .flush(), .__init__(), execute() returns the next queued resul…, .test_ai_available_caches_ai_plan()]
- "tests_test_risk_rank": "test_risk_rank.py" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L1 | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, _rank(), test_bounds(), test_confirmed_exploitable_outranks_con…, test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lo…]
- "tests_test_scope_crypt_testencryptdecryptroundtrip": "TestEncryptDecryptRoundtrip" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L28 | neighbors=[test_scope_crypt.py, .test_b64_roundtrip(), .test_different_plaintexts_are_distinct…, .test_different_recipient_cannot_decryp…, .test_multiple_encrypts_different(), .test_roundtrip_empty_scope()]
- "tests_test_scope_validator": "test_scope_validator.py" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, scope_validator.py, TestFetchEngagementScope, TestMergeExclusions, TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes": "TestTargetsInExcludes" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L93 | neighbors=[test_scope_validator.py, .test_all_excluded_returns_empty(), .test_drops_excluded_ip(), .test_drops_excluded_subnet(), .test_fully_excluded_cidr_is_dropped(), .test_hostname_passes_through()]
- "tests_test_service_match": "test_service_match.py" | kind=code-symbol | source=probe/tests/test_service_match.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, service_banner.py, TestHttpMatch, TestNoMatch, TestOtherServices, TestProbeLadder]
- "tests_test_tls_posture_testclassifycipher": "TestClassifyCipher" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L18 | neighbors=[test_tls_posture.py, .test_3des_is_weak(), .test_anonymous_is_weak(), .test_chacha20_is_aead(), .test_export_and_md5_are_weak(), .test_modern_aead_pfs()]
- "tests_test_transport_testidentity": "TestIdentity" | kind=code-symbol | source=probe/tests/test_transport.py:L29 | neighbors=[test_transport.py, .test_agent_state_updates_preserve_scop…, .test_auth_header(), .test_failed_atomic_replace_preserves_p…, .test_is_authenticated_false_initially(), .test_is_authenticated_true_with_creds()]
- "vuln_prioritizer_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AssetInput, FindingInput, vulnPrioritizer, DEMO_ASSETS, DEMO_FINDINGS]
- "websocket_manager_connectionmanager": "ConnectionManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L25 | neighbors=[manager.py, .broadcast(), .connect(), .disconnect(), .get_room_clients(), .__init__()]
- "workers_outbox_run_worker": "run_worker()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L284 | neighbors=[outbox.py, Main loop: claim → process → repeat. Sl…, _claim_batch(), Event, _process(), _reclaim_stale()]
- "workers_reaper": "reaper.py" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, config.py, database.py, expire_attempt(), reap_once()]
- "workflow_modes_engagementmode": "EngagementMode" | kind=code-symbol | source=probe/workflow/modes.py:L51 | neighbors=[modes.py, assessment(), discovery(), host_discovery(), port_scan(), re_scan()]
- "ad_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L1 | neighbors=[ADConnectionError, ADError, build_ad_finding(), DependencyMissingError, severity_from_str(), Shared building blocks for the Active D…]
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=probe/agent/agent.py:L47 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), Return an integer environment setting c…, _run_polled_job_with_heartbeats()]

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
