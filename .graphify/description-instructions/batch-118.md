# Node Description Batch 119 of 131

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

- "tests_test_probe_enrollment_test_generate_enroll_token_is_prefixed_hashed_and_shown_once": "test_generate_enroll_token_is_prefixed_hashed_and_shown_once()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L92 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_public_key_must_be_canonical_base64_of_32_bytes": "test_public_key_must_be_canonical_base64_of_32_bytes()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L29 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_refresh_secret_is_stable_per_request_and_device_secret": "test_refresh_secret_is_stable_per_request_and_device_secret()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L50 | neighbors=[test_probe_enrollment.py]
- "tests_test_probe_enrollment_test_site_policy_rejects_exclusion_outside_authorized_scope": "test_site_policy_rejects_exclusion_outside_authorized_scope()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L58 | neighbors=[test_probe_enrollment.py]
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
- "tests_test_router_db_test_mysql_greeting_on_odd_port": "test_mysql_greeting_on_odd_port()" | kind=code-symbol | source=probe/tests/test_router_db.py:L4 | neighbors=[test_router_db.py]
- "tests_test_router_db_test_plain_http_is_not_db": "test_plain_http_is_not_db()" | kind=code-symbol | source=probe/tests/test_router_db.py:L13 | neighbors=[test_router_db.py]
- "tests_test_router_db_test_redis_noauth_signature": "test_redis_noauth_signature()" | kind=code-symbol | source=probe/tests/test_router_db.py:L9 | neighbors=[test_router_db.py]
- "tests_test_runtime_topology_rationale_1": "Product-boundary tests for the single-dashboard Manager API." | kind=entity | source=manager/backend/tests/test_runtime_topology.py:L1 | neighbors=[test_runtime_topology.py]
- "tests_test_runtime_topology_test_manager_does_not_mount_a_static_dashboard": "test_manager_does_not_mount_a_static_dashboard()" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L6 | neighbors=[test_runtime_topology.py]
- "tests_test_runtime_topology_test_manager_root_is_service_metadata": "test_manager_root_is_service_metadata()" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L13 | neighbors=[test_runtime_topology.py]
- "tests_test_scope_crypt_rationale_1": "Tests for agent/scope_crypt.py" | kind=entity | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[test_scope_crypt.py]
- "tests_test_scope_crypt_rationale_79": "Each encryption uses a fresh ephemeral key, so blobs are different." | kind=entity | source=probe/tests/test_scope_crypt.py:L79 | neighbors=[.test_multiple_encrypts_different()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_b64_roundtrip": ".test_b64_roundtrip()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L70 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_plaintexts_are_distinct": ".test_different_plaintexts_are_distinct()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L64 | neighbors=[TestEncryptDecryptRoundtrip]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-118.json

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
