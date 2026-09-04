# Node Description Batch 82 of 330

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

- "tests_test_host_discovery_udp_testparsenbstat": "TestParseNbstat" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L37 | neighbors=[test_host_discovery_udp.py, .test_msbrowse_control_chars_dropped(), .test_names_hostname_domain_mac(), .test_not_a_response()]
- "tests_test_host_health_testoperatorvisibility": "TestOperatorVisibility" | kind=code-symbol | source=probe/tests/test_host_health.py:L280 | neighbors=[test_host_health.py, An offline host must reach the operator…, .test_flaky_note_is_not_an_error(), .test_offline_fact_carries_an_error_so_…]
- "tests_test_host_health_testoperatorvisibility_test_flaky_note_is_not_an_error": ".test_flaky_note_is_not_an_error()" | kind=code-symbol | source=probe/tests/test_host_health.py:L294 | neighbors=[A host that is merely filtered is not a…, TestOperatorVisibility, _monitor(), _r()]
- "tests_test_host_health_testsafetyproperty_test_offline_fact_marks_the_scan_incomplete_and_names_what_was_skipped": ".test_offline_fact_marks_the_scan_incomplete_and_names_what_was_skipped()" | kind=code-symbol | source=probe/tests/test_host_health.py:L131 | neighbors=[The whole point: 'we stopped early' mus…, TestSafetyProperty, _monitor(), _r()]
- "tests_test_host_health_teststrikeaccounting_test_strikes_must_be_consecutive": ".test_strikes_must_be_consecutive()" | kind=code-symbol | source=probe/tests/test_host_health.py:L66 | neighbors=[A healthy host with many inapplicable b…, TestStrikeAccounting, _monitor(), _r()]
- "tests_test_host_health_testverdict_test_firewalled_host_that_still_answers_is_flaky_not_offline": ".test_firewalled_host_that_still_answers_is_flaky_not_offline()" | kind=code-symbol | source=probe/tests/test_host_health.py:L84 | neighbors=[The headline false positive: silence fr…, TestVerdict, _monitor(), _r()]
- "tests_test_host_health_testverdict_test_flaky_host_can_be_suspected_again_later": ".test_flaky_host_can_be_suspected_again_later()" | kind=code-symbol | source=probe/tests/test_host_health.py:L121 | neighbors=[One false alarm must not disable the ch…, TestVerdict, _monitor(), _r()]
- "tests_test_integration_teststartupgauntlet": "TestStartupGauntlet" | kind=code-symbol | source=probe/tests/test_integration.py:L431 | neighbors=[test_integration.py, Phase 5: startup gauntlet checks., .test_gauntlet_hw_bind_blocks(), .test_gauntlet_skips_in_dev_mode()]
- "tests_test_integration_testtaskrunnerwithencryptedscope": "TestTaskRunnerWithEncryptedScope" | kind=code-symbol | source=probe/tests/test_integration.py:L100 | neighbors=[test_integration.py, Phase 4 + Phase 1: TaskRunner receives …, .test_decrypts_encrypted_scope_from_job…, .test_falls_back_when_decryption_fails()]
- "tests_test_integration_testtransportwithidentity": "TestTransportWithIdentity" | kind=code-symbol | source=probe/tests/test_integration.py:L238 | neighbors=[test_integration.py, Phase 4 + Phase 1: Transport sends publ…, .test_register_sends_public_key(), .test_register_without_public_key()]
- "tests_test_integrations_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L21 | neighbors=[test_integrations.py, .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]
- "tests_test_integrations_testputintegration": "TestPutIntegration" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L31 | neighbors=[test_integrations.py, .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]
- "tests_test_ipmi_scanner_testipmifindings": "TestIPMIFindings" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L62 | neighbors=[test_ipmi_scanner.py, ._fact(), .test_cipher_zero_is_critical(), .test_reachable_bmc_is_low()]
- "tests_test_ipmi_scanner_testipmiscanner": "TestIPMIScanner" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L44 | neighbors=[test_ipmi_scanner.py, ._sc(), .test_cipher_zero_open(), .test_no_ipmi_filtered()]
- "tests_test_ipv6_discovery_testparsers": "TestParsers" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L13 | neighbors=[test_ipv6_discovery.py, .test_ignores_non_ipv6_lines(), .test_parse_ip_neigh_linux(), .test_parse_ndp_macos()]
- "tests_test_ipv6_wiring_test_out_of_scope_neighbour_is_reported_but_never_probed": "test_out_of_scope_neighbour_is_reported_but_never_probed()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L110 | neighbors=[test_ipv6_wiring.py, The core restraint: discovery must not …, _run(), _wire()]
- "tests_test_job_cancel_test_job_outside_the_tenant_is_not_found": "test_job_outside_the_tenant_is_not_found()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L166 | neighbors=[test_job_cancel.py, _db(), _one(), _user()]
- "tests_test_loaders_valid_snapshot": "_valid_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L28 | neighbors=[test_loaders.py, .test_content_hash_mismatch_raises_valu…, .test_hash_mismatch_message_truncates_h…, _write_snapshot()]
- "tests_test_main_scripts_coverage_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L23 | neighbors=[test_main_scripts_coverage.py, _mk_scanner(), .test_default_ports_are_nmap_top100_not…, .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout": "TestDefaultsAndAdaptiveTimeout" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L186 | neighbors=[test_main_scripts_coverage.py, .test_adaptive_estimator_is_shared_and_…, .test_default_ports_are_nmap_top100_not…, .test_fixed_timeout_flag_disables_the_e…]
- "tests_test_main_scripts_datastore_probe_svc": "_svc()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L15 | neighbors=[test_main_scripts_datastore_probe.py, test_elasticsearch_and_couchdb_win_over…, test_memcached_version_and_stat_identif…, test_redis_info_and_noauth_identify_as_…]
- "tests_test_main_scripts_hardening_make_smb2_error": "make_smb2_error()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L122 | neighbors=[test_main_scripts_hardening.py, _smb2_header(), STATUS_INVALID_PARAMETER error response…, .test_error_response_not_trusted()]
- "tests_test_main_scripts_hardening_make_smb2_success": "make_smb2_success()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L113 | neighbors=[test_main_scripts_hardening.py, _smb2_header(), .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…]
- "tests_test_main_scripts_hardening_smb2_header": "_smb2_header()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L100 | neighbors=[test_main_scripts_hardening.py, make_smb2_error(), make_smb2_success(), A 64-byte SMB2 header. Caller prepends …]
- "tests_test_main_scripts_hardening_testudpstatemodel": "TestUdpStateModel" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L42 | neighbors=[test_main_scripts_hardening.py, ._scanner(), .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_hardening_testudpstatemodel_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L43 | neighbors=[TestUdpStateModel, _scope(), .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_unauth_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L51 | neighbors=[test_main_scripts_unauth.py, test_protected_redis_raises_no_unauth_f…, test_unauth_elasticsearch_is_high(), test_unauth_redis_is_critical_and_rce_f…]
- "tests_test_msrpc_scanner_testmsrpcfindings": "TestMSRPCFindings" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L81 | neighbors=[test_msrpc_scanner.py, ._fact(), .test_endpoints_low(), .test_zero_endpoints_silent()]
- "tests_test_msrpc_scanner_testmsrpcscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L57 | neighbors=[TestMSRPCScanner, .test_impacket_missing_is_error(), .test_no_msrpc_filtered(), .test_open()]
- "tests_test_nessus_scanner_rationale_1": "Unit tests for NessusScanner — all HTTP calls mocked." | kind=entity | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[test_nessus_scanner.py, FindingSeverity, FindingStatus, NessusScanner]
- "tests_test_nfs_scanner_testnfsfindings": "TestNFSFindings" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L117 | neighbors=[test_nfs_scanner.py, ._fact(), .test_restricted_exports_no_high_findin…, .test_world_readable_and_portmapper()]
- "tests_test_nfs_scanner_testnfsscanner": "TestNFSScanner" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L94 | neighbors=[test_nfs_scanner.py, ._sc(), .test_no_rpc_is_filtered(), .test_world_readable_export_open()]
- "tests_test_nmap_xml_safety_testnmapentityguard": "TestNmapEntityGuard" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L27 | neighbors=[test_nmap_xml_safety.py, .test_entity_declaration_is_refused(), .test_entity_guard_is_case_insensitive(), .test_legitimate_doctype_output_still_p…]
- "tests_test_notifications": "test_notifications.py" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, TestDeliver, TestNotifyTenant, test_notifications.py — integration del…]
- "tests_test_notifications_testdeliver": "TestDeliver" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L13 | neighbors=[test_notifications.py, .test_dispatches_to_the_kind(), .test_sender_error_is_swallowed(), .test_unknown_kind_returns_false()]
- "tests_test_nuclei_scanner_finding_line": "_finding_line()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L12 | neighbors=[test_nuclei_scanner.py, test_nonzero_exit_retains_and_marks_par…, test_run_scan_streams_jsonl_and_separat…, test_timeout_retains_findings_emitted_b…]
- "tests_test_online_get_raising": "_get_raising()" | kind=code-symbol | source=probe/tests/test_online.py:L58 | neighbors=[test_online.py, .test_fail_open_leaves_offline_result_u…, .test_network_error_is_fail_open(), .test_error_is_none()]
- "tests_test_online_nvd_bytes": "_nvd_bytes()" | kind=code-symbol | source=probe/tests/test_online.py:L25 | neighbors=[test_online.py, .test_gap_fill_sets_cvss_and_recomputes…, .test_online_all_cross_checks_and_annot…, .test_parses_score_severity_refs()]
- "tests_test_online_testenrichfindings_test_gap_fill_sets_cvss_and_recomputes_risk": ".test_gap_fill_sets_cvss_and_recomputes_risk()" | kind=code-symbol | source=probe/tests/test_online.py:L118 | neighbors=[TestEnrichFindings, _finding(), _get_returning(), _nvd_bytes()]
- "tests_test_online_testenrichfindings_test_online_all_cross_checks_and_annotates_mismatch": ".test_online_all_cross_checks_and_annotates_mismatch()" | kind=code-symbol | source=probe/tests/test_online.py:L139 | neighbors=[TestEnrichFindings, _finding(), _get_returning(), _nvd_bytes()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-081.json

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
