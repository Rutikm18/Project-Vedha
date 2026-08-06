# Node Description Batch 125 of 134

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

- "tests_test_task_runner_testrunnerheadless_test_explicit_empty_targets_never_expand_to_engagement_scope": ".test_explicit_empty_targets_never_expand_to_engagement_scope()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L71 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_rejects_empty_targets": ".test_rejects_empty_targets()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L60 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_rejects_non_object_params": ".test_rejects_non_object_params()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L120 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_rejects_non_string_target": ".test_rejects_non_string_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L132 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_rejects_unknown_use_case": ".test_rejects_unknown_use_case()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L49 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_resolves_full_assessment": ".test_resolves_full_assessment()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L100 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_resolves_use_case_correctly": ".test_resolves_use_case_correctly()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L89 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_scan_engine_exception_becomes_submittable_failure": ".test_scan_engine_exception_becomes_submittable_failure()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L180 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_target_precedence": ".test_target_precedence()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L168 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_uses_job_type_when_no_use_case": ".test_uses_job_type_when_no_use_case()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L110 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerscantypes_test_ot_passive_profile": ".test_ot_passive_profile()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L448 | neighbors=[TestRunnerScanTypes] | lang=en
- "tests_test_task_runner_testrunnerscantypes_test_web_triage_scan_type": ".test_web_triage_scan_type()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L459 | neighbors=[TestRunnerScanTypes] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_allows_in_scope_target": ".test_allows_in_scope_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L221 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_explicit_empty_local_ceiling_fails_closed": ".test_explicit_empty_local_ceiling_fails_closed()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L237 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_local_ceiling_filters_manager_authorized_targets": ".test_local_ceiling_filters_manager_authorized_targets()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L257 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_local_ceiling_is_forwarded_to_engine": ".test_local_ceiling_is_forwarded_to_engine()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L277 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_manager_job_without_scope_fails_closed": ".test_manager_job_without_scope_fails_closed()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L354 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_merge_engagement_and_job_excludes": ".test_merge_engagement_and_job_excludes()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L366 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_rejects_excluded_target": ".test_rejects_excluded_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L303 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_scope_fallback_preserves_manager_and_job_exclusions": ".test_scope_fallback_preserves_manager_and_job_exclusions()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L331 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_transport_rationale_1": "Tests for agent/transport.py" | kind=entity | source=probe/tests/test_transport.py:L1 | neighbors=[test_transport.py] | lang=en
- "tests_test_transport_rationale_16": "Create a Transport with a real state file path but no actual HTTP calls." | kind=entity | source=probe/tests/test_transport.py:L16 | neighbors=[transport()] | lang=pt
- "tests_test_transport_rationale_18": "Create a Transport with a real state file path but no actual HTTP calls." | kind=entity | source=probe/tests/test_transport.py:L18 | neighbors=[transport()] | lang=pt
- "tests_test_transport_testdeviceenrollment_test_activation_persists_recoverable_device_credential": ".test_activation_persists_recoverable_device_credential()" | kind=code-symbol | source=probe/tests/test_transport.py:L172 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testdeviceenrollment_test_create_enrollment_request_forwards_enroll_token": ".test_create_enrollment_request_forwards_enroll_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L210 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testdeviceenrollment_test_device_refresh_signs_unique_nonce_and_rotates_access_token": ".test_device_refresh_signs_unique_nonce_and_rotates_access_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L240 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testdeviceenrollment_test_legacy_token_is_not_forced_through_device_refresh": ".test_legacy_token_is_not_forced_through_device_refresh()" | kind=code-symbol | source=probe/tests/test_transport.py:L230 | neighbors=[TestDeviceEnrollment] | lang=en
- "tests_test_transport_testfetchscope_test_http_error_returns_none": ".test_http_error_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L393 | neighbors=[TestFetchScope] | lang=en
- "tests_test_transport_testfetchscope_test_returns_scope": ".test_returns_scope()" | kind=code-symbol | source=probe/tests/test_transport.py:L383 | neighbors=[TestFetchScope] | lang=en
- "tests_test_transport_testheartbeat_test_heartbeat_401_returns_false": ".test_heartbeat_401_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L326 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testheartbeat_test_heartbeat_sends_current_job": ".test_heartbeat_sends_current_job()" | kind=code-symbol | source=probe/tests/test_transport.py:L335 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testheartbeat_test_successful_heartbeat": ".test_successful_heartbeat()" | kind=code-symbol | source=probe/tests/test_transport.py:L317 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testhttpget_test_exception_returns_none": ".test_exception_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L498 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testhttpget_test_non_200_returns_none": ".test_non_200_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L489 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testhttpget_test_successful_get": ".test_successful_get()" | kind=code-symbol | source=probe/tests/test_transport.py:L479 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testidentity_test_agent_state_updates_preserve_scope_identity": ".test_agent_state_updates_preserve_scope_identity()" | kind=code-symbol | source=probe/tests/test_transport.py:L70 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testidentity_test_auth_header": ".test_auth_header()" | kind=code-symbol | source=probe/tests/test_transport.py:L38 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testidentity_test_failed_atomic_replace_preserves_previous_state": ".test_failed_atomic_replace_preserves_previous_state()" | kind=code-symbol | source=probe/tests/test_transport.py:L107 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testidentity_test_is_authenticated_false_initially": ".test_is_authenticated_false_initially()" | kind=code-symbol | source=probe/tests/test_transport.py:L30 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testidentity_test_is_authenticated_true_with_creds": ".test_is_authenticated_true_with_creds()" | kind=code-symbol | source=probe/tests/test_transport.py:L34 | neighbors=[TestIdentity] | lang=en

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
