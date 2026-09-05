# Node Description Batch 82 of 336

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

- "tests_test_dns_scanner_testdnsscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L98 | neighbors=[TestDNSScanner, .test_dnspython_missing_is_error(), .test_no_dns_is_filtered(), .test_zone_transfer_open()]
- "tests_test_dualstack_fallback_testrdpfallback": "TestRdpFallback" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L135 | neighbors=[test_dualstack_fallback.py, .test_none_when_no_family_speaks_rdp(), .test_probes_next_family_when_first_is_…, .test_unresolvable_host_is_survivable()]
- "tests_test_dualstack_fallback_testtlsfingerprintfallback": "TestTlsFingerprintFallback" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L169 | neighbors=[test_dualstack_fallback.py, .test_none_when_no_family_speaks_tls(), .test_unresolvable_host_is_survivable(), .test_uses_the_family_that_actually_spe…]
- "tests_test_engine_bridge_resolution": "test_engine_bridge_resolution.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_resolution.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6bb51ab feat: add detection-explain end…, 8cf23c2 feat(resolution): wire coverage…, test_run_records_coverage_and_invokes_r…]
- "tests_test_exploit_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L38 | neighbors=[test_exploit_engine.py, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_exploitability_testapplytofindings_test_kev_raises_the_score_and_priority": ".test_kev_raises_the_score_and_priority()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L111 | neighbors=[TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_exploitability_testapplytofindings_test_reason_is_recorded_in_notes": ".test_reason_is_recorded_in_notes()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L131 | neighbors=[TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_exploitability_testapplytofindings_test_score_is_capped_at_100": ".test_score_is_capped_at_100()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L126 | neighbors=[TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_exploitability_testapplytofindings_test_unlinked_finding_is_untouched": ".test_unlinked_finding_is_untouched()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L136 | neighbors=[TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_exploitability_testneverclaimsthecveispresent": "TestNeverClaimsTheCveIsPresent" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L45 | neighbors=[test_exploitability.py, .test_a_link_not_on_the_kev_list_is_kep…, .test_every_link_states_a_relation(), .test_refs_carry_the_relation_and_kev_s…]
- "tests_test_exploitability_testneverclaimsthecveispresent_test_a_link_not_on_the_kev_list_is_kept_but_marked": ".test_a_link_not_on_the_kev_list_is_kept_but_marked()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L61 | neighbors=[A stale or narrowed KEV snapshot must b…, TestNeverClaimsTheCveIsPresent, _epss(), _kev()]
- "tests_test_exposed_services_testdetect_test_backdoor_4444_is_high_internal": ".test_backdoor_4444_is_high_internal()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L76 | neighbors=[TestDetect, _asset(), _by_port(), _fact()]
- "tests_test_exposed_services_testdetect_test_banner_carried_as_evidence": ".test_banner_carried_as_evidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L91 | neighbors=[TestDetect, _asset(), _by_port(), _fact()]
- "tests_test_exposed_services_testdetect_test_internet_facing_escalates_severity": ".test_internet_facing_escalates_severity()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L82 | neighbors=[TestDetect, _asset(), _by_port(), _fact()]
- "tests_test_exposed_services_testdetect_test_real_lab_host_produces_expected_findings": ".test_real_lab_host_produces_expected_findings()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L109 | neighbors=[TestDetect, _asset(), _by_port(), _fact()]
- "tests_test_exposed_services_testobservedservicesignals_test_detect_uses_service_label_and_flag": ".test_detect_uses_service_label_and_flag()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L157 | neighbors=[TestObservedServiceSignals, _asset(), _by_port(), _fact()]
- "tests_test_exposed_services_testporthypothesiscontradiction_test_detect_records_the_observed_product": ".test_detect_records_the_observed_product()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L223 | neighbors=[TestPortHypothesisContradiction, _asset(), _by_port(), _fact()]
- "tests_test_fact_contract_emitted_paths_by_scanner": "_emitted_paths_by_scanner()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L34 | neighbors=[test_fact_contract.py, Map scanner -> set of top-level data ke…, test_every_rule_input_is_emitted_by_its…, test_report_unconsumed_evidence()]
- "tests_test_fact_contract_ingest_corpus": "_ingest_corpus()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L46 | neighbors=[test_fact_contract.py, _load_corpus(), Run the corpus through the REAL ingeste…, test_corpus_survives_ingestion()]
- "tests_test_fact_contract_test_every_rule_input_is_emitted_by_its_scanner": "test_every_rule_input_is_emitted_by_its_scanner()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L82 | neighbors=[test_fact_contract.py, The gate: for every rule, every declare…, _emitted_paths_by_scanner(), _load_corpus()]
- "tests_test_fact_contract_test_report_unconsumed_evidence": "test_report_unconsumed_evidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L102 | neighbors=[test_fact_contract.py, Reverse direction, informational: data …, _emitted_paths_by_scanner(), _load_corpus()]
- "tests_test_finding_events_testmerge_synth": "._synth()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L93 | neighbors=[TestMerge, .test_labels_attached(), .test_sorted_oldest_first(), .test_stored_supersedes_synthesized_sam…]
- "tests_test_finding_events_testmerge_test_sorted_oldest_first": ".test_sorted_oldest_first()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L111 | neighbors=[TestMerge, ._stored(), ._synth(), _types()]
- "tests_test_finding_schema": "test_finding_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_finding_patch_accepts_documented_m…, test_finding_patch_rejects_risk_score_a…, test_finding_summary_exposes_full_open_…]
- "tests_test_fleet_jobs_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L17 | neighbors=[test_fleet_jobs.py, test_filter_by_probe_and_engagement_run…, test_lists_jobs_with_probe_and_engageme…, test_running_filter_is_accepted()]
- "tests_test_fleet_jobs_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L13 | neighbors=[test_fleet_jobs.py, test_filter_by_probe_and_engagement_run…, test_lists_jobs_with_probe_and_engageme…, test_running_filter_is_accepted()]
- "tests_test_ftp_scanner_testftpfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L54 | neighbors=[TestFTPFindings, .test_anon_denied_is_silent(), .test_anon_login_only_is_medium(), .test_anon_read_is_high()]
- "tests_test_ftp_scanner_testftpscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L29 | neighbors=[TestFTPScanner, .test_anon_login_and_read_open(), .test_ftp_present_anon_denied_open_but_…, .test_no_ftp_filtered()]
- "tests_test_host_discovery_udp_testparsenbstat": "TestParseNbstat" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L37 | neighbors=[test_host_discovery_udp.py, .test_msbrowse_control_chars_dropped(), .test_names_hostname_domain_mac(), .test_not_a_response()]
- "tests_test_host_health_testoperatorvisibility": "TestOperatorVisibility" | kind=code-symbol | source=probe/tests/test_host_health.py:L280 | neighbors=[test_host_health.py, An offline host must reach the operator…, .test_flaky_note_is_not_an_error(), .test_offline_fact_carries_an_error_so_…]
- "tests_test_host_health_testoperatorvisibility_test_flaky_note_is_not_an_error": ".test_flaky_note_is_not_an_error()" | kind=code-symbol | source=probe/tests/test_host_health.py:L294 | neighbors=[A host that is merely filtered is not a…, TestOperatorVisibility, _monitor(), _r()]
- "tests_test_host_health_testsafetyproperty_test_offline_fact_marks_the_scan_incomplete_and_names_what_was_skipped": ".test_offline_fact_marks_the_scan_incomplete_and_names_what_was_skipped()" | kind=code-symbol | source=probe/tests/test_host_health.py:L131 | neighbors=[The whole point: 'we stopped early' mus…, TestSafetyProperty, _monitor(), _r()]
- "tests_test_host_health_teststrikeaccounting_test_strikes_must_be_consecutive": ".test_strikes_must_be_consecutive()" | kind=code-symbol | source=probe/tests/test_host_health.py:L66 | neighbors=[A healthy host with many inapplicable b…, TestStrikeAccounting, _monitor(), _r()]
- "tests_test_host_health_testverdict_test_firewalled_host_that_still_answers_is_flaky_not_offline": ".test_firewalled_host_that_still_answers_is_flaky_not_offline()" | kind=code-symbol | source=probe/tests/test_host_health.py:L84 | neighbors=[The headline false positive: silence fr…, TestVerdict, _monitor(), _r()]
- "tests_test_host_health_testverdict_test_flaky_host_can_be_suspected_again_later": ".test_flaky_host_can_be_suspected_again_later()" | kind=code-symbol | source=probe/tests/test_host_health.py:L121 | neighbors=[One false alarm must not disable the ch…, TestVerdict, _monitor(), _r()]
- "tests_test_integration_teststartupgauntlet": "TestStartupGauntlet" | kind=code-symbol | source=probe/tests/test_integration.py:L431 | neighbors=[test_integration.py, Phase 5: startup gauntlet checks., .test_gauntlet_hw_bind_blocks(), .test_gauntlet_skips_in_dev_mode()]
- "tests_test_integration_testtaskrunnerwithencryptedscope": "TestTaskRunnerWithEncryptedScope" | kind=code-symbol | source=probe/tests/test_integration.py:L100 | neighbors=[test_integration.py, Phase 4 + Phase 1: TaskRunner receives …, .test_decrypts_encrypted_scope_from_job…, .test_falls_back_when_decryption_fails()]
- "tests_test_integration_testtransportwithidentity": "TestTransportWithIdentity" | kind=code-symbol | source=probe/tests/test_integration.py:L238 | neighbors=[test_integration.py, Phase 4 + Phase 1: Transport sends publ…, .test_register_sends_public_key(), .test_register_without_public_key()]
- "tests_test_integrations_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L21 | neighbors=[test_integrations.py, .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]
- "tests_test_integrations_testputintegration": "TestPutIntegration" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L31 | neighbors=[test_integrations.py, .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-081.json

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
