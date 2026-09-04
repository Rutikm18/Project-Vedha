# Node Description Batch 272 of 332

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

- "tests_test_auth_login_testreasoncodes_test_bcrypt_failure_code": ".test_bcrypt_failure_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L242 | neighbors=[TestReasonCodes] | lang=en
- "tests_test_auth_login_testreasoncodes_test_database_failure_code": ".test_database_failure_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L245 | neighbors=[TestReasonCodes] | lang=en
- "tests_test_auth_login_testreasoncodes_test_disabled_tenant_code": ".test_disabled_tenant_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L236 | neighbors=[TestReasonCodes] | lang=en
- "tests_test_auth_login_testreasoncodes_test_disabled_user_code": ".test_disabled_user_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L233 | neighbors=[TestReasonCodes] | lang=en
- "tests_test_auth_login_testreasoncodes_test_expired_password_code": ".test_expired_password_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L239 | neighbors=[TestReasonCodes] | lang=en
- "tests_test_auth_login_testreasoncodes_test_password_mismatch_code": ".test_password_mismatch_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L230 | neighbors=[TestReasonCodes] | lang=en
- "tests_test_auth_login_testreasoncodes_test_user_not_found_code": ".test_user_not_found_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L227 | neighbors=[TestReasonCodes] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_bcrypt_round_trip_passes": ".test_bcrypt_round_trip_passes()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L277 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_cookie_config_fatal_in_production": ".test_cookie_config_fatal_in_production()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L283 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_cookie_config_ok_in_development": ".test_cookie_config_ok_in_development()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L293 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_database_check_returns_fatal_on_connection_error": ".test_database_check_returns_fatal_on_connection_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L303 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_known_weak_is_fatal": ".test_jwt_secret_known_weak_is_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L261 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_strong_is_ok": ".test_jwt_secret_strong_is_ok()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L269 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_too_short_is_fatal": ".test_jwt_secret_too_short_is_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L253 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_redis_check_returns_fatal_on_connection_error": ".test_redis_check_returns_fatal_on_connection_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L313 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_auth_login_teststartupdiagnostics_test_run_all_aborts_on_fatal": ".test_run_all_aborts_on_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L322 | neighbors=[TestStartupDiagnostics] | lang=en
- "tests_test_branch_registry_rationale_1": "test_branch_registry.py — the deep-scan branch registry and the invariants it ex" | kind=entity | source=probe/tests/test_branch_registry.py:L1 | neighbors=[test_branch_registry.py] | lang=en
- "tests_test_branch_registry_rationale_113": "Before the registry, these five planned NOTHING while the engine ran five     co" | kind=entity | source=probe/tests/test_branch_registry.py:L113 | neighbors=[test_service_specific_plan_matches_what…] | lang=en
- "tests_test_branch_registry_rationale_143": "An SNMP-only job must not fall back to a broad TCP sweep." | kind=entity | source=probe/tests/test_branch_registry.py:L143 | neighbors=[test_datagram_branches_need_no_tcp_stag…] | lang=en
- "tests_test_branch_registry_rationale_158": "smb's fact describes the host, so it must be keyed by (host, None) — not     by" | kind=entity | source=probe/tests/test_branch_registry.py:L158 | neighbors=[test_host_level_branch_is_cached_under_…] | lang=en
- "tests_test_branch_registry_rationale_185": "The database branch is the one spec that runs its scanner twice: known     engin" | kind=entity | source=probe/tests/test_branch_registry.py:L185 | neighbors=[test_db_branch_splits_known_and_router_…] | lang=en
- "tests_test_branch_registry_rationale_205": "SNMPScanner's signature has no `ports`; passing one would TypeError." | kind=entity | source=probe/tests/test_branch_registry.py:L205 | neighbors=[test_snmp_scanner_is_constructed_withou…] | lang=en
- "tests_test_branch_registry_rationale_36": "A spec the profile tables don't know about could never run." | kind=entity | source=probe/tests/test_branch_registry.py:L36 | neighbors=[.test_every_branch_is_gateable()] | lang=en
- "tests_test_branch_registry_rationale_41": "gate_5 intersects open ports with its own table; the engine uses the         spe" | kind=entity | source=probe/tests/test_branch_registry.py:L41 | neighbors=[.test_port_tables_match_gates()] | lang=en
- "tests_test_branch_registry_rationale_66": "A fact whose scanner name has no merge handler is collected, cached,         shi" | kind=entity | source=probe/tests/test_branch_registry.py:L66 | neighbors=[.test_every_component_can_be_merged_int…] | lang=en
- "tests_test_branch_registry_rationale_72": "An unlisted scanner falls back to 'uncertain' (re-probed every pass).         Th" | kind=entity | source=probe/tests/test_branch_registry.py:L72 | neighbors=[.test_every_component_has_a_cache_certa…] | lang=en
- "tests_test_branch_registry_test_full_assessment_plans_every_branch": "test_full_assessment_plans_every_branch()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L132 | neighbors=[test_branch_registry.py] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_branch_component_map_is_derived": ".test_branch_component_map_is_derived()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L62 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_catalog_entries_are_labelled": ".test_catalog_entries_are_labelled()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L58 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_components_are_unique": ".test_components_are_unique()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L77 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_every_branch_has_a_scanner_the_engine_can_resolve": ".test_every_branch_has_a_scanner_the_engine_can_resolve()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L49 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_every_component_is_in_the_plan_catalog": ".test_every_component_is_in_the_plan_catalog()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L53 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_branch_registry_testregistryconsistency_test_kwargs_builders_have_the_expected_signature": ".test_kwargs_builders_have_the_expected_signature()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L81 | neighbors=[TestRegistryConsistency] | lang=en
- "tests_test_campaign_progress_rationale_1": "VA Campaigns live view: per-probe jobs + pipeline phases + findings+remediation." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L1 | neighbors=[test_campaign_progress.py] | lang=en
- "tests_test_campaign_progress_rationale_118": "Build a campaign_progress scenario with a given job + detection-run state." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L118 | neighbors=[_run_scenario()] | lang=pt
- "tests_test_campaign_progress_rationale_168": "Regression: RUN_COMPLETED is 'completed', not 'done' — the endpoint must not" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L168 | neighbors=[test_completed_run_is_not_stuck_at_dete…] | lang=en
- "tests_test_campaign_progress_rationale_218": "The invariant. Checked across the states a real campaign passes through." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L218 | neighbors=[test_percent_reaches_100_exactly_when_t…] | lang=en
- "tests_test_campaign_progress_rationale_22": "A result whose .all() returns raw rows (used for the queue-state query)." | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L22 | neighbors=[_rows()] | lang=en
- "tests_test_campaign_progress_rationale_239": "The exact regression: the newest submission was detected, an earlier one was" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L239 | neighbors=[test_uncovered_submission_holds_progres…] | lang=en
- "tests_test_campaign_progress_rationale_268": "The other way a campaign never finishes: a run that starts and never     complet" | kind=entity | source=manager/backend/tests/test_campaign_progress.py:L268 | neighbors=[test_a_wedged_detection_run_explains_it…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-271.json

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
