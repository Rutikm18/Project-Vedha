# Node Description Batch 281 of 336

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
- "tests_test_detection_validation_testdetectioncorrelator_test_coverage_empty": ".test_coverage_empty()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L148 | neighbors=[TestDetectionCorrelator] | lang=en
- "tests_test_detection_validation_testdetectioncorrelator_test_naive_timestamp_does_not_crash": ".test_naive_timestamp_does_not_crash()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L113 | neighbors=[TestDetectionCorrelator] | lang=en
- "tests_test_detection_validation_testedrparsing_test_crowdstrike_parse": ".test_crowdstrike_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L270 | neighbors=[TestEDRParsing] | lang=en
- "tests_test_detection_validation_testedrparsing_test_defender_parse_and_host_filter": ".test_defender_parse_and_host_filter()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L284 | neighbors=[TestEDRParsing] | lang=en
- "tests_test_detection_validation_testedrparsing_test_factory": ".test_factory()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L312 | neighbors=[TestEDRParsing] | lang=en
- "tests_test_detection_validation_testedrparsing_test_sentinelone_parse": ".test_sentinelone_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L300 | neighbors=[TestEDRParsing] | lang=en
- "tests_test_detection_validation_testsiemparsing_test_elastic_parse": ".test_elastic_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L243 | neighbors=[TestSIEMParsing] | lang=en
- "tests_test_detection_validation_testsiemparsing_test_factory": ".test_factory()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L258 | neighbors=[TestSIEMParsing] | lang=en
- "tests_test_detection_validation_testsiemparsing_test_sentinel_parse": ".test_sentinel_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L232 | neighbors=[TestSIEMParsing] | lang=en
- "tests_test_detection_validation_testsiemparsing_test_splunk_parse": ".test_splunk_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L215 | neighbors=[TestSIEMParsing] | lang=en
- "tests_test_detection_validation_testsiemparsing_test_splunk_spl_includes_host_and_time": ".test_splunk_spl_includes_host_and_time()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L227 | neighbors=[TestSIEMParsing] | lang=en
- "tests_test_detection_validation_testsigmarulegenerator_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L175 | neighbors=[TestSigmaRuleGenerator] | lang=en
- "tests_test_detection_validation_testsigmarulegenerator_test_evidence_customises_rule": ".test_evidence_customises_rule()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L196 | neighbors=[TestSigmaRuleGenerator] | lang=en
- "tests_test_detection_validation_testsigmarulegenerator_test_known_technique_template": ".test_known_technique_template()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L178 | neighbors=[TestSigmaRuleGenerator] | lang=en
- "tests_test_detection_validation_testsigmarulegenerator_test_output_is_valid_yaml_and_stable_id": ".test_output_is_valid_yaml_and_stable_id()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L203 | neighbors=[TestSigmaRuleGenerator] | lang=en
- "tests_test_detection_validation_testsigmarulegenerator_test_subtechnique_falls_back_to_parent": ".test_subtechnique_falls_back_to_parent()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L185 | neighbors=[TestSigmaRuleGenerator] | lang=en
- "tests_test_detection_validation_testsigmarulegenerator_test_unknown_technique_uses_generic": ".test_unknown_technique_uses_generic()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L191 | neighbors=[TestSigmaRuleGenerator] | lang=en
- "tests_test_detection_validation_testsplunkintegration_skip_without_flag": ".skip_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L326 | neighbors=[TestSplunkIntegration] | lang=en
- "tests_test_detection_validation_testsplunkintegration_test_live_query": ".test_live_query()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L333 | neighbors=[TestSplunkIntegration] | lang=en
- "tests_test_device_identity_test_device_identity_rejects_invalid_private_key_encoding": "test_device_identity_rejects_invalid_private_key_encoding()" | kind=code-symbol | source=probe/tests/test_device_identity.py:L36 | neighbors=[test_device_identity.py] | lang=en
- "tests_test_device_identity_test_device_identity_round_trip_and_signature_proof": "test_device_identity_round_trip_and_signature_proof()" | kind=code-symbol | source=probe/tests/test_device_identity.py:L21 | neighbors=[test_device_identity.py] | lang=en
- "tests_test_device_identity_test_site_policy_signature_and_tofu_pin_are_enforced": "test_site_policy_signature_and_tofu_pin_are_enforced()" | kind=code-symbol | source=probe/tests/test_device_identity.py:L41 | neighbors=[test_device_identity.py] | lang=en
- "tests_test_device_profile_rationale_1": "test_device_profile.py — the probe device_inventory → Asset role mapping.  Pure" | kind=entity | source=manager/backend/tests/test_device_profile.py:L1 | neighbors=[test_device_profile.py] | lang=en
- "tests_test_device_profile_test_ambiguous_keeps_asset_type_none_but_records_role": "test_ambiguous_keeps_asset_type_none_but_records_role()" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L53 | neighbors=[test_device_profile.py] | lang=en
- "tests_test_device_profile_test_device_profiles_extracts_role_detail_and_confidence": "test_device_profiles_extracts_role_detail_and_confidence()" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L30 | neighbors=[test_device_profile.py] | lang=en
- "tests_test_device_profile_test_every_device_type_maps_to_the_right_asset_type": "test_every_device_type_maps_to_the_right_asset_type()" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L14 | neighbors=[test_device_profile.py] | lang=en
- "tests_test_device_profile_test_malformed_entries_are_skipped": "test_malformed_entries_are_skipped()" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L70 | neighbors=[test_device_profile.py] | lang=en
- "tests_test_device_profile_test_non_device_inventory_result_yields_no_profiles": "test_non_device_inventory_result_yields_no_profiles()" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L64 | neighbors=[test_device_profile.py] | lang=en
- "tests_test_device_profile_test_unmappable_roles_leave_asset_type_untouched": "test_unmappable_roles_leave_asset_type_untouched()" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L23 | neighbors=[test_device_profile.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-280.json

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
