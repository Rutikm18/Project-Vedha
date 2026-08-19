# Node Description Batch 12 of 227

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

- "commit:repo:github.com/Rutikm18/Project-Vedha@a4b970ca55febc554c4d6d9f90369fafaa5f8111": "a4b970c feat(fleet): add run command for already-downloaded install.sh" | kind=Commit | source=git | neighbors=[30261eb feat: enhance advisor flow with…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bd409f5724ece8d940d48f06f98b9f6188970117": "bd409f5 feat(resolution): async applier over engine-managed open findings" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans, feat/syn-scanner-osfp-adaptive] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c02c4652680a709056c4a8e342699c00e80454dc": "c02c465 feat(verification): optional LangGraph orchestration skin" | kind=Commit | source=git | neighbors=[verification_graph.py, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c5e2d0ed7a2fe2e171616a98cebb2295cf557314": "c5e2d0e chore: retire probe-go to spike/probe-go branch" | kind=Commit | source=git | neighbors=[1fe16c8 stable but some dead code, need…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@c7f226f03ff7acd5ce8d6938c21a4e8b7e8997b4": "c7f226f chore: bundle pending working-tree work for release" | kind=Commit | source=git | neighbors=[656e909 feat(ui): polish login page, to…, feat/complete-pending-work, main, portal-client.ts, scan_request.py, customer_access.py] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@caf1e5d0a9e53f79a5c9e541a083b332aa127fdd": "caf1e5d feat(verification): deterministic passive verdict core" | kind=Commit | source=git | neighbors=[0fbec7d feat(verification): add finding…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@cbf5d6cb96915e7c031de705eb116568a081940b": "cbf5d6c feat(resolution): pure decision core (coverage + confirm window + db gu…" | kind=Commit | source=git | neighbors=[9a36729 feat(resolution): coverage buil…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@de2d1c9825984fa315f761df4bb2da6139d7ff36": "de2d1c9 feat(verification): optional fail-closed LLM rationale + FP-triage" | kind=Commit | source=git | neighbors=[caf1e5d feat(verification): determinist…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=nl
- "commit:repo:github.com/Rutikm18/Project-Vedha@fadb4f53f6fecb205c9da67b084b4f8ad43ea578": "fadb4f5 fix(posture): hoist report-section test import; flush before section co…" | kind=Commit | source=git | neighbors=[0f0097b feat(posture): mirror posture s…, feat/autonomous-offensive-agent, feat/complete-pending-work, feat/coverage-gated-auto-resolution, feat/engagement-detail-uiux, feat/remediation-ai-plans] | lang=en
- "detection_engine_cpe_normalizer": "cpe_normalizer.py" | kind=code-symbol | source=manager/detection_engine/cpe_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, all_osv_source_packages(), clean_debian_version(), clean_rpm_version(), CPECandidate, normalize()] | lang=en
- "detection_engine_vuln_db": "vuln_db.py" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _boundary_versions(), _clear_caches(), _content_hash()] | lang=en
- "explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, ManagerAiResponse, POST(), assistant.ts] | lang=en
- "lib_auth_store": "auth-store.ts" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), OtpEntry, otpStore, OtpVerifyResult] | lang=en
- "lib_finding_id": "finding-id.ts" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, counters, generateFindingId(), resetCounters()] | lang=en
- "lib_nuclei_parser": "nuclei-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, Severity, countBySeverity(), NucleiMatch, nucleiMatchToFinding()] | lang=en
- "login_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/portal/login/page.tsx:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, 5c6aa54 feat(portal-ui): portal shell/p…, 81c81cb feat: implement outbox reclaim …] | lang=en
- "main_scripts_port_scanner": "port_scanner.py" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 2c53ae9 evasion(scanner): randomized sc…, 4733f24 evasion(scanner): --source-port…, 4d0377d Add unit tests for SMB scanner,…, 9c973dd feat(scanner): tarpit/honeypot …, ae08d19 feat(scanner): adaptive timeout…] | lang=en
- "models_agent_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/backend/app/models/agent.py:L12 | neighbors=[agent.py, str, Base, TimestampMixin, AgentRegisterRequest, AgentRegisterResponse] | lang=en
- "models_enums": "enums.py" | kind=code-symbol | source=manager/backend/app/models/enums.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Enum, AssetCriticality, AssetType, DetectionStatus] | lang=en
- "native_http_probe": "http-probe.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/http-probe.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractTitle(), fingerprint(), HttpProbeResult] | lang=en
- "routers_agents_agentregisterresponse": "AgentRegisterResponse" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L200 | neighbors=[agents.py, BaseModel, bootstrap_agent(), register_agent(), Asset, Engagement] | lang=en
- "routers_agents_enqueuejobrequest": "EnqueueJobRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L300 | neighbors=[agents.py, BaseModel, ._validate_intensity(), ._validate_uc(), Asset, Engagement] | lang=en
- "routers_ai_report_generaterequest": "GenerateRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L46 | neighbors=[ai_report.py, BaseModel, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath] | lang=en
- "routers_ai_report_rejectrequest": "RejectRequest" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L56 | neighbors=[ai_report.py, ReviewRequest, LLMReportGenerator, LLMUnavailableError, Asset, AttackPath] | lang=en
- "routers_exploits_approvalout": "ApprovalOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L86 | neighbors=[exploits.py, _approval_out(), BaseModel, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "routers_exploits_exploitresultout": "ExploitResultOut" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L69 | neighbors=[exploits.py, BaseModel, _result_out(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "routers_vuln_scans_rationale_1": "Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L1 | neighbors=[vuln_scans.py, Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_vuln_scans_rationale_279": "Run Nuclei and always leave its job in a truthful terminal state." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L279 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType] | lang=en
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, 37376de hardening(scanner): OPSEC de-si…, 4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _dec()] | lang=en
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=probe/scanner/web_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 37376de hardening(scanner): OPSEC de-si…, bce780a feat(probe): enumerate HTTP met…, d1b4dd3 trim frontend to 7 core pages; …, _fetch(), main()] | lang=en
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 72f68af feat(verification): expose veri…, 85e4537 feat(risk-rank): expose risk_ra…, 8ebc053 feat(risk-rank-ui): surface ver…, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "services_job_result_service": "job_result_service.py" | kind=code-symbol | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, cac022c Everything is done and verified…, _apply_device_profile()] | lang=en
- "str": "str" | kind=code-symbol | neighbors=[FindingState, SourceConfidence, AgentStatus, AssetCriticality, AssetType, DetectionStatus] | lang=en
- "tests_test_ad_assessment_fakeattr": "_FakeAttr" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L31 | neighbors=[test_ad_assessment.py, .__init__(), .__getitem__(), ADCSChecker, CertTemplate, ASREPRoastChecker] | lang=en
- "tests_test_agent_policy_roe": "_roe()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L30 | neighbors=[test_agent_policy.py, .test_decision_carries_action_and_tier(), .test_denylisted_module_denied(), .test_excluded_target_denied(), .test_exploit_attempt_cap_denied(), .test_halted_engagement_denies_everythi…] | lang=en
- "tests_test_agent_policy_testevaluateaction": "TestEvaluateAction" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L36 | neighbors=[test_agent_policy.py, .test_decision_carries_action_and_tier(), .test_denylisted_module_denied(), .test_excluded_target_denied(), .test_exploit_attempt_cap_denied(), .test_halted_engagement_denies_everythi…] | lang=en
- "tests_test_ai_engine_testvulnprioritizer": "TestVulnPrioritizer" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L47 | neighbors=[test_ai_engine.py, .setup_method(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_fallback_score_capped(), .test_higher_cvss_scores_higher()] | lang=en
- "tests_test_customer_access": "test_customer_access.py" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, c4386e4 feat(customers): operator Custo…, _added(), _mock_db(), _operator()] | lang=en
- "tests_test_detection_validation_rationale_1": "Unit tests for the detection validation engine (Prompt 7).  SIEM/EDR HTTP is moc" | kind=entity | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[test_detection_validation.py, AttackAction, DetectionCorrelator, DetectionGap, CrowdStrikeFalcon, EDRDetection] | lang=en
- "tests_test_exploit_engine_testmetasploitintegration": "TestMetasploitIntegration" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L419 | neighbors=[test_exploit_engine.py, Run against a live Metasploitable2 lab …, .skip_without_flag(), .test_connect_and_list_modules(), .test_run_safe_scanner_smb(), MetasploitRPCClient] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-011.json

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
