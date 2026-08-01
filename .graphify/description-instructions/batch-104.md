# Node Description Batch 105 of 119

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

- "tests_test_integration_testtransportwithidentity_test_register_sends_public_key": ".test_register_sends_public_key()" | kind=code-symbol | source=probe/tests/test_integration.py:L241 | neighbors=[TestTransportWithIdentity]
- "tests_test_integration_testwebsocketmessageprotocol_test_heartbeat_message": ".test_heartbeat_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L306 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_integration_testwebsocketmessageprotocol_test_hello_message": ".test_hello_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L276 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_integration_testwebsocketmessageprotocol_test_job_push_message": ".test_job_push_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L280 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_integration_testwebsocketmessageprotocol_test_result_message": ".test_result_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L294 | neighbors=[TestWebSocketMessageProtocol]
- "tests_test_job_result_service_test_terminal_result_retry_is_idempotent": "test_terminal_result_retry_is_idempotent()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L18 | neighbors=[test_job_result_service.py]
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
- "tests_test_nuclei_background_nestedtransaction_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L23 | neighbors=[_NestedTransaction]
- "tests_test_nuclei_background_nestedtransaction_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L26 | neighbors=[_NestedTransaction]
- "tests_test_nuclei_background_scalarresult_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L15 | neighbors=[_ScalarResult]
- "tests_test_nuclei_background_scalarresult_scalar_one_or_none": ".scalar_one_or_none()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L18 | neighbors=[_ScalarResult]
- "tests_test_nuclei_background_sessionfactory_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L60 | neighbors=[_SessionFactory]
- "tests_test_nuclei_scanner_fakeprocess_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L31 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_kill": ".kill()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L61 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_terminate": ".terminate()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L57 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_wait": ".wait()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L50 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_test_missing_binary_is_a_reported_failure": "test_missing_binary_is_a_reported_failure()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L95 | neighbors=[test_nuclei_scanner.py]
- "tests_test_passive_collector_socket_fileno": ".fileno()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L28 | neighbors=[_Socket]
- "tests_test_passive_collector_socket_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L24 | neighbors=[_Socket]
- "tests_test_passive_collector_test_zero_listeners_returns_structured_failure": "test_zero_listeners_returns_structured_failure()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L135 | neighbors=[test_passive_collector.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-104.json

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
