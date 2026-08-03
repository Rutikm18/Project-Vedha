# Node Description Batch 115 of 131

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_integration_testresultspoolwithretry_test_submit_retries_on_failure": ".test_submit_retries_on_failure()" | kind=code-symbol | source=probe/tests/test_integration.py:L216 | neighbors=[TestResultSpoolWithRetry]
- "tests_test_integration_testscopevalidationpipeline_test_accepts_in_scope_rejects_out_of_scope": ".test_accepts_in_scope_rejects_out_of_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L168 | neighbors=[TestScopeValidationPipeline]
- "tests_test_integration_testscopevalidationpipeline_test_all_excluded_returns_empty": ".test_all_excluded_returns_empty()" | kind=code-symbol | source=probe/tests/test_integration.py:L190 | neighbors=[TestScopeValidationPipeline]
- "tests_test_integration_testscopevalidationpipeline_test_excludes_override_scope": ".test_excludes_override_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L174 | neighbors=[TestScopeValidationPipeline]
- "tests_test_integration_testscopevalidationpipeline_test_merge_exclusions_deduplicates": ".test_merge_exclusions_deduplicates()" | kind=code-symbol | source=probe/tests/test_integration.py:L184 | neighbors=[TestScopeValidationPipeline]
- "tests_test_integration_testtransportwithidentity_test_register_sends_public_key": ".test_register_sends_public_key()" | kind=code-symbol | source=probe/tests/test_integration.py:L241 | neighbors=[TestTransportWithIdentity]
- "tests_test_integration_testwebsocketmessageprotocol_test_heartbeat_message": ".test_heartbeat_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L306 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_integration_testwebsocketmessageprotocol_test_hello_message": ".test_hello_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L276 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_integration_testwebsocketmessageprotocol_test_job_push_message": ".test_job_push_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L280 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_integration_testwebsocketmessageprotocol_test_result_message": ".test_result_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L294 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_job_attempt_service_test_claim_creates_immutable_attempt_with_returned_fence": "test_claim_creates_immutable_attempt_with_returned_fence()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L13 | neighbors=[test_job_attempt_service.py]
- "tests_test_job_attempt_service_test_current_fence_renews_attempt_and_logical_job": "test_current_fence_renews_attempt_and_logical_job()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L75 | neighbors=[test_job_attempt_service.py]
- "tests_test_job_attempt_service_test_lost_claim_does_not_create_attempt": "test_lost_claim_does_not_create_attempt()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L40 | neighbors=[test_job_attempt_service.py]
- "tests_test_job_attempt_service_test_stale_fence_cannot_renew_attempt": "test_stale_fence_cannot_renew_attempt()" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L58 | neighbors=[test_job_attempt_service.py]
- "tests_test_job_result_service_test_out_of_scope_result_is_rejected_before_database_mutation": "test_out_of_scope_result_is_rejected_before_database_mutation()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L98 | neighbors=[test_job_result_service.py]
- "tests_test_job_result_service_test_result_scope_accepts_authorized_targets_and_control_records": "test_result_scope_accepts_authorized_targets_and_control_records()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L13 | neighbors=[test_job_result_service.py]
- "tests_test_job_result_service_test_result_scope_fails_closed": "test_result_scope_fails_closed()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L36 | neighbors=[test_job_result_service.py]
- "tests_test_job_result_service_test_stale_attempt_gets_terminal_receipt_without_mutation": "test_stale_attempt_gets_terminal_receipt_without_mutation()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L136 | neighbors=[test_job_result_service.py]
- "tests_test_job_result_service_test_terminal_result_retry_is_idempotent": "test_terminal_result_retry_is_idempotent()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L51 | neighbors=[test_job_result_service.py]
- "tests_test_manager_ai_test_ai_request_rejects_unsafe_model_and_oversized_context": "test_ai_request_rejects_unsafe_model_and_oversized_context()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L214 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_ollama_generation_owns_security_prompt_and_context": "test_manager_ollama_generation_owns_security_prompt_and_context()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L13 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openai_generation_is_server_side": "test_manager_openai_generation_is_server_side()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L82 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openai_rejects_unconfigured_and_unenabled_model": "test_manager_openai_rejects_unconfigured_and_unenabled_model()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L114 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openrouter_free_selection_is_server_side": "test_manager_openrouter_free_selection_is_server_side()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L51 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_rejects_cloud_model_not_enabled_by_deployment": "test_manager_rejects_cloud_model_not_enabled_by_deployment()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L150 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_rejects_ollama_cloud_proxy_as_local": "test_manager_rejects_ollama_cloud_proxy_as_local()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L199 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_rejects_unconfigured_cloud_provider": "test_manager_rejects_unconfigured_cloud_provider()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L135 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_status_returns_only_server_configured_choices": "test_manager_status_returns_only_server_configured_choices()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L168 | neighbors=[test_manager_ai.py]
- "tests_test_nessus_scanner_scanner": "scanner()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L18 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_authenticate_api_key": "test_authenticate_api_key()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L37 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_critical": "test_map_finding_critical()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L129 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_info_severity": "test_map_finding_info_severity()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L163 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_no_cvss": "test_map_finding_no_cvss()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L170 | neighbors=[test_nessus_scanner.py]
- "tests_test_nuclei_background_fakesession_add": ".add()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L46 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L34 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L37 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_commit": ".commit()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L52 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_flush": ".flush()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L49 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L31 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_rollback": ".rollback()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L55 | neighbors=[_FakeSession]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-114.json

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
