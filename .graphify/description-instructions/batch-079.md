# Node Description Batch 80 of 336

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

- "scripts_seed_admin_detect_drift": "_detect_drift()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L150 | neighbors=[seed_admin.py, log_warn(), Warn if the tenant has multiple admins …, _seed_once()]
- "scripts_seed_admin_log": "_log()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L71 | neighbors=[seed_admin.py, log_error(), log_info(), log_warn()]
- "scripts_seed_admin_log_error": "log_error()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L89 | neighbors=[seed_admin.py, _log(), main(), _seed_with_retry()]
- "scripts_seed_admin_log_info": "log_info()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L81 | neighbors=[seed_admin.py, _log(), main(), _seed_once()]
- "scripts_seed_admin_rationale_1": "Idempotent admin seeder — production-grade rewrite.  Behavior:   First run : cre" | kind=entity | source=manager/backend/scripts/seed_admin.py:L1 | neighbors=[seed_admin.py, UserRole, Tenant, User]
- "scripts_seed_admin_validate_env": "_validate_env()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L95 | neighbors=[seed_admin.py, main(), Returns (email, password, tenant_name, …, log_warn()]
- "scripts_startup_validator_databaseconnectivityvalidator": "DatabaseConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L310 | neighbors=[startup_validator.py, .validate(), Verifies actual database connectivity a…, run_all_validators()]
- "scripts_startup_validator_redisconnectivityvalidator": "RedisConnectivityValidator" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L354 | neighbors=[startup_validator.py, Verifies Redis connectivity at startup., .validate(), run_all_validators()]
- "scripts_startup_validator_startupvalidationerror": "StartupValidationError" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L27 | neighbors=[startup_validator.py, Raised when a required configuration in…, RuntimeError, .raise_if_errors()]
- "services_finding_events_merge_timeline": "merge_timeline()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L206 | neighbors=[finding_events.py, build_timeline(), _decorate(), Merge stored + synthesized events, olde…]
- "services_job_result_service_result_checksum": "result_checksum()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L49 | neighbors=[job_result_service.py, process_job_result(), Stable idempotency checksum for one att…, Recursively strip NUL (U+0000) from eve…]
- "services_llm_managerllmservice_anthropic": "._anthropic()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L494 | neighbors=[ManagerLlmService, ._client(), ._dispatch(), .generate()]
- "services_llm_managerllmservice_auto_cloud_provider": "._auto_cloud_provider()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L125 | neighbors=[ManagerLlmService, ._default_runtime(), First configured cloud provider, or Non…, First configured cloud provider, or Non…]
- "services_llm_managerllmservice_ollama": "._ollama()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L429 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_openai": "._openai()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L473 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_openrouter": "._openrouter()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L448 | neighbors=[ManagerLlmService, ._dispatch(), ._client(), .generate()]
- "services_llm_managerllmservice_status": ".status()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L195 | neighbors=[ManagerLlmService, _is_local_ollama_model(), ._client(), ._default_runtime()]
- "services_posture_aggregate": "aggregate()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L47 | neighbors=[posture.py, _clamp01(), compute_scores(), Noisy-OR: 100·(1 − ∏(1 − clamp(p))). Em…]
- "services_posture_present_in_run": "_present_in_run()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L104 | neighbors=[posture.py, compare(), _to_utc(), True when the finding was live as of ru…]
- "services_project_time_project_now": "project_now()" | kind=code-symbol | source=manager/backend/app/services/project_time.py:L60 | neighbors=[project_time.py, project_file_stamp(), project_timestamp(), Current time as an AWARE datetime in th…]
- "services_reference_make_reference": "make_reference()" | kind=code-symbol | source=manager/backend/app/services/reference.py:L83 | neighbors=[reference.py, suffix_for(), Build a reference. `created_at` should …, scan_job_reference()]
- "services_reference_suffix_for": "suffix_for()" | kind=code-symbol | source=manager/backend/app/services/reference.py:L72 | neighbors=[reference.py, make_reference(), The stable code for one row. Determinis…, _encode()]
- "services_remediation_kb_recipe_for_finding": "recipe_for_finding()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L346 | neighbors=[remediation_kb.py, Return a structured, OS-filtered remedi…, classify_finding(), os_key()]
- "services_scope_targets_validate_targets_in_scope": "validate_targets_in_scope()" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L66 | neighbors=[scope_targets.py, Return the normalized list of authorize…, _expand_requested(), _parse_networks()]
- "services_sla_summarize": "summarize()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L113 | neighbors=[sla.py, Aggregate SLA states across a set of fi…, compute(), Aggregate SLA states across a set of fi…]
- "services_validation_ingest_ingest_validation_result": "ingest_validation_result()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L51 | neighbors=[validation_ingest.py, apply_validation_outcome(), looks_like_validation_result(), If ``job_id`` belongs to a ValidationRe…]
- "settings_page_inlineinput": "inlineInput()" | kind=code-symbol | source=manager/frontend/app/settings/page.tsx:L183 | neighbors=[page.tsx, ApiKeysSection(), AuditLogSection(), IntegrationSection()]
- "supporting_research_evidence_store_identityresult": "IdentityResult" | kind=code-symbol | source=Supporting_research/evidence_store.py:L133 | neighbors=[evidence_store.py, .asset_count(), .observations_for(), resolve_identity()]
- "supporting_research_evidence_store_time_travel": "time_travel()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L378 | neighbors=[evidence_store.py, Audit-grade: what did the evidence supp…, AssetVerdict, retroactive_detect()]
- "supporting_research_test_evidence_store_ssh_obs": "ssh_obs()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L32 | neighbors=[test_evidence_store.py, build_fleet(), .test_hostname_never_overrides_a_finger…, .test_third_party_conclusions_are_kept_…]
- "tests_backend_auth_test": "backend-auth.test.ts" | kind=code-symbol | source=manager/frontend/tests/backend-auth.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, bearerFrom(), cookieFrom()]
- "tests_findings_detail_layout_test": "findings-detail-layout.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-detail-layout.test.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, findingsPage]
- "tests_test_accuracy_gate_testcli": "TestCli" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L205 | neighbors=[test_accuracy_gate.py, .test_cli_exits_two_on_a_corpus_error(), .test_cli_exits_zero_on_passing_corpora…, .test_cli_json_mode_is_machine_readable…]
- "tests_test_accuracy_gate_testprovenance": "TestProvenance" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L129 | neighbors=[test_accuracy_gate.py, .test_gate_counts_the_two_kinds_separat…, .test_nmap_labels_count_as_accuracy_evi…, .test_self_regression_labels_do_not()]
- "tests_test_adaptive_rate_testudpscanneradaptive": "TestUdpScannerAdaptive" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L185 | neighbors=[test_adaptive_rate.py, .test_adaptive_scanner_creates_controll…, .test_adaptive_scanner_detects_open_on_…, .test_non_adaptive_scanner_has_no_contr…]
- "tests_test_adaptive_rate_testwindowgating": "TestWindowGating" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L79 | neighbors=[test_adaptive_rate.py, .test_acquire_blocks_when_window_full(), .test_release_unblocks_waiter(), .test_report_loss_shrinks_and_releases()]
- "tests_test_agent_dispatch_claim_fixture": "_claim_fixture()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L195 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…]
- "tests_test_agent_identity_cached_transport": "_cached_transport()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L11 | neighbors=[test_agent_identity.py, test_cached_identity_refreshes_current_…, test_cached_identity_retries_transient_…, test_rejected_cached_token_falls_back_t…]
- "tests_test_agents_testagentexecutabletypes": "TestAgentExecutableTypes" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L34 | neighbors=[test_agents.py, .test_network_types_included(), .test_server_side_types_excluded(), ScanJobType]
- "tests_test_agents_testagentregistrationrefresh": "TestAgentRegistrationRefresh" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L238 | neighbors=[test_agents.py, .test_agent_can_refresh_only_its_own_ro…, .test_agent_cannot_refresh_another_iden…, ScanJobType]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-079.json

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
