# Node Description Batch 287 of 336

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_host_discovery_udp_test_icmp_unreachable_from_closed_port_proves_stack_is_up": "test_icmp_unreachable_from_closed_port_proves_stack_is_up()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L155 | neighbors=[test_host_discovery_udp.py]
- "tests_test_host_discovery_udp_test_reverse_dns_name_recorded_and_becomes_alias": "test_reverse_dns_name_recorded_and_becomes_alias()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L206 | neighbors=[test_host_discovery_udp.py]
- "tests_test_host_discovery_udp_test_udp_tier_skipped_when_neighbor_vouches": "test_udp_tier_skipped_when_neighbor_vouches()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L187 | neighbors=[test_host_discovery_udp.py]
- "tests_test_host_discovery_udp_test_udp_tier_skipped_when_tcp_proves_life": "test_udp_tier_skipped_when_tcp_proves_life()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L166 | neighbors=[test_host_discovery_udp.py]
- "tests_test_host_discovery_udp_testfusewithudp_test_icmp_unreachable_alone": ".test_icmp_unreachable_alone()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L68 | neighbors=[TestFuseWithUdp]
- "tests_test_host_discovery_udp_testfusewithudp_test_no_signals_unchanged": ".test_no_signals_unchanged()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L82 | neighbors=[TestFuseWithUdp]
- "tests_test_host_discovery_udp_testfusewithudp_test_tcp_plus_udp_corroborate": ".test_tcp_plus_udp_corroborate()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L74 | neighbors=[TestFuseWithUdp]
- "tests_test_host_discovery_udp_testfusewithudp_test_udp_reply_alone_is_confirmed_alive": ".test_udp_reply_alone_is_confirmed_alive()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L60 | neighbors=[TestFuseWithUdp]
- "tests_test_host_discovery_udp_testparsenbstat_test_not_a_response": ".test_not_a_response()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L48 | neighbors=[TestParseNbstat]
- "tests_test_host_health_rationale_1": "test_host_health.py — mid-scan target-offline detection.  The interesting cases" | kind=entity | source=probe/tests/test_host_health.py:L1 | neighbors=[test_host_health.py]
- "tests_test_host_health_rationale_122": "One false alarm must not disable the check for the rest of the scan." | kind=entity | source=probe/tests/test_host_health.py:L122 | neighbors=[.test_flaky_host_can_be_suspected_again…]
- "tests_test_host_health_rationale_132": "The whole point: 'we stopped early' must never read as 'nothing found'." | kind=entity | source=probe/tests/test_host_health.py:L132 | neighbors=[.test_offline_fact_marks_the_scan_incom…]
- "tests_test_host_health_rationale_186": "Regression: \"open|filtered\" is the UDP no-reply verdict, not an open port.     R" | kind=entity | source=probe/tests/test_host_health.py:L186 | neighbors=[TestUdpNoReplyIsNotContact]
- "tests_test_host_health_rationale_203": "The primary detector. Branch-failure evidence covers only the milliseconds     t" | kind=entity | source=probe/tests/test_host_health.py:L203 | neighbors=[TestHeartbeat]
- "tests_test_host_health_rationale_281": "An offline host must reach the operator's screen, not just the fact list.     Ex" | kind=entity | source=probe/tests/test_host_health.py:L281 | neighbors=[TestOperatorVisibility]
- "tests_test_host_health_rationale_295": "A host that is merely filtered is not a problem with the run." | kind=entity | source=probe/tests/test_host_health.py:L295 | neighbors=[.test_flaky_note_is_not_an_error()]
- "tests_test_host_health_rationale_38": "A closed port is the host's own stack answering — positive proof of         life" | kind=entity | source=probe/tests/test_host_health.py:L38 | neighbors=[.test_rst_is_contact_not_silence()]
- "tests_test_host_health_rationale_57": "A branch that declined to run says nothing about the host." | kind=entity | source=probe/tests/test_host_health.py:L57 | neighbors=[.test_no_results_is_not_silence()]
- "tests_test_host_health_rationale_67": "A healthy host with many inapplicable branches must never accumulate         its" | kind=entity | source=probe/tests/test_host_health.py:L67 | neighbors=[.test_strikes_must_be_consecutive()]
- "tests_test_host_health_rationale_85": "The headline false positive: silence from every branch, but the host         is" | kind=entity | source=probe/tests/test_host_health.py:L85 | neighbors=[.test_firewalled_host_that_still_answer…]
- "tests_test_host_health_testconfiguration_test_bad_threshold_falls_back_to_a_sane_value": ".test_bad_threshold_falls_back_to_a_sane_value()" | kind=code-symbol | source=probe/tests/test_host_health.py:L179 | neighbors=[TestConfiguration]
- "tests_test_host_health_testconfiguration_test_threshold_is_tunable_by_env": ".test_threshold_is_tunable_by_env()" | kind=code-symbol | source=probe/tests/test_host_health.py:L173 | neighbors=[TestConfiguration]
- "tests_test_host_health_testheartbeat_test_a_broken_probe_never_condemns_a_host": ".test_a_broken_probe_never_condemns_a_host()" | kind=code-symbol | source=probe/tests/test_host_health.py:L262 | neighbors=[TestHeartbeat]
- "tests_test_host_health_testheartbeat_test_a_single_miss_is_not_enough": ".test_a_single_miss_is_not_enough()" | kind=code-symbol | source=probe/tests/test_host_health.py:L215 | neighbors=[TestHeartbeat]
- "tests_test_http_lease_rationale_121": "An operator cancel (409) is DEFINITIVE, unlike a flaky network.      The grace b" | kind=entity | source=probe/tests/test_http_lease.py:L121 | neighbors=[test_revoked_lease_cancels_the_attempt_…]
- "tests_test_http_lease_test_engine_cancellation_stops_async_scan_work": "test_engine_cancellation_stops_async_scan_work()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L101 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_poll_auth_failure_is_not_hidden": "test_poll_auth_failure_is_not_hidden()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L33 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_polled_job_renews_lease_until_runner_finishes": "test_polled_job_renews_lease_until_runner_finishes()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L42 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_repeated_lease_rejection_cancels_running_attempt": "test_repeated_lease_rejection_cancels_running_attempt()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L74 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_transient_poll_failure_propagates_to_loop_handler": "test_transient_poll_failure_propagates_to_loop_handler()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L20 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_transient_poll_failure_returns_no_jobs": "test_transient_poll_failure_returns_no_jobs()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L15 | neighbors=[test_http_lease.py]
- "tests_test_hw_bind_rationale_1": "Tests for agent/hw_bind.py" | kind=entity | source=probe/tests/test_hw_bind.py:L1 | neighbors=[test_hw_bind.py]
- "tests_test_hw_bind_testcheckhwbind_test_passes_when_match": ".test_passes_when_match()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L22 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_raises_on_mismatch": ".test_raises_on_mismatch()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L28 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_raises_when_unset_and_enforced": ".test_raises_when_unset_and_enforced()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L39 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_skips_when_unset_and_dev_mode": ".test_skips_when_unset_and_dev_mode()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L34 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testgethwid_test_deterministic_within_session": ".test_deterministic_within_session()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L17 | neighbors=[TestGetHwId]
- "tests_test_hw_bind_testgethwid_test_returns_32_hex_chars": ".test_returns_32_hex_chars()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L12 | neighbors=[TestGetHwId]
- "tests_test_installer_contract_test_installer_rejects_missing_or_unknown_arguments": "test_installer_rejects_missing_or_unknown_arguments()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L31 | neighbors=[test_installer_contract.py]
- "tests_test_installer_contract_test_installer_requires_only_manager_endpoint_in_dry_run": "test_installer_requires_only_manager_endpoint_in_dry_run()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L11 | neighbors=[test_installer_contract.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-286.json

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
