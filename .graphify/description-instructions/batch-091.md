# Node Description Batch 92 of 186

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

- "tests_test_detection_core_testverify_test_filtered_port_penalty": ".test_filtered_port_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L668 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_protocol_tier_base_85": ".test_protocol_tier_base_85()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L643 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_state_downgrade_below_40": ".test_state_downgrade_below_40()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L689 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testvulndb_test_covers": ".test_covers()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L877 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_cvss_vector_index": ".test_cvss_vector_index()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L882 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_cvss_vector_missing": ".test_cvss_vector_missing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L890 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_known_products_sorted": ".test_known_products_sorted()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L894 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_lookup_existing": ".test_lookup_existing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L868 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_lookup_missing_returns_empty": ".test_lookup_missing_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L873 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_validation_testdetectioncorrelator_test_compute_coverage": ".test_compute_coverage()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L105 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_detected_by_siem": ".test_detected_by_siem()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L54 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_detected_when_edr_not_blocking": ".test_detected_when_edr_not_blocking()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L69 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_gap_report_ignores_detected": ".test_gap_report_ignores_detected()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L135 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_generate_gap_report": ".test_generate_gap_report()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L126 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_host_match_by_ip": ".test_host_match_by_ip()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L92 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_missed_when_nothing": ".test_missed_when_nothing()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L75 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_out_of_window_is_missed": ".test_out_of_window_is_missed()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L80 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_prevented_by_edr": ".test_prevented_by_edr()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L62 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_wrong_host_is_missed": ".test_wrong_host_is_missed()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L86 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_engine_bridge_regression": "test_engine_bridge_regression.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_regression.py:L1 | neighbors=[937737b feat(resolution): reopen + flag…, test_reopen_flips_remediated_to_open_an…]
- "tests_test_engine_bridge_resolution": "test_engine_bridge_resolution.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_resolution.py:L1 | neighbors=[8cf23c2 feat(resolution): wire coverage…, test_run_records_coverage_and_invokes_r…]
- "tests_test_engine_bridge_verification": "test_engine_bridge_verification.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_verification.py:L1 | neighbors=[2fcec73 feat(verification): stamp verdi…, test_stamp_verification_sets_columns_wh…]
- "tests_test_exploit_engine_engagement": "_engagement()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L49 | neighbors=[test_exploit_engine.py, .test_validate_scope_out_of_range()]
- "tests_test_exploit_engine_pytest_addoption": "pytest_addoption()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L464 | neighbors=[test_exploit_engine.py, Register --msf-host CLI option for inte…]
- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_format": ".test_generate_dns_callback_token_format()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L290 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_unique": ".test_generate_dns_callback_token_unique()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L298 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_safety_meterpreter_raises": ".test_validate_safety_meterpreter_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L275 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_get_job_status_running": ".test_get_job_status_running()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L218 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_kill_job": ".test_kill_job()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L227 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_list_modules_exploit": ".test_list_modules_exploit()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L198 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_run_module_error_raises": ".test_run_module_error_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L212 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_run_module_returns_job_id": ".test_run_module_returns_job_id()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L204 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_finding_out_computed_test_confirmed_exploited_outranks_contradicted": "test_confirmed_exploited_outranks_contradicted()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L32 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_explicit_risk_rank_is_preserved": "test_explicit_risk_rank_is_preserved()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L38 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_lifecycle_fields_round_trip": "test_lifecycle_fields_round_trip()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L43 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_risk_rank_is_computed_not_none": "test_risk_rank_is_computed_not_none()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L26 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_reopen_endpoint_test_reopen_non_remediated_is_conflict": "test_reopen_non_remediated_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L40 | neighbors=[test_finding_reopen_endpoint.py, _db_with()]
- "tests_test_finding_reopen_endpoint_test_reopen_remediated_finding_sets_open_and_audits": "test_reopen_remediated_finding_sets_open_and_audits()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L23 | neighbors=[test_finding_reopen_endpoint.py, _db_with()]
- "tests_test_finding_resolution_schema": "test_finding_resolution_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, test_finding_has_resolution_lifecycle_c…]
- "tests_test_finding_risk_rank_api": "test_finding_risk_rank_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L1 | neighbors=[85e4537 feat(risk-rank): expose risk_ra…, test_finding_schema_exposes_risk_rank()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-091.json

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
