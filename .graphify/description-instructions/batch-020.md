# Node Description Batch 21 of 209

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

- "models_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/models/agent.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Enum, Agent] | lang=en
- "register_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, toUiAgent(), backend(), withBackend(), GET, 2885afa Add comprehensive probe testing…] | lang=en
- "reopen_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/reopen/route.ts:L1 | neighbors=[8ebc053 feat(risk-rank-ui): surface ver…, adapters.ts, toUiFinding(), backend.ts, backend(), BackendError] | lang=en
- "request_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), isEmailAllowed(), POST(), 2885afa Add comprehensive probe testing…] | lang=en
- "routers_ad_rationale_1": "Active Directory assessment API.  POST /engagements/{id}/ad/assess        — laun" | kind=entity | source=manager/backend/app/routers/ad.py:L1 | neighbors=[ad.py, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_ad_rationale_135": "Background task: run the AD assessment and persist findings + job result." | kind=entity | source=manager/backend/app/routers/ad.py:L135 | neighbors=[_run_ad_assessment_and_save(), ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_agents_list_use_cases": "list_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L547 | neighbors=[agents.py, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…] | lang=en
- "routers_agents_rationale_106": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L106 | neighbors=[_scope_is_reachable(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=pt
- "routers_agents_rationale_142": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L142 | neighbors=[_job_reachability_scope(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_agents_rationale_210": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L210 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_390": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L390 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_428": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L428 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_447": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L447 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_709": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L709 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_93": "Resolve the capability a probe must advertise for a job." | kind=entity | source=manager/backend/app/routers/agents.py:L93 | neighbors=[_required_scan_type(), Asset, Engagement, AssetType, ScanJobStatus, ScanJobType] | lang=en
- "routers_engagements_refresh_overview_cache": "_refresh_overview_cache()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L97 | neighbors=[engagements.py, bulk_import_assets(), create_engagement(), import_facts(), Write-through cache refresh on the WRIT…, _compute_overview()] | lang=en
- "routers_vuln_scans_run_nuclei_and_save": "_run_nuclei_and_save()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L270 | neighbors=[vuln_scans.py, Run Nuclei and always leave its job in …, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), _nuclei_finding(), _nuclei_terminal_result()] | lang=en
- "schemas_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, AiGenerateRequest, AiGenerateResponse] | lang=en
- "scripts_startup_validator_run_all_validators": "run_all_validators()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L396 | neighbors=[startup_validator.py, Run all validators. Use in FastAPI life…, CheckResult, DatabaseConnectivityValidator, RedisConnectivityValidator, ValidationReport] | lang=en
- "services_llm_managerllmservice_dispatch": "._dispatch()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L251 | neighbors=[ManagerLlmService, AiRuntimeError, ._anthropic(), ._ollama(), ._openai(), ._openrouter()] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine": "TestWindowStateMachine" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L27 | neighbors=[test_adaptive_rate.py, .test_congestion_avoidance_grows_sublin…, .test_initial_window(), .test_loss_halves_window(), .test_loss_sets_ssthresh_to_half(), .test_recovery_after_loss_enters_conges…] | lang=en
- "tests_test_agents_testpromoteassets": "TestPromoteAssets" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L693 | neighbors=[test_agents.py, Discovery results → assets/services pro…, .test_creates_asset_and_services_with_c…, .test_dedupes_duplicate_services_in_sam…, .test_empty_result_is_noop(), .test_skips_host_without_ip()] | lang=en
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient] | lang=en
- "tests_test_auth_login_make_user": "_make_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L44 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future(), .test_raises_expired_password()] | lang=en
- "tests_test_auth_login_testreasoncodes": "TestReasonCodes" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L223 | neighbors=[test_auth_login.py, Ensure every exception class has the ex…, .test_bcrypt_failure_code(), .test_database_failure_code(), .test_disabled_tenant_code(), .test_disabled_user_code()] | lang=en
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()] | lang=en
- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L90 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()] | lang=en
- "tests_test_loaders": "test_loaders.py" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, TestLoadEpssErrors, TestLoadKevErrors, TestLoadSnapshotErrors, _valid_epss(), _valid_kev()] | lang=en
- "tests_test_loaders_testloadsnapshoterrors": "TestLoadSnapshotErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L55 | neighbors=[test_loaders.py, .setup_method(), .test_content_hash_mismatch_raises_valu…, .test_error_message_mentions_re_sync(), .test_hash_mismatch_message_truncates_h…, .test_malformed_json_raises()] | lang=en
- "tests_test_main_scripts_coverage_mk_scanner": "_mk_scanner()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L27 | neighbors=[test_main_scripts_coverage.py, _scope(), .test_adaptive_estimator_is_shared_and_…, .test_fixed_timeout_flag_disables_the_e…, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…] | lang=en
- "tests_test_main_scripts_datastore_probe": "test_main_scripts_datastore_probe.py" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, service_banner.py, _svc(), test_elasticsearch_and_couchdb_win_over…, test_ladder_includes_safe_datastore_pro…, test_memcached_probe_response_yields_un…] | lang=en
- "tests_test_main_scripts_statemodel": "test_main_scripts_statemodel.py" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, test_backward_compatible_old_style_cons…, test_canonical_states_are_the_six_docum…, test_explicit_first_class_value_wins_ov…, test_semantics_in_data_are_promoted_to_…] | lang=en
- "tests_test_new_scanners_testdeltaengine_write_jsonl": "._write_jsonl()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L379 | neighbors=[TestDeltaEngine, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…] | lang=en
- "tests_test_nuclei_scanner": "test_nuclei_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, FakeProcess, _finding_line(), test_missing_binary_is_a_reported_failu…, test_nonzero_exit_retains_and_marks_par…, test_nonzero_exit_without_findings_rais…] | lang=en
- "tests_test_os_fingerprint": "test_os_fingerprint.py" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, TestFingerprintOs, TestIcmpBuilders, TestIcmpCapability, TestIcmpParse] | lang=en
- "tests_test_os_fingerprint_testttlinference": "TestTtlInference" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L94 | neighbors=[test_os_fingerprint.py, .test_hop_estimate(), .test_os_family_linux(), .test_os_family_network(), .test_os_family_unknown_on_none(), .test_os_family_windows()] | lang=en
- "tests_test_pat_auth": "test_pat_auth.py" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, test_new_pat_token_shape_and_hash_stabi…, test_pat_builder_rejects_unknown_scope(), test_pat_builder_returns_token_once_and…, test_pat_builder_supports_non_expiring_…, test_pat_scope_allows_probe_cli_paths()] | lang=en
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L911 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_ot_passive()] | lang=en
- "tests_test_risk_rank": "test_risk_rank.py" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L1 | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, _rank(), test_bounds(), test_confirmed_exploitable_outranks_con…, test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lo…] | lang=en
- "tests_test_scope_crypt_testencryptdecryptroundtrip": "TestEncryptDecryptRoundtrip" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L28 | neighbors=[test_scope_crypt.py, .test_b64_roundtrip(), .test_different_plaintexts_are_distinct…, .test_different_recipient_cannot_decryp…, .test_multiple_encrypts_different(), .test_roundtrip_empty_scope()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-020.json

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
