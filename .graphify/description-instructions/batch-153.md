# Node Description Batch 154 of 330

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

- "tests_test_job_cancel_test_current_user_has_no_email_field": "test_current_user_has_no_email_field()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L224 | neighbors=[test_job_cancel.py, Pins the reason this endpoint may not r…]
- "tests_test_loaders_testloadepsserrors_test_epss_get_returns_none_for_unknown_cve": ".test_epss_get_returns_none_for_unknown_cve()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L172 | neighbors=[TestLoadEpssErrors, _valid_epss()]
- "tests_test_loaders_testloadepsserrors_test_valid_epss_loads": ".test_valid_epss_loads()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L164 | neighbors=[TestLoadEpssErrors, _valid_epss()]
- "tests_test_loaders_testloadkeverrors_test_valid_kev_loads": ".test_valid_kev_loads()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L138 | neighbors=[TestLoadKevErrors, _valid_kev()]
- "tests_test_loaders_testloadsnapshoterrors_test_error_message_mentions_re_sync": ".test_error_message_mentions_re_sync()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L101 | neighbors=[The FileNotFoundError message should me…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_malformed_json_raises": ".test_malformed_json_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L77 | neighbors=[Completely broken JSON must propagate a…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_missing_file_raises_file_not_found": ".test_missing_file_raises_file_not_found()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L59 | neighbors=[A path that doesn't exist must raise Fi…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_missing_required_key_raises": ".test_missing_required_key_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L85 | neighbors=[A JSON file that is valid JSON but miss…, TestLoadSnapshotErrors]
- "tests_test_loaders_valid_kev": "_valid_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L42 | neighbors=[test_loaders.py, .test_valid_kev_loads()]
- "tests_test_main_scripts_completeness_test_fallback_count_based_when_no_requested_set": "test_fallback_count_based_when_no_requested_set()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L64 | neighbors=[test_main_scripts_completeness.py, _rec()]
- "tests_test_main_scripts_correlation_test_correlations_are_evidence_backed": "test_correlations_are_evidence_backed()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L91 | neighbors=[test_main_scripts_correlation.py, _run()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_adaptive_estimator_is_shared_and_adapts_down_from_fast_rtts": ".test_adaptive_estimator_is_shared_and_adapts_down_from_fast_rtts()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L195 | neighbors=[TestDefaultsAndAdaptiveTimeout, _mk_scanner()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_default_ports_are_nmap_top100_not_the_35_port_set": ".test_default_ports_are_nmap_top100_not_the_35_port_set()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L187 | neighbors=[TestDefaultsAndAdaptiveTimeout, _scope()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_fixed_timeout_flag_disables_the_estimator": ".test_fixed_timeout_flag_disables_the_estimator()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L214 | neighbors=[TestDefaultsAndAdaptiveTimeout, _mk_scanner()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_all_65535_ports_scheduled_exactly_once": ".test_all_65535_ports_scheduled_exactly_once()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L103 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_concurrency_is_bounded_by_the_pool": ".test_concurrency_is_bounded_by_the_pool()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L117 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner()]
- "tests_test_main_scripts_datastore_probe_test_elasticsearch_and_couchdb_win_over_generic_http": "test_elasticsearch_and_couchdb_win_over_generic_http()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L31 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_datastore_probe_test_memcached_version_and_stat_identify_as_memcached": "test_memcached_version_and_stat_identify_as_memcached()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L26 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_datastore_probe_test_redis_info_and_noauth_identify_as_redis": "test_redis_info_and_noauth_identify_as_redis()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L21 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_device_testclassifyfromresults": "TestClassifyFromResults" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L71 | neighbors=[test_main_scripts_device.py, .test_extracts_signals_from_scan_result…]
- "tests_test_main_scripts_errno_test_definitive_states": "test_definitive_states()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L21 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_errno_test_describe_os_error_is_fully_debuggable": "test_describe_os_error_is_fully_debuggable()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L49 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_errno_test_scanner_side_errors_are_error_not_filtered": "test_scanner_side_errors_are_error_not_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L28 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_errno_test_unknown_errno_is_self_identifying_and_never_filtered": "test_unknown_errno_is_self_identifying_and_never_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L36 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_findings_test_accepts_scanresult_objects_not_just_dicts": "test_accepts_scanresult_objects_not_just_dicts()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L322 | neighbors=[test_main_scripts_findings.py, _ids()]
- "tests_test_main_scripts_findings_test_confirmed_and_port_hint_do_not_double_report": "test_confirmed_and_port_hint_do_not_double_report()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L239 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_confirmed_ftp_cleartext_is_high_confidence": "test_confirmed_ftp_cleartext_is_high_confidence()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L230 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_confirmed_redis_is_high_confidence_even_on_nonstandard_port": "test_confirmed_redis_is_high_confidence_even_on_nonstandard_port()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L212 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_dangerous_http_methods_medium": "test_dangerous_http_methods_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L250 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_every_finding_is_evidence_backed": "test_every_finding_is_evidence_backed()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L305 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_exposed_redis_is_high_exposure_medium_confidence": "test_exposed_redis_is_high_exposure_medium_confidence()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L173 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_findings_are_deduped_by_rule_target_port": "test_findings_are_deduped_by_rule_target_port()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L285 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_findings_sorted_most_severe_first": "test_findings_sorted_most_severe_first()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L291 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_missing_security_headers_is_low": "test_missing_security_headers_is_low()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L262 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_no_finding_carries_a_cve_id": "test_no_finding_carries_a_cve_id()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L299 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed": "test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L223 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_rdp_exposed_medium": "test_rdp_exposed_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L180 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_server_version_disclosure_is_info": "test_server_version_disclosure_is_info()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L256 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_smbv1_enabled_is_high": "test_smbv1_enabled_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L103 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_snmp_default_community_is_high": "test_snmp_default_community_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L124 | neighbors=[test_main_scripts_findings.py, _run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-153.json

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
