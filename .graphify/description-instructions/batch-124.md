# Node Description Batch 125 of 144

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

- "tests_test_external_engine_wrappers_test_masscan_nonzero_with_valid_output_is_degraded": "test_masscan_nonzero_with_valid_output_is_degraded()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L103 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_range_must_be_fully_in_scope": "test_masscan_range_must_be_fully_in_scope()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L123 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_timeout_is_not_zero_findings": "test_masscan_timeout_is_not_zero_findings()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L91 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_tolerates_partial_json_and_counts_bad_records": "test_masscan_tolerates_partial_json_and_counts_bad_records()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L82 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_empty_failure_is_not_zero_findings": "test_nmap_empty_failure_is_not_zero_findings()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L42 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_extra_args_accept_bounded_tuning": "test_nmap_extra_args_accept_bounded_tuning()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L29 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_extra_args_cannot_replace_validated_targets": "test_nmap_extra_args_cannot_replace_validated_targets()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L21 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_malformed_xml_is_an_explicit_parse_error": "test_nmap_malformed_xml_is_an_explicit_parse_error()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L60 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_xml_error_state_is_preserved_as_result": "test_nmap_xml_error_state_is_preserved_as_result()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L67 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_finding_resolution_schema_test_finding_has_resolution_lifecycle_columns": "test_finding_has_resolution_lifecycle_columns()" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L6 | neighbors=[test_finding_resolution_schema.py]
- "tests_test_finding_risk_rank_api_test_finding_schema_exposes_risk_rank": "test_finding_schema_exposes_risk_rank()" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L6 | neighbors=[test_finding_risk_rank_api.py]
- "tests_test_finding_schema_test_finding_patch_accepts_documented_maximum_risk_score": "test_finding_patch_accepts_documented_maximum_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L9 | neighbors=[test_finding_schema.py]
- "tests_test_finding_schema_test_finding_patch_rejects_risk_score_above_scale": "test_finding_patch_rejects_risk_score_above_scale()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L15 | neighbors=[test_finding_schema.py]
- "tests_test_finding_schema_test_finding_summary_exposes_full_open_severity_breakdown": "test_finding_summary_exposes_full_open_severity_breakdown()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L20 | neighbors=[test_finding_schema.py]
- "tests_test_finding_verification_api_test_finding_schema_exposes_verification_fields": "test_finding_schema_exposes_verification_fields()" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_api.py:L6 | neighbors=[test_finding_verification_api.py]
- "tests_test_finding_verification_schema_test_finding_has_verification_columns": "test_finding_has_verification_columns()" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_schema.py:L6 | neighbors=[test_finding_verification_schema.py]
- "tests_test_http_lease_test_engine_cancellation_stops_async_scan_work": "test_engine_cancellation_stops_async_scan_work()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L89 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_poll_auth_failure_is_not_hidden": "test_poll_auth_failure_is_not_hidden()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L23 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_polled_job_renews_lease_until_runner_finishes": "test_polled_job_renews_lease_until_runner_finishes()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L32 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_repeated_lease_rejection_cancels_running_attempt": "test_repeated_lease_rejection_cancels_running_attempt()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L64 | neighbors=[test_http_lease.py]
- "tests_test_http_lease_test_transient_poll_failure_returns_no_jobs": "test_transient_poll_failure_returns_no_jobs()" | kind=code-symbol | source=probe/tests/test_http_lease.py:L15 | neighbors=[test_http_lease.py]
- "tests_test_hw_bind_rationale_1": "Tests for agent/hw_bind.py" | kind=entity | source=probe/tests/test_hw_bind.py:L1 | neighbors=[test_hw_bind.py]
- "tests_test_hw_bind_testcheckhwbind_test_passes_when_match": ".test_passes_when_match()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L22 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_raises_on_mismatch": ".test_raises_on_mismatch()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L28 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_raises_when_unset_and_enforced": ".test_raises_when_unset_and_enforced()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L39 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testcheckhwbind_test_skips_when_unset_and_dev_mode": ".test_skips_when_unset_and_dev_mode()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L34 | neighbors=[TestCheckHwBind]
- "tests_test_hw_bind_testgethwid_test_deterministic_within_session": ".test_deterministic_within_session()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L17 | neighbors=[TestGetHwId]
- "tests_test_hw_bind_testgethwid_test_returns_32_hex_chars": ".test_returns_32_hex_chars()" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L12 | neighbors=[TestGetHwId]
- "tests_test_installer_contract_test_installer_rejects_missing_or_unknown_arguments": "test_installer_rejects_missing_or_unknown_arguments()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L31 | neighbors=[test_installer_contract.py]
- "tests_test_installer_contract_test_installer_requires_only_manager_endpoint_in_dry_run": "test_installer_requires_only_manager_endpoint_in_dry_run()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L11 | neighbors=[test_installer_contract.py]
- "tests_test_installer_contract_test_installer_source_has_no_human_or_job_credentials": "test_installer_source_has_no_human_or_job_credentials()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L49 | neighbors=[test_installer_contract.py]
- "tests_test_integration_rationale_1": "Integration tests — full probe lifecycles exercised through the public APIs of a" | kind=entity | source=probe/tests/test_integration.py:L1 | neighbors=[test_integration.py]
- "tests_test_integration_rationale_101": "Phase 4 + Phase 1: TaskRunner receives encrypted scope and decrypts it." | kind=entity | source=probe/tests/test_integration.py:L101 | neighbors=[TestTaskRunnerWithEncryptedScope]
- "tests_test_integration_rationale_104": "Job carries encrypted_scope → TaskRunner decrypts → uses it." | kind=entity | source=probe/tests/test_integration.py:L104 | neighbors=[.test_decrypts_encrypted_scope_from_job…]
- "tests_test_integration_rationale_136": "Wrong key → decryption fails → graceful fallback to params scope." | kind=entity | source=probe/tests/test_integration.py:L136 | neighbors=[.test_falls_back_when_decryption_fails()]
- "tests_test_integration_rationale_166": "Phase 1: combined scope validation (validate + excludes)." | kind=entity | source=probe/tests/test_integration.py:L166 | neighbors=[TestScopeValidationPipeline]
- "tests_test_integration_rationale_198": "Phase 1: result spool with upload retry." | kind=entity | source=probe/tests/test_integration.py:L198 | neighbors=[TestResultSpoolWithRetry]
- "tests_test_integration_rationale_239": "Phase 4 + Phase 1: Transport sends public_key during registration." | kind=entity | source=probe/tests/test_integration.py:L239 | neighbors=[TestTransportWithIdentity]
- "tests_test_integration_rationale_260": "Backward compat: registration without public_key is fine." | kind=entity | source=probe/tests/test_integration.py:L260 | neighbors=[.test_register_without_public_key()]
- "tests_test_integration_rationale_274": "Phase 2: WebSocket message parsing." | kind=entity | source=probe/tests/test_integration.py:L274 | neighbors=[TestWebSocketMessageProtocol]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-124.json

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
