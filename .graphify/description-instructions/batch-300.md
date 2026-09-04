# Node Description Batch 301 of 330

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

- "tests_test_resolution_decision_test_medium_resolves_on_first_covered_clean_run": "test_medium_resolves_on_first_covered_clean_run()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L29 | neighbors=[test_resolution_decision.py] | lang=en
- "tests_test_resolution_decision_test_not_covered_is_skipped_and_counter_untouched": "test_not_covered_is_skipped_and_counter_untouched()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L15 | neighbors=[test_resolution_decision.py] | lang=en
- "tests_test_resolution_decision_test_threshold_is_stricter_for_critical_and_high": "test_threshold_is_stricter_for_critical_and_high()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L7 | neighbors=[test_resolution_decision.py] | lang=en
- "tests_test_resolve_asset_cache_rationale_1": "Perf/N+1: _resolve_asset memoizes per-run so a host with many findings is resolv" | kind=entity | source=manager/backend/tests/test_resolve_asset_cache.py:L1 | neighbors=[test_resolve_asset_cache.py] | lang=en
- "tests_test_resolve_asset_cache_test_cache_resolves_each_host_once": "test_cache_resolves_each_host_once()" | kind=code-symbol | source=manager/backend/tests/test_resolve_asset_cache.py:L15 | neighbors=[test_resolve_asset_cache.py] | lang=en
- "tests_test_resolve_asset_cache_test_host_port_target_normalized": "test_host_port_target_normalized()" | kind=code-symbol | source=manager/backend/tests/test_resolve_asset_cache.py:L42 | neighbors=[test_resolve_asset_cache.py] | lang=en
- "tests_test_resolve_asset_cache_test_no_cache_keeps_old_behavior": "test_no_cache_keeps_old_behavior()" | kind=code-symbol | source=manager/backend/tests/test_resolve_asset_cache.py:L31 | neighbors=[test_resolve_asset_cache.py] | lang=en
- "tests_test_resolve_rationale_1": "test_resolve.py — resolve() address-family selection (task A9)." | kind=entity | source=probe/tests/test_resolve.py:L1 | neighbors=[test_resolve.py] | lang=pt
- "tests_test_resolve_rationale_12": "Fake getaddrinfo results: (family, socktype, proto, canonname, sockaddr)." | kind=entity | source=probe/tests/test_resolve.py:L12 | neighbors=[_infos()] | lang=en
- "tests_test_resolve_testresolvefamily_test_unresolvable_raises": ".test_unresolvable_raises()" | kind=code-symbol | source=probe/tests/test_resolve.py:L40 | neighbors=[TestResolveFamily] | lang=en
- "tests_test_result_archive_rationale_1": "test_result_archive.py — the local result archive written before submission.  Th" | kind=entity | source=probe/tests/test_result_archive.py:L1 | neighbors=[test_result_archive.py] | lang=en
- "tests_test_result_archive_rationale_130": "A read-only filesystem must cost a warning, never a scan result." | kind=entity | source=probe/tests/test_result_archive.py:L130 | neighbors=[.test_unwritable_directory_does_not_fai…] | lang=pt
- "tests_test_result_archive_rationale_152": "Unset env => alongside agent/ scanner/ workflow/ (in the image, /app/result)." | kind=entity | source=probe/tests/test_result_archive.py:L152 | neighbors=[.test_default_location_is_the_probe_roo…] | lang=en
- "tests_test_result_archive_rationale_163": "The agent creates the archive directory at boot so the operator sees the     pat" | kind=entity | source=probe/tests/test_result_archive.py:L163 | neighbors=[TestPrepareAtStartup] | lang=en
- "tests_test_result_archive_rationale_186": "The Linux bind-mount case: Docker creates the source as root, so the         dir" | kind=entity | source=probe/tests/test_result_archive.py:L186 | neighbors=[.test_existing_but_unwritable_directory…] | lang=en
- "tests_test_result_archive_rationale_27": "The disable latch is module state; keep tests independent." | kind=entity | source=probe/tests/test_result_archive.py:L27 | neighbors=[_reset_archive_latch()] | lang=en
- "tests_test_result_archive_rationale_99": "A rejected job is exactly the case an operator wants to inspect." | kind=entity | source=probe/tests/test_result_archive.py:L99 | neighbors=[.test_failure_envelopes_are_archived_to…] | lang=en
- "tests_test_result_archive_testprepareatstartup_test_creates_the_directory_including_parents": ".test_creates_the_directory_including_parents()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L167 | neighbors=[TestPrepareAtStartup] | lang=en
- "tests_test_result_archive_testprepareatstartup_test_disabled_when_env_is_empty": ".test_disabled_when_env_is_empty()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L199 | neighbors=[TestPrepareAtStartup] | lang=en
- "tests_test_result_archive_testprepareatstartup_test_is_idempotent_across_restarts": ".test_is_idempotent_across_restarts()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L179 | neighbors=[TestPrepareAtStartup] | lang=en
- "tests_test_result_archive_testprepareatstartup_test_leaves_no_canary_file_behind": ".test_leaves_no_canary_file_behind()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L174 | neighbors=[TestPrepareAtStartup] | lang=en
- "tests_test_result_archive_testprepareatstartup_test_startup_failure_does_not_raise": ".test_startup_failure_does_not_raise()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L204 | neighbors=[TestPrepareAtStartup] | lang=en
- "tests_test_result_spool_rationale_1": "Tests for agent/result_spool.py" | kind=entity | source=probe/tests/test_result_spool.py:L1 | neighbors=[test_result_spool.py] | lang=en
- "tests_test_result_spool_rationale_13": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=probe/tests/test_result_spool.py:L13 | neighbors=[spool()] | lang=en
- "tests_test_result_spool_rationale_14": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=probe/tests/test_result_spool.py:L14 | neighbors=[spool()] | lang=en
- "tests_test_result_spool_testresultspool_test_byte_high_water_mark_pauses_new_work_without_eviction": ".test_byte_high_water_mark_pauses_new_work_without_eviction()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L194 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_custom_retry_config": ".test_custom_retry_config()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L179 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_exists": ".test_exists()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L64 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_file_high_water_mark_pauses_new_work": ".test_file_high_water_mark_pauses_new_work()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L183 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_flush_quarantines_permanent_rejection": ".test_flush_quarantines_permanent_rejection()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L166 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_flush_spool_empty": ".test_flush_spool_empty()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L135 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_flush_spool_partial": ".test_flush_spool_partial()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L154 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_flush_spool_with_pending": ".test_flush_spool_with_pending()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L139 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_load_corrupt": ".test_load_corrupt()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L57 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_load_missing": ".test_load_missing()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L53 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_max_retries_uses_class_default": ".test_max_retries_uses_class_default()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L175 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_permanent_rejection_is_quarantined_without_retry": ".test_permanent_rejection_is_quarantined_without_retry()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L121 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_rejects_job_id_path_traversal": ".test_rejects_job_id_path_traversal()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L37 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_rejects_non_positive_capacity": ".test_rejects_non_positive_capacity()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L210 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_remove": ".test_remove()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L70 | neighbors=[TestResultSpool] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-300.json

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
