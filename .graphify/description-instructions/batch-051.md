# Node Description Batch 52 of 336

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

- "tests_test_resolution_coverage": "test_resolution_coverage.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L1 | neighbors=[9a36729 feat(resolution): coverage buil…, test_coverage_counts_only_completed_sca…, test_coverage_empty_when_no_scanner_run…, test_host_of_strips_single_port(), test_skipped_scanner_is_not_reported_as…, test_skipped_scanner_still_proves_nothi…]
- "tests_test_resolution_decision": "test_resolution_decision.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L1 | neighbors=[cbf5d6c feat(resolution): pure decision…, test_db_change_blocks_resolution(), test_high_needs_two_covered_clean_runs(), test_medium_resolves_on_first_covered_c…, test_not_covered_is_skipped_and_counter…, test_threshold_is_stricter_for_critical…]
- "tests_test_result_archive_testarchiveidentity": "TestArchiveIdentity" | kind=code-symbol | source=probe/tests/test_result_archive.py:L66 | neighbors=[test_result_archive.py, .test_archived_json_equals_the_submitte…, .test_failure_envelopes_are_archived_to…, .test_filename_is_result_plus_timestamp…, .test_no_partial_files_are_left_behind(), .test_two_jobs_in_the_same_second_do_no…]
- "tests_test_router_signals_testtlsprobednegative": "TestTlsProbedNegative" | kind=code-symbol | source=probe/tests/test_router_signals.py:L107 | neighbors=[test_router_signals.py, service_banner now ATTEMPTS a TLS hands…, .test_absence_guess_kept_for_facts_with…, .test_binary_protocol_ports_route_nowhe…, .test_probed_and_failed_is_not_tls(), .test_probed_and_succeeded_still_routes…]
- "tests_test_rsync_scanner_testhandshake": "TestHandshake" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L50 | neighbors=[test_rsync_scanner.py, Protocol >= 32 daemons append their dig…, .test_echo_stops_at_the_first_line(), .test_greeting_is_echoed_verbatim_inclu…, .test_legacy_greeting_without_digest_li…, .test_non_rsync_greeting_returns_none_a…]
- "tests_test_scanner_congestion_testreprobecleanuppass_summary": "._summary()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L352 | neighbors=[TestReprobeCleanupPass, .test_completeness_holds_after_correcti…, .test_disabled_reprobe_leaves_false_fil…, .test_genuinely_filtered_ports_stay_fil…, .test_no_ambiguous_ports_means_no_clean…, .test_recovers_ports_the_fast_sweep_cal…]
- "tests_test_scanner_parity": "test_scanner_parity.py" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _py_files(), test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_…, test_scanner_module_matches_main_script…, test_scanner_parity.py — the no-drift g…]
- "tests_test_scope_crypt": "test_scope_crypt.py" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, scope_crypt.py, TestEncryptDecryptRoundtrip, TestKeyGeneration, Tests for agent/scope_crypt.py, 2885afa Add comprehensive probe testing…]
- "tests_test_scope_targets_testtargetswithinscope": "TestTargetsWithinScope" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L23 | neighbors=[test_scope_targets.py, .test_cidr_subset_in_scope(), .test_no_targets_returns_whole_scope(), .test_range_expands_to_covered_networks…, .test_single_ip_in_scope(), .test_string_target_is_accepted()]
- "tests_test_scope_validator_testfetchengagementscope": "TestFetchEngagementScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L170 | neighbors=[test_scope_validator.py, .test_http_get_raises(), .test_http_get_returns_incomplete(), .test_http_get_returns_none(), .test_returns_excludes(), .test_returns_scope_from_http_get()]
- "tests_test_seed_admin_testvalidateenv": "TestValidateEnv" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L38 | neighbors=[test_seed_admin.py, .test_all_known_weak_passwords_blocked_…, .test_allows_weak_password_in_developme…, .test_raises_on_weak_password_in_produc…, .test_raises_when_email_missing(), .test_returns_force_reset_true()]
- "tests_test_service_banner_ident_scanner": "_scanner()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L138 | neighbors=[test_service_banner_ident.py, test_matched_rung_banner_is_the_one_rep…, test_prefers_decrypted_tls_reply_over_p…, .test_client_first_ports_skip_null_rung…, .test_greet_timeout_tracks_operator_tim…, .test_no_tls_flag_drops_rung()]
- "tests_test_service_banner_ident_testparsehttphead": "TestParseHttpHead" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L108 | neighbors=[test_service_banner_ident.py, .test_bare_lf_headers(), .test_basic_auth_challenge(), .test_non_http_is_empty(), .test_rtsp_is_http_shaped(), .test_status_server_title()]
- "tests_test_service_match_testotherservices": "TestOtherServices" | kind=code-symbol | source=probe/tests/test_service_match.py:L58 | neighbors=[test_service_match.py, .test_mariadb_handshake(), .test_redis_info(), .test_redis_noauth(), .test_smtp_postfix(), .test_vsftpd()]
- "tests_test_smb_ldap_scanners_testsmbenumscanner": "TestSMBEnumScanner" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L62 | neighbors=[test_smb_ldap_scanners.py, ._sc(), .test_impacket_missing_is_error(), .test_no_smb_is_filtered(), .test_null_refused_is_open_but_secure(), .test_null_session_open_with_shares_and…]
- "tests_test_smb_ldap_scanners_testsmbldapfindings": "TestSMBLDAPFindings" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L205 | neighbors=[test_smb_ldap_scanners.py, .test_ldap_anon_bind_and_search(), .test_ldap_anon_bind_only_no_search(), .test_ldap_secure_is_silent(), .test_smb_null_session_and_users(), .test_smb_secure_is_silent()]
- "tests_test_ssh_scanner_testfulldbcoverage": "TestFullDBCoverage" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L242 | neighbors=[test_ssh_scanner.py, ._eval(), .test_3des_ctr_cipher_is_failure(), .test_gss_kex_offered_by_server_is_fail…, .test_hmac_ripemd160_is_failure(), .test_rijndael_cbc_cipher_is_failure()]
- "tests_test_ssh_scanner_testsshstatustaxonomy": "TestSSHStatusTaxonomy" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L339 | neighbors=[test_ssh_scanner.py, ._scanner(), .test_confirmed_ssh_open_with_parsed_ba…, .test_connect_failure_is_filtered(), .test_open_but_no_banner_is_open_not_ss…, .test_open_non_ssh_is_open_not_filtered…]
- "tests_test_stage2_reconcile_cm": "_CM" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L168 | neighbors=[test_stage2_reconcile.py, .__aenter__(), .__aexit__(), .__init__(), test_reap_stale_runs_marks_running_as_f…, test_write_heartbeat_upserts()]
- "tests_test_stage2_reconcile_test_multi_agent_all_covered_is_complete": "test_multi_agent_all_covered_is_complete()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L113 | neighbors=[test_stage2_reconcile.py, _job(), _rows(), _run(), _scalars(), _user()]
- "tests_test_stage2_reconcile_test_multi_agent_latest_done_but_earlier_uncovered_is_detecting": "test_multi_agent_latest_done_but_earlier_uncovered_is_detecting()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L90 | neighbors=[test_stage2_reconcile.py, _job(), _rows(), _run(), _scalars(), _user()]
- "tests_test_stage2_reconcile_test_stale_heartbeat_with_pending_is_stalled_before_overdue": "test_stale_heartbeat_with_pending_is_stalled_before_overdue()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L229 | neighbors=[test_stage2_reconcile.py, _hb(), _job(), _rows(), _scalars(), _user()]
- "tests_test_syn_scanner_testoptionparsing": "TestOptionParsing" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L304 | neighbors=[test_syn_scanner.py, .test_malformed_options_never_raise(), .test_mss_absent_returns_none(), .test_mss_after_nop_padding(), .test_mss_extracted(), .test_mss_skips_other_options()]
- "tests_test_tarpit_testassesstarpit": "TestAssessTarpit" | kind=code-symbol | source=probe/tests/test_tarpit.py:L17 | neighbors=[test_tarpit.py, .test_boundary_floor_and_ratio_trip_exa…, .test_busy_real_host_is_not_flagged(), .test_nearly_all_open_large_scan_is_fla…, .test_tiny_all_open_scan_is_below_the_f…, .test_zero_attempted_is_safe()]
- "tests_test_tier1_correlations_run": "_run()" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L13 | neighbors=[test_tier1_correlations.py, test_anon_data_exposure_cluster(), test_mgmt_plane_exposed_on_cipher_zero_…, test_mgmt_plane_needs_two_when_no_ciphe…, test_single_anon_finding_does_not_corre…, test_user_enum_plus_weak_auth()]
- "tests_test_tls_fingerprint": "test_tls_fingerprint.py" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello, test_tls_fingerprint.py — Tier 2.3: act…]
- "tests_test_tls_posture": "test_tls_posture.py" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, tls_scanner.py, _modern(), TestClassifyCipher, TestGradeTlsPosture, test_tls_posture.py — Tier 2.4: cipher-…]
- "tests_test_two_tree_parity": "test_two_tree_parity.py" | kind=code-symbol | source=probe/tests/test_two_tree_parity.py:L1 | neighbors=[6e2818f Add support for additional serv…, _mirrored_py_files(), test_mirrored_set_is_nonempty(), test_no_unmirrored_scanner_files(), test_scanner_and_main_scripts_are_byte_…, test_two_tree_parity.py — the guard the…]
- "tests_test_validation_endpoints_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L50 | neighbors=[test_validation_endpoints.py, test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_deri…, test_reject_marks_rejected()]
- "tests_test_validation_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_validation.py:L110 | neighbors=[test_validation.py, .__init__(), .request(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_gate": "test_validation_gate.py" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, _ids(), TestNoFabricatedIcmpLiveness, TestRdpNlaGate, TestUdpNoReplyRejected, test_validation_gate.py — the "validati…]
- "tests_test_validation_gate_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L27 | neighbors=[test_validation_gate.py, .test_icmp_unavailable_os_observation_r…, .test_nla_enforced_suppresses_no_nla_fi…, .test_positive_control_nla_off_is_flagg…, .test_open_filtered_amplifier_not_flagg…, .test_positive_control_answered_amplifi…]
- "tests_test_validation_ingest_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L23 | neighbors=[test_validation_ingest.py, test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…, test_inconclusive_leaves_finding_unchan…, test_ingest_confirmed_updates_request_a…]
- "tests_test_verification_core": "test_verification_core.py" | kind=code-symbol | source=manager/backend/tests/test_verification_core.py:L1 | neighbors=[caf1e5d feat(verification): determinist…, test_authoritative_is_confirmed(), test_high_confidence_inferred_is_corrob…, test_kev_suspected_finding_needs_review…, test_low_confidence_inferred_is_inferre…, test_missing_confidence_defaults_to_inf…]
- "tests_test_version_compare": "test_version_compare.py" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, test_dpkg_compare_public_api(), test_pure_python_matches_known_pairs(), test_pure_python_matches_real_dpkg_bina…, Cross-validates the pure-Python Debian …, 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_wire_identity_testchoosesourceport": "TestChooseSourcePort" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L38 | neighbors=[test_wire_identity.py, Evasion: a fixed source port (e.g. 53/8…, .test_boundary_ports_are_valid(), .test_none_gives_random_ephemeral(), .test_out_of_range_falls_back_to_random…, .test_uses_configured_valid_port()]
- "tools_installer_managedpath": "managedPath()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L48 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), isManaged(), removeTool()]
- "users_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/users/route.ts:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, backend.ts, backend(), with-backend.ts, withBackend(), GET]
- "versions_0001_initial": "0001_initial.py" | kind=code-symbol | source=manager/backend/alembic/versions/0001_initial.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Initial schema — all tables  Revision I…, 298a9d4 trim frontend to 7 core pages; …]
- "vuln_nuclei_nucleiscanner_parse_output": ".parse_output()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L381 | neighbors=[NucleiScanner, ._map_finding(), Parse nuclei JSONL output → list of Fin…, Parse nuclei JSONL output → list of Fin…, .run_scan(), Parse nuclei JSONL output → list of Fin…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-051.json

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
