# Node Description Batch 306 of 332

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_scan_funnel_testrouteports_test_no_match_returns_empty": ".test_no_match_returns_empty()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L105 | neighbors=[TestRoutePorts] | lang=en
- "tests_test_scan_funnel_testrouteports_test_port_in_multiple_routes": ".test_port_in_multiple_routes()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L109 | neighbors=[TestRoutePorts] | lang=en
- "tests_test_scan_funnel_testrouteports_test_sorted_output": ".test_sorted_output()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L114 | neighbors=[TestRoutePorts] | lang=en
- "tests_test_scan_health_rationale_1": "test_scan_health.py — the probe scan-metrics → coverage/health verdict.  Guards" | kind=entity | source=manager/backend/tests/test_scan_health.py:L1 | neighbors=[test_scan_health.py] | lang=en
- "tests_test_scan_health_test_aggregates_across_hosts": "test_aggregates_across_hosts()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L48 | neighbors=[test_scan_health.py] | lang=en
- "tests_test_scan_health_test_no_metrics_means_nothing_to_attest": "test_no_metrics_means_nothing_to_attest()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L40 | neighbors=[test_scan_health.py] | lang=en
- "tests_test_scanner_congestion_fakesock_getsockopt": ".getsockopt()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L214 | neighbors=[_FakeSock] | lang=en
- "tests_test_scanner_congestion_fakesock_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L211 | neighbors=[_FakeSock] | lang=en
- "tests_test_scanner_congestion_rationale_1": "test_scanner_congestion.py — proof tests for the offensive-accuracy pass (RESEAR" | kind=entity | source=probe/tests/test_scanner_congestion.py:L1 | neighbors=[test_scanner_congestion.py] | lang=en
- "tests_test_scanner_congestion_rationale_201": "A synthetic Linux `struct tcp_info`: 8 u8 flag bytes then 20 u32 fields." | kind=entity | source=probe/tests/test_scanner_congestion.py:L201 | neighbors=[_tcp_info_buf()] | lang=pt
- "tests_test_scanner_congestion_rationale_232": "TCP_MAXSEG on an ESTABLISHED socket is the post-options effective         segmen" | kind=entity | source=probe/tests/test_scanner_congestion.py:L232 | neighbors=[.test_maxseg_is_reported_but_never_as_a…] | lang=en
- "tests_test_scanner_congestion_rationale_242": "End-to-end form of the same guarantee, through os_fingerprint." | kind=entity | source=probe/tests/test_scanner_congestion.py:L242 | neighbors=[.test_timestamped_ethernet_host_is_not_…] | lang=en
- "tests_test_scanner_congestion_rationale_264": "THE accuracy guarantee for #6b.          os_fingerprint scores `tcp_window` agai" | kind=entity | source=probe/tests/test_scanner_congestion.py:L264 | neighbors=[.test_never_synthesizes_an_initial_tcp_…] | lang=en
- "tests_test_scanner_congestion_rationale_306": "The false negative #9 exists to kill: a dual-stack host whose IPv6         path" | kind=entity | source=probe/tests/test_scanner_congestion.py:L306 | neighbors=[.test_v4_is_reachable_even_when_aaaa_so…] | lang=en
- "tests_test_scanner_congestion_rationale_337": "A host that rate-limits its RSTs answers only when probed gently. The     fast s" | kind=entity | source=probe/tests/test_scanner_congestion.py:L337 | neighbors=[TestReprobeCleanupPass] | lang=en
- "tests_test_scanner_congestion_rationale_342": "Silent for the first `answer_after` probes per port, then a real RST." | kind=entity | source=probe/tests/test_scanner_congestion.py:L342 | neighbors=[._rate_limited()] | lang=en
- "tests_test_scanner_congestion_rationale_384": "Corrected ports must be recorded ONCE, with their final state." | kind=entity | source=probe/tests/test_scanner_congestion.py:L384 | neighbors=[.test_completeness_holds_after_correcti…] | lang=en
- "tests_test_scanner_congestion_rationale_415": "A converged estimator can be tuned to a path that was dropping us." | kind=entity | source=probe/tests/test_scanner_congestion.py:L415 | neighbors=[.test_cleanup_raises_the_timeout_floor()] | lang=en
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_window_never_falls_below_one": ".test_window_never_falls_below_one()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L192 | neighbors=[TestConnectCongestionWindow] | lang=en
- "tests_test_scanner_congestion_testharvesttcpstack_test_none_socket_yields_nothing": ".test_none_socket_yields_nothing()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L225 | neighbors=[TestHarvestTcpStack] | lang=en
- "tests_test_scanner_congestion_testharvesttcpstack_test_object_without_getsockopt_is_survivable": ".test_object_without_getsockopt_is_survivable()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L228 | neighbors=[TestHarvestTcpStack] | lang=en
- "tests_test_scanner_congestion_testresolvecandidates_test_absent_requested_family_falls_back_rather_than_failing": ".test_absent_requested_family_falls_back_rather_than_failing()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L317 | neighbors=[TestResolveCandidates] | lang=en
- "tests_test_scanner_congestion_testresolvecandidates_test_literal_ip_resolves_to_itself": ".test_literal_ip_resolves_to_itself()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L330 | neighbors=[TestResolveCandidates] | lang=en
- "tests_test_scanner_congestion_testresolvecandidates_test_unresolvable_name_raises": ".test_unresolvable_name_raises()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L324 | neighbors=[TestResolveCandidates] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_backoff_is_bounded_by_min_rate": ".test_backoff_is_bounded_by_min_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L51 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_clean_round_increases_rate_additively": ".test_clean_round_increases_rate_additively()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L39 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_empty_round_is_ignored_not_treated_as_total_loss": ".test_empty_round_is_ignored_not_treated_as_total_loss()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L70 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_first_pace_does_not_block": ".test_first_pace_does_not_block()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L84 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_growth_is_bounded_by_max_rate": ".test_growth_is_bounded_by_max_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L57 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_loss_just_under_threshold_does_not_back_off": ".test_loss_just_under_threshold_does_not_back_off()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L64 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_lossy_round_halves_the_rate": ".test_lossy_round_halves_the_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L45 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_pace_actually_spends_wall_time_at_a_low_rate": ".test_pace_actually_spends_wall_time_at_a_low_rate()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L75 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_rate_zero_disables_pacing": ".test_rate_zero_disables_pacing()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L90 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testsendpacer_test_stats_expose_throttling": ".test_stats_expose_throttling()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L97 | neighbors=[TestSendPacer] | lang=en
- "tests_test_scanner_congestion_testwaitreadable_test_returns_false_when_nothing_arrives_before_deadline": ".test_returns_false_when_nothing_arrives_before_deadline()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L107 | neighbors=[TestWaitReadable] | lang=en
- "tests_test_scanner_congestion_testwaitreadable_test_returns_true_as_soon_as_data_is_waiting": ".test_returns_true_as_soon_as_data_is_waiting()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L114 | neighbors=[TestWaitReadable] | lang=en
- "tests_test_scanner_congestion_testwaitreadable_test_unselectable_object_degrades_to_assume_readable": ".test_unselectable_object_degrades_to_assume_readable()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L129 | neighbors=[TestWaitReadable] | lang=en
- "tests_test_scanner_congestion_testwaitreadable_test_zero_timeout_never_blocks": ".test_zero_timeout_never_blocks()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L122 | neighbors=[TestWaitReadable] | lang=en
- "tests_test_scanner_parity_rationale_1": "test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1" | kind=entity | source=probe/tests/test_scanner_parity.py:L1 | neighbors=[test_scanner_parity.py] | lang=en
- "tests_test_scanner_parity_rationale_30": "Every scanner module authored in main_scripts must exist in scanner/." | kind=entity | source=probe/tests/test_scanner_parity.py:L30 | neighbors=[test_scanner_is_superset_of_no_missing_…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-305.json

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
