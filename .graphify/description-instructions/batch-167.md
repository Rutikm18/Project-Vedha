# Node Description Batch 168 of 380

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

- "tests_test_cli_test_poll_job_rejects_invalid_timing": "test_poll_job_rejects_invalid_timing()" | kind=code-symbol | source=probe/tests/test_cli.py:L291 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_returns_terminal_status": "test_poll_job_returns_terminal_status()" | kind=code-symbol | source=probe/tests/test_cli.py:L298 | neighbors=[test_cli.py, FakeClient]
- "tests_test_cli_test_poll_job_times_out": "test_poll_job_times_out()" | kind=code-symbol | source=probe/tests/test_cli.py:L308 | neighbors=[test_cli.py, FakeClient]
- "tests_test_customer_access_testrejectscanrequest": "TestRejectScanRequest" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L193 | neighbors=[test_customer_access.py, .test_reject_records_reason()]
- "tests_test_cve_correlation_testingestpagination_pages": "._pages()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L266 | neighbors=[TestIngestPagination, .test_resume()]
- "tests_test_cve_correlation_testingestpagination_test_resume": ".test_resume()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L274 | neighbors=[TestIngestPagination, ._pages()]
- "tests_test_dangling_agent_pin_testpinnedagentliveness_test_malformed_pin_never_strands_a_job": ".test_malformed_pin_never_strands_a_job()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L87 | neighbors=[TestPinnedAgentLiveness, _db_heartbeat()]
- "tests_test_dangling_agent_pin_testpinnedagentliveness_test_unknown_agent_is_not_live": ".test_unknown_agent_is_not_live()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L81 | neighbors=[TestPinnedAgentLiveness, _db_heartbeat()]
- "tests_test_dangling_agent_pin_testpinnedagentliveness_test_window_is_far_longer_than_the_90s_liveness_check": ".test_window_is_far_longer_than_the_90s_liveness_check()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L75 | neighbors=[Reusing the 90s online/offline threshol…, TestPinnedAgentLiveness]
- "tests_test_dangling_agent_pin_testpinsemantics_test_dangling_pin_is_logged_not_silent": ".test_dangling_pin_is_logged_not_silent()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L109 | neighbors=[An ignored pin changes routing, so it m…, TestPinSemantics]
- "tests_test_dangling_agent_pin_testpinsemantics_test_fallback_still_runs_the_eligibility_gate": ".test_fallback_still_runs_the_eligibility_gate()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L115 | neighbors=[The safety property: ignoring a stale p…, TestPinSemantics]
- "tests_test_db_fact_shape_test_probe_output_never_overrides_the_marker": "test_probe_output_never_overrides_the_marker()" | kind=code-symbol | source=probe/tests/test_db_fact_shape.py:L29 | neighbors=[test_db_fact_shape.py, A probe returning its own `db` key must…]
- "tests_test_db_fact_shape_test_redis_unauth_shape_survives_stamping": "test_redis_unauth_shape_survives_stamping()" | kind=code-symbol | source=probe/tests/test_db_fact_shape.py:L36 | neighbors=[test_db_fact_shape.py, The one high-value DB signal already co…]
- "tests_test_db_mongodb_auth_testauthinterpretation_test_auth_marker_wins_over_ok_marker": ".test_auth_marker_wins_over_ok_marker()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L69 | neighbors=[A reply containing both must be read as…, TestAuthInterpretation]
- "tests_test_db_mongodb_auth_testauthinterpretation_test_silence_claims_nothing": ".test_silence_claims_nothing()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L63 | neighbors=[Neither exposed nor hardened — an empty…, TestAuthInterpretation]
- "tests_test_db_mongodb_auth_testopmsgframing_test_db_field_is_present": ".test_db_field_is_present()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L40 | neighbors=[OP_MSG requires $db inside the command …, TestOpMsgFraming]
- "tests_test_db_mongodb_auth_testopmsgframing_test_opcode_is_op_msg_not_op_query": ".test_opcode_is_op_msg_not_op_query()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L29 | neighbors=[2013 = OP_MSG. 2004 = OP_QUERY, which m…, TestOpMsgFraming]
- "tests_test_db_mysql_greeting_testidentification_test_version_and_protocol": ".test_version_and_protocol()" | kind=code-symbol | source=probe/tests/test_db_mysql_greeting.py:L34 | neighbors=[TestIdentification, _greeting()]
- "tests_test_db_mysql_greeting_testtlsposture_test_client_ssl_advertised": ".test_client_ssl_advertised()" | kind=code-symbol | source=probe/tests/test_db_mysql_greeting.py:L47 | neighbors=[TestTLSPosture, _greeting()]
- "tests_test_db_mysql_greeting_testtlsposture_test_protocol_9_has_no_capability_flags": ".test_protocol_9_has_no_capability_flags()" | kind=code-symbol | source=probe/tests/test_db_mysql_greeting.py:L62 | neighbors=[TestTLSPosture, _greeting()]
- "tests_test_db_posture_rules_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L33 | neighbors=[test_db_posture_rules.py, _fire()]
- "tests_test_db_posture_rules_testcleartexttransport_test_auth_enforced_is_not_applied": ".test_auth_enforced_is_not_applied()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L112 | neighbors=[Authentication in front does not protec…, TestCleartextTransport]
- "tests_test_db_posture_rules_testcleartexttransport_test_fires_when_server_says_it_cannot_encrypt": ".test_fires_when_server_says_it_cannot_encrypt()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L93 | neighbors=[TestCleartextTransport, _fire()]
- "tests_test_db_posture_rules_testcontract_test_declared_inputs_exist_in_the_real_corpus": ".test_declared_inputs_exist_in_the_real_corpus()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L136 | neighbors=[Guards the failure no unit test catches…, TestContract]
- "tests_test_db_posture_rules_testcontract_test_every_captured_engine_carries_the_marker": ".test_every_captured_engine_carries_the_marker()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L146 | neighbors=[The marker is the one thing all engines…, TestContract]
- "tests_test_db_posture_rules_testcontract_test_requires_names_only_universal_paths": ".test_requires_names_only_universal_paths()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L122 | neighbors=[`requires` must name ONLY paths that EV…, TestContract]
- "tests_test_db_scanner_run": "_run()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L33 | neighbors=[test_db_scanner.py, _probe()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_rejects_garbage_with_type_byte": ".test_oracle_rejects_garbage_with_type_byte()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L73 | neighbors=[TestMysqlxVsOracle, _probe()]
- "tests_test_db_tds_prelogin_testencryptionposture_test_not_supported_means_no_tls_at_all": ".test_not_supported_means_no_tls_at_all()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L48 | neighbors=[TestEncryptionPosture, _prelogin_response()]
- "tests_test_db_tds_prelogin_testencryptionposture_test_required_is_the_hardened_case": ".test_required_is_the_hardened_case()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L54 | neighbors=[TestEncryptionPosture, _prelogin_response()]
- "tests_test_db_tds_prelogin_testpositiveevidenceonly_test_identification_survives_a_missing_encryption_option": ".test_identification_survives_a_missing_encryption_option()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L77 | neighbors=[TestPositiveEvidenceOnly, _prelogin_response()]
- "tests_test_db_tds_prelogin_testpositiveevidenceonly_test_truncated_table_claims_nothing_extra": ".test_truncated_table_claims_nothing_extra()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L84 | neighbors=[TestPositiveEvidenceOnly, _prelogin_response()]
- "tests_test_db_tds_prelogin_testpositiveevidenceonly_test_unknown_encryption_value_is_not_invented": ".test_unknown_encryption_value_is_not_invented()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L94 | neighbors=[TestPositiveEvidenceOnly, _prelogin_response()]
- "tests_test_db_tds_prelogin_testversion": "TestVersion" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L69 | neighbors=[test_db_tds_prelogin.py, .test_version_is_decoded()]
- "tests_test_db_tds_prelogin_testversion_test_version_is_decoded": ".test_version_is_decoded()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L70 | neighbors=[TestVersion, _prelogin_response()]
- "tests_test_default_cred_rule_testrulemetadata_test_declares_its_required_input": ".test_declares_its_required_input()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L115 | neighbors=[TestRuleMetadata, _rule()]
- "tests_test_default_cred_rule_testrulemetadata_test_is_registered": ".test_is_registered()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L112 | neighbors=[TestRuleMetadata, _rule()]
- "tests_test_default_cred_rule_testrulemetadata_test_reads_the_scanners_that_emit_auth_surface": ".test_reads_the_scanners_that_emit_auth_surface()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L118 | neighbors=[TestRuleMetadata, _rule()]
- "tests_test_default_cred_rule_testrulemetadata_test_severity_and_attack_mapping": ".test_severity_and_attack_mapping()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L121 | neighbors=[TestRuleMetadata, _rule()]
- "tests_test_detection_core_testaggregate_test_dedup_within_run": ".test_dedup_within_run()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1143 | neighbors=[TestAggregate, _finding()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-167.json

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
