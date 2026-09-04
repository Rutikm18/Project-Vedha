# Node Description Batch 49 of 330

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

- "scanner_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L273 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__(), True only when a real SYN scan can work…, True only when a real SYN scan can work…, True only when a real SYN scan can work…]
- "scanner_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L274 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "scanner_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version(), Never send an IP literal as SNI — non-c…, Never send an IP literal as SNI — non-c…]
- "scanner_va_campaign_vacampaign": "VACampaign" | kind=code-symbol | source=probe/scanner/va_campaign.py:L290 | neighbors=[va_campaign.py, build_campaign(), Runs the ordered stages sequentially, e…, .__init__(), ._refresh_totals(), .run()]
- "scanner_va_campaign_vacampaign_run": ".run()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L301 | neighbors=[run_campaign(), VACampaign, .finish(), .mark(), .snapshot(), ._refresh_totals()]
- "scanner_vnc_scanner_vncscanner": "VNCScanner" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L101 | neighbors=[vnc_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "scanner_vnc_scanner_vncscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L108 | neighbors=[Blocking: RFB version handshake + read …, VNCScanner, classify_security_types(), parse_rfb_version(), _read_security_types(), _recv_exact()]
- "scanner_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/scanner/web_scanner.py:L136 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target(), ._schemes_for()]
- "scanner_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/scanner/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "schemas_ai_aigeneraterequest": "AiGenerateRequest" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L18 | neighbors=[ai.py, BaseModel, .validate_bounded_input(), AiRuntimeError, ManagerLlmService, Runtime]
- "schemas_finding_findingout": "FindingOut" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L121 | neighbors=[finding.py, BaseModel, ._populate_risk_rank(), DetectionStatus, FindingSeverity, FindingStatus]
- "schemas_remediation": "remediation.py" | kind=code-symbol | source=manager/backend/app/schemas/remediation.py:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, RemediationPlanDetailOut, RemediationPlanOut, RemediationStepOut]
- "scripts_seed_admin_seed_with_retry": "_seed_with_retry()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L294 | neighbors=[seed_admin.py, main(), Exponential-backoff retry for transient…, log_error(), log_warn(), _seed_once()]
- "services_llm_managerllmservice_runtime": "._runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L155 | neighbors=[ManagerLlmService, ._fallback_candidates(), .generate(), AiRuntimeError, _is_local_ollama_model(), Runtime]
- "services_scope_crypto": "scope_crypto.py" | kind=code-symbol | source=manager/backend/app/services/scope_crypto.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, encrypt_scope(), encrypt_scope_b64(), public_key_from_b64(), scope_crypto.py — manager-side: encrypt…, 2885afa Add comprehensive probe testing…]
- "services_sla_compute": "compute()" | kind=code-symbol | source=manager/backend/app/services/sla.py:L60 | neighbors=[sla.py, SlaResult, _windows(), Compute the SLA state for one finding. …, summarize(), Compute the SLA state for one finding. …]
- "states_datastate_errorstate": "ErrorState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L52 | neighbors=[ExposureCards.tsx, LiveOverview.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, DataState.tsx]
- "supporting_research_test_evidence_store_openssh_below": "openssh_below()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L54 | neighbors=[test_evidence_store.py, demo(), .test_a_brand_new_rule_answers_against_…, .test_current_state_comes_from_latest_e…, .test_remediation_is_verified_by_eviden…, .test_time_travel_recovers_the_historic…]
- "supporting_research_test_evidence_store_testidentity": "TestIdentity" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L95 | neighbors=[test_evidence_store.py, .setUp(), .test_fingerprint_identity_finds_exactl…, .test_hostname_never_overrides_a_finger…, .test_ip_identity_is_wrong_in_both_dire…, .test_observations_without_any_fingerpr…]
- "test_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/integrations/test/route.ts:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, backend.ts, backend(), with-backend.ts, withBackend(), POST]
- "tests_findings_adapters_test": "findings-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-adapters.test.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, adapters.ts, toApiFindingPatch(), toUiFinding()]
- "tests_test_accuracy_gate_port_fact": "_port_fact()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L36 | neighbors=[test_accuracy_gate.py, .test_ground_truth_states_alone_is_a_va…, .test_gate_counts_the_two_kinds_separat…, .test_regression_only_directory_still_w…, .test_matching_port_state_scores_perfec…, .test_thresholds_are_overridable()]
- "tests_test_agent_dispatch_testagentwebsocketauthentication": "TestAgentWebSocketAuthentication" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L16 | neighbors=[test_agent_dispatch.py, .test_accepts_bearer_header(), .test_rejects_query_string_credentials(), ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_dispatch_testjobsecretboundary": "TestJobSecretBoundary" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L67 | neighbors=[test_agent_dispatch.py, .test_allows_non_secret_scan_tuning(), .test_detects_persisted_secret_material…, ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_policy": "test_agent_policy.py" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L1 | neighbors=[bc08715 feat(agent): risk-tier action c…, ecbb4ad feat(agent): rules-of-engagemen…, _roe(), TestClassifyAction, TestEvaluateAction, test_agent_policy.py — the pure determi…]
- "tests_test_agents_testgetagentjobs": "TestGetAgentJobs" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L298 | neighbors=[test_agents.py, .test_404_when_agent_unknown(), .test_jobs_include_params(), .test_skips_job_outside_declared_networ…, .test_skips_job_when_capability_is_miss…, ScanJobType]
- "tests_test_agents_testotprofilegate": "TestOTProfileGate" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L170 | neighbors=[test_agents.py, .test_allows_passive_discovery_on_ot_en…, .test_blocks_active_scan_type_on_ot_eng…, .test_blocks_explicit_active_scan_type_…, .test_it_and_iot_profiles_unaffected(), ScanJobType]
- "tests_test_agents_testregisteragent_test_agent_token_is_long_lived": ".test_agent_token_is_long_lived()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L683 | neighbors=[Agent token must outlive the 15-min acc…, TestRegisterAgent, _user(), Agent token must outlive the 15-min acc…, Agent token must outlive the 15-min acc…, Agent token must outlive the 15-min acc…]
- "tests_test_agents_testregisteragent_test_reuses_existing_probe_by_name": ".test_reuses_existing_probe_by_name()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L648 | neighbors=[Re-registering the same-named probe mus…, TestRegisterAgent, _user(), Re-registering the same-named probe mus…, Re-registering the same-named probe mus…, Re-registering the same-named probe mus…]
- "tests_test_ai_engine_asset": "_asset()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L36 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher(), .test_predict_priority_uses_fallback_wh…]
- "tests_test_ai_engine_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L170 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_ai_engine_rationale_1": "Unit tests for the AI engine (Prompt 8).  The Anthropic client is mocked (no API" | kind=entity | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_campaign_progress_rows": "_rows()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L21 | neighbors=[test_campaign_progress.py, _progress(), A result whose .all() returns raw rows …, _run_scenario(), test_campaign_progress_aggregates_jobs_…, test_campaign_progress_no_detection_yet…]
- "tests_test_campaign_progress_run_scenario": "_run_scenario()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L117 | neighbors=[test_campaign_progress.py, Build a campaign_progress scenario with…, _rows(), _scalars(), test_completed_run_is_not_stuck_at_dete…, test_pipeline_advances_through_every_ph…]
- "tests_test_campaign_progress_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L13 | neighbors=[test_campaign_progress.py, _progress(), test_campaign_progress_aggregates_jobs_…, test_campaign_progress_no_detection_yet…, test_completed_run_is_not_stuck_at_dete…, test_pipeline_advances_through_every_ph…]
- "tests_test_cve_correlation_testvulndb": "TestVulnDB" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L119 | neighbors=[test_cve_correlation.py, .test_counts(), .test_cves_for_cpe_in_range(), .test_kev_sorts_first(), .test_out_of_range_excluded(), .test_vendor_norm()]
- "tests_test_db_scanner_testmysqlxvsoracle": "TestMysqlxVsOracle" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L53 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle(), .test_oracle_rejects_garbage_with_type_…, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_detection_coverage_test_completed_no_blind_is_plain_complete": "test_completed_no_blind_is_plain_complete()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L73 | neighbors=[test_detection_coverage.py, _job(), _rows(), _run(), _scalars(), _user()]
- "tests_test_detection_coverage_test_completed_with_blind_rules_is_complete_with_gaps": "test_completed_with_blind_rules_is_complete_with_gaps()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L47 | neighbors=[test_detection_coverage.py, _job(), _rows(), _run(), _scalars(), _user()]
- "tests_test_dns_scanner_testderivezones": "TestDeriveZones" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L25 | neighbors=[test_dns_scanner.py, .test_bounded(), .test_explicit_zone_used_as_is(), .test_extra_before_target_derived(), .test_hostname_target_reduces_to_regist…, .test_ip_target_derives_nothing()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-048.json

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
