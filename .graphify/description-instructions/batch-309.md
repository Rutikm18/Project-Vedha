# Node Description Batch 310 of 336

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

- "tests_test_runtime_topology_test_manager_root_is_service_metadata": "test_manager_root_is_service_metadata()" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L13 | neighbors=[test_runtime_topology.py] | lang=en
- "tests_test_scan_funnel_fakediscovery_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L25 | neighbors=[FakeDiscovery] | lang=en
- "tests_test_scan_funnel_fakediscovery_scan_target": ".scan_target()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L29 | neighbors=[FakeDiscovery] | lang=en
- "tests_test_scan_funnel_fakemsrpc_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L257 | neighbors=[_FakeMSRPC] | lang=en
- "tests_test_scan_funnel_fakemsrpc_scan_target": ".scan_target()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L260 | neighbors=[_FakeMSRPC] | lang=en
- "tests_test_scan_funnel_fakeportscanner_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L37 | neighbors=[FakePortScanner] | lang=en
- "tests_test_scan_funnel_fakeportscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L42 | neighbors=[FakePortScanner] | lang=en
- "tests_test_scan_funnel_opensetportfactory_call": ".__call__()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L241 | neighbors=[_OpenSetPortFactory] | lang=en
- "tests_test_scan_funnel_opensetportfactory_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L237 | neighbors=[_OpenSetPortFactory] | lang=en
- "tests_test_scan_funnel_rationale_1": "test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel" | kind=entity | source=probe/tests/test_scan_funnel.py:L1 | neighbors=[test_scan_funnel.py] | lang=en
- "tests_test_scan_funnel_rationale_233": "Port-scanner factory whose scanners report a port open iff it is in     `actuall" | kind=entity | source=probe/tests/test_scan_funnel.py:L233 | neighbors=[_OpenSetPortFactory] | lang=en
- "tests_test_scan_funnel_rationale_255": "A deep scanner on 135 that returns EPM-advertised dynamic ports." | kind=entity | source=probe/tests/test_scan_funnel.py:L255 | neighbors=[_FakeMSRPC] | lang=en
- "tests_test_scan_funnel_rationale_65": "Build a funnel with fakes; return (funnel, discovery, port_scanner, created)." | kind=entity | source=probe/tests/test_scan_funnel.py:L65 | neighbors=[_make_funnel()] | lang=en
- "tests_test_scan_funnel_rationale_67": "Build a funnel with fakes; return (funnel, discovery, port_scanner, created)." | kind=entity | source=probe/tests/test_scan_funnel.py:L67 | neighbors=[_make_funnel()] | lang=en
- "tests_test_scan_funnel_recordingdeep_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L50 | neighbors=[RecordingDeep] | lang=en
- "tests_test_scan_funnel_recordingdeep_scan_target": ".scan_target()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L55 | neighbors=[RecordingDeep] | lang=en
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_candidate_ports_cover_all_routes": ".test_candidate_ports_cover_all_routes()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L212 | neighbors=[TestBuildDefaultFunnel] | lang=en
- "tests_test_scan_funnel_testreconcileports_test_ignores_non_ints_and_empty": ".test_ignores_non_ints_and_empty()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L226 | neighbors=[TestReconcilePorts] | lang=en
- "tests_test_scan_funnel_testreconcileports_test_union_dedup_sorted": ".test_union_dedup_sorted()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L222 | neighbors=[TestReconcilePorts] | lang=en
- "tests_test_scan_funnel_testrouteports_test_intersection_only": ".test_intersection_only()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L101 | neighbors=[TestRoutePorts] | lang=en
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
- "tests_test_scanner_congestion_rationale_430": "Congestion control must react to a CHANGE in delivery, not to a steady     rate" | kind=entity | source=probe/tests/test_scanner_congestion.py:L430 | neighbors=[TestDeliveryAwareBackoff] | lang=en
- "tests_test_scanner_congestion_rationale_445": "~97% definitive (the measured RST-suppressing host) must NOT throttle." | kind=entity | source=probe/tests/test_scanner_congestion.py:L445 | neighbors=[.test_mostly_answering_host_is_not_trea…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-309.json

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
