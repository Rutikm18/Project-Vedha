# Node Description Batch 25 of 186

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

- "scanner_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L220 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), .__init__(), .scan_target(), ICMP-echo liveness + TTL harvest -> OS-…]
- "scanner_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()]
- "scanner_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L300 | neighbors=[PortScanner, _family_of(), ._build(), ._scan_port(), One connect() and its classification. A…, classify_os_error()]
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L749 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Subclasses implement `scan_target(self,…]
- "scanner_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L294 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…, Simple async rate limiter: at most `rat…]
- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/scanner/scanner_base.py:L129 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json(), One observation about one target. Pure …]
- "scanner_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…, workflow_engine.py]
- "scanner_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L238 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()]
- "scanner_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L200 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…]
- "scanner_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L261 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…]
- "scanner_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L276 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "schemas_auth_currentuser": "CurrentUser" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L20 | neighbors=[auth.py, BaseModel, Parsed from JWT claims — attached to re…, Close the global Redis connection pool.…, Reads user claims injected by TenantIso…, FastAPI dependency that enforces role-b…]
- "schemas_engagement_engagementcreate": "EngagementCreate" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L44 | neighbors=[engagement.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), EngagementStatus]
- "schemas_finding_findingpatch": "FindingPatch" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[finding.py, BaseModel, All fields optional — PATCH semantics., All fields optional — PATCH semantics., DetectionStatus, FindingSeverity]
- "scripts_seed_admin_seed_once": "_seed_once()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L192 | neighbors=[seed_admin.py, All DB work in a single transaction. Ro…, _detect_drift(), _hash(), log_info(), _verify_hash()]
- "scripts_startup_validator_validationreport": "ValidationReport" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L42 | neighbors=[startup_validator.py, run_all_validators(), .add(), .errors(), .print_summary(), .raise_if_errors()]
- "services_job_result_service_process_job_result": "process_job_result()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L127 | neighbors=[job_result_service.py, _promote_assets(), result_checksum(), validate_result_scope(), Process a scan job result.  Called from…, Process a scan job result.  Called from…]
- "services_job_result_service_rationale_143": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L143 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_job_result_service_rationale_33": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L33 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_llm_managerllmservice_client": "._client()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L367 | neighbors=[ManagerLlmService, ._anthropic(), ._ensure_installed_ollama_model(), ._ollama(), ._openai(), ._openrouter()]
- "services_llm_managerllmservice_default_runtime": "._default_runtime()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L94 | neighbors=[ManagerLlmService, AiRuntimeError, ._auto_cloud_provider(), Runtime, ._fallback_candidates(), .generate()]
- "services_llm_managerllmservice_generate_with_fallback": ".generate_with_fallback()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L322 | neighbors=[ManagerLlmService, AiRuntimeError, ._build_system(), ._dispatch(), ._ensure_installed_ollama_model(), ._fallback_candidates()]
- "services_posture_compute_scores": "compute_scores()" | kind=code-symbol | source=manager/backend/app/services/posture.py:L79 | neighbors=[posture.py, build_posture(), aggregate(), _exploit_prob(), grade_for(), _risk_prob()]
- "siem_config_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, SIEMConfig, GET(), POST(), 298a9d4 trim frontend to 7 core pages; …]
- "summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, backend(), with-backend.ts, withBackend(), ApiSummary]
- "tests_test_active_validation_escalation_ev": "_ev()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L6 | neighbors=[test_active_validation_escalation.py, test_confirmed_authoritative_does_not_e…, test_high_severity_suspected_escalates_…, test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_esca…, test_ot_profile_never_escalates()]
- "tests_test_agent_dispatch_testatomicwebsocketclaim": "TestAtomicWebSocketClaim" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L220 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…, ScanJobStatus, ScanJobType]
- "tests_test_agents_testenqueueagentjob": "TestEnqueueAgentJob" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L43 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()]
- "tests_test_ai_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L24 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_unavailable_without_client(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher()]
- "tests_test_ai_normalizer": "test_ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _fact(), TestAINormalizerCache, TestExtractRawText, TestFakeAIClient, TestProposeCandidates]
- "tests_test_attack_paths_rationale_1": "Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci" | kind=entity | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_engagement_lists": "test_engagement_lists.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user(), Unit tests for the dashboard list endpo…]
- "tests_test_finding_out_computed": "test_finding_out_computed.py" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L1 | neighbors=[8ebc053 feat(risk-rank-ui): surface ver…, _base(), test_confirmed_exploited_outranks_contr…, test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_risk_rank_is_computed_not_none()]
- "tests_test_host_discovery_mobile": "test_host_discovery_mobile.py" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, host_discovery.py, TestDeviceHint, TestLocallyAdministered, TestNormalizeMac, TestVendorLookup]
- "tests_test_host_discovery_mobile_testnormalizemac": "TestNormalizeMac" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L9 | neighbors=[test_host_discovery_mobile.py, .test_extracts_from_arp_line(), .test_lowercases(), .test_rejects_broadcast(), .test_rejects_garbage(), .test_rejects_multicast()]
- "tests_test_job_result_service": "test_job_result_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_out_of_scope_result_is_rejected_be…, test_result_scope_accepts_authorized_ta…, test_result_scope_fails_closed(), test_stale_attempt_gets_terminal_receip…]
- "tests_test_main_scripts_coverage_mk_scanner": "_mk_scanner()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L27 | neighbors=[test_main_scripts_coverage.py, _scope(), .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…]
- "tests_test_main_scripts_coverage_testprofiles": "TestProfiles" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L41 | neighbors=[test_main_scripts_coverage.py, .test_custom_dedups_and_requires_ports(), .test_full_is_entire_tcp_space(), .test_quick_is_small_and_contains_smb(), .test_top1000_covers_windows_ground_tru…, .test_top100_is_100_unique()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics": "TestWorkerPoolAndMetrics" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L81 | neighbors=[test_main_scripts_coverage.py, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state()]
- "tests_test_nuclei_background": "test_nuclei_background.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L1 | neighbors=[b4b12a9 Rename project and update files, _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_backgroun…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-024.json

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
