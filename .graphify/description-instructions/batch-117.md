# Node Description Batch 118 of 330

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

- "tests_test_scanner_parity_py_files": "_py_files()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L25 | neighbors=[test_scanner_parity.py, test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_…]
- "tests_test_scanner_parity_test_no_extra_scanner_files": "test_no_extra_scanner_files()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L38 | neighbors=[test_scanner_parity.py, scanner/ must not carry modules that ma…, _py_files()]
- "tests_test_scanner_parity_test_scanner_is_superset_of_no_missing_files": "test_scanner_is_superset_of_no_missing_files()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L29 | neighbors=[test_scanner_parity.py, Every scanner module authored in main_s…, _py_files()]
- "tests_test_scope_crypt_testkeygeneration": "TestKeyGeneration" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L15 | neighbors=[test_scope_crypt.py, .test_generates_32_byte_keys(), .test_generates_different_keys_each_cal…]
- "tests_test_scope_targets_testipversionsafety": "TestIpVersionSafety" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L88 | neighbors=[test_scope_targets.py, .test_v6_in_v6_scope(), .test_v6_target_against_v4_scope_is_rej…]
- "tests_test_seed_admin_testdriftdetection": "TestDriftDetection" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L308 | neighbors=[test_seed_admin.py, .test_warns_on_multiple_admins(), .test_warns_on_stale_admin_emails()]
- "tests_test_seed_admin_testpasswordrotation": "TestPasswordRotation" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L189 | neighbors=[test_seed_admin.py, .test_rotation_raises_on_hash_verify_fa…, .test_rotation_updates_hash_and_verifie…]
- "tests_test_service_banner_ident_test_https_on_arbitrary_port_identifies_and_flags_tls": "test_https_on_arbitrary_port_identifies_and_flags_tls()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L273 | neighbors=[test_service_banner_ident.py, The HTTPS-on-9443 case: plaintext rungs…, _self_signed()]
- "tests_test_service_banner_ident_test_matched_rung_banner_is_the_one_reported": "test_matched_rung_banner_is_the_one_reported()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L216 | neighbors=[test_service_banner_ident.py, The banner and the match must come from…, _scanner()]
- "tests_test_service_match_testnomatch": "TestNoMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L87 | neighbors=[test_service_match.py, .test_empty_returns_none(), .test_unrecognized_returns_none()]
- "tests_test_service_match_testprobeladder": "TestProbeLadder" | kind=code-symbol | source=probe/tests/test_service_match.py:L95 | neighbors=[test_service_match.py, .test_ladder_has_http_and_generic(), .test_ladder_starts_with_null_probe()]
- "tests_test_service_posture_rules_asset": "_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L34 | neighbors=[test_service_posture_rules.py, test_experimental_scanner_findings_are_…, .test_no_longer_reports_schema_drift()]
- "tests_test_service_posture_rules_test_rule_fires_on_captured_shape": "test_rule_fires_on_captured_shape()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L68 | neighbors=[test_service_posture_rules.py, _corpus(), _fire()]
- "tests_test_service_posture_rules_testnegatives_test_vnc_weak_suppressed_when_no_auth_present": ".test_vnc_weak_suppressed_when_no_auth_present()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L134 | neighbors=[no-auth is strictly worse and is report…, TestNegatives, _fire()]
- "tests_test_service_posture_rules_testrdpnotls_test_fires_on_ssl_not_allowed": ".test_fires_on_ssl_not_allowed()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L199 | neighbors=[TestRdpNoTls, _corpus(), _fire()]
- "tests_test_service_posture_rules_testrdpnotls_test_ignores_uninterpreted_failure_codes": ".test_ignores_uninterpreted_failure_codes()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L203 | neighbors=[Only codes carrying posture meaning fir…, TestRdpNoTls, _fire()]
- "tests_test_sla_policy_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L16 | neighbors=[test_sla_policy.py, .test_custom_window_relaxes_state(), .test_default_window_breaches()]
- "tests_test_sla_policy_row": "_row()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L46 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_resolve_windows_fallback_and_cust…]
- "tests_test_sla_policy_testpolicyawarecompute": "TestPolicyAwareCompute" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L23 | neighbors=[test_sla_policy.py, .test_custom_window_relaxes_state(), .test_default_window_breaches()]
- "tests_test_sla_policy_testslapolicyroutes_test_get_env_defaults_when_no_row": ".test_get_env_defaults_when_no_row()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L53 | neighbors=[TestSlaPolicyRoutes, _db(), _operator()]
- "tests_test_sla_policy_testslapolicyroutes_test_put_creates_when_absent": ".test_put_creates_when_absent()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L63 | neighbors=[TestSlaPolicyRoutes, _db(), _operator()]
- "tests_test_sla_policy_testslapolicyroutes_test_resolve_windows_fallback_and_custom": ".test_resolve_windows_fallback_and_custom()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L71 | neighbors=[TestSlaPolicyRoutes, _db(), _row()]
- "tests_test_smb_ldap_scanners_testmainscriptsparity": "TestMainScriptsParity" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L251 | neighbors=[test_smb_ldap_scanners.py, .test_main_scripts_findings_derive_smb_…, .test_scanners_import_in_both_trees()]
- "tests_test_smb_ldap_scanners_testmergeusers": "TestMergeUsers" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L46 | neighbors=[test_smb_ldap_scanners.py, .test_decode_strips_nul(), .test_dedup_samr_wins()]
- "tests_test_smb_ntlm_build_testbuildmap": "TestBuildMap" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L133 | neighbors=[test_smb_ntlm_build.py, .test_client_server_shared_build_surfac…, .test_confidence_high_on_exact_match()]
- "tests_test_smb_scanner_smb2_error_response": "_smb2_error_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L14 | neighbors=[test_smb_scanner.py, An SMB2 ERROR response (e.g. STATUS_INV…, test_error_response_not_parsed_as_signi…]
- "tests_test_smb_scanner_test_error_response_not_parsed_as_signing": "test_error_response_not_parsed_as_signing()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L50 | neighbors=[test_smb_scanner.py, The confirmed bug: an SMB2 error respon…, _smb2_error_response()]
- "tests_test_smb_scanner_test_signing_supported_field_present": "test_signing_supported_field_present()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L71 | neighbors=[test_smb_scanner.py, Step 13: expose signing_supported (prot…, _smb2_negotiate_response()]
- "tests_test_smtp_scanner_testpurelogic": "TestPureLogic" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L17 | neighbors=[test_smtp_scanner.py, .test_parse_ehlo_capabilities(), .test_vrfy_leaks()]
- "tests_test_smtp_scanner_testsmtpscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L32 | neighbors=[TestSMTPScanner, .test_no_smtp_filtered(), .test_open()]
- "tests_test_ssh_scanner_nl": "_nl()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L29 | neighbors=[test_ssh_scanner.py, _kexinit(), Encode an SSH name-list: uint32 length …]
- "tests_test_ssh_scanner_testmainscriptsparity": "TestMainScriptsParity" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L315 | neighbors=[test_ssh_scanner.py, .test_main_scripts_scanner_and_findings…, .test_main_scripts_vendored_db_matches_…]
- "tests_test_ssh_scanner_testterrapin": "TestTerrapin" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L144 | neighbors=[test_ssh_scanner.py, .test_chacha20_without_strict_kex_is_vu…, .test_strict_kex_present_is_not_vulnera…]
- "tests_test_stage2_reconcile_hb": "_hb()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L206 | neighbors=[test_stage2_reconcile.py, test_fresh_heartbeat_reports_worker_ali…, test_stale_heartbeat_with_pending_is_st…]
- "tests_test_syn_scanner_testadaptivetimeouttoggle": "TestAdaptiveTimeoutToggle" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L429 | neighbors=[test_syn_scanner.py, .test_adaptive_on_by_default(), .test_can_disable()]
- "tests_test_syn_scanner_testparsepacketsignals": "TestParsePacketSignals" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L336 | neighbors=[test_syn_scanner.py, .test_no_options_gives_none_mss(), .test_window_ttl_mss_surfaced()]
- "tests_test_syn_scanner_testsyndefaults": "TestSynDefaults" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L288 | neighbors=[test_syn_scanner.py, .test_default_ports_are_nmap_top100(), .test_default_retries_is_two()]
- "tests_test_tarpit_testportscannertarpitflag_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L43 | neighbors=[TestPortScannerTarpitFlag, .test_all_open_host_flagged_as_tarpit(), .test_mostly_closed_host_not_flagged()]
- "tests_test_tarpit_testportscannertarpitflag_summary": "._summary()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L48 | neighbors=[TestPortScannerTarpitFlag, .test_all_open_host_flagged_as_tarpit(), .test_mostly_closed_host_not_flagged()]
- "tests_test_tarpit_testportscannertarpitflag_test_all_open_host_flagged_as_tarpit": ".test_all_open_host_flagged_as_tarpit()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L51 | neighbors=[TestPortScannerTarpitFlag, ._scanner(), ._summary()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-117.json

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
