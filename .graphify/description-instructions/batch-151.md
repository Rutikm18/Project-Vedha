# Node Description Batch 152 of 332

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

- "tests_test_exploit_engine_testmetasploitrpcclient_test_kill_job": ".test_kill_job()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L227 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_list_modules_exploit": ".test_list_modules_exploit()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L198 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_run_module_error_raises": ".test_run_module_error_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L212 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_run_module_returns_job_id": ".test_run_module_returns_job_id()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L204 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploitability_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L177 | neighbors=[test_exploitability.py, test_end_to_end_smbv1_is_ranked_by_real…]
- "tests_test_exploitability_test_end_to_end_smbv1_is_ranked_by_real_exploitation": "test_end_to_end_smbv1_is_ranked_by_real_exploitation()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L197 | neighbors=[test_exploitability.py, _fact()]
- "tests_test_exploitability_test_linked_cves_are_actually_on_the_pinned_kev_list": "test_linked_cves_are_actually_on_the_pinned_kev_list()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L190 | neighbors=[test_exploitability.py, If a curated link names a CVE the shipp…]
- "tests_test_exploitability_testapplytofindings_test_no_databases_is_a_no_op": ".test_no_databases_is_a_no_op()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L141 | neighbors=[TestApplyToFindings, _finding()]
- "tests_test_exploitability_testapplytofindings_test_priority_bands_match_posture_rules": ".test_priority_bands_match_posture_rules()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L150 | neighbors=[A re-rank here must never disagree with…, TestApplyToFindings]
- "tests_test_exposed_services_testporthypothesiscontradiction_test_backdoor_evidence_is_never_suppressed": ".test_backdoor_evidence_is_never_suppressed()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L210 | neighbors=[A shell answering on a benign-listed po…, TestPortHypothesisContradiction]
- "tests_test_fact_contract_test_corpus_is_present_and_nonempty": "test_corpus_is_present_and_nonempty()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L60 | neighbors=[test_fact_contract.py, _load_corpus()]
- "tests_test_finding_events_testeventtypeforstatus": "TestEventTypeForStatus" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L124 | neighbors=[test_finding_events.py, .test_maps_status_to_specific_event()]
- "tests_test_finding_events_testmerge_test_labels_attached": ".test_labels_attached()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L118 | neighbors=[TestMerge, ._synth()]
- "tests_test_finding_events_testpatchaudits_test_manual_remediation_sets_close_metadata_and_audits_reason": ".test_manual_remediation_sets_close_metadata_and_audits_reason()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L195 | neighbors=[TestPatchAudits, _finding()]
- "tests_test_finding_events_testpatchaudits_test_status_change_records_event": ".test_status_change_records_event()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L160 | neighbors=[TestPatchAudits, _finding()]
- "tests_test_finding_events_testsynthesize_test_auto_resolution_event": ".test_auto_resolution_event()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L66 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testsynthesize_test_detected_actor_falls_back_to_detection_engine": ".test_detected_actor_falls_back_to_detection_engine()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L55 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testsynthesize_test_detected_actor_labels_network_va_campaign": ".test_detected_actor_labels_network_va_campaign()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L51 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testsynthesize_test_genesis_detected_from_first_seen": ".test_genesis_detected_from_first_seen()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L45 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testsynthesize_test_reopened_inferred_from_count": ".test_reopened_inferred_from_count()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L78 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testtimelineendpoint": "TestTimelineEndpoint" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L137 | neighbors=[test_finding_events.py, .test_returns_synthesized_timeline()]
- "tests_test_finding_events_testtimelineendpoint_test_returns_synthesized_timeline": ".test_returns_synthesized_timeline()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L139 | neighbors=[TestTimelineEndpoint, _finding()]
- "tests_test_finding_out_computed_test_confirmed_exploited_outranks_contradicted": "test_confirmed_exploited_outranks_contradicted()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L32 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_detail_asset_context_round_trips_without_changing_list_contract": "test_detail_asset_context_round_trips_without_changing_list_contract()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L55 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_explicit_risk_rank_is_preserved": "test_explicit_risk_rank_is_preserved()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L44 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_lifecycle_fields_round_trip": "test_lifecycle_fields_round_trip()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L49 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_nested_enrichment_kev_is_part_of_the_rank": "test_nested_enrichment_kev_is_part_of_the_rank()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L38 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_risk_rank_is_computed_not_none": "test_risk_rank_is_computed_not_none()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L26 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_reopen_endpoint_test_reopen_non_remediated_is_conflict": "test_reopen_non_remediated_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L48 | neighbors=[test_finding_reopen_endpoint.py, _db_with()]
- "tests_test_finding_reopen_endpoint_test_reopen_remediated_finding_sets_open_and_audits": "test_reopen_remediated_finding_sets_open_and_audits()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L24 | neighbors=[test_finding_reopen_endpoint.py, _db_with()]
- "tests_test_finding_resolution_schema": "test_finding_resolution_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, test_finding_has_resolution_lifecycle_c…]
- "tests_test_finding_risk_rank_api": "test_finding_risk_rank_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L1 | neighbors=[85e4537 feat(risk-rank): expose risk_ra…, test_finding_schema_exposes_risk_rank()]
- "tests_test_finding_section_testfindingsection_test_backward_compatible_keys_kept": ".test_backward_compatible_keys_kept()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L95 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_section_testfindingsection_test_clean_host_shows_no_findings_honestly": ".test_clean_host_shows_no_findings_honestly()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L51 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_section_testfindingsection_test_each_finding_tagged_with_verified_provenance": ".test_each_finding_tagged_with_verified_provenance()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L88 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_section_testfindingsection_test_findings_are_ranked_worst_first": ".test_findings_are_ranked_worst_first()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L76 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_section_testfindingsection_test_vulnerable_host_shows_ranked_vulnerabilities": ".test_vulnerable_host_shows_ranked_vulnerabilities()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L61 | neighbors=[TestFindingSection, ._sum()]
- "tests_test_finding_verification_api": "test_finding_verification_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_api.py:L1 | neighbors=[72f68af feat(verification): expose veri…, test_finding_schema_exposes_verificatio…]
- "tests_test_finding_verification_schema": "test_finding_verification_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_schema.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, test_finding_has_verification_columns()]
- "tests_test_ftp_scanner_testftpfindings_test_anon_denied_is_silent": ".test_anon_denied_is_silent()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L70 | neighbors=[TestFTPFindings, ._fact()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-151.json

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
