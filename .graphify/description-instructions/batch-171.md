# Node Description Batch 172 of 380

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

- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_unique": ".test_generate_dns_callback_token_unique()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L298 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_safety_meterpreter_raises": ".test_validate_safety_meterpreter_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L275 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_get_job_status_running": ".test_get_job_status_running()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L218 | neighbors=[TestMetasploitRPCClient, ._make_client()]
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
- "tests_test_finding_compliance_test_default_creds_maps_to_hipaa_authentication": "test_default_creds_maps_to_hipaa_authentication()" | kind=code-symbol | source=manager/backend/tests/test_finding_compliance.py:L50 | neighbors=[test_finding_compliance.py, _f()]
- "tests_test_finding_compliance_test_default_creds_maps_to_pci_default_accounts": "test_default_creds_maps_to_pci_default_accounts()" | kind=code-symbol | source=manager/backend/tests/test_finding_compliance.py:L37 | neighbors=[test_finding_compliance.py, _f()]
- "tests_test_finding_compliance_test_each_ref_has_controls_and_a_rationale": "test_each_ref_has_controls_and_a_rationale()" | kind=code-symbol | source=manager/backend/tests/test_finding_compliance.py:L26 | neighbors=[test_finding_compliance.py, _f()]
- "tests_test_finding_compliance_test_every_finding_maps_to_all_five_frameworks": "test_every_finding_maps_to_all_five_frameworks()" | kind=code-symbol | source=manager/backend/tests/test_finding_compliance.py:L20 | neighbors=[test_finding_compliance.py, _f()]
- "tests_test_finding_compliance_test_generic_and_empty_findings_still_map_all_frameworks_nonempty": "test_generic_and_empty_findings_still_map_all_frameworks_nonempty()" | kind=code-symbol | source=manager/backend/tests/test_finding_compliance.py:L56 | neighbors=[test_finding_compliance.py, _f()]
- "tests_test_finding_compliance_test_missing_patch_maps_to_nist_flaw_remediation": "test_missing_patch_maps_to_nist_flaw_remediation()" | kind=code-symbol | source=manager/backend/tests/test_finding_compliance.py:L42 | neighbors=[test_finding_compliance.py, _f()]
- "tests_test_finding_compliance_test_weak_tls_maps_to_pci_transmission_control": "test_weak_tls_maps_to_pci_transmission_control()" | kind=code-symbol | source=manager/backend/tests/test_finding_compliance.py:L32 | neighbors=[test_finding_compliance.py, _f()]
- "tests_test_finding_content_test_active_exploitation_adds_urgency_to_business_impact": "test_active_exploitation_adds_urgency_to_business_impact()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L98 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_business_impact_scales_up_for_a_critical_asset": "test_business_impact_scales_up_for_a_critical_asset()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L91 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_cves_are_woven_into_technical_details": "test_cves_are_woven_into_technical_details()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L104 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_every_category_yields_nonempty_prose": "test_every_category_yields_nonempty_prose()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L48 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_kev_makes_it_weaponized_and_actively_exploited": "test_kev_makes_it_weaponized_and_actively_exploited()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L70 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_nested_enrichment_kev_is_honoured": "test_nested_enrichment_kev_is_honoured()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L76 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_overrides_take_precedence_field_by_field": "test_overrides_take_precedence_field_by_field()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L109 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_to_dict_is_api_shaped": "test_to_dict_is_api_shaped()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L116 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_unvalidated_finding_uses_the_exact_honest_line": "test_unvalidated_finding_uses_the_exact_honest_line()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L56 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_content_test_validated_finding_is_stated_plainly_not_hedged": "test_validated_finding_is_stated_plainly_not_hedged()" | kind=code-symbol | source=manager/backend/tests/test_finding_content.py:L63 | neighbors=[test_finding_content.py, _f()]
- "tests_test_finding_enrichment_test_detail_enrichment_honours_content_overrides": "test_detail_enrichment_honours_content_overrides()" | kind=code-symbol | source=manager/backend/tests/test_finding_enrichment.py:L87 | neighbors=[test_finding_enrichment.py, _finding()]
- "tests_test_finding_enrichment_test_detail_enrichment_populates_all_sections": "test_detail_enrichment_populates_all_sections()" | kind=code-symbol | source=manager/backend/tests/test_finding_enrichment.py:L68 | neighbors=[test_finding_enrichment.py, _finding()]
- "tests_test_finding_enrichment_test_detail_enrichment_scales_business_impact_by_criticality": "test_detail_enrichment_scales_business_impact_by_criticality()" | kind=code-symbol | source=manager/backend/tests/test_finding_enrichment.py:L81 | neighbors=[test_finding_enrichment.py, _finding()]
- "tests_test_finding_enrichment_test_detail_enrichment_survives_missing_evidence": "test_detail_enrichment_survives_missing_evidence()" | kind=code-symbol | source=manager/backend/tests/test_finding_enrichment.py:L97 | neighbors=[test_finding_enrichment.py, _finding()]
- "tests_test_finding_enrichment_test_findingout_computes_maturity_and_active_from_evidence": "test_findingout_computes_maturity_and_active_from_evidence()" | kind=code-symbol | source=manager/backend/tests/test_finding_enrichment.py:L44 | neighbors=[test_finding_enrichment.py, _out()]
- "tests_test_finding_enrichment_test_findingout_defaults_to_theoretical_when_no_signal": "test_findingout_defaults_to_theoretical_when_no_signal()" | kind=code-symbol | source=manager/backend/tests/test_finding_enrichment.py:L50 | neighbors=[test_finding_enrichment.py, _out()]
- "tests_test_finding_enrichment_test_findingout_list_leaves_heavy_prose_null": "test_findingout_list_leaves_heavy_prose_null()" | kind=code-symbol | source=manager/backend/tests/test_finding_enrichment.py:L56 | neighbors=[test_finding_enrichment.py, _out()]
- "tests_test_finding_events_testeventtypeforstatus": "TestEventTypeForStatus" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L124 | neighbors=[test_finding_events.py, .test_maps_status_to_specific_event()]
- "tests_test_finding_events_testmerge_test_labels_attached": ".test_labels_attached()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L118 | neighbors=[TestMerge, ._synth()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-171.json

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
