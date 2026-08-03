# Node Description Batch 110 of 131

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

- "tests_test_auth_login_teststartupdiagnostics_test_redis_check_returns_fatal_on_connection_error": ".test_redis_check_returns_fatal_on_connection_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L313 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_run_all_aborts_on_fatal": ".test_run_all_aborts_on_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L322 | neighbors=[TestStartupDiagnostics]
- "tests_test_cli_fakeclient_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_cli.py:L153 | neighbors=[FakeClient]
- "tests_test_cli_fakeclient_request": ".request()" | kind=code-symbol | source=probe/tests/test_cli.py:L157 | neighbors=[FakeClient]
- "tests_test_cli_test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity": "test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity()" | kind=code-symbol | source=probe/tests/test_cli.py:L318 | neighbors=[test_cli.py]
- "tests_test_cli_test_cmd_doctor_fails_when_no_agent_unless_allowed": "test_cmd_doctor_fails_when_no_agent_unless_allowed()" | kind=code-symbol | source=probe/tests/test_cli.py:L248 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_rejects_malformed_json": "test_config_store_rejects_malformed_json()" | kind=code-symbol | source=probe/tests/test_cli.py:L31 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_rejects_non_object_profiles": "test_config_store_rejects_non_object_profiles()" | kind=code-symbol | source=probe/tests/test_cli.py:L38 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_writes_private_file": "test_config_store_writes_private_file()" | kind=code-symbol | source=probe/tests/test_cli.py:L13 | neighbors=[test_cli.py]
- "tests_test_cli_test_normalize_manager_url_trims_and_validates": "test_normalize_manager_url_trims_and_validates()" | kind=code-symbol | source=probe/tests/test_cli.py:L72 | neighbors=[test_cli.py]
- "tests_test_cli_test_parse_param_pairs_rejects_missing_equals": "test_parse_param_pairs_rejects_missing_equals()" | kind=code-symbol | source=probe/tests/test_cli.py:L59 | neighbors=[test_cli.py]
- "tests_test_cli_test_parse_param_pairs_supports_json_values": "test_parse_param_pairs_supports_json_values()" | kind=code-symbol | source=probe/tests/test_cli.py:L45 | neighbors=[test_cli.py]
- "tests_test_cli_test_parser_accepts_json_after_concrete_commands": "test_parser_accepts_json_after_concrete_commands()" | kind=code-symbol | source=probe/tests/test_cli.py:L80 | neighbors=[test_cli.py]
- "tests_test_cli_test_resolve_profile_env_overrides_config": "test_resolve_profile_env_overrides_config()" | kind=code-symbol | source=probe/tests/test_cli.py:L106 | neighbors=[test_cli.py]
- "tests_test_cli_test_resolve_profile_reports_missing_manager_or_token": "test_resolve_profile_reports_missing_manager_or_token()" | kind=code-symbol | source=probe/tests/test_cli.py:L134 | neighbors=[test_cli.py]
- "tests_test_cli_test_split_values_accepts_repeated_and_csv_values": "test_split_values_accepts_repeated_and_csv_values()" | kind=code-symbol | source=probe/tests/test_cli.py:L64 | neighbors=[test_cli.py]
- "tests_test_db_scanner_fakereader_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L18 | neighbors=[FakeReader]
- "tests_test_db_scanner_fakereader_read": ".read()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L21 | neighbors=[FakeReader]
- "tests_test_db_scanner_fakewriter_drain": ".drain()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L29 | neighbors=[FakeWriter]
- "tests_test_db_scanner_fakewriter_write": ".write()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L26 | neighbors=[FakeWriter]
- "tests_test_db_scanner_rationale_1": "Regression tests for db_scanner fingerprint matchers.  Focus: MySQL X Protocol (" | kind=entity | source=probe/tests/test_db_scanner.py:L1 | neighbors=[test_db_scanner.py]
- "tests_test_db_unauth_test_redis_authenticated": "test_redis_authenticated()" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L11 | neighbors=[test_db_unauth.py]
- "tests_test_db_unauth_test_redis_unauthenticated": "test_redis_unauthenticated()" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L4 | neighbors=[test_db_unauth.py]
- "tests_test_detection_core_testallosvsourcepackages_test_returns_list": ".test_returns_list()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L994 | neighbors=[TestAllOsvSourcePackages]
- "tests_test_detection_core_testallosvsourcepackages_test_sorted": ".test_sorted()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L999 | neighbors=[TestAllOsvSourcePackages]
- "tests_test_detection_core_testasset_test_add_alias": ".test_add_alias()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L157 | neighbors=[TestAsset]
- "tests_test_detection_core_testclassifyconfidence_test_authoritative_scanners": ".test_authoritative_scanners()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L203 | neighbors=[TestClassifyConfidence]
- "tests_test_detection_core_testclassifyconfidence_test_inferred_scanners": ".test_inferred_scanners()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L207 | neighbors=[TestClassifyConfidence]
- "tests_test_detection_core_testcleandebianversion_test_no_revision": ".test_no_revision()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L982 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleandebianversion_test_strips_epoch": ".test_strips_epoch()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L977 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleandebianversion_test_strips_revision": ".test_strips_revision()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L972 | neighbors=[TestCleanDebianVersion]
- "tests_test_detection_core_testcleanrpmversion_test_strips_release": ".test_strips_release()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L989 | neighbors=[TestCleanRpmVersion]
- "tests_test_detection_core_testcorrelatesmbpatch_test_no_smb_facts_returns_none": ".test_no_smb_facts_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L561 | neighbors=[TestCorrelateSmbPatch]
- "tests_test_detection_core_testcvss_test_known_vectors": ".test_known_vectors()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L286 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_parse_vector": ".test_parse_vector()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L298 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_returns_none_for_malformed": ".test_returns_none_for_malformed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L294 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_returns_none_for_v2_vector": ".test_returns_none_for_v2_vector()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L291 | neighbors=[TestCvss]
- "tests_test_detection_core_testcvss_test_roundup_exact_boundary": ".test_roundup_exact_boundary()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L303 | neighbors=[TestCvss]
- "tests_test_detection_core_testdeceptionscore_test_capped_at_1": ".test_capped_at_1()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L633 | neighbors=[TestDeceptionScore]
- "tests_test_detection_core_testdeceptionscore_test_combined_high": ".test_combined_high()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L630 | neighbors=[TestDeceptionScore]

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
