# Node Description Batch 111 of 131

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

- "tests_test_detection_core_testdeceptionscore_test_contradictory_os": ".test_contradictory_os()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L626 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_high_product_count": ".test_high_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L623 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_low_product_count": ".test_low_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L617 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_moderate_product_count": ".test_moderate_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L620 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testfindingpostinit_test_refuses_zero_evidence_refs": ".test_refuses_zero_evidence_refs()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L114 | neighbors=[TestFindingPostInit]
- "tests_test_detection_core_testingestfile_test_authoritative_scanner_creates_authoritative_fact": ".test_authoritative_scanner_creates_authoritative_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L255 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_empty_file": ".test_empty_file()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L238 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_hostname_target_not_ip_keyed": ".test_hostname_target_not_ip_keyed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L265 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_multi_file_accumulation": ".test_multi_file_accumulation()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L245 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_quarantines_malformed": ".test_quarantines_malformed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L231 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_valid_jsonl": ".test_valid_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L221 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestvalidation_test_empty_target": ".test_empty_target()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L195 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testingestvalidation_test_missing_required_field": ".test_missing_required_field()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L188 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testingestvalidation_test_non_dict_record": ".test_non_dict_record()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L192 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testingestvalidation_test_port_not_int": ".test_port_not_int()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L198 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testingestvalidation_test_valid_record": ".test_valid_record()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L185 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testisip_test_hostname": ".test_hostname()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L216 | neighbors=[TestIsIp]
- "tests_test_detection_core_testisip_test_valid_ipv4": ".test_valid_ipv4()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L213 | neighbors=[TestIsIp]
- "tests_test_detection_core_testmakefindingid_test_deterministic": ".test_deterministic()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L99 | neighbors=[TestMakeFindingId]
- "tests_test_detection_core_testmakefindingid_test_different_inputs_different_ids": ".test_different_inputs_different_ids()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L104 | neighbors=[TestMakeFindingId]
- "tests_test_detection_core_testmakefindingid_test_length_16": ".test_length_16()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L109 | neighbors=[TestMakeFindingId]
- "tests_test_detection_core_testproductfromcpe_test_extracts_product": ".test_extracts_product()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L553 | neighbors=[TestProductFromCpe]
- "tests_test_detection_core_testproductfromcpe_test_short_cpe_returns_cpe": ".test_short_cpe_returns_cpe()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L556 | neighbors=[TestProductFromCpe]
- "tests_test_detection_core_testversioninranges_test_empty_ranges": ".test_empty_ranges()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L373 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_ignores_unknown_type": ".test_ignores_unknown_type()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L351 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_introduced_fixed": ".test_introduced_fixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L313 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_last_affected": ".test_last_affected()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L335 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_no_match_returns_false_none": ".test_no_match_returns_false_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L365 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_regression_sequence": ".test_regression_sequence()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L378 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_semver_type_included": ".test_semver_type_included()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L358 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_unbounded_introduced": ".test_unbounded_introduced()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L343 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_version_at_fixed": ".test_version_at_fixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L328 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_version_before_introduced": ".test_version_before_introduced()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L321 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testvulndb_test_content_hash_deterministic": ".test_content_hash_deterministic()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L898 | neighbors=[TestVulnDB]
- "tests_test_detection_core_testwilsonci_test_all_appearances": ".test_all_appearances()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1017 | neighbors=[TestWilsonCi]
- "tests_test_detection_core_testwilsonci_test_perfect_appearance": ".test_perfect_appearance()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1009 | neighbors=[TestWilsonCi]
- "tests_test_detection_core_testwilsonci_test_zero_appearances": ".test_zero_appearances()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1013 | neighbors=[TestWilsonCi]
- "tests_test_detection_core_testwilsonci_test_zero_n": ".test_zero_n()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1021 | neighbors=[TestWilsonCi]
- "tests_test_detection_validation_pytest_addoption": "pytest_addoption()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L312 | neighbors=[test_detection_validation.py]
- "tests_test_detection_validation_testdetectioncorrelator_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L51 | neighbors=[TestDetectionCorrelator]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-110.json

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
