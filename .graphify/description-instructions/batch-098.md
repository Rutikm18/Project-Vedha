# Node Description Batch 99 of 104

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

- "tests_test_task_runner_rationale_13": "Return a minimal successful result without doing any real I/O." | kind=entity | source=probe/tests/test_task_runner.py:L13 | neighbors=[_fake_run_scan()] | lang=pt
- "tests_test_task_runner_rationale_152": "When scope fetch fails, manager-embedded scope is still enforced." | kind=entity | source=probe/tests/test_task_runner.py:L152 | neighbors=[.test_scope_fallback_when_fetch_fails()] | lang=en
- "tests_test_task_runner_rationale_201": "Verify the submit callback is called with the correct payload." | kind=entity | source=probe/tests/test_task_runner.py:L201 | neighbors=[.test_calls_submit_with_result()] | lang=en
- "tests_test_task_runner_rationale_226": "When spool_submit is provided, it's used instead of direct submit." | kind=entity | source=probe/tests/test_task_runner.py:L226 | neighbors=[.test_uses_spool_when_available()] | lang=en
- "tests_test_task_runner_rationale_38": "TaskRunner with no-op dependencies (no real scanning)." | kind=entity | source=probe/tests/test_task_runner.py:L38 | neighbors=[runner()] | lang=en
- "tests_test_task_runner_rationale_47": "Tests that use the real engine but with no-op callbacks." | kind=entity | source=probe/tests/test_task_runner.py:L47 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_rejects_empty_targets": ".test_rejects_empty_targets()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L60 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_rejects_unknown_use_case": ".test_rejects_unknown_use_case()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L49 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_resolves_full_assessment": ".test_resolves_full_assessment()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L82 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_resolves_use_case_correctly": ".test_resolves_use_case_correctly()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L71 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_uses_job_type_when_no_use_case": ".test_uses_job_type_when_no_use_case()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L92 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerscantypes_test_ot_passive_profile": ".test_ot_passive_profile()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L258 | neighbors=[TestRunnerScanTypes] | lang=en
- "tests_test_task_runner_testrunnerscantypes_test_web_triage_scan_type": ".test_web_triage_scan_type()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L269 | neighbors=[TestRunnerScanTypes] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_allows_in_scope_target": ".test_allows_in_scope_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L120 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_manager_job_without_scope_fails_closed": ".test_manager_job_without_scope_fails_closed()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L164 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_merge_engagement_and_job_excludes": ".test_merge_engagement_and_job_excludes()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L176 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_task_runner_testrunnerscopevalidation_test_rejects_excluded_target": ".test_rejects_excluded_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L136 | neighbors=[TestRunnerScopeValidation] | lang=en
- "tests_test_transport_rationale_1": "Tests for agent/transport.py" | kind=entity | source=probe/tests/test_transport.py:L1 | neighbors=[test_transport.py] | lang=en
- "tests_test_transport_rationale_16": "Create a Transport with a real state file path but no actual HTTP calls." | kind=entity | source=probe/tests/test_transport.py:L16 | neighbors=[transport()] | lang=pt
- "tests_test_transport_testfetchscope_test_http_error_returns_none": ".test_http_error_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L173 | neighbors=[TestFetchScope] | lang=en
- "tests_test_transport_testfetchscope_test_returns_scope": ".test_returns_scope()" | kind=code-symbol | source=probe/tests/test_transport.py:L163 | neighbors=[TestFetchScope] | lang=en
- "tests_test_transport_testheartbeat_test_heartbeat_401_returns_false": ".test_heartbeat_401_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L108 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testheartbeat_test_heartbeat_sends_current_job": ".test_heartbeat_sends_current_job()" | kind=code-symbol | source=probe/tests/test_transport.py:L117 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testheartbeat_test_successful_heartbeat": ".test_successful_heartbeat()" | kind=code-symbol | source=probe/tests/test_transport.py:L99 | neighbors=[TestHeartbeat] | lang=en
- "tests_test_transport_testhttpget_test_exception_returns_none": ".test_exception_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L266 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testhttpget_test_non_200_returns_none": ".test_non_200_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L257 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testhttpget_test_successful_get": ".test_successful_get()" | kind=code-symbol | source=probe/tests/test_transport.py:L247 | neighbors=[TestHttpGet] | lang=en
- "tests_test_transport_testidentity_test_auth_header": ".test_auth_header()" | kind=code-symbol | source=probe/tests/test_transport.py:L36 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testidentity_test_is_authenticated_false_initially": ".test_is_authenticated_false_initially()" | kind=code-symbol | source=probe/tests/test_transport.py:L28 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testidentity_test_is_authenticated_true_with_creds": ".test_is_authenticated_true_with_creds()" | kind=code-symbol | source=probe/tests/test_transport.py:L32 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testidentity_test_save_and_clear_state": ".test_save_and_clear_state()" | kind=code-symbol | source=probe/tests/test_transport.py:L40 | neighbors=[TestIdentity] | lang=en
- "tests_test_transport_testpolljobs_test_poll_401_raises": ".test_poll_401_raises()" | kind=code-symbol | source=probe/tests/test_transport.py:L141 | neighbors=[TestPollJobs] | lang=en
- "tests_test_transport_testpolljobs_test_poll_uses_limit_param": ".test_poll_uses_limit_param()" | kind=code-symbol | source=probe/tests/test_transport.py:L150 | neighbors=[TestPollJobs] | lang=en
- "tests_test_transport_testpolljobs_test_returns_jobs": ".test_returns_jobs()" | kind=code-symbol | source=probe/tests/test_transport.py:L130 | neighbors=[TestPollJobs] | lang=en
- "tests_test_transport_testregister_test_registration_401_raises": ".test_registration_401_raises()" | kind=code-symbol | source=probe/tests/test_transport.py:L81 | neighbors=[TestRegister] | lang=en
- "tests_test_transport_testregister_test_registration_sends_public_key": ".test_registration_sends_public_key()" | kind=code-symbol | source=probe/tests/test_transport.py:L88 | neighbors=[TestRegister] | lang=en
- "tests_test_transport_testregister_test_successful_registration": ".test_successful_registration()" | kind=code-symbol | source=probe/tests/test_transport.py:L57 | neighbors=[TestRegister] | lang=en
- "tests_test_transport_testsubmitresult_test_2xx_variants_return_true": ".test_2xx_variants_return_true()" | kind=code-symbol | source=probe/tests/test_transport.py:L219 | neighbors=[TestSubmitResult] | lang=en
- "tests_test_transport_testsubmitresult_test_client_errors_return_false_no_data_loss": ".test_client_errors_return_false_no_data_loss()" | kind=code-symbol | source=probe/tests/test_transport.py:L209 | neighbors=[TestSubmitResult] | lang=en
- "tests_test_transport_testsubmitresult_test_large_payload_is_gzipped": ".test_large_payload_is_gzipped()" | kind=code-symbol | source=probe/tests/test_transport.py:L226 | neighbors=[TestSubmitResult] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-098.json

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
