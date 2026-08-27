# Node Description Batch 44 of 92

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

- "scanner_udp_scanner_ike_probe": "_ike_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L77 | neighbors=[udp_scanner.py, Minimal IKEv2 IKE_SA_INIT probe.  Sends…]
- "scanner_udp_scanner_interpret_dns_recursion": "interpret_dns_recursion()" | kind=code-symbol | source=scanner/udp_scanner.py:L173 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_interpret_memcached_stats": "interpret_memcached_stats()" | kind=code-symbol | source=scanner/udp_scanner.py:L184 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_interpret_ntp_monlist": "interpret_ntp_monlist()" | kind=code-symbol | source=scanner/udp_scanner.py:L169 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_ipmi_probe": "_ipmi_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L139 | neighbors=[udp_scanner.py, RMCP Ping (ASF Presence Ping) to detect…]
- "scanner_udp_scanner_mdns_probe": "_mdns_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L158 | neighbors=[udp_scanner.py, mDNS PTR query for _services._dns-sd._u…]
- "scanner_udp_scanner_ntp_monlist_probe": "_ntp_monlist_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L50 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_ssdp_probe": "_ssdp_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L146 | neighbors=[udp_scanner.py, UPnP/SSDP M-SEARCH — unicast to target:…]
- "scanner_udp_scanner_tftp_probe": "_tftp_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L132 | neighbors=[udp_scanner.py, TFTP RRQ for a non-existent file.  Erro…]
- "scanner_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/udp_scanner.py:L376 | neighbors=[UDPScanner, ._probe()]
- "scanner_unauth_access_as_text": "_as_text()" | kind=code-symbol | source=scanner/unauth_access.py:L40 | neighbors=[unauth_access.py, classify_unauth_access()]
- "scanner_vantage_matrix_is_external": "_is_external()" | kind=code-symbol | source=scanner/vantage_matrix.py:L34 | neighbors=[vantage_matrix.py, reconcile_vantages()]
- "scanner_web_scanner_fetch": "_fetch()" | kind=code-symbol | source=scanner/web_scanner.py:L78 | neighbors=[web_scanner.py, parse_allow_header()]
- "scanner_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=scanner/web_scanner.py:L55 | neighbors=[web_scanner.py, .redirect_request()]
- "scanner_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=scanner/web_scanner.py:L143 | neighbors=[WebScanner, .scan_target()]
- "scanner_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/web_scanner.py:L160 | neighbors=[WebScanner, ._scan_port()]
- "scanner_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=scanner/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "scanner_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=scanner/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=scanner/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=scanner/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_transport_order": "._transport_order()" | kind=code-symbol | source=scanner/windows_collector.py:L299 | neighbors=[WindowsCollector, ._collect_host()]
- "scanner_windows_collector_windowscollector_winrm_result": "._winrm_result()" | kind=code-symbol | source=scanner/windows_collector.py:L306 | neighbors=[WindowsCollector, ._collect_host()]
- "tests_test_agent_identity_test_cached_identity_refreshes_current_capabilities": "test_cached_identity_refreshes_current_capabilities()" | kind=code-symbol | source=tests/test_agent_identity.py:L42 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agent_identity_test_cached_identity_retries_transient_refresh_failure": "test_cached_identity_retries_transient_refresh_failure()" | kind=code-symbol | source=tests/test_agent_identity.py:L69 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_agent_identity_test_rejected_cached_token_falls_back_to_idempotent_registration": "test_rejected_cached_token_falls_back_to_idempotent_registration()" | kind=code-symbol | source=tests/test_agent_identity.py:L92 | neighbors=[test_agent_identity.py, _cached_transport()]
- "tests_test_async_udp_sinkprotocol": "_SinkProtocol" | kind=code-symbol | source=tests/test_async_udp.py:L31 | neighbors=[test_async_udp.py, .datagram_received()]
- "tests_test_cli_test_cmd_doctor_success_with_online_agent": "test_cmd_doctor_success_with_online_agent()" | kind=code-symbol | source=tests/test_cli.py:L204 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_cmd_scan_run_builds_dispatch_payload": "test_cmd_scan_run_builds_dispatch_payload()" | kind=code-symbol | source=tests/test_cli.py:L167 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_rejects_invalid_timing": "test_poll_job_rejects_invalid_timing()" | kind=code-symbol | source=tests/test_cli.py:L291 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_returns_terminal_status": "test_poll_job_returns_terminal_status()" | kind=code-symbol | source=tests/test_cli.py:L298 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_times_out": "test_poll_job_times_out()" | kind=code-symbol | source=tests/test_cli.py:L308 | neighbors=[test_cli.py, FakeClient]
- "tests_test_db_scanner_run": "_run()" | kind=code-symbol | source=tests/test_db_scanner.py:L33 | neighbors=[test_db_scanner.py, _probe()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_rejects_garbage_with_type_byte": ".test_oracle_rejects_garbage_with_type_byte()" | kind=code-symbol | source=tests/test_db_scanner.py:L73 | neighbors=[TestMysqlxVsOracle, _probe()]
- "tests_test_e2e_engagement_to_findings_plant": "_plant()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L36 | neighbors=[test_e2e_engagement_to_findings.py, test_real_scan_of_open_datastore_yields…]
- "tests_test_e2e_engagement_to_findings_test_correlated_findings_cite_their_base_findings": "test_correlated_findings_cite_their_base_findings()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L161 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_engagement_dispatch_reaches_probe_and_enforces_scope": "test_engagement_dispatch_reaches_probe_and_enforces_scope()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L67 | neighbors=[test_e2e_engagement_to_findings.py, _manager()]
- "tests_test_e2e_engagement_to_findings_test_manager_correlation_finds_all_three_attack_paths": "test_manager_correlation_finds_all_three_attack_paths()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L148 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_ntlm_relay_is_high_when_smbv1_present_medium_otherwise": "test_ntlm_relay_is_high_when_smbv1_present_medium_otherwise()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L169 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_out_of_scope_target_is_refused_end_to_end": "test_out_of_scope_target_is_refused_end_to_end()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L88 | neighbors=[test_e2e_engagement_to_findings.py, _manager()]
- "tests_test_installer_contract_test_installer_accepts_enroll_token_and_insecure_for_http_manager": "test_installer_accepts_enroll_token_and_insecure_for_http_manager()" | kind=code-symbol | source=tests/test_installer_contract.py:L62 | neighbors=[test_installer_contract.py, _dry_run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-043.json

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
