# Node Description Batch 108 of 119

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

- "tests_test_probe_core_testtuningfromparams_test_passive_listen_seconds": ".test_passive_listen_seconds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L888 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_recheck_hours": ".test_recheck_hours()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L884 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_ssh_creds": ".test_ssh_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L872 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testtuningfromparams_test_win_creds": ".test_win_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L880 | neighbors=[TestTuningFromParams]
- "tests_test_probe_core_testusecasesresolve_test_default_discovery": ".test_default_discovery()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L940 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_fallback_to_job_type": ".test_fallback_to_job_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L936 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_fallback_to_scan_type": ".test_fallback_to_scan_type()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L931 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_full_assessment": ".test_full_assessment()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L917 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_ot_passive": ".test_ot_passive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L922 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_unknown_use_case_raises": ".test_unknown_use_case_raises()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L927 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_use_cases_count": ".test_use_cases_count()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L944 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testusecasesresolve_test_valid_use_case": ".test_valid_use_case()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L912 | neighbors=[TestUseCasesResolve]
- "tests_test_probe_core_testworkflowcache_test_get_missing": ".test_get_missing()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L754 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_load_handles_corrupt_lines": ".test_load_handles_corrupt_lines()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L805 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_save_raises_without_path": ".test_save_raises_without_path()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L800 | neighbors=[TestWorkflowCache]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_missing": ".test_should_recheck_missing()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L758 | neighbors=[TestWorkflowCache]
- "tests_test_result_spool_rationale_1": "Tests for agent/result_spool.py" | kind=entity | source=probe/tests/test_result_spool.py:L1 | neighbors=[test_result_spool.py]
- "tests_test_result_spool_rationale_13": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=probe/tests/test_result_spool.py:L13 | neighbors=[spool()]
- "tests_test_result_spool_rationale_14": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=probe/tests/test_result_spool.py:L14 | neighbors=[spool()]
- "tests_test_result_spool_testresultspool_test_custom_retry_config": ".test_custom_retry_config()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L156 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_exists": ".test_exists()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L64 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_empty": ".test_flush_spool_empty()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L121 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_partial": ".test_flush_spool_partial()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L140 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_with_pending": ".test_flush_spool_with_pending()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L125 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_load_corrupt": ".test_load_corrupt()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L57 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_load_missing": ".test_load_missing()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L53 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_max_retries_uses_class_default": ".test_max_retries_uses_class_default()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L152 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_rejects_job_id_path_traversal": ".test_rejects_job_id_path_traversal()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L37 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_remove": ".test_remove()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L70 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_remove_missing": ".test_remove_missing()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L76 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_save_and_load": ".test_save_and_load()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L19 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_save_is_atomic_no_temp_leftover": ".test_save_is_atomic_no_temp_leftover()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L26 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_spool_count": ".test_spool_count()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L80 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_spool_directory_and_result_are_private": ".test_spool_directory_and_result_are_private()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L46 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_exception": ".test_submit_with_retry_exception()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L113 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_failure": ".test_submit_with_retry_failure()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L100 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_success": ".test_submit_with_retry_success()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L87 | neighbors=[TestResultSpool]
- "tests_test_router_db_test_mysql_greeting_on_odd_port": "test_mysql_greeting_on_odd_port()" | kind=code-symbol | source=probe/tests/test_router_db.py:L4 | neighbors=[test_router_db.py]
- "tests_test_router_db_test_plain_http_is_not_db": "test_plain_http_is_not_db()" | kind=code-symbol | source=probe/tests/test_router_db.py:L13 | neighbors=[test_router_db.py]
- "tests_test_router_db_test_redis_noauth_signature": "test_redis_noauth_signature()" | kind=code-symbol | source=probe/tests/test_router_db.py:L9 | neighbors=[test_router_db.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-107.json

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
