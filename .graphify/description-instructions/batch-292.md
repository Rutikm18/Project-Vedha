# Node Description Batch 293 of 330

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
- "tests_test_pipeline_concurrency_rationale_31": "The lock must be taken BEFORE the first read, or the race it prevents can     st" | kind=entity | source=manager/backend/tests/test_pipeline_concurrency.py:L31 | neighbors=[test_detection_locks_the_engagement_bef…] | lang=en
- "tests_test_pipeline_concurrency_rationale_45": "pg_advisory_lock (session) would leak on any path that forgets to unlock.     Th" | kind=entity | source=manager/backend/tests/test_pipeline_concurrency.py:L45 | neighbors=[test_the_lock_is_transaction_scoped_not…] | lang=en
- "tests_test_pipeline_concurrency_rationale_58": "Two concurrent handlers must contend, so the key has to be a pure function     o" | kind=entity | source=manager/backend/tests/test_pipeline_concurrency.py:L58 | neighbors=[test_the_same_engagement_always_maps_to…] | lang=en
- "tests_test_pipeline_concurrency_rationale_71": "Collisions are harmless (two unrelated engagements briefly serialise) but     sh" | kind=entity | source=manager/backend/tests/test_pipeline_concurrency.py:L71 | neighbors=[test_different_engagements_generally_do…] | lang=en
- "tests_test_pipeline_concurrency_rationale_83": "pg_advisory_xact_lock takes a signed bigint; an out-of-range key raises." | kind=entity | source=manager/backend/tests/test_pipeline_concurrency.py:L83 | neighbors=[test_the_key_fits_a_postgres_bigint()] | lang=en
- "tests_test_pipeline_rationale_1": "Tests for pipeline.py — the orchestrator with 0% prior coverage.  Covers the cri" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L1 | neighbors=[test_pipeline.py] | lang=en
- "tests_test_pipeline_rationale_114": "A completely empty file must not produce any findings." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L114 | neighbors=[.test_empty_jsonl_returns_no_findings()] | lang=pt
- "tests_test_pipeline_rationale_124": "Passing an empty path list must return empty findings and no facts." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L124 | neighbors=[.test_no_paths_returns_empty()] | lang=en
- "tests_test_pipeline_rationale_131": "A completely empty file must not produce any findings." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L131 | neighbors=[.test_empty_jsonl_returns_no_findings()] | lang=pt
- "tests_test_pipeline_rationale_140": "A credentialed package at a version inside a vulnerable range must         produ" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L140 | neighbors=[.test_ssh_inventory_vulnerable_package_…] | lang=pt
- "tests_test_pipeline_rationale_141": "Passing an empty path list must return empty findings and no facts." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L141 | neighbors=[.test_no_paths_returns_empty()] | lang=en
- "tests_test_pipeline_rationale_151": "Findings from an authoritative (credentialed) source must be         confirmed —" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L151 | neighbors=[.test_ssh_inventory_finding_is_confirme…] | lang=en
- "tests_test_pipeline_rationale_157": "A credentialed package at a version inside a vulnerable range must         produ" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L157 | neighbors=[.test_ssh_inventory_vulnerable_package_…] | lang=pt
- "tests_test_pipeline_rationale_164": "A banner-derived (inferred) source match can only produce 'suspected'         —" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L164 | neighbors=[.test_banner_finding_is_suspected_not_c…] | lang=pt
- "tests_test_pipeline_rationale_168": "Findings from an authoritative (credentialed) source must be         confirmed —" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L168 | neighbors=[.test_ssh_inventory_finding_is_confirme…] | lang=en
- "tests_test_pipeline_rationale_177": "A host running the fixed version must not produce a finding." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L177 | neighbors=[.test_no_finding_for_patched_version()] | lang=pt
- "tests_test_pipeline_rationale_181": "A banner-derived (inferred) source match can only produce 'suspected'         —" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L181 | neighbors=[.test_banner_finding_is_suspected_not_c…] | lang=pt
- "tests_test_pipeline_rationale_188": "When all three dbs are injected, the pipeline must not try to read         the d" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L188 | neighbors=[.test_injected_dbs_used_no_file_io()] | lang=en
- "tests_test_pipeline_rationale_194": "A host running the fixed version must not produce a finding." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L194 | neighbors=[.test_no_finding_for_patched_version()] | lang=pt
- "tests_test_pipeline_rationale_205": "When all three dbs are injected, the pipeline must not try to read         the d" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L205 | neighbors=[.test_injected_dbs_used_no_file_io()] | lang=en
- "tests_test_pipeline_rationale_217": "Without an exposure dict the fields stay None — pipeline never guesses." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L217 | neighbors=[.test_no_exposure_fields_are_none()] | lang=en
- "tests_test_pipeline_rationale_234": "Different IPs must produce independent findings — dedup is per         (asset, C" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L234 | neighbors=[.test_two_identical_hosts_each_get_thei…] | lang=en
- "tests_test_pipeline_rationale_247": "The same (asset, CVE) can't appear twice in the output — dedup         must coll" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L247 | neighbors=[.test_findings_deduped_within_same_host…] | lang=en
- "tests_test_pipeline_rationale_261": "Without an exposure dict the fields stay None — pipeline never guesses." | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L261 | neighbors=[.test_no_exposure_fields_are_none()] | lang=en
- "tests_test_pipeline_rationale_278": "Different IPs must produce independent findings — dedup is per         (asset, C" | kind=entity | source=manager/detection_engine/tests/test_pipeline.py:L278 | neighbors=[.test_two_identical_hosts_each_get_thei…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-292.json

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
