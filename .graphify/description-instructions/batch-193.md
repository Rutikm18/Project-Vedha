# Node Description Batch 194 of 209

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

- "tests_test_scope_validator_testtargetsinexcludes_test_no_excludes_returns_all": ".test_no_excludes_returns_all()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L108 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_port_suffix_is_not_treated_as_an_ip": ".test_port_suffix_is_not_treated_as_an_ip()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L122 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testtargetsinexcludes_test_port_suffix_stripped": ".test_port_suffix_stripped()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L91 | neighbors=[TestTargetsInExcludes]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_cidr_must_be_fully_contained": ".test_cidr_must_be_fully_contained()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L62 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_empty_targets": ".test_empty_targets()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L44 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_explicit_hostname_scope_allows_exact_hostname_only": ".test_explicit_hostname_scope_allows_exact_hostname_only()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L36 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_hostname_passes_through": ".test_hostname_passes_through()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L29 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_hostname_rejected_when_scope_is_ip_only": ".test_hostname_rejected_when_scope_is_ip_only()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L29 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_invalid_cidr_ignored": ".test_invalid_cidr_ignored()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L49 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_ip_in_cidr_allowed": ".test_ip_in_cidr_allowed()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L15 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_ipv6_literal_is_validated_without_colon_truncation": ".test_ipv6_literal_is_validated_without_colon_truncation()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L77 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_multiple_cidrs": ".test_multiple_cidrs()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L84 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_outside_cidr_rejected": ".test_outside_cidr_rejected()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L22 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_port_suffix_is_not_a_valid_network_target": ".test_port_suffix_is_not_a_valid_network_target()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L55 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_port_suffix_stripped": ".test_port_suffix_stripped()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L46 | neighbors=[TestValidateTargetsInScope]
- "tests_test_scope_validator_testvalidatetargetsinscope_test_range_must_be_fully_contained": ".test_range_must_be_fully_contained()" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L69 | neighbors=[TestValidateTargetsInScope]
- "tests_test_seed_admin_rationale_1": "Tests for seed_admin.py.  Covers:   - first deployment: creates tenant + admin," | kind=entity | source=manager/backend/tests/test_seed_admin.py:L1 | neighbors=[test_seed_admin.py]
- "tests_test_seed_admin_testdatabaseunavailable_test_retries_then_raises_database_unavailable": ".test_retries_then_raises_database_unavailable()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L290 | neighbors=[TestDatabaseUnavailable]
- "tests_test_seed_admin_testdriftdetection_test_warns_on_multiple_admins": ".test_warns_on_multiple_admins()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L310 | neighbors=[TestDriftDetection]
- "tests_test_seed_admin_testdriftdetection_test_warns_on_stale_admin_emails": ".test_warns_on_stale_admin_emails()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L332 | neighbors=[TestDriftDetection]
- "tests_test_seed_admin_testexistingadminnoreset_test_noop_when_user_exists_and_no_force_reset": ".test_noop_when_user_exists_and_no_force_reset()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L141 | neighbors=[TestExistingAdminNoReset]
- "tests_test_seed_admin_testfirstdeployment_test_creates_tenant_and_admin_on_first_run": ".test_creates_tenant_and_admin_on_first_run()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L98 | neighbors=[TestFirstDeployment]
- "tests_test_seed_admin_testhashhelpers_test_different_calls_produce_different_hashes": ".test_different_calls_produce_different_hashes()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L87 | neighbors=[TestHashHelpers]
- "tests_test_seed_admin_testhashhelpers_test_hash_and_verify_round_trip": ".test_hash_and_verify_round_trip()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L78 | neighbors=[TestHashHelpers]
- "tests_test_seed_admin_testhashhelpers_test_wrong_password_fails_verify": ".test_wrong_password_fails_verify()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L83 | neighbors=[TestHashHelpers]
- "tests_test_seed_admin_testpasswordrotation_test_rotation_raises_on_hash_verify_failure": ".test_rotation_raises_on_hash_verify_failure()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L240 | neighbors=[TestPasswordRotation]
- "tests_test_seed_admin_testpasswordrotation_test_rotation_updates_hash_and_verifies": ".test_rotation_updates_hash_and_verifies()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L191 | neighbors=[TestPasswordRotation]
- "tests_test_seed_admin_testvalidateenv_test_all_known_weak_passwords_blocked_in_production": ".test_all_known_weak_passwords_blocked_in_production()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L66 | neighbors=[TestValidateEnv]
- "tests_test_seed_admin_testvalidateenv_test_allows_weak_password_in_development": ".test_allows_weak_password_in_development()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L51 | neighbors=[TestValidateEnv]
- "tests_test_seed_admin_testvalidateenv_test_raises_on_weak_password_in_production": ".test_raises_on_weak_password_in_production()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L44 | neighbors=[TestValidateEnv]
- "tests_test_seed_admin_testvalidateenv_test_raises_when_email_missing": ".test_raises_when_email_missing()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L39 | neighbors=[TestValidateEnv]
- "tests_test_seed_admin_testvalidateenv_test_returns_force_reset_true": ".test_returns_force_reset_true()" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L58 | neighbors=[TestValidateEnv]
- "tests_test_service_identifier_testserviceidentifier_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L7 | neighbors=[TestServiceIdentifier]
- "tests_test_service_match_rationale_1": "test_service_match.py — Tier 2.5: service soft-matching (banner -> product/versi" | kind=entity | source=probe/tests/test_service_match.py:L1 | neighbors=[test_service_match.py]
- "tests_test_service_match_testhttpmatch_test_apache_version": ".test_apache_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L42 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_iis_version": ".test_iis_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L47 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_nginx_version": ".test_nginx_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L36 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_nginx_without_version": ".test_nginx_without_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L52 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testnomatch_test_empty_returns_none": ".test_empty_returns_none()" | kind=code-symbol | source=probe/tests/test_service_match.py:L91 | neighbors=[TestNoMatch]
- "tests_test_service_match_testnomatch_test_unrecognized_returns_none": ".test_unrecognized_returns_none()" | kind=code-symbol | source=probe/tests/test_service_match.py:L88 | neighbors=[TestNoMatch]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-193.json

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
