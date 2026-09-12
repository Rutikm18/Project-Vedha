# Node Description Batch 315 of 380

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

- "tests_test_db_mongodb_auth_rationale_30": "2013 = OP_MSG. 2004 = OP_QUERY, which modern servers reject." | kind=entity | source=probe/tests/test_db_mongodb_auth.py:L30 | neighbors=[.test_opcode_is_op_msg_not_op_query()] | lang=nl
- "tests_test_db_mongodb_auth_rationale_41": "OP_MSG requires $db inside the command document." | kind=entity | source=probe/tests/test_db_mongodb_auth.py:L41 | neighbors=[.test_db_field_is_present()] | lang=en
- "tests_test_db_mongodb_auth_rationale_64": "Neither exposed nor hardened — an empty dict keeps the rule honest         inste" | kind=entity | source=probe/tests/test_db_mongodb_auth.py:L64 | neighbors=[.test_silence_claims_nothing()] | lang=en
- "tests_test_db_mongodb_auth_rationale_70": "A reply containing both must be read as enforced — the error path is         the" | kind=entity | source=probe/tests/test_db_mongodb_auth.py:L70 | neighbors=[.test_auth_marker_wins_over_ok_marker()] | lang=en
- "tests_test_db_mongodb_auth_testauthinterpretation_test_successful_serverstatus_means_exposed": ".test_successful_serverstatus_means_exposed()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L57 | neighbors=[TestAuthInterpretation] | lang=en
- "tests_test_db_mongodb_auth_testauthinterpretation_test_unauthorized_codename": ".test_unauthorized_codename()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L53 | neighbors=[TestAuthInterpretation] | lang=en
- "tests_test_db_mongodb_auth_testauthinterpretation_test_unauthorized_means_auth_enforced": ".test_unauthorized_means_auth_enforced()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L47 | neighbors=[TestAuthInterpretation] | lang=en
- "tests_test_db_mongodb_auth_testopmsgframing_test_bson_document_is_self_consistent": ".test_bson_document_is_self_consistent()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L34 | neighbors=[TestOpMsgFraming] | lang=en
- "tests_test_db_mongodb_auth_testopmsgframing_test_declared_length_matches_actual": ".test_declared_length_matches_actual()" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L25 | neighbors=[TestOpMsgFraming] | lang=en
- "tests_test_db_mysql_greeting_rationale_1": "test_db_mysql_greeting.py — MySQL TLS posture from the server's own capability f" | kind=entity | source=probe/tests/test_db_mysql_greeting.py:L1 | neighbors=[test_db_mysql_greeting.py] | lang=en
- "tests_test_db_mysql_greeting_rationale_52": "Flags present and CLIENT_SSL clear — a real negative, safe to report." | kind=entity | source=probe/tests/test_db_mysql_greeting.py:L52 | neighbors=[.test_client_ssl_absent_means_cleartext…] | lang=en
- "tests_test_db_mysql_greeting_rationale_57": "Absent evidence must not become a cleartext finding." | kind=entity | source=probe/tests/test_db_mysql_greeting.py:L57 | neighbors=[.test_short_packet_claims_nothing()] | lang=pt
- "tests_test_db_mysql_greeting_testidentification_test_non_mysql_is_rejected": ".test_non_mysql_is_rejected()" | kind=code-symbol | source=probe/tests/test_db_mysql_greeting.py:L40 | neighbors=[TestIdentification] | lang=en
- "tests_test_db_posture_rules_rationale_1": "test_db_posture_rules.py — the database rule pack.  WHY IT EXISTS. db_scan was t" | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L1 | neighbors=[test_db_posture_rules.py] | lang=en
- "tests_test_db_posture_rules_rationale_102": "MySQL 8.4.11 advertises CLIENT_SSL — must not be reported." | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L102 | neighbors=[.test_silent_on_real_tls_capable_mysql()] | lang=en
- "tests_test_db_posture_rules_rationale_107": "Absent evidence is not a cleartext finding — a short read would         otherwis" | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L107 | neighbors=[.test_silent_when_the_probe_never_learn…] | lang=pt
- "tests_test_db_posture_rules_rationale_113": "Authentication in front does not protect a cleartext channel — it         just m" | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L113 | neighbors=[.test_auth_enforced_is_not_applied()] | lang=en
- "tests_test_db_posture_rules_rationale_123": "`requires` must name ONLY paths that EVERY db_scan fact carries.          This i" | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L123 | neighbors=[.test_requires_names_only_universal_pat…] | lang=en
- "tests_test_db_posture_rules_rationale_137": "Guards the failure no unit test catches: a rule reading a path the         probe" | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L137 | neighbors=[.test_declared_inputs_exist_in_the_real…] | lang=en
- "tests_test_db_posture_rules_rationale_147": "The marker is the one thing all engines must agree on — if a probe         refac" | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L147 | neighbors=[.test_every_captured_engine_carries_the…] | lang=en
- "tests_test_db_posture_rules_rationale_40": "The real db_scan fact for one port, straight from the probe corpus." | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L40 | neighbors=[_captured()] | lang=en
- "tests_test_db_posture_rules_rationale_73": "The trap: identification alone must never imply exposure. MongoDB         answer" | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L73 | neighbors=[.test_silent_on_ismaster_only_shape()] | lang=en
- "tests_test_db_posture_rules_rationale_83": "Without the discriminator the rule must not fire on a foreign fact." | kind=entity | source=manager/detection_engine/tests/test_db_posture_rules.py:L83 | neighbors=[.test_requires_the_db_marker()] | lang=en
- "tests_test_db_posture_rules_testunauthenticatedaccess_test_severity_is_critical": ".test_severity_is_critical()" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L86 | neighbors=[TestUnauthenticatedAccess] | lang=en
- "tests_test_db_scanner_fakereader_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L18 | neighbors=[FakeReader] | lang=en
- "tests_test_db_scanner_fakereader_read": ".read()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L21 | neighbors=[FakeReader] | lang=en
- "tests_test_db_scanner_fakewriter_drain": ".drain()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L29 | neighbors=[FakeWriter] | lang=en
- "tests_test_db_scanner_fakewriter_write": ".write()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L26 | neighbors=[FakeWriter] | lang=en
- "tests_test_db_scanner_rationale_1": "Regression tests for db_scanner fingerprint matchers.  Focus: MySQL X Protocol (" | kind=entity | source=probe/tests/test_db_scanner.py:L1 | neighbors=[test_db_scanner.py] | lang=en
- "tests_test_db_tds_prelogin_rationale_1": "test_db_tds_prelogin.py — MSSQL encryption posture from the TDS PRELOGIN reply." | kind=entity | source=probe/tests/test_db_tds_prelogin.py:L1 | neighbors=[test_db_tds_prelogin.py] | lang=en
- "tests_test_db_tds_prelogin_rationale_100": "The malformed original could not elicit an ENCRYPTION option at all." | kind=entity | source=probe/tests/test_db_tds_prelogin.py:L100 | neighbors=[TestRequestIsWellFormed] | lang=en
- "tests_test_db_tds_prelogin_rationale_27": "Build a server PRELOGIN reply the way SQL Server actually frames one." | kind=entity | source=probe/tests/test_db_tds_prelogin.py:L27 | neighbors=[_prelogin_response()] | lang=en
- "tests_test_db_tds_prelogin_rationale_61": "ENCRYPT_OFF must NOT be read as 'cannot encrypt' — TDS still encrypts         th" | kind=entity | source=probe/tests/test_db_tds_prelogin.py:L61 | neighbors=[.test_off_still_supports_tls()] | lang=en
- "tests_test_db_tds_prelogin_testpositiveevidenceonly_test_garbage_does_not_raise": ".test_garbage_does_not_raise()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L89 | neighbors=[TestPositiveEvidenceOnly] | lang=en
- "tests_test_db_tds_prelogin_testrequestiswellformed_test_header_length_matches_body": ".test_header_length_matches_body()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L102 | neighbors=[TestRequestIsWellFormed] | lang=en
- "tests_test_db_tds_prelogin_testrequestiswellformed_test_option_table_parses_and_offsets_are_in_range": ".test_option_table_parses_and_offsets_are_in_range()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L106 | neighbors=[TestRequestIsWellFormed] | lang=en
- "tests_test_db_unauth_test_redis_authenticated": "test_redis_authenticated()" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L11 | neighbors=[test_db_unauth.py] | lang=en
- "tests_test_db_unauth_test_redis_unauthenticated": "test_redis_unauthenticated()" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L4 | neighbors=[test_db_unauth.py] | lang=en
- "tests_test_default_cred_rule_rationale_1": "Default-credential CANDIDATE detection.  The biggest real-world IoT risk, and a" | kind=entity | source=manager/detection_engine/tests/test_default_cred_rule.py:L1 | neighbors=[test_default_cred_rule.py] | lang=en
- "tests_test_default_cred_rule_rationale_128": "Future maintainers must not mistake this for a proven login." | kind=entity | source=manager/detection_engine/tests/test_default_cred_rule.py:L128 | neighbors=[.test_fp_notes_state_it_is_unconfirmed()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-314.json

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
