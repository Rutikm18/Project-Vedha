# Node Description Batch 333 of 380

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

- "tests_test_main_scripts_unauth_test_redis_silent_is_unknown": "test_redis_silent_is_unknown()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L21 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_redis_unauth_info_leak_is_true": "test_redis_unauth_info_leak_is_true()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L12 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_vantage_rationale_1": "test_main_scripts_vantage.py — multi-vantage reconciliation (P0+++ \"Multi-vantag" | kind=entity | source=probe/tests/test_main_scripts_vantage.py:L1 | neighbors=[test_main_scripts_vantage.py]
- "tests_test_manager_ai_rationale_232": "The advisor_flow rules instruct the model to use lifecycle facts, and the     re" | kind=entity | source=manager/backend/tests/test_manager_ai.py:L232 | neighbors=[test_advisor_flow_prompt_grounds_lifecy…]
- "tests_test_manager_ai_rationale_233": "Settings with provider unset and all cloud keys pinned, so .env cannot     leak" | kind=entity | source=manager/backend/tests/test_manager_ai.py:L233 | neighbors=[_cloud()]
- "tests_test_manager_ai_rationale_299": "Settings with provider unset and all cloud keys pinned, so .env cannot     leak" | kind=entity | source=manager/backend/tests/test_manager_ai.py:L299 | neighbors=[_cloud()]
- "tests_test_manager_ai_test_advisor_prompt_enforces_the_vulnerability_brief_contract": "test_advisor_prompt_enforces_the_vulnerability_brief_contract()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L253 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_ai_request_rejects_unsafe_model_and_oversized_context": "test_ai_request_rejects_unsafe_model_and_oversized_context()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L215 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_anthropic_generate_sends_prompt_cache_blocks": "test_anthropic_generate_sends_prompt_cache_blocks()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L440 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_anthropic_system_blocks_single_block_when_no_context": "test_anthropic_system_blocks_single_block_when_no_context()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L430 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_anthropic_system_blocks_split_stable_prefix_from_context": "test_anthropic_system_blocks_split_stable_prefix_from_context()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L415 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_async_llm_http_client_uses_injected_transport_and_default_timeout": "test_async_llm_http_client_uses_injected_transport_and_default_timeout()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L276 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_fallback_skips_provider_with_invalid_key": "test_fallback_skips_provider_with_invalid_key()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L491 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_gemini_is_auto_detected_and_reported_in_status": "test_gemini_is_auto_detected_and_reported_in_status()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L503 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_gemini_generation_is_server_side": "test_manager_gemini_generation_is_server_side()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L357 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_gemini_rejects_unconfigured_and_unenabled_model": "test_manager_gemini_rejects_unconfigured_and_unenabled_model()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L395 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_ollama_generation_owns_security_prompt_and_context": "test_manager_ollama_generation_owns_security_prompt_and_context()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L14 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openai_generation_is_server_side": "test_manager_openai_generation_is_server_side()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L83 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openai_rejects_unconfigured_and_unenabled_model": "test_manager_openai_rejects_unconfigured_and_unenabled_model()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L115 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openrouter_free_selection_is_server_side": "test_manager_openrouter_free_selection_is_server_side()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L52 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_rejects_cloud_model_not_enabled_by_deployment": "test_manager_rejects_cloud_model_not_enabled_by_deployment()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L151 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_rejects_ollama_cloud_proxy_as_local": "test_manager_rejects_ollama_cloud_proxy_as_local()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L200 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_rejects_unconfigured_cloud_provider": "test_manager_rejects_unconfigured_cloud_provider()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L136 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_status_returns_only_server_configured_choices": "test_manager_status_returns_only_server_configured_choices()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L169 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_non_ascii_key_is_treated_as_unconfigured_not_a_crash": "test_non_ascii_key_is_treated_as_unconfigured_not_a_crash()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L472 | neighbors=[test_manager_ai.py]
- "tests_test_manual_reopen_test_manual_reopen_restores_open_and_audits": "test_manual_reopen_restores_open_and_audits()" | kind=code-symbol | source=manager/backend/tests/test_manual_reopen.py:L9 | neighbors=[test_manual_reopen.py]
- "tests_test_msrpc_scanner_rationale_1": "test_msrpc_scanner.py — MSRPC endpoint-mapper (EPM) enumeration.  Pure summary l" | kind=entity | source=probe/tests/test_msrpc_scanner.py:L1 | neighbors=[test_msrpc_scanner.py]
- "tests_test_msrpc_scanner_rationale_28": "EPM bindings carry the dynamic RPC ports the funnel's fixed port set never     s" | kind=entity | source=probe/tests/test_msrpc_scanner.py:L28 | neighbors=[TestDynamicPorts]
- "tests_test_msrpc_scanner_testdynamicports_test_extract_tcp_and_dynamic": ".test_extract_tcp_and_dynamic()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L31 | neighbors=[TestDynamicPorts]
- "tests_test_msrpc_scanner_testdynamicports_test_out_of_range_port_dropped": ".test_out_of_range_port_dropped()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L51 | neighbors=[TestDynamicPorts]
- "tests_test_msrpc_scanner_testdynamicports_test_summarize_surfaces_dynamic_ports": ".test_summarize_surfaces_dynamic_ports()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L45 | neighbors=[TestDynamicPorts]
- "tests_test_msrpc_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L98 | neighbors=[TestParity]
- "tests_test_msrpc_scanner_testsummarize_test_distinct_interfaces_and_named": ".test_distinct_interfaces_and_named()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L19 | neighbors=[TestSummarize]
- "tests_test_nessus_scanner_scanner": "scanner()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L18 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_authenticate_api_key": "test_authenticate_api_key()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L37 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_critical": "test_map_finding_critical()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L129 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_info_severity": "test_map_finding_info_severity()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L163 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_no_cvss": "test_map_finding_no_cvss()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L170 | neighbors=[test_nessus_scanner.py]
- "tests_test_network_va_accuracy_listener_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L29 | neighbors=[_Listener]
- "tests_test_network_va_accuracy_listener_serve": "._serve()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L57 | neighbors=[_Listener]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-332.json

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
