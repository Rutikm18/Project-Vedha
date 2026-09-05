# Node Description Batch 113 of 336

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
- "tests_test_ipmi_scanner_resp": "_resp()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L18 | neighbors=[test_ipmi_scanner.py, .test_parse_nonzero_status_is_safe(), .test_parse_status_zero_is_cipher_zero()]
- "tests_test_ipmi_scanner_testipmifindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L63 | neighbors=[TestIPMIFindings, .test_cipher_zero_is_critical(), .test_reachable_bmc_is_low()]
- "tests_test_ipmi_scanner_testipmiscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L45 | neighbors=[TestIPMIScanner, .test_cipher_zero_open(), .test_no_ipmi_filtered()]
- "tests_test_ipv6_wiring_test_disabled_by_default": "test_disabled_by_default()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L136 | neighbors=[test_ipv6_wiring.py, Only the scan types that opt in pay for…, _wire()]
- "tests_test_ipv6_wiring_test_discovery_failure_does_not_abort_the_engagement": "test_discovery_failure_does_not_abort_the_engagement()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L149 | neighbors=[test_ipv6_wiring.py, _run(), _wire()]
- "tests_test_ipv6_wiring_test_in_scope_neighbour_is_added_and_scanned": "test_in_scope_neighbour_is_added_and_scanned()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L102 | neighbors=[test_ipv6_wiring.py, _run(), _wire()]
- "tests_test_ipv6_wiring_test_the_fact_records_both_sides": "test_the_fact_records_both_sides()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L120 | neighbors=[test_ipv6_wiring.py, _run(), _wire()]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed_test_per_request_info_lines_are_suppressed": ".test_per_request_info_lines_are_suppressed()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L91 | neighbors=[The actual regression: one INFO line pe…, TestPollingNoiseIsSuppressed, ._configure()]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed_test_transport_errors_still_surface": ".test_transport_errors_still_surface()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L96 | neighbors=[Quieting must not hide a genuinely unre…, TestPollingNoiseIsSuppressed, ._configure()]
- "tests_test_job_cancel_testqueuelimit_test_pending_count_helper_counts": ".test_pending_count_helper_counts()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L187 | neighbors=[TestQueueLimit, _count(), _db()]
- "tests_test_loaders_testloadsnapshoterrors_test_content_hash_mismatch_raises_value_error": ".test_content_hash_mismatch_raises_value_error()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L65 | neighbors=[A snapshot whose records don't match th…, TestLoadSnapshotErrors, _valid_snapshot()]
- "tests_test_loaders_testloadsnapshoterrors_test_hash_mismatch_message_truncates_hash": ".test_hash_mismatch_message_truncates_hash()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L107 | neighbors=[The ValueError for a hash mismatch must…, TestLoadSnapshotErrors, _valid_snapshot()]
- "tests_test_loaders_testloadsnapshoterrors_test_valid_snapshot_loads_cleanly": ".test_valid_snapshot_loads_cleanly()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L93 | neighbors=[A well-formed snapshot must load withou…, TestLoadSnapshotErrors, _write_snapshot()]
- "tests_test_loaders_valid_epss": "_valid_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L46 | neighbors=[test_loaders.py, .test_epss_get_returns_none_for_unknown…, .test_valid_epss_loads()]
- "tests_test_loaders_write_snapshot": "_write_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L38 | neighbors=[test_loaders.py, .test_valid_snapshot_loads_cleanly(), _valid_snapshot()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-112.json

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
