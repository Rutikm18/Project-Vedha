# Node Description Batch 26 of 336

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

- "services_llm_managerllmservice_dispatch": "._dispatch()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L292 | neighbors=[ManagerLlmService, AiRuntimeError, ._anthropic(), ._ollama(), ._openai(), ._openrouter()] | lang=en
- "services_sla": "sla.py" | kind=code-symbol | source=manager/backend/app/services/sla.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, c5ebd38 feat(sla): per-tenant custom SL…, config.py, compute(), default_windows(), SlaResult] | lang=en
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, backend(), withBackend(), ApiSlaItem, ApiSlaSummary, GET] | lang=en
- "states_datastate_datastate": "DataState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L108 | neighbors=[DashboardGrid.tsx, page.tsx, page.tsx, page.tsx, page.tsx, page.tsx] | lang=en
- "summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, backend.ts, backend()] | lang=en
- "tests_engagement_adapters_test": "engagement-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/engagement-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 42f4e28 feat: enhance security operatio…, 7a637eb feat: network VA accuracy, KEV …, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, adapters.ts] | lang=en
- "tests_test_accuracy_gate_write": "_write()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L25 | neighbors=[test_accuracy_gate.py, .test_corpus_without_any_labels_is_reje…, .test_corpus_without_facts_is_rejected(), .test_ground_truth_states_alone_is_a_va…, .test_unknown_provenance_is_rejected(), .test_unlabeled_provenance_is_rejected()] | lang=en
- "tests_test_agent_dispatch": "test_agent_dispatch.py" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, _claim_fixture(), TestAgentWebSocketAuthentication] | lang=en
- "tests_test_agents_redis": "_redis()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L26 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()] | lang=en
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard] | lang=en
- "tests_test_ai_normalizer_testproposecandidates": "TestProposeCandidates" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L153 | neighbors=[test_ai_normalizer.py, .test_ai_assisted_flag_set_on_candidate…, .test_cache_hit_bypasses_client(), .test_client_failure_returns_empty(), .test_malformed_response_missing_produc…, .test_malformed_response_not_a_list_ret…] | lang=en
- "tests_test_attack_path_correlation_get": "_get()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L19 | neighbors=[test_attack_path_correlation.py, test_cleartext_cluster_needs_two(), test_device_role_from_facts_also_amplif…, test_exposed_db_with_unauth_is_critical…, test_legacy_windows_smbv1_plus_rdp(), test_ntlm_relay_high_when_smbv1_also_en…] | lang=en
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, .test_run_without_connection_returns_em…, .test_run_write_noop_without_connection…, .test_sync_to_neo4j_noop_without_client…, PathAnalyzer, GraphBuilder] | lang=en
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
- "tests_test_portal_scope": "test_portal_scope.py" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _client(), _operator(), TestAssertClient, TestClientScoped, TestPortalTokenClaims] | lang=en
- "tests_test_posture_trace": "test_posture_trace.py" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _asset(), _fact(), _outcome(), TestAbsentVersusClean, TestBehaviourPreserved] | lang=en

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
