# Node Description Batch 39 of 330

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

- "scanner_service_enum_serviceenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_enum.py:L558 | neighbors=[ServiceEnumScanner, classify_roles(), Enrichment, guess_os(), resolve_hostnames(), ._probe_port()]
- "scanner_smb_enum_scanner_smbenumscanner_enumerate": "._enumerate()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L227 | neighbors=[Blocking: attempt a null session and en…, SMBEnumScanner, _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), _merge_users()]
- "scanner_smtp_scanner": "smtp_scanner.py" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, main(), parse_ehlo_capabilities(), SMTPScanner, vrfy_leaks(), smtp_scanner.py — SMTP hygiene: user en…]
- "scanner_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…, workflow_engine.py]
- "scanner_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L224 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie(), Keyed 32-bit ISN for (dst_ip, dst_port,…, Keyed 32-bit ISN for (dst_ip, dst_port,…]
- "scanner_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L231 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie(), A genuine reply to our SYN acknowledges…, A genuine reply to our SYN acknowledges…]
- "scanner_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L275 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…]
- "scanner_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L165 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni(), Attempt a handshake forcing one protoco…, Attempt a handshake forcing one protoco…]
- "scanner_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L282 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "scanner_va_campaign_build_campaign": "build_campaign()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L620 | neighbors=[va_campaign.py, CampaignContext, default_stages(), ProgressReporter, VACampaign, Wire a campaign with the real scanners …]
- "scanner_va_campaign_cliprogressview": "CliProgressView" | kind=code-symbol | source=probe/scanner/va_campaign.py:L649 | neighbors=[va_campaign.py, .__call__(), ._format(), .__init__(), ._redraw(), ._transitions()]
- "scanner_va_campaign_progressreporter_flush": "._flush()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L265 | neighbors=[ProgressReporter, .finish(), _atomic_write_json(), .snapshot(), .__init__(), .mark()]
- "schemas_auth_currentuser": "CurrentUser" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L20 | neighbors=[auth.py, BaseModel, Parsed from JWT claims — attached to re…, Close the global Redis connection pool.…, Reads user claims injected by TenantIso…, FastAPI dependency that enforces role-b…]
- "schemas_engagement_engagementcreate": "EngagementCreate" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L44 | neighbors=[engagement.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), EngagementStatus]
- "scripts_seed_admin_seed_once": "_seed_once()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L192 | neighbors=[seed_admin.py, All DB work in a single transaction. Ro…, _detect_drift(), _hash(), log_info(), _verify_hash()]
- "scripts_startup_validator_validationreport": "ValidationReport" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L42 | neighbors=[startup_validator.py, run_all_validators(), .add(), .errors(), .print_summary(), .raise_if_errors()]
- "services_finding_events_synthesize_events": "synthesize_events()" | kind=code-symbol | source=manager/backend/app/services/finding_events.py:L108 | neighbors=[finding_events.py, build_timeline(), Derive the canonical lifecycle events t…, _detected_actor(), _detected_detail(), _ev()]
- "services_job_result_service_rationale_143": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L143 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_job_result_service_rationale_33": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L33 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_job_result_service_validate_result_scope": "validate_result_scope()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L131 | neighbors=[job_result_service.py, process_job_result(), Return result identities outside the jo…, _identity_ip(), _result_network_identities(), Return result identities outside the jo…]
- "services_llm_managerllmservice_client": "._client()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L408 | neighbors=[ManagerLlmService, ._anthropic(), ._ensure_installed_ollama_model(), ._ollama(), ._openai(), ._openrouter()]
- "services_llm_managerllmservice_default_runtime": "._default_runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L135 | neighbors=[ManagerLlmService, AiRuntimeError, ._auto_cloud_provider(), Runtime, ._fallback_candidates(), .generate()]
- "services_llm_managerllmservice_fallback_candidates": "._fallback_candidates()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L341 | neighbors=[ManagerLlmService, ._default_runtime(), ._runtime(), Runtime, .generate_with_fallback(), Ordered runtimes to try: requested/defa…]
- "services_posture_compute_scores": "compute_scores()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L79 | neighbors=[posture.py, build_posture(), aggregate(), _exploit_prob(), grade_for(), _risk_prob()]
- "services_project_time": "project_time.py" | kind=code-symbol | source=manager/backend/app/services/project_time.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, project_file_stamp(), project_now(), project_timestamp(), _resolve_project_tz(), to_project_tz()]
- "services_risk_rank": "risk_rank.py" | kind=code-symbol | source=manager/backend/app/services/risk_rank.py:L1 | neighbors=[0d6be85 feat(risk-rank): explainable 0-…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, _bounded(), compute_risk_rank()]
- "siem_config_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, SIEMConfig, GET(), POST(), 298a9d4 trim frontend to 7 core pages; …]
- "sla_policy_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/sla-policy/route.ts:L1 | neighbors=[aedddfa feat(settings): editable SLA po…, backend.ts, backend(), with-backend.ts, withBackend(), GET]
- "supporting_research_evidence_store_resolve_identity": "resolve_identity()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L174 | neighbors=[evidence_store.py, Cluster observations into assets using …, _identity_keys(), IdentityResult, _UnionFind, .find()]
- "supporting_research_test_evidence_store_build_fleet": "build_fleet()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L72 | neighbors=[test_evidence_store.py, smb_obs(), ssh_obs(), demo(), 30 days of history. HOST_A is patched o…, .setUp()]
- "tests_test_active_validation_escalation_ev": "_ev()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L6 | neighbors=[test_active_validation_escalation.py, test_confirmed_authoritative_does_not_e…, test_high_severity_suspected_escalates_…, test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_esca…, test_ot_profile_never_escalates()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim": "TestAtomicWebSocketClaim" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L220 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…, ScanJobStatus, ScanJobType]
- "tests_test_agent_read_tools_fakesession": "_FakeSession" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L32 | neighbors=[test_agent_read_tools.py, .execute(), .__init__(), Returns queued results in call order an…, test_list_assets_batches_services_no_n_…, test_list_assets_caps_services_at_30()]
- "tests_test_agents_testenqueueagentjob": "TestEnqueueAgentJob" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L49 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()]
- "tests_test_ai_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L24 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_unavailable_without_client(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher()]
- "tests_test_ai_normalizer": "test_ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _fact(), TestAINormalizerCache, TestExtractRawText, TestFakeAIClient, TestProposeCandidates]
- "tests_test_attack_paths_rationale_1": "Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci" | kind=entity | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected": "TestNormalPipelineUnaffected" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L72 | neighbors=[test_campaign_progress_terminal.py, Regression guard: the happy path and it…, .test_complete_campaign(), .test_complete_with_gaps(), .test_defaults_keep_backwards_compatibi…, .test_no_jobs_is_pending()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults": "TestTerminalWithoutResults" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L38 | neighbors=[test_campaign_progress_terminal.py, .test_a_dead_queue_is_still_reported_as…, .test_all_cancelled_campaign_is_termina…, .test_all_failed_campaign_is_terminal(), .test_does_not_hijack_a_campaign_that_p…, .test_partial_cancel_with_one_success_s…]
- "tests_test_cve_correlation_testcpe": "TestCpe" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L75 | neighbors=[test_cve_correlation.py, .test_datastore_map_entries(), .test_mysql_vs_mariadb_vendor(), .test_no_version_returns_none(), .test_openssh(), .test_unknown_product_returns_none()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-038.json

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
