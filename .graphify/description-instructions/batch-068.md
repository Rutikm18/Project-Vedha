# Node Description Batch 69 of 380

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

- "services_finding_events_build_timeline": "build_timeline()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L216 | neighbors=[finding_events.py, merge_timeline(), _row_to_dict(), synthesize_events(), The finding's full lifecycle timeline: …]
- "services_finding_events_val": "_val()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L54 | neighbors=[finding_events.py, event_type_for_status(), Accept a FindingEventType/FindingStatus…, record_event(), synthesize_events()]
- "services_finding_priority": "finding_priority.py" | kind=code-symbol | source=manager/backend/app/services/finding_priority.py:L1 | neighbors=[ef14810 Implement instance locking mech…, priority_key(), severity_order_case(), severity_rank(), finding_priority.py — the single defini…]
- "services_job_attempt_service": "job_attempt_service.py" | kind=code-symbol | source=manager/backend/app/services/job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, config.py, AttemptClaim, claim_job_attempt(), renew_job_attempt()]
- "services_job_result_service_identity_ip": "_identity_ip()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L116 | neighbors=[job_result_service.py, Parse a probe identity as an IP, tolera…, validate_result_scope(), Parse a probe identity as an IP, tolera…, Parse a probe identity as an IP, tolera…]
- "services_job_result_service_result_network_identities": "_result_network_identities()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L78 | neighbors=[job_result_service.py, Return network identities that could cr…, validate_result_scope(), Return network identities that could cr…, Return network identities that could cr…]
- "services_llm_http_client": "llm_http_client.py" | kind=code-symbol | source=manager/backend/app/services/llm_http_client.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, AsyncLlmHttpClient, Shared asynchronous HTTP transport for …]
- "services_llm_managerllmservice_anthropic": "._anthropic()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L603 | neighbors=[ManagerLlmService, _anthropic_system_blocks(), ._client(), ._dispatch(), .generate()]
- "services_llm_managerllmservice_ensure_installed_ollama_model": "._ensure_installed_ollama_model()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L515 | neighbors=[ManagerLlmService, AiRuntimeError, ._client(), .generate(), .generate_with_fallback()]
- "services_llm_managerllmservice_status": ".status()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L280 | neighbors=[ManagerLlmService, _is_local_ollama_model(), ._client(), ._default_runtime(), _usable_key()]
- "services_posture_build_posture": "build_posture()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L159 | neighbors=[posture.py, compare(), compute_scores(), _to_utc(), Full dashboard/report payload. Degrades…]
- "services_posture_compare": "compare()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L120 | neighbors=[posture.py, build_posture(), _present_in_run(), _severity(), Bucket findings across the previous→lat…]
- "services_remediation_kb_classify_finding": "classify_finding()" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L79 | neighbors=[remediation_kb.py, _cves(), _text(), Map a finding to a KB category key usin…, recipe_for_finding()]
- "services_scheduler": "scheduler.py" | kind=code-symbol | source=manager/backend/app/services/scheduler.py:L1 | neighbors=[93d36f9 feat(scheduling): due-schedule …, advance(), due_schedules(), run_due(), scheduler.py — decide which scan schedu…]
- "services_scope_targets": "scope_targets.py" | kind=code-symbol | source=manager/backend/app/services/scope_targets.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _expand_requested(), _parse_networks(), validate_targets_in_scope(), scope_targets.py — the single source of…]
- "services_sla_slaresult": "SlaResult" | kind=code-symbol | source=manager/backend/app/services/sla.py:L46 | neighbors=[sla.py, compute(), .is_tracked(), FindingStatus, Finding]
- "services_validation_ingest": "validation_ingest.py" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, apply_validation_outcome(), ingest_validation_result(), looks_like_validation_result(), validation_ingest.py — turn a probe's s…]
- "supporting_research_evidence_store_retroactive_detect": "retroactive_detect()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L296 | neighbors=[evidence_store.py, Answer a brand-new rule against evidenc…, AssetVerdict, _iso(), time_travel()]
- "supporting_research_evidence_store_unionfind": "_UnionFind" | kind=code-symbol | source=Supporting_research/evidence_store.py:L146 | neighbors=[evidence_store.py, resolve_identity(), .find(), .__init__(), .union()]
- "tests_conftest": "conftest.py" | kind=code-symbol | source=probe/tests/conftest.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 8f6bf49 Refactor code structure and rem…, _isolate_result_archive(), pytest_configure(), 2885afa Add comprehensive probe testing…]
- "tests_evidence_presentation_test": "evidence-presentation.test.ts" | kind=code-symbol | source=manager/frontend/tests/evidence-presentation.test.ts:L1 | neighbors=[315cf9c feat(frontend): refine reports …, 76240ac UI UX Update, ce7ab6e Merge origin/main: reconcile fi…, evidence-presentation.ts, presentEvidence()]
- "tests_test_active_validation_interpret": "test_active_validation_interpret.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_interpret.py:L1 | neighbors=[7bd104a feat(active-validation): pure r…, test_confirmed_upgrades_and_sets_exploi…, test_contradicted_marks_false_positive(), test_inconclusive_keeps_state_unchanged…, test_missing_or_garbage_result_is_incon…]
- "tests_test_ad_assessment_enum_with_entries": "_enum_with_entries()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L45 | neighbors=[test_ad_assessment.py, .test_get_computers_flags_dc(), .test_get_groups_marks_privileged(), .test_get_users_disabled_account(), .test_get_users_parses_uac_and_spn()]
- "tests_test_adaptive_rate_testudpretransmit": "TestUdpRetransmit" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L119 | neighbors=[test_adaptive_rate.py, .test_retries_exhaust_on_silence(), .test_retry_recovers_dropped_reply(), .test_returns_immediately_on_closed(), .test_returns_immediately_on_reply()]
- "tests_test_agent_dispatch_testusecasecatalogparity": "TestUseCaseCatalogParity" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L35 | neighbors=[test_agent_dispatch.py, .test_manager_and_probe_route_use_cases…, ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_read_tools_test_list_assets_batches_services_no_n_plus_one": "test_list_assets_batches_services_no_n_plus_one()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L59 | neighbors=[test_agent_read_tools.py, _asset(), _FakeSession, _Result, _svc()]
- "tests_test_agent_read_tools_test_list_assets_caps_services_at_30": "test_list_assets_caps_services_at_30()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L79 | neighbors=[test_agent_read_tools.py, _asset(), _FakeSession, _Result, _svc()]
- "tests_test_agents_testregisteragent": "TestRegisterAgent" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L675 | neighbors=[test_agents.py, .test_agent_token_is_long_lived(), .test_creates_when_none_exists(), .test_reuses_existing_probe_by_name(), ScanJobType]
- "tests_test_ai_engine_testllmreportgenerator_test_technical_finding_runs_guard": ".test_technical_finding_runs_guard()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L223 | neighbors=[TestLLMReportGenerator, _asset(), _finding(), _mock_db(), _resp()]
- "tests_test_ai_normalizer_testainormalizercache": "TestAINormalizerCache" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L123 | neighbors=[test_ai_normalizer.py, .test_cache_persists_across_instances(), .test_get_returns_none_on_miss(), .test_key_is_content_hash_not_plaintext…, .test_put_and_get_roundtrip()]
- "tests_test_attack_path_correlation_ids": "_ids()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L15 | neighbors=[test_attack_path_correlation.py, test_cleartext_cluster_needs_two(), test_correlation_is_host_scoped(), test_exposed_db_without_unauth_does_not…, test_no_relay_when_signing_required()]
- "tests_test_auth_surface_testloginform": "TestLoginForm" | kind=code-symbol | source=probe/tests/test_auth_surface.py:L53 | neighbors=[test_auth_surface.py, .test_challenge_wins_over_form(), .test_ordinary_page_has_no_auth_surface…, .test_password_input_is_detected_as_a_f…, .test_single_quoted_password_input_is_d…]
- "tests_test_campaign_progress_beat": "_beat()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L311 | neighbors=[test_campaign_progress.py, test_a_briefly_running_run_with_a_dead_…, test_a_dead_worker_is_called_out_quickl…, test_a_long_run_with_a_live_worker_is_n…, test_stall_never_claims_completion_eith…]
- "tests_test_campaign_progress_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L17 | neighbors=[test_campaign_progress.py, _progress(), _run_scenario(), test_campaign_progress_aggregates_jobs_…, test_campaign_progress_no_detection_yet…]
- "tests_test_campaign_progress_terminal": "test_campaign_progress_terminal.py" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _status(), TestNormalPipelineUnaffected, TestTerminalWithoutResults, A campaign whose jobs all ended without…]
- "tests_test_campaign_progress_test_a_briefly_running_run_is_not_called_stalled": "test_a_briefly_running_run_is_not_called_stalled()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L283 | neighbors=[test_campaign_progress.py, A run that started seconds ago is busy,…, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_a_wedged_detection_run_explains_itself": "test_a_wedged_detection_run_explains_itself()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L267 | neighbors=[test_campaign_progress.py, The other way a campaign never finishes…, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_naive_started_at_does_not_crash_the_page": "test_naive_started_at_does_not_crash_the_page()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L294 | neighbors=[test_campaign_progress.py, started_at can come back tz-naive depen…, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_percent_reaches_100_exactly_when_the_campaign_is_complete": "test_percent_reaches_100_exactly_when_the_campaign_is_complete()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L217 | neighbors=[test_campaign_progress.py, The invariant. Checked across the state…, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_uncovered_submission_holds_progress_below_100": "test_uncovered_submission_holds_progress_below_100()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L238 | neighbors=[test_campaign_progress.py, The exact regression: the newest submis…, _job(), _progress(), _run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-068.json

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
