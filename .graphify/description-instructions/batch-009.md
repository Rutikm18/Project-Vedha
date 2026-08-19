# Node Description Batch 10 of 227

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

- "tests_test_auth_login": "test_auth_login.py" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, _make_db(), _make_tenant(), _make_user(), TestAuthenticateBcryptFailure] | lang=en
- "tests_test_detection_core_testcleanrpmversion": "TestCleanRpmVersion" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L988 | neighbors=[test_detection_core.py, .test_strips_release(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_core_testcpecandidatecpe23": "TestCPECandidateCpe23" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L907 | neighbors=[test_detection_core.py, .test_cpe23_format(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_core_testfactref": "TestFactRef" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L174 | neighbors=[test_detection_core.py, .test_ref_format(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_core_testfindingtodict": "TestFindingToDict" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L166 | neighbors=[test_detection_core.py, .test_enums_serialized_to_values(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_core_testnormalizeweb": "TestNormalizeWeb" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L925 | neighbors=[test_detection_core.py, .test_server_header(), ConsistencyReport, FindingConsistency, CPECandidate, EpssDB] | lang=en
- "tests_test_detection_validation_testsplunkintegration": "TestSplunkIntegration" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L296 | neighbors=[test_detection_validation.py, .skip_without_flag(), .test_live_query(), AttackAction, DetectionCorrelator, DetectionGap] | lang=en
- "tests_test_exploit_engine": "test_exploit_engine.py" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _engagement(), _finding(), pytest_addoption(), TestExploitOrchestrator] | lang=en
- "tests_test_exploit_engine_testvalidatemodule": "TestValidateModule" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L103 | neighbors=[test_exploit_engine.py, .test_dos_blocked(), .test_encoder_blocked(), .test_exploit_module_allowed(), .test_fuzzer_blocked(), .test_scanner_module_allowed()] | lang=en
- "tests_test_exploit_engine_testvalidatescope": "TestValidateScope" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L128 | neighbors=[test_exploit_engine.py, .test_excluded_cidr_takes_priority(), .test_invalid_ip_fails(), .test_ip_in_excluded_fails(), .test_ip_in_scope_passes(), .test_ip_out_of_scope_fails()] | lang=en
- "tests_test_outbox_reclaim": "test_outbox_reclaim.py" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, _mock_session(), _now(), _sql(), test_boundary_at_exactly_the_lease_is_r…, test_dead_letter_and_requeue_are_mutual…] | lang=en
- "tests_test_pipeline_empty_epss": "_empty_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L36 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default(), .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…] | lang=en
- "tests_test_pipeline_empty_kev": "_empty_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L32 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default(), .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…] | lang=en
- "tests_test_remediation_routes": "test_remediation_routes.py" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, _db_scalar(), _FakeDB, _finding(), _GenAI] | lang=en
- "tests_test_scan_funnel_make_funnel": "_make_funnel()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L64 | neighbors=[test_scan_funnel.py, FakeDiscovery, FakePortScanner, _scope(), Build a funnel with fakes; return (funn…, .test_db_scanner_invoked_with_db_port()] | lang=en
- "tests_test_service_identifier_testserviceidentifier_id": "._id()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L10 | neighbors=[TestServiceIdentifier, .test_confidence_floor_port_hint(), .test_ftp_banner(), .test_high_confidence_combined(), .test_http_server_header(), .test_kerberos_banner()] | lang=en
- "ad_adcs_certtemplate": "CertTemplate" | kind=code-symbol | source=manager/backend/app/ad/adcs.py:L37 | neighbors=[adcs.py, .enumerate_templates(), ACE, LDAPEnumerator, FindingSeverity, _FakeAttr] | lang=en
- "agent_cli_managerclient_request": ".request()" | kind=code-symbol | source=probe/agent/cli.py:L125 | neighbors=[cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create(), cmd_engagements_list()] | lang=en
- "auth_startup_run_startup_diagnostics": "run_startup_diagnostics()" | kind=code-symbol | source=manager/backend/app/auth/startup.py:L280 | neighbors=[startup.py, Run all startup checks concurrently.   …, _check_admin_account(), _check_bcrypt(), _check_cookie_config(), _check_cors()] | lang=en
- "commands_interactive_mainmenu": "mainMenu()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L2041 | neighbors=[interactive.ts, choose(), confirm(), divider(), ensureAuthenticated(), ln()] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@0fbec7dfc54f7cd50921f99169270a9330d111d0": "0fbec7d feat(verification): add finding verification verdict columns + migration" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@2fcec73635c396d5433940b61f8b85a02e532d50": "2fcec73 feat(verification): stamp verdicts on detection-run findings (flagged)" | kind=Commit | source=git | neighbors=[config.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@41b692a77a1dd6d2e5666f2fa2f8aa4b1e084e64": "41b692a Update project files" | kind=Commit | source=git | neighbors=[08e0594 deployement ready, AssistantFab.tsx, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@80b6dbcc5515152a76b93176716127f4f997f356": "80b6dbc Remove environment secrets from repository" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@8d65c9264d0935e030c458e4b761dd1587b0a2d1": "8d65c92 first commit" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@a0b870c8a083dca715a6f06baf63cd015adb389d": "a0b870c fix(posture): score over open findings only; lock grade-band boundary t…" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=pt
- "commit:repo:github.com/Rutikm18/Project-Vedha@c0f3b4c86830cc30f1c8a4da8694f7aa5c0807dc": "c0f3b4c feat(probe-enroll): trust-on-first-use auto-enrollment + gen-env policy…" | kind=Commit | source=git | neighbors=[22701ea Add tests for scanner parity an…, agent.py, config.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c5ebd3818a42f2cb9d5f6661004e3f5737bb605a": "c5ebd38 feat(sla): per-tenant custom SLA policies (item 4 backend)" | kind=Commit | source=git | neighbors=[2b4ff71 feat(fleet): one-click Approve …, main.py, feat/complete-pending-work, feat/engagement-detail-uiux, integration/all-branches, main] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@ddb51f2d79c6e862a9478d09389375d3f223afc3": "ddb51f2 feat(resolution): add finding resolution-lifecycle columns + migration" | kind=Commit | source=git | neighbors=[5d5c158 refactor: remove unused dashboa…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "components_sidebar": "Sidebar.tsx" | kind=code-symbol | source=manager/frontend/components/Sidebar.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, b5ffcb0 Refactor Vedha probe installer …, c4386e4 feat(customers): operator Custo…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "components_themeprovider": "ThemeProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ThemeProvider.tsx:L1 | neighbors=[layout.tsx, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, PageShell.tsx, subscribeToHydration()] | lang=en
- "console_primitives": "Primitives.tsx" | kind=code-symbol | source=manager/frontend/components/console/Primitives.tsx:L1 | neighbors=[5d5c158 refactor: remove unused dashboa…, Delta(), Meter(), Panel(), Readout(), SeverityChip()] | lang=en
- "detection_correlator_attackaction": "AttackAction" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L34 | neighbors=[correlator.py, EDRDetection, SIEMAlert, SigmaRuleGenerator, DetectionStatus, Detection validation API (DetectionVali…] | lang=en
- "launch_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, a789cca scanner: real use-case library,…, INTENSITY_PRESETS, LaunchBody] | lang=en
- "lib_findings_store_getallfindings": "getAllFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L33 | neighbors=[ask.ts, findings.ts, interactive.ts, findings-store.ts, deleteFinding(), ensureDir()] | lang=en
- "lib_job_store": "job-store.ts" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, createJob(), ensureDir(), genJobId(), getAllJobs(), getJobByScanId()] | lang=en
- "lib_scanner_request_validation": "scanner-request-validation.ts" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L1 | neighbors=[b4b12a9 Rename project and update files, isRecord(), isValidHostname(), isValidScannerTarget(), NETEXEC_CHECKS, NetExecScanRequest] | lang=en
- "models_agent_agent": "Agent" | kind=code-symbol | source=manager/backend/app/models/agent.py:L18 | neighbors=[agent.py, Base, TimestampMixin, Base, TimestampMixin, AgentRegisterRequest] | lang=en
- "routers_ai_report_reviewrequest": "ReviewRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L52 | neighbors=[ai_report.py, RejectRequest, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset] | lang=en
- "routers_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 2cddd52 fix(posture): tenant-scope run …, 9de087a feat(posture): add GET /analyti…, a0b870c fix(posture): score over open f…, dependencies.py, exposure()] | lang=en

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
