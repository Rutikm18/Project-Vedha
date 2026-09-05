# Node Description Batch 276 of 336

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

- "tests_test_attack_paths_testpathanalyzer_test_find_paths_to_target": ".test_find_paths_to_target()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L114 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_identify_chokepoints": ".test_identify_chokepoints()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L150 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_no_paths_for_unknown_target": ".test_no_paths_for_unknown_target()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L129 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_paths_sorted_by_risk_desc": ".test_paths_sorted_by_risk_desc()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L123 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_score_path_clamped_0_100": ".test_score_path_clamped_0_100()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L145 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_score_path_credential_reuse_bonus": ".test_score_path_credential_reuse_bonus()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L139 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_score_path_rewards_cvss_penalises_hops": ".test_score_path_rewards_cvss_penalises_hops()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L133 | neighbors=[TestPathAnalyzer]
- "tests_test_auth_login_rationale_1": "Tests for authentication login flow.  Covers:   - login success   - user_not_fou" | kind=entity | source=manager/backend/tests/test_auth_login.py:L1 | neighbors=[test_auth_login.py]
- "tests_test_auth_login_rationale_224": "Ensure every exception class has the expected reason_code attribute.     These c" | kind=entity | source=manager/backend/tests/test_auth_login.py:L224 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_rationale_70": "AsyncSession mock that returns user on first execute, tenant on second." | kind=entity | source=manager/backend/tests/test_auth_login.py:L70 | neighbors=[_make_db()]
- "tests_test_auth_login_testauthenticatedatabasefailure_test_raises_database_failure_on_sqlalchemy_error": ".test_raises_database_failure_on_sqlalchemy_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L183 | neighbors=[TestAuthenticateDatabaseFailure]
- "tests_test_auth_login_testreasoncodes_test_bcrypt_failure_code": ".test_bcrypt_failure_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L242 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_database_failure_code": ".test_database_failure_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L245 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_disabled_tenant_code": ".test_disabled_tenant_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L236 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_disabled_user_code": ".test_disabled_user_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L233 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_expired_password_code": ".test_expired_password_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L239 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_password_mismatch_code": ".test_password_mismatch_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L230 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_user_not_found_code": ".test_user_not_found_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L227 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_teststartupdiagnostics_test_bcrypt_round_trip_passes": ".test_bcrypt_round_trip_passes()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L277 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_cookie_config_fatal_in_production": ".test_cookie_config_fatal_in_production()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L283 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_cookie_config_ok_in_development": ".test_cookie_config_ok_in_development()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L293 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_database_check_returns_fatal_on_connection_error": ".test_database_check_returns_fatal_on_connection_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L303 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_known_weak_is_fatal": ".test_jwt_secret_known_weak_is_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L261 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_strong_is_ok": ".test_jwt_secret_strong_is_ok()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L269 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_too_short_is_fatal": ".test_jwt_secret_too_short_is_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L253 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_redis_check_returns_fatal_on_connection_error": ".test_redis_check_returns_fatal_on_connection_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L313 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_run_all_aborts_on_fatal": ".test_run_all_aborts_on_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L322 | neighbors=[TestStartupDiagnostics]
- "tests_test_branch_registry_rationale_1": "test_branch_registry.py — the deep-scan branch registry and the invariants it ex" | kind=entity | source=probe/tests/test_branch_registry.py:L1 | neighbors=[test_branch_registry.py]
- "tests_test_branch_registry_rationale_113": "Before the registry, these five planned NOTHING while the engine ran five     co" | kind=entity | source=probe/tests/test_branch_registry.py:L113 | neighbors=[test_service_specific_plan_matches_what…]
- "tests_test_branch_registry_rationale_143": "An SNMP-only job must not fall back to a broad TCP sweep." | kind=entity | source=probe/tests/test_branch_registry.py:L143 | neighbors=[test_datagram_branches_need_no_tcp_stag…]
- "tests_test_branch_registry_rationale_158": "smb's fact describes the host, so it must be keyed by (host, None) — not     by" | kind=entity | source=probe/tests/test_branch_registry.py:L158 | neighbors=[test_host_level_branch_is_cached_under_…]
- "tests_test_branch_registry_rationale_185": "The database branch is the one spec that runs its scanner twice: known     engin" | kind=entity | source=probe/tests/test_branch_registry.py:L185 | neighbors=[test_db_branch_splits_known_and_router_…]
- "tests_test_branch_registry_rationale_205": "SNMPScanner's signature has no `ports`; passing one would TypeError." | kind=entity | source=probe/tests/test_branch_registry.py:L205 | neighbors=[test_snmp_scanner_is_constructed_withou…]
- "tests_test_branch_registry_rationale_36": "A spec the profile tables don't know about could never run." | kind=entity | source=probe/tests/test_branch_registry.py:L36 | neighbors=[.test_every_branch_is_gateable()]
- "tests_test_branch_registry_rationale_41": "gate_5 intersects open ports with its own table; the engine uses the         spe" | kind=entity | source=probe/tests/test_branch_registry.py:L41 | neighbors=[.test_port_tables_match_gates()]
- "tests_test_branch_registry_rationale_66": "A fact whose scanner name has no merge handler is collected, cached,         shi" | kind=entity | source=probe/tests/test_branch_registry.py:L66 | neighbors=[.test_every_component_can_be_merged_int…]
- "tests_test_branch_registry_rationale_72": "An unlisted scanner falls back to 'uncertain' (re-probed every pass).         Th" | kind=entity | source=probe/tests/test_branch_registry.py:L72 | neighbors=[.test_every_component_has_a_cache_certa…]
- "tests_test_branch_registry_test_full_assessment_plans_every_branch": "test_full_assessment_plans_every_branch()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L132 | neighbors=[test_branch_registry.py]
- "tests_test_branch_registry_testregistryconsistency_test_branch_component_map_is_derived": ".test_branch_component_map_is_derived()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L62 | neighbors=[TestRegistryConsistency]
- "tests_test_branch_registry_testregistryconsistency_test_catalog_entries_are_labelled": ".test_catalog_entries_are_labelled()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L58 | neighbors=[TestRegistryConsistency]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-275.json

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
