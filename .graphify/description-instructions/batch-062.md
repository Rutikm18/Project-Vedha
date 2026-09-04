# Node Description Batch 63 of 332

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

- "tests_test_e2e_engagement_to_findings_vulnerable_host_facts": "_vulnerable_host_facts()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L137 | neighbors=[test_e2e_engagement_to_findings.py, Exactly what the probe's smb/port scann…, test_correlated_findings_cite_their_bas…, test_manager_correlation_finds_all_thre…, test_ntlm_relay_is_high_when_smbv1_pres…]
- "tests_test_engagement_validation": "test_engagement_validation.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_create_normalizes_name_scopes_and_…, test_create_rejects_invalid_scope_entri…, test_create_rejects_reversed_date_range…, test_update_rejects_blank_name_invalid_…]
- "tests_test_exploitability_testapplytofindings_test_declared_severity_is_never_rewritten": ".test_declared_severity_is_never_rewritten()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L119 | neighbors=[Severity is the rule's judgement of the…, TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_exploitability_testapplytofindings_test_idempotent_across_repeated_application": ".test_idempotent_across_repeated_application()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L162 | neighbors=[The pipeline may enrich the same findin…, TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_fact_contract_load_corpus": "_load_corpus()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L27 | neighbors=[test_fact_contract.py, _ingest_corpus(), test_corpus_is_present_and_nonempty(), test_every_rule_input_is_emitted_by_its…, test_report_unconsumed_evidence()]
- "tests_test_finding_section": "test_finding_section.py" | kind=code-symbol | source=probe/tests/test_finding_section.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, findings.py, TestFindingSection, TestScannerRegistry, test_finding_section.py — the scanner-m…]
- "tests_test_ftp_scanner_testftpfindings": "TestFTPFindings" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L53 | neighbors=[test_ftp_scanner.py, ._fact(), .test_anon_denied_is_silent(), .test_anon_login_only_is_medium(), .test_anon_read_is_high()]
- "tests_test_ftp_scanner_testftpscanner": "TestFTPScanner" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L28 | neighbors=[test_ftp_scanner.py, ._sc(), .test_anon_login_and_read_open(), .test_ftp_present_anon_denied_open_but_…, .test_no_ftp_filtered()]
- "tests_test_host_discovery_udp_nbstat_reply": "_nbstat_reply()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L24 | neighbors=[test_host_discovery_udp.py, Build a NetBIOS node-status response (R…, test_netbios_reply_proves_life_and_name…, .test_msbrowse_control_chars_dropped(), .test_names_hostname_domain_mac()]
- "tests_test_host_discovery_udp_responder": "_Responder" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L90 | neighbors=[test_host_discovery_udp.py, .connection_made(), .datagram_received(), .__init__(), _udp_server()]
- "tests_test_host_discovery_udp_testfusewithudp": "TestFuseWithUdp" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L59 | neighbors=[test_host_discovery_udp.py, .test_icmp_unreachable_alone(), .test_no_signals_unchanged(), .test_tcp_plus_udp_corroborate(), .test_udp_reply_alone_is_confirmed_aliv…]
- "tests_test_host_health_testsafetyproperty": "TestSafetyProperty" | kind=code-symbol | source=probe/tests/test_host_health.py:L130 | neighbors=[test_host_health.py, .test_healthy_host_produces_no_facts_at…, .test_offline_fact_marks_the_scan_incom…, .test_offline_host_stops_accumulating_o…, .test_one_offline_host_does_not_implica…]
- "tests_test_host_health_testudpnoreplyisnotcontact": "TestUdpNoReplyIsNotContact" | kind=code-symbol | source=probe/tests/test_host_health.py:L185 | neighbors=[test_host_health.py, Regression: "open|filtered" is the UDP …, .test_a_real_open_port_still_counts_as_…, .test_mixed_udp_silence_and_a_real_open…, .test_udp_no_reply_counts_as_silence()]
- "tests_test_hw_bind_testcheckhwbind": "TestCheckHwBind" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L21 | neighbors=[test_hw_bind.py, .test_passes_when_match(), .test_raises_on_mismatch(), .test_raises_when_unset_and_enforced(), .test_skips_when_unset_and_dev_mode()]
- "tests_test_integration_testfulljoblifecycle": "TestFullJobLifecycle" | kind=code-symbol | source=probe/tests/test_integration.py:L311 | neighbors=[test_integration.py, End-to-end: identity → register → job →…, .test_complete_flow_with_encrypted_scop…, .test_job_ot_passive_profile(), .test_job_rejected_all_targets_out_of_s…]
- "tests_test_integration_testidentityandencryption": "TestIdentityAndEncryption" | kind=code-symbol | source=probe/tests/test_integration.py:L64 | neighbors=[test_integration.py, Phase 4: identity generation + scope en…, .test_different_key_cannot_decrypt(), .test_full_identity_lifecycle(), .test_scope_encryption_roundtrip()]
- "tests_test_integration_testresultspoolwithretry": "TestResultSpoolWithRetry" | kind=code-symbol | source=probe/tests/test_integration.py:L197 | neighbors=[test_integration.py, Phase 1: result spool with upload retry., .test_spool_persists_and_flushes(), .test_submit_exhausts_retries(), .test_submit_retries_on_failure()]
- "tests_test_integrations_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L17 | neighbors=[test_integrations.py, .test_list_masks_secret(), .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]
- "tests_test_ipmi_scanner_testwireformat": "TestWireFormat" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L23 | neighbors=[test_ipmi_scanner.py, .test_open_session_request_offers_ciphe…, .test_parse_nonzero_status_is_safe(), .test_parse_rejects_non_response(), .test_parse_status_zero_is_cipher_zero()]
- "tests_test_ipv6_discovery": "test_ipv6_discovery.py" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, ipv6_discovery.py, TestDiscoverFiltering, TestParsers, test_ipv6_discovery.py — FIX 3: IPv6 ne…]
- "tests_test_ipv6_wiring_run": "_run()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L96 | neighbors=[test_ipv6_wiring.py, test_discovery_failure_does_not_abort_t…, test_in_scope_neighbour_is_added_and_sc…, test_out_of_scope_neighbour_is_reported…, test_the_fact_records_both_sides()]
- "tests_test_job_attempt_service": "test_job_attempt_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, test_claim_creates_immutable_attempt_wi…, test_current_fence_renews_attempt_and_l…, test_lost_claim_does_not_create_attempt…, test_stale_fence_cannot_renew_attempt()]
- "tests_test_job_cancel_test_terminal_jobs_cannot_be_cancelled": "test_terminal_jobs_cannot_be_cancelled()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L156 | neighbors=[test_job_cancel.py, _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_testqueuelimit": "TestQueueLimit" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L182 | neighbors=[test_job_cancel.py, .test_fourth_queued_job_is_refused(), .test_limit_is_three(), .test_pending_count_helper_counts(), .test_third_queued_job_is_still_accepte…]
- "tests_test_job_cancel_testqueuelimit_test_fourth_queued_job_is_refused": ".test_fourth_queued_job_is_refused()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L192 | neighbors=[TestQueueLimit, _count(), _db(), _one(), _user()]
- "tests_test_loaders_testloadkeverrors": "TestLoadKevErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L124 | neighbors=[test_loaders.py, .setup_method(), .test_malformed_kev_json_raises(), .test_missing_kev_file_raises(), .test_valid_kev_loads()]
- "tests_test_main_scripts_correlation_get": "_get()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L21 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_legacy_windows_surface_smbv1_plus_…, test_ntlm_relay_is_high_when_smbv1_also…, test_ntlm_relay_is_medium_when_only_sig…]
- "tests_test_main_scripts_correlation_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L17 | neighbors=[test_main_scripts_correlation.py, test_correlation_does_not_cross_hosts(), test_no_legacy_surface_with_only_smbv1(), test_no_relay_finding_when_signing_requ…, test_single_cleartext_service_does_not_…]
- "tests_test_main_scripts_coverage_summary": "_summary()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L35 | neighbors=[test_main_scripts_coverage.py, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state(), .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_errno_oserr": "_oserr()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L17 | neighbors=[test_main_scripts_errno.py, test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_scanner_side_errors_are_error_not_…, test_unknown_errno_is_self_identifying_…]
- "tests_test_main_scripts_hardening_testosconfidence": "TestOsConfidence" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L73 | neighbors=[test_main_scripts_hardening.py, .test_linux_ttl_only_capped(), .test_no_signal_is_unknown(), .test_ttl_only_is_not_absolute(), .test_two_signals_beat_one()]
- "tests_test_main_scripts_rdp_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L137 | neighbors=[test_main_scripts_rdp.py, test_confirmed_rdp_wins_dedup_over_port…, test_confirmed_rdp_with_nla_has_no_nla_…, test_confirmed_rdp_without_nla_is_high_…, test_nla_required_rdp_is_low_severity_n…]
- "tests_test_msrpc_scanner_testdynamicports": "TestDynamicPorts" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L27 | neighbors=[test_msrpc_scanner.py, EPM bindings carry the dynamic RPC port…, .test_extract_tcp_and_dynamic(), .test_out_of_range_port_dropped(), .test_summarize_surfaces_dynamic_ports()]
- "tests_test_msrpc_scanner_testmsrpcscanner": "TestMSRPCScanner" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L56 | neighbors=[test_msrpc_scanner.py, ._sc(), .test_impacket_missing_is_error(), .test_no_msrpc_filtered(), .test_open()]
- "tests_test_network_va_accuracy_va_scan": "va_scan()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L78 | neighbors=[test_network_va_accuracy.py, One real network_va against loopback wi…, _Listener, .start(), .stop()]
- "tests_test_new_scanners_testversionchange": "TestVersionChange" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L361 | neighbors=[test_new_scanners.py, .test_different_versions(), .test_empty_old_version(), .test_same_version(), .test_whitespace_normalised()]
- "tests_test_nfs_scanner_mount_export_reply": "_mount_export_reply()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L30 | neighbors=[test_nfs_scanner.py, _xstr(), .test_main_scripts(), .test_mount_export_parse_and_world_flag…, .test_rpc_reply_header_stripping()]
- "tests_test_online_testclionlineflag": "TestCliOnlineFlag" | kind=code-symbol | source=probe/tests/test_online.py:L180 | neighbors=[test_online.py, ._db(), ._facts(), .test_no_online_flag_skips_enrichment(), .test_online_flag_invokes_enrichment()]
- "tests_test_online_testlookupnvd": "TestLookupNvd" | kind=code-symbol | source=probe/tests/test_online.py:L77 | neighbors=[test_online.py, .test_empty_result_is_none(), .test_garbage_json_is_fail_open(), .test_network_error_is_fail_open(), .test_parses_score_severity_refs()]
- "tests_test_online_testlookupvulners": "TestLookupVulners" | kind=code-symbol | source=probe/tests/test_online.py:L100 | neighbors=[test_online.py, .test_error_is_none(), .test_exploit_present_is_true(), .test_no_exploit_is_false(), .test_no_key_returns_none()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-062.json

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
