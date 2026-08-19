# Node Description Batch 212 of 227

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
- "tests_test_service_match_testotherservices_test_mariadb_handshake": ".test_mariadb_handshake()" | kind=code-symbol | source=probe/tests/test_service_match.py:L70 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_info": ".test_redis_info()" | kind=code-symbol | source=probe/tests/test_service_match.py:L77 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_noauth": ".test_redis_noauth()" | kind=code-symbol | source=probe/tests/test_service_match.py:L82 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_smtp_postfix": ".test_smtp_postfix()" | kind=code-symbol | source=probe/tests/test_service_match.py:L65 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_vsftpd": ".test_vsftpd()" | kind=code-symbol | source=probe/tests/test_service_match.py:L59 | neighbors=[TestOtherServices]
- "tests_test_service_match_testprobeladder_test_ladder_has_http_and_generic": ".test_ladder_has_http_and_generic()" | kind=code-symbol | source=probe/tests/test_service_match.py:L102 | neighbors=[TestProbeLadder]
- "tests_test_service_match_testprobeladder_test_ladder_starts_with_null_probe": ".test_ladder_starts_with_null_probe()" | kind=code-symbol | source=probe/tests/test_service_match.py:L96 | neighbors=[TestProbeLadder]
- "tests_test_service_match_testscannerintegration_test_scanner_identifies_ssh_on_nonstandard_port": ".test_scanner_identifies_ssh_on_nonstandard_port()" | kind=code-symbol | source=probe/tests/test_service_match.py:L109 | neighbors=[TestScannerIntegration]
- "tests_test_service_match_testsshmatch_test_dropbear": ".test_dropbear()" | kind=code-symbol | source=probe/tests/test_service_match.py:L23 | neighbors=[TestSshMatch]
- "tests_test_service_match_testsshmatch_test_generic_ssh": ".test_generic_ssh()" | kind=code-symbol | source=probe/tests/test_service_match.py:L29 | neighbors=[TestSshMatch]
- "tests_test_service_match_testsshmatch_test_openssh_version": ".test_openssh_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L17 | neighbors=[TestSshMatch]
- "tests_test_sla_policy_rationale_1": "test_sla_policy.py — per-tenant custom SLA windows (item 4)." | kind=entity | source=manager/backend/tests/test_sla_policy.py:L1 | neighbors=[test_sla_policy.py]
- "tests_test_smb_scanner_rationale_15": "An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns     this" | kind=entity | source=probe/tests/test_smb_scanner.py:L15 | neighbors=[_smb2_error_response()]
- "tests_test_smb_scanner_rationale_51": "The confirmed bug: an SMB2 error response (STATUS_INVALID_PARAMETER) was     rea" | kind=entity | source=probe/tests/test_smb_scanner.py:L51 | neighbors=[test_error_response_not_parsed_as_signi…]
- "tests_test_smb_scanner_rationale_63": "A response with the wrong body StructureSize is not a valid NEGOTIATE." | kind=entity | source=probe/tests/test_smb_scanner.py:L63 | neighbors=[test_truncated_negotiate_body_not_parse…]
- "tests_test_smb_scanner_rationale_72": "Step 13: expose signing_supported (protocol-precise), not only the     ambiguous" | kind=entity | source=probe/tests/test_smb_scanner.py:L72 | neighbors=[test_signing_supported_field_present()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-211.json

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
