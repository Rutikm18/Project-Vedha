# Node Description Batch 167 of 336

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

- "tests_test_smtp_scanner_testsmtpfindings_test_hardened_is_silent": ".test_hardened_is_silent()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L62 | neighbors=[TestSMTPFindings, ._fact()]
- "tests_test_smtp_scanner_testsmtpfindings_test_user_enum_and_no_starttls": ".test_user_enum_and_no_starttls()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L55 | neighbors=[TestSMTPFindings, ._fact()]
- "tests_test_smtp_scanner_testsmtpscanner_test_no_smtp_filtered": ".test_no_smtp_filtered()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L44 | neighbors=[TestSMTPScanner, ._sc()]
- "tests_test_smtp_scanner_testsmtpscanner_test_open": ".test_open()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L36 | neighbors=[TestSMTPScanner, ._sc()]
- "tests_test_ssh_scanner_testevaluate_eval": "._eval()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L95 | neighbors=[TestEvaluate, _kexinit()]
- "tests_test_ssh_scanner_testfulldbcoverage_eval": "._eval()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L243 | neighbors=[TestFullDBCoverage, _kexinit()]
- "tests_test_ssh_scanner_testmainscriptsparity_test_main_scripts_scanner_and_findings_agree": ".test_main_scripts_scanner_and_findings_agree()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L316 | neighbors=[TestMainScriptsParity, _kexinit()]
- "tests_test_ssh_scanner_testnofalsepositives_eval": "._eval()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L272 | neighbors=[TestNoFalsePositives, _kexinit()]
- "tests_test_ssh_scanner_testparsekexinit_test_empty_language_list": ".test_empty_language_list()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L85 | neighbors=[TestParseKexinit, _kexinit()]
- "tests_test_ssh_scanner_testparsekexinit_test_handles_payload_without_leading_type_byte": ".test_handles_payload_without_leading_type_byte()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L79 | neighbors=[TestParseKexinit, _kexinit()]
- "tests_test_ssh_scanner_testparsekexinit_test_parses_all_name_lists": ".test_parses_all_name_lists()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L70 | neighbors=[TestParseKexinit, _kexinit()]
- "tests_test_ssh_scanner_testsshfindings_test_clean_server_raises_nothing": ".test_clean_server_raises_nothing()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L211 | neighbors=[TestSSHFindings, ._fact()]
- "tests_test_ssh_scanner_testsshfindings_test_terrapin_raises_finding": ".test_terrapin_raises_finding()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L206 | neighbors=[TestSSHFindings, ._fact()]
- "tests_test_ssh_scanner_testsshfindings_test_weak_algorithms_raise_finding": ".test_weak_algorithms_raise_finding()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L198 | neighbors=[TestSSHFindings, ._fact()]
- "tests_test_ssh_scanner_testsshscanner_test_weak_server_reports_open_with_failures": ".test_weak_server_reports_open_with_failures()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L169 | neighbors=[TestSSHScanner, _kexinit()]
- "tests_test_ssh_scanner_testsshstatustaxonomy_test_confirmed_ssh_open_with_parsed_banner": ".test_confirmed_ssh_open_with_parsed_banner()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L361 | neighbors=[TestSSHStatusTaxonomy, _kexinit()]
- "tests_test_ssh_scanner_testterrapin_test_chacha20_without_strict_kex_is_vulnerable": ".test_chacha20_without_strict_kex_is_vulnerable()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L153 | neighbors=[TestTerrapin, _kexinit()]
- "tests_test_ssh_scanner_testterrapin_test_strict_kex_present_is_not_vulnerable": ".test_strict_kex_present_is_not_vulnerable()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L145 | neighbors=[TestTerrapin, _kexinit()]
- "tests_test_ssh_scanner_testterrapinfidelity_test_cbc_plus_etm_is_vulnerable_without_strict_kex": ".test_cbc_plus_etm_is_vulnerable_without_strict_kex()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L302 | neighbors=[TestTerrapinFidelity, ._ev()]
- "tests_test_ssh_scanner_testterrapinfidelity_test_cbc_without_etm_mac_is_not_terrapin": ".test_cbc_without_etm_mac_is_not_terrapin()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L307 | neighbors=[TestTerrapinFidelity, ._ev()]
- "tests_test_ssh_scanner_testterrapinfidelity_test_chacha20_without_openssh_suffix_still_vulnerable": ".test_chacha20_without_openssh_suffix_still_vulnerable()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L296 | neighbors=[TestTerrapinFidelity, ._ev()]
- "tests_test_stage2_reconcile_test_reap_stale_runs_marks_running_as_failed": "test_reap_stale_runs_marks_running_as_failed()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L175 | neighbors=[test_stage2_reconcile.py, _CM]
- "tests_test_stage2_reconcile_test_write_heartbeat_upserts": "test_write_heartbeat_upserts()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L195 | neighbors=[test_stage2_reconcile.py, _CM]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_closed_and_filtered_suppressed_by_default": ".test_closed_and_filtered_suppressed_by_default()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L396 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_open_result_carries_signals_and_os_guess": ".test_open_result_carries_signals_and_os_guess()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L354 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_open_without_signals_has_no_os_guess": ".test_open_without_signals_has_no_os_guess()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L391 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_os_guess_is_tagged_tcp_derived_not_icmp": ".test_os_guess_is_tagged_tcp_derived_not_icmp()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L370 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_p0f_stack_label_from_harvested_option_layout": ".test_p0f_stack_label_from_harvested_option_layout()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L380 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testbuildresultsenrichment_test_windows_ttl_maps_to_windows": ".test_windows_ttl_maps_to_windows()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L364 | neighbors=[TestBuildResultsEnrichment, ._scanner()]
- "tests_test_syn_scanner_testparsepacketsignals_test_window_ttl_mss_surfaced": ".test_window_ttl_mss_surfaced()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L337 | neighbors=[TestParsePacketSignals, _synack_with_options()]
- "tests_test_syn_scanner_testsynretransmit_test_answered_ports_are_not_retransmitted": ".test_answered_ports_are_not_retransmitted()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L248 | neighbors=[TestSynRetransmit, ._patch()]
- "tests_test_syn_scanner_testsynretransmit_test_retries_zero_sends_one_syn_per_port": ".test_retries_zero_sends_one_syn_per_port()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L278 | neighbors=[TestSynRetransmit, ._patch()]
- "tests_test_syn_scanner_testsynretransmit_test_silent_ports_are_retried_retries_plus_one_times": ".test_silent_ports_are_retried_retries_plus_one_times()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L233 | neighbors=[TestSynRetransmit, ._patch()]
- "tests_test_syn_scanner_testverifyreplycookie_test_reply_from_other_host_fails": ".test_reply_from_other_host_fails()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L129 | neighbors=[TestVerifyReplyCookie, ._make_synack_reply()]
- "tests_test_syn_scanner_testverifyreplycookie_test_valid_cookie_verifies": ".test_valid_cookie_verifies()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L119 | neighbors=[TestVerifyReplyCookie, ._make_synack_reply()]
- "tests_test_syn_scanner_testverifyreplycookie_test_wrong_ack_fails": ".test_wrong_ack_fails()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L124 | neighbors=[TestVerifyReplyCookie, ._make_synack_reply()]
- "tests_test_task_runner_fake_run_scan": "_fake_run_scan()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L12 | neighbors=[test_task_runner.py, Return a minimal successful result with…]
- "tests_test_task_runner_runner": "runner()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L37 | neighbors=[test_task_runner.py, TaskRunner with no-op dependencies (no …]
- "tests_test_tier1_correlations_test_anon_data_exposure_cluster": "test_anon_data_exposure_cluster()" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L17 | neighbors=[test_tier1_correlations.py, _run()]
- "tests_test_tier1_correlations_test_mgmt_plane_exposed_on_cipher_zero_alone": "test_mgmt_plane_exposed_on_cipher_zero_alone()" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L49 | neighbors=[test_tier1_correlations.py, _run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-166.json

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
