# Node Description Batch 294 of 332

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

- "tests_test_os_fingerprint_testttlinference_test_os_family_linux": ".test_os_family_linux()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L209 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_os_family_network": ".test_os_family_network()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L215 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_os_family_unknown_on_none": ".test_os_family_unknown_on_none()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L218 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_os_family_windows": ".test_os_family_windows()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L212 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_round_up_to_128": ".test_round_up_to_128()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L197 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_round_up_to_255": ".test_round_up_to_255()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L201 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_round_up_to_64": ".test_round_up_to_64()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L193 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fusion_rationale_1": "test_os_fusion.py — FIX 3(a): cross-scanner OS identification with calibrated, m" | kind=entity | source=probe/tests/test_os_fusion.py:L1 | neighbors=[test_os_fusion.py] | lang=pt
- "tests_test_os_stage_wiring_open": "_open()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L32 | neighbors=[test_os_stage_wiring.py] | lang=en
- "tests_test_os_stage_wiring_rationale_1": "test_os_stage_wiring.py — the OS-identification stage in the agent workflow.  Be" | kind=entity | source=probe/tests/test_os_stage_wiring.py:L1 | neighbors=[test_os_stage_wiring.py] | lang=en
- "tests_test_os_stage_wiring_test_dead_host_is_never_os_probed": "test_dead_host_is_never_os_probed()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L199 | neighbors=[test_os_stage_wiring.py] | lang=en
- "tests_test_os_stage_wiring_test_smb_build_probe_skipped_when_445_is_closed": "test_smb_build_probe_skipped_when_445_is_closed()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L172 | neighbors=[test_os_stage_wiring.py] | lang=en
- "tests_test_os_stage_wiring_testassetmerge_test_os_fact_is_cacheable_as_deterministic": ".test_os_fact_is_cacheable_as_deterministic()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L108 | neighbors=[TestAssetMerge] | lang=en
- "tests_test_os_stage_wiring_testplan_test_full_assessment_includes_it": ".test_full_assessment_includes_it()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L70 | neighbors=[TestPlan] | lang=en
- "tests_test_os_stage_wiring_testplan_test_not_planned_for_a_udp_only_job": ".test_not_planned_for_a_udp_only_job()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L65 | neighbors=[TestPlan] | lang=en
- "tests_test_os_stage_wiring_testplan_test_not_planned_for_liveness_only": ".test_not_planned_for_liveness_only()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L59 | neighbors=[TestPlan] | lang=en
- "tests_test_os_stage_wiring_testplan_test_os_stage_planned_from_the_port_stage_up": ".test_os_stage_planned_from_the_port_stage_up()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L53 | neighbors=[TestPlan] | lang=en
- "tests_test_passive_collector_socket_fileno": ".fileno()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L28 | neighbors=[_Socket] | lang=en
- "tests_test_passive_collector_socket_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L24 | neighbors=[_Socket] | lang=en
- "tests_test_passive_collector_test_zero_listeners_returns_structured_failure": "test_zero_listeners_returns_structured_failure()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L135 | neighbors=[test_passive_collector.py] | lang=en
- "tests_test_passive_collector_writer_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L16 | neighbors=[_Writer] | lang=en
- "tests_test_passive_collector_writer_write": ".write()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L19 | neighbors=[_Writer] | lang=en
- "tests_test_pat_auth_test_new_pat_token_shape_and_hash_stability": "test_new_pat_token_shape_and_hash_stability()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L44 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_builder_rejects_unknown_scope": "test_pat_builder_rejects_unknown_scope()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L88 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_builder_returns_token_once_and_stores_hash_only": "test_pat_builder_returns_token_once_and_stores_hash_only()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L52 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_builder_supports_non_expiring_tokens_only_when_requested": "test_pat_builder_supports_non_expiring_tokens_only_when_requested()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L74 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_scope_allows_probe_cli_paths": "test_pat_scope_allows_probe_cli_paths()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L16 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_scope_matrix_for_api_scopes": "test_pat_scope_matrix_for_api_scopes()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L27 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_validate_pat_scopes_dedupes_and_rejects_unknown": "test_validate_pat_scopes_dedupes_and_rejects_unknown()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L35 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_perf_optimization_rationale_1": "Tests for the P1+P2 performance optimization of the detection engine.  P1 — vers" | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L1 | neighbors=[test_perf_optimization.py] | lang=en
- "tests_test_perf_optimization_rationale_27": "dpkg_compare must use the pure-Python comparator in the hot path.     Shelling o" | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L27 | neighbors=[test_dpkg_compare_does_not_call_the_bin…] | lang=en
- "tests_test_perf_optimization_rationale_50": "Isolate the guard's in-memory + on-disk validation cache per test." | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L50 | neighbors=[clean_guard_cache()] | lang=en
- "tests_test_perf_optimization_rationale_58": "No dpkg binary → nothing to cross-check against; return [] and never     attempt" | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L58 | neighbors=[test_guard_is_noop_without_dpkg()] | lang=en
- "tests_test_perf_optimization_rationale_76": "When the binary disagrees with pure-Python on an adjacent pair, that pair     is" | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L76 | neighbors=[test_guard_reports_divergence_and_warns…] | lang=en
- "tests_test_perf_optimization_test_guard_passes_when_pure_python_agrees_with_dpkg": "test_guard_passes_when_pure_python_agrees_with_dpkg()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L67 | neighbors=[test_perf_optimization.py] | lang=en
- "tests_test_perf_optimization_test_guard_validates_once_per_cache_key": "test_guard_validates_once_per_cache_key()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L86 | neighbors=[test_perf_optimization.py] | lang=en
- "tests_test_perf_optimization_test_load_kev_and_epss_memoized": "test_load_kev_and_epss_memoized()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L142 | neighbors=[test_perf_optimization.py] | lang=en
- "tests_test_pipeline_concurrency_rationale_1": "test_pipeline_concurrency.py — the two correctness fixes from ADR-0001.  R1: the" | kind=entity | source=manager/backend/tests/test_pipeline_concurrency.py:L1 | neighbors=[test_pipeline_concurrency.py] | lang=en
- "tests_test_pipeline_concurrency_rationale_129": "The guard must not swallow real work." | kind=entity | source=manager/backend/tests/test_pipeline_concurrency.py:L129 | neighbors=[test_a_first_delivery_still_runs_detect…] | lang=en
- "tests_test_pipeline_concurrency_rationale_148": "Pre-existing behaviour: a vanished scan_result logs and returns rather     than" | kind=entity | source=manager/backend/tests/test_pipeline_concurrency.py:L148 | neighbors=[test_a_missing_submission_is_not_an_err…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-293.json

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
