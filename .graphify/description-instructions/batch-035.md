# Node Description Batch 36 of 131

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

- "scripts_seed_admin_log_info": "log_info()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L81 | neighbors=[seed_admin.py, _log(), main(), _seed_once()]
- "scripts_seed_admin_rationale_1": "Idempotent admin seeder — production-grade rewrite.  Behavior:   First run : cre" | kind=entity | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[seed_admin.py, UserRole, Tenant, User]
- "scripts_seed_admin_validate_env": "_validate_env()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L95 | neighbors=[seed_admin.py, main(), Returns (email, password, tenant_name, …, log_warn()]
- "scripts_startup_validator_databaseconnectivityvalidator": "DatabaseConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L310 | neighbors=[startup_validator.py, .validate(), Verifies actual database connectivity a…, run_all_validators()]
- "scripts_startup_validator_redisconnectivityvalidator": "RedisConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L354 | neighbors=[startup_validator.py, Verifies Redis connectivity at startup., .validate(), run_all_validators()]
- "scripts_startup_validator_startupvalidationerror": "StartupValidationError" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L27 | neighbors=[startup_validator.py, Raised when a required configuration in…, RuntimeError, .raise_if_errors()]
- "services_llm_managerllmservice_default_runtime": "._default_runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L74 | neighbors=[ManagerLlmService, Runtime, .generate(), .status()]
- "services_llm_managerllmservice_ensure_installed_ollama_model": "._ensure_installed_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L245 | neighbors=[ManagerLlmService, AiRuntimeError, ._client(), .generate()]
- "services_llm_managerllmservice_status": ".status()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L126 | neighbors=[ManagerLlmService, _is_local_ollama_model(), ._client(), ._default_runtime()]
- "states_datastate_errorstate": "ErrorState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L50 | neighbors=[Exposure.tsx, LiveOverview.tsx, SlaStatus.tsx, DataState.tsx]
- "tests_backend_auth_test": "backend-auth.test.ts" | kind=code-symbol | source=manager/frontend/tests/backend-auth.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, bearerFrom(), cookieFrom()]
- "tests_test_agent_dispatch_claim_fixture": "_claim_fixture()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L190 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…]
- "tests_test_agent_identity_cached_transport": "_cached_transport()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L11 | neighbors=[test_agent_identity.py, test_cached_identity_refreshes_current_…, test_cached_identity_retries_transient_…, test_rejected_cached_token_falls_back_t…]
- "tests_test_agents_testagentexecutabletypes": "TestAgentExecutableTypes" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L28 | neighbors=[test_agents.py, .test_network_types_included(), .test_server_side_types_excluded(), ScanJobType]
- "tests_test_agents_testagentregistrationrefresh": "TestAgentRegistrationRefresh" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L230 | neighbors=[test_agents.py, .test_agent_can_refresh_only_its_own_ro…, .test_agent_cannot_refresh_another_iden…, ScanJobType]
- "tests_test_agents_testlistagents": "TestListAgents" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L526 | neighbors=[test_agents.py, .test_fresh_disconnected_agent_is_not_r…, .test_lists_with_online_flag(), ScanJobType]
- "tests_test_agents_testpromoteassets_test_dedupes_duplicate_services_in_same_probe_result": ".test_dedupes_duplicate_services_in_same_probe_result()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L721 | neighbors=[A single web scan can emit multiple fac…, TestPromoteAssets, A single web scan can emit multiple fac…, A single web scan can emit multiple fac…]
- "tests_test_auth_login_testauthenticatebcryptfailure_test_raises_bcrypt_failure_on_passlib_error": ".test_raises_bcrypt_failure_on_passlib_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L164 | neighbors=[TestAuthenticateBcryptFailure, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatedisabledtenant_test_raises_disabled_tenant": ".test_raises_disabled_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L124 | neighbors=[TestAuthenticateDisabledTenant, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword_test_not_expired_when_future": ".test_not_expired_when_future()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L149 | neighbors=[TestAuthenticateExpiredPassword, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword_test_raises_expired_password": ".test_raises_expired_password()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L137 | neighbors=[TestAuthenticateExpiredPassword, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatepasswordmismatch_test_raises_password_mismatch": ".test_raises_password_mismatch()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L97 | neighbors=[TestAuthenticatePasswordMismatch, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatesuccess_test_null_password_expires_at_never_expires": ".test_null_password_expires_at_never_expires()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L208 | neighbors=[TestAuthenticateSuccess, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatesuccess_test_returns_user_on_valid_credentials": ".test_returns_user_on_valid_credentials()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L195 | neighbors=[TestAuthenticateSuccess, _make_db(), _make_tenant(), _make_user()]
- "tests_test_db_scanner_fakereader": "FakeReader" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L17 | neighbors=[test_db_scanner.py, .__init__(), .read(), _probe()]
- "tests_test_db_scanner_fakewriter": "FakeWriter" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L25 | neighbors=[test_db_scanner.py, .drain(), .write(), _probe()]
- "tests_test_db_unauth": "test_db_unauth.py" | kind=code-symbol | source=probe/tests/test_db_unauth.py:L1 | neighbors=[e8262a3 feat(probe): explicit unauthent…, db_scanner.py, test_redis_authenticated(), test_redis_unauthenticated()]
- "tests_test_exploit_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L38 | neighbors=[test_exploit_engine.py, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_finding_schema": "test_finding_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_finding_patch_accepts_documented_m…, test_finding_patch_rejects_risk_score_a…, test_finding_summary_exposes_full_open_…]
- "tests_test_integration_teststartupgauntlet": "TestStartupGauntlet" | kind=code-symbol | source=probe/tests/test_integration.py:L431 | neighbors=[test_integration.py, Phase 5: startup gauntlet checks., .test_gauntlet_hw_bind_blocks(), .test_gauntlet_skips_in_dev_mode()]
- "tests_test_integration_testtaskrunnerwithencryptedscope": "TestTaskRunnerWithEncryptedScope" | kind=code-symbol | source=probe/tests/test_integration.py:L100 | neighbors=[test_integration.py, Phase 4 + Phase 1: TaskRunner receives …, .test_decrypts_encrypted_scope_from_job…, .test_falls_back_when_decryption_fails()]
- "tests_test_integration_testtransportwithidentity": "TestTransportWithIdentity" | kind=code-symbol | source=probe/tests/test_integration.py:L238 | neighbors=[test_integration.py, Phase 4 + Phase 1: Transport sends publ…, .test_register_sends_public_key(), .test_register_without_public_key()]
- "tests_test_nessus_scanner_rationale_1": "Unit tests for NessusScanner — all HTTP calls mocked." | kind=entity | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[test_nessus_scanner.py, FindingSeverity, FindingStatus, NessusScanner]
- "tests_test_nuclei_scanner_finding_line": "_finding_line()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L12 | neighbors=[test_nuclei_scanner.py, test_nonzero_exit_retains_and_marks_par…, test_run_scan_streams_jsonl_and_separat…, test_timeout_retains_findings_emitted_b…]
- "tests_test_probe_core_testassetneedsrechecklive": "TestAssetNeedsRecheckLive" | kind=code-symbol | source=probe/tests/test_probe_core.py:L475 | neighbors=[test_probe_core.py, .test_never_seen(), .test_recently_seen(), .test_stale()]
- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=probe/tests/test_probe_core.py:L265 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]
- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=probe/tests/test_probe_core.py:L294 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]
- "tests_test_probe_core_testgate4": "TestGate4" | kind=code-symbol | source=probe/tests/test_probe_core.py:L308 | neighbors=[test_probe_core.py, .test_all_closed(), .test_no_open_ports(), .test_with_open_ports()]
- "tests_test_probe_core_testratelimiter": "TestRateLimiter" | kind=code-symbol | source=probe/tests/test_probe_core.py:L247 | neighbors=[test_probe_core.py, .test_min_interval(), .test_wait_returns_immediately_at_zero_…, .test_zero_rate()]
- "tests_test_probe_core_testroutebranches": "TestRouteBranches" | kind=code-symbol | source=probe/tests/test_probe_core.py:L419 | neighbors=[test_probe_core.py, .test_http_banner_routes_web(), .test_no_banners_no_routing(), .test_silent_nonstandard_port_routes_tl…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-035.json

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
