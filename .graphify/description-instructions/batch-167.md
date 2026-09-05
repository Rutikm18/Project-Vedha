# Node Description Batch 168 of 336

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
- "tests_test_transport_testdeviceenrollment_test_token_rotated_by_another_process_is_readopted": ".test_token_rotated_by_another_process_is_readopted()" | kind=code-symbol | source=probe/tests/test_transport.py:L281 | neighbors=[The freshness check reads the STATE FIL…, TestDeviceEnrollment]
- "tests_test_transport_testidentity_test_clear_manager_binding_drops_pin_keeps_keypairs": ".test_clear_manager_binding_drops_pin_keeps_keypairs()" | kind=code-symbol | source=probe/tests/test_transport.py:L57 | neighbors=[Re-pointing to a different manager must…, TestIdentity]
- "tests_test_two_tree_parity_test_mirrored_set_is_nonempty": "test_mirrored_set_is_nonempty()" | kind=code-symbol | source=probe/tests/test_two_tree_parity.py:L40 | neighbors=[test_two_tree_parity.py, _mirrored_py_files()]
- "tests_test_two_tree_parity_test_no_unmirrored_scanner_files": "test_no_unmirrored_scanner_files()" | kind=code-symbol | source=probe/tests/test_two_tree_parity.py:L56 | neighbors=[test_two_tree_parity.py, A scanner that exists in only one tree …]
- "tests_test_va_campaign_test_catalog_ids_are_unique_and_match_default_stages": "test_catalog_ids_are_unique_and_match_default_stages()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L222 | neighbors=[test_va_campaign.py, _scope()]
- "tests_test_va_campaign_test_cli_view_deduplicates_unchanged_status": "test_cli_view_deduplicates_unchanged_status()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L311 | neighbors=[test_va_campaign.py, _Buf]
- "tests_test_va_campaign_test_cli_view_emits_one_line_per_transition": "test_cli_view_emits_one_line_per_transition()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L298 | neighbors=[test_va_campaign.py, _Buf]
- "tests_test_va_campaign_test_disabled_opt_in_stage_is_skipped_and_excluded_from_percent": "test_disabled_opt_in_stage_is_skipped_and_excluded_from_percent()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L80 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_enabled_opt_in_stage_runs": "test_enabled_opt_in_stage_runs()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L99 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_facts_accumulate_into_totals": "test_facts_accumulate_into_totals()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L137 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_gate_not_met_skips_stage": "test_gate_not_met_skips_stage()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L64 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_percent_and_current_stage_transitions": "test_percent_and_current_stage_transitions()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L175 | neighbors=[test_va_campaign.py, _reporter()]
- "tests_test_va_campaign_test_progress_snapshot_shape": "test_progress_snapshot_shape()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L159 | neighbors=[test_va_campaign.py, _reporter()]
- "tests_test_va_campaign_test_stage_error_is_isolated_not_fatal": "test_stage_error_is_isolated_not_fatal()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L119 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_va_campaign_test_stages_run_in_order_and_thread_context": "test_stages_run_in_order_and_thread_context()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L40 | neighbors=[test_va_campaign.py, _run()]
- "tests_test_validation_endpoints_exec": "_exec()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L28 | neighbors=[test_validation_endpoints.py, _mock_db()]
- "tests_test_validation_gate_testnofabricatedicmpliveness": "TestNoFabricatedIcmpLiveness" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L71 | neighbors=[test_validation_gate.py, .test_icmp_unavailable_os_observation_r…]
- "tests_test_validation_gate_testnofabricatedicmpliveness_test_icmp_unavailable_os_observation_raises_no_exposure": ".test_icmp_unavailable_os_observation_raises_no_exposure()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L72 | neighbors=[TestNoFabricatedIcmpLiveness, _ids()]
- "tests_test_validation_gate_testrdpnlagate_test_nla_enforced_suppresses_no_nla_finding": ".test_nla_enforced_suppresses_no_nla_finding()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L56 | neighbors=[TestRdpNlaGate, _ids()]
- "tests_test_validation_gate_testrdpnlagate_test_positive_control_nla_off_is_flagged": ".test_positive_control_nla_off_is_flagged()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L62 | neighbors=[TestRdpNlaGate, _ids()]
- "tests_test_validation_gate_testudpnoreplyrejected_test_open_filtered_amplifier_not_flagged": ".test_open_filtered_amplifier_not_flagged()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L36 | neighbors=[TestUdpNoReplyRejected, _ids()]
- "tests_test_validation_gate_testudpnoreplyrejected_test_positive_control_answered_amplifier_is_flagged": ".test_positive_control_answered_amplifier_is_flagged()" | kind=code-symbol | source=probe/tests/test_validation_gate.py:L43 | neighbors=[TestUdpNoReplyRejected, _ids()]
- "tests_test_validation_ingest_test_confirmed_never_overrides_human_closed_finding": "test_confirmed_never_overrides_human_closed_finding()" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L55 | neighbors=[test_validation_ingest.py, _finding()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-167.json

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
