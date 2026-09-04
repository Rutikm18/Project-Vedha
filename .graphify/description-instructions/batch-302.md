# Node Description Batch 303 of 332

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

- "tests_test_result_archive_rationale_27": "The disable latch is module state; keep tests independent." | kind=entity | source=probe/tests/test_result_archive.py:L27 | neighbors=[_reset_archive_latch()]
- "tests_test_result_archive_rationale_99": "A rejected job is exactly the case an operator wants to inspect." | kind=entity | source=probe/tests/test_result_archive.py:L99 | neighbors=[.test_failure_envelopes_are_archived_to…]
- "tests_test_result_archive_testprepareatstartup_test_creates_the_directory_including_parents": ".test_creates_the_directory_including_parents()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L167 | neighbors=[TestPrepareAtStartup]
- "tests_test_result_archive_testprepareatstartup_test_disabled_when_env_is_empty": ".test_disabled_when_env_is_empty()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L199 | neighbors=[TestPrepareAtStartup]
- "tests_test_result_archive_testprepareatstartup_test_is_idempotent_across_restarts": ".test_is_idempotent_across_restarts()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L179 | neighbors=[TestPrepareAtStartup]
- "tests_test_result_archive_testprepareatstartup_test_leaves_no_canary_file_behind": ".test_leaves_no_canary_file_behind()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L174 | neighbors=[TestPrepareAtStartup]
- "tests_test_result_archive_testprepareatstartup_test_startup_failure_does_not_raise": ".test_startup_failure_does_not_raise()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L204 | neighbors=[TestPrepareAtStartup]
- "tests_test_result_spool_rationale_1": "Tests for agent/result_spool.py" | kind=entity | source=probe/tests/test_result_spool.py:L1 | neighbors=[test_result_spool.py]
- "tests_test_result_spool_rationale_13": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=probe/tests/test_result_spool.py:L13 | neighbors=[spool()]
- "tests_test_result_spool_rationale_14": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=probe/tests/test_result_spool.py:L14 | neighbors=[spool()]
- "tests_test_result_spool_testresultspool_test_byte_high_water_mark_pauses_new_work_without_eviction": ".test_byte_high_water_mark_pauses_new_work_without_eviction()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L194 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_custom_retry_config": ".test_custom_retry_config()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L179 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_exists": ".test_exists()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L64 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_file_high_water_mark_pauses_new_work": ".test_file_high_water_mark_pauses_new_work()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L183 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_quarantines_permanent_rejection": ".test_flush_quarantines_permanent_rejection()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L166 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_empty": ".test_flush_spool_empty()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L135 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_partial": ".test_flush_spool_partial()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L154 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_with_pending": ".test_flush_spool_with_pending()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L139 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_load_corrupt": ".test_load_corrupt()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L57 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_load_missing": ".test_load_missing()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L53 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_max_retries_uses_class_default": ".test_max_retries_uses_class_default()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L175 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_permanent_rejection_is_quarantined_without_retry": ".test_permanent_rejection_is_quarantined_without_retry()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L121 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_rejects_job_id_path_traversal": ".test_rejects_job_id_path_traversal()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L37 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_rejects_non_positive_capacity": ".test_rejects_non_positive_capacity()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L210 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_remove": ".test_remove()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L70 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_remove_missing": ".test_remove_missing()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L76 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_save_and_load": ".test_save_and_load()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L19 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_save_is_atomic_no_temp_leftover": ".test_save_is_atomic_no_temp_leftover()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L26 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_spool_count": ".test_spool_count()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L80 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_spool_directory_and_result_are_private": ".test_spool_directory_and_result_are_private()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L46 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_exception": ".test_submit_with_retry_exception()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L113 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_failure": ".test_submit_with_retry_failure()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L100 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_submit_with_retry_success": ".test_submit_with_retry_success()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L87 | neighbors=[TestResultSpool]
- "tests_test_risk_port_coverage_rationale_1": "test_risk_port_coverage.py — the collection half of the exposed-service rules." | kind=entity | source=probe/tests/test_risk_port_coverage.py:L1 | neighbors=[test_risk_port_coverage.py]
- "tests_test_risk_port_coverage_rationale_101": "A connect scan is one socket per port per host, so this list is a cost as     we" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L101 | neighbors=[test_sweep_stays_within_a_sane_budget()]
- "tests_test_risk_port_coverage_rationale_110": "The sweep is profile catalog UNION the TCP branch tables; a regression that" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L110 | neighbors=[test_branch_tables_still_contribute()]
- "tests_test_risk_port_coverage_rationale_128": "The complement of the rule above, pinned so a future edit cannot quietly     add" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L128 | neighbors=[test_datagram_branch_ports_are_not_in_t…]
- "tests_test_risk_port_coverage_rationale_54": "Exactly what a default network_va puts on the wire: the profile catalog     plus" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L54 | neighbors=[_swept_by_network_va()]
- "tests_test_risk_port_coverage_rationale_72": "Called out separately: these carry the highest severity and were 100%     unscan" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L72 | neighbors=[test_every_backdoor_port_is_swept()]
- "tests_test_risk_port_coverage_rationale_81": "Reverse direction: VA_RISK_PORTS must not accumulate ports the manager has     n" | kind=entity | source=probe/tests/test_risk_port_coverage.py:L81 | neighbors=[test_va_risk_ports_are_all_actually_in_…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-302.json

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
