# Node Description Batch 352 of 380

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

- "tests_test_scanner_congestion_rationale_232": "TCP_MAXSEG on an ESTABLISHED socket is the post-options effective         segmen" | kind=entity | source=probe/tests/test_scanner_congestion.py:L232 | neighbors=[.test_maxseg_is_reported_but_never_as_a…] | lang=en
- "tests_test_scanner_congestion_rationale_233": "TCP_MAXSEG on an ESTABLISHED socket is the post-options effective         segmen" | kind=entity | source=probe/tests/test_scanner_congestion.py:L233 | neighbors=[.test_maxseg_is_reported_but_never_as_a…] | lang=en
- "tests_test_scanner_congestion_rationale_242": "End-to-end form of the same guarantee, through os_fingerprint." | kind=entity | source=probe/tests/test_scanner_congestion.py:L242 | neighbors=[.test_timestamped_ethernet_host_is_not_…] | lang=en
- "tests_test_scanner_congestion_rationale_243": "End-to-end form of the same guarantee, through os_fingerprint." | kind=entity | source=probe/tests/test_scanner_congestion.py:L243 | neighbors=[.test_timestamped_ethernet_host_is_not_…] | lang=en
- "tests_test_scanner_congestion_rationale_264": "THE accuracy guarantee for #6b.          os_fingerprint scores `tcp_window` agai" | kind=entity | source=probe/tests/test_scanner_congestion.py:L264 | neighbors=[.test_never_synthesizes_an_initial_tcp_…] | lang=en
- "tests_test_scanner_congestion_rationale_265": "THE accuracy guarantee for #6b.          os_fingerprint scores `tcp_window` agai" | kind=entity | source=probe/tests/test_scanner_congestion.py:L265 | neighbors=[.test_never_synthesizes_an_initial_tcp_…] | lang=en
- "tests_test_scanner_congestion_rationale_306": "The false negative #9 exists to kill: a dual-stack host whose IPv6         path" | kind=entity | source=probe/tests/test_scanner_congestion.py:L306 | neighbors=[.test_v4_is_reachable_even_when_aaaa_so…] | lang=en
- "tests_test_scanner_congestion_rationale_307": "The false negative #9 exists to kill: a dual-stack host whose IPv6         path" | kind=entity | source=probe/tests/test_scanner_congestion.py:L307 | neighbors=[.test_v4_is_reachable_even_when_aaaa_so…] | lang=en
- "tests_test_scanner_congestion_rationale_337": "A host that rate-limits its RSTs answers only when probed gently. The     fast s" | kind=entity | source=probe/tests/test_scanner_congestion.py:L337 | neighbors=[TestReprobeCleanupPass] | lang=en
- "tests_test_scanner_congestion_rationale_338": "A host that rate-limits its RSTs answers only when probed gently. The     fast s" | kind=entity | source=probe/tests/test_scanner_congestion.py:L338 | neighbors=[TestReprobeCleanupPass] | lang=en
- "tests_test_scanner_congestion_rationale_342": "Silent for the first `answer_after` probes per port, then a real RST." | kind=entity | source=probe/tests/test_scanner_congestion.py:L342 | neighbors=[._rate_limited()] | lang=en
- "tests_test_scanner_congestion_rationale_343": "Silent for the first `answer_after` probes per port, then a real RST." | kind=entity | source=probe/tests/test_scanner_congestion.py:L343 | neighbors=[._rate_limited()] | lang=en
- "tests_test_scanner_congestion_rationale_384": "Corrected ports must be recorded ONCE, with their final state." | kind=entity | source=probe/tests/test_scanner_congestion.py:L384 | neighbors=[.test_completeness_holds_after_correcti…] | lang=en
- "tests_test_scanner_congestion_rationale_385": "Corrected ports must be recorded ONCE, with their final state." | kind=entity | source=probe/tests/test_scanner_congestion.py:L385 | neighbors=[.test_completeness_holds_after_correcti…] | lang=en
- "tests_test_scanner_congestion_rationale_415": "A converged estimator can be tuned to a path that was dropping us." | kind=entity | source=probe/tests/test_scanner_congestion.py:L415 | neighbors=[.test_cleanup_raises_the_timeout_floor()] | lang=en
- "tests_test_scanner_congestion_rationale_416": "A converged estimator can be tuned to a path that was dropping us." | kind=entity | source=probe/tests/test_scanner_congestion.py:L416 | neighbors=[.test_cleanup_raises_the_timeout_floor()] | lang=en
- "tests_test_scanner_congestion_rationale_430": "Congestion control must react to a CHANGE in delivery, not to a steady     rate" | kind=entity | source=probe/tests/test_scanner_congestion.py:L430 | neighbors=[TestDeliveryAwareBackoff] | lang=en
- "tests_test_scanner_congestion_rationale_431": "Congestion control must react to a CHANGE in delivery, not to a steady     rate" | kind=entity | source=probe/tests/test_scanner_congestion.py:L431 | neighbors=[TestDeliveryAwareBackoff] | lang=en
- "tests_test_scanner_congestion_rationale_445": "~97% definitive (the measured RST-suppressing host) must NOT throttle." | kind=entity | source=probe/tests/test_scanner_congestion.py:L445 | neighbors=[.test_mostly_answering_host_is_not_trea…] | lang=en
- "tests_test_scanner_congestion_rationale_446": "~97% definitive (the measured RST-suppressing host) must NOT throttle." | kind=entity | source=probe/tests/test_scanner_congestion.py:L446 | neighbors=[.test_mostly_answering_host_is_not_trea…] | lang=en
- "tests_test_scanner_congestion_rationale_452": "A genuinely lossy path (verified separately with 60% netem loss) must         st" | kind=entity | source=probe/tests/test_scanner_congestion.py:L452 | neighbors=[.test_collapsed_delivery_still_backs_of…] | lang=en
- "tests_test_scanner_congestion_rationale_455": "A genuinely lossy path (verified separately with 60% netem loss) must         st" | kind=entity | source=probe/tests/test_scanner_congestion.py:L455 | neighbors=[.test_collapsed_delivery_still_backs_of…] | lang=en
- "tests_test_scanner_congestion_rationale_460": "Never throttle on a handful of early probes." | kind=entity | source=probe/tests/test_scanner_congestion.py:L460 | neighbors=[.test_no_opinion_before_the_sample_floo…] | lang=en
- "tests_test_scanner_congestion_rationale_464": "Never throttle on a handful of early probes." | kind=entity | source=probe/tests/test_scanner_congestion.py:L464 | neighbors=[.test_no_opinion_before_the_sample_floo…] | lang=en
- "tests_test_scanner_congestion_rationale_472": "Delivery returning must clear the loss condition — the ratchet that         made" | kind=entity | source=probe/tests/test_scanner_congestion.py:L472 | neighbors=[.test_recovery_after_a_bad_patch()] | lang=en
- "tests_test_scanner_congestion_rationale_478": "Delivery returning must clear the loss condition — the ratchet that         made" | kind=entity | source=probe/tests/test_scanner_congestion.py:L478 | neighbors=[.test_recovery_after_a_bad_patch()] | lang=en
- "tests_test_scanner_congestion_rationale_490": "One quiet host must not throttle the next." | kind=entity | source=probe/tests/test_scanner_congestion.py:L490 | neighbors=[.test_window_resets_between_hosts()] | lang=en
- "tests_test_scanner_congestion_rationale_497": "One quiet host must not throttle the next — nor one scanned beside it." | kind=entity | source=probe/tests/test_scanner_congestion.py:L497 | neighbors=[.test_each_scan_owns_its_delivery_windo…] | lang=en
- "tests_test_scanner_congestion_rationale_526": "A collapsed window must be able to climb back within the scan's lifetime.      `" | kind=entity | source=probe/tests/test_scanner_congestion.py:L526 | neighbors=[TestCollapseRecovery] | lang=en
- "tests_test_scanner_congestion_rationale_544": "The floor is tied to min_window (2x), NOT to max_window.          A max_window-d" | kind=entity | source=probe/tests/test_scanner_congestion.py:L544 | neighbors=[.test_ssthresh_keeps_a_slow_start_runwa…] | lang=en
- "tests_test_scanner_congestion_rationale_556": "A window of 1 turns a 65,535-port sweep into a 12-hour crawl, and buys         n" | kind=entity | source=probe/tests/test_scanner_congestion.py:L556 | neighbors=[.test_window_never_fully_serialises()] | lang=pt
- "tests_test_scanner_congestion_rationale_561": "Measured: 80 successes with the floors vs 198 without — and, more         import" | kind=entity | source=probe/tests/test_scanner_congestion.py:L561 | neighbors=[.test_recovery_to_usable_throughput_is_…] | lang=en
- "tests_test_scanner_congestion_rationale_571": "Documents the regression: without the floors, recovery is quadratic." | kind=entity | source=probe/tests/test_scanner_congestion.py:L571 | neighbors=[.test_old_behaviour_was_slow()] | lang=en
- "tests_test_scanner_congestion_rationale_586": "The floor must not neuter congestion control: 80 -> 8 is still 10x." | kind=entity | source=probe/tests/test_scanner_congestion.py:L586 | neighbors=[.test_backoff_is_still_meaningful()] | lang=en
- "tests_test_scanner_congestion_rationale_591": "port_scanner derives the floor from concurrency, so a small scan does         no" | kind=entity | source=probe/tests/test_scanner_congestion.py:L591 | neighbors=[.test_floor_scales_with_concurrency()] | lang=en
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_window_never_falls_below_one": ".test_window_never_falls_below_one()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L193 | neighbors=[TestConnectCongestionWindow] | lang=en
- "tests_test_scanner_congestion_testharvesttcpstack_test_none_socket_yields_nothing": ".test_none_socket_yields_nothing()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L226 | neighbors=[TestHarvestTcpStack] | lang=en
- "tests_test_scanner_congestion_testharvesttcpstack_test_object_without_getsockopt_is_survivable": ".test_object_without_getsockopt_is_survivable()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L229 | neighbors=[TestHarvestTcpStack] | lang=en
- "tests_test_scanner_congestion_testresolvecandidates_test_absent_requested_family_falls_back_rather_than_failing": ".test_absent_requested_family_falls_back_rather_than_failing()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L318 | neighbors=[TestResolveCandidates] | lang=en
- "tests_test_scanner_congestion_testresolvecandidates_test_literal_ip_resolves_to_itself": ".test_literal_ip_resolves_to_itself()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L331 | neighbors=[TestResolveCandidates] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-351.json

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
