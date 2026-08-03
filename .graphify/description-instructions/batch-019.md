# Node Description Batch 20 of 131

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

- "routers_analytics_protocolrisk": "ProtocolRisk" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L27 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_analytics_zonehealth": "ZoneHealth" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L32 | neighbors=[analytics.py, BaseModel, Asset, Engagement, FindingStatus, Finding]
- "routers_engagements_import_facts": "import_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L294 | neighbors=[engagements.py, _parse_probe_file(), _promote_from_facts(), _read_capped(), _refresh_overview_cache(), Offline ingest path: upload a probe's s…]
- "routers_findings_rationale_25": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L25 | neighbors=[_tenant_finding(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_findings_rationale_26": "Fetch a finding scoped to the caller's tenant via its parent engagement.      Fi" | kind=entity | source=manager/backend/app/routers/findings.py:L26 | neighbors=[Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding, _tenant_finding()]
- "routers_findings_rationale_48": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L48 | neighbors=[sla_summary(), Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding]
- "routers_findings_rationale_49": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L49 | neighbors=[Engagement, DetectionStatus, FindingSeverity, FindingStatus, Finding, sla_summary()]
- "routers_probe_enrollment_activate_enrollment": "activate_enrollment()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L524 | neighbors=[probe_enrollment.py, _authenticated_request(), _derive_refresh_secret(), _policy(), _rate_limit(), _secret_hash()]
- "routers_probe_enrollment_create_enrollment_request": "create_enrollment_request()" | kind=code-symbol | source=manager/backend/app/routers/probe_enrollment.py:L309 | neighbors=[probe_enrollment.py, _decode_public_key(), enroll_token_is_usable(), _keyed_hash(), _provision_agent_for_site(), _rate_limit()]
- "scanner_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L198 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()]
- "scanner_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L236 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()]
- "scanner_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()]
- "scanner_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L490 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()]
- "scanner_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…, workflow_engine.py]
- "schemas_auth_currentuser": "CurrentUser" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L20 | neighbors=[auth.py, BaseModel, Parsed from JWT claims — attached to re…, Close the global Redis connection pool.…, Reads user claims injected by TenantIso…, FastAPI dependency that enforces role-b…]
- "schemas_engagement_engagementcreate": "EngagementCreate" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L44 | neighbors=[engagement.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), EngagementStatus]
- "scripts_seed_admin_seed_once": "_seed_once()" | kind=code-symbol | source=manager/backend/scripts/seed_admin.py:L192 | neighbors=[seed_admin.py, All DB work in a single transaction. Ro…, _detect_drift(), _hash(), log_info(), _verify_hash()]
- "scripts_startup_validator_validationreport": "ValidationReport" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L42 | neighbors=[startup_validator.py, run_all_validators(), .add(), .errors(), .print_summary(), .raise_if_errors()]
- "services_job_result_service_process_job_result": "process_job_result()" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L127 | neighbors=[job_result_service.py, _promote_assets(), result_checksum(), validate_result_scope(), Process a scan job result.  Called from…, Process a scan job result.  Called from…]
- "services_job_result_service_rationale_143": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L143 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_job_result_service_rationale_33": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L33 | neighbors=[Asset, AssetType, ScanJobStatus, ScanJob, ScanResult, Service]
- "services_llm": "llm.py" | kind=code-symbol | source=manager/backend/app/services/llm.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, config.py, AiRuntimeError, _is_local_ollama_model(), ManagerLlmService]
- "services_llm_managerllmservice_client": "._client()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L239 | neighbors=[ManagerLlmService, ._anthropic(), ._ensure_installed_ollama_model(), ._ollama(), ._openai(), ._openrouter()]
- "services_llm_runtime": "Runtime" | kind=code-symbol | source=manager/backend/app/services/llm.py:L28 | neighbors=[llm.py, ._default_runtime(), ._runtime(), Settings, AiGenerateRequest, AiProviderStatus]
- "siem_config_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/siem-config/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, detectionStore, SIEMConfig, GET(), POST(), 298a9d4 trim frontend to 7 core pages; …]
- "states_datastate_emptystate": "EmptyState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L36 | neighbors=[page.tsx, Exposure.tsx, SlaStatus.tsx, page.tsx, page.tsx, page.tsx]
- "summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/summary/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, backend(), with-backend.ts, withBackend(), ApiSummary]
- "tests_test_agent_dispatch_testatomicwebsocketclaim": "TestAtomicWebSocketClaim" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L215 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…, ScanJobStatus, ScanJobType]
- "tests_test_agents_testenqueueagentjob": "TestEnqueueAgentJob" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L43 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()]
- "tests_test_ai_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L24 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_unavailable_without_client(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher()]
- "tests_test_attack_paths_rationale_1": "Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci" | kind=entity | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_engagement_lists": "test_engagement_lists.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user(), Unit tests for the dashboard list endpo…]
- "tests_test_installer_contract": "test_installer_contract.py" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _dry_run(), test_installer_accepts_enroll_token_and…, test_installer_rejects_missing_or_unkno…, test_installer_requires_only_manager_en…, test_installer_source_has_no_human_or_j…]
- "tests_test_job_result_service": "test_job_result_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_out_of_scope_result_is_rejected_be…, test_result_scope_accepts_authorized_ta…, test_result_scope_fails_closed(), test_stale_attempt_gets_terminal_receip…]
- "tests_test_nuclei_background": "test_nuclei_background.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L1 | neighbors=[b4b12a9 Rename project and update files, _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_backgroun…]
- "tests_test_nuclei_background_nestedtransaction": "_NestedTransaction" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L22 | neighbors=[test_nuclei_background.py, .begin_nested(), .__aenter__(), .__aexit__(), ScanJobStatus, NucleiRunReport]
- "tests_test_nuclei_background_scalarresult": "_ScalarResult" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L14 | neighbors=[test_nuclei_background.py, .execute(), .__init__(), .scalar_one_or_none(), ScanJobStatus, NucleiRunReport]
- "tests_test_probe_core_testclassifycertainty": "TestClassifyCertainty" | kind=code-symbol | source=probe/tests/test_probe_core.py:L706 | neighbors=[test_probe_core.py, .test_error_overrides(), .test_host_discovery_uncertain(), .test_service_banner_deterministic(), .test_tcp_port_scan_deterministic(), .test_udp_port_scan_uncertain()]
- "tests_test_scope_validator_testmergeexclusions": "TestMergeExclusions" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L144 | neighbors=[test_scope_validator.py, .test_both_empty(), .test_empty_engagement_excludes(), .test_empty_job_excludes(), .test_merges_no_duplicates(), .test_none_job_excludes()]
- "tests_test_udp_amplifiers": "test_udp_amplifiers.py" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L1 | neighbors=[fe868e6 feat(probe): real UDP amplifica…, udp_scanner.py, test_dns_open_recursion(), test_memcached_exposed(), test_ntp_monlist_absent(), test_ntp_monlist_enabled()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-019.json

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
