# Node Description Batch 161 of 186

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

- "tests_test_integration_rationale_315": "Simulate the full probe lifecycle from identity to result submission." | kind=entity | source=probe/tests/test_integration.py:L315 | neighbors=[.test_complete_flow_with_encrypted_scop…] | lang=en
- "tests_test_integration_rationale_383": "All targets outside scope → job is rejected cleanly." | kind=entity | source=probe/tests/test_integration.py:L383 | neighbors=[.test_job_rejected_all_targets_out_of_s…] | lang=en
- "tests_test_integration_rationale_409": "OT passive profile resolves correctly." | kind=entity | source=probe/tests/test_integration.py:L409 | neighbors=[.test_job_ot_passive_profile()] | lang=en
- "tests_test_integration_rationale_42": "Return a minimal valid scan result (no real network I/O)." | kind=entity | source=probe/tests/test_integration.py:L42 | neighbors=[_fake_run_scan()] | lang=pt
- "tests_test_integration_rationale_432": "Phase 5: startup gauntlet checks." | kind=entity | source=probe/tests/test_integration.py:L432 | neighbors=[TestStartupGauntlet] | lang=en
- "tests_test_integration_rationale_435": "With LICENSE_ENFORCED=false, gauntlet returns None." | kind=entity | source=probe/tests/test_integration.py:L435 | neighbors=[.test_gauntlet_skips_in_dev_mode()] | lang=en
- "tests_test_integration_rationale_443": "Wrong HW fingerprint blocks startup." | kind=entity | source=probe/tests/test_integration.py:L443 | neighbors=[.test_gauntlet_hw_bind_blocks()] | lang=en
- "tests_test_integration_rationale_65": "Phase 4: identity generation + scope encryption roundtrip." | kind=entity | source=probe/tests/test_integration.py:L65 | neighbors=[TestIdentityAndEncryption] | lang=en
- "tests_test_integration_rationale_68": "Generate identity → encrypt scope → decrypt scope." | kind=entity | source=probe/tests/test_integration.py:L68 | neighbors=[.test_full_identity_lifecycle()] | lang=en
- "tests_test_integration_rationale_79": "Manager encrypts → probe decrypts." | kind=entity | source=probe/tests/test_integration.py:L79 | neighbors=[.test_scope_encryption_roundtrip()] | lang=en
- "tests_test_integration_rationale_92": "A different probe cannot decrypt scope meant for another probe." | kind=entity | source=probe/tests/test_integration.py:L92 | neighbors=[.test_different_key_cannot_decrypt()] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_spool_persists_and_flushes": ".test_spool_persists_and_flushes()" | kind=code-symbol | source=probe/tests/test_integration.py:L200 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_submit_exhausts_retries": ".test_submit_exhausts_retries()" | kind=code-symbol | source=probe/tests/test_integration.py:L227 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_submit_retries_on_failure": ".test_submit_retries_on_failure()" | kind=code-symbol | source=probe/tests/test_integration.py:L216 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_accepts_in_scope_rejects_out_of_scope": ".test_accepts_in_scope_rejects_out_of_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L168 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_all_excluded_returns_empty": ".test_all_excluded_returns_empty()" | kind=code-symbol | source=probe/tests/test_integration.py:L190 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_excludes_override_scope": ".test_excludes_override_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L174 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_merge_exclusions_deduplicates": ".test_merge_exclusions_deduplicates()" | kind=code-symbol | source=probe/tests/test_integration.py:L184 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testtransportwithidentity_test_register_sends_public_key": ".test_register_sends_public_key()" | kind=code-symbol | source=probe/tests/test_integration.py:L241 | neighbors=[TestTransportWithIdentity] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_heartbeat_message": ".test_heartbeat_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L306 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_hello_message": ".test_hello_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L276 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_job_push_message": ".test_job_push_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L280 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_result_message": ".test_result_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L294 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_job_attempt_service_test_claim_creates_immutable_attempt_with_returned_fence": "test_claim_creates_immutable_attempt_with_returned_fence()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L13 | neighbors=[test_job_attempt_service.py] | lang=en
- "tests_test_job_attempt_service_test_current_fence_renews_attempt_and_logical_job": "test_current_fence_renews_attempt_and_logical_job()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L75 | neighbors=[test_job_attempt_service.py] | lang=en
- "tests_test_job_attempt_service_test_lost_claim_does_not_create_attempt": "test_lost_claim_does_not_create_attempt()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L40 | neighbors=[test_job_attempt_service.py] | lang=en
- "tests_test_job_attempt_service_test_stale_fence_cannot_renew_attempt": "test_stale_fence_cannot_renew_attempt()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L58 | neighbors=[test_job_attempt_service.py] | lang=en
- "tests_test_job_result_service_test_out_of_scope_result_is_rejected_before_database_mutation": "test_out_of_scope_result_is_rejected_before_database_mutation()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L98 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_job_result_service_test_result_scope_accepts_authorized_targets_and_control_records": "test_result_scope_accepts_authorized_targets_and_control_records()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L13 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_job_result_service_test_result_scope_fails_closed": "test_result_scope_fails_closed()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L36 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_job_result_service_test_stale_attempt_gets_terminal_receipt_without_mutation": "test_stale_attempt_gets_terminal_receipt_without_mutation()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L136 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_job_result_service_test_terminal_result_retry_is_idempotent": "test_terminal_result_retry_is_idempotent()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L51 | neighbors=[test_job_result_service.py] | lang=en
- "tests_test_loaders_rationale_1": "Tests for loader error paths in vuln_db.py and enrichment_db.py.  These are the" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L1 | neighbors=[test_loaders.py] | lang=en
- "tests_test_loaders_rationale_102": "The FileNotFoundError message should mention re-syncing, so         operators kn" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L102 | neighbors=[.test_error_message_mentions_re_sync()] | lang=en
- "tests_test_loaders_rationale_108": "The ValueError for a hash mismatch must include truncated hashes         in the" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L108 | neighbors=[.test_hash_mismatch_message_truncates_h…] | lang=en
- "tests_test_loaders_rationale_60": "A path that doesn't exist must raise FileNotFoundError with a         helpful me" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L60 | neighbors=[.test_missing_file_raises_file_not_foun…] | lang=en
- "tests_test_loaders_rationale_66": "A snapshot whose records don't match the stored content_hash must         raise" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L66 | neighbors=[.test_content_hash_mismatch_raises_valu…] | lang=en
- "tests_test_loaders_rationale_78": "Completely broken JSON must propagate as an exception — never         silently y" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L78 | neighbors=[.test_malformed_json_raises()] | lang=en
- "tests_test_loaders_rationale_86": "A JSON file that is valid JSON but missing the 'records' key         must raise" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L86 | neighbors=[.test_missing_required_key_raises()] | lang=en
- "tests_test_loaders_rationale_94": "A well-formed snapshot must load without error and return a VulnDB         that" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L94 | neighbors=[.test_valid_snapshot_loads_cleanly()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-160.json

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
