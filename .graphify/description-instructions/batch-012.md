# Node Description Batch 13 of 236

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@3ad95f45b1a7fcabc284bdb92a99e96a7ed33d57": "3ad95f4 feat: Optimize asset service fetching and enhance password handling- Re…" | kind=Commit | source=git | neighbors=[agent.py, router.py, startup.py, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@65e568441bfb43e313c743db52bd2f65fb7e86fe": "65e5684 feat(probe): transparent job logging (real use-case + result summary)" | kind=Commit | source=git | neighbors=[1af3404 feat(deploy): probe-free manage…, agent.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@6a1c958273a695fdfb8a8e43254742b6436b3b8e": "6a1c958 docs(plans): record execution status for active-validation + risk-rank …" | kind=Commit | source=git | neighbors=[50d6554 feat(active-validation): approv…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@88c92781d5435f80d9b62fb0869cca708fc4920b": "88c9278 feat(ai): pin manager LLM pipeline to Claude Sonnet 4.6" | kind=Commit | source=git | neighbors=[1d5ae94 feat(fleet): live "Connected pr…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, feat/remediation-ai-plans]
- "commit:repo:github.com/Rutikm18/Project-Vedha@e3958e7d0893279d1784154afd4ac1719633063f": "e3958e7 feat(customers): reveal + copy customer login password from dashboard (…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches, main]
- "explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, ManagerAiResponse, POST(), assistant.ts]
- "lib_auth_store": "auth-store.ts" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), OtpEntry, otpStore, OtpVerifyResult]
- "lib_finding_id": "finding-id.ts" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, counters, generateFindingId(), resetCounters()]
- "lib_nuclei_parser": "nuclei-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, countBySeverity(), NucleiMatch, nucleiMatchToFinding()]
- "login_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/login/page.tsx:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 5c6aa54 feat(portal-ui): portal shell/p…, 81c81cb feat: implement outbox reclaim …]
- "main_scripts_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 9c973dd feat(scanner): tarpit/honeypot …, ae08d19 feat(scanner): adaptive timeout…]
- "models_agent_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/backend/app/models/agent.py:L12 | neighbors=[agent.py, str, Base, TimestampMixin, AgentRegisterRequest, AgentRegisterResponse]
- "models_enums": "enums.py" | kind=code-symbol | source=manager/backend/app/models/enums.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Enum, AssetCriticality, AssetType, DetectionStatus]
- "native_http_probe": "http-probe.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractTitle(), fingerprint(), HttpProbeResult]
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L200 | neighbors=[agents.py, BaseModel, bootstrap_agent(), register_agent(), Asset, Engagement]
- "routers_agents_enqueuejobrequest": "EnqueueJobRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L301 | neighbors=[agents.py, BaseModel, ._validate_intensity(), ._validate_uc(), Asset, Engagement]
- "routers_ai_report_generaterequest": "GenerateRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L46 | neighbors=[ai_report.py, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath]
- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L56 | neighbors=[ai_report.py, ReviewRequest, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath]
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L86 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_exploits_exploitresultout": "ExploitResultOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L69 | neighbors=[exploits.py, BaseModel, _result_out(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError]
- "routers_vuln_scans_rationale_1": "Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[vuln_scans.py, Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus]
- "routers_vuln_scans_rationale_279": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L279 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _dec()]
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/scanner/web_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 37376de hardening(scanner): OPSEC de-si…, bce780a feat(probe): enumerate HTTP met…, d1b4dd3 trim frontend to 7 core pages; …, _fetch(), main()]
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 72f68af feat(verification): expose veri…, 85e4537 feat(risk-rank): expose risk_ra…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …]
- "str": "str" | kind=code-symbol | neighbors=[FindingState, SourceConfidence, AgentStatus, AssetCriticality, AssetType, DetectionStatus]
- "tests_test_ad_assessment_fakeattr": "_FakeAttr" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L31 | neighbors=[test_ad_assessment.py, .__init__(), .__getitem__(), ADCSChecker, CertTemplate, ASREPRoastChecker]
- "tests_test_agent_policy_roe": "_roe()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L30 | neighbors=[test_agent_policy.py, .test_decision_carries_action_and_tier(), .test_denylisted_module_denied(), .test_excluded_target_denied(), .test_exploit_attempt_cap_denied(), .test_halted_engagement_denies_everythi…]
- "tests_test_agent_policy_testevaluateaction": "TestEvaluateAction" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L36 | neighbors=[test_agent_policy.py, .test_decision_carries_action_and_tier(), .test_denylisted_module_denied(), .test_excluded_target_denied(), .test_exploit_attempt_cap_denied(), .test_halted_engagement_denies_everythi…]
- "tests_test_ai_engine_testvulnprioritizer": "TestVulnPrioritizer" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L47 | neighbors=[test_ai_engine.py, .setup_method(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_fallback_score_capped(), .test_higher_cvss_scores_higher()]
- "tests_test_customer_access": "test_customer_access.py" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, _added(), _mock_db(), _operator()]
- "tests_test_detection_validation_rationale_1": "Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc" | kind=entity | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection]
- "tests_test_exploit_engine_testmetasploitintegration": "TestMetasploitIntegration" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L419 | neighbors=[test_exploit_engine.py, Run against a live Metasploitable2 lab …, .skip_without_flag(), .test_connect_and_list_modules(), .test_run_safe_scanner_smb(), MetasploitRPCClient]
- "tests_test_main_scripts_correlation": "test_main_scripts_correlation.py" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L1 | neighbors=[6c1f014 feat(correlation): implement co…, _get(), _ids(), _run(), test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts()]
- "tests_test_main_scripts_findings_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L19 | neighbors=[test_main_scripts_findings.py, test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_ntp_monlist_and_dns_open_recursion…, test_open_filtered_never_raises_exposur…]
- "tests_test_main_scripts_rdp": "test_main_scripts_rdp.py" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _cc(), _run(), test_cc_without_negotiation_is_standard…, test_confirmed_rdp_wins_dedup_over_port…, test_confirmed_rdp_with_nla_has_no_nla_…]
- "tests_test_main_scripts_unauth": "test_main_scripts_unauth.py" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, unauth_access.py, _run(), test_couchdb_and_memcached_and_mongodb(), test_elasticsearch_unauth_vs_secured(), test_non_datastore_service_is_unknown()]
- "tests_test_nessus_scanner": "test_nessus_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _mock_response(), scanner(), test_authenticate_api_key(), test_create_scan(), test_create_scan_with_credentials()]
- "tests_test_new_scanners_testmobilescanner": "TestMobileScanner" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L518 | neighbors=[test_new_scanners.py, .test_adb_checksum_empty(), .test_adb_checksum_known_value(), .test_adb_cnxn_checksum_matches(), .test_adb_cnxn_command_field(), .test_adb_cnxn_magic_invariant()]
- "tests_test_nuclei_background_fakesession": "_FakeSession" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L30 | neighbors=[test_nuclei_background.py, .add(), .__aenter__(), .__aexit__(), .begin_nested(), .commit()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-012.json

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
