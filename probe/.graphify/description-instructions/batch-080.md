# Node Description Batch 81 of 92

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

- "tests_test_resolve_rationale_1": "test_resolve.py — resolve() address-family selection (task A9)." | kind=entity | source=tests/test_resolve.py:L1 | neighbors=[test_resolve.py] | lang=pt
- "tests_test_resolve_rationale_12": "Fake getaddrinfo results: (family, socktype, proto, canonname, sockaddr)." | kind=entity | source=tests/test_resolve.py:L12 | neighbors=[_infos()] | lang=en
- "tests_test_resolve_testresolvefamily_test_unresolvable_raises": ".test_unresolvable_raises()" | kind=code-symbol | source=tests/test_resolve.py:L40 | neighbors=[TestResolveFamily] | lang=en
- "tests_test_result_spool_rationale_1": "Tests for agent/result_spool.py" | kind=entity | source=tests/test_result_spool.py:L1 | neighbors=[test_result_spool.py] | lang=en
- "tests_test_result_spool_rationale_14": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=tests/test_result_spool.py:L14 | neighbors=[spool()] | lang=en
- "tests_test_result_spool_testresultspool_test_byte_high_water_mark_pauses_new_work_without_eviction": ".test_byte_high_water_mark_pauses_new_work_without_eviction()" | kind=code-symbol | source=tests/test_result_spool.py:L194 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_custom_retry_config": ".test_custom_retry_config()" | kind=code-symbol | source=tests/test_result_spool.py:L179 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_exists": ".test_exists()" | kind=code-symbol | source=tests/test_result_spool.py:L64 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_file_high_water_mark_pauses_new_work": ".test_file_high_water_mark_pauses_new_work()" | kind=code-symbol | source=tests/test_result_spool.py:L183 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_flush_quarantines_permanent_rejection": ".test_flush_quarantines_permanent_rejection()" | kind=code-symbol | source=tests/test_result_spool.py:L166 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_flush_spool_empty": ".test_flush_spool_empty()" | kind=code-symbol | source=tests/test_result_spool.py:L135 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_flush_spool_partial": ".test_flush_spool_partial()" | kind=code-symbol | source=tests/test_result_spool.py:L154 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_flush_spool_with_pending": ".test_flush_spool_with_pending()" | kind=code-symbol | source=tests/test_result_spool.py:L139 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_load_corrupt": ".test_load_corrupt()" | kind=code-symbol | source=tests/test_result_spool.py:L57 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_load_missing": ".test_load_missing()" | kind=code-symbol | source=tests/test_result_spool.py:L53 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_max_retries_uses_class_default": ".test_max_retries_uses_class_default()" | kind=code-symbol | source=tests/test_result_spool.py:L175 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_permanent_rejection_is_quarantined_without_retry": ".test_permanent_rejection_is_quarantined_without_retry()" | kind=code-symbol | source=tests/test_result_spool.py:L121 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_rejects_job_id_path_traversal": ".test_rejects_job_id_path_traversal()" | kind=code-symbol | source=tests/test_result_spool.py:L37 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_rejects_non_positive_capacity": ".test_rejects_non_positive_capacity()" | kind=code-symbol | source=tests/test_result_spool.py:L210 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_remove": ".test_remove()" | kind=code-symbol | source=tests/test_result_spool.py:L70 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_remove_missing": ".test_remove_missing()" | kind=code-symbol | source=tests/test_result_spool.py:L76 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_save_and_load": ".test_save_and_load()" | kind=code-symbol | source=tests/test_result_spool.py:L19 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_save_is_atomic_no_temp_leftover": ".test_save_is_atomic_no_temp_leftover()" | kind=code-symbol | source=tests/test_result_spool.py:L26 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_spool_count": ".test_spool_count()" | kind=code-symbol | source=tests/test_result_spool.py:L80 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_spool_directory_and_result_are_private": ".test_spool_directory_and_result_are_private()" | kind=code-symbol | source=tests/test_result_spool.py:L46 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_submit_with_retry_exception": ".test_submit_with_retry_exception()" | kind=code-symbol | source=tests/test_result_spool.py:L113 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_submit_with_retry_failure": ".test_submit_with_retry_failure()" | kind=code-symbol | source=tests/test_result_spool.py:L100 | neighbors=[TestResultSpool] | lang=en
- "tests_test_result_spool_testresultspool_test_submit_with_retry_success": ".test_submit_with_retry_success()" | kind=code-symbol | source=tests/test_result_spool.py:L87 | neighbors=[TestResultSpool] | lang=en
- "tests_test_router_db_test_mysql_greeting_on_odd_port": "test_mysql_greeting_on_odd_port()" | kind=code-symbol | source=tests/test_router_db.py:L4 | neighbors=[test_router_db.py] | lang=en
- "tests_test_router_db_test_plain_http_is_not_db": "test_plain_http_is_not_db()" | kind=code-symbol | source=tests/test_router_db.py:L13 | neighbors=[test_router_db.py] | lang=en
- "tests_test_router_db_test_redis_noauth_signature": "test_redis_noauth_signature()" | kind=code-symbol | source=tests/test_router_db.py:L9 | neighbors=[test_router_db.py] | lang=en
- "tests_test_scan_funnel_fakediscovery_init": ".__init__()" | kind=code-symbol | source=tests/test_scan_funnel.py:L23 | neighbors=[FakeDiscovery] | lang=en
- "tests_test_scan_funnel_fakediscovery_scan_target": ".scan_target()" | kind=code-symbol | source=tests/test_scan_funnel.py:L27 | neighbors=[FakeDiscovery] | lang=en
- "tests_test_scan_funnel_fakeportscanner_init": ".__init__()" | kind=code-symbol | source=tests/test_scan_funnel.py:L35 | neighbors=[FakePortScanner] | lang=en
- "tests_test_scan_funnel_fakeportscanner_scan_target": ".scan_target()" | kind=code-symbol | source=tests/test_scan_funnel.py:L40 | neighbors=[FakePortScanner] | lang=en
- "tests_test_scan_funnel_rationale_1": "test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel" | kind=entity | source=tests/test_scan_funnel.py:L1 | neighbors=[test_scan_funnel.py] | lang=en
- "tests_test_scan_funnel_rationale_65": "Build a funnel with fakes; return (funnel, discovery, port_scanner, created)." | kind=entity | source=tests/test_scan_funnel.py:L65 | neighbors=[_make_funnel()] | lang=en
- "tests_test_scan_funnel_recordingdeep_init": ".__init__()" | kind=code-symbol | source=tests/test_scan_funnel.py:L48 | neighbors=[RecordingDeep] | lang=en
- "tests_test_scan_funnel_recordingdeep_scan_target": ".scan_target()" | kind=code-symbol | source=tests/test_scan_funnel.py:L53 | neighbors=[RecordingDeep] | lang=en
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_candidate_ports_cover_all_routes": ".test_candidate_ports_cover_all_routes()" | kind=code-symbol | source=tests/test_scan_funnel.py:L210 | neighbors=[TestBuildDefaultFunnel] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-080.json

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
