# Node Description Batch 10 of 209

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

- "scanner_passive_collector": "passive_collector.py" | kind=code-symbol | source=probe/scanner/passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, d1b4dd3 trim frontend to 7 core pages; …, _coverage(), _device_hint(), _is_readable(), _listener_error_code()]
- "schemas_portal": "portal.py" | kind=code-symbol | source=manager/backend/app/schemas/portal.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, c52feb4 feat(portal): reskin User Porta…, ClientEngagementOut, ClientFindingOut, ClientPostureOut]
- "scripts_startup_validator": "startup_validator.py" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, AppEnvironmentValidator, CheckResult, ConfigValidator, CookieValidator, CorsValidator]
- "tests_test_ad_assessment_testbuildadfinding": "TestBuildADFinding" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L58 | neighbors=[test_ad_assessment.py, .test_attack_narrative_carried_in_evide…, .test_invalid_severity_falls_back_to_in…, .test_required_fields_present(), ADCSChecker, CertTemplate]
- "tests_test_agents_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L22 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()]
- "tests_test_detection_core_rationale_1": "Detection engine test suite — unit tests for the core detection/correlation pipe" | kind=entity | source=manager/detection_engine/tests/test_detection_core.py:L1 | neighbors=[test_detection_core.py, ConsistencyReport, FindingConsistency, CPECandidate, EpssDB, KevDB]
- "tests_test_pipeline": "test_pipeline.py" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _banner_jsonl(), _empty_epss(), _empty_jsonl(), _empty_kev(), _mock_vuln_db()]
- "tests_test_pipeline_openssh_vuln_db": "_openssh_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L49 | neighbors=[test_pipeline.py, _mock_vuln_db(), Returns a VulnDB with a record that mat…, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default()]
- "tools_manifest": "manifest.ts" | kind=code-symbol | source=manager/frontend/lib/tools/manifest.ts:L1 | neighbors=[tools.ts, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, currentPlatform(), Platform, TOOL_MANIFEST]
- "ad_ldap_enum_aduser": "ADUser" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L55 | neighbors=[ldap_enum.py, .get_users(), ADConnectionError, DependencyMissingError, _FakeAttr, _FakeEntry]
- "agent_agent_main": "main()" | kind=code-symbol | source=probe/agent/agent.py:L205 | neighbors=[agent.py, _bounded_env_int(), _classify_connection_error(), _dbg(), _is_local_manager_url(), _load_env()]
- "agent_license": "license.py" | kind=code-symbol | source=probe/agent/license.py:L1 | neighbors=[agent.py, _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError]
- "agent_task_runner": "task_runner.py" | kind=code-symbol | source=probe/agent/task_runner.py:L1 | neighbors=[JobResult, TaskRunner, use_cases.py, task_runner.py — orchestrates the full …, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "auth_startup_run_startup_diagnostics": "run_startup_diagnostics()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L282 | neighbors=[startup.py, Run all startup checks concurrently.   …, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()]
- "commands_interactive_ask": "ask()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L39 | neighbors=[interactive.ts, choose(), confirm(), ensureAuthenticated(), pickHostSubset(), pickTargets()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@10ceacaffacf60f95eeb0e9b2b247b62bfa5dfb8": "10ceaca feat: implement AI model fallback mechanism and enhance model selection…" | kind=Commit | source=git | neighbors=[AssistantDrawer.tsx, ModelSwitcher.tsx, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@8ebc0534dda8a1316f41c2fccf928f42acf9ed46": "8ebc053 feat(risk-rank-ui): surface verification + lifecycle state on findings …" | kind=Commit | source=git | neighbors=[6a1c958 docs(plans): record execution s…, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, 4d0377d Add unit tests for SMB scanner,…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bb0ef3d473623bac3404761b5c3d34baa72612dd": "bb0ef3d feat(probe): route DB services on non-standard ports via banner signatu…" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/coverage-gated-auto-resolution, feat/syn-scanner-osfp-adaptive, integration/all-branches, main, spike/probe-go]
- "commit:repo:github.com/Rutikm18/Project-Vedha@c4386e4cbc0ee346a71c211a96326772b677c561": "c4386e4 feat(customers): operator Customers dashboard + per-customer portal slug" | kind=Commit | source=git | neighbors=[ae08d19 feat(scanner): adaptive timeout…, main.py, feat/syn-scanner-osfp-adaptive, main, 1d5ae94 feat(fleet): live "Connected pr…, Sidebar.tsx]
- "components_themeprovider": "ThemeProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L1 | neighbors=[layout.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, subscribeToHydration()]
- "detection_engine_cpe_normalizer": "cpe_normalizer.py" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), CPECandidate, normalize()]
- "detection_engine_vuln_db": "vuln_db.py" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _boundary_versions(), _clear_caches(), _content_hash()]
- "explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, ManagerAiResponse, POST(), assistant.ts]
- "lib_auth_store": "auth-store.ts" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), OtpEntry, otpStore, OtpVerifyResult]
- "lib_finding_id": "finding-id.ts" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, counters, generateFindingId(), resetCounters()]
- "lib_nuclei_parser": "nuclei-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, countBySeverity(), NucleiMatch, nucleiMatchToFinding()]
- "models_agent_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/backend/app/models/agent.py:L12 | neighbors=[agent.py, str, Base, TimestampMixin, AgentRegisterRequest, AgentRegisterResponse]
- "models_enums": "enums.py" | kind=code-symbol | source=manager/backend/app/models/enums.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Enum, AssetCriticality, AssetType, DetectionStatus]
- "native_http_probe": "http-probe.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractTitle(), fingerprint(), HttpProbeResult]
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L200 | neighbors=[agents.py, BaseModel, bootstrap_agent(), register_agent(), Asset, Engagement]
- "routers_agents_enqueuejobrequest": "EnqueueJobRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L300 | neighbors=[agents.py, BaseModel, ._validate_intensity(), ._validate_uc(), Asset, Engagement]
- "routers_ai_report_generaterequest": "GenerateRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L46 | neighbors=[ai_report.py, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath]
- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L56 | neighbors=[ai_report.py, ReviewRequest, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath]
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L86 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_exploits_exploitresultout": "ExploitResultOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L69 | neighbors=[exploits.py, BaseModel, _result_out(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_vuln_scans_rationale_1": "Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[vuln_scans.py, Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "routers_vuln_scans_rationale_279": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L279 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_mcp_ai_scanner": "mcp_ai_scanner.py" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _auth_shaped_json_body(), _known_false_positive(), main(), _mcp_oauth_signal()]
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 72f68af feat(verification): expose veri…, 85e4537 feat(risk-rank): expose risk_ra…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …]
- "services_job_result_service": "job_result_service.py" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, cac022c Everything is done and verified…, _apply_device_profile()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-009.json

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
