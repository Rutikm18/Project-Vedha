# Node Description Batch 67 of 131

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

- "tests_test_detection_core_testcomputepriority_test_unknown_tier": ".test_unknown_tier()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L780 | neighbors=[TestComputePriority, _finding()]
- "tests_test_detection_core_testcorrelatesmbpatch_test_smbv1_with_missing_hotfixes_returns_finding": ".test_smbv1_with_missing_hotfixes_returns_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L570 | neighbors=[TestCorrelateSmbPatch, _fact()]
- "tests_test_detection_core_testcorrelatesmbpatch_test_smbv1_with_patched_host_returns_none": ".test_smbv1_with_patched_host_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L582 | neighbors=[TestCorrelateSmbPatch, _fact()]
- "tests_test_detection_core_testcorrelatesmbpatch_test_smbv1_without_hotfix_data_returns_none": ".test_smbv1_without_hotfix_data_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L565 | neighbors=[TestCorrelateSmbPatch, _fact()]
- "tests_test_detection_core_testcpecandidatecpe23_test_cpe23_format": ".test_cpe23_format()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L908 | neighbors=[TestCPECandidateCpe23, _candidate()]
- "tests_test_detection_core_testdedupfindings_test_authoritative_upgrades_state": ".test_authoritative_upgrades_state()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L493 | neighbors=[TestDedupFindings, _finding()]
- "tests_test_detection_core_testdedupfindings_test_different_ids_preserved": ".test_different_ids_preserved()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L503 | neighbors=[TestDedupFindings, _finding()]
- "tests_test_detection_core_testdedupfindings_test_evidence_refs_dedup_preserving_order": ".test_evidence_refs_dedup_preserving_order()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L508 | neighbors=[TestDedupFindings, _finding()]
- "tests_test_detection_core_testdedupfindings_test_merges_same_id": ".test_merges_same_id()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L484 | neighbors=[TestDedupFindings, _finding()]
- "tests_test_detection_core_testepssdb_test_case_insensitive": ".test_case_insensitive()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L858 | neighbors=[TestEpssDb, _mock_epss_db()]
- "tests_test_detection_core_testepssdb_test_get_existing": ".test_get_existing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L850 | neighbors=[TestEpssDb, _mock_epss_db()]
- "tests_test_detection_core_testepssdb_test_get_missing": ".test_get_missing()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L854 | neighbors=[TestEpssDb, _mock_epss_db()]
- "tests_test_detection_core_testfactref_test_ref_format": ".test_ref_format()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L175 | neighbors=[TestFactRef, _fact()]
- "tests_test_detection_core_testfindingconsistency_test_classification_intermittent": ".test_classification_intermittent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1046 | neighbors=[TestFindingConsistency, _finding()]
- "tests_test_detection_core_testfindingconsistency_test_classification_mostly_stable": ".test_classification_mostly_stable()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1040 | neighbors=[TestFindingConsistency, _finding()]
- "tests_test_detection_core_testfindingconsistency_test_classification_stable": ".test_classification_stable()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1034 | neighbors=[TestFindingConsistency, _finding()]
- "tests_test_detection_core_testfindingconsistency_test_rate": ".test_rate()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1028 | neighbors=[TestFindingConsistency, _finding()]
- "tests_test_detection_core_testfindingpostinit_test_accepts_nonempty_evidence_refs": ".test_accepts_nonempty_evidence_refs()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L123 | neighbors=[TestFindingPostInit, _finding()]
- "tests_test_detection_core_testfindingtodict_test_enums_serialized_to_values": ".test_enums_serialized_to_values()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L167 | neighbors=[TestFindingToDict, _finding()]
- "tests_test_detection_core_testkevdb_test_case_insensitive": ".test_case_insensitive()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L844 | neighbors=[TestKevDb, _mock_kev_db()]
- "tests_test_detection_core_testkevdb_test_is_kev": ".test_is_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L839 | neighbors=[TestKevDb, _mock_kev_db()]
- "tests_test_detection_core_testnormalize_test_dispatches_banner": ".test_dispatches_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L961 | neighbors=[TestNormalize, _fact()]
- "tests_test_detection_core_testnormalize_test_unknown_scanner_returns_empty": ".test_unknown_scanner_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L966 | neighbors=[TestNormalize, _fact()]
- "tests_test_detection_core_testnormalizebanner_test_empty_banner": ".test_empty_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L919 | neighbors=[TestNormalizeBanner, _fact()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-066.json

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
