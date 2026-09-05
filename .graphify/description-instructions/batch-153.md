# Node Description Batch 154 of 336

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

- "tests_test_finding_resolution_schema": "test_finding_resolution_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, test_finding_has_resolution_lifecycle_c…]
- "tests_test_finding_risk_rank_api": "test_finding_risk_rank_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L1 | neighbors=[85e4537 feat(risk-rank): expose risk_ra…, test_finding_schema_exposes_risk_rank()]
- "tests_test_finding_section_testfindingsection_test_backward_compatible_keys_kept": ".test_backward_compatible_keys_kept()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L95 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_section_testfindingsection_test_clean_host_shows_no_findings_honestly": ".test_clean_host_shows_no_findings_honestly()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L51 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_section_testfindingsection_test_each_finding_tagged_with_verified_provenance": ".test_each_finding_tagged_with_verified_provenance()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L88 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_section_testfindingsection_test_findings_are_ranked_worst_first": ".test_findings_are_ranked_worst_first()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L76 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_section_testfindingsection_test_vulnerable_host_shows_ranked_vulnerabilities": ".test_vulnerable_host_shows_ranked_vulnerabilities()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L61 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_verification_api": "test_finding_verification_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_api.py:L1 | neighbors=[72f68af feat(verification): expose veri…, test_finding_schema_exposes_verificatio…]
- "tests_test_finding_verification_schema": "test_finding_verification_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_schema.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, test_finding_has_verification_columns()]
- "tests_test_ftp_scanner_testftpfindings_test_anon_denied_is_silent": ".test_anon_denied_is_silent()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L70 | neighbors=[TestFTPFindings, ._fact()]
- "tests_test_ftp_scanner_testftpfindings_test_anon_login_only_is_medium": ".test_anon_login_only_is_medium()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L65 | neighbors=[TestFTPFindings, ._fact()]
- "tests_test_ftp_scanner_testftpfindings_test_anon_read_is_high": ".test_anon_read_is_high()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L58 | neighbors=[TestFTPFindings, ._fact()]
- "tests_test_ftp_scanner_testftpscanner_test_anon_login_and_read_open": ".test_anon_login_and_read_open()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L33 | neighbors=[TestFTPScanner, ._sc()]
- "tests_test_ftp_scanner_testftpscanner_test_ftp_present_anon_denied_open_but_secure": ".test_ftp_present_anon_denied_open_but_secure()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L46 | neighbors=[TestFTPScanner, ._sc()]
- "tests_test_ftp_scanner_testftpscanner_test_no_ftp_filtered": ".test_no_ftp_filtered()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L41 | neighbors=[TestFTPScanner, ._sc()]
- "tests_test_ftp_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L75 | neighbors=[test_ftp_scanner.py, .test_main_scripts()]
- "tests_test_host_discovery_udp_test_netbios_reply_proves_life_and_names_host": "test_netbios_reply_proves_life_and_names_host()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L129 | neighbors=[test_host_discovery_udp.py, _nbstat_reply()]
- "tests_test_host_discovery_udp_test_tcp_reset_counts_as_proof_of_life": "test_tcp_reset_counts_as_proof_of_life()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L232 | neighbors=[test_host_discovery_udp.py, A RST mid-handshake (ConnectionResetErr…]
- "tests_test_host_discovery_udp_test_udp_tier_skipped_when_arp_definitively_failed": "test_udp_tier_skipped_when_arp_definitively_failed()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L251 | neighbors=[test_host_discovery_udp.py, On-LAN INCOMPLETE/FAILED = nobody owns …]
- "tests_test_host_discovery_udp_testparsenbstat_test_msbrowse_control_chars_dropped": ".test_msbrowse_control_chars_dropped()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L52 | neighbors=[TestParseNbstat, _nbstat_reply()]
- "tests_test_host_discovery_udp_testparsenbstat_test_names_hostname_domain_mac": ".test_names_hostname_domain_mac()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L38 | neighbors=[TestParseNbstat, _nbstat_reply()]
- "tests_test_host_discovery_udp_udp_server": "_udp_server()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L103 | neighbors=[test_host_discovery_udp.py, _Responder]
- "tests_test_host_health_testheartbeat_test_cancellation_is_clean": ".test_cancellation_is_clean()" | kind=code-symbol | source=probe/tests/test_host_health.py:L251 | neighbors=[TestHeartbeat, _monitor()]
- "tests_test_host_health_testheartbeat_test_declares_offline_after_consecutive_misses": ".test_declares_offline_after_consecutive_misses()" | kind=code-symbol | source=probe/tests/test_host_health.py:L207 | neighbors=[TestHeartbeat, _monitor()]
- "tests_test_host_health_testheartbeat_test_healthy_host_is_never_marked": ".test_healthy_host_is_never_marked()" | kind=code-symbol | source=probe/tests/test_host_health.py:L235 | neighbors=[TestHeartbeat, _monitor()]
- "tests_test_host_health_testsilencedetection_test_any_contact_beats_many_failures": ".test_any_contact_beats_many_failures()" | kind=code-symbol | source=probe/tests/test_host_health.py:L60 | neighbors=[TestSilenceDetection, _r()]
- "tests_test_host_health_testsilencedetection_test_filtered_is_silence_but_only_suspicion": ".test_filtered_is_silence_but_only_suspicion()" | kind=code-symbol | source=probe/tests/test_host_health.py:L49 | neighbors=[TestSilenceDetection, _r()]
- "tests_test_host_health_testsilencedetection_test_no_results_is_not_silence": ".test_no_results_is_not_silence()" | kind=code-symbol | source=probe/tests/test_host_health.py:L56 | neighbors=[A branch that declined to run says noth…, TestSilenceDetection]
- "tests_test_host_health_testsilencedetection_test_open_and_observed_are_contact": ".test_open_and_observed_are_contact()" | kind=code-symbol | source=probe/tests/test_host_health.py:L42 | neighbors=[TestSilenceDetection, _r()]
- "tests_test_host_health_testsilencedetection_test_transport_error_code_is_silence": ".test_transport_error_code_is_silence()" | kind=code-symbol | source=probe/tests/test_host_health.py:L52 | neighbors=[TestSilenceDetection, _r()]
- "tests_test_host_health_testsilencedetection_test_unreachable_is_silence": ".test_unreachable_is_silence()" | kind=code-symbol | source=probe/tests/test_host_health.py:L46 | neighbors=[TestSilenceDetection, _r()]
- "tests_test_host_health_testudpnoreplyisnotcontact_test_a_real_open_port_still_counts_as_contact": ".test_a_real_open_port_still_counts_as_contact()" | kind=code-symbol | source=probe/tests/test_host_health.py:L195 | neighbors=[TestUdpNoReplyIsNotContact, _r()]
- "tests_test_host_health_testudpnoreplyisnotcontact_test_mixed_udp_silence_and_a_real_open_port_is_contact": ".test_mixed_udp_silence_and_a_real_open_port_is_contact()" | kind=code-symbol | source=probe/tests/test_host_health.py:L198 | neighbors=[TestUdpNoReplyIsNotContact, _r()]
- "tests_test_host_health_testudpnoreplyisnotcontact_test_udp_no_reply_counts_as_silence": ".test_udp_no_reply_counts_as_silence()" | kind=code-symbol | source=probe/tests/test_host_health.py:L192 | neighbors=[TestUdpNoReplyIsNotContact, _r()]
- "tests_test_host_health_testverdict_test_a_broken_liveness_probe_never_aborts_the_scan": ".test_a_broken_liveness_probe_never_aborts_the_scan()" | kind=code-symbol | source=probe/tests/test_host_health.py:L113 | neighbors=[TestVerdict, _r()]
- "tests_test_http_lease_test_revoked_lease_cancels_the_attempt_immediately": "test_revoked_lease_cancels_the_attempt_immediately()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L120 | neighbors=[test_http_lease.py, An operator cancel (409) is DEFINITIVE,…]
- "tests_test_installer_contract_test_installer_accepts_enroll_token_and_insecure_for_http_manager": "test_installer_accepts_enroll_token_and_insecure_for_http_manager()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L62 | neighbors=[test_installer_contract.py, _dry_run()]
- "tests_test_installer_contract_test_installer_without_token_still_shows_manual_approval": "test_installer_without_token_still_shows_manual_approval()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L76 | neighbors=[test_installer_contract.py, _dry_run()]
- "tests_test_integration_fake_run_scan": "_fake_run_scan()" | kind=code-symbol | source=probe/tests/test_integration.py:L41 | neighbors=[test_integration.py, Return a minimal valid scan result (no …]
- "tests_test_integration_testfulljoblifecycle_test_complete_flow_with_encrypted_scope": ".test_complete_flow_with_encrypted_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L314 | neighbors=[Simulate the full probe lifecycle from …, TestFullJobLifecycle]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-153.json

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
