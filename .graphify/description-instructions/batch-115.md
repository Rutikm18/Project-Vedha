# Node Description Batch 116 of 332

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

- "tests_test_posture_rules_testudphonesty_test_no_reply_udp_raises_nothing": ".test_no_reply_udp_raises_nothing()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L125 | neighbors=[TestUdpHonesty, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_deprecated_tls_version": ".test_deprecated_tls_version()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L90 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_modern_only_tls_raises_nothing": ".test_modern_only_tls_raises_nothing()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L106 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_rdp_no_nla_confirmed_high_and_unauth": ".test_rdp_no_nla_confirmed_high_and_unauth()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L82 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_self_signed_and_expired_cert": ".test_self_signed_and_expired_cert()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L112 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_smbv1_is_confirmed_critical": ".test_smbv1_is_confirmed_critical()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L76 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_trace_testbehaviourpreserved_test_dedup_still_one_finding_per_rule_port_but_trace_per_eval": ".test_dedup_still_one_finding_per_rule_port_but_trace_per_eval()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L129 | neighbors=[TestBehaviourPreserved, _asset(), _fact()]
- "tests_test_posture_trace_testnoevidence": "TestNoEvidence" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L77 | neighbors=[test_posture_trace.py, .test_no_evidence_is_asset_scoped_not_p…, .test_scanner_absent_yields_no_evidence…]
- "tests_test_posture_trace_testnoevidence_test_no_evidence_is_asset_scoped_not_per_fact": ".test_no_evidence_is_asset_scoped_not_per_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L84 | neighbors=[TestNoEvidence, _asset(), _fact()]
- "tests_test_posture_trace_testsummarize": "TestSummarize" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L141 | neighbors=[test_posture_trace.py, .test_every_verdict_is_reachable(), .test_summarize_counts_blind_rules()]
- "tests_test_posture_trace_testsummarize_test_every_verdict_is_reachable": ".test_every_verdict_is_reachable()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L153 | neighbors=[TestSummarize, _asset(), _fact()]
- "tests_test_posture_trace_testsummarize_test_summarize_counts_blind_rules": ".test_summarize_counts_blind_rules()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L142 | neighbors=[TestSummarize, _asset(), _fact()]
- "tests_test_printer_scanner_testprinterscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L35 | neighbors=[TestPrinterScanner, .test_no_printer_filtered(), .test_open()]
- "tests_test_probe_core_testassetmergecredentialed": "TestAssetMergeCredentialed" | kind=code-symbol | source=probe/tests/test_probe_core.py:L568 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory()]
- "tests_test_probe_core_testassetmergecredentialed_test_ssh_inventory": ".test_ssh_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L569 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergecredentialed_test_windows_inventory": ".test_windows_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L576 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery": "TestAssetMergeHostDiscovery" | kind=code-symbol | source=probe/tests/test_probe_core.py:L502 | neighbors=[test_probe_core.py, .test_alive_sets_timestamp(), .test_responding_ports()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_alive_sets_timestamp": ".test_alive_sets_timestamp()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L503 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_responding_ports": ".test_responding_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L510 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergepassivecollect_test_passive_facts_appended": ".test_passive_facts_appended()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L584 | neighbors=[TestAssetMergePassiveCollect, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan": "TestAssetMergePortScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L521 | neighbors=[test_probe_core.py, .test_tcp_open(), .test_udp_uncertain()]
- "tests_test_probe_core_testassetmergeportscan_test_tcp_open": ".test_tcp_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L522 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan_test_udp_uncertain": ".test_udp_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L528 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeservicebanner_test_banner_stored": ".test_banner_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L535 | neighbors=[TestAssetMergeServiceBanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergesmbscan_test_smb_state_host_level": ".test_smb_state_host_level()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L560 | neighbors=[TestAssetMergeSmbScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergetlsscan_test_tls_facts_stored": ".test_tls_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L544 | neighbors=[TestAssetMergeTlsScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeunknownscanner_test_unknown_scanner_ignored": ".test_unknown_scanner_ignored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L593 | neighbors=[TestAssetMergeUnknownScanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergewebscan_test_web_facts_stored": ".test_web_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L552 | neighbors=[TestAssetMergeWebScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetopenportsfordeepscan": "TestAssetOpenPortsForDeepScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L489 | neighbors=[test_probe_core.py, .test_empty(), .test_only_open()]
- "tests_test_probe_core_testcapabilities": "TestCapabilities" | kind=code-symbol | source=probe/tests/test_probe_core.py:L930 | neighbors=[test_probe_core.py, .test_capabilities_sorted(), .test_known_scan_types()]
- "tests_test_probe_simple_approve_testsimpleapproveinput": "TestSimpleApproveInput" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L38 | neighbors=[test_probe_simple_approve.py, .test_defaults_are_all_optional(), .test_overrides_accepted()]
- "tests_test_project_time_testfilestamp": "TestFileStamp" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L60 | neighbors=[test_project_time.py, .test_filename_safe(), .test_no_z_suffix_on_local_time()]
- "tests_test_raw_facts_sr": "_sr()" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L21 | neighbors=[test_raw_facts.py, test_raw_facts_filter_by_scanner(), test_raw_facts_grouped_by_scanner()]
- "tests_test_raw_facts_test_raw_facts_bounds_and_no_results": "test_raw_facts_bounds_and_no_results()" | kind=code-symbol | source=manager/backend/tests/test_raw_facts.py:L72 | neighbors=[test_raw_facts.py, _scalars(), _user()]
- "tests_test_reaper_objects": "_objects()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L8 | neighbors=[test_reaper.py, test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_reference_testshape_test_uses_the_rows_own_date_not_today": ".test_uses_the_rows_own_date_not_today()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L35 | neighbors=[A backfilled reference must match what …, TestShape, _at()]
- "tests_test_reference_teststability": "TestStability" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L86 | neighbors=[test_reference.py, .test_different_rows_get_different_refe…, .test_the_same_row_always_gets_the_same…]
- "tests_test_reference_teststability_test_the_same_row_always_gets_the_same_reference": ".test_the_same_row_always_gets_the_same_reference()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L87 | neighbors=[It is quoted in tickets — it must not m…, TestStability, _at()]
- "tests_test_reference_testtellingthemapart": "TestTellingThemApart" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L74 | neighbors=[test_reference.py, .test_a_reference_is_distinguishable_fr…, .test_an_unregistered_prefix_is_not_our…]
- "tests_test_remediation_generator_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L26 | neighbors=[test_remediation_generator.py, .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-115.json

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
