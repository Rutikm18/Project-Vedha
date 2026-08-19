# Node Description Batch 18 of 227

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

- "models_detection_run_detectionrun": "DetectionRun" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L40 | neighbors=[detection_run.py, Base, TimestampMixin, engine_bridge.py — run the deterministi…, A previously-remediated finding whose i…, Background entry point (P1: keep detect…]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 58c2d10 feat(active-validation): Valida…, 81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …]
- "path_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L1 | neighbors=[22701ea Add tests for scanner parity an…, backend.ts, backend(), BackendError, bearerFrom(), cookieFrom()]
- "routers_agent_ws": "agent_ws.py" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, database.py, _agent_token_from_websocket()]
- "routers_agents_encrypt_scope_for_agent": "_encrypt_scope_for_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L476 | neighbors=[agents.py, enqueue_agent_job(), get_agent_jobs(), Encrypt the engagement scope for a spec…, Encrypt the engagement scope for a spec…, Encrypt the engagement scope for a spec…]
- "routers_agents_rationale_1": "Agent registration, heartbeat, job polling, and result submission." | kind=entity | source=manager/backend/app/routers/agents.py:L1 | neighbors=[agents.py, Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_208": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L208 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_246": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L246 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_265": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L265 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_459": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L459 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_detection_rationale_1": "Detection validation API (DetectionValidationAPI).  POST /engagements/{id}/detec" | kind=entity | source=manager/backend/app/routers/detection.py:L1 | neighbors=[detection.py, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_detection_rationale_240": "Background task: pull SIEM/EDR telemetry, correlate, persist results." | kind=entity | source=manager/backend/app/routers/detection.py:L240 | neighbors=[_run_correlation(), AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_health": "health.py" | kind=code-symbol | source=manager/backend/app/routers/health.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, database.py, dependencies.py, version.py]
- "routers_remediation": "remediation.py" | kind=code-symbol | source=manager/backend/app/routers/remediation.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, dependencies.py, _build_upsert_stmt(), _cached_plan(), generate_remediation()]
- "scanner_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, Delta, DeltaEngine, _extract_service(), _extract_version(), main()]
- "scanner_findings_data": "_data()" | kind=code-symbol | source=probe/scanner/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_rdp(), _rule_smb(), _rule_snmp(), _rule_tls()]
- "scanner_ja4s": "ja4s.py" | kind=code-symbol | source=probe/scanner/ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()]
- "scanner_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), main()]
- "scanner_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/scanner/scanner_base.py:L725 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…]
- "scanner_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L695 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()]
- "scanner_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=probe/scanner/scanner_base.py:L564 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()]
- "scanner_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()]
- "scanner_syn_scanner_synscanner": "SynScanner" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L245 | neighbors=[syn_scanner.py, SYN scan on privileged Linux; transpare…, BaseScanner, ._build_results(), ._fallback_scan(), .__init__()]
- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate]
- "schemas_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, EngagementCreate, EngagementDetail, EngagementFilter]
- "scripts_startup_validator_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L34 | neighbors=[startup_validator.py, .validate(), .validate(), .validate(), .validate(), .validate()]
- "scripts_startup_validator_validationreport_add": ".add()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L45 | neighbors=[.validate(), .validate(), .validate(), .validate(), .validate(), .validate()]
- "services_llm": "llm.py" | kind=code-symbol | source=manager/backend/app/services/llm.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, 88c9278 feat(ai): pin manager LLM pipel…, cac022c Everything is done and verified…]
- "services_llm_managerllmservice_generate": ".generate()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L287 | neighbors=[ManagerLlmService, ._build_system(), ._default_runtime(), ._dispatch(), ._ensure_installed_ollama_model(), ._runtime()]
- "states_datastate_emptystate": "EmptyState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L38 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, page.tsx]
- "tests_assistant_test": "assistant.test.ts" | kind=code-symbol | source=manager/frontend/tests/assistant.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 65f22a7 Add comprehensive tests for aut…, route.ts, POST(), assistant.ts, cveRecordToFactCard()]
- "tests_scanner_adapters_test": "scanner-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/scanner-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, netexec-parser.ts, parseNetExecLog(), openvas-client.ts, parseOpenVASHelperOutput()]
- "tests_test_ai_engine_testllmreportgenerator": "TestLLMReportGenerator" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L177 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_attack_paths_testgraphvisualizer": "TestGraphVisualizer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L185 | neighbors=[test_attack_paths.py, .test_d3_highlights_top_path(), .test_d3_marks_compromised(), .test_d3_shape(), .test_layout_is_deterministic(), PathAnalyzer]
- "tests_test_auth_login_make_db": "_make_db()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L69 | neighbors=[test_auth_login.py, AsyncSession mock that returns user on …, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future()]
- "tests_test_customer_access_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L27 | neighbors=[test_customer_access.py, db.execute yields the given scalar_one_…, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_assigns_agent_to_engagement()]
- "tests_test_db_scanner": "test_db_scanner.py" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, db_scanner.py, FakeReader, FakeWriter, _probe(), _run()]
- "tests_test_detection_core_candidate": "_candidate()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L44 | neighbors=[test_detection_core.py, .test_cpe23_format(), .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding()]
- "tests_test_detection_validation_action": "_action()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L37 | neighbors=[test_detection_validation.py, .test_compute_coverage(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking(), .test_gap_report_ignores_detected(), .test_generate_gap_report()]
- "tests_test_main_scripts_hardening": "test_main_scripts_hardening.py" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, make_smb2_error(), make_smb2_success(), _run(), _scope()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-017.json

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
