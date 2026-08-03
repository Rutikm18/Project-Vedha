# Node Description Batch 7 of 131

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

- "auth_exceptions": "exceptions.py" | kind=code-symbol | source=manager/backend/app/auth/exceptions.py:L1 | neighbors=[AuthenticationError, BcryptFailureError, DatabaseFailureError, DatabaseUnavailableError, DisabledTenantError, DisabledUserError]
- "auth_router": "router.py" | kind=code-symbol | source=manager/backend/app/auth/router.py:L1 | neighbors=[database.py, dependencies.py, ratelimit.py, _authenticate(), create_personal_access_token(), list_personal_access_tokens()]
- "detection_siem_siemalert": "SIEMAlert" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L24 | neighbors=[siem.py, .parse_response(), .parse_response(), .parse_response(), AttackAction, DetectionCorrelator]
- "detection_sigma_sigmarulegenerator": "SigmaRuleGenerator" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L107 | neighbors=[sigma.py, ._customise_detection(), .generate_sigma_for_technique(), ._lookup_template(), AttackAction, DetectionCorrelator]
- "discovery_service_id_servicefingerprint": "ServiceFingerprint" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L13 | neighbors=[service_id.py, .identify(), NucleiRunReport, NucleiScanError, NucleiScanner, NucleiScanner — async subprocess wrappe…]
- "graph_analyzer_pathanalyzer": "PathAnalyzer" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L60 | neighbors=[analyzer.py, ._exploit_info(), .find_blast_radius(), .find_paths_to_target(), .identify_chokepoints(), .__init__()]
- "lib_backend_bearerfrom": "bearerFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L97 | neighbors=[route.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "lib_exploit_store": "exploit-store.ts" | kind=code-symbol | source=manager/frontend/lib/exploit-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, approvals, ApprovalStatus, AuditEntry, auditLog, ExploitApprovalRequest]
- "models_attack_path_attackpath": "AttackPath" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L11 | neighbors=[attack_path.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…]
- "models_detection_detectionresult": "DetectionResult" | kind=code-symbol | source=manager/backend/app/models/detection.py:L12 | neighbors=[detection.py, Base, TimestampMixin, Base, TimestampMixin, DetectionStatus]
- "native_port_scan": "port-scan.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, CheckOpts, checkPort(), expandTarget()]
- "routers_engagements_engagementupdate": "EngagementUpdate" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L483 | neighbors=[engagements.py, BaseModel, .normalize_name(), .validate_dates(), .validate_scopes(), Asset]
- "scanner_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/scanner/passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, _coverage(), _device_hint(), _is_readable()]
- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 95904f1 feat(probe): detect SMB signing…, d1b4dd3 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main()]
- "services_llm_managerllmservice": "ManagerLlmService" | kind=code-symbol | source=manager/backend/app/services/llm.py:L64 | neighbors=[llm.py, ._anthropic(), ._client(), ._default_runtime(), ._ensure_installed_ollama_model(), .generate()]
- "tests_test_ai_engine_testhallucinationguard": "TestHallucinationGuard" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L104 | neighbors=[test_ai_engine.py, .setup_method(), .test_cve_all_known_valid(), .test_cve_invention_flagged(), .test_cvss_match_passes(), .test_cvss_mismatch_flagged()]
- "tests_test_attack_paths_testgraphbuilder": "TestGraphBuilder" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L52 | neighbors=[test_attack_paths.py, .test_asset_node_attributes(), .test_connects_to_and_same_segment_edge…, .test_credential_reuse_edges(), .test_exploit_complexity_falls_back_to_…, .test_exploit_complexity_from_vector()]
- "tests_test_auth_login": "test_auth_login.py" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, _make_db(), _make_tenant(), _make_user(), TestAuthenticateBcryptFailure]
- "tests_test_detection_core_testcleanrpmversion": "TestCleanRpmVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L988 | neighbors=[test_detection_core.py, .test_strips_release(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_core_testcpecandidatecpe23": "TestCPECandidateCpe23" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L907 | neighbors=[test_detection_core.py, .test_cpe23_format(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_core_testfactref": "TestFactRef" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L174 | neighbors=[test_detection_core.py, .test_ref_format(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_core_testfindingtodict": "TestFindingToDict" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L166 | neighbors=[test_detection_core.py, .test_enums_serialized_to_values(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_core_testnormalizeweb": "TestNormalizeWeb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L925 | neighbors=[test_detection_core.py, .test_server_header(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB]
- "tests_test_detection_validation_testsplunkintegration": "TestSplunkIntegration" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L296 | neighbors=[test_detection_validation.py, .skip_without_flag(), .test_live_query(), AttackAction, DetectionCorrelator, DetectionGap]
- "tests_test_exploit_engine": "test_exploit_engine.py" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator]
- "tests_test_exploit_engine_testvalidatemodule": "TestValidateModule" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L103 | neighbors=[test_exploit_engine.py, .test_dos_blocked(), .test_encoder_blocked(), .test_exploit_module_allowed(), .test_fuzzer_blocked(), .test_scanner_module_allowed()]
- "tests_test_exploit_engine_testvalidatescope": "TestValidateScope" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L128 | neighbors=[test_exploit_engine.py, .test_excluded_cidr_takes_priority(), .test_invalid_ip_fails(), .test_ip_in_excluded_fails(), .test_ip_in_scope_passes(), .test_ip_out_of_scope_fails()]
- "tests_test_service_identifier_testserviceidentifier_id": "._id()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L10 | neighbors=[TestServiceIdentifier, .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined(), .test_http_server_header(), .test_kerberos_banner()]
- "ad_adcs_certtemplate": "CertTemplate" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L37 | neighbors=[adcs.py, .enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity, _FakeAttr]
- "agent_agent_run_ws_push_loop": "_run_ws_push_loop()" | kind=code-symbol | source=probe/agent/agent.py:L414 | neighbors=[agent.py, main(), Persistent WebSocket push loop.      Re…, _flush_spool_over_http(), say(), _ws_heartbeat_sender()]
- "agent_agent_say": "say()" | kind=code-symbol | source=probe/agent/agent.py:L76 | neighbors=[agent.py, _check_anti_debug(), _enroll_device(), _flush_spool_over_http(), _load_or_create_identity(), main()]
- "agent_cli_managerclient_request": ".request()" | kind=code-symbol | source=probe/agent/cli.py:L125 | neighbors=[cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create(), cmd_engagements_list()]
- "app_layout": "layout.tsx" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L1 | neighbors=[metadata, RootLayout(), AssistantProvider.tsx, AssistantProvider(), QueryProvider.tsx, QueryProvider()]
- "commands_interactive_mainmenu": "mainMenu()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2041 | neighbors=[interactive.ts, choose(), confirm(), divider(), ensureAuthenticated(), ln()]
- "detection_correlator_attackaction": "AttackAction" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L34 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus, Detection validation API (DetectionVali…]
- "lib_assistant": "assistant.ts" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, 1fe16c8 stable but some dead code, need…, cveRecordToFactCard()]
- "lib_findings_store_getallfindings": "getAllFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L33 | neighbors=[ask.ts, findings.ts, interactive.ts, findings-store.ts, deleteFinding(), ensureDir()]
- "lib_job_store": "job-store.ts" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId()]
- "lib_scanner_request_validation": "scanner-request-validation.ts" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L1 | neighbors=[b4b12a9 Rename project and update files, isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS, NetExecScanRequest]
- "models_agent_agent": "Agent" | kind=code-symbol | source=manager/backend/app/models/agent.py:L18 | neighbors=[agent.py, Base, TimestampMixin, Base, TimestampMixin, AgentRegisterRequest]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-006.json

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
