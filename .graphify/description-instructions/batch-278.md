# Node Description Batch 279 of 336

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

- "tests_test_cve_correlation_testversion_test_in_range_end_exclusive": ".test_in_range_end_exclusive()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L56 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_in_range_exact": ".test_in_range_exact()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L65 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_in_range_start_inclusive": ".test_in_range_start_inclusive()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L61 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_in_range_unconstrained_is_false": ".test_in_range_unconstrained_is_false()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L69 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_parse_debian_epoch_and_distro_suffix": ".test_parse_debian_epoch_and_distro_suffix()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L41 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_parse_leading_v_and_empty": ".test_parse_leading_v_and_empty()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L46 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_parse_openssh_portable": ".test_parse_openssh_portable()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L35 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testversion_test_parse_openssl_letter_suffix": ".test_parse_openssl_letter_suffix()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L38 | neighbors=[TestVersion]
- "tests_test_cve_correlation_testvulndb_test_counts": ".test_counts()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L137 | neighbors=[TestVulnDB]
- "tests_test_cve_correlation_testvulndb_test_cves_for_cpe_in_range": ".test_cves_for_cpe_in_range()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L120 | neighbors=[TestVulnDB]
- "tests_test_cve_correlation_testvulndb_test_kev_sorts_first": ".test_kev_sorts_first()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L125 | neighbors=[TestVulnDB]
- "tests_test_cve_correlation_testvulndb_test_out_of_range_excluded": ".test_out_of_range_excluded()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L130 | neighbors=[TestVulnDB]
- "tests_test_cve_correlation_testvulndb_test_vendor_norm": ".test_vendor_norm()" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L134 | neighbors=[TestVulnDB]
- "tests_test_db_scanner_fakereader_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L18 | neighbors=[FakeReader]
- "tests_test_db_scanner_fakereader_read": ".read()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L21 | neighbors=[FakeReader]
- "tests_test_db_scanner_fakewriter_drain": ".drain()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L29 | neighbors=[FakeWriter]
- "tests_test_db_scanner_fakewriter_write": ".write()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L26 | neighbors=[FakeWriter]
- "tests_test_db_scanner_rationale_1": "Regression tests for db_scanner fingerprint matchers.  Focus: MySQL X Protocol (" | kind=entity | source=probe/tests/test_db_scanner.py:L1 | neighbors=[test_db_scanner.py]
- "tests_test_db_unauth_test_redis_authenticated": "test_redis_authenticated()" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L11 | neighbors=[test_db_unauth.py]
- "tests_test_db_unauth_test_redis_unauthenticated": "test_redis_unauthenticated()" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L4 | neighbors=[test_db_unauth.py]
- "tests_test_detection_core_rationale_238": "ipv6_discovery reports on the RUN, not a host: its target is the local         i" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L238 | neighbors=[.test_run_scoped_fact_is_ingested_but_c…]
- "tests_test_detection_core_testallosvsourcepackages_test_returns_list": ".test_returns_list()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1063 | neighbors=[TestAllOsvSourcePackages]
- "tests_test_detection_core_testallosvsourcepackages_test_sorted": ".test_sorted()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1068 | neighbors=[TestAllOsvSourcePackages]
- "tests_test_detection_core_testasset_test_add_alias": ".test_add_alias()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L163 | neighbors=[TestAsset]
- "tests_test_detection_core_testclassifyconfidence_test_authoritative_scanners": ".test_authoritative_scanners()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L209 | neighbors=[TestClassifyConfidence]
- "tests_test_detection_core_testclassifyconfidence_test_inferred_scanners": ".test_inferred_scanners()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L213 | neighbors=[TestClassifyConfidence]
- "tests_test_detection_core_testcleandebianversion_test_no_revision": ".test_no_revision()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1051 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleandebianversion_test_strips_epoch": ".test_strips_epoch()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1046 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleandebianversion_test_strips_revision": ".test_strips_revision()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1041 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleanrpmversion_test_strips_release": ".test_strips_release()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1058 | neighbors=[TestCleanRpmVersion]
- "tests_test_detection_core_testcorrelatesmbpatch_test_no_smb_facts_returns_none": ".test_no_smb_facts_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L630 | neighbors=[TestCorrelateSmbPatch]
- "tests_test_detection_core_testcvss_test_known_vectors": ".test_known_vectors()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L328 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_parse_vector": ".test_parse_vector()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L340 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_returns_none_for_malformed": ".test_returns_none_for_malformed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L336 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_returns_none_for_v2_vector": ".test_returns_none_for_v2_vector()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L333 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_roundup_exact_boundary": ".test_roundup_exact_boundary()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L345 | neighbors=[TestCvss]
- "tests_test_detection_core_testdeceptionscore_test_capped_at_1": ".test_capped_at_1()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L702 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_combined_high": ".test_combined_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L699 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_contradictory_os": ".test_contradictory_os()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L695 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_high_product_count": ".test_high_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L692 | neighbors=[TestDeceptionScore]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-278.json

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
