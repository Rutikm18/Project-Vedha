# Node Description Batch 89 of 380

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "scripts_startup_validator_redisconnectivityvalidator": "RedisConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L354 | neighbors=[startup_validator.py, Verifies Redis connectivity at startup., .validate(), run_all_validators()]
- "scripts_startup_validator_startupvalidationerror": "StartupValidationError" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L27 | neighbors=[startup_validator.py, Raised when a required configuration in…, RuntimeError, .raise_if_errors()]
- "services_evidence_summary_format_value": "_format_value()" | kind=code-symbol | source=manager/backend/app/services/evidence_summary.py:L71 | neighbors=[evidence_summary.py, _sentence_case(), Render one evidence value as a short pl…, summarize_evidence()]
- "services_finding_events_merge_timeline": "merge_timeline()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L206 | neighbors=[finding_events.py, build_timeline(), _decorate(), Merge stored + synthesized events, olde…]
- "services_finding_workflow_event_detail": "_event_detail()" | kind=code-symbol | source=manager/backend/app/services/finding_workflow.py:L21 | neighbors=[finding_workflow.py, patch_finding(), Keep the established manager timeline c…, reopen_finding()]
- "services_job_result_service_result_checksum": "result_checksum()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L49 | neighbors=[job_result_service.py, process_job_result(), Stable idempotency checksum for one att…, Recursively strip NUL (U+0000) from eve…]
- "services_llm_managerllmservice_ollama": "._ollama()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L533 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_openai": "._openai()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L577 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_openrouter": "._openrouter()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L552 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_notifications_deliver": "deliver()" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L101 | neighbors=[notifications.py, notify_tenant(), Send via one integration. True on succe…, Send via one integration. True on succe…]
- "services_notifications_notify_tenant": "notify_tenant()" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L117 | neighbors=[notifications.py, deliver(), Deliver to every ENABLED integration fo…, Deliver to every ENABLED integration fo…]
- "services_posture_aggregate": "aggregate()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L47 | neighbors=[posture.py, _clamp01(), compute_scores(), Noisy-OR: 100·(1 − ∏(1 − clamp(p))). Em…]
- "services_posture_present_in_run": "_present_in_run()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L104 | neighbors=[posture.py, compare(), _to_utc(), True when the finding was live as of ru…]
- "services_project_time_project_now": "project_now()" | kind=code-symbol | source=manager/backend/app/services/project_time.py:L60 | neighbors=[project_time.py, project_file_stamp(), project_timestamp(), Current time as an AWARE datetime in th…]
- "services_reference_make_reference": "make_reference()" | kind=code-symbol | source=manager/backend/app/services/reference.py:L83 | neighbors=[reference.py, suffix_for(), Build a reference. `created_at` should …, scan_job_reference()]
- "services_reference_suffix_for": "suffix_for()" | kind=code-symbol | source=manager/backend/app/services/reference.py:L72 | neighbors=[reference.py, make_reference(), The stable code for one row. Determinis…, _encode()]
- "services_remediation_kb_recipe_for_finding": "recipe_for_finding()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L346 | neighbors=[remediation_kb.py, Return a structured, OS-filtered remedi…, classify_finding(), os_key()]
- "services_scheduler_run_due": "run_due()" | kind=code-symbol | source=manager/backend/app/services/scheduler.py:L43 | neighbors=[scheduler.py, Enqueue every due schedule, then advanc…, advance(), due_schedules()]
- "services_scope_targets_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L66 | neighbors=[scope_targets.py, Return the normalized list of authorize…, _expand_requested(), _parse_networks()]
- "services_sla_summarize": "summarize()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L113 | neighbors=[sla.py, Aggregate SLA states across a set of fi…, compute(), Aggregate SLA states across a set of fi…]
- "services_validation_ingest_ingest_validation_result": "ingest_validation_result()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L51 | neighbors=[validation_ingest.py, apply_validation_outcome(), looks_like_validation_result(), If ``job_id`` belongs to a ValidationRe…]
- "settings_page_inlineinput": "inlineInput()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L191 | neighbors=[page.tsx, ApiKeysSection(), AuditLogSection(), IntegrationSection()]
- "supporting_research_evidence_store_identityresult": "IdentityResult" | kind=code-symbol | source=Supporting_research/evidence_store.py:L133 | neighbors=[evidence_store.py, .asset_count(), .observations_for(), resolve_identity()]
- "supporting_research_evidence_store_time_travel": "time_travel()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L378 | neighbors=[evidence_store.py, Audit-grade: what did the evidence supp…, AssetVerdict, retroactive_detect()]
- "supporting_research_test_evidence_store_ssh_obs": "ssh_obs()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L32 | neighbors=[test_evidence_store.py, build_fleet(), .test_hostname_never_overrides_a_finger…, .test_third_party_conclusions_are_kept_…]
- "tests_backend_auth_test": "backend-auth.test.ts" | kind=code-symbol | source=manager/frontend/tests/backend-auth.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, bearerFrom(), cookieFrom()]
- "tests_console_source_test": "console-source.test.ts" | kind=code-symbol | source=manager/frontend/tests/console-source.test.ts:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, console-source.tsx, consolePathFor(), normalizePortalDataset()]
- "tests_test_accuracy_gate_testcli": "TestCli" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L205 | neighbors=[test_accuracy_gate.py, .test_cli_exits_two_on_a_corpus_error(), .test_cli_exits_zero_on_passing_corpora…, .test_cli_json_mode_is_machine_readable…]
- "tests_test_accuracy_gate_testprovenance": "TestProvenance" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L129 | neighbors=[test_accuracy_gate.py, .test_gate_counts_the_two_kinds_separat…, .test_nmap_labels_count_as_accuracy_evi…, .test_self_regression_labels_do_not()]
- "tests_test_adaptive_rate_testudpscanneradaptive": "TestUdpScannerAdaptive" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L185 | neighbors=[test_adaptive_rate.py, .test_adaptive_scanner_creates_controll…, .test_adaptive_scanner_detects_open_on_…, .test_non_adaptive_scanner_has_no_contr…]
- "tests_test_adaptive_rate_testwindowgating": "TestWindowGating" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L79 | neighbors=[test_adaptive_rate.py, .test_acquire_blocks_when_window_full(), .test_release_unblocks_waiter(), .test_report_loss_shrinks_and_releases()]
- "tests_test_agent_dispatch_claim_fixture": "_claim_fixture()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L195 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…]
- "tests_test_agent_identity_cached_transport": "_cached_transport()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L11 | neighbors=[test_agent_identity.py, test_cached_identity_refreshes_current_…, test_cached_identity_retries_transient_…, test_rejected_cached_token_falls_back_t…]
- "tests_test_agents_testagentexecutabletypes": "TestAgentExecutableTypes" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L34 | neighbors=[test_agents.py, .test_network_types_included(), .test_server_side_types_excluded(), ScanJobType]
- "tests_test_agents_testagentregistrationrefresh": "TestAgentRegistrationRefresh" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L238 | neighbors=[test_agents.py, .test_agent_can_refresh_only_its_own_ro…, .test_agent_cannot_refresh_another_iden…, ScanJobType]
- "tests_test_agents_testlistagents": "TestListAgents" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L564 | neighbors=[test_agents.py, .test_fresh_disconnected_agent_is_not_r…, .test_lists_with_online_flag(), ScanJobType]
- "tests_test_auth_login_testauthenticatebcryptfailure_test_raises_bcrypt_failure_on_passlib_error": ".test_raises_bcrypt_failure_on_passlib_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L164 | neighbors=[TestAuthenticateBcryptFailure, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticatedisabledtenant_test_raises_disabled_tenant": ".test_raises_disabled_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L124 | neighbors=[TestAuthenticateDisabledTenant, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword_test_not_expired_when_future": ".test_not_expired_when_future()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L149 | neighbors=[TestAuthenticateExpiredPassword, _make_db(), _make_tenant(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword_test_raises_expired_password": ".test_raises_expired_password()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L137 | neighbors=[TestAuthenticateExpiredPassword, _make_db(), _make_tenant(), _make_user()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-088.json

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
