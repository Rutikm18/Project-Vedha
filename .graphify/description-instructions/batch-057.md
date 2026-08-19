# Node Description Batch 58 of 227

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

- "schemas_engagement_validate_scope_entries": "validate_scope_entries()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L12 | neighbors=[engagement.py, .validate_scopes(), Validate and de-duplicate exact IP/CIDR…, Validate and de-duplicate exact IP/CIDR…]
- "schemas_finding_rationale_21": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[FindingPatch, DetectionStatus, FindingSeverity, FindingStatus]
- "scripts_seed_admin_detect_drift": "_detect_drift()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L150 | neighbors=[seed_admin.py, log_warn(), Warn if the tenant has multiple admins …, _seed_once()]
- "scripts_seed_admin_log": "_log()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L71 | neighbors=[seed_admin.py, log_error(), log_info(), log_warn()]
- "scripts_seed_admin_log_error": "log_error()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L89 | neighbors=[seed_admin.py, _log(), main(), _seed_with_retry()]
- "scripts_seed_admin_log_info": "log_info()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L81 | neighbors=[seed_admin.py, _log(), main(), _seed_once()]
- "scripts_seed_admin_rationale_1": "Idempotent admin seeder — production-grade rewrite.  Behavior:   First run : cre" | kind=entity | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[seed_admin.py, UserRole, Tenant, User]
- "scripts_seed_admin_validate_env": "_validate_env()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L95 | neighbors=[seed_admin.py, main(), Returns (email, password, tenant_name, …, log_warn()]
- "scripts_startup_validator_databaseconnectivityvalidator": "DatabaseConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L310 | neighbors=[startup_validator.py, .validate(), Verifies actual database connectivity a…, run_all_validators()]
- "scripts_startup_validator_redisconnectivityvalidator": "RedisConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L354 | neighbors=[startup_validator.py, Verifies Redis connectivity at startup., .validate(), run_all_validators()]
- "scripts_startup_validator_startupvalidationerror": "StartupValidationError" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L27 | neighbors=[startup_validator.py, Raised when a required configuration in…, RuntimeError, .raise_if_errors()]
- "services_llm_managerllmservice_anthropic": "._anthropic()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L456 | neighbors=[ManagerLlmService, ._client(), ._dispatch(), .generate()]
- "services_llm_managerllmservice_ollama": "._ollama()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L391 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_openai": "._openai()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L435 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_openrouter": "._openrouter()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L410 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_status": ".status()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L154 | neighbors=[ManagerLlmService, _is_local_ollama_model(), ._client(), ._default_runtime()]
- "services_posture_aggregate": "aggregate()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L47 | neighbors=[posture.py, _clamp01(), compute_scores(), Noisy-OR: 100·(1 − ∏(1 − clamp(p))). Em…]
- "services_posture_present_in_run": "_present_in_run()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L104 | neighbors=[posture.py, compare(), _to_utc(), True when the finding was live as of ru…]
- "services_remediation_kb_recipe_for_finding": "recipe_for_finding()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L346 | neighbors=[remediation_kb.py, Return a structured, OS-filtered remedi…, classify_finding(), os_key()]
- "services_scope_targets_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L66 | neighbors=[scope_targets.py, Return the normalized list of authorize…, _expand_requested(), _parse_networks()]
- "services_sla_summarize": "summarize()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L113 | neighbors=[sla.py, Aggregate SLA states across a set of fi…, compute(), Aggregate SLA states across a set of fi…]
- "services_validation_ingest_ingest_validation_result": "ingest_validation_result()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L51 | neighbors=[validation_ingest.py, apply_validation_outcome(), looks_like_validation_result(), If ``job_id`` belongs to a ValidationRe…]
- "tests_backend_auth_test": "backend-auth.test.ts" | kind=code-symbol | source=manager/frontend/tests/backend-auth.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, bearerFrom(), cookieFrom()]
- "tests_test_adaptive_rate_testudpscanneradaptive": "TestUdpScannerAdaptive" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L185 | neighbors=[test_adaptive_rate.py, .test_adaptive_scanner_creates_controll…, .test_adaptive_scanner_detects_open_on_…, .test_non_adaptive_scanner_has_no_contr…]
- "tests_test_adaptive_rate_testwindowgating": "TestWindowGating" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L79 | neighbors=[test_adaptive_rate.py, .test_acquire_blocks_when_window_full(), .test_release_unblocks_waiter(), .test_report_loss_shrinks_and_releases()]
- "tests_test_agent_dispatch_claim_fixture": "_claim_fixture()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L195 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…]
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
- "tests_test_customer_access_testapprovescanrequest": "TestApproveScanRequest" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L150 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…]
- "tests_test_customer_access_testapprovescanrequest_test_approve_non_pending_is_conflict": ".test_approve_non_pending_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L180 | neighbors=[TestApproveScanRequest, _mock_db(), _operator(), _pending_request()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-057.json

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
