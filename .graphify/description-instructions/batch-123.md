# Node Description Batch 124 of 134

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

- "tests_test_scope_validator_testvalidatetargetsinscope_test_hostname_passes_through": ".test_hostname_passes_through()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L29 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_hostname_rejected_when_scope_is_ip_only": ".test_hostname_rejected_when_scope_is_ip_only()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L29 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_invalid_cidr_ignored": ".test_invalid_cidr_ignored()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L49 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_ip_in_cidr_allowed": ".test_ip_in_cidr_allowed()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L15 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_ipv6_literal_is_validated_without_colon_truncation": ".test_ipv6_literal_is_validated_without_colon_truncation()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L77 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_multiple_cidrs": ".test_multiple_cidrs()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L84 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_outside_cidr_rejected": ".test_outside_cidr_rejected()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L22 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_port_suffix_is_not_a_valid_network_target": ".test_port_suffix_is_not_a_valid_network_target()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L55 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_port_suffix_stripped": ".test_port_suffix_stripped()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L46 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testvalidatetargetsinscope_test_range_must_be_fully_contained": ".test_range_must_be_fully_contained()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L69 | neighbors=[TestValidateTargetsInScope] | lang=en
- "tests_test_seed_admin_rationale_1": "Tests for seed_admin.py.  Covers:   - first deployment: creates tenant + admin," | kind=entity | source=manager/backend/tests/test_seed_admin.py:L1 | neighbors=[test_seed_admin.py] | lang=en
- "tests_test_seed_admin_testdatabaseunavailable_test_retries_then_raises_database_unavailable": ".test_retries_then_raises_database_unavailable()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L290 | neighbors=[TestDatabaseUnavailable] | lang=en
- "tests_test_seed_admin_testdriftdetection_test_warns_on_multiple_admins": ".test_warns_on_multiple_admins()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L310 | neighbors=[TestDriftDetection] | lang=en
- "tests_test_seed_admin_testdriftdetection_test_warns_on_stale_admin_emails": ".test_warns_on_stale_admin_emails()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L332 | neighbors=[TestDriftDetection] | lang=en
- "tests_test_seed_admin_testexistingadminnoreset_test_noop_when_user_exists_and_no_force_reset": ".test_noop_when_user_exists_and_no_force_reset()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L141 | neighbors=[TestExistingAdminNoReset] | lang=en
- "tests_test_seed_admin_testfirstdeployment_test_creates_tenant_and_admin_on_first_run": ".test_creates_tenant_and_admin_on_first_run()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L98 | neighbors=[TestFirstDeployment] | lang=en
- "tests_test_seed_admin_testhashhelpers_test_different_calls_produce_different_hashes": ".test_different_calls_produce_different_hashes()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L87 | neighbors=[TestHashHelpers] | lang=en
- "tests_test_seed_admin_testhashhelpers_test_hash_and_verify_round_trip": ".test_hash_and_verify_round_trip()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L78 | neighbors=[TestHashHelpers] | lang=en
- "tests_test_seed_admin_testhashhelpers_test_wrong_password_fails_verify": ".test_wrong_password_fails_verify()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L83 | neighbors=[TestHashHelpers] | lang=en
- "tests_test_seed_admin_testpasswordrotation_test_rotation_raises_on_hash_verify_failure": ".test_rotation_raises_on_hash_verify_failure()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L240 | neighbors=[TestPasswordRotation] | lang=en
- "tests_test_seed_admin_testpasswordrotation_test_rotation_updates_hash_and_verifies": ".test_rotation_updates_hash_and_verifies()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L191 | neighbors=[TestPasswordRotation] | lang=en
- "tests_test_seed_admin_testvalidateenv_test_all_known_weak_passwords_blocked_in_production": ".test_all_known_weak_passwords_blocked_in_production()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L66 | neighbors=[TestValidateEnv] | lang=en
- "tests_test_seed_admin_testvalidateenv_test_allows_weak_password_in_development": ".test_allows_weak_password_in_development()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L51 | neighbors=[TestValidateEnv] | lang=en
- "tests_test_seed_admin_testvalidateenv_test_raises_on_weak_password_in_production": ".test_raises_on_weak_password_in_production()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L44 | neighbors=[TestValidateEnv] | lang=en
- "tests_test_seed_admin_testvalidateenv_test_raises_when_email_missing": ".test_raises_when_email_missing()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L39 | neighbors=[TestValidateEnv] | lang=en
- "tests_test_seed_admin_testvalidateenv_test_returns_force_reset_true": ".test_returns_force_reset_true()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L58 | neighbors=[TestValidateEnv] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-123.json

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
