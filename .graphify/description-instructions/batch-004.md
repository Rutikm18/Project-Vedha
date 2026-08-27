# Node Description Batch 5 of 92

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

- "main_scripts_scan_funnel_rationale_95": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=main_scripts/scan_funnel.py:L95 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, _candidate_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_97": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=main_scripts/scan_funnel.py:L97 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, _candidate_ports(), ResultWriter, ScanResult]
- "main_scripts_scan_funnel_rationale_98": "The port set worth scanning = union of every route's ports (deduped)." | kind=entity | source=main_scripts/scan_funnel.py:L98 | neighbors=[DBScanner, HostDiscoveryScanner, MCPAIScanner, _candidate_ports(), ResultWriter, ScanResult]
- "main_scripts_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=main_scripts/windows_collector.py:L236 | neighbors=[windows_collector.py, RateLimiter, ResultWriter, ScanResult, ScopeGuard, ._collect_host()]
- "scanner_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, ae7a30b feat: add Posture & Patch-Compa…, _auth_shaped_json_body(), _known_false_positive(), main(), _mcp_oauth_signal()]
- "scanner_mobile_scanner": "mobile_scanner.py" | kind=code-symbol | source=scanner/mobile_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), main(), MobileScanner]
- "scanner_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=scanner/scan_funnel.py:L109 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "tests_test_main_scripts_completeness": "test_main_scripts_completeness.py" | kind=code-symbol | source=tests/test_main_scripts_completeness.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, port_scanner.py, scanner_base.py, _metrics(), _rec(), test_duplicate_port_is_detected()]
- "tests_test_main_scripts_coverage": "test_main_scripts_coverage.py" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, port_scanner.py, scanner_base.py, _closed(), _mk_scanner()]
- "tests_test_new_scanners": "test_new_scanners.py" | kind=code-symbol | source=tests/test_new_scanners.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, snmp_scanner.py, delta_engine(), _make_scan_record(), TestDeltaEngine, TestIoTScanner]
- "tests_test_new_scanners_testdeltaengine": "TestDeltaEngine" | kind=code-symbol | source=tests/test_new_scanners.py:L380 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_probe_core_testgate5": "TestGate5" | kind=code-symbol | source=tests/test_probe_core.py:L322 | neighbors=[test_probe_core.py, .test_dynamically_routed_overrides_port…, .test_explicit_snmp_does_not_require_tc…, .test_iot_profile_no_smb(), .test_it_profile_tls_with_tls_port(), .test_mcp_ai_allowed_on_it_ai_port()]
- "tests_test_scope_validator_testvalidatetargetsinscope": "TestValidateTargetsInScope" | kind=code-symbol | source=tests/test_scope_validator.py:L14 | neighbors=[test_scope_validator.py, .test_cidr_must_be_fully_contained(), .test_empty_targets(), .test_explicit_hostname_scope_allows_ex…, .test_hostname_rejected_when_scope_is_i…, .test_invalid_cidr_ignored()]
- "tests_test_smb_scanner": "test_smb_scanner.py" | kind=code-symbol | source=tests/test_smb_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, smb_scanner.py, _smb2_error_response(), _smb2_negotiate_response(), test_error_response_not_parsed_as_signi…]
- "tests_test_task_runner_testrunnerheadless": "TestRunnerHeadless" | kind=code-symbol | source=tests/test_task_runner.py:L46 | neighbors=[test_task_runner.py, Tests that use the real engine but with…, .test_explicit_empty_targets_never_expa…, .test_rejects_empty_targets(), .test_rejects_non_object_params(), .test_rejects_non_string_target()]
- "workflow_execution": "execution.py" | kind=code-symbol | source=workflow/execution.py:L1 | neighbors=[engine.py, ae7a30b feat: add Posture & Patch-Compa…, test_passive_collector.py, test_workflow_execution.py, scanner_base.py, classify_scanner_error()]
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=agent/cli.py:L226 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()]
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=agent/cli.py:L29 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), cmd_validate(), .load()]
- "agent_scope_crypt": "scope_crypt.py" | kind=code-symbol | source=agent/scope_crypt.py:L1 | neighbors=[bytes_to_pubkey_b64(), decrypt_scope(), decrypt_scope_b64(), encrypt_scope(), encrypt_scope_b64(), generate_identity()]
- "main_scripts_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=main_scripts/delta_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, Delta, DeltaEngine, _extract_service(), _extract_version(), main()]
- "main_scripts_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=main_scripts/findings.py:L1053 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "main_scripts_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=main_scripts/findings.py:L1036 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "main_scripts_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=main_scripts/findings.py:L1013 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "main_scripts_findings_run_findings": "run_findings()" | kind=code-symbol | source=main_scripts/findings.py:L1149 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict(), Derive findings from collected facts. P…, Derive findings from collected facts. P…]
- "main_scripts_ja4s": "ja4s.py" | kind=code-symbol | source=main_scripts/ja4s.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()]
- "main_scripts_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=main_scripts/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), BaseScanner]
- "main_scripts_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, _auth_shaped_json_body(), _known_false_positive(), main(), _mcp_oauth_signal()]
- "main_scripts_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L286 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), ._icmp_timestamp(), .__init__(), .scan_target()]
- "main_scripts_passive_collector": "passive_collector.py" | kind=code-symbol | source=main_scripts/passive_collector.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _coverage(), _device_hint(), _is_readable(), _listener_error_code(), main()]
- "main_scripts_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=main_scripts/tls_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, classify_cipher(), _get_cert_der(), grade_tls_posture(), main(), _parse_cert_der()]
- "scanner_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=scanner/delta_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, Delta, DeltaEngine, _extract_service(), _extract_version(), main()]
- "scanner_findings_corr_cleartext_cluster": "_corr_cleartext_cluster()" | kind=code-symbol | source=scanner/findings.py:L1053 | neighbors=[findings.py, _by_target(), Finding, Two or more cleartext services on one h…, Two or more cleartext services on one h…, Two or more cleartext services on one h…]
- "scanner_findings_corr_legacy_windows": "_corr_legacy_windows()" | kind=code-symbol | source=scanner/findings.py:L1036 | neighbors=[findings.py, _by_target(), Finding, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…, SMBv1 (wormable) + exposed RDP (brute-f…]
- "scanner_findings_corr_ntlm_relay": "_corr_ntlm_relay()" | kind=code-symbol | source=scanner/findings.py:L1013 | neighbors=[findings.py, _by_target(), Finding, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…, SMB signing not required => a viable NT…]
- "scanner_findings_run_findings": "run_findings()" | kind=code-symbol | source=scanner/findings.py:L1149 | neighbors=[findings.py, _main(), Derive findings from collected facts. P…, _as_dict(), Derive findings from collected facts. P…, Derive findings from collected facts. P…]
- "scanner_ja4s": "ja4s.py" | kind=code-symbol | source=scanner/ja4s.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()]
- "scanner_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=scanner/nmap_wrapper.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, ae7a30b feat: add Posture & Patch-Compa…, _have_nmap(), main(), NmapExecutionError, _parse_nmap_xml()]
- "scanner_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=scanner/scan_funnel.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), main()]
- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=scanner/smb_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, main(), _netbios_session(), parse_smb2_security_mode(), _smb1_negotiate()]
- "tests_test_main_scripts_hardening": "test_main_scripts_hardening.py" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, scanner_base.py, make_smb2_error(), make_smb2_success(), _run(), _scope()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-004.json

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
