# Node Description Batch 107 of 227

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

- "tests_test_ai_normalizer_testextractrawtext_test_db_scan_without_engine_returns_none": ".test_db_scan_without_engine_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L91 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_port_scan_returns_none": ".test_port_scan_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L100 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_service_banner_falls_back_to_banner": ".test_service_banner_falls_back_to_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L52 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_service_banner_first_line_takes_priority_over_banner": ".test_service_banner_first_line_takes_priority_over_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L56 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_service_banner_no_text_returns_none": ".test_service_banner_no_text_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L61 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_service_banner_uses_first_line": ".test_service_banner_uses_first_line()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L48 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_web_scan_empty_data_returns_none": ".test_web_scan_empty_data_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L81 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_web_scan_server_and_hints_combined": ".test_web_scan_server_and_hints_combined()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L75 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_web_scan_server_only": ".test_web_scan_server_only()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L65 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_web_scan_tech_hints_only": ".test_web_scan_tech_hints_only()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L69 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_async_udp_sinkprotocol": "_SinkProtocol" | kind=code-symbol | source=probe/tests/test_async_udp.py:L31 | neighbors=[test_async_udp.py, .datagram_received()]
- "tests_test_attack_path_correlation_test_correlation_is_host_scoped": "test_correlation_is_host_scoped()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L131 | neighbors=[test_attack_path_correlation.py, _ids()]
- "tests_test_attack_path_correlation_test_device_role_from_facts_also_amplifies": "test_device_role_from_facts_also_amplifies()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L62 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_exposed_db_with_unauth_is_critical": "test_exposed_db_with_unauth_is_critical()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L95 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_exposed_db_without_unauth_does_not_fire": "test_exposed_db_without_unauth_does_not_fire()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L106 | neighbors=[test_attack_path_correlation.py, _ids()]
- "tests_test_attack_path_correlation_test_legacy_windows_smbv1_plus_rdp": "test_legacy_windows_smbv1_plus_rdp()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L74 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_no_relay_when_signing_required": "test_no_relay_when_signing_required()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L42 | neighbors=[test_attack_path_correlation.py, _ids()]
- "tests_test_attack_path_correlation_test_ntlm_relay_high_when_smbv1_also_enabled": "test_ntlm_relay_high_when_smbv1_also_enabled()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L34 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_ntlm_relay_medium_when_only_signing_not_required": "test_ntlm_relay_medium_when_only_signing_not_required()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L24 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_ntlm_relay_on_domain_controller_is_critical": "test_ntlm_relay_on_domain_controller_is_critical()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L51 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_snmp_default_community_on_network_device_is_high": "test_snmp_default_community_on_network_device_is_high()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L113 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_snmp_default_community_without_network_role_is_medium": "test_snmp_default_community_without_network_role_is_medium()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L122 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_auth_login_testauthenticatebcryptfailure": "TestAuthenticateBcryptFailure" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L162 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…]
- "tests_test_auth_login_testauthenticatedatabasefailure": "TestAuthenticateDatabaseFailure" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L181 | neighbors=[test_auth_login.py, .test_raises_database_failure_on_sqlalc…]
- "tests_test_auth_login_testauthenticatedisabledtenant": "TestAuthenticateDisabledTenant" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L122 | neighbors=[test_auth_login.py, .test_raises_disabled_tenant()]
- "tests_test_auth_login_testauthenticatedisableduser": "TestAuthenticateDisabledUser" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L109 | neighbors=[test_auth_login.py, .test_raises_disabled_user()]
- "tests_test_auth_login_testauthenticatepasswordmismatch": "TestAuthenticatePasswordMismatch" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L95 | neighbors=[test_auth_login.py, .test_raises_password_mismatch()]
- "tests_test_auth_login_testauthenticateusernotfound": "TestAuthenticateUserNotFound" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L84 | neighbors=[test_auth_login.py, .test_raises_user_not_found()]
- "tests_test_auth_login_testauthenticateusernotfound_test_raises_user_not_found": ".test_raises_user_not_found()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L86 | neighbors=[TestAuthenticateUserNotFound, _make_db()]
- "tests_test_cli_test_cmd_doctor_success_with_online_agent": "test_cmd_doctor_success_with_online_agent()" | kind=code-symbol | source=probe/tests/test_cli.py:L204 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_cmd_scan_run_builds_dispatch_payload": "test_cmd_scan_run_builds_dispatch_payload()" | kind=code-symbol | source=probe/tests/test_cli.py:L167 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_rejects_invalid_timing": "test_poll_job_rejects_invalid_timing()" | kind=code-symbol | source=probe/tests/test_cli.py:L291 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_returns_terminal_status": "test_poll_job_returns_terminal_status()" | kind=code-symbol | source=probe/tests/test_cli.py:L298 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_times_out": "test_poll_job_times_out()" | kind=code-symbol | source=probe/tests/test_cli.py:L308 | neighbors=[test_cli.py, FakeClient]
- "tests_test_customer_access_testrejectscanrequest": "TestRejectScanRequest" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L193 | neighbors=[test_customer_access.py, .test_reject_records_reason()]
- "tests_test_db_scanner_run": "_run()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L33 | neighbors=[test_db_scanner.py, _probe()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_rejects_garbage_with_type_byte": ".test_oracle_rejects_garbage_with_type_byte()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L73 | neighbors=[TestMysqlxVsOracle, _probe()]
- "tests_test_detection_core_testaggregate_test_dedup_within_run": ".test_dedup_within_run()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1074 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testaggregate_test_multi_run_intermittent": ".test_multi_run_intermittent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1068 | neighbors=[TestAggregate, _finding()]
- "tests_test_detection_core_testaggregate_test_multi_run_stable": ".test_multi_run_stable()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1061 | neighbors=[TestAggregate, _finding()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-106.json

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
