# Node Description Batch 24 of 236

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

- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L90 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_loaders": "test_loaders.py" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, TestLoadEpssErrors, TestLoadKevErrors, TestLoadSnapshotErrors, _valid_epss(), _valid_kev()]
- "tests_test_loaders_testloadsnapshoterrors": "TestLoadSnapshotErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L55 | neighbors=[test_loaders.py, .setup_method(), .test_content_hash_mismatch_raises_valu…, .test_error_message_mentions_re_sync(), .test_hash_mismatch_message_truncates_h…, .test_malformed_json_raises()]
- "tests_test_main_scripts_coverage_mk_scanner": "_mk_scanner()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L27 | neighbors=[test_main_scripts_coverage.py, _scope(), .test_adaptive_estimator_is_shared_and_…, .test_fixed_timeout_flag_disables_the_e…, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…]
- "tests_test_main_scripts_datastore_probe": "test_main_scripts_datastore_probe.py" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, service_banner.py, _svc(), test_elasticsearch_and_couchdb_win_over…, test_ladder_includes_safe_datastore_pro…, test_memcached_probe_response_yields_un…]
- "tests_test_main_scripts_statemodel": "test_main_scripts_statemodel.py" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, test_backward_compatible_old_style_cons…, test_canonical_states_are_the_six_docum…, test_explicit_first_class_value_wins_ov…, test_semantics_in_data_are_promoted_to_…]
- "tests_test_new_scanners_testdeltaengine_write_jsonl": "._write_jsonl()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L382 | neighbors=[TestDeltaEngine, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_nuclei_scanner": "test_nuclei_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, FakeProcess, _finding_line(), test_missing_binary_is_a_reported_failu…, test_nonzero_exit_retains_and_marks_par…, test_nonzero_exit_without_findings_rais…]
- "tests_test_os_fingerprint_testttlinference": "TestTtlInference" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L192 | neighbors=[test_os_fingerprint.py, .test_hop_estimate(), .test_os_family_linux(), .test_os_family_network(), .test_os_family_unknown_on_none(), .test_os_family_windows()]
- "tests_test_pat_auth": "test_pat_auth.py" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, test_new_pat_token_shape_and_hash_stabi…, test_pat_builder_rejects_unknown_scope(), test_pat_builder_returns_token_once_and…, test_pat_builder_supports_non_expiring_…, test_pat_scope_allows_probe_cli_paths()]
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
- "websocket_manager_graphwebsocketmanager_handle_client": ".handle_client()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L360 | neighbors=[GraphWebSocketManager, .connect(), .disconnect(), .send_personal(), ._handle_message(), Handle a new WebSocket client connectio…]
- "workers_outbox_reclaim_stale": "_reclaim_stale()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L230 | neighbors=[outbox.py, Requeue events a dead worker left in PR…, _dead_letter_stale_stmt(), _requeue_stale_stmt(), _stale_cutoff(), run_worker()]
- "workers_reaper": "reaper.py" | kind=code-symbol | source=manager/backend/app/workers/reaper.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, config.py, database.py, expire_attempt(), reap_once()]
- "workflow_modes_engagementmode": "EngagementMode" | kind=code-symbol | source=probe/workflow/modes.py:L51 | neighbors=[modes.py, assessment(), discovery(), host_discovery(), port_scan(), re_scan()]
- "ad_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L1 | neighbors=[ADConnectionError, ADError, build_ad_finding(), DependencyMissingError, severity_from_str(), Shared building blocks for the Active D…]
- "agent_agent_bounded_env_int": "_bounded_env_int()" | kind=code-symbol | source=probe/agent/agent.py:L47 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), Return an integer environment setting c…, _run_polled_job_with_heartbeats()]
- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L709 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say(), Release a staged job only after the man…, Release a staged job only after the man…]
- "agent_device_identity": "device_identity.py" | kind=code-symbol | source=probe/agent/device_identity.py:L1 | neighbors=[decode_key(), encode_key(), generate_signing_identity(), sign_b64(), signing_public_from_private(), verify_site_policy()]
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L196 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…, Coerce val to float and clamp to [lo, h…]
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L282 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count unique open network endpoints, no…]
- "agent_engine_derive_post_stage": "_derive_post_stage()" | kind=code-symbol | source=probe/agent/engine.py:L442 | neighbors=[engine.py, _derive_devices(), _derive_exposure(), Return (extra ScanResults to append as …, run_scan(), _results_by_target()]
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L216 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Translate operator-supplied job params …, Return the effective whole-job deadline…]
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L49 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError]
- "agent_result_spool_resultspool_flush_spool": ".flush_spool()" | kind=code-symbol | source=probe/agent/result_spool.py:L184 | neighbors=[Re-attempt upload of all previously spo…, ResultSpool, .exists(), ._path(), .quarantine(), .remove()]
- "agent_result_spool_resultspool_remove": ".remove()" | kind=code-symbol | source=probe/agent/result_spool.py:L110 | neighbors=[Remove the spool file for a successfull…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()]
- "agent_transport_atomic_write_private_state": "_atomic_write_private_state()" | kind=code-symbol | source=probe/agent/transport.py:L83 | neighbors=[transport.py, _sync_directory(), Durably replace one private JSON state …, .update_state(), Durably replace one private JSON state …, Durably replace one private JSON state …]
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L507 | neighbors=[Send a heartbeat to the manager.       …, Transport, .ensure_device_access(), Send a heartbeat to the manager.       …, Send a heartbeat to the manager.       …, Send a heartbeat to the manager.       …]
- "ai_prioritizer": "prioritizer.py" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[extract_features(), _to_float(), VulnPrioritizer, VulnPrioritizer — ML-based vulnerabilit…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …]
- "app_config_settings": "Settings" | kind=code-symbol | source=manager/backend/app/config.py:L7 | neighbors=[config.py, get_settings(), .cors_origins(), .is_production(), BaseSettings, AiRuntimeError]
- "assistant_modelswitcher": "ModelSwitcher.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/ModelSwitcher.tsx:L1 | neighbors=[AssistantDrawer.tsx, AiStatus, ModelSelection, ModelSwitcher(), ProviderStatus, readStored()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-023.json

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
