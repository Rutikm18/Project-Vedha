# Node Description Batch 112 of 332

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

- "tests_test_exploitability_testtiers_test_epss_max_takes_the_worst_linked_cve": ".test_epss_max_takes_the_worst_linked_cve()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L102 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_high_epss_without_kev_is_likely": ".test_high_epss_without_kev_is_likely()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L79 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_kev_listed_is_actively_exploited": ".test_kev_listed_is_actively_exploited()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L74 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_kev_outranks_epss": ".test_kev_outranks_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L92 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_low_epss_is_unknown": ".test_low_epss_is_unknown()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L88 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_rule_with_no_linkage": ".test_rule_with_no_linkage()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L97 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exposed_services_test_exposed_findings_flow_through_detect_posture": "test_exposed_findings_flow_through_detect_posture()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L124 | neighbors=[test_exposed_services.py, _asset(), _fact()]
- "tests_test_exposed_services_testdetect_test_dedicated_ports_not_double_reported": ".test_dedicated_ports_not_double_reported()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L97 | neighbors=[TestDetect, _asset(), _fact()]
- "tests_test_exposed_services_testdetect_test_udp_ports_ignored": ".test_udp_ports_ignored()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L104 | neighbors=[TestDetect, _asset(), _fact()]
- "tests_test_fact_contract_test_corpus_survives_ingestion": "test_corpus_survives_ingestion()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L65 | neighbors=[test_fact_contract.py, The gate the name-level check above can…, _ingest_corpus()]
- "tests_test_finding_events_testmerge_stored": "._stored()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L98 | neighbors=[TestMerge, .test_sorted_oldest_first(), .test_stored_supersedes_synthesized_sam…]
- "tests_test_finding_events_testmerge_test_stored_supersedes_synthesized_same_type": ".test_stored_supersedes_synthesized_same_type()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L103 | neighbors=[TestMerge, ._stored(), ._synth()]
- "tests_test_finding_events_testpatchaudits": "TestPatchAudits" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L158 | neighbors=[test_finding_events.py, .test_manual_remediation_sets_close_met…, .test_status_change_records_event()]
- "tests_test_finding_events_testsynthesize_test_manual_remediation_event": ".test_manual_remediation_event()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L73 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_events_testsynthesize_test_no_reobserved_when_last_seen_equals_genesis": ".test_no_reobserved_when_last_seen_equals_genesis()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L63 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_events_testsynthesize_test_reobserved_when_last_seen_advances": ".test_reobserved_when_last_seen_advances()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L59 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_events_testsynthesize_test_terminal_confirmed_state_emitted": ".test_terminal_confirmed_state_emitted()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L84 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_events_testsynthesize_test_terminal_false_positive_state_emitted": ".test_terminal_false_positive_state_emitted()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L87 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_reopen_endpoint_db_with": "_db_with()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L15 | neighbors=[test_finding_reopen_endpoint.py, test_reopen_non_remediated_is_conflict(), test_reopen_remediated_finding_sets_ope…]
- "tests_test_fleet_jobs_test_filter_by_probe_and_engagement_run_without_error": "test_filter_by_probe_and_engagement_run_without_error()" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L54 | neighbors=[test_fleet_jobs.py, _scalars(), _user()]
- "tests_test_fleet_jobs_test_lists_jobs_with_probe_and_engagement_names": "test_lists_jobs_with_probe_and_engagement_names()" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L22 | neighbors=[test_fleet_jobs.py, _scalars(), _user()]
- "tests_test_fleet_jobs_test_running_filter_is_accepted": "test_running_filter_is_accepted()" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L46 | neighbors=[test_fleet_jobs.py, _scalars(), _user()]
- "tests_test_ftp_scanner_testpurelogic": "TestPureLogic" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L18 | neighbors=[test_ftp_scanner.py, .test_banner_software(), .test_parse_pasv()]
- "tests_test_host_discovery_mobile_testlocallyadministered": "TestLocallyAdministered" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L32 | neighbors=[test_host_discovery_mobile.py, .test_globally_unique_macs(), .test_randomized_phone_macs()]
- "tests_test_host_discovery_mobile_testvendorlookup": "TestVendorLookup" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L44 | neighbors=[test_host_discovery_mobile.py, .test_known_oui(), .test_unknown_oui()]
- "tests_test_host_health_testconfiguration": "TestConfiguration" | kind=code-symbol | source=probe/tests/test_host_health.py:L172 | neighbors=[test_host_health.py, .test_bad_threshold_falls_back_to_a_san…, .test_threshold_is_tunable_by_env()]
- "tests_test_host_health_testoperatorvisibility_test_offline_fact_carries_an_error_so_it_becomes_an_issue": ".test_offline_fact_carries_an_error_so_it_becomes_an_issue()" | kind=code-symbol | source=probe/tests/test_host_health.py:L286 | neighbors=[TestOperatorVisibility, _monitor(), _r()]
- "tests_test_host_health_testsafetyproperty_test_healthy_host_produces_no_facts_at_all": ".test_healthy_host_produces_no_facts_at_all()" | kind=code-symbol | source=probe/tests/test_host_health.py:L156 | neighbors=[TestSafetyProperty, _monitor(), _r()]
- "tests_test_host_health_testsafetyproperty_test_offline_host_stops_accumulating_observations": ".test_offline_host_stops_accumulating_observations()" | kind=code-symbol | source=probe/tests/test_host_health.py:L149 | neighbors=[TestSafetyProperty, _monitor(), _r()]
- "tests_test_host_health_testsafetyproperty_test_one_offline_host_does_not_implicate_its_peers": ".test_one_offline_host_does_not_implicate_its_peers()" | kind=code-symbol | source=probe/tests/test_host_health.py:L163 | neighbors=[TestSafetyProperty, _monitor(), _r()]
- "tests_test_host_health_testsilencedetection_test_rst_is_contact_not_silence": ".test_rst_is_contact_not_silence()" | kind=code-symbol | source=probe/tests/test_host_health.py:L37 | neighbors=[A closed port is the host's own stack a…, TestSilenceDetection, _r()]
- "tests_test_host_health_teststrikeaccounting": "TestStrikeAccounting" | kind=code-symbol | source=probe/tests/test_host_health.py:L65 | neighbors=[test_host_health.py, .test_strikes_must_be_consecutive(), .test_threshold_reached_raises_suspicio…]
- "tests_test_host_health_teststrikeaccounting_test_threshold_reached_raises_suspicion_only": ".test_threshold_reached_raises_suspicion_only()" | kind=code-symbol | source=probe/tests/test_host_health.py:L75 | neighbors=[TestStrikeAccounting, _monitor(), _r()]
- "tests_test_host_health_testverdict_test_host_that_stopped_answering_is_offline": ".test_host_that_stopped_answering_is_offline()" | kind=code-symbol | source=probe/tests/test_host_health.py:L98 | neighbors=[TestVerdict, _monitor(), _r()]
- "tests_test_host_health_testverdict_test_no_recheck_is_spent_below_threshold": ".test_no_recheck_is_spent_below_threshold()" | kind=code-symbol | source=probe/tests/test_host_health.py:L106 | neighbors=[TestVerdict, _monitor(), _r()]
- "tests_test_hw_bind_testgethwid": "TestGetHwId" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L11 | neighbors=[test_hw_bind.py, .test_deterministic_within_session(), .test_returns_32_hex_chars()]
- "tests_test_installer_contract_dry_run": "_dry_run()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L55 | neighbors=[test_installer_contract.py, test_installer_accepts_enroll_token_and…, test_installer_without_token_still_show…]
- "tests_test_integrations_testputintegration_test_create_encrypts_secret_and_masks_it": ".test_create_encrypts_secret_and_masks_it()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L38 | neighbors=[TestPutIntegration, _db(), _operator()]
- "tests_test_integrations_testputintegration_test_rejects_unknown_kind": ".test_rejects_unknown_kind()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L32 | neighbors=[TestPutIntegration, _db(), _operator()]
- "tests_test_integrations_testputintegration_test_update_without_secret_keeps_existing": ".test_update_without_secret_keeps_existing()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L52 | neighbors=[TestPutIntegration, _db(), _operator()]

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
