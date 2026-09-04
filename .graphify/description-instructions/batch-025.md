# Node Description Batch 26 of 332

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

- "tests_test_auth_login_teststartupdiagnostics": "TestStartupDiagnostics" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L251 | neighbors=[test_auth_login.py, .test_bcrypt_round_trip_passes(), .test_cookie_config_fatal_in_production…, .test_cookie_config_ok_in_development(), .test_database_check_returns_fatal_on_c…, .test_jwt_secret_known_weak_is_fatal()] | lang=en
- "tests_test_customer_access_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L23 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_assigns_agent_to_engagement(), .test_unknown_agent_is_404()] | lang=en
- "tests_test_cve_correlation_testcorrelate": "TestCorrelate" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L167 | neighbors=[test_cve_correlation.py, .test_backport_banner_downgrades_confid…, .test_clean_banner_stays_medium(), .test_dedup_by_cve_target_port(), .test_exposed_top_finding(), .test_facts_without_cpe_ignored()] | lang=en
- "tests_test_cve_correlation_testversion": "TestVersion" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L34 | neighbors=[test_cve_correlation.py, .test_compare(), .test_in_range_end_exclusive(), .test_in_range_exact(), .test_in_range_start_inclusive(), .test_in_range_unconstrained_is_false()] | lang=en
- "tests_test_dualstack_fallback": "test_dualstack_fallback.py" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, scanner_base.py, TestOsFingerprintSmbBuildFallback, TestRdpFallback, TestResolveIpCandidates, TestSmbNegotiateFallback] | lang=en
- "tests_test_exploit_engine_rationale_1": "Unit tests for the exploitation engine.  All external connections (Metasploit RP" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "tests_test_exploit_engine_rationale_420": "Run against a live Metasploitable2 lab target.     Requires: msfrpcd running, Me" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L420 | neighbors=[TestMetasploitIntegration, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=pt
- "tests_test_exploit_engine_rationale_465": "Register --msf-host CLI option for integration tests." | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L465 | neighbors=[pytest_addoption(), MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "tests_test_exposed_services_asset": "_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L22 | neighbors=[test_exposed_services.py, test_exposed_findings_flow_through_dete…, .test_backdoor_4444_is_high_internal(), .test_banner_carried_as_evidence(), .test_dedicated_ports_not_double_report…, .test_internet_facing_escalates_severit…] | lang=en
- "tests_test_exposed_services_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L16 | neighbors=[test_exposed_services.py, test_exposed_findings_flow_through_dete…, .test_backdoor_4444_is_high_internal(), .test_banner_carried_as_evidence(), .test_dedicated_ports_not_double_report…, .test_internet_facing_escalates_severit…] | lang=en
- "tests_test_fact_contract": "test_fact_contract.py" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, 8f6bf49 Refactor code structure and rem…, _emitted_paths_by_scanner(), _ingest_corpus(), _load_corpus(), test_corpus_is_present_and_nonempty()] | lang=en
- "tests_test_fd_limit": "test_fd_limit.py" | kind=code-symbol | source=probe/tests/test_fd_limit.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, port_scanner.py, scanner_base.py, test_caps_below_soft_limit(), test_floor_when_limit_tiny(), test_full_profile_covers_the_whole_tcp_…] | lang=en
- "tests_test_job_cancel_count": "_count()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L65 | neighbors=[test_job_cancel.py, test_cancel_records_who_did_it(), test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…, test_pending_job_is_cancelled_and_freed…, test_running_job_bumps_the_fence_to_abo…] | lang=en
- "tests_test_main_scripts_correlation_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L13 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts(), test_correlations_are_evidence_backed(), test_legacy_windows_surface_smbv1_plus_…, test_no_legacy_surface_with_only_smbv1()] | lang=en
- "tests_test_main_scripts_device_testclassifydevice": "TestClassifyDevice" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L17 | neighbors=[test_main_scripts_device.py, .test_domain_controller(), .test_iot_camera(), .test_network_device_router(), .test_printer(), .test_service_product_reinforces_server…] | lang=en
- "tests_test_main_scripts_errno": "test_main_scripts_errno.py" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _oserr(), test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_dns_failure_is_error_not_filtered(), test_errno_none_falls_back_to_os_error()] | lang=en
- "tests_test_new_scanners_make_scan_record": "_make_scan_record()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L315 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…] | lang=en
- "tests_test_new_scanners_testiotscanner": "TestIoTScanner" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L246 | neighbors=[test_new_scanners.py, .test_coap_get_wellknown_header(), .test_coap_get_wellknown_path(), .test_coap_response_parse_205(), .test_coap_response_parse_404(), .test_coap_response_parse_short()] | lang=en
- "tests_test_nfs_scanner": "test_nfs_scanner.py" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, scanner_base.py, _mount_export_reply(), _portmap_dump_reply(), TestNFSFindings, TestNFSScanner] | lang=en
- "tests_test_online_get_returning": "_get_returning()" | kind=code-symbol | source=probe/tests/test_online.py:L51 | neighbors=[test_online.py, A fake transport that ignores its args …, .test_gap_fill_sets_cvss_and_recomputes…, .test_online_all_cross_checks_and_annot…, .test_empty_result_is_none(), .test_garbage_json_is_fail_open()] | lang=en
- "tests_test_os_fingerprint_teststacksignature": "TestStackSignature" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L283 | neighbors=[test_os_fingerprint.py, .test_fingerprint_os_folds_in_stack_but…, .test_fingerprint_os_stack_guess_none_w…, .test_linux_from_option_layout_and_wsca…, .test_macos_darwin_layout(), .test_no_ttl_yields_no_stack()] | lang=en
- "tests_test_outbox_reclaim_now": "_now()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L25 | neighbors=[test_outbox_reclaim.py, test_boundary_at_exactly_the_lease_is_r…, test_dead_letter_and_requeue_are_mutual…, test_dead_letter_stmt_targets_exhausted…, test_expired_processing_lock_is_reclaim…, test_fresh_processing_lock_is_not_recla…] | lang=en
- "tests_test_portal_assistant_ask": "_ask()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L76 | neighbors=[test_portal_assistant.py, test_a_non_client_user_is_refused(), test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_model_failure_surfaces_its_status_…] | lang=en
- "tests_test_portal_assistant_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L60 | neighbors=[test_portal_assistant.py, execute() → engagement, then findings, …, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_model_failure_surfaces_its_status_…] | lang=en
- "tests_test_portal_read_testcreatescanrequest": "TestCreateScanRequest" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L242 | neighbors=[test_portal_read.py, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_operator_cannot_create(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict()] | lang=en
- "tests_test_posture_trace": "test_posture_trace.py" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _asset(), _fact(), _outcome(), TestAbsentVersusClean, TestBehaviourPreserved] | lang=en
- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=probe/tests/test_probe_core.py:L189 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()] | lang=en
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L948 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_network_va_resolves()] | lang=en
- "tests_test_remediation_kb_f": "_f()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L11 | neighbors=[test_remediation_kb.py, .test_cve_without_keyword_is_patch(), .test_keyword_categories(), .test_order_specificity_anon_ftp_beats_…, .test_unmatched_is_generic(), .test_missing_os_defaults_to_generic()] | lang=en
- "tests_test_remediation_routes_fakedb": "_FakeDB" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L65 | neighbors=[test_remediation_routes.py, .execute(), .flush(), .__init__(), execute() returns the next queued resul…, .test_ai_available_caches_ai_plan()] | lang=en
- "tests_test_result_archive": "test_result_archive.py" | kind=code-symbol | source=probe/tests/test_result_archive.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, task_runner.py, _job(), _ok_result(), _reset_archive_latch(), _runner()] | lang=en
- "tests_test_rsync_scanner": "test_rsync_scanner.py" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, scanner_base.py, _FakeSock, TestHandshake, TestParity] | lang=en
- "tests_test_run_all_reconcile": "test_run_all_reconcile.py" | kind=code-symbol | source=probe/tests/test_run_all_reconcile.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, run_all.py, scan_funnel.py, test_advertised_dynamic_ports_extractio…, test_open_tcp_ports_ignores_non_open_an…, test_reconcile_folds_in_only_reachable_…] | lang=en
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks": "TestTheScopeGateStillWorks" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L72 | neighbors=[test_run_scoped_fact_scope.py, The exemption must be narrow. These are…, .test_an_unknown_scanner_gets_no_exempt…, .test_excluded_cidr_still_wins(), .test_hostname_target_is_still_refused(), .test_out_of_scope_finding_is_still_rej…] | lang=en
- "tests_test_smb_ntlm_build_challenge": "_challenge()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L16 | neighbors=[test_smb_ntlm_build.py, Synthesize an NTLMSSP CHALLENGE (Type-2…, .test_end_to_end_framing_extracts_build…, .test_ntlm_os_build_shared_function(), .test_legacy_6_1_is_win7(), .test_no_version_field_yields_name_but_…] | lang=en
- "tests_test_transport_testsubmitresult": "TestSubmitResult" | kind=code-symbol | source=probe/tests/test_transport.py:L425 | neighbors=[test_transport.py, .test_2xx_variants_return_true(), .test_large_payload_is_gzipped(), .test_network_error_returns_false(), .test_permanent_client_errors_are_marke…, .test_retryable_client_errors_return_fa…] | lang=en
- "tests_test_validation_endpoints": "test_validation_endpoints.py" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _mock_db(), test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids()] | lang=en
- "tests_test_vantage_fusion_probe": "_probe()" | kind=code-symbol | source=manager/backend/tests/test_vantage_fusion.py:L15 | neighbors=[test_vantage_fusion.py, Build a one-target probe exposure resul…, test_ambiguous_when_only_open_filtered(), test_declared_external_vantage_without_…, test_external_vantage_open_makes_port_e…, test_fused_service_exposure_is_keyed_fo…] | lang=en
- "tests_test_vuln_enrichment_make_http_mock": "_make_http_mock()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L52 | neighbors=[test_vuln_enrichment.py, Create a mock httpx.AsyncClient that re…, test_check_cisa_kev_absent(), test_check_cisa_kev_case_insensitive(), test_check_cisa_kev_present(), test_enrich_full()] | lang=en
- "tests_test_wire_identity": "test_wire_identity.py" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L1 | neighbors=[2c53ae9 evasion(scanner): randomized sc…, 37376de hardening(scanner): OPSEC de-si…, 4733f24 evasion(scanner): --source-port…, TestChooseSourcePort, TestEvasionFlags, TestJitteredDelay] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-025.json

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
