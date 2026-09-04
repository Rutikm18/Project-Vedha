# Node Description Batch 166 of 332

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
- "tests_test_tier1_correlations_test_mgmt_plane_needs_two_when_no_cipher_zero": "test_mgmt_plane_needs_two_when_no_cipher_zero()" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L56 | neighbors=[test_tier1_correlations.py, _run()]
- "tests_test_tier1_correlations_test_single_anon_finding_does_not_correlate": "test_single_anon_finding_does_not_correlate()" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L30 | neighbors=[test_tier1_correlations.py, _run()]
- "tests_test_tier1_correlations_test_user_enum_plus_weak_auth": "test_user_enum_plus_weak_auth()" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L36 | neighbors=[test_tier1_correlations.py, _run()]
- "tests_test_tier1_wiring_gate_funnel": "_funnel()" | kind=code-symbol | source=probe/tests/test_tier1_wiring_gate.py:L35 | neighbors=[test_tier1_wiring_gate.py, test_tcp_branches_are_fully_wired()]
- "tests_test_tier1_wiring_gate_test_tcp_branches_are_fully_wired": "test_tcp_branches_are_fully_wired()" | kind=code-symbol | source=probe/tests/test_tier1_wiring_gate.py:L44 | neighbors=[test_tier1_wiring_gate.py, _funnel()]
- "tests_test_tls_fingerprint_testparseserverhello_test_extracts_version_and_cipher": ".test_extracts_version_and_cipher()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L59 | neighbors=[TestParseServerHello, _synthetic_server_hello()]
- "tests_test_tls_fingerprint_testparseserverhello_test_tls13_version_from_supported_versions_ext": ".test_tls13_version_from_supported_versions_ext()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L65 | neighbors=[TestParseServerHello, _synthetic_server_hello()]
- "tests_test_tls_legacy_versions_test_try_version_reports_client_side_refusal_separately": "test_try_version_reports_client_side_refusal_separately()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L125 | neighbors=[test_tls_legacy_versions.py, A version the probe cannot OFFER is 'no…]
- "tests_test_tls_port_coverage_test_refused_handshake_is_an_error_not_a_false_negative": "test_refused_handshake_is_an_error_not_a_false_negative()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L87 | neighbors=[test_tls_port_coverage.py, Why widening is safe.      A port that …]
- "tests_test_tls_port_coverage_testdeliberateexclusions_test_rdp_is_excluded": ".test_rdp_is_excluded()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L69 | neighbors=[3389 reaches TLS only after the X.224 r…, TestDeliberateExclusions]
- "tests_test_tls_port_coverage_testdeliberateexclusions_test_starttls_upgrade_ports_excluded": ".test_starttls_upgrade_ports_excluded()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L82 | neighbors=[STARTTLS negotiates in-band; implicit T…, TestDeliberateExclusions]
- "tests_test_tls_port_coverage_testdeliberateexclusions_test_winrm_plaintext_listeners_excluded": ".test_winrm_plaintext_listeners_excluded()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L76 | neighbors=[5986 is WinRM's TLS listener and IS inc…, TestDeliberateExclusions]
- "tests_test_tls_port_coverage_testsinglesourceoftruth_test_branch_spec_matches_the_gate": ".test_branch_spec_matches_the_gate()" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L38 | neighbors=[The drift that used to exist: spec allo…, TestSingleSourceOfTruth]
- "tests_test_tls_posture_testgradetlsposture_test_grade_a_modern": ".test_grade_a_modern()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L73 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_b_no_tls13": ".test_grade_b_no_tls13()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L78 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_c_tls11": ".test_grade_c_tls11()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L83 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_tls_posture_testgradetlsposture_test_grade_f_tls10": ".test_grade_f_tls10()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L94 | neighbors=[TestGradeTlsPosture, _modern()]
- "tests_test_two_tree_parity_test_mirrored_set_is_nonempty": "test_mirrored_set_is_nonempty()" | kind=code-symbol | source=probe/tests/test_two_tree_parity.py:L40 | neighbors=[test_two_tree_parity.py, _mirrored_py_files()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-165.json

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
