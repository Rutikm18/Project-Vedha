# Node Description Batch 91 of 104

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_db_scanner_fakewriter_drain": ".drain()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L29 | neighbors=[FakeWriter]
- "tests_test_db_scanner_fakewriter_write": ".write()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L26 | neighbors=[FakeWriter]
- "tests_test_db_scanner_rationale_1": "Regression tests for db_scanner fingerprint matchers.  Focus: MySQL X Protocol (" | kind=entity | source=probe/tests/test_db_scanner.py:L1 | neighbors=[test_db_scanner.py]
- "tests_test_detection_core_testallosvsourcepackages_test_returns_list": ".test_returns_list()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L994 | neighbors=[TestAllOsvSourcePackages]
- "tests_test_detection_core_testallosvsourcepackages_test_sorted": ".test_sorted()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L999 | neighbors=[TestAllOsvSourcePackages]
- "tests_test_detection_core_testasset_test_add_alias": ".test_add_alias()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L157 | neighbors=[TestAsset]
- "tests_test_detection_core_testclassifyconfidence_test_authoritative_scanners": ".test_authoritative_scanners()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L203 | neighbors=[TestClassifyConfidence]
- "tests_test_detection_core_testclassifyconfidence_test_inferred_scanners": ".test_inferred_scanners()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L207 | neighbors=[TestClassifyConfidence]
- "tests_test_detection_core_testcleandebianversion_test_no_revision": ".test_no_revision()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L982 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleandebianversion_test_strips_epoch": ".test_strips_epoch()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L977 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleandebianversion_test_strips_revision": ".test_strips_revision()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L972 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleanrpmversion_test_strips_release": ".test_strips_release()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L989 | neighbors=[TestCleanRpmVersion]
- "tests_test_detection_core_testcorrelatesmbpatch_test_no_smb_facts_returns_none": ".test_no_smb_facts_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L561 | neighbors=[TestCorrelateSmbPatch]
- "tests_test_detection_core_testcvss_test_known_vectors": ".test_known_vectors()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L286 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_parse_vector": ".test_parse_vector()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L298 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_returns_none_for_malformed": ".test_returns_none_for_malformed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L294 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_returns_none_for_v2_vector": ".test_returns_none_for_v2_vector()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L291 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_roundup_exact_boundary": ".test_roundup_exact_boundary()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L303 | neighbors=[TestCvss]
- "tests_test_detection_core_testdeceptionscore_test_capped_at_1": ".test_capped_at_1()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L633 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_combined_high": ".test_combined_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L630 | neighbors=[TestDeceptionScore]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-090.json

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
