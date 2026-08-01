# Node Description Batch 110 of 119

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

- "tests_test_scope_validator_testvalidatetargetsinscope_test_ip_in_cidr_allowed": ".test_ip_in_cidr_allowed()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L15 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_ipv6_literal_is_validated_without_colon_truncation": ".test_ipv6_literal_is_validated_without_colon_truncation()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L77 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_multiple_cidrs": ".test_multiple_cidrs()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L84 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_outside_cidr_rejected": ".test_outside_cidr_rejected()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L22 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_port_suffix_is_not_a_valid_network_target": ".test_port_suffix_is_not_a_valid_network_target()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L55 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_port_suffix_stripped": ".test_port_suffix_stripped()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L46 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_range_must_be_fully_contained": ".test_range_must_be_fully_contained()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L69 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_service_identifier_testserviceidentifier_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L7 | neighbors=[TestServiceIdentifier] | lang=en
- "tests_test_smb_scanner_test_garbage_response": "test_garbage_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L28 | neighbors=[test_smb_scanner.py] | lang=en
- "tests_test_task_runner_rationale_1": "Tests for agent/task_runner.py" | kind=entity | source=probe/tests/test_task_runner.py:L1 | neighbors=[test_task_runner.py] | lang=en
- "tests_test_task_runner_rationale_105": "When scope is fetched and targets are outside it." | kind=entity | source=probe/tests/test_task_runner.py:L105 | neighbors=[.test_rejects_out_of_scope_target()] | lang=en
- "tests_test_task_runner_rationale_13": "Return a minimal successful result without doing any real I/O." | kind=entity | source=probe/tests/test_task_runner.py:L13 | neighbors=[_fake_run_scan()] | lang=pt
- "tests_test_task_runner_rationale_152": "When scope fetch fails, manager-embedded scope is still enforced." | kind=entity | source=probe/tests/test_task_runner.py:L152 | neighbors=[.test_scope_fallback_when_fetch_fails()] | lang=en
- "tests_test_task_runner_rationale_201": "Verify the submit callback is called with the correct payload." | kind=entity | source=probe/tests/test_task_runner.py:L201 | neighbors=[.test_calls_submit_with_result()] | lang=en
- "tests_test_task_runner_rationale_206": "When scope is fetched and targets are outside it." | kind=entity | source=probe/tests/test_task_runner.py:L206 | neighbors=[.test_rejects_out_of_scope_target()] | lang=en
- "tests_test_task_runner_rationale_226": "When spool_submit is provided, it's used instead of direct submit." | kind=entity | source=probe/tests/test_task_runner.py:L226 | neighbors=[.test_uses_spool_when_available()] | lang=en
- "tests_test_task_runner_rationale_319": "When scope fetch fails, manager-embedded scope is still enforced." | kind=entity | source=probe/tests/test_task_runner.py:L319 | neighbors=[.test_scope_fallback_when_fetch_fails()] | lang=en
- "tests_test_task_runner_rationale_38": "TaskRunner with no-op dependencies (no real scanning)." | kind=entity | source=probe/tests/test_task_runner.py:L38 | neighbors=[runner()] | lang=en
- "tests_test_task_runner_rationale_391": "Verify the submit callback is called with the correct payload." | kind=entity | source=probe/tests/test_task_runner.py:L391 | neighbors=[.test_calls_submit_with_result()] | lang=en
- "tests_test_task_runner_rationale_416": "When spool_submit is provided, it's used instead of direct submit." | kind=entity | source=probe/tests/test_task_runner.py:L416 | neighbors=[.test_uses_spool_when_available()] | lang=en
- "tests_test_task_runner_rationale_47": "Tests that use the real engine but with no-op callbacks." | kind=entity | source=probe/tests/test_task_runner.py:L47 | neighbors=[TestRunnerHeadless] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-109.json

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
