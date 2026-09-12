# Node Description Batch 316 of 380

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

- "tests_test_default_cred_rule_rationale_49": "Same shape the other posture-rule tests use (tests/test_posture_rules.py)." | kind=entity | source=manager/detection_engine/tests/test_default_cred_rule.py:L49 | neighbors=[_fact()] | lang=en
- "tests_test_default_cred_rule_rationale_78": "The finding must read as a candidate, not a confirmation." | kind=entity | source=manager/detection_engine/tests/test_default_cred_rule.py:L78 | neighbors=[.test_evidence_explains_what_was_not_te…] | lang=pt
- "tests_test_default_cred_rule_rationale_84": "web_scan hints the vendor on the surface; other scanners may carry it         at" | kind=entity | source=manager/detection_engine/tests/test_default_cred_rule.py:L84 | neighbors=[.test_vendor_falls_back_to_the_fact_whe…] | lang=en
- "tests_test_default_cred_rule_rationale_94": "Evidence invariant — a vendor name alone proves nothing." | kind=entity | source=manager/detection_engine/tests/test_default_cred_rule.py:L94 | neighbors=[.test_no_auth_surface_at_all()] | lang=pt
- "tests_test_default_cred_rule_rationale_98": "A camera whose web UI is firewalled off is not this risk." | kind=entity | source=manager/detection_engine/tests/test_default_cred_rule.py:L98 | neighbors=[.test_scheme_none_is_not_a_login_surfac…] | lang=en
- "tests_test_default_cred_rule_testcatalog_test_known_vendor_has_defaults": ".test_known_vendor_has_defaults()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L26 | neighbors=[TestCatalog] | lang=en
- "tests_test_default_cred_rule_testcatalog_test_lookup_is_case_and_whitespace_insensitive": ".test_lookup_is_case_and_whitespace_insensitive()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L32 | neighbors=[TestCatalog] | lang=en
- "tests_test_default_cred_rule_testcatalog_test_none_and_empty_return_none": ".test_none_and_empty_return_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L38 | neighbors=[TestCatalog] | lang=en
- "tests_test_default_cred_rule_testcatalog_test_unknown_vendor_returns_none": ".test_unknown_vendor_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L35 | neighbors=[TestCatalog] | lang=en
- "tests_test_deps_rationale_1": "Phase 7 — Layer-2 dependency install logic (wheel-first, strict = wheel-only). P" | kind=entity | source=probe/tests/test_deps.py:L1 | neighbors=[test_deps.py] | lang=en
- "tests_test_deps_test_permissive_is_wheel_first_then_source_fallback": "test_permissive_is_wheel_first_then_source_fallback()" | kind=code-symbol | source=probe/tests/test_deps.py:L27 | neighbors=[test_deps.py] | lang=en
- "tests_test_deps_test_reqs_hash_stable_and_sensitive": "test_reqs_hash_stable_and_sensitive()" | kind=code-symbol | source=probe/tests/test_deps.py:L18 | neighbors=[test_deps.py] | lang=en
- "tests_test_deps_test_strict_is_wheel_only_no_source_build": "test_strict_is_wheel_only_no_source_build()" | kind=code-symbol | source=probe/tests/test_deps.py:L34 | neighbors=[test_deps.py] | lang=en
- "tests_test_deps_test_venv_python_is_os_correct": "test_venv_python_is_os_correct()" | kind=code-symbol | source=probe/tests/test_deps.py:L10 | neighbors=[test_deps.py] | lang=en
- "tests_test_detection_core_rationale_238": "ipv6_discovery reports on the RUN, not a host: its target is the local         i" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L238 | neighbors=[.test_run_scoped_fact_is_ingested_but_c…] | lang=en
- "tests_test_detection_core_testallosvsourcepackages_test_returns_list": ".test_returns_list()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1063 | neighbors=[TestAllOsvSourcePackages] | lang=en
- "tests_test_detection_core_testallosvsourcepackages_test_sorted": ".test_sorted()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1068 | neighbors=[TestAllOsvSourcePackages] | lang=en
- "tests_test_detection_core_testasset_test_add_alias": ".test_add_alias()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L163 | neighbors=[TestAsset] | lang=en
- "tests_test_detection_core_testclassifyconfidence_test_authoritative_scanners": ".test_authoritative_scanners()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L209 | neighbors=[TestClassifyConfidence] | lang=en
- "tests_test_detection_core_testclassifyconfidence_test_inferred_scanners": ".test_inferred_scanners()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L213 | neighbors=[TestClassifyConfidence] | lang=en
- "tests_test_detection_core_testcleandebianversion_test_no_revision": ".test_no_revision()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1051 | neighbors=[TestCleanDebianVersion] | lang=en
- "tests_test_detection_core_testcleandebianversion_test_strips_epoch": ".test_strips_epoch()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1046 | neighbors=[TestCleanDebianVersion] | lang=en
- "tests_test_detection_core_testcleandebianversion_test_strips_revision": ".test_strips_revision()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1041 | neighbors=[TestCleanDebianVersion] | lang=en
- "tests_test_detection_core_testcleanrpmversion_test_strips_release": ".test_strips_release()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1058 | neighbors=[TestCleanRpmVersion] | lang=en
- "tests_test_detection_core_testcorrelatesmbpatch_test_no_smb_facts_returns_none": ".test_no_smb_facts_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L630 | neighbors=[TestCorrelateSmbPatch] | lang=en
- "tests_test_detection_core_testcvss_test_known_vectors": ".test_known_vectors()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L328 | neighbors=[TestCvss] | lang=en
- "tests_test_detection_core_testcvss_test_parse_vector": ".test_parse_vector()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L340 | neighbors=[TestCvss] | lang=en
- "tests_test_detection_core_testcvss_test_returns_none_for_malformed": ".test_returns_none_for_malformed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L336 | neighbors=[TestCvss] | lang=en
- "tests_test_detection_core_testcvss_test_returns_none_for_v2_vector": ".test_returns_none_for_v2_vector()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L333 | neighbors=[TestCvss] | lang=en
- "tests_test_detection_core_testcvss_test_roundup_exact_boundary": ".test_roundup_exact_boundary()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L345 | neighbors=[TestCvss] | lang=en
- "tests_test_detection_core_testdeceptionscore_test_capped_at_1": ".test_capped_at_1()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L702 | neighbors=[TestDeceptionScore] | lang=en
- "tests_test_detection_core_testdeceptionscore_test_combined_high": ".test_combined_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L699 | neighbors=[TestDeceptionScore] | lang=en
- "tests_test_detection_core_testdeceptionscore_test_contradictory_os": ".test_contradictory_os()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L695 | neighbors=[TestDeceptionScore] | lang=en
- "tests_test_detection_core_testdeceptionscore_test_high_product_count": ".test_high_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L692 | neighbors=[TestDeceptionScore] | lang=en
- "tests_test_detection_core_testdeceptionscore_test_low_product_count": ".test_low_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L686 | neighbors=[TestDeceptionScore] | lang=en
- "tests_test_detection_core_testdeceptionscore_test_moderate_product_count": ".test_moderate_product_count()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L689 | neighbors=[TestDeceptionScore] | lang=en
- "tests_test_detection_core_testfindingpostinit_test_refuses_zero_evidence_refs": ".test_refuses_zero_evidence_refs()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L120 | neighbors=[TestFindingPostInit] | lang=en
- "tests_test_detection_core_testingestfile_test_authoritative_scanner_creates_authoritative_fact": ".test_authoritative_scanner_creates_authoritative_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L297 | neighbors=[TestIngestFile] | lang=en
- "tests_test_detection_core_testingestfile_test_empty_file": ".test_empty_file()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L280 | neighbors=[TestIngestFile] | lang=en
- "tests_test_detection_core_testingestfile_test_hostname_target_not_ip_keyed": ".test_hostname_target_not_ip_keyed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L307 | neighbors=[TestIngestFile] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-315.json

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
