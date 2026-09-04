# Node Description Batch 164 of 332

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

- "tests_test_scope_targets_test_property_every_accepted_target_is_subnet_of_scope": "test_property_every_accepted_target_is_subnet_of_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L98 | neighbors=[test_scope_targets.py, Whatever the validator accepts must be …]
- "tests_test_scope_targets_testnoscopeauthorizesnothing": "TestNoScopeAuthorizesNothing" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L15 | neighbors=[test_scope_targets.py, .test_empty_scope_denies_all()]
- "tests_test_seed_admin_testdatabaseunavailable": "TestDatabaseUnavailable" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L288 | neighbors=[test_seed_admin.py, .test_retries_then_raises_database_unav…]
- "tests_test_seed_admin_testexistingadminnoreset": "TestExistingAdminNoReset" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L139 | neighbors=[test_seed_admin.py, .test_noop_when_user_exists_and_no_forc…]
- "tests_test_seed_admin_testfirstdeployment": "TestFirstDeployment" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L96 | neighbors=[test_seed_admin.py, .test_creates_tenant_and_admin_on_first…]
- "tests_test_service_banner_ident_self_signed": "_self_signed()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L247 | neighbors=[test_service_banner_ident.py, test_https_on_arbitrary_port_identifies…]
- "tests_test_service_banner_ident_test_prefers_decrypted_tls_reply_over_plaintext_noise": "test_prefers_decrypted_tls_reply_over_plaintext_noise()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L196 | neighbors=[test_service_banner_ident.py, _scanner()]
- "tests_test_service_banner_ident_test_slow_greeting_still_identifies": "test_slow_greeting_still_identifies()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L170 | neighbors=[test_service_banner_ident.py, A speak-first daemon that delays its 22…]
- "tests_test_service_banner_ident_testladder_test_client_first_ports_skip_null_rung": ".test_client_first_ports_skip_null_rung()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L147 | neighbors=[TestLadder, _scanner()]
- "tests_test_service_banner_ident_testladder_test_greet_timeout_tracks_operator_timeout": ".test_greet_timeout_tracks_operator_timeout()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L156 | neighbors=[TestLadder, _scanner()]
- "tests_test_service_banner_ident_testladder_test_no_tls_flag_drops_rung": ".test_no_tls_flag_drops_rung()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L153 | neighbors=[TestLadder, _scanner()]
- "tests_test_service_identifier_rationale_1": "Unit tests for ServiceIdentifier." | kind=entity | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[test_service_identifier.py, ServiceIdentifier]
- "tests_test_service_identifier_testserviceidentifier_test_confidence_floor_port_hint": ".test_confidence_floor_port_hint()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L70 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ftp_banner": ".test_ftp_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L28 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_high_confidence_combined": ".test_high_confidence_combined()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L75 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_http_server_header": ".test_http_server_header()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L19 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_kerberos_banner": ".test_kerberos_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L48 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ldap_banner": ".test_ldap_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L52 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_mssql_banner": ".test_mssql_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L44 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_mysql_banner": ".test_mysql_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L36 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_rdp_port_hint": ".test_rdp_port_hint()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L56 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_redis_pong": ".test_redis_pong()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L40 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_smb_detection": ".test_smb_detection()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L32 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_smtp_banner": ".test_smtp_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L24 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ssh_banner": ".test_ssh_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L13 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_unknown_service_empty_banner": ".test_unknown_service_empty_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L65 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_version_extraction": ".test_version_extraction()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L61 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_match_testscannerintegration": "TestScannerIntegration" | kind=code-symbol | source=probe/tests/test_service_match.py:L108 | neighbors=[test_service_match.py, .test_scanner_identifies_ssh_on_nonstan…]
- "tests_test_service_posture_rules_test_new_rules_agree_with_probe_findings_severity": "test_new_rules_agree_with_probe_findings_severity()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L227 | neighbors=[test_service_posture_rules.py, The manager and the probe's own finding…]
- "tests_test_service_posture_rules_test_smb_null_session_fires_when_permitted": "test_smb_null_session_fires_when_permitted()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L106 | neighbors=[test_service_posture_rules.py, _fire()]
- "tests_test_service_posture_rules_test_ssh_terrapin_fires_when_strict_kex_absent": "test_ssh_terrapin_fires_when_strict_kex_absent()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L80 | neighbors=[test_service_posture_rules.py, _fire()]
- "tests_test_service_posture_rules_test_ssh_weak_algorithms": "test_ssh_weak_algorithms()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L87 | neighbors=[test_service_posture_rules.py, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_dns_refused_transfer": ".test_dns_refused_transfer()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L121 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_ftp_without_anonymous": ".test_ftp_without_anonymous()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L117 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_ipmi_cipher_zero_rejected": ".test_ipmi_cipher_zero_rejected()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L158 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_ldap_bind_refused": ".test_ldap_bind_refused()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L130 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_nfs_restricted_exports": ".test_nfs_restricted_exports()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L126 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_rsync_auth_required": ".test_rsync_auth_required()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L153 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_smtp_with_starttls": ".test_smtp_with_starttls()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L149 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_vnc_weak_fires_when_it_is_the_only_option": ".test_vnc_weak_fires_when_it_is_the_only_option()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L144 | neighbors=[TestNegatives, _fire()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-163.json

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
