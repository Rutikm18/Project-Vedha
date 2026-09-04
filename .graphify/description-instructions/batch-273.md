# Node Description Batch 274 of 330

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

- "tests_test_detection_core_testdeceptionscore_test_capped_at_1": ".test_capped_at_1()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L702 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_combined_high": ".test_combined_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L699 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_contradictory_os": ".test_contradictory_os()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L695 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_high_product_count": ".test_high_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L692 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_low_product_count": ".test_low_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L686 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_moderate_product_count": ".test_moderate_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L689 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testfindingpostinit_test_refuses_zero_evidence_refs": ".test_refuses_zero_evidence_refs()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L120 | neighbors=[TestFindingPostInit]
- "tests_test_detection_core_testingestfile_test_authoritative_scanner_creates_authoritative_fact": ".test_authoritative_scanner_creates_authoritative_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L297 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_empty_file": ".test_empty_file()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L280 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_hostname_target_not_ip_keyed": ".test_hostname_target_not_ip_keyed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L307 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_multi_file_accumulation": ".test_multi_file_accumulation()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L287 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_quarantines_malformed": ".test_quarantines_malformed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L273 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_run_scoped_fact_with_interface_target_creates_no_asset": ".test_run_scoped_fact_with_interface_target_creates_no_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L262 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestfile_test_valid_jsonl": ".test_valid_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L227 | neighbors=[TestIngestFile]
- "tests_test_detection_core_testingestvalidation_test_empty_target": ".test_empty_target()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L201 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testingestvalidation_test_missing_required_field": ".test_missing_required_field()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L194 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testingestvalidation_test_non_dict_record": ".test_non_dict_record()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L198 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testingestvalidation_test_port_not_int": ".test_port_not_int()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L204 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testingestvalidation_test_valid_record": ".test_valid_record()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L191 | neighbors=[TestIngestValidation]
- "tests_test_detection_core_testisip_test_hostname": ".test_hostname()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L222 | neighbors=[TestIsIp]
- "tests_test_detection_core_testisip_test_valid_ipv4": ".test_valid_ipv4()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L219 | neighbors=[TestIsIp]
- "tests_test_detection_core_testmakefindingid_test_deterministic": ".test_deterministic()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L105 | neighbors=[TestMakeFindingId]
- "tests_test_detection_core_testmakefindingid_test_different_inputs_different_ids": ".test_different_inputs_different_ids()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L110 | neighbors=[TestMakeFindingId]
- "tests_test_detection_core_testmakefindingid_test_length_16": ".test_length_16()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L115 | neighbors=[TestMakeFindingId]
- "tests_test_detection_core_testproductfromcpe_test_extracts_product": ".test_extracts_product()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L622 | neighbors=[TestProductFromCpe]
- "tests_test_detection_core_testproductfromcpe_test_short_cpe_returns_cpe": ".test_short_cpe_returns_cpe()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L625 | neighbors=[TestProductFromCpe]
- "tests_test_detection_core_testversioninranges_test_empty_ranges": ".test_empty_ranges()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L415 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_ignores_unknown_type": ".test_ignores_unknown_type()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L393 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_introduced_fixed": ".test_introduced_fixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L355 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_last_affected": ".test_last_affected()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L377 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_no_match_returns_false_none": ".test_no_match_returns_false_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L407 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_regression_sequence": ".test_regression_sequence()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L420 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_semver_type_included": ".test_semver_type_included()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L400 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_unbounded_introduced": ".test_unbounded_introduced()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L385 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_version_at_fixed": ".test_version_at_fixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L370 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_version_before_introduced": ".test_version_before_introduced()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L363 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testvulndb_test_content_hash_deterministic": ".test_content_hash_deterministic()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L967 | neighbors=[TestVulnDB]
- "tests_test_detection_core_testwilsonci_test_all_appearances": ".test_all_appearances()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1086 | neighbors=[TestWilsonCi]
- "tests_test_detection_core_testwilsonci_test_perfect_appearance": ".test_perfect_appearance()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1078 | neighbors=[TestWilsonCi]
- "tests_test_detection_core_testwilsonci_test_zero_appearances": ".test_zero_appearances()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1082 | neighbors=[TestWilsonCi]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-273.json

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
