# Node Description Batch 34 of 330

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

- "tests_test_os_fingerprint_testprovenance": "TestProvenance" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L369 | neighbors=[test_os_fingerprint.py, ._scanner(), .test_datagram_echo_without_ttl_does_no…, .test_icmp_unavailable_tcp_hints_is_met…, .test_icmp_unavailable_with_tcp_ttl_is_…, .test_no_icmp_but_tcp_ttl_hint_is_metho…]
- "tests_test_os_fusion": "test_os_fusion.py" | kind=code-symbol | source=probe/tests/test_os_fusion.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, _os(), test_build_only_is_strong_but_not_certa…, test_build_smb2_hostname_is_high_confid…, test_no_os_signal_yields_no_finding(), test_smb2_plus_p0f_stack_is_medium()]
- "tests_test_portal_assistant_llm": "_llm()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L86 | neighbors=[test_portal_assistant.py, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_only_the_whitelisted_finding_field…, test_reply_is_timestamped_and_attribute…]
- "tests_test_portal_assistant_test_only_the_whitelisted_finding_fields_reach_the_model": "test_only_the_whitelisted_finding_fields_reach_the_model()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L119 | neighbors=[test_portal_assistant.py, Internal triage/evidence fields must ne…, _ask(), _client(), _db(), _engagement()]
- "tests_test_portal_read_db_for_create": "_db_for_create()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L216 | neighbors=[test_portal_read.py, Mock the create_scan_request db flow: e…, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict()]
- "tests_test_portal_scope": "test_portal_scope.py" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _client(), _operator(), TestAssertClient, TestClientScoped, TestPortalTokenClaims]
- "tests_test_posture_confidence": "test_posture_confidence.py" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _asset(), _by_rule(), _fact(), TestAssessor, TestChains]
- "tests_test_probe_core_testtuningfromparams": "TestTuningFromParams" | kind=code-symbol | source=probe/tests/test_probe_core.py:L898 | neighbors=[test_probe_core.py, .test_clamped_rate(), .test_defaults(), .test_no_ssh_creds_without_user(), .test_passive_listen_seconds(), .test_recheck_hours()]
- "tests_test_raw_facts": "test_raw_facts.py" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L1 | neighbors=[25c014d feat: enhance campaign progress…, _scalars(), _sr(), test_raw_facts_bounds_and_no_results(), test_raw_facts_filter_by_scanner(), test_raw_facts_grouped_by_scanner()]
- "tests_test_remediation_generator_testparsejsonresponse": "TestParseJsonResponse" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L32 | neighbors=[test_remediation_generator.py, .test_empty_returns_empty(), .test_junk_returns_empty(), .test_non_object_json_returns_empty(), .test_plain_object(), .test_recovers_from_preamble()]
- "tests_test_remediation_routes_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L27 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, .test_cached_hit_without_force_returns_…, .test_cross_tenant_is_404(), .test_cached_ai_on_hit()]
- "tests_test_result_archive_job": "_job()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L42 | neighbors=[test_result_archive.py, .test_archived_json_equals_the_submitte…, .test_failure_envelopes_are_archived_to…, .test_filename_is_result_plus_timestamp…, .test_no_partial_files_are_left_behind(), .test_two_jobs_in_the_same_second_do_no…]
- "tests_test_result_archive_runner": "_runner()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L33 | neighbors=[test_result_archive.py, .test_archived_json_equals_the_submitte…, .test_failure_envelopes_are_archived_to…, .test_filename_is_result_plus_timestamp…, .test_no_partial_files_are_left_behind(), .test_two_jobs_in_the_same_second_do_no…]
- "tests_test_result_archive_testprepareatstartup": "TestPrepareAtStartup" | kind=code-symbol | source=probe/tests/test_result_archive.py:L162 | neighbors=[test_result_archive.py, The agent creates the archive directory…, .test_creates_the_directory_including_p…, .test_disabled_when_env_is_empty(), .test_existing_but_unwritable_directory…, .test_is_idempotent_across_restarts()]
- "tests_test_result_spool": "test_result_spool.py" | kind=code-symbol | source=probe/tests/test_result_spool.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, result_spool.py, spool(), TestResultSpool]
- "tests_test_risk_port_coverage_swept_by_network_va": "_swept_by_network_va()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L53 | neighbors=[test_risk_port_coverage.py, Exactly what a default network_va puts …, test_branch_tables_still_contribute(), test_datagram_branch_ports_are_not_in_t…, test_every_backdoor_port_is_swept(), test_named_high_value_ports_are_scanned…]
- "tests_test_risk_rank_rank": "_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L6 | neighbors=[test_risk_rank.py, test_bounds(), test_confirmed_exploitable_outranks_con…, test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lo…, test_kev_raises_rank()]
- "tests_test_risk_score_contract": "test_risk_score_contract.py" | kind=code-symbol | source=manager/backend/tests/test_risk_score_contract.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, test_only_detection_engine_posture_evid…, test_posture_severity_and_evidence_driv…]
- "tests_test_scan_health": "test_scan_health.py" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _summary(), test_aggregates_across_hosts(), test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scanner_congestion_testresolvecandidates": "TestResolveCandidates" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L295 | neighbors=[test_scanner_congestion.py, .test_absent_requested_family_falls_bac…, .test_deduplicates_repeated_addresses(), .test_family_filter_restricts_results(), .test_literal_ip_resolves_to_itself(), .test_returns_every_family_in_order()]
- "tests_test_scope_targets": "test_scope_targets.py" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, test_property_every_accepted_target_is_…, TestExclusions, TestIpVersionSafety, TestNoScopeAuthorizesNothing, TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected": "TestOutOfScopeIsRejected" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L44 | neighbors=[test_scope_targets.py, .test_blank_token_is_rejected(), .test_cidr_broader_than_scope(), .test_explicit_empty_list_is_rejected(), .test_hostname_is_not_routable(), .test_ip_outside_scope()]
- "tests_test_sla_policy": "test_sla_policy.py" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L1 | neighbors=[c5ebd38 feat(sla): per-tenant custom SL…, _db(), _finding(), _operator(), _row(), TestPolicyAwareCompute]
- "tests_test_smb_ntlm_build_testparsechallenge": "TestParseChallenge" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L38 | neighbors=[test_smb_ntlm_build.py, .test_legacy_6_1_is_win7(), .test_no_version_field_yields_name_but_…, .test_non_challenge_returns_none(), .test_server_2022_build_20348(), .test_unknown_build_still_classified_wi…]
- "tests_test_syn_scanner_testbuildresultsenrichment": "TestBuildResultsEnrichment" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L349 | neighbors=[test_syn_scanner.py, ._scanner(), .test_closed_and_filtered_suppressed_by…, .test_open_result_carries_signals_and_o…, .test_open_without_signals_has_no_os_gu…, .test_os_guess_is_tagged_tcp_derived_no…]
- "tests_test_tier1_correlations": "test_tier1_correlations.py" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L1 | neighbors=[6e2818f Add support for additional serv…, _run(), test_anon_data_exposure_cluster(), test_mgmt_plane_exposed_on_cipher_zero_…, test_mgmt_plane_needs_two_when_no_ciphe…, test_single_anon_finding_does_not_corre…]
- "tests_test_tls_integration": "test_tls_integration.py" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, tls_scanner.py, _self_signed(), test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_legacy_versions_legacytlsserver": "_LegacyTLSServer" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L55 | neighbors=[test_tls_legacy_versions.py, .__enter__(), .__exit__(), .__init__(), ._serve(), A loopback server pinned to exactly one…]
- "tests_test_tls_port_coverage": "test_tls_port_coverage.py" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, service_enum.py, test_refused_handshake_is_an_error_not_…, TestDeliberateExclusions, TestSingleSourceOfTruth, TestWidenedCoverage]
- "tests_test_tls_posture_testgradetlsposture": "TestGradeTlsPosture" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L72 | neighbors=[test_tls_posture.py, .test_empty_cipher_details_still_grades…, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_no_forward_secrecy(), .test_grade_c_tls11()]
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NucleiRunReport, NucleiScanError, NucleiScanner]
- "vuln_tasks": "tasks.py" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment()]
- "websocket_manager_agentconnectionmanager_push_job_to_first_online": ".push_job_to_first_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L207 | neighbors=[AgentConnectionManager, .online_agents_for_tenant(), .push_job(), Push a job to the first online agent in…, Push a job to the first online agent in…, Push a job to the first online agent in…]
- "websocket_manager_connectionmanager_broadcast": ".broadcast()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L51 | neighbors=[ConnectionManager, .disconnect(), .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), ._handle_message()]
- "workers_outbox_mark_retry_or_dead": "_mark_retry_or_dead()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L367 | neighbors=[outbox.py, _process(), Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…]
- "workflow_gates_gate_0_is_passive_profile": "gate_0_is_passive_profile()" | kind=code-symbol | source=probe/workflow/gates.py:L98 | neighbors=[gates.py, gate_2_host_discovery(), gate_3_port_scan(), gate_4b_os_fingerprint(), True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…]
- "workflow_host_health_hosthealthmonitor_state": "._state()" | kind=code-symbol | source=probe/workflow/host_health.py:L129 | neighbors=[HostHealthMonitor, .confirm(), .is_offline(), ._mark_offline(), .note_skipped(), .observe()]
- "workflow_workflow_engine_run_branch": "_run_branch()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L292 | neighbors=[workflow_engine.py, Run ONE deep-scan branch for one host: …, _record(), _record_reused(), _scan_one(), _split_cached()]
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, DependencyMissingError, Base class for Active Directory assessm…, FindingSeverity]
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L213 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-033.json

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
