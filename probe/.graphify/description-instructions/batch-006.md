# Node Description Batch 7 of 92

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

- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=tests/test_probe_core.py:L911 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_network_va_resolves()]
- "workflow_asset": "asset.py" | kind=code-symbol | source=workflow/asset.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, de583d8 feat(workflow): wire os_fingerp…, test_probe_core.py, test_workflow_execution.py, scanner_base.py, Asset]
- "workflow_cache": "cache.py" | kind=code-symbol | source=workflow/cache.py:L1 | neighbors=[engine.py, ae7a30b feat: add Posture & Patch-Compa…, de583d8 feat(workflow): wire os_fingerp…, test_probe_core.py, test_probe_next_features.py, scanner_base.py]
- "workflow_gates_gate_0_is_passive_profile": "gate_0_is_passive_profile()" | kind=code-symbol | source=workflow/gates.py:L63 | neighbors=[gates.py, gate_2_host_discovery(), gate_3_port_scan(), True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…]
- "workflow_workflow_engine_gather_per_host": "_gather_per_host()" | kind=code-symbol | source=workflow/workflow_engine.py:L84 | neighbors=[workflow_engine.py, _scan_one(), Run per-host probes with bounded fan-ou…, run_engagement(), Run per-host probes with bounded fan-ou…, Run per-host probes with bounded fan-ou…]
- "workflow_workflow_engine_scan_one": "_scan_one()" | kind=code-symbol | source=workflow/workflow_engine.py:L71 | neighbors=[workflow_engine.py, _gather_per_host(), Run one component without allowing a ta…, run_engagement(), Run one component without allowing a ta…, Run one component without allowing a ta…]
- "agent_cli_cmd_auth_login": "cmd_auth_login()" | kind=code-symbol | source=agent/cli.py:L237 | neighbors=[cli.py, CliError, ConfigStore, .set_profile(), _env(), ManagerClient]
- "agent_engine_leaselosterror": "LeaseLostError" | kind=code-symbol | source=agent/engine.py:L514 | neighbors=[engine.py, ScanResult, ScopeGuard, RuntimeError, WorkflowCache, ExecutionTrace]
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…]
- "agent_task_runner": "task_runner.py" | kind=code-symbol | source=agent/task_runner.py:L1 | neighbors=[JobResult, TaskRunner, use_cases.py, task_runner.py — orchestrates the full …, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…]
- "main_scripts_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=main_scripts/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, .__init__(), ResultWriter, ScanResult, ScopeGuard, OSError]
- "main_scripts_scan_funnel_build_default_funnel": "build_default_funnel()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L215 | neighbors=[scan_funnel.py, ScanFunnel, Wire the funnel with the package's real…, Wire the funnel with the package's real…, Wire the funnel with the package's real…, Wire the funnel with the package's real…]
- "main_scripts_scan_funnel_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L97 | neighbors=[scan_funnel.py, The port set worth scanning = union of …, .run_host(), The port set worth scanning = union of …, The port set worth scanning = union of …, The port set worth scanning = union of …]
- "main_scripts_scan_funnel_route_ports": "route_ports()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L65 | neighbors=[scan_funnel.py, Map a host's open ports onto the deep-s…, .run_host(), Map a host's open ports onto the deep-s…, Map a host's open ports onto the deep-s…, Map a host's open ports onto the deep-s…]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L282 | neighbors=[tls_fingerprint.py, BaseScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard]
- "scanner_scan_funnel_build_default_funnel": "build_default_funnel()" | kind=code-symbol | source=scanner/scan_funnel.py:L215 | neighbors=[scan_funnel.py, ScanFunnel, Wire the funnel with the package's real…, Wire the funnel with the package's real…, Wire the funnel with the package's real…, Wire the funnel with the package's real…]
- "scanner_scan_funnel_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=scanner/scan_funnel.py:L97 | neighbors=[scan_funnel.py, The port set worth scanning = union of …, .run_host(), The port set worth scanning = union of …, The port set worth scanning = union of …, The port set worth scanning = union of …]
- "scanner_scan_funnel_funnelresult": "FunnelResult" | kind=code-symbol | source=scanner/scan_funnel.py:L83 | neighbors=[scan_funnel.py, The full outcome of funnelling one host., .run_host(), The full outcome of funnelling one host., The full outcome of funnelling one host., The full outcome of funnelling one host.]
- "scanner_scan_funnel_route_ports": "route_ports()" | kind=code-symbol | source=scanner/scan_funnel.py:L65 | neighbors=[scan_funnel.py, Map a host's open ports onto the deep-s…, .run_host(), Map a host's open ports onto the deep-s…, Map a host's open ports onto the deep-s…, Map a host's open ports onto the deep-s…]
- "scanner_scanner_base_adaptiveratecontroller": "AdaptiveRateController" | kind=code-symbol | source=scanner/scanner_base.py:L401 | neighbors=[scanner_base.py, .acquire(), .__init__(), ._on_loss(), ._on_success(), .report_loss()]
- "scanner_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=scanner/syn_scanner.py:L245 | neighbors=[syn_scanner.py, SYN scan on privileged Linux; transpare…, BaseScanner, ._build_results(), ._fallback_scan(), .__init__()]
- "tests_test_adaptive_rate_testwindowstatemachine": "TestWindowStateMachine" | kind=code-symbol | source=tests/test_adaptive_rate.py:L27 | neighbors=[test_adaptive_rate.py, .test_congestion_avoidance_grows_sublin…, .test_initial_window(), .test_loss_halves_window(), .test_loss_sets_ssthresh_to_half(), .test_recovery_after_loss_enters_conges…]
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_main_scripts_coverage_mk_scanner": "_mk_scanner()" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L27 | neighbors=[test_main_scripts_coverage.py, _scope(), .test_adaptive_estimator_is_shared_and_…, .test_fixed_timeout_flag_disables_the_e…, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…]
- "tests_test_main_scripts_datastore_probe": "test_main_scripts_datastore_probe.py" | kind=code-symbol | source=tests/test_main_scripts_datastore_probe.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, service_banner.py, _svc(), test_elasticsearch_and_couchdb_win_over…, test_ladder_includes_safe_datastore_pro…, test_memcached_probe_response_yields_un…]
- "tests_test_main_scripts_statemodel": "test_main_scripts_statemodel.py" | kind=code-symbol | source=tests/test_main_scripts_statemodel.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, scanner_base.py, test_backward_compatible_old_style_cons…, test_canonical_states_are_the_six_docum…, test_explicit_first_class_value_wins_ov…, test_semantics_in_data_are_promoted_to_…]
- "tests_test_new_scanners_testdeltaengine_write_jsonl": "._write_jsonl()" | kind=code-symbol | source=tests/test_new_scanners.py:L382 | neighbors=[TestDeltaEngine, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_os_fingerprint_testttlinference": "TestTtlInference" | kind=code-symbol | source=tests/test_os_fingerprint.py:L192 | neighbors=[test_os_fingerprint.py, .test_hop_estimate(), .test_os_family_linux(), .test_os_family_network(), .test_os_family_unknown_on_none(), .test_os_family_windows()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip": "TestEncryptDecryptRoundtrip" | kind=code-symbol | source=tests/test_scope_crypt.py:L28 | neighbors=[test_scope_crypt.py, .test_b64_roundtrip(), .test_different_plaintexts_are_distinct…, .test_different_recipient_cannot_decryp…, .test_multiple_encrypts_different(), .test_roundtrip_empty_scope()]
- "tests_test_service_match": "test_service_match.py" | kind=code-symbol | source=tests/test_service_match.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, service_banner.py, TestHttpMatch, TestNoMatch, TestOtherServices, TestProbeLadder]
- "tests_test_task_runner": "test_task_runner.py" | kind=code-symbol | source=tests/test_task_runner.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, task_runner.py, _fake_run_scan(), runner(), TestRunnerHeadless, TestRunnerScanTypes]
- "tests_test_tls_posture_testclassifycipher": "TestClassifyCipher" | kind=code-symbol | source=tests/test_tls_posture.py:L18 | neighbors=[test_tls_posture.py, .test_3des_is_weak(), .test_anonymous_is_weak(), .test_chacha20_is_aead(), .test_export_and_md5_are_weak(), .test_modern_aead_pfs()]
- "tests_test_transport_testidentity": "TestIdentity" | kind=code-symbol | source=tests/test_transport.py:L29 | neighbors=[test_transport.py, .test_agent_state_updates_preserve_scop…, .test_auth_header(), .test_failed_atomic_replace_preserves_p…, .test_is_authenticated_false_initially(), .test_is_authenticated_true_with_creds()]
- "tests_test_transport_testsubmitresult": "TestSubmitResult" | kind=code-symbol | source=tests/test_transport.py:L425 | neighbors=[test_transport.py, .test_2xx_variants_return_true(), .test_large_payload_is_gzipped(), .test_network_error_returns_false(), .test_permanent_client_errors_are_marke…, .test_retryable_client_errors_return_fa…]
- "tests_test_ws_claim_protocol": "test_ws_claim_protocol.py" | kind=code-symbol | source=tests/test_ws_claim_protocol.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, agent.py, result_spool.py, test_busy_probe_declines_additional_off…, test_http_spool_flush_removes_only_mana…, test_offer_is_staged_and_only_sends_ack…]
- "workflow_asset_asset_needs_recheck_live": ".needs_recheck_live()" | kind=code-symbol | source=workflow/asset.py:L82 | neighbors=[Asset, _utcnow(), Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…]
- "workflow_modes_engagementmode": "EngagementMode" | kind=code-symbol | source=workflow/modes.py:L51 | neighbors=[modes.py, assessment(), discovery(), host_discovery(), port_scan(), re_scan()]
- "workflow_router": "router.py" | kind=code-symbol | source=workflow/router.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, test_probe_core.py, test_router_db.py, looks_like_db(), looks_like_http(), looks_like_ssh()]
- "workflow_workflow_engine_port_candidates": "_port_candidates()" | kind=code-symbol | source=workflow/workflow_engine.py:L122 | neighbors=[workflow_engine.py, Return TCP ports worth scanning for thi…, run_engagement(), Return TCP ports worth scanning for thi…, Return TCP ports worth scanning for thi…, Return TCP ports worth scanning for thi…]
- "workflow_workflow_engine_split_cached": "_split_cached()" | kind=code-symbol | source=workflow/workflow_engine.py:L104 | neighbors=[workflow_engine.py, Splits candidate_ports into (ports that…, run_engagement(), Splits candidate_ports into (ports that…, Splits candidate_ports into (ports that…, Splits candidate_ports into (ports that…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-006.json

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
