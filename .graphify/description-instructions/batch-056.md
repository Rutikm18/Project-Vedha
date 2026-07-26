# Node Description Batch 57 of 104

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

- "tests_test_detection_core_testnormalizebanner_test_ssh_banner": ".test_ssh_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L914 | neighbors=[TestNormalizeBanner, _fact()]
- "tests_test_detection_core_testnormalizedb_test_mysql_mariadb_engine_with_mariadb_suffix": ".test_mysql_mariadb_engine_with_mariadb_suffix()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L938 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizedb_test_mysql_mariadb_engine_without_mariadb_suffix_returns_empty": ".test_mysql_mariadb_engine_without_mariadb_suffix_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L933 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizedb_test_no_version_confidence_low": ".test_no_version_confidence_low()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L953 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizedb_test_postgresql": ".test_postgresql()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L944 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizedb_test_unknown_engine": ".test_unknown_engine()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L949 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizeweb_test_server_header": ".test_server_header()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L926 | neighbors=[TestNormalizeWeb, _fact()]
- "tests_test_detection_core_testsuppressnegated_test_keeps_authoritative_finding": ".test_keeps_authoritative_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L527 | neighbors=[TestSuppressNegated, _finding()]
- "tests_test_detection_core_testsuppressnegated_test_keeps_inferred_when_no_authoritative": ".test_keeps_inferred_when_no_authoritative()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L534 | neighbors=[TestSuppressNegated, _finding()]
- "tests_test_detection_core_testverify_test_ai_cap_at_60": ".test_ai_cap_at_60()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L656 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_ai_no_cap_if_already_below": ".test_ai_no_cap_if_already_below()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L661 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_auth_enforced_penalty": ".test_auth_enforced_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L673 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_authoritative_tier_base_95": ".test_authoritative_tier_base_95()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L638 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_backport_penalty": ".test_backport_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L649 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_checks_dict_populated": ".test_checks_dict_populated()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L703 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_confidence_clamped_at_zero": ".test_confidence_clamped_at_zero()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L712 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_confirmed_never_downgraded": ".test_confirmed_never_downgraded()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L697 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_deception_high_penalty": ".test_deception_high_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L679 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_deception_moderate_penalty": ".test_deception_moderate_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L684 | neighbors=[TestVerify, _finding()]
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
- "tests_test_exploit_engine_engagement": "_engagement()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L49 | neighbors=[test_exploit_engine.py, .test_validate_scope_out_of_range()]
- "tests_test_exploit_engine_pytest_addoption": "pytest_addoption()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L464 | neighbors=[test_exploit_engine.py, Register --msf-host CLI option for inte…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-056.json

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
