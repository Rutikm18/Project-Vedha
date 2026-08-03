# Node Description Batch 112 of 131

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

- "tests_test_detection_validation_testdetectioncorrelator_test_coverage_empty": ".test_coverage_empty()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L121 | neighbors=[TestDetectionCorrelator]
- "tests_test_detection_validation_testdetectioncorrelator_test_naive_timestamp_does_not_crash": ".test_naive_timestamp_does_not_crash()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L98 | neighbors=[TestDetectionCorrelator]
- "tests_test_detection_validation_testedrparsing_test_crowdstrike_parse": ".test_crowdstrike_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L243 | neighbors=[TestEDRParsing]
- "tests_test_detection_validation_testedrparsing_test_defender_parse_and_host_filter": ".test_defender_parse_and_host_filter()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L257 | neighbors=[TestEDRParsing]
- "tests_test_detection_validation_testedrparsing_test_factory": ".test_factory()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L285 | neighbors=[TestEDRParsing]
- "tests_test_detection_validation_testedrparsing_test_sentinelone_parse": ".test_sentinelone_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L273 | neighbors=[TestEDRParsing]
- "tests_test_detection_validation_testsiemparsing_test_elastic_parse": ".test_elastic_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L216 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsiemparsing_test_factory": ".test_factory()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L231 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsiemparsing_test_sentinel_parse": ".test_sentinel_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L205 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsiemparsing_test_splunk_parse": ".test_splunk_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L188 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsiemparsing_test_splunk_spl_includes_host_and_time": ".test_splunk_spl_includes_host_and_time()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L200 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsigmarulegenerator_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L148 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_evidence_customises_rule": ".test_evidence_customises_rule()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L169 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_known_technique_template": ".test_known_technique_template()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L151 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_output_is_valid_yaml_and_stable_id": ".test_output_is_valid_yaml_and_stable_id()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L176 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_subtechnique_falls_back_to_parent": ".test_subtechnique_falls_back_to_parent()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L158 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_unknown_technique_uses_generic": ".test_unknown_technique_uses_generic()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L164 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsplunkintegration_skip_without_flag": ".skip_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L299 | neighbors=[TestSplunkIntegration]
- "tests_test_detection_validation_testsplunkintegration_test_live_query": ".test_live_query()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L306 | neighbors=[TestSplunkIntegration]
- "tests_test_device_identity_test_device_identity_rejects_invalid_private_key_encoding": "test_device_identity_rejects_invalid_private_key_encoding()" | kind=code-symbol | source=probe/tests/test_device_identity.py:L36 | neighbors=[test_device_identity.py]
- "tests_test_device_identity_test_device_identity_round_trip_and_signature_proof": "test_device_identity_round_trip_and_signature_proof()" | kind=code-symbol | source=probe/tests/test_device_identity.py:L21 | neighbors=[test_device_identity.py]
- "tests_test_device_identity_test_site_policy_signature_and_tofu_pin_are_enforced": "test_site_policy_signature_and_tofu_pin_are_enforced()" | kind=code-symbol | source=probe/tests/test_device_identity.py:L41 | neighbors=[test_device_identity.py]
- "tests_test_engagement_lists_rationale_1": "Unit tests for the dashboard list endpoints (jobs + assets)." | kind=entity | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[test_engagement_lists.py]
- "tests_test_engagement_validation_test_create_normalizes_name_scopes_and_duplicates": "test_create_normalizes_name_scopes_and_duplicates()" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L10 | neighbors=[test_engagement_validation.py]
- "tests_test_engagement_validation_test_create_rejects_invalid_scope_entries": "test_create_rejects_invalid_scope_entries()" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L31 | neighbors=[test_engagement_validation.py]
- "tests_test_engagement_validation_test_create_rejects_reversed_date_range": "test_create_rejects_reversed_date_range()" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L36 | neighbors=[test_engagement_validation.py]
- "tests_test_engagement_validation_test_update_rejects_blank_name_invalid_scope_and_reversed_dates": "test_update_rejects_blank_name_invalid_scope_and_reversed_dates()" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L46 | neighbors=[test_engagement_validation.py]
- "tests_test_exploit_engine_testmetasploitintegration_skip_without_flag": ".skip_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L434 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitintegration_test_connect_and_list_modules": ".test_connect_and_list_modules()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L441 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitintegration_test_run_safe_scanner_smb": ".test_run_safe_scanner_smb()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L450 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_call_without_connect_raises": ".test_call_without_connect_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L233 | neighbors=[TestMetasploitRPCClient]
- "tests_test_exploit_engine_testnucleiexploitrunner_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L351 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_evidence_truncated_to_max_bytes": ".test_evidence_truncated_to_max_bytes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L405 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_extract_evidence_includes_curl": ".test_extract_evidence_includes_curl()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L395 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_nonexistent_template_not_safe": ".test_nonexistent_template_not_safe()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L369 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_hit": ".test_parse_poc_output_hit()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L374 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_malformed_json_skipped": ".test_parse_poc_output_malformed_json_skipped()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L389 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_miss": ".test_parse_poc_output_miss()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L380 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_wrong_cve": ".test_parse_poc_output_wrong_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L385 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_safe_template_passes": ".test_safe_template_passes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L354 | neighbors=[TestNucleiExploitRunner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-111.json

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
