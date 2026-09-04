# Node Description Batch 276 of 332

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_detection_core_testingestvalidation_test_missing_required_field": ".test_missing_required_field()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L194 | neighbors=[TestIngestValidation] | lang=en
- "tests_test_detection_core_testingestvalidation_test_non_dict_record": ".test_non_dict_record()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L198 | neighbors=[TestIngestValidation] | lang=en
- "tests_test_detection_core_testingestvalidation_test_port_not_int": ".test_port_not_int()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L204 | neighbors=[TestIngestValidation] | lang=en
- "tests_test_detection_core_testingestvalidation_test_valid_record": ".test_valid_record()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L191 | neighbors=[TestIngestValidation] | lang=en
- "tests_test_detection_core_testisip_test_hostname": ".test_hostname()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L222 | neighbors=[TestIsIp] | lang=en
- "tests_test_detection_core_testisip_test_valid_ipv4": ".test_valid_ipv4()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L219 | neighbors=[TestIsIp] | lang=en
- "tests_test_detection_core_testmakefindingid_test_deterministic": ".test_deterministic()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L105 | neighbors=[TestMakeFindingId] | lang=en
- "tests_test_detection_core_testmakefindingid_test_different_inputs_different_ids": ".test_different_inputs_different_ids()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L110 | neighbors=[TestMakeFindingId] | lang=en
- "tests_test_detection_core_testmakefindingid_test_length_16": ".test_length_16()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L115 | neighbors=[TestMakeFindingId] | lang=en
- "tests_test_detection_core_testproductfromcpe_test_extracts_product": ".test_extracts_product()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L622 | neighbors=[TestProductFromCpe] | lang=en
- "tests_test_detection_core_testproductfromcpe_test_short_cpe_returns_cpe": ".test_short_cpe_returns_cpe()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L625 | neighbors=[TestProductFromCpe] | lang=en
- "tests_test_detection_core_testversioninranges_test_empty_ranges": ".test_empty_ranges()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L415 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_ignores_unknown_type": ".test_ignores_unknown_type()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L393 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_introduced_fixed": ".test_introduced_fixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L355 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_last_affected": ".test_last_affected()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L377 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_no_match_returns_false_none": ".test_no_match_returns_false_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L407 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_regression_sequence": ".test_regression_sequence()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L420 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_semver_type_included": ".test_semver_type_included()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L400 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_unbounded_introduced": ".test_unbounded_introduced()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L385 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_version_at_fixed": ".test_version_at_fixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L370 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testversioninranges_test_version_before_introduced": ".test_version_before_introduced()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L363 | neighbors=[TestVersionInRanges] | lang=en
- "tests_test_detection_core_testvulndb_test_content_hash_deterministic": ".test_content_hash_deterministic()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L967 | neighbors=[TestVulnDB] | lang=en
- "tests_test_detection_core_testwilsonci_test_all_appearances": ".test_all_appearances()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1086 | neighbors=[TestWilsonCi] | lang=en
- "tests_test_detection_core_testwilsonci_test_perfect_appearance": ".test_perfect_appearance()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1078 | neighbors=[TestWilsonCi] | lang=en
- "tests_test_detection_core_testwilsonci_test_zero_appearances": ".test_zero_appearances()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1082 | neighbors=[TestWilsonCi] | lang=en
- "tests_test_detection_core_testwilsonci_test_zero_n": ".test_zero_n()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1090 | neighbors=[TestWilsonCi] | lang=en
- "tests_test_detection_coverage_rationale_1": "Detection-trace coverage surfaced in the API: complete_with_gaps + explain.  Gua" | kind=entity | source=manager/backend/tests/test_detection_coverage.py:L1 | neighbors=[test_detection_coverage.py] | lang=en
- "tests_test_detection_pipeline_gaps_ctx_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L171 | neighbors=[_ctx] | lang=en
- "tests_test_detection_pipeline_gaps_ctx_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L172 | neighbors=[_ctx] | lang=en
- "tests_test_detection_pipeline_gaps_ctx_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L170 | neighbors=[_ctx] | lang=en
- "tests_test_detection_pipeline_gaps_rationale_1": "test_detection_pipeline_gaps.py — four ways facts reached the manager and then f" | kind=entity | source=manager/backend/tests/test_detection_pipeline_gaps.py:L1 | neighbors=[test_detection_pipeline_gaps.py] | lang=en
- "tests_test_detection_pipeline_gaps_rationale_126": "An older probe reports none. Coverage stays empty and nothing auto-resolves —" | kind=entity | source=manager/backend/tests/test_detection_pipeline_gaps.py:L126 | neighbors=[test_missing_scanner_runs_degrades_to_e…] | lang=en
- "tests_test_detection_pipeline_gaps_rationale_150": "Facts are persisted whenever they are present, but the outbox enqueue used to" | kind=entity | source=manager/backend/tests/test_detection_pipeline_gaps.py:L150 | neighbors=[test_enqueue_is_not_gated_on_success()] | lang=en
- "tests_test_detection_pipeline_gaps_rationale_169": "Minimal async-context-manager wrapper around a mock session." | kind=entity | source=manager/backend/tests/test_detection_pipeline_gaps.py:L169 | neighbors=[_ctx] | lang=pt
- "tests_test_detection_pipeline_gaps_rationale_46": "`data` is read with .get() by every rule. A string there used to raise mid-run" | kind=entity | source=manager/backend/tests/test_detection_pipeline_gaps.py:L46 | neighbors=[test_a_non_dict_data_payload_is_quarant…] | lang=en
- "tests_test_detection_pipeline_gaps_rationale_65": "attack_path_findings runs on meta['accepted_facts']. If that still contained" | kind=entity | source=manager/backend/tests/test_detection_pipeline_gaps.py:L65 | neighbors=[test_accepted_facts_excludes_what_inges…] | lang=en
- "tests_test_detection_pipeline_gaps_rationale_85": "No engine means no ingest verdict. Without a verdict we cannot call any fact" | kind=entity | source=manager/backend/tests/test_detection_pipeline_gaps.py:L85 | neighbors=[test_accepted_facts_falls_back_to_raw_w…] | lang=pt
- "tests_test_detection_pipeline_gaps_rationale_97": "scan_results has no scanner_runs column; the job's result blob does. Passing" | kind=entity | source=manager/backend/tests/test_detection_pipeline_gaps.py:L97 | neighbors=[test_facts_ready_reads_scanner_runs_fro…] | lang=en
- "tests_test_detection_validation_pytest_addoption": "pytest_addoption()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L339 | neighbors=[test_detection_validation.py] | lang=en
- "tests_test_detection_validation_testdetectioncorrelator_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L51 | neighbors=[TestDetectionCorrelator] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-275.json

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
