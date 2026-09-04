# Node Description Batch 150 of 332

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

- "tests_test_detection_core_testfindingtodict_test_enums_serialized_to_values": ".test_enums_serialized_to_values()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L173 | neighbors=[TestFindingToDict, _finding()]
- "tests_test_detection_core_testingestfile_test_run_scoped_fact_is_ingested_but_creates_no_asset": ".test_run_scoped_fact_is_ingested_but_creates_no_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L237 | neighbors=[ipv6_discovery reports on the RUN, not …, TestIngestFile]
- "tests_test_detection_core_testkevdb_test_case_insensitive": ".test_case_insensitive()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L913 | neighbors=[TestKevDb, _mock_kev_db()]
- "tests_test_detection_core_testkevdb_test_is_kev": ".test_is_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L908 | neighbors=[TestKevDb, _mock_kev_db()]
- "tests_test_detection_core_testnormalize_test_dispatches_banner": ".test_dispatches_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1030 | neighbors=[TestNormalize, _fact()]
- "tests_test_detection_core_testnormalize_test_unknown_scanner_returns_empty": ".test_unknown_scanner_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1035 | neighbors=[TestNormalize, _fact()]
- "tests_test_detection_core_testnormalizebanner_test_empty_banner": ".test_empty_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L988 | neighbors=[TestNormalizeBanner, _fact()]
- "tests_test_detection_core_testnormalizebanner_test_ssh_banner": ".test_ssh_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L983 | neighbors=[TestNormalizeBanner, _fact()]
- "tests_test_detection_core_testnormalizedb_test_mysql_mariadb_engine_with_mariadb_suffix": ".test_mysql_mariadb_engine_with_mariadb_suffix()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1007 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizedb_test_mysql_mariadb_engine_without_mariadb_suffix_returns_empty": ".test_mysql_mariadb_engine_without_mariadb_suffix_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1002 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizedb_test_no_version_confidence_low": ".test_no_version_confidence_low()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1022 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizedb_test_postgresql": ".test_postgresql()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1013 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizedb_test_unknown_engine": ".test_unknown_engine()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1018 | neighbors=[TestNormalizeDb, _fact()]
- "tests_test_detection_core_testnormalizeweb_test_server_header": ".test_server_header()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L995 | neighbors=[TestNormalizeWeb, _fact()]
- "tests_test_detection_core_testsuppressnegated_test_keeps_authoritative_finding": ".test_keeps_authoritative_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L596 | neighbors=[TestSuppressNegated, _finding()]
- "tests_test_detection_core_testsuppressnegated_test_keeps_inferred_when_no_authoritative": ".test_keeps_inferred_when_no_authoritative()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L603 | neighbors=[TestSuppressNegated, _finding()]
- "tests_test_detection_core_testverify_test_ai_cap_at_60": ".test_ai_cap_at_60()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L725 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_ai_no_cap_if_already_below": ".test_ai_no_cap_if_already_below()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L730 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_auth_enforced_penalty": ".test_auth_enforced_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L742 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_authoritative_tier_base_95": ".test_authoritative_tier_base_95()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L707 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_backport_penalty": ".test_backport_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L718 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_checks_dict_populated": ".test_checks_dict_populated()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L772 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_confidence_clamped_at_zero": ".test_confidence_clamped_at_zero()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L781 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_confirmed_never_downgraded": ".test_confirmed_never_downgraded()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L766 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_deception_high_penalty": ".test_deception_high_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L748 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_deception_moderate_penalty": ".test_deception_moderate_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L753 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_filtered_port_penalty": ".test_filtered_port_penalty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L737 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_protocol_tier_base_85": ".test_protocol_tier_base_85()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L712 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testverify_test_state_downgrade_below_40": ".test_state_downgrade_below_40()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L758 | neighbors=[TestVerify, _finding()]
- "tests_test_detection_core_testvulndb_test_covers": ".test_covers()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L946 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_cvss_vector_index": ".test_cvss_vector_index()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L951 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_cvss_vector_missing": ".test_cvss_vector_missing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L959 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_known_products_sorted": ".test_known_products_sorted()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L963 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_lookup_existing": ".test_lookup_existing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L937 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_core_testvulndb_test_lookup_missing_returns_empty": ".test_lookup_missing_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L942 | neighbors=[TestVulnDB, _mock_vuln_db()]
- "tests_test_detection_coverage_test_explain_no_run_says_never_ran": "test_explain_no_run_says_never_ran()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L144 | neighbors=[test_detection_coverage.py, _user()]
- "tests_test_detection_pipeline_gaps_test_enqueue_is_not_gated_on_success": "test_enqueue_is_not_gated_on_success()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L149 | neighbors=[test_detection_pipeline_gaps.py, Facts are persisted whenever they are p…]
- "tests_test_detection_pipeline_gaps_test_total_rejection_leaves_no_facts_for_correlation": "test_total_rejection_leaves_no_facts_for_correlation()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L78 | neighbors=[test_detection_pipeline_gaps.py, _fact()]
- "tests_test_detection_validation_testdetectioncorrelator_test_compute_coverage": ".test_compute_coverage()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L120 | neighbors=[TestDetectionCorrelator, _action()]
- "tests_test_detection_validation_testdetectioncorrelator_test_detected_by_siem": ".test_detected_by_siem()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L54 | neighbors=[TestDetectionCorrelator, _action()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-149.json

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
